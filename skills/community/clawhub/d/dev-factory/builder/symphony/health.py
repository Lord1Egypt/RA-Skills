"""Health Check Server for Symphony

Provides HTTP endpoint for monitoring daemon status.
Returns metrics: active tasks, concurrency usage, retry queue size.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Optional

try:
    from aiohttp import web
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False
    web = None

logger = logging.getLogger('builder-agent.symphony.health')


class HealthCheckServer:
    """Health check HTTP server

    Provides endpoints:
    - GET /health - Health status and statistics
    - GET /metrics - Prometheus-style metrics
    - GET /ready - Readiness probe
    """

    def __init__(self, orchestrator, port: int = 8080, host: str = "0.0.0.0"):
        """Initialize health check server

        Args:
            orchestrator: SymphonyOrchestrator instance
            port: Port to listen on
            host: Host to bind to
        """
        if not HAS_AIOHTTP:
            raise ImportError("aiohttp is required for health check server")

        self.orchestrator = orchestrator
        self.port = port
        self.host = host
        self.app = web.Application()
        self.runner = None
        self.site = None

        # Setup routes
        self.app.router.add_get('/health', self.health_handler)
        self.app.router.add_get('/metrics', self.metrics_handler)
        self.app.router.add_get('/ready', self.ready_handler)
        self.app.router.add_get('/', self.root_handler)

        logger.info("Health check server configured: %s:%d", host, port)

    async def start(self):
        """Start the health check server"""
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()

        self.site = web.TCPSite(self.runner, self.host, self.port)
        await self.site.start()

        logger.info("Health check server started: http://%s:%d", self.host, self.port)

    async def stop(self):
        """Stop the health check server"""
        if self.site:
            await self.site.stop()
            logger.info("Health check server stopped")

        if self.runner:
            await self.runner.cleanup()

    async def root_handler(self, request):
        """Root endpoint"""
        return web.json_response({
            'service': 'dev-factory-symphony',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat(),
            'endpoints': [
                '/health',
                '/metrics',
                '/ready'
            ]
        })

    async def health_handler(self, request):
        """Health check endpoint

        Returns overall health status and statistics
        """
        stats = self.orchestrator.get_statistics()

        # Determine health status
        is_healthy = True
        health_issues = []

        # Check for stale tasks
        if stats['state_machine']['stale_tasks'] > 0:
            is_healthy = False
            health_issues.append(f"{stats['state_machine']['stale_tasks']} stale tasks")

        # Check for large retry queue
        if stats['state_machine']['retry_queue_size'] > 10:
            is_healthy = False
            health_issues.append(f"{stats['state_machine']['retry_queue_size']} tasks in retry queue")

        # Check concurrency
        utilization = stats['concurrency']['utilization_percent']
        if utilization > 95:
            health_issues.append(f"High concurrency utilization: {utilization:.1f}%")

        response = {
            'status': 'healthy' if is_healthy else 'degraded',
            'timestamp': datetime.now().isoformat(),
            'orchestrator': {
                'running': stats['running'],
            },
            'tasks': {
                'total': stats['state_machine']['total_tasks'],
                'active': stats['state_machine']['active_tasks'],
                'stale': stats['state_machine']['stale_tasks'],
                'retry_queue': stats['state_machine']['retry_queue_size'],
                'by_state': stats['state_machine']['by_state'],
            },
            'concurrency': {
                'active': stats['concurrency']['active_tasks'],
                'max': stats['concurrency']['max_concurrent_builds'],
                'available': stats['concurrency']['available_slots'],
                'utilization_percent': stats['concurrency']['utilization_percent'],
            },
            'workspace': {
                'total_workspaces': stats['workspace']['total_workspaces'],
                'total_size_mb': stats['workspace']['total_size_mb'],
                'base_dir': stats['workspace']['base_dir'],
            },
        }

        if health_issues:
            response['issues'] = health_issues

        status_code = 200 if is_healthy else 503
        return web.json_response(response, status=status_code)

    async def metrics_handler(self, request):
        """Prometheus-style metrics endpoint

        Returns metrics in Prometheus text format
        """
        stats = self.orchestrator.get_statistics()

        metrics = []

        # Task metrics
        metrics.append("# TYPE dev_factory_tasks_total gauge")
        metrics.append(f"dev_factory_tasks_total {stats['state_machine']['total_tasks']}")

        metrics.append("# TYPE dev_factory_tasks_active gauge")
        metrics.append(f"dev_factory_tasks_active {stats['state_machine']['active_tasks']}")

        metrics.append("# TYPE dev_factory_tasks_stale gauge")
        metrics.append(f"dev_factory_tasks_stale {stats['state_machine']['stale_tasks']}")

        metrics.append("# TYPE dev_factory_tasks_retry_queue gauge")
        metrics.append(f"dev_factory_tasks_retry_queue {stats['state_machine']['retry_queue_size']}")

        # Task state metrics
        for state, count in stats['state_machine']['by_state'].items():
            safe_state = state.replace('-', '_')
            metrics.append(f"dev_factory_tasks_by_state{{state=\"{safe_state}\"}} {count}")

        # Concurrency metrics
        metrics.append("# TYPE dev_factory_concurrency_active gauge")
        metrics.append(f"dev_factory_concurrency_active {stats['concurrency']['active_tasks']}")

        metrics.append("# TYPE dev_factory_concurrency_max gauge")
        metrics.append(f"dev_factory_concurrency_max {stats['concurrency']['max_concurrent_builds']}")

        metrics.append("# TYPE dev_factory_concurrency_utilization gauge")
        metrics.append(f"dev_factory_concurrency_utilization {stats['concurrency']['utilization_percent']}")

        # Workspace metrics
        metrics.append("# TYPE dev_factory_workspaces_total gauge")
        metrics.append(f"dev_factory_workspaces_total {stats['workspace']['total_workspaces']}")

        metrics.append("# TYPE dev_factory_workspaces_size_bytes gauge")
        metrics.append(f"dev_factory_workspaces_size_bytes {stats['workspace']['total_size_bytes']}")

        # Orchestrator status
        metrics.append("# TYPE dev_factory_orchestrator_running gauge")
        metrics.append(f"dev_factory_orchestrator_running {1 if stats['running'] else 0}")

        return web.Response(text='\n'.join(metrics), content_type='text/plain')

    async def ready_handler(self, request):
        """Readiness probe endpoint

        Returns 200 if orchestrator is ready to accept tasks
        """
        stats = self.orchestrator.get_statistics()

        is_ready = (
            stats['running'] and
            stats['concurrency']['available_slots'] > 0
        )

        if is_ready:
            return web.json_response({
                'status': 'ready',
                'timestamp': datetime.now().isoformat(),
                'available_slots': stats['concurrency']['available_slots'],
            })
        else:
            return web.json_response({
                'status': 'not_ready',
                'timestamp': datetime.now().isoformat(),
                'reason': 'not_running' if not stats['running'] else 'at_capacity',
            }, status=503)


class SimpleHealthChecker:
    """Simple health checker without HTTP server

    Can be used when aiohttp is not available
    """

    def __init__(self, orchestrator):
        """Initialize health checker

        Args:
            orchestrator: SymphonyOrchestrator instance
        """
        self.orchestrator = orchestrator

    def get_health_status(self) -> Dict:
        """Get health status

        Returns:
            Health status dictionary
        """
        stats = self.orchestrator.get_statistics()

        is_healthy = (
            stats['running'] and
            stats['state_machine']['stale_tasks'] == 0 and
            stats['concurrency']['utilization_percent'] < 95
        )

        return {
            'status': 'healthy' if is_healthy else 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'statistics': stats,
        }

    def print_health_status(self):
        """Print health status to console"""
        status = self.get_health_status()

        print("=" * 60)
        print(f"Dev-Factory Symphony Health Status: {status['status'].upper()}")
        print(f"Timestamp: {status['timestamp']}")
        print("=" * 60)

        stats = status['statistics']

        print("\nOrchestrator:")
        print(f"  Running: {stats['running']}")

        print("\nTasks:")
        print(f"  Total: {stats['state_machine']['total_tasks']}")
        print(f"  Active: {stats['state_machine']['active_tasks']}")
        print(f"  Stale: {stats['state_machine']['stale_tasks']}")
        print(f"  Retry Queue: {stats['state_machine']['retry_queue_size']}")

        print("\nConcurrency:")
        print(f"  Active: {stats['concurrency']['active_tasks']}/{stats['concurrency']['max_concurrent_builds']}")
        print(f"  Available: {stats['concurrency']['available_slots']}")
        print(f"  Utilization: {stats['concurrency']['utilization_percent']:.1f}%")

        print("\nWorkspace:")
        print(f"  Total: {stats['workspace']['total_workspaces']}")
        print(f"  Size: {stats['workspace']['total_size_mb']:.2f} MB")

        print("=" * 60)


def create_health_checker(orchestrator, use_http: bool = True,
                         port: int = 8080):
    """Create health checker (HTTP or simple)

    Args:
        orchestrator: SymphonyOrchestrator instance
        use_http: Whether to use HTTP server
        port: Port for HTTP server

    Returns:
        Health checker instance
    """
    if use_http and HAS_AIOHTTP:
        return HealthCheckServer(orchestrator, port=port)
    else:
        if use_http and not HAS_AIOHTTP:
            logger.warning("aiohttp not available, using simple health checker")

        return SimpleHealthChecker(orchestrator)
