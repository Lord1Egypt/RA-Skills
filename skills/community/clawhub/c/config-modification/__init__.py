# [OC-WM] licensed-to: macmini@MacminideMac-mini | bundle: vendor-suite | ts: 2026-03-09T17:30:16Z
"""
config-modification-v2.3 — 配置修改防护系统
==========================================

整合了拦截矩阵、四联校验、自动回滚的统一防护系统

核心模块:
- intercept_matrix: 拦截矩阵，定义哪些操作需要触发校验
- quad_check: 四联校验状态机 (schema/diff/rollback/health)
- auto_rollback: 失败自动回滚 + 告警系统
- config_modification_v2: 统一入口 CLI

快速开始:
  from intercept_matrix import should_intercept, get_check_level
  from quad_check import QuadCheckStateMachine, CheckPhase
  from auto_rollback import AutoRollback, check_and_rollback
  
  # 1. 检查是否需要拦截
  if should_intercept("edit", "/path/to/config.json"):
      # 2. 执行四联校验
      qc = QuadCheckStateMachine("/path/to/config.json")
      results = qc.run_all()
      
      # 3. 检查失败并回滚
      check_and_rollback(results, "/path/to/config.json")

版本: 2.3.0
日期: 2026-03-04
"""

from .intercept_matrix import (
    should_intercept,
    get_check_level,
    get_intercept_details,
    is_sensitive_path,
    CONFIG_RISK_LEVELS,
    ACTION_TRIGGERS
)

from .quad_check import (
    QuadCheckStateMachine,
    CheckPhase,
    CheckResult
)

from .auto_rollback import (
    AutoRollback,
    check_and_rollback,
    AlertManager,
    ALERT_RULES
)

__version__ = "2.3.0"
__all__ = [
    # intercept_matrix
    "should_intercept",
    "get_check_level", 
    "get_intercept_details",
    "is_sensitive_path",
    # quad_check
    "QuadCheckStateMachine",
    "CheckPhase",
    "CheckResult",
    # auto_rollback
    "AutoRollback",
    "check_and_rollback",
    "AlertManager",
    "ALERT_RULES"
]
