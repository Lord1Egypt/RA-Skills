#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finoview 期货研究报告 API 调用脚本
用于获取 finoview.com.cn 的期货研究报告数据

使用方式：
    1. 首次使用需设置环境变量 FINOVIEW_API_KEY 和 FINOVIEW_API_SECRET
    2. Linux/Mac: export FINOVIEW_API_KEY="your_key" && export FINOVIEW_API_SECRET="your_secret"
    3. Windows: set FINOVIEW_API_KEY="your_key" && set FINOVIEW_API_SECRET="your_secret"
    4. 或在系统环境变量中配置这两个变量

    reports = get_data_from_api("2026-03-29")
    reports = get_data_from_api("2026-03-29", "2502")  # 黑色金属
    reports = get_data_from_api("2026-03-29", "2505")  # 能源化工
"""

import os
import http.client
import json
from typing import List, Dict, Any, Optional


def get_credentials() -> tuple:
    """
    从环境变量获取 API 凭证
    
    Returns:
        (appkey, appsecret) 元组，如果未配置则返回 None
    
    Raises:
        ValueError: 当凭证未配置时抛出友好错误提示
    """
    appkey = os.environ.get("FINOVIEW_API_KEY")
    appsecret = os.environ.get("FINOVIEW_API_SECRET")
    
    if not appkey or not appsecret:
        error_msg = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║  ⚠️  API 凭证未配置                                                         ║
║                                                                            ║
║  为了使用此功能，您需要配置 finoview API 的凭证：                          ║
║                                                                            ║
║  1. 设置环境变量：                                                        ║
║     - FINOVIEW_API_KEY: 您的 API Key                                      ║
║     - FINOVIEW_API_SECRET: 您的 API Secret                                ║
║                                                                            ║
║  2. 配置方法：                                                            ║
║     - 临时设置（当前会话）：                                                ║
║       Linux/Mac:  export FINOVIEW_API_KEY="your_key"                       ║
║                    export FINOVIEW_API_SECRET="your_secret"                ║
║       Windows:    set FINOVIEW_API_KEY="your_key"                          ║
║                    set FINOVIEW_API_SECRET="your_secret"                   ║
║                                                                            ║
║     - 永久设置：                                                            ║
║       将上述 export 命令添加到 ~/.bashrc、~/.bash_profile 或 ~/.zshrc        ║
║       或在系统环境变量中直接配置                                           ║
║                                                                            ║
║  3. 获取凭证：                                                              ║
║     请联系 finoview.com.cn 获取您的 API 凭证                                 ║
║                                                                            ║
║  💡 提示：配置完成后重启应用即可生效                                       ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
        """
        raise ValueError(error_msg)
    
    return appkey, appsecret


def get_data_from_api(date: str, indCode: str = "") -> List[Dict[str, Any]]:
    """
    调用 finoview API 获取期货研究报告
    
    Args:
        date: 报告查询日期，格式：YYYY-MM-DD
        indCode: 期货类别代码（可选，留空获取全部类别）
    
    Returns:
        报告列表，每个报告包含标题、作者、摘要、PDF 链接等信息
    
    Raises:
        ValueError: API 凭证未配置
        Exception: API 调用失败
    """
    # 获取 API 凭证
    appkey, appsecret = get_credentials()
    
    conn = http.client.HTTPSConnection("www.finoview.com.cn")
    
    # 构建请求参数
    params = {
        "time": date,
        "appkey": appkey,
        "appsecret": appsecret
    }
    if indCode:
        params["indCode"] = indCode
    
    payload = json.dumps(params)
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': 'www.finoview.com.cn',
        'Connection': 'keep-alive'
    }
    conn.request("POST", "/autoApi/foreign/report_list", payload, headers)
    res = conn.getresponse()
    data = res.read()
    datas = json.loads(data.decode("utf-8"))
    datas = datas['data']
    return datas


def get_data_from_api_safe(date: str, indCode: str = "") -> List[Dict[str, Any]]:
    """
    带错误处理的 API 调用函数
    
    Args:
        date: 报告查询日期，格式：YYYY-MM-DD
        indCode: 期货类别代码（可选）
    
    Returns:
        报告列表，出错时返回空列表，并打印错误信息
    """
    try:
        conn = http.client.HTTPSConnection("www.finoview.com.cn", timeout=10)
        
        # 获取 API 凭证
        appkey, appsecret = get_credentials()
        
        # 构建请求参数
        params = {
            "time": date,
            "appkey": appkey,
            "appsecret": appsecret
        }
        if indCode:
            params["indCode"] = indCode
        
        payload = json.dumps(params)
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': 'www.finoview.com.cn',
            'Connection': 'keep-alive'
        }
        conn.request("POST", "/autoApi/foreign/report_list", payload, headers)
        res = conn.getresponse()
        
        if res.status != 200:
            raise Exception(f"API 返回状态码：{res.status}")
            
        data = json.loads(res.read().decode("utf-8"))
        
        if 'data' not in data:
            raise Exception(f"API 返回数据格式错误：{data}")
            
        return data['data']
        
    except ValueError as e:
        # 凭证未配置的错误
        print(f"\n⚠️  {e}\n")
        return []
    except Exception as e:
        # 其他错误
        print(f"\n❌ API 调用失败：{e}\n")
        return []


