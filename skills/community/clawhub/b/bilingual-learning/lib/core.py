"""
双语学习 Skill 核心模块
语言方向: CN -> EN
"""

import json
import uuid
from datetime import datetime
from pathlib import Path

DataPath = Path(__file__).parent.parent / "data"

# 默认配置
DEFAULT_CONFIG = {
    "difficulty": "medium",
    "question_type": "hybrid"
}

def load_config() -> dict:
    """加载配置文件"""
    config_path = DataPath / "config.json"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(config: dict):
    """保存配置文件"""
    DataPath.mkdir(parents=True, exist_ok=True)
    config_path = DataPath / "config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

class WordLibrary:
    """词库管理基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.path = DataPath / f"{name}.json"
        self.words: list[dict] = []
        self.load()
    
    def reload(self):
        """重新从磁盘加载"""
        self.load()
    
    def load(self):
        """从文件加载词库"""
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as f:
                self.words = json.load(f)
        else:
            self.words = []
    
    def save(self):
        """保存词库到文件"""
        DataPath.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.words, f, ensure_ascii=False, indent=2)
    
    def add(self, word: str, pos: str = "", field: str = "", book: str = "default"):
        """添加单词"""
        if self.find(word):
            return False
        entry = {
            "id": str(uuid.uuid4())[:8],
            "name": word,
            "pos": pos,
            "field": field,
            "book": book,
            "added_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.words.append(entry)
        self.save()
        return True
    
    def delete(self, word_or_id: str):
        """删除单词（按名称或ID）"""
        for i, w in enumerate(self.words):
            if w["name"] == word_or_id or w["id"] == word_or_id:
                self.words.pop(i)
                self.save()
                return True
        return False
    
    def find(self, word: str):
        """查找单词"""
        for w in self.words:
            if w["name"] == word:
                return w
        return None
    
    def list_all(self):
        """列出所有单词"""
        return self.words
    
    def clear(self):
        """清空词库"""
        self.words = []
        self.save()


class NewWordLibrary(WordLibrary):
    """生词库"""
    def __init__(self):
        super().__init__("new_words")


class KnownWordLibrary(WordLibrary):
    """熟词库"""
    def __init__(self):
        super().__init__("known_words")


def transfer_word(word: str, from_lib: str, to_lib: str):
    """生熟词库传递"""
    source = NewWordLibrary() if from_lib == "new" else KnownWordLibrary()
    target = NewWordLibrary() if to_lib == "new" else KnownWordLibrary()
    
    entry = source.find(word)
    if not entry:
        return False, f"单词 '{word}' 不在 {from_lib} 词库中"
    
    if target.find(word):
        return False, f"单词 '{word}' 已在 {to_lib} 词库中"
    
    source.delete(word)
    target.reload()
    target.words.append(entry)
    target.save()
    return True, f"单词 '{word}' 已从 {from_lib} 词库转移到 {to_lib} 词库"
