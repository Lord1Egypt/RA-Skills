#!/usr/bin/env python3
"""
douyin 评论深度抓取(虚拟滚动 harvest, 人类模式默认)
=====================================================

背景:douyin PC web 的评论区是虚拟滚动,初始只渲染 5-6 条 [data-e2e="comment-item"];
需要反复 scroll 容器才触发 lazy load 加载更多。

本脚本的工程化要点(踩过的坑):
1. 滚动容器 selector = .parent-route-container.route-scroll-container
   (不是任何最大的可滚动 div,也不是 window)
2. 评论 item 的 innerText 格式固定:
       user
       ...               <- 占位符,跳过
       评论正文
       1天前·重庆         <- 相对时间 + IP 属地
       123               <- 点赞数
       分享 / 回复 / 展开N条回复  <- 操作按钮
3. `...` 那一行必须跳过 - 不是截断,是 douyin 的 UI 占位符
4. ab eval 返回值有"最外层双引号 + unicode escape"两层,需要 json.loads 两次
5. localStorage 是可靠的中转(无 ab eval 输出限制)
6. 必须串行 - ab 单 tab 单 session,多 video 不能并行

风控设计(默认人类模式,最低风控):
  - scroll 用 scrollBy(0, 200-500px) 模拟手指拨动,不是 scrollTop=jump
  - 每个 round sleep 1.5-5 秒(读评论节奏),10% 概率长停留 2-6 秒
  - max round 15(原来 25) + limited depth 早停(round > 8 && added < 2)
  - --max 默认 200(原来 500)
  - 视频间 sleep base 25s * random.uniform(0.7, 1.3) (15-40s 区间)
  - 可选 --warmup:抓前先刷 5-15s 推荐流,看一两个视频再回来(更像真人)
  - --aggressive 走老逻辑(scrollTop=jump, 25 round, 抓满 500),仅在确认低风险时用

用法:
    # 单视频(人类模式默认)
    python3 comments-harvest.py <aweme_id> --max 200

    # 批量(自动串行,视频间 15-40s 间隔)
    python3 comments-harvest.py <id1> <id2> <id3> --max 200

    # 加暖身(更安全但慢 1-2 分钟)
    python3 comments-harvest.py <aweme_id> --warmup

    # 激进模式(快但有风控风险,确认账号稳时用)
    python3 comments-harvest.py <aweme_id> --max 500 --aggressive

    # URL 形式
    python3 comments-harvest.py --url https://www.douyin.com/video/7650771029597359394

依赖:agent-browser skill 已就绪;keepalive.py state 已 save
"""
import argparse
import csv
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

# 路径由 paths.py 统一管理(默认 $SKILL/data/, 可用 DOUYIN_DATA_DIR 环境变量覆盖)
from paths import COOKIE_FILE, STATE_FILE, DATA_DIR, EXPORTS_DIR, TMP_DIR, SKILL_DIR, report as report_paths

try:
    from downloader import download_for_aweme
    HAS_DOWNLOADER = True
except ImportError:
    HAS_DOWNLOADER = False


# =============================================================================
# JS 模板:两种 harvest 模式
# =============================================================================

