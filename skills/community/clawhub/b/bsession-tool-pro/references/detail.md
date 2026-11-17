# 详细参考 - bsession-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import os
import json

class SessionPersister:
    """会话持久化（专业版）"""

    def __init__(self, workspace="~/.bsession/workspace"):
        self.workspace = os.path.expanduser(workspace)
        self.conf_dir = os.path.join(self.workspace, "conf")
        self.scripts_dir = os.path.join(self.workspace, "scripts")
        os.makedirs(self.conf_dir, exist_ok=True)
        os.makedirs(self.scripts_dir, exist_ok=True)

    def save_session(self, name, config, script_code):
        """保存会话为可复用脚本"""
        conf_path = os.path.join(self.conf_dir, f"{name}.conf")
        with open(conf_path, "w", encoding="utf-8") as f:
            f.write(self._generate_conf(config))

        script_path = os.path.join(self.scripts_dir, f"{name}.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_code)

        print(f"会话已保存：{name}")
        print(f"  配置：{conf_path}")
        print(f"  脚本：{script_path}")
        return {"conf": conf_path, "script": script_path}

    def _generate_conf(self, config):
        """生成conf文件"""
        lines = ["[env]"]
        for k, v in config.items():
            lines.append(f"{k}={v}")
        return "\n".join(lines)

    def load_session(self, name):
        """加载已保存的会话"""
        conf_path = os.path.join(self.conf_dir, f"{name}.conf")
        script_path = os.path.join(self.scripts_dir, f"{name}.py")

        if not os.path.exists(conf_path):
            return {"error": f"会话 {name} 不存在"}

        with open(conf_path, "r", encoding="utf-8") as f:
            conf_content = f.read()

        return {
            "name": name,
            "conf": conf_content,
            "script_path": script_path,
            "exists": True
        }

    def list_sessions(self):
        """列出所有保存的会话"""
        sessions = []
        for f in os.listdir(self.conf_dir):
            if f.endswith(".conf"):
                sessions.append(f[:-5])  # 去掉.conf
        return sessions

persister = SessionPersister()
config = {
    "CDP_PORT": "9222",
    "SESSION_NAME": "price-monitor",
    "N8N_WEBHOOK_URL": "https://n8n.example.com/webhook/xxx",
    "CHECK_INTERVAL": "1800"
}
script = '''#!/usr/bin/env python3
"""价格监控会话"""
import os, sys, time
sys.path.insert(0, "/app")
from lib.browser import ab, find_ref, send_webhook, make_logger

logger = make_logger(os.environ.get("SESSION_NAME", "default"))

def run():
    port = int(os.environ.get("CDP_PORT", 9222))
    ab(port, "open", "https://shop.example.com/product/123")
    time.sleep(5)
    snap = ab(port, "snapshot")
    price_ref = find_ref(snap, "价格")
    if price_ref:
        price_text = find_ref(snap, "价格", extract=True)
        logger.info(f"当前价格：{price_text}")
        send_webhook(os.environ["N8N_WEBHOOK_URL"], {"price": price_text})

if __name__ == "__main__":
    run()
'''

persister.save_session("price-monitor", config, script)
print("\n已保存的会话：", persister.list_sessions())
```

## 代码示例 (python)

```python
import requests
import json

class WebhookNotifier:
    """Webhook通知器（专业版）"""

    def __init__(self):
        self.channels = {}

    def register(self, name, url, channel_type="generic"):
        """注册通知渠道"""
        self.channels[name] = {"url": url, "type": channel_type}
        print(f"已注册渠道：{name}（{channel_type}）")

    def notify(self, channel_name, title, content, **kwargs):
        """发送通知"""
        if channel_name not in self.channels:
            print(f"渠道 {channel_name} 未注册")
            return False

        channel = self.channels[channel_name]
        url = channel["url"]
        channel_type = channel["type"]

        try:
            if channel_type == "slack":
                return self._send_slack(url, title, content)
            elif channel_type == "feishu":
                return self._send_feishu(url, title, content)
            elif channel_type == "wechat":
                return self._send_wechat(url, title, content)
            elif channel_type == "email":
                return self._send_email(url, title, content)
            else:
                return self._send_generic(url, title, content)
        except Exception as e:
            print(f"通知失败：{e}")
            return False

    def _send_slack(self, url, title, content):
        """Slack通知"""
        payload = {
            "text": f"*{title}*\n{content}",
            "username": "bsession-bot"
        }
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200

    def _send_feishu(self, url, title, content):
        """飞书通知"""
        payload = {
            "msg_type": "text",
            "content": {"text": f"{title}\n{content}"}
        }
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200

    def _send_wechat(self, url, title, content):
        """企业微信通知"""
        payload = {
            "msgtype": "text",
            "text": {"content": f"{title}\n{content}"}
        }
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200

    def _send_email(self, url, title, content):
        """邮件通知（通过Webhook API）"""
        payload = {"subject": title, "body": content}
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200

    def _send_generic(self, url, title, content):
        """通用Webhook"""
        payload = {"title": title, "content": content, "timestamp": str(time.time())}
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200

notifier = WebhookNotifier()
notifier.register("slack-alerts", "REDACTED-SECRET", "slack")
notifier.register("feishu-alerts", "https://open.feishu.cn/open-apis/bot/v2/hook/xxx", "feishu")
notifier.register("wechat-alerts", "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx", "wechat")

notifier.notify("slack-alerts", "价格变化", "商品123价格从¥99调整为¥89")
notifier.notify("feishu-alerts", "任务失败", "会话 price-monitor 执行超时")
```

## 代码示例 (python)

```python
import time
import threading
from datetime import datetime

class RecurringSession:
    """定时会话任务（专业版）"""

    def __init__(self, name, interval=1800, webhook_url=None):
        self.name = name
        self.interval = interval  # 秒
        self.webhook_url = webhook_url
        self.last_state = None
        self.running = False
        self.thread = None

    def start(self):
        """启动定时任务"""
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()
        print(f"[{self.name}] 定时任务已启动，间隔 {self.interval}s")

    def stop(self):
        """停止定时任务"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print(f"[{self.name}] 定时任务已停止")

    def _loop(self):
        """循环执行"""
        while self.running:
            try:
                current_state = self._fetch_and_parse()
                if self.last_state is None:
                    self.last_state = current_state
                    print(f"[{self.name}] 初始化状态")
                elif current_state != self.last_state:
                    self._on_change(self.last_state, current_state)
                    self.last_state = current_state
                else:
                    print(f"[{self.name}] {datetime.now().strftime('%H:%M:%S')} 状态无变化")
            except Exception as e:
                print(f"[{self.name}] 执行失败：{e}")
                self._send_alert(f"任务失败：{e}")

            time.sleep(self.interval)

    def _fetch_and_parse(self):
        """抓取并解析页面（需子类实现）"""
        result = bsession_fetch("https://shop.example.com/product/123")
        return result.get("content", "")[:500]

    def _on_change(self, old_state, new_state):
        """状态变化处理"""
        message = f"[{self.name}] 检测到状态变化\n旧：{old_state[:100]}\n新：{new_state[:100]}"
        print(message)
        if self.webhook_url:
            self._send_webhook(message)

    def _send_webhook(self, message):
        """发送Webhook通知"""
        import requests
        payload = {"text": message, "session": self.name}
        try:
            requests.post(self.webhook_url, json=payload, timeout=10)
            print(f"[{self.name}] Webhook已发送")
        except Exception as e:
            print(f"[{self.name}] Webhook失败：{e}")

    def _send_alert(self, message):
        """发送告警"""
        self._send_webhook(f"[ALERT] {message}")

session = RecurringSession(
    name="price-monitor",
    interval=1800,
    webhook_url="REDACTED-SECRET"
)
session.start()
```

## 代码示例 (python)

```python
import concurrent.futures

class BatchSessionManager:
    """批量会话管理器（专业版）"""

    def __init__(self, max_workers=3):
        self.max_workers = max_workers
        self.sessions = {}
        self.stats = {}

    def register_session(self, name, config):
        """注册会话"""
        self.sessions[name] = config
        self.stats[name] = {"runs": 0, "success": 0, "failed": 0}

    def run_all(self):
        """批量运行所有会话"""
        print(f"启动 {len(self.sessions)} 个会话，并发数 {self.max_workers}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._run_session, name, config): name
                for name, config in self.sessions.items()
            }

            for future in concurrent.futures.as_completed(futures):
                name = futures[future]
                try:
                    result = future.result()
                    self.stats[name]["runs"] += 1
                    if result.get("success"):
                        self.stats[name]["success"] += 1
                    else:
                        self.stats[name]["failed"] += 1
                except Exception as e:
                    print(f"会话 {name} 异常：{e}")
                    self.stats[name]["failed"] += 1

        self._print_stats()

    def _run_session(self, name, config):
        """运行单个会话"""
        print(f"[{name}] 开始执行...")
        try:
            result = subprocess.run(
                ["docker", "exec", "agent-browser", "bsession", "run", name],
                capture_output=True, text=True, timeout=config.get("timeout", 300)
            )
            success = result.returncode == 0
            print(f"[{name}] 执行{'成功' if success else '失败'}")
            return {"success": success, "output": result.stdout}
        except subprocess.TimeoutExpired:
            print(f"[{name}] 执行超时")
            return {"success": False, "error": "timeout"}

    def _print_stats(self):
        """打印统计"""
        print("\n=== 批量执行统计 ===")
        for name, stats in self.stats.items():
            total = stats["runs"]
            success = stats["success"]
            print(f"{name}: {success}/{total} 成功")

manager = BatchSessionManager(max_workers=3)
manager.register_session("price-monitor", {"timeout": 60})
manager.register_session("stock-check", {"timeout": 90})
manager.register_session("news-digest", {"timeout": 120})
manager.run_all()
```

