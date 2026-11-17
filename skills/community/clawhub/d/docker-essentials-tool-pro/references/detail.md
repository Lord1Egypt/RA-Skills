# 详细参考 - docker-essentials-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import subprocess
import json
from datetime import datetime

class ImageAnalyzer:
    """Docker镜像深度分析器"""

    def __init__(self, image_name):
        self.image_name = image_name
        self.history = None
        self.layers = None

    def analyze(self):
        """执行完整分析"""
        self._get_history()
        self._get_size()
        self._get_labels()
        return self._generate_report()

    def _get_history(self):
        """获取镜像构建历史"""
        result = subprocess.run(
            ["docker", "history", "--format", "{{json .}}", self.image_name],
            capture_output=True, text=True
        )
        self.history = [json.loads(line) for line in result.stdout.strip().split('\n')]

    def _get_size(self):
        """获取镜像大小"""
        result = subprocess.run(
            ["docker", "inspect", "--format", "{{.Size}}", self.image_name],
            capture_output=True, text=True
        )
        self.size = int(result.stdout.strip())

    def _get_labels(self):
        """获取镜像标签信息"""
        result = subprocess.run(
            ["docker", "inspect", "--format", "{{json .Config.Labels}}", self.image_name],
            capture_output=True, text=True
        )
        self.labels = json.loads(result.stdout.strip()) if result.stdout.strip() != "null" else {}

    def _generate_report(self):
        """生成分析报告"""
        total_layer_size = sum(
            self._parse_size(h.get("Size", "0")) for h in self.history
        )

        optimizable = []
        for h in self.history:
            size = self._parse_size(h.get("Size", "0"))
            if size > 50 * 1024 * 1024:  # 大于50MB的层
                optimizable.append({
                    "command": h.get("CreatedBy", ""),
                    "size_mb": round(size / 1024 / 1024, 2),
                    "suggestion": "建议合并RUN指令或清理缓存"
                })

        return {
            "image": self.image_name,
            "total_size_mb": round(self.size / 1024 / 1024, 2),
            "layer_count": len(self.history),
            "labels": self.labels,
            "optimizable_layers": optimizable,
            "recommendations": self._get_recommendations()
        }

    def _parse_size(self, size_str):
        """解析大小字符串"""
        if isinstance(size_str, (int, float)):
            return int(size_str)
        return 0

    def _get_recommendations(self):
        """生成优化建议"""
        recs = []
        if self.size > 500 * 1024 * 1024:
            recs.append("镜像超过500MB,建议使用多阶段构建减小体积")
        if len(self.history) > 15:
            recs.append("层数过多,建议合并RUN指令")
        return recs

analyzer = ImageAnalyzer("myapp:1.0")
report = analyzer.analyze()
print(json.dumps(report, indent=2, ensure_ascii=False))
```

## 代码示例 (python)

```python
import subprocess
import json
import time

class ContainerMonitor:
    """容器资源监控与告警"""

    def __init__(self, thresholds=None):
        self.thresholds = thresholds or {
            "cpu_percent": 80.0,
            "memory_percent": 85.0,
            "memory_limit": "512M"
        }

    def get_stats(self, container_name=None):
        """获取容器资源使用统计"""
        cmd = ["docker", "stats", "--no-stream", "--format", "{{json .}}"]
        if container_name:
            cmd.append(container_name)

        result = subprocess.run(cmd, capture_output=True, text=True)
        stats = []
        for line in result.stdout.strip().split('\n'):
            if line:
                stats.append(json.loads(line))
        return stats

    def check_thresholds(self, stats):
        """检查是否超过阈值"""
        alerts = []
        for s in stats:
            name = s.get("Name", "unknown")
            cpu = self._parse_percent(s.get("CPUPerc", "0%"))
            mem = self._parse_percent(s.get("MemPerc", "0%"))

            if cpu > self.thresholds["cpu_percent"]:
                alerts.append({
                    "container": name,
                    "metric": "cpu",
                    "value": f"{cpu}%",
                    "threshold": f"{self.thresholds['cpu_percent']}%"
                })

            if mem > self.thresholds["memory_percent"]:
                alerts.append({
                    "container": name,
                    "metric": "memory",
                    "value": f"{mem}%",
                    "threshold": f"{self.thresholds['memory_percent']}%"
                })
        return alerts

    def _parse_percent(self, s):
        """解析百分比字符串"""
        try:
            return float(s.strip('%'))
        except (ValueError, AttributeError):
            return 0.0

    def monitor_loop(self, interval=30):
        """持续监控循环"""
        while True:
            stats = self.get_stats()
            alerts = self.check_thresholds(stats)
            for alert in alerts:
                print(f"[ALERT] {alert['container']} - "
                      f"{alert['metric']}: {alert['value']} "
                      f"(阈值: {alert['threshold']})")
            time.sleep(interval)
