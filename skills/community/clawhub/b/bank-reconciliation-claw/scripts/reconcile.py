#!/usr/bin/env python3
"""
银行流水对账虾 - 核心对账脚本
用法:
  python3 reconcile.py reconcile --bank <file> --orders <file> [--invoices <file>] [--output <file>]
  python3 reconcile.py preview --file <file>
  python3 reconcile.py export --report <file> --bitable-url <url>
"""

import argparse
import sys
import re
from pathlib import Path
from datetime import datetime, timedelta

try:
    import pandas as pd
except ImportError:
    print("❌ 缺少依赖: pip install pandas openpyxl")
    sys.exit(1)


# ─── 字段标准化 ────────────────────────────────────────────────────────────────

DATE_ALIASES = ["交易日期", "记账日期", "交易创建时间", "交易时间", "开票日期", "业务日期",
                "单据日期", "支付时间", "付款时间", "Posting Date", "过账日期", "date", "Date", "DATE"]
AMOUNT_ALIASES = ["交易金额", "发生额", "金额（元）", "金额(元)", "价税合计", "含税金额",
                  "Amount", "amount", "AMOUNT"]
ID_ALIASES = ["流水号", "交易流水号", "交易号", "交易单号", "订单号", "单据编号",
              "发票号码", "Document Number", "凭证号", "id", "ID"]


def find_column(df: pd.DataFrame, aliases: list[str]) -> str | None:
    """模糊匹配列名"""
    cols_lower = {c.strip().lower(): c for c in df.columns}
    for alias in aliases:
        if alias in df.columns:
            return alias
        if alias.lower() in cols_lower:
            return cols_lower[alias.lower()]
    return None


def normalize_amount(series: pd.Series) -> pd.Series:
    """清理金额列：去除 ¥ $ , 等符号，转为 float"""
    return (series.astype(str)
            .str.replace(r"[¥$,，\s]", "", regex=True)
            .str.replace(r"[（(]", "-", regex=True)
            .str.replace(r"[）)]", "", regex=True)
            .pipe(pd.to_numeric, errors="coerce"))


def normalize_date(series: pd.Series) -> pd.Series:
    """统一日期格式为 datetime"""
    return pd.to_datetime(series, errors="coerce")


def desensitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """对敏感字段脱敏（仅用于展示，不影响匹配计算）"""
    df = df.copy()
    for col in df.columns:
        col_lower = col.lower()
        if any(k in col_lower for k in ["账号", "account"]):
            df[col] = df[col].astype(str).apply(
                lambda x: x[:4] + "****" + x[-4:] if len(x) >= 8 else "****")
        elif any(k in col_lower for k in ["姓名", "name", "户名"]):
            df[col] = df[col].astype(str).apply(
                lambda x: x[0] + "**" if len(x) >= 2 else "**")
        elif any(k in col_lower for k in ["手机", "phone", "mobile"]):
            df[col] = df[col].astype(str).apply(
                lambda x: re.sub(r"(\d{3})\d{4}(\d{4})", r"\1****\2", x))
    return df


def load_file(path: str) -> pd.DataFrame:
    """加载 Excel 或 CSV 文件"""
    p = Path(path)
    if not p.exists():
        print(f"❌ 文件不存在: {path}")
        sys.exit(1)
    if p.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(path, dtype=str)
    elif p.suffix.lower() == ".csv":
        for enc in ["utf-8", "gbk", "utf-8-sig"]:
            try:
                return pd.read_csv(path, dtype=str, encoding=enc)
            except UnicodeDecodeError:
                continue
        print(f"❌ 无法解析文件编码: {path}")
        sys.exit(1)
    else:
        print(f"❌ 不支持的文件格式: {p.suffix}（仅支持 .xlsx .xls .csv）")
        sys.exit(1)


def prepare_df(df: pd.DataFrame, label: str) -> pd.DataFrame:
    """标准化数据框：识别日期、金额、ID 列"""
    date_col = find_column(df, DATE_ALIASES)
    amount_col = find_column(df, AMOUNT_ALIASES)
    id_col = find_column(df, ID_ALIASES)

    if not date_col:
        print(f"⚠️  [{label}] 未找到日期列，可用列: {list(df.columns)}")
        date_col = df.columns[0]
    if not amount_col:
        print(f"⚠️  [{label}] 未找到金额列，可用列: {list(df.columns)}")
        amount_col = df.columns[1]
    if not id_col:
        print(f"⚠️  [{label}] 未找到编号列，将使用行号作为 ID")
        df["_id"] = df.index.astype(str)
        id_col = "_id"

    df = df.copy()
    df["_date"] = normalize_date(df[date_col])
    df["_amount"] = normalize_amount(df[amount_col])
    df["_id"] = df[id_col].astype(str).str.strip()
    df["_label"] = label
    df["_matched"] = False
    df["_match_id"] = ""
    df["_match_type"] = ""
    df["_anomaly"] = ""
    return df