# 人类模式(默认):scrollBy + 随机 sleep + 长停留概率
# ★ 关键:拆成 incremental step,每次 eval 跑 1 round(~3-5s),由 Python 循环调用
# 避免单次 eval 超 30s 触发 ab daemon busy
HARVEST_JS_HUMAN = r"""
(() => {
  // 初始化/恢复状态
  if (!window.__hc) {
    const scrollEl = document.querySelector('.parent-route-container.route-scroll-container');
    if (!scrollEl) return JSON.stringify({error: 'no scroll container'});
    window.__hc = {
      scrollEl: scrollEl,
      seen: new Set(),
      collected: [],
      chunkIdx: 0,
      round: 0,
      totalAdded: 0,
      lastAdded: 0,
      stalledRounds: 0,
    };
    return JSON.stringify({init: true, msg: 'ready'});
  }
  // 单 round:scrollBy + sleep + collect
  const state = window.__hc;
  const sleep = (ms) => new Promise(r => setTimeout(r, ms));
  const rand = (min, max) => min + Math.random() * (max - min);

  return (async () => {
    const s = state.scrollEl;
    const step = rand(200, 500);
    s.scrollBy(0, step);
    let wait = rand(1500, 5000);
    if (Math.random() < 0.10) wait += rand(2000, 6000);
    await sleep(wait);

    const items = s.querySelectorAll('[data-e2e="comment-item"]');
    let added = 0;
    for (const item of items) {
      const key = item.innerText.slice(0, 250);
      if (state.seen.has(key)) continue;
      state.seen.add(key);
      const ls = item.innerText.split('\n').map(s => s.trim()).filter(Boolean);
      if (ls.length < 2) continue;
      const user = ls[0] || '匿名';
      let timeStr = '';
      for (const l of ls) {
        if (/\d+(天|小时|分|秒)前|刚刚|周前|月前|年前/.test(l) && l.length < 30) timeStr = l;
      }
      let text = '', like = 0;
      for (let i = 1; i < ls.length; i++) {
        const l = ls[i];
        if (l === '...' || l === '回复' || l === '展开' || l === '收起' ||
            l === '置顶' || l === '作者' || l === '热' || l === '分享' || l === '举报') continue;
        if (timeStr && l === timeStr) continue;
        if (/^\d+(\.\d+)?$/.test(l) && l.length < 8) { like = parseFloat(l); continue; }
        if (l === user) continue;
        if (/^展开\d+条回复$/.test(l)) continue;
        if (!text && l.length >= 2) text = l;
      }
      if (text) {
        state.collected.push({user, text, digg_count: like, time: timeStr});
        state.totalAdded++;
        added++;
        // 每 20 条写一次 localStorage
        if (state.collected.length >= 20) {
          localStorage.setItem('__hc_chunk_' + state.chunkIdx, JSON.stringify(state.collected));
          state.chunkIdx++;
          state.collected = [];
        }
      }
    }
    state.round++;
    state.lastAdded = added;
    if (added < 2) state.stalledRounds++; else state.stalledRounds = 0;
    return JSON.stringify({round: state.round, added, total: state.totalAdded, stalled: state.stalledRounds});
  })();
})()
"""

# 激进模式(原版):scrollTop = scrollHeight, 一次拿一批
HARVEST_JS_AGGRESSIVE = r"""
(async () => {
  const scrollEl = document.querySelector('.parent-route-container.route-scroll-container');
  if (!scrollEl) return JSON.stringify({error: 'no scroll container'});

  const sleep = (ms) => new Promise(r => setTimeout(r, ms));
  const seen = new Set();
  let collected = [];
  let chunkIdx = parseInt(localStorage.getItem('__hc_chunk') || '0');

  const parseItem = (item) => {
    const ls = item.innerText.split('\n').map(s => s.trim()).filter(Boolean);
    if (ls.length < 2) return null;
    const user = ls[0] || '匿名';
    let timeStr = '';
    for (const l of ls) {
      if (/\d+(天|小时|分|秒)前|刚刚|周前|月前|年前/.test(l) && l.length < 30) timeStr = l;
    }
    let text = '', like = 0;
    for (let i = 1; i < ls.length; i++) {
      const l = ls[i];
      if (l === '...' || l === '回复' || l === '展开' || l === '收起' ||
          l === '置顶' || l === '作者' || l === '热' || l === '分享' || l === '举报') continue;
      if (timeStr && l === timeStr) continue;
      if (/^\d+(\.\d+)?$/.test(l) && l.length < 8) { like = parseFloat(l); continue; }
      if (l === user) continue;
      if (/^展开\d+条回复$/.test(l)) continue;
      if (!text && l.length >= 2) text = l;
    }
    return { user, text, digg_count: like, time: timeStr };
  };

  const flush = () => {
    if (collected.length === 0) return;
    localStorage.setItem('__hc_chunk_' + chunkIdx, JSON.stringify(collected));
    chunkIdx++;
    localStorage.setItem('__hc_chunk', String(chunkIdx));
    collected = [];
  };

  for (let round = 0; round < 25; round++) {
    scrollEl.scrollTop = scrollEl.scrollHeight;
    await sleep(900);
    const items = document.querySelectorAll('[data-e2e="comment-item"]');
    let added = 0;
    for (const item of items) {
      const key = item.innerText.slice(0, 250);
      if (seen.has(key)) continue;
      seen.add(key);
      const parsed = parseItem(item);
      if (parsed && parsed.text) {
        collected.push(parsed);
        added++;
        if (collected.length >= 30) flush();
      }
    }
    if (round > 5 && added === 0) {
      scrollEl.scrollTop += 200;
      await sleep(800);
      if (document.querySelectorAll('[data-e2e="comment-item"]').length === items.length) break;
    }
  }
  flush();
  return JSON.stringify({mode: 'aggressive', chunks: chunkIdx, total: seen.size});
})()
"""

