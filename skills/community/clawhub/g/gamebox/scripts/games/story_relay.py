"""小说接龙 — 多人协作创作，LLM 调和风格"""

import random


GENRES = [
    "奇幻", "科幻", "悬疑", "言情", "武侠",
    "恐怖", "喜剧", "历史", "末日", "赛博朋克",
]


def init(players, config=None):
    """初始化小说接龙"""
    cfg = config or {}
    genre = cfg.get("genre", random.choice(GENRES))
    setting = cfg.get("setting", "")
    max_rounds = cfg.get("max_rounds", 50)
    words_per_turn = cfg.get("words_per_turn", 200)  # 每人每轮字数上限建议
    max_words = cfg.get("max_words", 10000)  # 全文总字数上限

    # 随机确定写作顺序
    order = list(players)
    random.shuffle(order)

    return {
        "game_type": "story_relay",
        "genre": genre,
        "setting": setting,
        "max_rounds": max_rounds,
        "words_per_turn": words_per_turn,
        "max_words": max_words,
        "write_order": order,
        "current_writer_idx": 0,
        "segments": [],       # 已写段落 [{writer, content, word_count, ts}]
        "total_words": 0,
        "round": 1,
        "phase": "writing",   # writing / reviewing / finished
        "characters": {},     # 角色: {name: description}
        "plot_threads": [],   # 剧情线索
        "style_notes": {},    # 每位作者的写作风格备注
        "finished": False,
    }


def resolve(state, user, action_name, action_params):
    """解析动作"""
    hint = {"action": action_name, "player": user}
    order = state["write_order"]

    # 检查是否轮到该作者
    current_writer = order[state["current_writer_idx"] % len(order)]
    if action_name == "write" and user != current_writer:
        hint["error"] = f"未轮到你，当前轮到 {current_writer}"
        return state, hint

    if action_name == "write":
        """提交段落"""
        content = action_params.get("content", "").strip()
        if not content:
            return state, {"error": "内容不能为空"}

        word_count = len(content)

        # 检查字数
        if state["max_words"] and state["total_words"] + word_count > state["max_words"]:
            hint["error"] = f"超出总字数上限 ({state['max_words']})"
            return state, hint

        segment = {
            "writer": user,
            "content": content,
            "word_count": word_count,
            "round": state["round"],
        }
        state["segments"].append(segment)
        state["total_words"] += word_count

        # 推进到下一位作者
        state["current_writer_idx"] += 1
        if state["current_writer_idx"] % len(order) == 0:
            state["round"] += 1

        # 检查是否到达最大轮数
        if state["round"] > state["max_rounds"]:
            state["finished"] = True
            state["phase"] = "finished"
            hint["narrative"] = "小说已完成！"
            hint["needs_llm"] = True
        else:
            next_writer = order[state["current_writer_idx"] % len(order)]
            hint["narrative"] = f"{user} 写了一段 ({word_count} 字)。轮到 {next_writer}"
            hint["needs_llm"] = True
            hint["next_writer"] = next_writer
            hint["current_text"] = _get_recent_text(state, 3)

    elif action_name == "add_character":
        """添加角色"""
        name = action_params.get("name", "")
        desc = action_params.get("description", "")
        if not name:
            return state, {"error": "角色名不能为空"}
        state["characters"][name] = {
            "description": desc,
            "created_by": user,
        }
        hint["narrative"] = f"{user} 添加了角色: {name}"
        hint["needs_llm"] = False

    elif action_name == "add_plot_thread":
        """添加剧情线索"""
        thread = action_params.get("thread", "")
        if not thread:
            return state, {"error": "线索不能为空"}
        state["plot_threads"].append({
            "content": thread,
            "created_by": user,
            "resolved": False,
        })
        hint["narrative"] = f"{user} 添加了剧情线索"
        hint["needs_llm"] = False

    elif action_name == "resolve_thread":
        """解决剧情线索"""
        idx = action_params.get("index")
        resolution = action_params.get("resolution", "")
        if idx is not None and 0 <= idx < len(state["plot_threads"]):
            state["plot_threads"][idx]["resolved"] = True
            state["plot_threads"][idx]["resolution"] = resolution
            hint["narrative"] = f"{user} 推进了剧情线索"
        else:
            hint["error"] = "无效线索编号"
        hint["needs_llm"] = False

    elif action_name == "revise":
        """修改自己最近的段落"""
        idx = action_params.get("index")
        new_content = action_params.get("content", "").strip()
        if idx is None or idx < 0 or idx >= len(state["segments"]):
            return state, {"error": "无效段落编号"}
        seg = state["segments"][idx]
        if seg["writer"] != user:
            return state, {"error": "只能修改自己的段落"}
        old_count = seg["word_count"]
        seg["content"] = new_content
        seg["word_count"] = len(new_content)
        state["total_words"] += len(new_content) - old_count
        hint["narrative"] = f"{user} 修改了第 {idx + 1} 段"
        hint["needs_llm"] = False

    elif action_name == "finish":
        """提前结束"""
        if user != order[0]:  # 只有第一个作者（发起者）可以结束
            return state, {"error": "只有发起者可以提前结束"}
        state["finished"] = True
        state["phase"] = "finished"
        hint["narrative"] = f"{user} 结束了小说创作"
        hint["needs_llm"] = True

    elif action_name == "read":
        """读取当前全文或最近段落"""
        count = action_params.get("last", 5)
        text = _get_recent_text(state, count)
        hint["narrative"] = text
        hint["needs_llm"] = False

    else:
        return state, {"error": f"未知动作: {action_name}"}

    return state, hint


def _get_recent_text(state, last_n):
    """获取最近 N 段文本"""
    segments = state["segments"][-last_n:]
    return "\n\n".join(f"[{s['writer']}] {s['content']}" for s in segments)


def check_win(state):
    """接龙无胜负，结束即完成"""
    if state.get("finished"):
        return {
            "winner": "all",
            "message": f"小说完成！共 {state['round'] - 1} 轮，{state['total_words']} 字，{len(state['segments'])} 段。",
            "stats": {
                "rounds": state["round"] - 1,
                "words": state["total_words"],
                "segments": len(state["segments"]),
                "authors": state["write_order"],
            }
        }
    return None
