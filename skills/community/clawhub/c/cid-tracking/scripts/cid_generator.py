#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CID 生成器 - 为各广告平台生成 Click ID 追踪链接
支持：抖音巨量引擎、快手磁力引擎、腾讯广点通
"""

import uuid
import hashlib
import time
import json
import argparse
from datetime import datetime
from urllib.parse import urlencode, quote


class CIDGenerator:
    """CID 生成器基类"""
    
    def __init__(self, config=None):
        self.config = config or {}
    
    def generate_cid(self, campaign_id=None, ad_id=None, user_id=None):
        """生成唯一 Click ID"""
        timestamp = str(int(time.time() * 1000))
        unique_id = str(uuid.uuid4()).replace('-', '')
        cid = f"{timestamp}{unique_id[:16]}"
        
        if campaign_id:
            cid = f"{cid}_c{campaign_id}"
        if ad_id:
            cid = f"{cid}_a{ad_id}"
            
        return cid.upper()
    
    def generate_tracking_url(self, landing_url, cid, extra_params=None):
        """生成带 CID 的追踪链接"""
        params = {
            'cid': cid,
            'ts': int(time.time())
        }
        
        if extra_params:
            params.update(extra_params)
        
        separator = '&' if '?' in landing_url else '?'
        return f"{landing_url}{separator}{urlencode(params)}"


class OceanEngineGenerator(CIDGenerator):
    """抖音巨量引擎 CID 生成器"""
    
    PLATFORM_NAME = "oceanengine"
    
    def generate_cid(self, campaign_id=None, ad_id=None, user_id=None):
        """巨量引擎 CID 格式：时间戳 + 随机字符串 (32 位)"""
        base_cid = super().generate_cid(campaign_id, ad_id, user_id)
        # 确保 32 位
        if len(base_cid) < 32:
            base_cid = base_cid + hashlib.md5(base_cid.encode()).hexdigest()[:32-len(base_cid)]
        return base_cid[:32].upper()
    
    def generate_tracking_url(self, landing_url, cid, extra_params=None):
        """巨量引擎追踪链接格式"""
        params = {
            'cid': cid,
            'sessionid': '',  # 可选
            'ts': int(time.time())
        }
        
        if extra_params:
            params.update(extra_params)
        
        # 巨量引擎特殊参数
        params['imei'] = ''  # 可选，设备标识
        params['os'] = ''    # 可选，操作系统
        
        separator = '&' if '?' in landing_url else '?'
        return f"{landing_url}{separator}{urlencode(params)}"


class KuaishouGenerator(CIDGenerator):
    """快手磁力引擎 CID 生成器"""
    
    PLATFORM_NAME = "kuaishou"
    
    def generate_cid(self, campaign_id=None, ad_id=None, user_id=None):
        """快手 CID 格式：UUID 格式"""
        base_cid = super().generate_cid(campaign_id, ad_id, user_id)
        # 转换为 UUID 格式
        if len(base_cid) >= 32:
            return f"{base_cid[:8]}-{base_cid[8:12]}-{base_cid[12:16]}-{base_cid[16:20]}-{base_cid[20:32]}".upper()
        return base_cid.upper()
    
    def generate_tracking_url(self, landing_url, cid, extra_params=None):
        """快手追踪链接格式"""
        params = {
            'cid': cid,
            'timestamp': int(time.time() * 1000)
        }
        
        if extra_params:
            params.update(extra_params)
        
        separator = '&' if '?' in landing_url else '?'
        return f"{landing_url}{separator}{urlencode(params)}"


class TencentGenerator(CIDGenerator):
    """腾讯广点通 CID 生成器"""
    
    PLATFORM_NAME = "tencent"
    
    def generate_cid(self, campaign_id=None, ad_id=None, user_id=None):
        """广点通 CID 格式：MD5 哈希"""
        base_cid = super().generate_cid(campaign_id, ad_id, user_id)
        # 使用 MD5 生成 32 位哈希
        return hashlib.md5(base_cid.encode()).hexdigest().upper()
    
    def generate_tracking_url(self, landing_url, cid, extra_params=None):
        """广点通追踪链接格式"""
        params = {
            'cid': cid,
            'ts': int(time.time()),
            'r': ''  # 可选，回传标识
        }
        
        if extra_params:
            params.update(extra_params)
        
        separator = '&' if '?' in landing_url else '?'
        return f"{landing_url}{separator}{urlencode(params)}"


def get_generator(platform, config=None):
    """获取对应平台的 CID 生成器"""
    generators = {
        'oceanengine': OceanEngineGenerator,
        'douyin': OceanEngineGenerator,
        'kuaishou': KuaishouGenerator,
        'ks': KuaishouGenerator,
        'tencent': TencentGenerator,
        'guangdiantong': TencentGenerator,
        'qq': TencentGenerator
    }
    
    platform_lower = platform.lower()
    if platform_lower not in generators:
        raise ValueError(f"不支持的平台：{platform}. 支持的平台：{list(generators.keys())}")
    
    return generators[platform_lower](config)


def main():
    parser = argparse.ArgumentParser(description='CID 追踪链接生成器')
    parser.add_argument('--platform', '-p', required=True, 
                        help='广告平台：oceanengine, kuaishou, tencent')
    parser.add_argument('--campaign-id', '-c', type=str,
                        help='广告计划 ID')
    parser.add_argument('--ad-id', '-a', type=str,
                        help='广告创意 ID')
    parser.add_argument('--landing-url', '-u', type=str, required=True,
                        help='落地页 URL')
    parser.add_argument('--count', '-n', type=int, default=1,
                        help='生成数量 (默认 1)')
    parser.add_argument('--output', '-o', type=str,
                        help='输出文件路径 (JSON 格式)')
    
    args = parser.parse_args()
    
    # 创建生成器
    generator = get_generator(args.platform)
    
    # 生成 CID
    results = []
    for i in range(args.count):
        cid = generator.generate_cid(
            campaign_id=args.campaign_id,
            ad_id=args.ad_id
        )
        
        tracking_url = generator.generate_tracking_url(
            landing_url=args.landing_url,
            cid=cid
        )
        
        results.append({
            'index': i + 1,
            'cid': cid,
            'tracking_url': tracking_url,
            'platform': args.platform,
            'campaign_id': args.campaign_id,
            'ad_id': args.ad_id,
            'landing_url': args.landing_url,
            'created_at': datetime.now().isoformat()
        })
        
        print(f"\n[#{i+1}] CID: {cid}")
        print(f"    追踪链接：{tracking_url}".encode('gbk', 'replace').decode('gbk'))
    
    # 输出到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n[OK] 已保存到：{args.output}")
    
    # 输出汇总
    print(f"\n{'='*60}")
    print(f"[OK] 成功生成 {len(results)} 个 CID 追踪链接")
    print(f"平台：{args.platform}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
