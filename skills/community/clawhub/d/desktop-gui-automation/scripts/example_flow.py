#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
example_flow.py — 业务脚本骨架。

演示如何基于 gui_auto.py 编排一个"每日自动领奖/签到"闭环。
按目标软件改写：WIN_TITLE、模板路径、入口步骤、幂等信号、坐标。

流程范式（务必保留这个顺序，它是稳定闭环的关键）：
  激活窗口 → 关残留弹窗 → 打开入口 → 幂等判断 → 点击 → 二次确认 → 关弹窗 → 写日志
"""
import os
import time
import traceback

import gui_auto as g

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
ASSETS = os.path.join(ROOT, "assets")
LOGS = os.path.join(ROOT, "logs")
LOGMD = os.path.join(ROOT, "checkin-log.md")

WIN_TITLE = "目标软件窗口标题"          # TODO 改成实际标题
TPL_ENTRY = os.path.join(ASSETS, "entry.png")      # TODO 入口按钮模板
TPL_DONE = os.path.join(ASSETS, "done.png")        # TODO "已领取"灰按钮模板
TPL_CLAIM = os.path.join(ASSETS, "claim.png")      # TODO "立即领取"黑按钮模板

CLOSE_X = [(1473, 136)]   # TODO 弹窗关闭按钮候选坐标；无则留空走 Esc


def ensure_window():
    return g.activate_window(WIN_TITLE)


def open_entry():
    """打开功能入口。用模板定位，命中即点。"""
    pt = g.locate(TPL_ENTRY, 0.82)
    if not pt:
        return False
    g.click(pt[0], pt[1], pause=2)
    g.shot("01_opened")
    return True


def run():
    try:
        if not ensure_window():
            g.write_log("未完成：找不到目标窗口", LOGM)
            return
        g.close_dialog(CLOSE_X)
        time.sleep(0.5)

        # 幂等判断：出现"已领取"信号则整体跳过
        if g.locate(TPL_DONE, 0.78):
            g.shot("already_done")
            g.write_log("今日已完成（幂等跳过）", LOGM)
            g.close_dialog(CLOSE_X)
            return

        if not open_entry():
            g.write_log("未完成：未找到入口按钮（界面可能改版）", LOGM)
            return

        # 执行前留证
        g.shot("before")
        btn = g.locate(TPL_CLAIM, 0.78)
        if not btn:
            g.write_log("未完成：未找到领取按钮", LOGM)
            g.close_dialog(CLOSE_X)
            return
        g.click(btn[0], btn[1], pause=2.5)
        g.shot("after")

        # 二次确认：再次检测"已完成"信号
        time.sleep(1)
        ok = g.locate(TPL_DONE, 0.8)
        g.close_dialog(CLOSE_X)
        if ok:
            g.write_log("领取成功：界面已显示「已领取」", LOGM)
        else:
            g.write_log("部分完成：已点击但未能二次确认，请核对 logs/ 截图", LOGM)

    except Exception:
        g.shot("error")
        g.write_log("未完成（脚本异常）：" + traceback.format_exc().replace("\n", " | ")[:400], LOGM)


if __name__ == "__main__":
    run()
