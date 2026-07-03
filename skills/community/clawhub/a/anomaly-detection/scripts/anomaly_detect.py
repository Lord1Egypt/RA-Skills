#!/usr/bin/env python3
"""
Chronos-2 时序异常检测引擎
Usage: python anomaly_detect.py --input data.csv --output results/ [--prediction-length 30]

基于 Chronos-2 零样本时序大模型的异常检测。
工作流：数据加载 → Chronos-2预测 → 残差计算 → 多方法融合检测 → 异常分类 → JSON输出
"""

import argparse
import json
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path

warnings.filterwarnings("ignore")


def install_dependencies():
    """检查并安装缺失的依赖"""
    deps = {
        "pandas": "pandas",
        "numpy": "numpy",
        "plotly": "plotly",
        "openpyxl": "openpyxl",
        "scipy": "scipy",
    }
    missing = []
    for module, pkg in deps.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(pkg)

    try:
        __import__("chronos")
    except ImportError:
        missing.append("chronos-forecasting")

    if missing:
        print(f"[INFO] 安装依赖: {', '.join(missing)}")
        import subprocess

        env = os.environ.copy()
        if "HF_ENDPOINT" not in env:
            env["HF_ENDPOINT"] = "https://hf-mirror.com"

        for pkg in missing:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg, "-q"],
                env=env,
            )
        print("[INFO] 依赖安装完成")


install_dependencies()

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats


