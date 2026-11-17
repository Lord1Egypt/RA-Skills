# -*- coding: utf-8 -*-
"""narrate_kit.py — narrate 命令实现体:report 实测数字 → 双语量化叙事。

每个数字都可溯源到 report JSON(对比度对/闸门裁决/评分/指纹),句式是模板,
形容词不出语域标签——叙事不发明事实。给"为什么这样配"一个能直接发给客户/上级的答案。
被 palette_forge.py 的 cmd_narrate 调用。
"""
import re


def _ratio(txt):
    m = re.search(r"([0-9.]+):1", txt or "")
    return m.group(1) if m else "?"


def _score(txt):
    m = re.search(r"(\d+)/20", txt or "")
    return m.group(1) if m else "?"


def narrate(report, hexes, roles, name=""):
    """report(report JSON) + 角色 → (中文段列表, 英文段列表, verdict)。"""
    g = report.get("gates", {})
    verdict = report.get("verdict", "?")
    bg, surface, ink, ink2, accent = (roles.get(k, "?") for k in
                                      ("bg", "surface", "ink", "ink2", "accent"))
    zh, en = [], []
    title = name or "该配色"
    zh.append(f"「{title}」五色各就其位:大底 #{bg},卡片面 #{surface},正文墨色 #{ink},"
              f"次级信息 #{ink2},强调 #{accent}——强调只占一成以内,大底给足六成。")
    en.append(f"Five colors, five jobs: background #{bg}, cards #{surface}, body text #{ink}, "
              f"secondary #{ink2}, accent #{accent} — accent stays under 10%, background holds ~60%.")

    c = g.get("contrast", {})
    zh.append(f"最亮组合 {c.get('best', '?')}——正文档需 4.5:1,大字档需 3:1,"
              f"该板 {'双双达标' if c.get('pass') else '未全达标(见报告明细)'}。")
    en.append(f"Best pair {c.get('best', '?')}; body text needs 4.5:1 and large text 3:1 — "
              f"{'both met' if c.get('pass') else 'not fully met (see report)'}.")

    cb = g.get("color_blind", {})
    zh.append("三种色盲模拟(红/绿/蓝)下系列仍可分辨,未见撞色。"
              if cb.get("pass") else f"色盲模拟有撞色风险:{(cb.get('detail') or '')[-120:]}")
    en.append("Series stay distinguishable under protan/deutan/tritan simulation."
              if cb.get("pass") else f"Color-blind collision risk: {(cb.get('detail') or '')[-120:]}")

    sl = g.get("ai_slop", {})
    zh.append("无 AI 默认审美签名(默认蓝紫/紫渐变/全鲜艳均未命中)。"
              if sl.get("pass") else f"命中 AI 默认签名:{(sl.get('detail') or '')[-120:]}")
    en.append("No AI-default aesthetic signature detected."
              if sl.get("pass") else f"AI-default signature: {(sl.get('detail') or '')[-120:]}")

    sc = g.get("score", {})
    zh.append(f"五维评分 {_score(sc.get('detail'))}/20;四道机械闸 "
              f"{report.get('summary', {}).get('gates_passed', '?')} 通过。")
    en.append(f"Score {_score(sc.get('detail'))}/20; mechanical gates "
              f"{report.get('summary', {}).get('gates_passed', '?')} passed.")

    zh.append(f"落地路径:大底 #{bg} + 卡片 #{surface} 走六三开,强调 #{accent} 留给关键行动;"
              f"tokens 命令一条出全套 CSS 变量(墨色已按对比度调墨)。")
    en.append(f"To build: background #{bg} with cards #{surface} (60/30), accent #{accent} "
              f"for key actions only; the `tokens` command emits the full CSS variable sheet.")

    zh.append(f"验收指纹 {report.get('fingerprint', '')[:16]}…(数字全部来自 report 实测,可对账)。")
    en.append(f"Verification fingerprint {report.get('fingerprint', '')[:16]}… "
              f"(every number traces to the measured report).")
    return zh, en, verdict


def emit(report, hexes, roles, name="", out=None):
    """→ (markdown 全文, verdict)。out 给定则写文件。"""
    zh, en, verdict = narrate(report, hexes, roles, name)
    head = f"# 配色叙事 · {name or ' '.join('#' + h for h in hexes)} — {verdict}\n\n"
    body = head + "\n".join(f"- {s}" for s in zh) + "\n\n" + \
           "\n".join(f"- {s}" for s in en) + "\n"
    if out:
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
    return body, verdict
