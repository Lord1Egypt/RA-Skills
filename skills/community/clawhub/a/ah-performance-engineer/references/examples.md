# Performance Engineer — Code Examples

## Example 1

```yaml
performance_pillars:
  latency:
    definition: "Time to process a single request"
    targets:
      - p50 < 100ms
      - p95 < 500ms
      - p99 < 1000ms
    optimization:
      - Reduce computation time
      - Optimize database queries
      - Implement caching
      - Use CDNs for static content
  
  throughput:
    definition: "Number of requests processed per unit time"
    targets:
      - RPS > 10000
      - Concurrent users > 5000
    optimization:
      - Horizontal scaling
      - Load balancing
      - Connection pooling
      - Async processing
  
  resource_utilization:
    definition: "Efficient use of system resources"
    targets:
      - CPU < 70%
      - Memory < 80%
      - Disk I/O < 80%
    optimization:
      - Code optimization
      - Memory management
      - I/O batching
      - Resource pooling
  
  scalability:
    definition: "Ability to handle increased load"
    metrics:
      - Linear scaling factor
      - Cost per transaction
    optimization:
      - Microservices architecture
      - Database sharding
      - Caching layers
      - Queue-based architecture
```

## Example 2

```python
# Python profiling example
import cProfile
import pstats
import line_profiler
import memory_profiler
from pyflame import flame_graph

class PerformanceProfiler:
    def __init__(self, app):
        self.app = app
        self.profiler = cProfile.Profile()
        
    def profile_cpu(self, func, *args, **kwargs):
        """CPU profiling with cProfile"""
        self.profiler.enable()
        result = func(*args, **kwargs)
        self.profiler.disable()
        
        stats = pstats.Stats(self.profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(20)  # Top 20 functions
        
        # Generate call graph
        stats.dump_stats('profile.stats')
        # gprof2dot -f pstats profile.stats | dot -Tpng -o profile.png
        
        return result
    
    @profile  # line_profiler decorator
    def profile_line_by_line(self, func):
        """Line-by-line profiling"""
        # kernprof -l -v script.py
        return func()
    
    @memory_profiler.profile
    def profile_memory(self, func):
        """Memory usage profiling"""
        # python -m memory_profiler script.py
        return func()
    
    def generate_flame_graph(self):
        """Generate flame graph for visualization"""
        # pyflame -s 60 -r 0.01 python script.py | flamegraph.pl > flame.svg
        pass

# Java profiling with async-profiler
class JavaProfiler:
    def start_profiling(self, pid):
        """
        ./profiler.sh start -e cpu -i 1ms -f profile.html $PID
        ./profiler.sh status $PID
        ./profiler.sh stop $PID
        """
        pass
    
    def heap_dump(self, pid):
        """
        jmap -dump:format=b,file=heap.hprof $PID
        jhat heap.hprof  # Analyze with jhat
        """
        pass
    
    def thread_dump(self, pid):
        """
        jstack $PID > thread_dump.txt
        # Or kill -3 $PID for thread dump in logs
        """
        pass
```

## Example 3

