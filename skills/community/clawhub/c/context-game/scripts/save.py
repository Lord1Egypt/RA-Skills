#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
save.py — 《上下文》存档引擎（纯 Python 3 标准库，Windows 兼容）

SKILL.md 的铁律：state.json 只能通过本脚本写入。本脚本负责：
  schema 校验 → .bak 备份 → 临时文件 + os.replace 原子写。

子命令一览
  init        --slot NAME                       初始化新档（state.json + memory.md 骨架）
  update      --slot NAME --payload FILE|-      校验并原子写入 state.json（FILE 为 - 时读 stdin）
  roll        --slot NAME --difficulty N --modifier N --reason TEXT [--label TEXT]
                                                掷骰判定，结果追加到 rolls.jsonl
  pressure    --slot NAME [--table TEXT]        世界压力掷表：确定性 d100，追加到 rolls.jsonl
  validate    --slot NAME                       校验存档完整性
  world-init  --slot NAME --payload FILE        校验自定义世界骨架并落盘为该档 world.json
  archive     --slot NAME [--summary FILE|-]    活跃区事件段写入 archives/NNN.md，
                                                若提供 --summary 则用其替换压缩区文本

roll 参数契约
  --difficulty N   必填 int，必须 ∈ {40, 60, 75, 90}（rules.md §2 四档白名单）。不在集合内
                   直接报错退出，不落盘。禁止自创档位——难度只反映客观困难度，四档为：
                   常规=40 / 困难=60 / 极高=75 / 近乎不可能=90；
                   真正的琐碎行动不应掷骰（不产生判定）。
  --modifier N     必填 int。修正值 = 关系资本 + 情报优势 + NPC 态度修正（见 rules.md §2），
                   由裁决者按涉事对象逐项算出，不是凭感觉填的常数。
  --reason TEXT    必填 str。说明本次判定的难度档位选择依据与修正值来源（须可追溯），
                   原样写入记录 reason 字段，供事后审计"是否照章判定"。
                   合法示例：难度=困难60(说服戒备者)；修正=+8 阿庚trust98 + 0 NPC态度
  --label TEXT     可选 str。简短叙事标签（写入记录 label 字段）。

pressure 参数契约（世界压力掷表，非成败判定）
  --slot NAME      必填。该档 state.json 提供 clock。
  --table TEXT     可选。压力表标识；缺省为空串。
  行为：返回确定性 d100，取值 1..100（与 roll 的 base 同域）。
        种子 = sha256(f"{slot}|pressure|{n_prior+1}|{clock.day}|{clock.hour}")，
        n_prior = 该档 rolls.jsonl 现有非空行数 → 同档同回合可复现、不同回合必不同。
        pressure 不受 roll 的 difficulty 下限约束（它只查表，不判成败）。

rolls.jsonl 记录 schema（JSONL，每行一条，只追加）
  所有记录共有：n(int,自增序号) / seed(str,种子原文) / seed_hash(int) /
                clock(dict) / ts(str,UTC ISO8601) / kind(str)
  kind="roll"      ：difficulty / modifier / base(1..100) / total / margin /
                     success(bool) / fortune(str) / label(str) / reason(str,必填)
  kind="pressure"  ：d100(1..100) / table(str,可为空)
  字段顺序：既有字段顺序保持不变，新字段（kind/reason）一律追加在记录尾部。

roll/pressure 结果记录位置（设计决策）：写入 saves/<slot>/rolls.jsonl（JSONL，每行一条），
不塞进 state.json —— 保持 state.json 六字段账本纯净，rolls.jsonl 只追加不修改，
天然满足"前缀稳定"的缓存纪律。

