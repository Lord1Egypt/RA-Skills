"""游戏内消息系统 — 支持 公共/私聊/角色频道"""

import os


def cmd_send(params):
    """发送消息"""
    gid = params.get("game_id")
    sender = params.get("user")
    content = params.get("content", "")
    msg_type = params.get("msg_type", "public")  # public / private / role
    target = params.get("to")  # 私聊目标用户 或 角色频道名

    if not gid or not sender:
        return output_error(1, "缺少 game_id 或 user 参数")
    if not content:
        return output_error(1, "消息内容不能为空")

    safe_sender = safe_username(sender)

    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")

    if msg_type == "private" and not target:
        return output_error(1, "私聊需要指定 to 参数")
    if msg_type == "role" and not target:
        return output_error(1, "角色频道需要指定 to 参数（角色名）")

    msg = {
        "ts": now_ts(),
        "from": safe_sender,
        "type": msg_type,
        "content": content,
    }

    # 根据类型写入不同位置
    msg_dir = os.path.join(gp, "messages")

    if msg_type == "public":
        # 公共消息 → messages/public/
        d = os.path.join(msg_dir, "public")
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, f"{now_file()}_{safe_sender}_{gen_id()}.json")

    elif msg_type == "private":
        # 私聊 → messages/private/{target}/
        d = os.path.join(msg_dir, "private", target)
        os.makedirs(d, exist_ok=True)
        msg["to"] = target
        path = os.path.join(d, f"{now_file()}_{safe_sender}_{gen_id()}.json")

        # 也存一份到发送者自己的私聊记录
        d2 = os.path.join(msg_dir, "private", safe_sender)
        os.makedirs(d2, exist_ok=True)
        path2 = os.path.join(d2, f"{now_file()}_{safe_sender}_{gen_id()}.json")
        save_json(path2, msg)

    elif msg_type == "role":
        # 角色频道 → messages/role/{role_name}/
        d = os.path.join(msg_dir, "role", target)
        os.makedirs(d, exist_ok=True)
        msg["role"] = target
        path = os.path.join(d, f"{now_file()}_{safe_sender}_{gen_id()}.json")

    elif msg_type == "system":
        # 系统消息 → messages/system/
        d = os.path.join(msg_dir, "system")
        os.makedirs(d, exist_ok=True)
        msg["from"] = "system"
        path = os.path.join(d, f"{now_file()}_{gen_id()}.json")

    else:
        return output_error(1, f"未知消息类型: {msg_type}，可选: public/private/role/system")

    save_json(path, msg)
    output_ok(msg, "消息已发送")


def cmd_receive(params):
    """接收消息"""
    gid = params.get("game_id")
    user = params.get("user")
    channel = params.get("channel")  # public / private / role / system / all
    role = params.get("role")        # 角色名（channel=role 时需要）
    since = params.get("since")      # 时间戳，只看此之后的消息
    limit = params.get("limit", 50)

    if not gid or not user:
        return output_error(1, "缺少 game_id 或 user 参数")

    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")

    safe_user = safe_username(user)
    msg_dir = os.path.join(gp, "messages")
    result = []

    def collect(directory):
        """收集目录中所有未读消息"""
        if not os.path.isdir(directory):
            return
        for fp in list_files_sorted(directory, ".json"):
            entry = load_json(fp)
            if not entry:
                continue
            if since and entry.get("ts", "") <= since:
                continue
            # 标记已读（重命名加 .read）
            read_marker = fp + ".read"
            if not os.path.exists(read_marker):
                # 读取时标记
                try:
                    with open(read_marker, "w") as f:
                        f.write(safe_user)
                except OSError:
                    pass
            result.append(entry)

    if not channel or channel == "all":
        collect(os.path.join(msg_dir, "public"))
        collect(os.path.join(msg_dir, "private", safe_user))
        collect(os.path.join(msg_dir, "system"))
    elif channel == "public":
        collect(os.path.join(msg_dir, "public"))
    elif channel == "private":
        collect(os.path.join(msg_dir, "private", safe_user))
    elif channel == "role" and role:
        collect(os.path.join(msg_dir, "role", role))
    elif channel == "system":
        collect(os.path.join(msg_dir, "system"))
    else:
        return output_error(1, f"未知频道: {channel}")

    # 按时间排序，限制数量
    result.sort(key=lambda x: x.get("ts", ""))
    result = result[-int(limit):]

    output_ok({
        "user": safe_user,
        "count": len(result),
        "messages": result
    })


def cmd_channels(params):
    """列出可用频道"""
    gid = params.get("game_id")
    user = params.get("user")

    if not gid:
        return output_error(1, "缺少 game_id 参数")

    gp = game_path(params, gid)
    meta = load_json(os.path.join(gp, "meta.json"))
    if not meta:
        return output_error(2, "游戏不存在")

    msg_dir = os.path.join(gp, "messages")
    channels = {
        "public": os.path.isdir(os.path.join(msg_dir, "public")),
        "private": os.path.isdir(os.path.join(msg_dir, "private", user)) if user else False,
        "system": os.path.isdir(os.path.join(msg_dir, "system")),
    }

    # 列出角色频道
    role_dir = os.path.join(msg_dir, "role")
    channels["roles"] = []
    if os.path.isdir(role_dir):
        channels["roles"] = sorted(os.listdir(role_dir))

    output_ok(channels)


COMMANDS = {
    "send":     cmd_send,
    "receive":  cmd_receive,
    "channels": cmd_channels,
}

if __name__ == "__main__":
    from common import (
        parse_input, output_ok, output_error,
        game_path, load_json, list_files_sorted,
        safe_username, gen_id, now_ts, now_file,
        save_json
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
