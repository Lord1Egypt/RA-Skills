# -*- coding: utf-8 -*-
"""参考资料读取核心库（纯标准库实现，供 scripts/ 内部调用）。

本技能 `references/` 目录下的 6 份参考资料以专用容器格式存放，**不能用普通文件
读取工具直接打开**，必须经本模块还原后才能使用；命令行入口见 `scripts/ref_reader.py`。

对外接口
--------
    REF_ITEMS          参考资料清单 [(名称, 一句话说明), ...]
    RefError           读取失败异常，异常消息可直接展示给使用者
    RefMissing         参考资料文件不存在
    list_names()       全部参考资料名称
    exists(name)       某份资料是否存在
    read_text(name)    还原为 JSON 文本
    load(name)         还原并解析为 dict
    to_markdown(data)  把资料结构渲染为 Markdown 文本，便于阅读
    pack(plain_text)   把 JSON 文本装进容器 dict（维护资料时使用，运行期无需调用）
"""
import base64
import hashlib
import json
import os
import sys

# ---------------------------------------------------------------- 基础常量

TAG = "bld-ref"          # 容器标识
REV = 1                  # 容器版本
ROUNDS = 200000          # 参数推导迭代轮数
KEY_BYTES = 32           # 数据变换参数长度
CHECK_BYTES = 32         # 校验值长度
BLOCK_BYTES = 16
MIN_ROUNDS = 1000
MAX_ROUNDS = 2000000

REFERENCES_DIRNAME = "references"

# 参考资料清单：（名称, 一句话说明）
REF_ITEMS = [
    ("methodology",
     "整门课程 / 一课次各栏内容撰写方法论、教学日历填写规则（写内容前必读，按需分节查阅）"),
    ("bloom_reference",
     "布卢姆教育目标分类学（2001 修订版）行为动词表、知识类型与二维呈现规则（写学习目标时查阅）"),
    ("design_plan_guide",
     "design_data.json 的顶层结构、字段与模版对应关系、交互点格式与填写要点（写 JSON 前查阅）"),
    ("faq",
     "常见报错速查（现象 → 一句话修复）与常见问题解答（报错或使用者提问时查阅）"),
    ("output_preview",
     "四类产物的文件名、版面结构、HTML/PPT 页序、成品片段与生成后核对清单（想了解生成效果时查阅）"),
    ("footer_note",
     "四类产物文末 / 末页统一原样插入的固定说明文字（由脚本自动附带，可按需调整内容）"),
]

REF_NAMES = tuple(name for name, _ in REF_ITEMS)


class RefError(Exception):
    """参考资料读取失败；消息为面向使用者的中文提示。"""


class RefMissing(RefError):
    """参考资料文件不存在。"""


# ---------------------------------------------------------------- 分组变换
# 说明：以下函数实现对 16 字节分组做可逆变换，仅用于本技能的参考资料容器，
# 与 Python 标准库组合使用，不引入任何第三方依赖。

def _build_tables():
    """运行期生成正向 / 反向替换表，避免在源码中硬编码大表。"""
    p = 1
    q = 1
    forward = [0] * 256
    while True:
        p = (p ^ ((p << 1) & 0xFF) ^ (0x1B if p & 0x80 else 0)) & 0xFF
        q ^= (q << 1) & 0xFF
        q ^= (q << 2) & 0xFF
        q ^= (q << 4) & 0xFF
        if q & 0x80:
            q ^= 0x09
        q &= 0xFF
        x = (q ^ ((q << 1) | (q >> 7)) ^ ((q << 2) | (q >> 6))
             ^ ((q << 3) | (q >> 5)) ^ ((q << 4) | (q >> 4))) & 0xFF
        forward[p] = x ^ 0x63
        if p == 1:
            break
    forward[0] = 0x63
    backward = [0] * 256
    for i, v in enumerate(forward):
        backward[v] = i
    return forward, backward


_FWD, _REV = _build_tables()

_RC = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D]


