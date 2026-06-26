#!/usr/bin/env python3
"""
Prometheus Query Client for OpenClaw Metric Topics

This script provides a command-line interface to query OpenClaw metrics data
stored in Tencent Cloud CLS metric topics via Prometheus API.

Authentication:
    Credentials are read from TCCLI credential file.
    - SecretId is used as the username for Basic Auth.
    - SecretKey#Token is used as the password for Basic Auth (temporary credentials).
    
    Run `tccli auth login` to obtain credentials.

Usage Examples:
    # Instant query (single point in time)
    python prometheus_query.py --region ap-guangzhou --topic-id <topic_id> \
        --query "up" --instant

    # Range query (time series)
    python prometheus_query.py --region ap-guangzhou --topic-id <topic_id> \
        --query "rate(http_requests_total[5m])" \
        --start "2024-01-01T00:00:00Z" --end "2024-01-01T01:00:00Z" --step 60s

    # Query with relative time
    python prometheus_query.py --region ap-guangzhou --topic-id <topic_id> \
        --query "sum(rate(requests_total[5m]))" \
        --start-relative 1h --step 1m
"""

import sys
import json
import argparse
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from urllib.parse import urljoin

# 导入公共模块
from common import (
    get_credentials_tuple,
    validate_region,
    validate_topic_id,
    validate_label_name,
    sanitize_error_message,
    VALID_REGIONS,
)


def get_prometheus_url(region: str, topic_id: str) -> str:
    """
    Construct the Prometheus API URL.
    
    Args:
        region: 腾讯云地域（已经过验证）
        topic_id: 指标主题 ID（已经过验证）
        
    Returns:
        Prometheus API base URL
    """
    return f"https://{region}.cls.tencentcs.com/prometheus/{topic_id}"


def parse_time(time_str: Optional[str]) -> Optional[float]:
    """
    Parse time string to Unix timestamp.
    
    Accepts:
        - Unix timestamp (int or float)
        - ISO format: 2024-01-01T00:00:00Z
        - Date format: 2024-01-01
    """
    if time_str is None:
        return None
    
    # Try as Unix timestamp
    try:
        return float(time_str)
    except ValueError:
        pass
    
    # Try ISO format
    try:
        dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        return dt.timestamp()
    except ValueError:
        pass
    
    # Try date format
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%d")
        return dt.timestamp()
    except ValueError:
        pass
    
    raise ValueError(f"Cannot parse time string: {time_str}")


def parse_duration(duration_str: Optional[str]) -> Optional[timedelta]:
    """
    Parse duration string to timedelta.
    
    Accepts: 30s, 5m, 1h, 1d, 1w
    
    Args:
        duration_str: 时间间隔字符串
        
    Returns:
        timedelta 对象，如果输入为空则返回 None
        
    Raises:
        ValueError: 如果格式无效
    """
    if not duration_str:
        return None
    
    # 校验最小长度（至少需要一个数字和一个单位）
    if len(duration_str) < 2:
        raise ValueError(f"Invalid duration format: '{duration_str}'. Expected format like '30s', '5m', '1h', '1d', '1w'")
    
    unit_map = {
        's': 'seconds',
        'm': 'minutes',
        'h': 'hours',
        'd': 'days',
        'w': 'weeks'
    }
    
    value = duration_str[:-1]
    unit = duration_str[-1]
    
    if unit not in unit_map:
        raise ValueError(f"Unknown duration unit: '{unit}'. Valid units are: s, m, h, d, w")
    
    # 校验数值部分
    if not value.isdigit():
        raise ValueError(f"Invalid duration value: '{value}'. Must be a positive integer.")
    
    return timedelta(**{unit_map[unit]: int(value)})


