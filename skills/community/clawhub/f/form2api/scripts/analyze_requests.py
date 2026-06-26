#!/usr/bin/env python3
"""
请求过滤 + 字段分析工具
输入：从浏览器 CDP 获取的原始请求列表（JSON）
输出：过滤后的候选请求，附上字段类型标注

用法：
  python3 analyze_requests.py <requests.json> [--window 5]
  echo '[...]' | python3 analyze_requests.py - [--window 5]
"""

import json
import sys
import re
from urllib.parse import urlparse

# 排除的静态资源扩展名
STATIC_EXTENSIONS = {
    ".js", ".css", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".map", ".webp", ".mp4", ".mp3"
}

# 排除的 tracking/analytics 域名关键词
TRACKING_DOMAINS = [
    "google-analytics", "googletagmanager", "doubleclick", "facebook.net",
    "baidu.com/hm", "cnzz", "mixpanel", "amplitude", "segment.io",
    "sentry.io", "bugsnag", "datadog"
]

# 提交类请求特征
SUBMIT_PATH_KEYWORDS = [
    "submit", "create", "save", "add", "publish", "post", "insert",
    "update", "edit", "modify", "upload", "send", "confirm", "apply"
]

# 业务响应特征
BUSINESS_RESPONSE_PATTERNS = [
    r'"code"\s*:\s*\d+',
    r'"status"\s*:\s*\d+',
    r'"success"\s*:\s*(true|false)',
    r'"errno"\s*:\s*\d+',
    r'"msg"\s*:',
    r'"message"\s*:',
    r'"data"\s*:',
]

# 固定值特征（可能是系统字段）
FIXED_VALUE_PATTERNS = {
    "uuid": r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    "hex32": r'^[0-9A-Fa-f]{32,64}$',
    "timestamp_ms": r'^\d{13}$',
    "timestamp_s": r'^\d{10}$',
    "url": r'^https?://',
}


def is_static_resource(url: str) -> bool:
    parsed = urlparse(url)
    path = parsed.path.lower()
    for ext in STATIC_EXTENSIONS:
        if path.endswith(ext):
            return True
    return False


def is_tracking_request(url: str) -> bool:
    url_lower = url.lower()
    for keyword in TRACKING_DOMAINS:
        if keyword in url_lower:
            return True
    return False


def has_business_response(response_body: str) -> bool:
    for pattern in BUSINESS_RESPONSE_PATTERNS:
        if re.search(pattern, response_body):
            return True
    return False


def is_submit_like_path(url: str) -> bool:
    parsed = urlparse(url)
    path = parsed.path.lower()
    for keyword in SUBMIT_PATH_KEYWORDS:
        if keyword in path:
            return True
    return False


def guess_field_type(key: str, value) -> dict:
    """猜测字段的语义类型"""
    val_str = str(value) if value is not None else ""
    
    info = {"value": value, "type": "unknown", "annotation": ""}

    # 检查是否是固定值模式
    for pattern_name, pattern in FIXED_VALUE_PATTERNS.items():
        if re.match(pattern, val_str):
            info["type"] = "system_fixed"
            info["annotation"] = f"<固定值 ({pattern_name})>"
            return info

    # 根据 key 名猜测
    key_lower = key.lower()
    
    if any(k in key_lower for k in ["token", "key", "secret", "auth", "sign"]):
        info["type"] = "auth"
        info["annotation"] = "<认证字段，从 Cookie/Header 提取>"
    elif any(k in key_lower for k in ["time", "date", "ts", "timestamp"]):
        info["type"] = "auto_generated"
        info["annotation"] = "<时间戳，自动生成>"
    elif any(k in key_lower for k in ["id", "uid", "userid"]) and len(val_str) > 8:
        info["type"] = "system_id"
        info["annotation"] = "<系统 ID，保持原值>"
    elif any(k in key_lower for k in ["template", "type", "mode", "status", "flag"]) and isinstance(value, (int, bool)):
        info["type"] = "enum_fixed"
        info["annotation"] = f"<枚举固定值: {value}>"
    elif isinstance(value, str) and len(value) > 0 and len(value) < 200:
        info["type"] = "user_input"
        info["annotation"] = "<用户输入>"
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        info["type"] = "numeric"
        info["annotation"] = "<数值>"
    
    return info


