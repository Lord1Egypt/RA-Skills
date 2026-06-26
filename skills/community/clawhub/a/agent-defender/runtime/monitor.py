#!/usr/bin/env python3
"""
运行时实时行为防护模块
"""
import os
import json
import time
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

# 运行时行为规则
RUNTIME_RULES = {
    "syscall": [
        {"id": "R001", "name": "危险Shell执行", "pattern": r"execve|fork|clone", "risk": "CRITICAL"},
        {"id": "R002", "name": "批量删除", "pattern": r"rm -rf|del /f /s", "risk": "HIGH"},
    ],
    "file": [
        {"id": "R003", "name": "敏感路径访问", "pattern": r"/etc/passwd|~/.ssh/|C:\\Windows\\System32", "risk": "HIGH"},
        {"id": "R004", "name": "持久化配置", "pattern": r"cron|systemd|registry", "risk": "HIGH"},
    ],
    "network": [
        {"id": "R005", "name": "异常外发", "pattern": r"beacon|exfil|long-poll", "risk": "CRITICAL"},
    ]
}

class RuntimeMonitor:
    """运行时监控器"""
    
    def __init__(self):
        self.events = []
        self.counters = defaultdict(int)
        self.config = self.load_config()
    
    def load_config(self):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    
    def check_event(self, event_type, event_data):
        """检查事件"""
        results = []
        
        rules = RUNTIME_RULES.get(event_type, [])
        
        for rule in rules:
            if re.search(rule["pattern"], str(event_data), re.IGNORECASE):
                results.append({
                    "event_type": event_type,
                    "rule_id": rule["id"],
                    "name": rule["name"],
                    "risk": rule["risk"],
                    "data": event_data,
                    "timestamp": time.time()
                })
                
                # 更新计数器
                key = f"{event_type}:{rule['id']}"
                self.counters[key] += 1
        
        return results
    
    def should_block(self, results):
        """判断是否应该阻断"""
        thresholds = self.config["runtime"]["thresholds"]
        
        # 高风险直接阻断
        for r in results:
            if r["risk"] == "CRITICAL":
                return True, "CRITICAL risk detected"
        
        # 高频检测
        for count in self.counters.values():
            if count >= thresholds["high_frequency"]:
                return True, "High frequency detected"
        
        return False, None
    
    def log_event(self, event):
        """记录事件"""
        self.events.append(event)
    
    def get_summary(self):
        """获取摘要"""
        return {
            "total_events": len(self.events),
            "counters": dict(self.counters),
            "risks": self.get_risk_summary()
        }
    
    def get_risk_summary(self):
        """风险摘要"""
        summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for event in self.events:
            risk = event.get("risk", "LOW")
            if risk in summary:
                summary[risk] += 1
        return summary

def main():
    import argparse
    parser = argparse.ArgumentParser(description="运行时监控")
    parser.add_argument("--start", action="store_true", help="启动监控")
    parser.add_argument("--status", action="store_true", help="查看状态")
    
    args = parser.parse_args()
    
    monitor = RuntimeMonitor()
    
    if args.start:
        print("🚀 运行时监控已启动...")
        print("按 Ctrl+C 停止")
        try:
            while True:
                time.sleep(60)
                print(".", end="", flush=True)
        except KeyboardInterrupt:
            print("\n\n监控摘要:")
            print(json.dumps(monitor.get_summary(), indent=2))
    
    elif args.status:
        print("监控状态:")
        print(json.dumps(monitor.get_summary(), indent=2))
    
    else:
        print("用法:")
        print("  --start   启动监控")
        print("  --status  查看状态")

if __name__ == "__main__":
    main()
