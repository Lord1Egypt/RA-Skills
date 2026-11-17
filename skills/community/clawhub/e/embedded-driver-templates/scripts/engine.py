#!/usr/bin/env python3
"""嵌入式驱动模板库引擎：从 mcu-debug-mcp v4.5.4 core.py 原样抽取（S2 同源，不改逻辑）。

覆盖：driver_list / driver_get / driver_wiring（9 款预验证驱动）
     + peripheral_records / peripheral_api_brief / peripheral_api_get（外设初始化顺序层）。
驱动数据（drivers/ 9 目录）与 MCP 包内同一份内容，S2 同源复制。
"""

from __future__ import annotations

import glob
import json
import os
import re

__version__ = "1.0.0"

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(os.path.dirname(HERE), "assets")
# ★ 平台两级目录限制（2026-10-28 驳回实证：Skill 包仅支持 根/二级/文件）：
#   驱动文件从 assets/drivers/<名>/<文件> 压平为 assets/<名>__<文件>（双下划线分隔），
#   引擎按前缀聚合，对 driver_list/get/wiring/api 的输出格式零影响。
_SEP = "__"

def _driver_dirs():
    """列举驱动库 → [(名, 前缀路径)]。压平后"目录"= assets/<名>__* 文件组。"""
    if not os.path.isdir(ASSETS_DIR):
        return []
    names = []
    for f in sorted(os.listdir(ASSETS_DIR)):
        if _SEP in f and os.path.isfile(os.path.join(ASSETS_DIR, f)):
            n = f.split(_SEP, 1)[0]
            if n and n not in names:
                names.append(n)
    return [(n, os.path.join(ASSETS_DIR, n + _SEP)) for n in names]


def _driver_dir(name):
    """按名解析驱动前缀路径（大小写不敏感）；没有返回 None。

    返回值是 glob 前缀（assets/<名>__），不是真实目录——调用方全部走
    os.path.join(ddir, ...) + glob/exists，前缀路径同样成立。
    """
    key = (name or "").strip().lower()
    if not key:
        return None
    for nm, p in _driver_dirs():
        if nm.lower() == key:
            return p
    return None


def _driver_meta(name):
    ddir = _driver_dir(name)
    meta_path = (glob.glob(glob.escape(ddir) + "meta.json") or [""])[0] if ddir else ""
    if meta_path and os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def driver_list():
    dirs = _driver_dirs()
    if not dirs:
        return "驱动库目录不存在。"
    lines = ["共 %d 个预验证驱动：" % len(dirs)]
    for n, _p in dirs:
        meta = _driver_meta(n)
        lines.append("- %s：%s（验证：%s）" % (n, meta.get("desc", ""), meta.get("verified", "见 meta.json")))
    return "\n".join(lines)


def driver_get(name):
    # ★ 空名不能当成「某个驱动目录」：os.path.join(驱动库, "") 拼出来的是驱动库
    #   根目录，而它**确实存在** ⟹ 会走进「目录存在但没内容」分支，输出
    #   "驱动  目录存在，但里面没有任何可读内容"——用户完全看不懂（真实回放已复现）。
    dirs = _driver_dirs()
    if not dirs:
        return "驱动库目录不存在。"
    if not (name or "").strip():
        return "没给驱动名。可用：%s" % ", ".join(n for n, _p in dirs)
    ddir = _driver_dir(name)
    if not ddir:
        return "没有名为 %s 的驱动。可用：%s" % (name, ", ".join(n for n, _p in dirs))
    parts = []
    meta = _driver_meta(name)
    if meta:
        parts.append("【验证记录】%s" % json.dumps(meta, ensure_ascii=False))
    for pattern in ("*.md", "*.h", "*.c"):
        for f in sorted(glob.glob(glob.escape(ddir) + pattern)):
            with open(f, "r", encoding="utf-8") as fh:
                parts.append("===== %s =====\n%s" % (os.path.basename(f), fh.read()))
    if not parts:
        # ★ 空响应也算假答案：用户分不清"驱动确实是空的"还是"工具没干活"
        return ("驱动 %s 目录存在，但里面没有任何可读内容（既没有 meta.json，"
                "也没有 *.md/*.h/*.c）——这个驱动还没写全，或被误删了。"
                "用 driver_list 看其他可用驱动。" % name)
    return "\n\n".join(parts)


