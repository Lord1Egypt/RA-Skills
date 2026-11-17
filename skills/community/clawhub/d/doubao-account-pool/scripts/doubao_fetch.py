# -*- coding: utf-8 -*-
"""豆包多实例工作台 —— 取件链路（浏览器重启后从会话首页找回生成结果）。

子命令:
  fetch   打开最近会话 → 真点击打开 → 滚动到底 → DOM 抓图/视频 URL → 高清下载

用法:
  python doubao_fetch.py fetch --slot 1 --out ./output

核心问题：浏览器重启后页面停在新对话首页，一张图都看不到。
必须先用 CDP 真点击（Input.dispatchMouseEvent）打开最近那条会话，
JS 合成 click 对豆包 SPA 无效。

输出: 只打印 @@ 开头的结构化短行，绝不回流页面文本/DOM/base64。
"""
import argparse
import hashlib
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request

# ---------- 底座 API（冻结签名，由 doubao_core 提供）----------
from doubao_core import S, port_of, log, up as core_up, DOUBAO_HOME, DOUBAO_OUTDIR

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
DOUBAO_URL = "https://www.doubao.com/chat/"
_SLOT_PID_DIR = os.path.join(DOUBAO_HOME, "pids")


# ---------------------------------------------------------------------------
# 浏览器生命周期管理（与 doubao_image.py 共享逻辑）
# ---------------------------------------------------------------------------

def _find_chrome():
    """探测 Chrome/Chromium/Edge 可执行文件路径。"""
    env = os.environ.get("DOUBAO_CHROME", "")
    if env and os.path.isfile(env):
        return env
    pf = os.environ.get("ProgramFiles", r"C:\Program Files")
    pf86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
    local = os.environ.get("LOCALAPPDATA", "")
    candidates = []
    for base_dir in [pf, pf86, local]:
        for sub in [
            r"Google\Chrome\Application\chrome.exe",
            r"Google\Chrome Beta\Application\chrome.exe",
            r"Google\Chrome SxS\Application\chrome.exe",
            r"Chromium\Application\chrome.exe",
            r"Microsoft\Edge\Application\msedge.exe",
        ]:
            candidates.append(os.path.join(base_dir, sub))
    for c in candidates:
        if os.path.isfile(c):
            return c
    for name in ["chrome", "chromium", "google-chrome", "msedge"]:
        p = shutil.which(name)
        if p:
            return p
    return ""


def _udd_of(n):
    """实例 n 的浏览器 profile（User Data Dir）绝对路径。"""
    return os.path.join(DOUBAO_HOME, "doubao_p%d" % n)


def _pid_file(n):
    """实例 n 的 PID 文件路径。"""
    return os.path.join(_SLOT_PID_DIR, "slot%d.pid" % n)


def _is_alive(port, timeout=1.5):
    """检测端口是否在监听。"""
    try:
        s = socket.create_connection(("127.0.0.1", port), timeout=timeout)
        s.close()
        return True
    except (ConnectionRefusedError, OSError, socket.timeout):
        return False


def _ensure_browser(slot):
    """确保实例浏览器存活。不存活则启动。"""
    port = port_of(slot)
    if _is_alive(port):
        return
    # 统一走底座 core.up()：启动参数 / user-data-dir / pidfile 口径只此一处，
    # 避免「启动器两套 → down() 认错 pidfile → 漏杀」的生命周期漏洞。
    core_up(slot)
    t0 = time.time()
    while time.time() - t0 < 30:
        if _is_alive(port):
            return
        time.sleep(1.5)
    raise RuntimeError("浏览器启动超时 slot=%d port=%d" % (slot, port))


# ---------------------------------------------------------------------------
# JS 模板
# ---------------------------------------------------------------------------

# 黑名单：左侧导航中不是会话条目的文本
CHAT_BLACK = [
    "新工作任务", "新对话", "定时任务", "技能", "云盘", "API 服务",
    "更多", "置顶", "项目", "创建新项目", "最近", "豆包", "主对话",
    "登录", "注册",
]

# 在左侧侧边栏中定位最近一条会话条目（真实矩形坐标）
FIND_SESSION_JS = r"""(() => {
  const black = %s;
  let best = null;
  [...document.querySelectorAll('a,div[role="link"],li,div')].forEach(e => {
    const t = (e.innerText || '').replace(/\s+/g, ' ').trim();
    if (!t || t.length > 40) return;
    if (black.some(b => t === b || t.indexOf(b) === 0)) return;
    const r = e.getBoundingClientRect();
    // 侧边栏区域：x < 330, y > 280（避开顶部导航和功能区）
    if (r.x < 4 || r.x > 330 || r.width < 80 || r.height < 14 || r.height > 60) return;
    if (r.y < 280) return;
    if (!best || r.y < best.y) best = {
      x: Math.round(r.x), y: Math.round(r.y),
      w: Math.round(r.width), h: Math.round(r.height), t: t
    };
  });
  return JSON.stringify(best || {});
})()"""

