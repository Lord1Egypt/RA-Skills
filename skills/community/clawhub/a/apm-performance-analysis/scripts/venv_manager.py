#!/usr/bin/env python3
"""
APM 智能运维 Skill 脚本运行器

由于采用内嵌（vendored）官方 SDK 方案，不再需要虚拟环境和 pip 安装。
本脚本保留 `run` 命令接口以实现向后兼容，内部直接使用当前 Python 解释器执行目标脚本。

用法示例:
    # 直接运行 apm_mcp_client.py（推荐方式，无需 venv_manager）
    python scripts/apm_mcp_client.py list-tools

    # 通过 venv_manager.py run 运行（向后兼容）
    python scripts/venv_manager.py run scripts/apm_mcp_client.py list-tools

    # 检查环境状态
    python scripts/venv_manager.py status
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()


def run_script(script_args):
    """
    使用当前 Python 解释器运行目标脚本。

    由于 SDK 已内嵌在 scripts/tencentcloud/ 中，不再需要虚拟环境。

    Args:
        script_args: 脚本路径及参数列表

    Returns:
        int: 脚本退出码
    """
    python_path = sys.executable
    cmd = [python_path] + script_args

    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"错误: 执行脚本失败: {e}")
        return 1


def get_status():
    """
    获取环境状态信息。

    Returns:
        dict: 状态信息
    """
    sdk_path = SCRIPT_DIR / "tencentcloud"
    apm_client_path = sdk_path / "apm" / "v20210622" / "apm_client.py"

    status = {
        "mode": "vendored_sdk",
        "description": "使用内嵌官方 SDK，无需虚拟环境",
        "python_path": sys.executable,
        "python_version": sys.version,
        "sdk_path": str(sdk_path),
        "sdk_available": apm_client_path.is_file(),
        "credential_configured": bool(
            os.environ.get("TENCENTCLOUD_SECRET_ID")
            and os.environ.get("TENCENTCLOUD_SECRET_KEY")
        ),
    }

    # 检查 SDK 文件完整性
    required_files = [
        "tencentcloud/__init__.py",
        "tencentcloud/common/__init__.py",
        "tencentcloud/common/abstract_client.py",
        "tencentcloud/common/credential.py",
        "tencentcloud/apm/v20210622/apm_client.py",
        "tencentcloud/apm/v20210622/models.py",
    ]
    missing_files = []
    for f in required_files:
        if not (SCRIPT_DIR / f).is_file():
            missing_files.append(f)

    status["sdk_complete"] = len(missing_files) == 0
    if missing_files:
        status["missing_files"] = missing_files

    return status


# ---------------------------------------------------------------------------
# 命令行入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="APM 智能运维 Skill 脚本运行器（内嵌 SDK 模式）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "说明:\n"
            "  本 Skill 使用内嵌（vendored）的腾讯云官方 SDK，无需虚拟环境和 pip 安装。\n"
            "  可直接运行: python scripts/apm_mcp_client.py <command>\n"
            "\n"
            "示例:\n"
            "  # 通过 run 命令运行（向后兼容）\n"
            "  python venv_manager.py run scripts/apm_mcp_client.py list-tools\n"
            "\n"
            "  # 直接运行（推荐）\n"
            "  python scripts/apm_mcp_client.py list-tools\n"
            "\n"
            "  # 查看环境状态\n"
            "  python venv_manager.py status\n"
        ),
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # run - 运行脚本（向后兼容）
    run_parser = subparsers.add_parser(
        "run",
        help="运行 Python 脚本（向后兼容，内部直接使用当前解释器）",
    )
    run_parser.add_argument(
        "script_args",
        nargs=argparse.REMAINDER,
        help="要运行的脚本路径及参数",
    )

    # ensure - 向后兼容，无实际操作
    subparsers.add_parser(
        "ensure",
        help="环境就绪检查（内嵌 SDK 模式下始终就绪）",
    )

    # status - 查看状态
    status_parser = subparsers.add_parser(
        "status",
        help="查看环境状态",
    )
    status_parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="输出格式，默认 text",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "run":
        if not args.script_args:
            print("错误: 请提供要运行的脚本路径及参数")
            print(f"示例: python {__file__} run scripts/apm_mcp_client.py list-tools")
            sys.exit(1)

        exit_code = run_script(args.script_args)
        sys.exit(exit_code)

    elif args.command == "ensure":
        status = get_status()
        if status["sdk_complete"]:
            print("环境就绪: 内嵌官方 SDK 完整可用，无需额外安装。")
            print(f"Python: {status['python_path']}")
            print(f"SDK 路径: {status['sdk_path']}")
            print(f"\n可直接运行: python scripts/apm_mcp_client.py <command>")
        else:
            print("错误: 内嵌 SDK 不完整，缺失文件:")
            for f in status.get("missing_files", []):
                print(f"  - {f}")
            sys.exit(1)

    elif args.command == "status":
        status = get_status()

        if args.output == "json":
            print(json.dumps(status, indent=2, ensure_ascii=False))
        else:
            print("APM Skill 环境状态")
            print("=" * 60)
            print(f"  模式:        内嵌官方 SDK（vendored）")
            print(f"  Python:      {status['python_path']}")
            print(f"  版本:        {status['python_version'].split()[0]}")
            print(f"  SDK 路径:    {status['sdk_path']}")
            print(f"  SDK 可用:    {'是' if status['sdk_available'] else '否'}")
            print(f"  SDK 完整:    {'是' if status['sdk_complete'] else '否'}")
            print(f"  凭证已配置:  {'是' if status['credential_configured'] else '否'}")

            if not status["sdk_complete"]:
                print(f"\n  缺失文件:")
                for f in status.get("missing_files", []):
                    print(f"    - {f}")
            print("=" * 60)


if __name__ == "__main__":
    main()