def _schedule(key):
    """由主参数展开出各轮变换参数。返回 (参数扁平表, 轮数)。"""
    nk = len(key) // 4
    nr = nk + 6
    words = [list(key[4 * i:4 * i + 4]) for i in range(nk)]
    for i in range(nk, 4 * (nr + 1)):
        temp = list(words[i - 1])
        if i % nk == 0:
            temp = temp[1:] + temp[:1]
            temp = [_FWD[b] for b in temp]
            temp[0] ^= _RC[i // nk - 1]
        elif nk > 6 and i % nk == 4:
            temp = [_FWD[b] for b in temp]
        words.append([words[i - nk][j] ^ temp[j] for j in range(4)])
    flat = []
    for w in words:
        flat.extend(w)
    return flat, nr


def _mix_key(state, subkeys, rnd):
    off = rnd * BLOCK_BYTES
    for i in range(BLOCK_BYTES):
        state[i] ^= subkeys[off + i]


def _permute_rows(s):
    out = [0] * 16
    for c in range(4):
        for r in range(4):
            out[4 * c + r] = s[4 * ((c + r) % 4) + r]
    return out


def _unpermute_rows(s):
    out = [0] * 16
    for c in range(4):
        for r in range(4):
            out[4 * c + r] = s[4 * ((c - r) % 4) + r]
    return out


def _double(a):
    a <<= 1
    if a & 0x100:
        a = (a ^ 0x1B) & 0xFF
    return a & 0xFF


def _combine_columns(s):
    out = [0] * 16
    for c in range(4):
        i = 4 * c
        a0, a1, a2, a3 = s[i], s[i + 1], s[i + 2], s[i + 3]
        out[i] = _double(a0) ^ (_double(a1) ^ a1) ^ a2 ^ a3
        out[i + 1] = a0 ^ _double(a1) ^ (_double(a2) ^ a2) ^ a3
        out[i + 2] = a0 ^ a1 ^ _double(a2) ^ (_double(a3) ^ a3)
        out[i + 3] = (_double(a0) ^ a0) ^ a1 ^ a2 ^ _double(a3)
    return out


def _mul_field(a, b):
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return p & 0xFF


def _separate_columns(s):
    out = [0] * 16
    for c in range(4):
        i = 4 * c
        a0, a1, a2, a3 = s[i], s[i + 1], s[i + 2], s[i + 3]
        out[i] = _mul_field(a0, 14) ^ _mul_field(a1, 11) ^ _mul_field(a2, 13) ^ _mul_field(a3, 9)
        out[i + 1] = _mul_field(a0, 9) ^ _mul_field(a1, 14) ^ _mul_field(a2, 11) ^ _mul_field(a3, 13)
        out[i + 2] = _mul_field(a0, 13) ^ _mul_field(a1, 9) ^ _mul_field(a2, 14) ^ _mul_field(a3, 11)
        out[i + 3] = _mul_field(a0, 11) ^ _mul_field(a1, 13) ^ _mul_field(a2, 9) ^ _mul_field(a3, 14)
    return out


def _decode_stream(key, iv, data):
    """还原一段分组数据流。"""
    if len(data) == 0 or len(data) % BLOCK_BYTES != 0:
        raise RefError("数据长度不合法，参考资料文件已损坏")
    subkeys, nr = _schedule(key)
    out = bytearray()
    prev = list(iv)
    for pos in range(0, len(data), BLOCK_BYTES):
        block = list(data[pos:pos + BLOCK_BYTES])
        s = list(block)
        _mix_key(s, subkeys, nr)
        for rnd in range(nr - 1, 0, -1):
            s = _unpermute_rows(s)
            s = [_REV[b] for b in s]
            _mix_key(s, subkeys, rnd)
            s = _separate_columns(s)
        s = _unpermute_rows(s)
        s = [_REV[b] for b in s]
        _mix_key(s, subkeys, 0)
        out.extend([s[i] ^ prev[i] for i in range(BLOCK_BYTES)])
        prev = block
    return bytes(out)


def _encode_stream(key, iv, data):
    """把一段分组数据流装进容器用。"""
    subkeys, nr = _schedule(key)
    out = bytearray()
    prev = list(iv)
    for pos in range(0, len(data), BLOCK_BYTES):
        block = list(data[pos:pos + BLOCK_BYTES])
        s = [block[i] ^ prev[i] for i in range(BLOCK_BYTES)]
        _mix_key(s, subkeys, 0)
        for rnd in range(1, nr):
            s = [_FWD[b] for b in s]
            s = _permute_rows(s)
            s = _combine_columns(s)
            _mix_key(s, subkeys, rnd)
        s = [_FWD[b] for b in s]
        s = _permute_rows(s)
        _mix_key(s, subkeys, nr)
        out.extend(s)
        prev = s
    return bytes(out)


def _pad(data):
    n = BLOCK_BYTES - (len(data) % BLOCK_BYTES)
    return data + bytes([n]) * n


def _unpad(data):
    if not data:
        raise RefError("参考资料内容为空")
    n = data[-1]
    if n < 1 or n > BLOCK_BYTES or data[-n:] != bytes([n]) * n:
        raise RefError("内容校验未通过，参考资料已被改动或版本不匹配")
    return data[:-n]


# ---------------------------------------------------------------- 参数推导

def _material():
    """使用分散片段在运行期拼装内部识别码，不落成整串明文。"""
    parts = ["Bl", "end", "edLD", "-2026", "0907", "-R", "ef", "-K", "ey", "-7C", "49"]
    return "".join(parts)


_MAC_BLOCK = 64  # 内部摘要算法的分组长度（字节）


def _mac(message, params):
    """基于标准摘要函数构造带参数的校验值（内部格式，供本模块使用）。"""
    k = params
    if len(k) > _MAC_BLOCK:
        k = hashlib.sha256(k).digest()
    k = k + b"\x00" * (_MAC_BLOCK - len(k))
    inner = hashlib.sha256(bytes(b ^ 0x36 for b in k) + message).digest()
    return hashlib.sha256(bytes(b ^ 0x5C for b in k) + inner).digest()


def _stretch(salt, rounds, length):
    """由内部识别码与随机器参数反复迭代，推导出运行期变换参数。"""
    secret = _material().encode("utf-8")
    out = bytearray()
    block_index = 1
    while len(out) < length:
        u = _mac(salt + block_index.to_bytes(4, "big"), secret)
        acc = int.from_bytes(u, "big")
        for _ in range(rounds - 1):
            u = _mac(u, secret)
            acc ^= int.from_bytes(u, "big")
        out += acc.to_bytes(32, "big")
        block_index += 1
    return bytes(out[:length])


def _derive(salt, rounds):
    """推导 (数据变换参数, 校验参数)。"""
    raw = _stretch(salt, rounds, KEY_BYTES + CHECK_BYTES)
    return raw[:KEY_BYTES], raw[KEY_BYTES:KEY_BYTES + CHECK_BYTES]


# ---------------------------------------------------------------- 容器读写

def _check_base(container):
    parts = [
        str(container.get("kind", "")),
        str(container.get("rev", "")),
        str(container.get("salt", "")),
        str(container.get("rounds", "")),
        str(container.get("nonce", "")),
        str(container.get("data", "")),
    ]
    return "|".join(parts).encode("utf-8")


def _compute_check(container, check_params):
    return _mac(_check_base(container), check_params)


def _same_bytes(a, b):
    """常数时间比较，避免逐字节提前返回。"""
    if len(a) != len(b):
        return False
    diff = 0
    for x, y in zip(a, b):
        diff |= x ^ y
    return diff == 0


def pack(plain_text):
    """把 JSON 文本装进容器（返回 dict，可直接 json.dump 落盘）。

    维护资料时使用：`json.dump(pack(text), f, ensure_ascii=False, indent=2)`。
    运行期读取无需调用本函数。
    """
    salt = os.urandom(16)
    nonce = os.urandom(16)
    stream_key, check_key = _derive(salt, ROUNDS)
    body = _encode_stream(stream_key, nonce, _pad(plain_text.encode("utf-8")))
    container = {
        "kind": TAG,
        "rev": REV,
        "salt": base64.b64encode(salt).decode("ascii"),
        "rounds": ROUNDS,
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "data": base64.b64encode(body).decode("ascii"),
    }
    container["check"] = base64.b64encode(_compute_check(container, check_key)).decode("ascii")
    return container


def unpack(container):
    """把容器还原为 JSON 文本。失败时抛出 RefError。"""
    if not isinstance(container, dict):
        raise RefError("参考资料结构异常")
    if container.get("kind") != TAG:
        raise RefError("文件标识不正确，不是本技能的参考资料")
    rev = int(container.get("rev") or 0)
    if rev != REV:
        raise RefError("参考资料版本不兼容（rev=%s）" % rev)
    rounds = int(container.get("rounds") or 0)
    if not (MIN_ROUNDS <= rounds <= MAX_ROUNDS):
        raise RefError("参考资料参数异常（rounds=%s）" % rounds)
    try:
        salt = base64.b64decode(container.get("salt") or "")
        nonce = base64.b64decode(container.get("nonce") or "")
        body = base64.b64decode(container.get("data") or "")
        digest = base64.b64decode(container.get("check") or "")
    except Exception:
        raise RefError("参考资料字段缺失或被破坏，无法读取")
    stream_key, check_key = _derive(salt, rounds)
    if not _same_bytes(_compute_check(container, check_key), digest):
        raise RefError("完整性校验未通过，参考资料已被改动")
    return _unpad(_decode_stream(stream_key, nonce, body)).decode("utf-8")


# ---------------------------------------------------------------- 路径与读取

def skill_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)


