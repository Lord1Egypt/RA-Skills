# -*- coding: utf-8 -*-
"""豆包视频生成可移植模块 —— 十二步固定链路 + 重抓 + 防误购保护

依赖: doubao_core (冻结 API：S, port_of, cfg, find_ffmpeg, log)
用法:
  python doubao_video.py vid --slot N --image 垫图.png --file 词.txt --out DIR [--name 名]
  python doubao_video.py vid-regrab --slot N --out DIR [--name 名]

输出: @@ 开头的结构化短行（<300 字符）
"""
import sys
import os
import json
import time
import re
import subprocess

# ── 导入冻结底座（绝不自建 CDP） ──
from doubao_core import S, port_of, cfg, find_ffmpeg, log

# ── 常量 ──
DOUBAO_URL = "https://www.doubao.com/chat/"
MAX_WAIT_GEN = 1200          # 等生成最长 20 分钟
POLL_INTERVAL = 60           # 轮询间隔 60 秒
CARD_POLL_MAX = 180          # 等确认卡最长 3 分钟
CARD_POLL_INTERVAL = 8       # 确认卡轮询间隔
MIN_DOWNLOAD_BYTES = 80000   # 下载最低字节数（< 80KB 视为失败）

# ── 付费关键词（出现任一即中止，绝不确认扣款） ──
PAID_KEYWORDS = [
    "消耗付费用量", "付费用量", "消耗积分", "订阅", "专业版",
    "升级会员", "开通会员", "升级", "开通", "付费", "积分",
]
# ── 用量耗尽关键词 ──
OUT_KEYWORDS = [
    "免费次数用完", "明天再来", "次数已用完", "用量不足",
    "免费次数已用完",
]
# ── 基础用量关键词 ──
FREE_KEYWORDS = [
    "消耗每日基础用量", "消耗基础用量", "基础用量",
]


# ══════════════════════════════════════════════════════════════
# JavaScript 片段（冻结：TipTap 注入 + 发送 + 读页面文本）
# ══════════════════════════════════════════════════════════════

# 注入提示词到 TipTap 编辑器
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

