# Monitoring Specialist — Code Examples

## Example 1

```yaml
# Prometheus configuration
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    region: 'us-east-1'

# Alerting configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

# Recording rules for performance
rule_files:
  - '/etc/prometheus/recording_rules.yml'
  - '/etc/prometheus/alerting_rules.yml'

# Service discovery
scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node1:9100', 'node2:9100', 'node3:9100']

  - job_name: 'blackbox'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
          - https://example.com
          - https://api.example.com/health
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: blackbox:9115
```

## Example 2

```yaml
# alerting_rules.yml
groups:
  - name: availability
    interval: 30s
    rules:
      - alert: ServiceDown
        expr: up{job="api"} == 0
        for: 2m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "Service {{ $labels.instance }} is down"
          description: "{{ $labels.instance }} has been down for more than 2 minutes"
          runbook: "https://wiki.example.com/runbooks/service-down"

      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
            /
            sum(rate(http_requests_total[5m])) by (service)
          ) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate for {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }} for {{ $labels.service }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High latency for {{ $labels.service }}"
          description: "95th percentile latency is {{ $value }}s for {{ $labels.service }}"

  - name: resource_utilization
    rules:
      - alert: HighCPUUsage
        expr: |
          (
            100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
          ) > 80
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is {{ $value }}% on {{ $labels.instance }}"

      - alert: HighMemoryUsage
        expr: |
          (
            (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
            / node_memory_MemTotal_bytes
          ) > 0.9
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is {{ $value | humanizePercentage }} on {{ $labels.instance }}"

      - alert: DiskSpaceLow
        expr: |
          (
            node_filesystem_avail_bytes{fstype!~"tmpfs|fuse.lxcfs|squashfs|vfat"}
            / node_filesystem_size_bytes
          ) < 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Only {{ $value | humanizePercentage }} disk space left on {{ $labels.instance }} ({{ $labels.mountpoint }})"
```

## Example 3

```json
{
  "dashboard": {
    "title": "Service Overview",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{ service }}"
          }
        ],
        "type": "graph",
        "yaxes": [{"format": "reqps"}]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) by (service) / sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{ service }}"
          }
        ],
        "type": "graph",
        "yaxes": [{"format": "percentunit"}],
        "thresholds": [
          {"value": 0.01, "color": "yellow"},
          {"value": 0.05, "color": "red"}
        ]
      },
      {
        "title": "P95 Latency",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))",
            "legendFormat": "{{ service }}"
          }
        ],
        "type": "graph",
        "yaxes": [{"format": "s"}]
      },
      {
        "title": "Service Health",
        "targets": [
          {
            "expr": "up{job=\"api\"}",
            "legendFormat": "{{ instance }}"
          }
        ],
        "type": "stat",
        "thresholds": {
          "mode": "absolute",
          "steps": [
            {"color": "red", "value": 0},
            {"color": "green", "value": 1}
          ]
        }
      }
    ]
  }
}
```

## Example 4

```yaml
# Logstash pipeline configuration
input {
  beats {
    port => 5044
  }
  
  kafka {
    bootstrap_servers => "kafka:9092"
    topics => ["application-logs"]
    codec => json
  }
}

filter {
  # Parse JSON logs
  if [message] =~ /^\{.*\}$/ {
    json {
      source => "message"
    }
  }
  
  # Extract fields from log message
  grok {
    match => {
      "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} \\[%{DATA:thread}\\] %{DATA:logger} - %{GREEDYDATA:msg}"
    }
  }
  
  # Add GeoIP information
  if [client_ip] {
    geoip {
      source => "client_ip"
      target => "geoip"
    }
  }
  
  # Calculate response time
  if [response_time] {
    ruby {
      code => "
        event.set('response_time_ms', event.get('response_time').to_f * 1000)
      "
    }
  }
  
  # Add environment metadata
  mutate {
    add_field => {
      "environment" => "${ENVIRONMENT:production}"
      "datacenter" => "${DATACENTER:us-east-1}"
    }
  }
  
  # Parse user agent
  if [user_agent] {
    useragent {
      source => "user_agent"
      target => "ua"
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{[@metadata][beat]}-%{+YYYY.MM.dd}"
  }
  
  # Send critical errors to Slack
  if [level] == "ERROR" or [level] == "FATAL" {
    http {
      url => "${SLACK_WEBHOOK_URL}"
      http_method => "post"
      format => "json"
      mapping => {
        "text" => "Error in %{service}: %{msg}"
        "attachments" => [
          {
            "color" => "danger"
            "fields" => [
              {"title" => "Service", "value" => "%{service}"},
              {"title" => "Level", "value" => "%{level}"},
              {"title" => "Time", "value" => "%{timestamp}"}
            ]
          }
        ]
      }
    }
  }
}
```

## Example 5

