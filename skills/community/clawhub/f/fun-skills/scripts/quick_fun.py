#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速娱乐脚本
包含各种小游戏和娱乐功能
"""

import random
import sys
import time

class QuickFun:
    def __init__(self):
        self.games = {
            "猜数字": self.guess_number,
            "硬币翻转": self.coin_flip,
            "石头剪刀布": self.rock_paper_scissors,
            "骰子滚动": self.dice_roll,
            "幸运数字": self.lucky_number,
            "命运预测": self.fortune_teller
        }
    
    def guess_number(self):
        """猜数字游戏"""
        print("🎯 猜数字游戏 (1-10)")
        number = random.randint(1, 10)
        
        for attempt in range(3):
            try:
                guess = int(input(f"第{attempt+1}次尝试: "))
                if guess == number:
                    print("🎉 恭喜！猜对了！")
                    return True
                elif guess < number:
                    print("📈 再高一点")
                else:
                    print("📉 再低一点")
            except ValueError:
                print("请输入1-10的数字")
        
        print(f"❌ 游戏结束！数字是 {number}")
        return False
    
    def coin_flip(self):
        """硬币翻转"""
        result = random.choice(["正面", "反面"])
        print(f"🪙 硬币在空中翻转...")
        time.sleep(1)
        print(f"🎯 结果: {result}")
        return result
    
    def rock_paper_scissors(self):
        """石头剪刀布"""
        choices = ["石头", "剪刀", "布"]
        computer = random.choice(choices)
        
        print("✊✌️✋ 石头剪刀布！")
        print("选择: 石头, 剪刀, 布")
        
        user = input("你的选择: ").strip()
        
        if user not in choices:
            print("无效选择，请重试")
            return None
        
        print(f"🤖 电脑出: {computer}")
        print(f"👤 你出: {user}")
        
        if user == computer:
            print("🤝 平局！")
            return "平局"
        elif (user == "石头" and computer == "剪刀") or \
             (user == "剪刀" and computer == "布") or \
             (user == "布" and computer == "石头"):
            print("🎉 你赢了！")
            return "赢"
        else:
            print("❌ 你输了！")
            return "输"
    
    def dice_roll(self, count=1):
        """掷骰子"""
        print(f"🎲 掷骰子...")
        time.sleep(0.5)
        
        results = []
        for i in range(count):
            roll = random.randint(1, 6)
            results.append(roll)
            print(f"骰子{i+1}: {roll}")
        
        if count > 1:
            print(f"总计: {sum(results)}")
        
        return results
    
    def lucky_number(self):
        """幸运数字生成"""
        print("🔮 生成幸运数字...")
        time.sleep(0.5)
        
        # 生成多个幸运数字
        numbers = {
            "今日幸运数字": random.randint(1, 100),
            "幸运颜色": random.choice(["红色", "蓝色", "绿色", "黄色", "紫色"]),
            "幸运方向": random.choice(["东", "南", "西", "北"]),
            "幸运短语": random.choice(["今天会是美好的一天！", "机会正在路上", "保持积极心态"])
        }
        
        for key, value in numbers.items():
            print(f"{key}: {value}")
        
        return numbers
    
    def fortune_teller(self):
        """命运预测"""
        fortunes = [
            "今天你会遇到惊喜！",
            "一个重要的机会正在等待你",
            "保持耐心，好事即将发生",
            "你的创造力今天会达到高峰",
            "有人会给你带来好消息",
            "今天适合尝试新事物",
            "你的努力很快就会得到回报",
            "保持微笑，它会传染的"
        ]
        
        print("🔮 命运预测中...")
        time.sleep(1)
        
        fortune = random.choice(fortunes)
        print(f"📜 预测: {fortune}")
        
        return fortune
    
    def list_games(self):
        """列出所有游戏"""
        print("🎮 可用的快速游戏：")
        for i, game in enumerate(self.games.keys(), 1):
            print(f"{i}. {game}")
    
    def play_game(self, game_name):
        """玩指定游戏"""
        if game_name in self.games:
            return self.games[game_name]()
        else:
            print(f"未知游戏: {game_name}")
            return None

def main():
    fun = QuickFun()
    
    if len(sys.argv) > 1:
        game_name = sys.argv[1]
        fun.play_game(game_name)
    else:
        print("🎪 快速娱乐中心")
        print("=" * 40)
        
        fun.list_games()
        print("\n选择游戏:")
        
        try:
            choice = input("输入游戏名称或编号: ").strip()
            
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(fun.games):
                    game_name = list(fun.games.keys())[choice_num - 1]
                else:
                    print("无效编号")
                    return
            else:
                game_name = choice
            
            print(f"\n🎯 开始游戏: {game_name}")
            print("-" * 40)
            fun.play_game(game_name)
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    main()