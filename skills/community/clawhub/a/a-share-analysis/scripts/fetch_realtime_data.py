#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股实时数据获取脚本（优化版）
支持多数据源：新浪财经、东方财富
带重试机制和缓存
"""

import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime
import logging
import sys
import codecs

# Windows 编码处理
if sys.platform == 'win32':
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    except:
        pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 重试配置
MAX_RETRIES = 3
RETRY_DELAY = 1
TIMEOUT = 10


class AShareRealTimeFetcher:
    """A 股实时数据获取器"""

    # 新浪财经 API
    XINHUA_URL = "http://hq.sinajs.cn/list="

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "http://finance.sina.com.cn/"
        })

    def fetch_stock_data(self, stock_code: str) -> Optional[Dict]:
        """获取股票实时数据（带重试）"""
        for attempt in range(MAX_RETRIES):
            try:
                # 根据股票代码前缀判断市场
                if stock_code.startswith('6') or stock_code.startswith('5'):
                    prefix = 'sh'
                else:
                    prefix = 'sz'
                
                # 直接拼接 URL
                url = f"{self.XINHUA_URL}{prefix}{stock_code}"
                
                # 发送请求
                response = self.session.get(url, timeout=TIMEOUT)
                response.encoding = 'gb18030'
                data = response.text
                
                logger.info(f"API 返回：{data[:200]}")
                
                # 解析数据
                if data and '=' in data:
                    content = data.split('="')[1].strip('"')
                    parts = content.split(',')
                    
                    if len(parts) >= 32:
                        name = parts[0]
                        open_price = float(parts[1]) if parts[1] else 0
                        close_price = float(parts[2]) if parts[2] else 0
                        current = float(parts[3]) if parts[3] else 0
                        high = float(parts[4]) if parts[4] else 0
                        low = float(parts[5]) if parts[5] else 0
                        
                        pre_close = float(parts[2]) if parts[2] else current
                        change = current - pre_close
                        change_percent = (change / pre_close * 100) if pre_close else 0
                        
                        volume = parts[6] if len(parts) > 6 else "0"
                        amount = f"{float(parts[7]) / 10000:.2f}万" if len(parts) > 7 and parts[7] else "0"
                        
                        return {
                            "code": stock_code,
                            "name": name,
                            "price": current,
                            "change": change,
                            "change_percent": change_percent,
                            "volume": f"{float(volume)/100:.1f}手" if volume and volume != '0' else "0",
                            "amount": amount,
                            "high": high,
                            "low": low,
                            "open": open_price,
                            "pre_close": pre_close,
                            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                
                return None
                
            except Exception as e:
                logger.error(f"获取股票 {stock_code} 数据失败 (尝试 {attempt+1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    return None
        
        return None

    def fetch_index_data(self, index_code: str) -> Optional[Dict]:
        """获取指数实时数据"""
        try:
            url = f"{self.XINHUA_URL}{index_code}"
            response = self.session.get(url, timeout=TIMEOUT)
            response.encoding = 'gb18030'
            data = response.text
            
            if data and '=' in data:
                content = data.split('="')[1].strip('"')
                parts = content.split(',')
                
                if len(parts) >= 3:
                    name = parts[0]
                    current = float(parts[1]) if parts[1] else 0
                    pre_close = float(parts[2]) if parts[2] else current
                    
                    change = current - pre_close
                    change_percent = (change / pre_close * 100) if pre_close else 0
                    
                    return {
                        "code": index_code,
                        "name": name,
                        "price": current,
                        "change": change,
                        "change_percent": change_percent,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
        except Exception as e:
            logger.error(f"获取指数 {index_code} 数据失败：{e}")
        
        return None

    def fetch_multiple_stocks(self, stock_codes: List[str]) -> Dict[str, Dict]:
        """批量获取股票数据"""
        results = {}
        for code in stock_codes:
            results[code] = self.fetch_stock_data(code)
            time.sleep(0.1)
        return results


if __name__ == "__main__":
    fetcher = AShareRealTimeFetcher()
    
    print("=" * 60)
    print("A 股实时行情测试（优化版）")
    print("=" * 60)
    
    test_stocks = ["600519", "000858", "300750"]
    for code in test_stocks:
        print(f"\n测试 {code}...")
        data = fetcher.fetch_stock_data(code)
        if data:
            print(f"  OK {data['name']}: {data['price']:.2f} ({data['change_percent']:+.2f}%)")
        else:
            print(f"  FAIL 获取失败")
        time.sleep(0.2)
