#!/usr/bin/env python3
"""
bili-review - B站视频字幕抓取 + 评论区爬取
子功能:
  subtitle  <bvid|url>           抓取AI字幕(yt-dlp, 自动复用本地登录态)
  comments  <bvid|url> --limit   爬取评论区(公开API, 免登录, 按点赞排序)
  all       <bvid|url>           字幕+评论一起输出
  login                          从浏览器提取登录态存本地(首次需授权一次, 有效约150天)
  status                          查看登录态状态

登录态方案: 首次执行自动从浏览器提取 cookie 存 cookies.txt, 之后150天内自动复用;
          过期后自动重新提取。多浏览器自动探测(chrome/edge/firefox/brave等)。
纯 Python 标准库, 无第三方 API Key。
"""
import argparse
import concurrent.futures
import hashlib
import http.cookiejar
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zlib
from pathlib import Path

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

BVID_PATTERN = re.compile(r'BV[0-9A-Za-z]{10}')
AID_PATTERN = re.compile(r'(?:av|AV)(\d+)')

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
COOKIE_FILE = BASE_DIR / "cookies.txt"

BROWSERS = ["chrome", "edge", "firefox", "brave", "chromium",
            "opera", "vivaldi", "whale", "safari"]


def extract_bvid(text: str) -> str:
    """从 BV号 / AV号 / 完整链接 / b23.tv 短链中提取 BV 号."""
    text = str(text).strip()
    m = BVID_PATTERN.search(text)
    if m:
        return m.group(0)

    # 支持 AV 号 (如 av170001, AV2)
    m_aid = AID_PATTERN.search(text)
    if m_aid:
        aid = m_aid.group(1)
        try:
            data = http_get_json(f"https://api.bilibili.com/x/web-interface/view?aid={aid}")
            if data.get('code') == 0 and data.get('data', {}).get('bvid'):
                return data['data']['bvid']
        except Exception:
            pass

    if 'b23.tv' in text:
        url = text if text.startswith(('http://', 'https://')) else f"https://{text}"
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                final_url = resp.geturl()
            m = BVID_PATTERN.search(final_url)
            if m:
                return m.group(0)
        except Exception:
            pass
    raise ValueError(f"无法从输入中解析BV号: {text}")


def http_get_json(url: str, referer: str = None, retries: int = 3) -> dict:
    """带 412 限流退避重试的 JSON 请求."""
    headers = {'User-Agent': UA}
    if referer:
        headers['Referer'] = referer
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 412 and attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            raise RuntimeError(f"B站限流(HTTP {e.code}), 请稍后重试") from e
        except urllib.error.URLError as e:
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue
            raise RuntimeError(f"网络请求失败: {e.reason}") from e


def get_video_info(bvid: str) -> dict:
    """通过 view 接口获取 aid、cid 和元信息."""
    data = http_get_json(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}",
                         referer=f"https://www.bilibili.com/video/{bvid}")
    if data.get('code') != 0:
        raise RuntimeError(f"获取视频信息失败: {data.get('message')}")
    d = data['data']
    pubdate_ts = d.get('pubdate', 0)
    pubdate_str = time.strftime('%Y-%m-%d', time.localtime(pubdate_ts)) if pubdate_ts else '未知'
    cid = d.get('cid') or (d.get('pages') and d['pages'][0].get('cid')) or 0
    return {
        'aid': d['aid'],
        'cid': cid,
        'duration': d.get('duration', 0),
        'title': d['title'],
        'author': d['owner']['name'],
        'pubdate': pubdate_str,
        'stats': {
            'view': d['stat']['view'],
            'like': d['stat']['like'],
            'comment': d['stat']['reply'],
            'danmaku': d['stat'].get('danmaku', 0),
        },
    }


# ---------- 登录态管理 ----------

def find_ytdlp_python() -> str:
    """定位安装了 yt_dlp 模块的 python 环境(用于解密浏览器 cookie)."""
    # 1. 当前环境若直接支持 yt_dlp 模块，直接复用
    try:
        import yt_dlp  # noqa: F401
        return sys.executable
    except ImportError:
        pass

    # 2. 检查 which yt-dlp 的 shebang 解释器
    ytdlp_bin = shutil.which('yt-dlp')
    if ytdlp_bin and os.path.exists(ytdlp_bin):
        try:
            with open(ytdlp_bin, 'rb') as f:
                first_line = f.readline().decode('utf-8', errors='ignore').strip()
                if first_line.startswith('#!') and 'python' in first_line:
                    py_path = first_line[2:].strip()
                    if os.path.exists(py_path):
                        return py_path
        except Exception:
            pass

    # 3. macOS Homebrew 常见路径探测
    candidates = []
    try:
        prefix = subprocess.run(['brew', '--prefix', 'yt-dlp'], capture_output=True,
                                text=True, timeout=5)
        if prefix.returncode == 0:
            candidates.append(str(Path(prefix.stdout.strip()) / "libexec" / "bin" / "python3"))
    except Exception:
        pass
    candidates.append('/opt/homebrew/opt/yt-dlp/libexec/bin/python3')
    candidates.append('/usr/local/opt/yt-dlp/libexec/bin/python3')
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return sys.executable


