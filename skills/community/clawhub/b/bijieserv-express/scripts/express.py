#!/usr/bin/env python3
"""
必捷免费快递查询 SKILL
功能：免费实时查询快递物流轨迹，支持2000+快递公司
"""

import os
import re
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class BJExpress:
    """必捷免费快递查询器"""
    
    # API 地址
    API_URL = "https://www.bijieserv.com/api/method/express_app.open.v1.query.exec"
    
    # 快递公司编码映射（常用）
    EXPRESS_COMPANIES = {
        'yuantong': '圆通速递',
        'zhongtong': '中通快递',
        'shunfeng': '顺丰速运',
        'yunda': '韵达快递',
        'shentong': '申通快递',
        'jd': '京东物流',
        'jtexpress': '极兔速递',
        'ems': 'EMS',
        'debangkuaidi': '德邦快递',
        'danniao': '菜鸟速递',
        'youzhengguonei': '邮政快递包裹',
        'dhl': 'DHL',
        'fedex': 'FedEx',
        'ups': 'UPS',
        'tnt': 'TNT'
    }
    
    # 物流状态映射
    STATE_MAP = {
        '0': ('在途', '快件在运输途中'),
        '1': ('已揽收', '快递公司已揽收'),
        '2': ('疑难', '快件存在异常情况'),
        '3': ('已签收', '快件已签收'),
        '4': ('退签', '快件已退签'),
        '5': ('派送中', '快件正在派件中'),
        '6': ('退回', '快件正在返回发货人途中'),
        '7': ('转投', '快件转给其他快递公司'),
        '8': ('清关', '快件正在清关'),
        '10': ('待清关', '快件等待清关'),
        '11': ('清关中', '快件正在清关流程中'),
        '12': ('已清关', '快件已完成清关'),
        '13': ('清关异常', '清关过程中出现异常'),
        '14': ('拒签', '收件人拒绝签收')
    }
    
    # 默认请求头（必需）
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.bijieserv.com',
        'Referer': 'https://www.bijieserv.com/',
        'Connection': 'keep-alive',
    }
    
    def __init__(self):
        """初始化"""
        self.query_history = {}  # 查询历史，用于锁单检测
    
    def validate_tracking_number(self, num: str) -> bool:
        """验证快递单号格式"""
        if not num:
            return False
        return 6 <= len(num) <= 32
    
    def validate_phone(self, phone: str) -> bool:
        """验证手机号格式"""
        if not phone:
            return True  # 选填，不验证
        return bool(re.match(r'^1[3-9]\d{9}$', phone))
    
    def check_lockout(self, num: str) -> Tuple[bool, str]:
        """
        检查是否可能锁单
        
        Returns:
            (是否安全, 提示信息)
        """
        if num in self.query_history:
            last_query = self.query_history[num]
            elapsed = (datetime.now() - last_query).total_seconds()
            if elapsed < 1800:  # 30分钟
                remaining = 1800 - elapsed
                return False, f"⚠️ 该单号 {int(remaining/60)} 分钟前已查询过，频繁查询可能导致锁单。建议 {int(remaining/60)} 分钟后再查。"
        return True, ""
    
    def map_company_code(self, company_name: str) -> str:
        """
        映射快递公司名称到编码
        
        Args:
            company_name: 快递公司名称（如"圆通"、"顺丰"）
        
        Returns:
            快递公司编码
        """
        company_name = company_name.lower().strip()
        
        # 直接匹配
        if company_name in self.EXPRESS_COMPANIES:
            return company_name
        
        # 模糊匹配
        mapping = {
            '圆通': 'yuantong', 'yt': 'yuantong',
            '中通': 'zhongtong', 'zt': 'zhongtong',
            '顺丰': 'shunfeng', 'sf': 'shunfeng',
            '韵达': 'yunda', 'yd': 'yunda',
            '申通': 'shentong', 'st': 'shentong',
            '京东': 'jd', 'jd': 'jd',
            '极兔': 'jtexpress', 'jt': 'jtexpress',
            'ems': 'ems', '邮政': 'youzhengguonei',
            '德邦': 'debangkuaidi', 'db': 'debangkuaidi',
            '菜鸟': 'danniao',
            'dhl': 'dhl',
            'fedex': 'fedex', '联邦': 'fedex',
            'ups': 'ups',
            'tnt': 'tnt'
        }
        
        return mapping.get(company_name, company_name)
    
    def get_company_name(self, code: str) -> str:
        """获取快递公司名称"""
        return self.EXPRESS_COMPANIES.get(code, code)
    
    def desensitize_text(self, text: str) -> str:
        """
        脱敏处理：隐藏手机号中间4位
        
        Args:
            text: 原始文本
        
        Returns:
            脱敏后的文本
        """
        if not text:
            return text
        
        # 匹配手机号 (11位数字)
        phone_pattern = r'(1[3-9]\d)(\d{4})(\d{4})'
        text = re.sub(phone_pattern, r'\1****\3', text)
        
        # 匹配固话 (区号-号码)
        tel_pattern = r'(\d{3,4}-)(\d{3})(\d{4})'
        text = re.sub(tel_pattern, r'\1\2****', text)
        
        return text
    
    def query(self, num: str, com: str, phone: str = '', 
              from_addr: str = '', to_addr: str = '',
              resultv2: str = '4') -> Tuple[bool, Dict or str]:
        """
        查询快递物流信息
        
        Args:
            num: 快递单号
            com: 快递公司编码
            phone: 手机号（顺丰/中通必填，但API要求参数存在）
            from_addr: 出发地（参数可为空）
            to_addr: 目的地（参数可为空）
            resultv2: 功能扩展标识 0/1/4/8
        
        Returns:
            (成功状态, 结果数据或错误信息)
        """
        # 参数校验
        if not self.validate_tracking_number(num):
            return False, "❌ 快递单号格式不正确（应为6-32位字符）"
        
        if not com:
            return False, "❌ 请选择快递公司"
        
        # 锁单检测
        safe, warning = self.check_lockout(num)
        if not safe:
            return False, warning
        
        # 构建请求参数（所有参数都要有，值可以为空）
        payload = {
            'com': com,
            'num': num,
            'phone': phone or '',  # 可为空
            '_from': from_addr or '',  # 可为空
            'to': to_addr or '',  # 可为空
            'show': '0',
            'order': 'desc',
            'lang': 'zh',
            'resultv2': resultv2,
            'needCourierInfo': 'true'
        }
        
        try:
            response = requests.post(
                self.API_URL,
                data=payload,
                headers=self.DEFAULT_HEADERS,
                timeout=15
            )
            
            # 记录查询时间
            self.query_history[num] = datetime.now()
            
            if response.status_code == 200:
                result = response.json()
                msg_obj = result.get('message', {})
                
                if not msg_obj.get('success'):
                    code = msg_obj.get('code', -1)
                    msg_text = msg_obj.get('message', '未知错误')
                    
                    if "频繁" in msg_text:
                        retry_time = msg_obj.get('retry_after', 600)
                        return False, f"⚠️ 查询过于频繁，请 {retry_time//60} 分钟后再试。"
                    elif "锁单" in msg_text:
                        return False, "⚠️ 该单号被锁定，请至少等待 30 分钟后再次查询。"
                    elif "格式不正确" in msg_text:
                        return False, "❌ 快递单号格式不正确（应为6-32位字符）。"
                    else:
                        return False, f"❌ 查询失败：{msg_text}"
                
                data = msg_obj.get('data', {})
                if not data or data.get('status') != '200':
                    return False, "❌ 未查询到物流信息，请确认单号是否正确或包裹是否已发货。"
                
                return True, data
            else:
                return False, f"❌ HTTP 错误: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "❌ 请求超时，请稍后重试"
        except requests.exceptions.RequestException as e:
            return False, f"❌ 请求异常: {str(e)}"
    
    def format_result(self, data: Dict) -> str:
        """
        格式化查询结果为 Markdown
        
        Args:
            data: API返回的数据
        
        Returns:
            Markdown格式字符串
        """
        if not data:
            return "❌ 未获取到物流信息"
        
        nu = data.get('nu', '')
        com_code = data.get('com', '')
        state = data.get('state', '0')
        ischeck = data.get('ischeck', '0')
        tracks = data.get('data', [])
        
        # 获取状态信息
        state_info = self.STATE_MAP.get(state, ('未知', '未知状态'))
        
        lines = []
        lines.append("="*60)
        lines.append("📦 物流追踪结果")
        lines.append("="*60)
        lines.append(f"快递单号: {nu}")
        lines.append(f"快递公司: {self.get_company_name(com_code)}")
        lines.append(f"当前状态: {state_info[0]}")
        lines.append(f"是否签收: {'✅ 已签收' if ischeck == '1' else '❌ 未签收'}")
        
        # 时效预测
        if 'arrivalTime' in data:
            arrival = data['arrivalTime']
            lines.append(f"预计到达: {arrival.get('arrivalTime', '-')}")
        
        lines.append("")
        lines.append(f"🕐 最新物流轨迹 (共{len(tracks)}条)")
        lines.append("-"*60)
        
        # 物流轨迹
        if tracks:
            for i, track in enumerate(tracks[:10], 1):  # 最多显示10条
                time_str = track.get('ftime', track.get('time', ''))
                context = self.desensitize_text(track.get('context', ''))
                status = track.get('status', '')
                location = track.get('location', '')
                
                lines.append(f"\n{i}. [{time_str}] {status}")
                lines.append(f"   {context}")
                if location:
                    lines.append(f"   📍 {location}")
        
        lines.append("")
        lines.append("="*60)
        
        return "\n".join(lines)

