#!/usr/bin/env python3
"""MaxAEO 开放 API 命令行：到豆包、DeepSeek、腾讯元宝等 AI 平台真实提问，
看回答有没有提到你的品牌、排第几、和哪些竞品一起出现、引用了哪些网页，并生成一份可转发的报告。

只用 Python 标准库（3.8+），不需要 pip 安装任何东西。没有 Key 时不会调用接口。

用法：
  python3 maxaeo.py ask --question "孩子6岁零基础，英语启蒙APP哪个好？" --brand "伴鱼|伴鱼绘本"            # 只看计划和点数
  python3 maxaeo.py ask --question "…" --question "…" --brand 伴鱼 --platforms doubao,deepseek --confirm   # 真正提问
  python3 maxaeo.py report --file maxaeo_results/xxx.json --brand 伴鱼 --competitors "斑马|斑马AI课,叽里呱啦"
  python3 maxaeo.py set-key gdev_xxx
  python3 maxaeo.py get --task-id task_xxx --brand 伴鱼
  python3 maxaeo.py platforms
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SKILL_SLUG = "geo-yuanbao-brand-rank"  # 打包时按技能替换，用来区分用户从哪个技能来
SKILL_VERSION = "1.0.0"
BASE_URL = "https://maxaeo.cn/geoapi/geodata/developer"
CONSOLE_URL = ("https://maxaeo.cn/developers/?utm_source=clawhub&utm_medium=skill"
               f"&utm_campaign=developer-api&utm_content={SKILL_SLUG}")
USER_AGENT = f"{SKILL_SLUG}/{SKILL_VERSION} (clawhub)"
KEY_FILE = os.path.join(os.path.expanduser("~"), ".maxaeo", "api_key")
RESULT_DIR = "maxaeo_results"
TERMINAL = {"succeeded", "failed", "canceled"}
RETRYABLE = {-1, 1024, 1025}
DEFAULT_PLATFORMS = "yuanbao"
MAX_QUESTIONS = 5

# 平台快照（2026-11）。p2 = 标准档每次成功扣的点数，优先档（p1）翻倍。以 platforms 命令的实时单价为准。
PLATFORMS = [
    ("doubao", "豆包", 3), ("deepseek", "DeepSeek", 3), ("kimi", "Kimi", 20), ("yuanbao", "腾讯元宝", 3),
    ("qianwen", "千问", 3), ("wenxin", "文心一言", 3), ("zhipu", "智谱清言", 3), ("xunfei", "讯飞星火", 3),
    ("metaso", "秘塔 AI 搜索", 3), ("xiaohongshu", "小红书点点", 3),
    ("chatgpt", "ChatGPT", 3), ("gemini", "Gemini", 3), ("claude", "Claude", 5), ("perplexity", "Perplexity", 3),
    ("copilot", "Copilot", 5), ("grok", "Grok", 3), ("google-ai-mode", "Google AI Mode", 3),
    ("google-ai-overview", "Google AI Overviews", 3),
]
NAMES = {p: n for p, n, _ in PLATFORMS}
P2_PRICE = {p: c for p, _, c in PLATFORMS}


# ---------- Key ----------

def api_key():
    key = os.environ.get("MAXAEO_API_KEY", "").strip()
    if key:
        return key
    try:
        with open(KEY_FILE, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def key_help():
    return (
        "还差一步：需要一个 MaxAEO 的 Key（这一步没有花任何点数）。\n"
        f"  1. 打开 {CONSOLE_URL}\n"
        "  2. 手机号登录（新账号送 100 点）\n"
        "  3. 在「API Key」页点「创建」，复制那串 gdev_ 开头的 Key\n"
        "  4. 把 Key 粘贴发到这里，我保存好就直接开始，以后不用再给"
    )


# ---------- HTTP ----------

class MaxAEOError(Exception):
    def __init__(self, ret, msg):
        self.ret = ret
        try:
            self.message = json.loads(msg).get("zh") or msg  # msg 是 {"zh","en"} JSON 字符串
        except (TypeError, ValueError, AttributeError):
            self.message = msg
        super().__init__(f"ret={ret}: {self.message}")


class HTTPStatusError(Exception):
    def __init__(self, status):
        self.status = status
        super().__init__(f"HTTP {status}")


def post(path, body, timeout=30, key=None):
    req = urllib.request.Request(
        BASE_URL + path,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key or api_key()}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        raise HTTPStatusError(e.code) from None
    data = json.loads(raw.decode("utf-8"))  # 不看 Content-Type，直接按 UTF-8 JSON 解析
    if data.get("ret") != 1:
        raise MaxAEOError(data.get("ret"), data.get("msg", ""))
    return data["data"]["ent"]


def read(path, body, retries=4):
    """查询类接口可以安全重试。"""
    for attempt in range(retries + 1):
        try:
            return post(path, body)
        except (urllib.error.URLError, TimeoutError, OSError, HTTPStatusError, MaxAEOError) as e:
            retryable = not isinstance(e, MaxAEOError) or e.ret in RETRYABLE
            if isinstance(e, HTTPStatusError) and e.status in (401, 404, 405):
                retryable = False
            if not retryable or attempt == retries:
                raise
            time.sleep(2 ** (attempt + 1))
    raise RuntimeError("unreachable")


def submit(platform, query, priority):
    """提交不是幂等的：结果不明时先用 /task/key/list 找回，确认没有才重新提交，避免重复扣点。"""
    body = {"platform": platform, "query": query, "priority": priority}
    started = int(time.time()) - 60
    for attempt in range(5):
        try:
            return post("/task/submit", body)
        except MaxAEOError as e:
            if e.ret in (1024, 1025):  # 被限流，确定没有创建任务
                time.sleep(15 * (2 ** attempt))
                continue
            if e.ret != -1:
                raise
        except HTTPStatusError as e:
            if e.status in (401, 404, 405):
                raise
        except (urllib.error.URLError, TimeoutError, OSError):
            pass
        found = read("/task/key/list", {
            "keyword": query.strip()[:256], "platform": platform, "start_time": started, "page_size": 5,
        })
        if found.get("items"):
            return read("/task/get", {"task_id": found["items"][0]["task_id"]})
    raise RuntimeError("提交多次未成功，请稍后再试")


# ---------- 分析 ----------

def parse_names(raw):
    """"伴鱼|伴鱼绘本,斑马" → [["伴鱼","伴鱼绘本"],["斑马"]]。第一个是显示名，后面是别名。"""
    out = []
    for item in (raw or "").replace("，", ",").split(","):
        names = [n.strip() for n in item.split("|") if n.strip()]
        if names:
            out.append(names)
    return out


def first_pos(text, aliases):
    low = text.lower()
    hits = [low.find(a.lower()) for a in aliases]
    hits = [h for h in hits if h >= 0]
    return min(hits) if hits else -1


def refs_of(task):
    return (task.get("raw_result") or {}).get("references") or []


# 常见信源按「站」归并：子域名合到一起，并给出中文名
SITE_LABELS = [
    ("mp.weixin.qq.com", "微信公众号"), ("baike.baidu.com", "百度百科"), ("baijiahao.baidu.com", "百家号"),
    ("zhidao.baidu.com", "百度知道"), ("tieba.baidu.com", "百度贴吧"), ("zhihu.com", "知乎"),
    ("xiaohongshu.com", "小红书"), ("douyin.com", "抖音"), ("iesdouyin.com", "抖音"), ("bilibili.com", "B站"), ("smzdm.com", "什么值得买"),
    ("toutiao.com", "今日头条"), ("sohu.com", "搜狐"), ("163.com", "网易"), ("qq.com", "腾讯网"),
    ("tousu.sina.com.cn", "黑猫投诉"), ("sina.com.cn", "新浪"), ("sina.cn", "新浪"), ("weibo.com", "微博"), ("csdn.net", "CSDN"), ("jd.com", "京东"), ("taobao.com", "淘宝"),
    ("douban.com", "豆瓣"), ("wikipedia.org", "维基百科"), ("youtube.com", "YouTube"), ("reddit.com", "Reddit"),
]


def domain_of(url):
    """返回 (归并键, 显示名)。"""
    try:
        host = (urllib.parse.urlparse(url or "").hostname or "").lower()
    except ValueError:
        return "", ""
    if not host:
        return "", ""
    for suffix, label in SITE_LABELS:
        if host == suffix or host.endswith("." + suffix):
            return label, label
    parts = host.split(".")
    n = 3 if len(parts) >= 3 and parts[-2] in ("com", "net", "org", "gov", "edu") and len(parts[-1]) == 2 else 2
    root = ".".join(parts[-n:])
    return root, root


def analyze(tasks, brand, competitors):
    """每个成功回答里：哪些品牌出现了、按出现先后排第几；所有回答的引用域名汇总。"""
    groups = ([brand] if brand else []) + competitors
    rows = []
    for t in tasks:
        row = {"task": t, "ok": t.get("status") == "succeeded", "order": [], "rank": None,
               "brand_in_q": bool(brand) and first_pos(t.get("query") or "", brand) >= 0}
        if row["ok"]:
            answer = t.get("answer") or ""
            pos = [(first_pos(answer, g), g[0]) for g in groups]
            row["order"] = [name for p, name in sorted(pos) if p >= 0]
            if brand and brand[0] in row["order"] and not row["brand_in_q"]:
                row["rank"] = row["order"].index(brand[0]) + 1
        rows.append(row)
    ok_rows = [r for r in rows if r["ok"]]
    rank_rows = [r for r in ok_rows if not r["brand_in_q"]]  # 问题里直接带了品牌的，不算推荐和排名
    share = []
    for g in groups:
        n = sum(1 for r in rank_rows if g[0] in r["order"])
        ranks = [r["order"].index(g[0]) + 1 for r in rank_rows if g[0] in r["order"]]
        share.append({"name": g[0], "hits": n, "total": len(rank_rows),
                      "avg_rank": round(sum(ranks) / len(ranks), 1) if ranks else None,
                      "is_brand": bool(brand) and g is brand})
    share.sort(key=lambda s: (-s["hits"], s["avg_rank"] or 99))
    domains = {}
    for r in ok_rows:
        for ref in refs_of(r["task"]):
            d, label = domain_of(ref.get("url"))
            if not d:
                continue
            e = domains.setdefault(d, {"domain": label, "refs": 0, "cited": 0, "known": 0, "platforms": set()})
            e["refs"] += 1
            e["cited"] += 1 if ref.get("cited") is True else 0
            e["known"] += 1 if ref.get("cited") in (True, False) else 0
            e["platforms"].add(str(NAMES.get(r["task"].get("platform"), r["task"].get("platform"))))
    top_domains = sorted(domains.values(), key=lambda e: (-e["cited"], -e["refs"]))[:15]
    for e in top_domains:
        e["platforms"] = sorted(e["platforms"])
    cited_refs = {}
    for r in ok_rows:
        for ref in refs_of(r["task"]):
            url = ref.get("url") or ""
            if not url or ref.get("cited") is not True:
                continue
            c = cited_refs.setdefault(url, {"title": ref.get("title") or "", "url": url, "n": 0, "platforms": set()})
            c["n"] += 1
            c["platforms"].add(str(NAMES.get(r["task"].get("platform"), r["task"].get("platform"))))
    top_cited = sorted(cited_refs.values(), key=lambda c: -c["n"])[:10]
    for c in top_cited:
        c["platforms"] = sorted(c["platforms"])
    brand_domains = []
    if brand:
        for r in ok_rows:
            for ref in refs_of(r["task"]):
                blob = " ".join(str(ref.get(k) or "") for k in ("title", "url", "source", "domain", "snippet"))
                if first_pos(blob, brand) >= 0:
                    brand_domains.append((NAMES.get(r["task"].get("platform")), ref.get("title") or "", ref.get("url") or ""))
    share = [x for x in share if x["total"]]
    return {"rows": rows, "share": share, "domains": top_domains, "brand_refs": brand_domains, "top_cited": top_cited,
            "ranked": bool(competitors),
            "spent": sum(t.get("credits") or 0 for t in tasks)}


# ---------- 输出 ----------

def status_zh(t):
    return {"succeeded": "成功", "failed": "失败", "canceled": "已取消"}.get(t.get("status"), "还在跑")


def print_markdown(result, brand, questions):
    rows = result["rows"]
    multi_q = len(questions) > 1
    head = "| " + ("问题 | " if multi_q else "") + "平台 | " + (f"提到「{brand[0]}」 | 排第几 | " if brand else "") + "回答里出现的品牌（按先后） | 扣点 |"
    print(head)
    print("|" + "---|" * (head.count("|") - 1))
    for r in rows:
        t = r["task"]
        qi = questions.index(t.get("query")) + 1 if t.get("query") in questions else "?"
        cells = []
        if multi_q:
            cells.append(f"Q{qi}")
        cells.append(NAMES.get(t.get("platform"), t.get("platform")))
        if brand:
            if r["ok"] and r["brand_in_q"]:
                cells += ["问题里就有", "不排"]
            elif r["ok"]:
                rank = (f"第 {r['rank']}" if r["rank"] else "—") if result["ranked"] else ("出报告时算" if r["rank"] else "—")
                cells += ["是" if r["rank"] else "否", rank]
            else:
                cells += [status_zh(t), "—"]
        cells.append("、".join(r["order"]) if r["ok"] and r["order"] else ("（没有识别到已知品牌）" if r["ok"] else "—"))
        cells.append(str(t.get("credits") or 0))
        print("| " + " | ".join(cells) + " |")
    if multi_q:
        for i, q in enumerate(questions, 1):
            print(f"Q{i}：{q}")
    if len(result["share"]) > 1:
        print("\n品牌被推荐的次数（只算问题里没点名品牌的回答）：")
        for s in result["share"]:
            avg = f"，平均排第 {s['avg_rank']}" if s["avg_rank"] else ""
            print(f"  - {s['name']}{'（你）' if s['is_brand'] else ''}：{s['hits']}/{s['total']}{avg}")
    if result["domains"]:
        print("\nAI 最常引用的网站：")
        for e in result["domains"][:8]:
            cited = f"正文引用 {e['cited']} 次，" if e["known"] else "（平台未标注是否引用）"
            print(f"  - {e['domain']}：{cited}出现在 {e['refs']} 条来源里（{'、'.join(e['platforms'])}）")
    if result["top_cited"]:
        print("\n被正文引用的文章：")
        for c in result["top_cited"][:8]:
            print(f"  - {c['title']} {c['url']}（{'、'.join(c['platforms'])}）")
    if brand:
        if result["brand_refs"]:
            print(f"\n来源里和「{brand[0]}」直接相关的网页：")
            for p, title, url in result["brand_refs"][:6]:
                print(f"  - [{p}] {title} {url}".rstrip())
        else:
            print(f"\n来源里没有一条是「{brand[0]}」自己的网页或直接写它的网页。")
    print(f"\n本次共扣 {result['spent']} 点。每个平台只问了一次，结论是「这次提到 / 没提到」，不是稳定的提及率。")


def render_html(result, brand, questions, made_at):
    e = html.escape
    rows = result["rows"]
    ok_rows = [r for r in rows if r["ok"]]
    rank_rows = [r for r in ok_rows if not r["brand_in_q"]]
    hit = sum(1 for r in rank_rows if r["rank"])
    title = f"{brand[0]} 的 AI 搜索曝光速查" if brand else "AI 平台回答速查"
    tiles = [("成功回答", f"{len(ok_rows)}/{len(rows)}")]
    if brand:
        ranks = [r["rank"] for r in rank_rows if r["rank"]]
        tiles += [("推荐了你的回答", f"{hit}/{len(rank_rows)}" if rank_rows else "—"),
                  ("提到时平均排第", f"{sum(ranks) / len(ranks):.1f}" if ranks and result["ranked"] else "—")]
    tiles.append(("本次扣点", str(result["spent"])))
    trs = []
    for r in rows:
        t = r["task"]
        name = str(NAMES.get(t.get("platform"), t.get("platform")))
        q = questions.index(t.get("query")) + 1 if t.get("query") in questions else "?"
        if not r["ok"]:
            badge = f'<span class="b off">{e(status_zh(t))}</span>'
        elif not brand:
            badge = ""
        elif r["brand_in_q"]:
            badge = '<span class="b off">问题含品牌 · 看口碑</span>'
        elif r["rank"]:
            badge = f'<span class="b yes">提到 · 第 {r["rank"]}</span>' if result["ranked"] else '<span class="b yes">提到</span>'
        else:
            badge = '<span class="b no">没提到</span>'
        order = "、".join(e(n) for n in r["order"]) if r["order"] else "—"
        trs.append(f"<tr><td>{'Q' + str(q) + ' · ' if len(questions) > 1 else ''}{e(name)}</td><td>{badge}</td><td>{order}</td></tr>")
    share_rows = []
    top = max([s["hits"] for s in result["share"]] + [1])
    for s in result["share"]:
        w = int(100 * s["hits"] / top) if top else 0
        share_rows.append(
            f'<div class="bar{" me" if s["is_brand"] else ""}"><span class="n">{e(s["name"])}</span>'
            f'<span class="t"><i style="width:{w}%"></i></span><span class="v">{s["hits"]}/{s["total"]}'
            f'{" · 均第 " + str(s["avg_rank"]) if s["avg_rank"] else ""}</span></div>')
    dom_rows = "".join(
        f"<tr><td>{e(d['domain'])}</td><td>{(str(d['cited']) if d['known'] else '未标注') + ' / ' + str(d['refs'])}</td><td>{e('、'.join(d['platforms']))}</td></tr>"
        for d in result["domains"][:12])
    details = []
    for r in rows:
        t = r["task"]
        if not r["ok"]:
            continue
        name = str(NAMES.get(t.get("platform"), t.get("platform")))
        ans = e(t.get("answer") or "")
        if brand:
            for alias in sorted(brand, key=len, reverse=True):
                ans = re.sub(re.escape(e(alias)), lambda m: f"<mark>{m.group(0)}</mark>", ans, flags=re.I)
        link = f' · <a href="{e(t["share_link"])}" target="_blank" rel="noopener">在 {e(name)} 打开</a>' if t.get("share_link") else ""
        details.append(f"<details><summary>{e(name)}：{e(t.get('query') or '')}{link}</summary><div class=\"ans\">{ans}</div></details>")
    qs = "".join(f"<li>{e(q)}</li>" for q in questions)
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><style>
:root{{--bg:#f6f7f9;--card:#fff;--ink:#16181d;--mute:#667085;--line:#e4e7ec;--acc:#2f5bea;--yes:#0f9d58;--no:#d93025}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0f1115;--card:#171a21;--ink:#e8eaed;--mute:#9aa0a6;--line:#2a2f3a;--acc:#7b9bff;--yes:#34c27a;--no:#ff6b5f}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif}}
.w{{max-width:920px;margin:0 auto;padding:28px 16px 48px}}h1{{font-size:24px;margin:0 0 4px}}h2{{font-size:17px;margin:28px 0 10px}}
.sub{{color:var(--mute);font-size:13px}}.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-top:18px}}.tile .k{{color:var(--mute);font-size:13px}}.tile .v{{font-size:26px;font-weight:600}}
table{{width:100%;border-collapse:collapse}}td,th{{padding:8px 6px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;font-size:14px}}th{{color:var(--mute);font-weight:500;white-space:nowrap}}
.b{{display:inline-block;padding:1px 8px;border-radius:99px;font-size:12px;white-space:nowrap}}.yes{{background:color-mix(in srgb,var(--yes) 15%,transparent);color:var(--yes)}}
.no{{background:color-mix(in srgb,var(--no) 13%,transparent);color:var(--no)}}.off{{background:var(--line);color:var(--mute)}}
.bar{{display:grid;grid-template-columns:110px 1fr 110px;gap:10px;align-items:center;margin:6px 0;font-size:14px}}.bar .t{{background:var(--line);border-radius:99px;height:8px;overflow:hidden}}
.bar i{{display:block;height:100%;background:var(--mute)}}.bar.me i{{background:var(--acc)}}.bar.me .n{{font-weight:600;color:var(--acc)}}.bar .v{{color:var(--mute);font-size:13px}}
details{{border-top:1px solid var(--line);padding:10px 0}}summary{{cursor:pointer}}.ans{{white-space:pre-wrap;color:var(--ink);font-size:14px;margin-top:8px}}
mark{{background:color-mix(in srgb,var(--acc) 25%,transparent);color:inherit;padding:0 2px;border-radius:3px}}a{{color:var(--acc)}}
.note{{color:var(--mute);font-size:13px;margin-top:10px}}.foot{{margin-top:32px;color:var(--mute);font-size:13px}}
@media (max-width:560px){{.bar{{grid-template-columns:72px 1fr auto}}.bar .v{{font-size:12px}}td,th{{font-size:13px;padding:7px 4px}}}}
</style></head><body><div class="w">
<h1>{e(title)}</h1><div class="sub">{e(made_at)} 实测 · 到真实 AI 平台提问，不是模拟</div>
<div class="card" style="margin-top:14px"><div class="sub">问的问题</div><ol style="margin:6px 0 0;padding-left:20px">{qs}</ol></div>
<div class="tiles">{"".join(f'<div class="card tile"><div class="k">{e(k)}</div><div class="v">{e(v)}</div></div>' for k, v in tiles)}</div>
<h2>各平台怎么答</h2><div class="card"><table><tr><th>平台</th><th>结果</th><th>回答里出现的品牌（按先后）</th></tr>{"".join(trs)}</table>
<div class="note">每个平台只问了一次，AI 每次回答会有出入：这里是「这次提到 / 没提到」，不是稳定的提及率。</div></div>
{('<h2>谁被推荐得最多</h2><div class="sub" style="margin:-4px 0 8px">只算问题里没点名品牌的回答</div><div class="card">' + "".join(share_rows) + '</div>') if len(result["share"]) > 1 else ""}
{('<h2>AI 最常引用的网站</h2><div class="card"><table><tr><th>网站</th><th>正文引用 / 出现</th><th>平台</th></tr>' + dom_rows + '</table><div class="note">想被 AI 推荐，优先在这些网站上有关于你的内容。</div></div>') if dom_rows else ""}
{('<h2>被正文引用的文章</h2><div class="card"><table><tr><th>文章</th><th>平台</th></tr>' + "".join(f'<tr><td><a href="{e(c["url"])}" target="_blank" rel="noopener">{e(c["title"] or c["url"])}</a></td><td>{e("、".join(c["platforms"]))}</td></tr>' for c in result["top_cited"]) + '</table></div>') if result["top_cited"] else ""}
<h2>回答原文</h2><div class="card">{"".join(details) or '<div class="sub">没有成功的回答</div>'}</div>
<div class="foot">数据由 <a href="{e(CONSOLE_URL)}" target="_blank" rel="noopener">MaxAEO 开放 API</a> 实测生成。想长期跟踪这些问题在各 AI 平台的变化，可以用 <a href="https://maxaeo.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=report&utm_content={SKILL_SLUG}" target="_blank" rel="noopener">MaxAEO 品牌监测</a>。</div>
</div></body></html>"""


