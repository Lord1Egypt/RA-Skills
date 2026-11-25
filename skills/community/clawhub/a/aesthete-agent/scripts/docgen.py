#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docgen.py — 文档即代码(0.26):从引擎真实 CLI 面生成 docs/COMMANDS.md。

来源=每个子命令的 --help 实跑输出(最诚实的文档源:文档即 CLI 行为本身,不是手抄);
新鲜度由 release_check C4 机制化(重跑 docgen 与已提交文件 byte-diff,过期即 FAIL)。
纯 stdlib。用法: python3 scripts/docgen.py [--check]
  --check  只对比不写入(rc 0=文档新鲜;rc 1=过期,stdout 给出差异摘要)。
"""
import argparse
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs", "COMMANDS.md")

ENGINE = os.path.join(HERE, "palette_forge.py")
STANDALONE = [  # 独立 CLI 工具(引擎外)
    ("lint_page.py", "lint_page — HTML 交付前静态审计(色板漂移/字号/渐变/emoji/渲染证据)"),
    ("make_variants.py", "make_variants — 送审对比页"),
]

# 子命令一句话导读(决策表同源的 10 秒路由,避免裸 --help 没有任务视角)
WHEN = {
    "match": "按 brief 出配色(排序主键=得分,所见即所排)",
    "report": "四道机械闸评分(可挂第五闸 drama)",
    "evidence": "页面证据卷宗:静态 lint + 四闸合成 JSON+人读 HTML",
    "audit": "外部页面机械体检(漂移带替换值/禁渐变/对比对/字号/AI 签名)",
    "lint": None,  # lint_page 独立,见 STANDALONE
    "patch": "把审计结果变成字面替换对(--apply 直修并复检)",
    "loop": "渲染评审闭环清单(截图三铁律/qc 对账/五镜/停止条件)",
    "scaffold": "整页起点(五配方+AUTO 明暗路由)",
    "scene": "单场景样机(wallet/dashboard/landing…)",
    "chartpal": "图表配色三型(分类/顺序/发散,色盲模拟验证)",
    "tokens": "设计令牌表(CSS 变量+JSON,含动效令牌)",
    "typescale": "CJK 字阶(--fluid 流体+排印底座)",
    "narrate": "把实测闸门转成双语纯数字说明",
    "direct": "整页配色机械度量(温度旅程/饱和曲线/主色戏剧;--render 渲染事实)",
    "exemplar": "范例库检索注入(渲染评审过的成页样例)",
    "qc": "截图对账(大底真伪/板外入侵带,渲染实况=声明)",
    "matrix": "主题色板矩阵(跨主题一次性看全)",
    "themes": "主题清单(库内全部已验证主题)",
    "directions": "跨语域方向探索",
    "make_variants": None,
    "blind": "盲评对比页(双盲候选,防先入为主)",
    "card": "单卡片样机(结构化信息卡)",
    "check-image": "图片审查(尺寸/格式/文字安全)",
    "contrast": "两色对比度查询(带判据说明)",
    "critique": "整页审美批评(按法则集逐条点名)",
    "doctor": "环境自检(依赖/字体/浏览器探活)",
    "export": "导出(ASE/JSON/图片)",
    "extract": "从图片提取色板(聚类+去脏)",
    "harmony": "配色和谐度量(半径/跨度)",
    "house": "风格板(整页风格预览)",
    "mutate": "色板变异(单维扰动生成近亲板)",
    "ramp": "单色明度坡(语义档生成)",
    "roles": "OKLCH 角色派生(60-30-10+语义档)",
    "score": "四闸评分明细",
    "search": "库内检索(brief/标签直达)",
    "selftest": "引擎自测(结构不变量)",
    "semantic": "已并入 chartpal(兼容别名)",
    "showcase": "场景图墙(多场景拼版)",
    "slop": "反俗套扫描(tailwind 默认/紫域/玻璃拟态)",
    "theme": "单主题详情(色板+角色)",
    "visualize": "可视化样机(dashboard/编辑器等)",
}


def discover():
    """从 palette_forge.py 源里抓 add_parser 名单(AST 级,不靠手抄清单)。"""
    import ast
    names = []
    src = open(ENGINE, encoding="utf-8").read()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "add_parser" and node.args:
                a = node.args[0]
                if isinstance(a, ast.Constant) and isinstance(a.value, str):
                    names.append(a.value)
    return sorted(set(names))


def capture(cmd_help):
    r = subprocess.run([sys.executable, ENGINE, cmd_help, "--help"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (r.stdout or r.stderr).strip()


def build():
    lines = ["<!-- 本文件由 scripts/docgen.py 生成(来源=各命令 --help 实跑输出)。",
             "     手改无效;改文档请改引擎 help 文案后重跑 docgen;新鲜度由 release_check C4 校验 -->",
             "", "# 命令全量参考(自动生成)", "",
             "> 决策表(10 秒选对命令)在 SKILL.md/SKILL_ZH.md;本文件=全量 flags 参考。", ""]
    subs = discover()
    missing = [c for c in subs if c not in WHEN]
    if missing:
        print("docgen: WHEN 导读缺词条: %s —— 先补 WHEN 表再生成" % missing, file=sys.stderr)
        sys.exit(2)
    for name in subs:
        lines += ["## palette_forge %s" % name, ""]
        if WHEN.get(name):
            lines += ["> %s" % WHEN[name], ""]
        lines += ["```", capture(name), "```", ""]
    for fn, desc in STANDALONE:
        r = subprocess.run([sys.executable, os.path.join(HERE, fn), "--help"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        lines += ["## %s" % fn, "", "> %s" % desc, "", "```", (r.stdout or r.stderr).strip(), "```", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只对比不写入(rc 0=新鲜,1=过期)")
    args = ap.parse_args()
    doc = build()
    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else None
    if args.check:
        if old is None:
            print("docgen --check: docs/COMMANDS.md 不存在 —— 先跑 docgen 生成", file=sys.stderr)
            sys.exit(1)
        if old == doc:
            print("docgen --check: 文档新鲜(与 CLI 面一致)")
            sys.exit(0)
        import difflib
        d = [l for l in difflib.unified_diff(old.splitlines(), doc.splitlines(), "committed", "fresh", lineterm="")
             if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))][:12]
        print("docgen --check: 文档过期(CLI 面已变),差异 %d 行摘要:" % len(d), file=sys.stderr)
        print("\n".join(d), file=sys.stderr)
        sys.exit(1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(doc)
    n = doc.count("\n## ")
    print("docgen: docs/COMMANDS.md 生成(%d 个命令节, %d 字符)" % (n, len(doc)))


if __name__ == "__main__":
    main()
