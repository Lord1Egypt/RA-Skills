# 详细参考 - cron-guard-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import subprocess
import logging
import time
from datetime import datetime
from pathlib import Path

class CronGuard:
    """定时任务安全防护（免费版核心）"""

    def __init__(self, log_dir="cron_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            filename=self.log_dir / 'guard.log',
            encoding='utf-8'
        )
        self.logger = logging.getLogger(__name__)

    def execute_guarded(self, script_path, timeout=300, max_retries=1,
                        retry_delay=10, on_failure="alert"):
        """带防护栏的执行"""
        self.logger.info(f"=== 开始执行：{script_path} ===")

        pre_check = self._pre_check(script_path)
        if not pre_check["passed"]:
            self.logger.error(f"预检查失败：{pre_check['reason']}")
            return self._handle_failure(script_path, pre_check["reason"], on_failure)

        for attempt in range(max_retries + 1):
            success, output = self._run_with_timeout(script_path, timeout)

            if success:
                self.logger.info(f"执行成功（第{attempt+1}次尝试）")
                self._log_success(script_path, output)
                return True

            self.logger.warning(f"第{attempt+1}次失败：{output}")

            if attempt < max_retries:
                self.logger.info(f"等待{retry_delay}秒后重试...")
                time.sleep(retry_delay)

        return self._handle_failure(script_path, output, on_failure)

    def _pre_check(self, script_path):
        """预检查：路径、权限、依赖"""
        path = Path(script_path)

        if not path.exists():
            return {"passed": False, "reason": f"文件不存在：{script_path}"}

        if not path.stat().st_mode & 0o111:
            return {"passed": False, "reason": f"无执行权限：{script_path}"}

        return {"passed": True, "reason": ""}

    def _run_with_timeout(self, script_path, timeout):
        """带超时执行"""
        try:
            result = subprocess.run(
                ["bash", str(script_path)],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, f"退出码{result.returncode}: {result.stderr}"
        except subprocess.TimeoutExpired:
            return False, f"超时（{timeout}秒）"
        except Exception as e:
            return False, str(e)

    def _handle_failure(self, script_path, error, strategy):
        """异常恢复策略"""
        self.logger.error(f"执行失败：{script_path} - {error}")

        if strategy == "retry":
            self.logger.info("策略：重试（已在上层处理）")
        elif strategy == "skip":
            self.logger.info("策略：跳过本次执行")
        elif strategy == "degrade":
            self.logger.info("策略：降级执行（使用备用方案）")
        elif strategy == "alert":
            self.logger.error("策略：发送告警通知")
            self._send_alert(script_path, error)

        return False

    def _send_alert(self, script_path, error):
        """发送告警（简化版）"""
        alert_msg = f"""
        [定时任务告警]
        脚本：{script_path}
        时间：{datetime.now().isoformat()}
        错误：{error}
        请及时检查处理。
        """
        alert_file = self.log_dir / "alerts.log"
        alert_file.write_text(alert_msg, encoding="utf-8", errors="ignore")
        print(alert_msg)

    def _log_success(self, script_path, output):
        """记录成功日志"""
        log_entry = {
            "script": script_path,
            "time": datetime.now().isoformat(),
            "status": "success",
            "output_preview": output[:200] if output else ""
        }
        success_log = self.log_dir / "success.json"
        import json
        logs = json.loads(success_log.read_text(encoding="utf-8")) if success_log.exists() else []
        logs.append(log_entry)
        success_log.write_text(json.dumps(logs, ensure_ascii=False, indent=2), encoding="utf-8")

guard = CronGuard(log_dir="/tmp/cron_logs")

guard.execute_guarded(
    script_path="/opt/scripts/backup.sh",
    timeout=600,
    max_retries=2,
    retry_delay=30,
    on_failure="alert"
)
```

