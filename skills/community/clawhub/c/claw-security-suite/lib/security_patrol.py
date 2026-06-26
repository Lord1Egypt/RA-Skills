#!/usr/bin/env python3
"""
claw-security-suite
第四层：定期安全巡检
每日自动巡检、每周全量扫描、基线完整性保护
"""

import os
import hashlib
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

try:
    from .static_scanner import StaticScanner, ScanResult
    from .logic_auditor import LogicAuditor, AuditResult
except ImportError:
    # 当直接运行脚本时，添加父目录到路径并绝对导入
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from lib.static_scanner import StaticScanner, ScanResult
    from lib.logic_auditor import LogicAuditor, AuditResult

BASELINE_FILE = "/app/working/security/baseline.json"
REPORT_DIR = "/app/working/logs/security/"

@dataclass
class FileBaseline:
    path: str
    hash: str
    last_checked: str

@dataclass
class PatrolResult:
    timestamp: str
    files_checked: int
    changes_detected: int
    issues_found: int
    details: List[str]
    
    def to_dict(self):
        return asdict(self)

class SecurityPatrol:
    def __init__(self):
        os.makedirs(REPORT_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(BASELINE_FILE), exist_ok=True)
    
    def compute_hash(self, filepath: str) -> Optional[str]:
        """计算文件hash"""
        if not os.path.isfile(filepath):
            return None
        try:
            hasher = hashlib.sha256()
            with open(filepath, 'rb') as f:
                while chunk := f.read(65536):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return None
    
    def load_baseline(self) -> Dict[str, FileBaseline]:
        """加载基线"""
        if not os.path.exists(BASELINE_FILE):
            return {}
        try:
            with open(BASELINE_FILE, 'r') as f:
                data = json.load(f)
            return {k: FileBaseline(**v) for k, v in data.items()}
        except Exception:
            return {}
    
    def save_baseline(self, baseline: Dict[str, FileBaseline]):
        """保存基线"""
        data = {k: asdict(v) for k, v in baseline.items()}
        with open(BASELINE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def daily_patrol(self, skills_dir: str = "/app/working/skills") -> PatrolResult:
        """每日巡检：检查核心文件完整性"""
        baseline = self.load_baseline()
        changes_detected = 0
        issues_found = 0
        details = []
        files_checked = 0
        
        # 扫描skills目录下的核心文件
        for root, dirs, files in os.walk(skills_dir):
            for f in files:
                if f.endswith('.py') or f == 'SKILL.md' or f == '_meta.json':
                    fullpath = os.path.join(root, f)
                    files_checked += 1
                    current_hash = self.compute_hash(fullpath)
                    
                    if fullpath in baseline:
                        if baseline[fullpath].hash != current_hash:
                            changes_detected += 1
                            details.append(f"⚠️  文件已变更: {fullpath}")
                    else:
                        # 新文件，静态扫描
                        scanner = StaticScanner()
                        issues = scanner.scan_file(fullpath)
                        if issues:
                            high = sum(1 for i in issues if "危险：" in i)
                            if high > 0:
                                issues_found += 1
                                details.append(f"❌ 新文件 {fullpath} 包含高危问题: {issues}")
                    
                    # 更新基线
                    baseline[fullpath] = FileBaseline(
                        path=fullpath,
                        hash=current_hash,
                        last_checked=datetime.utcnow().isoformat()
                    )
        
        self.save_baseline(baseline)
        
        result = PatrolResult(
            timestamp=datetime.utcnow().isoformat(),
            files_checked=files_checked,
            changes_detected=changes_detected,
            issues_found=issues_found,
            details=details
        )
        
        # 保存报告
        date_str = datetime.now().strftime("%Y%m%d")
        report_path = os.path.join(REPORT_DIR, f"daily_patrol_{date_str}.json")
        with open(report_path, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
        
        return result
    
    def weekly_scan(self, skills_dir: str = "/app/working/skills") -> Dict:
        """每周全量扫描：全量静态扫描+逻辑审计"""
        print("Starting weekly full security scan...")
        
        static_scanner = StaticScanner()
        static_result = static_scanner.scan_directory(skills_dir)
        
        logic_auditor = LogicAuditor()
        audit_result = logic_auditor.audit_directory(skills_dir)
        
        date_str = datetime.now().strftime("%Y%m%d")
        report_path = os.path.join(REPORT_DIR, f"weekly_scan_{date_str}.json")
        
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "static_scan": {
                "is_safe": static_result.is_safe,
                "high_risk_count": static_result.high_risk_count,
                "medium_risk_count": static_result.medium_risk_count,
                "issues": static_result.issues
            },
            "logic_audit": {
                "is_safe": audit_result.is_safe,
                "findings": [asdict(f) for f in audit_result.findings]
            }
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Weekly scan complete, report saved to {report_path}")
        return report
    
    def get_report_path(self):
        return REPORT_DIR

# 对外接口
def daily_patrol() -> PatrolResult:
    patrol = SecurityPatrol()
    return patrol.daily_patrol()

def weekly_scan() -> Dict:
    patrol = SecurityPatrol()
    return patrol.weekly_scan()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python security_patrol.py daily   - Run daily patrol")
        print("  python security_patrol.py weekly  - Run weekly full scan")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == 'daily':
        result = daily_patrol()
        print(f"✅ Daily patrol complete")
        print(f"  Files checked: {result.files_checked}")
        print(f"  Changes detected: {result.changes_detected}")
        print(f"  Issues found: {result.issues_found}")
        if result.details:
            print("\nDetails:")
            for d in result.details:
                print(f"  {d}")
    elif cmd == 'weekly':
        result = weekly_scan()
        static = result['static_scan']
        audit = result['logic_audit']
        print(f"\nStatic scan: {'✅ PASS' if static['is_safe'] else '❌ FAIL'}")
        print(f"  High risk: {static['high_risk_count']}, Medium: {static['medium_risk_count']}")
        print(f"\nLogic audit: {'✅ PASS' if audit['is_safe'] else '❌ FAIL'}")
        print(f"  Findings: {len(audit['findings'])}")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
