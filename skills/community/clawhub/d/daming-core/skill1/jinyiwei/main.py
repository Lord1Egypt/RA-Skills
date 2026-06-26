"""
锦衣卫 - 巡查、记录、预警
负责巡查系统运行，记录关键事件，发出预警
"""

import json
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from ..config import ACTIVE_TASKS_DIR, LOCAL_LOGS_DIR


class JinYiWei:
    """锦衣卫 - 巡查预警系统"""
    
    def __init__(self):
        self.patrol_logs = []
        self.alert_thresholds = {
            "task_count": 50,  # 最大活跃任务数
            "token_usage_rate": 0.8,  # Token使用率阈值
            "failed_audits": 3,  # 连续失败审核数
            "execution_timeout": 3600  # 执行超时时间（秒）
        }
    
    def patrol_system(self) -> Dict:
        """
        巡查系统
        返回巡查报告
        """
        patrol_report = {
            "patrol_id": self._generate_patrol_id(),
            "patrol_started": datetime.now().isoformat(),
            "patrol_areas": [],
            "findings": [],
            "alerts": [],
            "recommendations": [],
            "overall_status": "normal"
        }
        
        try:
            # 巡查区域1：三省状态
            patrol_report["patrol_areas"].append("三省状态")
            self._patrol_sansheng(patrol_report)
            
            # 巡查区域2：六部运行
            patrol_report["patrol_areas"].append("六部运行")
            self._patrol_liubu(patrol_report)
            
            # 巡查区域3：任务执行
            patrol_report["patrol_areas"].append("任务执行")
            self._patrol_tasks(patrol_report)
            
            # 巡查区域4：文件完整性
            patrol_report["patrol_areas"].append("文件完整性")
            self._patrol_file_integrity(patrol_report)
            
            # 巡查区域5：资源使用
            patrol_report["patrol_areas"].append("资源使用")
            self._patrol_resource_usage(patrol_report)
            
            # 确定总体状态
            if patrol_report["alerts"]:
                patrol_report["overall_status"] = "warning"
            if len(patrol_report["alerts"]) > 3:
                patrol_report["overall_status"] = "critical"
            
        except Exception as e:
            patrol_report["overall_status"] = "error"
            patrol_report["error"] = str(e)
        
        patrol_report["patrol_completed"] = datetime.now().isoformat()
        
        # 记录巡查日志
        self._record_patrol_log(patrol_report)
        
        return patrol_report
    
    def _patrol_sansheng(self, report: Dict) -> None:
        """巡查三省状态"""
        findings = []
        
        # 检查中书省
        try:
            from ..zhongshu.main import get_recent_tasks
            recent_tasks = get_recent_tasks(limit=10)
            findings.append({
                "area": "中书省",
                "status": "正常",
                "recent_tasks": len(recent_tasks)
            })
        except Exception as e:
            findings.append({
                "area": "中书省",
                "status": "异常",
                "error": str(e)
            })
            report["alerts"].append("中书省功能异常")
        
        # 检查门下省
        try:
            from ..menxia.main import get_audit_stats
            audit_stats = get_audit_stats()
            findings.append({
                "area": "门下省",
                "status": "正常",
                "pass_rate": audit_stats.get("pass_rate", 0)
            })
        except Exception as e:
            findings.append({
                "area": "门下省",
                "status": "异常",
                "error": str(e)
            })
            report["alerts"].append("门下省功能异常")
        
        # 检查尚书省
        try:
            from ..shangshu.main import ShangShu
            shangshu = ShangShu()
            findings.append({
                "area": "尚书省",
                "status": "正常",
                "description": "六部协调机构"
            })
        except Exception as e:
            findings.append({
                "area": "尚书省",
                "status": "异常",
                "error": str(e)
            })
            report["alerts"].append("尚书省功能异常")
        
        report["findings"].extend(findings)
    
    def _patrol_liubu(self, report: Dict) -> None:
        """巡查六部运行"""
        findings = []
        
        # 六部列表
        bu_list = ["hu", "gong", "bing", "xing", "li_bu"]
        
        for bu in bu_list:
            try:
                module_name = f"..bu.{bu}.main"
                module = __import__(module_name, fromlist=[''])
                
                # 检查模块是否可用
                findings.append({
                    "area": f"{bu}部",
                    "status": "正常",
                    "available": True
                })
            except Exception as e:
                findings.append({
                    "area": f"{bu}部",
                    "status": "异常",
                    "available": False,
                    "error": str(e)
                })
                report["alerts"].append(f"{bu}部模块异常")
        
        report["findings"].extend(findings)
    
    def _patrol_tasks(self, report: Dict) -> None:
        """巡查任务执行"""
        if not ACTIVE_TASKS_DIR.exists():
            report["findings"].append({
                "area": "任务目录",
                "status": "正常",
                "active_tasks": 0
            })
            return
        
        task_dirs = [d for d in ACTIVE_TASKS_DIR.iterdir() if d.is_dir()]
        active_tasks = len(task_dirs)
        
        report["findings"].append({
            "area": "活跃任务",
            "status": "正常" if active_tasks <= self.alert_thresholds["task_count"] else "警告",
            "active_tasks": active_tasks,
            "threshold": self.alert_thresholds["task_count"]
        })
        
        if active_tasks > self.alert_thresholds["task_count"]:
            report["alerts"].append(f"活跃任务数量过多: {active_tasks}")
        
        # 检查任务状态
        status_counts = {}
        for task_dir in task_dirs[:10]:  # 只检查前10个任务
            task_file = task_dir / "task_draft.json"
            if task_file.exists():
                try:
                    with open(task_file, 'r', encoding='utf-8') as f:
                        task_data = json.load(f)
                    status = task_data.get("status", "unknown")
                    status_counts[status] = status_counts.get(status, 0) + 1
                except:
                    pass
        
        report["findings"].append({
            "area": "任务状态分布",
            "status_counts": status_counts
        })
    
    def _patrol_file_integrity(self, report: Dict) -> None:
        """巡查文件完整性"""
        findings = []
        
        # 检查关键目录
        critical_dirs = [
            ACTIVE_TASKS_DIR,
            LOCAL_LOGS_DIR,
            Path(__file__).parent.parent / "config"
        ]
        
        for dir_path in critical_dirs:
            if dir_path.exists():
                findings.append({
                    "area": f"目录检查: {dir_path.name}",
                    "status": "正常",
                    "exists": True
                })
            else:
                findings.append({
                    "area": f"目录检查: {dir_path.name}",
                    "status": "异常",
                    "exists": False
                })
                report["alerts"].append(f"关键目录不存在: {dir_path}")
        
        # 检查关键文件
        critical_files = [
            Path(__file__).parent.parent / "config.py",
            ACTIVE_TASKS_DIR / ".gitkeep" if ACTIVE_TASKS_DIR.exists() else None
        ]
        
        for file_path in critical_files:
            if file_path and file_path.exists():
                # 计算文件哈希
                try:
                    file_hash = self._calculate_file_hash(file_path)
                    findings.append({
                        "area": f"文件检查: {file_path.name}",
                        "status": "正常",
                        "hash": file_hash[:8]
                    })
                except Exception as e:
                    findings.append({
                        "area": f"文件检查: {file_path.name}",
                        "status": "异常",
                        "error": str(e)
                    })
        
        report["findings"].extend(findings)
    
    def _patrol_resource_usage(self, report: Dict) -> None:
        """巡查资源使用"""
        findings = []
        
        # 检查Token使用情况
        total_tokens = 0
        used_tokens = 0
        
        if ACTIVE_TASKS_DIR.exists():
            for task_dir in ACTIVE_TASKS_DIR.iterdir():
                if task_dir.is_dir():
                    ledger_file = task_dir / "token_ledger.json"
                    if ledger_file.exists():
                        try:
                            with open(ledger_file, 'r', encoding='utf-8') as f:
                                ledger = json.load(f)
                            total_tokens += ledger.get("initial_budget", 0)
                            used_tokens += ledger.get("used_tokens", 0)
                        except:
                            pass
        
        if total_tokens > 0:
            usage_rate = used_tokens / total_tokens
            findings.append({
                "area": "Token使用率",
                "status": "正常" if usage_rate <= self.alert_thresholds["token_usage_rate"] else "警告",
                "usage_rate": round(usage_rate, 2),
                "threshold": self.alert_thresholds["token_usage_rate"]
            })
            
            if usage_rate > self.alert_thresholds["token_usage_rate"]:
                report["alerts"].append(f"Token使用率过高: {usage_rate:.2%}")
        
        report["findings"].extend(findings)
    
    def _generate_patrol_id(self) -> str:
        """生成巡查ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"PATROL_{timestamp}"
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """计算文件哈希值"""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()
    
    def _record_patrol_log(self, patrol_report: Dict) -> None:
        """记录巡查日志"""
        patrol_log_file = LOCAL_LOGS_DIR / "jinyiwei_patrols.json"
        
        patrol_logs = []
        if patrol_log_file.exists():
            with open(patrol_log_file, 'r', encoding='utf-8') as f:
                patrol_logs = json.load(f)
        
        patrol_logs.append(patrol_report)
        
        # 只保留最近50次巡查记录
        if len(patrol_logs) > 50:
            patrol_logs = patrol_logs[-50:]
        
        with open(patrol_log_file, 'w', encoding='utf-8') as f:
            json.dump(patrol_logs, f, ensure_ascii=False, indent=2)
        
        self.patrol_logs.append(patrol_report)
    
    def get_recent_patrols(self, limit: int = 10) -> List[Dict]:
        """获取最近巡查记录"""
        patrol_log_file = LOCAL_LOGS_DIR / "jinyiwei_patrols.json"
        
        if patrol_log_file.exists():
            with open(patrol_log_file, 'r', encoding='utf-8') as f:
                patrol_logs = json.load(f)
            return patrol_logs[-limit:] if patrol_logs else []
        return []
    
    def check_alert_conditions(self) -> List[str]:
        """检查预警条件"""
        alerts = []
        
        # 获取最近巡查报告
        recent_patrols = self.get_recent_patrols(limit=5)
        
        for patrol in recent_patrols:
            if patrol.get("overall_status") in ["warning", "critical"]:
                alerts.append(f"巡查发现异常: {patrol.get('patrol_id')}")
        
        return alerts


def create_jinyiwei() -> JinYiWei:
    """创建锦衣卫实例"""
    return JinYiWei()


def patrol_system() -> Dict:
    """巡查系统（对外接口）"""
    jinyiwei = JinYiWei()
    return jinyiwei.patrol_system()


def get_system_status() -> Dict:
    """获取系统状态"""
    jinyiwei = JinYiWei()
    
    # 获取最近巡查
    recent_patrols = jinyiwei.get_recent_patrols(limit=3)
    
    # 检查预警
    alerts = jinyiwei.check_alert_conditions()
    
    return {
        "status_checked_at": datetime.now().isoformat(),
        "recent_patrols": [p.get("patrol_id") for p in recent_patrols],
        "active_alerts": alerts,
        "system_status": "normal" if not alerts else "warning"
    }


def get_security_logs(limit: int = 10) -> list:
    """获取安全日志"""
    security_log_file = LOCAL_LOGS_DIR / "security_events.json"
    
    if not security_log_file.exists():
        return []
    
    with open(security_log_file, 'r', encoding='utf-8') as f:
        security_events = json.load(f)
    
    return security_events[-limit:]


if __name__ == "__main__":
    print("🏛️ 锦衣卫功能测试")
    result = monitor_security_events()
    print(f"✅ 安全监控完成: {result['status']}")
