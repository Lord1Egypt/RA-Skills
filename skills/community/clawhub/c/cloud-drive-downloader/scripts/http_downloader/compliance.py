"""合规声明与用户责任确认。

本模块只用于下载用户已获授权或公开许可能否使用的直链文件。
调用方必须在下载前明确确认自己拥有下载/使用该文件的授权。
"""

from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    _boot_parent = _boot_os.path.dirname(_boot_here)
    for _boot_dir in (_boot_here, _boot_parent):
        if _boot_dir not in _boot_sys.path:
            _boot_sys.path.insert(0, _boot_dir)
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


class ComplianceError(RuntimeError):
    """未确认授权时抛出的错误。"""

COMPLIANCE_NOTICE = (
    "\n"
    "=== 合规声明（请先阅读）===\n"
    "1. 本下载模块只接受 HTTP/HTTPS 直链，仅用于下载你已获得授权、\n"
    "   或公开许可（Public Domain / CC / 官方允许下载等）的公开文件。\n"
    "2. 不包含网盘分享链接解析、绕过登录/防盗链/验证码/会员鉴权、\n"
    "   破解、盗版资源搜索等能力。\n"
    "3. 下载与使用任何文件，请自行确认版权与许可；侵权风险由使用者承担。\n"
    "4. 请勿将本模块用于侵犯他人知识产权或违反所适用法律法规的用途。\n"
    "================================\n"
)

CONFIRM_FLAG = "--confirm-own-use"
PROMPT_TEXT = "我已确认本人对该文件拥有下载/使用授权（输入 yes 继续，其余退出）: "


def confirm(interactive: bool = True) -> None:
    """要求用户确认授权。interactive=False 时必须由 CLI 显式传入确认开关。"""
    if not interactive:
        raise ComplianceError(
            f"未确认授权：请在命令中显式添加 {CONFIRM_FLAG}，表示你拥有所下载内容的授权。"
        )
    print(COMPLIANCE_NOTICE)
    answer = input(PROMPT_TEXT).strip().lower()
    if answer not in ("y", "yes", "是", "确认"):
        raise ComplianceError("已取消：未获得用户授权确认，不下载。")