```python
# Locust load testing script
from locust import HttpUser, task, between
import random
import json

class APILoadTest(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Login and get auth token"""
        response = self.client.post("/auth/login", json={
            "username": f"user_{random.randint(1, 10000)}",
            "password": "testpass"
        })
        self.token = response.json()["token"]
        self.client.headers.update({"Authorization": f"Bearer {self.token}"})
    
    @task(3)
    def get_items(self):
        """Weight: 3 - Most common operation"""
        with self.client.get("/api/items", 
                            catch_response=True) as response:
            if response.elapsed.total_seconds() > 1:
                response.failure(f"Request took {response.elapsed.total_seconds()}s")
            elif response.status_code == 200:
                response.success()
    
    @task(2)
    def create_item(self):
        """Weight: 2 - Moderate frequency"""
        self.client.post("/api/items", json={
            "name": f"Item {random.randint(1, 1000)}",
            "price": random.uniform(10, 1000)
        })
    
    @task(1)
    def complex_query(self):
        """Weight: 1 - Heavy operation"""
        self.client.get("/api/analytics/report", params={
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "group_by": "category"
        })

# K6 load testing script
"""
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export let errorRate = new Rate('errors');

export let options = {
    stages: [
        { duration: '2m', target: 100 },  // Ramp up
        { duration: '5m', target: 100 },  // Stay at 100 users
        { duration: '2m', target: 200 },  // Spike to 200
        { duration: '5m', target: 200 },  // Stay at 200
        { duration: '2m', target: 0 },    // Ramp down
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'],  // 95% of requests under 500ms
        errors: ['rate<0.1'],              // Error rate under 10%
    },
};

export default function() {
    let response = http.get('https://api.example.com/endpoint');
    
    check(response, {
        'status is 200': (r) => r.status === 200,
        'response time < 500ms': (r) => r.timings.duration < 500,
    }) || errorRate.add(1);
    
    sleep(1);
}
"""
```

## Example 4

```sql
-- Query optimization techniques
-- 1. Use EXPLAIN ANALYZE
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT u.*, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > NOW() - INTERVAL '30 days'
GROUP BY u.id;

-- 2. Index optimization
-- Covering index for common query
CREATE INDEX CONCURRENTLY idx_orders_user_date_total 
ON orders(user_id, created_at) 
INCLUDE (total_amount, status);

-- Partial index for filtered queries
CREATE INDEX idx_active_users ON users(email) 
WHERE deleted_at IS NULL AND status = 'active';

-- 3. Query rewriting for performance
-- Instead of IN with subquery
SELECT * FROM orders WHERE user_id IN (
    SELECT id FROM users WHERE country = 'US'
);

-- Use EXISTS
SELECT o.* FROM orders o
WHERE EXISTS (
    SELECT 1 FROM users u 
    WHERE u.id = o.user_id AND u.country = 'US'
);

-- 4. Materialized views for complex aggregations
CREATE MATERIALIZED VIEW daily_sales_summary AS
SELECT 
    DATE(created_at) as sale_date,
    COUNT(*) as total_orders,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value
FROM orders
GROUP BY DATE(created_at)
WITH DATA;

CREATE UNIQUE INDEX ON daily_sales_summary(sale_date);

-- Refresh strategy
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales_summary;

-- 5. Partitioning large tables
CREATE TABLE orders_2024 PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- 6. Connection pooling configuration
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '4GB';
ALTER SYSTEM SET effective_cache_size = '12GB';
ALTER SYSTEM SET work_mem = '256MB';
```

## Example 5

```javascript
// React performance optimization
import { memo, useMemo, useCallback, lazy, Suspense } from 'react';
import { FixedSizeList as VirtualList } from 'react-window';

// 1. Code splitting with lazy loading
const HeavyComponent = lazy(() => 
  import(/* webpackChunkName: "heavy" */ './HeavyComponent')
);

// 2. Memoization for expensive computations
function DataGrid({ items, filters }) {
  const filteredItems = useMemo(() => {
    console.time('Filtering');
    const result = items.filter(item => 
      filters.every(filter => filter.test(item))
    );
    console.timeEnd('Filtering');
    return result;
  }, [items, filters]);
  
  // 3. Virtual scrolling for large lists
  const Row = memo(({ index, style }) => (
    <div style={style}>
      {filteredItems[index].name}
    </div>
  ));
  
  return (
    <VirtualList
      height={600}
      itemCount={filteredItems.length}
      itemSize={35}
      width="100%"
    >
      {Row}
    </VirtualList>
  );
}

// 4. Web Workers for heavy computations
const worker = new Worker(new URL('./worker.js', import.meta.url));

function processLargeDataset(data) {
  return new Promise((resolve) => {
    worker.postMessage({ cmd: 'process', data });
    worker.onmessage = (e) => resolve(e.data);
  });
}

// 5. Performance monitoring
const observer = new PerformanceObserver((list) => {
  list.getEntries().forEach((entry) => {
    // Log to analytics
    analytics.track('performance', {
      name: entry.name,
      duration: entry.duration,
      type: entry.entryType
    });
  });
});

observer.observe({ 
  entryTypes: ['navigation', 'resource', 'measure', 'mark'] 
});

// 6. Resource hints
<link rel="preconnect" href="https://api.example.com">
<link rel="dns-prefetch" href="https://cdn.example.com">
<link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
<link rel="prefetch" href="/next-page-data.json">
```

