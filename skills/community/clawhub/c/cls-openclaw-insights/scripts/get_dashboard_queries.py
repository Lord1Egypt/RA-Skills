#!/usr/bin/env python3
"""
提取 OpenClaw 仪表盘模板中的关键查询信息

此脚本调用腾讯云 CLS API 获取 OpenClaw 仪表盘模板，
并提取其中的关键信息，包括：
- 图表标题（代表查询用途）
- 主题类型（日志/指标）
- 查询语句

环境变量：
    凭证通过 TCCLI 凭证文件读取。
    执行 `tccli auth login` 获取凭证。

使用示例：
    # 获取所有查询（默认表格格式）
    # DescribeTemplates 是全局接口，--region 不影响结果（默认 ap-guangzhou）
    python get_dashboard_queries.py

    # 输出 JSON 格式
    python get_dashboard_queries.py --format json

    # 只显示日志类型的查询
    python get_dashboard_queries.py --type log

    # 只显示指标类型的查询
    python get_dashboard_queries.py --type metric

    # 输出 Markdown 表格
    python get_dashboard_queries.py --format markdown
"""

import sys
import json
import re
import argparse
from typing import Dict, Any, List, Optional

# 导入公共模块
from common import (
    create_cls_client,
    validate_region,
    sanitize_error_message,
    VALID_REGIONS,
)

try:
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
except ImportError:
    print("错误: 未安装 tencentcloud-sdk-python")
    print("请执行: pip install tencentcloud-sdk-python")
    sys.exit(1)


def get_openclaw_templates(client) -> List[Dict[str, Any]]:
    """
    获取 OpenClaw 仪表盘模板
    
    API 返回结构：
    Response.Templates[].SubTypes[].TemplateItems[]
    
    其中 SubType == "CLS_Openclaw" 的 SubTypes 包含 OpenClaw 模板
    """
    params = {
        "Filters": [
            {
                "Key": "ResourceType",
                "Values": ["DASHBOARD"]
            }
        ]
    }
    
    result = client.call_json("DescribeTemplates", params)
    
    # 处理 Response 包装
    if "Response" in result:
        result = result["Response"]
    
    # 遍历模板，找到 OpenClaw 的 TemplateItems
    openclaw_templates = []
    templates = result.get("Templates", [])
    
    for template in templates:
        sub_types = template.get("SubTypes", [])
        for sub in sub_types:
            if sub.get("SubType") == "CLS_Openclaw":
                # 找到 OpenClaw，提取 TemplateItems
                items = sub.get("TemplateItems", [])
                for item in items:
                    # 转换为我们需要的结构
                    # item 有: TemplateItemId, Name, ResourceType, Value
                    # Value 是 JSON 字符串，包含仪表盘配置
                    openclaw_templates.append({
                        "Name": item.get("Name", ""),
                        "Resource": item.get("Value", ""),
                        "SubType": "CLS_Openclaw"
                    })
    
    return openclaw_templates


def extract_query_info(templates: List[Dict[str, Any]], debug: bool = False) -> List[Dict[str, str]]:
    """
    从模板中提取查询信息
    
    返回列表，每项包含：
    - title: 图表标题
    - type: 主题类型 (log/metric)
    - query: 查询语句
    - dashboard: 所属仪表盘名称
    
    Args:
        templates: 仪表盘模板列表
        debug: 是否输出调试信息
    """
    queries = []
    
    for template in templates:
        template_name = template.get("Name", "未知仪表盘")
        resource = template.get("Resource", "")
        
        # Resource 是 JSON 字符串，需要解析
        try:
            dashboard_config = json.loads(resource) if isinstance(resource, str) else resource
        except json.JSONDecodeError:
            if debug:
                print(f"[DEBUG] 无法解析仪表盘 '{template_name}' 的 Resource JSON", file=sys.stderr)
            continue
        
        # 获取 dashboardData
        dashboard_data = dashboard_config.get("dashboardData", dashboard_config)
        
        # 获取 panels 或 charts
        panels = dashboard_data.get("panels", dashboard_data.get("charts", []))
        
        if not panels:
            if debug:
                print(f"[DEBUG] 仪表盘 '{template_name}' 中未找到 'panels' 或 'charts'", file=sys.stderr)
            continue
        
        for panel in panels:
            title = panel.get("title", "未命名图表")
            panel_type = panel.get("type", "")
            
            # 跳过 row 类型（分组标题）
            if panel_type == "row":
                continue
            
            # 从 targets 或 target 中提取查询
            targets = panel.get("targets", [])
            if not targets:
                target = panel.get("target")
                if target:
                    targets = [target]
            
            for t in targets:
                query_str = t.get("Query", "")
                if query_str and query_str.strip():
                    topic_type = determine_query_type(t, query_str)
                    queries.append({
                        "dashboard": template_name,
                        "title": title,
                        "type": topic_type,
                        "query": query_str.strip()
                    })
    
    return queries


