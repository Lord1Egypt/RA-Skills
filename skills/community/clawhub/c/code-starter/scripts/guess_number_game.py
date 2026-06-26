#!/usr/bin/env python3
"""
猜数字游戏 - 完整版
适合教学演示和学生参考
"""

import random

def guess_number_game():
    """猜数字游戏主函数"""
    
    # 欢迎信息
    print("=" * 40)
    print("🎮 猜数字游戏")
    print("=" * 40)
    print("我想了一个1到100的数字，你能猜中吗？")
    print()
    
    # 游戏设置
    number = random.randint(1, 100)
    max_attempts = 10
    attempts = 0
    
    # 游戏循环
    while attempts < max_attempts:
        # 获取玩家输入
        try:
            guess = int(input(f"第{attempts + 1}次尝试，你猜几？"))
        except ValueError:
            print("⚠️  请输入一个数字！")
            continue
        
        attempts += 1
        
        # 判断结果
        if guess == number:
            print(f"🎉 恭喜你！{attempts}次猜中了！")
            if attempts <= 3:
                print("太厉害了！你是猜数字天才！")
            elif attempts <= 7:
                print("表现不错！")
            else:
                print("终于猜对了！")
            break
        elif guess > number:
            print(f"📈 大了！还有{max_attempts - attempts}次机会")
        else:
            print(f"📉 小了！还有{max_attempts - attempts}次机会")
        
        # 检查是否用完机会
        if attempts >= max_attempts:
            print(f"😢 机会用完了！答案是 {number}")
    
    # 询问是否再玩
    play_again = input("\n再玩一次？(y/n): ")
    if play_again.lower() == 'y':
        print()
        guess_number_game()
    else:
        print("👋 再见！")

if __name__ == "__main__":
    guess_number_game()
