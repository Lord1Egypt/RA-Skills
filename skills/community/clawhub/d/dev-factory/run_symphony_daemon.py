#!/usr/bin/env python3
"""Run dev-factory in Symphony daemon mode

This script starts the long-running daemon that:
1. Polls Notion for new tasks
2. Manages parallel build processing
3. Handles retries with exponential backoff
4. Provides health check endpoint
"""

import argparse
import asyncio
import logging
import signal
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from builder.symphony.orchestrator import SymphonyOrchestrator
from builder.symphony.health import HealthCheckServer
from config import load_config, setup_logging


logger = logging.getLogger('builder-agent.daemon')


class SymphonyDaemon:
    """Symphony daemon runner"""

    def __init__(self, config, enable_health_server: bool = True,
                 health_port: int = 8080):
        """Initialize daemon

        Args:
            config: Dev-factory configuration
            enable_health_server: Enable health check server
            health_port: Port for health check server
        """
        self.config = config
        self.enable_health_server = enable_health_server
        self.health_port = health_port

        # Initialize orchestrator
        self.orchestrator = SymphonyOrchestrator(config)

        # Health check server
        self.health_server = None
        if self.enable_health_server:
            self.health_server = HealthCheckServer(
                self.orchestrator,
                port=health_port
            )

        # Shutdown flag
        self.shutdown_requested = False

        # Setup signal handlers
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info("Received signal %d, initiating shutdown...", signum)
            self.shutdown_requested = True
            self.orchestrator.stop()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    async def run(self):
        """Run the daemon"""
        logger.info("Starting Symphony daemon...")
        logger.info("Configuration:")
        logger.info("  - Poll interval: %ds", self.orchestrator.poll_interval)
        logger.info("  - Stall timeout: %ds", self.orchestrator.stall_timeout)
        logger.info("  - Max concurrent builds: %d",
                   self.config.features.parallel_builds and 3 or 1)

        # Start health check server
        if self.health_server:
            await self.health_server.start()
            logger.info("Health check server started on port %d", self.health_port)

        try:
            # Run orchestrator daemon loop
            await self.orchestrator.run_daemon()

        except Exception as e:
            logger.error("Daemon error: %s", e)
            raise

        finally:
            # Stop health check server
            if self.health_server:
                await self.health_server.stop()
                logger.info("Health check server stopped")

            logger.info("Symphony daemon stopped")

    def print_statistics(self):
        """Print orchestrator statistics"""
        stats = self.orchestrator.get_statistics()

        logger.info("=" * 50)
        logger.info("Orchestrator Statistics")
        logger.info("=" * 50)

        # State machine stats
        sm_stats = stats['state_machine']
        logger.info("State Machine:")
        logger.info("  Total tasks: %d", sm_stats['total_tasks'])
        logger.info("  By state:")
        for state, count in sm_stats['by_state'].items():
            logger.info("    %s: %d", state, count)
        logger.info("  Active tasks: %d", sm_stats['active_tasks'])
        logger.info("  Stale tasks: %d", sm_stats['stale_tasks'])
        logger.info("  Retry queue: %d", sm_stats['retry_queue_size'])

        # Concurrency stats
        cc_stats = stats['concurrency']
        logger.info("Concurrency:")
        logger.info("  Active: %d/%d", cc_stats['active_tasks'],
                   cc_stats['max_concurrent_builds'])
        logger.info("  Available slots: %d", cc_stats['available_slots'])
        logger.info("  Utilization: %.2f%%", cc_stats['utilization_percent'])

        # Workspace stats
        ws_stats = stats['workspace']
        logger.info("Workspace:")
        logger.info("  Total workspaces: %d", ws_stats['total_workspaces'])
        logger.info("  Total size: %.2f MB", ws_stats['total_size_mb'])

        logger.info("=" * 50)


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Run dev-factory in Symphony daemon mode"
    )
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to config file'
    )
    parser.add_argument(
        '--no-health-server',
        action='store_true',
        help='Disable health check server'
    )
    parser.add_argument(
        '--health-port',
        type=int,
        default=8080,
        help='Port for health check server (default: 8080)'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Log level (default: INFO)'
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Override log level if specified
    if args.log_level:
        config.logging.level = args.log_level

    # Setup logging
    logger = setup_logging(config)
    logger.info("Dev-Factory Symphony Daemon v1.0")

    # Create and run daemon
    daemon = SymphonyDaemon(
        config,
        enable_health_server=not args.no_health_server,
        health_port=args.health_port
    )

    try:
        await daemon.run()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error("Fatal error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