def determine_query_type(query_config: Dict[str, Any], query_str: str) -> str:
    """
    判断查询类型
    
    通过以下特征判断（优先级从高到低）：
    1. 配置中的 type 字段（最可靠）
    2. CQL 特有语法特征（管道符模式）
    3. PromQL 特有语法特征（函数和时间范围选择器）
    4. 指标名前缀特征
    """
    # 1. 检查配置中的 type 字段（最可靠）
    q_type = query_config.get("type", "").lower()
    if q_type in ["log", "cls"]:
        return "log"
    if q_type in ["metric", "prometheus", "prom"]:
        return "metric"
    
    # 通过查询语句特征判断
    query_lower = query_str.lower()
    query_stripped = query_str.strip()
    
    # 2. CQL/SQL 特有语法特征（使用正则进行词边界匹配）
    # CQL 的管道语法是独特的：* | SELECT ... 或者直接 SELECT ...
    cql_patterns = [
        r'\|\s*select\b',          # 管道后跟 SELECT（CQL 特有）
        r'^\s*select\b',           # 以 SELECT 开头
        r'\bfrom\s+[\w\.\*]+\s+where\b',  # FROM table WHERE 模式
        r'\bgroup\s+by\b',         # GROUP BY
        r'\border\s+by\b',         # ORDER BY
        r'\bhistogram\s*\(',       # histogram 函数（CQL）
        r'__timestamp__',          # CLS 时间戳字段
        r'__source__',             # CLS 来源字段
        r'__filename__',           # CLS 文件名字段
    ]
    
    for pattern in cql_patterns:
        if re.search(pattern, query_lower, re.IGNORECASE):
            return "log"
    
    # 3. PromQL 特有语法特征
    promql_patterns = [
        r'\b(sum|avg|min|max|count|rate|increase|histogram_quantile|topk|bottomk|irate|delta|deriv|predict_linear|absent|absent_over_time|changes|resets)\s*\(',  # PromQL 函数
        r'\b(sum|avg|min|max|count)\s+by\s*\(',  # 聚合 by 语法
        r'\b(sum|avg|min|max|count)\s+without\s*\(',  # 聚合 without 语法
        r'\[\d+[smhdwy]\]',         # 时间范围选择器 [5m], [1h] 等
        r'\boffset\s+\d+[smhdwy]\b',  # offset 语法
        r'\{[^}]*=~?[^}]*\}',       # label 匹配器语法 {job="prometheus"}
    ]
    
    for pattern in promql_patterns:
        if re.search(pattern, query_lower, re.IGNORECASE):
            return "metric"
    
    # 4. 包含特定前缀的指标名通常是 Prometheus 指标
    metric_prefixes = ["openclaw_", "system_", "process_", "go_", "node_", "container_"]
    for prefix in metric_prefixes:
        if query_stripped.startswith(prefix) or f"{{{prefix}" in query_stripped:
            return "metric"
    
    return "unknown"


def format_table(queries: List[Dict[str, str]], show_dashboard: bool = False) -> str:
    """格式化为表格输出"""
    if not queries:
        return "未找到查询信息"
    
    lines = []
    
    # 计算列宽
    max_title = max(len(q["title"]) for q in queries)
    max_title = max(max_title, 8)  # 最小宽度
    max_type = 8
    
    if show_dashboard:
        max_dashboard = max(len(q["dashboard"]) for q in queries)
        max_dashboard = max(max_dashboard, 6)
        header = f"{'仪表盘':<{max_dashboard}}  {'标题':<{max_title}}  {'类型':<{max_type}}  查询语句"
        separator = f"{'-' * max_dashboard}  {'-' * max_title}  {'-' * max_type}  {'-' * 40}"
    else:
        header = f"{'标题':<{max_title}}  {'类型':<{max_type}}  查询语句"
        separator = f"{'-' * max_title}  {'-' * max_type}  {'-' * 40}"
    
    lines.append(header)
    lines.append(separator)
    
    for q in queries:
        query_display = q["query"]
        # 截断过长的查询
        if len(query_display) > 80:
            query_display = query_display[:77] + "..."
        
        if show_dashboard:
            lines.append(f"{q['dashboard']:<{max_dashboard}}  {q['title']:<{max_title}}  {q['type']:<{max_type}}  {query_display}")
        else:
            lines.append(f"{q['title']:<{max_title}}  {q['type']:<{max_type}}  {query_display}")
    
    return "\n".join(lines)


