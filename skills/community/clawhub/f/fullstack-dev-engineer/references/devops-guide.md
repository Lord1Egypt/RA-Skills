# 运维实践指南

## 目录
- [容器化部署](#容器化部署)
- [CI/CD流水线](#cicd流水线)
- [监控与告警](#监控与告警)
- [日志管理](#日志管理)
- [故障排查](#故障排查)
- [性能优化](#性能优化)
- [安全加固](#安全加固)
- [灾难恢复](#灾难恢复)

## 容器化部署

### Docker最佳实践

#### Dockerfile优化
```dockerfile
# 多阶段构建
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# 生产镜像
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000
USER node
CMD ["node", "dist/main.js"]
```

#### Docker Compose配置
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      - db
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### Kubernetes部署

#### Deployment配置
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### Service配置
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: LoadBalancer
```

#### Ingress配置
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

## CI/CD流水线

### GitHub Actions

#### 自动化测试和部署
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
    - uses: actions/checkout@v3

    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Run linter
      run: npm run lint

    - name: Run tests
      run: npm run test:coverage

    - name: Upload coverage
      uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          myapp:latest
          myapp:${{ github.sha }}
        cache-from: type=registry,ref=myapp:latest
        cache-to: type=inline

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        method: kubeconfig
        kubeconfig: ${{ secrets.KUBE_CONFIG }}

    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/myapp \
          myapp=myapp:${{ github.sha }} \
          --namespace=production

        kubectl rollout status deployment/myapp \
          --namespace=production
```

### GitLab CI/CD

```yaml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: myapp

test:
  stage: test
  image: node:20
  cache:
    paths:
      - node_modules/
  script:
    - npm ci
    - npm run lint
    - npm run test:coverage
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $DOCKER_IMAGE:$CI_COMMIT_SHA .
    - docker push $DOCKER_IMAGE:$CI_COMMIT_SHA
  only:
    - main

deploy_staging:
  stage: deploy
  image:
    name: bitnami/kubectl:latest
  script:
    - kubectl config use-context staging
    - kubectl set image deployment/myapp myapp=$DOCKER_IMAGE:$CI_COMMIT_SHA
    - kubectl rollout status deployment/myapp
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - main

deploy_production:
  stage: deploy
  image:
    name: bitnami/kubectl:latest
  script:
    - kubectl config use-context production
    - kubectl set image deployment/myapp myapp=$DOCKER_IMAGE:$CI_COMMIT_SHA
    - kubectl rollout status deployment/myapp
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - main
```

## 监控与告警

### Prometheus配置

#### prometheus.yml
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - alertmanager:9093

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: 'myapp'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - production
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
```

#### 告警规则（alerts.yml）
```yaml
groups:
  - name: myapp_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} for {{ $labels.instance }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, instance)
          ) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "95th percentile latency is {{ $value }}s"

      - alert: PodNotReady
        expr: kube_pod_status_ready{condition="true"} == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Pod is not ready"
          description: "Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} is not ready"

      - alert: DatabaseConnectionPoolExhausted
        expr: |
          pg_stat_activity_count{datname="myapp"} / pg_settings_max_connections > 0.9
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Database connection pool nearly exhausted"
          description: "{{ $value | humanizePercentage }} of connections used"
```

### Grafana仪表盘

#### 关键指标面板
```json
{
  "dashboard": {
    "title": "Application Performance",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (method, path)"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))"
          }
        ]
      },
      {
        "title": "Response Time (95th percentile)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))"
          }
        ]
      },
      {
        "title": "CPU Usage",
        "targets": [
          {
            "expr": "100 * (1 - avg(rate(node_cpu_seconds_total{mode=\"idle\"}[5m])))"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "targets": [
          {
            "expr": "100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)"
          }
        ]
      }
    ]
  }
}
```

## 日志管理

### ELK Stack配置

#### Logstash配置
```conf
input {
  beats {
    port => 5044
  }
}

filter {
  if [kubernetes][namespace] == "production" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}" }
    }

    date {
      match => [ "timestamp", "ISO8601" ]
    }

    # 添加应用元数据
    mutate {
      add_field => {
        "environment" => "production"
        "app_name" => "%{[kubernetes][labels][app]}"
      }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "myapp-%{+YYYY.MM.dd}"
  }
}
```

#### 日志查询示例
```json
// Kibana查询语法
// 1. 查看错误日志
level: "ERROR"

// 2. 查看特定用户的请求
user_id: "123" AND level: "INFO"

// 3. 查看慢查询
message: *slow* AND duration:>1000

// 4. 查看最近1小时的错误
@timestamp:[now-1h TO now] AND level: "ERROR"

// 5. 统计错误类型
aggs: {
  "error_types": {
    "terms": {
      "field": "error_type.keyword",
      "size": 10
    }
  }
}
```

## 故障排查

### 常见问题诊断

#### Pod无法启动
```bash
# 查看Pod状态
kubectl describe pod <pod-name> -n <namespace>

# 查看日志
kubectl logs <pod-name> -n <namespace>

# 查看事件
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# 进入Pod调试
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh
```

#### 服务不可用
```bash
# 检查Service
kubectl get svc -n <namespace>

