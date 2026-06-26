"""
斗地主牌的定义和管理
"""

from enum import IntEnum
from typing import List, Dict, Set, Tuple
from collections import Counter

class Card(IntEnum):
    """牌的定义 (3-17)"""
    JOKER_S = 16   # 小王
    JOKER_B = 17   # 大王
    TWO = 15       # 2
    A = 14
    K = 13
    Q = 12
    J = 11
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3

# 牌名映射
CARD_NAMES = {
    3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
    8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q',
    13: 'K', 14: 'A', 15: '2', 16: '🃏', 17: '👑'
}

class CardSet:
    """牌集合管理"""
    
    def __init__(self):
        # 每种牌的数量 (共54张)
        self.cards = Counter()
        
    def add(self, card: int, count: int = 1):
        """添加牌"""
        self.cards[card] += count
        
    def remove(self, card: int, count: int = 1) -> bool:
        """移除牌，返回是否成功"""
        if self.cards[card] >= count:
            self.cards[card] -= count
            if self.cards[card] == 0:
                del self.cards[card]
            return True
        return False
    
    def count(self, card: int) -> int:
        """统计某种牌的数量"""
        return self.cards.get(card, 0)
    
    def total(self) -> int:
        """总牌数"""
        return sum(self.cards.values())
    
    def to_list(self) -> List[int]:
        """转为列表（带重复）"""
        result = []
        for card, cnt in sorted(self.cards.items(), reverse=True):
            result.extend([card] * cnt)
        return result
    
    def copy(self) -> 'CardSet':
        """复制"""
        cs = CardSet()
        cs.cards = self.cards.copy()
        return cs
    
    @staticmethod
    def full_deck() -> 'CardSet':
        """创建完整牌组"""
        cs = CardSet()
        for card in range(3, 16):  # 3-2
            cs.add(card, 4)
        cs.add(Card.JOKER_S, 1)
        cs.add(Card.JOKER_B, 1)
        return cs


class HandType(IntEnum):
    """牌型"""
    PASS = 0           # 不出
    SINGLE = 1         # 单牌
    PAIR = 2           # 对子
    TRIPLE = 3         # 三张
    TRIPLE_ONE = 4     # 三带一
    TRIPLE_TWO = 5     # 三带二
    STRAIGHT = 6       # 顺子
    STRAIGHT_PAIR = 7  # 连对
    PLANE = 8          # 飞机
    PLANE_WINGS = 9    # 飞机带翅膀
    FOUR_TWO = 10      # 四带二
    BOMB = 11          # 炸弹
    ROCKET = 12        # 王炸


