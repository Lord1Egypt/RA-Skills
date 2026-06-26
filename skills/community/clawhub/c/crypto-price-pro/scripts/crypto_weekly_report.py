#!/usr/bin/env python3
"""
生成虚拟币周报并发送邮件
包含 7 天价格数据、趋势图、市场分析
"""

import sys
import os
import smtplib
import urllib.request
import urllib.error
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta

# 币种映射
COIN_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "BNB": "binancecoin",
    "SOL": "solana",
    "DOGE": "dogecoin"
}

# 默认配置
DEFAULT_COINS = ["BTC", "ETH", "BNB", "SOL", "DOGE"]
DAYS = 7

# 邮箱配置（从环境变量读取，避免硬编码敏感信息）
# 使用方法：
# export EMAIL_SENDER="your_email@126.com"
# export EMAIL_SENDER_NAME="Your Name"
# export EMAIL_PASSWORD="your_smtp_password"
# export EMAIL_RECIPIENT="recipient@example.com"
RECIPIENT = os.getenv('EMAIL_RECIPIENT')
SENDER_EMAIL = os.getenv('EMAIL_SENDER')
SENDER_NAME = os.getenv('EMAIL_SENDER_NAME', 'Crypto Report')
SMTP_PASSWORD = os.getenv('EMAIL_PASSWORD')  # 必须设置环境变量

def get_crypto_history(symbol, days=7):
    """获取历史价格数据"""
    symbol = symbol.upper()
    coin_id = COIN_MAP.get(symbol, symbol.lower())
    
    api_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = f"vs_currency=usd&days={days}&interval=daily"
    
    try:
        url = f"{api_url}?{params}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            prices = data.get("prices", [])
            
            result = []
            for timestamp_ms, price in prices:
                date = datetime.fromtimestamp(timestamp_ms / 1000).strftime("%m-%d")
                result.append((date, price))
            
            return result
            
    except Exception as e:
        return {"error": f"获取数据失败：{str(e)}"}

def get_current_price(symbol):
    """获取当前价格"""
    symbol = symbol.upper()
    coin_id = COIN_MAP.get(symbol, symbol.lower())
    
    api_url = "https://api.coingecko.com/api/v3/simple/price"
    params = f"ids={coin_id}&vs_currencies=usd,cny&include_24hr_change=true"
    
    try:
        url = f"{api_url}?{params}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if coin_id not in data:
                return None
            
            coin_data = data[coin_id]
            return {
                "symbol": symbol,
                "usd": coin_data.get("usd", 0),
                "cny": coin_data.get("cny", 0),
                "change_24h": coin_data.get("usd_24h_change", 0)
            }
    except Exception as e:
        return {"error": str(e)}

