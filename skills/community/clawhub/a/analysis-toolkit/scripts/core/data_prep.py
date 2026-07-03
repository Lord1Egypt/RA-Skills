"""
数据准备引擎 — LLM 给出结构化指令，Python 自动执行数据清理与转换。

## 工作流程

```
用户原始数据 (Excel/CSV/数组)
  ↓
LLM 分析 → 生成 prep_instructions
  ↓
data_prep.py 执行 instructions → 清理后的数据
  ↓
validator.py 校验（列存在、数据量、NaN、类型）
  ↓
计算函数执行
```

## LLM 指令格式

```python
prep_instructions = {
    "rename": {
        "浓度ppm": "x",           # 用户数据列 → 函数期望列名
        "响应值": "y",
    },
    "drop_columns": ["备注", "批号"],   # 删除无关列
    "type_cast": {
        "日期": "datetime",            # 支持: datetime, float, int, str, category
        "结果": "float",
    },
    "dropna": True,                     # 删除包含 NaN 的行
    "filter": {                         # 行过滤（可选）
        "column": "结果",
        "min": 0,
        "max": 1000,
        "remove_outliers": True,        # 超出 mean±3σ 的标记为 NaN
    },
    "aggregate": {                      # 聚合（可选，用于时序/分组数据）
        "group_by": "实验室",
        "agg_column": "结果",
        "agg_func": "mean",             # mean / median / std / count
    },
}
```
"""
import pandas as pd
import numpy as np
from typing import Optional


def _warn(msg: str):
    """统一警告输出"""
    import warnings
    warnings.warn(f"[数据准备] {msg}")