# 发送按钮（多路兜底）
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
  try { b.click(); } catch (e) {}
  const props = b[Object.keys(b).find(k => k.startsWith('__reactProps'))];
  if (props && props.onClick) {
    try { props.onClick({preventDefault:()=>{}, stopPropagation:()=>{}, target:b, currentTarget:b}); } catch(e) {}
  }
  return 'SENT';
})()"""

# 读页面尾部文本
TAIL_JS = r"""(() => (document.body.innerText || '').slice(-1600))()"""

# 确认卡检测（含所有关键词）
CARD_JS = r"""(() => {
  const t = document.body.innerText || '';
  const keys = ['确认，开始生成','开始生成','消耗','付费','用量','积分',
                '次数','订阅','专业版','升级会员','开通会员'];
  const hit = keys.filter(k => t.indexOf(k) >= 0);
  return JSON.stringify({hit: hit, tail: t.slice(-1400)});
})()"""

# 切换到视频生成模式
VG_MODE_JS = r"""(() => {
  const norm = e => (e.innerText||'').trim();
  const c = [...document.querySelectorAll('button,div,span')].filter(e => {
    const r = e.getBoundingClientRect();
    return r.width>40 && r.height>18 && r.height<60 && norm(e)==='视频生成';
  });
  if (!c.length) return 'NO_VG';
  c.sort((a,b)=>a.getBoundingClientRect().width-b.getBoundingClientRect().width)[0].click();
  return 'VG_OK';
})()"""

# 抓视频 URL（点击视频容器 + 扫描 video/performance 资源）
VID_GRAB_JS = r"""(() => {
  const out = [];
  for (const v of document.querySelectorAll('video')) {
    const s2 = v.currentSrc || v.src || '';
    if (s2) out.push(s2);
    for (const so of v.querySelectorAll('source')) if (so.src) out.push(so.src);
  }
  for (const e of performance.getEntriesByType('resource')) {
    if (/\.mp4|tos-cn-v|vdl\.doubao|\/video\//.test(e.name)) out.push(e.name);
  }
  return JSON.stringify([...new Set(out)].slice(0, 10));
})()"""

# 定位视频容器中心点（用于点击播放触发资源加载）
VID_CONTAINER_JS = r"""(() => {
  const els = [...document.querySelectorAll("div[class*='block-video']")];
  let best = null;
  for (const e of els) {
    const r = e.getBoundingClientRect();
    if (r.width > 120 && (!best || r.width > best.getBoundingClientRect().width)) best = e;
  }
  if (!best) return 'NOV';
  const b = best.getBoundingClientRect();
  return JSON.stringify({x: Math.round(b.x + b.width/2), y: Math.round(b.y + b.height/2)});
})()"""


# ══════════════════════════════════════════════════════════════
# 辅助函数
# ══════════════════════════════════════════════════════════════

def _paycheck(text):
    """扫描文本中是否出现付费/订阅关键词 → 返回分类。
    返回: 'paid' | 'out' | 'free' | None
    关键：paid 在前，一旦命中立即返回，绝不遗漏。"""
    if any(kw in text for kw in PAID_KEYWORDS):
        return "paid"
    if any(kw in text for kw in OUT_KEYWORDS):
        return "out"
    if any(kw in text for kw in FREE_KEYWORDS):
        return "free"
    return None


def _check_paid_abort(slot, s, stage=""):
    """主动读页面文本，检查是否有付费弹窗/升级提示。
    返回: True=应中止 | False=安全继续"""
    try:
        tail = s.ev(TAIL_JS, 1.5) or ""
    except Exception:
        return False
    verdict = _paycheck(tail)
    if verdict == "paid":
        print("@@PAID_ABORT slot=%s stage=%s 付费关键词命中，已中止" % (slot, stage), flush=True)
        return True
    if verdict == "out":
        print("@@OUT_ABORT slot=%s stage=%s 基础用量已用完，已中止" % (slot, stage), flush=True)
        return True
    return False


def _detect_vg_mode(slot, s):
    """② 切换到视频生成模式"""
    vg = s.ev(VG_MODE_JS, 2.0)
    if "NO_VG" in str(vg):
        print("@@ERR slot=%s 未找到「视频生成」按钮" % slot, flush=True)
        return False
    print("@@STEP2 slot=%s VG_OK 切换成功" % slot, flush=True)
    return True


def _upload_image(slot, s, image_path):
    """③ 上传垫图（通过 file input）"""
    abs_img = os.path.abspath(image_path)
    if not os.path.exists(abs_img):
        print("@@ERR slot=%s 垫图不存在: %s" % (slot, abs_img), flush=True)
        return False
    # 等编辑器渲染
    time.sleep(4)
    doc = s.send("DOM.getDocument", {"depth": -1})
    root = (doc.get("result") or {}).get("root", {}).get("nodeId")
    if not root:
        print("@@ERR slot=%s 无法获取 DOM" % slot, flush=True)
        return False
    q = s.send("DOM.querySelector", {"nodeId": root, "selector": "input[type=file]"})
    nid = (q.get("result") or {}).get("nodeId")
    if not nid:
        print("@@ERR slot=%s 未找到 file input" % slot, flush=True)
        return False
    s.send("DOM.setFileInputFiles", {"files": [abs_img], "nodeId": nid})
    time.sleep(14)  # 等上传+缩略图渲染
    print("@@STEP3 slot=%s 上传完成 %s" % (slot, os.path.basename(abs_img)), flush=True)
    return True


def _inject_prompt(slot, s, prompt_text):
    """④ 注入提示词到 TipTap 编辑器"""
    for att in range(5):
        r = s.ev(SET_JS % json.dumps(prompt_text, ensure_ascii=False), 1.5)
        if "SET_LEN=0" not in str(r) and "NO_EDITOR" not in str(r) and "ERR" not in str(r):
            print("@@STEP4 slot=%s 注入成功 %s" % (slot, r), flush=True)
            return True
        time.sleep(4)
    print("@@ERR slot=%s 注入失败（5次重试）" % slot, flush=True)
    return False


def _send_prompt(slot, s):
    """⑤ 发送提示词"""
    r = s.ev(SEND_JS, 2.5)
    if "SENT" not in str(r):
        print("@@ERR slot=%s 发送失败: %s" % (slot, r), flush=True)
        return False
    print("@@STEP5 slot=%s 发送成功" % slot, flush=True)
    return True


def _wait_card(slot, s):
    """⑥ 读确认卡 —— 等待确认卡/弹层出现"""
    t0 = time.time()
    while time.time() - t0 < CARD_POLL_MAX:
        try:
            st = json.loads(s.ev(CARD_JS, 1.5))
        except Exception:
            time.sleep(CARD_POLL_INTERVAL)
            continue
        hits = st.get("hit") or []
        tail = st.get("tail") or ""
        # 先做付费检查
        verdict = _paycheck(tail)
        if verdict == "paid":
            print("@@PAID_ABORT slot=%s 确认卡含付费字样，已中止" % slot, flush=True)
            return None
        if verdict == "out":
            print("@@OUT_ABORT slot=%s 确认卡含用量耗尽，已中止" % slot, flush=True)
            return None
        if "确认，开始生成" in tail or "开始生成" in tail:
            print("@@STEP6 slot=%s 确认卡命中 %s" % (slot, json.dumps(hits, ensure_ascii=False)), flush=True)
            return tail
        time.sleep(CARD_POLL_INTERVAL)
    # 超时没出确认卡 → 可能静默拒答
    return None


def _pay_gate(slot, s, card_tail):
    """⑦ 防误购保护 —— 本模块第一优先级
    确认卡/弹层出现「专业版/订阅/付费用量/升级/开通会员」任一关键词
    → 立即中止该实例并回 @@PAID_ABORT
    绝不点击任何升级按钮、绝不确认扣款
    基础用量正常时回 @@SAFE free
    """
    verdict = _paycheck(card_tail or "")
    if verdict == "paid":
        print("@@PAID_ABORT slot=%s 防误购保护拦截（未确认扣款）" % slot, flush=True)
        return False
    if verdict == "out":
        print("@@OUT_ABORT slot=%s 基础用量已用完" % slot, flush=True)
        return False
    print("@@SAFE free slot=%s 基础用量正常" % slot, flush=True)
    return True


def _confirm_generate(slot, s):
    """⑧ 确认生成（点「确认，开始生成」按钮）"""
    # 再次注入确认文本
    s.ev(SET_JS % json.dumps("确认，开始生成", ensure_ascii=False), 1.5)
    time.sleep(0.8)
    r = s.ev(SEND_JS, 2.5)
    print("@@STEP8 slot=%s 确认已发送" % slot, flush=True)
    # 发送后再检查一次付费弹窗
    time.sleep(3)
    return not _check_paid_abort(slot, s, "confirm")


def _wait_generation(slot, s):
    """⑨ 等待生成完成（轮询页面文本）"""
    t0 = time.time()
    poll_count = 0
    while time.time() - t0 < MAX_WAIT_GEN:
        time.sleep(POLL_INTERVAL)
        poll_count += 1
        try:
            s.ev("window.scrollTo(0, document.body.scrollHeight); 1", 1.0)
        except Exception:
            pass
        time.sleep(10)
        try:
            tail = s.ev(TAIL_JS, 2.0) or ""
        except Exception:
            continue
        # 生成过程中也要检查付费弹窗
        verdict = _paycheck(tail)
        if verdict == "paid":
            print("@@PAID_ABORT slot=%s 生成过程中出现付费提示" % slot, flush=True)
            return "paid"
        if verdict == "out":
            print("@@OUT_ABORT slot=%s 生成过程中用量耗尽" % slot, flush=True)
            return "out"
        if "你的视频生成好了" in tail:
            print("@@STEP9 slot=%s 生成完成 (%ds, %d次轮询)" % (
                slot, int(time.time() - t0), poll_count), flush=True)
            return "done"
        if "生成失败" in tail or "违反" in tail or "版权" in tail:
            print("@@REJECT slot=%s 生成失败/违规" % slot, flush=True)
            return "reject"
    # 超时：可能是静默拒答（零回复、不出确认卡、不报错）
    print("@@NOCARD slot=%s 等待生成超时（可能静默拒答/用量耗尽）" % slot, flush=True)
    return "timeout"


def _click_video_container(s):
    """点击视频容器触发资源加载"""
    r = s.ev(VID_CONTAINER_JS, 2.5)
    if isinstance(r, str) and r.startswith("{"):
        c = json.loads(r)
        s.send("Input.dispatchMouseEvent", {
            "type": "mouseMoved", "x": c["x"], "y": c["y"]
        })
        time.sleep(1.2)
        for typ in ("mousePressed", "mouseReleased"):
            s.send("Input.dispatchMouseEvent", {
                "type": typ, "x": c["x"], "y": c["y"],
                "button": "left", "clickCount": 1
            })
            time.sleep(0.3)
        time.sleep(6)


def _grab_video_url(slot, s):
    """⑩ 抓视频直链"""
    try:
        s.ev("(() => { window.scrollTo(0, document.body.scrollHeight); return 1; })()", 2.0)
    except Exception:
        pass
    time.sleep(2)
    _click_video_container(s)
    urls = []
    for _ in range(10):
        try:
            urls = json.loads(s.ev(VID_GRAB_JS, 3.0) or "[]")
        except Exception:
            urls = []
        if urls:
            break
        time.sleep(4)
    # 兜底：直接扫 video 元素
    if not urls:
        try:
            urls = json.loads(s.ev(
                "(() => JSON.stringify([...document.querySelectorAll('video')]"
                ".map(v => v.currentSrc || v.src || '').filter(Boolean)))()",
                3.0) or "[]")
        except Exception:
            urls = []
    # 优选 doubao CDN 域名
    best = [u for u in urls if "vdl.doubao.com" in u or "tos-cn-v" in u
            or ".mp4" in u or ".mp4?" in u]
    url = (best or urls or [""])[0]
    if url:
        print("@@STEP10 slot=%s URL=%s" % (slot, url[:110]), flush=True)
    else:
        print("@@NOURL slot=%s 未抓到视频直链" % slot, flush=True)
    return url


def _download_video(url, out_path):
    """⑪ 下载视频（curl 重试 3 次）"""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    tmp = out_path + ".part"
    for attempt in range(3):
        subprocess.run([
            "curl", "-sL", "--max-time", "300", "--retry", "2",
            "-H", "User-Agent: Mozilla/5.0",
            "-H", "Referer: https://www.doubao.com/",
            "-o", tmp, url
        ], capture_output=True, timeout=400)
        try:
            sz = os.path.getsize(tmp)
        except OSError:
            sz = 0
        if sz > MIN_DOWNLOAD_BYTES:
            os.replace(tmp, out_path)
            print("@@STEP11 下载完成 %dB %s" % (sz, os.path.basename(out_path)), flush=True)
            return sz
        time.sleep(5)
    print("@@DLFAIL 下载失败（3次重试）", flush=True)
    return 0


def _probe_spec(out_path):
    """⑫ 规格核对：必须有音轨（优先 PyAV，退化 ffmpeg -i）"""
    has_audio = False
    width, height, duration = 0, 0, 0.0
    # 优先 PyAV
    try:
        import av
        container = av.open(out_path)
        v_stream = next((s for s in container.streams if s.type == "video"), None)
        a_stream = next((s for s in container.streams if s.type == "audio"), None)
        has_audio = a_stream is not None
        if v_stream:
            width = v_stream.width or 0
            height = v_stream.height or 0
            duration = float(v_stream.duration or 0) * float(v_stream.time_base or 1)
        container.close()
    except ImportError:
        # 退化：ffmpeg -i 解析 stderr
        ff = find_ffmpeg()
        if ff:
            try:
                r = subprocess.run([ff, "-i", out_path], capture_output=True, text=True, timeout=30)
                info = (r.stderr or "")
                has_audio = "Audio:" in info
                dim = re.search(r"(\d{3,5})x(\d{3,5})", info)
                if dim:
                    width, height = int(dim.group(1)), int(dim.group(2))
                dm = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", info)
                if dm:
                    duration = int(dm.group(1)) * 3600 + int(dm.group(2)) * 60 + float(dm.group(3))
            except Exception:
                pass
    print("@@STEP12 %dx%d %.1fs audio=%s %s" % (
        width, height, duration, "Y" if has_audio else "N", os.path.basename(out_path)),
        flush=True)
    if not has_audio:
        print("@@WARN 该视频无音轨！", flush=True)
    return has_audio


# ══════════════════════════════════════════════════════════════
# 主命令
# ══════════════════════════════════════════════════════════════

def cmd_vid(args):
    """vid --slot N --image 垫图.png --file 词.txt --out DIR [--name 名]
    十二步固定链路：探活→切模式→上传→注入→发送→读卡→防误购保护→确认→等完成→抓链→下载→核对
    """
    # 解析参数
    slot = None
    image_path = None
    prompt_file = None
    out_dir = None
    name = None
    i = 0
    while i < len(args):
        if args[i] == "--slot" and i + 1 < len(args):
            slot = int(args[i + 1]); i += 2
        elif args[i] == "--image" and i + 1 < len(args):
            image_path = args[i + 1]; i += 2
        elif args[i] == "--file" and i + 1 < len(args):
            prompt_file = args[i + 1]; i += 2
        elif args[i] == "--out" and i + 1 < len(args):
            out_dir = args[i + 1]; i += 2
        elif args[i] == "--name" and i + 1 < len(args):
            name = args[i + 1]; i += 2
        else:
            i += 1

    if slot is None or out_dir is None:
        print("@@ERR 必须指定 --slot N 和 --out DIR", flush=True)
        return
    if image_path is None and prompt_file is None:
        print("@@ERR 必须指定 --image 或 --file", flush=True)
        return

    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_name = name or ("镜%02d" % slot)
    out_path = os.path.join(out_dir, out_name + ".mp4")

    # 读取提示词
    prompt_text = ""
    if prompt_file:
        pf = os.path.abspath(prompt_file)
        if not os.path.exists(pf):
            print("@@ERR 提示词文件不存在: %s" % pf, flush=True)
            return
        with open(pf, encoding="utf-8") as f:
            prompt_text = f.read().strip()

    # ── 认领锁（避免多实例撞同一镜白烧用量） ──
    lock_path = out_path + ".lock"
    if os.path.exists(lock_path):
        try:
            lock_info = open(lock_path, encoding="utf-8").read().strip()
            print("@@LOCKED slot=%s 文件已被锁: %s" % (slot, lock_info), flush=True)
            return
        except Exception:
            pass
    with open(lock_path, "w", encoding="utf-8") as f:
        f.write("slot=%d time=%s" % (slot, time.strftime("%Y-%m-%d %H:%M:%S")))
    log("vid", "slot=%d 开始十二步链路" % slot)

    try:
        s = S(port_of(slot))

        # ① 探活
        try:
            s.send("Page.navigate", {"url": DOUBAO_URL})
            time.sleep(8)
            ready = s.ready(limit=25)
            if ready < 0:
                print("@@ERR slot=%s 页面未就绪" % slot, flush=True)
                return
        except Exception as e:
            print("@@ERR slot=%s 连接失败: %s" % (slot, str(e)[:60]), flush=True)
            return
        if _check_paid_abort(slot, s, "probe"):
            return
        print("@@STEP1 slot=%s 探活OK (ready=%s)" % (slot, ready), flush=True)

        # ② 切视频生成模式
        if not _detect_vg_mode(slot, s):
            return
        time.sleep(3)

        # ③ 上传垫图
        if image_path:
            if not _upload_image(slot, s, image_path):
                return

        # ④ 注入提示词
        if prompt_text:
            if not _inject_prompt(slot, s, prompt_text):
                return
        time.sleep(1)

        # ⑤ 发送
        if not _send_prompt(slot, s):
            return

        # ⑥ 读确认卡
        card_tail = _wait_card(slot, s)
        if card_tail is None:
            # 没出确认卡 → 可能静默拒答
            print("@@NOCARD slot=%s 未出现确认卡（静默拒答或生成失败）" % slot, flush=True)
            return
        if card_tail is None:  # PAID_ABORT 已打印
            return

        # ⑦ 防误购保护（本模块第一优先级）
        if not _pay_gate(slot, s, card_tail):
            return  # @@PAID_ABORT 已打印

        # ⑧ 确认生成
        if not _confirm_generate(slot, s):
            return

        # ⑨ 等完成
        gen_result = _wait_generation(slot, s)
        if gen_result == "timeout":
            return  # @@NOCARD 已打印（静默拒答识别）
        if gen_result != "done":
            return  # paid/out/reject 已打印

        # ⑩ 抓视频链
        url = _grab_video_url(slot, s)
        if not url:
            return

        # ⑪ 下载
        sz = _download_video(url, out_path)
        if not sz:
            return

        # ⑫ 规格核对（必须有音轨）
        has_audio = _probe_spec(out_path)

        log("vid", "slot=%d 完成 %s %dB audio=%s" % (slot, out_path, sz, has_audio))
        print("@@DONE slot=%s %s %dB" % (slot, out_path, sz), flush=True)

    except Exception as e:
        print("@@ERR slot=%s 未捕获异常: %s" % (slot, str(e)[:100]), flush=True)
        log("vid", "slot=%d 异常: %s" % (slot, str(e)[:200]))
    finally:
        # 清锁
        try:
            if os.path.exists(lock_path):
                os.remove(lock_path)
        except Exception:
            pass
        try:
            s.close()
        except Exception:
            pass


def cmd_regrab(args):
    """vid-regrab --slot N --out DIR [--name 名]
    已生成但没抓到链的重抓，绝不许重跑生成（白烧用量）
    """
    slot = None
    out_dir = None
    name = None
    i = 0
    while i < len(args):
        if args[i] == "--slot" and i + 1 < len(args):
            slot = int(args[i + 1]); i += 2
        elif args[i] == "--out" and i + 1 < len(args):
            out_dir = args[i + 1]; i += 2
        elif args[i] == "--name" and i + 1 < len(args):
            name = args[i + 1]; i += 2
        else:
            i += 1

    if slot is None or out_dir is None:
        print("@@ERR 必须指定 --slot N 和 --out DIR", flush=True)
        return

    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_name = name or ("镜%02d" % slot)
    out_path = os.path.join(out_dir, out_name + ".mp4")

    # 检查是否已下载
    if os.path.exists(out_path) and os.path.getsize(out_path) > MIN_DOWNLOAD_BYTES:
        print("@@SKIP 文件已存在: %s (%dB)" % (out_path, os.path.getsize(out_path)), flush=True)
        return

    log("regrab", "slot=%d 重抓视频链（不重新生成）" % slot)
    try:
        s = S(port_of(slot))

        # 直接抓链（不走发送/确认/等待流程）
        url = _grab_video_url(slot, s)
        if not url:
            print("@@NOURL2 slot=%s 重抓失败" % slot, flush=True)
            return

        sz = _download_video(url, out_path)
        if not sz:
            return

        # 规格核对
        _probe_spec(out_path)
        log("regrab", "slot=%d 完成 %s %dB" % (slot, out_path, sz))
        print("@@DONE slot=%s %s %dB" % (slot, out_path, sz), flush=True)

    except Exception as e:
        print("@@ERR slot=%s 重抓异常: %s" % (slot, str(e)[:100]), flush=True)
        log("regrab", "slot=%d 异常: %s" % (slot, str(e)[:200]))
    finally:
        try:
            s.close()
        except Exception:
            pass


# ══════════════════════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════════════════════

USAGE = """用法:
  python doubao_video.py vid --slot N --image 垫图.png --file 词.txt --out DIR [--name 名]
  python doubao_video.py vid-regrab --slot N --out DIR [--name 名]

十二步固定链路:
  ①探活 ②切视频生成模式 ③上传垫图 ④注入提示词 ⑤发送
  ⑥读确认卡 ⑦防误购保护 ⑧确认生成 ⑨等完成 ⑩抓视频链 ⑪下载 ⑫规格核对(必须有音轨)

防误购保护: 确认卡/弹层出现「专业版/订阅/付费用量/升级/开通会员」任一关键词
          → 立即中止 @@PAID_ABORT，绝不点击升级按钮、绝不确认扣款
静默拒答: 提示词正常发出、豆包零回复、不出确认卡、不报错 → @@NOCARD
重抓: vid-regrab 只抓链+下载，绝不重跑生成（白烧用量）
"""

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(USAGE)
        return
    cmd = sys.argv[1]
    rest = sys.argv[2:]
    if cmd == "vid":
        cmd_vid(rest)
    elif cmd == "vid-regrab":
        cmd_regrab(rest)
    else:
        print("未知命令: %s\n%s" % (cmd, USAGE))


if __name__ == "__main__":
    main()
