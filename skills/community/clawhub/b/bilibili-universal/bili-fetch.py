#!/usr/bin/env python3
"""
bili-fetch.py — bilibili 抓取 skill 核心脚本

子命令:
  1. paths                              打印路径配置
  2. search   <keyword>                 主题搜索 (视频搜索接口, 按 order 排序)
  3. user-search <keyword>             用户名 → mid 解析
  4. user     <mid>  [--videos N]      UP 主主页 + 视频列表 (走 SPA)
  5. video    <bvid>  [--comments N]   单视频详情 + 热门评论
  6. comments <bvid|aid> [--ps N]      单独抓评论 (热评/最新)

数据路径:
  - HTTP API 调用走 agent-browser eval (内部 fetch, 复用 buvid cookie + wbi 签名环境)
  - SPA 渲染走 agent-browser open + wait selector (UP 主空间页面)
  - 不强制登录, 已登录 cookie 可注入到 agent-browser 拿到更完整的数据 (1080P, 关注状态)

cookie 路径由 paths.py 统一管理 (默认 $SKILL/data/, 可用 BI_DATA_DIR 覆盖)
"""

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

# 路径统一管理
from paths import report as report_paths

# B 站 API 域名
API_BASE = "https://api.bilibili.com"
WEB_BASE = "https://www.bilibili.com"
SPACE_BASE = "https://space.bilibili.com"
SEARCH_BASE = "https://search.bilibili.com"

# 常见 tid → 分区名 (不全, 未列入的会显示 tid N)
TID_NAMES = {
    21: "日常", 22: "鬼畜", 24: "MMD/3D", 25: "短片/手书/配音",
    27: "综合", 28: "原创音乐", 29: "音乐选集", 30: "VOCALOID",
    31: "翻唱", 32: "演奏", 33: "宅舞", 36: "科技", 37: "人文历史",
    39: "影视", 41: "娱乐", 47: "鬼畜", 48: "鬼畜调教",
    75: "动物", 76: "美食", 80: "运动", 86: "特摄",
    95: "宅物", 119: "资讯", 122: "资讯", 124: "社会",
    126: "生活", 127: "搞笑", 128: "明星", 129: "时尚",
    130: "美妆", 131: "游戏", 132: "知识", 133: "影视杂谈",
    134: "影视剪辑", 135: "影视解说", 136: "动画", 137: "漫画",
    138: "搞笑", 141: "剧集", 152: "国创", 155: "资讯",
    156: "教育", 157: "健康", 158: "生活记录", 159: "亲子",
    160: "汽车", 161: "运动竞技", 162: "户外", 163: "健身",
    164: "三农", 165: "音乐", 166: "二次元", 168: "国创相关",
    171: "游戏资讯", 172: "游戏攻略", 173: "单机游戏", 174: "电子竞技",
    175: "手游", 176: "网络游戏", 177: "综艺", 178: "娱乐杂谈",
    179: "娱乐解说", 180: "脱口秀", 181: "国产剧", 182: "海外剧",
}


# ============== 工具函数 ==============

def err(msg):
    print(f"❌ {msg}", file=sys.stderr)


def ok(msg):
    print(f"✅ {msg}")


def info(msg):
    print(f"  {msg}")


def run(cmd, timeout=30, check=False):
    """跑 agent-browser 命令"""
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode != 0:
        print(f"  stdout: {r.stdout[:300]}")
        print(f"  stderr: {r.stderr[:300]}")
    return r


def ab_open(url, timeout=30):
    """open URL"""
    return run(['agent-browser', 'open', url], timeout=timeout)


def ab_eval(js, timeout=20):
    """evaluate JS, return parsed Python object (dict / list / str / int / None)

    agent-browser eval 永远把返回值序列化成 JSON 字符串输出,
    而且是 双层 JSON 编码:
      1) JS 端 JSON.stringify(obj) -> '{"a":1}'
      2) agent-browser 把这个字符串当返回值再 dump 一次 -> '"{\\"a\\":1}"'
    所以 Python 端要 json.loads 两次才能拿到 dict。
    约定: JS 端必须用 JSON.stringify(...) 包裹返回值,保证序列化。
    """
    r = run(['agent-browser', 'eval', js], timeout=timeout)
    out = r.stdout.strip()
    if not out:
        return None
    try:
        outer = json.loads(out)
    except json.JSONDecodeError:
        return out
    if isinstance(outer, str):
        try:
            return json.loads(outer)
        except json.JSONDecodeError:
            return outer
    return outer


