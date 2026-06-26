"""
游戏状态管理
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from cards import Card, CardSet, HandType, CardPattern, format_cards, can_beat
import time

@dataclass
class Player:
    """玩家"""
    position: str  # 'left', 'right', 'me'
    is_landlord: bool = False
    cards_count: int = 17  # 剩余牌数
    played_history: List[dict] = field(default_factory=list)  # 出牌历史
    
    def play(self, cards: List[int]):
        """出牌"""
        self.played_history.append({
            'cards': cards,
            'time': time.time()
        })
        if cards:
            self.cards_count -= len(cards)


@dataclass
class Round:
    """一轮出牌"""
    starter: str  # 谁开始的
    plays: Dict[str, List[int]] = field(default_factory=dict)  # 各家出的牌
    winner: Optional[str] = None  # 这一轮谁赢了
    
    def is_complete(self) -> bool:
        """这轮是否结束"""
        if len(self.plays) < 3:
            return False
        # 两个人pass后结束
        passes = sum(1 for cards in self.plays.values() if not cards)
        return passes >= 2
    
    def get_last_play(self) -> tuple:
        """获取最后一个有效出牌"""
        for pos in ['right', 'me', 'left']:  # 逆序
            if pos in self.plays and self.plays[pos]:
                cards = self.plays[pos]
                hand_type, main, _ = CardPattern.analyze(cards)
                return pos, cards, hand_type, main
        return None, [], HandType.PASS, 0


class GameState:
    """游戏状态"""
    
    def __init__(self):
        self.players = {
            'me': Player('me'),
            'left': Player('left'),
            'right': Player('right')
        }
        
        # 完整牌组
        self.full_deck = CardSet.full_deck()
        
        # 我的牌
        self.my_cards: List[int] = []
        
        # 已出的牌（用于推算剩余牌）
        self.played_cards = CardSet()
        
        # 当前回合
        self.current_round: Optional[Round] = None
        self.rounds: List[Round] = []
        
        # 当前轮到谁
        self.current_player: str = 'me'
        
        # 游戏结束
        self.game_over = False
        self.winner = None
        
    def reset(self):
        """重置游戏"""
        for player in self.players.values():
            player.is_landlord = False
            player.cards_count = 17
            player.played_history.clear()
        
        self.my_cards = []
        self.played_cards = CardSet()
        self.current_round = None
        self.rounds.clear()
        self.current_player = 'me'
        self.game_over = False
        self.winner = None
    
    def set_landlord(self, position: str):
        """设置地主"""
        self.players[position].is_landlord = True
        self.players[position].cards_count = 20  # 地主多3张
        
        # 如果是我，更新我的牌
        if position == 'me':
            pass  # 牌会在set_my_cards中设置
    
    def set_my_cards(self, cards: List[int]):
        """设置我的手牌"""
        self.my_cards = sorted(cards, reverse=True)
        
        # 从完整牌组移除我的牌
        for card in cards:
            self.full_deck.remove(card)
    
    def start_round(self, starter: str):
        """开始新一轮"""
        if self.current_round and not self.current_round.is_complete():
            # 上一轮未完成，先结束
            self.rounds.append(self.current_round)
        
        self.current_round = Round(starter=starter)
        self.current_player = starter
    
    def play_cards(self, position: str, cards: List[int]):
        """玩家出牌"""
        if not self.current_round:
            self.start_round(position)
        
        # 记录出牌
        self.current_round.plays[position] = cards
        self.players[position].play(cards)
        
        # 记录到已出牌
        for card in cards:
            self.played_cards.add(card)
        
        # 如果是我的牌，更新我的手牌
        if position == 'me':
            for card in cards:
                if card in self.my_cards:
                    self.my_cards.remove(card)
        
        # 检查是否有人出完
        if self.players[position].cards_count == 0:
            self.game_over = True
            self.winner = position
            return
        
        # 检查回合是否结束
        if self.current_round.is_complete():
            # 找出赢家（最后一个出牌的）
            for pos in ['left', 'right', 'me']:
                if pos in self.current_round.plays and self.current_round.plays[pos]:
                    self.current_round.winner = pos
                    break
            self.rounds.append(self.current_round)
            self.current_round = None
            self.start_round(self.current_round.winner if self.current_round else position)
        
        # 下一个玩家
        self._next_player()
    
    def _next_player(self):
        """下一个玩家"""
        order = ['left', 'me', 'right']
        idx = order.index(self.current_player)
        self.current_player = order[(idx + 1) % 3]
    
    def get_remaining_cards(self) -> CardSet:
        """获取未出的牌"""
        remaining = CardSet()
        for card in range(3, 18):
            remaining.add(card, self.full_deck.count(card) - self.played_cards.count(card))
        return remaining
    
    def guess_opponent_cards(self, position: str) -> List[int]:
        """
        推测对手的牌
        基于已出的牌和我的牌
        """
        remaining = self.get_remaining_cards()
        
        # 移除我的牌
        for card in self.my_cards:
            remaining.remove(card)
        
        # 简单策略：随机返回剩余牌（实际应该更智能）
        return remaining.to_list()[:self.players[position].cards_count]
    
    def get_playable_cards(self, last_cards: List[int], last_type: HandType, last_main: int) -> List[List[int]]:
        """
        获取可以出的牌组合
        """
        if not last_cards:  # 我先出
            return self._get_all_combinations()
        
        playable = []
        
        # 找能打过的牌
        all_combos = self._get_all_combinations()
        for combo in all_combos:
            if can_beat(combo, last_cards, last_type, last_main):
                playable.append(combo)
        
        # 加上pass
        playable.append([])
        
        return playable
    
    def _get_all_combinations(self) -> List[List[int]]:
        """获取所有可能的出牌组合"""
        combos = []
        cards = self.my_cards.copy()
        
        if not cards:
            return combos
        
        # 单牌
        for card in set(cards):
            combos.append([card])
        
        # 对子
        from collections import Counter
        counter = Counter(cards)
        for card, cnt in counter.items():
            if cnt >= 2:
                combos.append([card, card])
        
        # 三张
        for card, cnt in counter.items():
            if cnt >= 3:
                combos.append([card, card, card])
        
        # 炸弹
        for card, cnt in counter.items():
            if cnt == 4:
                combos.append([card, card, card, card])
        
        # 王炸
        if Card.JOKER_S in cards and Card.JOKER_B in cards:
            combos.append([Card.JOKER_S, Card.JOKER_B])
        
        # 三带一
        for card, cnt in counter.items():
            if cnt >= 3:
                for other in counter.keys():
                    if other != card:
                        combos.append([card, card, card, other])
        
        # 三带二
        for card, cnt in counter.items():
            if cnt >= 3:
                for other, other_cnt in counter.items():
                    if other != card and other_cnt >= 2:
                        combos.append([card, card, card, other, other])
        
        # 顺子（简化版）
        sorted_cards = sorted(set(cards))
        for i in range(len(sorted_cards) - 4):
            seq = sorted_cards[i:i+5]
            if seq[-1] < 15 and all(counter.get(c, 0) >= 1 for c in seq):
                combo = []
                for c in seq:
                    combo.append(c)
                combos.append(combo)
        
        return combos
    
    def print_status(self):
        """打印当前状态"""
        print("\n" + "="*50)
        print(f"当前轮到: {self.current_player}")
        print(f"我的牌 ({len(self.my_cards)}): {format_cards(self.my_cards)}")
        
        for pos, player in self.players.items():
            landlord_mark = " [地主]" if player.is_landlord else ""
            print(f"{pos}: {player.cards_count}张{landlord_mark}")
        
        if self.current_round:
            print("\n本轮出牌:")
            for pos, cards in self.current_round.plays.items():
                print(f"  {pos}: {format_cards(cards)}")
        
        print("\n已出的牌:", format_cards(self.played_cards.to_list()))
        print("="*50)


if __name__ == "__main__":
    # 测试
    game = GameState()
    game.set_my_cards([3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
    game.set_landlord('me')
    
    game.print_status()
    
    # 模拟出牌
    game.start_round('me')
    game.play_cards('me', [3])
    game.play_cards('left', [4])
    game.play_cards('right', [5])
    
    game.print_status()