state.json 顶层字段固定顺序（紧凑 JSON，无缩进，追加字段挂尾部）：
  1 player      dict  {name, identity, background?, ...}
  2 location    str   当前所在（"名字即契约"：必须与 relations 中实体名一致）
  3 clock       dict  {day: int, hour: int}   游戏内时间，day 从 1 起，hour 0-23
  4 relations   dict  {实体名: {type: npc|faction, attitude: int(-100..100),
                        trust: int(0..100), standing: str, secrets: [str],
                        leverage: [str], notes: str}}
                      实体上限 100 个，超出必须归档
  5 flags       dict  {布尔/数值标记: bool|int|float|str}
                       # 悬疑局保留键（完整清单与语义见 rules/suspicion.md §6.2）：
                       #   闸门 suspicion_last_end_day(int)/suspicion_count_this_year(int)/
                       #        suspicion_year(int)/suspicion_last_faction(str)
                       #   运行态 suspicion_faction(str)/suspicion_phase(str)/suspicion_start_day(int)/
                       #          suspicion_window_left(int)/suspicion_traces(int)
                       #   线索与身份 clue_<slug>(bool)/player_hidden_role(str)
  6 events      list  [{id, name, status: open|closed|dormant, tension: int(0..100),
                        summary, due_clock?}]
  *尾部可追加额外字段（如 mode, world_ref, created_at, retired, dead），顺序保持首次出现。

实体上限规则：len(relations) > 100 时 update 拒绝写入，提示先调用 archive / 归档。

退出码：0 成功；1 用法或输入错误；2 校验失败（stderr 给出原因，stdout 不污染）。
所有输出统一为单行 JSON（ensure_ascii=False），便于 agent 直接解析。
"""

import argparse
import hashlib
import json
import os
import random
import sys
import tempfile
from datetime import datetime, timezone

# ---------------------------------------------------------------- 常量与路径

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # skill/
SAVES_DIR = os.path.join(BASE_DIR, "saves")

FIELD_ORDER = ["player", "location", "clock", "relations", "flags", "events"]
ENTITY_CAP = 100
# roll 难度白名单（rules.md §2 四档）：只允许这四档，禁止自创档位。
# 难度只反映客观困难度；四档名称见 DIFFICULTY_TIERS，用于报错指引。
DIFFICULTY_TIERS = {40: "常规", 60: "困难", 75: "极高", 90: "近乎不可能"}
DIFFICULTY_ALLOWED = tuple(sorted(DIFFICULTY_TIERS))
ACTIVE_EVENT_CAP = 30          # memory.md 活跃区条目上限（软提示，由 agent 遵守）
MEMORY_SUMMARY_CAP = 500       # memory.md 压缩区字数上限（软提示）
ENGINE_TAIL_FIELDS = {"created_at", "updated_at", "mode", "world_ref", "retired"}
# 注：死亡档标记 dead（SKILL.md §8）属"允许的尾部额外字段"，但不在本集合内——
# 它会触发"额外字段将追加到尾部"的警告（警告级，不拒写），故无需加入本集合。

STATE_SCHEMA_DOC = """
state.json 顶层 schema（固定顺序）：
  player    : dict   必填。name/identity 至少存在。
  location  : str    必填。非空。
  clock     : dict   必填。{day:int>=1, hour:int 0..23}
  relations : dict   必填。<=100 个实体；每个实体至少含 type 字段，
                     type ∈ {npc, faction}；attitude int -100..100；trust int 0..100。
  flags     : dict   必填。值为 bool/int/float/str。
  events    : list   必填。每项为 dict，含 id(str), name(str),
                     status ∈ {open, closed, dormant}, tension int 0..100。
尾部允许追加任意额外字段（不得与以上六键冲突）。
"""

WORLD_SCHEMA_DOC = """
world.json（自定义世界）schema：
  meta           : dict   {name: str, version: int,
                           tone_family?: str（新字段，见 world-gen-protocol.md §3）,
                           tone_variant?: str（新字段，1-6 字题材变体标签）,
                           tone?: str（旧字段，仅兼容；等价于 tone_family）}
                          必须有 tone_family 或 tone 之一，否则视为硬科幻默认基调
  continents     : list   1..2 项。每项 {id, name, summary}
  nations        : list   4..6 项。每项 {id, name, continent, summary,
                                  tension_seeds: list 2..3 项 str}
  neutral_port   : dict   {id, name, continent, summary}（必须恰好 1 个）
  faction_matrix : dict   {"A|B": {"relation": int -100..100, "note": str}}
                          A、B 必须是 nations ∪ {neutral_port.id} 中的 id；
                          所有 pair 的 relation 值两两互不相同（非对称规则）；
                          无向对只写一次（按 id 字典序，A|B 且 A<B）。
