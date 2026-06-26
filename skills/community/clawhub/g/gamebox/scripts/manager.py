"""游戏管理 — 创建/加入/启动/结束/列出游戏"""

import sys
import os

# 支持的游戏类型
GAME_TYPES = ["rpg", "werewolf", "story_relay", "ctf", "civilization"]

# 各游戏最小/最大玩家数
GAME_PLAYERS = {
    "rpg":           {"min": 1, "max": 8},
    "werewolf":      {"min": 5, "max": 12},
    "story_relay":   {"min": 2, "max": 10},
    "ctf":           {"min": 2, "max": 20},
    "civilization":  {"min": 2, "max": 8},
}


def cmd_create(params):
    """创建新游戏"""
    game_type = params.get("game_type")
    game_name = params.get("game_name", "")
    creator = params.get("user")
    config = params.get("config", {})

    if not game_type or game_type not in GAME_TYPES:
        return output_error(1, f"无效游戏类型，可选: {', '.join(GAME_TYPES)}")
    if not creator:
        return output_error(1, "缺少 user 参数")

    safe_user = safe_username(creator)
    if not safe_user:
        return output_error(1, "用户名仅允许字母数字下划线，最长32字符")

    gid = gen_id()
    gp = game_path(params, gid)

    # 游戏元信息
    meta = {
        "id": gid,
        "type": game_type,
        "name": game_name or f"{game_type}_{gid}",
        "creator": safe_user,
        "players": [safe_user],
        "config": config,
        "status": "waiting",  # waiting -> playing -> ended
        "created_at": now_ts(),
        "started_at": None,
        "ended_at": None,
    }
    save_json(os.path.join(gp, "meta.json"), meta)

    # 初始空状态（由具体游戏模块的 start 来填充）
    write_state(gp, {
        "phase": "lobby",
        "turn": 0,
        "round": 0,
        "data": {}
    })

    append_log(gp, "game_created", f"{safe_user} 创建了 {game_type} 游戏")
    output_ok(meta, "游戏创建成功")


def cmd_join(params):
    """加入游戏"""
    gid = params.get("game_id")
    user = params.get("user")

    if not gid or not user:
        return output_error(1, "缺少 game_id 或 user 参数")

    safe_user = safe_username(user)
    if not safe_user:
        return output_error(1, "用户名仅允许字母数字下划线")

    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")

    if meta["status"] != "waiting":
        return output_error(3, f"游戏当前状态为 {meta['status']}，无法加入")

    if safe_user in meta["players"]:
        return output_error(3, "你已经在此游戏中")

    limits = GAME_PLAYERS[meta["type"]]
    if len(meta["players"]) >= limits["max"]:
        return output_error(3, f"游戏已满（最多 {limits['max']} 人）")

    meta["players"].append(safe_user)
    save_json(os.path.join(gp, "meta.json"), meta)
    append_log(gp, "player_joined", f"{safe_user} 加入了游戏")

    output_ok({
        "game_id": gid,
        "players": meta["players"],
        "player_count": len(meta["players"]),
        "min_players": limits["min"],
        "max_players": limits["max"]
    }, "加入成功")


def cmd_start(params):
    """启动游戏"""
    gid = params.get("game_id")
    user = params.get("user")

    if not gid or not user:
        return output_error(1, "缺少 game_id 或 user 参数")

    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")

    if meta["status"] != "waiting":
        return output_error(3, f"游戏状态为 {meta['status']}，无法启动")

    if meta["creator"] != user:
        return output_error(3, "只有创建者可以启动游戏")

    limits = GAME_PLAYERS[meta["type"]]
    if len(meta["players"]) < limits["min"]:
        return output_error(3, f"人数不足（最少需要 {limits['min']} 人，当前 {len(meta['players'])} 人）")

    # 加载对应游戏模块初始化状态
    game_type = meta["type"]
    try:
        mod = __import__(f"games.{game_type}", fromlist=["init"])
        init_data = mod.init(meta["players"], meta["config"])
    except Exception as e:
        # 如果游戏模块不存在，使用默认空状态
        init_data = {"game_type": game_type}

    meta["status"] = "playing"
    meta["started_at"] = now_ts()
    save_json(os.path.join(gp, "meta.json"), meta)

    state = read_state(gp)
    state["phase"] = "playing"
    state["turn"] = 1
    state["round"] = 1
    state["data"] = init_data
    write_state(gp, state)

    append_log(gp, "game_started", f"游戏开始，{len(meta['players'])} 名玩家")
    output_ok(meta, "游戏已启动")