# 单 chunk 读取
READ_ONE_JS = r"""
(() => {
  const idx = window.__read_idx || 0;
  const total = parseInt(localStorage.getItem('__hc_chunk') || '0');
  if (idx >= total) return JSON.stringify({done: true, idx, total});
  const key = '__hc_chunk_' + idx;
  const raw = localStorage.getItem(key);
  window.__read_idx = idx + 1;
  if (!raw) return JSON.stringify({idx, total, hasMore: true, data: null, note: 'chunk missing'});
  return JSON.stringify({idx, total, hasMore: idx + 1 < total, data: JSON.parse(raw)});
})()
"""

# 关闭登录弹窗
DISMISS_PANEL_JS = """
(() => {
  ['#login-full-panel-1pukt12088zk0', '#douyin_login_comp_flat_panel'].forEach(sel => {
    const p = document.querySelector(sel);
    if (p) { let cur = p; for (let i=0; i<5; i++) { if (!cur.parentElement) break; cur = cur.parentElement; } cur.remove(); }
  });
  document.querySelectorAll('[class*="mask"], [class*="Mask"]').forEach(e => e.remove());
  return 'dismissed';
})()
"""

# 暖身:刷推荐流 + 看一两个视频再回来(让进入目标视频的路径看起来"自然")
WARMUP_JS = r"""
(async () => {
  const sleep = (ms) => new Promise(r => setTimeout(r, ms));
  const log = [];
  // 1) 先在 douyin.com 推荐页滚一会儿
  const feedLinks = Array.from(document.querySelectorAll('a[href*="/video/"]'));
  log.push(`feed links: ${feedLinks.length}`);
  if (feedLinks.length === 0) return JSON.stringify({warmup: 'no feed', log});

  // 2) 滚 feed 5-10s
  window.scrollBy(0, 800);
  await sleep(rand(2500, 5000));
  window.scrollBy(0, 800);
  await sleep(rand(2000, 4000));

  // 3) 点开一个非目标视频,看 3-8s,返回
  //    排除当前视频 (URL 含当前 aweme_id)
  const currentUrl = location.href;
  const candidates = feedLinks.filter(a => !a.href.includes(currentAwemeId));
  if (candidates.length > 0) {
    const pick = candidates[Math.floor(Math.random() * Math.min(3, candidates.length))];
    pick.click();
    await sleep(rand(3000, 8000));
    log.push(`visited: ${pick.href.slice(0, 60)}`);
    history.back();
    await sleep(rand(2000, 4000));
  }

  // 4) 再滚一下,模拟"看完又刷了一会儿"
  window.scrollBy(0, 600);
  await sleep(rand(2000, 3500));
  return JSON.stringify({warmup: 'ok', log});

  function rand(min, max) { return min + Math.random() * (max - min); }
})()
"""


# =============================================================================
# Python 工具函数
# =============================================================================

def err(msg):
    print(f"❌ {msg}", file=sys.stderr)


def ok(msg):
    print(f"✅ {msg}")


def human_sleep(base_sec: float, jitter: float = 0.3):
    """人类节奏 sleep:base * uniform(1-jitter, 1+jitter)
    默认 jitter=0.3, 即 sleep 范围 0.7x ~ 1.3x base
    例:human_sleep(25) → 17.5 ~ 32.5 秒
    """
    actual = base_sec * random.uniform(1 - jitter, 1 + jitter)
    time.sleep(actual)


def run_ab(args, timeout=30):
    """subprocess wrapper for agent-browser"""
    return subprocess.run(
        ["agent-browser"] + args,
        capture_output=True, text=True, timeout=timeout,
    )


def ab_eval(js: str, timeout: int = 30):
    """通过临时文件执行 ab eval(避免 shell 转义)"""
    js_file = str(TMP_DIR / "_ab_eval_tmp.js")
    Path(js_file).write_text(js)
    return subprocess.run(
        f"agent-browser eval \"$(cat {js_file})\"",
        shell=True, capture_output=True, text=True, timeout=timeout,
    )


