#!/usr/bin/env python3
"""B站字幕获取工具 v2 — Wbi签名 + 双路径 + 内容校验

路径1: /x/player/wbi/v2 (带Wbi签名) → 字幕URL列表 → CDN下载 → 校验
路径2: /x/web-interface/view/conclusion/get (带Wbi签名) → AI总结接口内置的AI字幕

校验: 时间覆盖率 + 标题关键词命中
用法: python3 bili_subtitle.py BV1xxx
输出: /tmp/bili_meta/<bvid>/ 下的 subs.json / info.json / result.json
"""
import requests, json, os, sys, re, time
from functools import reduce
from hashlib import md5
from urllib.parse import urlencode

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
COOKIE_FILE = os.path.expanduser("~/.bilibili_cookie.txt")

mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35,
    27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13,
    37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4,
    22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52,
]

def load_cookie():
    for p in [COOKIE_FILE, os.path.expanduser("~/.bilibili_cookie_storage"),
              os.path.expanduser("~/.config/bilibili_transcriber/cookie")]:
        if os.path.exists(p):
            return open(p).read().strip()
    return ""

def get_wbi_keys(session):
    """从 nav 接口获取 img_key/sub_key"""
    r = session.get("https://api.bilibili.com/x/web-interface/nav", timeout=15)
    d = r.json()["data"]["wbi_img"]
    img_key = d["img_url"].rsplit("/", 1)[1].split(".")[0]
    sub_key = d["sub_url"].rsplit("/", 1)[1].split(".")[0]
    return img_key, sub_key

def get_mixin_key(orig):
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, "")[:32]

def enc_wbi(params, img_key, sub_key):
    mixin_key = get_mixin_key(img_key + sub_key)
    params["wts"] = round(time.time())
    params = dict(sorted(params.items()))
    # 过滤特殊字符
    params = {k: "".join(filter(lambda ch: ch not in "!'()*", str(v))) for k, v in params.items()}
    query = urlencode(params)
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()
    params["w_rid"] = wbi_sign
    return params

def validate(body, duration, title):
    """校验字幕有效性，返回 (valid, level, reason)
    strong = 关键词命中+覆盖率; weak = 高覆盖率+足句数; fail = 拒绝
    """
    if not body:
        return False, "fail", "字幕为空"
    last_ts = max(b["to"] for b in body)
    cov = last_ts / duration if duration > 0 else 0
    if cov > 2.0:
        return False, "fail", f"覆盖率异常 {cov:.0%}，可能属于其他视频"
    if cov < 0.5:
        return False, "fail", f"覆盖率过低 {last_ts:.0f}/{duration}s = {cov:.0%}，字幕不完整"
    en_words = re.findall(r"[A-Za-z]{3,}", title)
    zh_words = re.findall(r"[\u4e00-\u9fff]{2,4}", title)
    kws = [k.lower() for k in en_words + zh_words[:5]]
    all_text = " ".join(b["content"] for b in body).lower()
    hits = [k for k in kws if k in all_text]
    if hits:
        return True, "strong", f"OK 强校验 (覆盖率{cov:.0%}, 命中{hits[:3]})"
    if len(body) >= 100 and cov >= 0.7:
        return True, "weak", f"OK 弱校验 (覆盖率{cov:.0%}, {len(body)}句, 关键词零命中但覆盖充分)"
    return False, "fail", f"关键词{kws[:5]}零命中且覆盖率仅{cov:.0%}"

def fetch_player_v2(session, bvid, cid, img_key, sub_key, headers):
    """路径1: player/wbi/v2 签名请求"""
    params = enc_wbi({"bvid": bvid, "cid": cid}, img_key, sub_key)
    r = session.get("https://api.bilibili.com/x/player/wbi/v2",
                    params=params, headers=headers, timeout=15)
    j = r.json()
    if j.get("code") != 0:
        return [], f"code={j.get('code')} {j.get('message')}"
    subs = j.get("data", {}).get("subtitle", {}).get("subtitles", []) or []
    return subs, "ok"

