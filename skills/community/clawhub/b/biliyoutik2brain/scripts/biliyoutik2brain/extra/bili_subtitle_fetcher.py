#!/usr/bin/env python3
"""
B站字幕提取 + whisper 交叉验证模块

工作流:
  bvid/cid → api.bilibili.com (字幕JSON)
                 + whisper转录 (by transcriber_bilibili.py)
                 ↓
            领域纠错词典 → 交叉比对 → 最优输出

字幕源优先级:
  1. 创作者上传字幕 (subtitles[].lan != 'ai' 且允许公开)
  2. B站AI字幕 (need_login_subtitle=False 时可直接拿)
  3. 需登录的AI字幕 (通过浏览器fetch代理 或 cookie)
  4. whisper转录兜底

认证策略:
  - 直接cookie: 从 ~/.openclaw/bilibili_cookies.json 读取
  - 浏览器代理: 调用 evaluate + fetch (自动携带HttpOnly cookie)
"""

import json
import os
import re
import subprocess
import sys
import time
from typing import Dict, List, Optional, Tuple

import requests

# ─── 辅助函数（取代 transcriber_bilibili 依赖） ───────

def _get_video_info_by_bvid(bvid: str) -> Optional[Dict]:
    """从 B站 API 获取视频基础信息"""
    try:
        r = requests.get(
            f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}",
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com"},
            timeout=15,
        )
        data = r.json()
        if data.get("code") == 0:
            d = data["data"]
            return {
                "bvid": d["bvid"],
                "cid": d.get("cid", 0),
                "title": d["title"],
            }
    except Exception:
        pass
    return None


# ─── 配置 ─────────────────────────────────────────────

BROWSER_CDP_PORT = 18800
COOKIE_FILE = os.path.expanduser("~/.openclaw/bilibili_cookies.json")
API_BASE = "https://api.bilibili.com"

# ─── 领域纠错词典 ──────────────────────────────────────
# 来源: 从之前转录积累的交易术语ASR常见错误
# 格式: { 错误写法: 正确写法 }
_CORRECTIONS = {
    # whisper 常见错误 (从 #001-#004 积累)
    "单里吃": "单笔",
    "单米值": "单笔值", "单米": "单笔",
    "三榜": "三宝", "三绑": "三宝",  # 杰克三宝
    "脏色": "止损",
    "防抗过": "怕是空",
    "进热真乐": "境界",
    "大台街": "大台阶",
    "一符一符": "一笔一笔",
    "一服一服": "一笔一笔",
    "单位吃": "单笔",
    "单位": "单边",
    "脏是": "止损",
    "脏收": "止损",
    "脏帅": "止损",
    "刺射": "亏损",
    "吃算": "持仓",
    "刺数": "亏损",
    "刺率": "亏损率",
    "五路": "五手",
    "八大手": "八手",
    "黑线": "K线",
    "运线": "均线",
    "运线上坡": "均线上坡",
    "三分": "三分",
    "十分": "十分",
    "一十五": "15倍",
    "两万元": "两万块",
    "赔四百五": "赔450",
    "两万零一百三十二": "20132",
    "一七三三零": "17330",
    "一比一减掉": "1:1减掉",
    "初始东西": "初始资金",
    "初始零": "初始0",
    "这个东西桌子": "这个数字",
    # B站字幕可能犯的错
    "15倍的一块钱": "15倍盈亏比",
}

# ─── Cookie 加载 ──────────────────────────────────────


def load_cookies() -> Dict[str, str]:
    """从保存的cookie文件加载B站cookie"""
    if not os.path.exists(COOKIE_FILE):
        return {}
    try:
        with open(COOKIE_FILE) as f:
            cookies_raw = json.load(f)
        cookies = {}
        for c in cookies_raw:
            if c.get("domain", "").endswith("bilibili.com"):
                cookies[c["name"]] = c["value"]
        return cookies
    except Exception:
        return {}


def has_auth_cookies(cookies: Dict[str, str]) -> bool:
    """检查是否有足够的认证cookie"""
    return bool(cookies.get("SESSDATA") and cookies.get("bili_jct"))


# ─── 核心API ──────────────────────────────────────────


def fetch_player_v2(bvid: str, cid: int) -> Optional[Dict]:
    """获取 x/player/v2 数据，包含字幕信息
    
    先尝试直接请求（无cookie），如果 need_login_subtitle=True，
    再尝试带cookie请求。
    """
    url = f"{API_BASE}/x/player/v2?bvid={bvid}&cid={cid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Referer": f"https://www.bilibili.com/video/{bvid}",
    }

    # 第1步：无cookie尝试
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("code") == 0:
                return data["data"]
    except Exception:
        pass

    # 第2步：带cookie尝试
    cookies = load_cookies()
    if cookies:
        try:
            r = requests.get(
                url, headers=headers, cookies=cookies, timeout=10
            )
            if r.status_code == 200:
                data = r.json()
                if data.get("code") == 0:
                    return data["data"]
        except Exception:
            pass

    return None