"""

# tone_family 允许的枚举值（见 world-gen-protocol.md §3）。
# 保留 hard-sci-fi-political-thriller 作为硬科幻题材与旧档兼容值。
TONE_FAMILIES = {
    "hard-sci-fi-political-thriller",  # 硬科幻政治惊悚（硬科幻题材 + 兼容旧档）
    "modern-urban",                     # 现代都市
    "military",                         # 军事
    "mystery",                          # 悬疑
    "corporate-war",                    # 商战
    "campus",                           # 校园
    "romance",                          # 情感
    "isekai",                           # 穿越
    "cultivation",                      # 修仙
    "closed-circle",                    # 封闭囚笼
    "court-intrigue",                   # 宫廷权谋
    "apocalypse",                       # 末日废土
    "espionage",                        # 谍战
    "wuxia",                            # 江湖武侠
}

def fortune_word(margin):
    """按 margin 映射运势描述词：惨败/失败/勉强成功/成功/意外转机。"""
    if margin <= -30:
        return "惨败"
    if margin < 0:
        return "失败"
    if margin < 10:
        return "勉强成功"
    if margin < 25:
        return "成功"
    return "意外转机"

# ---------------------------------------------------------------- 工具函数


def _setup_stdout():
    """Windows 控制台避免 GBK 乱码：强制 utf-8，失败则静默降级。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def out(payload):
    print(json.dumps(payload, ensure_ascii=False))


def fail(msg, code=2):
    sys.stderr.write(json.dumps({"ok": False, "error": msg}, ensure_ascii=False) + "\n")
    sys.exit(code)


def slot_dir(slot):
    if not slot or any(ch in slot for ch in '/\\:*?"<>|'):
        fail("非法槽位名: %r（不得含路径分隔符等字符）" % slot, 1)
    return os.path.join(SAVES_DIR, slot)


def slot_paths(slot):
    d = slot_dir(slot)
    return {
        "dir": d,
        "state": os.path.join(d, "state.json"),
        "memory": os.path.join(d, "memory.md"),
        "rolls": os.path.join(d, "rolls.jsonl"),
        "world": os.path.join(d, "world.json"),
        "archives": os.path.join(d, "archives"),
    }


def atomic_write(path, text):
    """临时文件 + os.replace 原子写（同目录，保证同分区 replace）。"""
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def backup(path):
    """把旧档复制为 .bak（覆盖旧 .bak）。"""
    if os.path.exists(path):
        bak = path + ".bak"
        with open(path, "rb") as src, open(bak, "wb") as dst:
            dst.write(src.read())


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_payload(path):
    """--payload FILE，FILE 为 '-' 时读 stdin。"""
    if path == "-":
        return sys.stdin.read()
    if not os.path.isfile(path):
        fail("payload 文件不存在: %s" % path, 1)
    return read_text(path)


def require_slot(slot, kind="state"):
    p = slot_paths(slot)
    target = p[kind]
    if not os.path.isfile(target):
        fail("存档不存在: %s（先执行 init）" % target, 1)
    return p


# ---------------------------------------------------------------- state 校验