def analyze_payload(payload_str: str) -> dict:
    """分析请求 payload，标注字段类型"""
    if not payload_str:
        return {}
    
    try:
        # 尝试 JSON 解析
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        # 尝试 URL-encoded 格式
        from urllib.parse import parse_qs
        try:
            parsed = parse_qs(payload_str)
            payload = {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
        except Exception:
            return {"_raw": payload_str}
    
    result = {}
    if isinstance(payload, dict):
        for key, value in payload.items():
            result[key] = guess_field_type(key, value)
    elif isinstance(payload, list):
        result["_array"] = {"type": "array", "value": payload, "annotation": "<数组数据>"}
    
    return result


def filter_requests(requests: list, time_window_seconds: int = 10) -> list:
    """过滤出候选的表单提交请求"""
    if not requests:
        return []

    candidates = []
    
    for req in requests:
        url = req.get("url", "")
        method = req.get("method", "GET").upper()
        response_body = req.get("responseBody", "")

        # 基础过滤
        if is_static_resource(url):
            continue
        if is_tracking_request(url):
            continue
        
        score = 0
        reasons = []

        # POST/PUT/PATCH 优先
        if method in ("POST", "PUT", "PATCH", "DELETE"):
            score += 3
            reasons.append(f"method={method}")
        
        # 路径含提交关键词
        if is_submit_like_path(url):
            score += 2
            reasons.append("submit-like path")
        
        # 有业务响应体
        if has_business_response(response_body):
            score += 2
            reasons.append("business response")
        
        # 有请求体
        if req.get("requestBody"):
            score += 1
            reasons.append("has body")

        if score >= 2:  # 至少满足2分才算候选
            req["_score"] = score
            req["_reasons"] = reasons
            candidates.append(req)
    
    # 按分数降序
    candidates.sort(key=lambda x: x.get("_score", 0), reverse=True)
    return candidates


def format_output(candidates: list) -> str:
    """格式化输出分析结果"""
    if not candidates:
        return "⚠️  未发现候选提交请求。请确认表单已提交，或拦截器是否成功注入。\n"
    
    lines = [f"🎯 发现 {len(candidates)} 个候选请求（按可信度排序）\n"]
    lines.append("=" * 60)
    
    for i, req in enumerate(candidates, 1):
        url = req.get("url", "")
        method = req.get("method", "GET")
        score = req.get("_score", 0)
        reasons = ", ".join(req.get("_reasons", []))
        req_body = req.get("requestBody", "")
        resp_body = req.get("responseBody", "")
        resp_status = req.get("responseStatus", "?")
        
        lines.append(f"\n【{i}】 {method} {url}")
        lines.append(f"     可信度: {'⭐' * min(score, 5)} ({score}分) | 原因: {reasons}")
        lines.append(f"     HTTP状态: {resp_status}")
        
        # 分析请求体
        if req_body:
            lines.append(f"\n  📤 请求体（原始）:")
            try:
                parsed = json.loads(req_body)
                lines.append(f"     {json.dumps(parsed, ensure_ascii=False, indent=4)}")
            except Exception:
                lines.append(f"     {req_body}")

            lines.append(f"\n  📤 请求体分析（字段标注）:")
            field_analysis = analyze_payload(req_body)
            if "_raw" in field_analysis:
                lines.append(f"     (非JSON格式，见上方原始内容)")
            else:
                for field_name, field_info in field_analysis.items():
                    annotation = field_info.get("annotation", "")
                    value = field_info.get("value", "")
                    val_preview = str(value)[:80] + ("..." if len(str(value)) > 80 else "")
                    lines.append(f"     • {field_name}: {val_preview}  {annotation}")
        
        # 响应体预览
        if resp_body:
            preview = resp_body[:200].replace("\n", " ")
            lines.append(f"\n  📥 响应预览: {preview}")
        
        lines.append("\n" + "-" * 60)
    
    return "\n".join(lines)


def main():
    time_window = 10
    for i, arg in enumerate(sys.argv):
        if arg == "--window" and i + 1 < len(sys.argv):
            time_window = int(sys.argv[i + 1])

    # 读取输入
    if len(sys.argv) >= 2 and sys.argv[1] != "-" and not sys.argv[1].startswith("--"):
        with open(sys.argv[1]) as f:
            raw = f.read()
    else:
        raw = sys.stdin.read()

    try:
        requests_data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    candidates = filter_requests(requests_data, time_window)
    output = format_output(candidates)
    print(output)

    # 同时输出结构化 JSON 到文件（供后续生成文档使用）
    output_file = "/tmp/form_api_analysis.json"
    with open(output_file, "w") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
    print(f"\n📄 结构化结果已保存到: {output_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
