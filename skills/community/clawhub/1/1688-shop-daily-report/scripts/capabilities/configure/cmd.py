#!/usr/bin/env python3
"""AK 配置命令 — CLI 入口"""

COMMAND_NAME = "configure"
COMMAND_DESC = "配置 AK"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.configure.service import validate_ak, save_ak, check_existing_config


def _mask_ak(ak: str) -> str:
    if len(ak) >= 8:
        return f"{ak[:4]}****{ak[-4:]}"
    return "****"


def main():
    try:
        has_existing, existing_ak = check_existing_config()

        if len(sys.argv) < 2:
            if has_existing:
                md = f"✅ AK 已配置: `{_mask_ak(existing_ak)}`"
            else:
                md = "❌ 尚未配置 AK\n\n运行: `cli.py configure YOUR_AK`"
            print_output(has_existing, md, {"configured": has_existing})
            return

        ak = sys.argv[1].strip()
        is_valid, error_msg = validate_ak(ak)
        if not is_valid:
            print_output(False, f"❌ {error_msg}", {"configured": False})
            return

        write_ok = save_ak(ak)
        if not write_ok:
            print_output(False, "❌ AK 写入失败", {"configured": False})
            return

        md = f"✅ AK 配置成功: `{_mask_ak(ak)}`"
        print_output(True, md, {"configured": True})
    except Exception as e:
        print_error(e, {"configured": False})


if __name__ == "__main__":
    main()
