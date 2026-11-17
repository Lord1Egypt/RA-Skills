#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""report_pdf.py —— 图表化 PDF 报告生成（纯标准库，中文可嵌入，含图表）

输入：一份 JSON spec（结构见 references/report-spec.md）
  blocks 支持：h1 / h2 / p / bullets / kv / bar / line / pie / funnel / waterfall /
                table / checklist / callout / spacer

用法：
  python report_pdf.py --self-test
  python report_pdf.py --demo --out ./报告.pdf
  python report_pdf.py --spec report.json --out ./报告.pdf [--font C:/Windows/Fonts/simhei.ttf]
退出码：0 成功；2 输入错误。
"""

import argparse
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_core import PDF, PALETTE  # noqa: E402

MARGIN = 48.0
BOTTOM = 56.0


def _tmp_dir():
    """临时目录优先级：环境变量 ECOMMERCE_OPS_TMP → 非系统盘候选 → 系统临时目录。

    默认尽量不写系统盘（避免占用 C 盘空间）；开源用户可用环境变量指向任意位置，
    找不到非系统盘时自动回退到系统临时目录，保证可移植。
    """
    env = os.environ.get("ECOMMERCE_OPS_TMP")
    if env:
        os.makedirs(env, exist_ok=True)
        return env
    # 非系统盘候选（Windows 常见的数据盘；不存在则忽略）
    for p in ("F:/workbuddy/_tmp", "F:/_tmp", "D:/_tmp"):
        if os.path.isdir(os.path.dirname(p)) or os.path.isdir(p):
            try:
                os.makedirs(p, exist_ok=True)
                return p
            except OSError:
                continue
    d = os.path.join(tempfile.gettempdir(), "ecom_pdf")
    os.makedirs(d, exist_ok=True)
    return d


class Renderer:
    def __init__(self, doc):
        self.d = doc
        self.y = MARGIN
        self.page_no = 0
        self.new_page(first=True)

    def new_page(self, first=False):
        self.d.new_page()
        self.page_no += 1
        self.y = MARGIN
        if not first:
            self.y = MARGIN

    def footer(self):
        self.d.add_text("第 %d 页" % self.page_no, self.d.W - MARGIN - 46, self.d.H - 34, 8.5, PALETTE["muted"])

    def need(self, h):
        if self.y + h > self.d.H - BOTTOM:
            self.footer()
            self.new_page()
            return True
        return False

    # ---------- blocks ----------
    def h1(self, b):
        self.need(40)
        self.d.add_text(b["text"], MARGIN, self.y, 17, PALETTE["ink"], bold=True)
        self.y += 24
        self.d.line(MARGIN, self.y - 4, self.d.W - MARGIN, self.y - 4, PALETTE["brand"], lw=1.2)
        self.y += 12

    def h2(self, b):
        self.need(32)
        self.d.add_text(b["text"], MARGIN, self.y, 13, PALETTE["brand"], bold=True)
        self.y += 22

    def p(self, b):
        size = b.get("size", 10.5)
        for ln in self.d.wrap(b["text"], size, self.d.W - 2 * MARGIN):
            self.need(size + 6)
            self.d.add_text(ln, MARGIN, self.y, size, PALETTE["muted"] if b.get("muted") else PALETTE["ink"])
            self.y += size + 4.5
        self.y += 4

    def bullets(self, b):
        size = b.get("size", 10.5)
        for it in b["items"]:
            lines = self.d.wrap(str(it), size, self.d.W - 2 * MARGIN - 16)
            for j, ln in enumerate(lines):
                self.need(size + 6)
                if j == 0:
                    self.d.add_text("·", MARGIN + 2, self.y, size, PALETTE["brand"])
                self.d.add_text(ln, MARGIN + 14, self.y, size, PALETTE["ink"])
                self.y += size + 4
        self.y += 4

    def kv(self, b):
        items = [(k, v) for k, v in b["items"]]
        h = self.d.kv_cards(MARGIN, self.y, self.d.W - 2 * MARGIN, items,
                            per_row=b.get("per_row", 3), h=b.get("h", 52))
        self.y += h + 6

    def callout(self, b):
        size = 10.5
        lines = self.d.wrap(b["text"], size, self.d.W - 2 * MARGIN - 24)
        h = 14 + len(lines) * (size + 4)
        self.need(h + 8)
        tone = b.get("tone", "warn")
        fill = (0.99, 0.94, 0.90) if tone == "warn" else ((0.93, 0.97, 0.95) if tone == "ok" else (0.94, 0.96, 0.99))
        edge = PALETTE["warn"] if tone == "warn" else (PALETTE["brand2"] if tone == "ok" else PALETTE["brand"])
        self.d.rect(MARGIN, self.y, self.d.W - 2 * MARGIN, h, fill=fill, radius=3)
        self.d.rect(MARGIN, self.y, 3.5, h, fill=edge)
        yy = self.y + 8
        for ln in lines:
            self.d.add_text(ln, MARGIN + 14, yy, size, PALETTE["ink"])
            yy += size + 4
        self.y += h + 10

    def bar(self, b):
        h = b.get("h", 170)
        self.need(h + 10)
        colors = None
        if b.get("colors"):
            colors = [PALETTE.get(c, PALETTE["brand"]) for c in b["colors"]]
        self.d.bar_chart(MARGIN, self.y, self.d.W - 2 * MARGIN, h, b.get("title", ""),
                         b["labels"], [float(v) for v in b["values"]], b.get("unit", ""), colors)
        self.y += h + 10

    def line(self, b):
        h = b.get("h", 180)
        self.need(h + 10)
        series = [{"name": s.get("name", ""), "values": [float(v) for v in s["values"]]} for s in b["series"]]
        self.d.line_chart(MARGIN, self.y, self.d.W - 2 * MARGIN, h, b.get("title", ""), b["labels"], series,
                          b.get("unit", ""))
        self.y += h + 10

    def pie(self, b):
        s = b.get("size", 150)
        self.need(s + 10)
        self.d.pie_chart(MARGIN, self.y, s, b.get("title", ""), b["labels"], [float(v) for v in b["values"]])
        self.y += s + 14

    def funnel(self, b):
        """漏斗图：labels 为环节名，values 为该环节绝对量（首端最大）。"""
        h = b.get("h", 190)
        self.need(h + 10)
        self.d.funnel_chart(MARGIN, self.y, self.d.W - 2 * MARGIN, h, b.get("title", ""),
                            b["labels"], [float(v) for v in b["values"]], b.get("unit", ""))
        self.y += h + 10

    def waterfall(self, b):
        """瀑布图：labels 为级名，values 为该级增减量（正=增加、负=扣减）。"""
        h = b.get("h", 180)
        self.need(h + 10)
        self.d.waterfall_chart(MARGIN, self.y, self.d.W - 2 * MARGIN, h, b.get("title", ""),
                               b["labels"], [float(v) for v in b["values"]], b.get("unit", ""))
        self.y += h + 10

    def table(self, b):
        w = self.d.W - 2 * MARGIN
        self.need(60)
        h = self.d.table(MARGIN, self.y, w, b["header"], b["rows"], b.get("widths"),
                         b.get("size", 9))
        self.y += h + 12

    def checklist(self, b):
        size = 10.5
        for it in b["items"]:
            ok = it.get("ok", True) if isinstance(it, dict) else True
            txt = it.get("text") if isinstance(it, dict) else str(it)
            lines = self.d.wrap(txt, size, self.d.W - 2 * MARGIN - 22)
            for j, ln in enumerate(lines):
                self.need(size + 6)
                if j == 0:
                    self.d.add_text("√" if ok else "×", MARGIN + 2, self.y, size,
                                    PALETTE["brand2"] if ok else PALETTE["up"])
                self.d.add_text(ln, MARGIN + 18, self.y, size, PALETTE["ink"])
                self.y += size + 4
        self.y += 6

    def spacer(self, b):
        self.y += b.get("h", 12)

    def run(self, spec):
        self.d.add_text(spec.get("title", "报告"), MARGIN, self.y, 20, PALETTE["ink"], bold=True)
        self.y += 30
        sub = spec.get("subtitle")
        if sub:
            self.d.add_text(sub, MARGIN, self.y, 11, PALETTE["muted"])
            self.y += 20
        meta = spec.get("meta") or {}
        if meta:
            self.d.add_text("  |  ".join("%s：%s" % (k, v) for k, v in meta.items()), MARGIN, self.y, 9, PALETTE["muted"])
            self.y += 14
        self.d.line(MARGIN, self.y, self.d.W - MARGIN, self.y, PALETTE["brand"], lw=1.4)
        self.y += 18
        handlers = {"h1": self.h1, "h2": self.h2, "p": self.p, "bullets": self.bullets, "kv": self.kv,
                    "callout": self.callout, "bar": self.bar, "line": self.line, "pie": self.pie,
                    "funnel": self.funnel, "waterfall": self.waterfall,
                    "table": self.table, "checklist": self.checklist, "spacer": self.spacer}
        for b in spec.get("blocks", []):
            fn = handlers.get(b.get("type"))
            if fn:
                fn(b)
        self.footer()


DEMO_SPEC = {
    "title": "选品与投放决策报告（示例）",
    "subtitle": "SKU：便携榨汁杯 500ml ｜ 平台：抖音小店 ｜ 数据区间：2026-08-01 ~ 2026-08-31",
    "meta": {"生成时间": "2026-09-27", "数据来源": "抖音电商罗盘 + 巨量千川", "口径": "支付买家数"},
    "blocks": [
        {"type": "h1", "text": "一、结论先行"},
        {"type": "callout", "tone": "ok", "text": "建议上架，但首月投放必须控制 CPC ≤ 1.62 元：保本 ROI 为 1.85，当前实测 ROI 3.25，安全垫约 75%。"},
        {"type": "kv", "per_row": 3, "items": [["毛利率 g", "54.0%"], ["保本 ROI", "1.85"], ["实测 ROI", "3.25"],
                                               ["最高可承受 CPC", "1.62 元"], ["最高可承受 CPM", "32.4 元"], ["净利率", "22.0%"]]},
        {"type": "h1", "text": "二、成本结构与利润"},
        {"type": "bar", "title": "单件成本构成（元）", "labels": ["商品成本", "履约", "佣金", "退货损失", "广告", "净利"],
         "values": [38.0, 6.5, 6.45, 1.6, 18.0, 28.4], "unit": ""},
        {"type": "pie", "title": "成本占比", "labels": ["商品成本", "履约物流", "佣金", "退货损失", "广告投放"],
         "values": [38.0, 6.5, 6.45, 1.6, 18.0]},
        {"type": "h1", "text": "三、投放趋势"},
        {"type": "line", "title": "近 6 周 ROI 与 CPC 走势", "labels": ["W1", "W2", "W3", "W4", "W5", "W6"],
         "series": [{"name": "ROI", "values": [2.1, 2.4, 2.9, 3.1, 3.25, 3.4]},
                    {"name": "CPC(元)", "values": [1.9, 1.8, 1.7, 1.65, 1.6, 1.55]}]},
        {"type": "h1", "text": "四、转化漏斗与利润拆解"},
        {"type": "funnel", "title": "全链路转化漏斗（支付买家数口径）", "unit": "",
         "labels": ["曝光", "点击", "访问", "下单", "支付"],
         "values": [182000, 7280, 6550, 1048, 936]},
        {"type": "waterfall", "title": "单件利润逐级拆解（元）",
         "labels": ["售价", "商品成本", "履约物流", "佣金", "退货损失", "广告投放"],
         "values": [129.0, -38.0, -6.5, -6.45, -1.6, -18.0]},
        {"type": "h1", "text": "五、风险与下一步"},
        {"type": "table", "header": ["风险项", "等级", "动作"],
         "rows": [["退货率高于类目均值", "P1", "补充实物视频与尺码说明"],
                  ["达人坑位费与佣金可能重复计", "P1", "核对结算单等效佣金率"],
                  ["标题含极限词「最佳」", "P0", "改为「更合适」后方可上架"]]},
        {"type": "checklist", "items": [{"ok": True, "text": "利润模型已用真实结算数据校验"},
                                        {"ok": True, "text": "ROI 采用千川单一来源口径"},
                                        {"ok": False, "text": "文案违禁词未清零，需整改后上架"}]},
    ],
}


def build(spec, out_path, font_path=None):
    doc = PDF(font_path=font_path)
    r = Renderer(doc)
    r.run(spec)
    info = doc.save(out_path, title=spec.get("title", "报告"), meta=spec.get("meta") or {})
    info["page_no_rendered"] = r.page_no
    return info


def self_test() -> int:
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok = ok and cond
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    out = os.path.join(_tmp_dir(), "_report_pdf_selftest.pdf")
    try:
        info = build(DEMO_SPEC, out)
    except Exception as e:
        print("  [FAIL] 生成 PDF 抛异常：%r" % e)
        return 1
    chk("PDF 文件已生成", os.path.exists(out))
    chk("体积 > 5KB（中文字体已嵌入）", info["bytes"] > 5000)
    chk("页数 >= 1", info["pages"] >= 1)
    chk("图表数 >= 3", info["charts"] >= 3)
    chk("表格数 >= 1", info["tables"] >= 1)
    try:
        os.remove(out)
    except OSError:
        pass
    print("report_pdf self-test: %s" % ("ALL PASS" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="图表化 PDF 报告生成")
    ap.add_argument("--spec", help="报告 spec JSON")
    ap.add_argument("--demo", action="store_true", help="生成内置示例报告")
    ap.add_argument("--out", help="输出 PDF 路径")
    ap.add_argument("--font", help="指定中文字体 ttf/ttc")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if not a.out:
        ap.error("需要 --out")
    if a.demo:
        spec = DEMO_SPEC
    elif a.spec:
        with open(a.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    else:
        ap.error("需要 --spec 或 --demo")
        return 2
    info = build(spec, a.out, a.font)
    print(json.dumps(info, ensure_ascii=False, indent=2) if a.json
          else "PDF 已生成：%s（%d 页 / %.1f KB / 图表 %d / 表格 %d）"
          % (info["path"], info["pages"], info["bytes"] / 1024, info["charts"], info["tables"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
