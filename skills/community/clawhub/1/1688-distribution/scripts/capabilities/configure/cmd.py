#!/usr/bin/env python3
"""AK 配置命令 — CLI 入口"""

COMMAND_NAME = "configure"
COMMAND_DESC = "配置 AK"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))

from scripts._sys._output import print_output, print_error
from scripts.capabilities.configure.service import (
    validate_ak, configure_ak, remove_ak, check_existing_config,
)


def _mask_ak(ak: str) -> str:
    if len(ak) >= 8:
        return f"{ak[:4]}****{ak[-4:]}"
    return "****"


def main(args=None):
    """
    AK 配置命令入口。

    Args:
        args: 命令参数列表。为 None 时从 sys.argv[1:] 读取。
              通过 cli.py 路由时传入 sys.argv[2:]。

    支持的参数：
        <AK>            配置新的 AK
        --reset <AK>    重置 AK（清除旧 AK + 配置新 AK）
        --clear         取消 AK 配置
        --status        查看 AK 配置状态
        --get-ak        通过浏览器授权获取 AK
    """
    if args is None:
        args = sys.argv[1:]

    # 无参数时自动查询本地 AK 状态
    if len(args) < 1:
        args = ["--status"]

    try:
        has_existing, existing_ak, existing_source = check_existing_config()

        # --status: 查看 AK 配置状态
        if "--status" in args:
            if has_existing:
                print_output(True,
                    f"✅ AK 已配置: `{_mask_ak(existing_ak)}`",
                    {"configured": True, "ak": existing_ak})
            else:
                print_output(True,
                    "❌ 尚未配置 AK\n\n运行: `python3 scripts/capabilities/configure/cmd.py --get-ak` 通过浏览器授权获取",
                    {"configured": False, "ak": None})
            return

        # --get-ak：通过浏览器授权获取 AK
        if "--get-ak" in args:
            from scripts._sys._authorize import get_ak
            sys.exit(get_ak())

        # --clear: 取消 AK
        if "--clear" in args:
            if not has_existing:
                print_output(True, "当前未配置 AK，无需清除。", {"configured": False})
                return
            remove_ok = remove_ak()
            if remove_ok:
                print_output(True, "✅ AK 已清除", {"configured": False})
            else:
                print_output(False, "❌ AK 清除失败，请检查文件权限", {"configured": True})
            return

        # --reset <AK>: 重置 AK
        if "--reset" in args:
            reset_idx = args.index("--reset")
            if reset_idx + 1 >= len(args):
                print_output(False, "缺少参数：`--reset` 后需要提供新的 AK", {"configured": False})
                return

            ak = args[reset_idx + 1].strip()
            is_valid, error_msg = validate_ak(ak)
            if not is_valid:
                print_output(False, f"❌ {error_msg}", {"configured": False})
                return

            write_ok, storage_location = configure_ak(ak)
            if not write_ok:
                print_output(False, "❌ AK 写入失败，请检查文件权限", {"configured": False})
                return

            print_output(True, "✅ AK 已重置", {"configured": True})
            return

        # 直接传入 AK -> 配置
        ak = args[0].strip()
        is_valid, error_msg = validate_ak(ak)
        if not is_valid:
            print_output(False, f"❌ {error_msg}", {"configured": False})
            return

        write_ok, storage_location = configure_ak(ak)
        if not write_ok:
            print_output(False, "❌ AK 写入失败，请检查文件权限", {"configured": False})
            return

        print_output(True, "✅ AK 设置成功", {"configured": True})
    except Exception as e:
        print_error(e, {"configured": False})


if __name__ == "__main__":
    main()