def driver_wiring(name):
    """查驱动接线知识库（wiring.md）：接什么引脚、坑在哪、怎么解读输出。"""
    dirs = _driver_dirs()
    if not dirs:
        return "驱动库目录不存在。"
    ddir = _driver_dir(name)
    if not ddir:
        return "没有名为 %s 的驱动。可用：%s" % (name, ", ".join(n for n, _p in dirs))
    path = (glob.glob(glob.escape(ddir) + "wiring.md") or [""])[0]
    if not os.path.exists(path):
        return "驱动 %s 暂无 wiring.md。" % name
    with open(path, "r", encoding="utf-8") as f:
        return f.read()



_PORT_SYM_RE = re.compile(
    r"HAL_[A-Za-z_0-9]+"
    r"|\b(?:I2C\d?|SPI\d?|USART\d+|UART\d+|TIM\d+|GPIO[A-Z]?|DWT)\b")
_HEX_ADDR_RE = re.compile(r"0[xX][0-9A-Fa-f]{2}")
# 初始化顺序要求：只摘 port 头注释里的原句，不改写
_INIT_REQ_RE = re.compile(
    r"^[^\n]*?(?:先|必须|需要|确保)[^\n]*?(?:初始化|配置|Init|Start|start)[^\n]*$",
    re.M)

_BUS_RULES = (
    ("i2c", ("i2c",)),
    ("uart", ("uart", "usart", "串口")),
    ("timer_pwm", ("pwm", "hal_tim", "ccr", "定时器")),
    ("gpio_timing", ("gpio", "trig", "echo", "pin_out", "pin_read")),
)


def _port_source(name):
    """读驱动的 *_port.h 原文（适配层是外设用法的唯一真身）。"""
    ddir = _driver_dir(name)
    if not ddir:
        return ""
    texts = []
    for f in sorted(glob.glob(glob.escape(ddir) + "*_port.h")):
        try:
            with open(f, "r", encoding="utf-8") as fh:
                texts.append(fh.read())
        except Exception:
            pass
    return "\n".join(texts)


def _uniq(seq, limit=None):
    """保序去重（派生视图里同一符号常在多处出现）。"""
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
            if limit and len(out) >= limit:
                break
    return out


def _component_bus(meta, port_text):
    hay = " ".join([meta.get("desc", ""), meta.get("usage", ""),
                     port_text]).lower()
    for bus, keys in _BUS_RULES:
        for k in keys:
            if k.lower() in hay:
                return bus
    return "unknown"


def _needs_us_timing(port_text):
    """这个驱动的适配层是否真需要**微秒精度**延时。

    ★ 为什么按 DWT 符号判、不按 `_delay_us` 函数名判（2026-10-13 实测踩过）：
      stepper_28byj48 也有 `stepper_delay_us()`，但它注释里写的是
   「HAL_Delay 毫秒粒度即可，半步延时通常 1-10ms 量级」——函数名只是接口
   统一而已。按函数名判会把它误标成「需微秒时序」，用户照着去配 DWT 属于
   白费功夫。反过来 dht11/ds18b20/hcsr04 的注释里明写「毫秒粒度不能用」
   且示例实现就是 DWT->CYCCNT——判据落在 DWT 上才对得上真机事实。
    """
    return "DWT" in port_text


def _split_clauses(text):
    """按中文分句切文本，但**括号内不切**。

    ★ 为什么需要括号感知（实测踩过）：mpu6050 的 usage 是
    「port 层提供 I2C 读写两函数（7 位地址 0x68，AD0 接地）」——括号里那个逗号
    是 0x68 与 AD0 之间的分隔，按裸逗号切会把它腰斩成「7 位地址 0x68」，
    用户读到的是句残话。
    """
    out, buf, depth = [], [], 0
    for ch in text or "":
        if ch in "（(【[":
            depth += 1
        elif ch in "）)】]":
            depth = max(0, depth - 1)
        if depth == 0 and ch in "，；;":
            out.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    if buf:
        out.append("".join(buf).strip())
    return [x for x in out if x]