def fetch_conclusion(session, bvid, cid, up_mid, img_key, sub_key, headers):
    """路径2: AI总结接口内置字幕"""
    params = enc_wbi({"bvid": bvid, "cid": cid, "up_mid": up_mid}, img_key, sub_key)
    r = session.get("https://api.bilibili.com/x/web-interface/view/conclusion/get",
                    params=params, headers=headers, timeout=15)
    j = r.json()
    if j.get("code") != 0:
        return None, None, f"code={j.get('code')} {j.get('message')}"
    mr = j.get("data", {}).get("model_result", {})
    summary = mr.get("summary", "")
    # 把 conclusion 的 part_subtitle 转成统一格式
    body = []
    for seg in mr.get("subtitle", []) or []:
        for ps in seg.get("part_subtitle", []) or []:
            body.append({"from": ps["start_timestamp"], "to": ps["end_timestamp"],
                         "content": ps["content"]})
    return summary, body, "ok"

def main(bvid):
    cookie = load_cookie()
    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Referer": f"https://www.bilibili.com/video/{bvid}/"})
    if cookie:
        session.headers["Cookie"] = cookie

    # 视频信息
    r = session.get(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}", timeout=15)
    d = r.json()["data"]
    cid, aid, title, duration = d["cid"], d["aid"], d["title"], d["duration"]
    up_mid = d["owner"]["mid"]
    outdir = f"/tmp/bili_meta/{bvid}"
    os.makedirs(outdir, exist_ok=True)
    json.dump({"bvid": bvid, "aid": aid, "cid": cid, "title": title,
               "duration": duration, "up": d["owner"]["name"], "up_mid": up_mid,
               "stat": d["stat"]},
              open(f"{outdir}/info.json", "w"), ensure_ascii=False)
    print(f"📺 {title} | {d['owner']['name']} | {duration//60}分{duration%60}秒")

    headers = {"Origin": "https://www.bilibili.com"}
    img_key, sub_key = get_wbi_keys(session)

    # ---- 路径1: player/wbi/v2 ----
    subs, msg = fetch_player_v2(session, bvid, cid, img_key, sub_key, headers)
    print(f"路径1 player/wbi/v2: {len(subs)}条字幕 ({msg})")
    result = {"source": None, "valid": False, "body": [], "summary": None}
    cc_subs = [s for s in subs if not s.get("lan", "").startswith("ai-")]
    order = (cc_subs + [s for s in subs if s.get("lan", "").startswith("ai-")])
    for s in order:
        url = s.get("subtitle_url") or s.get("subtitle_url_v2")
        if not url:
            continue
        body = session.get("https:" + url, headers=headers, timeout=30).json().get("body", [])
        ok, level, reason = validate(body, duration, title)
        print(f"  [{s.get('lan')}] 句数={len(body)} 校验: {reason}")
        if ok:
            result = {"source": "player/wbi/v2:" + s.get("lan"), "valid": True,
                      "body": body, "summary": None, "level": level}
            break

    # ---- 路径2: conclusion/get ----
    if not result["valid"]:
        summary, cbody, msg2 = fetch_conclusion(session, bvid, cid, up_mid, img_key, sub_key, headers)
        print(f"路径2 conclusion/get: {len(cbody or [])}条字幕, summary={bool(summary)} ({msg2})")
        if cbody:
            ok, level, reason = validate(cbody, duration, title)
            print(f"  conclusion字幕校验: {reason}")
            if ok:
                result = {"source": "conclusion/get", "valid": True,
                          "body": cbody, "summary": summary, "level": level}
        if not result["valid"] and summary:
            # 字幕缺失/不完整但AI摘要可用（超长视频常见：字幕只生成前几十秒，摘要仍完整）
            result = {"source": "conclusion/get:summary-only", "valid": True,
                      "body": [], "summary": summary, "level": "summary"}
            print(f"  降级使用AI摘要 ({len(summary)}字)")

    json.dump(result, open(f"{outdir}/result.json", "w"), ensure_ascii=False)
    if result["valid"]:
        n = len(result["body"])
        txt = "".join(b["content"] for b in result["body"])
        print(f"✅ 成功: source={result['source']} 句数={n} 字符={len(txt)}")
        print(f"   保存: {outdir}/result.json")
    else:
        print("❌ 两条路径均失败 → 降级: 评论课代表 / Whisper")
    return result["valid"]

if __name__ == "__main__":
    bvid = sys.argv[1] if len(sys.argv) > 1 else None
    if not bvid:
        print("用法: python3 bili_subtitle.py BV1xxx")
        sys.exit(1)
    sys.exit(0 if main(bvid) else 1)