def ab_screenshot(path, full=False, timeout=30):
    """截图"""
    cmd = ['agent-browser', 'screenshot', str(path)]
    if full:
        cmd.insert(2, '--full')
    return run(cmd, timeout=timeout)


def check_block(data_or_text):
    """检查返回结果是否被风控/拦截,返回错误码字符串或 None"""
    if isinstance(data_or_text, dict):
        code = data_or_text.get('code')
        msg = (data_or_text.get('message') or data_or_text.get('msg') or '').lower()
    else:
        s = str(data_or_text)
        code = None
        msg = s.lower()

    # B 站风控常见 code
    if code in (-352, -403, -799):
        return 'wbi_or_risk_control'
    if code == -101:
        return 'not_login'  # 需要登录
    if code == -404:
        return 'not_found'
    if code == 25010 or '风控' in msg or '验证码' in msg or 'captcha' in msg:
        return 'captcha'
    if '访问权限不足' in msg:
        return 'permission_denied'
    return None


def bvid_to_aid(bvid):
    """BV 号 → aid (通过 web-interface/view 拿)"""
    js = f"""(async () => {{
      const r = await fetch('https://api.bilibili.com/x/web-interface/view?bvid={bvid}', {{credentials:'include'}});
      const j = await r.json();
      return JSON.stringify({{code: j.code, aid: j?.data?.aid, title: j?.data?.title, msg: j.message}});
    }})()"""
    res = ab_eval(js, timeout=15)
    if not res:
        return None
    return res.get('aid') if isinstance(res, dict) else None


# ============== 子命令 ==============

def cmd_paths(args):
    """打印路径配置"""
    report_paths()
    return 0


def cmd_search(args):
    """主题搜索 — 视频搜索 API"""
    keyword = args.keyword
    info(f"搜索: {keyword!r}  order={args.order}  pages={args.pages}")

    all_results = []
    for page in range(1, args.pages + 1):
        js = f"""(async () => {{
          const kw = {json.dumps(keyword)};
          const url = 'https://api.bilibili.com/x/web-interface/search/type'
            + '?search_type=video'
            + '&keyword=' + encodeURIComponent(kw)
            + '&order={args.order}'
            + '&page={page}'
            + '&page_size=' + {args.ps};
          const r = await fetch(url, {{credentials:'include'}});
          const j = await r.json();
          const list = j?.data?.result || [];
          const items = list.map(v => ({{
            bvid: v.bvid, aid: v.aid, title: v.title.replace(/<[^>]*>/g,''),
            author: v.author, mid: v.mid,
            duration: v.duration, play: v.play, danmaku: v.danmaku,
            review: v.review, pubdate: v.pubdate, tag: v.tag,
            url: 'https://www.bilibili.com/video/' + v.bvid
          }}));
          return JSON.stringify({{code: j.code, msg: j.message, page: {page},
                                   total: j?.data?.numResults, pages: j?.data?.numPages,
                                   items}});
        }})()"""
        res = ab_eval(js, timeout=20)
        if not res:
            err(f"page {page} 拿不到结果")
            continue
        if block := check_block(res):
            err(f"page {page} 被拦: {block}  ({res.get('msg', '')})")
            break
        all_results.extend(res.get('items', []))
        info(f"page {page}: +{len(res.get('items', []))} 条 (累计 {len(all_results)})")
        time.sleep(0.5)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            json.dump({'keyword': keyword, 'order': args.order, 'count': len(all_results),
                       'items': all_results}, f, ensure_ascii=False, indent=2)
        ok(f"已保存到 {out}")
    else:
        print(f"\n🔍 「{keyword}」 (order={args.order})  命中 {len(all_results)} 条\n")
        for i, v in enumerate(all_results[:args.show], 1):
            print(f"  {i:>3}. [{v['duration']:>6}] {v['title'][:50]}")
            print(f"       {v['author']} · 👁 {v['play']} · 💬 {v['review']} · {v['url']}")
    return 0