def references_dir():
    return os.path.join(skill_root(), REFERENCES_DIRNAME)


def ref_path(name):
    base = name[:-5] if str(name).lower().endswith(".json") else str(name)
    return os.path.join(references_dir(), base + ".json")


def list_names():
    return list(REF_NAMES)


def exists(name):
    return os.path.isfile(ref_path(name))


def read_text(name):
    """把指定参考资料还原为 JSON 文本。"""
    path = ref_path(name)
    if not os.path.isfile(path):
        raise RefMissing("找不到参考资料「%s」" % name)
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            container = json.load(f)
    except json.JSONDecodeError:
        raise RefError("参考资料「%s」文件损坏，无法解析" % name)
    except UnicodeDecodeError:
        raise RefError("参考资料「%s」文件编码异常" % name)
    return unpack(container)


def load(name):
    """把指定参考资料还原并解析为 dict。"""
    try:
        return json.loads(read_text(name))
    except json.JSONDecodeError:
        raise RefError("参考资料「%s」内容结构异常" % name)


# ---------------------------------------------------------------- Markdown 还原

def _head(lines, text, level=2):
    if text:
        lines.append("#" * level + " " + str(text))
        lines.append("")


def _para(lines, text):
    if text:
        lines.append(str(text))
        lines.append("")


