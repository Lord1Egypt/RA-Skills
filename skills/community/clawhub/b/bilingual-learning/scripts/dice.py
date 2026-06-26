#!/usr/bin/env python3
"""
随机生成器（筛子）
用于考试选题、难度调整等随机场景
"""

import random

class Dice:
    """筛子类 - 生成随机数或进行随机选择"""
    
    def __init__(self, sides: int = 6, seed: int = None):
        self.sides = sides
        if seed is not None:
            random.seed(seed)
    
    def roll(self) -> int:
        """掷筛子"""
        return random.randint(1, self.sides)
    
    @staticmethod
    def choose(probabilities: dict) -> str:
        """
        按概率选择
        probabilities: {"选项1": 0.3, "选项2": 0.5, "选项3": 0.2}
        """
        r = random.random()
        cumulative = 0
        for option, prob in probabilities.items():
            cumulative += prob
            if r <= cumulative:
                return option
        return list(probabilities.keys())[-1]
    
    @staticmethod
    def pick(items: list, count: int = 1):
        """从列表中随机抽取"""
        if count >= len(items):
            return items
        return random.sample(items, count)

def demo():
    print("=== 筛子演示 ===")
    d = Dice(6)
    print(f"掷D6: {d.roll()}")
    
    print("\n=== 概率选择演示 ===")
    choice = Dice.choose({"rare": 0.3, "medium": 0.5, "dense": 0.2})
    print(f"难度选择结果: {choice}")
    
    print("\n=== 随机抽取演示 ===")
    items = ["apple", "banana", "cherry", "date", "elderberry"]
    picked = Dice.pick(items, 3)
    print(f"从 {items} 中抽取3个: {picked}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        d = Dice(6)
        print(d.roll())
