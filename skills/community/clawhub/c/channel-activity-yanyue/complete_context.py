#!/usr/bin/env python3
"""
完整上下文系统 - 短期记忆 + 长期记忆整合
改进版本：支持30分钟TTL + 完整上下文整合
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import uuid

class CompleteContext:
    """完整上下文管理器 - 短期记忆 + 长期记忆"""
    
    def __init__(self, workspace_path: str = None):
        self.workspace_path = workspace_path or "."
        self.stm_cache_path = f"{self.workspace_path}/memory/short-term-cache.json"
        self.ltm_path = f"{self.workspace_path}/MEMORY.md"
        
        # 短期记忆配置：30分钟TTL
        self.stm_config = {
            "ttl_seconds": 1800,  # 30分钟
            "max_entries": 50,
            "cleanup_interval_seconds": 300,  # 5分钟清理
            "auto_cleanup": True
        }
        
        self.stm_entries = []
        self.ltm_content = ""
        self.last_cleanup = time.time()
        
        self._load_all()
    
    def _load_all(self):
        """加载短期和长期记忆"""
        self._load_stm()
        self._load_ltm()
    
    def _load_stm(self):
        """加载短期记忆"""
        try:
            if Path(self.stm_cache_path).exists():
                with open(self.stm_cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.stm_entries = data.get('entries', [])
                    self.stm_config.update(data.get('config', {}))
        except Exception as e:
            print(f"[完整上下文] 加载短期记忆失败: {e}")
            self.stm_entries = []
    
    def _load_ltm(self):
        """加载长期记忆"""
        try:
            if Path(self.ltm_path).exists():
                with open(self.ltm_path, 'r', encoding='utf-8') as f:
                    self.ltm_content = f.read()
        except Exception as e:
            print(f"[完整上下文] 加载长期记忆失败: {e}")
            self.ltm_content = ""
    
    def _save_stm(self):
        """保存短期记忆"""
        try:
            Path(self.stm_cache_path).parent.mkdir(parents=True, exist_ok=True)
            data = {
                "module": "complete-context",
                "version": "2.0.0",
                "updated": datetime.now().isoformat(),
                "config": self.stm_config,
                "entries": self.stm_entries
            }
            with open(self.stm_cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[完整上下文] 保存短期记忆失败: {e}")
    
    def _cleanup_expired(self):
        """清理过期短期记忆"""
        now = time.time()
        if now - self.last_cleanup > self.stm_config['cleanup_interval_seconds']:
            before_count = len(self.stm_entries)
            expired_entries = [
                entry for entry in self.stm_entries
                if entry.get('expires_at', 0) <= now
            ]
            
            # 将过期内容升级到长期记忆
            if expired_entries:
                self._upgrade_to_ltm(expired_entries)
            
            self.stm_entries = [
                entry for entry in self.stm_entries
                if entry.get('expires_at', 0) > now
            ]
            
            after_count = len(self.stm_entries)
            if before_count > after_count:
                print(f"[完整上下文] 清理了 {before_count - after_count} 条过期短期记忆")
            
            self.last_cleanup = now
            self._save_stm()
    
    def _upgrade_to_ltm(self, entries: List[Dict]):
        """将过期短期记忆升级到长期记忆"""
        if not entries:
            return
        
        # TODO: 实现MEMORY.md的追加写入
        # 这里需要根据MEMORY.md的实际格式来实现
        
        print(f"[完整上下文] 准备升级 {len(entries)} 条记忆到长期记忆")
        for entry in entries:
            print(f"  - {entry.get('content', '')[:50]}...")
    
    # ========== 核心接口 ==========
    
    def write_stm(
        self,
        content: str,
        channel: str,
        user_id: str,
        context: Optional[Dict] = None,
        ttl: Optional[int] = None
    ) -> str:
        """
        写入短期记忆
        
        Args:
            content: 记忆内容
            channel: 通道标识
            user_id: 用户ID
            context: 上下文信息
            ttl: 过期时间（默认30分钟）
        
        Returns:
            记忆ID
        """
        # 清理过期内容
        if self.stm_config['auto_cleanup']:
            self._cleanup_expired()
        
        # 检查容量
        if len(self.stm_entries) >= self.stm_config['max_entries']:
            # 触发升级
            self._upgrade_to_ltm(self.stm_entries[:10])
            self.stm_entries = self.stm_entries[10:]
        
        # 创建新条目
        now = time.time()
        ttl_seconds = ttl or self.stm_config['ttl_seconds']
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
        
        self.stm_entries.append(entry)
        self._save_stm()
        
        print(f"[完整上下文] 写入短期记忆: {entry_id} (TTL: {ttl_seconds}秒)")
        return entry_id
    
    def get_complete_context(
        self,
        channel: Optional[str] = None,
        user_id: Optional[str] = None,
        include_ltm: bool = True
    ) -> Dict[str, Any]:
        """
        获取完整上下文（短期 + 长期）
        
        Args:
            channel: 过滤通道
            user_id: 过滤用户
            include_ltm: 是否包含长期记忆
        
        Returns:
            {
                "short_term": [...],  # 短期记忆
                "long_term": "...",    # 长期记忆
                "combined": "..."      # 整合后的完整上下文
            }
        """
        # 清理过期内容
        if self.stm_config['auto_cleanup']:
            self._cleanup_expired()
        
        # 获取短期记忆
        stm_results = []
        now = time.time()
        
        for entry in reversed(self.stm_entries):
            if entry.get('expires_at', 0) <= now:
                continue
            if channel and entry.get('channel') != channel:
                continue
            if user_id and entry.get('user_id') != user_id:
                continue
            stm_results.append(entry)
        
        # 构建完整上下文
        result = {
            "short_term": stm_results,
            "long_term": self.ltm_content if include_ltm else "",
            "stats": {
                "stm_count": len(stm_results),
                "ltm_length": len(self.ltm_content) if include_ltm else 0,
                "channels": self._count_channels(stm_results)
            }
        }
        
        # 整合上下文
        result["combined"] = self._combine_context(stm_results, self.ltm_content if include_ltm else "")
        
        return result
    
    def _count_channels(self, entries: List[Dict]) -> Dict[str, int]:
        """统计通道分布"""
        channels = {}
        for entry in entries:
            channel = entry.get('channel', 'unknown')
            channels[channel] = channels.get(channel, 0) + 1
        return channels
    
    def _combine_context(
        self,
        stm_entries: List[Dict],
        ltm_content: str
    ) -> str:
        """
        整合短期和长期记忆为完整上下文
        
        格式：
        [短期记忆 - 最近30分钟]
        - 内容1
        - 内容2
        
        [长期记忆 - 永久记忆]
        MEMORY.md内容
        """
        combined = []
        
        # 短期记忆部分
        if stm_entries:
            combined.append("[短期记忆 - 最近30分钟]")
            for entry in stm_entries:
                timestamp = entry.get('created_at', '')
                content = entry.get('content', '')
                channel = entry.get('channel', '')
                combined.append(f"- [{channel}] {timestamp}: {content}")
            combined.append("")
        
        # 长期记忆部分
        if ltm_content:
            combined.append("[长期记忆 - 永久记忆]")
            combined.append(ltm_content)
        
        return "\n".join(combined)
    
    def query(self, query_text: str, limit: int = 10) -> Dict[str, Any]:
        """
        查询完整上下文
        
        Args:
            query_text: 查询文本
            limit: 返回条目限制
        
        Returns:
            {
                "short_term_matches": [...],
                "long_term_matches": [...],
                "total_matches": int
            }
        """
        # 清理过期内容
        if self.stm_config['auto_cleanup']:
            self._cleanup_expired()
        
        query_lower = query_text.lower()
        now = time.time()
        
        # 查询短期记忆
        stm_matches = []
        for entry in reversed(self.stm_entries):
            if entry.get('expires_at', 0) <= now:
                continue
            if query_lower in entry.get('content', '').lower():
                stm_matches.append(entry)
                if len(stm_matches) >= limit:
                    break
        
        # 查询长期记忆
        ltm_matches = []
        if query_lower in self.ltm_content.lower():
            # 简单返回包含查询词的行
            lines = self.ltm_content.split('\n')
            for i, line in enumerate(lines):
                if query_lower in line.lower():
                    ltm_matches.append({
                        "line_number": i + 1,
                        "content": line.strip()
                    })
                    if len(ltm_matches) >= limit:
                        break
        
        return {
            "short_term_matches": stm_matches,
            "long_term_matches": ltm_matches,
            "total_matches": len(stm_matches) + len(ltm_matches)
        }


# 使用示例
if __name__ == "__main__":
    ctx = CompleteContext(".")
    
    # 写入测试
    entry_id = ctx.write_stm(
        content="星之君要求：短期记忆30分钟TTL",
        channel="feishu",
        user_id="ou_472d0b86d66dd43850b6d7c249c76d28",
        context={"type": "requirement", "priority": "high"}
    )
    
    # 获取完整上下文
    complete = ctx.get_complete_context()
    print(f"\n✅ 短期记忆: {complete['stats']['stm_count']} 条")
    print(f"✅ 长期记忆: {complete['stats']['ltm_length']} 字符")
    print(f"\n完整上下文:\n{complete['combined'][:500]}...")
    
    # 查询测试
    results = ctx.query("短期记忆")
    print(f"\n✅ 查询结果: {results['total_matches']} 条匹配")