def extract_cookies_from_browser(browser: str, output: Path) -> bool:
    """用 yt-dlp 的 python 调用 extract_cookies.py 从指定浏览器提取 cookie.
    仅提取 B站 相关域名, 不导出其他网站; 保存为 600 权限."""
    try:
        cmd = [find_ytdlp_python(), str(SCRIPTS_DIR / "extract_cookies.py"), browser, str(output)]
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=60)
        if output.exists() and output.stat().st_size > 0:
            os.chmod(output, 0o600)
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    return False


def validate_login(cookie_file: Path) -> bool:
    """通过 nav 接口校验 cookie 是否有效(需包含有效 SESSDATA)."""
    if not cookie_file.exists():
        return False
    cj = http.cookiejar.MozillaCookieJar(str(cookie_file))
    try:
        cj.load(ignore_discard=True, ignore_expires=True)
    except Exception:
        return False
    if 'SESSDATA' not in {c.name: c.value for c in cj}:
        return False
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    try:
        req = urllib.request.Request("https://api.bilibili.com/x/web-interface/nav",
                                     headers={'User-Agent': UA, 'Referer': 'https://www.bilibili.com/'})
        with opener.open(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        return data.get('data', {}).get('isLogin', False)
    except Exception:
        return False


def get_cookie_file() -> Path:
    """获取有效 cookie 文件; 无则自动从浏览器提取(首次需授权一次)."""
    if COOKIE_FILE.exists() and validate_login(COOKIE_FILE):
        return COOKIE_FILE

    print("未检测到有效登录态, 正在从浏览器提取 cookie ...", file=sys.stderr)
    for browser in BROWSERS:
        tmp = Path(tempfile.mkdtemp()) / "cookies.txt"
        if extract_cookies_from_browser(browser, tmp) and validate_login(tmp):
            os.chmod(tmp, 0o600)
            tmp.replace(COOKIE_FILE)
            print(f"已从 {browser} 提取登录态 -> {COOKIE_FILE}", file=sys.stderr)
            return COOKIE_FILE
    raise RuntimeError(
        "浏览器 cookie 提取失败(弹窗被取消或无B站登录)。"
        f"请确认浏览器已登录B站后重试: python3 {SCRIPTS_DIR / 'bili_review.py'} login")


def get_login_uname(cookie_file: Path) -> str:
    cj = http.cookiejar.MozillaCookieJar(str(cookie_file))
    cj.load(ignore_discard=True, ignore_expires=True)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    req = urllib.request.Request("https://api.bilibili.com/x/web-interface/nav",
                                 headers={'User-Agent': UA})
    data = json.loads(opener.open(req, timeout=15).read().decode())
    return data.get('data', {}).get('uname', '')


def cmd_login(args) -> None:
    """显式提取浏览器 cookie 到本地文件."""
    if COOKIE_FILE.exists() and validate_login(COOKIE_FILE):
        print(f"登录态已存在且有效: {COOKIE_FILE}")
        print(f"当前账号: {get_login_uname(COOKIE_FILE)} (有效期约150天)")
        return
    print("将从浏览器提取B站登录态; 系统弹窗弹出时请授权(仅需一次, 之后150天内自动复用)")
    get_cookie_file()
    print(f"登录成功: {get_login_uname(COOKIE_FILE)} (有效期约150天)")


def cmd_status(args) -> None:
    """查看登录态状态."""
    if COOKIE_FILE.exists() and validate_login(COOKIE_FILE):
        print(f"登录态有效: {COOKIE_FILE}")
        print(f"当前账号: {get_login_uname(COOKIE_FILE)}")
    elif COOKIE_FILE.exists():
        print(f"登录态已过期: {COOKIE_FILE} (运行 login 重新提取)")
    else:
        print(f"未找到登录态文件: {COOKIE_FILE} (运行 login 提取)")


# ---------- 评论区 ----------

def fmt_date(ts: int) -> str:
    return time.strftime('%Y-%m-%d', time.localtime(ts)) if ts else '未知'


# 楼层爬取公式: 楼层 = min(200, ceil(评论数×30% ÷ 20) × 20)
# 数学性质: 单调不降, 20条/页对齐, 自动封顶200楼(10页)
def floor_limit(total: int) -> int:
    return min(200, math.ceil(total * 0.3 / 20) * 20)


# 楼中楼单楼规则: 按某楼评论的楼中楼数量决定爬取条数(对齐到20条/页)
def reply_limit(count: int) -> int:
    if count <= 20:
        return count
    elif count <= 250:
        return 40  # 2页
    else:
        return 60  # 3页


def fetch_replies(aid: int, rpid: int, max_replies: int = 60) -> list:
    """抓取某条评论的深度楼中楼回复: 按 pn 翻页直到收集满 max_replies 条或数据结束.
    基于 rpid 集合防死循环, 过滤过短无意义水评."""
    collected = []
    seen_rpids = set()
    pn = 1
    while len(collected) < max_replies:
        try:
            data = http_get_json(
                f"https://api.bilibili.com/x/v2/reply/reply?type=1&oid={aid}"
                f"&root={rpid}&ps=20&pn={pn}",
                referer="https://www.bilibili.com/")
        except Exception:
            break
        if data.get('code') != 0:
            break
        replies = (data.get('data') or {}).get('replies') or []
        if not replies:
            break
        page_rpids = {r['rpid'] for r in replies}
        if page_rpids.issubset(seen_rpids):
            break
        for r in replies:
            if r['rpid'] in seen_rpids:
                continue
            seen_rpids.add(r['rpid'])
            text = r.get('content', {}).get('message', '').strip()
            if len(text) <= 1:
                continue
            collected.append({
                'like': r.get('like', 0),
                'author': r.get('member', {}).get('uname', '匿名'),
                'date': fmt_date(r.get('ctime', 0)),
                'text': text,
            })
            if len(collected) >= max_replies:
                break
        cursor = (data.get('data') or {}).get('page') or {}
        if cursor.get('count', 0) <= pn * 20:
            break
        pn += 1
    return collected


def estimate_crawl(total: int, include_replies: bool = False) -> tuple:
    """预估全量抓取的请求次数和耗时."""
    main_pages = math.ceil(total / 20)
    if include_replies:
        # 预估约 25% 的楼层有深度回复需要深挖，平均每个 1.5 页
        reply_reqs = int(main_pages * 20 * 0.25 * 1.5)
        est_reqs = main_pages + reply_reqs
        sec = max(2, int(est_reqs / 10))
    else:
        est_reqs = main_pages
        sec = max(1, int(est_reqs / 5))

    if sec < 60:
        time_str = f"约 {sec} 秒"
    else:
        mins = sec // 60
        time_str = f"约 {mins} 分 {sec % 60} 秒"
    return est_reqs, time_str


def confirm_full_crawl(total: int, include_replies: bool, yes: bool) -> bool:
    """针对大评论量全量抓取进行时间预估与二次确认. 返回 True 表示确认全量，False 表示降级为默认限制."""
    if total <= 500 or yes:
        return True
    est_reqs, time_str = estimate_crawl(total, include_replies)
    prompt_msg = (
        f"\n[提示] 视频总评论数: {fmt_num(total)} 条。\n"
        f"全量扫描预计需要 {est_reqs} 次请求，耗时 {time_str}（高频请求可能触发 B 站限流）。\n"
        f"是否继续全量抓取？[y/N]: "
    )
    if not sys.stdin.isatty():
        print(f"[提示] 视频总评论数: {fmt_num(total)} 条。全量预计耗时 {time_str}。(非交互环境未指定 -y，自动使用默认安全上限)", file=sys.stderr)
        return False
    try:
        res = input(prompt_msg).strip().lower()
        if res in ('y', 'yes'):
            return True
        print("已取消全量抓取，自动使用默认安全上限（最多 200 楼）继续执行。\n", file=sys.stderr)
        return False
    except (KeyboardInterrupt, EOFError):
        print("\n已取消全量抓取，自动使用默认安全上限（最多 200 楼）继续执行。\n", file=sys.stderr)
        return False


def fetch_comments(bvid: str, limit: int = 200, include_replies: bool = False, is_full: bool = False) -> dict:
    """爬取评论区: 免登录公开API, 热门排序(mode=3).
    楼层规则: limit=0 或 is_full=True 为全量抓取，否则 min(200, 评论数×30%对齐20/页).
    轻量去噪: 过滤过短字符, 同一文本出现超过3次则跳过(不中断主流程).
    死循环防护: 基于 rpid 集合与 cursor 状态判断.
    楼中楼: 默认利用接口自带预览; 开启 include_replies 时多线程并发深挖."""
    info = get_video_info(bvid)
    total = info['stats']['comment']
    target = float('inf') if (is_full or limit == 0) else min(floor_limit(total), limit)
    comments = []
    seen_rpids = set()
    text_freq = {}
    next_page = 0

    try:
        while len(comments) < target:
            data = http_get_json(
                f"https://api.bilibili.com/x/v2/reply/main?type=1&oid={info['aid']}"
                f"&mode=3&next={next_page}",
                referer=f"https://www.bilibili.com/video/{bvid}")
            if data.get('code') != 0:
                raise RuntimeError(f"获取评论失败: {data.get('message')}")
            d = data.get('data') or {}
            replies = d.get('replies') or []
            if not replies:
                break
            page_rpids = {r['rpid'] for r in replies}
            if page_rpids.issubset(seen_rpids):
                break
            for r in replies:
                rpid = r['rpid']
                if rpid in seen_rpids:
                    continue
                seen_rpids.add(rpid)
                text = r.get('content', {}).get('message', '').strip()
                if len(text) <= 1:
                    continue
                text_freq[text] = text_freq.get(text, 0) + 1
                if text_freq[text] > 3:
                    continue  # 同文本刷屏超过3次仅跳过当前条, 绝不中断后续爬取
                c = {
                    'rpid': rpid,
                    'like': r.get('like', 0),
                    'author': r.get('member', {}).get('uname', '匿名'),
                    'date': fmt_date(r.get('ctime', 0)),
                    'text': text,
                    'rcount': r.get('rcount', 0),
                    'replies': [],
                }
                # 白嫖主接口自带的 1~3 条热评回复
                for er in (r.get('replies') or []):
                    er_text = er.get('content', {}).get('message', '').strip()
                    if len(er_text) > 1:
                        c['replies'].append({
                            'like': er.get('like', 0),
                            'author': er.get('member', {}).get('uname', '匿名'),
                            'date': fmt_date(er.get('ctime', 0)),
                            'text': er_text,
                        })
                comments.append(c)
                if len(comments) >= target:
                    break
            cursor = d.get('cursor') or {}
            next_page = cursor.get('next', next_page + 1)
            if cursor.get('is_end') or next_page is None:
                break

        # 开启 --replies 时，对回复数多于已解析条数的楼层进行线程池并发深挖
        if include_replies:
            needs_deep = [c for c in comments if c['rcount'] > len(c['replies'])]
            if needs_deep:
                def enrich(comment):
                    max_r = reply_limit(comment['rcount'])
                    deep = fetch_replies(info['aid'], comment['rpid'], max_replies=max_r)
                    if deep:
                        comment['replies'] = deep

                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    list(executor.map(enrich, needs_deep))

    except KeyboardInterrupt:
        print(f"\n[已中断] 正在整理并输出当前已抓取的 {len(comments)} 条评论...", file=sys.stderr)

    return {'info': info, 'total': total, 'comments': comments}


def fmt_num(n) -> str:
    n = int(n or 0)
    if n >= 10000:
        return f"{n / 10000:.1f}万"
    return str(n)


def print_comments_list(result: dict, include_meta: bool = True) -> None:
    info = result['info']
    if include_meta:
        print(f"# 视频: {info['title']}")
        print(f"# BVID: {info.get('bvid', '')}")
        print(f"# UP主: {info['author']}")
        print(f"# 发布时间: {info.get('pubdate', '')}")
        s = info['stats']
        print(f"# 播放: {fmt_num(s['view'])} / 点赞: {fmt_num(s['like'])} / 评论: {fmt_num(s['comment'])}")
        print(f"# 评论总数(接口返回): {fmt_num(result['total'])}")
        print()
    print(f"## 热门评论 TOP {len(result['comments'])}")
    for i, c in enumerate(result['comments'], 1):
        date_str = f"[{c['date']}] " if c.get('date') else ""
        print(f"{i}. {date_str}[点赞 {fmt_num(c['like'])}] {c['author']}: {c['text']}")
        for j, r in enumerate(c.get('replies', []), 1):
            r_date_str = f"[{r['date']}] " if r.get('date') else ""
            print(f"   └ 楼中楼{j}. {r_date_str}[点赞 {fmt_num(r['like'])}] {r['author']}: {r['text']}")


# ---------- 字幕 (WBI 原生直连 + yt-dlp 降级保底) ----------

MIXIN_KEY_ENC_TAB = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]