def _bullets(lines, items, mark="- "):
    if not items:
        return
    for it in items:
        lines.append(mark + str(it))
    lines.append("")


def _table(lines, header, rows):
    if not header:
        return
    lines.append("| " + " | ".join(str(h) for h in header) + " |")
    lines.append("|" + "|".join(["---"] * len(header)) + "|")
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    lines.append("")


def _cell(val):
    if isinstance(val, (list, tuple)):
        return "、".join(str(v) for v in val)
    if val is None:
        return ""
    return str(val)


def _fallback(lines, val, depth=0):
    """未显式支持的结构：按 key / 列表 / 文本 尽力渲染，保证不报错。"""
    pad = "  " * depth
    if isinstance(val, dict):
        for k, v in val.items():
            if isinstance(v, (dict, list)):
                lines.append("%s**%s**：" % (pad, k))
                lines.append("")
                _fallback(lines, v, depth + 1)
            else:
                lines.append("%s**%s**：%s" % (pad, k, _cell(v)))
        lines.append("")
    elif isinstance(val, (list, tuple)):
        for v in val:
            if isinstance(v, (dict, list)):
                _fallback(lines, v, depth)
            else:
                lines.append("%s- %s" % (pad, _cell(v)))
        lines.append("")
    elif str(val).strip():
        lines.append(pad + str(val))
        lines.append("")


def _toc(lines, toc):
    if not isinstance(toc, dict):
        return
    _head(lines, toc.get("heading"), 2)
    items = toc.get("items") or []
    if items:
        _bullets(lines, ["%s　%s" % (it.get("topic", ""), it.get("where", "")) for it in items])