# ─── 匹配逻辑 ──────────────────────────────────────────────────────────────────

def reconcile_two(df_bank: pd.DataFrame, df_orders: pd.DataFrame,
                  date_tolerance: int = 3, amount_tolerance: float = 1.0) -> tuple:
    """两表对账：流水 vs 订单"""
    matched_pairs = []
    unmatched_bank = []
    unmatched_orders = list(df_orders.index)

    for bi, brow in df_bank.iterrows():
        b_amount = brow["_amount"]
        b_date = brow["_date"]
        best_match = None
        best_score = -1

        for oi in unmatched_orders:
            orow = df_orders.loc[oi]
            o_amount = orow["_amount"]
            o_date = orow["_date"]

            if pd.isna(b_amount) or pd.isna(o_amount):
                continue

            amount_diff = abs(b_amount - o_amount)
            date_diff = abs((b_date - o_date).days) if not (pd.isna(b_date) or pd.isna(o_date)) else 999

            # 精确匹配
            if amount_diff == 0 and date_diff <= date_tolerance:
                best_match = oi
                best_score = 100
                break
            # 模糊匹配
            elif amount_diff <= amount_tolerance and date_diff <= date_tolerance * 2:
                score = 50 - amount_diff - date_diff
                if score > best_score:
                    best_match = oi
                    best_score = score

        if best_match is not None:
            orow = df_orders.loc[best_match]
            amount_diff = abs(brow["_amount"] - orow["_amount"])
            date_diff = abs((brow["_date"] - orow["_date"]).days) if not (pd.isna(brow["_date"]) or pd.isna(orow["_date"])) else 0

            match_type = "精确匹配" if best_score == 100 else "模糊匹配"
            anomaly = ""
            if amount_diff > 0:
                anomaly = f"🟡 金额差异 {amount_diff:.2f}"
            if date_diff > date_tolerance:
                anomaly += f" 🔵 日期偏差 {date_diff}天"

            matched_pairs.append({
                "流水ID": brow["_id"],
                "流水日期": brow["_date"].strftime("%Y-%m-%d") if not pd.isna(brow["_date"]) else "",
                "流水金额": brow["_amount"],
                "订单ID": orow["_id"],
                "订单日期": orow["_date"].strftime("%Y-%m-%d") if not pd.isna(orow["_date"]) else "",
                "订单金额": orow["_amount"],
                "匹配类型": match_type,
                "异常标记": anomaly,
            })
            unmatched_orders.remove(best_match)
        else:
            unmatched_bank.append(bi)

    # 未匹配流水
    unmatched_bank_rows = []
    for bi in unmatched_bank:
        brow = df_bank.loc[bi]
        unmatched_bank_rows.append({
            "来源": "银行流水",
            "ID": brow["_id"],
            "日期": brow["_date"].strftime("%Y-%m-%d") if not pd.isna(brow["_date"]) else "",
            "金额": brow["_amount"],
            "异常类型": "🔴 未匹配",
        })

    # 未匹配订单
    for oi in unmatched_orders:
        orow = df_orders.loc[oi]
        unmatched_bank_rows.append({
            "来源": "系统订单",
            "ID": orow["_id"],
            "日期": orow["_date"].strftime("%Y-%m-%d") if not pd.isna(orow["_date"]) else "",
            "金额": orow["_amount"],
            "异常类型": "🔴 未匹配",
        })

    return matched_pairs, unmatched_bank_rows


def detect_duplicates(df: pd.DataFrame) -> list:
    """检测重复条目"""
    dupes = df[df.duplicated(subset=["_amount", "_date"], keep=False)]
    result = []
    for _, row in dupes.iterrows():
        result.append({
            "来源": row["_label"],
            "ID": row["_id"],
            "日期": row["_date"].strftime("%Y-%m-%d") if not pd.isna(row["_date"]) else "",
            "金额": row["_amount"],
            "异常类型": "🟠 重复条目",
        })
    return result


# ─── 报告生成 ──────────────────────────────────────────────────────────────────

