#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 Playwright 把 HTML 渲染为 PDF（严格按任务要求，禁用 Chrome headless 命令行）"""
import os
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
HTML = pathlib.Path(os.environ.get("PHTML", HERE / "涨停板龙虎榜深度研判报告-20260911.html"))
PDF = pathlib.Path(os.environ.get("PPDF", HERE / "涨停板龙虎榜深度研判报告-20260911.pdf"))

from playwright.sync_api import sync_playwright

def main() -> int:
    url = HTML.as_uri()
    print(f"[1] 载入页面: {url}")

    with sync_playwright() as p:
        # 优先用 Playwright 自带 chromium，失败则回退系统 Chrome
        browser = None
        try:
            browser = p.chromium.launch(args=["--allow-file-access-from-files"])
            print("[2] 已启动 Playwright 内置 Chromium")
        except Exception as e:
            print(f"[2] 内置 Chromium 不可用 ({e.__class__.__name__})，回退系统 Chrome")
            browser = p.chromium.launch(
                channel="chrome",
                args=["--allow-file-access-from-files"],
            )
            print("[2b] 已启动系统 Google Chrome")

        page = browser.new_page(viewport={"width": 703, "height": 1400})
        # 关键：先切到 print 媒体，让 ECharts 按打印尺寸初始化，
        # 避免画布尺寸与容器错位导致图注被覆盖
        page.emulate_media(media="print")
        page.goto(url, wait_until="load", timeout=120_000)

        # 等待 ECharts 渲染完成标志
        try:
            page.wait_for_function("window.__chartsReady === true", timeout=60_000)
            print("[3] ECharts 渲染完成标志已就绪 (__chartsReady=true)")
        except Exception as e:
            print(f"[3] 等待渲染标志超时: {e}")

        # 强制一次 resize，确保画布与容器尺寸完全一致
        page.evaluate("window.dispatchEvent(new Event('resize'))")
        page.wait_for_timeout(700)

        # 二次确认 canvas 已实际绘制像素
        drawn = page.evaluate(
            """() => {
                const out = [];
                document.querySelectorAll('canvas').forEach((cv, i) => {
                    let ink = 0;
                    try {
                        const ctx = cv.getContext('2d');
                        const d = ctx.getImageData(0, 0, cv.width, cv.height).data;
                        // 采样统计非透明像素
                        for (let k = 3; k < d.length; k += 400) { if (d[k] > 8) ink++; }
                    } catch (e) { ink = -1; }
                    out.push({i, w: cv.width, h: cv.height, ink});
                });
                return out;
            }"""
        )
        print(f"[4] canvas 检测: {drawn}")
        ok_charts = [c for c in drawn if c["ink"] > 0]
        if len(ok_charts) < 3:
            print(f"[!] 警告：仅 {len(ok_charts)} 个 canvas 有绘制内容（期望 3）")

        # 额外等待字体/布局稳定
        page.wait_for_timeout(1200)

        page.pdf(
            path=str(PDF),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        print(f"[5] PDF 已写出: {PDF}")
        browser.close()

    size = PDF.stat().st_size
    print(f"[6] 文件大小: {size/1024:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