def execute_prep(data, instructions: dict):
    """
    执行 LLM 提供的数据准备指令。

    Parameters
    ----------
    data : pd.DataFrame | list | dict | np.ndarray
        原始数据
    instructions : dict
        LLM 生成的数据准备指令

    Returns
    -------
    dict
        {
            "data": pd.DataFrame | array-like,  # 准备后的数据
            "success": bool,
            "applied_steps": list[str],          # 实际执行的步骤
            "warnings": list[str],               # 警告/提示
            "error": str | None,                 # 错误信息
        }
    """
    applied = []
    warns = []

    # ── 第 0 步：统一转为 DataFrame ──
    df = _to_dataframe(data)
    if df is None:
        return {
            "data": data,
            "success": False,
            "applied_steps": [],
            "warnings": [],
            "error": "无法识别输入数据类型。支持: DataFrame, CSV 路径, 字典列表, 数组",
        }

    original_rows = len(df)
    applied.append(f"加载数据: {original_rows} 行")

    # ── 第 1 步：列重命名 ──
    rename_map = instructions.get("rename", {})
    if rename_map:
        # 只重命名存在的列
        valid_rename = {k: v for k, v in rename_map.items() if k in df.columns}
        missing_rename = [k for k in rename_map if k not in df.columns]
        if valid_rename:
            df = df.rename(columns=valid_rename)
            applied.append(f"重命名列: {valid_rename}")
        if missing_rename:
            warns.append(f"重命名失败: 列 {missing_rename} 不存在")

    # ── 第 2 步：删除无用列 ──
    drop_cols = instructions.get("drop_columns", [])
    if drop_cols:
        existing_drop = [c for c in drop_cols if c in df.columns]
        if existing_drop:
            df = df.drop(columns=existing_drop)
            applied.append(f"删除列: {existing_drop}")

    # ── 第 3 步：类型转换 ──
    type_map = instructions.get("type_cast", {})
    for col, dtype in type_map.items():
        if col not in df.columns:
            warns.append(f"类型转换失败: 列 '{col}' 不存在")
            continue
        try:
            if dtype == "datetime":
                df[col] = pd.to_datetime(df[col], errors="coerce")
            elif dtype == "float":
                df[col] = pd.to_numeric(df[col], errors="coerce")
            elif dtype == "int":
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
            elif dtype == "str":
                df[col] = df[col].astype(str)
            elif dtype == "category":
                df[col] = df[col].astype("category")
            applied.append(f"类型转换: {col} → {dtype}")
        except Exception as e:
            warns.append(f"类型转换失败: {col} → {dtype} ({e})")

    # ── 第 4 步：删除空值行 ──
    if instructions.get("dropna", False):
        before = len(df)
        df = df.dropna()
        dropped = before - len(df)
        if dropped > 0:
            applied.append(f"删除 {dropped} 行包含空值的数据")

    # ── 第 5 步：行过滤 ──
    filter_cfg = instructions.get("filter", {})
    if filter_cfg:
        col = filter_cfg.get("column")
        if col and col in df.columns:
            before = len(df)
            min_val = filter_cfg.get("min")
            max_val = filter_cfg.get("max")
            if min_val is not None:
                df = df[df[col] >= min_val]
            if max_val is not None:
                df = df[df[col] <= max_val]
            if filter_cfg.get("remove_outliers", False):
                mean = df[col].mean()
                std = df[col].std()
                if std > 0:
                    outlier_mask = (df[col] >= mean - 3 * std) & (df[col] <= mean + 3 * std)
                    df = df[outlier_mask]
                    applied.append(f"删除异常值 (mean±3σ): {before - len(df)} 行")
                else:
                    warns.append(f"标准差为0，跳过异常值检测")
            filtered = before - len(df)
            if filtered > 0:
                applied.append(f"行过滤 '{col}': 移除 {filtered} 行")

    # ── 第 6 步：聚合 ──
    agg = instructions.get("aggregate", {})
    if agg and agg.get("group_by") and agg.get("agg_column"):
        gb = agg["group_by"]
        ac = agg["agg_column"]
        func = agg.get("agg_func", "mean")
        if gb in df.columns and ac in df.columns:
            df = df.groupby(gb, as_index=False)[ac].agg(func).reset_index()
            applied.append(f"聚合: 按 {gb} 分组, {ac} → {func}")
        else:
            warns.append(f"聚合失败: 分组列或聚合列不存在")

    after_rows = len(df) if isinstance(df, pd.DataFrame) else original_rows
    if after_rows < original_rows:
        warns.append(f"数据从 {original_rows} 行减少到 {after_rows} 行")
    if after_rows == 0:
        return {
            "data": df,
            "success": False,
            "applied_steps": applied,
            "warnings": warns + ["处理后数据为空，无法继续计算"],
            "error": "数据准备后为空",
        }

    # ── 返回原始数据还是 DataFrame？ ──
    # 如果输入是 array-like 且只有一个数值列，降维回数组
    result_data = df
    if isinstance(data, (list, np.ndarray)) and not isinstance(data, pd.DataFrame):
        num_cols = df.select_dtypes(include=[np.number]).columns
        if len(num_cols) == 1:
            result_data = df[num_cols[0]].values

    return {
        "data": result_data,
        "success": True,
        "applied_steps": applied,
        "warnings": warns,
        "error": None,
    }


# ═══════════════════════════════════════════════════════
# 格式校验器（LLM 传入数据后 → 计算前执行）
# ═══════════════════════════════════════════════════════

