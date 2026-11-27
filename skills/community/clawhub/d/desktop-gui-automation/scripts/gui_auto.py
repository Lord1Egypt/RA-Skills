#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gui_auto.py — Windows 桌面 GUI 自动化通用工具库。

提供：截屏、局部放大、窗口枚举/激活、图像模板定位、点击、拖动滚动、
结构化日志。既可 CLI 单独调用做界面勘察，也可被业务脚本 import 复用。

依赖：pip install pyautogui pillow opencv-python-headless

CLI 用法：
  python gui_auto.py shot [--out FILE]
  python gui_auto.py crop <png> x0 y0 x1 y1 [zoom]
  python gui_auto.py windows
  python gui_auto.py activate "窗口标题" [--maximize]
  python gui_auto.py locate <模板.png> [--conf 0.82] [--region x,y,w,h]
  python gui_auto.py click X Y
  python gui_auto.py drag X Y1 Y2 [--sec 1.0]
  python gui_auto.py log "记录内容" [--file checkin-log.md]

作为库：
  import gui_auto as g
  g.activate_window("WorkBuddy")
  pt = g.locate("assets/btn.png", conf=0.82)
  if pt: g.click(pt[0], pt[1])
  g.write_log("领取成功")
"""
import sys
import os
import time
import argparse
from datetime import datetime

import pyautogui
from PIL import Image

pyautogui.FAILSAFE = True   # 鼠标移到左上角可紧急中止
pyautogui.PAUSE = 0.2


def ts_full():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def ts_short():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


# ---------- 截屏与图像 ----------

def grab():
    """截取整个主屏，返回 PIL.Image。会话隔离时会抛 OSError。"""
    from PIL import ImageGrab
    return ImageGrab.grab().convert("RGB")


def shot(name=None, out=None, base="logs"):
    """截屏存盘并返回绝对路径。"""
    path = out
    if not path:
        os.makedirs(base, exist_ok=True)
        path = os.path.join(base, f"{ts_short()}_{name or 'shot'}.png")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    grab().save(path)
    print(f"SHOT {path}")
    return path


def crop(src, x0, y0, x1, y1, zoom=1, out=None):
    """裁局部并放大，返回路径。用于精确读坐标。"""
    im = Image.open(src).convert("RGB")
    box = (int(x0), int(y0), int(x1), int(y1))
    part = im.crop(box)
    if zoom and zoom != 1:
        part = part.resize((part.width * int(zoom), part.height * int(zoom)))
    if not out:
        root, ext = os.path.splitext(src)
        out = f"{root}_crop{ext}"
    part.save(out)
    print(f"CROP {out} src_box={box} zoom={zoom}")
    return out


def orig_from_crop(crop_x, crop_y, x0, y0, zoom):
    """把放大图上的点换算回原始屏幕坐标。"""
    return int(x0) + int(crop_x) / float(zoom), int(y0) + int(crop_y) / float(zoom)


# ---------- 窗口 ----------

def list_windows():
    """返回 [(title, left, top, width, height, is_active)]。"""
    out = []
    for w in pyautogui.getAllWindows():
        title = (w.title or "").strip()
        if title:
            out.append((title, w.left, w.top, w.width, w.height, w.isActive))
    return out


def activate_window(title, maximize=True, exact=True):
    """按标题激活窗口，返回是否成功。"""
    wins = list_windows()
    cand = [w for w in wins if (w[0] == title if exact else title in w[0])]
    if not cand:
        cand = [w for w in wins if title in w[0]]
    if not cand:
        print(f"ERR window not found: {title}")
        return False
    t, l, tp, wd, ht, _ = cand[0]
    try:
        target = next(x for x in pyautogui.getAllWindows() if (x.title or "").strip() == t)
        if maximize and not target.isMaximized:
            target.maximize()
            time.sleep(1)
        if target.isMinimized:
            target.restore()
        target.activate()
    except Exception as e:
        print(f"WARN activate: {e}")
    time.sleep(0.5)
    return True


# ---------- 定位与操作 ----------

def locate(tpl_path, conf=0.82, region=None):
    """模板匹配，命中返回 (cx, cy)，未找到返回 None。空结果/异常统一吞掉。"""
    if not os.path.exists(tpl_path):
        print(f"ERR template missing: {tpl_path}")
        return None
    try:
        r = pyautogui.locateOnScreen(tpl_path, confidence=conf, region=region)
        if not r:
            return None
        c = pyautogui.center(r)
        return (int(c.x), int(c.y))
    except Exception:
        return None


def click(x, y, pause=1.0):
    pyautogui.click(int(x), int(y))
    time.sleep(pause)


def drag(x, y1, y2, sec=1.0):
    """在固定 x 上从 y1 拖到 y2，常用于滚动条。"""
    pyautogui.moveTo(int(x), int(y1))
    time.sleep(0.3)
    pyautogui.dragTo(int(x), int(y2), duration=sec, button="left")
    time.sleep(1.0)


def scroll(x, y, clicks=-4, times=1):
    pyautogui.moveTo(int(x), int(y))
    for _ in range(times):
        pyautogui.scroll(clicks)
        time.sleep(0.15)
    time.sleep(0.8)


def close_dialog(candidates=None, esc=True):
    """尝试关闭弹窗：按候选坐标点 X，再按 Esc。按实际软件调整坐标。"""
    for (x, y) in (candidates or []):
        try:
            pyautogui.click(x, y)
            time.sleep(0.4)
        except Exception:
            pass
    if esc:
        pyautogui.press("esc")
        time.sleep(0.4)


# ---------- 日志 ----------

def write_log(line, path="checkin-log.md"):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{ts_full()} {line}\n")
    print("LOG", line[:160])


# ---------- CLI ----------

def main():
    p = argparse.ArgumentParser(description="Windows 桌面 GUI 自动化工具")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("shot"); s.add_argument("--out"); s.add_argument("--base", default="logs")
    s = sub.add_parser("crop")
    for a in ("src", "x0", "y0", "x1", "y1"): s.add_argument(a)
    s.add_argument("zoom", nargs="?", type=int, default=2); s.add_argument("--out")
    sub.add_parser("windows")
    s = sub.add_parser("activate"); s.add_argument("title"); s.add_argument("--no-max", action="store_true")
    s = sub.add_parser("locate"); s.add_argument("tpl"); s.add_argument("--conf", type=float, default=0.82); s.add_argument("--region")
    s = sub.add_parser("click"); s.add_argument("x", type=int); s.add_argument("y", type=int)
    s = sub.add_parser("drag"); s.add_argument("x", type=int); s.add_argument("y1", type=int); s.add_argument("y2", type=int); s.add_argument("--sec", type=float, default=1.0)
    s = sub.add_parser("log"); s.add_argument("text"); s.add_argument("--file", default="checkin-log.md")

    a = p.parse_args()
    if a.cmd == "shot":
        shot(out=a.out, base=a.base)
    elif a.cmd == "crop":
        crop(a.src, a.x0, a.y0, a.x1, a.y1, a.zoom, a.out)
    elif a.cmd == "windows":
        for w in list_windows():
            print(f"{w[0]!r}  pos=({w[1]},{w[2]}) size=({w[3]}x{w[4]}) {'ACTIVE' if w[5] else ''}")
    elif a.cmd == "activate":
        ok = activate_window(a.title, maximize=not a.no_max)
        print("OK" if ok else "FAILED")
    elif a.cmd == "locate":
        region = None
        if a.region:
            region = tuple(int(v) for v in a.region.split(","))
        pt = locate(a.tpl, a.conf, region)
        print(f"LOCATE {'%d,%d' % pt if pt else 'NOT FOUND'}")
    elif a.cmd == "click":
        click(a.x, a.y)
        print(f"CLICK {a.x},{a.y}")
    elif a.cmd == "drag":
        drag(a.x, a.y1, a.y2, a.sec)
        print("DRAG done")
    elif a.cmd == "log":
        write_log(a.text, a.file)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