# 检查Endpoint
kubectl get endpoints <service-name> -n <namespace>

# 测试服务连通性
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://<service-name>.<namespace>.svc.cluster.local

# 检查Ingress
kubectl describe ingress <ingress-name> -n <namespace>
```

#### 性能问题
```bash
# 查看资源使用
kubectl top pods -n <namespace>
kubectl top nodes

# 查看Pod资源限制
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 "Limits"

# 查看容器资源使用
kubectl exec <pod-name> -n <namespace> -- top
```

### 故障排查流程

```bash
#!/bin/bash
# 故障排查脚本

NAMESPACE=${1:-production}

echo "=== 检查Pod状态 ==="
kubectl get pods -n $NAMESPACE

echo -e "\n=== 检查最近的事件 ==="
kubectl get events -n $NAMESPACE --sort-by='.lastTimestamp' --field-selector type!=Normal | tail -20

echo -e "\n=== 检查资源使用 ==="
kubectl top pods -n $NAMESPACE

echo -e "\n=== 检查Service状态 ==="
kubectl get svc -n $NAMESPACE

echo -e "\n=== 检查Ingress状态 ==="
kubectl get ingress -n $NAMESPACE

echo -e "\n=== 检查PVC状态 ==="
kubectl get pvc -n $NAMESPACE
```

## 性能优化

### 应用层优化

#### Node.js性能调优
```javascript
// cluster模式
const cluster = require('cluster');
const os = require('os');

if (cluster.isMaster) {
  const cpuCount = os.cpus().length;
  console.log(`Master ${process.pid} is running`);

  for (let i = 0; i < cpuCount; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
    cluster.fork();
  });
} else {
  require('./app');
}
```

#### 数据库连接池配置
```javascript
// PostgreSQL连接池
const pool = new Pool({
  host: process.env.DB_HOST,
  port: 5432,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20, // 最大连接数
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

### 系统层优化

#### Nginx配置优化
```nginx
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    # 开启gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript;

    # 连接优化
    keepalive_timeout 65;
    keepalive_requests 100;

    # 缓存配置
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

    upstream myapp {
        least_conn;
        server app1:3000 weight=3;
        server app2:3000 weight=2;
        server app3:3000 backup;
        keepalive 32;
    }

    server {
        listen 80;
        server_name myapp.example.com;

        location / {
            proxy_pass http://myapp;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            proxy_cache my_cache;
            proxy_cache_valid 200 10m;
        }
    }
}
```

## 安全加固

### 容器安全

#### 最小权限原则
```yaml
# SecurityContext配置
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: myapp
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
```

#### 镜像扫描
```bash
# 使用Trivy扫描镜像
trivy image myapp:latest

# 使用Clair扫描
clairctl analyze myapp:latest

# 集成到CI/CD
- name: Scan Docker image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:latest
    format: 'sarif'
    output: 'trivy-results.sarif'
```

### 网络安全

#### NetworkPolicy配置
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: myapp-network-policy
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: nginx
    ports:
    - protocol: TCP
      port: 3000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

### 密钥管理

#### Secret管理
```bash
# 创建Secret
kubectl create secret generic myapp-secrets \
  --from-literal=database-url='postgresql://user:pass@db:5432/myapp' \
  --from-literal=api-key='your-api-key' \
  -n production

# 使用Sealed Secrets加密Secret
kubeseal -f secret.yaml -w sealed-secret.yaml

# 或使用External Secrets Operator引用外部密钥管理器
```

## 灾难恢复

### 备份策略

#### 数据库备份
```bash
#!/bin/bash
# PostgreSQL备份脚本

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/postgres"
RETENTION_DAYS=7

# 创建备份
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME | gzip > $BACKUP_DIR/myapp_$DATE.sql.gz

# 清理旧备份
find $BACKUP_DIR -name "myapp_*.sql.gz" -mtime +$RETENTION_DAYS -delete

# 上传到S3
aws s3 cp $BACKUP_DIR/myapp_$DATE.sql.gz s3://my-backups/postgres/
```

#### Kubernetes资源备份
```bash
# 使用Velero备份
velero backup create myapp-backup \
  --include-namespaces production \
  --selector app=myapp \
  --ttl 72h

# 定时备份
velero schedule create daily-backup \
  --schedule="0 2 * * *" \
  --include-namespaces production \
  --ttl 168h
```

### 恢复流程

```bash
#!/bin/bash
# 恢复脚本

echo "=== 停止应用 ==="
kubectl scale deployment myapp --replicas=0 -n production

echo "=== 恢复数据库 ==="
aws s3 cp s3://my-backups/postgres/myapp_20240106_020000.sql.gz - | gunzip | psql -h $DB_HOST -U $DB_USER -d $DB_NAME

echo "=== 启动应用 ==="
kubectl scale deployment myapp --replicas=3 -n production

echo "=== 等待Pod就绪 ==="
kubectl rollout status deployment/myapp -n production

echo "=== 验证服务 ==="
curl -f http://myapp.example.com/health || exit 1

echo "=== 恢复完成 ==="
```