def get_subtitle_url(subtitle_data: Dict) -> Optional[str]:
    """从 subtitle 信息中提取字幕URL
    
    优先创作者的，次选AI字幕。
    如果 need_login_subtitle=True 但 subtitles=[]，返回 None。
    """
    need_login = subtitle_data.get("need_login_subtitle", False)
    subtitles = subtitle_data.get("subtitles") or []

    if subtitles:
        # 优先非AI字幕（创作者上传）
        for sub in subtitles:
            lan_doc = sub.get("lan_doc", "").lower()
            sub_url = sub.get("subtitle_url", "")
            # 跳过AI字幕标签，优先人工
            if "ai" not in lan_doc and "auto" not in lan_doc and sub_url:
                return sub_url

        # 没有人工字幕，取第一个（通常是AI）
        first_url = subtitles[0].get("subtitle_url", "")
        if first_url:
            return first_url

    # 需要登录但没有subtitles
    if need_login:
        return None

    return None


def fetch_subtitle_json(subtitle_url: str) -> Optional[Dict]:
    """下载字幕JSON文件"""
    if not subtitle_url:
        return None

    # 补全 https://
    url = subtitle_url
    if url.startswith("//"):
        url = "https:" + url

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Referer": "https://www.bilibili.com/",
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass

    return None


# ─── 浏览器代理（绕过HttpOnly） ───────────────────────


def fetch_via_browser(bvid: str, cid: int) -> Optional[Dict]:
    """通过浏览器获取字幕
    
    注意：CDP websocket 因 origin 限制有 403 问题，
    需要外部调用 browser tool 来获取 subtitle_url，
    然后通过 fetch_subtitle_by_url 下载。
    
    这里尝试直接通过 curl 浏览器 cookies 的方式
    （如果之前保存了 SESSDATA cookie）。
    """
    cookies = load_cookies()
    if not has_auth_cookies(cookies):
        return None
    
    # 走 API 通道（带完整cookie）
    player_data = fetch_player_v2(bvid, cid)
    if not player_data:
        return None
    
    subtitle_info = player_data.get("subtitle", {})
    sub_url = get_subtitle_url(subtitle_info)
    if not sub_url:
        return None
    
    sub_json = fetch_subtitle_json(sub_url)
    if not sub_json:
        return None
    
    body = sub_json.get("body", [])
    if not body:
        return None
    
    return {
        "source": "api_cookie",
        "need_login": subtitle_info.get("need_login_subtitle", False),
        "subtitle_url": sub_url,
        "body": body,
        "count": len(body),
    }


def fetch_subtitle_by_url(subtitle_url: str) -> Optional[Dict]:
    """外部传入 subtitle_url 直接下载字幕JSON
    
    用于经过浏览器获取 URL 后调用的场景。
    """
    sub_json = fetch_subtitle_json(subtitle_url)
    if not sub_json:
        return None
    
    body = sub_json.get("body", [])
    if not body:
        return None
    
    return {
        "source": "external_url",
        "subtitle_url": subtitle_url,
        "body": body,
        "count": len(body),
        "text": subtitle_text_plain(body),
    }


# ─── 文本处理 ─────────────────────────────────────────


def subtitle_body_to_text(body: List[Dict]) -> str:
    """将字幕body数组转为纯文本（保留时间信息）"""
    lines = []
    for seg in body:
        content = seg.get("content", "").strip()
        from_sec = seg.get("from", 0)
        to_sec = seg.get("to", 0)
        if content:
            lines.append({
                "text": content,
                "from": from_sec,
                "to": to_sec,
            })
    return lines


def subtitle_text_plain(body: List[Dict]) -> str:
    """只拼接文本，不保留时间"""
    return "\n".join(seg.get("content", "").strip() for seg in body if seg.get("content", "").strip())


def apply_corrections(text: str, corrections: Dict[str, str] = None) -> str:
    """对文本应用领域纠错词典"""
    if corrections is None:
        corrections = _CORRECTIONS
    result = text
    for wrong, correct in corrections.items():
        result = result.replace(wrong, correct)
    return result


