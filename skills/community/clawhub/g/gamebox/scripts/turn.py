"""回合控制 — 轮次/阶段/超时管理"""

import os


def cmd_next_turn(params):
    """推进到下一个玩家回合"""
    gid = params.get("game_id")
    user = params.get("user")

    if not gid or not user:
        return output_error(1, "缺少 game_id 或 user 参数")

    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")
    if meta["status"] != "playing":
        return output_error(3, "游戏未在进行中")

    state = read_state(gp)
    players = meta["players"]
    turn = state.get("turn", 1)

    # 计算下一个玩家索引
    current_idx = (turn - 1) % len(players)
    next_idx = (current_idx + 1) % len(players)

    # 如果转了一圈，round + 1
    if next_idx == 0:
        state["round"] = state.get("round", 1) + 1

    state["turn"] = turn + 1
    write_state(gp, state)

    current_player = players[next_idx]
    append_log(gp, "next_turn", f"轮到 {current_player}（第 {state['round']} 轮）")

    output_ok({
        "turn": state["turn"],
        "round": state["round"],
        "current_player": current_player,
        "players": players,
        "turn_order": [players[(next_idx + i) % len(players)] for i in range(len(players))]
    }, f"轮到 {current_player}")


def cmd_set_phase(params):
    """设置游戏阶段"""
    gid = params.get("game_id")
    user = params.get("user")
    phase = params.get("phase")

    if not gid or not phase:
        return output_error(1, "缺少 game_id 或 phase 参数")

    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")

    state = read_state(gp)
    old_phase = state.get("phase", "unknown")
    state["phase"] = phase
    write_state(gp, state)

    append_log(gp, "phase_change", f"{old_phase} -> {phase}")
    output_ok({
        "old_phase": old_phase,
        "new_phase": phase,
        "turn": state.get("turn", 1),
        "round": state.get("round", 1)
    })


def cmd_skip_turn(params):
    """跳过当前玩家（超时）"""
    gid = params.get("game_id")
    user = params.get("user")

    if not gid:
        return output_error(1, "缺少 game_id 参数")

    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")

    state = read_state(gp)
    players = meta["players"]
    turn = state.get("turn", 1)
    skipped_idx = (turn - 1) % len(players)
    skipped_player = players[skipped_idx]

    append_log(gp, "turn_skipped", f"{skipped_player} 超时被跳过")

    # 自动推进
    params_copy = dict(params)
    return cmd_next_turn(params_copy)


def cmd_status(params):
    """查看当前回合状态"""
    gid = params.get("game_id")

    if not gid:
        return output_error(1, "缺少 game_id 参数")

    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")

    state = read_state(gp)
    players = meta["players"]
    turn = state.get("turn", 1)
    current_idx = (turn - 1) % len(players)

    output_ok({
        "game_id": gid,
        "status": meta["status"],
        "phase": state.get("phase"),
        "turn": turn,
        "round": state.get("round", 1),
        "current_player": players[current_idx] if players else None,
        "players": players,
        "turn_order": [players[(current_idx + i) % len(players)] for i in range(len(players))]
    })


COMMANDS = {
    "next":  cmd_next_turn,
    "phase": cmd_set_phase,
    "skip":  cmd_skip_turn,
    "status": cmd_status,
}

if __name__ == "__main__":
    from common import (
        parse_input, output_ok, output_error,
        game_path, load_json, read_state, write_state,
        append_log
    )
    params = parse_input()
    if isinstance(params, dict) and "status" in params:
        import sys
        sys.exit(params.get("code", 1))

    action = params.get("action")
    if not action or action not in COMMANDS:
        import sys
        output_error(1, f"缺少 action 参数，可选: {', '.join(COMMANDS.keys())}")

    COMMANDS[action](params)