# 滚动到底部
SCROLL_BOTTOM_JS = r"""(() => { window.scrollTo(0, document.body.scrollHeight); return 'OK'; })()"""

# 列出页面上所有 rc_gen_image（去重，返回大小和 URL）
LIST_IMAGES_JS = r"""(() => {
  const imgs = [...document.querySelectorAll("img")].filter(i =>
    (i.src || '').indexOf('rc_gen_image') >= 0
  );
  const seen = {};
  const out = [];
  imgs.forEach(i => {
    const k = (i.src || '').split('?')[0];
    if (seen[k]) return;
    seen[k] = 1;
    out.push({src: i.src, w: i.naturalWidth, h: i.naturalHeight, n: i.src.length});
  });
  return JSON.stringify({n: out.length, big: out.filter(x => x.w > 1200), all: out.map(x => x.w + 'x' + x.h)});
})()"""

# 页面状态检查
STATUS_JS = r"""(() => {
  const t = document.body.innerText || '';
  const keys = ['已完成图片生成', '图片生成完成', '已生成', '生成好了',
                '生成中', '正在生成', '失败了', '重新生成'];
  const hit = keys.filter(k => t.indexOf(k) >= 0);
  return JSON.stringify({hit: hit, tail: t.slice(-260).replace(/\n+/g, ' | ')});
})()"""

# 收集页面中所有视频链接
FETCH_VIDEO_JS = r"""(() => {
  const vids = [];
  document.querySelectorAll('video').forEach(v => {
    const src = v.currentSrc || v.src || '';
    if (src) vids.push({type: 'video_tag', src: src});
  });
  document.querySelectorAll('video').forEach(v => {
    if (v.srcObject) {
      try { vids.push({type: 'video_blob', src: v.srcObject.toString()}); } catch (e) {}
    }
  });
  const body = document.body.innerText || '';
  const vidRe = /https?:\/\/[^\s"']+\.(?:mp4|mov|webm|m3u8)[^\s"']*/g;
  let m;
  while ((m = vidRe.exec(body)) !== null) {
    vids.push({type: 'text_link', src: m[0]});
  }
  return JSON.stringify(vids);
})()"""


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def _mouse_click(s, x, y):
    """真实 CDP 鼠标点击（Input.dispatchMouseEvent）。"""
    s.send("Input.dispatchMouseEvent", {
        "type": "mouseMoved", "x": int(x), "y": int(y)
    })
    time.sleep(0.12)
    for t in ("mousePressed", "mouseReleased"):
        s.send("Input.dispatchMouseEvent", {
            "type": t, "x": int(x), "y": int(y),
            "button": "left", "clickCount": 1
        })
        time.sleep(0.12)


def _download(url, dst_path):
    """带 User-Agent + Referer 的 HTTP 下载，先写临时文件再原子替换。"""
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://www.doubao.com/",
    })
    data = urllib.request.urlopen(req, timeout=120).read()
    os.makedirs(os.path.dirname(dst_path) or ".", exist_ok=True)
    tmp = dst_path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, dst_path)
    return data


def _file_md5(path):
    """计算文件 MD5。"""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# fetch 子命令
# ---------------------------------------------------------------------------

