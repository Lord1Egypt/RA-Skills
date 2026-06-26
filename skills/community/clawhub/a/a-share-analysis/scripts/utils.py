#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股分析系统 - 工具函数库
包含：重试机制、缓存、日志、数据验证等
"""

import os
import sys
import json
import time
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from functools import wraps
import requests

# 配置
CONFIG = {
    'cache_enabled': True,
    'cache_ttl': 300,  # 5 分钟
    'cache_dir': 'cache',
    'max_retries': 3,
    'retry_delay': 1,  # 秒
    'timeout': 10,
    'output_dir': 'a-share-reports',
    'memory_dir': 'memory',
}

# 日志设置
def setup_logger(name: str, log_file: str = 'analysis.log', level: int = logging.INFO) -> logging.Logger:
    """设置日志"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 文件处理器
    try:
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(level)
        
        # 格式化
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception as e:
        print(f"日志文件创建失败：{e}")
    
    # 控制台处理器
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger

logger = setup_logger('ashare')


# 重试装饰器
def retry(max_retries: int = None, delay: float = None):
    """重试装饰器"""
    if max_retries is None:
        max_retries = CONFIG['max_retries']
    if delay is None:
        delay = CONFIG['retry_delay']
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"{func.__name__} 失败 ({i+1}/{max_retries}): {e}")
                    if i < max_retries - 1:
                        time.sleep(delay * (i + 1))  # 递增延迟
            logger.error(f"{func.__name__} 最终失败：{last_exception}")
            raise last_exception
        return wrapper
    return decorator


# 缓存装饰器
def cache(ttl: int = None, cache_dir: str = None):
    """缓存装饰器"""
    if ttl is None:
        ttl = CONFIG['cache_ttl']
    if cache_dir is None:
        cache_dir = os.path.join(os.path.dirname(__file__), CONFIG['cache_dir'])
    
    os.makedirs(cache_dir, exist_ok=True)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not CONFIG['cache_enabled']:
                return func(*args, **kwargs)
            
            # 生成缓存键
            cache_key = hashlib.md5(
                f"{func.__name__}:{args}:{kwargs}".encode()
            ).hexdigest()
            cache_file = os.path.join(cache_dir, f"{cache_key}.json")
            
            # 检查缓存
            if os.path.exists(cache_file):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached = json.load(f)
                    
                    # 检查过期
                    cached_time = datetime.fromisoformat(cached['_cached_at'])
                    if datetime.now() - cached_time < timedelta(seconds=ttl):
                        logger.debug(f"缓存命中：{func.__name__}")
                        return cached['_data']
                    else:
                        os.remove(cache_file)
                except Exception as e:
                    logger.warning(f"缓存读取失败：{e}")
                    if os.path.exists(cache_file):
                        os.remove(cache_file)
            
            # 执行函数并缓存
            result = func(*args, **kwargs)
            
            try:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        '_cached_at': datetime.now().isoformat(),
                        '_data': result
                    }, f, ensure_ascii=False, indent=2, default=str)
                logger.debug(f"缓存已保存：{func.__name__}")
            except Exception as e:
                logger.warning(f"缓存保存失败：{e}")
            
            return result
        return wrapper
    return decorator


# 数据验证
def validate_stock_data(data: Dict) -> bool:
    """验证股票数据"""
    required_fields = ['code', 'name', 'price']
    
    for field in required_fields:
        if field not in data:
            logger.error(f"缺少必需字段：{field}")
            return False
    
    if data['price'] <= 0:
        logger.error(f"无效价格：{data['price']}")
        return False
    
    if not isinstance(data.get('change_percent'), (int, float)):
        logger.warning(f"涨跌幅类型错误：{type(data.get('change_percent'))}")
    
    return True


def validate_technical_data(data: Dict) -> bool:
    """验证技术分析数据"""
    if not data:
        return False
    
    required = ['signal', 'trend']
    for field in required:
        if field not in data:
            logger.warning(f"技术分析缺少字段：{field}")
    
    return True