```python
# OpenTelemetry instrumentation
from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

# Configure tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

# Add span processor
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Auto-instrument libraries
RequestsInstrumentor().instrument()
FlaskInstrumentor().instrument_app(app)

# Manual instrumentation
@app.route('/api/process')
def process_request():
    with tracer.start_as_current_span("process_request") as span:
        span.set_attribute("user.id", request.user_id)
        span.set_attribute("request.method", request.method)
        
        # Database operation
        with tracer.start_as_current_span("database_query"):
            result = db.query("SELECT * FROM users WHERE id = ?", user_id)
            span.set_attribute("db.statement", "SELECT * FROM users")
            span.set_attribute("db.rows_affected", len(result))
        
        # External service call
        with tracer.start_as_current_span("external_api_call"):
            response = requests.get("https://api.external.com/data")
            span.set_attribute("http.status_code", response.status_code)
            span.set_attribute("http.url", response.url)
        
        # Business logic
        with tracer.start_as_current_span("business_logic"):
            processed = process_data(result, response.json())
            span.set_attribute("items.processed", len(processed))
        
        return jsonify(processed)

# Trace context propagation
def make_downstream_request(url, data):
    headers = {}
    TraceContextTextMapPropagator().inject(headers)
    
    with tracer.start_as_current_span("downstream_request"):
        response = requests.post(url, json=data, headers=headers)
        return response.json()
```

## Example 6

```python
from prometheus_client import Counter, Histogram, Gauge, Summary
import time

# Define custom metrics
request_count = Counter(
    'app_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'app_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.001, 0.01, 0.1, 0.5, 1, 2, 5, 10]
)

active_users = Gauge(
    'app_active_users',
    'Number of active users'
)

cache_hit_ratio = Summary(
    'app_cache_hit_ratio',
    'Cache hit ratio'
)

# Middleware for automatic metrics collection
class MetricsMiddleware:
    def __init__(self, app):
        self.app = app
        
    def __call__(self, environ, start_response):
        start_time = time.time()
        
        def custom_start_response(status, headers):
            # Extract status code
            status_code = int(status.split()[0])
            
            # Record metrics
            method = environ['REQUEST_METHOD']
            path = environ['PATH_INFO']
            
            request_count.labels(
                method=method,
                endpoint=path,
                status=status_code
            ).inc()
            
            request_duration.labels(
                method=method,
                endpoint=path
            ).observe(time.time() - start_time)
            
            return start_response(status, headers)
        
        return self.app(environ, custom_start_response)
```

## Example 7

```javascript
// Puppeteer synthetic monitoring script
const puppeteer = require('puppeteer');
const { StatsD } = require('node-statsd');

const statsd = new StatsD({ host: 'statsd', port: 8125 });

async function syntheticCheck() {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  
  try {
    // Performance timing
    const startTime = Date.now();
    
    // Navigate to page
    await page.goto('https://example.com', {
      waitUntil: 'networkidle2',
      timeout: 30000
    });
    
    // Measure page load time
    const loadTime = Date.now() - startTime;
    statsd.timing('synthetic.page_load', loadTime);
    
    // Check for specific elements
    const loginButton = await page.$('#login');
    if (!loginButton) {
      throw new Error('Login button not found');
    }
    
    // Perform user journey
    await page.click('#login');
    await page.waitForSelector('#username', { timeout: 5000 });
    
    await page.type('#username', 'test@example.com');
    await page.type('#password', 'password');
    
    const loginStart = Date.now();
    await page.click('#submit');
    await page.waitForSelector('#dashboard', { timeout: 10000 });
    
    const loginTime = Date.now() - loginStart;
    statsd.timing('synthetic.login_time', loginTime);
    
    // Check API endpoint
    const apiResponse = await page.evaluate(() => {
      return fetch('/api/health')
        .then(res => res.json());
    });
    
    if (apiResponse.status !== 'healthy') {
      throw new Error('API unhealthy');
    }
    
    statsd.increment('synthetic.check.success');
    
  } catch (error) {
    console.error('Synthetic check failed:', error);
    statsd.increment('synthetic.check.failure');
    
    // Take screenshot for debugging
    await page.screenshot({ path: `/tmp/error-${Date.now()}.png` });
    
    // Send alert
    await sendAlert({
      level: 'critical',
      message: `Synthetic check failed: ${error.message}`,
      screenshot: `/tmp/error-${Date.now()}.png`
    });
    
  } finally {
    await browser.close();
  }
}

// Run every 5 minutes
setInterval(syntheticCheck, 5 * 60 * 1000);
```

## Example 8

```yaml
# SLI definitions
slis:
  - name: availability
    query: |
      sum(rate(http_requests_total{status!~"5.."}[5m]))
      /
      sum(rate(http_requests_total[5m]))
  
  - name: latency
    query: |
      histogram_quantile(0.95,
        sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
      )
  
  - name: error_rate
    query: |
      sum(rate(http_requests_total{status=~"5.."}[5m]))
      /
      sum(rate(http_requests_total[5m]))

# SLO definitions
slos:
  - name: availability_slo
    sli: availability
    target: 0.999  # 99.9%
    window: 30d
    
  - name: latency_slo
    sli: latency
    target: 0.5  # 500ms
    comparison: "<"
    window: 30d
    
  - name: error_rate_slo
    sli: error_rate
    target: 0.001  # 0.1%
    comparison: "<"
    window: 30d

# Error budget calculation
error_budgets:
  - name: availability_budget
    slo: availability_slo
    calculation: |
      (1 - slo_target) * window_duration - 
      (1 - current_sli_value) * window_duration
```