def save_results(questions, brand_raw, tasks):
    os.makedirs(RESULT_DIR, exist_ok=True)
    path = os.path.join(RESULT_DIR, time.strftime("%Y%m%d-%H%M%S") + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"questions": questions, "brand": brand_raw, "made_at": time.strftime("%Y-%m-%d %H:%M"),
                   "tasks": tasks}, f, ensure_ascii=False)
    return path


def write_report(result, brand, questions, made_at, out):
    with open(out, "w", encoding="utf-8") as f:
        f.write(render_html(result, brand, questions, made_at))
    return out


def parse_platforms(raw):
    platforms = []
    for p in (raw or DEFAULT_PLATFORMS).replace("，", ",").split(","):
        p = p.strip().lower()
        if p and p not in platforms:
            platforms.append(p)
    return platforms


# ---------- 命令 ----------

def cmd_ask(args):
    questions = []
    for q in args.question:
        q = q.strip()
        if q and q not in questions:
            questions.append(q)
    if not questions:
        print("问题不能为空。")
        return 2
    if len(questions) > MAX_QUESTIONS:
        print(f"一次最多 {MAX_QUESTIONS} 个问题，先挑最重要的。")
        return 2
    platforms = parse_platforms(args.platform or args.platforms)
    unknown = [p for p in platforms if p not in P2_PRICE]
    if unknown:
        print(f"不认识的平台：{', '.join(unknown)}。可用：{', '.join(P2_PRICE)}")
        return 2
    mult = 2 if args.priority == 1 else 1
    total = sum(P2_PRICE[p] * mult for p in platforms) * len(questions)
    qtext = "、".join(f"「{q}」" for q in questions)
    plan = (f"问{'、'.join(NAMES[p] for p in platforms)}这 {len(platforms)} 个平台{qtext}"
            f"（{len(questions) * len(platforms)} 次提问），共约 {total} 点，失败不扣。")
    if not api_key():
        print("计划：" + plan)
        print()
        print(key_help())
        return 0
    if not args.confirm:
        print("计划：" + plan)
        print("请先向用户确认；同意后加 --confirm 重新运行。")
        return 0

    tasks, errors, stop = [], [], False
    for q in questions:
        for p in platforms:
            if stop:
                break
            if tasks or errors:
                time.sleep(0.6)
            try:
                tasks.append(submit(p, q, args.priority))
            except MaxAEOError as e:
                if e.ret == 1023:
                    errors.append(f"点数不够，{NAMES[p]}起没有再提交。可以去控制台充值：{CONSOLE_URL}")
                    stop = True
                elif e.ret == 1030:
                    errors.append("Key 有问题，请到控制台检查，或重新发一个 Key。")
                    stop = True
                else:
                    hint = {1029: "这个平台暂时不可用"}.get(e.ret, e.message)
                    errors.append(f"{NAMES[p]}：{hint}（没有扣点）")
            except HTTPStatusError as e:
                errors.append(f"{NAMES[p]}：接口返回 HTTP {e.status}"
                              + ("，Key 无效，请到控制台检查或重新发一个 Key" if e.status == 401 else ""))
                stop = stop or e.status == 401

    deadline = time.time() + args.timeout
    while tasks and any(t["status"] not in TERMINAL for t in tasks) and time.time() < deadline:
        time.sleep(15)
        for i, t in enumerate(tasks):
            if t["status"] not in TERMINAL:
                try:
                    tasks[i] = read("/task/get", {"task_id": t["task_id"]})
                except (MaxAEOError, HTTPStatusError, urllib.error.URLError, TimeoutError, OSError):
                    pass

    for e in errors:
        print(e)
    if not tasks:
        return 1
    path = save_results(questions, args.brand, tasks)
    brand = (parse_names(args.brand) or [None])[0]
    result = analyze(tasks, brand, parse_names(args.competitors))
    print_markdown(result, brand, questions)
    pending = [t for t in tasks if t["status"] not in TERMINAL]
    if pending:
        print("\n还没出结果的（之后用 get 取回，不要重新提问，会重复扣点）：")
        for t in pending:
            print(f"  python3 scripts/maxaeo.py get --task-id {t['task_id']}")
    print(f"\n结果已保存：{path}")
    print("下一步：从上面回答里找出出现的竞品名，运行 report 生成报告（不再扣点）：")
    print(f"  python3 scripts/maxaeo.py report --file {path}"
          + (f" --brand \"{args.brand}\"" if args.brand else "") + " --competitors \"竞品A|别名,竞品B\"")
    if args.answers:
        for r in result["rows"]:
            t = r["task"]
            if r["ok"]:
                print(f"\n## {NAMES.get(t.get('platform'))} · {t.get('query')}")
                print((t.get("answer") or "")[:args.answers])
    return 0


