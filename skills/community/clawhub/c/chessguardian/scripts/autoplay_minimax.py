#!/usr/bin/env python3
"""Minimax with Alpha-Beta Pruning autoplay bot for ChessGuardian live games.
Plays as Black using a custom minimax engine against the server's Stockfish (White).

Usage:
  python3 autoplay_minimax.py <game_id> [--depth 4] [--delay 5] [--url URL]
  python3 autoplay_minimax.py new [--depth 4] [--delay 5] [--url URL]  # starts a new game

The minimax engine evaluates positions using:
  - Material count (piece values)
  - Piece-square tables (positional bonuses)
  - Mobility (number of legal moves)
  - King safety (castling rights, pawn shield)
  - Center control
"""

import argparse
import math
import sys
import time
from typing import Optional, Tuple

import chess
import requests

DEFAULT_URL = "https://chessguardian-production.up.railway.app"
DEFAULT_DEPTH = 4  # Minimax is much slower than Stockfish, 4 is reasonable
DEFAULT_DELAY = 5

# ─── Piece Values (centipawns) ───
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}

# ─── Piece-Square Tables (from White's perspective, flip for Black) ───
# Values represent positional bonuses in centipawns

PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0,
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

ROOK_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0,
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20,
]

KING_MIDGAME_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20,
]

PST = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE,
    chess.KING: KING_MIDGAME_TABLE,
}


def pst_value(piece_type: int, square: int, is_white: bool) -> int:
    """Get piece-square table value. Flip table for black pieces."""
    table = PST.get(piece_type)
    if not table:
        return 0
    if is_white:
        return table[square]
    else:
        # Mirror vertically for black
        row = 7 - (square // 8)
        col = square % 8
        return table[row * 8 + col]


def evaluate(board: chess.Board) -> int:
    """Evaluate position in centipawns from White's perspective.
    Positive = White advantage, Negative = Black advantage."""

    if board.is_checkmate():
        return -30000 if board.turn == chess.WHITE else 30000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    if board.can_claim_draw():
        return 0

    score = 0

    # Material + piece-square tables
    for square, piece in board.piece_map().items():
        value = PIECE_VALUES.get(piece.piece_type, 0)
        pst = pst_value(piece.piece_type, square, piece.color == chess.WHITE)
        if piece.color == chess.WHITE:
            score += value + pst
        else:
            score -= value + pst

    # Mobility bonus (number of legal moves)
    mobility = board.legal_moves.count()
    if board.turn == chess.WHITE:
        score += mobility * 2
    else:
        score -= mobility * 2

    # Bonus for castling rights
    if board.has_kingside_castling_rights(chess.WHITE):
        score += 15
    if board.has_queenside_castling_rights(chess.WHITE):
        score += 10
    if board.has_kingside_castling_rights(chess.BLACK):
        score -= 15
    if board.has_queenside_castling_rights(chess.BLACK):
        score -= 10

    # Check bonus
    if board.is_check():
        score += 20 if board.turn == chess.BLACK else -20

    return score


def order_moves(board: chess.Board):
    """Order moves for better alpha-beta pruning: captures first, then checks."""
    moves = list(board.legal_moves)

    def move_score(move):
        s = 0
        # MVV-LVA for captures
        if board.is_capture(move):
            victim = board.piece_type_at(move.to_square)
            attacker = board.piece_type_at(move.from_square)
            if victim and attacker:
                s += PIECE_VALUES.get(victim, 0) * 10 - PIECE_VALUES.get(attacker, 0)
            else:
                s += 500
        # Promotion
        if move.promotion:
            s += PIECE_VALUES.get(move.promotion, 0)
        # Check
        board.push(move)
        if board.is_check():
            s += 50
        board.pop()
        return -s  # Negative for descending sort

    moves.sort(key=move_score)
    return moves


def minimax(board: chess.Board, depth: int, alpha: int, beta: int, maximizing: bool) -> Tuple[int, Optional[chess.Move]]:
    """Minimax with alpha-beta pruning.
    Returns (eval_score, best_move)."""

    if depth == 0 or board.is_game_over():
        return evaluate(board), None

    best_move = None

    if maximizing:
        max_eval = -999999
        for move in order_moves(board):
            board.push(move)
            eval_score, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval, best_move
    else:
        min_eval = 999999
        for move in order_moves(board):
            board.push(move)
            eval_score, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval, best_move


def find_best_move(fen: str, depth: int) -> Tuple[str, str, str, int]:
    """Find the best move using minimax. Returns (san, uci, eval_str, eval_cp)."""
    board = chess.Board(fen)
    maximizing = board.turn == chess.WHITE

    start = time.time()
    eval_cp, best_move = minimax(board, depth, -999999, 999999, maximizing)
    elapsed = time.time() - start

    if not best_move:
        # Fallback: pick first legal move
        best_move = list(board.legal_moves)[0]
        eval_cp = 0

    san = board.san(best_move)
    uci = best_move.uci()
    eval_str = f"{eval_cp / 100:+.2f}"

    print(f"         ⏱️  {elapsed:.1f}s | nodes explored")
    return san, uci, eval_str, eval_cp


# ─── Game API ───

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


def eval_to_pct(cp):
    return max(0, min(100, round(50 + 50 * math.tanh(cp / 600))))


def main():
    parser = argparse.ArgumentParser(description="Minimax Alpha-Beta autoplay for ChessGuardian")
    parser.add_argument("game_id", help="Live game ID or 'new' to start a new game")
    parser.add_argument("--depth", type=int, default=DEFAULT_DEPTH, help=f"Search depth (default: {DEFAULT_DEPTH})")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--max-moves", type=int, default=200)
    args = parser.parse_args()

    game_id = args.game_id
    if game_id.lower() == "new":
        game_id = start_new_game(args.url)

    print(f"\n🧠 MINIMAX ALPHA-BETA AUTOPLAY — Game {game_id}")
    print(f"   Engine: Minimax + Alpha-Beta Pruning (depth {args.depth})")
    print(f"   Evaluation: Material + PST + Mobility + King Safety")
    print(f"   Delay: {args.delay}s | Max moves: {args.max_moves}")
    print(f"   Live: {args.url}/live/{game_id}")
    print(f"{'─' * 55}")

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

            san, uci, eval_str, eval_cp = find_best_move(fen, args.depth)
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

    print("👋 Done")


if __name__ == "__main__":
    main()
