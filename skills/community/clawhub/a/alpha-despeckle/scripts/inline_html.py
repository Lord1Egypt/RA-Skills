#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""inline_html.py —— 把目检 HTML 里的相对路径图片内联成单文件。

⛔ 为什么需要它：skill 生成的目检页（探测/聚类/闪烁/结果）都用
   `<img src='相对目录/x.png'>` 引用本地图片。把这种 HTML 单独发给别人
   （或推给用户预览）时，图片**一张都不会跟过去**，对方看到的是空壳。
   实测：推 42KB 的「半岛闪烁风险.html」→ 用户反馈「没推给我啊」。

用法：
    python inline_html.py 半岛闪烁风险.html
    python inline_html.py 半岛闪烁风险.html --quality 72

输出：<原名>_单文件.html（图片转 JPEG 内联，白底铺底避免透明变黑）
"""
import argparse, base64, io, pathlib, re, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html", help="要内联的 HTML（图片路径相对该文件所在目录）")
    ap.add_argument("--quality", type=int, default=72, help="JPEG 质量，默认 72")
    ap.add_argument("--out", default=None, help="输出文件名，默认 <原名>_单文件.html")
    a = ap.parse_args()

    src = pathlib.Path(a.html)
    t = src.read_text(encoding="utf-8")
    refs = re.findall(r"src='([^']+)'", t)
    # 兼容双引号写法
    refs += [m for m in re.findall(r'src="([^"]+)"', t) if m not in refs]

    cache, ok, miss = {}, 0, []
    def encode(rel):
        nonlocal ok
        if rel in cache:
            return cache[rel]
        f = src.parent / rel
        if not f.exists() or rel.startswith("data:"):
            miss.append(rel)
            return None
        try:
            from PIL import Image
            buf = io.BytesIO()
            Image.open(f).convert("RGB").save(buf, "JPEG", quality=a.quality, optimize=True)
            data = buf.getvalue()
        except Exception:
            data = f.read_bytes()                      # 非图片 → 原样内联
        b = f"data:image/{'jpeg' if data[:2] == b'\xff\xd8' else 'png'};base64," + base64.b64encode(data).decode()
        cache[rel] = b
        ok += 1
        return b

    def repl_sq(m):
        b = encode(m.group(1))
        return f"src='{b}'" if b else m.group(0)
    def repl_dq(m):
        b = encode(m.group(1))
        return f'src="{b}"' if b else m.group(0)

    t = re.sub(r"src='([^']+)'", repl_sq, t)
    t = re.sub(r'src="([^"]+)"', repl_dq, t)

    out = pathlib.Path(a.out) if a.out else src.with_name(src.stem + "_单文件.html")
    out.write_text(t, encoding="utf-8")
    print(f"内联 {ok} 张 / 缺失 {len(miss)} 张")
    if miss:
        print("缺失（已保留原路径）：")
        for m in miss[:10]:
            print("  ", m)
    print(f"输出：{out}  {out.stat().st_size/1024/1024:.1f} MB")

if __name__ == "__main__":
    main()