def validate_and_load(input_path: str) -> pd.DataFrame:
    """加载并校验输入数据"""
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {input_path}")

    suffix = path.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(path, parse_dates=True)
    elif suffix in (".xlsx", ".xls"):
        df = pd.read_excel(path, parse_dates=True)
    elif suffix == ".json":
        df = pd.read_json(path)
    elif suffix == ".parquet":
        df = pd.read_parquet(path)
    else:
        raise ValueError(f"不支持的文件格式: {suffix}")

    cols = df.columns.tolist()
    print(f"[INFO] 检测到列: {cols}")

    # 找时间列
    time_col = None
    for c in cols:
        if c.lower() in ("timestamp", "date", "time", "日期", "时间", "ds"):
            time_col = c
            break
    if time_col is None:
        for c in cols:
            try:
                pd.to_datetime(df[c])
                time_col = c
                break
            except (ValueError, TypeError):
                continue
    if time_col is None:
        # 尝试将第一列当索引
        try:
            df.index = pd.to_datetime(df.iloc[:, 0])
            time_col = df.columns[0]
            df["_time"] = df.index
            time_col = "_time"
        except Exception:
            raise ValueError("无法识别时间列，请确保数据包含日期/时间列")

    # 找数值列
    target_col = None
    target_keywords = (
        "sales", "target", "value", "销量", "销售额", "数量", "amount", "y",
        "price", "价格", "metric", "指标", "count", "计数", "revenue", "收入",
        "traffic", "流量", "temperature", "温度", "cpu", "memory", "内存",
    )
    for c in cols:
        if c != time_col and c.lower() in target_keywords:
            target_col = c
            break
    if target_col is None:
        for c in cols:
            if c != time_col and pd.api.types.is_numeric_dtype(df[c]):
                target_col = c
                break
    if target_col is None:
        raise ValueError("无法找到数值目标列，请确保数据包含数值列")

    print(f"[INFO] 时间列: {time_col}, 目标列: {target_col}")

    df = df[[time_col, target_col]].copy()
    df.columns = ["timestamp", "target"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    df["target"] = pd.to_numeric(df["target"], errors="coerce")

    # 去重（同一时间点取均值）
    df = df.groupby("timestamp", as_index=False)["target"].mean()

    # 缺失值处理
    n_missing = df["target"].isna().sum()
    if n_missing > 0:
        print(f"[WARN] 发现 {n_missing} 个缺失值，使用线性插值")
        df["target"] = df["target"].interpolate(method="linear").ffill().bfill()

    # 推断频率
    time_diffs = df["timestamp"].diff().dropna()
    freq_seconds = time_diffs.median().total_seconds()
    if freq_seconds < 60:
        freq = "S"
    elif freq_seconds < 3600:
        freq = "T"
    elif freq_seconds < 86400:
        freq = "H"
    elif freq_seconds < 604800:
        freq = "D"
    elif freq_seconds < 2592000:
        freq = "W"
    else:
        freq = "M"

    print(f"[INFO] 推断频率: {freq}, 数据长度: {len(df)}, 缺失值: {n_missing}")

    if len(df) < 20:
        print("[WARN] 数据点少于 20，异常检测结果可能不够可靠")

    return df


def run_chronos_forecast(
    df: pd.DataFrame,
    prediction_length: int = 1,
    context_length: int = 2048,
) -> tuple:
    """
    运行 Chronos-2 逐点回测式预测。
    返回 (forecast_values, forecast_timestamps): 每个历史点的预测值
    """
    from chronos import Chronos2Pipeline

    print("[INFO] 加载 Chronos-2 模型...")
    pipeline = Chronos2Pipeline.from_pretrained(
        "amazon/chronos-2",
        device_map="cpu",
    )

    n = len(df)
    # 使用滑动窗口：用前 window 个点预测下一个点
    min_history = max(10, n // 5)  # 至少需要10个历史点

    forecasts = []
    forecast_timestamps = []

    # 对每个点，用其之前的数据预测
    step = max(1, n // 50)  # 如果数据量大，每隔几个点预测一次以提高效率
    if n > 500:
        print(f"[INFO] 数据量较大({n}点)，每隔 {step} 点做一次回测预测")

    indices = list(range(min_history, n, step))
    total = len(indices)
    print(f"[INFO] 回测预测: 共 {total} 个检验点")

    for idx, i in enumerate(indices):
        if (idx + 1) % max(1, total // 10) == 0:
            print(f"  进度: {idx + 1}/{total}")

        hist_slice = df.iloc[:i].copy()
        hist_slice = hist_slice.tail(context_length)

        actual_target = df.iloc[i]["target"]
        actual_ts = df.iloc[i]["timestamp"]

        df_model = hist_slice[["timestamp", "target"]].copy()
        df_model["item_id"] = "series_1"
        df_model = df_model[["item_id", "timestamp", "target"]]

        try:
            fc_df = pipeline.predict_df(
                df_model,
                prediction_length=1,
                quantile_levels=[0.1, 0.5, 0.9],
                id_column="item_id",
                timestamp_column="timestamp",
                target="target",
            )
            pred_value = fc_df["0.5"].iloc[0]
        except Exception as e:
            print(f"  [WARN] 预测失败 idx={i}: {e}，使用简单均值")
            pred_value = hist_slice["target"].mean()

        forecasts.append({
            "timestamp": str(actual_ts),
            "actual": float(actual_target),
            "predicted": float(pred_value),
        })
        forecast_timestamps.append(actual_ts)

    print("[INFO] 回测预测完成")
    return forecasts, forecast_timestamps


def detect_anomalies_zscore(residuals: np.ndarray, threshold: float = 2.5) -> np.ndarray:
    """Z-score 异常检测"""
    if len(residuals) < 4:
        return np.zeros(len(residuals), dtype=bool)
    mean = np.mean(residuals)
    std = np.std(residuals)
    if std < 1e-10:
        return np.zeros(len(residuals), dtype=bool)
    z_scores = np.abs((residuals - mean) / std)
    return z_scores > threshold


def detect_anomalies_modified_zscore(residuals: np.ndarray, threshold: float = 3.0) -> np.ndarray:
    """改进 Z-score (基于 MAD，更鲁棒)"""
    if len(residuals) < 4:
        return np.zeros(len(residuals), dtype=bool)
    median = np.median(residuals)
    mad = np.median(np.abs(residuals - median))
    if mad < 1e-10:
        return np.zeros(len(residuals), dtype=bool)
    modified_z = 0.6745 * np.abs(residuals - median) / mad
    return modified_z > threshold


def detect_anomalies_iqr(residuals: np.ndarray, multiplier: float = 1.5) -> np.ndarray:
    """IQR 异常检测"""
    if len(residuals) < 4:
        return np.zeros(len(residuals), dtype=bool)
    q1 = np.percentile(residuals, 25)
    q3 = np.percentile(residuals, 75)
    iqr = q3 - q1
    if iqr < 1e-10:
        return np.zeros(len(residuals), dtype=bool)
    lower = q1 - multiplier * iqr
    upper = q3 + multiplier * iqr
    return (residuals < lower) | (residuals > upper)


def detect_anomalies_moving_avg(series: np.ndarray, window: int = 5, threshold: float = 2.0) -> np.ndarray:
    """移动平均偏离检测（检测趋势突变）"""
    if len(series) < window:
        return np.zeros(len(series), dtype=bool)
    moving_avg = pd.Series(series).rolling(window=window, center=True).mean().fillna(method="bfill").fillna(method="ffill").values
    deviations = np.abs(series - moving_avg)
    threshold_val = np.std(deviations) * threshold if np.std(deviations) > 1e-10 else np.median(deviations) * 3
    return deviations > threshold_val


def classify_anomaly_type(
    anomaly_flags: np.ndarray,
    residuals: np.ndarray,
    values: np.ndarray,
    idx: int,
) -> str:
    """分类异常类型"""
    is_anomaly = anomaly_flags[idx]
    if not is_anomaly:
        return "normal"

    # 检查前后连续性 → 集体异常
    consecutive_count = 1
    j = idx + 1
    while j < len(anomaly_flags) and anomaly_flags[j]:
        consecutive_count += 1
        j += 1
    j = idx - 1
    while j >= 0 and anomaly_flags[j]:
        consecutive_count += 1
        j -= 1

    if consecutive_count >= 3:
        # 检查是否是水平偏移（连续异常且残差同向）
        if idx > 0 and idx < len(anomaly_flags) - 1:
            pre_mean = np.mean(values[max(0, idx - 10):idx])
            post_mean = np.mean(values[idx:min(len(values), idx + 10)])
            if abs(post_mean - pre_mean) / (abs(pre_mean) + 1e-10) > 0.3:
                return "level_shift"
        return "collective"
    elif consecutive_count == 2:
        return "contextual"
    else:
        return "point"


def compute_severity(z_score: float, iqr_ratio: float) -> str:
    """根据偏离程度判定严重度"""
    if abs(z_score) > 3.5 or iqr_ratio > 3.0:
        return "P0_严重"
    elif abs(z_score) > 2.5 or iqr_ratio > 1.5:
        return "P1_警告"
    else:
        return "P2_轻微"


def detect_all_anomalies(
    df: pd.DataFrame,
    forecasts: list,
    zscore_threshold: float = 2.5,
    mad_threshold: float = 3.0,
    iqr_multiplier: float = 1.5,
) -> dict:
    """融合多种方法进行异常检测"""
    n = len(forecasts)
    actuals = np.array([f["actual"] for f in forecasts])
    predicted = np.array([f["predicted"] for f in forecasts])
    residuals = actuals - predicted

    # 方法1: Z-score
    flag_zscore = detect_anomalies_zscore(residuals, zscore_threshold)

    # 方法2: 改进 Z-score (MAD)
    flag_mad = detect_anomalies_modified_zscore(residuals, mad_threshold)

    # 方法3: IQR
    flag_iqr = detect_anomalies_iqr(residuals, iqr_multiplier)

    # 方法4: 移动平均偏离
    flag_ma = detect_anomalies_moving_avg(actuals, window=max(3, n // 10))

    # 融合：至少两种方法标记才认为是异常（减少误报）
    votes = flag_zscore.astype(int) + flag_mad.astype(int) + flag_iqr.astype(int) + flag_ma.astype(int)
    anomaly_flags = votes >= 2

    # 计算每个点的 Z-score 和 IQR 比率（用于严重度判定）
    mean_res = np.mean(residuals)
    std_res = np.std(residuals) if np.std(residuals) > 1e-10 else 1.0
    z_scores = np.abs((residuals - mean_res) / std_res)

    q1 = np.percentile(residuals, 25)
    q3 = np.percentile(residuals, 75)
    iqr = q3 - q1 if (q3 - q1) > 1e-10 else 1.0
    iqr_ratios = np.abs(residuals - np.median(residuals)) / (iqr / 2)

    # 构建异常详情
    anomalies = []
    anomaly_summary_count = {"P0_严重": 0, "P1_警告": 0, "P2_轻微": 0}

    for i in range(n):
        if anomaly_flags[i]:
            a_type = classify_anomaly_type(anomaly_flags, residuals, actuals, i)
            severity = compute_severity(z_scores[i], iqr_ratios[i])
            direction = "偏高" if residuals[i] > 0 else "偏低"

            anomaly = {
                "index": i,
                "timestamp": forecasts[i]["timestamp"],
                "actual": round(actuals[i], 4),
                "predicted": round(predicted[i], 4),
                "residual": round(residuals[i], 4),
                "residual_pct": round(residuals[i] / (abs(predicted[i]) + 1e-10) * 100, 2),
                "z_score": round(z_scores[i], 3),
                "iqr_ratio": round(iqr_ratios[i], 3),
                "type": a_type,
                "severity": severity,
                "direction": direction,
                "vote_count": int(votes[i]),
                "methods": {
                    "zscore": bool(flag_zscore[i]),
                    "mad": bool(flag_mad[i]),
                    "iqr": bool(flag_iqr[i]),
                    "moving_avg": bool(flag_ma[i]),
                },
            }
            anomalies.append(anomaly)
            anomaly_summary_count[severity] += 1

    # 计算统计摘要
    total_points = n
    anomaly_count = len(anomalies)
    anomaly_rate = anomaly_count / total_points * 100 if total_points > 0 else 0

    # 按类型统计
    type_counts = {}
    for a in anomalies:
        t = a["type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    summary = {
        "total_points": total_points,
        "anomaly_count": anomaly_count,
        "anomaly_rate": round(anomaly_rate, 2),
        "severity_breakdown": anomaly_summary_count,
        "type_breakdown": type_counts,
        "residual_stats": {
            "mean": round(float(np.mean(residuals)), 4),
            "std": round(float(np.std(residuals)), 4),
            "min": round(float(np.min(residuals)), 4),
            "max": round(float(np.max(residuals)), 4),
            "mae": round(float(np.mean(np.abs(residuals))), 4),
            "rmse": round(float(np.sqrt(np.mean(residuals**2))), 4),
        },
        "methods_used": {
            "zscore_threshold": zscore_threshold,
            "mad_threshold": mad_threshold,
            "iqr_multiplier": iqr_multiplier,
            "fusion_rule": "至少2种方法标记才确认为异常",
        },
        "detection_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # 准备全部时序数据（含预测值和残差）
    time_series = []
    for i, f in enumerate(forecasts):
        point = {
            "timestamp": f["timestamp"],
            "actual": f["actual"],
            "predicted": round(predicted[i], 4),
            "residual": round(residuals[i], 4),
            "z_score": round(z_scores[i], 3),
            "is_anomaly": bool(anomaly_flags[i]),
        }
        time_series.append(point)

    return {
        "summary": summary,
        "anomalies": anomalies,
        "time_series": time_series,
        "metadata": {
            "model": "amazon/chronos-2",
            "data_points": total_points,
            "anomaly_count": anomaly_count,
            "detection_methods": ["zscore", "modified_zscore_mad", "iqr", "moving_average"],
            "fusion_strategy": "majority_voting_2_of_4",
        },
    }


def save_results(results: dict, output_dir: str, df: pd.DataFrame):
    """保存检测结果"""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # JSON 主数据
    json_path = out / "anomaly_data.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[INFO] JSON 数据已保存: {json_path}")

    # CSV 异常明细
    if results["anomalies"]:
        anomalies_df = pd.DataFrame(results["anomalies"])
        csv_path = out / "anomalies.csv"
        anomalies_df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"[INFO] 异常明细已保存: {csv_path}")

    # CSV 全量时序
    ts_df = pd.DataFrame(results["time_series"])
    ts_csv = out / "time_series_with_detection.csv"
    ts_df.to_csv(ts_csv, index=False, encoding="utf-8-sig")
    print(f"[INFO] 全量时序数据已保存: {ts_csv}")


def main():
    parser = argparse.ArgumentParser(description="Chronos-2 时序异常检测引擎")
    parser.add_argument("--input", "-i", required=True, help="输入数据文件 (CSV/Excel/JSON)")
    parser.add_argument("--output", "-o", required=True, help="输出目录")
    parser.add_argument(
        "--zscore-threshold", type=float, default=2.5, help="Z-score 异常阈值 (默认 2.5)"
    )
    parser.add_argument(
        "--mad-threshold", type=float, default=3.0, help="改进 Z-score (MAD) 阈值 (默认 3.0)"
    )
    parser.add_argument(
        "--iqr-multiplier", type=float, default=1.5, help="IQR 乘数 (默认 1.5)"
    )
    parser.add_argument("--context-length", "-c", type=int, default=2048, help="最大上下文长度")
    parser.add_argument("--hf-endpoint", type=str, default=None, help="HuggingFace 镜像地址")

    args = parser.parse_args()

    if args.hf_endpoint:
        os.environ["HF_ENDPOINT"] = args.hf_endpoint
    elif "HF_ENDPOINT" not in os.environ:
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

    # Step 1: 加载和校验
    print("=" * 55)
    print("🔍 Chronos-2 时序异常检测引擎")
    print("=" * 55)
    df = validate_and_load(args.input)

    # Step 2: Chronos-2 回测预测
    print(f"\n[INFO] 开始回测预测，共 {len(df)} 个数据点...")
    forecasts, _ = run_chronos_forecast(df, context_length=args.context_length)

    # Step 3: 多方法异常检测
    print("\n[INFO] 多方法融合异常检测...")
    results = detect_all_anomalies(
        df,
        forecasts,
        zscore_threshold=args.zscore_threshold,
        mad_threshold=args.mad_threshold,
        iqr_multiplier=args.iqr_multiplier,
    )

    # Step 4: 保存结果
    save_results(results, args.output, df)

    # 打印摘要
    s = results["summary"]
    print(f"\n{'=' * 55}")
    print(f"✅ 异常检测完成！")
    print(f"   数据点数:     {s['total_points']}")
    print(f"   异常点数:     {s['anomaly_count']} ({s['anomaly_rate']}%)")
    print(f"   严重级别:     P0严重={s['severity_breakdown']['P0_严重']}, "
          f"P1警告={s['severity_breakdown']['P1_警告']}, "
          f"P2轻微={s['severity_breakdown']['P2_轻微']}")
    print(f"   异常类型:     {s['type_breakdown']}")
    print(f"   残差 MAE:     {s['residual_stats']['mae']}")
    print(f"   残差 RMSE:    {s['residual_stats']['rmse']}")
    print(f"   输出目录:     {args.output}")
    print(f"{'=' * 55}")


if __name__ == "__main__":
    main()
