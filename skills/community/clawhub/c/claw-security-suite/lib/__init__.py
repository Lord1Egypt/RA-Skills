"""
claw-security-suite
OpenClaw 完整四层纵深安全防御体系

Exports:
- StaticScanner / scan() -> 第一层：静态代码扫描
- LogicAuditor / audit() -> 第二层：逻辑安全审计
- RuntimeProtector / check_input() -> 第三层：运行时防护
- SecurityPatrol / daily_patrol() / weekly_scan() -> 第四层：定期巡检
"""

from .static_scanner import StaticScanner, scan, ScanResult
from .logic_auditor import LogicAuditor, audit, AuditResult, AuditFinding
from .runtime_protector import RuntimeProtector, check_input, CheckResult
from .security_patrol import SecurityPatrol, daily_patrol, weekly_scan, PatrolResult

__version__ = "1.0.0"
__author__ = "Kenz1117"
