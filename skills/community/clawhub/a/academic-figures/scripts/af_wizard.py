# -*- coding: utf-8 -*-
"""--wizard 选图向导（v3.0.0 自 gen_figure.py 拆出；行为与 v2.8/v2.9 完全一致）。
四问生成完整命令：数据形态 → 图型 → 输出格式 → 数据文件；非 TTY 环境打印决策树不挂起。"""
import os
import sys

_WIZARD_SHAPES = [
    ("各组一组数值（分组比较；看完整分布选 raincloud）", ["bar", "grouped_bar", "box", "violin", "raincloud", "line"],
     "templates/02-rct-baseline-bar.json"),
    ("均值 ± 误差棒（SD/SE）", ["bar"], "templates/02-rct-baseline-bar.json"),
    ("两列连续值（相关/散点）", ["scatter"], "templates/12-dose-response-scatter.json"),
    ("生存数据（时间+事件，分组）", ["km"], "templates/03-survival-km.json"),
    ("诊断试验（标志物+金标准）", ["roc"], "templates/04-diagnostic-roc.json"),
    ("预测概率分箱 vs 实际发生率（模型校准）", ["calibration"], "templates/calibration.json"),
    ("预测模型临床净收益 vs 阈值（决策曲线）", ["dca"], "templates/dca.json"),
    ("预测模型查表尺（列线图，变量计分→总积分→概率）", ["nomogram"], "templates/nomogram.json"),
    ("暴露-结局非线性剂量反应（RCS 样条，HR/OR 带 CI）", ["rcs"], "templates/rcs.json"),
    ("疗效亚组分析（各层效应+P 交互，亚组森林图）", ["subgroup"], "templates/subgroup.json"),
    ("基因/元素集合（交并关系；≥5 集合选 upset）", ["venn", "upset"], "templates/venn.json"),
    ("每例最佳缓解百分比（肿瘤瀑布图）", ["waterfall"], "templates/waterfall.json"),
    ("每例治疗/随访时长（临床游泳图）", ["swimmer"], "templates/swimmer.json"),
    ("多组分布逐组移动全景（山脊图）", ["ridgeline"], "templates/ridgeline.json"),
    ("逐条目两点差距（哑铃图）", ["dumbbell"], "templates/dumbbell.json"),
    ("二维数值矩阵（行×列）", ["heatmap", "cluster_heatmap"], "templates/cluster_heatmap.json"),
    ("逐例生存+协变量（多因素 Cox 回归）", ["forest"], None),
    ("效应值+标准误（Meta 分析）", ["forest", "funnel", "galbraith"], "templates/01-meta-forest.json"),
    ("流程步骤/研究设计", ["diagram", "stacked_bar", "prisma"],
     "templates/16-study-design-diagram.json"),
    ("同一对象两次测量（一致性/前后）", ["bland_altman", "paired"],
     "templates/bland_altman.json"),
    ("多变量降维（样本分类展示）", ["pca"], "templates/pca.json"),
]
_WIZARD_FORMATS = [("png", "png（默认，通用）"), ("pdf", "pdf（投稿矢量）"),
                   ("tiff", "tiff（期刊 600dpi 位图）"), ("svg", "svg（网页/再编辑）")]


def _wizard_ask(prompt, options, default=1):
    """问一题；空输入/EOF 落默认。返回选择序号（0 基）。"""
    try:
        raw = input(prompt).strip()
    except EOFError:
        raw = ""
    if not raw:
        return default - 1 if default is not None else 0
    try:
        idx = int(raw) - 1
    except ValueError:
        return default - 1 if default is not None else 0
    if 0 <= idx < len(options):
        return idx
    return default - 1 if default is not None else 0


def _wizard_guide():
    """非交互环境（agent/管道）：打印选图决策树，绝不挂起。"""
    print("【选图向导】交互环境可用 `--wizard` 问答式生成命令；当前为非交互环境，以下是决策树：")
    print()
    for i, (shape, types, _t) in enumerate(_WIZARD_SHAPES, 1):
        print(f"{i:2d}. 数据是「{shape}」→ -t {' / '.join(types)}")
    print()
    print("通用骨架：python3 scripts/gen_figure.py -t <图型> -d <数据.json> -o <输出> [选项]")
    print("常用选项：--journal nejm|lancet|science|nature|cma|cn-core ｜ --theme okabe-ito（色盲安全）")
    print("          --verify（PDF 重叠门禁）｜ --multi-format png,pdf ｜ --cjk 中文")
    print("不确定图型：python3 scripts/gen_figure.py --suggest -d <数据文件>")


def _run_wizard():
    """交互式向导：4 问生成完整命令。AF_WIZARD_FORCE=1 时非 TTY 也走交互
    （管道喂答案可用于测试/脚本）；EOF 逐题落默认值，永不抛异常挂起。"""
    interactive = sys.stdin.isatty() or os.environ.get("AF_WIZARD_FORCE")
    if not interactive:
        _wizard_guide()
        return
    print("【选图向导】4 个问题生成完整命令（直接回车取默认）")
    print()
    print("1) 你的数据长什么样？")
    for i, (shape, _t, _tp) in enumerate(_WIZARD_SHAPES, 1):
        print(f"   {i:2d}. {shape}")
    si = _wizard_ask("   选择 [1]: ", _WIZARD_SHAPES, default=1)
    shape, types, tmpl = _WIZARD_SHAPES[si]
    print()
    print(f"2) 推荐图型（「{shape}」）：")
    for i, t in enumerate(types, 1):
        print(f"   {i}. {t}")
    ti = _wizard_ask(f"   选择 [1]: ", types, default=1)
    chart = types[ti]
    print()
    print("3) 输出格式：")
    for i, (fcode, fdesc) in enumerate(_WIZARD_FORMATS, 1):
        print(f"   {i}. {fdesc}")
    fi = _wizard_ask("   选择 [1]: ", _WIZARD_FORMATS, default=1)
    fmt = _WIZARD_FORMATS[fi][0]
    print()
    try:
        data_path = input("4) 数据文件路径（回车=先用模板）: ").strip()
    except EOFError:
        data_path = ""
    if not data_path:
        # v4.7 D-14：图型同名模板优先（如 upset → templates/upset.json），
        # 向导推荐命令不再指向异图型模板
        _same = f"templates/{chart}.json"
        if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__))), _same)):
            tmpl = _same
        if tmpl:
            data_path = tmpl
            print(f"   → 先复制模板改数据：cp {tmpl} mydata.json")
        else:
            data_path = "mydata.json"
            print(f"   → 该图型无场景模板，数据格式见：python3 scripts/gen_figure.py --explain {chart}")
    out_path = "figure." + fmt
    print()
    print("── 生成命令 ──────────────────────────────")
    print(f"python3 scripts/gen_figure.py -t {chart} -d {data_path} -o {out_path}")
    print("─────────────────────────────────────────")
    print(f"图型细节：python3 scripts/gen_figure.py --explain {chart}")




if __name__ == "__main__":
    # v7.8.0 批次2（跨线 U6 精神自查）：本模块是 gen_figure --wizard 的实现库，
    # 直接执行无入口语义——指路 + rc=2（禁静默 rc=0 零输出）。
    print("内部模块：请通过 python3 scripts/gen_figure.py --wizard 调用交互式向导。",
          file=sys.stderr)
    sys.exit(2)