def _check_state(data):
    """返回 (重排后的 dict, 警告列表)；失败抛 ValueError。"""
    warns = []
    if not isinstance(data, dict):
        raise ValueError("state 顶层必须是 JSON 对象")
    for key in FIELD_ORDER:
        if key not in data:
            raise ValueError("缺少必填字段: %s" % key)
    unknown_first = [k for k in data if k not in FIELD_ORDER]
    for k in unknown_first:
        if k not in ENGINE_TAIL_FIELDS:
            warns.append("额外字段 %r 将追加到尾部" % k)

    player = data["player"]
    if not isinstance(player, dict) or "name" not in player:
        raise ValueError("player 必须是含 name 键的对象")
    if not player.get("name"):
        warns.append("player.name 为空（新档骨架可接受，开局流程应尽快补写）")
    if not isinstance(data["location"], str):
        raise ValueError("location 必须是字符串")
    if not data["location"].strip():
        warns.append("location 为空（新档骨架可接受，开局流程应尽快补写）")
    clock = data["clock"]
    if not (isinstance(clock, dict) and isinstance(clock.get("day"), int)
            and clock["day"] >= 1 and isinstance(clock.get("hour"), int)
            and 0 <= clock["hour"] <= 23):
        raise ValueError("clock 必须是 {day:int>=1, hour:0..23}")

    relations = data["relations"]
    if not isinstance(relations, dict):
        raise ValueError("relations 必须是对象")
    if len(relations) > ENTITY_CAP:
        raise ValueError("relations 实体数 %d 超上限 %d，请先归档"
                         % (len(relations), ENTITY_CAP))
    for name, rel in relations.items():
        if not isinstance(rel, dict):
            raise ValueError("relations[%r] 必须是对象" % name)
        if rel.get("type") not in ("npc", "faction"):
            raise ValueError("relations[%r].type 必须是 npc 或 faction" % name)
        att = rel.get("attitude", 0)
        tru = rel.get("trust", 0)
        if not isinstance(att, int) or not -100 <= att <= 100:
            raise ValueError("relations[%r].attitude 必须是 -100..100 的整数" % name)
        if not isinstance(tru, int) or not 0 <= tru <= 100:
            raise ValueError("relations[%r].trust 必须是 0..100 的整数" % name)
    if data["location"] not in relations and relations:
        warns.append("location %r 不在 relations 中（可为新地点，但专名产生后应尽快登记）"
                     % data["location"])

    flags = data["flags"]
    if not isinstance(flags, dict):
        raise ValueError("flags 必须是对象")
    for k, v in flags.items():
        if not isinstance(v, (bool, int, float, str)):
            raise ValueError("flags[%r] 值类型必须是 bool/int/float/str" % k)

    events = data["events"]
    if not isinstance(events, list):
        raise ValueError("events 必须是数组")
    if len(events) > ACTIVE_EVENT_CAP:
        warns.append("events %d 条超过建议上限 %d，建议归档" % (len(events), ACTIVE_EVENT_CAP))
    seen_ids = set()
    for ev in events:
        if not isinstance(ev, dict):
            raise ValueError("events 每项必须是对象")
        for req in ("id", "name", "status", "tension"):
            if req not in ev:
                raise ValueError("events 项缺少字段: %s" % req)
        if ev["status"] not in ("open", "closed", "dormant"):
            raise ValueError("events[%s].status 非法: %r" % (ev["id"], ev["status"]))
        if not isinstance(ev["tension"], int) or not 0 <= ev["tension"] <= 100:
            raise ValueError("events[%s].tension 必须是 0..100 的整数" % ev["id"])
        if ev["id"] in seen_ids:
            raise ValueError("events id 重复: %s" % ev["id"])
        seen_ids.add(ev["id"])
    return data, warns


def reorder_state(data):
    """六字段按固定顺序排前，其余按原出现顺序追加尾部。"""
    ordered = {k: data[k] for k in FIELD_ORDER}
    for k in data:
        if k not in FIELD_ORDER:
            ordered[k] = data[k]
    return ordered


# ---------------------------------------------------------------- world 校验


