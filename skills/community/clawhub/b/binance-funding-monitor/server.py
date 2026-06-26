#!/usr/bin/env python3
"""
币安资金费率套利监控 - SkillPay 收费版 MCP Server
每次调用收费 0.001 USDT
"""

import os
import sys
import json
import asyncio
from typing import Any, Dict, List
from datetime import datetime

# MCP Server 框架
from mcp.server import Server
from mcp.types import TextContent

# SkillPay 支付验证 - 从环境变量读取
SKILLPAY_API_KEY = os.getenv("SKILLPAY_API_KEY", "")
SKILLPAY_ENDPOINT = os.getenv("SKILLPAY_ENDPOINT", "https://api.skillpay.me/v1")

# 币安监控模块 - 使用本地副本
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from funding_arbitrage import FundingRateArbitrage

app = Server("binance-funding-monitor")


async def verify_payment(session_id: str) -> bool:
    """验证用户是否已支付 - 使用 SkillPay API"""
    if not SKILLPAY_API_KEY or SKILLPAY_API_KEY == "YOUR_API_KEY_HERE":
        # 开发模式：跳过支付验证
        return True
    
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{SKILLPAY_ENDPOINT}/verify",
                headers={
                    "Authorization": f"Bearer {SKILLPAY_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "session_id": session_id,
                    "skill_name": "binance-funding-monitor",
                    "amount": "1",
                    "currency": "USDT"
                }
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result.get("verified", False)
                else:
                    print(f"SkillPay API 错误: {resp.status}", file=sys.stderr)
                    return False
    except Exception as e:
        print(f"Payment verification error: {e}", file=sys.stderr)
        return False


@app.call_tool()
async def get_account_summary(arguments: dict) -> List[TextContent]:
    """获取币安账户总览"""
    session_id = arguments.get("session_id", "")
    
    if not await verify_payment(session_id):
        return [TextContent(
            type="text",
            text="❌ 支付验证失败。请先在 SkillPay 完成支付 (0.001 USDT)。"
        )]
    
    try:
        trader = FundingRateArbitrage()
        total, available = trader.get_account_balance()
        used = total - available
        used_pct = (used / total * 100) if total > 0 else 0
        
        report = f"""📊 币安账户总览
━━━━━━━━━━━━━━━━━━━━
💰 总权益: {total:.2f} USDT
🔒 已用保证金: {used:.2f} USDT ({used_pct:.1f}%)
💵 可用余额: {available:.2f} USDT
━━━━━━━━━━━━━━━━━━━━"""
        
        return [TextContent(type="text", text=report)]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取账户信息失败: {e}")]


@app.call_tool()
async def get_positions(arguments: dict) -> List[TextContent]:
    """获取当前持仓"""
    session_id = arguments.get("session_id", "")
    
    if not await verify_payment(session_id):
        return [TextContent(
            type="text",
            text="❌ 支付验证失败。请先在 SkillPay 完成支付 (0.001 USDT)。"
        )]
    
    try:
        trader = FundingRateArbitrage()
        positions = trader.get_positions()
        
        if not positions:
            return [TextContent(type="text", text="📭 当前无持仓")]
        
        lines = [f"📈 当前持仓 ({len(positions)} 个)", "━━━━━━━━━━━━━━━━━━━━"]
        for p in positions:
            emoji = "🟢" if p['unrealized_pnl'] >= 0 else "🔴"
            lines.append(f"{p['symbol']}: {p['side']} {emoji}{p['unrealized_pnl']:+.2f} USDT")
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        
        return [TextContent(type="text", text="\n".join(lines))]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取持仓失败: {e}")]


@app.call_tool()
async def get_funding_income(arguments: dict) -> List[TextContent]:
    """获取资金费收入统计"""
    session_id = arguments.get("session_id", "")
    days = arguments.get("days", 7)
    
    if not await verify_payment(session_id):
        return [TextContent(
            type="text",
            text="❌ 支付验证失败。请先在 SkillPay 完成支付 (0.001 USDT)。"
        )]
    
    try:
        import time
        trader = FundingRateArbitrage()
        
        end_time = int(time.time() * 1000)
        start_time = end_time - (days * 24 * 60 * 60 * 1000)
        
        data = trader._request('GET', '/fapi/v1/income', {
            'incomeType': 'FUNDING_FEE',
            'startTime': start_time,
            'endTime': end_time,
            'limit': 1000
        }, signed=True)
        
        total_income = sum(float(item.get('income', 0)) for item in data)
        
        report = f"""💰 资金费收入统计 (近{days}天)
━━━━━━━━━━━━━━━━━━━━
总计收入: {total_income:+.4f} USDT
━━━━━━━━━━━━━━━━━━━━"""
        
        return [TextContent(type="text", text=report)]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取资金费收入失败: {e}")]


@app.call_tool()
async def get_full_report(arguments: dict) -> List[TextContent]:
    """获取完整监控报告"""
    session_id = arguments.get("session_id", "")
    
    if not await verify_payment(session_id):
        return [TextContent(
            type="text",
            text="❌ 支付验证失败。请先在 SkillPay 完成支付 (0.001 USDT)。"
        )]
    
    try:
        import time
        trader = FundingRateArbitrage()
        
        # 账户
        total, available = trader.get_account_balance()
        used = total - available
        used_pct = (used / total * 100) if total > 0 else 0
        
        # 持仓
        positions = trader.get_positions()
        
        # 资金费
        end_time = int(time.time() * 1000)
        start_time = end_time - (7 * 24 * 60 * 60 * 1000)
        data = trader._request('GET', '/fapi/v1/income', {
            'incomeType': 'FUNDING_FEE',
            'startTime': start_time,
            'endTime': end_time,
            'limit': 1000
        }, signed=True)
        total_income = sum(float(item.get('income', 0)) for item in data)
        total_unrealized = sum(p['unrealized_pnl'] for p in positions)
        
        report_lines = [
            "📊 币安资金费率套利监控报告",
            f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "【账户状态】",
            f"总权益: {total:.2f} USDT",
            f"已用保证金: {used:.2f} USDT ({used_pct:.1f}%)",
            f"可用余额: {available:.2f} USDT",
            "",
            "【盈亏统计】(近7天)",
            f"资金费收入: {total_income:+.4f} USDT",
            f"持仓浮动盈亏: {total_unrealized:+.4f} USDT",
            f"合计盈亏: {total_income + total_unrealized:+.4f} USDT",
            "",
            f"【当前持仓】({len(positions)} 个)"
        ]
        
        for p in positions:
            emoji = "🟢" if p['unrealized_pnl'] >= 0 else "🔴"
            report_lines.append(f"{p['symbol']}: {p['side']} 浮动:{emoji}{p['unrealized_pnl']:+.2f}")
        
        if not positions:
            report_lines.append("(无持仓)")
        
        report_lines.append("")
        report_lines.append("✅ 数据获取成功")
        
        return [TextContent(type="text", text="\n".join(report_lines))]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取报告失败: {e}")]


async def main():
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())