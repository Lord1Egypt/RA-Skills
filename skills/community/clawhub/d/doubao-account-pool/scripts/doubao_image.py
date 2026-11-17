# -*- coding: utf-8 -*-
"""豆包多实例工作台 —— 出图 + 高清下载（可移植版）。

子命令:
  img        单张出图 + 高清下载（新对话、基线闸、自动落盘）
  img-batch  批量出图（多实例并发错峰 + MD5 去重）

用法:
  python doubao_image.py img --slot 1 --file prompt.txt --out ./output
  python doubao_image.py img-batch --spec jobs.json --out ./output

核心机制:
  1. 每张图必须在全新对话中投喂（继承上文 = 串味 = 批量废图头号原因）
  2. 基线闸：投喂前记录 rc_gen_image 数量，投喂后只接受数量增长的新图
  3. 批量并发错峰：workers=3，起跑间隔 0.4s 防稳定性保护
  4. 内置 MD5 去重：不同文件名 md5 相同 = 抓到同一张，标不可信

输出: 只打印 @@ 开头的结构化短行，绝不回流页面文本/DOM/base64。
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import socket
import sys
import time
import threading
import urllib.request

# ---------- 底座 API（冻结签名，由 doubao_core 提供）----------
from doubao_core import S, port_of, log, up as core_up, DOUBAO_HOME, DOUBAO_OUTDIR

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
DOUBAO_URL = "https://www.doubao.com/chat/"
_SLOT_PID_DIR = os.path.join(DOUBAO_HOME, "pids")


# ---------------------------------------------------------------------------
# 浏览器生命周期管理
# ---------------------------------------------------------------------------

def _find_chrome():
    """探测 Chrome/Chromium/Edge 可执行文件路径。DOUBAO_CHROME 环境变量优先。"""
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

# TipTap 编辑器注入提示词
SET_JS = r"""(() => {
  const div = document.querySelector('.tiptap.ProseMirror');
  if (!div) return 'NO_EDITOR';
  const txt = %s;
  try {
    if (div.editor && div.editor.commands) {
      div.editor.commands.setContent(txt);
    } else {
      div.focus();
      document.execCommand('selectAll', false, null);
      document.execCommand('delete', false, null);
      document.execCommand('insertText', false, txt);
    }
  } catch (e) { return 'SET_ERR:' + e.message; }
  return 'SET_LEN=' + (div.innerText || '').length;
})()"""

# 发送键（多路兜底：优先 flow-end-msg-send，否则找无文字+含图标的按钮）
SEND_JS = r"""(() => {
  let b = document.getElementById('flow-end-msg-send');
  if (!b) {
    const cands = [...document.querySelectorAll('button,div[role=button],div')]
      .filter(e => {
        const r = e.getBoundingClientRect();
        if (r.width < 20 || r.width > 60 || r.height < 20 || r.height > 60) return false;
        if (r.y < window.innerHeight * 0.5) return false;
        const t = (e.innerText || '').trim();
        return t === '' && e.querySelector('svg');
      });
    if (!cands.length) return 'NO_SEND_BTN';
    b = cands[cands.length - 1];
  }
  const props = b[Object.keys(b).find(k => k.startsWith('__reactProps'))];
  try { b.click(); } catch (e) {}
  if (props && props.onClick) {
    try { props.onClick({preventDefault:()=>{}, stopPropagation:()=>{}, target:b, currentTarget:b}); } catch (e) {}
  }
  return 'SENT';
})()"""

# 点击「图像生成」模式按钮
CLICK_IMG_JS = r"""(() => {
  const norm = e => (e.innerText||'').split(String.fromCharCode(10)).join('')
    .split(String.fromCharCode(13)).join('').split(String.fromCharCode(9)).join('').trim();
  if ((document.body.innerText||'').indexOf('描述你想要的图片') >= 0) return 'ALREADY_IMG';
  let c = [...document.querySelectorAll('button,div,span,a')].filter(e => {
    const r = e.getBoundingClientRect();
    return r.width > 40 && r.height > 18 && r.height < 90 && norm(e) === '图像生成';
  });
  if (!c.length) return 'NO_IMG_BTN';
  c.sort((a,b) => a.getBoundingClientRect().width - b.getBoundingClientRect().width)[0].click();
  return 'CLICKED';
})()"""

# 安全确认弹窗处理
MODAL_JS = r"""(() => {
  const t = document.body.innerText || '';
  if (t.indexOf('安全确认') < 0 && t.indexOf('充分授权') < 0) return 'NO_MODAL';
  const btns = [...document.querySelectorAll('button,div,span')].filter(e => {
    const tx = (e.innerText||'').trim();
    const r = e.getBoundingClientRect();
    return tx === '确认' && r.width > 30 && r.height > 18 && r.width < 400;
  });
  if (!btns.length) return 'NO_BTN';
  btns.sort((a,b) => b.getBoundingClientRect().width - a.getBoundingClientRect().width);
  btns[0].click();
  return 'MODAL_OK';
})()"""

# 统计 rc_gen_image 数量（基线闸核心）
COUNT_JS = r"""(() => document.querySelectorAll("img[src*='rc_gen_image']").length)()"""

# 忙碌状态检测
BUSY_JS = r"""(() => {
  const t = document.body.innerText || '';
  return JSON.stringify({
    busy: /正在生成|生成中|绘制中|排队|思考中/.test(t),
    n: document.querySelectorAll("img[src*='rc_gen_image']").length,
    tail: t.slice(-160)
  });
})()"""

# 点击最大的新图（让页面加载高清大图）
CLICK_BIG_JS = r"""(() => {
  const imgs=[...document.querySelectorAll("img[src*='rc_gen_image']")];
  const tail = imgs.slice(__BASE_N__);
  const pool = tail.length ? tail : imgs;
  let best=null, bw=0;
  pool.forEach(im=>{const b=im.getBoundingClientRect(); if(b.width>bw){bw=b.width;best=im;}});
  if(!best) return 'NOIMG';
  best.scrollIntoView({block:'center'});
  const b=best.getBoundingClientRect();
  return JSON.stringify({x:Math.round(b.x+b.width/2), y:Math.round(b.y+b.height/2)});
})()"""

# 从 DOM 取高清 URL（naturalWidth > 2000 过滤缩略图）
HI_URL_JS = r"""(() => {
  const imgs=[...document.querySelectorAll("img[src*='rc_gen_image']")];
  const tail = imgs.slice(__BASE_N__);
  const pick = arr => { let b=''; arr.forEach(im=>{const u=im.currentSrc||im.src||''; if(u) b=u;}); return b; };
  const hiOf = arr => arr.filter(im=>im.naturalWidth>2000);
  let best='';
  if (hiOf(tail).length) best = pick(hiOf(tail));
  else if (tail.length) best = pick(tail);
  else if (hiOf(imgs).length) best = pick(hiOf(imgs));
  else best = pick(imgs);
  return best;
})()"""


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def _file_md5(path):
    """计算文件 MD5。"""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


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


# ---------------------------------------------------------------------------
# img 子命令：单张出图 + 高清下载
# ---------------------------------------------------------------------------

def cmd_img(args):
    """单张出图完整链路：
    1. 确保浏览器存活
    2. 打开新对话（防串味）
    3. 基线闸：记录投喂前 rc_gen_image 数量
    4. 注入提示词 → 发送 → 等生成
    5. 确认数量增长（基线闸通过）
    6. 点击新图加载高清 → 下载
    """
    slot = args.slot
    prompt_file = args.file
    out_dir = args.out

    os.makedirs(out_dir, exist_ok=True)
    _ensure_browser(slot)

    # 读取提示词
    with open(prompt_file, encoding="utf-8") as f:
        prompt = f.read().strip()
    if not prompt:
        print("@@FAIL 提示词文件为空 slot=%d" % slot, flush=True)
        return

    s = S(port_of(slot))
    try:
        # ① 打开新对话（核心：继承上文 = 串味）
        s.navigate(DOUBAO_URL)
        s.ready(limit=25)
        time.sleep(6)

        # ② 切换到图像生成模式
        for att in range(3):
            mode = s.ev(CLICK_IMG_JS, 2.0)
            if mode in ("CLICKED", "ALREADY_IMG"):
                break
            time.sleep(3)
        log("img", "mode=%s slot=%d" % (mode, slot))
        if mode not in ("CLICKED", "ALREADY_IMG"):
            time.sleep(4)
            mode = s.ev(CLICK_IMG_JS, 2.0)
            if mode not in ("CLICKED", "ALREADY_IMG"):
                print("@@FAIL 无法切换图像生成模式(slot=%d mode=%s)" % (slot, mode), flush=True)
                return

        time.sleep(3)

        # ③ 等待编辑器就绪
        editor = "NO"
        for _ in range(8):
            editor = s.ev(
                r"(() => {const e=document.querySelector('[contenteditable=true],textarea');"
                r"return e?'READY':'NO';})()", 1.0
            )
            if editor == "READY":
                break
            time.sleep(2)
        log("img", "editor=%s slot=%d" % (editor, slot))
        if editor != "READY":
            print("@@FAIL 编辑器未就绪(slot=%d)" % slot, flush=True)
            return

        time.sleep(2)

        # ④ 处理安全确认弹窗
        modal = s.ev(MODAL_JS, 1.5)
        log("img", "modal=%s slot=%d" % (modal, slot))
        time.sleep(1)

        # ⑤ 基线闸：记录投喂前图片数量
        base = 0
        try:
            base = int(s.ev(COUNT_JS, 1.0) or 0)
        except Exception:
            base = 0
        log("img", "baseline=%d slot=%d" % (base, slot))

        # ⑥ 注入提示词
        injected = "NO"
        for att in range(5):
            injected = s.ev(SET_JS % json.dumps(prompt, ensure_ascii=False), 1.5)
            if "SET_LEN=0" not in str(injected) and "NO_EDITOR" not in str(injected) and "ERR" not in str(injected):
                break
            log("img", "inject_retry%d=%s slot=%d" % (att + 1, injected, slot))
            time.sleep(4)
        log("img", "set=%s slot=%d" % (injected, slot))
        if "SET_LEN=0" in str(injected):
            print("@@FAIL 注入失败(SET_LEN=0) slot=%d" % slot, flush=True)
            return

        time.sleep(1.0)

        # ⑦ 发送
        sent = s.ev(SEND_JS, 2.5)
        log("img", "send=%s slot=%d" % (sent, slot))
        time.sleep(4)

        # ⑧ 等生成完成（最多 300 秒）
        t0 = time.time()
        while time.time() - t0 < 300:
            try:
                st = json.loads(s.ev(BUSY_JS, 1.0) or "{}")
            except Exception:
                st = {}
            cur = int(st.get("n") or 0)
            busy = st.get("busy", False)
            elapsed = int(time.time() - t0)
            log("img", "wait %ds busy=%s gen=%d base=%d slot=%d" % (elapsed, busy, cur, base, slot))
            if cur > base:
                time.sleep(5)
                break
            if not busy and elapsed > 30:
                break
            time.sleep(9)

        # ⑨ 基线闸验证：必须有新图
        cnt = 0
        try:
            cnt = int(s.ev(COUNT_JS, 2.0) or 0)
        except Exception:
            cnt = 0
        if cnt <= base:
            print("@@FAIL 基线闸拦截(base=%d cnt=%d) 本轮无新生成图 slot=%d" % (base, cnt, slot), flush=True)
            return

        time.sleep(6)

        # ⑩ 点击新图中最大的那张，触发高清大图加载
        click_result = s.ev(CLICK_BIG_JS.replace("__BASE_N__", str(base)), 3.0)
        try:
            coords = json.loads(click_result) if isinstance(click_result, str) else {}
        except Exception:
            coords = {}
        if coords:
            s.send("Input.dispatchMouseEvent", {
                "type": "mouseMoved", "x": coords["x"], "y": coords["y"]
            })
            time.sleep(0.6)
            for t in ("mousePressed", "mouseReleased"):
                s.send("Input.dispatchMouseEvent", {
                    "type": t, "x": coords["x"], "y": coords["y"],
                    "button": "left", "clickCount": 1
                })
                time.sleep(0.4)
            time.sleep(6)

        # ⑪ 轮询取高清 URL
        url = ""
        for _ in range(10):
            url = s.ev(HI_URL_JS.replace("__BASE_N__", str(base)), 3.0) or ""
            if url:
                break
            time.sleep(4)

        if not url:
            print("@@FAIL 未取到高清URL slot=%d" % slot, flush=True)
            return

        # ⑫ 下载高清图
        ts = time.strftime("%m%d_%H%M%S")
        dst = os.path.join(out_dir, "doubao_%s_%s.jpg" % (slot, ts))
        data = _download(url, dst)
        md5 = _file_md5(dst)
        print("@@OK slot=%d %s %dKB md5=%s" % (slot, dst, len(data) // 1024, md5[:12]), flush=True)

    finally:
        try:
            s.close()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# img-batch 子命令：批量出图
# ---------------------------------------------------------------------------

def _batch_worker(item, delay, out_dir, results, lock):
    """单个 worker：投喂 + 等生成 + 取高清，结果写入 results 列表。"""
    time.sleep(delay)
    slot = item["slot"]
    task_id = item.get("id", "unknown")
    prompt_text = item.get("prompt", "")
    prompt_file = item.get("file", "")

    result = {"id": task_id, "slot": slot, "status": "FAIL", "path": "", "md5": ""}

    try:
        # 读提示词
        if prompt_file:
            with open(prompt_file, encoding="utf-8") as f:
                prompt = f.read().strip()
        else:
            prompt = prompt_text
        if not prompt:
            result["reason"] = "提示词为空"
            with lock:
                results.append(result)
            return

        _ensure_browser(slot)
        s = S(port_of(slot))
        try:
            # 新对话
            s.navigate(DOUBAO_URL)
            s.ready(limit=25)
            time.sleep(6)

            # 图像生成模式
            for att in range(3):
                mode = s.ev(CLICK_IMG_JS, 2.0)
                if mode in ("CLICKED", "ALREADY_IMG"):
                    break
                time.sleep(3)
            time.sleep(3)

            # 编辑器就绪
            for _ in range(8):
                editor = s.ev(
                    r"(() => {const e=document.querySelector('[contenteditable=true],textarea');"
                    r"return e?'READY':'NO';})()", 1.0
                )
                if editor == "READY":
                    break
                time.sleep(2)
            if editor != "READY":
                result["reason"] = "编辑器未就绪"
                with lock:
                    results.append(result)
                return

            time.sleep(2)
            s.ev(MODAL_JS, 1.5)
            time.sleep(1)

            # 基线闸
            base = 0
            try:
                base = int(s.ev(COUNT_JS, 1.0) or 0)
            except Exception:
                base = 0

            # 注入 + 发送
            injected = "NO"
            for att in range(5):
                injected = s.ev(SET_JS % json.dumps(prompt, ensure_ascii=False), 1.5)
                if "SET_LEN=0" not in str(injected) and "NO_EDITOR" not in str(injected):
                    break
                time.sleep(4)
            if "SET_LEN=0" in str(injected):
                result["reason"] = "注入失败"
                with lock:
                    results.append(result)
                return

            time.sleep(1.0)
            s.ev(SEND_JS, 2.5)
            time.sleep(4)

            # 等生成
            t0 = time.time()
            while time.time() - t0 < 300:
                try:
                    st = json.loads(s.ev(BUSY_JS, 1.0) or "{}")
                except Exception:
                    st = {}
                cur = int(st.get("n") or 0)
                if cur > base:
                    time.sleep(5)
                    break
                if not st.get("busy", False) and int(time.time() - t0) > 30:
                    break
                time.sleep(9)

            # 基线闸验证
            cnt = 0
            try:
                cnt = int(s.ev(COUNT_JS, 2.0) or 0)
            except Exception:
                cnt = 0
            if cnt <= base:
                result["reason"] = "基线闸拦截(base=%d cnt=%d)" % (base, cnt)
                with lock:
                    results.append(result)
                return

            time.sleep(6)

            # 点击 + 取高清
            cr = s.ev(CLICK_BIG_JS.replace("__BASE_N__", str(base)), 3.0)
            try:
                co = json.loads(cr) if isinstance(cr, str) else {}
            except Exception:
                co = {}
            if co:
                s.send("Input.dispatchMouseEvent", {
                    "type": "mouseMoved", "x": co["x"], "y": co["y"]
                })
                time.sleep(0.6)
                for t in ("mousePressed", "mouseReleased"):
                    s.send("Input.dispatchMouseEvent", {
                        "type": t, "x": co["x"], "y": co["y"],
                        "button": "left", "clickCount": 1
                    })
                    time.sleep(0.4)
                time.sleep(6)

            url = ""
            for _ in range(10):
                url = s.ev(HI_URL_JS.replace("__BASE_N__", str(base)), 3.0) or ""
                if url:
                    break
                time.sleep(4)

            if not url:
                result["reason"] = "未取到高清URL"
                with lock:
                    results.append(result)
                return

            ts = time.strftime("%m%d_%H%M%S")
            dst = os.path.join(out_dir, "%s_%s.jpg" % (task_id, ts))
            data = _download(url, dst)
            md5 = _file_md5(dst)
            result["status"] = "OK"
            result["path"] = dst
            result["md5"] = md5
            result["size_kb"] = len(data) // 1024

        finally:
            try:
                s.close()
            except Exception:
                pass

    except Exception as e:
        result["reason"] = str(e)[:120]

    with lock:
        results.append(result)


def cmd_img_batch(args):
    """批量出图：
    spec.json 每行一条 {"id":"镜01","slot":1,"prompt":"..."} 或 {"id":"镜01","slot":1,"file":"词.txt"}
    多实例并行 workers=3，起跑间隔 0.4s 错峰防稳定性保护。
    结果写 result.json。
    """
    spec_file = args.spec
    out_dir = args.out
    workers = args.workers
    stagger = args.stagger

    os.makedirs(out_dir, exist_ok=True)

    with open(spec_file, encoding="utf-8") as f:
        spec = json.load(f)

    if not isinstance(spec, list) or not spec:
        print("@@FAIL spec.json 为空或格式错误", flush=True)
        return

    log("batch", "spec=%d workers=%d stagger=%.1f" % (len(spec), workers, stagger))

    results = []
    lock = threading.Lock()
    threads = []

    for i, item in enumerate(spec):
        delay = i * stagger
        t = threading.Thread(
            target=_batch_worker,
            args=(item, delay, out_dir, results, lock),
            daemon=True,
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join(timeout=600)

    # MD5 去重体检
    md5_map = {}
    for r in results:
        m = r.get("md5", "")
        if m:
            if m in md5_map:
                r["duplicate_of"] = md5_map[m]
                r["status"] = "DUPLICATE"
            else:
                md5_map[m] = r.get("id", "")

    # 写 result.json
    result_path = os.path.join(out_dir, "result.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 汇总
    ok_count = sum(1 for r in results if r.get("status") == "OK")
    dup_count = sum(1 for r in results if r.get("status") == "DUPLICATE")
    fail_count = len(results) - ok_count - dup_count

    for r in results:
        s = r.get("status", "FAIL")
        rid = r.get("id", "")
        slot = r.get("slot", "")
        if s == "OK":
            print("@@RESULT id=%s slot=%s OK path=%s md5=%s" % (
                rid, slot, r.get("path", ""), r.get("md5", "")[:12]), flush=True)
        elif s == "DUPLICATE":
            print("@@RESULT id=%s slot=%s DUPLICATE dup_of=%s" % (
                rid, slot, r.get("duplicate_of", "")), flush=True)
        else:
            print("@@RESULT id=%s slot=%s FAIL reason=%s" % (
                rid, slot, r.get("reason", "")[:80]), flush=True)

    print("@@BATCHDONE total=%d ok=%d duplicate=%d fail=%d result=%s" % (
        len(results), ok_count, dup_count, fail_count, result_path), flush=True)


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="doubao_image",
        description="豆包多实例工作台 —— 出图 + 高清下载（可移植版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
子命令:
  img        单张出图 + 高清下载（新对话、基线闸、自动落盘）
  img-batch  批量出图（多实例并发错峰 + MD5 去重）

核心机制:
  1. 每张图必须在全新对话中投喂（继承上文 = 串味 = 批量废图头号原因）
  2. 基线闸：投喂前记录 rc_gen_image 数量，投喂后只接受数量增长的新图
  3. 批量并发错峰：workers=3，起跑间隔 0.4s 防稳定性保护
  4. 内置 MD5 去重：不同文件名 md5 相同 = 抓到同一张，标不可信

环境变量:
  DOUBAO_HOME    状态根目录（含实例 Chrome profile 等）
  DOUBAO_OUTDIR  默认产出目录
  DOUBAO_CHROME  Chrome/Edge 可执行文件路径

示例:
  python doubao_image.py img --slot 1 --file prompt.txt --out ./output
  python doubao_image.py img-batch --spec jobs.json --out ./output
""")
    sub = parser.add_subparsers(dest="command", required=True)

    p_img = sub.add_parser("img", help="单张出图 + 高清下载")
    p_img.add_argument("--slot", type=int, required=True, help="实例编号（1-N）")
    p_img.add_argument("--file", type=str, required=True, help="提示词文件路径")
    p_img.add_argument("--out", type=str, default=".", help="输出目录（默认当前目录）")

    p_batch = sub.add_parser("img-batch", help="批量出图（多实例并发错峰）")
    p_batch.add_argument("--spec", type=str, required=True, help="任务规格 JSON 文件")
    p_batch.add_argument("--out", type=str, default=".", help="输出目录（默认当前目录）")
    p_batch.add_argument("--workers", type=int, default=3, help="并发 worker 数（默认 3）")
    p_batch.add_argument("--stagger", type=float, default=0.4, help="起跑间隔秒数（默认 0.4，防稳定性保护）")

    args = parser.parse_args()
    if args.command == "img":
        cmd_img(args)
    elif args.command == "img-batch":
        cmd_img_batch(args)


if __name__ == "__main__":
    main()