def _section(lines, sec):
    level = int(sec.get("level") or 2)
    _head(lines, sec.get("heading") or sec.get("id"), level)
    stype = sec.get("type")
    if stype == "code" or sec.get("code"):
        lines.append("```")
        lines.append(str(sec.get("code", "")).rstrip("\n"))
        lines.append("```")
        lines.append("")
    elif stype == "checklist" or (stype is None and sec.get("items")):
        _bullets(lines, sec.get("items") or [], "- [ ] ")
    elif sec.get("text"):
        _para(lines, sec.get("text"))
    elif stype is None and not sec.get("items"):
        return
    else:
        _fallback(lines, {k: v for k, v in sec.items()
                          if k not in ("id", "level", "heading", "type")})


def _block(lines, blk):
    _head(lines, blk.get("heading") or blk.get("id"), 2)
    _para(lines, blk.get("lead"))
    btype = blk.get("type")
    if btype == "table":
        header = blk.get("columns") or []
        rows = blk.get("rows") or []
        keys = list(rows[0].keys())[:len(header)] if rows and isinstance(rows[0], dict) else []
        _table(lines, header, [[_cell(r.get(k, "")) for k in keys] for r in rows] if keys
               else [[_cell(c) for c in r] for r in rows])
    elif btype == "bullets":
        _bullets(lines, blk.get("items"))
    elif btype == "code":
        lines.append("```")
        lines.append(str(blk.get("code", "")).rstrip("\n"))
        lines.append("```")
        lines.append("")
    elif btype == "matrix":
        cols = blk.get("columns") or []
        cells = blk.get("cells") or {}
        _table(lines, ["知识类型"] + list(cols),
               [[kt] + [_cell(v) for v in (cells.get(kt) or [])] for kt in blk.get("knowledge_types") or []])
    elif blk.get("text"):
        _para(lines, blk.get("text"))
    else:
        _fallback(lines, {k: v for k, v in blk.items() if k not in ("id", "heading", "type")})
    if blk.get("cautions"):
        _para(lines, blk.get("caution_lead"))
        _bullets(lines, blk.get("cautions"))
    if blk.get("note"):
        lines.append("> " + str(blk["note"]))
        lines.append("")


def _error_handling(lines, eh):
    if not isinstance(eh, dict):
        return
    _head(lines, eh.get("heading"), 2)
    _para(lines, eh.get("lead"))
    _bullets(lines, eh.get("steps"))
    _para(lines, eh.get("quick_fix_lead"))
    fixes = eh.get("quick_fix") or []
    if fixes:
        _table(lines, ["现象", "修复"], [[_cell(f.get("symptom", "")), _cell(f.get("fix", ""))]
                                        for f in fixes])


def _questions(lines, questions, heading):
    if not questions:
        return
    _head(lines, heading or "常见问题解答", 2)
    for q in questions:
        lines.append("**%s %s**" % (q.get("id", ""), q.get("question", "")))
        lines.append("")
        _para(lines, q.get("answer"))


def _entries(lines, entries):
    if not entries:
        return
    for e in entries:
        lines.append("%s.%s" % (e.get("no", ""), e.get("text", "")))
        lines.append("")


def to_markdown(data):
    """把一份参考资料的结构渲染为 Markdown 文本。"""
    lines = []
    _head(lines, data.get("title"), 1)
    _para(lines, data.get("intro"))
    _bullets(lines, data.get("notes"))
    _toc(lines, data.get("toc"))
    for sec in data.get("sections") or []:
        _section(lines, sec)
    for blk in data.get("blocks") or []:
        _block(lines, blk)
    _error_handling(lines, data.get("error_handling"))
    _questions(lines, data.get("questions"), data.get("questions_heading"))
    _entries(lines, data.get("entries"))
    ver = data.get("version_line")
    if ver:
        lines.append("")
        lines.append(str(ver))
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- 自检入口

def selftest():
    """快速自检：装入后能否原样还原。返回 (是否通过, 说明)。"""
    probe = '{"probe": "参考资料自检", "n": 123, "arr": [1, 2, 3]}'
    try:
        back = unpack(pack(probe))
    except Exception as e:
        return False, "装入 / 还原自检失败：%s" % e
    if back != probe:
        return False, "装入 / 还原结果与原文不一致"
    return True, "装入 / 还原自检通过"


if __name__ == "__main__":  # 直接运行时给出提示，避免误用
    print("本文件是 scripts/ref_reader.py 的支撑模块，请通过命令行入口使用：")
    print("    python scripts/ref_reader.py --help")
    sys.exit(0)
