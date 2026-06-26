#!/usr/bin/env python3
"""
简单短期记忆 - 记录别的通道每分钟说了什么（支持家庭组架构）
星之君需求：简单设计，30 分钟 TTL，支持家庭组隔离和 AI 自主分享
"""
import json
from datetime import datetime, timedelta
from pathlib import Path

class ChannelActivity:
    """通道活动记录器 - 支持家庭组架构"""
    
    def __init__(self, cache_path="memory/channel-activity.json"):
        self.cache_path = cache_path
        self.ttl_minutes = 30
        self.data = self._load()
    
    def _load(self):
        """加载数据"""
        try:
            if Path(self.cache_path).exists():
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {
            "version": "3.0",
            "ttl_minutes": 30,
            "family_groups": {},  # 家庭组管理
            "identities": {}  # 向后兼容
        }
    
    def _save(self):
        """保存数据"""
        Path(self.cache_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    # ========== 家庭组管理 ==========
    
    def create_family_group(self, family_id: str, members: list = None):
        """
        创建家庭组
        
        Args:
            family_id: 家庭组 ID（例如："family_A"）
            members: 成员列表（例如：["user_A", "user_B"]）
        """
        if family_id not in self.data["family_groups"]:
            self.data["family_groups"][family_id] = {
                "members": members or [],
                "created_at": datetime.now().isoformat()
            }
            self._save()
            print(f"[家庭组] 创建 {family_id}, 成员：{members}")
    
    def add_to_family(self, family_id: str, identity: str):
        """
        添加成员到家庭组
        
        Args:
            family_id: 家庭组 ID
            identity: 用户身份标识
        """
        if family_id not in self.data["family_groups"]:
            self.create_family_group(family_id)
        
        if identity not in self.data["family_groups"][family_id]["members"]:
            self.data["family_groups"][family_id]["members"].append(identity)
            self._save()
            print(f"[家庭组] 添加 {identity} 到 {family_id}")
    
    def get_family_group(self, identity: str):
        """
        获取用户所属的家庭组
        
        Args:
            identity: 用户身份标识
        
        Returns:
            家庭组 ID 或 None
        """
        for family_id, group in self.data["family_groups"].items():
            if identity in group["members"]:
                return family_id
        return None
    
    # ========== 记录功能 ==========
    
    def record(self, identity: str, channel: str, message: str, user_id: str = None, max_length: int = 100):
        """
        记录通道活动
        
        Args:
            identity: 用户身份标识
            channel: 通道名（feishu/qq 等）
            message: 消息内容（自动提取摘要）
            user_id: 用户 ID（可选）
            max_length: 摘要最大长度（默认 100 字）
        """
        now = datetime.now()
        
        # 提取摘要（截断长消息）
        if len(message) > max_length:
            summary = message[:max_length] + "..."
        else:
            summary = message
        
        # 初始化 identity 和通道
        if identity not in self.data["identities"]:
            self.data["identities"][identity] = {}
        if channel not in self.data["identities"][identity]:
            self.data["identities"][identity][channel] = []
        
        # 添加记录（只存摘要）
        entry = {
            "time": now.isoformat(),
            "summary": summary,
            "user_id": user_id
        }
        self.data["identities"][identity][channel].append(entry)
        
        # 清理超过 30 分钟的记录
        cutoff = now - timedelta(minutes=self.ttl_minutes)
        self.data["identities"][identity][channel] = [
            e for e in self.data["identities"][identity][channel]
            if datetime.fromisoformat(e["time"]) > cutoff
        ]
        
        self._save()
        print(f"[通道活动] 记录 {identity}/{channel}: {summary}")
    
    # ========== 获取上下文（支持家庭组共享） ==========
    
    def get_context_summary(self, current_identity: str, current_channel: str = None, 
                           ai_decision: bool = True, max_chars: int = 1000):
        """
        获取上下文摘要（支持家庭组共享）
        
        Args:
            current_identity: 当前用户身份标识
            current_channel: 当前通道（排除的通道）
            ai_decision: 是否启用 AI 自主决定共享（默认 True）
            max_chars: 最大字符数
        
        Returns:
            str: 格式化的整合摘要
        """
        # 获取当前用户的家庭组
        family_id = self.get_family_group(current_identity)
        
        # 收集所有相关 identity 的活动
        all_entries = []
        
        # 1. 当前 identity 的其他通道
        if current_identity in self.data["identities"]:
            identity_data = self.data["identities"][current_identity]
            for channel, entries in identity_data.items():
                if current_channel and channel == current_channel:
                    continue
                for entry in entries:
                    if datetime.fromisoformat(entry["time"]) > datetime.now() - timedelta(minutes=30):
                        all_entries.append({
                            "identity": current_identity,
                            "channel": channel,
                            "time": entry["time"],
                            "summary": entry["summary"]
                        })
        
        # 2. 如果在家庭组内且启用 AI 自主决定，可以包含其他家庭成员的内容
        if ai_decision and family_id:
            family_members = self.data["family_groups"][family_id]["members"]
            for member_identity in family_members:
                if member_identity == current_identity:
                    continue  # 跳过自己
                
                # AI 自主决定：这里可以添加逻辑来决定是否共享
                # 简单实现：家庭组内默认共享
                if member_identity in self.data["identities"]:
                    identity_data = self.data["identities"][member_identity]
                    for channel, entries in identity_data.items():
                        for entry in entries:
                            if datetime.fromisoformat(entry["time"]) > datetime.now() - timedelta(minutes=30):
                                all_entries.append({
                                    "identity": member_identity,
                                    "channel": channel,
                                    "time": entry["time"],
                                    "summary": entry["summary"],
                                    "from_family": True  # 标记来自家庭成员
                                })
        
        if not all_entries:
            return ""
        
        # 按时间排序（最新的在前）
        all_entries.sort(key=lambda x: x["time"], reverse=True)
        
        # 智能整合摘要
        summary_groups = {}
        for entry in all_entries:
            key = f"{entry['identity']}_{entry['channel']}"
            if key not in summary_groups:
                summary_groups[key] = {
                    "identity": entry["identity"],
                    "channel": entry["channel"],
                    "count": 0,
                    "messages": [],
                    "from_family": entry.get("from_family", False)
                }
            summary_groups[key]["count"] += 1
            summary_groups[key]["messages"].append(entry["summary"])
        
        # 生成整合摘要
        lines = [f"[最近 30 分钟活动整合摘要]"]
        
        for key, data in summary_groups.items():
            identity = data["identity"]
            channel = data["channel"]
            count = data["count"]
            messages = data["messages"]
            from_family = data["from_family"]
            
            prefix = f"[家庭组] " if from_family else ""
            
            if count == 1:
                lines.append(f"- {prefix}{identity}/{channel}（1 条）：{messages[0]}")
            elif count <= 3:
                lines.append(f"- {prefix}{identity}/{channel}（{count}条）：{'; '.join(messages)}")
            else:
                first_msg = messages[0]
                last_msg = messages[-1]
                lines.append(f'- {prefix}{identity}/{channel}（{count}条）：从"{first_msg}"到"{last_msg}"等{count}条活动')
        
        result = "\n".join(lines)
        
        # 截断到最大字符数
        if len(result) > max_chars:
            result = result[:max_chars] + "...[内容已精简]"
        
        return result
    
    # ========== 更新、删除、搜索功能 ==========
    
    def update(self, identity: str, channel: str, old_summary: str, new_summary: str):
        """更新已有记忆"""
        if identity not in self.data["identities"]:
            return False
        if channel not in self.data["identities"][identity]:
            return False
        
        updated = False
        for entry in self.data["identities"][identity][channel]:
            if entry["summary"] == old_summary:
                entry["summary"] = new_summary
                updated = True
                break
        
        if updated:
            self._save()
            print(f"[通道活动] 更新 {identity}/{channel}: {old_summary[:20]}... → {new_summary[:20]}...")
        
        return updated
    
    def delete(self, identity: str, channel: str, summary: str):
        """删除特定记忆"""
        if identity not in self.data["identities"]:
            return False
        if channel not in self.data["identities"][identity]:
            return False
        
        before_count = len(self.data["identities"][identity][channel])
        self.data["identities"][identity][channel] = [
            e for e in self.data["identities"][identity][channel]
            if e["summary"] != summary
        ]
        after_count = len(self.data["identities"][identity][channel])
        
        if before_count > after_count:
            self._save()
            print(f"[通道活动] 删除 {identity}/{channel}: {summary[:50]}...")
            return True
        
        return False
    
    def search(self, identity: str, keyword: str, max_results: int = 10):
        """搜索记忆"""
        if identity not in self.data["identities"]:
            return []
        
        results = []
        keyword_lower = keyword.lower()
        
        for channel, entries in self.data["identities"][identity].items():
            for entry in entries:
                if keyword_lower in entry["summary"].lower():
                    results.append({
                        "channel": channel,
                        "time": entry["time"],
                        "summary": entry["summary"]
                    })
                    if len(results) >= max_results:
                        return results
        
        results.sort(key=lambda x: x["time"], reverse=True)
        return results
    
    def clear(self, identity: str = None):
        """清理记忆"""
        if identity:
            if identity in self.data["identities"]:
                del self.data["identities"][identity]
                self._save()
                print(f"[通道活动] 清理 {identity} 的所有记忆")
        else:
            self.data["identities"] = {}
            self._save()
            print(f"[通道活动] 清理所有记忆")

# 使用示例
if __name__ == "__main__":
    ca = ChannelActivity()
    
    # 创建家庭组
    ca.create_family_group("family_A", ["user_A", "user_B"])
    
    # 记录活动
    ca.record("user_A", "feishu", "项目 A 需要处理")
    ca.record("user_A", "qq", "下午 3 点开会")
    ca.record("user_B", "qq", "妈妈去买菜了")
    
    # 获取上下文（家庭组内共享）
    print('\\n=== user_A 在 QQ 会话中（可以看到家庭组内的内容）===')
    summary = ca.get_context_summary("user_A", current_channel="qq", ai_decision=True)
    print(summary)
    
    # 搜索
    print('\\n=== 搜索 user_A 的"项目" ===')
    results = ca.search("user_A", "项目")
    for r in results:
        print(f"[{r['channel']}] {r['summary']}")
