#!/usr/bin/env python3
"""
biz-data-insight 异常检测脚本

检测业务数据中的异常值，支持标准差（sigma）和四分位距（IQR）两种方法。
此功能仅限付费用户使用。

用法示例:
    python3 anomaly_detector.py --data '{"values": [100, 102, 98, 105, 250, 99], "labels": ["1月","2月","3月","4月","5月","6月"]}'
    python3 anomaly_detector.py --data-file ./metrics.json --method both
"""

import argparse
import json
import math
import sys
from typing import Any, Dict, List, Optional

from utils import output_success, output_error, check_subscription, format_number


# ============================================================
# 统计计算
# ============================================================

def _mean(values: List[float]) -> float:
    """计算均值。"""
    return sum(values) / len(values)


def _std(values: List[float], mean_val: float) -> float:
    """计算总体标准差。"""
    variance = sum((v - mean_val) ** 2 for v in values) / len(values)
    return math.sqrt(variance)


def _percentile(sorted_values: List[float], p: float) -> float:
    """使用线性插值计算百分位数。

    Args:
        sorted_values: 已排序的数值列表。
        p: 百分位数（0-100）。

    Returns:
        对应百分位的数值。
    """
    n = len(sorted_values)
    k = (p / 100.0) * (n - 1)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_values[int(k)]
    return sorted_values[f] * (c - k) + sorted_values[c] * (k - f)


# ============================================================
# 异常检测方法
# ============================================================

def detect_sigma(
    values: List[float],
    labels: List[str],
    metric_name: str,
    unit: str,
    sigma_threshold: float = 2.0,
) -> List[Dict[str, Any]]:
    """使用标准差方法检测异常值。

    判定规则:
        - |value - mean| > 2σ: severity = "warning"
        - |value - mean| > 3σ: severity = "critical"

    Args:
        values: 数值列表。
        labels: 对应的标签列表。
        metric_name: 指标名称。
        unit: 数值单位。
        sigma_threshold: 判定异常的标准差倍数阈值，默认 2.0。

    Returns:
        检测到的异常列表。
    """
    anomalies = []
    mean_val = _mean(values)
    std_val = _std(values, mean_val)

    if std_val == 0:
        return anomalies

    for i, value in enumerate(values):
        deviation = abs(value - mean_val) / std_val
        if deviation > sigma_threshold:
            severity = "critical" if deviation > 3.0 else "warning"
            direction = "偏高" if value > mean_val else "偏低"
            description = (
                f"{metric_name}在{labels[i]}异常{direction}"
                f"（{format_number(value, 2)}{unit}），"
                f"超出均值{round(deviation, 1)}个标准差"
            )
            anomalies.append({
                "index": i,
                "label": labels[i],
                "value": value,
                "metric_name": metric_name,
                "method": "sigma",
                "severity": severity,
                "description": description,
                "stats": {
                    "mean": round(mean_val, 2),
                    "std": round(std_val, 2),
                    "deviation": round(deviation, 1),
                },
            })

    return anomalies


def detect_iqr(
    values: List[float],
    labels: List[str],
    metric_name: str,
    unit: str,
) -> List[Dict[str, Any]]:
    """使用四分位距（IQR）方法检测异常值。

    判定规则:
        - 超出 1.5*IQR 范围: severity = "warning"
        - 超出 3*IQR 范围: severity = "critical"

    Args:
        values: 数值列表。
        labels: 对应的标签列表。
        metric_name: 指标名称。
        unit: 数值单位。

    Returns:
        检测到的异常列表。
    """
    anomalies = []
    sorted_vals = sorted(values)

    q1 = _percentile(sorted_vals, 25)
    q3 = _percentile(sorted_vals, 75)
    iqr = q3 - q1

    if iqr == 0:
        return anomalies

    lower_warning = q1 - 1.5 * iqr
    upper_warning = q3 + 1.5 * iqr
    lower_critical = q1 - 3.0 * iqr
    upper_critical = q3 + 3.0 * iqr

    for i, value in enumerate(values):
        if value < lower_warning or value > upper_warning:
            if value < lower_critical or value > upper_critical:
                severity = "critical"
            else:
                severity = "warning"

            direction = "偏高" if value > upper_warning else "偏低"
            description = (
                f"{metric_name}在{labels[i]}异常{direction}"
                f"（{format_number(value, 2)}{unit}），"
                f"超出IQR正常范围"
            )
            anomalies.append({
                "index": i,
                "label": labels[i],
                "value": value,
                "metric_name": metric_name,
                "method": "iqr",
                "severity": severity,
                "description": description,
                "stats": {
                    "q1": round(q1, 2),
                    "q3": round(q3, 2),
                    "iqr": round(iqr, 2),
                    "lower_bound": round(lower_warning, 2),
                    "upper_bound": round(upper_warning, 2),
                },
            })

    return anomalies


# ============================================================
# 数据解析与主逻辑
# ============================================================