def cmd_user_search(args):
    """用户名 → mid 解析 (走搜索接口, 不进 SPA)"""
    keyword = args.keyword
    info(f"搜 UP 主: {keyword!r}")

    js = f"""(async () => {{
      const kw = {json.dumps(keyword)};
      const url = 'https://api.bilibili.com/x/web-interface/search/type'
        + '?search_type=bili_user'
        + '&keyword=' + encodeURIComponent(kw)
        + '&page=1&page_size=20';
      const r = await fetch(url, {{credentials:'include'}});
      const j = await r.json();
      const list = j?.data?.result || [];
      const items = list.map(u => ({{
        mid: u.mid, uname: u.uname, usign: u.usign,
        fans: u.fans, videos: u.videos, level: u.level,
        space_url: 'https://space.bilibili.com/' + u.mid
      }}));
      return JSON.stringify({{code: j.code, msg: j.message, count: list.length, items}});
    }})()"""
    res = ab_eval(js, timeout=15)
    if not res:
        err("拿不到结果")
        return 1
    if block := check_block(res):
        err(f"被拦: {block}  ({res.get('msg', '')})")
        return 1

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            json.dump({'keyword': keyword, 'items': res['items']}, f, ensure_ascii=False, indent=2)
        ok(f"已保存到 {out}")
    else:
        print(f"\n👤 「{keyword}」  候选 {res['count']} 个\n")
        for i, u in enumerate(res['items'][:args.show], 1):
            tag = " ← 名称精确匹配" if u['uname'] == keyword else ""
            print(f"  {i:>2}. mid={u['mid']}  {u['uname']}{tag}")
            print(f"       粉丝 {u['fans']} · 视频 {u['videos']} · Lv.{u['level']}")
            if u['usign']:
                print(f"       {u['usign'][:80]}")
            print(f"       {u['space_url']}")
    return 0


