"""
回复缓存管理器
- 缓存最近100条已回复的内容
- 相同或相似的消息直接复用缓存回复
"""
import json
import os
import hashlib
from collections import OrderedDict
from typing import Optional, Dict
from config import REPLY_FILE


class ReplyCache:
    """回复缓存管理器"""
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        # 使用 OrderedDict 保持插入顺序，方便淘汰旧缓存
        self.cache = OrderedDict()
        self.load_from_file()
    
    def _generate_key(self, user_message: str) -> str:
        """
        生成消息的唯一key
        使用消息内容的hash作为key
        """
        # 清理消息：去除空格、转小写
        cleaned = user_message.strip().lower().replace(" ", "").replace("　", "")
        return hashlib.md5(cleaned.encode('utf-8')).hexdigest()
    
    def get(self, user_message: str) -> Optional[Dict]:
        """
        从缓存获取回复
        
        Returns:
            缓存的回复数据，如果没有则返回None
        """
        key = self._generate_key(user_message)
        
        if key in self.cache:
            # 移动到末尾（最新使用）
            self.cache.move_to_end(key)
            return self.cache[key]
        
        return None
    
    def set(self, user_message: str, reply_data: Dict):
        """
        设置缓存
        """
        key = self._generate_key(user_message)
        
        # 如果已存在，先删除再添加（移动到末尾）
        if key in self.cache:
            del self.cache[key]
        
        # 添加到缓存
        self.cache[key] = {
            'user_message': user_message,
            'ai_reply': reply_data.get('reply'),
            'timestamp': reply_data.get('timestamp'),
            'use_count': 1  # 使用次数
        }
        
        # 如果超过最大容量，淘汰最旧的
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
        
        # 保存到文件
        self.save_to_file()
    
    def increment_use(self, user_message: str):
        """增加缓存使用次数"""
        key = self._generate_key(user_message)
        if key in self.cache:
            self.cache[key]['use_count'] = self.cache[key].get('use_count', 1) + 1
            self.cache.move_to_end(key)
            self.save_to_file()
    
    def load_from_file(self):
        """从文件加载缓存"""
        cache_file = REPLY_FILE.replace('.jsonl', '_cache.json')
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 转换为 OrderedDict
                    for key, value in data.items():
                        self.cache[key] = value
            except Exception as e:
                print(f"加载缓存失败: {e}")
    
    def save_to_file(self):
        """保存缓存到文件"""
        cache_file = REPLY_FILE.replace('.jsonl', '_cache.json')
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(dict(self.cache), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存缓存失败: {e}")
    
    def get_stats(self) -> Dict:
        """获取缓存统计信息"""
        return {
            'total_cached': len(self.cache),
            'max_size': self.max_size,
            'total_uses': sum(item.get('use_count', 1) for item in self.cache.values())
        }
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
        cache_file = REPLY_FILE.replace('.jsonl', '_cache.json')
        if os.path.exists(cache_file):
            os.remove(cache_file)


# 全局缓存实例
_reply_cache = None


def get_cache() -> ReplyCache:
    """获取全局缓存实例"""
    global _reply_cache
    if _reply_cache is None:
        _reply_cache = ReplyCache(max_size=100)
    return _reply_cache


def get_cached_reply(user_message: str) -> Optional[str]:
    """
    获取缓存的回复
    
    Returns:
        缓存的回复内容，如果没有则返回None
    """
    cache = get_cache()
    cached = cache.get(user_message)
    
    if cached:
        # 增加使用次数
        cache.increment_use(user_message)
        return cached['ai_reply']
    
    return None


def cache_reply(user_message: str, reply: str, timestamp: str = None):
    """
    缓存回复
    """
    if timestamp is None:
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cache = get_cache()
    cache.set(user_message, {
        'reply': reply,
        'timestamp': timestamp
    })


if __name__ == '__main__':
    # 测试缓存功能
    print("测试回复缓存功能")
    print("=" * 60)
    
    # 模拟缓存回复
    cache_reply("樊老师孩子高敏感怎么引导", "高敏感孩子需要接纳和理解...")
    cache_reply("这本书多少钱", "这本书今天直播间有优惠...")
    
    # 获取缓存
    print("\n测试获取缓存：")
    msg = "樊老师孩子高敏感怎么引导"
    cached = get_cached_reply(msg)
    if cached:
        print(f"命中缓存: {cached}")
    else:
        print("缓存未命中")
    
    # 获取不同消息
    msg2 = "没见过的消息"
    cached2 = get_cached_reply(msg2)
    if cached2:
        print(f"命中缓存: {cached2}")
    else:
        print(f"'{msg2}' 缓存未命中")
    
    # 统计
    stats = get_cache().get_stats()
    print(f"\n缓存统计: {stats}")