def validate(data, required_type=None, required_columns: list = None,
             min_rows: int = 1, min_groups: int = None) -> dict:
    """
    数据格式前置校验。在 LLM 提供/准备数据后、计算前执行。

    Parameters
    ----------
    data : pd.DataFrame | array-like | dict
    required_type : str, optional
        期望类型. "dataframe", "array", "dict"
    required_columns : list[str], optional
        DataFrame 下必需的列名
    min_rows : int
        最小数据行数（默认 1）
    min_groups : int, optional
        分组数最小值（用于 ANOVA 等场景）

    Returns
    -------
    dict
        {
            "valid": bool,
            "warnings": list[str],
            "errors": list[str],
            "n_rows": int,
        }
    """
    errors = []
    warnings = []

    # 空值检查
    if data is None:
        errors.append("数据为空（data=None），请提供数据后重试")
        return {"valid": False, "warnings": [], "errors": errors, "n_rows": 0}

    if isinstance(data, pd.DataFrame):
        n_rows = len(data)
        if n_rows == 0:
            errors.append("DataFrame 为空（0 行），请提供数据后重试")
        if n_rows < min_rows:
            warnings.append(f"数据仅 {n_rows} 行，建议至少 {min_rows} 行以获得可靠结果")

        # 必需列检查
        if required_columns:
            missing = [c for c in required_columns if c not in data.columns]
            if missing:
                errors.append(f"缺少必需列: {missing}")

        # 数值列 NaN 检查
        num_cols = data.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            nan_count = data[col].isna().sum()
            if nan_count > 0:
                warnings.append(f"列 '{col}' 有 {nan_count} 个空值，将被跳过")

        # 分组数检查
        if min_groups and required_columns:
            for col in required_columns:
                if col in data.columns:
                    n_groups = data[col].nunique()
                    if n_groups < min_groups:
                        errors.append(f"列 '{col}' 仅有 {n_groups} 个组，需要至少 {min_groups} 个")

    elif isinstance(data, (list, np.ndarray)):
        arr = np.asarray(data)
        n_rows = len(arr)
        if n_rows == 0:
            errors.append("数据为空（空数组），请提供数据后重试")
        if n_rows < min_rows:
            warnings.append(f"数据仅 {n_rows} 个点，建议至少 {min_rows} 个")
        # 检查 NaN
        if np.any(np.isnan(arr.astype(float))):
            warnings.append("数据中包含 NaN，将被跳过")

    elif isinstance(data, dict):
        n_rows = len(data)
        if required_columns:
            missing = [c for c in required_columns if c not in data]
            if missing:
                errors.append(f"字典中缺少必需键: {missing}")

    else:
        errors.append(f"不支持的数据类型: {type(data).__name__}")
        return {"valid": False, "warnings": [], "errors": errors, "n_rows": 0}

    return {
        "valid": len(errors) == 0,
        "warnings": warnings,
        "errors": errors,
        "n_rows": n_rows,
    }


# ═══════════════════════════════════════════════════════
# 内部工具
# ═══════════════════════════════════════════════════════

def _to_dataframe(data):
    """统一将输入转为 DataFrame"""
    if isinstance(data, pd.DataFrame):
        return data.copy()
    if isinstance(data, dict):
        return pd.DataFrame(data)
    if isinstance(data, (list, np.ndarray)):
        arr = list(data) if isinstance(data, np.ndarray) else data
        # 字典列表 → 直接展开为多列
        if arr and isinstance(arr[0], dict):
            return pd.DataFrame(arr)
        # 数值列表 → 单列 DataFrame
        arr_np = np.asarray(arr)
        if arr_np.ndim == 1:
            return pd.DataFrame({"value": arr_np})
        return pd.DataFrame(arr_np)
    return None


# ═══════════════════════════════════════════════════════
# 演示入口
# ═══════════════════════════════════════════════════════

def demo():
    """演示 LLM 指令 + Python 执行的完整流程"""
    try:
        import pandas as pd
    except ImportError:
        print("演示需要 pandas，请先安装: pip install pandas")
        return
    # 模拟用户提供的原始数据
    raw = [
        {"样品名": "标准1", "浓度ppm": 0, "响应值": 101, "备注": "空白"},
        {"样品名": "标准2", "浓度ppm": 5, "响应值": 32500, "备注": ""},
        {"样品名": "标准3", "浓度ppm": 10, "响应值": 66000, "备注": ""},
        {"样品名": "标准4", "浓度ppm": 15, "响应值": 91300, "备注": ""},
        {"样品名": "标准5", "浓度ppm": 20, "响应值": 133005, "备注": ""},
    ]

    # LLM 生成的指令（基于 接口指南 中的字段要求）
    ins = {
        "rename": {"浓度ppm": "x", "响应值": "y"},
        "drop_columns": ["样品名", "备注"],
        "type_cast": {"x": "float", "y": "float"},
        "dropna": True,
    }

    result = execute_prep(raw, ins)
    val = validate(result["data"],
                   required_type="dataframe",
                   required_columns=["x", "y"],
                   min_rows=3)

    print("=== 数据准备 ===")
    for step in result["applied_steps"]:
        print(f"  ✓ {step}")
    if result["warnings"]:
        for w in result["warnings"]:
            print(f"  ⚠ {w}")

    print("\n=== 格式校验 ===")
    if val["valid"]:
        print("  ✅ 数据格式正确")
    for w in val["warnings"]:
        print(f"  ⚠ {w}")
    for e in val["errors"]:
        print(f"  ✗ {e}")

    print("\n=== 准备后数据 ===")
    print(result["data"])


if __name__ == "__main__":
    demo()