def cmd_user(args):
    """UP 主主页 — 走 SPA, 拿空间元数据 + 视频列表"""
    mid = str(args.mid)
    if mid.isdigit() and 'space.bilibili.com' not in mid:
        space_url = f"{SPACE_BASE}/{mid}/upload/video"
    else:
        # 兼容 https://space.bilibili.com/XXX/... 形式
        m = re.search(r'space\.bilibili\.com/(\d+)', mid)
        if not m:
            err(f"无法从 {mid} 提取 mid")
            return 1
        mid = m.group(1)
        space_url = f"{SPACE_BASE}/{mid}/upload/video"

    info(f"UP 主 mid={mid}  videos={args.videos}")
    info(f"打开 {space_url}")

    # SPA 加载策略
    # - auto (默认): 先 poll 2s 看是否已有 cards, 有就跳过 reload
    # - yes      : 强制 reload()  (老问题会让已渲染 session 变空)
    # - no       : 不 reload (全新 session 需配合足够等待)
    ab_open(space_url)
    if args.reload == 'yes':
        time.sleep(2)
        ab_eval("location.reload()")
    elif args.reload == 'auto':
        # 智能检测: 2s 内看到 cards 就跳过 reload, 否则才调
        for _ in range(4):
            time.sleep(0.5)
            n = ab_eval("document.querySelectorAll('.bili-video-card').length")
            if isinstance(n, int) and n > 0:
                info(f"已渲染 {n} 个视频卡片, 跳过 reload")
                break
        else:
            info("未检测到卡片, 强制 reload")
            ab_eval("location.reload()")
            # reload 后还要等渲染
            time.sleep(2)
    # args.reload == 'no': 什么都不做

    # 轮询等待 .bili-video-card 渲染 (SPA 经常 5-12s 才出)
    for _ in range(30):
        time.sleep(1)
        n = ab_eval("document.querySelectorAll('.bili-video-card').length")
        if isinstance(n, int) and n > 0:
            info(f"已渲染 {n} 个视频卡片")
            break
    else:
        info("⚠️ 等待 30s 仍未渲染, 继续尝试")

    # --scroll: 通过分页拿全量 (B 站 UP 主空间是带分页器, 不是滚动加载)
    # 实现要点: SPA 翻页会替换 .bili-video-card, 所以必须在 Python 层 跨页 累积 bvids
    paginated_bvids_titles = []  # [(bvid, title), ...] 跨页累积
    if getattr(args, 'scroll', False):
        info("开始翻页拿全量...")

        def _do_pagination_loop():
            max_pages = 100
            for page_idx in range(1, max_pages):
                # 收集当前页 bvids (在 SPA 替换 .bili-video-card 之前)
                page_js = """(() => {
                  const cards = Array.from(document.querySelectorAll('.bili-video-card'));
                  const list = cards.map(c => {
                    const a = c.querySelector('a[href*=\"/video/\"]');
                    const bvid = a?.href?.match(/BV\\w+/)?.[0];
                    const title = c.querySelector('.bili-video-card__title')?.textContent?.trim() || '';
                    return bvid ? [bvid, title] : null;
                  }).filter(Boolean);
                  const btns = Array.from(document.querySelectorAll('button.vui_pagenation--btn-side'));
                  const nextBtn = btns.find(b => (b.textContent||'').trim() === '下一页');
                  const disabled = !nextBtn || nextBtn.disabled || (nextBtn.className||'').includes('disabled');
                  return JSON.stringify({list, disabled});
                })()"""
                res = ab_eval(page_js)
                d = res if isinstance(res, dict) else {}
                plist = d.get('list', []) if isinstance(d, dict) else []
                next_disabled = d.get('disabled', True) if isinstance(d, dict) else True

                for bvid, title in plist:
                    if not any(b == bvid for b, _ in paginated_bvids_titles):
                        paginated_bvids_titles.append((bvid, title))

                cur_total = len(paginated_bvids_titles)
                info(f"页 {page_idx}: 抓 {len(plist)}, 累积 {cur_total}")

                if cur_total >= args.videos:
                    info(f"累积 {cur_total} 已达到 --videos={args.videos}")
                    return True
                if next_disabled:
                    info("下一页 disabled (末页)")
                    return True

                # 点下一页 (验证 active 变化)
                before_active = str(ab_eval("""(() => {
                  const active = document.querySelector('.vui_button--active, button.vui_button--active');
                  return active ? active.textContent.trim() : '';
                })()""") or '').strip()
                clicked = ab_eval("""(() => {
                  const btns = Array.from(document.querySelectorAll('button.vui_pagenation--btn-side'));
                  const next = btns.find(b => (b.textContent||'').trim() === '下一页');
                  if (next && !next.disabled) { next.click(); return true; }
                  return false;
                })()""")
                if not clicked:
                    info("点下一页失败")
                    return True
                for _ in range(15):
                    time.sleep(0.5)
                    now_active = str(ab_eval("""(() => {
                      const active = document.querySelector('.vui_button--active, button.vui_button--active');
                      return active ? active.textContent.trim() : '';
                    })()""") or '').strip()
                    if now_active != before_active:
                        break
                else:
                    info("警告: active 页码 未变 (SPA 未切换), 停止")
                    return True
                time.sleep(1)
            return True

        _do_pagination_loop()
        # 重试: fresh session 首次访问 SPA 偶尔不渲染, 主动 close --all + 重来一次
        if not paginated_bvids_titles:
            info("首次 抓 0, 可能是 fresh session 未能渲染, 主动 close --all + 重试")
            subprocess.run(['agent-browser', 'close', '--all'], capture_output=True, timeout=15)
            time.sleep(2)
            ab_open(space_url)
            time.sleep(8)
            # 再走主 reload + 长轮询
            if args.reload != 'no':
                if args.reload == 'yes':
                    ab_eval("location.reload()")
                for _ in range(30):
                    time.sleep(1)
                    n = ab_eval("document.querySelectorAll('.bili-video-card').length")
                    if isinstance(n, int) and n > 0:
                        info(f"重试渲染成功 {n} 个")
                        break
            _do_pagination_loop()

        info(f"--scroll 完成: 总 {len(paginated_bvids_titles)} 个不重复 BV")

    js = f"""(() => {{
      // 1) UP 主头部元数据
      const name = document.querySelector('.nickname, .h-name, .user-name, [class*=\"nickname\"]')?.textContent?.trim() || '';
      const sign = document.querySelector('.desc, .h-sign, [class*=\"sign\"], [class*=\"signature\"]')?.textContent?.trim() || '';
      const items = document.querySelectorAll('.nav-statistics__item');
      const followTxt = items[0]?.textContent?.trim() || '';
      const fansTxt = items[1]?.textContent?.trim() || '';

      // 2) 视频列表
      const cards = Array.from(document.querySelectorAll('.bili-video-card')).slice(0, {args.videos});
      const videos = cards.map(c => {{
        const a = c.querySelector('a[href*=\"/video/\"]');
        const bvid = a?.href?.match(/BV\\w+/)?. [0];
        const title = c.querySelector('.bili-video-card__title')?.textContent?.trim();
        const date = c.querySelector('.bili-video-card__subtitle span')?.textContent?.trim();
        const stats = Array.from(c.querySelectorAll('.bili-cover-card__stat span')).map(s => s.textContent.trim());
        return {{
          bvid, title, date,
          play: stats[0], danmaku: stats[1], duration: stats[2],
          url: 'https://www.bilibili.com/video/' + bvid
        }};
      }});

      return JSON.stringify({{
        mid: {mid}, name, sign, fans: fansTxt, follow: followTxt,
        space_url: 'https://space.bilibili.com/{mid}',
        videos_count: videos.length, videos
      }});
    }})()"""
    res = ab_eval(js, timeout=15)
    if not res:
        err("eval 没拿到数据 (SPA 可能没渲染, 试试 agent-browser close --all 后重跑)")
        return 1

    # --scroll: 把跨页累积的 bvid 合并到输出 (翻到的后面页只有 bvid+title, 详情字段会在 harvest 的 video 命令里补)
    if getattr(args, 'scroll', False) and paginated_bvids_titles:
        existing = {v['bvid']: v for v in res.get('videos', []) if v.get('bvid')}
        merged = []
        for bvid, title in paginated_bvids_titles[:args.videos]:
            if bvid in existing:
                merged.append(existing[bvid])
            else:
                # 占位: 只带 bvid + title, harvest 会补全其他字段
                merged.append({
                    'bvid': bvid, 'title': title, 'date': '', 'play': '', 'danmaku': '', 'duration': '',
                    'url': 'https://www.bilibili.com/video/' + bvid,
                })
        res['videos'] = merged
        res['videos_count'] = len(merged)
        info(f"合并后总 videos: {len(merged)}")

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
        ok(f"已保存到 {out}")
    else:
        print(f"\n👤 {res.get('name') or '(未抓到昵称)'}  mid={mid}")
        print(f"   签名: {res.get('sign') or '(空)'}")
        print(f"   粉丝/关注: {res.get('fans') or '?'} / {res.get('follow') or '?'}")
        print(f"   {res.get('space_url')}\n")
        print(f"   最近 {len(res['videos'])} 个视频:")
        for i, v in enumerate(res['videos'], 1):
            print(f"   {i:>3}. [{v['date']:>10}] [{v['duration']:>6}] {v['title'][:45]}")
            print(f"        👁 {v['play']}  💬弹幕 {v['danmaku']}")
    return 0


