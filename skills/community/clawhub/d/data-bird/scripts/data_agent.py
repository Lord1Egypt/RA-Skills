"""
DataAgent: 读取 CSV/Excel/MySQL，输出 DataFrame + 字段元数据 + 数据场景画像。
"""
import os
from typing import Any, Dict, List, Optional

import pandas as pd


_TIME_HINTS = ("date", "time", "日期", "时间", "月份", "季度", "年份", "周", "day", "month", "year")
_FINANCE_HINTS = ("收入", "营收", "销售额", "利润", "毛利", "成本", "费用", "金额", "回款", "revenue", "profit", "cost")
_PRODUCT_HINTS = ("产品", "商品", "sku", "型号", "库存", "件数", "品类", "category")
_CUSTOMER_HINTS = ("客户", "用户", "会员", "账号", "手机号", "联系人", "customer", "user")
_OPS_HINTS = ("工单", "时长", "效率", "转化", "产能", "处理", "完成", "throughput", "duration", "rate")
_ENTITY_HINTS = ("公司", "企业", "地址", "行业", "地区", "区域", "省", "市", "联系人", "电话", "email")


def infer_column_type(series: pd.Series) -> str:
    """推断列语义类型: time | metric | dimension"""
    name = str(series.name or "").lower()
    if any(k in name for k in _TIME_HINTS):
        return "time"

    non_null = series.dropna()
    if non_null.empty:
        return "dimension"

    try:
        numeric = pd.to_numeric(non_null, errors="coerce")
        if numeric.notna().all():
            return "metric"
    except Exception:
        pass

    if pd.api.types.is_datetime64_any_dtype(series):
        return "time"

    if pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series):
        try:
            text_sample = non_null.astype(str).head(20)
            looks_like_time = text_sample.str.contains(r"[-/:年月日T ]", regex=True).mean() >= 0.6
            if looks_like_time:
                parsed_time = pd.to_datetime(non_null, errors="coerce")
                if parsed_time.notna().mean() >= 0.8:
                    return "time"
        except Exception:
            pass

    try:
        unique_ratio = float(non_null.astype(str).nunique()) / float(len(non_null))
        if unique_ratio < 0.8:
            return "dimension"
    except Exception:
        pass
    return "dimension"


def _match_hints(names: List[str], hints: tuple) -> bool:
    lowered = " ".join(str(name or "").lower() for name in names)
    return any(k in lowered for k in hints)


def _infer_scenario(time_cols: List[str], metric_cols: List[str], dim_cols: List[str]) -> str:
    all_cols = time_cols + metric_cols + dim_cols
    if metric_cols and time_cols:
        if _match_hints(metric_cols, _FINANCE_HINTS):
            return "financial_time_series"
        if _match_hints(all_cols, _PRODUCT_HINTS):
            return "product_operations"
        if _match_hints(all_cols, _CUSTOMER_HINTS):
            return "customer_behavior"
        return "time_series_business"
    if metric_cols and dim_cols:
        if _match_hints(all_cols, _FINANCE_HINTS):
            return "financial_snapshot"
        if _match_hints(all_cols, _PRODUCT_HINTS):
            return "product_mix"
        if _match_hints(all_cols, _OPS_HINTS):
            return "operations_snapshot"
        return "categorical_comparison"
    if dim_cols and not metric_cols:
        if _match_hints(all_cols, _ENTITY_HINTS) or len(dim_cols) >= 3:
            return "entity_profile"
        return "categorical_profile"
    if metric_cols:
        return "numeric_profile"
    return "generic_profile"


def _scenario_label(scenario: str) -> str:
    labels = {
        "financial_time_series": "财务时序分析",
        "product_operations": "产品与运营分析",
        "customer_behavior": "客户行为分析",
        "time_series_business": "经营趋势分析",
        "financial_snapshot": "财务结构分析",
        "product_mix": "产品结构分析",
        "operations_snapshot": "运营效率分析",
        "categorical_comparison": "分类对比分析",
        "entity_profile": "数据画像分析",
        "categorical_profile": "分类画像分析",
        "numeric_profile": "数值画像分析",
        "generic_profile": "通用数据画像",
    }
    return labels.get(scenario, "通用数据分析")


def _time_range(df: pd.DataFrame, time_col: Optional[str]) -> Dict[str, Any]:
    if not time_col or time_col not in df.columns:
        return {}
    series = pd.to_datetime(df[time_col], errors="coerce").dropna()
    if series.empty:
        return {}
    return {
        "start": str(series.min()),
        "end": str(series.max()),
        "period_count": int(series.nunique()),
    }