def _check_world(data):
    """校验自定义世界骨架，失败抛 ValueError。"""
    if not isinstance(data, dict):
        raise ValueError("world 顶层必须是 JSON 对象")
    for key in ("meta", "continents", "nations", "neutral_port", "faction_matrix"):
        if key not in data:
            raise ValueError("world 缺少字段: %s" % key)

    meta = data["meta"]
    if not isinstance(meta, dict) or not meta.get("name"):
        raise ValueError("meta 必须是含 name 的对象")

    # tone 兼容：新档用 tone_family + tone_variant；旧档用 tone（单字符串）。
    # 两者都给：tone_family 优先，tone_variant 保留。
    # 两者都不给：默认为硬科幻（硬科幻题材兼容值），保持向后兼容。
    tf = meta.get("tone_family")
    tv = meta.get("tone_variant")
    legacy_tone = meta.get("tone")
    if tf is not None:
        if not isinstance(tf, str) or tf not in TONE_FAMILIES:
            raise ValueError("meta.tone_family 必须是 %s 之一" % "/".join(sorted(TONE_FAMILIES)))
        if tv is not None and (not isinstance(tv, str) or not tv.strip()):
            raise ValueError("meta.tone_variant 必须是非空字符串")
    elif legacy_tone is not None:
        # 旧档兼容：把 tone 提升到 tone_family；若 tone 值不在枚举中（自定义题材），警告但不拦
        if not isinstance(legacy_tone, str):
            raise ValueError("meta.tone 必须是字符串")
    # 都不提供：允许（默认视为硬科幻，不强制报错，兼容最早期裸 meta 的世界骨架）

    continents = data["continents"]
    if not isinstance(continents, list) or not 1 <= len(continents) <= 2:
        raise ValueError("continents 必须 1..2 项")
    cont_ids = set()
    for c in continents:
        if not isinstance(c, dict) or not c.get("id") or not c.get("name"):
            raise ValueError("continent 项必须含 id 与 name")
        cont_ids.add(c["id"])

    nations = data["nations"]
    if not isinstance(nations, list) or not 4 <= len(nations) <= 6:
        raise ValueError("nations 必须 4..6 项")
    nation_ids = []
    for n in nations:
        if not isinstance(n, dict) or not n.get("id") or not n.get("name"):
            raise ValueError("nation 项必须含 id 与 name")
        if n.get("continent") not in cont_ids:
            raise ValueError("nation %r 的 continent 不在 continents 中" % n["id"])
        seeds = n.get("tension_seeds")
        if not isinstance(seeds, list) or not 2 <= len(seeds) <= 3 \
                or not all(isinstance(s, str) and s.strip() for s in seeds):
            raise ValueError("nation %r 的 tension_seeds 必须 2..3 条非空字符串" % n["id"])
        nation_ids.append(n["id"])

    np_ = data["neutral_port"]
    if not isinstance(np_, dict) or not np_.get("id") or not np_.get("name"):
        raise ValueError("neutral_port 必须含 id 与 name")
    if np_.get("continent") not in cont_ids:
        raise ValueError("neutral_port 的 continent 不在 continents 中")

    entities = nation_ids + [np_["id"]]
    if len(set(entities)) != len(entities):
        raise ValueError("实体 id 重复")

    matrix = data["faction_matrix"]
    if not isinstance(matrix, dict) or not matrix:
        raise ValueError("faction_matrix 必须是非空对象")
    seen_pairs = set()
    values = []
    for key, val in matrix.items():
        if not isinstance(key, str) or "|" not in key:
            raise ValueError("faction_matrix 键必须是 'A|B' 形式: %r" % key)
        a, b = key.split("|", 1)
        if a not in entities or b not in entities:
            raise ValueError("faction_matrix %r 含未知实体 id" % key)
        if a == b:
            raise ValueError("faction_matrix 不允许自指: %r" % key)
        pair = tuple(sorted((a, b)))
        if pair in seen_pairs:
            raise ValueError("faction_matrix 重复对（无向对只写一次）: %r" % key)
        seen_pairs.add(pair)
        if not isinstance(val, dict) or not isinstance(val.get("relation"), int) \
                or not -100 <= val["relation"] <= 100:
            raise ValueError("faction_matrix[%r].relation 必须是 -100..100 的整数" % key)
        values.append(val["relation"])
    if len(set(values)) != len(values):
        raise ValueError("faction_matrix 非对称校验失败：relation 值必须两两互不相同")
    return data