def cmd_video(args):
    """单视频详情 + 热门评论"""
    vid = args.video
    info(f"视频: {vid}")

    # 兼容 BV/av 号和 URL
    m = re.search(r'(BV\w+)', vid)
    if m:
        bvid = m.group(1)
    elif vid.lower().startswith('av'):
        aid = int(vid[2:])
        js = f"""(async () => {{
          const r = await fetch('https://api.bilibili.com/x/web-interface/view?aid={aid}', {{credentials:'include'}});
          const j = await r.json();
          return JSON.stringify({{bvid: j?.data?.bvid, code: j.code}});
        }})()"""
        r = ab_eval(js, timeout=15)
        if not r or not r.get('bvid'):
            err("aid 查不到对应 bvid")
            return 1
        bvid = r['bvid']
    else:
        err(f"无法识别 video 参数: {vid}")
        return 1

    # 详情
    detail_js = f"""(async () => {{
      const r = await fetch('https://api.bilibili.com/x/web-interface/view?bvid={bvid}', {{credentials:'include'}});
      const j = await r.json();
      const v = j?.data;
      if (!v) return JSON.stringify({{code: j.code, msg: j.message}});
      return JSON.stringify({{
        code: j.code, msg: j.message,
        bvid: v.bvid, aid: v.aid, title: v.title, desc: v.desc,
        duration: v.duration,
        duration_text: (() => {{
          const s = v.duration, h = Math.floor(s/3600), m = Math.floor((s%3600)/60), ss = s%60;
          return (h > 0 ? h + ':' : '') + String(m).padStart(2,'0') + ':' + String(ss).padStart(2,'0');
        }})(),
        pubdate: v.pubdate, ctime: v.ctime,
        pubdate_text: new Date(v.pubdate*1000).toISOString().slice(0,10),
        tname: v.tname, tid: v.tid,
        owner: v.owner,  // mid, name, face
        stat: v.stat,    // view, like, coin, favorite, share, reply, danmaku
        pages: (v.pages || []).map(p => p.part),
        url: 'https://www.bilibili.com/video/' + v.bvid
      }});
    }})()"""
    detail = ab_eval(detail_js, timeout=15)
    if not detail or detail.get('code') != 0:
        err(f"详情失败: {detail}")
        return 1
    if block := check_block(detail):
        err(f"被拦: {block}")
        return 1

    # 评论
    if args.comments > 0:
        aid = detail['aid']
        comments_js = f"""(async () => {{
          const r = await fetch('https://api.bilibili.com/x/v2/reply/main?oid={aid}&type=1&mode=3&next=0&ps={args.comments}', {{credentials:'include'}});
          const j = await r.json();
          const replies = (j?.data?.replies || []).map(rp => ({{
            rpid: rp.rpid, uname: rp.member?.uname, mid: rp.member?.mid,
            content: rp.content?.message, like: rp.like, ctime: rp.ctime,
            location: rp.reply_control?.location || ''
          }}));
          return JSON.stringify({{
            code: j.code, msg: j.message,
            count: j?.data?.cursor?.all_count || j?.data?.page?.count || 0,
            sample: replies
          }});
        }})()"""
        comments = ab_eval(comments_js, timeout=15)
        if comments and comments.get('code') == 0:
            detail['comments_count'] = comments.get('count', 0)
            detail['comments_sample'] = comments.get('sample', [])
        else:
            detail['comments_sample'] = []
            err(f"评论拉取失败: {comments}")

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(detail, f, ensure_ascii=False, indent=2)
        ok(f"已保存到 {out}")
    else:
        st = detail.get('stat', {})
        print(f"\n🎬 {detail['title']}")
        partition = detail.get('tname') or TID_NAMES.get(detail.get('tid', 0), f"tid {detail.get('tid', '?')}")
        print(f"   BV: {detail['bvid']}  AV: {detail['aid']}  分区: {partition}")
        print(f"   UP: {detail['owner']['name']} (mid={detail['owner']['mid']})")
        dur_text = detail['duration_text']
        print(f"   时长: {dur_text}  发布: {detail['pubdate_text']}")
        print(f"   简介: {detail['desc'][:200]}")
        print(f"   数据: 👁 {st.get('view')}  👍 {st.get('like')}  💰 {st.get('coin')}  ⭐ {st.get('favorite')}  💬 {st.get('reply')}  弹幕 {st.get('danmaku')}")
        if detail.get('comments_sample'):
            print(f"\n   💬 评论 (总数 {detail.get('comments_count', '?')}, 展示 {len(detail['comments_sample'])}):")
            for c in detail['comments_sample']:
                loc = f" [{c.get('location')}]" if c.get('location') else ''
                print(f"     • {c['uname']}{loc} (👍{c['like']}): {c['content'][:120]}")

    # 弹幕落盘 (走 bilibili_api 库, 不走 agent-browser)
    if args.danmaku_out:
        bvid = detail['bvid']
        info(f"抓弹幕: {bvid} → {args.danmaku_out}")
        dms = _fetch_danmaku_bvid(bvid)
        if dms is not None:
            outp = Path(args.danmaku_out)
            outp.parent.mkdir(parents=True, exist_ok=True)
            with open(outp, 'w', encoding='utf-8') as f:
                json.dump(dms, f, ensure_ascii=False, indent=2)
            ok(f"弹幕 {len(dms)} 条 → {outp}")
        else:
            err(f"弹幕拉取失败: {bvid}")
    return 0