def instant_query(
    base_url: str,
    auth: tuple,
    query: str,
    time: Optional[float] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    Execute an instant query (single point in time).
    
    Args:
        base_url: Prometheus API base URL
        auth: (username, password) tuple for Basic Auth
        query: PromQL query string
        time: Evaluation timestamp (Unix timestamp), default is current time
        timeout: Request timeout in seconds
    
    Returns:
        API response
    """
    url = urljoin(base_url + "/", "api/v1/query")
    
    params = {"query": query}
    if time is not None:
        params["time"] = time
    
    response = requests.get(url, params=params, auth=auth, timeout=timeout)
    response.raise_for_status()
    
    return response.json()


def range_query(
    base_url: str,
    auth: tuple,
    query: str,
    start: float,
    end: float,
    step: str,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    Execute a range query (time series).
    
    Args:
        base_url: Prometheus API base URL
        auth: (username, password) tuple for Basic Auth
        query: PromQL query string
        start: Start timestamp (Unix timestamp)
        end: End timestamp (Unix timestamp)
        step: Query resolution step (e.g., "15s", "1m")
        timeout: Request timeout in seconds
    
    Returns:
        API response
    """
    url = urljoin(base_url + "/", "api/v1/query_range")
    
    params = {
        "query": query,
        "start": start,
        "end": end,
        "step": step
    }
    
    response = requests.get(url, params=params, auth=auth, timeout=timeout)
    response.raise_for_status()
    
    return response.json()


def list_series(
    base_url: str,
    auth: tuple,
    match: list,
    start: Optional[float] = None,
    end: Optional[float] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    List time series matching label matchers.
    
    Args:
        base_url: Prometheus API base URL
        auth: (username, password) tuple for Basic Auth
        match: List of label matchers (e.g., ["up", "process_start_time_seconds{job='prometheus'}"])
        start: Start timestamp
        end: End timestamp
        timeout: Request timeout in seconds
    
    Returns:
        API response
    """
    url = urljoin(base_url + "/", "api/v1/series")
    
    params = {"match[]": match}
    if start is not None:
        params["start"] = start
    if end is not None:
        params["end"] = end
    
    response = requests.get(url, params=params, auth=auth, timeout=timeout)
    response.raise_for_status()
    
    return response.json()


def list_labels(
    base_url: str,
    auth: tuple,
    start: Optional[float] = None,
    end: Optional[float] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    List all label names.
    
    Args:
        base_url: Prometheus API base URL
        auth: (username, password) tuple for Basic Auth
        start: Start timestamp
        end: End timestamp
        timeout: Request timeout in seconds
    
    Returns:
        API response
    """
    url = urljoin(base_url + "/", "api/v1/labels")
    
    params = {}
    if start is not None:
        params["start"] = start
    if end is not None:
        params["end"] = end
    
    response = requests.get(url, params=params, auth=auth, timeout=timeout)
    response.raise_for_status()
    
    return response.json()


def list_label_values(
    base_url: str,
    auth: tuple,
    label_name: str,
    start: Optional[float] = None,
    end: Optional[float] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    List values for a specific label.
    
    Args:
        base_url: Prometheus API base URL
        auth: (username, password) tuple for Basic Auth
        label_name: Label name to get values for
        start: Start timestamp
        end: End timestamp
        timeout: Request timeout in seconds
    
    Returns:
        API response
    """
    url = urljoin(base_url + "/", f"api/v1/label/{label_name}/values")
    
    params = {}
    if start is not None:
        params["start"] = start
    if end is not None:
        params["end"] = end
    
    response = requests.get(url, params=params, auth=auth, timeout=timeout)
    response.raise_for_status()
    
    return response.json()


def format_output(data: Dict[str, Any], pretty: bool = True) -> str:
    """Format output as JSON."""
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False)
    return json.dumps(data, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Query OpenClaw metrics from Tencent Cloud CLS via Prometheus API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--region", "-r",
        required=True,
        choices=sorted(VALID_REGIONS),
        help="Tencent Cloud region (e.g., ap-guangzhou, ap-shanghai)"
    )
    
    parser.add_argument(
        "--topic-id", "-t",
        required=True,
        help="Metric topic ID"
    )
    
    # Query parameters
    parser.add_argument(
        "--query", "-q",
        default="",
        help="PromQL query string (required for data queries, optional for metadata queries)"
    )
    
    parser.add_argument(
        "--instant",
        action="store_true",
        help="Execute instant query (single point in time)"
    )
    
    parser.add_argument(
        "--time",
        help="Evaluation timestamp for instant query (Unix timestamp or ISO format)"
    )
    
    parser.add_argument(
        "--start",
        help="Start time for range query (Unix timestamp or ISO format)"
    )
    
    parser.add_argument(
        "--end",
        help="End time for range query (Unix timestamp or ISO format)"
    )
    
    parser.add_argument(
        "--start-relative",
        help="Relative start time from now (e.g., 1h, 30m, 1d)"
    )
    
    parser.add_argument(
        "--step", "-s",
        default="1m",
        help="Query resolution step for range query (e.g., 15s, 1m, 5m). Default: 1m"
    )
    
    # Metadata queries
    parser.add_argument(
        "--list-series",
        action="store_true",
        help="List time series matching the query"
    )
    
    parser.add_argument(
        "--list-labels",
        action="store_true",
        help="List all label names"
    )
    
    parser.add_argument(
        "--label-values",
        help="List values for a specific label"
    )
    
    # Output options
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Output compact JSON (no indentation)"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30)"
    )
    
    args = parser.parse_args()
    
    try:
        # 验证地域
        validate_region(args.region)
        
        # 验证 topic_id 格式（防止路径遍历）
        validate_topic_id(args.topic_id)
        
        # 检查 --query 是否在需要时提供
        # list_labels 和 label_values 不需要 --query，但 list_series 需要作为 match[] 参数
        needs_no_query = args.list_labels or args.label_values
        if not needs_no_query and not args.query:
            if args.list_series:
                parser.error("--query is required for --list-series (used as match[] selector, e.g., '{__name__=~\"openclaw.*\"}')")
            else:
                parser.error("--query is required for data queries (instant or range queries)")
        
        secret_id, secret_key, token = get_credentials_tuple()
        base_url = get_prometheus_url(args.region, args.topic_id)
        # Prometheus API 使用 Basic Auth：username=secretId, password=secretKey#token
        password = f"{secret_key}#{token}" if token else secret_key
        auth = (secret_id, password)
        
        # Determine time range
        start_time = None
        end_time = None
        
        if args.start_relative:
            duration = parse_duration(args.start_relative)
            end_time = datetime.now().timestamp()
            start_time = (datetime.now() - duration).timestamp()
        else:
            if args.start:
                start_time = parse_time(args.start)
            if args.end:
                end_time = parse_time(args.end)
        
        # Execute appropriate query
        if args.list_labels:
            result = list_labels(base_url, auth, start_time, end_time, args.timeout)
        
        elif args.label_values:
            # 验证标签名格式（防止路径遍历）
            validate_label_name(args.label_values)
            result = list_label_values(base_url, auth, args.label_values, start_time, end_time, args.timeout)
        
        elif args.list_series:
            result = list_series(base_url, auth, [args.query], start_time, end_time, args.timeout)
        
        elif args.instant:
            eval_time = parse_time(args.time) if args.time else None
            result = instant_query(base_url, auth, args.query, eval_time, args.timeout)
        
        else:
            # Range query
            if start_time is None or end_time is None:
                parser.error("--start and --end (or --start-relative) are required for range queries. Use --instant for point-in-time queries.")
            
            result = range_query(base_url, auth, args.query, start_time, end_time, args.step, args.timeout)
        
        print(format_output(result, not args.compact))
    
    except requests.exceptions.RequestException as e:
        # 清理错误消息，防止凭证泄露
        safe_error = sanitize_error_message(e)
        print(f"Request Error: {safe_error}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Value Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # 清理错误消息，防止凭证泄露
        safe_error = sanitize_error_message(e)
        print(f"Error: {safe_error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
