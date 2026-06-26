#!/usr/bin/env python3
"""
🛡️ agent-defender Pre-Execution Guard
=====================================
在执行外部代码/Skill 前进行安全扫描，发现恶意代码立即阻断

使用方式:
    python3 pre_exec_guard.py scan "code here"
    python3 pre_exec_guard.py scan-file /path/to/file
    python3 pre_exec_guard.py check-skill /path/to/skill
    python3 pre_exec_guard.py status
"""

import sys
import json
import argparse
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))
from scanner_v2 import DefenderScanner


class PreExecGuard:
    """执行前安全扫描"""
    
    def __init__(self):
        self.scanner = DefenderScanner()
        self.scanner.load_rules()
        self.audit_log = Path(__file__).parent / "logs" / "pre_exec_audit.jsonl"
        self.audit_log.parent.mkdir(exist_ok=True)
    
    def scan_code(self, code: str) -> dict:
        """扫描代码字符串"""
        result = self.scanner.detect(code)
        
        # 审计日志
        self._log({
            "type": "code_scan",
            "input_length": len(code),
            "result": result
        })
        
        return result
    
    def scan_file(self, file_path: str) -> dict:
        """扫描文件"""
        path = Path(file_path)
        if not path.exists():
            return {"error": f"文件不存在: {file_path}"}
        
        result = self.scanner.scan_file(path)
        
        self._log({
            "type": "file_scan",
            "file": str(file_path),
            "result": result
        })
        
        return result
    
    def scan_skill(self, skill_path: str) -> dict:
        """扫描整个 Skill 目录"""
        skill_dir = Path(skill_path)
        if not skill_dir.exists():
            return {"error": f"Skill 目录不存在: {skill_path}"}
        
        # 扫描关键文件
        scan_targets = [
            skill_dir / "SKILL.md",
            skill_dir / "README.md",
        ]
        
        # 扫描所有代码文件
        for pattern in ["*.py", "*.sh", "*.js", "*.ts"]:
            scan_targets.extend(skill_dir.glob(f"**/{pattern}"))
        
        results = {
            "skill_path": str(skill_path),
            "files_scanned": 0,
            "malicious_files": [],
            "safe_files": [],
            "overall_risk": "SAFE"
        }
        
        for target in scan_targets:
            if not target.exists():
                continue
            
            if target.is_file():
                result = self.scanner.scan_file(target)
                results["files_scanned"] += 1
                
                if result.get("is_malicious"):
                    results["malicious_files"].append({
                        "file": str(target.relative_to(skill_dir)),
                        "risk_level": result.get("risk_level"),
                        "risk_score": result.get("risk_score"),
                        "threats": result.get("threats", [])
                    })
                    results["overall_risk"] = result.get("risk_level", "HIGH")
                else:
                    results["safe_files"].append(str(target.relative_to(skill_dir)))
        
        self._log({
            "type": "skill_scan",
            "skill": str(skill_path),
            "result": results
        })
        
        return results
    
    def should_block(self, result: dict) -> tuple:
        """判断是否应该阻断"""
        if "error" in result:
            return False, f"扫描错误: {result['error']}"
        
        if result.get("is_malicious"):
            risk_level = result.get("risk_level", "UNKNOWN")
            risk_score = result.get("risk_score", 0)
            
            # CRITICAL/HIGH 风险直接阻断
            if risk_level in ["CRITICAL", "HIGH"]:
                return True, f"阻断: {risk_level} 风险 ({risk_score}) - {result.get('reason', '')}"
            
            # MEDIUM 风险警告但允许（可配置）
            if risk_level == "MEDIUM":
                return False, f"警告: MEDIUM 风险 - {result.get('reason', '')}"
        
        return False, "安全扫描通过"
    
    def _log(self, entry: dict):
        """写审计日志"""
        import datetime
        entry["timestamp"] = datetime.datetime.now().isoformat()
        with open(self.audit_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="🛡️ Pre-Execution Guard")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # scan 命令
    scan_parser = subparsers.add_parser("scan", help="扫描代码字符串")
    scan_parser.add_argument("code", help="要扫描的代码")
    scan_parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    # scan-file 命令
    file_parser = subparsers.add_parser("scan-file", help="扫描文件")
    file_parser.add_argument("path", help="文件路径")
    file_parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    # check-skill 命令
    skill_parser = subparsers.add_parser("check-skill", help="扫描 Skill 目录")
    skill_parser.add_argument("path", help="Skill 目录路径")
    skill_parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    # status 命令
    subparsers.add_parser("status", help="查看状态")
    
    args = parser.parse_args()
    
    guard = PreExecGuard()
    
    if args.command == "scan":
        result = guard.scan_code(args.code)
        block, msg = guard.should_block(result)
        
        if args.json:
            print(json.dumps({"result": result, "block": block, "message": msg}, ensure_ascii=False))
        else:
            if result.get("is_malicious"):
                print(f"⚠️  恶意代码检测")
                print(f"   风险等级: {result.get('risk_level')}")
                print(f"   风险评分: {result.get('risk_score')}")
                print(f"   原因: {result.get('reason')}")
                for threat in result.get("threats", [])[:3]:
                    print(f"   - {threat.get('category')}: {threat.get('rule_id')}")
            else:
                print(f"✅ 安全代码")
    
    elif args.command == "scan-file":
        result = guard.scan_file(args.path)
        block, msg = guard.should_block(result)
        
        if args.json:
            print(json.dumps({"result": result, "block": block, "message": msg}, ensure_ascii=False))
        else:
            if result.get("is_malicious"):
                print(f"⚠️  恶意文件: {args.path}")
                print(f"   风险等级: {result.get('risk_level')}")
            else:
                print(f"✅ 安全文件: {args.path}")
    
    elif args.command == "check-skill":
        result = guard.scan_skill(args.path)
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(f"\n🛡️ Skill 安全扫描: {args.path}")
            print(f"   扫描文件: {result.get('files_scanned')}")
            print(f"   恶意文件: {len(result.get('malicious_files', []))}")
            print(f"   安全文件: {len(result.get('safe_files', []))}")
            print(f"   总体风险: {result.get('overall_risk')}")
            
            if result.get("malicious_files"):
                print(f"\n⚠️  恶意文件列表:")
                for f in result["malicious_files"]:
                    print(f"   - {f['file']} ({f['risk_level']})")
    
    elif args.command == "status":
        print(f"✅ Pre-Execution Guard 就绪")
        print(f"   扫描器: {guard.scanner.__class__.__name__}")
        print(f"   审计日志: {guard.audit_log}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
