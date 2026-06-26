#!/usr/bin/env python3
"""
Token Budget Real-time Monitor
Token 预算实时监控

功能：
1. 实时监控上下文使用量
2. 提前预警（80%、90% 阈值）
3. 建议压缩时机

参考 Claude Code 的 tokenBudget 设计
"""

import os
import re
import time
import subprocess
from pathlib import Path

# 技能本地目录
SKILL_ROOT = Path(__file__).parent.parent
from datetime import datetime
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass

MEMORY_ROOT = SKILL_ROOT / "memory"
BUDGET_LOG = MEMORY_ROOT / "logs" / "budget" / "budget-alerts.json"

# 上下文窗口（MiniMax-M2.7-highspeed: 205k）
CONTEXT_WINDOW = 205_000

# 预警阈值
WARNING_THRESHOLDS = [0.80, 0.90, 0.95]


@dataclass
class BudgetSnapshot:
    """预算快照"""
    timestamp: str
    session_key: str
    used_tokens: int
    max_tokens: int
    percent: float
    cache_percent: int


class TokenBudgetMonitor:
    """Token 预算监控器"""
    
    def __init__(self):
        self.last_warning_level = 0
        self.alerts: Dict[str, list] = {}
        self._load_alerts()
    
    def _load_alerts(self):
        """加载历史预警"""
        if BUDGET_LOG.exists():
            try:
                self.alerts = json.loads(BUDGET_LOG.read_text())
            except:
                pass
    
    def _save_alerts(self):
        """保存预警记录"""
        BUDGET_LOG.parent.mkdir(parents=True, exist_ok=True)
        BUDGET_LOG.write_text(json.dumps(self.alerts, indent=2))
    
    def get_context_usage(self, session_key: str = "main") -> Optional[BudgetSnapshot]:
        """获取上下文使用情况"""
        try:
            result = subprocess.run(
                ["openclaw", "status"],
                capture_output=True, text=True, timeout=30
            )
            output = result.stdout + result.stderr
            
            for line in output.split('\n'):
                if session_key in line and '/205k' in line:
                    match = re.search(r'(\d+)k/(\d+)k\s*\((\d+)%\)\s*·\s*🗄️\s*(\d+)%\s*cached', line)
                    if match:
                        used_k = int(match.group(1))
                        max_k = int(match.group(2))
                        used_pct = int(match.group(3))
                        cache_pct = int(match.group(4))
                        
                        return BudgetSnapshot(
                            timestamp=datetime.now().isoformat(),
                            session_key=session_key,
                            used_tokens=used_k * 1000,
                            max_tokens=max_k * 1000,
                            percent=used_pct / 100,
                            cache_percent=cache_pct
                        )
        except Exception as e:
            pass
        
        return None
    
    def check_budget(self, session_key: str = "main") -> Tuple[bool, str]:
        """
        检查预算，返回 (是否需要预警, 预警信息)
        """
        snapshot = self.get_context_usage(session_key)
        
        if not snapshot:
            return False, ""
        
        # 检查阈值
        current_level = 0
        warning_msg = ""
        
        for i, threshold in enumerate(WARNING_THRESHOLDS):
            if snapshot.percent >= threshold:
                current_level = i + 1
                remaining = int((1 - snapshot.percent) * snapshot.max_tokens / 1000)
                warning_msg = f"""
⚠️ Token 预算预警 ({(snapshot.percent * 100):.0f}%)

阈值: {int(threshold * 100)}%
已使用: {snapshot.used_tokens // 1000}k / {snapshot.max_tokens // 1000}k
剩余: 约 {remaining}k tokens
Cache 命中率: {snapshot.cache_percent}%

建议: {'立即压缩' if snapshot.percent >= 0.90 else '考虑压缩'}
"""
        
        # 只在级别变化时预警
        if current_level > self.last_warning_level:
            self.last_warning_level = current_level
            self._record_alert(session_key, snapshot, current_level)
            return True, warning_msg
        
        # 重置级别（如果使用率下降）
        if current_level < self.last_warning_level:
            self.last_warning_level = current_level
        
        return False, ""
    
    def _record_alert(self, session_key: str, snapshot: BudgetSnapshot, level: int):
        """记录预警"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.alerts:
            self.alerts[today] = []
        
        self.alerts[today].append({
            "timestamp": snapshot.timestamp,
            "session": session_key,
            "percent": snapshot.percent,
            "level": level
        })
        
        # 只保留最近7天
        cutoff = (datetime.now().timestamp() - 7 * 86400)
        self.alerts = {
            d: alerts for d, alerts in self.alerts.items()
            if datetime.fromisoformat(d).timestamp() > cutoff
        }
        
        self._save_alerts()
    
    def get_report(self) -> str:
        """获取完整报告"""
        snapshot = self.get_context_usage()
        
        lines = [
            "=" * 50,
            "💰 Token 预算监控",
            "=" * 50,
            "",
        ]
        
        if snapshot:
            percent = snapshot.percent * 100
            
            # 状态条
            bar_len = 30
            filled = int(bar_len * snapshot.percent)
            bar = "█" * filled + "░" * (bar_len - filled)
            
            lines.append(f"[{bar}] {percent:.1f}%")
            lines.append(f"已使用: {snapshot.used_tokens // 1000}k / {snapshot.max_tokens // 1000}k")
            lines.append(f"Cache: {snapshot.cache_percent}%")
            lines.append("")
            
            # 阈值标记
            for threshold in WARNING_THRESHOLDS:
                marker = "👆" if snapshot.percent >= threshold else ""
                lines.append(f"  {int(threshold * 100)}%: {marker}")
            
            # 建议
            if snapshot.percent >= 0.95:
                lines.append("")
                lines.append("🚨 紧急: 立即压缩上下文！")
            elif snapshot.percent >= 0.90:
                lines.append("")
                lines.append("⚠️ 警告: 建议尽快压缩")
            elif snapshot.percent >= 0.80:
                lines.append("")
                lines.append("💡 提示: 接近阈值，注意监控")
        else:
            lines.append("无法获取上下文使用情况")
        
        # 最近预警
        if self.alerts:
            lines.append("")
            lines.append("📋 最近预警:")
            for date, alerts in sorted(self.alerts.items(), reverse=True)[:3]:
                lines.append(f"  {date}: {len(alerts)} 次")
        
        return "\n".join(lines)


import json


def get_monitor() -> TokenBudgetMonitor:
    return TokenBudgetMonitor()


if __name__ == "__main__":
    import sys
    
    monitor = get_monitor()
    
    if len(sys.argv) < 2:
        print(monitor.get_report())
    else:
        cmd = sys.argv[1]
        
        if cmd == "status":
            print(monitor.get_report())
        
        elif cmd == "check":
            session = sys.argv[2] if len(sys.argv) > 2 else "main"
            needs_alert, message = monitor.check_budget(session)
            if needs_alert:
                print(message)
            else:
                print(f"✅ Token 使用正常 ({monitor.get_context_usage(session).percent * 100:.1f}%)")
        
        elif cmd == "watch":
            print("监控 Token 使用情况（Ctrl+C 退出）...")
            try:
                while True:
                    os.system('clear')
                    print(monitor.get_report())
                    time.sleep(10)
            except KeyboardInterrupt:
                print("\n退出监控")
