#!/usr/bin/env python3
"""Stockfish autoplay bot for ChessGuardian live games.
Plays as Black using Stockfish engine against the server's Stockfish (White).

Usage:
  python3 autoplay_stockfish.py <game_id> [--depth 20] [--delay 5] [--url URL]
  python3 autoplay_stockfish.py new [--depth 20] [--delay 5] [--url URL]  # starts a new game
"""

import argparse
import math
import sys
import time

import chess
import chess.engine
import requests

DEFAULT_URL = "https://chessguardian-production.up.railway.app"
DEFAULT_DEPTH = 20
DEFAULT_DELAY = 5


def get_stockfish():
    for path in ["/usr/games/stockfish", "/usr/local/bin/stockfish", "stockfish"]:
        try:
            engine = chess.engine.SimpleEngine.popen_uci(path)
            print(f"✅ Stockfish loaded: {path}")
            return engine
        except Exception:
            continue
    print("❌ Stockfish not found!")
    sys.exit(1)


def start_new_game(base_url):
    resp = requests.post(f"{base_url}/api/live/start", json={"mode": "ai"})
    resp.raise_for_status()
    data = resp.json()
    game_id = data["id"]
    print(f"🆕 New game started: {game_id}")
    print(f"   First move: {data['history'][0]}")
    return game_id


def get_state(base_url, game_id):
    resp = requests.get(f"{base_url}/api/live/{game_id}")
    resp.raise_for_status()
    return resp.json()


def make_move(base_url, game_id, move):
    resp = requests.post(f"{base_url}/api/live/{game_id}/move", json={"move": move})
    return resp.json()


def find_best_move(engine, fen, depth):
    board = chess.Board(fen)
    result = engine.play(board, chess.engine.Limit(depth=depth))
    san = board.san(result.move)
    uci = result.move.uci()

    info = engine.analyse(board, chess.engine.Limit(depth=depth))
    score = info.get("score")
    eval_str, eval_cp = "", 0
    if score:
        pov = score.white()
        if pov.is_mate():
            eval_str = f"M{pov.mate()}"
            eval_cp = 10000 if pov.mate() > 0 else -10000
        else:
            eval_cp = pov.score()
            eval_str = f"{eval_cp / 100:+.2f}"
    return san, uci, eval_str, eval_cp


def eval_to_pct(cp):
    return max(0, min(100, round(50 + 50 * math.tanh(cp / 600))))


def main():
    parser = argparse.ArgumentParser(description="Stockfish autoplay for ChessGuardian")
    parser.add_argument("game_id", help="Live game ID or 'new' to start a new game")
    parser.add_argument("--depth", type=int, default=DEFAULT_DEPTH)
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--max-moves", type=int, default=200)
    args = parser.parse_args()

    game_id = args.game_id
    if game_id.lower() == "new":
        game_id = start_new_game(args.url)

    print(f"\n♟️  STOCKFISH AUTOPLAY — Game {game_id}")
    print(f"   Engine: Stockfish (depth {args.depth})")
    print(f"   Delay: {args.delay}s | Max moves: {args.max_moves}")
    print(f"   Live: {args.url}/live/{game_id}")
    print(f"{'─' * 55}")

    engine = get_stockfish()

    try:
        move_count = 0
        while move_count < args.max_moves:
            state = get_state(args.url, game_id)

            if state.get("error"):
                print(f"❌ {state['error']}")
                break
            if state.get("gameOver"):
                print(f"\n🏁 Game Over! {state['status']} | Result: {state.get('result', 'N/A')}")
                print(f"   Total moves: {len(state['history'])}")
                break

            if state.get("turn") != "black":
                time.sleep(1)
                continue

            fen = state["fen"]
            history = state.get("history", [])
            move_num = len(history) // 2 + 1

            san, uci, eval_str, eval_cp = find_best_move(engine, fen, args.depth)
            black_pct = 100 - eval_to_pct(eval_cp)
            print(f"  {move_num}... {san:<8} eval: {eval_str:>8}  Black: {black_pct}%")

            result = make_move(args.url, game_id, san)
            if result.get("error"):
                result = make_move(args.url, game_id, uci)
                if result.get("error"):
                    print(f"  ❌ Move rejected: {result['error']}")
                    break

            sf_move = result.get("stockfishMove")
            if sf_move:
                new_num = len(result.get("history", [])) // 2 + 1
                print(f"  {new_num}. {sf_move:<8} (Server Stockfish)")

            if result.get("gameOver"):
                status = result.get("status", "unknown")
                res = result.get("result", "N/A")
                winner = "White" if res == "1-0" else "Black" if res == "0-1" else "Draw"
                print(f"\n🏆 {status.upper()}! {winner} wins!")
                print(f"   Total moves: {len(result.get('history', []))}")
                break

            move_count += 1
            time.sleep(args.delay)

    except KeyboardInterrupt:
        print("\n⏹️  Stopped")
    finally:
        engine.quit()
        print("👋 Engine closed")


if __name__ == "__main__":
    main()