def _parse_metrics(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """将输入数据统一解析为指标列表。

    支持单指标格式和多指标格式（metrics 数组）。

    Args:
        data: 输入的 JSON 数据字典。

    Returns:
        指标列表，每个元素包含 name、values、labels、unit。

    Raises:
        ValueError: 当数据格式不合法时抛出。
    """
    if "metrics" in data:
        # 多指标格式
        metrics = data["metrics"]
        if not isinstance(metrics, list) or len(metrics) == 0:
            raise ValueError("metrics 必须为非空数组")
        result = []
        for idx, m in enumerate(metrics):
            if "values" not in m:
                raise ValueError(f"第 {idx + 1} 个指标缺少 values 字段")
            values = m["values"]
            labels = m.get("labels", [str(i + 1) for i in range(len(values))])
            if len(labels) != len(values):
                raise ValueError(
                    f"第 {idx + 1} 个指标的 labels 数量（{len(labels)}）"
                    f"与 values 数量（{len(values)}）不一致"
                )
            result.append({
                "name": m.get("name", f"指标{idx + 1}"),
                "values": [float(v) for v in values],
                "labels": labels,
                "unit": m.get("unit", ""),
            })
        return result
    elif "values" in data:
        # 单指标格式
        values = data["values"]
        labels = data.get("labels", [str(i + 1) for i in range(len(values))])
        if len(labels) != len(values):
            raise ValueError(
                f"labels 数量（{len(labels)}）与 values 数量（{len(values)}）不一致"
            )
        return [{
            "name": data.get("metric_name", "数据"),
            "values": [float(v) for v in values],
            "labels": labels,
            "unit": data.get("unit", ""),
        }]
    else:
        raise ValueError("输入数据必须包含 values 或 metrics 字段")


def run_detection(
    data: Dict[str, Any],
    method: str = "both",
    sigma_threshold: float = 2.0,
) -> Dict[str, Any]:
    """执行异常检测并返回结果。

    Args:
        data: 输入数据字典。
        method: 检测方法，"sigma"、"iqr" 或 "both"。
        sigma_threshold: 标准差阈值，默认 2.0。

    Returns:
        包含 anomalies 和 summary 的结果字典。
    """
    metrics = _parse_metrics(data)

    all_anomalies: List[Dict[str, Any]] = []
    total_checked = 0
    methods_used: List[str] = []

    if method in ("sigma", "both"):
        methods_used.append("sigma")
    if method in ("iqr", "both"):
        methods_used.append("iqr")

    for metric in metrics:
        values = metric["values"]
        labels = metric["labels"]
        name = metric["name"]
        unit = metric["unit"]
        total_checked += len(values)

        if len(values) < 3:
            # 数据点过少，跳过检测
            continue

        if method in ("sigma", "both"):
            all_anomalies.extend(
                detect_sigma(values, labels, name, unit, sigma_threshold)
            )
        if method in ("iqr", "both"):
            all_anomalies.extend(
                detect_iqr(values, labels, name, unit)
            )

    # 去重：同一索引同一指标可能被两种方法同时检出，保留全部但统计去重数量
    severity_dist = {"warning": 0, "critical": 0}
    for a in all_anomalies:
        severity_dist[a["severity"]] += 1

    return {
        "anomalies": all_anomalies,
        "summary": {
            "total_checked": total_checked,
            "anomaly_count": len(all_anomalies),
            "methods_used": methods_used,
            "severity_distribution": severity_dist,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        description="业务数据异常检测工具（付费功能）",
    )
    parser.add_argument(
        "--data",
        type=str,
        default=None,
        help="JSON 格式的数据字符串",
    )
    parser.add_argument(
        "--data-file",
        type=str,
        default=None,
        help="JSON 数据文件路径（与 --data 二选一）",
    )
    parser.add_argument(
        "--method",
        type=str,
        choices=["sigma", "iqr", "both"],
        default="both",
        help="检测方法: sigma（标准差）、iqr（四分位距）、both（两者都用），默认 both",
    )
    parser.add_argument(
        "--sigma-threshold",
        type=float,
        default=2.0,
        help="标准差检测阈值，默认 2.0",
    )
    parser.add_argument(
        "--tier",
        type=str,
        default=None,
        help="订阅等级覆盖（free 或 paid）",
    )
    return parser


def main() -> None:
    """主入口函数。"""
    parser = build_parser()
    args = parser.parse_args()

    # 订阅校验：仅付费用户可使用
    try:
        subscription = check_subscription(args.tier)
    except ValueError as e:
        output_error(str(e), code="SUBSCRIPTION_ERROR")
        sys.exit(1)

    if subscription["tier"] != "paid":
        output_error(
            "异常检测为付费功能，请升级到付费版（¥99/月）",
            code="SUBSCRIPTION_REQUIRED",
        )
        sys.exit(1)

    # 读取输入数据
    if args.data is not None:
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError as e:
            output_error(f"JSON 解析失败: {e}", code="INVALID_INPUT")
            sys.exit(1)
    elif args.data_file is not None:
        try:
            with open(args.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            output_error(f"文件不存在: {args.data_file}", code="FILE_NOT_FOUND")
            sys.exit(1)
        except json.JSONDecodeError as e:
            output_error(f"文件 JSON 解析失败: {e}", code="INVALID_INPUT")
            sys.exit(1)
        except OSError as e:
            output_error(f"文件读取失败: {e}", code="FILE_ERROR")
            sys.exit(1)
    else:
        output_error("请通过 --data 或 --data-file 提供输入数据", code="MISSING_INPUT")
        sys.exit(1)

    if not isinstance(data, dict):
        output_error(
            f"输入数据必须为 JSON 对象，当前类型为 {type(data).__name__}",
            code="INVALID_INPUT",
        )
        sys.exit(1)

    # 执行异常检测
    try:
        result = run_detection(
            data=data,
            method=args.method,
            sigma_threshold=args.sigma_threshold,
        )
    except ValueError as e:
        output_error(str(e), code="DETECTION_ERROR")
        sys.exit(1)

    output_success(result)


if __name__ == "__main__":
    main()
