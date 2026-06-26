"""
OpenClaw 调用接口
让 AI 助手可以直接调用斗地主功能
"""

import sys
import os
import json
from typing import List, Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cards import format_cards, CardPattern, HandType
from game import GameState
from ai import DDZAI
from screen import GameScreenScanner

class DDZAPI:
    """斗地主API接口"""
    
    def __init__(self):
        self.game = GameState()
        self.ai = DDZAI(self.game)
        self.scanner = GameScreenScanner()
    
    def scan(self) -> Dict:
        """扫描屏幕"""
        state = self.scanner.scan()
        return {
            'my_cards': state['my_cards'],
            'left_count': state['left_cards_count'],
            'right_count': state['right_cards_count'],
            'landlord': state['landlord']
        }
    
    def set_my_cards(self, cards: List[int]) -> Dict:
        """设置我的牌"""
        self.game.set_my_cards(cards)
        return {'status': 'ok', 'cards': format_cards(cards)}
    
    def set_landlord(self, position: str) -> Dict:
        """设置地主"""
        if position not in ['me', 'left', 'right']:
            return {'status': 'error', 'message': 'invalid position'}
        self.game.set_landlord(position)
        return {'status': 'ok', 'landlord': position}
    
    def suggest(self) -> Dict:
        """推荐出牌"""
        cards, reason = self.ai.suggest_play()
        analysis = self.ai.analyze_hand()
        
        return {
            'recommend': cards,
            'recommend_str': format_cards(cards),
            'reason': reason,
            'analysis': analysis,
            'current_player': self.game.current_player
        }
    
    def play(self, cards: List[int]) -> Dict:
        """出牌"""
        if self.game.current_player != 'me':
            return {'status': 'error', 'message': 'not my turn'}
        
        self.game.play_cards('me', cards)
        return {
            'status': 'ok',
            'played': format_cards(cards),
            'remaining': len(self.game.my_cards)
        }
    
    def reset(self) -> Dict:
        """重置"""
        self.game.reset()
        return {'status': 'ok'}
    
    def status(self) -> Dict:
        """当前状态"""
        return {
            'my_cards': format_cards(self.game.my_cards),
            'my_count': len(self.game.my_cards),
            'left_count': self.game.players['left'].cards_count,
            'right_count': self.game.players['right'].cards_count,
            'current_player': self.game.current_player,
            'landlord': {pos: p.is_landlord for pos, p in self.game.players.items()}
        }


# 命令行接口
def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ddzaishot API')
    parser.add_argument('action', choices=['scan', 'suggest', 'status', 'reset', 'demo'])
    parser.add_argument('--cards', type=str, help='我的牌 (如: 3,4,5,6,7)')
    parser.add_argument('--landlord', type=str, help='地主位置')
    
    args = parser.parse_args()
    
    api = DDZAPI()
    
    if args.action == 'demo':
        # 演示模式
        import random
        cards = list(range(3, 16)) * 4 + [16, 17]
        random.shuffle(cards)
        my_cards = sorted(cards[:17], reverse=True)
        
        api.set_my_cards(my_cards)
        api.set_landlord('me')
        
        result = api.suggest()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'scan':
        result = api.scan()
        print(json.dumps(result, ensure_ascii=False))
    
    elif args.action == 'suggest':
        if args.cards:
            cards = [int(x) for x in args.cards.split(',')]
            api.set_my_cards(cards)
        if args.landlord:
            api.set_landlord(args.landlord)
        
        result = api.suggest()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'status':
        result = api.status()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'reset':
        result = api.reset()
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
