"""
AI决策引擎
"""

from typing import List, Tuple, Optional
from cards import Card, HandType, CardPattern, can_beat, format_cards
from game import GameState
import random

class DDZAI:
    """斗地主AI"""
    
    def __init__(self, game: GameState):
        self.game = game
    
    def suggest_play(self) -> Tuple[List[int], str]:
        """
        推荐出牌
        返回: (推荐的牌, 理由)
        """
        if self.game.current_player != 'me':
            return [], "还没轮到我"
        
        # 获取上一个有效出牌
        last_pos, last_cards, last_type, last_main = self._get_last_play()
        
        # 如果是我先出
        if last_pos == 'me' or not last_cards:
            return self._suggest_first_play()
        
        # 否则要打过上家
        return self._suggest_beat_play(last_cards, last_type, last_main)
    
    def _get_last_play(self) -> Tuple[str, List[int], HandType, int]:
        """获取上一个有效出牌"""
        if self.game.current_round:
            return self.game.current_round.get_last_play()
        # 上一轮
        if self.game.rounds:
            last_round = self.game.rounds[-1]
            return last_round.get_last_play()
        return '', [], HandType.PASS, 0
    
    def _suggest_first_play(self) -> Tuple[List[int], str]:
        """推荐先出"""
        cards = self.game.my_cards
        if not cards:
            return [], "没有牌了"
        
        # 策略优先级：
        # 1. 出单牌（小的先出）
        # 2. 出对子
        # 3. 出顺子
        # 4. 保留炸弹和王炸
        
        from collections import Counter
        counter = Counter(cards)
        
        # 找最小的单牌
        min_single = min(cards)
        
        # 找对子
        pairs = [c for c, cnt in counter.items() if cnt >= 2]
        
        # 找顺子
        straights = self._find_straights(cards)
        
        # 如果只剩一手牌，直接出
        if len(cards) <= 5:
            # 检查是否是完整牌型
            hand_type, _, _ = CardPattern.analyze(cards)
            if hand_type != HandType.PASS:
                return cards, f"最后一手: {format_cards(cards)}"
        
        # 优先出单牌（最小的）
        if min_single < 12:  # 小于Q
            return [min_single], f"出小单: {format_cards([min_single])}"
        
        # 出对子
        if pairs:
            min_pair = min(pairs)
            return [min_pair, min_pair], f"出对子: {format_cards([min_pair, min_pair])}"
        
        # 出顺子
        if straights:
            straight = straights[0]
            return straight, f"出顺子: {format_cards(straight)}"
        
        # 只能出大牌了
        return [min_single], f"出单牌: {format_cards([min_single])}"
    
    def _suggest_beat_play(self, last_cards: List[int], last_type: HandType, last_main: int) -> Tuple[List[int], str]:
        """推荐打过上家"""
        cards = self.game.my_cards
        
        # 获取所有能打的组合
        playable = self.game.get_playable_cards(last_cards, last_type, last_main)
        
        if not playable:
            return [], "pass"
        
        # 去掉pass
        playable = [p for p in playable if p]
        
        if not playable:
            return [], "pass"
        
        # 策略：
        # 1. 如果对手牌少，用大牌压
        # 2. 否则用最小的能打过的牌
        # 3. 考虑是否用炸弹
        
        # 分析对手剩余牌数
        left_count = self.game.players['left'].cards_count
        right_count = self.game.players['right'].cards_count
        min_opponent = min(left_count, right_count)
        
        # 对手牌少时要压制
        if min_opponent <= 3:
            # 找最大的
            playable.sort(key=len, reverse=True)
            best = playable[0]
            return best, f"对手牌少，压制: {format_cards(best)}"
        
        # 正常情况出最小的
        playable.sort(key=lambda x: (len(x), max(x) if x else 0))
        
        # 避免拆炸弹
        non_bomb = [p for p in playable if len(p) != 4 and not (len(p) == 2 and Card.JOKER_S in p)]
        
        if non_bomb:
            choice = non_bomb[0]
            return choice, f"出牌: {format_cards(choice)}"
        
        # 只能用炸弹了
        choice = playable[0]
        hand_type, _, _ = CardPattern.analyze(choice)
        if hand_type == HandType.BOMB:
            return choice, f"用炸弹: {format_cards(choice)}"
        elif hand_type == HandType.ROCKET:
            return choice, f"用王炸: {format_cards(choice)}"
        
        return choice, f"出牌: {format_cards(choice)}"
    
    def _find_straights(self, cards: List[int]) -> List[List[int]]:
        """找顺子"""
        from collections import Counter
        counter = Counter(cards)
        straights = []
        
        sorted_cards = sorted(set(cards))
        
        for i in range(len(sorted_cards) - 4):
            # 至少5张
            seq = []
            for j in range(i, min(i + 12, len(sorted_cards))):
                card = sorted_cards[j]
                if card >= 15:  # 不含2和王
                    break
                if counter[card] >= 1:
                    seq.append(card)
                else:
                    break
            
            if len(seq) >= 5:
                straights.append(seq[:5])  # 最小5张
        
        return straights
    
    def analyze_hand(self) -> str:
        """分析手牌情况"""
        cards = self.game.my_cards
        if not cards:
            return "没有牌了"
        
        from collections import Counter
        counter = Counter(cards)
        
        analysis = []
        
        # 统计
        singles = sum(1 for c in counter.values() if c == 1)
        pairs = sum(1 for c in counter.values() if c == 2)
        triples = sum(1 for c in counter.values() if c == 3)
        bombs = sum(1 for c in counter.values() if c == 4)
        
        analysis.append(f"单牌: {singles}张")
        analysis.append(f"对子: {pairs}对")
        analysis.append(f"三张: {triples}组")
        analysis.append(f"炸弹: {bombs}个")
        
        # 王炸
        if Card.JOKER_S in cards and Card.JOKER_B in cards:
            analysis.append("有王炸")
        
        # 大牌
        big_cards = [c for c in cards if c >= 14]
        analysis.append(f"大牌(A及以上): {len(big_cards)}张")
        
        return " | ".join(analysis)
    
    def predict_opponent(self, position: str) -> str:
        """预测对手牌型"""
        player = self.game.players[position]
        
        if player.cards_count == 0:
            return "已出完"
        
        # 基于出牌历史推测
        history = player.played_history
        
        if not history:
            return f"剩余{player.cards_count}张，未知"
        
        # 分析最近的出牌
        recent = history[-3:] if len(history) >= 3 else history
        
        # 检查是否出过炸弹
        has_bomb = any(len(h['cards']) >= 4 for h in history)
        
        # 检查是否出过大牌
        big_cards = []
        for h in history:
            for c in h['cards']:
                if c >= 14:
                    big_cards.append(c)
        
        prediction = f"剩余{player.cards_count}张"
        
        if not has_bomb:
            prediction += "，可能有炸弹"
        
        if len(big_cards) < 2:
            prediction += "，可能有大牌"
        
        return prediction


if __name__ == "__main__":
    # 测试
    from game import GameState
    
    game = GameState()
    game.set_my_cards([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 3, 3])
    game.set_landlord('me')
    game.current_player = 'me'
    
    ai = DDZAI(game)
    
    print("手牌分析:", ai.analyze_hand())
    print()
    
    cards, reason = ai.suggest_play()
    print(f"推荐: {format_cards(cards)}")
    print(f"理由: {reason}")