def cross_validate(subtitle_text: str, whisper_text: str, 
                   source_label: str = "subtitle") -> Dict:
    """交叉验证字幕 vs whisper
    
    返回结构:
    {
        "primary": str,          # 选定的主文本
        "confidence": float,     # 置信度 0-1
        "corrections_applied": int,
        "sources": {
            "subtitle": { "text": str, "length": int },
            "whisper": { "text": str, "length": int },
        },
        "merged": str,           # 合并后的最优文本
    }
    """
    sub_clean = apply_corrections(subtitle_text.strip())
    wh_clean = apply_corrections(whisper_text.strip())

    sub_len = len(sub_clean)
    wh_len = len(wh_clean)
    wh_ok = wh_len > 20  # whisper有足够内容

    result = {
        "sources": {
            "subtitle": {"text": sub_clean, "length": sub_len},
            "whisper": {"text": wh_clean, "length": wh_len},
        },
        "corrections_applied": sum(
            1 for w, c in _CORRECTIONS.items()
            if w in subtitle_text + whisper_text
        ),
    }

    # 策略：谁更长/更可信
    if sub_len > 50 and wh_ok:
        # 两者都有内容：字幕优先（B站模型更好），whisper补充
        merged = sub_clean
        # 如果在whisper中发现字幕没有的段落，追加
        wh_lines = [l.strip() for l in wh_clean.split("\n") if len(l.strip()) > 5]
        for line in wh_lines:
            if line not in sub_clean:
                merged += "\n" + line
        result["primary"] = sub_clean
        result["merged"] = merged
        result["confidence"] = min(1.0, 0.7 + 0.3 * (sub_len / max(sub_len, wh_len)))
    elif sub_len > 50:
        result["primary"] = sub_clean
        result["merged"] = sub_clean
        result["confidence"] = 0.7
    elif wh_ok:
        result["primary"] = wh_clean
        result["merged"] = wh_clean
        result["confidence"] = 0.5
    else:
        result["primary"] = subtitle_text or whisper_text or ""
        result["merged"] = subtitle_text or whisper_text or ""
        result["confidence"] = 0.0

    return result


# ─── 主流程 ──────────────────────────────────────────


def fetch_subtitle(bvid: str, cid: int, 
                   use_browser: bool = False,
                   preauth_url: str = None) -> Optional[Dict]:
    """获取B站字幕
    
    Args:
        bvid: B站视频BV号
        cid: 分P的CID
        use_browser: 通过cookie文件认证（需SESSDATA在cookie文件中）
        preauth_url: 浏览器获取的已验证subtitle_url（绕过认证限制）
    
    认证策略:
        1. preauth_url 优先（用户通过浏览器预先获取的URL）
        2. API直接请求（无cookie，可获取公开字幕）
        3. 带cookie请求（需SESSDATA，HttpOnly限制）
        4. 返回空结果 → 回退whisper
    
    Returns:
        {
            "source": str | None,     # 数据来源
            "available": bool,        # 是否有字幕可用
            "need_login": bool,       # 是否需要登录
            "subtitle_url": str|None, # 字幕URL
            "body": List[Dict]|None,  # 字幕段
            "text": str,              # 纯文本
            "segments": List[Dict],   # 含时间戳
        }
    """
    result = {
        "source": None,
        "available": False,
        "need_login": False,
        "subtitle_url": None,
        "body": None,
        "text": "",
        "segments": [],
    }

    # 方案1: 外部已验证的URL
    if preauth_url:
        sub_json = fetch_subtitle_json(preauth_url)
        if sub_json:
            body = sub_json.get("body", [])
            if body:
                result.update({
                    "source": "preauth_url",
                    "available": True,
                    "subtitle_url": preauth_url,
                    "body": body,
                    "segments": subtitle_body_to_text(body),
                    "text": subtitle_text_plain(body),
                })
                return result

    # 方案2: 带cookie的API
    if use_browser:
        cookies = load_cookies()
        if cookies:
            player_data = fetch_player_v2(bvid, cid)
            if player_data:
                subtitle_info = player_data.get("subtitle", {})
                sub_url = get_subtitle_url(subtitle_info)
                if sub_url:
                    sub_json = fetch_subtitle_json(sub_url)

        if cookies and not sub_json:
            # 可能有cookie但没有SESSDATA，从player response检测
            pass

    # 方案3: 无cookie直接API
    if not result["available"]:
        player_data = fetch_player_v2(bvid, cid)
        if player_data:
            subtitle_info = player_data.get("subtitle", {})
            need_login = subtitle_info.get("need_login_subtitle", False)
            result["need_login"] = need_login
            subtitles = subtitle_info.get("subtitles") or []
            
            # 如果公开字幕存在，直接下载
            if not need_login and subtitles:
                sub_url = get_subtitle_url(subtitle_info)
                if sub_url:
                    sub_json = fetch_subtitle_json(sub_url)
                    if sub_json:
                        body = sub_json.get("body", [])
                        if body:
                            result.update({
                                "source": "api_direct",
                                "available": True,
                                "subtitle_url": sub_url,
                                "body": body,
                                "segments": subtitle_body_to_text(body),
                                "text": subtitle_text_plain(body),
                            })
                            return result
    return result