# ---------------------------------------------------------------- 子命令


def cmd_init(args):
    p = slot_paths(args.slot)
    if os.path.exists(p["state"]):
        fail("槽位已存在: %s（用其他名字，或先手动清理）" % args.slot, 1)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    state = {
        "player": {"name": "", "identity": ""},
        "location": "",
        "clock": {"day": 1, "hour": 8},
        "relations": {},
        "flags": {},
        "events": [],
        "mode": args.mode,
        "created_at": now,
        "updated_at": now,
    }
    ordered = reorder_state(state)
    atomic_write(p["state"], json.dumps(ordered, ensure_ascii=False,
                                        separators=(",", ":")))
    memory = (
        "# 故事至今（压缩区，<=500 字）\n\n（尚未开始。开局后由 agent 撰写。）\n\n"
        "# 近期事件（活跃区，<=30 条）\n\n（尚无记录。开局后在此追加 `- 【day X hh:00】事件描述`。）\n"
    )
    atomic_write(p["memory"], memory)
    os.makedirs(p["archives"], exist_ok=True)
    out({"ok": True, "slot": args.slot, "state": p["state"], "memory": p["memory"]})


def cmd_update(args):
    p = require_slot(args.slot)
    raw = read_payload(args.payload)
    try:
        data = json.loads(raw)
    except ValueError as e:
        fail("payload 不是合法 JSON: %s" % e)
    try:
        _, warns = _check_state(data)
    except ValueError as e:
        fail("校验失败: %s" % e)
    ordered = reorder_state(data)
    ordered["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    backup(p["state"])
    atomic_write(p["state"], json.dumps(ordered, ensure_ascii=False,
                                        separators=(",", ":")))
    out({"ok": True, "slot": args.slot, "warnings": warns,
         "entities": len(ordered["relations"]), "path": p["state"]})


def _require_difficulty(difficulty):
    """roll 难度硬校验：必须取自 rules.md §2 四档白名单 {40,60,75,90}，否则报错退出。

    难度只反映客观困难度，四档为：
    常规=40 / 困难=60 / 极高=75 / 近乎不可能=90。
    禁止自创档位（如 45/50/88）——把"只写文档"变成"硬校验"，防止约束漂移。
    真正的琐碎行动不应掷骰（不产生判定）。
    """
    if difficulty not in DIFFICULTY_TIERS:
        ladder = " / ".join("%d(%s)" % (v, DIFFICULTY_TIERS[v]) for v in DIFFICULTY_ALLOWED)
        fail("错误：--difficulty 必须取四档之一：%s；当前 %s。禁止自创档位——"
             "难度只反映客观困难度。" % (ladder, difficulty), 1)


def _require_reason(reason):
    """roll 修正值可追溯硬校验：--reason 必填且非空。"""
    if reason is None or not str(reason).strip():
        fail("错误：roll 必须提供 --reason，说明修正值来源（关系资本/情报优势/NPC态度）"
             "与难度档位依据，禁止填 0 了事。合法示例："
             "--reason \"难度=困难60(说服戒备者)；修正=+8 阿庚trust98 + 0 NPC态度\"", 1)


def _count_rolls(path):
    """统计 rolls.jsonl 现有非空行数（不存在则为 0）。"""
    if not os.path.isfile(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def cmd_roll(args):
    p = require_slot(args.slot)
    _require_difficulty(args.difficulty)
    _require_reason(args.reason)
    with open(p["state"], "r", encoding="utf-8") as f:
        state = json.load(f)
    n_prior = _count_rolls(p["rolls"])
    clock = state.get("clock", {})
    seed_str = "%s|%d|%d|%d|%d|%d" % (args.slot, n_prior + 1, args.difficulty,
                                      args.modifier, clock.get("day", 1),
                                      clock.get("hour", 0))
    seed = int(hashlib.sha256(seed_str.encode("utf-8")).hexdigest()[:12], 16)
    rng = random.Random(seed)
    base = rng.randint(1, 100)
    total = base + args.modifier
    margin = total - args.difficulty
    success = margin >= 0
    fortune = fortune_word(margin)
    record = {
        "n": n_prior + 1, "seed": seed_str, "seed_hash": seed,
        "difficulty": args.difficulty, "modifier": args.modifier,
        "base": base, "total": total, "margin": margin,
        "success": success, "fortune": fortune,
        "clock": dict(clock), "label": args.label or "",
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "kind": "roll", "reason": args.reason,
    }
    os.makedirs(p["dir"], exist_ok=True)
    with open(p["rolls"], "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    record["ok"] = True
    out(record)


def cmd_pressure(args):
    """世界压力掷表：确定性 d100（1..100），追加一条 kind="pressure" 记录。

    与 roll 同构的种子算法（保证同档同回合可复现、不同回合必不同），
    但不做难度校验——它不是成败判定，只是查"世界随机压力表"。
    """
    p = require_slot(args.slot)
    with open(p["state"], "r", encoding="utf-8") as f:
        state = json.load(f)
    n_prior = _count_rolls(p["rolls"])
    clock = state.get("clock", {})
    n = n_prior + 1
    seed_str = "%s|pressure|%d|%d|%d" % (args.slot, n, clock.get("day", 1),
                                         clock.get("hour", 0))
    seed = int(hashlib.sha256(seed_str.encode("utf-8")).hexdigest()[:12], 16)
    rng = random.Random(seed)
    d100 = rng.randint(1, 100)
    table = args.table or ""
    record = {
        "n": n, "seed": seed_str, "seed_hash": seed,
        "d100": d100, "table": table,
        "clock": dict(clock),
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "kind": "pressure",
    }
    os.makedirs(p["dir"], exist_ok=True)
    with open(p["rolls"], "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    record["ok"] = True
    out(record)


def cmd_validate(args):
    p = require_slot(args.slot)
    try:
        data = json.loads(read_text(p["state"]))
        _, warns = _check_state(data)
    except ValueError as e:
        fail("state.json 校验失败: %s" % e)
    result = {"ok": True, "slot": args.slot, "warnings": warns,
              "has_world": os.path.isfile(p["world"]),
              "has_memory": os.path.isfile(p["memory"]),
              "rolls_recorded": 0}
    if os.path.isfile(p["rolls"]):
        with open(p["rolls"], "r", encoding="utf-8") as f:
            result["rolls_recorded"] = sum(1 for line in f if line.strip())
    out(result)


def cmd_world_init(args):
    p = slot_paths(args.slot)
    if not os.path.isfile(p["state"]):
        fail("槽位不存在: %s（先 init 再 world-init）" % args.slot, 1)
    raw = read_payload(args.payload)
    try:
        data = json.loads(raw)
    except ValueError as e:
        fail("payload 不是合法 JSON: %s" % e)
    try:
        _check_world(data)
    except ValueError as e:
        fail("世界骨架校验失败: %s" % e)
    backup(p["world"]) if os.path.isfile(p["world"]) else None
    atomic_write(p["world"], json.dumps(data, ensure_ascii=False,
                                        separators=(",", ":")))
    out({"ok": True, "slot": args.slot, "world": p["world"],
         "nations": len(data["nations"]), "pairs": len(data["faction_matrix"])})


def cmd_archive(args):
    p = require_slot(args.slot)
    text = read_text(p["memory"])
    lines = text.splitlines()
    mode, compressed, active = None, [], []
    for ln in lines:
        if ln.startswith("# 故事至今"):
            mode = "c"; continue
        if ln.startswith("# 近期事件"):
            mode = "a"; continue
        (compressed if mode == "c" else active if mode == "a" else []).append(ln)
    active_entries = [ln for ln in active if ln.strip()]
    if not active_entries:
        fail("活跃区没有可归档条目")
    os.makedirs(p["archives"], exist_ok=True)
    n = len([f for f in os.listdir(p["archives"]) if f.endswith(".md")]) + 1
    seg_name = "%03d.md" % n
    header = ("# 归档段 %03d（slot=%s，归档于 %s）\n\n以下为活跃区滚动压缩前的原始条目：\n"
              % (n, args.slot, datetime.now(timezone.utc).strftime("%Y-%m-%d")))
    seg_text = header + "\n".join(active_entries).rstrip() + "\n"
    atomic_write(os.path.join(p["archives"], seg_name), seg_text)

    if args.summary and args.summary != "-":
        new_summary = read_payload(args.summary).strip()
    elif args.summary == "-":
        new_summary = sys.stdin.read().strip()
    else:
        new_summary = None
    if new_summary is not None:
        compressed = ["", new_summary, ""]
    seg_note = "\n（更早的记录见 archives/ 目录，共 %d 段。）\n" % n
    memory = ("# 故事至今（压缩区，<=500 字）\n%s\n"
              "# 近期事件（活跃区，<=30 条）\n\n（归档后暂无新事件，按 SKILL.md 格式追加。）%s"
              % ("\n".join(compressed).strip() + "\n", seg_note))
    backup(p["memory"])
    atomic_write(p["memory"], memory)
    out({"ok": True, "slot": args.slot, "segment": seg_name,
         "entries_archived": len(active_entries),
         "summary_replaced": new_summary is not None,
         "memory": p["memory"]})


# ---------------------------------------------------------------- 入口


def main():
    _setup_stdout()
    ap = argparse.ArgumentParser(prog="save.py", description="《上下文》存档引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="初始化新档")
    s.add_argument("--slot", required=True)
    s.add_argument("--mode", default="official", choices=["official", "custom"])
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("update", help="校验并原子写入 state.json")
    s.add_argument("--slot", required=True)
    s.add_argument("--payload", required=True, help="JSON 文件路径，或 - 读 stdin")
    s.set_defaults(func=cmd_update)

    s = sub.add_parser("roll", help="掷骰判定（难度四档 40/60/75/90，--reason 必填）")
    s.add_argument("--slot", required=True)
    s.add_argument("--difficulty", type=int, required=True,
                   help="判定难度，必须 ∈ {40,60,75,90}（rules.md §2 四档，禁止自创档位）")
    s.add_argument("--modifier", type=int, required=True,
                   help="修正值（关系资本+情报优势+NPC态度，见 rules.md §2）")
    s.add_argument("--reason", default=None,
                   help="必填：难度档位依据 + 修正值来源（可追溯，禁止填 0 了事）")
    s.add_argument("--label", default="", help="本次判定的说明（写入日志）")
    s.set_defaults(func=cmd_roll)

    s = sub.add_parser("pressure", help="世界压力掷表：确定性 d100（1..100）")
    s.add_argument("--slot", required=True)
    s.add_argument("--table", default="", help="压力表标识（可为空）")
    s.set_defaults(func=cmd_pressure)

    s = sub.add_parser("validate", help="校验存档完整性")
    s.add_argument("--slot", required=True)
    s.set_defaults(func=cmd_validate)

    s = sub.add_parser("world-init", help="校验自定义世界骨架并落盘")
    s.add_argument("--slot", required=True)
    s.add_argument("--payload", required=True)
    s.set_defaults(func=cmd_world_init)

    s = sub.add_parser("archive", help="活跃区归档 + 压缩区滚动合并")
    s.add_argument("--slot", required=True)
    s.add_argument("--summary", default=None,
                   help="新压缩区文本文件（或 - 读 stdin）；省略则保留原压缩区")
    s.set_defaults(func=cmd_archive)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
