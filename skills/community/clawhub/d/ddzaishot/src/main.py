#!/usr/bin/env python3
"""
ddzaishot - 斗地主AI助手主程序
"""

import sys
import os
import time
import threading
from typing import Optional

# 添加src到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cards import format_cards, CardPattern, HandType
from game import GameState
from screen import GameScreenScanner
from ai import DDZAI
from mouse import MouseController, AutoPlayer

class DDZAssistant:
    """斗地主助手"""
    
    def __init__(self):
        self.game = GameState()
        self.scanner = GameScreenScanner()
        self.ai = DDZAI(self.game)
        self.mouse = MouseController()
        self.auto_player = AutoPlayer(self.mouse)
        
        self.running = False
        self.auto_mode = False
        
    def start(self):
        """启动助手"""
        print("\n" + "="*60)
        print("  ddzaishot - 斗地主AI助手 💎")
        print("="*60)
        print("\n命令:")
        print("  s - 扫描屏幕并识别")
        print("  p - 推荐出牌")
        print("  r - 重置游戏")
        print("  m - 手动输入我的牌")
        print("  l - 设置地主")
        print("  c - 鼠标校准")
        print("  a - 切换自动模式")
        print("  h - 显示帮助")
        print("  q - 退出")
        print("\n" + "="*60 + "\n")
        
        self.running = True
        
        while self.running:
            try:
                cmd = input("> ").strip().lower()
                self.handle_command(cmd)
            except KeyboardInterrupt:
                print("\n退出...")
                break
            except Exception as e:
                print(f"错误: {e}")
    
    def handle_command(self, cmd: str):
        """处理命令"""
        if not cmd:
            return
        
        if cmd == 'q' or cmd == 'quit':
            self.running = False
            print("再见！")
        
        elif cmd == 'h' or cmd == 'help':
            self.show_help()
        
        elif cmd == 's' or cmd == 'scan':
            self.scan_screen()
        
        elif cmd == 'p' or cmd == 'play':
            self.suggest_play()
        
        elif cmd == 'r' or cmd == 'reset':
            self.reset_game()
        
        elif cmd == 'm' or cmd == 'manual':
            self.manual_input()
        
        elif cmd == 'l' or cmd == 'landlord':
            self.set_landlord()
        
        elif cmd == 'c' or cmd == 'calibrate':
            self.calibrate_mouse()
        
        elif cmd == 'a' or cmd == 'auto':
            self.toggle_auto()
        
        elif cmd == 'd' or cmd == 'demo':
            self.demo_mode()
        
        else:
            print(f"未知命令: {cmd}")
    
    def show_help(self):
        """显示帮助"""
        print("\n--- 帮助 ---")
        print("s - 扫描屏幕，识别当前牌局")
        print("p - AI推荐出牌")
        print("m - 手动输入我的牌（格式: 3 4 5 6 7...）")
        print("l - 设置地主（输入: me/left/right）")
        print("r - 重置游戏")
        print("c - 鼠标校准")
        print("a - 切换自动出牌模式")
        print("d - 演示模式（随机牌测试）")
        print("q - 退出")
        print()
    
    def scan_screen(self):
        """扫描屏幕"""
        print("\n正在扫描屏幕...")
        
        try:
            state = self.scanner.scan()
            
            print(f"\n识别结果:")
            print(f"  我的牌: {format_cards(state['my_cards'])}")
            print(f"  左边玩家: {state['left_cards_count']}张")
            print(f"  右边玩家: {state['right_cards_count']}张")
            print(f"  地主: {state['landlord']}")
            
            # 更新游戏状态
            if state['my_cards']:
                self.game.set_my_cards(state['my_cards'])
            
            # 保存截图
            self.scanner.save_screenshot("logs/last_scan.png")
            print("\n截图已保存到 logs/last_scan.png")
            
        except Exception as e:
            print(f"扫描失败: {e}")
            print("提示: 请确保游戏窗口可见")
    
    def suggest_play(self):
        """推荐出牌"""
        print("\n--- AI分析 ---")
        
        # 手牌分析
        analysis = self.ai.analyze_hand()
        print(f"手牌分析: {analysis}")
        
        # 推荐出牌
        cards, reason = self.ai.suggest_play()
        
        print(f"\n推荐出牌: {format_cards(cards)}")
        print(f"理由: {reason}")
        
        # 对手预测
        print(f"\n对手情况:")
        for pos in ['left', 'right']:
            pred = self.ai.predict_opponent(pos)
            landlord_mark = " [地主]" if self.game.players[pos].is_landlord else ""
            print(f"  {pos}: {pred}{landlord_mark}")
        
        # 如果开启自动模式
        if self.auto_mode and cards:
            print("\n自动出牌中...")
            # 需要将牌转换为索引
            # 这里简化处理
            self.auto_player.auto_play([])
    
    def reset_game(self):
        """重置游戏"""
        self.game.reset()
        print("游戏已重置")
    
    def manual_input(self):
        """手动输入牌"""
        print("\n输入我的牌（用空格分隔，如: 3 3 4 5 6 7 8）")
        print("牌值: 3-10, 11=J, 12=Q, 13=K, 14=A, 15=2, 16=小王, 17=大王")
        
        try:
            line = input("牌: ").strip()
            cards = [int(x) for x in line.split()]
            
            self.game.set_my_cards(cards)
            print(f"已设置: {format_cards(cards)}")
            
        except ValueError:
            print("输入格式错误")
    
    def set_landlord(self):
        """设置地主"""
        print("\n输入地主位置 (me/left/right):")
        pos = input("> ").strip().lower()
        
        if pos in ['me', 'left', 'right']:
            self.game.set_landlord(pos)
            print(f"地主: {pos}")
        else:
            print("无效位置")
    
    def calibrate_mouse(self):
        """鼠标校准"""
        print("\n开始鼠标校准...")
        positions = self.mouse.calibrate()
        
        # 保存配置
        print("\n建议将以下配置保存到配置文件:")
        print(f"card_positions = {positions}")
    
    def toggle_auto(self):
        """切换自动模式"""
        self.auto_mode = not self.auto_mode
        self.auto_player.enabled = self.auto_mode
        
        status = "开启" if self.auto_mode else "关闭"
        print(f"自动模式: {status}")
    
    def demo_mode(self):
        """演示模式"""
        print("\n--- 演示模式 ---")
        
        # 随机发牌
        import random
        
        all_cards = []
        for card in range(3, 16):  # 3-2
            all_cards.extend([card] * 4)
        all_cards.extend([16, 17])  # 大小王
        
        random.shuffle(all_cards)
        
        # 我拿17张
        my_cards = sorted(all_cards[:17], reverse=True)
        
        self.game.set_my_cards(my_cards)
        self.game.set_landlord('me')  # 假设我是地主
        self.game.players['me'].cards_count = 20  # 地主20张
        
        print(f"我的牌: {format_cards(my_cards)}")
        print(f"我是地主 💰")
        
        self.game.current_player = 'me'
        
        # AI分析
        self.suggest_play()


def main():
    """主函数"""
    # 创建logs目录
    os.makedirs("logs", exist_ok=True)
    
    # 启动助手
    assistant = DDZAssistant()
    assistant.start()


if __name__ == "__main__":
    main()
