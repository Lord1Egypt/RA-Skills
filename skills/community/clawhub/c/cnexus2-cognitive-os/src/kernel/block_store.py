"""Block store — append-only. Mirrors core_essence/04_data_model_essence.md §2."""
from typing import List, Dict, Any

class BlockStore:
    def __init__(self):
        self.blocks: List[Dict[str, Any]] = []

    @property
    def count(self) -> int:
        return len(self.blocks)

    def add(self, block: Dict[str, Any]) -> bool:
        self.blocks.append(block)
        return True

    def get_persona(self):
        return [b for b in self.blocks if b.get("label") == "persona"]

    def get_emotion(self):
        return [b for b in self.blocks if b.get("label") == "emotion"]

    def replace_emotion(self, block):
        self.blocks = [b for b in self.blocks if b.get("label") != "emotion"]
        self.blocks.append(block)
        return True
