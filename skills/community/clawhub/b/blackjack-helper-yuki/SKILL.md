---
name: blackjack
description: |
  Blackjack (21点) decision assistant. Provides optimal action recommendations based on player's hand and dealer's upcard:
  Hit, Stand, Double, Split, Surrender.
  
  Triggered by: 21点, Blackjack, 二十一, Blackjack,  블랙잭, ブラックジャック, Vingt-et-un, Veintiuno, etc.
---

# Blackjack Strategy Guide

Provides optimal action recommendations based on mathematical probability.

## Decision Rules

### Hard Totals (A counts as 1)

| Player Total | Dealer 2-6 | Dealer 7-10 | Dealer A |
|--------------|------------|-------------|----------|
| 8 or less   | Hit | Hit | Hit |
| 9           | Double | Hit | Hit |
| 10          | Double | Double | Double |
| 11          | Double | Double | Hit |
| 12-16       | Stand | Hit | Hit |
| 17+         | Stand | Stand | Stand |

### Soft Totals (A counts as 11)

| Player Hand | Dealer 2-6 | Dealer 7-A |
|-------------|------------|------------|
| A,2-6       | Hit | Hit |
| A,7         | Stand | Hit |
| A,8-9       | Stand | Stand |

### Pairs

| Pair | Dealer 2-6 | Dealer 7-A |
|------|------------|------------|
| A-A  | Split | Split |
| 8-8  | Split | Split |
| 9-9  | Split | Stand |
| 7-7  | Split | Hit |
| 2-2, 3-3, 6-6 | Split | Hit |
| 4-4, 5-5, 10-10 | Don't split | Don't split |

## How to Use

Provide:
- Player's hand (e.g., 15, soft 17, pair of 8s)
- Dealer's upcard (e.g., dealer 7, dealer Q)

Recommendations:
- **Hit** = Take another card
- **Stand** = Keep current hand
- **Double** = Double bet, get exactly one more card
- **Split** = Split pair into two hands
- **Surrender** = Forfeit half bet (first decision only)

## Examples

> "Player 15, dealer 7" → Recommend: Hit (12-16 vs 7-A)

> "Pair of A's, dealer 6" → Recommend: Split

> "Soft 18, dealer 9" → Recommend: Stand

> "Player 11, dealer A" → Recommend: Hit

## Supported Languages

| Language | 21点 Expression | Keywords |
|----------|----------------|----------|
| English | Twenty-one | blackjack, hit, stand, double, split |
| 中文 | 二十一点 | 21点、要牌、停牌 |
| 日本語 | ブラックジャック | ヒット、スタンド |
| Français | Vingt-et-un | tirer, rester, doubler |
| Español | Veintiuno | pedir, plantarse |