# 便捷函数
def quick_query(company: str, num: str, phone: str = '', 
                from_addr: str = '', to_addr: str = '',
                resultv2: str = '4') -> str:
    """
    快速查询快递
    
    Args:
        company: 快递公司名称或编码
        num: 快递单号
        phone: 手机号（可选）
        from_addr: 出发地（可选）
        to_addr: 目的地（可选）
        resultv2: 功能扩展标识
    
    Returns:
        格式化后的查询结果
    """
    express = BJExpress()
    
    # 映射快递公司编码
    com_code = express.map_company_code(company)
    
    success, result = express.query(
        num=num,
        com=com_code,
        phone=phone,
        from_addr=from_addr,
        to_addr=to_addr,
        resultv2=resultv2
    )
    
    if success:
        return express.format_result(result)
    else:
        return result

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='必捷免费快递查询')
    parser.add_argument('company', help='快递公司（如：圆通、顺丰）')
    parser.add_argument('num', help='快递单号')
    parser.add_argument('--phone', default='', help='手机号（可选）')
    parser.add_argument('--from', dest='from_addr', default='', help='出发地（可选）')
    parser.add_argument('--to', dest='to_addr', default='', help='目的地（可选）')
    parser.add_argument('--resultv2', default='4', choices=['0', '1', '4', '8'], 
                        help='功能扩展：0=基础, 1=行政解析, 4=高级状态, 8=时效预测')
    
    args = parser.parse_args()
    
    result = quick_query(
        company=args.company,
        num=args.num,
        phone=args.phone,
        from_addr=args.from_addr,
        to_addr=args.to_addr,
        resultv2=args.resultv2
    )
    
    print(result)
