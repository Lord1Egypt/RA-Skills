#!/usr/bin/env python3
"""
FeishuMentionResolver - 飞书@提及解析器 (Python 版本)

将文本中的 @name 自动替换为 @name openid 格式
支持多 bot、多群，API 结果本地缓存 2 小时
"""

import json
import os
import re
import time
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any
import hashlib


class FeishuMentionResolver:
    """飞书@提及解析器"""
    
    def __init__(self, cache_dir: Optional[str] = None, options: Optional[Dict] = None):
        """
        初始化解析器
        
        Args:
            cache_dir: 缓存目录路径，默认 ~/.openclaw/workspace/cache/feishu_mentions
            options: 配置选项
                - botMappings: {"@机器人名": "rs_xxx"}
                - aliases: [{"name": "真实名", "alias": ["别名 1"]}]
        """
        self.cache_dir = Path(cache_dir) if cache_dir else \
            Path.home() / ".openclaw" / "workspace" / "cache" / "feishu_mentions"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 缓存过期时间：2 小时
        self.cache_ttl = 2 * 60 * 60  # 2 hours in seconds
        
        # ========== 新增功能 ==========
        # 机器人映射表
        self.bot_mappings = options.get('botMappings', {}) if options else {}
        
        # 用户别名映射
        self.user_aliases = options.get('aliases', []) if options else []
        
        # 内存缓存
        self.memory_cache: Dict[Tuple[str, str], List[Dict]] = {}
        
        print("[FeishuMention] 已启用机器人和别名支持")
        print(f"   - 机器人数量：{len(self.bot_mappings)}")
        print(f"   - 别名规则数：{len(self.user_aliases)}")
    
    def _get_cache_file(self, app_id: str, chat_id: str) -> Path:
        """获取特定 bot+群的缓存文件路径"""
        cache_key = f"{app_id}_{chat_id}"
        cache_hash = hashlib.md5(cache_key.encode()).hexdigest()[:16]
        return self.cache_dir / f"{cache_hash}.json"
    
    def _load_cache(self, app_id: str, chat_id: str) -> Optional[List[Dict]]:
        """加载缓存数据"""
        cache_file = self._get_cache_file(app_id, chat_id)
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查是否过期
            if time.time() - data.get("updated_at", 0) > self.cache_ttl:
                return None
            
            return data.get("members_data")
        except (json.JSONDecodeError, IOError):
            return None
    
    def _save_cache(self, app_id: str, chat_id: str, members_data: List[Dict]):
        """保存缓存数据"""
        cache_file = self._get_cache_file(app_id, chat_id)
        
        cached_data = {
            "updated_at": time.time(),
            "members_data": members_data
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cached_data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"警告：无法保存缓存到 {cache_file}: {e}")
    
    def get_cached_members(self, app_id: str, chat_id: str) -> Optional[List[Dict]]:
        """从缓存获取成员列表"""
        cache_key = (app_id, chat_id)
        
        # 先查内存缓存
        if cache_key in self.memory_cache:
            timestamp, members = self.memory_cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return members
        
        # 再查文件缓存
        members = self._load_cache(app_id, chat_id)
        
        if members:
            self.memory_cache[cache_key] = (time.time(), members)
        
        return members
    
    def save_cache(self, app_id: str, chat_id: str, members_data: List[Dict]):
        """保存成员列表到缓存"""
        cache_key = (app_id, chat_id)
        self._save_cache(app_id, chat_id, members_data)
        self.memory_cache[cache_key] = (time.time(), members_data)
    
    async def resolve_mention(self, mention: str, app_id: str, chat_id: str) -> str:
        """解析单个提及"""
        # 检查是否已经是 openid 格式
        if re.match(r'^@.*?:ou_', mention):
            return mention
        
        name_match = re.match(r'^@(.*?)$', mention)
        if not name_match:
            return mention
        
        name = name_match.group(1)
        matched_openid = None
        
        # ========== 改进：优先级处理 ==========
        
        # ① 优先检查机器人映射表（最高优先级）
        if name in self.bot_mappings:
            matched_openid = self.bot_mappings[name]
            print(f"[FeishuMention] 匹配到机器人：{name} → {matched_openid}")
            return f"@{name} {matched_openid}"
        
        # ② 检查用户别名映射
        for alias_rule in self.user_aliases:
            if alias_rule['name'] == name or name in alias_rule.get('alias', []):
                print(f"[FeishuMention] 别名匹配：{name} → {alias_rule['name']}")
                # 用真实姓名再查一次
                return await self.resolve_mention(f"@{alias_rule['name']}", app_id, chat_id)
        
        # ③ 查本地缓存的成员列表
        members = self.get_cached_members(app_id, chat_id)
        
        if members:
            for member in members:
                if member.get('name') == name:
                    matched_openid = member.get('open_id')
                    break
        
        if matched_openid:
            return f"@{name} {matched_openid}"
        
        # ④ 缓存未命中，尝试实时获取（需要实现）
        # TODO: 实现 fetch_members_from_api
        
        # ⑤ 仍未匹配，返回原样
        return mention
    
    def resolve_text_mentions(self, text: str, app_id: str, chat_id: str) -> str:
        """批量解析文本中的所有@提及"""
        # 匹配所有 @开头的内容
        pattern = r'(?<!:)(@[^\s:,。\!?；:\'".,!?;]+)(?![^\w])'
        
        matches = list(re.finditer(pattern, text))
        
        if not matches:
            return text
        
        # 按反向顺序替换
        result = text
        for match in reversed(matches):
            full_match = match.group(0)
            
            # 跳过已经是 openid 格式的提及
            if re.match(r'^@.*?:ou_', full_match):
                continue
            
            resolved = asyncio.run(self.resolve_mention(full_match, app_id, chat_id))
            result = result[:match.start()] + resolved + result[match.end():]
        
        return result
    
    def invalidate_cache(self, app_id: str, chat_id: str):
        """使指定 bot+ 群的缓存失效"""
        cache_file = self._get_cache_file(app_id, chat_id)
        
        if cache_file.exists():
            cache_file.unlink()
            print(f"[FeishuMention] 已清除缓存：{cache_file}")
        
        # 同时清除内存缓存
        cache_key = (app_id, chat_id)
        if cache_key in self.memory_cache:
            del self.memory_cache[cache_key]
    
    def clear_all_cache(self):
        """清除所有缓存"""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
        
        self.memory_cache.clear()
        print(f"[FeishuMention] 已清除所有缓存")