def open_video(aweme_id: str) -> bool:
    """打开视频页,检查登录态,关闭弹窗。返回是否成功(非 captcha 状态)"""
    url = f"https://www.douyin.com/video/{aweme_id}"
    r = run_ab(["--state", STATE_FILE, "open", url], timeout=30)
    if r.returncode != 0:
        err(f"agent-browser open 失败: {r.stderr[:200]}")
        return False
    time.sleep(5)
    # 检查 title
    t = run_ab(["eval", "document.title"], timeout=10)
    title = t.stdout.strip().strip('"').strip("'")
    if "验证码中间页" in title:
        err("页面是验证码中间页 - 风控触发,等 30s 再试或重跑 keepalive.py state save")
        return False
    if title.startswith("抖音-") or title == "":
        err(f"页面 title 异常: '{title[:50]}' - state 没注入,跑 keepalive.py state load/save")
        return False
    # 额外 captcha iframe 检查
    c = run_ab(["eval",
        "Array.from(document.querySelectorAll('iframe[id*=\"captcha\"]'))"
        ".filter(f => f.offsetWidth>100 && f.offsetHeight>100).length"],
        timeout=10)
    if c.stdout.strip().strip('"').strip("'") != "0":
        err("页面有可见 captcha iframe - 风控触发,等 30s 再试")
        return False
    ok(f"页面打开成功: {title[:60]}")
    # 关闭登录弹窗
    run_ab(["eval", DISMISS_PANEL_JS], timeout=10)
    return True


def do_warmup(aweme_id: str):
    """暖身:刷 5-15s 推荐流,看一两个视频再回来"""
    print("  → 暖身中(刷 feed + 看一两个视频)...")
    # 注入 aweme_id 到 warmup js
    js = WARMUP_JS.replace("currentAwemeId", f"'{aweme_id}'")
    r = ab_eval(js, timeout=60)
    if r.returncode != 0:
        err(f"  warmup 失败(非致命): {r.stderr[:100]}")
    else:
        try:
            result = json.loads(json.loads(r.stdout.strip() or '{}'))
            print(f"  → warmup: {result.get('warmup', '?')}, log: {result.get('log', [])}")
        except (json.JSONDecodeError, ValueError):
            print(f"  → warmup 完成 (raw: {r.stdout[:80]})")