def run(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    读取数据源，返回扩充后的 context。
    context 需包含: datasource { type, config }，其中 config 含 file_path (csv) 或连接信息 (mysql)
    """
    ds = context.get("datasource") or {}
    ds_type = (ds.get("type") or "csv").lower()
    config = ds.get("config") or {}
    options = context.get("options") if isinstance(context.get("options"), dict) else {}
    max_rows = int(options.get("max_rows") or 10000)
    max_file_mb = float(options.get("max_file_mb") or 10)
    if ds_type == "mysql" and not bool(options.get("enable_mysql", True)):
        raise ValueError("免费版暂不支持 MySQL 数据源。输入“升级套餐”可查看付费版入口。")

    if ds_type in ("csv", "excel"):
        file_path = config.get("file_path") or config.get("path") or ""
        if not file_path or not os.path.isfile(file_path):
            raise FileNotFoundError(f"数据文件不存在: {file_path}")
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > max_file_mb:
            raise ValueError(f"单文件需 ≤ {max_file_mb:.0f}MB，当前 {size_mb:.1f}MB")

        if file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path, nrows=max_rows)
        else:
            df = pd.read_csv(file_path, nrows=max_rows, encoding="utf-8-sig")

    elif ds_type == "mysql":
        import mysql.connector

        conn = mysql.connector.connect(
            host=config.get("host", "localhost"),
            port=config.get("port", 3306),
            user=config.get("user"),
            password=config.get("password"),
            database=config.get("database"),
        )
        sql = config.get("sql") or f"SELECT * FROM {config.get('table', '')} LIMIT {max_rows}"
        df = pd.read_sql(sql, conn)
        conn.close()
    else:
        raise ValueError(f"不支持的数据源类型: {ds_type}")

    columns: List[Dict[str, Any]] = []
    profile_cols: List[Dict[str, Any]] = []
    n_rows = len(df)

    for col in df.columns:
        st = infer_column_type(df[col])
        role = "time" if st == "time" else ("measure" if st == "metric" else "dimension")
        null_ct = int(df[col].isna().sum())
        try:
            nuniq = int(df[col].nunique(dropna=True))
        except Exception:
            nuniq = 0
        top_values: List[str] = []
        try:
            top_values = [str(v) for v in df[col].astype(str).value_counts(dropna=True).head(3).index.tolist()]
        except Exception:
            pass
        columns.append(
            {
                "name": str(col),
                "semanticType": st,
                "dtype": str(df[col].dtype),
                "role": role,
            }
        )
        profile_cols.append(
            {
                "name": str(col),
                "semanticType": st,
                "dtype": str(df[col].dtype),
                "null_count": null_ct,
                "null_pct": round(100.0 * null_ct / n_rows, 2) if n_rows else 0.0,
                "unique_count": nuniq,
                "top_values": top_values,
            }
        )

    for c in columns:
        if c.get("semanticType") == "time":
            cn = c["name"]
            try:
                df[cn] = pd.to_datetime(df[cn], errors="coerce")
            except Exception:
                pass

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            mean_value = df[col].mean()
            fill_value = 0 if pd.isna(mean_value) else mean_value
            df[col] = df[col].fillna(fill_value)
        else:
            mode = df[col].mode(dropna=True)
            fill_value = mode.iloc[0] if not mode.empty else ""
            df[col] = df[col].fillna(fill_value)

    time_cols = [c["name"] for c in columns if c.get("semanticType") == "time"]
    metric_cols = [c["name"] for c in columns if c.get("semanticType") == "metric"]
    dim_cols = [c["name"] for c in columns if c.get("semanticType") == "dimension"]
    scenario = _infer_scenario(time_cols, metric_cols, dim_cols)

    high_missing = [p["name"] for p in profile_cols if p.get("null_pct", 0) >= 30]
    total_missing = sum(int(p.get("null_count", 0)) for p in profile_cols)
    total_cells = max(len(df.columns) * max(len(df), 1), 1)

    context["df"] = df
    context["schema"] = {
        "columns": columns,
        "row_count": len(df),
        "column_count": len(df.columns),
        "profile": {"columns": profile_cols},
        "time_columns": time_cols,
        "metric_columns": metric_cols,
        "dimension_columns": dim_cols,
        "detected_time_column": time_cols[0] if time_cols else None,
        "time_range": _time_range(df, time_cols[0] if time_cols else None),
        "scenario": scenario,
        "scenario_label": _scenario_label(scenario),
        "data_quality": {
            "high_missing_columns": high_missing,
            "total_missing_pct": round(100.0 * total_missing / total_cells, 2),
        },
    }
    return context