```

## 代码示例 (yaml)

```yaml
version: "2.0"
edition: pro

settings:
  registry: registry.company.com
  namespace: production
  tag_strategy: semantic

optimization:
  analyze_layers: true
  suggest_multistage: true
  max_image_size: 500MB
  base_image_preferences:
    - alpine
    - slim
    - distroless

security:
  scan_vulnerabilities: true
  check_root_user: true
  check_secrets: true
  check_exposed_ports: true
  fail_on: [critical, high]
  scan_tools: [trivy, grype]

swarm:
  enabled: true
  manager_nodes: 3
  worker_nodes: 5
  update_config:
    parallelism: 1
    delay: 10s
    failure_action: rollback

monitoring:
  enabled: true
  interval: 30
  thresholds:
    cpu: 80
    memory: 85
    disk: 90
  alert:
    webhook: "${ALERT_WEBHOOK_URL}"
    email:
      to: ops@company.com

ci_cd:
  auto_build: true
  auto_scan: true
  auto_deploy: true
  registry_auth: true

multi_tenant:
  enabled: true
  resource_quotas: true
  network_isolation: true
```

## 代码示例 (bash)

```bash
#!/bin/bash
IMAGE="myapp:1.0"
echo "=== 镜像优化流水线 ==="

echo "1. 镜像分析..."
docker history --no-trunc "$IMAGE" > "image-history.txt"
SIZE=$(docker inspect --format='{{.Size}}' "$IMAGE")
echo "当前大小: $((SIZE / 1024 / 1024))MB"

echo -e "\n2. 安全扫描..."
USER=$(docker inspect --format='{{.Config.User}}' "$IMAGE")
if [ -z "$USER" ]; then
    echo "[!] 添加非root用户"
fi

echo -e "\n3. 生成优化建议..."
cat > Dockerfile.optimized << 'EOF'
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:18-alpine
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodeapp -u 1001
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER nodeapp
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -q --spider http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
EOF

echo -e "\n4. 构建优化镜像..."
docker build -f Dockerfile.optimized -t myapp:1.0-optimized .

NEW_SIZE=$(docker inspect --format='{{.Size}}' myapp:1.0-optimized)
echo "优化后大小: $((NEW_SIZE / 1024 / 1024))MB"
echo "减小: $(( (SIZE - NEW_SIZE) / 1024 / 1024 ))MB"
```

## 代码示例 (yaml)

```yaml
version: '3.8'
services:
  web:
    image: myapp:1.0
    ports:
      - "8080:80"
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      restart_policy:
        condition: on-failure
        max_attempts: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
      placement:
        constraints:
          - node.role == worker

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db-data:/var/lib/postgresql/data
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager

volumes:
  db-data:
```

## 代码示例 (bash)

```bash
#!/bin/bash
IMAGE="${1:?用法: security-scan.sh <image>}"
echo "=== 容器安全扫描: $IMAGE ==="

echo "--- 镜像基础信息 ---"
docker inspect --format='
镜像: {{.RepoTags}}
操作系统: {{.Os}}
架构: {{.Architecture}}
大小: {{.Size}} bytes
创建时间: {{.Created}}
' "$IMAGE"

echo -e "\n--- 安全配置检查 ---"

USER=$(docker inspect --format='{{.Config.User}}' "$IMAGE")
if [ -z "$USER" ] || [ "$USER" = "root" ]; then
    echo "[!] 警告: 镜像以root用户运行"
else
    echo "[OK] 使用非root用户: $USER"
fi

MOUNTS=$(docker inspect --format='{{range .Mounts}}{{.Source}}:{{.Destination}} {{end}}' "$IMAGE")
echo "挂载点: ${MOUNTS:-无}"

ENV_VARS=$(docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' "$IMAGE")
echo "环境变量:"
echo "$ENV_VARS" | grep -iE "(password|secret|key|token)" && \
    echo "[!] 警告: 环境变量中可能包含敏感信息" || echo "[OK] 未发现敏感环境变量"

echo -e "\n--- 镜像层分析 ---"
docker history --no-trunc --format "{{.CreatedBy}}" "$IMAGE" | \
    grep -iE "(wget|curl|apt|yum|apk)" | head -10

echo -e "\n--- 暴露端口 ---"
docker inspect --format='{{range $p, $conf := .Config.ExposedPorts}}{{$p}}{{end}}' "$IMAGE"
```