## Example 6

```bash
#!/bin/bash
# Linux performance tuning script

# 1. CPU Performance
# Set CPU governor to performance
for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
    echo performance > $cpu
done

# Disable CPU frequency scaling
echo 0 > /sys/devices/system/cpu/intel_pstate/no_turbo

# 2. Memory optimization
# Transparent Huge Pages
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag

# Swappiness (prefer RAM over swap)
echo 10 > /proc/sys/vm/swappiness

# 3. Network optimization
cat >> /etc/sysctl.conf << EOF
# Network performance tuning
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 134217728
net.ipv4.tcp_wmem = 4096 65536 134217728
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_congestion_control = bbr
net.ipv4.tcp_notsent_lowat = 16384
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 15
net.ipv4.tcp_keepalive_time = 300
net.ipv4.tcp_keepalive_probes = 5
net.ipv4.tcp_keepalive_intvl = 15
EOF

sysctl -p

# 4. Disk I/O optimization
# Set scheduler for SSDs
for disk in /sys/block/sd*/queue/scheduler; do
    echo noop > $disk
done

# Increase read-ahead
for disk in /sys/block/sd*/queue/read_ahead_kb; do
    echo 256 > $disk
done

# 5. File system tuning
# Increase file descriptors
echo "* soft nofile 65535" >> /etc/security/limits.conf
echo "* hard nofile 65535" >> /etc/security/limits.conf

# 6. JVM tuning for Java applications
export JAVA_OPTS="-server \
    -Xms4g -Xmx4g \
    -XX:+UseG1GC \
    -XX:MaxGCPauseMillis=200 \
    -XX:ParallelGCThreads=4 \
    -XX:ConcGCThreads=2 \
    -XX:+DisableExplicitGC \
    -XX:+HeapDumpOnOutOfMemoryError \
    -XX:HeapDumpPath=/var/log/app/ \
    -Djava.awt.headless=true \
    -Djava.security.egd=file:/dev/./urandom"
```

## Example 7

