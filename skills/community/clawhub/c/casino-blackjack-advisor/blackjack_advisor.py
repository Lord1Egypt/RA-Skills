#!/usr/bin/env python3
"""
Blackjack Basic Strategy Advisor

Gives the mathematically optimal action (HIT/STAND/DOUBLE/SPLIT/SURRENDER)
for any blackjack hand using perfect basic strategy (6 decks, S17).
House edge with this strategy: 0.3%.

Usage:
  python blackjack_advisor.py                        # demo hands
  python blackjack_advisor.py "8,6" "7"              # hard 14 vs 7
  python blackjack_advisor.py "A,7" "6"              # soft 18 vs 6
  python blackjack_advisor.py "9,9" "6"              # pair 9s vs 6

Output: JSON with action, explanation, hand_type, total.

Author: Mibayy
"""
import sys, json

# Actions
HIT = "HIT"
STAND = "STAND"
DOUBLE = "DOUBLE"
SPLIT = "SPLIT"
SURRENDER = "SURRENDER"

# -------------------------------------------------------
# STRATEGIE DE BASE - 6 decks, dealer stands on soft 17
# Source: Wizard of Odds - optimal pour la plupart des casinos en ligne
# -------------------------------------------------------

# Hard hands: player_total -> {dealer_upcard: action}
HARD_STRATEGY = {
    4:  {2:HIT,3:HIT,4:HIT,5:HIT,6:HIT,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT},
    5:  {2:HIT,3:HIT,4:HIT,5:HIT,6:HIT,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT},
    6:  {2:HIT,3:HIT,4:HIT,5:HIT,6:HIT,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT},
    7:  {2:HIT,3:HIT,4:HIT,5:HIT,6:HIT,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT},
    8:  {2:HIT,3:HIT,4:HIT,5:HIT,6:HIT,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT},
    9:  {2:HIT,3:DOUBLE,4:DOUBLE,5:DOUBLE,6:DOUBLE,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT},
    10: {2:DOUBLE,3:DOUBLE,4:DOUBLE,5:DOUBLE,6:DOUBLE,7:DOUBLE,8:DOUBLE,9:DOUBLE,10:HIT,11:HIT},
    11: {2:DOUBLE,3:DOUBLE,4:DOUBLE,5:DOUBLE,6:DOUBLE,7:DOUBLE,8:DOUBLE,9:DOUBLE,10:DOUBLE,11:DOUBLE},
    12: {2:HIT,3:HIT,4:STAND,5:STAND,6:STAND,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT},
    13: {2:STAND,3:STAND,4:STAND,5:STAND,6:STAND,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT},
    14: {2:STAND,3:STAND,4:STAND,5:STAND,6:STAND,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT},
    15: {2:STAND,3:STAND,4:STAND,5:STAND,6:STAND,7:HIT,8:HIT,9:HIT,10:SURRENDER,11:HIT},
    16: {2:STAND,3:STAND,4:STAND,5:STAND,6:STAND,7:HIT,8:HIT,9:SURRENDER,10:SURRENDER,11:SURRENDER},
    17: {2:STAND,3:STAND,4:STAND,5:STAND,6:STAND,7:STAND,8:STAND,9:STAND,10:STAND,11:STAND},
    18: {2:STAND,3:STAND,4:STAND,5:STAND,6:STAND,7:STAND,8:STAND,9:STAND,10:STAND,11:STAND},
    19: {2:STAND,3:STAND,4:STAND,5:STAND,6:STAND,7:STAND,8:STAND,9:STAND,10:STAND,11:STAND},
    20: {2:STAND,3:STAND,4:STAND,5:STAND,6:STAND,7:STAND,8:STAND,9:STAND,10:STAND,11:STAND},
    21: {2:STAND,3:STAND,4:STAND,5:STAND,6:STAND,7:STAND,8:STAND,9:STAND,10:STAND,11:STAND},
}

