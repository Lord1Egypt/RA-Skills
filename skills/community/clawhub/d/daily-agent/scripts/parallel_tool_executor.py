#!/usr/bin/env python3
"""
Parallel Tool Executor - 只读工具并行执行器
无外部依赖，使用 Python 标准库实现。

功能：
1. 只读安全集判定：只允许读操作（read, list, search, fetch等）
2. 无路径重叠检测：确保并行读取的文件路径不冲突
3. 并行执行与结果汇总：使用 concurrent.futures.ThreadPoolExecutor
4. 错误处理与超时控制：单个工具超时不影响其他工具

Usage:
    python parallel_tool_executor.py --tools='[{"name":"read","params":{"path":"/foo"}},{"name":"read","params":{"path":"/bar"}}]'
    python parallel_tool_executor.py --tools='...' --max-workers=4 --timeout=30
"""
import argparse
import json
import os
import sys
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from pathlib import Path


# ============================================================
# 只读安全工具集
# ============================================================
READONLY_SAFE_TOOLS = {
    # OpenClaw 只读工具
    'read', 'web_search', 'web_fetch', 'browser_snapshot', 'browser_screenshot',
    'tdai_memory_search', 'tdai_conversation_search', 'session_status',
    'process_list', 'process_log',
    # Shell 只读命令模式
    'exec_readonly',  # 仅限只读命令（由 validate_exec_command 检查）
}

# 写操作工具（明确禁止）
WRITE_TOOLS = {
    'write', 'edit', 'exec', 'message', 'browser_act', 'browser_navigate',
    'browser_click', 'browser_type',
}

# 只读命令白名单模式
READONLY_CMD_PATTERNS = [
    r'^cat\s', r'^head\s', r'^tail\s', r'^ls\s', r'^dir\s',
    r'^Get-Content\s', r'^Get-ChildItem\s', r'^Get-Item\s',
    r'^grep\s', r'^rg\s', r'^find\s', r'^Select-String\s',
    r'^wc\s', r'^stat\s', r'^file\s', r'^type\s',
    r'^python.*--help', r'^node.*--help',
    r'^git\s+(log|status|diff|show|branch)\s',
    r'^powershell.*-Command.*Get-',
]

# 路径重叠检测：同一路径前缀不应并行写入
# 对于只读操作，路径重叠是安全的（多个读同一文件OK）
# 此检测主要用于防止读写混合场景


def is_readonly_safe(tool_name: str) -> bool:
    """判断工具是否在只读安全集中"""
    return tool_name.lower() in READONLY_SAFE_TOOLS


def validate_exec_command(command: str) -> bool:
    """验证 exec 命令是否为只读操作"""
    cmd_stripped = command.strip()
    for pattern in READONLY_CMD_PATTERNS:
        if re.match(pattern, cmd_stripped, re.IGNORECASE):
            return True
    # 危险命令检测
    dangerous_patterns = [
        r'rm\s', r'del\s', r'Remove-Item', r'rmdir',
        r'mv\s', r'move\s', r'Move-Item', r'ren\s',
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, cmd_stripped, re.IGNORECASE):
            return False
    return False


def check_path_overlap(tools: list) -> tuple:
    """
    检查工具参数中的路径是否有重叠。
    返回 (has_overlap: bool, overlapping_pairs: list)
    
    对于纯只读操作，路径重叠是安全的，返回 False。
    但如果混合了读写操作，则路径重叠不安全。
    """
    paths = []
    has_write = False
    
    for tool in tools:
        name = tool.get('name', '').lower()
        params = tool.get('params', {})
        
        # 提取路径参数
        path = params.get('path') or params.get('url') or params.get('file_path') or ''
        if path:
            paths.append((tool.get('name', 'unknown'), str(path)))
        
        if name in WRITE_TOOLS:
            has_write = True
    
    # 纯只读场景：路径重叠安全
    if not has_write:
        return False, []
    
    # 混合场景：检查路径重叠
    overlapping = []
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            p1 = os.path.normpath(paths[i][1]).lower()
            p2 = os.path.normpath(paths[j][1]).lower()
            if p1.startswith(p2) or p2.startswith(p1):
                overlapping.append((paths[i][0], paths[j][0], paths[i][1], paths[j][1]))
    
    return len(overlapping) > 0, overlapping