def cmd_report(args):
    try:
        with open(args.file, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        print(f"读不了结果文件：{e}")
        return 1
    brand_raw = args.brand if args.brand is not None else data.get("brand")
    brand = (parse_names(brand_raw) or [None])[0]
    questions = data.get("questions") or []
    tasks = data.get("tasks") or []
    if api_key():  # 补取当时没等到的结果；查询不扣点
        for i, t in enumerate(tasks):
            if t.get("status") not in TERMINAL:
                try:
                    tasks[i] = read("/task/get", {"task_id": t["task_id"]})
                except (MaxAEOError, HTTPStatusError, urllib.error.URLError, TimeoutError, OSError):
                    pass
        with open(args.file, "w", encoding="utf-8") as f:
            json.dump(dict(data, tasks=tasks), f, ensure_ascii=False)
    result = analyze(tasks, brand, parse_names(args.competitors))
    print_markdown(result, brand, questions)
    out = args.html or os.path.splitext(args.file)[0] + ".html"
    write_report(result, brand, questions, data.get("made_at") or "", out)
    print(f"\n报告已生成：{os.path.abspath(out)}（双击用浏览器打开，可以直接转发）")
    return 0


def cmd_set_key(args):
    key = args.key.strip()
    if not key.startswith("gdev_"):
        print("这不像 MaxAEO 的 Key（应该是 gdev_ 开头的一长串），请到控制台复制完整的 Key 再发一次。")
        return 1
    try:
        post("/platforms/get", {}, key=key)
    except HTTPStatusError as e:
        if e.status == 401:
            print("这个 Key 用不了（可能复制不全或已删除），请到控制台重新创建一个再发。")
            return 1
        raise
    except MaxAEOError as e:
        if e.ret == 1030:
            print("这个 Key 用不了（可能复制不全或已删除），请到控制台重新创建一个再发。")
            return 1
        raise
    os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
    fd = os.open(KEY_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(key)
    print(f"Key 已验证并保存在本机（{key[:9]}…{key[-4:]}），以后不用再给。")
    return 0


def cmd_get(args):
    if not api_key():
        print(key_help())
        return 0
    try:
        task = read("/task/get", {"task_id": args.task_id.strip()})
    except MaxAEOError as e:
        print(f"查不到这个任务：{e.message}")
        return 1
    brand = (parse_names(args.brand) or [None])[0]
    print_markdown(analyze([task], brand, []), brand, [task.get("query")])
    if task.get("status") == "succeeded":
        print("\n回答原文：")
        print((task.get("answer") or "")[:3000])
    return 0


def cmd_platforms(_args):
    if not api_key():
        print("平台与单价（标准档每次成功扣的点数，优先档翻倍）：")
        for p, n, c in PLATFORMS:
            print(f"  {p:<20} {n:<18} {c} 点")
        return 0
    ent = read("/platforms/get", {})
    for it in ent.get("items") or []:
        stat = f"近24h成功率 {it['success_rate']:.0%}，中位耗时 {it['p50_duration_seconds']} 秒" if it.get("has_stats") else "暂无统计"
        print(f"  {it['platform']:<20} {NAMES.get(it['platform'], ''):<18} {it['platform_status']:<12} "
              f"P2 {it['p2_credits']} 点 / P1 {it['p1_credits']} 点  {stat}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="MaxAEO：到 AI 平台真实提问，看品牌有没有被提到、排第几、引用了哪些网页")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("ask", help="提问（不加 --confirm 只显示计划和点数）")
    p.add_argument("--question", action="append", required=True, help=f"可以重复，最多 {MAX_QUESTIONS} 个")
    p.add_argument("--brand", help="你的品牌，别名用 | 隔开，例如 \"伴鱼|伴鱼绘本\"")
    p.add_argument("--competitors", help="竞品，逗号分隔，别名用 |，例如 \"斑马|斑马AI课,叽里呱啦\"")
    p.add_argument("--platforms", help=f"逗号分隔，默认 {DEFAULT_PLATFORMS}")
    p.add_argument("--platform", help="只问一个平台时用")
    p.add_argument("--priority", type=int, choices=[1, 2], default=2)
    p.add_argument("--timeout", type=int, default=300, help="最多等多少秒，默认 300")
    p.add_argument("--answers", type=int, default=600, help="每条回答打印多少字，0 不打印，默认 600")
    p.add_argument("--confirm", action="store_true")
    p = sub.add_parser("report", help="用保存的结果生成报告（不扣点）")
    p.add_argument("--file", required=True)
    p.add_argument("--brand")
    p.add_argument("--competitors")
    p.add_argument("--html", help="报告保存路径，默认和结果文件同名 .html")
    p = sub.add_parser("set-key", help="验证并保存 Key")
    p.add_argument("key")
    p = sub.add_parser("get", help="按 task_id 取结果")
    p.add_argument("--task-id", required=True)
    p.add_argument("--brand")
    sub.add_parser("platforms", help="平台列表与单价")
    args = ap.parse_args()
    handlers = {"ask": cmd_ask, "report": cmd_report, "set-key": cmd_set_key, "get": cmd_get, "platforms": cmd_platforms}
    try:
        return handlers[args.cmd](args)
    except MaxAEOError as e:
        tip = "请到控制台检查 Key：" + CONSOLE_URL if e.ret == 1030 else ""
        print(f"MaxAEO 返回错误 {e.ret}：{e.message}。{tip}")
    except HTTPStatusError as e:
        print(f"接口返回 HTTP {e.status}。" + ("Key 无效，请到控制台检查。" if e.status == 401 else ""))
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"连不上 MaxAEO（{e}），请检查网络后再试。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