def get_cookie_opener(cookie_file: Path = None) -> urllib.request.OpenerDirector:
    """构建支持本地 CookieJar 的 URL 请求处理器."""
    opener = urllib.request.build_opener()
    if cookie_file and cookie_file.exists():
        cj = http.cookiejar.MozillaCookieJar(str(cookie_file))
        cj.load(ignore_discard=True, ignore_expires=True)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    return opener


def get_wbi_keys(cookie_file: Path = None) -> tuple:
    """获取 WBI 签名所必需的 img_key 和 sub_key."""
    opener = get_cookie_opener(cookie_file)
    req = urllib.request.Request("https://api.bilibili.com/x/web-interface/nav",
                                 headers={'User-Agent': UA})
    try:
        with opener.open(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        wbi_img = data.get('data', {}).get('wbi_img', {})
        img_key = wbi_img.get('img_url', '').split('/')[-1].split('.')[0]
        sub_key = wbi_img.get('sub_url', '').split('/')[-1].split('.')[0]
        if img_key and sub_key:
            return img_key, sub_key
    except Exception as e:
        raise RuntimeError(f"动态获取 WBI 密钥异常: {e}")
    raise RuntimeError("未能从 B 站动态获取 WBI 验签参数")


def sign_wbi_params(params: dict, img_key: str, sub_key: str) -> dict:
    """计算 B 站 WBI 签名."""
    raw_key = img_key + sub_key
    mixin_key = ''.join([raw_key[n] for n in MIXIN_KEY_ENC_TAB])[:32]
    curr_time = round(time.time())
    p = {**params, 'wts': curr_time}
    p = dict(sorted(p.items()))
    p = {
        k: ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v in p.items()
    }
    query = urllib.parse.urlencode(p)
    wbi_sign = hashlib.md5((query + mixin_key).encode()).hexdigest()
    p['w_rid'] = wbi_sign
    return p


def fetch_subtitle_wbi(bvid: str, lang: str = None) -> str:
    """第一优先：Python 原生 WBI 直连引擎 (无需 yt-dlp, 0.2s 极速响应)."""
    language = lang or 'ai-zh'
    cookie_file = None
    try:
        cookie_file = get_cookie_file()
    except Exception:
        pass

    info = get_video_info(bvid)
    aid = info['aid']
    cid = info['cid']

    img_key, sub_key = get_wbi_keys(cookie_file)
    signed_params = sign_wbi_params({'aid': aid, 'cid': cid, 'bvid': bvid}, img_key, sub_key)
    query_str = urllib.parse.urlencode(signed_params)
    url = f"https://api.bilibili.com/x/player/wbi/v2?{query_str}"

    opener = get_cookie_opener(cookie_file)
    req = urllib.request.Request(url, headers={
        'User-Agent': UA,
        'Referer': f'https://www.bilibili.com/video/{bvid}'
    })

    with opener.open(req, timeout=12) as resp:
        res = json.loads(resp.read().decode('utf-8'))

    sub_list = res.get('data', {}).get('subtitle', {}).get('subtitles', [])
    if not sub_list:
        raise RuntimeError("未在 WBI 接口中发现可用字幕")

    # 匹配目标语言 (优先 ai-zh, zh-CN, zh-Hans 或指定语言)
    target = None
    if language:
        target = next((s for s in sub_list if s.get('lan') == language), None)
    if not target:
        target = next((s for s in sub_list if s.get('lan') in ('ai-zh', 'zh-CN', 'zh-Hans')), sub_list[0])

    sub_url = target.get('subtitle_url', '')
    if not sub_url:
        raise RuntimeError("字幕 URL 为空")
    if sub_url.startswith('//'):
        sub_url = 'https:' + sub_url

    sub_req = urllib.request.Request(sub_url, headers={'User-Agent': UA})
    with opener.open(sub_req, timeout=12) as resp:
        sub_json = json.loads(resp.read().decode('utf-8'))

    body = sub_json.get('body', [])
    if not body:
        raise RuntimeError("字幕内容为空")

    return format_subtitle_list(body)


def format_seconds_to_time(seconds: float) -> str:
    """格式化秒数为 [MM:SS]."""
    s = int(seconds)
    mm = str(s // 60).zfill(2)
    ss = str(s % 60).zfill(2)
    return f"[{mm}:{ss}]"


def format_subtitle_list(body: list) -> str:
    """将字幕 body 列表转换为去重聚合后的结构化时间戳文本（滑动去重 + 自然整句聚合）."""
    if not body or not isinstance(body, list):
        return ""
    cleaned_items = []
    last_text = ""
    for item in body:
        content = (item.get("content") or "").strip()
        if not content or content == last_text:
            continue
        if last_text and content.startswith(last_text):
            if cleaned_items:
                cleaned_items[-1]["content"] = content
                cleaned_items[-1]["to"] = float(item.get("to") or cleaned_items[-1]["to"])
                last_text = content
                continue
        elif last_text and last_text.startswith(content):
            continue
        cleaned_items.append({
            "from": float(item.get("from") or 0),
            "to": float(item.get("to") or 0),
            "content": content
        })
        last_text = content

    sentences = []
    current_sentence = ""
    sentence_start_time = None
    for i, item in enumerate(cleaned_items):
        if sentence_start_time is None:
            sentence_start_time = item["from"]
        if current_sentence:
            current_sentence += (" " if re.search(r'[a-zA-Z0-9]$', current_sentence) else "") + item["content"]
        else:
            current_sentence = item["content"]
        next_item = cleaned_items[i + 1] if i + 1 < len(cleaned_items) else None
        is_time_gap = next_item and (next_item["from"] - item["to"] > 2.5)
        is_punctuation = bool(re.search(r'[。！？!?；;\n]$', item["content"]))
        is_len = len(current_sentence) >= 50
        if not next_item or is_time_gap or is_punctuation or is_len:
            sentences.append(f"{format_seconds_to_time(sentence_start_time)} {current_sentence.strip()}")
            current_sentence = ""
            sentence_start_time = None
    return "\n".join(sentences)


def fetch_subtitle(bvid: str, lang: str = None) -> str:
    """双层字幕抓取引擎：优先 Python 原生 WBI 直连，失败则降级为 yt-dlp."""
    try:
        text = fetch_subtitle_wbi(bvid, lang)
        if text and text.strip():
            return text
    except Exception as e:
        # print(f"提示: WBI 原生字幕抓取未成功 ({e})，降级为 yt-dlp", file=sys.stderr)
        pass

    language = lang or 'ai-zh'
    cookie_file = None
    try:
        cookie_file = get_cookie_file()
    except RuntimeError as e:
        if language.startswith("ai-"):
            raise RuntimeError(f"{e}\nAI字幕需要登录态, 无法自动获取。")
        print(f"警告: {e}", file=sys.stderr)

    with tempfile.TemporaryDirectory() as temp_dir:
        cmd = ["yt-dlp", "--write-subs", "--write-auto-subs", "--skip-download",
               "--sub-lang", language, "--output", "subs", "--no-playlist"]
        if cookie_file:
            cmd.extend(["--cookies", str(cookie_file)])
        cmd.extend([
            "--add-header", f"User-Agent: {UA}",
            "--add-header", "Referer: https://www.bilibili.com/",
            f"https://www.bilibili.com/video/{bvid}",
        ])
        try:
            subprocess.run(cmd, cwd=temp_dir, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            err = (e.stderr or "").lower()
            if "412" in err or "rate" in err:
                raise RuntimeError("yt-dlp 被B站限流(HTTP 412), 稍后重试。")
            if "logged in" in err or "subtitles" in err:
                raise RuntimeError("该视频Bilibili官方暂未生成 AI 字幕，不支持总结。")
            raise RuntimeError(f"yt-dlp 执行失败: {e.stderr}")
        except FileNotFoundError:
            raise RuntimeError("未找到 yt-dlp, 请先安装: brew install yt-dlp")

        files = list(Path(temp_dir).glob("*.vtt")) + list(Path(temp_dir).glob("*.srt"))
        if not files:
            raise RuntimeError("该视频Bilibili官方暂未生成 AI 字幕，不支持总结。")

        content = files[0].read_text(encoding='utf-8', errors='replace')
        return clean_subtitle(content, files[0].suffix.lower())


def clean_subtitle(content: str, suffix: str) -> str:
    lines = content.splitlines()
    out = []
    ts = re.compile(r'\d{1,2}:\d{2}:\d{2}(?:[.,]\d{1,3})?\s*-->\s*\d{1,2}:\d{2}:\d{2}(?:[.,]\d{1,3})?')
    for line in lines:
        line = line.strip()
        if not line or line == 'WEBVTT' or line.isdigit() or line.startswith(('NOTE', 'STYLE', 'Kind:', 'Language:')):
            continue
        if ts.match(line):
            continue
        line = re.sub(r'<[^>]+>', '', line)
        # 仅做相邻重复行滑动去重，保留后续视频中正常重复出现的台词
        if not line or (out and out[-1] == line):
            continue
        out.append(line)
    return '\n'.join(out)


def print_subtitle_output(bvid: str, lang: str) -> None:
    info = get_video_info(bvid)
    text = fetch_subtitle(bvid, lang)
    s = info['stats']
    print(f"# 视频: {info['title']}")
    print(f"# BVID: {bvid}")
    print(f"# UP主: {info['author']}")
    print(f"# 发布时间: {info.get('pubdate', '')}")
    print(f"# 播放: {fmt_num(s['view'])} / 点赞: {fmt_num(s['like'])} / 评论: {fmt_num(s['comment'])}")
    print(f"# 字幕语言: {lang or 'ai-zh'}")
    print()
    print(text)


# ---------- 弹幕分析 ----------

def fmt_seconds_to_time(seconds: float) -> str:
    s = int(seconds or 0)
    mm = s // 60
    ss = s % 60
    return f"[{mm:02d}:{ss:02d}]"


def fetch_danmaku(cid: int) -> list:
    """获取视频全量 XML 弹幕 (免登录, 纯标准库 zlib 解压)."""
    if not cid:
        return []
    url = f"https://comment.bilibili.com/{cid}.xml"
    headers = {'User-Agent': UA, 'Referer': 'https://www.bilibili.com/'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
    except Exception as e:
        raise RuntimeError(f"获取弹幕失败: {e}") from e

    try:
        decompressed = zlib.decompress(raw, -zlib.MAX_WBITS)
    except Exception:
        try:
            decompressed = zlib.decompress(raw, zlib.MAX_WBITS | 32)
        except Exception:
            decompressed = raw

    xml_text = decompressed.decode('utf-8', errors='replace')
    items = re.findall(r'<d\s+p="([^"]+)">([^<]+)</d>', xml_text)
    results = []
    for p, text in items:
        text = text.strip()
        if not text:
            continue
        parts = p.split(',')
        try:
            t = float(parts[0])
        except Exception:
            t = 0.0
        results.append({
            'time': t,
            'text': text,
            'dmid': parts[7] if len(parts) > 7 else '',
        })
    results.sort(key=lambda x: x['time'])
    return results


def analyze_danmaku(danmaku_list: list, bucket_sec: int = 30, top_spikes: int = 5) -> dict:
    """分析弹幕: 时间轴分桶高能峰值检测与即时纠错/避坑预警提炼."""
    if not danmaku_list:
        return {'total': 0, 'highlights': [], 'corrections': []}

    buckets = {}
    correction_keywords = ('错', '避坑', '翻车', '其实', '注意', '假', 'bug', '骗', '误导', '不建议', '千万别', '坑')
    corrections = []

    for d in danmaku_list:
        b_idx = int(d['time'] // bucket_sec)
        start_sec = b_idx * bucket_sec
        if b_idx not in buckets:
            buckets[b_idx] = {
                'startTime': start_sec,
                'endTime': start_sec + bucket_sec,
                'count': 0,
                'texts': []
            }
        b = buckets[b_idx]
        b['count'] += 1
        b['texts'].append(d['text'])

        # 提取关键纠错/避坑弹幕
        if any(kw in d['text'] for kw in correction_keywords) and len(corrections) < 15:
            corrections.append({
                'time': d['time'],
                'timeFormatted': fmt_seconds_to_time(d['time']),
                'text': d['text']
            })

    sorted_buckets = sorted(buckets.values(), key=lambda x: x['count'], reverse=True)
    highlights = []
    for b in sorted_buckets[:top_spikes]:
        freq = {}
        for txt in b['texts']:
            clean = re.sub(r'[\s,.!?;:，。！？；：~～]+', '', txt)
            if len(clean) >= 2:
                freq[clean] = freq.get(clean, 0) + 1
        top_buzz = [w for w, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:3]]
        highlights.append({
            'timeRange': f"[{fmt_seconds_to_time(b['startTime']).strip('[]')} - {fmt_seconds_to_time(b['endTime']).strip('[]')}]",
            'count': b['count'],
            'topBuzzwords': top_buzz,
            'samples': b['texts'][:3]
        })

    return {
        'total': len(danmaku_list),
        'highlights': highlights,
        'corrections': corrections
    }


def format_danmaku_summary(analysis: dict) -> str:
    if not analysis or not analysis.get('total'):
        return "暂无弹幕时序数据"
    lines = [f"- 弹幕总量: {analysis['total']} 条"]
    if analysis.get('highlights'):
        lines.append("\n【高能时序峰值 TOP】:")
        for idx, h in enumerate(analysis['highlights'], 1):
            buzz_str = f" (热词: {', '.join(f'\"{w}\"' for w in h['topBuzzwords'])})" if h.get('topBuzzwords') else ""
            lines.append(f"{idx}. {h['timeRange']} 弹幕密度: {h['count']}条{buzz_str}")
            if h.get('samples'):
                lines.append(f"   └ 典型弹幕: {' | '.join(f'\"{s}\"' for s in h['samples'])}")
    if analysis.get('corrections'):
        lines.append("\n【即时纠错 / 避坑预警 / 关键弹幕】:")
        for c in analysis['corrections']:
            lines.append(f"- {c['timeFormatted']} {c['text']}")
    return "\n".join(lines)


def print_danmaku_output(bvid: str) -> None:
    info = get_video_info(bvid)
    dms = fetch_danmaku(info['cid'])
    analysis = analyze_danmaku(dms)
    s = info['stats']
    print(f"# 视频: {info['title']}")
    print(f"# BVID: {bvid}")
    print(f"# UP主: {info['author']}")
    print(f"# 发布时间: {info.get('pubdate', '')}")
    print(f"# 播放: {fmt_num(s['view'])} / 弹幕: {fmt_num(s.get('danmaku', len(dms)))} / 点赞: {fmt_num(s['like'])} / 评论: {fmt_num(s['comment'])}")
    print()
    print("## 弹幕时序分析")
    print()
    print(format_danmaku_summary(analysis))


# ---------- 入口 ----------

def main():
    parser = argparse.ArgumentParser(description="bili-review: B站字幕+弹幕+评论抓取")
    sub = parser.add_subparsers(dest="mode", required=True)

    p_login = sub.add_parser("login", help="从浏览器提取登录态存本地(首次授权一次)")
    p_login.set_defaults(func=cmd_login)

    p_status = sub.add_parser("status", help="查看登录态状态")
    p_status.set_defaults(func=cmd_status)

    for name in ("subtitle", "danmaku", "comments", "all"):
        p = sub.add_parser(name, help=f"{name} 抓取")
        p.add_argument("input", help="BV号 / 视频链接 / b23.tv 短链")
        if name in ("subtitle", "all"):
            p.add_argument("--lang", default=None, help="字幕语言(默认 ai-zh, 如 en 用 ai-en)")
        if name in ("comments", "all"):
            p.add_argument("--limit", type=int, default=200, help="楼层目标上限(默认200, 设为0或使用--all-comments表示全量抓取)")
            p.add_argument("--all-comments", action="store_true", help="全量爬取评论区(不设上限)")
            p.add_argument("-y", "--yes", action="store_true", help="自动确认全量抓取，跳过交互提示")
            p.add_argument("--replies", action="store_true", help="同时抓取楼中楼(按楼数规则对齐20条/页: 20内全爬, 250内取40, 250+取60)")
        p.set_defaults(func=None)
    args = parser.parse_args()

    if args.func:
        try:
            args.func(args)
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)
        return

    try:
        limit = getattr(args, 'limit', 200)
        if limit < 0:
            raise ValueError(f"--limit 不能为负数(当前 {limit})")
        bvid = extract_bvid(args.input)
        want_full = getattr(args, 'all_comments', False) or limit == 0
        is_full = False
        if want_full:
            info = get_video_info(bvid)
            is_full = confirm_full_crawl(info['stats']['comment'], getattr(args, 'replies', False), getattr(args, 'yes', False))
            if not is_full:
                limit = 200

        if args.mode == 'subtitle':
            print_subtitle_output(bvid, args.lang)
        elif args.mode == 'danmaku':
            print_danmaku_output(bvid)
        elif args.mode == 'comments':
            result = fetch_comments(bvid, limit, args.replies, is_full=is_full)
            result['info']['bvid'] = bvid
            print_comments_list(result, include_meta=True)
        else:
            info = get_video_info(bvid)
            info['bvid'] = bvid
            subtitle_text = fetch_subtitle(bvid, args.lang)
            danmaku_list = fetch_danmaku(info['cid'])
            danmaku_analysis = analyze_danmaku(danmaku_list)
            result = fetch_comments(bvid, limit, args.replies, is_full=is_full)
            s = info['stats']
            print(f"# 视频: {info['title']}")
            print(f"# BVID: {bvid}")
            print(f"# UP主: {info['author']}")
            print(f"# 发布时间: {info.get('pubdate', '')}")
            print(f"# 播放: {fmt_num(s['view'])} / 弹幕: {fmt_num(s.get('danmaku', len(danmaku_list)))} / 点赞: {fmt_num(s['like'])} / 评论: {fmt_num(s['comment'])}")
            print()
            print("## 字幕")
            print()
            print(subtitle_text)
            print()
            print("## 弹幕时序热点")
            print()
            print(format_danmaku_summary(danmaku_analysis))
            print()
            print("## 评论区")
            print()
            print_comments_list(result, include_meta=False)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

