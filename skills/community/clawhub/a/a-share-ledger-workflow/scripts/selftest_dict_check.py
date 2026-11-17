#!/usr/bin/env python3
"""selftest_dict_check.py —— 校验器第7项（台账↔bench.json 相对中位）双向自检。

为什么需要它：这个检查曾经**静默失效** —— 台账「相对中位」写法一变，正则就抓不到，
旧实现 `if not hits: continue` 直接跳过，整批标的没人校验，输出仍是「✅ 通过」。
（实测形态：32 只里只有 2 只被真正校验过。）

本自检把真实台账复制到临时目录，逐个注入坏状态，断言**必须报错**；
再回滚旧正则，断言覆盖率**必须掉下来**（证明覆盖率是实测值，不是恒等于总数）。

🔴 只读真实数据：全部操作发生在临时副本上。
用法：
    export STOCK_DATA_DIR=/path/to/your_stock_data
    python3 scripts/selftest_dict_check.py [-v]
退出码：0 = 全部通过；1 = 有断言失败
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_ledgers as V   # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    d = os.environ.get("STOCK_DATA_DIR", "").rstrip("/")
    if not d:
        raise SystemExit("🔴 未设置 STOCK_DATA_DIR")
    d = Path(d)
    real = sorted(list((d / "股票台账" / "候选").glob("*.md"))
                  + list((d / "股票台账" / "持仓中").glob("*.md")))
    if not real:
        raise SystemExit(f"🔴 {d}/股票台账 下没有台账")

    bench = V.load_gate_dicts().get("BENCH", {})
    require = sum(1 for v in bench.values() if v[1] is not None)
    ok, fail = 0, []

    def check(name, cond, extra=""):
        nonlocal ok
        if cond:
            ok += 1
            if args.verbose:
                print(f"  ✅ {name}")
        else:
            fail.append(f"{name} {extra}")
            print(f"  ❌ {name} {extra}")

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for f in real:
            shutil.copy(f, tmp / f.name)

        def files():
            return sorted(tmp.glob("*.md"))

        # ① 好状态：不误报 + 覆盖率满
        errs, cov = V.check_dict_consistency(files())
        check("好状态不误报", not errs, str(errs[:2]))
        check(f"覆盖率 = {require}/{require}",
              cov.get("checked") == require and cov.get("required") == require, str(cov))

        # 选一份有相对中位数值的台账作夹具
        target = next((f for f in files() if V.BENCH_PAT.search(f.read_text(encoding="utf-8"))), None)
        if target is None:
            print("  ❌ 找不到含「相对中位 …pt」的台账，无法做注入测试")
            return 1
        code = re.match(r"(.+?)_(\d{6})_", target.name).group(2)
        want = bench[code][1]
        orig = target.read_text(encoding="utf-8")

        def inject(text, new_pt, keep_label=True):
            """把文中**所有**「相对中位 …pt」的数值换成 new_pt。
            🔴 必须全替换：校验器是「任一命中即通过」，只改一处会被另一处抵消。"""
            def _r(m):
                if not keep_label:
                    return "相对中位 见附注"
                return m.group(0).replace(m.group(1), new_pt)
            return V.BENCH_PAT.sub(_r, text)

        # ② 数值冲突
        bad = inject(orig, f"{want + 99:+.2f}")
        assert bad != orig, "夹具失效：未能替换"
        target.write_text(bad, encoding="utf-8")
        errs, _ = V.check_dict_consistency(files())
        check("数值冲突必报", any("数值冲突" in e and code in e for e in errs), str(errs[:3]))
        target.write_text(orig, encoding="utf-8")

        # ③ 占位 0.00 未填（bench_pt 非 0 时）
        if want not in (0, 0.0):
            target.write_text(inject(orig, "0.00"), encoding="utf-8")
            errs, _ = V.check_dict_consistency(files())
            check("占位未填必报", any("占位" in e and code in e for e in errs), str(errs[:3]))
            target.write_text(orig, encoding="utf-8")

        # ④ 提不到数值 → fail-closed 必须报
        target.write_text(inject(orig, "", keep_label=False), encoding="utf-8")
        errs, cov2 = V.check_dict_consistency(files())
        check("提不到数值必报（fail-closed）",
              any("提不到数值" in e and code in e for e in errs), str(errs[:3]))
        check("提不到时覆盖率下降", cov2.get("checked") == require - 1, str(cov2))
        target.write_text(orig, encoding="utf-8")

        # ⑤ 基准日不符
        if V.BASE_START_RE.search(orig):
            bad = V.BASE_START_RE.sub("起点日 1999-01-01", orig, count=1)
            target.write_text(bad, encoding="utf-8")
            errs, _ = V.check_dict_consistency(files())
            check("基准日不符必报", any("基准日不符" in e for e in errs), str(errs[:3]))
            target.write_text(orig, encoding="utf-8")
        else:
            if args.verbose:
                print("  ⏭ 台账无基准起止行，跳基准日测试")

        # ⑥ 反向自证：回滚旧正则（不认表格竖线 |），覆盖率必须掉
        real_pat = V.BENCH_PAT
        V.BENCH_PAT = re.compile(r"相对(?:方向)?中位\s*\**\s*([\u2212\u2013\u2014\-]?\s*[\d.]+)\s*pt")
        try:
            _, cov_old = V.check_dict_consistency(files())
        finally:
            V.BENCH_PAT = real_pat
        check("回滚旧正则后覆盖率下降（证明覆盖率实测有效）",
              cov_old.get("checked", 0) <= cov.get("checked", 0), str(cov_old))

        # ⑦ 恢复后仍全绿
        errs, cov3 = V.check_dict_consistency(files())
        check("恢复后仍不误报", not errs and cov3.get("checked") == require, str(errs[:2]))

    print(f"\n自检：{ok} 项通过，{len(fail)} 项失败")
    if fail:
        for f in fail:
            print(f"  ❌ {f}")
        return 1
    print("✅ 第7项双向验证全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
