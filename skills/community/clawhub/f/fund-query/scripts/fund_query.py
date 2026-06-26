#!/usr/bin/env python3
"""
Fund Query Script
查询场外基金（公募基金）的实时估值、历史净值和基本信息。
使用天天基金（东方财富）公开 API。

用法:
    python3 fund_query.py <fund_code> [command]

参数:
    fund_code: 6位基金代码，如 005827, 110022
    command:   查询命令
               - estimate 或不传: 实时估值（默认）
               - info: 基金基本信息
               - history: 历史净值

示例:
    python3 fund_query.py 005827
    python3 fund_query.py 005827 info
    python3 fund_query.py 005827 history
"""

from __future__ import annotations

import sys
import json
import re
import urllib.request
import urllib.error
from datetime import datetime

# 输入校验：基金代码必须是6位数字
VALID_CODE_PATTERN = re.compile(r'^\d{6}$')


def validate_code(code: str) -> str | None:
    """校验基金代码。返回 None 表示合法，否则返回错误信息。"""
    if not VALID_CODE_PATTERN.match(code):
        return f"非法的基金代码 '{code}'。基金代码必须是6位数字。"
    return None


def fetch_jsonp(url: str) -> str:
    """获取 JSONP 响应内容"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'http://fund.eastmoney.com/'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        raise Exception(f"网络请求失败: {str(e)}")


def parse_jsonp(jsonp_str: str) -> dict | None:
    """解析 JSONP 响应为 JSON 对象"""
    # 格式: jsonpgz({"fundcode":"005827",...});
    match = re.search(r'\((.+)\)', jsonp_str, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
    return None


def get_estimate(fund_code: str) -> dict:
    """查询实时估值"""
    url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
    try:
        raw = fetch_jsonp(url)
        data = parse_jsonp(raw)
        
        if not data:
            return {
                "status": "error",
                "message": f"未找到基金 {fund_code}，请检查代码是否正确"
            }
        
        # 解析估值数据
        return {
            "status": "success",
            "code": data.get("fundcode", fund_code),
            "name": data.get("name", ""),
            "estimate_time": data.get("gztime", ""),  # 估值时间
            "estimate_value": float(data.get("gsz", 0)),  # 估值
            "estimate_change_pct": float(data.get("gszzl", 0)),  # 涨跌幅%
            "nav_date": data.get("jzrq", ""),  # 净值日期
            "nav_value": float(data.get("dwjz", 0)),  # 单位净值
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_info(fund_code: str) -> dict:
    """查询基金基本信息"""
    url = f"http://fund.eastmoney.com/pingzhongdata/{fund_code}.js"
    try:
        raw = fetch_jsonp(url)
        
        # 解析 JS 变量
        def extract_var(name: str, text: str) -> str:
            match = re.search(rf'var\s+{name}\s*=\s*"([^"]*)"', text)
            return match.group(1) if match else ""
        
        def extract_num(name: str, text: str) -> float:
            match = re.search(rf'var\s+{name}\s*=\s*([\d.]+)', text)
            return float(match.group(1)) if match else 0
        
        return {
            "status": "success",
            "code": fund_code,
            "name": extract_var("fS_name", raw),
            "type": extract_var("fS_code", raw),
            "establish_date": extract_var("fS_establishment", raw),
            "scale": extract_num("fS_scale", raw),  # 亿元
        }
    except Exception as e:
        # 如果详细信息获取失败，尝试从估值接口获取基本信息
        estimate = get_estimate(fund_code)
        if estimate.get("status") == "success":
            return {
                "status": "success",
                "code": fund_code,
                "name": estimate.get("name", ""),
                "type": "未知",
                "establish_date": "未知",
                "scale": 0,
            }
        return {"status": "error", "message": str(e)}


def get_history(fund_code: str, page_size: int = 10) -> dict:
    """查询历史净值"""
    url = f"http://api.fund.eastmoney.com/f10/lsjz?fundCode={fund_code}&pageIndex=1&pageSize={page_size}"
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'http://fund.eastmoney.com/'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        
        if data.get("ErrCode") != 0:
            return {
                "status": "error",
                "message": data.get("ErrMsg", "查询失败")
            }
        
        records = data.get("Data", {}).get("LSJZList", [])
        
        history = []
        for r in records:
            history.append({
                "date": r.get("FSRQ", ""),  # 净值日期
                "nav": float(r.get("DWJZ", 0)),  # 单位净值
                "acc_nav": float(r.get("LJJZ", 0)),  # 累计净值
                "change_pct": float(r.get("JZZZL", 0)) if r.get("JZZZL") else 0,  # 涨跌幅
            })
        
        return {
            "status": "success",
            "code": fund_code,
            "count": len(history),
            "history": history
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def format_estimate(data: dict) -> str:
    """格式化估值输出"""
    if data.get("status") != "success":
        return f"❌ {data.get('message', '查询失败')}"
    
    arrow = "↑" if data["estimate_change_pct"] >= 0 else "↓"
    return f"""📊 **{data['name']}**（{data['code']}）

💰 实时估值：{data['estimate_value']:.4f} 元 | 📈 涨跌幅：{data['estimate_change_pct']:.2f}% {arrow}
📅 估值时间：{data['estimate_time']}
📊 昨日净值：{data['nav_value']:.4f} 元（{data['nav_date']}）"""


def format_info(data: dict) -> str:
    """格式化基金信息输出"""
    if data.get("status") != "success":
        return f"❌ {data.get('message', '查询失败')}"
    
    scale_text = f"{data['scale']:.2f} 亿元" if data.get("scale", 0) > 0 else "未知"
    return f"""📊 **{data['name']}**（{data['code']}）

📋 基金类型：{data.get('type', '未知')}
📅 成立日期：{data.get('establish_date', '未知')}
💰 基金规模：{scale_text}"""


def format_history(data: dict) -> str:
    """格式化历史净值输出"""
    if data.get("status") != "success":
        return f"❌ {data.get('message', '查询失败')}"
    
    lines = [f"📊 **基金 {data['code']} 历史净值**（最近 {data['count']} 条）\n"]
    lines.append("```\n日期          单位净值    累计净值    涨跌幅")
    lines.append("-" * 45)
    
    for h in data.get("history", []):
        arrow = "↑" if h["change_pct"] >= 0 else "↓"
        lines.append(f"{h['date']}    {h['nav']:.4f}    {h['acc_nav']:.4f}    {h['change_pct']:+.2f}% {arrow}")
    
    lines.append("```")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "message": "用法: python3 fund_query.py <fund_code> [estimate|info|history]"
        }, ensure_ascii=False))
        sys.exit(1)
    
    fund_code = sys.argv[1].strip()
    command = sys.argv[2].strip().lower() if len(sys.argv) > 2 else "estimate"
    
    # 校验基金代码
    validation_error = validate_code(fund_code)
    if validation_error:
        print(json.dumps({"status": "error", "message": validation_error}, ensure_ascii=False))
        sys.exit(1)
    
    # 执行查询
    if command == "estimate":
        result = get_estimate(fund_code)
        print(format_estimate(result))
    elif command == "info":
        result = get_info(fund_code)
        print(format_info(result))
    elif command == "history":
        result = get_history(fund_code)
        print(format_history(result))
    else:
        print(json.dumps({
            "status": "error",
            "message": f"未知命令 '{command}'。支持: estimate, info, history"
        }, ensure_ascii=False))
        sys.exit(1)
    
    if result.get("status") != "success":
        sys.exit(1)


if __name__ == "__main__":
    main()
