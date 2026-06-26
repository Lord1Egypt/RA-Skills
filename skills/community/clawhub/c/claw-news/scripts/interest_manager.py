"""
Claw-News Interest Manager
兴趣列表管理模块
"""

import uuid
import json
import argparse
from datetime import datetime
from typing import List, Optional, Dict
from config import Config, Interest


class InterestManager:
    """关注列表管理器"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self._data = self.config.load_interests()
    
    @property
    def interests(self) -> List[Interest]:
        """获取所有关注项"""
        return [Interest.from_dict(i) for i in self._data.get("interests", [])]
    
    def get_by_id(self, interest_id: str) -> Optional[Interest]:
        """通过 ID 获取关注项"""
        for item in self.interests:
            if item.id == interest_id:
                return item
        return None
    
    def add(self, value: str, interest_type: str = "topic", 
            keywords: List[str] = None, priority: str = "medium") -> Interest:
        """添加新关注项"""
        # 检查是否已存在
        for existing in self.interests:
            if existing.value == value:
                print(f"⚠️ 关注项 '{value}' 已存在 (ID: {existing.id})")
                return existing
        
        # 生成关键词（如果没有提供）
        if keywords is None or len(keywords) == 0:
            keywords = [value]
            if interest_type == "person":
                # 为人名添加英文名变体
                keywords.extend(self._generate_person_keywords(value))
        
        new_interest = Interest(
            id=str(uuid.uuid4())[:8],
            type=interest_type,
            value=value,
            keywords=keywords,
            priority=priority,
            created_at=datetime.now().isoformat()
        )
        
        self._data["interests"].append(new_interest.to_dict())
        self._data["updated_at"] = datetime.now().isoformat()
        self.config.save_interests(self._data)
        
        print(f"✅ 已添加关注: {value} (ID: {new_interest.id})")
        return new_interest
    
    def remove(self, interest_id: str) -> bool:
        """删除关注项"""
        original_count = len(self._data["interests"])
        self._data["interests"] = [
            i for i in self._data["interests"] 
            if i.get("id") != interest_id
        ]
        
        if len(self._data["interests"]) < original_count:
            self._data["updated_at"] = datetime.now().isoformat()
            self.config.save_interests(self._data)
            print(f"✅ 已删除关注项 (ID: {interest_id})")
            return True
        else:
            print(f"⚠️ 未找到关注项 (ID: {interest_id})")
            return False
    
    def update(self, interest_id: str, **kwargs) -> Optional[Interest]:
        """更新关注项"""
        for i, item in enumerate(self._data["interests"]):
            if item.get("id") == interest_id:
                for key, value in kwargs.items():
                    if key in item:
                        item[key] = value
                item["updated_at"] = datetime.now().isoformat()
                self._data["updated_at"] = datetime.now().isoformat()
                self.config.save_interests(self._data)
                print(f"✅ 已更新关注项 (ID: {interest_id})")
                return Interest.from_dict(item)
        
        print(f"⚠️ 未找到关注项 (ID: {interest_id})")
        return None
    
    def list_all(self, interest_type: str = None) -> List[Interest]:
        """列出所有关注项"""
        interests = self.interests
        if interest_type:
            interests = [i for i in interests if i.type == interest_type]
        return interests
    
    def get_search_queries(self) -> List[Dict]:
        """获取用于搜索的查询列表"""
        queries = []
        for interest in self.interests:
            # 主查询词
            queries.append({
                "id": interest.id,
                "type": interest.type,
                "value": interest.value,
                "priority": interest.priority,
                "query": interest.value
            })
            # 关键词查询（对于高优先级）
            if interest.priority == "high" and len(interest.keywords) > 1:
                for kw in interest.keywords[1:3]:  # 最多额外 2 个关键词
                    queries.append({
                        "id": interest.id,
                        "type": interest.type,
                        "value": interest.value,
                        "priority": interest.priority,
                        "query": kw
                    })
        return queries
    
    def _generate_person_keywords(self, name: str) -> List[str]:
        """为人名生成相关关键词"""
        # 简单规则：中文字符 > 可能是中文人名
        keywords = []
        
        # 常见英文名映射（简单示例）
        name_mapping = {
            "马斯克": ["Elon Musk", "Musk"],
            "乔布斯": ["Steve Jobs", "Jobs"],
            "贝索斯": ["Jeff Bezos", "Bezos"],
            "扎克伯格": ["Mark Zuckerberg", "Zuckerberg"],
            "奥特曼": ["Sam Altman", "Altman"],
            "盖茨": ["Bill Gates", "Gates"],
        }
        
        if name in name_mapping:
            keywords.extend(name_mapping[name])
        
        return keywords
    
    def print_list(self, interest_type: str = None):
        """打印关注列表"""
        interests = self.list_all(interest_type)
        
        if not interests:
            print("📭 关注列表为空")
            return
        
        print(f"\n📋 关注列表 ({len(interests)} 项):\n")
        print(f"{'ID':<10} {'类型':<10} {'优先级':<8} {'关注内容':<20} {'关键词'}")
        print("-" * 70)
        
        for i in interests:
            type_emoji = {"topic": "📁", "person": "👤", "keyword": "🔑"}.get(i.type, "📌")
            keywords_str = ", ".join(i.keywords[:3])
            if len(i.keywords) > 3:
                keywords_str += " ..."
            print(f"{i.id:<10} {type_emoji} {i.type:<8} {'🔴' if i.priority=='high' else '🟡' if i.priority=='medium' else '🟢'} {i.priority:<6} {i.value:<18} {keywords_str}")
        
        print()


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="Claw-News Interest Manager")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有关注项")
    parser.add_argument("--add", "-a", type=str, help="添加关注项")
    parser.add_argument("--remove", "-r", type=str, help="删除关注项 (ID)")
    parser.add_argument("--type", "-t", type=str, default="topic", 
                       choices=["topic", "person", "keyword"],
                       help="关注项类型 (默认: topic)")
    parser.add_argument("--priority", "-p", type=str, default="medium",
                       choices=["high", "medium", "low"],
                       help="优先级 (默认: medium)")
    
    args = parser.parse_args()
    
    manager = InterestManager()
    
    if args.list or (not args.add and not args.remove):
        manager.print_list()
    
    if args.add:
        manager.add(args.add, args.type, priority=args.priority)
        manager.print_list()
    
    if args.remove:
        manager.remove(args.remove)
        manager.print_list()


if __name__ == "__main__":
    main()
