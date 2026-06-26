#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广告数据获取器 - 从各平台 API 获取广告数据
支持：抖音巨量引擎、快手磁力引擎、腾讯广点通
"""

import json
import requests
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class DataFetcher:
    """广告数据获取器基类"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.session = requests.Session()
    
    def fetch_campaign_data(self, start_date: str, end_date: str) -> List[Dict]:
        """获取广告计划数据"""
        raise NotImplementedError
    
    def fetch_ad_data(self, campaign_id: str, start_date: str, end_date: str) -> List[Dict]:
        """获取广告创意数据"""
        raise NotImplementedError
    
    def normalize_data(self, raw_data: List[Dict], platform: str) -> List[Dict]:
        """标准化数据格式"""
        normalized = []
        for item in raw_data:
            normalized.append({
                'platform': platform,
                'campaign_id': item.get('campaign_id', ''),
                'campaign_name': item.get('campaign_name', ''),
                'ad_id': item.get('ad_id', ''),
                'ad_name': item.get('ad_name', ''),
                'date': item.get('date', ''),
                'impression': int(item.get('impression', 0) or 0),
                'click': int(item.get('click', 0) or 0),
                'cost': float(item.get('cost', 0) or 0),
                'conversion': int(item.get('conversion', 0) or 0),
                'conversion_cost': float(item.get('conversion_cost', 0) or 0),
                'ctr': float(item.get('ctr', 0) or 0),
                'cvr': float(item.get('cvr', 0) or 0),
            })
        return normalized