```python
# Prometheus metrics collection
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

# Define metrics
request_count = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
request_duration = Histogram('app_request_duration_seconds', 'Request duration', ['method', 'endpoint'])
active_connections = Gauge('app_active_connections', 'Active connections')
cache_hit_rate = Gauge('app_cache_hit_rate', 'Cache hit rate')

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        
    def record_request(self, method, endpoint, duration):
        request_count.labels(method=method, endpoint=endpoint).inc()
        request_duration.labels(method=method, endpoint=endpoint).observe(duration)
        
    def update_connections(self, count):
        active_connections.set(count)
        
    def calculate_percentiles(self, data, percentiles=[50, 95, 99]):
        """Calculate percentiles for performance data"""
        sorted_data = sorted(data)
        results = {}
        for p in percentiles:
            index = int(len(sorted_data) * p / 100)
            results[f'p{p}'] = sorted_data[min(index, len(sorted_data)-1)]
        return results
    
    def analyze_performance(self, metrics_data):
        """Analyze performance and identify bottlenecks"""
        analysis = {
            'timestamp': time.time(),
            'summary': {},
            'bottlenecks': [],
            'recommendations': []
        }
        
        # Analyze response times
        if metrics_data['response_times']:
            percentiles = self.calculate_percentiles(metrics_data['response_times'])
            analysis['summary']['response_times'] = percentiles
            
            if percentiles['p95'] > 1000:  # 1 second
                analysis['bottlenecks'].append({
                    'type': 'high_latency',
                    'value': percentiles['p95'],
                    'severity': 'high'
                })
                analysis['recommendations'].append(
                    'Consider implementing caching or optimizing database queries'
                )
        
        # Analyze error rates
        error_rate = metrics_data.get('error_count', 0) / max(metrics_data.get('total_requests', 1), 1)
        if error_rate > 0.01:  # 1% error rate
            analysis['bottlenecks'].append({
                'type': 'high_error_rate',
                'value': error_rate,
                'severity': 'critical'
            })
            analysis['recommendations'].append(
                'Investigate error logs and implement retry mechanisms'
            )
        
        return analysis

# Grafana dashboard query examples
grafana_queries = {
    'request_rate': 'rate(app_requests_total[5m])',
    'error_rate': 'rate(app_requests_total{status=~"5.."}[5m])',
    'p95_latency': 'histogram_quantile(0.95, rate(app_request_duration_seconds_bucket[5m]))',
    'memory_usage': 'process_resident_memory_bytes / 1024 / 1024',
    'cpu_usage': 'rate(process_cpu_seconds_total[5m]) * 100'
}
```

## Example 8

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

class CapacityPlanner:
    def __init__(self, historical_data):
        self.data = historical_data
        
    def predict_growth(self, days_ahead=30):
        """Predict resource needs based on historical growth"""
        # Extract time series data
        timestamps = np.array([d['timestamp'] for d in self.data]).reshape(-1, 1)
        metrics = {
            'cpu': np.array([d['cpu'] for d in self.data]),
            'memory': np.array([d['memory'] for d in self.data]),
            'requests': np.array([d['requests'] for d in self.data])
        }
        
        predictions = {}
        for metric_name, values in metrics.items():
            # Fit linear regression
            model = LinearRegression()
            model.fit(timestamps, values)
            
            # Predict future values
            future_timestamp = timestamps[-1][0] + (86400 * days_ahead)
            predicted_value = model.predict([[future_timestamp]])[0]
            
            # Calculate growth rate
            current_value = values[-1]
            growth_rate = (predicted_value - current_value) / current_value
            
            predictions[metric_name] = {
                'current': current_value,
                'predicted': predicted_value,
                'growth_rate': growth_rate,
                'recommendation': self.get_recommendation(metric_name, predicted_value)
            }
        
        return predictions
    
    def get_recommendation(self, metric, predicted_value):
        thresholds = {
            'cpu': {'warning': 70, 'critical': 85},
            'memory': {'warning': 75, 'critical': 90},
            'requests': {'warning': 80000, 'critical': 100000}
        }
        
        if metric in thresholds:
            if predicted_value > thresholds[metric]['critical']:
                return f"CRITICAL: Add capacity immediately for {metric}"
            elif predicted_value > thresholds[metric]['warning']:
                return f"WARNING: Plan capacity increase for {metric}"
        
        return "Capacity adequate"
    
    def calculate_cost_optimization(self, current_resources, utilization):
        """Calculate potential cost savings from right-sizing"""
        savings = []
        
        for resource in current_resources:
            if utilization[resource['id']] < 30:
                savings.append({
                    'resource': resource['id'],
                    'current_size': resource['size'],
                    'recommended_size': resource['size'] // 2,
                    'monthly_savings': resource['monthly_cost'] * 0.5
                })
            elif utilization[resource['id']] < 50:
                savings.append({
                    'resource': resource['id'],
                    'current_size': resource['size'],
                    'recommended_size': resource['size'] * 0.75,
                    'monthly_savings': resource['monthly_cost'] * 0.25
                })
        
        return {
            'total_monthly_savings': sum(s['monthly_savings'] for s in savings),
            'recommendations': savings
        }
```