def subtitle_quality_check(text: str) -> float:
    """检查字幕质量：转录内容是否与标题描述匹配（领域内容检测）

    返回质量分 0-1:
    - 领域术语密度
    - 是否包含完整语句
    - 是否有明显无效内容（乱码、重复）
    """
    if not text or len(text) < 20:
        return 0.0

    # 交易领域关键词
    domain_kw = [
        "交易", "盈亏", "止损", "止盈", "仓位", "做多", "做空", "卖出", "买入",
        "资金", "风险", "收益", "成本", "行情", "单边", "趋势", "点位", "指标",
        "利润", "本金", "手数", "杠杆", "期货", "外汇", "股票", "K线", "均线",
        "市场", "投资", "涨跌", "回调",
    ]

    # 常见无效模式
    bad_patterns = [
        r"^.{0,5}$",                        # 过短
        r"^(这个|那个|一个|可以|就是|我们|你们|他们|这样|那样)$",  # 无意义词
        r"^[哈哈呵呵嘿嘿哦哦啊啊嗯嗯]+$",     # 语气词重复
    ]

    text_lower = text.lower()
    found_kw = sum(1 for kw in domain_kw if kw in text_lower)
    kw_score = min(1.0, found_kw / 5)  # 5个关键词=满分

    # 检测完整句子（有标点 + 超过5字）
    sentences = re.findall(r'[^。！？\n]{5,}[。！？]', text)
    sent_score = min(1.0, len(sentences) / 3)

    # 检测无效模式
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    bad_lines = sum(1 for l in lines if any(re.match(p, l) for p in bad_patterns))
    bad_ratio = bad_lines / max(len(lines), 1)

    quality = kw_score * 0.5 + sent_score * 0.3 + (1 - bad_ratio) * 0.2
    return min(1.0, quality)


# ─── 自测 ─────────────────────────────────────────────


def test_single(bvid: str, cid: int = None, use_browser: bool = False):
    """测试单个视频的字幕提取"""
    print(f"\n{'='*60}")
    print(f"测试: {bvid}")
    
    # 如果没给cid，先获取
    if not cid:
        info = _get_video_info_by_bvid(bvid)
        if info:
            cid = info.get("cid")
            print(f"  CID: {cid}")

    if not cid:
        print("  ❌ 无法获取CID")
        return

    # 提取字幕
    result = fetch_subtitle(bvid, cid, use_browser=use_browser)
    
    print(f"  源: {result['source'] or '❌ 无字幕'}")
    print(f"  需登录: {result['need_login']}")
    print(f"  字幕段数: {len(result.get('body') or [])}")
    print(f"  字幕文本长度: {len(result.get('text') or '')}")
    
    if result["text"]:
        quality = subtitle_quality_check(result["text"])
        print(f"  质量分: {quality:.2f}")
        print(f"\n  前200字:")
        print(f"  {'─'*40}")
        for line in result["text"].split("\n")[:10]:
            print(f"  {line[:80]}")
    else:
        print("  无字幕文本")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="B站字幕提取 + 交叉验证")
    parser.add_argument("bvid", help="B站视频BV号")
    parser.add_argument("--cid", type=int, help="分P CID（可选）")
    parser.add_argument("--browser", action="store_true", help="使用浏览器代理（支持HttpOnly cookie）")
    parser.add_argument("--cross", help="whisper转录文本文件路径（交叉验证）")
    
    args = parser.parse_args()
    
    result = fetch_subtitle(args.bvid, args.cid, use_browser=args.browser)
    
    if result["text"]:
        print(f"\n✅ 字幕提取成功 | 源: {result['source']} | {len(result.get('body') or [])}段")
        print(f"质量分: {subtitle_quality_check(result['text']):.2f}")
        
        if args.cross and os.path.exists(args.cross):
            whisper_text = open(args.cross, 'r', encoding='utf-8').read()
            cv = cross_validate(result["text"], whisper_text)
            print(f"\n交叉验证结果:")
            print(f"  置信度: {cv['confidence']:.2f}")
            print(f"  修正数: {cv['corrections_applied']}")
            print(f"  字幕长度: {len(cv['sources']['subtitle']['text'])}")
            print(f"  whisper长度: {len(cv['sources']['whisper']['text'])}")
    else:
        print(f"\n❌ 无可用字幕")
        print(f"  需登录: {result['need_login']}")
