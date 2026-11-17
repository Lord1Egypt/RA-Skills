# -*- coding: utf-8 -*-
"""doubao_login.py — 豆包扫码登录全流程
开登录弹窗 → 定位二维码 → 裁切放大（PIL）→ 检测过期 → 返回 @@QR 路径
另含 check（三重校验）和 nick（读昵称）。
Python 3.9+ 兼容，中文注释，UTF-8。
"""
import json
import os
import sys
import time
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doubao_core import cfg, home, out_dir, port_of, S, log

# ---------------------------------------------------------------------------
# JS 片段
# ---------------------------------------------------------------------------
CLICK_LOGIN = """(() => {
  const all = [...document.querySelectorAll('button,a,div,span,li,p')];
  const hit = all.filter(e => (e.innerText||'').trim() === '登录');
  if (!hit.length) return 'NO_LOGIN_BTN';
  hit[hit.length-1].click();
  return 'CLICKED';
})()"""

CLICK_REFRESH = """(() => {
  const all = [...document.querySelectorAll('button,a,div,span,li,p')];
  const hit = all.filter(e => {
    const t = (e.innerText||'').trim();
    return t === '点击刷新' || t === '刷新';
  });
  if (!hit.length) return 'NO_REFRESH';
  hit[hit.length-1].click();
  return 'REFRESHED';
})()"""

FIND_QR = """(() => {
  const out = [];
  document.querySelectorAll('img,canvas,svg').forEach(e => {
    const r = e.getBoundingClientRect();
    if (r.width < 110 || r.height < 110) return;
    if (Math.abs(r.width - r.height) > r.width * 0.18) return;
    if (r.width > 460) return;
    const src = (e.getAttribute('src') || '') + '|' + (e.tagName);
    out.push({tag: e.tagName, x: Math.round(r.x), y: Math.round(r.y),
              w: Math.round(r.width), h: Math.round(r.height),
              src: src.slice(0, 40)});
  });
  return JSON.stringify(out);
})()"""

CHECK_EXPIRED = """(() => {
  const t = document.body.innerText || '';
  return /二维码已过期|二维码失效|请刷新/.test(t) ? 'EXPIRED' : 'OK';
})()"""

# 三重校验 JS
CHECK_LOGIN_JS = r"""(() => {
  const t = document.body.innerText || '';
  const hasLoginBtn = [...document.querySelectorAll('button,a,div,span')]
      .some(e => (e.innerText||'').trim() === '登录');
  const noLoginParam = location.href.indexOf('login') < 0;
  // 找历史会话入口
  const hasHistory = [...document.querySelectorAll('button,a,div,span')]
      .some(e => (e.innerText||'').trim().length > 0 &&
           e.getBoundingClientRect().left < 200 &&
           e.getBoundingClientRect().top > 100);
  return JSON.stringify({hasLoginBtn, noLoginParam, hasHistory, url: location.href.slice(0,80)});
})()"""

NICK_JS = r"""(() => {
  for (const e of document.querySelectorAll('*')) {
    const t = (e.innerText || '').trim();
    if (!t || t.length > 20) continue;
    const r = e.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) continue;
    if (r.left >= 55 && r.left <= 70 && r.top > 380) {
      if (e.children.length > 1) continue;
      return t;
    }
  }
  return '';
})()"""


def _qr_zoom(s: S, n: int, out_path: str = None) -> str | None:
    """定位二维码元素 → 全屏截图 → 裁切放大 → 落盘。返回路径。"""
    cands = []
    for attempt in range(4):
        info = s.ev(FIND_QR, 1.0)
        try:
            cands = json.loads(info) if info else []
        except Exception:
            cands = []
        if cands:
            break
        s.ev(CLICK_REFRESH, 2.0)
        time.sleep(2.5)

    if not cands:
        print('@@NORECT 未找到二维码元素')
        return None

    # 取面积最大的
    c = sorted(cands, key=lambda z: -z['w'] * z['h'])[0]

    # DPR
    try:
        dpr = float(s.ev('window.devicePixelRatio', 0.3))
    except Exception:
        dpr = 1.0

    # 全屏截图
    sh = s.send('Page.captureScreenshot', {'format': 'png'})
    data = sh.get('result', {}).get('data')
    if not data:
        print('@@ERR 截图失败')
        return None

    from PIL import Image
    import io
    im = Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB')

    # 裁切
    pad = int(14 * dpr)
    box = (
        max(0, int(c['x'] * dpr) - pad),
        max(0, int(c['y'] * dpr) - pad),
        min(im.width, int((c['x'] + c['w']) * dpr) + pad),
        min(im.height, int((c['y'] + c['h']) * dpr) + pad),
    )
    crop = im.crop(box)

    # 放大到至少 1000px
    k = max(1, int(1000 / max(crop.width, crop.height)))
    if k > 1:
        crop = crop.resize((crop.width * k, crop.height * k), Image.LANCZOS)

    # 落盘
    if not out_path:
        out_path = os.path.join(out_dir(), f'doubao_qr_{n}_zoom.png')
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    crop.save(out_path)
    print(f'@@QR {out_path} {os.path.getsize(out_path)} {crop.size}')
    return out_path


def cmd_login(args):
    """扫码登录全流程：开弹窗 → 找码 → 裁切放大。"""
    n = int(args.slot)
    out_path = getattr(args, 'out', None)
    try:
        s = S(port_of(n))
        s.send('Page.navigate', {'url': 'https://www.doubao.com/chat/'})
        t = s.ready()
        log(f'slot={n} ready in {t}s')
        time.sleep(1.0)

        # 点登录按钮
        r = s.ev(CLICK_LOGIN, 2.5)
        log(f'click_login={r}')
        time.sleep(2.5)

        # 检测是否过期
        state = s.ev(CHECK_EXPIRED, 1.0)
        if state == 'EXPIRED':
            s.ev(CLICK_REFRESH, 2.0)
            time.sleep(2.5)

        # 裁切放大二维码
        result = _qr_zoom(s, n, out_path)
        if not result:
            print('@@ERR 二维码获取失败')

        s.close()
    except Exception as e:
        print(f'@@ERR slot={n} {str(e)[:200]}')


def check(n: int) -> str:
    """登录态三重校验：URL无login参数 + 页面无「立即登录/登录注册」 + 有历史会话入口。"""
    from doubao_core import alive
    if not alive(n):
        return 'ALIVE=NO'
    try:
        s = S(port_of(n))
        r = s.ev(CHECK_LOGIN_JS, 4.0)
        s.close()
        data = json.loads(r)
        if data.get('hasLoginBtn'):
            return 'LOGGED=NO'
        if data.get('noLoginParam'):
            return 'LOGGED=YES'
        return 'LOGGED=UNKNOWN'
    except Exception as e:
        return f'ERR {str(e)[:120]}'


def read_nick(n: int) -> str | None:
    """读取实例昵称。"""
    from doubao_core import alive
    if not alive(n):
        return None
    try:
        s = S(port_of(n))
        r = s.ev(NICK_JS, 6.0)
        s.close()
        return r.strip() if r and r.strip() else None
    except Exception:
        return None
