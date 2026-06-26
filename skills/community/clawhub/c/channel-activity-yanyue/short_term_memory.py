#!/usr/bin/env python3
"""
短期记忆系统 - 核心功能实现
功能：1分钟临时记忆缓存，支持多通道信息整合
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import uuid

class ShortTermMemory:
    """短期记忆管理器"""
    
    def __init__(self, cache_path: str = None):
        self.cache_path = cache_path or "memory/short-term-cache.json"
        self.config = {
            "ttl_seconds": 1800,  # 30分钟
            "max_entries": 50,
            "cleanup_interval_seconds": 300,  # 5分钟清理一次
            "auto_cleanup": True,
            "upgrade_to_long_term": True
        }
        self.entries = []
        self.last_cleanup = time.time()
        self._load_cache()
    
    def _load_cache(self):
        """加载缓存文件"""
        try:
            if Path(self.cache_path).exists():
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.entries = data.get('entries', [])
                    self.config.update(data.get('config', {}))
        except Exception as e:
            print(f"[短期记忆] 加载缓存失败: {e}")
            self.entries = []
    
    def _save_cache(self):
        """保存缓存文件"""
        try:
            Path(self.cache_path).parent.mkdir(parents=True, exist_ok=True)
            data = {
                "module": "short-term-memory",
                "version": "1.0.0",
                "updated": datetime.now().isoformat(),
                "config": self.config,
                "entries": self.entries,
                "stats": {
                    "total_entries": len(self.entries),
                    "channels": self._count_channels(),
                    "last_cleanup": datetime.fromtimestamp(self.last_cleanup).isoformat()
                }
            }
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[短期记忆] 保存缓存失败: {e}")
    
    def _count_channels(self) -> Dict[str, int]:
        """统计各通道条目数"""
        channels = {}
        for entry in self.entries:
            channel = entry.get('channel', 'unknown')
            channels[channel] = channels.get(channel, 0) + 1
        return channels
    
    def _cleanup_expired(self):
        """清理过期条目"""
        now = time.time()
        if now - self.last_cleanup > self.config['cleanup_interval_seconds']:
            before_count = len(self.entries)
            self.entries = [
                entry for entry in self.entries
                if entry.get('expires_at', 0) > now
            ]
            after_count = len(self.entries)
            if before_count > after_count:
                print(f"[短期记忆] 清理了 {before_count - after_count} 条过期记忆")
            self.last_cleanup = now
            self._save_cache()
    
    def write(
        self,
        content: str,
        channel: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None
    ) -> str:
        """
        写入短期记忆
        
        Args:
            content: 记忆内容
            channel: 通道标识（feishu, qq, etc.）
            user_id: 用户ID
            context: 上下文信息（可选）
            ttl: 过期时间（秒，可选，默认使用配置）
        
        Returns:
            记忆ID
        """
        # 清理过期条目
        if self.config['auto_cleanup']:
            self._cleanup_expired()
        
        # 检查容量
        if len(self.entries) >= self.config['max_entries']:
            # 删除最旧的条目
            self.entries.sort(key=lambda x: x['timestamp'], reverse=True)
            self.entries = self.entries[:self.config['max_entries'] - 1]
        
        # 创建新条目
        now = time.time()
        ttl_seconds = ttl or self.config['ttl_seconds']
        entry_id = f"{int(now)}_{uuid.uuid4().hex[:8]}"
        
        entry = {
            "id": entry_id,
            "timestamp": now,
            "created_at": datetime.fromtimestamp(now).isoformat(),
            "expires_at": now + ttl_seconds,
            "ttl_seconds": ttl_seconds,
            "channel": channel,
            "user_id": user_id,
            "content": content,
            "context": context or {}
        }
        
        self.entries.append(entry)
        self._save_cache()
        
        print(f"[短期记忆] 写入成功: {entry_id} (TTL: {ttl_seconds}秒)")
        return entry_id
    
    def read(
        self,
        channel: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        读取短期记忆
        
        Args:
            channel: 过滤通道（可选）
            user_id: 过滤用户ID（可选）
            limit: 返回条目数限制
        
        Returns:
            记忆条目列表
        """
        # 清理过期条目
        if self.config['auto_cleanup']:
            self._cleanup_expired()
        
        # 过滤条目
        results = []
        now = time.time()
        
        for entry in reversed(self.entries):  # 最新的在前
            # 检查是否过期
            if entry.get('expires_at', 0) <= now:
                continue
            
            # 过滤条件
            if channel and entry.get('channel') != channel:
                continue
            if user_id and entry.get('user_id') != user_id:
                continue
            
            results.append(entry)
            
            if len(results) >= limit:
                break
        
        return results
    
    def query(self, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        查询短期记忆
        
        Args:
            query_text: 查询文本
            limit: 返回条目数限制
        
        Returns:
            匹配的记忆条目列表
        """
        # 清理过期条目
        if self.config['auto_cleanup']:
            self._cleanup_expired()
        
        results = []
        query_lower = query_text.lower()
        now = time.time()
        
        for entry in reversed(self.entries):
            # 检查是否过期
            if entry.get('expires_at', 0) <= now:
                continue
            
            # 简单文本匹配
            if query_lower in entry.get('content', '').lower():
                results.append(entry)
                
                if len(results) >= limit:
                    break
        
        return results
    
    def upgrade_to_long_term(self, entry_id: str) -> bool:
        """
        升级为长期记忆
        
        Args:
            entry_id: 记忆ID
        
        Returns:
            是否成功
        """
        # 查找条目
        entry = None
        for e in self.entries:
            if e.get('id') == entry_id:
                entry = e
                break
        
        if not entry:
            print(f"[短期记忆] 未找到条目: {entry_id}")
            return False
        
        # 写入长期记忆（这里需要实现MEMORY.md的写入逻辑）
        # TODO: 实现MEMORY.md的追加写入
        
        print(f"[短期记忆] 升级为长期记忆: {entry_id}")
        print(f"内容: {entry.get('content')}")
        
        # 从短期记忆中移除
        self.entries = [e for e in self.entries if e.get('id') != entry_id]
        self._save_cache()
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        if self.config['auto_cleanup']:
            self._cleanup_expired()
        
        return {
            "total_entries": len(self.entries),
            "channels": self._count_channels(),
            "last_cleanup": datetime.fromtimestamp(self.last_cleanup).isoformat(),
            "config": self.config
        }

# 使用示例
if __name__ == "__main__":
    stm = ShortTermMemory()
    
    # 写入测试
    entry_id = stm.write(
        content="星之君说：记住要完成X任务",
        channel="feishu",
        user_id="ou_472d0b86d66dd43850b6d7c249c76d28",
        context={"type": "task", "priority": "high"}
    )
    
    # 读取测试
    entries = stm.read()
    print(f"\n当前短期记忆: {len(entries)} 条")
    
    # 查询测试
    results = stm.query("任务")
    print(f"\n查询结果: {len(results)} 条匹配")
    
    # 统计
    stats = stm.get_stats()
    print(f"\n统计信息: {json.dumps(stats, indent=2, ensure_ascii=False)}")