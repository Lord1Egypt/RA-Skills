# 详细参考 - cdn-toolkit-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
#!/usr/bin/env python3
"""专业版多CDN智能调度引擎"""

import requests
import json
import time
from collections import defaultdict

class MultiCDNRouter:
    """多CDN智能调度路由器"""

    def __init__(self):
        self.providers = {
            "cloudflare": {
                "name": "Cloudflare",
                "api": "https://api.cloudflare.com/client/v4",
                "regions": ["global"],
                "priority": 1
            },
            "cloudfront": {
                "name": "AWS CloudFront",
                "api": "https://cloudfront.amazonaws.com",
                "regions": ["us", "eu", "ap"],
                "priority": 2
            },
            "alicdn": {
                "name": "阿里云CDN",
                "api": "https://cdn.aliyuncs.com",
                "regions": ["cn", "ap"],
                "priority": 1
            }
        }
        self.health_status = {}
        self.performance_metrics = defaultdict(list)

    def health_check(self, provider):
        """CDN健康检查"""
        start = time.time()
        try:
            resp = requests.head(
                f"https://{provider}.example.com/health",
                timeout=5
            )
            latency = (time.time() - start) * 1000
            healthy = resp.status_code == 200
        except:
            latency = 9999
            healthy = False

        self.health_status[provider] = {
            "healthy": healthy,
            "latency_ms": round(latency),
            "last_check": time.time()
        }
        return self.health_status[provider]

    def select_best_cdn(self, user_region="global"):
        """选择最优CDN"""
        candidates = []

        for provider, config in self.providers.items():
            if user_region not in config["regions"] and "global" not in config["regions"]:
                continue

            health = self.health_check(provider)
            if not health["healthy"]:
                continue

            candidates.append({
                "provider": provider,
                "priority": config["priority"],
                "latency": health["latency_ms"]
            })

        if not candidates:
            return None

        candidates.sort(key=lambda x: (x["priority"], x["latency"]))
        return candidates[0]["provider"]

    def get_routing_report(self):
        """生成路由报告"""
        report = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "providers": {}
        }
        for provider in self.providers:
            health = self.health_status.get(provider, {})
            report["providers"][provider] = {
                "name": self.providers[provider]["name"],
                "healthy": health.get("healthy", False),
                "latency_ms": health.get("latency_ms", 0),
                "regions": self.providers[provider]["regions"]
            }
        return report

if __name__ == "__main__":
    router = MultiCDNRouter()

    for region in ["cn", "us", "eu", "ap"]:
        best = router.select_best_cdn(region)
        print(f"区域 {region}: 最优CDN = {best}")

    print(json.dumps(router.get_routing_report(), indent=2, ensure_ascii=False))
```

## 代码示例 (python)

```python
#!/usr/bin/env python3
"""专业版CDN实时监控与告警"""

import requests
import json
import smtplib
from datetime import datetime

class CDNMonitor:
    """CDN实时监控"""

    ALERT_THRESHOLDS = {
        "cache_hit_rate": 85,       # 缓存命中率阈值%
        "response_time_ms": 500,    # 响应时间阈值ms
        "error_rate": 1,            # 错误率阈值%
        "bandwidth_mbps": 1000,     # 带宽阈值Mbps
        "requests_per_sec": 10000   # 请求阈值QPS
    }

    def __init__(self, api_token, zone_id):
        self.api_token = api_token
        self.zone_id = zone_id
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    def get_analytics(self, since="-60"):
        """获取CDN分析数据"""
        resp = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/analytics/dashboard",
            headers=self.headers,
            params={
                "since": since,
                "until": "now",
                "continuous": "true"
            }
        )
        return resp.json().get("result", {})

    def check_alerts(self, analytics):
        """检查告警条件"""
        alerts = []

        total = analytics.get("totals", {})
        cached = total.get("cachedRequests", 0)
        all_reqs = total.get("requests", {}).get("all", 0)

        if all_reqs > 0:
            hit_rate = (cached / all_reqs) * 100
            if hit_rate < self.ALERT_THRESHOLDS["cache_hit_rate"]:
                alerts.append({
                    "level": "WARNING",
                    "metric": "cache_hit_rate",
                    "value": f"{hit_rate:.1f}%",
                    "threshold": f"{self.ALERT_THRESHOLDS['cache_hit_rate']}%",
                    "message": f"缓存命中率偏低: {hit_rate:.1f}%"
                })

        bandwidth = total.get("bandwidth", {})
        if bandwidth:
            alerts.append({
                "level": "INFO",
                "metric": "bandwidth",
                "value": f"{bandwidth.get('all', 0) / 1e6:.1f} Mbps",
                "message": "当前带宽数据已采集"
            })

        return alerts

    def send_alert(self, alerts):
        """发送告警"""
        if not alerts:
            return

        print(f"\n[{datetime.utcnow().isoformat()}] 发现 {len(alerts)} 个告警:")
        for alert in alerts:
            print(f"  [{alert['level']}] {alert['message']}")

if __name__ == "__main__":
    monitor = CDNMonitor("YOUR_TOKEN", "YOUR_ZONE_ID")
    analytics = monitor.get_analytics()
    alerts = monitor.check_alerts(analytics)
    monitor.send_alert(alerts)
```

