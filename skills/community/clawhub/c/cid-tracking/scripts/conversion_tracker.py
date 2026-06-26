#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
转化回传器 - 将订单数据回传到广告平台
支持：抖音巨量引擎、快手磁力引擎、腾讯广点通
"""

import json
import hashlib
import time
import requests
import argparse
from datetime import datetime
from typing import Dict, List


class ConversionTracker:
    """转化回传器基类"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.session = requests.Session()
    
    def track(self, cid: str, event_type: str, value: float, 
              order_id: str = None, timestamp: str = None) -> Dict:
        """回传转化数据"""
        raise NotImplementedError
    
    def hash_user_data(self, data: str, hash_type: str = 'sha256') -> str:
        """哈希用户数据 (用于隐私保护)"""
        if hash_type == 'sha256':
            return hashlib.sha256(data.encode()).hexdigest()
        elif hash_type == 'md5':
            return hashlib.md5(data.encode()).hexdigest()
        return data


class OceanEngineTracker(ConversionTracker):
    """抖音巨量引擎转化回传器"""
    
    BASE_URL = "https://ad.oceanengine.com/open_api/v2.0/promotion/conversion"
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.app_id = config.get('app_id', '')
        self.access_token = config.get('access_token', '')
        self.session.headers.update({
            'Access-Token': self.access_token,
            'Content-Type': 'application/json'
        })
    
    def track(self, cid: str, event_type: str, value: float,
              order_id: str = None, timestamp: str = None,
              user_id: str = None, phone: str = None) -> Dict:
        """
        回传巨量引擎转化
        
        Args:
            cid: Click ID
            event_type: 转化事件类型 (purchase, form_submit, etc.)
            value: 转化价值
            order_id: 订单 ID
            timestamp: 转化时间 (ISO 格式)
            user_id: 用户 ID (可选，哈希后传输)
            phone: 手机号 (可选，哈希后传输)
        """
        url = self.BASE_URL
        
        # 事件类型映射
        event_mapping = {
            'purchase': 'purchase',
            'order': 'purchase',
            'form_submit': 'form_submit',
            'phone_call': 'phone_call',
            'add_to_cart': 'add_to_cart'
        }
        
        payload = {
            'app_id': self.app_id,
            'event_type': event_mapping.get(event_type, event_type),
            'context': {
                'cid': cid,
                'convert_time': int(time.time()) if not timestamp else int(datetime.fromisoformat(timestamp).timestamp())
            },
            'properties': {
                'value': value,
                'order_id': order_id or cid
            }
        }
        
        # 添加用户数据 (哈希后)
        if user_id:
            payload['properties']['user_id'] = self.hash_user_data(user_id)
        if phone:
            payload['properties']['phone_num'] = self.hash_user_data(phone)
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get('code') == 0:
                return {
                    'success': True,
                    'message': '转化回传成功',
                    'platform': 'oceanengine',
                    'cid': cid,
                    'event_type': event_type,
                    'value': value
                }
            else:
                return {
                    'success': False,
                    'message': result.get('message', '回传失败'),
                    'platform': 'oceanengine',
                    'error_code': result.get('code')
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'platform': 'oceanengine'
            }


class KuaishouTracker(ConversionTracker):
    """快手磁力引擎转化回传器"""
    
    BASE_URL = "https://api.kuaishou.com/openapi/ad/convert"
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.app_id = config.get('app_id', '')
        self.access_token = config.get('access_token', '')
        self.session.headers.update({
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        })
    
    def track(self, cid: str, event_type: str, value: float,
              order_id: str = None, timestamp: str = None,
              user_id: str = None) -> Dict:
        """回传快手转化"""
        url = self.BASE_URL
        
        payload = {
            'cid': cid,
            'event_type': event_type,
            'convert_time': int(time.time() * 1000),
            'value': value
        }
        
        if order_id:
            payload['order_id'] = order_id
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get('result') == 1:
                return {
                    'success': True,
                    'message': '转化回传成功',
                    'platform': 'kuaishou',
                    'cid': cid
                }
            else:
                return {
                    'success': False,
                    'message': result.get('error_msg', '回传失败'),
                    'platform': 'kuaishou'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'platform': 'kuaishou'
            }


class TencentTracker(ConversionTracker):
    """腾讯广点通转化回传器"""
    
    BASE_URL = "https://e.qq.com/v1.0/conversion"
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.account_id = config.get('account_id', '')
        self.secret_id = config.get('secret_id', '')
        self.secret_key = config.get('secret_key', '')
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def track(self, cid: str, event_type: str, value: float,
              order_id: str = None, timestamp: str = None) -> Dict:
        """回传广点通转化"""
        # TODO: 实现腾讯签名算法
        print("⚠️  腾讯广点通需要实现签名算法")
        
        return {
            'success': False,
            'message': '腾讯广点通回传功能待实现',
            'platform': 'tencent'
        }


def get_tracker(platform: str, config: Dict) -> ConversionTracker:
    """获取对应平台的转化回传器"""
    trackers = {
        'oceanengine': OceanEngineTracker,
        'douyin': OceanEngineTracker,
        'kuaishou': KuaishouTracker,
        'ks': KuaishouTracker,
        'tencent': TencentTracker,
        'guangdiantong': TencentTracker
    }
    
    platform_lower = platform.lower()
    if platform_lower not in trackers:
        raise ValueError(f"不支持的平台：{platform}")
    
    return trackers[platform_lower](config)


def load_config(config_path: str = 'config.json') -> Dict:
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  配置文件不存在：{config_path}")
        return {}


def main():
    parser = argparse.ArgumentParser(description='转化回传器')
    parser.add_argument('--platform', '-p', required=True,
                        help='广告平台：oceanengine, kuaishou, tencent')
    parser.add_argument('--cid', '-c', required=True,
                        help='Click ID')
    parser.add_argument('--event', '-e', required=True,
                        help='转化事件：purchase, order, form_submit, etc.')
    parser.add_argument('--value', '-v', type=float, required=True,
                        help='转化价值 (订单金额)')
    parser.add_argument('--order-id', '-o', type=str,
                        help='订单 ID')
    parser.add_argument('--timestamp', '-t', type=str,
                        help='转化时间 (ISO 格式)')
    parser.add_argument('--config', '-C', type=str, default='config.json',
                        help='配置文件路径')
    parser.add_argument('--output', type=str,
                        help='输出结果文件 (JSON 格式)')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    platform_config = config.get(args.platform, {})
    
    if not platform_config:
        print(f"❌ 未配置 {args.platform} 平台凭证")
        return
    
    # 创建回传器
    tracker = get_tracker(args.platform, platform_config)
    
    # 回传转化
    print(f"📤 回传转化数据:")
    print(f"   平台：{args.platform}")
    print(f"   CID: {args.cid}")
    print(f"   事件：{args.event}")
    print(f"   价值：¥{args.value}")
    
    result = tracker.track(
        cid=args.cid,
        event_type=args.event,
        value=args.value,
        order_id=args.order_id,
        timestamp=args.timestamp
    )
    
    # 输出结果
    if result['success']:
        print(f"\n✅ {result['message']}")
    else:
        print(f"\n❌ {result['message']}")
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 保存结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n📁 结果已保存到：{args.output}")


if __name__ == '__main__':
    main()
