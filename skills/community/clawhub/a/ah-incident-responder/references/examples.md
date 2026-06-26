# Incident Responder — Code Examples

## Example 1

```python
# OpenTelemetry trace analysis
import json
from datetime import datetime, timedelta

def analyze_trace(trace_id):
    """Analyze distributed trace for bottlenecks"""
    spans = fetch_spans(trace_id)
    
    # Build span tree
    root = build_span_tree(spans)
    
    # Find critical path
    critical_path = find_critical_path(root)
    
    # Identify bottlenecks
    bottlenecks = []
    for span in critical_path:
        if span.duration > span.parent_p95:
            bottlenecks.append({
                'service': span.service,
                'operation': span.operation,
                'duration': span.duration,
                'expected_p95': span.parent_p95,
                'deviation': (span.duration / span.parent_p95 - 1) * 100
            })
    
    return {
        'trace_id': trace_id,
        'total_duration': root.duration,
        'span_count': len(spans),
        'service_count': len(set(s.service for s in spans)),
        'critical_path': critical_path,
        'bottlenecks': bottlenecks
    }

# Jaeger/Zipkin query
def query_slow_traces(service, operation, lookback_hours=1):
    query = {
        'service': service,
        'operation': operation,
        'start': datetime.now() - timedelta(hours=lookback_hours),
        'min_duration': '1s',
        'limit': 100
    }
    return jaeger_client.find_traces(query)
```

## Example 2

```sql
-- PostgreSQL slow query analysis
SELECT 
    query,
    calls,
    mean_exec_time,
    total_exec_time,
    stddev_exec_time
FROM pg_stat_statements
WHERE mean_exec_time > 1000
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Lock analysis
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks 
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
WHERE NOT blocked_locks.granted;

-- Connection pool analysis
SELECT 
    state,
    COUNT(*),
    MAX(now() - state_change) as max_duration
FROM pg_stat_activity
GROUP BY state;

-- Table bloat check
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    n_live_tup,
    n_dead_tup,
    round(n_dead_tup::numeric / NULLIF(n_live_tup + n_dead_tup, 0) * 100, 2) AS dead_percent
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

## Example 3

```python
#!/usr/bin/env python3
# Automated incident response orchestrator

import subprocess
import time
import json
from datetime import datetime
from typing import Dict, List

class IncidentResponder:
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.incident_id = self.generate_incident_id()
        self.start_time = datetime.utcnow()
        
    def diagnose_system(self) -> Dict:
        """Run comprehensive system diagnosis"""
        diagnostics = {
            'timestamp': datetime.utcnow().isoformat(),
            'incident_id': self.incident_id,
            'checks': {}
        }
        
        # Check system resources
        diagnostics['checks']['cpu'] = self.check_cpu()
        diagnostics['checks']['memory'] = self.check_memory()
        diagnostics['checks']['disk'] = self.check_disk()
        diagnostics['checks']['network'] = self.check_network()
        
        # Check application health
        diagnostics['checks']['services'] = self.check_services()
        diagnostics['checks']['endpoints'] = self.check_endpoints()
        
        # Check recent errors
        diagnostics['checks']['errors'] = self.analyze_error_logs()
        
        return diagnostics
    
    def check_cpu(self) -> Dict:
        """Check CPU usage and identify high-usage processes"""
        result = subprocess.run(
            ["top", "-b", "-n", "1"],
            capture_output=True,
            text=True
        )
        
        lines = result.stdout.split('\n')
        cpu_line = [l for l in lines if 'Cpu(s)' in l][0]
        
        # Parse top processes
        processes = []
        for line in lines[7:17]:  # Top 10 processes
            if line.strip():
                parts = line.split()
                processes.append({
                    'pid': parts[0],
                    'cpu': parts[8],
                    'mem': parts[9],
                    'command': parts[11]
                })
        
        return {
            'summary': cpu_line,
            'top_processes': processes,
            'status': 'critical' if float(processes[0]['cpu']) > 80 else 'ok'
        }
    
    def analyze_error_logs(self, lookback_minutes: int = 60) -> Dict:
        """Analyze error patterns in logs"""
        cmd = f"journalctl --since '{lookback_minutes} minutes ago' | grep -E 'ERROR|FATAL'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        errors = {}
        for line in result.stdout.split('\n'):
            if line:
                # Extract error type
                if 'ERROR' in line:
                    error_type = line.split('ERROR')[1].split()[0] if 'ERROR' in line else 'unknown'
                    errors[error_type] = errors.get(error_type, 0) + 1
        
        return {
            'error_counts': errors,
            'total_errors': sum(errors.values()),
            'unique_errors': len(errors),
            'top_errors': sorted(errors.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def auto_remediate(self, diagnostics: Dict) -> List[str]:
        """Attempt automatic remediation based on diagnostics"""
        actions_taken = []
        
        # High CPU - restart problematic services
        if diagnostics['checks']['cpu']['status'] == 'critical':
            for proc in diagnostics['checks']['cpu']['top_processes'][:3]:
                if float(proc['cpu']) > 90:
                    actions_taken.append(f"Restarted high-CPU process: {proc['command']}")
                    # subprocess.run([...])  # Actual restart command
        
        # Memory pressure - clear caches
        if diagnostics['checks']['memory'].get('usage_percent', 0) > 90:
            subprocess.run(["sync"], check=True)
            subprocess.run(["echo", "3", ">", "/proc/sys/vm/drop_caches"], shell=True)
            actions_taken.append("Cleared system caches due to memory pressure")
        
        # Disk space - clean up logs
        if diagnostics['checks']['disk'].get('usage_percent', 0) > 90:
            subprocess.run(["journalctl", "--vacuum-time=7d"], check=True)
            actions_taken.append("Cleaned up old logs to free disk space")
        
        return actions_taken

# Usage
responder = IncidentResponder('/etc/incident/config.yaml')
diagnostics = responder.diagnose_system()
actions = responder.auto_remediate(diagnostics)
```
