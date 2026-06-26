# Performance Tester — Code Examples

## Example 1

```javascript
// k6/config/test-config.js
export const config = {
  scenarios: {
    smoke_test: {
      executor: 'constant-vus',
      vus: 1,
      duration: '30s',
      tags: { test_type: 'smoke' }
    },
    load_test: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 10 },
        { duration: '5m', target: 10 },
        { duration: '2m', target: 20 },
        { duration: '5m', target: 20 },
        { duration: '2m', target: 0 }
      ],
      tags: { test_type: 'load' }
    },
    stress_test: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 20 },
        { duration: '5m', target: 20 },
        { duration: '2m', target: 50 },
        { duration: '5m', target: 50 },
        { duration: '2m', target: 100 },
        { duration: '5m', target: 100 },
        { duration: '10m', target: 0 }
      ],
      tags: { test_type: 'stress' }
    },
    spike_test: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '10s', target: 100 },
        { duration: '1m', target: 100 },
        { duration: '10s', target: 1400 },
        { duration: '3m', target: 1400 },
        { duration: '10s', target: 100 },
        { duration: '3m', target: 100 },
        { duration: '10s', target: 0 }
      ],
      tags: { test_type: 'spike' }
    }
  },
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests under 500ms
    http_req_failed: ['rate<0.1'],    // Error rate under 10%
    http_reqs: ['rate>100']           // At least 100 RPS
  }
};

// k6/utils/auth.js
import http from 'k6/http';
import { check } from 'k6';

export function authenticate(baseUrl, credentials) {
  const loginResponse = http.post(`${baseUrl}/api/auth/login`, {
    email: credentials.email,
    password: credentials.password
  }, {
    headers: { 'Content-Type': 'application/json' }
  });

  check(loginResponse, {
    'login successful': (r) => r.status === 200,
    'token received': (r) => r.json('token') !== undefined
  });

  return loginResponse.json('token');
}

export function getAuthHeaders(token) {
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  };
}

// k6/scenarios/user-journey.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { authenticate, getAuthHeaders } from '../utils/auth.js';
import { generateTestData } from '../utils/test-data.js';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';

export let options = {
  scenarios: {
    user_journey: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '1m', target: 5 },
        { duration: '3m', target: 5 },
        { duration: '1m', target: 10 },
        { duration: '3m', target: 10 },
        { duration: '1m', target: 0 }
      ]
    }
  },
  thresholds: {
    'http_req_duration{scenario:user_journey}': ['p(95)<1000'],
    'http_req_failed{scenario:user_journey}': ['rate<0.05'],
    'user_journey_duration': ['p(95)<30000'] // Complete journey under 30s
  }
};

export default function() {
  const startTime = new Date();
  
  // 1. Login
  const token = authenticate(BASE_URL, {
    email: `user${__VU}@example.com`,
    password: 'password123'
  });
  
  const headers = getAuthHeaders(token);
  sleep(1);

  // 2. Browse products
  const productsResponse = http.get(`${BASE_URL}/api/products`, { headers });
  check(productsResponse, {
    'products loaded': (r) => r.status === 200,
    'products count > 0': (r) => r.json('data').length > 0
  });
  sleep(2);

  // 3. View product details
  const products = productsResponse.json('data');
  const randomProduct = products[Math.floor(Math.random() * products.length)];
  
  const productResponse = http.get(`${BASE_URL}/api/products/${randomProduct.id}`, { headers });
  check(productResponse, {
    'product details loaded': (r) => r.status === 200
  });
  sleep(3);

  // 4. Add to cart
  const cartResponse = http.post(`${BASE_URL}/api/cart/items`, 
    JSON.stringify({
      productId: randomProduct.id,
      quantity: Math.floor(Math.random() * 3) + 1
    }), 
    { headers }
  );
  check(cartResponse, {
    'item added to cart': (r) => r.status === 201
  });
  sleep(1);

  // 5. View cart
  const cartViewResponse = http.get(`${BASE_URL}/api/cart`, { headers });
  check(cartViewResponse, {
    'cart loaded': (r) => r.status === 200,
    'cart has items': (r) => r.json('items').length > 0
  });
  sleep(2);

  // 6. Checkout process
  const checkoutData = generateTestData.checkoutInfo();
  const checkoutResponse = http.post(`${BASE_URL}/api/checkout`, 
    JSON.stringify(checkoutData), 
    { headers }
  );
  check(checkoutResponse, {
    'checkout successful': (r) => r.status === 200,
    'order created': (r) => r.json('orderId') !== undefined
  });

  // Record journey duration
  const journeyDuration = new Date() - startTime;
  console.log(`User journey completed in ${journeyDuration}ms`);
  
  sleep(1);
}

// k6/utils/test-data.js
export const generateTestData = {
  user() {
    return {
      email: `user${Math.random().toString(36).substr(2, 9)}@example.com`,
      password: 'password123',
      firstName: 'Test',
      lastName: 'User'
    };
  },

  product() {
    return {
      name: `Product ${Math.random().toString(36).substr(2, 9)}`,
      description: 'Test product description',
      price: Math.floor(Math.random() * 100) + 10,
      category: 'electronics'
    };
  },

  checkoutInfo() {
    return {
      shippingAddress: {
        street: '123 Test St',
        city: 'Test City',
        state: 'TS',
        zipCode: '12345',
        country: 'US'
      },
      paymentMethod: {
        type: 'credit_card',
        cardNumber: '4111111111111111',
        expiryDate: '12/25',
        cvv: '123'
      }
    };
  }
};
```