# 性能监控
def timing(func: Callable) -> Callable:
    """性能监控装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{func.__name__} 耗时：{elapsed:.2f}秒")
        return result
    return wrapper


# 批量分析汇总
def batch_analyze_summary(results: List[Dict]) -> Dict:
    """批量分析汇总"""
    if not results:
        return {'error': '无数据'}
    
    total = len(results)
    bullish = sum(1 for r in results if r.get('technical', {}).get('signal') == 'bullish')
    bearish = sum(1 for r in results if r.get('technical', {}).get('signal') == 'bearish')
    neutral = sum(1 for r in results if r.get('technical', {}).get('signal') == 'neutral')
    
    scores = [calculate_score(r) for r in results]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    return {
        'total': total,
        'bullish': bullish,
        'bearish': bearish,
        'neutral': neutral,
        'avg_score': round(avg_score, 1),
        'bullish_ratio': round(bullish / total * 100, 1),
        'bearish_ratio': round(bearish / total * 100, 1),
        'neutral_ratio': round(neutral / total * 100, 1),
    }


def calculate_score(data: Dict) -> float:
    """计算综合评分"""
    score = 5.0
    
    technical = data.get('technical', {})
    if technical.get('signal') == 'bullish':
        score += 1.5
    elif technical.get('signal') == 'bearish':
        score -= 1.5
    
    if technical.get('trend') == 'bullish':
        score += 0.5
    elif technical.get('trend') == 'bearish':
        score -= 0.5
    
    sentiment = data.get('news_sentiment', {})
    sentiment_score = sentiment.get('avg_sentiment_score', 0.5)
    score += (sentiment_score - 0.5) * 3
    
    change = data.get('change_percent', 0)
    if change > 3:
        score += 0.5
    elif change < -3:
        score -= 0.5
    
    return max(0, min(10, score))


# 股票池管理
class StockPool:
    """股票池管理"""
    
    def __init__(self, pool_file: str = 'stock_pool.json'):
        self.pool_file = pool_file
        self.data = self._load()
    
    def _load(self) -> Dict:
        """加载股票池"""
        if os.path.exists(self.pool_file):
            try:
                with open(self.pool_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            'watchlist': [],
            'portfolio': [],
            'blacklist': []
        }
    
    def save(self):
        """保存股票池"""
        with open(self.pool_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_to_watchlist(self, code: str):
        """添加到自选"""
        if code not in self.data['watchlist']:
            self.data['watchlist'].append(code)
            self.save()
            logger.info(f"添加到自选：{code}")
    
    def remove_from_watchlist(self, code: str):
        """从自选移除"""
        if code in self.data['watchlist']:
            self.data['watchlist'].remove(code)
            self.save()
            logger.info(f"从自选移除：{code}")
    
    def add_to_portfolio(self, code: str):
        """添加到持仓"""
        if code not in self.data['portfolio']:
            self.data['portfolio'].append(code)
            self.save()
            logger.info(f"添加到持仓：{code}")
    
    def add_to_blacklist(self, code: str):
        """添加到黑名单"""
        if code not in self.data['blacklist']:
            self.data['blacklist'].append(code)
            self.save()
            logger.info(f"添加到黑名单：{code}")
    
    def get_watchlist(self) -> List[str]:
        """获取自选列表"""
        return self.data['watchlist']
    
    def get_portfolio(self) -> List[str]:
        """获取持仓列表"""
        return self.data['portfolio']
    
    def is_blacklisted(self, code: str) -> bool:
        """检查是否在黑名单"""
        return code in self.data['blacklist']


# 清除缓存
def clear_cache(cache_dir: str = None):
    """清除缓存"""
    if cache_dir is None:
        cache_dir = os.path.join(os.path.dirname(__file__), CONFIG['cache_dir'])
    
    if not os.path.exists(cache_dir):
        return
    
    count = 0
    for file in os.listdir(cache_dir):
        if file.endswith('.json'):
            os.remove(os.path.join(cache_dir, file))
            count += 1
    
    logger.info(f"清除缓存：{count} 个文件")


# 系统信息
def get_system_info() -> Dict:
    """获取系统信息"""
    import platform
    
    return {
        'python_version': sys.version,
        'platform': platform.platform(),
        'config': CONFIG,
        'cache_enabled': CONFIG['cache_enabled'],
        'cache_dir': os.path.join(os.path.dirname(__file__), CONFIG['cache_dir']),
    }


if __name__ == "__main__":
    # 测试
    print("A 股分析系统工具库测试")
    print("=" * 50)
    
    # 测试系统信息
    info = get_system_info()
    print(f"Python: {info['python_version'][:50]}")
    print(f"缓存：{'启用' if info['cache_enabled'] else '禁用'}")
    
    # 测试股票池
    pool = StockPool()
    print(f"\n自选列表：{pool.get_watchlist()}")
    print(f"持仓列表：{pool.get_portfolio()}")
    
    # 测试评分计算
    test_data = {
        'technical': {'signal': 'bullish', 'trend': 'bullish'},
        'change_percent': 1.5
    }
    score = calculate_score(test_data)
    print(f"\n测试评分：{score}")
