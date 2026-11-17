# -*- coding: utf-8 -*-
"""ct-advisor 结构化错误信号（stderr 机器通道 · 2026-10-15 · B 方案）。

设计意图：
- stdout 的 CT_ANSWER 块只给**人**看；本通道给**调用方 agent** 看，让它无需解析
  自然语言即可决策「能否自愈 / 能否重试 / 只能原样转述」。
- 信号**只在真实失败时发射**；成功路径绝不发射——未报错时 agent 不得进入自愈流程
  （SKILL.md「Error Self-Heal Protocol」硬性规则第 1 条）。
- fix_cmd 一律由技能内置常量构造；**禁止**把任何远端返回内容拼进命令（防注入）。
- 格式恒定单行，字段顺序固定，便于正则/分词解析：
      [ct-advisor][ERR] code=<CODE> auto_fixable=<bool> retry_safe=<bool>
                       requires_network=<bool> [detail="..."] [fix_cmd="..."]
"""
from __future__ import annotations

import sys

SIGNAL_PREFIX = "[ct-advisor][ERR]"

# 错误码登记表：code -> 决策位
#   auto_fixable     : agent 是否可在用户授权后自行修复（执行 fix_cmd）
#   retry_safe       : 修复/恢复后重试是否安全（false = Coze 可能已收到请求，重试会重复发送）
#   requires_network : 修复动作自身是否依赖可用的出网链路
ERR_CODES = {
    # 已配置代理但不可达（代理进程未起 / 地址端口错 / 连接被拒）
    "CONN_FAIL_PROXY":  {"auto_fixable": False, "retry_safe": True,  "requires_network": True},
    # 无代理且直连失败（无出网路由 / DNS / 防火墙拦截）
    "CONN_FAIL_DIRECT": {"auto_fixable": False, "retry_safe": True,  "requires_network": True},
    # 读取超时：Coze 很可能已收到请求 -> 严禁自动重试（重复发送）
    "TIMEOUT":          {"auto_fixable": False, "retry_safe": False, "requires_network": True},
    # 鉴权失败：token 失效/被撤销，需维护者更新内嵌凭据
    "AUTH_401":         {"auto_fixable": False, "retry_safe": False, "requires_network": False},
    # Coze 返回非 2xx（5xx 等服务端错误）
    "COZE_HTTP_ERROR":  {"auto_fixable": False, "retry_safe": False, "requires_network": True},
    # 技能内部异常（配置损坏 / token 解码失败 / 响应解析失败 / 代码缺陷）
    "ORCH_FAIL":        {"auto_fixable": False, "retry_safe": False, "requires_network": False},
}


def _sanitize_field(text) -> str:
    """把 detail/fix_cmd 压成单行、去双引号，保证信号永远是单行可解析格式。"""
    s = str(text).replace('"', "'").replace("\n", " ").replace("\r", " ")
    return s.strip()


def emit_err_signal(code: str, detail: str = "", fix_cmd: str = None) -> None:
    """向 stderr 发射单行机器信号。**仅失败路径调用；成功路径禁止调用。**"""
    meta = ERR_CODES.get(code)
    if meta is None:
        # 未登记码按最保守策略处理：不可自愈、不可重试
        meta = {"auto_fixable": False, "retry_safe": False, "requires_network": False}
    parts = [
        SIGNAL_PREFIX,
        "code=%s" % code,
        "auto_fixable=%s" % ("true" if meta["auto_fixable"] else "false"),
        "retry_safe=%s" % ("true" if meta["retry_safe"] else "false"),
        "requires_network=%s" % ("true" if meta["requires_network"] else "false"),
    ]
    if detail:
        parts.append('detail="%s"' % _sanitize_field(detail))
    if fix_cmd:
        parts.append('fix_cmd="%s"' % _sanitize_field(fix_cmd))
    try:
        sys.stderr.write(" ".join(parts) + "\n")
    except Exception:  # noqa: BLE001  信号通道故障不得覆盖原始错误
        pass