def cmd_fetch(args):
    """取件流程：
    1. 确保浏览器存活
    2. 导航到豆包首页
    3. CDP 真点击打开最近会话（JS 合成 click 对 SPA 无效）
    4. 滚动到底
    5. DOM 抓取 rc_gen_image URL → 高清下载
    6. 抓取视频链接
    """
    slot = args.slot
    out_dir = args.out
    os.makedirs(out_dir, exist_ok=True)

    _ensure_browser(slot)

    s = S(port_of(slot))
    try:
        # ① 导航到豆包首页
        s.navigate(DOUBAO_URL)
        s.ready(limit=25)
        time.sleep(6)

        # ② CDP 真点击打开最近会话
        rect_raw = s.ev(FIND_SESSION_JS % json.dumps(CHAT_BLACK, ensure_ascii=False), 2.0)
        try:
            rect = json.loads(rect_raw)
        except Exception:
            rect = {}
        log("fetch", "session_rect=%s slot=%d" % (json.dumps(rect, ensure_ascii=False)[:120], slot))

        if not rect:
            print("@@FAIL 未找到最近会话条目 slot=%d" % slot, flush=True)
            return

        # 真点击（Input.dispatchMouseEvent），非 JS 合成
        click_x = rect["x"] + rect["w"] // 2
        click_y = rect["y"] + rect["h"] // 2
        _mouse_click(s, click_x, click_y)
        log("fetch", "clicked x=%d y=%d text=%s slot=%d" % (click_x, click_y, rect.get("t", ""), slot))
        time.sleep(8)  # 等 SPA 路由切换 + 内容加载

        # ③ 滚动到底部（触发懒加载）
        s.ev(SCROLL_BOTTOM_JS, 1.0)
        time.sleep(2)
        s.ev(SCROLL_BOTTOM_JS, 1.0)
        time.sleep(3)

        # ④ 抓取生成图 URL
        img_info_raw = s.ev(LIST_IMAGES_JS, 2.0) or "{}"
        try:
            img_info = json.loads(img_info_raw)
        except Exception:
            img_info = {"n": 0, "big": []}

        n_all = img_info.get("n", 0)
        big = img_info.get("big", [])
        log("fetch", "images n=%d big=%d slot=%d" % (n_all, len(big), slot))

        downloaded = []
        if not big:
            print("@@NONE 没有找到高清生成图(slot=%d, total=%d)" % (slot, n_all), flush=True)
        else:
            big.sort(key=lambda x: -x["w"])
            ts = time.strftime("%m%d_%H%M%S")
            seen_md5 = set()
            for i, item in enumerate(big[:5]):
                src = item["src"]
                fname = "fetch_%s_%s_%d.jpg" % (slot, ts, i)
                dst = os.path.join(out_dir, fname)
                try:
                    data = _download(src, dst)
                    md5 = _file_md5(dst)
                    if md5 in seen_md5:
                        os.remove(dst)
                        log("fetch", "dedup md5=%s idx=%d slot=%d" % (md5[:12], i, slot))
                        continue
                    seen_md5.add(md5)
                    downloaded.append({"path": dst, "md5": md5, "size": len(data),
                                       "w": item.get("w", 0), "h": item.get("h", 0)})
                    print("@@IMG slot=%d %s %dx%d %dKB md5=%s" % (
                        slot, dst, item.get("w", 0), item.get("h", 0),
                        len(data) // 1024, md5[:12]), flush=True)
                except Exception as e:
                    print("@@IMGFAIL slot=%d idx=%d reason=%s" % (slot, i, str(e)[:80]), flush=True)

            if not downloaded:
                print("@@FAIL 所有图片下载失败 slot=%d" % slot, flush=True)

        # ⑤ 抓取视频链接
        vid_raw = s.ev(FETCH_VIDEO_JS, 2.0) or "[]"
        try:
            vids = json.loads(vid_raw)
        except Exception:
            vids = []
        vid_count = 0
        if vids:
            seen_srcs = set()
            for v in vids:
                src = v.get("src", "")
                if src in seen_srcs or not src:
                    continue
                seen_srcs.add(src)
                vid_count += 1
                print("@@VID slot=%d type=%s src=%s" % (
                    slot, v.get("type", ""), src[:200]), flush=True)

        # ⑥ 汇总
        print("@@DONE slot=%d images=%d videos=%d" % (
            slot, len(downloaded), vid_count), flush=True)

    finally:
        try:
            s.close()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="doubao_fetch",
        description="豆包多实例工作台 —— 取件链路（从会话首页找回生成结果）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
子命令:
  fetch  打开最近会话 → 真点击 → 滚动 → 抓图/视频 → 高清下载

核心原理:
  浏览器重启后页面在新对话首页，生成图看不到。
  必须用 CDP Input.dispatchMouseEvent 真点击侧边栏会话条目打开历史会话，
  JS 合成 click 对豆包 SPA 无效。

环境变量:
  DOUBAO_HOME   状态根目录（含实例 Chrome profile 等）
  DOUBAO_OUTDIR 默认产出目录

示例:
  python doubao_fetch.py fetch --slot 1 --out ./output
  python doubao_fetch.py fetch --slot 3 --out ./output
""")
    sub = parser.add_subparsers(dest="command", required=True)

    p_fetch = sub.add_parser("fetch", help="打开最近会话 → 抓图/视频 → 高清下载")
    p_fetch.add_argument("--slot", type=int, required=True, help="实例编号（1-N）")
    p_fetch.add_argument("--out", type=str, default=".", help="输出目录（默认当前目录）")

    args = parser.parse_args()
    if args.command == "fetch":
        cmd_fetch(args)


if __name__ == "__main__":
    main()