# Soft hands (ace + card): player_second_card -> {dealer_upcard: action}
SOFT_STRATEGY = {
    2:  {2:HIT,3:HIT,4:HIT,5:DOUBLE,6:DOUBLE,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT},   # A+2
    3:  {2:HIT,3:HIT,4:HIT,5:DOUBLE,6:DOUBLE,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT},   # A+3
    4:  {2:HIT,3:HIT,4:DOUBLE,5:DOUBLE,6:DOUBLE,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT}, # A+4
    5:  {2:HIT,3:HIT,4:DOUBLE,5:DOUBLE,6:DOUBLE,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT}, # A+5
    6:  {2:HIT,3:DOUBLE,4:DOUBLE,5:DOUBLE,6:DOUBLE,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT}, # A+6
    7:  {2:STAND,3:DOUBLE,4:DOUBLE,5:DOUBLE,6:DOUBLE,7:STAND,8:STAND,9:HIT,10:HIT,11:HIT}, # A+7
    8:  {2:STAND,3:STAND,4:STAND,5:STAND,6:STAND,7:STAND,8:STAND,9:STAND,10:STAND,11:STAND}, # A+8
    9:  {2:STAND,3:STAND,4:STAND,5:STAND,6:STAND,7:STAND,8:STAND,9:STAND,10:STAND,11:STAND}, # A+9
}

# Pairs: pair_value -> {dealer_upcard: action}
PAIR_STRATEGY = {
    2:  {2:SPLIT,3:SPLIT,4:SPLIT,5:SPLIT,6:SPLIT,7:SPLIT,8:HIT,9:HIT,10:HIT,11:HIT},
    3:  {2:SPLIT,3:SPLIT,4:SPLIT,5:SPLIT,6:SPLIT,7:SPLIT,8:HIT,9:HIT,10:HIT,11:HIT},
    4:  {2:HIT,3:HIT,4:HIT,5:SPLIT,6:SPLIT,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT},
    5:  {2:DOUBLE,3:DOUBLE,4:DOUBLE,5:DOUBLE,6:DOUBLE,7:DOUBLE,8:DOUBLE,9:DOUBLE,10:HIT,11:HIT},
    6:  {2:SPLIT,3:SPLIT,4:SPLIT,5:SPLIT,6:SPLIT,7:HIT,8:HIT,9:HIT,10:HIT,11:HIT},
    7:  {2:SPLIT,3:SPLIT,4:SPLIT,5:SPLIT,6:SPLIT,7:SPLIT,8:HIT,9:HIT,10:HIT,11:HIT},
    8:  {2:SPLIT,3:SPLIT,4:SPLIT,5:SPLIT,6:SPLIT,7:SPLIT,8:SPLIT,9:SPLIT,10:SPLIT,11:SPLIT},
    9:  {2:SPLIT,3:SPLIT,4:SPLIT,5:SPLIT,6:SPLIT,7:STAND,8:SPLIT,9:SPLIT,10:STAND,11:STAND},
    10: {2:STAND,3:STAND,4:STAND,5:STAND,6:STAND,7:STAND,8:STAND,9:STAND,10:STAND,11:STAND},
    11: {2:SPLIT,3:SPLIT,4:SPLIT,5:SPLIT,6:SPLIT,7:SPLIT,8:SPLIT,9:SPLIT,10:SPLIT,11:SPLIT}, # Aces
}

# Explications pour chaque action
ACTION_EXPLAIN = {
    HIT: "Prend une carte. Ta main est trop basse.",
    STAND: "Reste. Ta main est suffisamment forte.",
    DOUBLE: "Double ta mise et prends UNE seule carte.",
    SPLIT: "Separe la paire en deux mains independantes.",
    SURRENDER: "Abandonne la main (recupere 50% de ta mise). Si pas disponible: HIT.",
}

def card_value(card: str) -> int:
    """Convertit une carte en valeur numerique."""
    card = card.upper().strip()
    if card in ['J', 'Q', 'K', '10']:
        return 10
    if card == 'A':
        return 11
    return int(card)

def dealer_value(dealer_card: str) -> int:
    """Valeur de la carte visible du dealer."""
    v = card_value(dealer_card)
    return 11 if v == 11 else v  # Ace = 11 pour dealer

