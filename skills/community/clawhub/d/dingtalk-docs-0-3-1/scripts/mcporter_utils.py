#!/usr/bin/env python3
"""
mcporter 公共工具函数

提供 mcporter 命令执行、响应解析、路径安全校验等通用功能，
供 create_doc.py、import_docs.py、export_docs.py 共用。
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple


def run_mcporter(tool: str, args: dict = None, timeout: int = 60) -> Tuple[bool, str]:
    """
    执行 mcporter 命令（使用 --args JSON 传参）

    Args:
        tool: 工具名称，如 dingtalk-docs.get_my_docs_root_dentry_uuid
        args: 参数字典，传入 --args JSON
        timeout: 超时时间（秒）

    Returns:
        (success, output) 元组
    """
    command = ['mcporter', 'call', tool, '--output', 'json']
    if args:
        command.extend(['--args', json.dumps(args, ensure_ascii=False)])
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, f"命令执行超时（{timeout}秒）"
    except Exception as error:
        return False, str(error)


def parse_response(output: str) -> Optional[dict]:
    """解析 mcporter 响应，自动处理嵌套 result 结构"""
    try:
        data = json.loads(output)
        if isinstance(data, dict) and 'result' in data:
            return data['result']
        return data
    except json.JSONDecodeError:
        return None


def get_root_dentry_uuid() -> Optional[str]:
    """获取"我的文档"根目录 ID"""
    success, output = run_mcporter('dingtalk-docs.get_my_docs_root_dentry_uuid')

    if not success:
        print(f"❌ 获取根目录 ID 失败：{output}")
        return None

    result = parse_response(output)
    if result is None:
        print(f"❌ 解析响应失败：{output}")
        return None
    return result.get('rootDentryUuid')


def resolve_safe_path(path: str) -> Path:
    """解析路径并限制在工作目录内，防止路径遍历攻击"""
    allowed_root = os.environ.get('OPENCLAW_WORKSPACE', os.getcwd())
    allowed_root = Path(allowed_root).resolve()

    if Path(path).is_absolute():
        target_path = Path(path).resolve()
    else:
        target_path = (Path.cwd() / path).resolve()

    try:
        target_path.relative_to(allowed_root)
        return target_path
    except ValueError:
        raise ValueError(
            f"路径超出允许范围：{path}\n"
            f"允许根目录：{allowed_root}\n"
            f"提示：设置 OPENCLAW_WORKSPACE 环境变量"
        )