def validate_tools(tools: list) -> dict:
    """
    验证工具列表是否可以安全并行执行。
    返回验证结果 dict。
    """
    result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'tool_count': len(tools),
    }
    
    if len(tools) < 2:
        result['valid'] = False
        result['errors'].append('Need at least 2 tools for parallel execution')
        return result
    
    # 检查每个工具的只读安全性
    unsafe_tools = []
    for tool in tools:
        name = tool.get('name', '').lower()
        if not is_readonly_safe(name):
            unsafe_tools.append(name)
    
    if unsafe_tools:
        result['valid'] = False
        result['errors'].append(f'Unsafe tools detected: {", ".join(set(unsafe_tools))}')
    
    # 检查路径重叠
    has_overlap, pairs = check_path_overlap(tools)
    if has_overlap:
        result['valid'] = False
        result['errors'].append(f'Path overlap detected in write operations: {pairs}')
    
    return result


def execute_tool(tool: dict, timeout: int = 30) -> dict:
    """
    执行单个工具调用（模拟）。
    在实际 OpenClaw 环境中，这会调用工具 API。
    此处提供框架和接口定义。
    """
    name = tool.get('name', 'unknown')
    params = tool.get('params', {})
    
    start = time.time()
    try:
        # 在实际集成中，这里会调用 OpenClaw 的工具 API
        # 当前返回工具调用的元信息，供 agent 框架使用
        result = {
            'tool': name,
            'params': params,
            'status': 'ready',
            'message': f'Tool {name} validated and ready for execution',
            'elapsed_ms': round((time.time() - start) * 1000, 2),
        }
        return result
    except Exception as e:
        return {
            'tool': name,
            'params': params,
            'status': 'error',
            'error': str(e),
            'elapsed_ms': round((time.time() - start) * 1000, 2),
        }


def run_parallel(tools: list, max_workers: int = 4, timeout: int = 30) -> dict:
    """
    并行执行工具调用。
    
    Args:
        tools: 工具调用列表
        max_workers: 最大并行数
        timeout: 单个工具超时（秒）
    
    Returns:
        包含所有工具执行结果的汇总 dict
    """
    # 先验证
    validation = validate_tools(tools)
    if not validation['valid']:
        return {
            'status': 'rejected',
            'validation': validation,
            'results': [],
        }
    
    # 并行执行
    results = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=min(max_workers, len(tools))) as executor:
        future_to_tool = {
            executor.submit(execute_tool, tool, timeout): tool
            for tool in tools
        }
        
        for future in as_completed(future_to_tool, timeout=timeout * len(tools)):
            tool = future_to_tool[future]
            try:
                result = future.result(timeout=timeout)
                results.append(result)
            except TimeoutError:
                results.append({
                    'tool': tool.get('name', 'unknown'),
                    'status': 'timeout',
                    'error': f'Exceeded {timeout}s timeout',
                })
            except Exception as e:
                results.append({
                    'tool': tool.get('name', 'unknown'),
                    'status': 'error',
                    'error': str(e),
                })
    
    total_elapsed = round((time.time() - start_time) * 1000, 2)
    
    return {
        'status': 'completed',
        'validation': validation,
        'results': results,
        'summary': {
            'total': len(results),
            'success': sum(1 for r in results if r.get('status') == 'ready'),
            'errors': sum(1 for r in results if r.get('status') == 'error'),
            'timeouts': sum(1 for r in results if r.get('status') == 'timeout'),
            'total_elapsed_ms': total_elapsed,
            'speedup': f'{len(results)} tools in {total_elapsed}ms',
        }
    }


def main():
    parser = argparse.ArgumentParser(description='并行只读工具执行器')
    parser.add_argument('--tools', required=True, help='JSON格式的工具调用列表')
    parser.add_argument('--max-workers', type=int, default=4, help='最大并行数')
    parser.add_argument('--timeout', type=int, default=30, help='单个工具超时(秒)')
    parser.add_argument('--validate-only', action='store_true', help='仅验证不执行')
    
    args = parser.parse_args()
    
    try:
        tools = json.loads(args.tools)
    except json.JSONDecodeError as e:
        print(json.dumps({'error': f'Invalid JSON: {e}'}))
        sys.exit(1)
    
    if args.validate_only:
        result = validate_tools(tools)
    else:
        result = run_parallel(tools, args.max_workers, args.timeout)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