def format_markdown(queries: List[Dict[str, str]], show_dashboard: bool = False) -> str:
    """格式化为 Markdown 表格"""
    if not queries:
        return "未找到查询信息"
    
    lines = []
    
    if show_dashboard:
        lines.append("| 仪表盘 | 标题 | 类型 | 查询语句 |")
        lines.append("|--------|------|------|----------|")
    else:
        lines.append("| 标题 | 类型 | 查询语句 |")
        lines.append("|------|------|----------|")
    
    for q in queries:
        # 转义 Markdown 特殊字符
        query_escaped = q["query"].replace("|", "\\|").replace("\n", " ")
        title_escaped = q["title"].replace("|", "\\|")
        
        if show_dashboard:
            dashboard_escaped = q["dashboard"].replace("|", "\\|")
            lines.append(f"| {dashboard_escaped} | {title_escaped} | {q['type']} | `{query_escaped}` |")
        else:
            lines.append(f"| {title_escaped} | {q['type']} | `{query_escaped}` |")
    
    return "\n".join(lines)


def format_json(queries: List[Dict[str, str]]) -> str:
    """格式化为 JSON"""
    return json.dumps(queries, indent=2, ensure_ascii=False)


def format_grouped(queries: List[Dict[str, str]]) -> str:
    """按类型分组输出"""
    if not queries:
        return "未找到查询信息"
    
    # 按类型分组
    log_queries = [q for q in queries if q["type"] == "log"]
    metric_queries = [q for q in queries if q["type"] == "metric"]
    unknown_queries = [q for q in queries if q["type"] == "unknown"]
    
    lines = []
    
    if log_queries:
        lines.append("=" * 60)
        lines.append("📋 日志查询 (CQL/SQL)")
        lines.append("=" * 60)
        for q in log_queries:
            lines.append(f"\n【{q['title']}】")
            lines.append(f"  {q['query']}")
    
    if metric_queries:
        lines.append("\n" + "=" * 60)
        lines.append("📊 指标查询 (PromQL)")
        lines.append("=" * 60)
        for q in metric_queries:
            lines.append(f"\n【{q['title']}】")
            lines.append(f"  {q['query']}")
    
    if unknown_queries:
        lines.append("\n" + "=" * 60)
        lines.append("❓ 未知类型")
        lines.append("=" * 60)
        for q in unknown_queries:
            lines.append(f"\n【{q['title']}】")
            lines.append(f"  {q['query']}")
    
    # 统计信息
    lines.append("\n" + "-" * 60)
    lines.append(f"统计: 日志查询 {len(log_queries)} 个, 指标查询 {len(metric_queries)} 个, 未知 {len(unknown_queries)} 个")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="提取 OpenClaw 仪表盘模板中的查询信息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--region", "-r",
        default="ap-guangzhou",
        choices=sorted(VALID_REGIONS),
        help="腾讯云地域 (默认: ap-guangzhou, DescribeTemplates 是全局接口，地域参数不影响结果)"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["table", "markdown", "json", "grouped"],
        default="grouped",
        help="输出格式: table(表格), markdown(MD表格), json, grouped(分组，默认)"
    )
    
    parser.add_argument(
        "--type", "-t",
        choices=["log", "metric", "all"],
        default="all",
        help="过滤查询类型: log(日志), metric(指标), all(全部，默认)"
    )
    
    parser.add_argument(
        "--show-dashboard",
        action="store_true",
        help="显示所属仪表盘名称"
    )
    
    parser.add_argument(
        "--raw",
        action="store_true",
        help="输出原始模板数据（调试用，注意可能包含敏感信息）"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="输出调试信息（如模板解析问题）"
    )
    
    args = parser.parse_args()
    
    try:
        # 验证地域
        validate_region(args.region)
        
        client = create_cls_client(args.region)
        templates = get_openclaw_templates(client)
        
        if not templates:
            print("未找到 OpenClaw 仪表盘模板")
            sys.exit(0)
        
        if args.raw:
            print(json.dumps(templates, indent=2, ensure_ascii=False))
            print("\n⚠️ 警告: 原始输出可能包含敏感配置信息，请勿分享", file=sys.stderr)
            sys.exit(0)
        
        queries = extract_query_info(templates, debug=args.debug)
        
        # 过滤类型
        if args.type != "all":
            queries = [q for q in queries if q["type"] == args.type]
        
        if not queries:
            print(f"未找到类型为 '{args.type}' 的查询")
            sys.exit(0)
        
        # 输出
        if args.format == "table":
            print(format_table(queries, args.show_dashboard))
        elif args.format == "markdown":
            print(format_markdown(queries, args.show_dashboard))
        elif args.format == "json":
            print(format_json(queries))
        else:  # grouped
            print(format_grouped(queries))
    
    except TencentCloudSDKException as e:
        safe_error = sanitize_error_message(e)
        print(f"API 错误: {safe_error}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"参数错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        safe_error = sanitize_error_message(e)
        print(f"错误: {safe_error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