class OceanEngineFetcher(DataFetcher):
    """抖音巨量引擎数据获取器"""
    
    BASE_URL = "https://ad.oceanengine.com/open_api/v1.3"
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.app_id = config.get('app_id', '')
        self.access_token = config.get('access_token', '')
        self.session.headers.update({
            'Access-Token': self.access_token
        })
    
    def fetch_campaign_data(self, start_date: str, end_date: str) -> List[Dict]:
        """获取巨量引擎广告计划数据"""
        url = f"{self.BASE_URL}/report/campaign/"
        
        params = {
            'app_id': self.app_id,
            'start_date': start_date.replace('-', ''),
            'end_date': end_date.replace('-', ''),
            'dimensions': ['campaign_id', 'campaign_name'],
            'metrics': ['impression', 'click', 'cost', 'convert']
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                return data.get('data', {}).get('list', [])
            else:
                print(f"API 错误：{data.get('message', 'Unknown error')}")
                return []
                
        except Exception as e:
            print(f"获取数据失败：{e}")
            return []
    
    def normalize_data(self, raw_data: List[Dict]) -> List[Dict]:
        """标准化巨量引擎数据"""
        normalized = []
        for item in raw_data:
            stats = item.get('statistics', {})
            normalized.append({
                'platform': 'oceanengine',
                'campaign_id': str(item.get('campaign_id', '')),
                'campaign_name': item.get('campaign_name', ''),
                'ad_id': '',
                'ad_name': '',
                'date': item.get('stat_time', ''),
                'impression': int(stats.get('impression', 0) or 0),
                'click': int(stats.get('click', 0) or 0),
                'cost': float(stats.get('cost', 0) or 0),
                'conversion': int(stats.get('convert', 0) or 0),
                'conversion_cost': float(stats.get('convert_cost', 0) or 0),
                'ctr': float(stats.get('ctr', 0) or 0),
                'cvr': float(stats.get('convert_rate', 0) or 0),
            })
        return normalized


class KuaishouFetcher(DataFetcher):
    """快手磁力引擎数据获取器"""
    
    BASE_URL = "https://api.kuaishou.com/openapi/ad"
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.app_id = config.get('app_id', '')
        self.access_token = config.get('access_token', '')
        self.session.headers.update({
            'Authorization': f'Bearer {self.access_token}'
        })
    
    def fetch_campaign_data(self, start_date: str, end_date: str) -> List[Dict]:
        """获取快手广告计划数据"""
        url = f"{self.BASE_URL}/report/campaign"
        
        payload = {
            'start_date': start_date,
            'end_date': end_date,
            'metrics': ['impression', 'click', 'cost', 'conversion'],
            'dimensions': ['campaign_id', 'campaign_name']
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get('result') == 1:
                return data.get('data', {}).get('list', [])
            else:
                print(f"API 错误：{data.get('error_msg', 'Unknown error')}")
                return []
                
        except Exception as e:
            print(f"获取数据失败：{e}")
            return []
    
    def normalize_data(self, raw_data: List[Dict]) -> List[Dict]:
        """标准化快手数据"""
        normalized = []
        for item in raw_data:
            normalized.append({
                'platform': 'kuaishou',
                'campaign_id': str(item.get('campaign_id', '')),
                'campaign_name': item.get('campaign_name', ''),
                'ad_id': '',
                'ad_name': '',
                'date': item.get('date', ''),
                'impression': int(item.get('impression', 0) or 0),
                'click': int(item.get('click', 0) or 0),
                'cost': float(item.get('cost', 0) or 0),
                'conversion': int(item.get('conversion', 0) or 0),
                'conversion_cost': float(item.get('conversion_cost', 0) or 0),
                'ctr': float(item.get('ctr', 0) or 0),
                'cvr': float(item.get('cvr', 0) or 0),
            })
        return normalized


class TencentFetcher(DataFetcher):
    """腾讯广点通数据获取器"""
    
    BASE_URL = "https://e.qq.com/v1.0"
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.account_id = config.get('account_id', '')
        self.secret_id = config.get('secret_id', '')
        self.secret_key = config.get('secret_key', '')
        # 实际使用需要实现腾讯签名算法
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def fetch_campaign_data(self, start_date: str, end_date: str) -> List[Dict]:
        """获取广点通广告计划数据"""
        url = f"{self.BASE_URL}/report"
        
        payload = {
            'account_id': self.account_id,
            'report_type': 'CAMPAIGN',
            'date_range': {
                'start_date': start_date,
                'end_date': end_date
            },
            'metrics': ['impression', 'click', 'cost', 'conversion'],
            'group_by': ['campaign_id', 'campaign_name']
        }
        
        # TODO: 实现腾讯签名
        print("⚠️  腾讯广点通需要实现签名算法，请参考官方文档")
        
        try:
            # 示例调用，实际需要签名
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                return data.get('data', {}).get('list', [])
            else:
                print(f"API 错误：{data.get('message', 'Unknown error')}")
                return []
                
        except Exception as e:
            print(f"获取数据失败：{e}")
            return []
    
    def normalize_data(self, raw_data: List[Dict]) -> List[Dict]:
        """标准化广点通数据"""
        normalized = []
        for item in raw_data:
            normalized.append({
                'platform': 'tencent',
                'campaign_id': str(item.get('campaign_id', '')),
                'campaign_name': item.get('campaign_name', ''),
                'ad_id': '',
                'ad_name': '',
                'date': item.get('date', ''),
                'impression': int(item.get('impression', 0) or 0),
                'click': int(item.get('click', 0) or 0),
                'cost': float(item.get('cost', 0) or 0),
                'conversion': int(item.get('conversion', 0) or 0),
                'conversion_cost': float(item.get('conversion_cost', 0) or 0),
                'ctr': float(item.get('ctr', 0) or 0),
                'cvr': float(item.get('cvr', 0) or 0),
            })
        return normalized


def get_fetcher(platform: str, config: Dict) -> DataFetcher:
    """获取对应平台的数据获取器"""
    fetchers = {
        'oceanengine': OceanEngineFetcher,
        'douyin': OceanEngineFetcher,
        'kuaishou': KuaishouFetcher,
        'ks': KuaishouFetcher,
        'tencent': TencentFetcher,
        'guangdiantong': TencentFetcher,
        'qq': TencentFetcher
    }
    
    platform_lower = platform.lower()
    if platform_lower not in fetchers:
        raise ValueError(f"不支持的平台：{platform}")
    
    return fetchers[platform_lower](config)


def load_config(config_path: str = 'config.json') -> Dict:
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  配置文件不存在：{config_path}")
        print("   请复制 config.example.json 为 config.json 并填写凭证")
        return {}


def main():
    parser = argparse.ArgumentParser(description='广告数据获取器')
    parser.add_argument('--platform', '-p', type=str, default='all',
                        help='广告平台：all, oceanengine, kuaishou, tencent')
    parser.add_argument('--start-date', '-s', type=str,
                        help='开始日期 (YYYY-MM-DD), 默认昨天')
    parser.add_argument('--end-date', '-e', type=str,
                        help='结束日期 (YYYY-MM-DD), 默认昨天')
    parser.add_argument('--config', '-c', type=str, default='config.json',
                        help='配置文件路径')
    parser.add_argument('--output', '-o', type=str,
                        help='输出文件路径 (JSON 格式)')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    # 确定日期范围
    if not args.start_date:
        yesterday = datetime.now() - timedelta(days=1)
        args.start_date = yesterday.strftime('%Y-%m-%d')
        args.end_date = args.start_date
    
    # 确定平台列表
    if args.platform == 'all':
        platforms = ['oceanengine', 'kuaishou', 'tencent']
    else:
        platforms = [args.platform]
    
    # 获取数据
    all_data = []
    for platform in platforms:
        print(f"\n📊 正在获取 {platform} 数据...")
        
        platform_config = config.get(platform, {})
        if not platform_config:
            print(f"  ⚠️  跳过 {platform} (未配置)")
            continue
        
        fetcher = get_fetcher(platform, platform_config)
        raw_data = fetcher.fetch_campaign_data(args.start_date, args.end_date)
        normalized = fetcher.normalize_data(raw_data)
        
        print(f"  ✅ 获取 {len(normalized)} 条记录")
        all_data.extend(normalized)
    
    # 输出结果
    print(f"\n{'='*60}")
    print(f"[OK] 共获取 {len(all_data)} 条广告数据")
    print(f"日期范围：{args.start_date} ~ {args.end_date}")
    print(f"{'='*60}")
    
    # 保存到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        print(f"\n📁 已保存到：{args.output}")
    
    # 打印摘要
    if all_data:
        total_cost = sum(item['cost'] for item in all_data)
        total_conversion = sum(item['conversion'] for item in all_data)
        total_impression = sum(item['impression'] for item in all_data)
        total_click = sum(item['click'] for item in all_data)
        
        print(f"\n📈 数据摘要:")
        print(f"   总消耗：¥{total_cost:.2f}")
        print(f"   总转化：{total_conversion}")
        print(f"   总展示：{total_impression:,}")
        print(f"   总点击：{total_click:,}")
        
        if total_click > 0:
            ctr = total_click / total_impression * 100
            print(f"   CTR: {ctr:.2f}%")
        
        if total_conversion > 0:
            cpa = total_cost / total_conversion
            print(f"   CPA: ¥{cpa:.2f}")


if __name__ == '__main__':
    main()