def run_harvest(aweme_id: str, max_count: int, mode: str = "human") -> list:
    """执行虚拟滚动 harvest,返回所有评论列表"""
    # 清 localStorage + window 全局状态
    run_ab(["eval",
        "localStorage.removeItem('__hc_chunk');"
        "for(let i=0;i<100;i++) localStorage.removeItem('__hc_chunk_'+i);"
        "delete window.__hc;"
        "window.__read_idx=0;'cleared'"], timeout=10)

    if mode == "aggressive":
        # 激进模式:单次长 eval(scrollTop=jump)
        js = HARVEST_JS_AGGRESSIVE
        js_file = str(TMP_DIR / "_harvest_oneshot.js")
        Path(js_file).write_text(js)
        r = subprocess.run(
            f"agent-browser eval \"$(cat {js_file})\"",
            shell=True, capture_output=True, text=True, timeout=120,
        )
        if r.returncode != 0:
            err(f"harvest eval 失败: {r.stderr[:200]}")
            return []
        try:
            meta = json.loads(json.loads(r.stdout.strip()))
        except (json.JSONDecodeError, ValueError) as e:
            err(f"harvest meta 解析失败: {e}, stdout={r.stdout[:200]}")
            return []
        total_chunks = meta.get("chunks", 0)
        total_seen = meta.get("total", 0)
        print(f"  → harvest 完成(aggressive): {total_seen} 条,分 {total_chunks} chunk")
    else:
        # 人类模式:incremental,每次 eval 跑 1 round(避免 ab daemon busy)
        js = HARVEST_JS_HUMAN
        js_file = str(TMP_DIR / "_harvest_step.js")
        Path(js_file).write_text(js)
        # 初始化(第一次 eval 走初始化分支)
        r = subprocess.run(
            f"agent-browser eval \"$(cat {js_file})\"",
            shell=True, capture_output=True, text=True, timeout=15,
        )
        if r.returncode != 0:
            err(f"harvest 初始化失败: {r.stderr[:200]}")
            return []
        # 循环 15 round
        max_rounds = 15
        stalled = 0
        total_added = 0
        for rnd in range(max_rounds):
            r = subprocess.run(
                f"agent-browser eval \"$(cat {js_file})\"",
                shell=True, capture_output=True, text=True, timeout=20,
            )
            if r.returncode != 0:
                err(f"  round {rnd+1} eval 失败: {r.stderr[:100]}")
                # 重试 1 次
                time.sleep(2)
                r = subprocess.run(
                    f"agent-browser eval \"$(cat {js_file})\"",
                    shell=True, capture_output=True, text=True, timeout=20,
                )
                if r.returncode != 0:
                    err(f"  round {rnd+1} 重试也失败,跳过")
                    continue
            try:
                step = json.loads(json.loads(r.stdout.strip()))
            except (json.JSONDecodeError, ValueError):
                continue
            if 'added' not in step:
                continue
            total_added += step['added']
            stalled = step.get('stalled', 0)
            # round 8 之后,stalled >= 2 就停
            if rnd >= 8 and stalled >= 2:
                print(f"  → round {step['round']}: +{step['added']} (累计 {total_added}, stalled {stalled} 轮,提前停)")
                break
            if rnd % 3 == 0 or step['added'] > 0:
                print(f"  → round {step['round']}: +{step['added']} (累计 {total_added})")
        # flush 剩余 collected
        flush_js = r"""
        (() => {
          if (!window.__hc) return JSON.stringify({done: true});
          if (window.__hc.collected.length > 0) {
            localStorage.setItem('__hc_chunk_' + window.__hc.chunkIdx, JSON.stringify(window.__hc.collected));
            window.__hc.chunkIdx++;
            window.__hc.collected = [];
          }
          localStorage.setItem('__hc_chunk', String(window.__hc.chunkIdx));
          return JSON.stringify({done: true, total: window.__hc.totalAdded, chunks: window.__hc.chunkIdx});
        })()
        """
        Path(str(TMP_DIR / "_harvest_flush.js")).write_text(flush_js)
        r = subprocess.run(
            f"agent-browser eval \"$(cat {TMP_DIR}/_harvest_flush.js)\"",
            shell=True, capture_output=True, text=True, timeout=10,
        )
        try:
            meta = json.loads(json.loads(r.stdout.strip()))
        except (json.JSONDecodeError, ValueError):
            meta = {"total": total_added, "chunks": 0}
        total_chunks = meta.get("chunks", 0)
        total_seen = meta.get("total", total_added)
        print(f"  → harvest 完成(human): {total_seen} 条,分 {total_chunks} chunk")

    # 逐个 chunk 读取
    collected = []
    for i in range(total_chunks + 5):
        if len(collected) >= max_count:
            break
        r = run_ab(["eval", READ_ONE_JS], timeout=10)
        try:
            obj = json.loads(json.loads(r.stdout.strip()))
        except (json.JSONDecodeError, ValueError):
            break
        if obj.get("done"):
            break
        chunk_data = obj.get("data") or []
        for c in chunk_data:
            if len(collected) >= max_count:
                break
            collected.append(c)
    return collected


def parse_user_location(time_str: str):
    """拆 '1天前·重庆' → ('1天前', '重庆')"""
    if not time_str:
        return "", ""
    m = re.match(r'^(.+?)(?:·(.+))?$', time_str)
    if m:
        return (m.group(1) or "").strip(), (m.group(2) or "").strip()
    return time_str, ""