def _fetch_danmaku_bvid(bvid, seg_from=None, seg_to=None):
    """拉单个 BV 的所有段弹幕 (走 bilibili_api 库, 不走 agent-browser).

    返回: list[dict] = [{time_ms, mode, fontsize, color, content, mid_hash, ctime, weight, pool, sender_id}, ...]
    """
    try:
        import asyncio
        from bilibili_api.video import Video
    except ImportError as e:
        err(f"未安装 bilibili_api: {e} (请在 .venv 里 pip install bilibili-api-python)")
        return None

    async def _go():
        v = Video(bvid=bvid)
        # 拿总段数 (6 分钟一段)
        info = await v.get_info()
        dur = info.get('duration', 0)  # 秒
        # 段数 = ceil(dur/360); 多 1 段余量防 B 站临时改索引
        total_segs = max(1, (dur + 359) // 360) + 1
        _sf = seg_from if seg_from is not None else 0
        _st = seg_to   if seg_to   is not None else total_segs
        _st = min(_st, total_segs)

        all_dms = []
        for s in range(_sf, _st):
            try:
                dms = await v.get_danmakus(from_seg=s, to_seg=s)
            except Exception as ex:
                err(f"  段 {s} 拉弹幕失败: {ex}")
                continue
            # 空段 = 后面也没了, break
            if not dms:
                break
            for d in dms:
                _ts = float(d.dm_time)  # B 站字段: 视频内偏移 (秒)
                all_dms.append({
                    'time_s':    round(_ts, 3),           # 视频内出现时间 (秒)
                    'time_ms':   int(_ts * 1000),         # 视频内出现时间 (ms)
                    'mode':      d.mode,                  # 1 滚动 / 4 底部 / 5 顶部
                    'font_size': d.font_size,
                    'color':     (('#' + str(d.color).lstrip('#').zfill(6).lower()) if d.color else '#ffffff'),
                    'content':   d.text,
                    'uid_hash':  d.crc32_id,              # mid 哈希 (B 站脱敏)
                    'pool':      d.pool,
                    'sender_id': d.id_str,
                    'weight':    d.weight,
                    'is_sub':    d.is_sub,                # 是否为字幕弹幕
                })
        return all_dms

    return asyncio.run(_go())


def cmd_danmaku(args):
    """单独抓弹幕 — 走 bilibili_api 库, 不受 agent-browser 风控影响"""
    vid = args.video
    m = re.search(r'(BV\w+)', vid)
    if not m:
        err(f"danmaku 子命令只支持 BV 号: {vid}")
        return 1
    bvid = m.group(1)
    info(f"弹幕: {bvid}  seg_from={args.seg_from} seg_to={args.seg_to}")

    dms = _fetch_danmaku_bvid(bvid, seg_from=args.seg_from, seg_to=args.seg_to)
    if dms is None:
        return 1
    ok(f"共 {len(dms)} 条弹幕")

    # stdout 模式: 展示前 N 条
    show = args.show
    if show and show > 0:
        for d in dms[:show]:
            print(f"  [{d['time_s']:>7.2f}s] {d['content']}")

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(dms, f, ensure_ascii=False, indent=2)
        ok(f"已保存到 {out}")
    return 0


def cmd_comments(args):
    """单独抓评论 (深翻页用)"""
    vid = args.video
    m = re.search(r'(BV\w+)', vid)
    bvid = m.group(1) if m else None

    if not bvid:
        # 可能是 aid
        if vid.lower().startswith('av'):
            aid = int(vid[2:])
        else:
            try:
                aid = int(vid)
            except ValueError:
                err(f"无法识别 video 参数: {vid}")
                return 1
    else:
        js = f"""(async () => {{
          const r = await fetch('https://api.bilibili.com/x/web-interface/view?bvid={bvid}', {{credentials:'include'}});
          const j = await r.json();
          return JSON.stringify({{code: j.code, aid: j?.data?.aid, title: j?.data?.title}});
        }})()"""
        r = ab_eval(js, timeout=15)
        if not r or not r.get('aid'):
            err("查不到 aid")
            return 1
        aid = r['aid']

    info(f"aid={aid}  ps={args.ps}  pages={args.pages}")

    all_replies = []
    next_offset = 0
    for page in range(args.pages):
        js = f"""(async () => {{
          const r = await fetch('https://api.bilibili.com/x/v2/reply/main?oid={aid}&type=1&mode=3&next={next_offset}&ps={args.ps}', {{credentials:'include'}});
          const j = await r.json();
          const replies = (j?.data?.replies || []).map(rp => ({{
            rpid: rp.rpid, uname: rp.member?.uname, mid: rp.member?.mid,
            content: rp.content?.message, like: rp.like, ctime: rp.ctime
          }}));
          return JSON.stringify({{
            code: j.code, msg: j.message,
            count: j?.data?.page?.count,
            replies,
            next: j?.data?.cursor?.pagination_reply?.next_offset || 0
          }});
        }})()"""
        r = ab_eval(js, timeout=20)
        if not r or r.get('code') != 0:
            err(f"page {page} 失败: {r}")
            break
        all_replies.extend(r.get('replies', []))
        next_offset = r.get('next', 0)
        info(f"page {page+1}: +{len(r.get('replies', []))} (累计 {len(all_replies)})")
        if next_offset == 0:
            break
        time.sleep(0.5)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            json.dump({'aid': aid, 'count': len(all_replies), 'replies': all_replies},
                      f, ensure_ascii=False, indent=2)
        ok(f"已保存到 {out}")
    else:
        print(f"\n💬 aid={aid}  共 {len(all_replies)} 条评论\n")
        for c in all_replies[:args.show]:
            print(f"  • {c['uname']} (👍{c['like']}): {c['content'][:140]}")
    return 0


# ============== 主入口 ==============

def main():
    p = argparse.ArgumentParser(
        description='bilibili 抓取 (走 agent-browser + 公开 API)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""子命令:
  paths                   打印路径配置
  search    <keyword>     主题视频搜索
  user-search <keyword>   用户名 → mid 解析
  user      <mid>         UP 主主页 + 视频列表
  video     <bvid|av号|URL> 单视频详情 + 评论
  comments  <bvid|aid>    单独深翻评论 (翻页)

示例:
  bili-fetch.py search "逗比的雀巢" --order pubdate
  bili-fetch.py user-search "逗比的雀巢"
  bili-fetch.py user 5294454 --videos 40
  bili-fetch.py video BV1K3Gz6pEoo --comments 20
  bili-fetch.py comments BV1K3Gz6pEoo --ps 50 --pages 5
"""
    )
    sub = p.add_subparsers(dest='cmd', required=True)

    # paths
    sub.add_parser('paths', help='打印路径配置')

    # search
    p1 = sub.add_parser('search', help='主题搜索')
    p1.add_argument('keyword', help='搜索关键词')
    p1.add_argument('--order', default='totalrank',
                    choices=['totalrank', 'click', 'pubdate', 'dm', 'stow', 'live',
                             'upuser', 'vv', 'favorite', 'hot'],
                    help='排序方式 (默认 totalrank 综合)')
    p1.add_argument('--pages', type=int, default=1, help='翻几页 (默认 1)')
    p1.add_argument('--ps', type=int, default=20, help='每页条数 (默认 20)')
    p1.add_argument('--show', type=int, default=20, help='stdout 模式展示几条 (默认 20)')
    p1.add_argument('--out', help='落盘到 JSON')

    # user-search
    p2 = sub.add_parser('user-search', help='用户名 → mid 解析')
    p2.add_argument('keyword', help='用户显示名')
    p2.add_argument('--show', type=int, default=10, help='展示几个候选 (默认 10)')
    p2.add_argument('--out', help='落盘 JSON')

    # user
    p3 = sub.add_parser('user', help='UP 主主页 + 视频列表 (走 SPA)')
    p3.add_argument('mid', help='mid 或 space URL')
    p3.add_argument('--videos', type=int, default=30, help='拿几条视频 (默认 30)')
    p3.add_argument('--out', help='落盘 JSON')
    p3.add_argument('--reload', dest='reload', default='auto',
                    choices=['auto', 'yes', 'no'],
                    help='SPA 加载策略 (默认 auto: 已渲染则跳过 reload, 避免破坏 session)')
    p3.add_argument('--scroll', dest='scroll', action='store_true',
                    help='自动滚到底拿全量列表 (适合 --videos > 40 或需要全部)')

    # video
    p4 = sub.add_parser('video', help='单视频详情 + 评论')
    p4.add_argument('video', help='BV号 / av号 / 视频URL')
    p4.add_argument('--comments', type=int, default=10, help='评论数 (默认 10, 0=不拿)')
    p4.add_argument('--danmaku-out', help='同时落盘弹幕到此文件 (JSON list, 需安装 bilibili-api)')
    p4.add_argument('--out', help='落盘 JSON')

    # comments
    p5 = sub.add_parser('comments', help='单独深翻评论')
    p5.add_argument('video', help='BV号 或 aid')
    p5.add_argument('--ps', type=int, default=20, help='每页条数 (默认 20)')
    p5.add_argument('--pages', type=int, default=3, help='最多翻几页 (默认 3)')
    p5.add_argument('--show', type=int, default=20, help='stdout 模式展示几条 (默认 20)')
    p5.add_argument('--out', help='落盘 JSON')

    # danmaku
    p6 = sub.add_parser('danmaku', help='抓弹幕 (走 bilibili_api 库, 不依赖 agent-browser)')
    p6.add_argument('video', help='BV 号')
    p6.add_argument('--seg-from', type=int, default=None, help='从第 N 段开始 (0=开头, 1 段=6 min)')
    p6.add_argument('--seg-to',   type=int, default=None, help='到第 N 段结束 (含)')
    p6.add_argument('--show', type=int, default=10, help='stdout 模式展示几条 (默认 10, 0=不展示)')
    p6.add_argument('--out', help='落盘 JSON')

    args = p.parse_args()
    fn = globals().get(f"cmd_{args.cmd.replace('-', '_')}")
    if not fn:
        err(f"未知子命令: {args.cmd}")
        return 1
    return fn(args) or 0


if __name__ == '__main__':
    sys.exit(main())