# ========== 便捷函数 ==========

def resolve(text: str, app_id: str, chat_id: str, options: Optional[Dict] = None) -> str:
    """便捷函数：直接解析文本"""
    resolver = FeishuMentionResolver(None, options)
    return resolver.resolve_text_mentions(text, app_id, chat_id)


def add_bot_mapping(at_name: str, open_id: str):
    """添加机器人映射"""
    global _global_resolver
    _global_resolver.bot_mappings[at_name] = open_id
    print(f"[FeishuMention] 添加机器人映射：{at_name} → {open_id}")


def add_user_alias(real_name: str, aliases: List[str]):
    """添加用户别名"""
    global _global_resolver
    _global_resolver.user_aliases.append({
        'name': real_name,
        'alias': aliases
    })
    print(f"[FeishuMention] 添加别名规则：{real_name} ← {aliases}")


# 全局实例
_global_resolver = FeishuMentionResolver()


if __name__ == "__main__":
    """测试脚本"""
    resolver = FeishuMentionResolver(options={
        'botMappings': {
            '@技术助手': 'rs_tech_001',
            '@数据查询': 'rs_data_001'
        },
        'aliases': [
            {'name': '张三', 'alias': ['小王', '老张']}
        ]
    })
    
    # 示例用法
    test_text = "你好 @技术助手，请问 @小王 在吗？@王五 记得回复一下。"
    app_id = "cliab1234567890abcdef"  # 替换为你的 App ID
    chat_id = "oc_1234567890abcdef"   # 替换为你的 Chat ID
    
    print(f"原文：{test_text}")
    print(f"解析后：{resolver.resolve_text_mentions(test_text, app_id, chat_id)}")