class CardPattern:
    """牌型分析"""
    
    @staticmethod
    def analyze(cards: List[int]) -> Tuple[HandType, int, List[int]]:
        """
        分析牌型
        返回: (牌型, 主牌点数, 完整牌列表)
        """
        if not cards:
            return HandType.PASS, 0, []
        
        counter = Counter(cards)
        counts = sorted(counter.items(), key=lambda x: (-x[1], -x[0]))
        n = len(cards)
        
        # 王炸
        if n == 2 and Card.JOKER_S in cards and Card.JOKER_B in cards:
            return HandType.ROCKET, 17, cards
        
        # 单牌
        if n == 1:
            return HandType.SINGLE, cards[0], cards
        
        # 对子
        if n == 2 and len(counter) == 1:
            return HandType.PAIR, cards[0], cards
        
        # 三张
        if n == 3 and len(counter) == 1 and counts[0][1] == 3:
            return HandType.TRIPLE, counts[0][0], cards
        
        # 炸弹
        if n == 4 and len(counter) == 1:
            return HandType.BOMB, cards[0], cards
        
        # 三带一
        if n == 4 and counts[0][1] == 3:
            return HandType.TRIPLE_ONE, counts[0][0], cards
        
        # 三带二
        if n == 5 and counts[0][1] == 3 and counts[1][1] == 2:
            return HandType.TRIPLE_TWO, counts[0][0], cards
        
        # 四带二（单）
        if n == 6 and counts[0][1] == 4:
            return HandType.FOUR_TWO, counts[0][0], cards
        
        # 四带二（对）
        if n == 8 and counts[0][1] == 4 and counts[1][1] == 2 and counts[2][1] == 2:
            return HandType.FOUR_TWO, counts[0][0], cards
        
        # 顺子 (5张以上连续单牌，不含2和王)
        if CardPattern._is_straight(cards, counter, 1):
            return HandType.STRAIGHT, min(cards), cards
        
        # 连对 (3对以上连续对子)
        if CardPattern._is_straight(cards, counter, 2):
            return HandType.STRAIGHT_PAIR, min(counter.keys()), cards
        
        # 飞机（2组以上连续三张）
        if CardPattern._is_plane(cards, counter):
            main_cards = [c for c, cnt in counter.items() if cnt >= 3]
            return HandType.PLANE, min(main_cards), cards
        
        # 飞机带翅膀
        if CardPattern._is_plane_with_wings(cards, counter):
            main_cards = [c for c, cnt in counter.items() if cnt >= 3]
            return HandType.PLANE_WINGS, min(main_cards), cards
        
        return HandType.PASS, 0, cards
    
    @staticmethod
    def _is_straight(cards: List[int], counter: Counter, group_size: int) -> bool:
        """检查是否是顺子/连对"""
        if len(cards) < 5 * group_size:
            return False
        if len(counter) * group_size != len(cards):
            return False
        
        values = sorted(counter.keys())
        # 不能包含2和王
        if any(v >= 15 for v in values):
            return False
        
        # 检查连续性
        for i in range(1, len(values)):
            if values[i] - values[i-1] != 1:
                return False
        
        # 检查数量
        return all(counter[v] == group_size for v in values)
    
    @staticmethod
    def _is_plane(cards: List[int], counter: Counter) -> bool:
        """检查是否是飞机"""
        triples = [c for c, cnt in counter.items() if cnt >= 3]
        if len(triples) < 2:
            return False
        
        triples.sort()
        # 检查连续性
        for i in range(1, len(triples)):
            if triples[i] - triples[i-1] != 1:
                return False
        
        # 不能包含2
        if any(t >= 15 for t in triples):
            return False
        
        return len(cards) == len(triples) * 3
    
    @staticmethod
    def _is_plane_with_wings(cards: List[int], counter: Counter) -> bool:
        """检查是否是飞机带翅膀"""
        triples = [c for c, cnt in counter.items() if cnt >= 3]
        if len(triples) < 2:
            return False
        
        triples.sort()
        for i in range(1, len(triples)):
            if triples[i] - triples[i-1] != 1:
                return False
        
        if any(t >= 15 for t in triples):
            return False
        
        plane_count = len(triples)
        expected_wings = plane_count * 1  # 每组三张带1张
        
        return len(cards) == plane_count * 3 + expected_wings or \
               len(cards) == plane_count * 3 + plane_count * 2  # 带单或带对


def can_beat(my_cards: List[int], last_cards: List[int], last_type: HandType, last_main: int) -> bool:
    """判断是否能打过上家"""
    if not last_cards:
        return True
    
    my_type, my_main, _ = CardPattern.analyze(my_cards)
    
    # 王炸最大
    if my_type == HandType.ROCKET:
        return True
    
    # 炸弹可以打非炸弹
    if my_type == HandType.BOMB:
        if last_type == HandType.ROCKET:
            return False
        if last_type == HandType.BOMB:
            return my_main > last_main
        return True
    
    # 同类型比大小
    if my_type == last_type and len(my_cards) == len(last_cards):
        return my_main > last_main
    
    return False


def format_cards(cards: List[int]) -> str:
    """格式化显示牌"""
    if not cards:
        return "pass"
    return ' '.join(CARD_NAMES.get(c, str(c)) for c in sorted(cards, reverse=True))