def _init_requirements(meta, port_text):
    """移植时的初始化/接线硬要求——两条真实证据源，合并去重：

    1. 适配层注释里的原句（「工程里先完成 HAL_I2C_MspInit 与 hi2c1 初始化」）；
    2. meta.usage 里点名 port 的分句（「port 里改定时器时钟/PSC/ARR 三处即可」）。
    只摘原文，不改写、不润色。
    """
    reqs = [s.strip(" */*") for s in _INIT_REQ_RE.findall(port_text)]
    for p in _split_clauses(meta.get("usage", "")):
        # 去掉「复制 xxx.h 进工程」这类文件搬运说明，只要移植动作本身
        if "port" in p.lower() and not p.startswith("复制"):
            reqs.append(p)
    return _uniq(reqs)


def peripheral_records():
    """外设 API 用法记录（结构化，G03 的数据层）。

    每条回答「这个驱动到底要哪几个外设、外设初始化顺序上有什么硬要求」——
    答案全部取自 *_port.h 里的真实代码与注释。
    """
    out = []
    for name, _p in _driver_dirs():
        meta = _driver_meta(name)
        if not meta:
            continue
        port_text = _port_source(name)
        if not port_text:
            continue
        reqs = _init_requirements(meta, port_text)
        out.append({
            "name": name,
            "bus": _component_bus(meta, port_text),
            "hal_symbols": _uniq(_PORT_SYM_RE.findall(port_text), limit=12),
            "init_requires": reqs[:3],
            "pitfalls": meta.get("common_pitfalls", ""),
            "source": "drivers/%s/*_port.h" % name,
        })
    return out


def peripheral_api_list(bus=None):
    """外设用法记录（结构化）。"""
    recs = peripheral_records()
    if bus:
        recs = [r for r in recs if r["bus"] == bus]
    return recs


def peripheral_api_brief(bus=None):
    """外设用法的文本视图：谁要哪个外设、初始化有什么硬要求。"""
    recs = peripheral_api_list(bus)
    if not recs:
        if bus:
            return "没有 bus=%s 的外设用法记录。" % bus
        return "外设 API 用法知识层为空（驱动库下没有 *_port.h 适配层）。"
    lines = ["共 %d 条外设用法（取自各驱动 *_port.h 适配层）：" % len(recs)]
    for r in recs:
        lines.append("- %s [%s]：%s" % (
            r["name"], r["bus"],
            "、".join(r["hal_symbols"][:5]) or "（无 HAL 符号，纯解析库）"))
        for q in r["init_requires"]:
            lines.append("    顺序要求：%s" % q)
    return "\n".join(lines)


def peripheral_api_get(name):
    """单个驱动的外设初始化要求全文（移植前照着核对一遍）。"""
    recs = peripheral_records()
    if not recs:
        return "外设 API 用法知识层为空（驱动库下没有 *_port.h 适配层）。"
    key = (name or "").strip().lower()
    if not key:
        return "没给驱动名。可用：%s" % ", ".join(r["name"] for r in recs)
    hit = next((r for r in recs if r["name"].lower() == key), None)
    if hit is None:
        return "没有名为 %s 的记录。可用：%s" % (
            name, ", ".join(r["name"] for r in recs))
    lines = ["【%s】外设：%s" % (hit["name"], "、".join(hit["hal_symbols"]) or "（无）")]
    if hit["init_requires"]:
        lines.append("初始化顺序要求（适配层注释原句）：")
        lines.extend("  · %s" % q for q in hit["init_requires"])
    else:
        lines.append("初始化顺序要求：适配层注释里没写（移植时按上面符号自行核对）。")
    lines.append("坑：%s" % (hit["pitfalls"] or "（meta.json 未记）"))
    lines.append("来源：%s" % hit["source"])
    return "\n".join(lines)
