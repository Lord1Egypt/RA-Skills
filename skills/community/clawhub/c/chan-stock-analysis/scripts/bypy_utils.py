#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度云盘工具模块
- 从百度云盘下载历史K线数据
- 上传分析报告和图表到百度云盘
"""

import os
import sys
import subprocess
import json
import io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def run_bypy_command(args, timeout=60):
    """执行bypy命令"""
    try:
        result = subprocess.run(
            ['bypy'] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            errors='replace'
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, '', 'Timeout'
    except Exception as e:
        return -1, '', str(e)


def check_bypy_auth():
    """检查bypy是否已授权"""
    ret, out, err = run_bypy_command(['whoami'])
    if ret == 0 and 'username' in out.lower():
        return True
    return False


def download_kline_from_baidu(code, level, local_dir):
    """
    从百度云盘下载K线数据文件
    
    Args:
        code: 股票代码
        level: K线级别 (daily, 30min, 5min, 1min)
        local_dir: 本地保存目录
    
    Returns:
        (success, filepath)
    """
    # 百度云盘路径
    remote_path = f"/knowledge/stockdata/{code}/{code}_{level}_k线.md"
    local_path = os.path.join(local_dir, f"{code}_{level}_k线.md")
    
    # 确保本地目录存在
    os.makedirs(local_dir, exist_ok=True)
    
    # 下载文件
    ret, out, err = run_bypy_command(['downfile', remote_path, local_path])
    
    if ret == 0 and os.path.exists(local_path):
        print(f"   📥 从百度云盘下载: {remote_path}")
        return True, local_path
    else:
        return False, None


def upload_to_baidu(local_path, remote_path):
    """
    上传文件到百度云盘
    
    Args:
        local_path: 本地文件路径
        remote_path: 百度云盘远程路径
    
    Returns:
        (success, message)
    """
    if not os.path.exists(local_path):
        return False, f"本地文件不存在: {local_path}"
    
    # 确保远程目录存在
    remote_dir = os.path.dirname(remote_path)
    if remote_dir:
        run_bypy_command(['mkdir', remote_dir])
    
    # 上传文件（覆盖）
    ret, out, err = run_bypy_command(['upload', local_path, remote_path, 'overwrite'])
    
    if ret == 0:
        print(f"   📤 上传到百度云盘: {remote_path}")
        return True, "上传成功"
    else:
        return False, f"上传失败: {err}"


def upload_report_to_baidu(report_path, chart_path, date_str, code):
    """
    上传分析报告和图表到百度云盘
    
    Args:
        report_path: 分析报告本地路径
        chart_path: 图表本地路径
        date_str: 日期字符串 (YYYY-MM-DD)
        code: 股票代码
    
    Returns:
        (report_success, chart_success)
    """
    report_success = False
    chart_success = False
    
    # 上传报告
    if report_path and os.path.exists(report_path):
        remote_report = f"/knowledge/stock/{date_str}/{os.path.basename(report_path)}"
        report_success, _ = upload_to_baidu(report_path, remote_report)
    
    # 上传图表
    if chart_path and os.path.exists(chart_path):
        remote_chart = f"/knowledge/stock/{date_str}/{os.path.basename(chart_path)}"
        chart_success, _ = upload_to_baidu(chart_path, remote_chart)
    
    return report_success, chart_success


def load_kline_from_md(filepath):
    """
    从Markdown文件加载K线数据
    
    Args:
        filepath: Markdown文件路径
    
    Returns:
        list of kline dicts
    """
    if not os.path.exists(filepath):
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 尝试解析Markdown中的JSON数据
        # 格式可能是: ```json\n[...]\n``` 或直接JSON数组
        import re
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', content)
        if json_match:
            json_str = json_match.group(1)
        else:
            # 尝试直接解析
            json_match = re.search(r'\[\s*\{[\s\S]*\}\s*\]', content)
            if json_match:
                json_str = json_match.group(0)
            else:
                return None
        
        klines = json.loads(json_str)
        return klines
    except Exception as e:
        print(f"   ⚠️ 解析K线文件失败: {e}")
        return None


def save_kline_to_md(klines, filepath, code, level):
    """
    保存K线数据到Markdown文件
    
    Args:
        klines: K线数据列表
        filepath: 保存路径
        code: 股票代码
        level: K线级别
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {code} {level} K线数据\n\n")
        f.write(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"数据条数: {len(klines)}\n\n")
        f.write("```json\n")
        f.write(json.dumps(klines, ensure_ascii=False, indent=2))
        f.write("\n```\n")
    
    print(f"   💾 保存K线数据: {filepath}")


def merge_kline_data(old_klines, new_klines, max_count=500):
    """
    合并旧的K线数据和新的K线数据
    
    Args:
        old_klines: 旧的K线数据
        new_klines: 新的K线数据
        max_count: 最大保留条数
    
    Returns:
        合并后的K线数据
    """
    if not old_klines:
        return new_klines[:max_count] if new_klines else None
    
    if not new_klines:
        return old_klines[-max_count:] if old_klines else None
    
    # 创建时间索引
    old_times = {k['datetime']: k for k in old_klines}
    
    # 合并数据
    merged = list(old_klines)
    for k in new_klines:
        dt = k['datetime']
        if dt not in old_times:
            merged.append(k)
    
    # 按时间排序并截取
    merged.sort(key=lambda x: x['datetime'])
    return merged[-max_count:]


if __name__ == "__main__":
    # 测试
    print("测试百度云盘工具...")
    
    # 检查授权
    if check_bypy_auth():
        print("✅ bypy已授权")
    else:
        print("❌ bypy未授权，请先运行 'bypy info' 进行授权")
    
    # 测试下载
    success, path = download_kline_from_baidu("XAUUSD", "daily", "D:/QClawData/workspace/test_baidu")
    if success:
        print(f"✅ 下载成功: {path}")
    else:
        print("❌ 下载失败或文件不存在")
