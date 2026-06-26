#!/usr/bin/env python3
"""
金融合规审计自动化技能 - 主入口
Financial Audit Automation Skill - Main Entry
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

# 添加 modules 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

try:
    from aml_monitor import AMLDetector
    from doc_validator import DocValidator
    from report_generator import generate_audit_report
    from sandbox import secure_execute
    HAS_MODULES = True
except ImportError:
    HAS_MODULES = False

# SkillPay 配置
API_KEY = os.environ.get('SKILLPAY_API_KEY', '')
SKILL_ID = os.environ.get('SKILLPAY_SKILL_ID', '')
VERSION = "1.0.0"

# 审计日志文件
AUDIT_LOG_FILE = Path("~/.openclaw/fin_audit_logs/audit_chain.log").expanduser()


class FinAuditAutomator:
    """金融合规审计自动化器"""
    
    def __init__(self, api_key: str = API_KEY, skill_id: str = SKILL_ID):
        self.api_key = api_key
        self.skill_id = skill_id
        self.demo_mode = not api_key
        self.trial_manager = TrialManager("fin-audit-automator")
        
        # 初始化审计日志目录
        AUDIT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        if HAS_MODULES:
            self.aml_detector = AMLDetector()
            self.doc_validator = DocValidator()
    
    def process(self, request_type: str, data: dict, user_id: str = "") -> Dict[str, Any]:
        """处理审计请求"""
        # 记录审计日志
        self._log_audit(f"REQUEST:{request_type}", user_id)
        
        if self.demo_mode:
            return self._demo_process(request_type, data)
        
        # 检查免费试用
        trial_remaining = self.trial_manager.get_trial_remaining(user_id)
        
        if trial_remaining > 0:
            self.trial_manager.use_trial(user_id)
            result = self._audit(request_type, data)
            result["trial_mode"] = True
            result["trial_remaining"] = trial_remaining - 1
            return result
        
        # 付费模式
        result = self._audit(request_type, data)
        result["trial_mode"] = False
        result["trial_remaining"] = 0
        return result
    
    def _demo_process(self, request_type: str, data: dict) -> Dict[str, Any]:
        """演示模式处理"""
        demo_responses = {
            "aml_check": {
                "success": True,
                "demo_mode": True,
                "alerts": [
                    {"type": "FREQ_ABNORMAL", "severity": "HIGH", "description": "1小时内5笔大额交易"},
                    {"type": "ROUND_AMOUNT", "severity": "MEDIUM", "description": "整数金额偏好"}
                ],
                "risk_score": 75,
                "recommendation": "建议人工复核",
                "trial_mode": False,
                "trial_remaining": 50
            },
            "fapiao_check": {
                "success": True,
                "demo_mode": True,
                "valid": False,
                "issues": ["抬头不符", "敏感商品未备注"],
                "ocr_text": "***发票*** 金额: ****元",
                "trial_mode": False,
                "trial_remaining": 50
            },
            "report_gen": {
                "success": True,
                "demo_mode": True,
                "report": "# 金融合规审计报告\\n\\n## 总体结论\\n本期发现2项潜在风险...",
                "trial_mode": False,
                "trial_remaining": 50
            }
        }
        
        return demo_responses.get(request_type, {
            "success": False,
            "error": "未知的请求类型",
            "supported_types": ["aml_check", "fapiao_check", "report_gen"]
        })
    
    def _audit(self, request_type: str, data: dict) -> Dict[str, Any]:
        """执行审计"""
        if not HAS_MODULES:
            return {"success": False, "error": "模块未安装"}
        
        try:
            if request_type == "aml_check":
                return self._aml_check(data)
            elif request_type == "fapiao_check":
                return self._fapiao_check(data)
            elif request_type == "report_gen":
                return self._report_gen(data)
            else:
                return {"success": False, "error": "未知的请求类型"}
        except Exception as e:
            self._log_audit(f"ERROR:{str(e)}", "")
            return {"success": False, "error": str(e)}
    
    def _aml_check(self, data: dict) -> Dict[str, Any]:
        """反洗钱检测"""
        import pandas as pd
        
        transactions = data.get("transactions", [])
        if not transactions:
            return {"success": False, "error": "未提供交易数据"}
        
        df = pd.DataFrame(transactions)
        alerts = self.aml_detector.detect_suspicious(df)
        
        # 计算风险分数
        risk_score = min(len(alerts) * 25, 100)
        
        self._log_audit(f"AML_CHECK:alerts={len(alerts)}", "")
        
        return {
            "success": True,
            "alerts": alerts,
            "risk_score": risk_score,
            "recommendation": "人工复核" if risk_score > 50 else "通过",
            "checked_count": len(transactions)
        }
    
    def _fapiao_check(self, data: dict) -> Dict[str, Any]:
        """发票校验"""
        image_path = data.get("image_path")
        if not image_path:
            return {"success": False, "error": "未提供发票图片路径"}
        
        result = self.doc_validator.validate_fapiao(image_path)
        
        self._log_audit(f"FAPIAO_CHECK:valid={result['valid']}", "")
        
        return {
            "success": True,
            **result
        }
    
    def _report_gen(self, data: dict) -> Dict[str, Any]:
        """生成审计报告"""
        findings = data.get("findings", [])
        period = data.get("period", "2024-Q1")
        
        report = generate_audit_report(findings, period)
        
        self._log_audit(f"REPORT_GEN:findings={len(findings)}", "")
        
        return {
            "success": True,
            "report": report,
            "findings_count": len(findings)
        }
    
    def _log_audit(self, action: str, user_id: str):
        """记录审计日志 (简易哈希链)"""
        timestamp = datetime.now().isoformat()
        entry = f"{timestamp}|{action}|{user_id}"
        entry_hash = hashlib.sha256(entry.encode()).hexdigest()[:16]
        
        log_line = f"{entry}|{entry_hash}\\n"
        
        with open(AUDIT_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_line)


# 免费试用管理
class TrialManager:
    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.trial_dir = Path("~/.openclaw/skill_trial").expanduser()
        self.trial_file = self.trial_dir / f"{skill_name}.json"
        self.max_free_calls = 50  # 50次免费试用
        self.trial_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_trial_data(self) -> Dict[str, Any]:
        if self.trial_file.exists():
            try:
                with open(self.trial_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_trial_data(self, data: Dict[str, Any]):
        with open(self.trial_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_trial_remaining(self, user_id: str) -> int:
        if not user_id:
            return 0
        data = self._load_trial_data()
        user_data = data.get(user_id, {})
        used_calls = user_data.get('used_calls', 0)
        return max(0, self.max_free_calls - used_calls)
    
    def use_trial(self, user_id: str) -> bool:
        if not user_id:
            return False
        data = self._load_trial_data()
        if user_id not in data:
            data[user_id] = {'used_calls': 0}
        data[user_id]['used_calls'] += 1
        self._save_trial_data(data)
        return True


def on_audit_request(request_type: str, data: dict, context: dict = None) -> dict:
    """OpenClaw调用入口"""
    context = context or {}
    user_id = context.get("user_id", "")
    
    automator = FinAuditAutomator()
    return automator.process(request_type, data, user_id)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='金融合规审计自动化技能')
    parser.add_argument('--type', '-t', choices=['aml_check', 'fapiao_check', 'report_gen'],
                       help='审计类型')
    parser.add_argument('--data', '-d', help='JSON格式数据')
    parser.add_argument('--user-id', '-u', help='用户ID')
    parser.add_argument('--demo', action='store_true', help='演示模式')
    
    args = parser.parse_args()
    
    if args.type:
        data = json.loads(args.data) if args.data else {}
        result = on_audit_request(args.type, data, {"user_id": args.user_id or "demo"})
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("🛡️ 金融合规审计自动化技能")
        print("使用 --type 参数指定审计类型")
        print("  aml_check - 反洗钱检测")
        print("  fapiao_check - 发票校验")
        print("  report_gen - 生成审计报告")


if __name__ == "__main__":
    main()
