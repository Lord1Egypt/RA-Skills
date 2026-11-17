#!/usr/bin/env python3
"""
Excel / CSV 数据清洗与体检工具

体检模式（只输出概况，不写任何文件）:
    python clean_excel.py data.xlsx

完整清洗（去重 + 缺失填充 + 异常值标记 + 报告）:
    python clean_excel.py data.xlsx --out clean.xlsx --dedupe \
        --numeric-fill median --outlier iqr --outlier-action flag --report report.md

可通过 --out-file 之外的参数组合控制行为；未指定任何清洗动作且未给 --out 时，
只做体检，不写出任何文件。

注意：永远输出为新文件，不覆盖原始输入。
"""

import argparse
import sys
from pathlib import Path

EXIT_FAIL = 1


def fail(msg):
    print("❌ " + msg)
    sys.exit(EXIT_FAIL)


try:
    import pandas as pd
except ImportError:
    fail("缺少 pandas，请先安装依赖：pip install pandas openpyxl")


def is_text_dtype(dtype):
    """
    判断是否为文本列。

    兼容跨 pandas 版本：
    - pandas 2.x：文本列通常为 object dtype
    - pandas 3.x：字符串列默认推断为 str dtype（不再是 object）

    不能直接用 `dtype == object` 判断，否则在 pandas 3 下会静默漏掉所有文本列。
    """
    try:
        types = pd.api.types
        if types.is_numeric_dtype(dtype) or types.is_bool_dtype(dtype):
            return False
        if types.is_datetime64_any_dtype(dtype) or types.is_timedelta64_dtype(dtype):
            return False
    except Exception:
        pass
    return True


