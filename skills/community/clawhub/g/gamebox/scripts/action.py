"""统一动作接口 — 所有游戏通过此脚本提交动作"""

import os


def cmd_do(params):
    """执行游戏动作"""
    gid = params.get("game_id")
    user = params.get("user")
    action_name = params.get("action_name")
    action_params = params.get("params", {})

    if not gid or not user or not action_name:
        return output_error(1, "缺少 game_id / user / action_name 参数")

    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")
    if meta["status"] != "playing":
        return output_error(3, "游戏未在进行中")

    # 验证是否轮到该玩家（单人游戏跳过检查）
    state = read_state(gp)
    players = meta["players"]
    turn = state.get("turn", 1)

    if len(players) > 1:
        current_idx = (turn - 1) % len(players)
        if players[current_idx] != user:
            current_player = players[current_idx]
            return output_error(3, f"未轮到你，当前轮到 {current_player}")

    # 动作记录
    action_dir = os.path.join(gp, "actions")
    os.makedirs(action_dir, exist_ok=True)
    action_entry = {
        "ts": now_ts(),
        "turn": turn,
        "user": user,
        "action": action_name,
        "params": action_params,
    }
    action_path = os.path.join(action_dir, f"{now_file()}_{gen_id()}.json")
    save_json(action_path, action_entry)

    append_log(gp, "action", f"{user} 执行 {action_name}: {action_params}")

    output_ok({
        "turn": turn,
        "user": user,
        "action": action_name,
        "params": action_params,
        "recorded": True
    }, "动作已记录")


def cmd_history(params):
    """查看动作历史"""
    gid = params.get("game_id")
    user_filter = params.get("user")
    action_filter = params.get("action_name")
    limit = params.get("limit", 50)

    if not gid:
        return output_error(1, "缺少 game_id 参数")

    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")

    action_dir = os.path.join(gp, "actions")
    files = list_files_sorted(action_dir, ".json")

    result = []
    for fp in reversed(files[-int(limit):]):
        entry = load_json(fp)
        if not entry:
            continue
        if user_filter and entry.get("user") != user_filter:
            continue
        if action_filter and entry.get("action") != action_filter:
            continue
        result.append(entry)

    output_ok({
        "total": len(result),
        "actions": result
    })


def cmd_undo(params):
    """撤销最近一条动作（仅创建者或动作本人）"""
    gid = params.get("game_id")
    user = params.get("user")

    if not gid or not user:
        return output_error(1, "缺少 game_id 或 user 参数")

    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")

    # 权限检查
    if user != meta["creator"]:
        return output_error(3, "只有创建者可以撤销动作")

    action_dir = os.path.join(gp, "actions")
    files = list_files_sorted(action_dir, ".json")

    if not files:
        return output_error(2, "没有可撤销的动作")

    last_file = files[-1]
    last_action = load_json(last_file)

    # 删除最后一条
    os.remove(last_file)

    append_log(gp, "action_undone", f"{user} 撤销了 {last_action.get('action')}")

    output_ok({
        "undone": last_action
    }, "动作已撤销")


COMMANDS = {
    "do":      cmd_do,
    "history": cmd_history,
    "undo":    cmd_undo,
}

if __name__ == "__main__":
    from common import (
        parse_input, output_ok, output_error,
        game_path, load_json, read_state, write_state,
        save_json, list_files_sorted,
        gen_id, now_ts, now_file,
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
