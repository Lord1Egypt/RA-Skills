# 详细参考 - cron-scheduler-pro-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

STORE_DIR = Path.home() / "workspace" / "scheduler" / "cron"
STORE_DIR.mkdir(parents=True, exist_ok=True)

class CronScheduler:
    """定时调度引擎（免费版核心）"""

    def __init__(self, store_dir=None):
        self.store_dir = Path(store_dir) if store_dir else STORE_DIR
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self.jobs_file = self.store_dir / "jobs.json"
        self.runs_file = self.store_dir / "runs.json"
        self._init_storage()

    def _init_storage(self):
        if not self.jobs_file.exists():
            self.jobs_file.write_text("[]", encoding="utf-8")
        if not self.runs_file.exists():
            self.runs_file.write_text("[]", encoding="utf-8")

    def _load_jobs(self):
        return json.loads(self.jobs_file.read_text(encoding="utf-8"))

    def _save_jobs(self, jobs):
        self.jobs_file.write_text(
            json.dumps(jobs, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def add_job(self, name, schedule_type, config, task):
        """添加定时任务"""
        jobs = self._load_jobs()
        job_id = f"job_{len(jobs) + 1:04d}"
        job = {
            "id": job_id,
            "name": name,
            "schedule_type": schedule_type,
            "schedule_config": config,
            "task": task,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "last_run": None,
            "next_run": self._calc_next_run(schedule_type, config)
        }
        jobs.append(job)
        self._save_jobs(jobs)
        print(f"✓ 任务已创建：{job_id} - {name}")
        print(f"  下次执行：{job['next_run']}")
        return job

    def list_jobs(self, status=None):
        """列出所有任务"""
        jobs = self._load_jobs()
        if status:
            jobs = [j for j in jobs if j["status"] == status]
        print(f"\n{'ID':<12} {'名称':<16} {'类型':<10} {'状态':<10} {'下次执行':<26}")
        print("-" * 80)
        for j in jobs:
            print(f"{j['id']:<12} {j['name']:<16} {j['schedule_type']:<10} "
                  f"{j['status']:<10} {j.get('next_run', 'N/A')}")
        print(f"\n共 {len(jobs)} 个任务")
        return jobs

    def pause_job(self, job_id):
        """暂停任务"""
        jobs = self._load_jobs()
        for j in jobs:
            if j["id"] == job_id:
                j["status"] = "paused"
                self._save_jobs(jobs)
                print(f"✓ 已暂停：{job_id} - {j['name']}")
                return
        print(f"✗ 未找到任务：{job_id}")

    def resume_job(self, job_id):
        """恢复任务"""
        jobs = self._load_jobs()
        for j in jobs:
            if j["id"] == job_id:
                j["status"] = "active"
                j["next_run"] = self._calc_next_run(
                    j["schedule_type"], j["schedule_config"])
                self._save_jobs(jobs)
                print(f"✓ 已恢复：{job_id} - {j['name']}")
                print(f"  下次执行：{j['next_run']}")
                return
        print(f"✗ 未找到任务：{job_id}")

    def archive_job(self, job_id):
        """归档任务"""
        jobs = self._load_jobs()
        for j in jobs:
            if j["id"] == job_id:
                j["status"] = "archived"
                self._save_jobs(jobs)
                print(f"✓ 已归档：{job_id} - {j['name']}")
                return
        print(f"✗ 未找到任务：{job_id}")

    def show_job(self, job_id):
        """查看任务详情"""
        jobs = self._load_jobs()
        for j in jobs:
            if j["id"] == job_id:
                print(json.dumps(j, ensure_ascii=False, indent=2))
                return j
        print(f"✗ 未找到任务：{job_id}")
        return None

    def _calc_next_run(self, schedule_type, config):
        """计算下次执行时间"""
        now = datetime.now()
        if schedule_type == "daily":
            time_str = config.get("time", "08:00")
            hour, minute = map(int, time_str.split(":"))
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
        elif schedule_type == "weekly":
            target_day = config.get("weekday", 0)  # 0=周一
            time_str = config.get("time", "08:00")
            hour, minute = map(int, time_str.split(":"))
            days_ahead = (target_day - now.weekday()) % 7
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if days_ahead == 0 and next_run <= now:
                days_ahead = 7
            next_run += timedelta(days=days_ahead)
        elif schedule_type == "monthly":
            day = config.get("day", 1)
            time_str = config.get("time", "08:00")
            hour, minute = map(int, time_str.split(":"))
            next_run = now.replace(day=day, hour=hour, minute=minute, second=0, microsecond=0)
            if next_run <= now:
                if now.month == 12:
                    next_run = next_run.replace(year=now.year + 1, month=1)
                else:
                    next_run = next_run.replace(month=now.month + 1)
        elif schedule_type == "interval":
            minutes = config.get("every_minutes", 60)
            next_run = now + timedelta(minutes=minutes)
        else:
            next_run = now + timedelta(hours=1)

        return next_run.isoformat()

scheduler = CronScheduler()

scheduler.add_job("每日晨报", "daily", {"time": "08:00"}, "生成晨报")
scheduler.add_job("每周周报", "weekly", {"weekday": 4, "time": "17:00"}, "生成周报")
scheduler.add_job("月度备份", "monthly", {"day": 1, "time": "02:00"}, "执行数据备份")
scheduler.add_job("健康检查", "interval", {"every_minutes": 30}, "检查API状态")

scheduler.list_jobs()

scheduler.pause_job("job_0004")
```