def load_dataframe(path, sheet=None):
    """根据扩展名读取 DataFrame。"""
    p = Path(path)
    if not p.exists():
        fail("文件不存在：" + str(path))
    suffix = p.suffix.lower()
    try:
        if suffix in (".xlsx", ".xls"):
            try:
                import openpyxl  # noqa: F401
            except ImportError:
                fail("读取 Excel 需要 openpyxl：pip install openpyxl")
            df = pd.read_excel(p, sheet_name=sheet if sheet is not None else 0)
        elif suffix == ".csv":
            try:
                df = pd.read_csv(p, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(p, encoding="gbk")
        else:
            fail("不支持的文件类型：" + suffix + "（支持 .xlsx / .xls / .csv）")
    except SystemExit:
        raise
    except Exception as exc:
        fail("读取文件失败：" + str(exc))
    if not isinstance(df, pd.DataFrame):
        fail("工作表读取结果异常，请检查 --sheet 参数")
    return df, p


def build_profile(df):
    """生成数据概览的 Markdown 行。"""
    rows = len(df)
    lines = ["- 规模：{} 行 × {} 列".format(rows, len(df.columns)), ""]
    lines.append("| 列名 | 类型 | 非空 | 缺失率 | 唯一值 | 示例值 |")
    lines.append("|------|------|------|--------|--------|--------|")
    for col in df.columns:
        series = df[col]
        non_null = int(series.notna().sum())
        miss_rate = (1 - non_null / rows) if rows else 0.0
        try:
            n_unique = int(series.nunique(dropna=True))
        except Exception:
            n_unique = -1
        sample = series.dropna().head(2).tolist()
        sample_str = "，".join(str(x)[:18] for x in sample) if sample else "-"
        lines.append(
            "| {} | {} | {} | {:.1%} | {} | {} |".format(
                col, series.dtype, non_null, miss_rate, n_unique, sample_str
            )
        )
    lines.append("")
    lines.append("- 完全重复行：{} 行".format(int(df.duplicated().sum())))
    return lines


def detect_outliers(df, method, cols=None):
    """返回 {列名: (异常数量, 下界, 上界, 布尔掩码)}。"""
    result = {}
    if method == "none":
        return result
    numeric = df.select_dtypes(include="number")
    if cols:
        numeric = numeric[[c for c in cols if c in numeric.columns]]
    for col in numeric.columns:
        series = df[col]
        values = series.dropna()
        if values.empty:
            continue
        if method == "iqr":
            q1, q3 = values.quantile(0.25), values.quantile(0.75)
            iqr = q3 - q1
            if iqr == 0:
                continue
            lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        else:  # zscore
            mean, std = values.mean(), values.std()
            if not std or pd.isna(std):
                continue
            lower, upper = mean - 3 * std, mean + 3 * std
        mask = series.notna() & ((series < lower) | (series > upper))
        count = int(mask.sum())
        if count:
            result[col] = (count, float(lower), float(upper), mask)
    return result


def normalize_text_columns(df):
    """去除文本列首尾空格，把空字符串与纯空格视为缺失。"""
    changed = []
    for col in df.columns:
        if is_text_dtype(df[col].dtype):
            before_na = int(df[col].isna().sum())
            cleaned = df[col].astype("string").str.strip()
            cleaned = cleaned.mask(cleaned.eq(""))
            after_na = int(cleaned.isna().sum())
            df[col] = cleaned
            if after_na > before_na:
                changed.append((col, after_na - before_na))
    return df, changed


def parse_args():
    parser = argparse.ArgumentParser(
        description="Excel/CSV 数据体检与清洗工具（不覆盖原始文件）"
    )
    parser.add_argument("input", help="输入文件路径（xlsx / xls / csv）")
    parser.add_argument("--sheet", default=None, help="工作表名称，默认第一个")
    parser.add_argument("--out", default=None, help="清洗结果输出路径")
    parser.add_argument("--dedupe", action="store_true", help="删除重复行")
    parser.add_argument("--subset", default=None, help="判重依据列，逗号分隔")
    parser.add_argument(
        "--numeric-fill",
        default="none",
        choices=["mean", "median", "zero", "none"],
        help="数值缺失填充策略，默认 none（不填充）",
    )
    parser.add_argument("--text-fill", default="未知", help="文本缺失填充值，默认「未知」")
    parser.add_argument(
        "--drop-row-na-threshold",
        type=float,
        default=None,
        help="缺失率高于该比例的行直接删除（0-1）",
    )
    parser.add_argument(
        "--drop-col-na-threshold",
        type=float,
        default=None,
        help="缺失率高于该比例的列直接删除（0-1）",
    )
    parser.add_argument(
        "--outlier", default="iqr", choices=["iqr", "zscore", "none"], help="异常值检测法，默认 iqr"
    )
    parser.add_argument(
        "--outlier-cols", default=None, help="参与异常值检测的列，逗号分隔，默认全部数值列"
    )
    parser.add_argument(
        "--outlier-action",
        default="flag",
        choices=["flag", "clip", "drop", "none"],
        help="异常值处理方式，默认 flag（加标记列，不删数据）",
    )
    parser.add_argument("--report", default=None, help="清洗报告 Markdown 输出路径")
    return parser.parse_args()


def collect_explicit_ops(args):
    """判断用户是否显式指定了清洗动作（决定是「体检」还是「清洗」）。"""
    ops = []
    if args.dedupe:
        ops.append("--dedupe")
    if args.subset:
        ops.append("--subset")
    if args.numeric_fill != "none":
        ops.append("--numeric-fill")
    if args.drop_row_na_threshold is not None:
        ops.append("--drop-row-na-threshold")
    if args.drop_col_na_threshold is not None:
        ops.append("--drop-col-na-threshold")
    if args.outlier_action in ("clip", "drop"):
        ops.append("--outlier-action=" + args.outlier_action)
    return ops


def write_output(df, out_arg, input_path):
    """写出清洗结果，返回最终路径。"""
    out_path = Path(out_arg) if out_arg else input_path.with_name(
        input_path.stem + "_cleaned.xlsx"
    )
    try:
        if out_path.suffix.lower() == ".csv":
            df.to_csv(out_path, index=False, encoding="utf-8-sig")
        else:
            if out_path.suffix.lower() not in (".xlsx", ".xls"):
                out_path = out_path.with_suffix(".xlsx")
            try:
                import openpyxl  # noqa: F401
            except ImportError:
                fail("写出 Excel 需要 openpyxl：pip install openpyxl")
            df.to_excel(out_path, index=False)
    except Exception as exc:
        fail("写出结果失败：" + str(exc))
    return out_path


def run_cleaning(df, args, outlier_cols):
    """执行清洗，返回 (清洗后 DataFrame, 操作日志)。"""
    log = []

    df, text_changed = normalize_text_columns(df)
    for col, count in text_changed:
        log.append("「{}」内有 {} 处空白/纯空格，已规整为缺失值".format(col, count))

    if args.drop_col_na_threshold is not None:
        threshold = args.drop_col_na_threshold
        keep = df.columns[df.isna().mean(axis=0) <= threshold]
        dropped = [c for c in df.columns if c not in set(keep)]
        if dropped:
            df = df[keep]
            log.append(
                "缺失率高于 {:.0%} 的列删除 {} 个：{}".format(
                    threshold, len(dropped), "、".join(str(c) for c in dropped)
                )
            )

    if args.drop_row_na_threshold is not None:
        threshold = args.drop_row_na_threshold
        before = len(df)
        df = df[df.isna().mean(axis=1) <= threshold]
        removed = before - len(df)
        if removed:
            log.append(
                "缺失率高于 {:.0%} 的行删除 {} 行（剩 {} 行）".format(
                    threshold, removed, len(df)
                )
            )

    if args.dedupe or args.subset:
        before = len(df)
        subset = args.subset.split(",") if args.subset else None
        if subset:
            missing_cols = [c for c in subset if c not in df.columns]
            if missing_cols:
                fail("--subset 指定列不存在：" + "、".join(missing_cols))
        df = df.drop_duplicates(subset=subset, keep="first")
        removed = before - len(df)
        label = "按「{}」判重".format("、".join(subset)) if subset else "完全重复"
        if removed:
            log.append("{} 删除 {} 行（剩 {} 行）".format(label, removed, len(df)))
        else:
            log.append("{} 未发现重复行".format(label))

    if args.numeric_fill != "none":
        for col in df.select_dtypes(include="number").columns:
            missing = int(df[col].isna().sum())
            if not missing:
                continue
            if args.numeric_fill == "mean":
                value = float(df[col].mean())
            elif args.numeric_fill == "median":
                value = float(df[col].median())
            else:
                value = 0.0
            df[col] = df[col].fillna(value)
            log.append(
                "「{}」缺失 {} 处，以{}值 {:.2f} 填充".format(
                    col,
                    missing,
                    {"mean": "平均", "median": "中位", "zero": "零"}[args.numeric_fill],
                    value,
                )
            )

    text_missing = 0
    for col in df.columns:
        if is_text_dtype(df[col].dtype):
            missing = int(df[col].isna().sum())
            if missing:
                df[col] = df[col].fillna(args.text_fill)
                text_missing += missing
    if text_missing:
        log.append(
            "文本列缺失共 {} 处，统一填充为「{}」".format(text_missing, args.text_fill)
        )

    if args.outlier != "none" and args.outlier_action != "none":
        found = detect_outliers(df, args.outlier, outlier_cols)
        if args.outlier_action == "flag":
            for col, (count, lower, upper, mask) in found.items():
                df["_outlier_" + str(col)] = mask.astype(bool)
                log.append(
                    "「{}」标记异常值 {} 条（{} 法，正常区间 [{:.2f}, {:.2f}]）".format(
                        col, count, args.outlier.upper(), lower, upper
                    )
                )
        elif args.outlier_action == "clip":
            for col, (count, lower, upper, _mask) in found.items():
                df[col] = df[col].clip(lower=lower, upper=upper)
                log.append(
                    "「{}」异常值 {} 条已盖帽到 [{:.2f}, {:.2f}]".format(
                        col, count, lower, upper
                    )
                )
        elif args.outlier_action == "drop":
            combine = None
            for col, (_c, _l, _u, mask) in found.items():
                combine = mask if combine is None else (combine | mask)
            if combine is not None:
                before = len(df)
                df = df[~combine]
                log.append(
                    "含异常值的行删除 {} 行（剩 {} 行）".format(before - len(df), len(df))
                )

    return df, log


def main():
    args = parse_args()
    df, path = load_dataframe(args.input, args.sheet)
    original_shape = df.shape

    # 体检报告必须在清洗【之前】生成
    profile_before = build_profile(df)

    print("=" * 60)
    print("数据体检：" + str(path))
    print("=" * 60)
    for line in profile_before:
        print(line)

    outlier_cols = args.outlier_cols.split(",") if args.outlier_cols else None
    overview = detect_outliers(df, args.outlier, outlier_cols)
    print("")
    if overview:
        print("- 疑似异常值：")
        for col, (count, lower, upper, _mask) in overview.items():
            print(
                "    · {}: {} 条，正常区间 [{:.2f}, {:.2f}]".format(col, count, lower, upper)
            )
    else:
        print("- 疑似异常值：无")

    explicit_ops = collect_explicit_ops(args)
    cleaning_requested = bool(explicit_ops) or args.out is not None

    if not cleaning_requested:
        print("")
        print("ℹ️  体检模式：未指定清洗动作且未给 --out，未写出任何文件。")
        print("    想要产出清洗文件，请加 --out <文件名> 或指定具体清洗动作。")
        return

    cleaned, log = run_cleaning(df, args, outlier_cols)
    out_path = write_output(cleaned, args.out, path)

    print("")
    print("=" * 60)
    print("清洗记录")
    print("=" * 60)
    if log:
        for index, line in enumerate(log, 1):
            print("{}. {}".format(index, line))
    else:
        print("（本次未产生任何数据改动）")
    print("")
    print(
        "规模变化：{} 行 × {} 列 → {} 行 × {} 列".format(
            original_shape[0], original_shape[1], len(cleaned), len(cleaned.columns)
        )
    )
    print("结果文件：" + str(out_path))

    if args.report:
        lines = ["# 数据清洗报告", ""]
        lines.append("- 输入文件：{}".format(path))
        lines.append("- 输出文件：{}".format(out_path))
        lines.append(
            "- 规模变化：{} 行 × {} 列 → {} 行 × {} 列".format(
                original_shape[0], original_shape[1], len(cleaned), len(cleaned.columns)
            )
        )
        lines.append("- 生效清洗动作：{}".format("、".join(explicit_ops) if explicit_ops else "仅异常值标记"))
        lines.append("")
        lines.append("## 清洗前体检")
        lines.extend(profile_before)
        lines.append("")
        lines.append("## 清洗记录")
        if log:
            for index, line in enumerate(log, 1):
                lines.append("{}. {}".format(index, line))
        else:
            lines.append("（本次未产生任何数据改动）")
        lines.append("")
        Path(args.report).write_text("\n".join(lines), encoding="utf-8")
        print("清洗报告：" + args.report)


if __name__ == "__main__":
    main()
