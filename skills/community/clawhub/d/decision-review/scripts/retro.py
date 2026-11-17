#!/usr/bin/env python3
"""决策复盘：把结构化字段渲染成 AAR 复盘文档。"""
import argparse, os


TPL = """# 决策复盘（AAR）

## 1. 背景
{background}

## 2. 预期结果
{expected}

## 3. 实际结果（事实）
{actual}

## 4. 差异
{delta}

## 5. 根因（5-Why）
{why}

## 6. 得失
- 做对了：{good}
- 做错了：{bad}

## 7. 改进项（具体·可验证）
{actions}

## 8. 沉淀原则
{principle}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--background", default="")
    ap.add_argument("--expected", default="")
    ap.add_argument("--actual", default="")
    ap.add_argument("--delta", default="")
    ap.add_argument("--why", default="")
    ap.add_argument("--good", default="")
    ap.add_argument("--bad", default="")
    ap.add_argument("--actions", default="")
    ap.add_argument("--principle", default="")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    def v(x, ph):
        return x if x else ph

    doc = TPL.format(
        background=v(args.background, "（待补充）"),
        expected=v(args.expected, "（待补充）"),
        actual=v(args.actual, "（待补充）"),
        delta=v(args.delta, "（待补充：预期与实际的差距）"),
        why=v(args.why, "（待补充：逐层追问到可改变的因素）"),
        good=v(args.good, "（待补充）"),
        bad=v(args.bad, "（待补充）"),
        actions=v(args.actions, "（待补充：每条带 owner/时限）"),
        principle=v(args.principle, "（待补充：一条可复用的决策原则）"),
    )
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(doc)
        print(f"✅ 复盘已写入：{args.output}")
    else:
        print(doc)


if __name__ == "__main__":
    main()
