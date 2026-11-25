#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「猫适口性试验记录」示例 xlsx（模拟数据，仅用于试跑/校验格式）。

用法：python assets/generate_sample.py assets/sample_cat_palatability.xlsx
"""
import os
import random
import sys

from openpyxl import Workbook

GROUPS = ["第一组", "第二组", "第三组"]
CATS = ["A01", "A02", "A03"]
MEALS = 5
FEEDING = 40.0
FIRST = ["A料", "B料", "同时采食", "A料", "B料", "无采食"]


def build(path, seed=42):
    rnd = random.Random(seed)
    wb = Workbook()
    ws = wb.active
    ws.title = "原始记录单"

    ws.cell(1, 1, "猫适口性试验记录表（示例数据，非真实实验）")
    ws.cell(2, 1, "单盆给料量(g)")
    ws.cell(2, 2, FEEDING)
    ws.cell(3, 1, "试验编号")
    ws.cell(3, 2, "DEMO-001")

    headers = ["组别", "序号", "猫号"]
    for m in range(1, MEALS + 1):
        headers += [f"第{m}餐余料A", f"第{m}餐余料B", f"第{m}餐首口料"]
    headers.append("备注")
    for c, h in enumerate(headers, start=1):
        ws.cell(4, c, h)

    # 第 6 行：A 料位置（A左/A右），仅每餐 A 列（3/6/9/12/15）有值
    for m in range(MEALS):
        ws.cell(6, 4 + m * 3, "A左" if m % 2 == 0 else "A右")

    row = 8
    seq = 0
    for gi, grp in enumerate(GROUPS):
        ws.cell(row, 1, grp)
        ws.cell(row, 2, f"对比料{gi + 1}：A=样品{gi + 1}，B=对照料")
        row += 1
        seq = 0
        for cat in CATS:
            seq += 1
            ws.cell(row, 1, grp)
            ws.cell(row, 2, seq)
            ws.cell(row, 3, cat)
            for m in range(MEALS):
                a_intake = max(0.0, min(FEEDING, rnd.gauss(24, 6)))
                b_intake = max(0.0, min(FEEDING, rnd.gauss(20, 6)))
                ws.cell(row, 4 + m * 3, round(FEEDING - a_intake, 1))
                ws.cell(row, 5 + m * 3, round(FEEDING - b_intake, 1))
                ws.cell(row, 6 + m * 3, rnd.choice(FIRST))
            row += 1

    # 人为注入脏数据：备注异常 + 余料缺失 + 极端离群
    ws.cell(9, 19, "打翻，待核")
    ws.cell(14, 4).value = None    # 第二组 A02 第1餐 余料A 缺失
    ws.cell(18, 7).value = 0.2     # 第三组 A02 第2餐 余料B 极端值（采食 39.8g）
    ws.cell(19, 19, "呕吐后数据模糊")

    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    wb.save(path)
    print(f"已生成示例：{path}")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "assets/sample_cat_palatability.xlsx")