def format_reports_to_markdown(reports: List[Dict[str, Any]], date: str = "") -> str:
    """
    将报告列表格式化为 Markdown 格式
    
    Args:
        reports: API 返回的报告列表
        date: 查询日期
    
    Returns:
        Markdown 格式的字符串
    """
    if not reports:
        return "暂无报告数据或 API 调用失败，请检查 API 凭证配置"
    
    output = []
    output.append(f"## Finoview 期货研究报告 - {date}\n")
    output.append(f"**报告数量**: {len(reports)}\n")
    output.append("---\n")
    
    for i, report in enumerate(reports, 1):
        output.append(f"### {i}. {report.get('title', '无标题')}\n")
        output.append(f"- **作者**: {report.get('author', '未知')}\n")
        output.append(f"- **类型**: {report.get('type', '未知')}\n")
        output.append(f"- **类别**: {report.get('varietyNames', report.get('indName', '未知'))}\n")
        output.append(f"- **日期**: {report.get('time', '未知')}\n")
        summary = report.get('summary', '无摘要')
        if len(summary) > 200:
            summary = summary[:200] + "..."
        output.append(f"- **摘要**: {summary}\n")
        output.append(f"- **PDF**: [{report.get('title', '下载 PDF')}]({report.get('url', '#')})\n")
        output.append("")
    
    return "\n".join(output)


def format_reports_to_table(reports: List[Dict[str, Any]]) -> str:
    """
    将报告列表格式化为 Markdown 表格
    
    Args:
        reports: API 返回的报告列表
    
    Returns:
        Markdown 表格格式的字符串
    """
    if not reports:
        return "暂无报告数据或 API 调用失败，请检查 API 凭证配置"
    
    # 表头
    output = []
    output.append("| 标题 | 作者 | 类型 | 类别 | 日期 | PDF 链接 |")
    output.append("|------|------|------|------|------|----------|")
    
    for report in reports:
        title = report.get('title', '无标题')[:30]
        author = report.get('author', '未知')[:20]
        rep_type = report.get('type', '未知')
        variety = report.get('varietyNames', report.get('indName', '未知'))[:20]
        time = report.get('time', '未知')
        url = f"[PDF]({report.get('url', '#')})"
        
        output.append(f"| {title} | {author} | {rep_type} | {variety} | {time} | {url} |")
    
    return "\n".join(output)


def check_credentials_status() -> bool:
    """
    检查 API 凭证是否已配置
    
    Returns:
        True 如果凭证已配置，否则返回 False
    """
    appkey = os.environ.get("FINOVIEW_API_KEY")
    appsecret = os.environ.get("FINOVIEW_API_SECRET")
    
    if not appkey or not appsecret:
        print("\n⚠️  API 凭证未配置")
        print("请设置以下环境变量：")
        print("  - FINOVIEW_API_KEY")
        print("  - FINOVIEW_API_SECRET")
        print("\n参考配置方法：")
        print("  Linux/Mac: export FINOVIEW_API_KEY='your_key'")
        print("             export FINOVIEW_API_SECRET='your_secret'")
        print("  Windows:   set FINOVIEW_API_KEY='your_key'")
        print("             set FINOVIEW_API_SECRET='your_secret'\n")
        return False
    
    print("✅ API 凭证已配置")
    return True


if __name__ == "__main__":
    # 首先检查凭证状态
    print("=" * 60)
    print("Finoview API 测试脚本")
    print("=" * 60)
    
    if not check_credentials_status():
        print("\n请配置 API 凭证后再运行此脚本")
        exit(1)
    
    # 测试调用
    print("\n获取 2026 年 3 月 29 日的所有报告...")
    reports = get_data_from_api("2026-03-29")
    
    if reports:
        print(f"\n✅ 共获取 {len(reports)} 篇报告\n")
        
        # 打印第一篇文章的详细信息
        first_report = reports[0]
        print("第一篇文章详情:")
        print(f"  标题：{first_report['title']}")
        print(f"  作者：{first_report['author']}")
        print(f"  类型：{first_report['type']}")
        print(f"  类别：{first_report['varietyNames']}")
        print(f"  日期：{first_report['time']}")
        print(f"  摘要：{first_report['summary'][:100]}...")
        print(f"  PDF: {first_report['url']}")
        
        # 显示表格格式
        print("\n" + "=" * 60)
        print("报告列表（表格格式）:")
        print("=" * 60)
        print(format_reports_to_table(reports[:5]))  # 只显示前 5 篇
        
    else:
        print("\n❌ 未获取到报告数据，请检查 API 凭证配置或网络连接")
