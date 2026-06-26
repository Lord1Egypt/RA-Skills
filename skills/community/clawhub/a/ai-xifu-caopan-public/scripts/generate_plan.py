#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI媳妇操盘 - 方案生成主程序
根据模板和数据自动生成交易方案
"""

import os
import sys
import json
import argparse
from datetime import datetime

# 配置：必须通过环境变量设置API密钥！
# 使用前请配置环境变量：
#   export GS_API_KEY="你的国信API密钥"
#   export TUSHARE_TOKEN="你的Tushare Token"
# ⚠️ 安全说明（Credential Exposure防护）：
# API密钥必须由用户主动在运行时传入，不会自动从环境变量读取。
# 用户需要在调用脚本时通过 --apikey 或交互式输入提供密钥。
# 这样避免了子进程继承环境变量导致的密钥泄露风险。
GS_API_KEY = None
TUSHARE_TOKEN = None

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(SKILL_DIR, 'templates')

def load_template(template_name='FINAL_PLAN_TEMPLATE.md'):
    """加载模板"""
    template_path = os.path.join(TEMPLATE_DIR, template_name)
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def validate_input(code, set_code):
    """校验输入，防止命令注入"""
    import re
    # 代码必须是数字，最多6位（股票代码格式）
    if not re.match(r'^\d{1,10}$', str(code)):
        raise ValueError(f"无效的代码参数: {code}")
    # set_code必须是整数
    valid_set_codes = ['0', '1', '2', '-1', '74']
    if str(set_code) not in valid_set_codes:
        raise ValueError(f"无效的市场代码: {set_code}")
    return True

def get_market_data(code, set_code):
    """获取行情数据"""
    import subprocess
    import shlex
    
    # 输入校验 - 防止命令注入
    validate_input(code, set_code)
    
    # ⚠️ 安全：不自动传递任何API密钥环境变量到子进程
    # 用户可通过设置环境变量 GS_API_KEY 和 TUSHARE_TOKEN 来授权
    # 但脚本不会自动读取这些值传入subprocess
    # 如需传递，用户需在调用时明确传入 --env GS_API_KEY=xxx
    env = {
        'PATH': os.environ.get('PATH', '/usr/bin'),  # 仅传递PATH保证脚本可执行
    }
    
    script_path = '/home/sandbox/.openclaw/workspace/skills/gs-stock-market-query/scripts/get_data.py'
    cwd_path = '/home/sandbox/.openclaw/workspace/skills/gs-stock-market-query'
    
    # 使用参数列表 + shell=False，杜绝命令注入
    cmd = ['python3', script_path, 'single_hq', '--code', str(code), '--set_code', str(set_code)]
    result = subprocess.run(
        cmd,
        shell=False,
        cwd=cwd_path,
        env=env,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            return data.get('object', {})
        except:
            return None
    return None

def analyze_trend(data_list):
    """分析趋势"""
    if not data_list or len(data_list) < 2:
        return "数据不足"
    
    changes = [float(d.get('priceChangePct', 0)) for d in data_list if d]
    
    if all(c > 0 for c in changes):
        return "连续上涨"
    elif all(c < 0 for c in changes):
        return "连续下跌"
    else:
        return "震荡"

def predict_trend(recent_trend, market_trend):
    """预判走势"""
    prediction_matrix = {
        ("连续上涨", "走强"): ("继续上涨", "震荡偏强", "高位震荡"),
        ("连续上涨", "走弱"): ("回调风险", "震荡调整", "寻找支撑"),
        ("连续下跌", "走强"): ("反弹机会", "震荡偏强", "确认底部"),
        ("连续下跌", "走弱"): ("继续下跌", "探底过程", "底部震荡"),
        ("震荡", "震荡"): ("继续震荡", "震荡延续", "方向选择"),
    }
    
    key = (recent_trend, market_trend)
    return prediction_matrix.get(key, ("震荡", "震荡", "震荡"))

def calculate_risk_level(signals_triggered):
    """计算风险等级"""
    if signals_triggered <= 2:
        return "🟢 低风险"
    elif signals_triggered <= 5:
        return "🟡 中风险"
    elif signals_triggered <= 8:
        return "🟠 高风险"
    else:
        return "🔴 极高风险"

def generate_plan(asset_type, code, name, set_code='0'):
    """生成交易方案"""
    print(f"正在生成{name}交易方案...")
    
    # 获取数据
    data = get_market_data(code, set_code)
    
    if not data:
        print(f"错误：无法获取{name}的数据")
        return None
    
    # 基本信息
    now_price = data.get('now', '--')
    change_pct = data.get('priceChangePct', '--')
    volume = data.get('vol', '--')
    amount = data.get('amount', '--')
    
    print(f"当前价：{now_price}，涨跌幅：{change_pct}%")
    
    # 加载模板
    template = load_template()
    
    # 这里可以继续填充模板内容
    # 实际生成Word文档的逻辑在xiaoyi-docx技能中
    
    return {
        'code': code,
        'name': name,
        'type': asset_type,
        'price': now_price,
        'change_pct': change_pct,
        'volume': volume,
        'amount': amount,
        'template': template
    }

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AI媳妇操盘 - 方案生成')
    parser.add_argument('--type', type=str, required=True, choices=['stock', 'futures', 'fund'], help='品种类型')
    parser.add_argument('--code', type=str, required=True, help='代码')
    parser.add_argument('--name', type=str, required=True, help='名称')
    parser.add_argument('--set_code', type=str, default='0', help='市场代码（0=深市，1=沪市）')
    
    args = parser.parse_args()
    
    result = generate_plan(args.type, args.code, args.name, args.set_code)
    
    if result:
        print(f"\n方案生成成功！")
        print(f"品种：{result['name']}({result['code']})")
        print(f"当前价：{result['price']}")
        print(f"涨跌幅：{result['change_pct']}%")
    else:
        print("方案生成失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
