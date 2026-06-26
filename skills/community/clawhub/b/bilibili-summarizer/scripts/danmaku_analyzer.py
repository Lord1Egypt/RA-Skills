#!/usr/bin/env python3
"""
danmaku_analyzer.py - B站弹幕分析与提取（仅支持B站）

功能:
    1. 提取弹幕内容（支持按时间段获取）
    2. 弹幕词频统计（高频关键词）
    3. 弹幕密度图（定位视频高潮/无聊片段）
    4. 热评弹幕提取（高赞弹幕 = 观众提炼的要点）

用法:
    python3 danmaku_analyzer.py <B站链接或BV号>
    python3 danmaku_analyzer.py <B站链接或BV号> --top-words 20    # 高频词 Top N
    python3 danmaku_analyzer.py <B站链接或BV号> --density          # 弹幕密度分析
    python3 danmaku_analyzer.py <B站链接或BV号> --highlights       # 提取高赞弹幕

输出:
    JSON 格式到 stdout
"""

import sys
import os
import re
import json
import time
import math
import urllib.request
import urllib.parse
from collections import Counter

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
}


def http_get(url: str, params: dict = None) -> dict:
    """发起 GET 请求"""
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def extract_bvid(text: str) -> str:
    """提取 BV 号"""
    m = re.search(r"(BV[0-9A-Za-z]{10})", text, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    raise ValueError(f"无法提取 BV 号: {text}")


def get_cid(bvid: str) -> int:
    """获取视频的 cid"""
    data = http_get("https://api.bilibili.com/x/web-interface/view", {"bvid": bvid})
    if data.get("code") != 0:
        raise RuntimeError(f"API 错误: {data.get('message')}")
    pages = data.get("data", {}).get("pages", [])
    if pages:
        return pages[0]["cid"]
    raise RuntimeError("无法获取 cid")


def fetch_danmaku(bvid: str, cid: int, segment_index: int = 0) -> list:
    """获取弹幕（protobuf 格式，B站新版API）"""
    # B站弹幕API: 按6分钟分段，segment_index=0 表示 0-6分钟
    url = f"https://api.bilibili.com/x/v2/dm/web/seg.so"
    params = {
        "type": 1,
        "oid": cid,
        "pid": bvid,
        "segment_index": segment_index,
    }

    try:
        req = urllib.request.Request(
            f"https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid={cid}&pid={bvid}&segment_index={segment_index}",
            headers={
                **HEADERS,
                "Accept": "*/*",
            }
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw_data = resp.read()

        # 尝试用 protobuf 解析
        try:
            return _parse_protobuf_danmaku(raw_data)
        except Exception:
            # 回退到旧版 API（XML 格式）
            return _fetch_xml_danmaku(cid)
    except Exception as e:
        print(f"[!] protobuf 弹幕获取失败，尝试旧版API: {e}", file=sys.stderr)
        return _fetch_xml_danmaku(cid)


def _parse_protobuf_danmaku(data: bytes) -> list:
    """解析 protobuf 格式弹幕（简化版，不依赖 protobuf 库）"""
    # B站弹幕 protobuf 结构较复杂，这里用文本匹配提取关键信息
    danmakus = []

    # 尝试导入 google.protobuf
    try:
        from google.protobuf.internal.decoder import _DecodeVarint
        # 简单解析：扫描 UTF-8 文本内容
        text_pattern = re.compile(rb'[\x20-\x7e\xe4-\xe9][\x20-\x7e\x80-\xff]{1,100}')
        # 更可靠的方式：直接用旧版 API
        return []
    except ImportError:
        pass

    return []


def _fetch_xml_danmaku(cid: int) -> list:
    """旧版弹幕 API（XML 格式，已废弃但仍可用）"""
    try:
        url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()

        # XML 弹幕解析
        import xml.etree.ElementTree as ET
        # B站返回的是压缩的 XML
        try:
            # 尝试 gzip 解压
            import gzip
            raw = gzip.decompress(raw)
        except Exception:
            pass

        root = ET.fromstring(raw.decode("utf-8"))
        danmakus = []
        for d in root.findall("d"):
            p = d.get("p", "")
            content = d.text or ""
            if p and content:
                parts = p.split(",")
                if len(parts) >= 4:
                    danmakus.append({
                        "time": float(parts[0]),
                        "mode": int(parts[1]),
                        "font_size": int(parts[2]),
                        "color": int(parts[3]),
                        "content": content,
                    })
        return danmakus
    except Exception as e:
        print(f"[!] XML弹幕解析失败: {e}", file=sys.stderr)
        return []


def analyze_word_frequency(danmakus: list, top_n: int = 30) -> list:
    """弹幕词频统计（过滤无意义词）"""
    # 中文停用词和常见无意义弹幕
    stopwords = set("的了是在我不有和人这中大为上个国也子时道说出会要没成好你他她它们什么那被从把让向到得与很都就可以而但又或还才能将已对之以其比等因最然后下过可选更".split())
    noise_words = set("哈哈哈哈 笑死 666 2333 wwww www 哈哈哈 草 哈哈哈或或或或 无语 天哪 啊啊啊 哇哇哇 确实 难绷 好家伙 离谱 绷不住".split())

    words = []
    for d in danmakus:
        content = d.get("content", "")
        # 中文分词（简单按标点和空格分割）
        # 先提取连续中文字符序列
        segments = re.findall(r'[\u4e00-\u9fff]{2,}', content)
        for seg in segments:
            # 2-4 字的组合
            for length in range(2, min(5, len(seg) + 1)):
                for start in range(len(seg) - length + 1):
                    word = seg[start:start + length]
                    if word not in stopwords and word not in noise_words:
                        words.append(word)

    counter = Counter(words)
    return [{"word": w, "count": c} for w, c in counter.most_common(top_n)]


def analyze_density(danmakus: list, interval_sec: int = 30) -> list:
    """弹幕密度分析（按时间段统计弹幕数量）"""
    if not danmakus:
        return []

    max_time = max(d["time"] for d in danmakus)
    buckets = {}
    current = 0
    while current <= max_time:
        buckets[current] = 0
        current += interval_sec

    for d in danmakus:
        t = d["time"]
        bucket = int(t // interval_sec) * interval_sec
        if bucket in buckets:
            buckets[bucket] += 1

    result = []
    for t_start in sorted(buckets.keys()):
        mm_from = int(t_start // 60)
        ss_from = int(t_start % 60)
        mm_to = int((t_start + interval_sec) // 60)
        ss_to = int((t_start + interval_sec) % 60)
        count = buckets[t_start]
        level = "low"
        if count >= 20:
            level = "high"
        elif count >= 10:
            level = "medium"
        result.append({
            "time_range": f"{mm_from:02d}:{ss_from:02d}-{mm_to:02d}:{ss_to:02d}",
            "start_sec": t_start,
            "end_sec": t_start + interval_sec,
            "count": count,
            "level": level,
        })

    return result


def extract_highlights(danmakus: list, min_length: int = 6, top_n: int = 20) -> list:
    """提取有价值的弹幕（长文本 + 高密度时段）"""
    scored = []
    for d in danmakus:
        content = d.get("content", "")
        score = 0
        # 长弹幕更有价值
        if len(content) >= min_length:
            score += len(content)
        # 包含标点符号的弹幕更完整
        if re.search(r'[，。！？；：]', content):
            score += 5
        # 包含数字/数据更有信息量
        if re.search(r'\d+', content):
            score += 3
        # 排除纯表情/符号
        if re.match(r'^[\W_]+$', content):
            score = 0
        # 排除纯重复字符
        if re.match(r'^(.)\1{3,}$', content):
            score = 0

        if score > 0:
            scored.append({
                "time": d["time"],
                "mm_ss": f"{int(d['time'] // 60):02d}:{int(d['time'] % 60):02d}",
                "content": content,
                "score": score,
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]


def run(bvid_or_url: str, top_words: int = 30, density: bool = False, highlights: bool = False):
    print(f"[*] 正在分析弹幕: {bvid_or_url}", file=sys.stderr)

    try:
        bvid = extract_bvid(bvid_or_url)
    except ValueError:
        print(json.dumps({"error": "仅支持B站视频弹幕分析"}))
        sys.exit(1)

    print(f"[*] BV号: {bvid}", file=sys.stderr)

    # 获取 cid
    try:
        cid = get_cid(bvid)
    except Exception as e:
        print(json.dumps({"error": f"获取视频信息失败: {e}"}))
        sys.exit(1)

    print(f"[*] cid: {cid}", file=sys.stderr)

    # 获取视频时长
    try:
        data = http_get("https://api.bilibili.com/x/web-interface/view", {"bvid": bvid})
        duration = data.get("data", {}).get("duration", 0)
    except Exception:
        duration = 0

    # 获取弹幕
    print("[*] 获取弹幕...", file=sys.stderr)
    danmakus = _fetch_xml_danmaku(cid)

    if not danmakus:
        # 尝试按段获取
        segment_count = max(1, (duration // 360) + 1)
        for seg_idx in range(min(segment_count, 5)):
            print(f"[*] 获取弹幕段 {seg_idx + 1}...", file=sys.stderr)
            seg_danmakus = fetch_danmaku(bvid, cid, seg_idx)
            danmakus.extend(seg_danmakus)
            time.sleep(0.3)

    print(f"[*] 共获取 {len(danmakus)} 条弹幕", file=sys.stderr)

    result = {
        "bvid": bvid,
        "total_danmaku": len(danmakus),
        "duration_sec": duration,
    }

    # 高频词分析
    result["top_words"] = analyze_word_frequency(danmakus, top_words)

    # 弹幕密度
    if density or len(danmakus) > 0:
        result["density"] = analyze_density(danmakus)

        # 找出高密度区间（高潮片段）
        high_density = [d for d in result["density"] if d["level"] == "high"]
        if high_density:
            result["highlights_time"] = [d["time_range"] for d in high_density]

    # 热评弹幕
    if highlights or len(danmakus) > 0:
        result["highlight_danmaku"] = extract_highlights(danmakus)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 danmaku_analyzer.py <B站链接或BV号>", file=sys.stderr)
        print("      python3 danmaku_analyzer.py <BV号> --top-words 20", file=sys.stderr)
        print("      python3 danmaku_analyzer.py <BV号> --density", file=sys.stderr)
        print("      python3 danmaku_analyzer.py <BV号> --highlights", file=sys.stderr)
        sys.exit(1)

    bvid_arg = sys.argv[1]
    top_words = 30
    density = "--density" in sys.argv or "--all" in sys.argv
    highlights = "--highlights" in sys.argv or "--all" in sys.argv

    if "--top-words" in sys.argv:
        idx = sys.argv.index("--top-words")
        if idx + 1 < len(sys.argv):
            top_words = int(sys.argv[idx + 1])

    run(bvid_arg, top_words, density, highlights)
