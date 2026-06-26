#!/usr/bin/env python3
"""快递监控 - 查询快递物流、绑定手机号自动获取快递"""

import requests
import re
import json
import os
import sys
from datetime import datetime

# 数据目录
DATA_DIR = os.path.expanduser("~/.openclaw/workspace/data/express")
os.makedirs(DATA_DIR, exist_ok=True)

PHONE_FILE = os.path.join(DATA_DIR, "phones.json")
EXPRESS_FILE = os.path.join(DATA_DIR, "express_history.json")

def load_phones():
    """加载绑定的手机号"""
    if os.path.exists(PHONE_FILE):
        with open(PHONE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_phones(phones):
    """保存手机号"""
    with open(PHONE_FILE, 'w') as f:
        json.dump(phones, f, ensure_ascii=False, indent=2)

def load_express_history():
    """加载快递历史"""
    if os.path.exists(EXPRESS_FILE):
        with open(EXPRESS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_express_history(history):
    """保存快递历史"""
    with open(EXPRESS_FILE, 'w') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def auto_detect_company(tracking_number):
    """自动识别快递公司"""
    url = 'https://m.kuaidi100.com/apicenter/kdquerytools.do?method=autoComNum'
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://m.kuaidi100.com/',
    }
    
    try:
        resp = requests.post(url, data={'text': tracking_number}, headers=headers, timeout=10)
        data = resp.json()
        
        if data.get('auto'):
            return data['auto'][0]['comCode'], data['auto'][0]['name']
        return None, None
    except Exception as e:
        return None, None

def get_express_info(tracking_number):
    """通过快递100免费API查询快递信息"""
    # 先自动识别快递公司
    company_code, company_name = auto_detect_company(tracking_number)
    
    if not company_code:
        # 尝试手动识别
        prefix = tracking_number[:2].upper()
        company_map = {
            'SF': ('shunfeng', '顺丰'),
            'YT': ('yuantong', '圆通'),
            'YTO': ('yuantong', '圆通'),
            'ZTO': ('zhongtong', '中通'),
            'STO': ('shentong', '申通'),
            'EMS': ('ems', 'EMS'),
            'JD': ('jd', '京东'),
            'SF': ('shunfeng', '顺丰')
        }
        for code, (c, n) in company_map.items():
            if tracking_number.upper().startswith(code):
                company_code = c
                company_name = n
                break
    
    if not company_code:
        company_code = 'yuantong'  # 默认圆通
        company_name = '圆通'
    
    # 查询快递信息
    url = 'https://m.kuaidi100.com/query'
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://m.kuaidi100.com/',
    }
    
    data = {
        'type': company_code,
        'postid': tracking_number
    }
    
    try:
        resp = requests.post(url, data=data, headers=headers, timeout=10)
        result = resp.json()
        
        if result.get('status') != '200':
            return None, result.get('message', '查询失败')
        
        # 解析状态
        state = result.get('state', '0')
        status_map = {
            '0': '在途',
            '1': '已揽收', 
            '2': '运输中',
            '3': '派送中',
            '4': '已签收',
            '5': '拒收',
            '6': '退件'
        }
        
        info = {
            'tracking_number': tracking_number,
            'company': company_name,
            'status': status_map.get(state, '未知'),
            'state': state,
            'traces': result.get('data', [])
        }
        
        # 保存到历史记录
        history = load_express_history()
        history[tracking_number] = {
            'company': company_name,
            'status': status_map.get(state, '未知'),
            'last_query': datetime.now().isoformat()
        }
        save_express_history(history)
        
        return info, None
        
    except Exception as e:
        return None, str(e)

def format_express_info(info):
    """格式化快递信息"""
    status = info.get('status', '未知')
    lines = [
        f"📦 快递: {info['tracking_number']}",
        f"🏢 快递公司: {info['company']}",
        f"📊 状态: {status}"
    ]
    
    traces = info.get('traces', [])
    if traces:
        latest = traces[0]
        lines.append(f"\n📍 最新:")
        lines.append(f"   {latest.get('ftime', '')}")
        lines.append(f"   {latest.get('context', '')}")
        
        if len(traces) > 1:
            lines.append(f"\n📜 物流轨迹:")
            for trace in traces[:5]:
                lines.append(f"  {trace.get('ftime', '')} - {trace.get('context', '')}")
    
    return "\n".join(lines)

def bind_phone(phone):
    """绑定手机号"""
    if not re.match(r'^1[3-9]\d{9}$', phone):
        return "❌ 手机号格式不正确"
    
    phones = load_phones()
    if phone in phones:
        return f"❌ 手机号 {phone} 已绑定"
    
    phones.append(phone)
    save_phones(phones)
    return f"✅ 已绑定手机号: {phone}\n可使用 '查看我的快递' 获取待收快递"

def main():
    if len(sys.argv) < 2:
        print("快递监控使用说明:")
        print("  python express_monitor.py query <单号>    查询快递")
        print("  python express_monitor.py bind <手机号>   绑定手机号")
        print("  python express_monitor.py list           查看快递列表")
        print("  python express_monitor.py check          检查新快递")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "query" and len(sys.argv) >= 3:
        tracking_number = sys.argv[2]
        info, error = get_express_info(tracking_number)
        if error:
            print(f"❌ 查询失败: {error}")
        else:
            print(format_express_info(info))
            
    elif cmd == "bind" and len(sys.argv) >= 3:
        phone = sys.argv[2]
        print(bind_phone(phone))
        
    elif cmd == "list":
        phones = load_phones()
        if phones:
            print(f"📱 绑定的手机号: {', '.join(phones)}")
        else:
            print("暂无绑定的手机号")
            
        history = load_express_history()
        if history:
            print(f"\n📦 历史快递: {len(history)}条")
            for tn, info in list(history.items())[-5:]:
                print(f"  {tn}: {info.get('status', '未知')}")
        else:
            print("暂无快递记录")
            
    elif cmd == "check":
        phones = load_phones()
        if not phones:
            print("请先绑定手机号: bind <手机号>")
            return
        print("检查新快递需要接入快递鸟API，当前仅支持单号查询")
        
    else:
        print("未知命令")

if __name__ == "__main__":
    main()
