#!/usr/bin/env python3
"""
akshare-stock技能包装器
提供OpenClaw原生技能接口
"""

import sys
import os
import subprocess
import re
from typing import Optional, Tuple

def run_akshare_query(query: str, platform: str = "qq") -> str:
    """执行akshare查询
    
    Args:
        query: 自然语言查询
        platform: 输出平台格式 (qq/telegram)
    
    Returns:
        格式化后的查询结果
    """
    skill_path = "/root/.openclaw/skills/akshare-stock"
    cmd = ["python3", "main.py", "--query", query, "--platform", platform]
    
    # 设置超时时间（根据查询类型调整）
    timeout = 15
    if any(keyword in query for keyword in ["港股", "美股", "可转债", "基金"]):
        timeout = 25  # 跨市场查询更慢
    
    try:
        result = subprocess.run(
            cmd,
            cwd=skill_path,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=timeout
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            # 清理输出中的进度条字符
            output = re.sub(r'\s*\d+%\|.*?\|\s*\d+/\d+.*?\n', '', output)
            output = re.sub(r'\s*\[\d+:\d+<\d+:\d+.*?\].*?\n', '', output)
            output = output.strip()
            
            if output:
                return output
            else:
                return "⚠️ 查询成功但返回结果为空"
        else:
            error_msg = result.stderr.strip() if result.stderr else "未知错误"
            # 提取关键错误信息
            if "ImportError" in error_msg:
                return "❌ 导入错误：请确认akshare已安装 (pip install akshare)"
            elif "Connection" in error_msg or "网络" in error_msg:
                return "🌐 网络连接错误：请检查网络连接后重试"
            elif "timeout" in error_msg.lower():
                return f"⏰ 查询超时 ({timeout}秒)：请简化查询条件或稍后重试"
            else:
                return f"❌ 查询失败: {error_msg[:200]}"
            
    except subprocess.TimeoutExpired:
        return f"⏰ 查询超时 ({timeout}秒)，请简化查询条件或稍后重试"
    except FileNotFoundError:
        return "❌ 找不到akshare-stock技能文件，请确认技能安装正确"
    except Exception as e:
        return f"⚠️ 执行错误: {str(e)[:200]}"

def preprocess_query(query: str) -> Tuple[str, str]:
    """预处理查询，提取平台偏好
    
    Returns:
        (processed_query, platform)
    """
    # 默认平台
    platform = "qq"
    
    # 清理查询
    query = query.strip()
    
    # 检查平台提示（未来扩展）
    if "--telegram" in query:
        platform = "telegram"
        query = query.replace("--telegram", "").strip()
    elif "--qq" in query:
        platform = "qq"
        query = query.replace("--qq", "").strip()
    
    return query, platform

def show_help() -> str:
    """显示帮助信息"""
    help_text = """📈 A股分析技能使用帮助

常用查询示例：
--------------------
📊 大盘行情
  • A股大盘
  • 上证指数
  • 创业板指

📈 个股分析
  • 贵州茅台近30日K线
  • 茅台资金流向
  • 600519怎么样

🧩 板块分析
  • 行业板块涨跌
  • 概念板块涨跌
  • 板块资金流向

🚦 市场统计
  • 今日涨停
  • 连板梯队

🌏 其他市场
  • 港股行情
  • 美股行情

📰 新闻研究
  • 财经新闻
  • 宁德时代研报

💡 使用提示：
1. 支持股票代码（600519）和常用名称（茅台）
2. 可指定时间范围（近30日、周线、月线）
3. 复杂查询可能需要更长时间
4. 数据非实时，有少许延迟

输入任意查询即可开始使用！"""
    return help_text

def main():
    """主函数：OpenClaw技能入口"""
    if len(sys.argv) < 2:
        # 没有参数时显示帮助
        print(show_help())
        sys.exit(0)
    
    # 获取查询参数
    query = " ".join(sys.argv[1:])
    
    # 处理帮助请求
    if query.lower() in ["帮助", "help", "--help", "-h", "用法", "怎么用"]:
        print(show_help())
        sys.exit(0)
    
    # 处理版本请求
    if query.lower() in ["版本", "version", "--version", "-v"]:
        print("akshare-wrapper v1.0 (2026-03-11)")
        sys.exit(0)
    
    # 预处理查询
    processed_query, platform = preprocess_query(query)
    
    # 执行查询
    result = run_akshare_query(processed_query, platform)
    
    # 输出结果
    print(result)

if __name__ == "__main__":
    main()