def cmd_end(params):
    """结束游戏"""
    gid = params.get("game_id")
    user = params.get("user")
    reason = params.get("reason", "手动结束")

    if not gid or not user:
        return output_error(1, "缺少 game_id 或 user 参数")

    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")

    if meta["status"] != "playing":
        return output_error(3, f"游戏状态为 {meta['status']}，无法结束")

    if meta["creator"] != user:
        return output_error(3, "只有创建者可以结束游戏")

    meta["status"] = "ended"
    meta["ended_at"] = now_ts()
    meta["end_reason"] = reason
    save_json(os.path.join(gp, "meta.json"), meta)

    state = read_state(gp)
    state["phase"] = "ended"
    write_state(gp, state)

    append_log(gp, "game_ended", reason)
    output_ok(meta, "游戏已结束")


def cmd_list(params):
    """列出游戏"""
    gd = games_dir(params)
    status_filter = params.get("status")  # 可选过滤：waiting/playing/ended
    type_filter = params.get("type")      # 可选过滤：游戏类型

    result = []
    if os.path.isdir(gd):
        for entry in sorted(os.listdir(gd)):
            meta_path = os.path.join(gd, entry, "meta.json")
            meta = load_json(meta_path)
            if not meta:
                continue
            if status_filter and meta["status"] != status_filter:
                continue
            if type_filter and meta["type"] != type_filter:
                continue
            result.append(meta)

    output_ok(result, f"共 {len(result)} 个游戏")


def cmd_info(params):
    """查看游戏详情"""
    gid = params.get("game_id")
    if not gid:
        return output_error(1, "缺少 game_id 参数")

    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")

    state = read_state(gp)
    output_ok({"meta": meta, "state": state})


def cmd_leave(params):
    """离开游戏（仅 waiting 状态可退出）"""
    gid = params.get("game_id")
    user = params.get("user")

    if not gid or not user:
        return output_error(1, "缺少 game_id 或 user 参数")

    safe_user = safe_username(user)
    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")

    if meta["status"] != "waiting":
        return output_error(3, "游戏已开始，无法退出")

    if safe_user not in meta["players"]:
        return output_error(3, "你不在游戏中")

    meta["players"].remove(safe_user)

    # 如果创建者退出且还有玩家，转让创建者
    if meta["creator"] == safe_user and meta["players"]:
        meta["creator"] = meta["players"][0]

    # 如果没人了，删除游戏
    if not meta["players"]:
        import shutil
        shutil.rmtree(gp, ignore_errors=True)
        return output_ok(None, "你是最后一人，游戏已删除")

    save_json(os.path.join(gp, "meta.json"), meta)
    append_log(gp, "player_left", f"{safe_user} 离开了游戏")
    output_ok({"players": meta["players"]}, "已退出游戏")


# 命令路由
COMMANDS = {
    "create": cmd_create,
    "join":   cmd_join,
    "start":  cmd_start,
    "end":    cmd_end,
    "leave":  cmd_leave,
    "list":   cmd_list,
    "info":   cmd_info,
}

if __name__ == "__main__":
    from common import (
        parse_input, output_ok, output_error,
        game_dir, games_dir, game_path,
        safe_username, safe_id, gen_id, now_ts,
        load_json, save_json, read_state, write_state,
        append_log
    )
    params = parse_input()
    if isinstance(params, dict) and "status" in params:
        sys.exit(params.get("code", 1))

    action = params.get("action")
    if not action or action not in COMMANDS:
        output_error(1, f"缺少 action 参数，可选: {', '.join(COMMANDS.keys())}")

    COMMANDS[action](params)
