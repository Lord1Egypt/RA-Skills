#!/usr/bin/env python3
"""
增强版成本追踪系统
整合 OpenClaw status 和 Claude Code 成本追踪设计
"""

import os, json, re, subprocess, time
from pathlib import Path

# 技能本地目录
SKILL_ROOT = Path(__file__).parent.parent
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict, field
from threading import Lock

MEMORY_ROOT = SKILL_ROOT / "memory"
COST_LOG_DIR = MEMORY_ROOT / "logs" / "cost"
DAILY_DIR = COST_LOG_DIR / "daily"

PRICING = {
    "MiniMax-M2.7": {"input": 0.3, "output": 1.2},
    "MiniMax-M2.7-highspeed": {"input": 0.3, "output": 1.2},
    "default": {"input": 0.3, "output": 1.2}
}

@dataclass
class SessionSnapshot:
    session_key: str
    model: str
    context_used: int
    context_max: int
    cache_percent: int
    age: str

@dataclass
class DailyCost:
    date: str
    sessions: List = field(default_factory=list)
    total_input_tokens_est: int = 0
    total_output_tokens_est: int = 0
    total_api_calls: int = 0
    estimated_cost_usd: float = 0.0
    cache_hit_percent_avg: int = 0
    active_sessions: int = 0
    tasks_active: int = 0
    notes: str = ""

class CostTracker:
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.daily = self._load_daily()
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        COST_LOG_DIR.mkdir(parents=True, exist_ok=True)
        DAILY_DIR.mkdir(parents=True, exist_ok=True)
    
    def _load_daily(self) -> DailyCost:
        today = datetime.now().strftime("%Y-%m-%d")
        daily_file = DAILY_DIR / f"{today}.json"
        if daily_file.exists():
            try:
                return DailyCost(**json.loads(daily_file.read_text()))
            except:
                pass
        return DailyCost(date=today)
    
    def _save_daily(self):
        today = datetime.now().strftime("%Y-%m-%d")
        daily_file = DAILY_DIR / f"{today}.json"
        daily_file.write_text(json.dumps(asdict(self.daily), indent=2, ensure_ascii=False))
    
    def poll_sessions(self) -> List[SessionSnapshot]:
        try:
            result = subprocess.run(["openclaw", "status"], capture_output=True, text=True, timeout=30)
            output = result.stdout + result.stderr
        except Exception as e:
            print(f"Failed to get openclaw status: {e}")
            return []
        
        sessions = []
        lines = output.split('\n')
        
        # 找到 Sessions 表格
        table_start = None
        for i, line in enumerate(lines):
            if line.strip() == 'Sessions':
                table_start = i
                break
        
        if table_start is None:
            return []
        
        table_section = '\n'.join(lines[table_start:table_start+20])
        
        for line in table_section.split('\n'):
            if 'agent:' not in line or 'cached' not in line:
                continue
            
            tokens_match = re.search(r'(\d+)k/(\d+)k\s*\((\d+)%\)', line)
            cache_match = re.search(r'🗄️\s*(\d+)%', line)
            key_match = re.search(r'(agent:[^\s│]+)', line)
            model_match = re.search(r'(MiniMax[^\s│]+)', line)
            age_match = re.search(r'│\s*(\w+)\s*│\s*([^│]+?)\s*│\s*[^│]+\s*│', line)
            
            if tokens_match and cache_match and key_match:
                used_k = int(tokens_match.group(1))
                max_k = int(tokens_match.group(2))
                cache_pct = int(cache_match.group(1))
                key = key_match.group(1)
                model = model_match.group(1) if model_match else "unknown"
                age = age_match.group(2) if age_match else ""
                
                sessions.append(SessionSnapshot(
                    session_key=key.strip(),
                    model=model,
                    context_used=used_k * 1000,
                    context_max=max_k * 1000,
                    cache_percent=cache_pct,
                    age=age
                ))
        
        return sessions
    
    def capture_snapshot(self, notes: str = "") -> DailyCost:
        sessions = self.poll_sessions()
        
        if sessions:
            total_input = sum(int(s.context_used * 0.3) for s in sessions)
            total_output = sum(int(s.context_used * 0.1) for s in sessions)
            avg_cache = sum(s.cache_percent for s in sessions) // len(sessions)
            
            self.daily.total_input_tokens_est += total_input
            self.daily.total_output_tokens_est += total_output
            self.daily.total_api_calls += len(sessions)
            pricing = PRICING.get("MiniMax-M2.7-highspeed", PRICING["default"])
            self.daily.estimated_cost_usd = (
                self.daily.total_input_tokens_est / 1_000_000 * pricing["input"] +
                self.daily.total_output_tokens_est / 1_000_000 * pricing["output"]
            )
            self.daily.cache_hit_percent_avg = avg_cache
            self.daily.active_sessions = len(sessions)
            self.daily.sessions = [
                {"key": s.session_key, "model": s.model, "context": f"{s.context_used//1000}k/{s.context_max//1000}k", "cache": s.cache_percent, "age": s.age}
                for s in sessions
            ]
        
        if notes:
            self.daily.notes += f"[{datetime.now().strftime('%H:%M')}] {notes}\n"
        
        self._save_daily()
        return self.daily
    
    def get_report(self) -> str:
        d = self.daily
        lines = [
            "=" * 50,
            f"  成本追踪报告 — {d.date}",
            "=" * 50,
            f"📊 活跃会话: {d.active_sessions}",
            f"📈 Token 估算: 输入 {d.total_input_tokens_est:,} / 输出 {d.total_output_tokens_est:,}",
            f"💰 成本估算: ${d.estimated_cost_usd:.4f}",
            f"🗄️ Cache 命中率: {d.cache_hit_percent_avg}%",
            "",
        ]
        if d.sessions:
            lines.append("📋 Session 明细:")
            for s in d.sessions[:8]:
                lines.append(f"  {s['key'][-35:]} {s['context']} 🗄{s['cache']}% {s['age']}")
            if len(d.sessions) > 8:
                lines.append(f"  ... 还有 {len(d.sessions)-8} 个")
        if d.notes:
            lines.append(f"\n📝 {d.notes}")
        return "\n".join(lines)
    
    def save_report(self) -> Path:
        today = datetime.now().strftime("%Y-%m-%d")
        report_file = COST_LOG_DIR / f"report-{today}.md"
        content = f"# 成本追踪 {today}\n\n{self.get_report()}\n"
        report_file.write_text(content)
        return report_file

if __name__ == "__main__":
    import sys
    tracker = CostTracker()
    if len(sys.argv) < 2:
        print(tracker.get_report())
    elif sys.argv[1] == "capture":
        tracker.capture_snapshot(sys.argv[2] if len(sys.argv) > 2 else "")
        print(tracker.get_report())
    elif sys.argv[1] == "test":
        tracker.capture_snapshot("测试")
        print(tracker.get_report())