## Example 2

```xml
<!-- jmeter/api-load-test.jmx -->
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="API Load Test">
      <stringProp name="TestPlan.comments">Comprehensive API load testing</stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.arguments" elementType="Arguments" guiclass="ArgumentsPanel">
        <collectionProp name="Arguments.arguments">
          <elementProp name="base_url" elementType="Argument">
            <stringProp name="Argument.name">base_url</stringProp>
            <stringProp name="Argument.value">${__P(base_url,http://localhost:3000)}</stringProp>
          </elementProp>
          <elementProp name="users" elementType="Argument">
            <stringProp name="Argument.name">users</stringProp>
            <stringProp name="Argument.value">${__P(users,10)}</stringProp>
          </elementProp>
          <elementProp name="ramp_time" elementType="Argument">
            <stringProp name="Argument.name">ramp_time</stringProp>
            <stringProp name="Argument.value">${__P(ramp_time,60)}</stringProp>
          </elementProp>
          <elementProp name="duration" elementType="Argument">
            <stringProp name="Argument.name">duration</stringProp>
            <stringProp name="Argument.value">${__P(duration,300)}</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
    </TestPlan>
    
    <hashTree>
      <!-- Thread Group for Load Testing -->
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="Load Test Users">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">-1</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">${users}</stringProp>
        <stringProp name="ThreadGroup.ramp_time">${ramp_time}</stringProp>
        <longProp name="ThreadGroup.start_time">1640995200000</longProp>
        <longProp name="ThreadGroup.end_time">1640995200000</longProp>
        <boolProp name="ThreadGroup.scheduler">true</boolProp>
        <stringProp name="ThreadGroup.duration">${duration}</stringProp>
        <stringProp name="ThreadGroup.delay"></stringProp>
      </ThreadGroup>
      
      <hashTree>
        <!-- HTTP Request Defaults -->
        <ConfigTestElement guiclass="HttpDefaultsGui" testclass="ConfigTestElement" testname="HTTP Request Defaults">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
            <collectionProp name="Arguments.arguments"></collectionProp>
          </elementProp>
          <stringProp name="HTTPSampler.domain">${__javaScript(${base_url}.replace(/https?:\/\//, '').split('/')[0])}</stringProp>
          <stringProp name="HTTPSampler.port"></stringProp>
          <stringProp name="HTTPSampler.protocol">${__javaScript(${base_url}.startsWith('https') ? 'https' : 'http')}</stringProp>
          <stringProp name="HTTPSampler.contentEncoding"></stringProp>
          <stringProp name="HTTPSampler.path"></stringProp>
        </ConfigTestElement>
        
        <!-- Cookie Manager -->
        <CookieManager guiclass="CookiePanel" testclass="CookieManager" testname="HTTP Cookie Manager">
          <collectionProp name="CookieManager.cookies"></collectionProp>
          <boolProp name="CookieManager.clearEachIteration">false</boolProp>
        </CookieManager>
        
        <!-- Login Request -->
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="Login">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
            <collectionProp name="Arguments.arguments">
              <elementProp name="" elementType="HTTPArgument">
                <boolProp name="HTTPArgument.always_encode">false</boolProp>
                <stringProp name="Argument.value">{"email":"user${__threadNum}@example.com","password":"password123"}</stringProp>
                <stringProp name="Argument.metadata">=</stringProp>
              </elementProp>
            </collectionProp>
          </elementProp>
          <stringProp name="HTTPSampler.domain"></stringProp>
          <stringProp name="HTTPSampler.port"></stringProp>
          <stringProp name="HTTPSampler.protocol"></stringProp>
          <stringProp name="HTTPSampler.contentEncoding"></stringProp>
          <stringProp name="HTTPSampler.path">/api/auth/login</stringProp>
          <stringProp name="HTTPSampler.method">POST</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout"></stringProp>
          <stringProp name="HTTPSampler.response_timeout"></stringProp>
        </HTTPSamplerProxy>
        
        <!-- JSON Extractor for Auth Token -->
        <hashTree>
          <JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor" testname="Extract Auth Token">
            <stringProp name="JSONPostProcessor.referenceNames">auth_token</stringProp>
            <stringProp name="JSONPostProcessor.jsonPathExprs">$.token</stringProp>
            <stringProp name="JSONPostProcessor.match_numbers"></stringProp>
            <stringProp name="JSONPostProcessor.defaultValues">NOTFOUND</stringProp>
          </JSONPostProcessor>
        </hashTree>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

## Example 3

```sql
-- postgres/performance-test-setup.sql
-- Create test tables with realistic data volumes
CREATE TABLE IF NOT EXISTS users_perf_test (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders_perf_test (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users_perf_test(id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items_perf_test (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders_perf_test(id),
    product_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Generate test data
INSERT INTO users_perf_test (email, first_name, last_name)
SELECT 
    'user' || generate_series || '@example.com',
    'FirstName' || generate_series,
    'LastName' || generate_series
FROM generate_series(1, 100000);

-- Insert orders (average 5 orders per user)
INSERT INTO orders_perf_test (user_id, order_date, total_amount, status)
SELECT 
    (random() * 99999 + 1)::INTEGER,
    CURRENT_TIMESTAMP - (random() * INTERVAL '365 days'),
    (random() * 1000 + 10)::DECIMAL(10,2),
    CASE 
        WHEN random() < 0.8 THEN 'completed'
        WHEN random() < 0.9 THEN 'pending'
        ELSE 'cancelled'
    END
FROM generate_series(1, 500000);

-- Insert order items (average 3 items per order)
INSERT INTO order_items_perf_test (order_id, product_id, quantity, unit_price)
SELECT 
    (random() * 499999 + 1)::INTEGER,
    (random() * 10000 + 1)::INTEGER,
    (random() * 5 + 1)::INTEGER,
    (random() * 100 + 5)::DECIMAL(10,2)
FROM generate_series(1, 1500000);

-- Create indexes for performance testing
CREATE INDEX idx_users_email ON users_perf_test(email);
CREATE INDEX idx_orders_user_id ON orders_perf_test(user_id);
CREATE INDEX idx_orders_date ON orders_perf_test(order_date);
CREATE INDEX idx_orders_status ON orders_perf_test(status);
CREATE INDEX idx_order_items_order_id ON order_items_perf_test(order_id);
CREATE INDEX idx_order_items_product_id ON order_items_perf_test(product_id);

-- Update table statistics
ANALYZE users_perf_test;
ANALYZE orders_perf_test;
ANALYZE order_items_perf_test;
```

## Example 4

```bash
#!/bin/bash
# scripts/database-performance-test.sh

# Database performance testing script using pgbench

DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-testdb}
DB_USER=${DB_USER:-testuser}
DB_PASSWORD=${DB_PASSWORD:-testpass}

# Performance test configurations
CLIENTS=(1 5 10 25 50 100)
DURATION=300  # 5 minutes per test
SCALE_FACTOR=100

echo "Starting database performance tests..."

# Initialize pgbench
echo "Initializing pgbench with scale factor $SCALE_FACTOR..."
pgbench -i -s $SCALE_FACTOR -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME

# Custom test scripts
cat > custom_readonly.sql << EOF
\set aid random(1, 100000 * :scale)
SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
EOF

cat > custom_writeonly.sql << EOF
\set aid random(1, 100000 * :scale)
\set delta random(-5000, 5000)
UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;
EOF

cat > custom_mixed.sql << EOF
\set aid random(1, 100000 * :scale)
\set delta random(-5000, 5000)
BEGIN;
SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;
COMMIT;
EOF

# Run performance tests
for clients in "${CLIENTS[@]}"; do
    echo "Running tests with $clients concurrent clients..."
    
    # Read-only test
    echo "  Read-only test..."
    pgbench -c $clients -j $(nproc) -T $DURATION -S -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME \
        > results/readonly_${clients}_clients.log 2>&1
    
    # Write-only test
    echo "  Write-only test..."
    pgbench -c $clients -j $(nproc) -T $DURATION -f custom_writeonly.sql -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME \
        > results/writeonly_${clients}_clients.log 2>&1
    
    # Mixed workload test
    echo "  Mixed workload test..."
    pgbench -c $clients -j $(nproc) -T $DURATION -f custom_mixed.sql -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME \
        > results/mixed_${clients}_clients.log 2>&1
    
    # Standard TPC-B test
    echo "  Standard TPC-B test..."
    pgbench -c $clients -j $(nproc) -T $DURATION -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME \
        > results/tpcb_${clients}_clients.log 2>&1
    
    echo "  Completed tests for $clients clients"
done

# Generate performance report
python3 scripts/analyze_pgbench_results.py results/
```

## Example 5

```python
# scripts/performance-monitor.py
import psutil
import time
import json
import requests
import logging
from datetime import datetime
import threading
import queue

class PerformanceMonitor:
    def __init__(self, interval=5):
        self.interval = interval
        self.running = False
        self.metrics_queue = queue.Queue()
        
    def start_monitoring(self):
        """Start performance monitoring in background"""
        self.running = True
        
        # Start system metrics collection
        system_thread = threading.Thread(target=self._collect_system_metrics)
        system_thread.daemon = True
        system_thread.start()
        
        # Start application metrics collection
        app_thread = threading.Thread(target=self._collect_app_metrics)
        app_thread.daemon = True
        app_thread.start()
        
        return system_thread, app_thread
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.running = False
    
    def _collect_system_metrics(self):
        """Collect system-level performance metrics"""
        while self.running:
            try:
                # CPU metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_count = psutil.cpu_count()
                cpu_freq = psutil.cpu_freq()
                
                # Memory metrics
                memory = psutil.virtual_memory()
                swap = psutil.swap_memory()
                
                # Disk metrics
                disk_usage = psutil.disk_usage('/')
                disk_io = psutil.disk_io_counters()
                
                # Network metrics
                network_io = psutil.net_io_counters()
                
                metrics = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'type': 'system',
                    'cpu': {
                        'percent': cpu_percent,
                        'count': cpu_count,
                        'frequency': cpu_freq.current if cpu_freq else None
                    },
                    'memory': {
                        'total': memory.total,
                        'available': memory.available,
                        'percent': memory.percent,
                        'used': memory.used,
                        'free': memory.free
                    },
                    'swap': {
                        'total': swap.total,
                        'used': swap.used,
                        'free': swap.free,
                        'percent': swap.percent
                    },
                    'disk': {
                        'total': disk_usage.total,
                        'used': disk_usage.used,
                        'free': disk_usage.free,
                        'percent': disk_usage.percent,
                        'read_bytes': disk_io.read_bytes if disk_io else 0,
                        'write_bytes': disk_io.write_bytes if disk_io else 0
                    },
                    'network': {
                        'bytes_sent': network_io.bytes_sent,
                        'bytes_recv': network_io.bytes_recv,
                        'packets_sent': network_io.packets_sent,
                        'packets_recv': network_io.packets_recv
                    }
                }
                
                self.metrics_queue.put(metrics)
                
            except Exception as e:
                logging.error(f"Error collecting system metrics: {e}")
            
            time.sleep(self.interval)
    
    def _collect_app_metrics(self):
        """Collect application-specific metrics"""
        while self.running:
            try:
                # Application metrics endpoint
                response = requests.get('http://localhost:3000/metrics', timeout=5)
                
                if response.status_code == 200:
                    app_metrics = response.json()
                    
                    metrics = {
                        'timestamp': datetime.utcnow().isoformat(),
                        'type': 'application',
                        'metrics': app_metrics
                    }
                    
                    self.metrics_queue.put(metrics)
                
            except Exception as e:
                logging.error(f"Error collecting application metrics: {e}")
            
            time.sleep(self.interval)
    
    def get_metrics(self):
        """Get collected metrics"""
        metrics = []
        while not self.metrics_queue.empty():
            metrics.append(self.metrics_queue.get())
        return metrics
    
    def save_metrics_to_file(self, filename):
        """Save metrics to file"""
        metrics = self.get_metrics()
        with open(filename, 'w') as f:
            json.dump(metrics, f, indent=2)
        return len(metrics)

# Performance test execution with monitoring
class PerformanceTestExecutor:
    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.results = {}
    
    def run_load_test(self, test_config):
        """Run load test with performance monitoring"""
        print(f"Starting load test: {test_config['name']}")
        
        # Start monitoring
        self.monitor.start_monitoring()
        
        try:
            # Execute K6 test
            import subprocess
            
            cmd = [
                'k6', 'run',
                '--out', 'json=results.json',
                '--env', f"BASE_URL={test_config['base_url']}",
                test_config['script']
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Load test completed successfully")
                self.results['load_test'] = {
                    'status': 'success',
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
            else:
                print(f"Load test failed: {result.stderr}")
                self.results['load_test'] = {
                    'status': 'failed',
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
        
        finally:
            # Stop monitoring and save metrics
            self.monitor.stop_monitoring()
            time.sleep(2)  # Allow time for final metrics collection
            
            metrics_count = self.monitor.save_metrics_to_file('performance_metrics.json')
            print(f"Saved {metrics_count} performance metrics")
    
    def analyze_results(self):
        """Analyze performance test results"""
        # Load K6 results
        try:
            with open('results.json', 'r') as f:
                k6_results = [json.loads(line) for line in f if line.strip()]
        except FileNotFoundError:
            k6_results = []
        
        # Load performance metrics
        try:
            with open('performance_metrics.json', 'r') as f:
                perf_metrics = json.load(f)
        except FileNotFoundError:
            perf_metrics = []
        
        # Analyze metrics
        analysis = self._analyze_metrics(k6_results, perf_metrics)
        
        # Generate report
        self._generate_report(analysis)
        
        return analysis
    
    def _analyze_metrics(self, k6_results, perf_metrics):
        """Analyze collected metrics"""
        analysis = {
            'summary': {},
            'performance_issues': [],
            'recommendations': []
        }
        
        # Analyze K6 metrics
        if k6_results:
            http_reqs = [r for r in k6_results if r.get('type') == 'Point' and r.get('metric') == 'http_reqs']
            http_req_duration = [r for r in k6_results if r.get('type') == 'Point' and r.get('metric') == 'http_req_duration']
            
            if http_req_duration:
                durations = [r['data']['value'] for r in http_req_duration]
                analysis['summary']['avg_response_time'] = sum(durations) / len(durations)
                analysis['summary']['max_response_time'] = max(durations)
                analysis['summary']['min_response_time'] = min(durations)
                analysis['summary']['total_requests'] = len(http_reqs)
        
        # Analyze system metrics
        if perf_metrics:
            system_metrics = [m for m in perf_metrics if m.get('type') == 'system']
            
            if system_metrics:
                cpu_usage = [m['cpu']['percent'] for m in system_metrics]
                memory_usage = [m['memory']['percent'] for m in system_metrics]
                
                analysis['summary']['avg_cpu_usage'] = sum(cpu_usage) / len(cpu_usage)
                analysis['summary']['max_cpu_usage'] = max(cpu_usage)
                analysis['summary']['avg_memory_usage'] = sum(memory_usage) / len(memory_usage)
                analysis['summary']['max_memory_usage'] = max(memory_usage)
                
                # Identify performance issues
                if max(cpu_usage) > 80:
                    analysis['performance_issues'].append('High CPU usage detected')
                    analysis['recommendations'].append('Consider CPU optimization or scaling')
                
                if max(memory_usage) > 85:
                    analysis['performance_issues'].append('High memory usage detected')
                    analysis['recommendations'].append('Consider memory optimization or scaling')
        
        return analysis
    
    def _generate_report(self, analysis):
        """Generate performance test report"""
        report = f"""
Performance Test Report
======================
Generated: {datetime.utcnow().isoformat()}

Summary:
--------
Average Response Time: {analysis['summary'].get('avg_response_time', 'N/A')} ms
Max Response Time: {analysis['summary'].get('max_response_time', 'N/A')} ms
Total Requests: {analysis['summary'].get('total_requests', 'N/A')}
Average CPU Usage: {analysis['summary'].get('avg_cpu_usage', 'N/A'):.2f}%
Max CPU Usage: {analysis['summary'].get('max_cpu_usage', 'N/A'):.2f}%
Average Memory Usage: {analysis['summary'].get('avg_memory_usage', 'N/A'):.2f}%
Max Memory Usage: {analysis['summary'].get('max_memory_usage', 'N/A'):.2f}%

Performance Issues:
------------------
"""
        
        for issue in analysis['performance_issues']:
            report += f"- {issue}\n"
        
        report += "\nRecommendations:\n----------------\n"
        
        for rec in analysis['recommendations']:
            report += f"- {rec}\n"
        
        with open('performance_report.txt', 'w') as f:
            f.write(report)
        
        print(report)

# Usage example
if __name__ == "__main__":
    executor = PerformanceTestExecutor()
    
    test_config = {
        'name': 'API Load Test',
        'script': 'k6/scenarios/user-journey.js',
        'base_url': 'http://localhost:3000'
    }
    
    executor.run_load_test(test_config)
    analysis = executor.analyze_results()
```

## Example 6

```yaml
# .github/workflows/performance-tests.yml
name: Performance Tests

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:
    inputs:
      test_environment:
        description: 'Environment to test'
        required: true
        default: 'staging'
        type: choice
        options:
        - staging
        - production
      test_duration:
        description: 'Test duration in seconds'
        required: true
        default: '300'
      concurrent_users:
        description: 'Number of concurrent users'
        required: true
        default: '50'

jobs:
  load-test:
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.test_environment || 'staging' }}
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: 18
    
    - name: Install K6
      run: |
        sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
        echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
        sudo apt-get update
        sudo apt-get install k6
    
    - name: Setup performance monitoring
      run: |
        pip install psutil requests
        sudo apt-get install postgresql-client
    
    - name: Run smoke test
      run: |
        k6 run --vus 1 --duration 30s \
          --env BASE_URL=${{ vars.BASE_URL }} \
          k6/scenarios/smoke-test.js
    
    - name: Run load test
      run: |
        python3 scripts/performance-monitor.py &
        MONITOR_PID=$!
        
        k6 run --vus ${{ github.event.inputs.concurrent_users || '50' }} \
          --duration ${{ github.event.inputs.test_duration || '300' }}s \
          --env BASE_URL=${{ vars.BASE_URL }} \
          --out json=results.json \
          k6/scenarios/user-journey.js
        
        kill $MONITOR_PID || true
    
    - name: Database performance test
      run: |
        ./scripts/database-performance-test.sh
      env:
        DB_HOST: ${{ secrets.DB_HOST }}
        DB_USER: ${{ secrets.DB_USER }}
        DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        DB_NAME: ${{ secrets.DB_NAME }}
    
    - name: Analyze results
      run: |
        python3 scripts/analyze-performance-results.py
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      with:
        name: performance-test-results
        path: |
          results.json
          performance_metrics.json
          performance_report.txt
          results/
        retention-days: 30
    
    - name: Performance regression check
      run: |
        python3 scripts/performance-regression-check.py \
          --current-results results.json \
          --baseline-results baseline/results.json \
          --threshold 10
    
    - name: Send Slack notification
      if: failure()
      uses: 8398a7/action-slack@v3
      with:
        status: failure
        channel: '#performance-alerts'
        text: 'Performance test failed on ${{ github.event.inputs.test_environment || "staging" }}'
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

  stress-test:
    runs-on: ubuntu-latest
    needs: load-test
    if: github.event.inputs.test_environment == 'staging'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Install K6
      run: |
        sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
        echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
        sudo apt-get update
        sudo apt-get install k6
    
    - name: Run stress test
      run: |
        k6 run --env BASE_URL=${{ vars.BASE_URL }} \
          --out json=stress-results.json \
          k6/scenarios/stress-test.js
    
    - name: Analyze stress test results
      run: |
        python3 scripts/analyze-stress-test.py stress-results.json
    
    - name: Upload stress test results
      uses: actions/upload-artifact@v3
      with:
        name: stress-test-results
        path: stress-results.json
        retention-days: 30
```

## Example 7

```javascript
// scripts/performance-budget.js
const performanceBudget = {
  // Response time budgets (in milliseconds)
  responseTime: {
    homepage: { p95: 1000, p99: 2000 },
    api_endpoints: { p95: 500, p99: 1000 },
    database_queries: { p95: 100, p99: 500 }
  },
  
  // Throughput budgets (requests per second)
  throughput: {
    api_endpoints: { min: 1000 },
    homepage: { min: 500 }
  },
  
  // Error rate budgets (percentage)
  errorRate: {
    max: 0.1  // 0.1% maximum error rate
  },
  
  // Resource utilization budgets
  resources: {
    cpu: { max: 70 },      // 70% maximum CPU usage
    memory: { max: 80 },   // 80% maximum memory usage
    disk: { max: 85 }      // 85% maximum disk usage
  }
};

class PerformanceBudgetValidator {
  constructor(budget) {
    this.budget = budget;
  }
  
  validateResults(testResults) {
    const violations = [];
    
    // Validate response times
    if (testResults.responseTime) {
      for (const [endpoint, metrics] of Object.entries(testResults.responseTime)) {
        const budget = this.budget.responseTime[endpoint];
        if (budget) {
          if (metrics.p95 > budget.p95) {
            violations.push(`${endpoint} P95 response time (${metrics.p95}ms) exceeds budget (${budget.p95}ms)`);
          }
          if (metrics.p99 > budget.p99) {
            violations.push(`${endpoint} P99 response time (${metrics.p99}ms) exceeds budget (${budget.p99}ms)`);
          }
        }
      }
    }
    
    // Validate throughput
    if (testResults.throughput) {
      for (const [endpoint, metrics] of Object.entries(testResults.throughput)) {
        const budget = this.budget.throughput[endpoint];
        if (budget && metrics.rps < budget.min) {
          violations.push(`${endpoint} throughput (${metrics.rps} RPS) below budget (${budget.min} RPS)`);
        }
      }
    }
    
    // Validate error rates
    if (testResults.errorRate && testResults.errorRate > this.budget.errorRate.max) {
      violations.push(`Error rate (${testResults.errorRate}%) exceeds budget (${this.budget.errorRate.max}%)`);
    }
    
    return {
      passed: violations.length === 0,
      violations: violations
    };
  }
}

module.exports = { performanceBudget, PerformanceBudgetValidator };
```