def generate_report(matched: list, anomalies: list, output_path: str,
                    bank_total: int, order_total: int):
    """生成 Excel 对账报告"""
    match_rate = len(matched) / max(bank_total, 1) * 100
    matched_amount = sum(r["流水金额"] for r in matched if r["流水金额"] == r["流水金额"])

    summary = {
        "指标": ["银行流水总笔数", "系统订单总笔数", "匹配成功笔数", "匹配率", "差异条目数", "匹配金额合计"],
        "数值": [bank_total, order_total, len(matched), f"{match_rate:.1f}%",
                len(anomalies), f"{matched_amount:,.2f}"],
    }

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        pd.DataFrame(summary).to_excel(writer, sheet_name="汇总", index=False)
        if matched:
            pd.DataFrame(matched).to_excel(writer, sheet_name="匹配明细", index=False)
        if anomalies:
            pd.DataFrame(anomalies).to_excel(writer, sheet_name="异常清单", index=False)

    print(f"\n✅ 对账完成！报告已保存至: {output_path}")
    print(f"   银行流水: {bank_total} 笔 | 系统订单: {order_total} 笔")
    print(f"   匹配成功: {len(matched)} 笔（{match_rate:.1f}%）")
    print(f"   差异条目: {len(anomalies)} 笔")


# ─── CLI 入口 ──────────────────────────────────────────────────────────────────

def cmd_reconcile(args):
    print("📂 加载数据文件...")
    df_bank = prepare_df(load_file(args.bank), "银行流水")
    df_orders = prepare_df(load_file(args.orders), "系统订单")

    print(f"   银行流水: {len(df_bank)} 条")
    print(f"   系统订单: {len(df_orders)} 条")

    # 检测重复
    dupes = detect_duplicates(df_bank) + detect_duplicates(df_orders)

    print(f"\n🔍 执行对账（日期容差 ±{args.date_tolerance} 天，金额容差 ±{args.amount_tolerance} 元）...")
    matched, unmatched = reconcile_two(df_bank, df_orders,
                                       date_tolerance=args.date_tolerance,
                                       amount_tolerance=args.amount_tolerance)

    anomalies = unmatched + dupes

    if args.invoices:
        print("📄 发票核销功能（三表对账）暂需手动核对，已在报告中列出未匹配条目")

    output = args.output or "reconciliation_report.xlsx"
    generate_report(matched, anomalies, output, len(df_bank), len(df_orders))


def cmd_preview(args):
    print(f"📂 预览文件: {args.file}")
    df = load_file(args.file)
    print(f"\n列名: {list(df.columns)}")
    print(f"行数: {len(df)}")
    print(f"\n前 5 行:")
    print(df.head().to_string())

    date_col = find_column(df, DATE_ALIASES)
    amount_col = find_column(df, AMOUNT_ALIASES)
    id_col = find_column(df, ID_ALIASES)
    print(f"\n自动识别:")
    print(f"  日期列: {date_col or '未识别'}")
    print(f"  金额列: {amount_col or '未识别'}")
    print(f"  编号列: {id_col or '未识别'}")


def cmd_export(args):
    print("📤 导出到飞书多维表格功能需配合飞书插件使用")
    print("   请在对话中说：'把这份对账报告写入飞书多维表格 <URL>'")
    print(f"   报告文件: {args.report}")


def main():
    parser = argparse.ArgumentParser(description="银行流水对账虾")
    sub = parser.add_subparsers(dest="command")

    # reconcile
    p_rec = sub.add_parser("reconcile", help="执行对账")
    p_rec.add_argument("--bank", required=True, help="银行流水文件路径")
    p_rec.add_argument("--orders", required=True, help="系统订单文件路径")
    p_rec.add_argument("--invoices", help="发票台账文件路径（可选）")
    p_rec.add_argument("--output", help="输出报告路径（默认 reconciliation_report.xlsx）")
    p_rec.add_argument("--date-tolerance", type=int, default=3, help="日期容差（天，默认3）")
    p_rec.add_argument("--amount-tolerance", type=float, default=1.0, help="金额容差（元，默认1.0）")

    # preview
    p_pre = sub.add_parser("preview", help="预览文件解析结果")
    p_pre.add_argument("--file", required=True, help="要预览的文件路径")

    # export
    p_exp = sub.add_parser("export", help="导出到飞书多维表格")
    p_exp.add_argument("--report", required=True, help="对账报告文件路径")
    p_exp.add_argument("--bitable-url", help="飞书多维表格 URL")

    args = parser.parse_args()

    if args.command == "reconcile":
        cmd_reconcile(args)
    elif args.command == "preview":
        cmd_preview(args)
    elif args.command == "export":
        cmd_export(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