def generate_weekly_chart(symbols, days=7, output_path=None):
    """生成 7 天趋势图"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    except ImportError:
        return {"error": "未安装 matplotlib"}
    
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6']
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    all_data = {}
    valid_symbols = []
    
    for symbol in symbols:
        history = get_crypto_history(symbol, days)
        if not isinstance(history, dict) or "error" not in history:
            all_data[symbol] = history
            valid_symbols.append(symbol)
    
    if not valid_symbols:
        return {"error": "无有效数据"}
    
    # 上图：价格走势
    for i, symbol in enumerate(valid_symbols):
        history = all_data[symbol]
        dates = [h[0] for h in history]
        prices = [h[1] for h in history]
        color = colors[i % len(colors)]
        
        ax1.plot(dates, prices, marker='o', linewidth=2, markersize=6, 
                label=symbol, color=color)
    
    ax1.set_title(f'Crypto Weekly Report - {days} Days Price Trend', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Price (USD)', fontsize=12)
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # 下图：涨跌幅对比
    for i, symbol in enumerate(valid_symbols):
        history = all_data[symbol]
        dates = [h[0] for h in history]
        prices = [h[1] for h in history]
        color = colors[i % len(colors)]
        
        start_price = prices[0]
        normalized = [(p / start_price - 1) * 100 for p in prices]
        
        ax2.plot(dates, normalized, marker='s', linewidth=2, markersize=6, 
                label=symbol, color=color)
    
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax2.set_title('Relative Change (%) from Start of Period', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Change (%)', fontsize=12)
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    
    # 添加总结表格
    summary_text = "7-Day Performance Summary:\n"
    for i, symbol in enumerate(valid_symbols):
        history = all_data[symbol]
        start = history[0][1]
        end = history[-1][1]
        change = (end / start - 1) * 100
        summary_text += f"{symbol}: {change:+.2f}%\n"
    
    fig.text(0.02, 0.02, summary_text, fontsize=10, 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    if output_path is None:
        date_str = datetime.now().strftime("%Y%m%d")
        output_path = f"/Users/admin/.openclaw/workspace/crypto_weekly_{date_str}.png"
    
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output_path

def generate_email_content(coins_data):
    """生成邮件内容"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 生成 HTML 报告
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h1 {{ color: #2c3e50; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #3498db; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .positive {{ color: #27ae60; font-weight: bold; }}
            .negative {{ color: #e74c3c; font-weight: bold; }}
            .summary {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <h1>📊 虚拟币周报 - {today}</h1>
        
        <div class="summary">
            <h2>📈 7 天市场总结</h2>
            <p>本报告涵盖过去 7 天的主流虚拟币价格走势和市场表现。</p>
        </div>
        
        <h2>💰 当前价格</h2>
        <table>
            <tr>
                <th>币种</th>
                <th>美元价格</th>
                <th>人民币价格</th>
                <th>24h 涨跌</th>
            </tr>
    """
    
    for symbol, data in coins_data.items():
        if "error" not in data:
            change_class = "positive" if data['change_24h'] >= 0 else "negative"
            change_emoji = "📈" if data['change_24h'] >= 0 else "📉"
            html += f"""
            <tr>
                <td><strong>{symbol}</strong></td>
                <td>${data['usd']:,.2f}</td>
                <td>¥{data['cny']:,.2f}</td>
                <td class="{change_class}">{change_emoji} {data['change_24h']:+.2f}%</td>
            </tr>
            """
    
    html += """
        </table>
        
        <h2>📊 7 天趋势图</h2>
        <p>趋势图已作为附件发送，包含价格走势和相对涨跌幅对比。</p>
        
        <div class="summary">
            <h3>🔍 市场分析</h3>
            <ul>
                <li>数据来源：CoinGecko API</li>
                <li>报告生成时间：""" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</li>
                <li>下次报告：明天上午 10:00</li>
            </ul>
        </div>
        
        <hr>
        <p style="color: #7f8c8d; font-size: 12px;">
            此邮件由 OpenClaw Crypto Price Skill 自动生成<br>
            如需退订或修改配置，请联系管理员
        </p>
    </body>
    </html>
    """
    
    return html

def send_email(recipient, subject, html_content, attachment_path=None):
    """发送邮件"""
    # 邮箱配置（从环境变量读取）
    sender = SENDER_EMAIL
    sender_name = SENDER_NAME
    password = SMTP_PASSWORD
    smtp_server = 'smtp.126.com'
    smtp_port = 465
    
    if not password:
        return {"error": "未设置邮箱密码，请设置环境变量：export EMAIL_PASSWORD='your_password'"}
    
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = f"{sender_name} <{sender}>"
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # 添加 HTML 内容
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # 添加附件
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 
                              f'attachment; filename="{os.path.basename(attachment_path)}"')
                msg.attach(part)
        
        # 发送邮件
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        
        return {"success": True, "message": "邮件发送成功"}
        
    except Exception as e:
        return {"error": f"发送失败：{str(e)}"}

def main():
    print("🚀 开始生成虚拟币周报...")
    print(f"{'='*50}")
    
    # 检查环境变量
    if not SENDER_EMAIL or not SMTP_PASSWORD or not RECIPIENT:
        print("❌ 错误：缺少必要的环境变量")
        print("\n请设置以下环境变量：")
        print("  export EMAIL_SENDER=\"your_email@126.com\"")
        print("  export EMAIL_PASSWORD=\"your_smtp_password\"")
        print("  export EMAIL_RECIPIENT=\"recipient@example.com\"")
        print("\n或复制 .env.example 为 .env 并填写配置")
        sys.exit(1)
    
    # 1. 获取所有币种数据
    print("📊 获取价格数据...")
    coins_data = {}
    for symbol in DEFAULT_COINS:
        data = get_current_price(symbol)
        if data and "error" not in data and "usd" in data:
            coins_data[symbol] = data
            print(f"  ✓ {symbol}: ${data['usd']:,.2f}")
        else:
            print(f"  ✗ {symbol}: 获取失败")
    
    # 2. 生成趋势图
    print("\n📈 生成 7 天趋势图...")
    date_str = datetime.now().strftime("%Y%m%d")
    chart_path = f"/Users/admin/.openclaw/workspace/crypto_weekly_{date_str}.png"
    
    chart_result = generate_weekly_chart(DEFAULT_COINS, DAYS, chart_path)
    
    if isinstance(chart_result, dict) and "error" in chart_result:
        print(f"❌ 图表生成失败：{chart_result['error']}")
        chart_path = None
    else:
        print(f"✅ 图表已保存：{chart_path}")
    
    # 3. 生成邮件内容
    print("\n📧 生成邮件内容...")
    today = datetime.now().strftime("%Y-%m-%d")
    subject = f"📊 虚拟币周报 - {today}"
    html_content = generate_email_content(coins_data)
    
    # 4. 发送邮件
    print(f"\n📤 发送邮件到 {RECIPIENT}...")
    result = send_email(RECIPIENT, subject, html_content, chart_path)
    
    if "success" in result:
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['error']}")
        sys.exit(1)
    
    print(f"\n{'='*50}")
    print("✅ 周报生成完成！")

if __name__ == "__main__":
    main()
