#!/usr/bin/env python3
"""AK 配置命令 -- CLI 入口"""

COMMAND_NAME = "configure"
COMMAND_DESC = "配置 AK"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from _risk_guard import emit_confirmation, get_confirmed_payload
from capabilities.configure.service import (
    validate_ak, configure_via_gateway, configure_via_file, check_existing_config,
)


def _mask_ak(ak: str) -> str:
    if len(ak) >= 8:
        return "{}****{}".format(ak[:4], ak[-4:])
    return "****"


def _do_write(ak: str) -> None:
    """实际写入 AK；Phase 2 / Phase 1 同步调用。"""
    write_ok = configure_via_gateway(ak) or configure_via_file(ak)
    if not write_ok:
        print_output(False,
                     "AK 写入失败（Gateway 不可用且 fallback 被拒绝/失败），请检查 Gateway 状态或文件权限",
                     {"configured": False})
        return

    md = (
        "AK 已保存: `{}`\n\n"
        "后续由 OpenClaw 配置注入生效（以配置为准，不使用本地会话缓存）。\n\n"
        "若当前会话仍提示 AK未配置或AK无效，请新开会话或执行：`openclaw secrets reload`"
    ).format(_mask_ak(ak))
    print_output(True, md, {"configured": True})


def main():
    try:
        # 查询分支（只读）：不走二次确认。
        # 注意：查询分支不会命中 SKILL.md 中的正则 `cli\.py\s+configure\s+\S+`，
        # 如果 Phase 2 被错误调起，下面读 payload 分支会接管。
        if len(sys.argv) < 2:
            has_existing, existing_ak = check_existing_config()
            if has_existing:
                src = ("环境变量（已生效）" if os.environ.get("ALI_1688_AK")
                       else "OpenClaw 配置（新会话/重载后生效）")
                md = "AK 已配置: `{}`（来源: {}）".format(_mask_ak(existing_ak), src)
            else:
                md = "AK 尚未配置\n\n运行: `cli.py configure YOUR_AK`"
            print_output(has_existing, md, {"configured": has_existing})
            return

        # 写入分支：AK 属凭证级敏感信息，必须走二次确认，防止 AI 被 prompt 注入后伪造或覆盖 AK。
        payload = get_confirmed_payload()
        if payload is None:
            ak = sys.argv[1].strip()
            is_valid, error_msg = validate_ak(ak)
            if not is_valid:
                print_output(False, "AK 格式错误: {}".format(error_msg), {"configured": False})
                return
            emit_confirmation(
                message="即将写入 AK `{}` 覆盖当前配置，是否确认？".format(_mask_ak(ak)),
                payload={"ak": ak},
                preview_markdown="待商家确认：写入 AK `{}`".format(_mask_ak(ak)),
            )
            return

        # Phase 2：仅从 payload 读 AK，彻底不取 sys.argv（避免中间环节篡改）。
        ak = (payload.get("ak") or "").strip()
        if not ak:
            print_output(False, "二次确认 payload.ak 缺失，拒绝写入", {"configured": False})
            return
        is_valid, error_msg = validate_ak(ak)
        if not is_valid:
            print_output(False, "AK 格式错误: {}".format(error_msg), {"configured": False})
            return
        _do_write(ak)
    except Exception as e:
        print_error(e, {"configured": False})


if __name__ == "__main__":
    main()
