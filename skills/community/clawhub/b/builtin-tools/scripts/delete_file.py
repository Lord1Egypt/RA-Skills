#!/usr/bin/env python3
"""delete_file — 删除文件"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

def main():
    params = parse_input()
    path = get_param(params, "path", required=True)
    recursive = get_param(params, "recursive", False)

    p = resolve_path(str(path))

    # 安全检查：禁止删除根目录和用户主目录
    danger_paths = [
        Path("/"), Path("C:\\"), Path("D:\\"),
        home_dir(),
    ]
    for dp in danger_paths:
        try:
            if p.resolve() == dp.resolve():
                output_error(f"安全策略禁止删除: {p}", EXIT_PARAM_ERROR)
        except Exception:
            pass

    if not p.exists():
        output_ok({"path": str(p), "deleted": False, "message": "文件不存在"})

    try:
        if p.is_file():
            p.unlink()
        elif p.is_dir():
            if recursive:
                import shutil
                shutil.rmtree(str(p))
            else:
                p.rmdir()
    except PermissionError:
        output_error(f"权限不足: {p}", EXIT_EXEC_ERROR)
    except OSError as e:
        output_error(f"删除失败: {e}", EXIT_EXEC_ERROR)

    output_ok({"path": str(p), "deleted": True})

if __name__ == "__main__":
    main()
