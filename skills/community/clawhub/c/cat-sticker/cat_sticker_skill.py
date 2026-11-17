#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
猫猫表情包技能系统  v1.0
Cat Sticker Skill System

功能：
  - 读取 custom_stickers.json，建立关键词→表情映射
  - 分析输入文本情绪关键词，按概率匹配表情
  - 指令调节：概率 / 开关 / 冷却轮数
  - 避免连续两张相同表情

用法（可被其他 Agent 调用）：
  import cat_sticker_skill as cs
  result = cs.pick_sticker("我好开心喵~")
  print(result)  # dict with keys: triggered, sticker, description, original_text

作者：夜玖 (NEKOLAND)
"""

import json
import os
import random
import re
import sys
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────
# 路径配置
# ─────────────────────────────────────────────
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = SCRIPT_DIR / "sticker_config.json"
STICKERS_JSON = SCRIPT_DIR / "custom_stickers.json"
COOLDOWN_FILE = SCRIPT_DIR / "sticker_cooldown.json"
STICKERS_DIR = SCRIPT_DIR  # 表情图片与 JSON 同目录

# ─────────────────────────────────────────────
# 全局状态（进程内冷却，防止同进程连续重复）
# ─────────────────────────────────────────────
_last_sticker_file: Optional[str] = None
_turn_counter: int = 0  # 模拟轮次，每调用一次 pick_sticker 递增

# ─────────────────────────────────────────────
# 核心数据结构
# ─────────────────────────────────────────────

# 情绪 → 关键词映射（精确优先，短词放后）
EMOTION_KEYWORDS: dict[str, list[str]] = {
    "撒娇":    ["撒娇", "抱抱", "贴贴", "蹭", "摸摸", "摸摸头", "rua", "rua我"],
    "卖萌":    ["卖萌", "可爱", "乖", "乖喵", "小可爱", "奶", "嗲", "喵~", "喵呜"],
    "害羞":    ["害羞", "脸红", "羞涩", "不好意思", "脸红红", "脸红ing"],
    "开心":    ["开心", "高兴", "快乐", "好耶", "棒", "开心", "happy", "耶", "好开心", "超开心"],
    "生气":    ["生气", "气", "怒", "哼", "讨厌", "气死我了", "气死", "烦", "恼"],
    "难过":    ["难过", "伤心", "委屈", "痛", "sad", "抑郁", "自闭", "哭哭"],
    "惊讶":    ["惊", "惊讶", "吓", "吓到", "卧槽", "震惊", "惊呆", "啊？", "卧槽"],
    "疑惑":    ["疑惑", "？", "什么", "不懂", "怎么", "为什么", "嗯？", "喵？"],
    "嫌弃":    ["嫌弃", "无语", "服了", "脑淤血", "离谱", "屑", "下头"],
    "无语":    ["无语", "无语了", "服了", "无话可说"],
    "害怕":    ["害怕", "怕", "惊", "恐惧", "瑟瑟", "抖"],
    "思考":    ["思考", "想", "嗯", "沉思", "脑子", "转一转"],
    "困":      ["困", "累", "睡觉", "晚安", "困了", "想睡", "困困", "困了", "晚安喵", "想睡觉"],
    "饿":      ["饿了", "馋", "吃", "想吃", "好饿", "嚼", "好想吃", "吃东西"],
    "喵叫":    ["喵", "咪", "喵~", "喵喵", "喵呜", "猫", "mua", "mua~", "咕噜", "喵~喵~"],
    "坏笑":    ["坏笑", "嘿嘿嘿", "桀桀桀", "阴险", "皮"],
    "大哭":    ["大哭", "哭", "呜呜", "哇", "呜呜呜"],
    "傻笑":    ["傻笑", "哈哈", "哈哈哈", "笑死", "笑死我了"],
    "投降":    ["投降", "服", "认输", "求饶", "我错了"],
    "OK":      ["ok", "OK", "好", "行", "可以", "收到"],
    "恶搞":    ["笨蛋", "蠢", "傻", "智障", "杂鱼", "你不行", "坏", "坏蛋", "笨", "笨死了"],
}

# 情绪 → 表情文件映射（从 custom_stickers.json 加载后填充）
_emotion_stickers: dict[str, list[dict]] = {}

# 全量表情列表
_all_stickers: list[dict] = []

# ─────────────────────────────────────────────
# 配置读写
# ─────────────────────────────────────────────

def load_config() -> dict:
    """读取 sticker_config.json，不存在则返回默认"""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return _default_config()

def save_config(cfg: dict) -> None:
    """持久化配置到 sticker_config.json"""
    CONFIG_FILE.write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def _default_config() -> dict:
    return {
        "enable": True,
        "probability": 0.7,
        "cooldown_rounds": 2,
        "max_per_turn": 1,
        "expose_path": False,
        "emotion_priority": [
            "撒娇","卖萌","害羞","开心","生气","难过","惊讶",
            "疑惑","嫌弃","无语","害怕","思考","困","饿",
            "喵叫","坏笑","大哭","傻笑","投降","OK","恶搞"
        ]
    }

def load_cooldown() -> dict:
    """读取冷却状态"""
    if COOLDOWN_FILE.exists():
        try:
            return json.loads(COOLDOWN_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"last_file": None, "cooldown_remaining": 0}

def save_cooldown(state: dict) -> None:
    """持久化冷却状态"""
    COOLDOWN_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

# ─────────────────────────────────────────────
# 表情库加载
# ─────────────────────────────────────────────

def load_stickers() -> list[dict]:
    """从 custom_stickers.json 加载表情列表"""
    if not STICKERS_JSON.exists():
        return []
    try:
        return json.loads(STICKERS_JSON.read_text(encoding="utf-8"))
    except Exception:
        return []

def build_emotion_map(stickers: list[dict]) -> dict[str, list[dict]]:
    """
    建立情绪 → 表情列表的映射
    description 字段的文本会被模糊匹配映射到对应情绪
    """
    emotion_map: dict[str, list[dict]] = {e: [] for e in EMOTION_KEYWORDS}
    # 其余表情归入 catchall
    emotion_map["其他"] = []

    for sticker in stickers:
        desc = sticker.get("description", "").strip()
        matched = False
        desc_lower = desc.lower()
        for emotion, keywords in EMOTION_KEYWORDS.items():
            for kw in keywords:
                if kw in desc_lower or kw in desc:
                    emotion_map[emotion].append(sticker)
                    matched = True
                    break
            if matched:
                break
        if not matched:
            # 兜底：按 description 关键词猜
            if any(w in desc_lower for w in ["哭","泪","呜"]):
                emotion_map["大哭"].append(sticker)
            elif any(w in desc_lower for w in ["笑","哈","嘻嘻","嘿嘿"]):
                emotion_map["傻笑"].append(sticker)
            elif any(w in desc_lower for w in ["笨","傻","蠢","坏"]):
                emotion_map["恶搞"].append(sticker)
            elif "喵" in desc:
                emotion_map["喵叫"].append(sticker)
            else:
                emotion_map["其他"].append(sticker)

    return emotion_map

# ─────────────────────────────────────────────
# 文本情绪分析
# ─────────────────────────────────────────────

def analyze_emotion(text: str) -> list[tuple[str, float]]:
    """
    分析文本，返回 [(情绪名, 匹配分数)] 列表，按分数降序
    分数 = 关键词命中数 × 关键词权重
    """
    text_lower = text.lower()
    cfg = load_config()
    weights = cfg.get("keyword_weights", {})

    scores: dict[str, float] = {}
    priority = cfg.get("emotion_priority", list(EMOTION_KEYWORDS.keys()))

    for emotion in priority:
        keywords = EMOTION_KEYWORDS.get(emotion, [])
        score = 0.0
        for kw in keywords:
            w = weights.get(kw, 0.8)
            # 中文不用 \b，直接 in 匹配即可
            # 短关键词（1-2字）用严格包含，长关键词加权
            if kw in text_lower:
                bonus = 1.5 if len(kw) >= 3 else 1.0
                score += w * bonus
        if score > 0:
            scores[emotion] = score

    # 按分数降序排列
    sorted_scores = sorted(scores.items(), key=lambda x: -x[1])
    return sorted_scores

# ─────────────────────────────────────────────
# 表情选取（核心）
# ─────────────────────────────────────────────

def pick_sticker(
    text: str,
    probability: Optional[float] = None,
    explicit_emotion: Optional[str] = None,
    override_enable: Optional[bool] = None,
) -> dict:
    """
    主入口函数。给定一段文本，返回表情结果 dict：

    {
        "triggered": bool,       # 是否触发了表情
        "sticker": str,          # 相对路径，不暴露绝对路径
        "description": str,      # 表情描述（description 字段）
        "emotion": str,          # 匹配到的情绪
        "confidence": float,     # 置信度
        "original_text": str,    # 原始输入文本
        "message": str,          # 给用户看的输出文本（Markdown 图片格式）
        "cooldown_remaining": int,
    }

    Parameters
    ----------
    text : 输入文本
    probability : 覆盖概率阈值（0~1），None 则读配置文件
    explicit_emotion : 强制指定情绪（用于指令直接调用）
    override_enable : 覆盖开关
    """
    global _last_sticker_file, _turn_counter, _all_stickers, _emotion_stickers

    cfg = load_config()
    cfg_enable = override_enable if override_enable is not None else cfg.get("enable", True)
    prob = probability if probability is not None else cfg.get("probability", 0.7)
    cooldown_rounds = cfg.get("cooldown_rounds", 2)
    max_per_turn = cfg.get("max_per_turn", 1)

    _turn_counter += 1

    # ── Step 1: 加载表情库（惰性） ──
    if not _all_stickers:
        _all_stickers = load_stickers()
        if not _all_stickers:
            return _make_result(False, text, reason="表情库为空或加载失败")
        _emotion_stickers = build_emotion_map(_all_stickers)

    # ── Step 2: 读取冷却状态 ──
    cooldown_state = load_cooldown()
    last_file = cooldown_state.get("last_file")
    remaining_before = cooldown_state.get("cooldown_remaining", 0)
    # 轮次递减：只在冷却进行中时递减，写回文件
    if remaining_before > 0:
        cooldown_state["cooldown_remaining"] = remaining_before - 1
        # 若减到0则清 last_file，下次不再拦截
        if cooldown_state["cooldown_remaining"] == 0:
            cooldown_state["last_file"] = None
        save_cooldown(cooldown_state)

    # ── Step 3: 判断是否触发 ──
    if not cfg_enable:
        return _make_result(False, text, reason="表情功能已关闭")
    if random.random() > prob:
        return _make_result(False, text, reason=f"概率未命中({prob})")
    if remaining_before > 0 and last_file:
        return _make_result(False, text, reason=f"冷却中(剩{remaining_before}轮)")

    # ── Step 4: 情绪分析 ──
    if explicit_emotion:
        emotions = [(explicit_emotion, 1.0)]
    else:
        emotions = analyze_emotion(text)
        if not emotions:
            return _make_result(False, text, reason="未识别到情绪关键词")

    # ── Step 5: 选取情绪对应表情 ──
    chosen_sticker = None
    chosen_emotion = None
    for emotion, score in emotions:
        pool = _emotion_stickers.get(emotion, [])
        if not pool:
            continue
        # 过滤冷却中（上次用过的）
        candidates = [s for s in pool if s.get("fileName") != last_file]
        if not candidates:
            candidates = pool  # 如果全被冷却就用

        chosen = random.choice(candidates)
        chosen_sticker = chosen
        chosen_emotion = emotion
        break

    if not chosen_sticker:
        # fallback：随机选一个不是上次的
        candidates = [s for s in _all_stickers if s.get("fileName") != last_file]
        if not candidates:
            candidates = _all_stickers
        chosen_sticker = random.choice(candidates)
        chosen_emotion = "其他"

    fname = chosen_sticker["fileName"]
    desc = chosen_sticker.get("description", fname)

    # ── Step 6: 更新冷却 ──
    _last_sticker_file = fname
    cooldown_state["last_file"] = fname
    cooldown_state["cooldown_remaining"] = cooldown_rounds
    save_cooldown(cooldown_state)

    # ── Step 7: 构造输出 ──
    # sticker_path: 完整绝对路径（供 <qqmedia> 标签使用）
    sticker_path = str(STICKERS_DIR / fname)
    # sticker_rel: 相对路径（用于 markdown 图片格式）
    sticker_rel = f"./{fname}"
    # message: 纯文本回复（不含图片，调用方自行拼接媒体）
    message = text

    return {
        "triggered": True,
        "sticker_path": sticker_path,   # 完整路径 → 用于 <qqmedia> 标签
        "sticker_rel": sticker_rel,     # 相对路径 → 用于 markdown 图片
        "fileName": fname,
        "description": desc,
        "emotion": chosen_emotion,
        "confidence": round(emotion_score(emotions, chosen_emotion), 3),
        "original_text": text,
        "message": message,             # 纯文本，调用方自行拼接图片
        "cooldown_remaining": cooldown_rounds,
        "last_file": fname,
    }

def emotion_score(emotions: list[tuple[str, float]], emotion: str) -> float:
    """获取某情绪的分数（归一化）"""
    if not emotions:
        return 0.0
    top = emotions[0][1] if emotions else 1.0
    for e, s in emotions:
        if e == emotion:
            return s / top if top > 0 else 0.0
    return 0.0

def _make_result(triggered: bool, text: str, reason: str = "") -> dict:
    return {
        "triggered": triggered,
        "sticker": None,
        "fileName": None,
        "description": None,
        "emotion": None,
        "confidence": 0.0,
        "original_text": text,
        "message": text if not triggered else "",
        "cooldown_remaining": 0,
        "last_file": None,
        "reason": reason,
    }

# ─────────────────────────────────────────────
# 指令解析（供外部调用）
# ─────────────────────────────────────────────

def parse_command(text: str) -> Optional[dict]:
    """
    解析用户指令，返回 {action, args} 或 None
    支持格式：
      表情开关 开/关
      表情概率 0.8
      表情冷却 3
      表情列表
      表情帮助
    """
    text = text.strip()
    m = re.match(r'^表情(开关|概率|冷却|列表|帮助)', text)
    if not m:
        return None
    cmd = m.group(1)
    args = text[len(m.group(0)):].strip()

    if cmd == "开关":
        if args in ("开", "启用", "on", "ON"):
            return {"action": "set_enable", "value": True}
        if args in ("关", "禁用", "off", "OFF"):
            return {"action": "set_enable", "value": False}
        return {"action": "error", "msg": "开关参数需为：开/关/on/off"}
    if cmd == "概率":
        try:
            v = float(args)
            if not (0 <= v <= 1):
                return {"action": "error", "msg": "概率需在 0~1 之间"}
            return {"action": "set_probability", "value": v}
        except ValueError:
            return {"action": "error", "msg": "概率值无效"}
    if cmd == "冷却":
        try:
            v = int(args)
            if v < 0:
                return {"action": "error", "msg": "冷却轮数需 ≥ 0"}
            return {"action": "set_cooldown", "value": v}
        except ValueError:
            return {"action": "error", "msg": "冷却轮数需为整数"}
    if cmd == "列表":
        return {"action": "list"}
    if cmd == "帮助":
        return {"action": "help"}

def handle_command(text: str) -> dict:
    """解析并执行指令，返回结果 dict"""
    cmd_info = parse_command(text)
    if not cmd_info:
        return {}

    action = cmd_info["action"]
    cfg = load_config()

    if action == "set_enable":
        cfg["enable"] = cmd_info["value"]
        save_config(cfg)
        state = "开启" if cmd_info["value"] else "关闭"
        return {"ok": True, "reply": f"表情功能已{state}喵~"}
    if action == "set_probability":
        cfg["probability"] = cmd_info["value"]
        save_config(cfg)
        return {"ok": True, "reply": f"表情触发概率已调整为 {cmd_info['value']*100:.0f}% 喵~"}
    if action == "set_cooldown":
        cfg["cooldown_rounds"] = cmd_info["value"]
        save_config(cfg)
        return {"ok": True, "reply": f"冷却轮数已调整为 {cmd_info['value']} 喵~"}
    if action == "list":
        stickers = load_stickers()
        # 按情绪分组
        emap = build_emotion_map(stickers)
        lines = ["**表情库内容喵~**\n"]
        for e, ss in emap.items():
            if ss:
                names = ", ".join(f"`{s['description']}`" for s in ss[:5])
                if len(ss) > 5:
                    names += f" ...(共{len(ss)}张)"
                lines.append(f"**{e}** ({len(ss)}张): {names}")
        return {"ok": True, "reply": "\n".join(lines)}
    if action == "help":
        help_text = """**表情包指令帮助喵~**

- `表情开关 开` / `表情开关 关` — 开启/关闭表情
- `表情概率 0.8` — 设置触发概率（0~1）
- `表情冷却 3` — 设置冷却轮数（发完隔几轮才能再发）
- `表情列表` — 查看所有可用表情
- `表情帮助` — 显示本帮助

**正常使用时**：直接说你的感受，夜玖会自动配上表情喵！"""
        return {"ok": True, "reply": help_text}
    if action == "error":
        return {"ok": False, "reply": f"指令错误：{cmd_info['msg']}"}
    return {}

# ─────────────────────────────────────────────
# 主入口（CLI 测试）
# ─────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 cat_sticker_skill.py <文本> [--force-emotion=情绪]")
        sys.exit(0)

    text = sys.argv[1]
    emotion = None
    for arg in sys.argv[2:]:
        if arg.startswith("--force-emotion="):
            emotion = arg.split("=", 1)[1]

    result = pick_sticker(text, explicit_emotion=emotion)
    print(json.dumps(result, ensure_ascii=False, indent=2))
