#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-Repair Library v1.1
一键修复脚本库 — 根据诊断上下文自动匹配修复方案

v1.1 改进:
  - Gateway restart 改用 taskkill + start (避免 openclaw gateway restart 挂死)
  - 新增 Session 归档修复计划
  - 新增 Gateway 内存告警修复计划
  - 修复后验证改为轮询模式 (30s, 每 5s 一次)

用法:
  from auto_repair import match_repair, RepairAction, verify_repair

  ctx = {"status": "stopped", "source": "cli"}
  actions = match_repair(ctx)
  if actions:
      for a in actions:
          a.execute()
      ok, msg = verify_repair()
"""

import subprocess
import time
import json
import logging
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

_HOME_DIR = Path.home()
_OPENCLAW_CMD = str(_HOME_DIR / "AppData/Roaming/npm/openclaw.cmd")


# ============================================================
# 修复动作定义
# ============================================================

@dataclass
class RepairAction:
    """一个可执行的修复动作"""
    issue: str
    description: str
    risk: str                       # low / medium / high
    auto_approve: bool = False
    commands: List[str] = field(default_factory=list)

    def execute(self) -> bool:
        """执行修复命令，返回是否成功"""
        for cmd in self.commands:
            try:
                logger.info("执行修复: %s -> %s", self.issue, cmd[:80])
                result = subprocess.run(
                    ["powershell", "-Command", cmd],
                    capture_output=True, text=True, timeout=60,
                )
                if result.returncode != 0:
                    logger.warning("修复命令失败: %s", result.stderr[:100])
                    return False
            except subprocess.TimeoutExpired:
                logger.warning("修复命令超时: %s", self.issue)
                return False
            except Exception as e:
                logger.error("修复异常: %s", e)
                return False
        logger.info("修复完成: %s", self.issue)
        return True

    def summary(self) -> str:
        return "[%s] %s" % (self.risk, self.description)


def _gateway_status() -> dict:
    """快速获取 Gateway 状态。"""
    try:
        r = subprocess.run(
            [_OPENCLAW_CMD, "gateway", "status", "--json"],
            capture_output=True, text=True, timeout=12, shell=True,
        )
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout)
    except Exception:
        pass
    return {}


def verify_repair(max_wait: int = 30, interval: int = 5) -> Tuple[bool, str]:
    """修复后验证 — 轮询 Gateway 状态，最多等 max_wait 秒。"""
    for attempt in range(max_wait // interval + 1):
        data = _gateway_status()
        if data:
            svc = data.get("service", {}).get("runtime", {}).get("status", "")
            rpc = data.get("rpc", {}).get("ok", False)
            if svc == "running" and rpc:
                return True, "Gateway 运行中，RPC 正常"
            if svc == "running":
                return True, "Gateway 运行中，RPC 未就绪"
        if attempt < max_wait // interval:
            time.sleep(interval)
    return False, "%ds 内验证未通过" % max_wait


# ============================================================
# 修复方案库
# ============================================================

def _safe_gateway_restart() -> List[str]:
    """安全重启 Gateway: 先 taskkill 杀掉旧进程，再 start。"""
    return [
        'Get-Process -Name "node" -ErrorAction SilentlyContinue | '
        'Where-Object { $_.CommandLine -match "openclaw.*gateway" } | '
        'Stop-Process -Force -ErrorAction SilentlyContinue',
        "Start-Sleep -Seconds 2",
        "openclaw gateway start",
    ]


REPAIR_PLANS: List[Dict] = [
    # ---- Gateway 停止 ----
    {
        "match": {"status": "stopped"},
        "actions": [
            RepairAction(
                issue="gateway_stopped",
                description="Gateway 进程未运行，尝试重启",
                risk="low",
                auto_approve=False,
                commands=_safe_gateway_restart(),
            ),
        ]
    },

    # ---- RPC 连接失败 ----
    {
        "match": {"rpc_ok": False},
        "actions": [
            RepairAction(
                issue="rpc_failed",
                description="Gateway RPC 连接异常，尝试重启",
                risk="medium",
                auto_approve=False,
                commands=_safe_gateway_restart(),
            ),
        ]
    },

    # ---- CLI 检查失败 ----
    {
        "match": {"source": "cli", "status": "cli_error"},
        "actions": [
            RepairAction(
                issue="cli_unavailable",
                description="openclaw CLI 不可用，检查安装路径",
                risk="low",
                auto_approve=True,
                commands=[
                    "Get-Command openclaw -ErrorAction SilentlyContinue | Select-Object Source"
                ]
            ),
        ]
    },

    # ---- HTTP API 不可达（Gateway 未响应）----
    {
        "match": {"source": "http", "status": "unreachable"},
        "actions": [
            RepairAction(
                issue="gateway_unreachable",
                description="Gateway HTTP API 不可达，检查端口并尝试重启",
                risk="medium",
                auto_approve=False,
                commands=[
                    "Test-NetConnection -ComputerName 127.0.0.1 -Port 18788 -WarningAction SilentlyContinue | Select-Object TcpTestSucceeded",
                ] + _safe_gateway_restart(),
            ),
        ]
    },

    # ---- Session 文件积压 ----
    {
        "match": {"session_backlog": True},
        "actions": [
            RepairAction(
                issue="session_backlog",
                description="Session 文件积压（>100 个），归档旧文件到 archive/",
                risk="low",
                auto_approve=True,
                commands=[
                    '$sDir = "%s"; $aDir = Join-Path $sDir "archive"; New-Item -ItemType Directory -Path $aDir -Force | Out-Null; '
                    'Get-ChildItem (Join-Path $sDir "*.jsonl") | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } | '
                    'Move-Item -Destination $aDir -Force; '
                    '$cnt = (Get-ChildItem (Join-Path $sDir "*.jsonl") | Measure-Object).Count; '
                    'Write-Host ("归档完成，当前活跃 Session: " + $cnt)'
                    % str(_HOME_DIR / ".openclaw" / "agents" / "main" / "sessions"),
                ]
            ),
        ]
    },

    # ---- Gateway 内存过高 ----
    {
        "match": {"gateway_memory_high": True},
        "actions": [
            RepairAction(
                issue="gateway_memory_high",
                description="Gateway 进程内存超过 800MB，建议重启",
                risk="medium",
                auto_approve=False,
                commands=_safe_gateway_restart(),
            ),
        ]
    },

    # ---- 模拟健康检查 ----
    {
        "match": {"source": "sim", "status": "healthy"},
        "actions": []
    },
]


# ============================================================
# 匹配引擎 (v1.1 — 支持新 ctx 字段)
# ============================================================

def match_repair(ctx: Dict[str, any]) -> Optional[List[RepairAction]]:
    """
    根据诊断上下文匹配修复方案。
    返回匹配的 RepairAction 列表，无匹配则返回 None。
    """
    if not ctx:
        return None

    best_score = 0
    best_actions = None

    for plan in REPAIR_PLANS:
        match = plan["match"]
        score = 0
        total = len(match)

        for key, expected in match.items():
            actual = ctx.get(key)
            if actual == expected:
                score += 1
            elif isinstance(expected, (list, tuple)) and actual in expected:
                score += 1
            elif actual and str(expected).lower() in str(actual).lower():
                score += 0.5

        if total > 0 and score / total >= 0.5 and score > best_score:
            best_score = score
            best_actions = plan["actions"]

    return best_actions if best_actions else None


def format_repair_suggestion(actions: List[RepairAction]) -> str:
    """将修复方案格式化为可读文本"""
    if not actions:
        return "未找到匹配的自动修复方案，需要人工诊断。"

    lines = ["**🔧 自动修复方案**\n"]
    for action in actions:
        risk_map = {"low": "✅", "medium": "⚠️", "high": "🔴"}
        risk_emoji = risk_map.get(action.risk, "❓")
        auto = "可自动执行" if action.auto_approve else "需要确认"
        lines.append("- %s **%s** (%s)" % (risk_emoji, action.description, auto))
    lines.append("\n共有 %d 个修复步骤" % len(actions))
    return "\n".join(lines)


# ============================================================
# 快速测试
# ============================================================

if __name__ == "__main__":
    test_cases = [
        {"status": "stopped", "source": "cli"},
        {"rpc_ok": False, "source": "cli"},
        {"status": "unreachable", "source": "http"},
        {"session_backlog": True},
        {"gateway_memory_high": True},
        {"status": "running", "rpc_ok": True, "source": "cli"},
    ]

    for ctx in test_cases:
        actions = match_repair(ctx)
        print("\n诊断上下文: %s" % ctx)
        print("匹配结果: %s" % (format_repair_suggestion(actions) if actions else "无匹配"))