def get_video_meta(aweme_id: str) -> dict:
    """从 douyin API 拿视频标题/作者/点赞(走 HTTP,无需 ab)"""
    import importlib.util
    fetch_path = SKILL_DIR / "douyin-fetch.py"
    if not fetch_path.exists():
        return {"title": "?", "author": "?", "likes": 0, "comments_total": 0}
    try:
        spec = importlib.util.spec_from_file_location("douyin_fetch", fetch_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        cookie = mod.load_cookie()
        resp = mod.http_get(
            "/aweme/v1/web/aweme/detail/",
            {"aweme_id": aweme_id}, cookie,
        )
        v = (resp or {}).get("aweme_detail") or {}
        if not v:
            return {"title": "?", "author": "?", "likes": 0, "comments_total": 0}
        a = v.get("author") or {}
        s = v.get("statistics") or {}
        return {
            "title": v.get("desc", "?"),
            "author": "@" + a.get("nickname", "?"),
            "likes": s.get("digg_count", 0),
            "comments_total": s.get("comment_count", 0),
            "publish": v.get("create_time"),
            "url": f"https://www.douyin.com/video/{aweme_id}",
        }
    except Exception as e:
        err(f"拿视频元信息失败: {e}")
        return {"title": "?", "author": "?", "likes": 0, "comments_total": 0}


def save_results(aweme_id: str, meta: dict, comments: list, output_dir: Path, mode: str,
                 download_info: Optional[dict] = None):
    """落盘 JSON + CSV

    download_info: 来自 downloader.download_for_aweme() 的结果,会嵌入:
      - JSON: 顶层 video.download 字段 + 顶层 download 字段
      - CSV:  每行加 video_download 列(同视频所有行一致)
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    download_path = (download_info or {}).get("path") or ""
    records = []
    for c in comments:
        rel_time, location = parse_user_location(c.get("time", ""))
        records.append({
            "video_id": aweme_id,
            "video_title": meta.get("title", "?"),
            "video_author": meta.get("author", "?"),
            "video_likes": meta.get("likes", 0),
            "user": c.get("user", ""),
            "text": c.get("text", ""),
            "digg_count": c.get("digg_count", 0),
            "relative_time": rel_time,
            "location": location,
            "video_download": download_path,
            "scraped_at": time.strftime("%Y-%m-%d"),
        })
    json_path = output_dir / f"comments_{aweme_id}.json"
    json_obj = {
        "video": meta,
        "scraped_at": time.strftime("%Y-%m-%d"),
        "source": "douyin (https://www.douyin.com)",
        "scraper": f"comments-harvest.py (agent-browser virtual scroll harvest, mode={mode})",
        "comment_count": len(records),
        "comments": records,
    }
    if download_info is not None:
        json_obj["download"] = download_info
        # 同步到 video 块,便于 aggregate.py 直接读
        if isinstance(json_obj.get("video"), dict):
            json_obj["video"]["download"] = {
                "path": download_info.get("path"),
                "quality": download_info.get("quality"),
                "size": download_info.get("downloaded_bytes"),
            }
    json_path.write_text(json.dumps(json_obj, ensure_ascii=False, indent=2), encoding="utf-8")
    csv_path = output_dir / f"comments_{aweme_id}.csv"
    base_fields = [
        "video_id", "video_title", "video_author", "video_likes",
        "user", "text", "digg_count", "relative_time", "location",
        "video_download", "scraped_at",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=base_fields)
        w.writeheader()
        for r in records:
            w.writerow({k: r.get(k, "") for k in base_fields})
    ok(f"已写入: {json_path.name} ({json_path.stat().st_size:,} bytes) + {csv_path.name} ({csv_path.stat().st_size:,} bytes)")
    return json_path, csv_path


def harvest_one(aweme_id: str, max_count: int, output_dir: Path,
                mode: str = "human", warmup: bool = False,
                download: bool = False, download_dir: Optional[Path] = None,
                quality: str = "play", cookie: str = "") -> bool:
    """单视频完整流程"""
    print(f"\n=== {aweme_id} (mode={mode}, warmup={warmup}, max={max_count}) ===")
    if not open_video(aweme_id):
        return False
    if warmup:
        do_warmup(aweme_id)
        # 暖身后重新打开目标视频（因为 warmup 可能 navigate 走了）
        if not open_video(aweme_id):
            return False
    comments = run_harvest(aweme_id, max_count, mode=mode)
    if not comments:
        err("harvest 没拿到任何评论")
        return False
    print(f"  → 共 {len(comments)} 条评论")
    meta = get_video_meta(aweme_id)
    print(f"  → 视频: {meta.get('title', '?')[:50]}... by {meta.get('author', '?')}")
    # 下载视频（如果指定）
    download_info = None
    if download:
        if not HAS_DOWNLOADER:
            err("--download 需要 downloader.py 模块（检查 skill 目录完整性）")
        elif not cookie:
            err("--download 需要 cookie 但未提供（cookie 应从路径 / 加载）")
        else:
            dest = download_dir if download_dir else (output_dir / "downloads")
            print(f"\n  → 下载视频 (quality={quality}) → {dest}")
            download_info = download_for_aweme(
                aweme_id=aweme_id, dest_dir=dest, cookie=cookie,
                title_hint=meta.get("title", ""), quality=quality,
            )
            if download_info.get("ok"):
                ok(f"  → 本地路径: {download_info['path']}")
            else:
                err(f"  → 下载失败: {download_info.get('error', '未知错误')}")
    save_results(aweme_id, meta, comments, output_dir, mode=mode,
                 download_info=download_info)
    return True


def main():
    ap = argparse.ArgumentParser(
        description="douyin 评论深度抓取(虚拟滚动 harvest, 人类模式默认)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("aweme_ids", nargs="*", help="一个或多个 aweme_id(纯数字)")
    ap.add_argument("--url", help="视频 URL(单视频模式,等同于给一个 aweme_id)")
    ap.add_argument("--max", type=int, default=200,
                    help="单视频最大抓取数(默认 200, 人类模式保守值; --aggressive 可调高)")
    ap.add_argument("--output", "-o", default=str(EXPORTS_DIR),
                    help=f"输出目录(默认 {EXPORTS_DIR})")
    ap.add_argument("--aggressive", action="store_true",
                    help="激进模式:scrollTop=jump + 25 round + 抓满 max(快但有风控风险)")
    ap.add_argument("--warmup", action="store_true",
                    help="暖身:抓前先刷 5-15s 推荐流 + 看一两个视频(更安全但慢 1-2 分钟)")
    ap.add_argument("--interval", type=float, default=25.0,
                    help="视频间 base sleep 秒数(人类模式默认 25, ±30%% jitter → 实际 17-32s)")
    ap.add_argument("--no-jitter", action="store_true",
                    help="禁用 video 间的随机 jitter（测试用）")
    ap.add_argument("--download", action="store_true",
                    help="下载视频到本地（1080p 无水印），路径写入每个 comments JSON/CSV")
    ap.add_argument("--download-dir",
                    help="视频下载目录（默认: <--output>/downloads/）")
    ap.add_argument("--quality", choices=["play", "download"], default="play",
                    help="下载画质: play=1080p 无水印（默认）/ download=720p 带水印")
    args = ap.parse_args()

    # 解析 aweme_id
    ids = list(args.aweme_ids)
    if args.url:
        m = re.search(r"/video/(\d+)", args.url)
        if not m:
            err(f"无法从 URL 提取 aweme_id: {args.url}")
            sys.exit(3)
        ids.append(m.group(1))

    if not ids:
        err("需要 aweme_id 或 --url")
        ap.print_help()
        sys.exit(2)

    # 预检
    if not Path(STATE_FILE).exists():
        err(f"state 文件不存在: {STATE_FILE}")
        err("→ 先跑 keepalive.py setup → inject → check → state save")
        sys.exit(1)

    mode = "aggressive" if args.aggressive else "human"
    output_dir = Path(args.output)
    download_dir = Path(args.download_dir) if args.download_dir else None
    cookie = ""
    if args.download:
        # 读 cookie 为下载需要（与 fetch.py 同样的 Netscape 解析逻辑）
        cookie_path = Path(COOKIE_FILE)
        if cookie_path.exists():
            raw = cookie_path.read_text()
            parts = []
            for line in raw.split("\n"):
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("//"):
                    continue
                if "\t" in line:
                    cols = line.split("\t")
                    if len(cols) >= 7:
                        parts.append(f"{cols[5]}={cols[6]}")
                    else:
                        parts.append(f"{cols[-2]}={cols[-1]}")
                elif "=" in line:
                    parts.append(line)
            cookie = "; ".join(parts)
        if not cookie:
            err("--download 需要 cookie，先跑 keepalive.py setup → inject")
            sys.exit(2)
    success = 0
    for i, aweme_id in enumerate(ids):
        if harvest_one(aweme_id, args.max, output_dir,
                       mode=mode, warmup=args.warmup,
                       download=args.download, download_dir=download_dir,
                       quality=args.quality, cookie=cookie):
            success += 1
        # 视频间 jitter (跳过最后一个)
        if i < len(ids) - 1 and not args.no_jitter:
            wait = args.interval * (1.0 if args.no_jitter else random.uniform(0.7, 1.3))
            print(f"  → 视频间 sleep {wait:.1f}s (base={args.interval}s × jitter)")
            time.sleep(wait)

    print(f"\n=== 完成 {success}/{len(ids)} (mode={mode}) ===")
    if success < len(ids):
        sys.exit(1)


if __name__ == "__main__":
    main()