def get_advice(player_cards: list[str], dealer_card: str) -> dict:
    """
    Retourne l'action optimale pour une main de blackjack.
    
    player_cards: liste de cartes ex ["8", "6"] ou ["A", "7"] ou ["9", "9"]
    dealer_card: carte visible du dealer ex "6"
    
    Returns: {action, explain, hand_type, total, confidence}
    """
    try:
        dealer = dealer_value(dealer_card)
        if dealer == 11:
            dealer = 11
        
        values = [card_value(c) for c in player_cards]
        
        # Paire?
        is_pair = len(player_cards) == 2 and values[0] == values[1]
        
        # Soft hand? (contient un As et total <= 21)
        has_ace = any(c.upper() == 'A' for c in player_cards)
        total_hard = sum(v if v != 11 else 1 for v in values)
        total_soft = sum(values)
        
        # Recalcule avec aces comme 1 si necessaire
        soft_total = total_soft
        hard_total = total_hard
        while soft_total > 21 and has_ace:
            soft_total -= 10
        
        is_soft = has_ace and soft_total != hard_total and soft_total <= 21
        is_blackjack = len(player_cards) == 2 and sorted([v for v in values]) in [[10,11],[11,10]]
        
        if is_blackjack:
            return {
                "action": "BLACKJACK",
                "explain": "Blackjack! Tu gagnes 1.5x ta mise (si casino paie 3:2).",
                "hand_type": "blackjack",
                "total": 21,
                "confidence": "parfait"
            }
        
        # Determine l'action
        action = None
        hand_type = ""
        display_total = soft_total if is_soft else hard_total
        
        if is_pair and len(player_cards) == 2:
            pair_val = values[0]
            if pair_val == 11:
                pair_val = 11  # Aces
            if pair_val == 10:
                pair_val = 10  # Tens
            hand_type = f"paire de {player_cards[0].upper()}"
            action = PAIR_STRATEGY.get(pair_val, {}).get(dealer, HIT)
        
        elif is_soft:
            # Soft hand: A + autre carte
            non_ace_val = next(v for v, c in zip(values, player_cards) if c.upper() != 'A')
            if non_ace_val == 10:
                non_ace_val = 10
            hand_type = f"soft {display_total}"
            action = SOFT_STRATEGY.get(non_ace_val, {}).get(dealer, STAND if display_total >= 18 else HIT)
        
        else:
            # Hard hand
            total = hard_total if not is_soft else soft_total
            hand_type = f"hard {total}"
            display_total = total
            if total >= 21:
                action = STAND
            elif total <= 8:
                action = HIT
            else:
                action = HARD_STRATEGY.get(min(total, 21), {}).get(dealer, HIT)
        
        # Si pas de double disponible -> HIT
        if action == DOUBLE and len(player_cards) > 2:
            action = HIT
        
        # Si pas de split disponible -> utilise hard strategy
        if action == SPLIT and len(player_cards) > 2:
            action = HARD_STRATEGY.get(min(display_total, 21), {}).get(dealer, HIT)
        
        return {
            "action": action,
            "explain": ACTION_EXPLAIN.get(action, ""),
            "hand_type": hand_type,
            "total": display_total,
            "confidence": "optimal"
        }
    
    except Exception as e:
        return {
            "action": "ERROR",
            "explain": f"Erreur: {str(e)} - Verifie les cartes entrees.",
            "hand_type": "unknown",
            "total": 0,
            "confidence": "none"
        }


if __name__ == "__main__":
    if len(sys.argv) == 3:
        # CLI mode: python blackjack_advisor.py "8,6" "7"
        player_cards = [c.strip() for c in sys.argv[1].split(",")]
        dealer_card  = sys.argv[2].strip()
        result = get_advice(player_cards, dealer_card)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Demo mode
        tests = [
            (["8", "6"],  "7"),    # Hard 14 vs 7 -> HIT
            (["A", "7"],  "6"),    # Soft 18 vs 6 -> DOUBLE
            (["9", "9"],  "6"),    # Pair 9s vs 6 -> SPLIT
            (["10", "6"], "10"),   # Hard 16 vs 10 -> SURRENDER
            (["A", "K"],  "5"),    # Blackjack
            (["5", "5"],  "9"),    # Pair 5s vs 9 -> DOUBLE (not split)
            (["A", "2"],  "5"),    # Soft 13 vs 5 -> DOUBLE
        ]
        print(f"{'Player':<15} {'Dealer':<8} {'Action':<12} {'Hand':<15} Explanation")
        print("-" * 80)
        for player, dealer in tests:
            r = get_advice(player, dealer)
            print(f"{str(player):<15} {dealer:<8} {r['action']:<12} {r['hand_type']:<15} {r['explain']}")
