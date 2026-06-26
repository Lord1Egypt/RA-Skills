#!/usr/bin/env python3
"""EV Calculator - 期望值计算器"""

import argparse
import json
from typing import Optional, Tuple

def calculate_ev(p: float, win: float, loss: float) -> float:
    """
    计算基础期望值
    
    Args:
        p: 胜率 (0-1)
        win: 赢的金额
        loss: 输的金额
    
    Returns:
        EV值 (正=赚，负=亏)
    """
    return p * win - (1 - p) * loss


def polymarket_ev(your_prob: float, market_price: float) -> Tuple[float, float]:
    """
    计算Polymarket的EV
    
    Args:
        your_prob: 你判断的真实概率 (0-1)
        market_price: 市场定价 (0-1)
    
    Returns:
        (edge, ev_per_dollar)
    """
    edge = your_prob - market_price
    ev_dollar = edge / market_price if market_price > 0 else 0
    return edge, ev_dollar


def kelly_from_ev(p: float, b: float, fraction: float = 0.5) -> float:
    """
    从EV转凯利仓位
    
    Args:
        p: 胜率
        b: 盈亏比
        fraction: 分数凯利系数
    
    Returns:
        建议仓位
    """
    f_star = (p * b - (1 - p)) / b
    if f_star < 0:
        return 0
    return f_star * fraction


def main():
    parser = argparse.ArgumentParser(description="EV Calculator - 期望值计算器")
    parser.add_argument("--p", type=float, help="胜率 (0-1, e.g., 0.55)")
    parser.add_argument("--win", type=float, help="赢的金额 (e.g., 1.10)")
    parser.add_argument("--loss", type=float, help="输的金额 (e.g., 1.00)")
    parser.add_argument("--market", type=float, help="市场定价 (Polymarket, 0-1)")
    parser.add_argument("--your", type=float, help="你的判断概率 (0-1)")
    parser.add_argument("--b", type=float, help="盈亏比 (win/loss)")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    
    args = parser.parse_args()
    
    result = {}
    
    if args.p is not None and args.win is not None and args.loss is not None:
        ev = calculate_ev(args.p, args.win, args.loss)
        ev_pct = (ev / args.loss * 100) if args.loss > 0 else 0
        
        result = {
            "type": "basic",
            "inputs": {
                "win_probability": args.p,
                "win": args.win,
                "loss": args.loss
            },
            "ev": round(ev, 4),
            "ev_percentage": round(ev_pct, 2),
            "verdict": "✅ 正期望" if ev > 0 else "❌ 负期望" if ev < 0 else "⚪ 持平"
        }
        
        # 如果有盈亏比，也算凯利
        if args.b:
            kelly = kelly_from_ev(args.p, args.b, 0.5)
            result["kelly_half"] = round(kelly * 100, 2)
    
    elif args.market is not None and args.your is not None:
        edge, ev = polymarket_ev(args.your, args.market)
        
        result = {
            "type": "polymarket",
            "inputs": {
                "market_price": args.market,
                "your_probability": args.your
            },
            "edge": round(edge, 4),
            "edge_percentage": round(edge * 100, 2),
            "ev_per_dollar": round(ev, 4),
            "verdict": "✅ 正期望" if edge > 0 else "❌ 负期望"
        }
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n🎯 EV 期望值计算")
        print(f"=" * 40)
        
        if result.get("type") == "basic":
            i = result["inputs"]
            print(f"胜率: {i['win_probability']*100:.0f}%")
            print(f"赢: ${i['win']} | 亏: ${i['loss']}")
            print(f"")
            print(f"EV: ${result['ev']:.4f} ({result['ev_percentage']:.1f}%)")
            print(f"判定: {result['verdict']}")
            
            if "kelly_half" in result:
                print(f"")
                print(f"🧮 建议仓位 (½凯利): {result['kelly_half']}%")
        
        elif result.get("type") == "polymarket":
            i = result["inputs"]
            print(f"市场定价: {i['market_price']*100:.0f}%")
            print(f"你的判断: {i['your_probability']*100:.0f}%")
            print(f"")
            print(f"Edge: {result['edge_percentage']:.1f}%")
            print(f"每$期望赚: ${result['ev_per_dollar']:.2f}")
            print(f"判定: {result['verdict']}")
        
        else:
            print("用法:")
            print("  基础EV: ev_calculator --p 0.55 --win 1.10 --loss 1.00")
            print("  Polymarket: ev_calculator --market 0.40 --your 0.60")


if __name__ == "__main__":
    main()
