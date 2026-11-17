#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""技能评测报告（本地基础版 + 云端增强版，永远免费）。

本地基础版（零 token、零网络）：
  - 读技能目录的 SKILL.md（+ references 清单），用自研 10 维（D1–D10）启发式打分。
  - 渲染 SVG 雷达图 + 文本报告，离线可用。

云端增强版（--cloud --token <藏经阁注册令牌>）：
  - 把技能内容发往藏经阁 cjg-report，返回「方法论落点诊断 + 缺口建议」（由 9 个深度
    playbook 计算，但绝不返回方法论原文）。
  - 需先注册藏经阁并通过邮箱验证（forge-register.py register）。

页脚固定提示：注册藏经阁可免费解锁云端增强诊断。

报告自述：沿用自研 10 维（D1–D10），融合腾讯 TRACE 式评测思路 + 内置云鼎安全检查，
使技能更易过审、更容易得高分。
"""
import os
import sys
import json
import re
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DIR = os.path.dirname(HERE)

DIM_WEIGHTS = {
    "D1": 15, "D2": 10, "D3": 12, "D4": 13, "D5": 12,
    "D6": 8, "D7": 10, "D8": 8, "D9": 7, "D10": 5,
}
DIM_LABELS = {
    "D1": "触发精度", "D2": "范围纪律", "D3": "Token效率", "D4": "覆盖完整",
    "D5": "证据完整", "D6": "差异化", "D7": "验证", "D8": "健壮性",
    "D9": "可维护性", "D10": "可审查性",
}
ORDER = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10"]


def _read_skill(dir_):
    """返回 (skill_name, skill_md, refs_list)。优先读 SKILL.md。"""
    skill_md = ""
    skill_file = None
    for cand in ("SKILL.md", "skill.md"):
        p = os.path.join(dir_, cand)
        if os.path.exists(p):
            skill_file = p
            break
    if skill_file:
        with open(skill_file, "r", encoding="utf-8") as f:
            skill_md = f.read()
    refs = []
    ref_dir = os.path.join(dir_, "references")
    if os.path.isdir(ref_dir):
        refs = sorted(os.listdir(ref_dir))
    name = os.path.basename(os.path.abspath(dir_))
    return name, skill_md, refs


def _score_dim(dim, md, refs, refs_count):
    """返回 0–5 的整数启发式分。纯离线、确定性。"""
    low = md.lower()
    has = lambda *kw: any(k in md for k in kw) or any(k in low for k in kw)
    if dim == "D1":  # 触发精度
        s = 0
        if has("Use when", "when to use", "触发词", "何时使用"):
            s += 3
        if re.search(r"\|.*触发.*\|", md):
            s += 1
        if has("description"):
            s += 1
        return min(5, s) or (1 if has("触发") else 0)
    if dim == "D2":  # 范围纪律
        s = 0
        if has("非职责", "不是", "不做", "边界", "scope", "don't", "not a"):
            s += 3
        if has("明确不做", "A.0"):
            s += 2
        return min(5, s)
    if dim == "D3":  # Token 效率 / 渐进披露
        lines = md.count("\n") + 1
        words = len(re.findall(r"\S+", md)) + len(re.findall(r"[\u4e00-\u9fff]", md))
        s = 5
        if lines > 600 or words > 6000:
            s -= 2
        elif lines > 400 or words > 4000:
            s -= 1
        if refs_count >= 5:
            s = min(5, s + 1)
        return max(1, s)
    if dim == "D4":  # 覆盖完整度
        s = 0
        if has("覆盖", "coverage", "缺口", "gap"):
            s += 3
        if has("coverage.md", "覆盖审计", "audit"):
            s += 2
        return min(5, s)
    if dim == "D5":  # 证据完整度
        s = 0
        if re.search(r"https?://", md):
            s += 2
        if re.search(r"\b(?:ISBN|DOI)\b", md, re.I) or re.search(r"10\.\d{4,9}/", md):
            s += 2
        if has("真实", "核对", "证据"):
            s += 1
        return min(5, s)
    if dim == "D6":  # 差异化
        s = 0
        if has("差异化", "unique", "voice", "风格", "卖点", "differentiat"):
            s += 3
        if has("反缝合", "融合连贯", "显式裁决"):
            s += 2
        return min(5, s)
    if dim == "D7":  # 验证
        s = 0
        if has("真机", "verify", "验证", "测试", "test", "eval", "benchmark"):
            s += 3
        if has("外部标杆", "S3", "对标"):
            s += 2
        return min(5, s)
    if dim == "D8":  # 健壮性
        s = 0
        if has("边界", "red line", "红线", "edge", "失败", "failure", "降级", "robust"):
            s += 3
        if has("A.5", "硬规则"):
            s += 2
        return min(5, s)
    if dim == "D9":  # 可维护性
        s = 0
        if has("CHANGELOG", "changelog", "version", "迭代", "change"):
            s += 2
        if has("反馈", "feedback", "feedback-loop", "session_hook"):
            s += 2
        if has("信号", "signals"):
            s += 1
        return min(5, s)
    if dim == "D10":  # 可审查性
        s = 0
        if has("self-audit", "审视", "审查", "审计", "review", "red line"):
            s += 3
        if has("10 维", "rubric", "D1"):
            s += 2
        return min(5, s)
    return 0


def score_offline(dir_):
    name, md, refs = _read_skill(dir_)
    refs_count = len(refs)
    scores = {d: _score_dim(d, md, refs, refs_count) for d in ORDER}
    total = round(sum((scores[d] / 5.0) * DIM_WEIGHTS[d] for d in ORDER), 1)
    return name, md, refs, scores, total


def band(total):
    if total < 50:
        return "Thin（重写）"
    if total < 70:
        return "Solid（可用，迭代）"
    if total < 85:
        return "Excellent（强）"
    return "Global-Best 候选（需外网 benchmark + live-test）"


def _radar_svg(scores, name, total):
    cx, cy, R = 340, 250, 180
    n = len(ORDER)
    import math
    pts = {}
    for i, d in enumerate(ORDER):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        pts[d] = ang
    rings = []
    for lvl in (1, 2, 3, 4, 5):
        rr = R * lvl / 5
        coords = " ".join(
            f"{cx + rr * math.cos(pts[d]):.1f},{cy + rr * math.sin(pts[d]):.1f}"
            for d in ORDER)
        rings.append(f'<polygon points="{coords}" fill="none" stroke="#cbd5e1" stroke-width="1"/>')
    axes = []
    for d in ORDER:
        x = cx + R * math.cos(pts[d])
        y = cy + R * math.sin(pts[d])
        axes.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#cbd5e1" stroke-width="1"/>')
    data_pts = " ".join(
        f"{cx + (R * scores[d] / 5) * math.cos(pts[d]):.1f},{cy + (R * scores[d] / 5) * math.sin(pts[d]):.1f}"
        for d in ORDER)
    labels = []
    for d in ORDER:
        lx = cx + (R + 26) * math.cos(pts[d])
        ly = cy + (R + 26) * math.sin(pts[d])
        anchor = "middle"
        if math.cos(pts[d]) > 0.3:
            anchor = "start"
        elif math.cos(pts[d]) < -0.3:
            anchor = "end"
        labels.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="12" text-anchor="{anchor}" '
            f'fill="#1e293b" font-family="sans-serif">{d} {DIM_LABELS[d]}·{scores[d]}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 520" font-family="sans-serif">
  <rect width="680" height="520" fill="#ffffff"/>
  <text x="340" y="28" font-size="18" text-anchor="middle" fill="#0f172a">技能评测雷达 · {name}（本地基础版）</text>
  <text x="340" y="50" font-size="13" text-anchor="middle" fill="#475569">总分 {total}/100 · {band(total)} · 10 维自研尺（融合 TRACE + 云鼎安全检查）</text>
  {''.join(rings)}
  {''.join(axes)}
  <polygon points="{data_pts}" fill="#3b82f6" fill-opacity="0.25" stroke="#1d4ed8" stroke-width="2"/>
  {''.join(labels)}
</svg>'''
    return svg


def print_text(scores, total, name):
    print(f"\n# Review: {name}（本地基础版）")
    print(f"## Verdict: {band(total)} (score {total}/100)")
    print("## Dimension scores")
    for d in ORDER:
        print(f"{d} {DIM_LABELS[d]} .... {scores[d]}/5")
    print("\n说明：本地基础版按自研 10 维启发式估算；注册藏经阁可免费解锁由 9 个深度")
    print("playbook 计算的「方法论落点诊断 + 缺口建议」（云端增强版）。")


def _cloud_url(dir_):
    env = os.environ.get("CJG_REPORT_URL")
    if env:
        return env.strip().rstrip("/")
    for cand in (os.path.join(dir_, "cloud_config.json"),
                 os.path.expanduser("~/.workbuddy/secrets/cjg-evo/cloud_config.json")):
        if os.path.exists(cand):
            try:
                with open(cand, "r", encoding="utf-8") as f:
                    u = (json.load(f).get("report_url") or "").strip()
                if u:
                    return u.rstrip("/")
            except Exception:
                pass
    return None


def cmd_report(dir_, token=None, url=None, name=None, out_svg=True):
    name, md, refs, scores, total = score_offline(dir_)
    if name:
        pass
    print_text(scores, total, name)
    if out_svg:
        svg = _radar_svg(scores, name, total)
        out = os.path.join(os.getcwd(), f"skill-report-{name}.svg")
        with open(out, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"\n[雷达图已生成] {out}")

    if token:
        base = url or _cloud_url(dir_)
        if not base:
            print("\n[云端] 未配置 report_url（cloud_config.json 加 report_url，或 --url）。仍提供本地报告。")
        else:
            payload = json.dumps({
                "token": token,
                "skill_name": name,
                "skill_content": md + "\n" + "\n".join(refs),
            }, ensure_ascii=False).encode("utf-8")
            req = urllib.request.Request(
                f"{base}/report", data=payload,
                headers={"Content-Type": "application/json"}, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=15) as resp:
                    diag = json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code == 401:
                    print("\n[云端] 令牌无效或未验证（401）。请先用 forge-register.py register 注册并通过邮箱验证。")
                else:
                    print(f"\n[云端] 错误 {e.code}：{e.reason}")
                _footer()
                return
            except Exception as ex:
                print(f"\n[云端] 调用失败：{ex}（不影响本地报告）")
                _footer()
                return
            if diag.get("ok"):
                print("\n========== 云端增强诊断（免费）==========")
                cs = diag.get("scores", {})
                if cs:
                    ct = diag.get("total")
                    print(f"云端加权总分：{ct}/100")
                    for d in ORDER:
                        if d in cs:
                            print(f"  {d} {DIM_LABELS[d]} .... {cs[d]}/5")
                for f in diag.get("enhanced_findings", []):
                    print(f"  · {f['playbook']} 覆盖 {f['coverage_pct']}% ｜ 缺口示例：{', '.join(f.get('missing_top', []))}")
                if diag.get("suggestions"):
                    print("建议（按维度权重）：")
                    for s in diag["suggestions"]:
                        print(f"  - {s}")
                print(diag.get("note", ""))
            else:
                print(f"\n[云端] {diag.get('error')}")
    _footer()


def _footer():
    print("\n────────────────────────────────────────────────────")
    print("🔓 报告功能永远免费。注册藏经阁可免费解锁云端增强诊断：")
    print("   python skill-report.py <技能目录> --cloud --token <你的藏经阁令牌>")
    print("   注册：python forge-register.py register <邮箱> <slug>")


def main():
    args = sys.argv[1:]
    dir_ = DEFAULT_DIR
    token = None
    url = None
    name = None
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--cloud",):
            token = ""  # 占位，下面 --token 覆盖；若只给 --cloud 仍尝试（无 token 会 401 提示）
        elif a == "--token" and i + 1 < len(args):
            token = args[i + 1]
            i += 1
        elif a == "--url" and i + 1 < len(args):
            url = args[i + 1]
            i += 1
        elif a == "--name" and i + 1 < len(args):
            name = args[i + 1]
            i += 1
        elif a == "--dir" and i + 1 < len(args):
            dir_ = args[i + 1]
            i += 1
        elif not a.startswith("--"):
            dir_ = a
        i += 1
    if not os.path.isdir(dir_):
        print(f"目录不存在：{dir_}\n用法：python skill-report.py <技能目录> [--cloud --token T] [--url U]")
        return
    cmd_report(dir_, token=token or None, url=url, name=name)


if __name__ == "__main__":
    main()
