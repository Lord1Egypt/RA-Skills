#!/usr/bin/env python3
"""
claw-security-suite
第二层：逻辑安全审计
分析代码逻辑是否越权，是否符合最小权限原则
"""

import os
import re
from dataclasses import dataclass
from typing import List, Dict, Optional

# OWASP Top 10 风险检查点
RISK_CHECKPOINTS = [
    {
        "name": "SQL注入",
        "pattern": r'execute.*\+|format.*sql|sql.*\%s',
        "description": "可能存在字符串拼接SQL，存在注入风险",
        "risk_level": "high"
    },
    {
        "name": "命令注入",
        "pattern": r'os\.system.*format|subprocess.*\+|eval.*input',
        "description": "可能存在命令注入风险",
        "risk_level": "high"
    },
    {
        "name": "权限越权",
        "pattern": r'\.\./\.\./|/etc/passwd|/root/|\/home\/',
        "description": "可能存在路径遍历/越权读取系统文件",
        "risk_level": "high"
    },
    {
        "name": "敏感数据泄露",
        "pattern": r'print.*api[_-]key|log.*api[_-]key|debug.*key',
        "description": "可能在日志/输出中泄露API密钥",
        "risk_level": "medium"
    },
    {
        "name": "未验证输入",
        "pattern": r'request\.GET\[\w+\]|input\(.*\).*exec',
        "description": "用户输入未验证直接使用",
        "risk_level": "medium"
    },
    {
        "name": "硬编码凭证",
        "pattern": r'api[_-]key\s*=\s*[\'"][a-zA-Z0-9]{30,}[\'"]',
        "description": "代码中硬编码API凭证",
        "risk_level": "high"
    },
    {
        "name": "未授权网络请求",
        "pattern": r'requests\.get|requests\.post',
        "description": "向外网发送请求，需要确认用途",
        "risk_level": "medium"
    },
]

@dataclass
class AuditFinding:
    checkpoint: str
    description: str
    risk_level: str  # high, medium, low
    location: str
    line: int

@dataclass
class AuditResult:
    is_safe: bool
    findings: List[AuditFinding]
    
    def to_report(self) -> str:
        lines = []
        high_count = sum(1 for f in self.findings if f.risk_level == 'high')
        medium_count = sum(1 for f in self.findings if f.risk_level == 'medium')
        
        if high_count == 0:
            lines.append("✅ 逻辑审计通过，未发现高危漏洞")
        else:
            lines.append(f"❌ 逻辑审计发现 {high_count} 个高危漏洞")
        if medium_count > 0:
            lines.append(f"⚠️  发现 {medium_count} 个中风险问题需要关注")
        
        if self.findings:
            lines.append("\n发现列表:")
            for i, finding in enumerate(self.findings, 1):
                prefix = "🔴" if finding.risk_level == 'high' else "🟡" if finding.risk_level == 'medium' else "🟢"
                lines.append(f"{prefix} {i}. [{finding.checkpoint}] {finding.description}")
                lines.append(f"    文件: {finding.location}:{finding.line}")
        
        return "\n".join(lines)

class LogicAuditor:
    def __init__(self):
        self.checkpoints = []
        for cp in RISK_CHECKPOINTS:
            self.checkpoints.append({
                **cp,
                "pattern": re.compile(cp["pattern"])
            })
    
    def audit_file(self, filepath: str) -> List[AuditFinding]:
        """审计单个文件"""
        findings = []
        _, ext = os.path.splitext(filepath)
        
        # 只审计代码文件
        if ext not in ['.py', '.sh', '.js', '.php']:
            return findings
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    for cp in self.checkpoints:
                        if cp["pattern"].search(line):
                            findings.append(AuditFinding(
                                checkpoint=cp["name"],
                                description=cp["description"],
                                risk_level=cp["risk_level"],
                                location=filepath,
                                line=line_num
                            ))
        except Exception as e:
            findings.append(AuditFinding(
                checkpoint="文件读取错误",
                description=str(e),
                risk_level="low",
                location=filepath,
                line=0
            ))
        
        return findings
    
    def audit_directory(self, dirpath: str, declared_permissions: Optional[Dict] = None) -> AuditResult:
        """审计整个目录"""
        all_findings = []
        
        for root, dirs, files in os.walk(dirpath):
            for f in files:
                if f.startswith('.git') or f.endswith('.pyc') or f == '__pycache__':
                    continue
                fullpath = os.path.join(root, f)
                findings = self.audit_file(fullpath)
                all_findings.extend(findings)
        
        # 判断是否安全：0高危就是安全
        high_count = sum(1 for f in all_findings if f.risk_level == 'high')
        is_safe = high_count == 0
        
        return AuditResult(
            is_safe=is_safe,
            findings=all_findings
        )

def audit(dirpath: str, declared_permissions: Optional[Dict] = None) -> AuditResult:
    """对外接口：审计目录"""
    auditor = LogicAuditor()
    return auditor.audit_directory(dirpath, declared_permissions)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <directory>")
        sys.exit(1)
    
    result = audit(sys.argv[1])
    print(result.to_report())
    if not result.is_safe:
        sys.exit(1)
