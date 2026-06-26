#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据缓存模块
功能：本地缓存股票数据，减少 API 调用，提高响应速度
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

# 缓存配置
CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')
CACHE_EXPIRY = 300  # 缓存过期时间（秒）= 5 分钟

class StockCache:
    """股票数据缓存类"""
    
    def __init__(self):
        """初始化缓存目录"""
        os.makedirs(CACHE_DIR, exist_ok=True)
        self.cache_file = os.path.join(CACHE_DIR, 'stock_cache.json')
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """加载缓存文件"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"[缓存加载失败]: {e}")
        return {}
    
    def _save_cache(self):
        """保存缓存文件"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[缓存保存失败]: {e}")
    
    def _is_expired(self, timestamp: float) -> bool:
        """检查缓存是否过期"""
        return (datetime.now().timestamp() - timestamp) > CACHE_EXPIRY
    
    def get(self, stock_code: str) -> Optional[Dict]:
        """
        获取缓存数据
        
        Args:
            stock_code: 股票代码
        
        Returns:
            缓存的数据，如果不存在或已过期则返回 None
        """
        if stock_code in self.cache:
            cached = self.cache[stock_code]
            if not self._is_expired(cached['timestamp']):
                print(f"[缓存命中] {stock_code}")
                return cached['data']
            else:
                print(f"[缓存过期] {stock_code}")
                del self.cache[stock_code]
        return None
    
    def set(self, stock_code: str, data: Dict):
        """
        设置缓存数据
        
        Args:
            stock_code: 股票代码
            data: 要缓存的数据
        """
        self.cache[stock_code] = {
            'data': data,
            'timestamp': datetime.now().timestamp(),
            'expiry': CACHE_EXPIRY
        }
        self._save_cache()
        print(f"[缓存已保存] {stock_code}")
    
    def clear(self):
        """清空所有缓存"""
        self.cache = {}
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        print("[缓存已清空]")
    
    def get_stats(self) -> Dict:
        """获取缓存统计信息"""
        now = datetime.now().timestamp()
        valid_count = sum(1 for c in self.cache.values() if not self._is_expired(c['timestamp']))
        expired_count = len(self.cache) - valid_count
        
        return {
            'total_items': len(self.cache),
            'valid_items': valid_count,
            'expired_items': expired_count,
            'cache_file_size': os.path.getsize(self.cache_file) if os.path.exists(self.cache_file) else 0,
            'expiry_seconds': CACHE_EXPIRY
        }


# 测试
if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    cache = StockCache()
    
    # 测试缓存
    test_data = {
        'success': True,
        'code': '002892',
        'name': '科力尔',
        'current_price': 11.84,
        'change_pct': 0.42
    }
    
    print("=" * 50)
    print("数据缓存模块测试")
    print("=" * 50)
    
    # 设置缓存
    print("\n[测试] 设置缓存")
    cache.set('002892', test_data)
    
    # 获取缓存
    print("\n[测试] 获取缓存")
    cached = cache.get('002892')
    if cached:
        print(f"✅ 缓存数据：{cached}")
    
    # 获取统计
    print("\n[测试] 缓存统计")
    stats = cache.get_stats()
    print(f"总项数：{stats['total_items']}")
    print(f"有效项：{stats['valid_items']}")
    print(f"过期项：{stats['expired_items']}")
    print(f"缓存文件大小：{stats['cache_file_size']} bytes")
    
    print("\n" + "=" * 50)
