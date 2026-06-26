#!/usr/bin/env python3
"""
Tencent Cloud CLS API Client for OpenClaw Monitoring Data Analysis

This script provides a command-line interface to query OpenClaw monitoring data
stored in Tencent Cloud Log Service (CLS).

Authentication:
    Credentials are read from TCCLI credential file.
    Run `tccli auth login` to obtain credentials.

Usage Examples:
    # List OpenClaw log topics
    python cls_api.py --region ap-guangzhou --action DescribeTopics --biz-type 0

    # List OpenClaw metric topics
    python cls_api.py --region ap-guangzhou --action DescribeTopics --biz-type 1

    # Get log topic field schema (index configuration)
    python cls_api.py --region ap-guangzhou --action DescribeIndex --topic-id <topic_id>

    # Search logs
    python cls_api.py --region ap-guangzhou --action SearchLog \
        --topic-id <topic_id> --query "*" \
        --from-time 1608794854000 --to-time 1608794855000

    # Generate query suggestions
    python cls_api.py --region ap-guangzhou --action ChatCompletions \
        --topic-id <topic_id> --chat-question "如何统计日志条数变化趋势？"

    # Get dashboard templates (global API, region doesn't matter)
    python cls_api.py --action DescribeTemplates
"""

import sys
import json
import argparse
from datetime import datetime
from typing import Optional, Dict, Any

# 导入公共模块
from common import (
    create_cls_client,
    validate_region,
    validate_topic_id,
    sanitize_error_message,
    VALID_REGIONS,
)

try:
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
except ImportError:
    print("Error: tencentcloud-sdk-python is not installed.")
    print("Please install it with: pip install tencentcloud-sdk-python")
    sys.exit(1)


def describe_topics(client, biz_type: int = 0, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """
    Get list of OpenClaw topics.
    
    Args:
        client: CLS API client
        biz_type: 0 for log topics, 1 for metric topics
        limit: Maximum number of results
        offset: Pagination offset
    
    Returns:
        API response containing topic list
    """
    params = {
        "Filters": [
            {
                "Key": "assumerName",
                "Values": ["OpenClaw"]
            }
        ],
        "BizType": biz_type,
        "Limit": limit,
        "Offset": offset
    }
    
    return client.call_json("DescribeTopics", params)


def search_log(
    client,
    topic_id: str,
    query: str,
    from_time: int,
    to_time: int,
    limit: int = 100,
    offset: int = 0,
    sort: str = "desc",
    syntax_rule: int = 1,
    context: Optional[str] = None,
    sampling_rate: Optional[float] = None
) -> Dict[str, Any]:
    """
    Search logs in a topic.
    
    Args:
        client: CLS API client
        topic_id: Log topic ID
        query: CQL/Lucene query string
        from_time: Start time in milliseconds
        to_time: End time in milliseconds
        limit: Maximum number of results (max 1000)
        offset: Pagination offset
        sort: Sort order ('asc' or 'desc')
        syntax_rule: 0 for Lucene, 1 for CQL (recommended)
        context: Context for pagination
        sampling_rate: Sampling rate for analysis queries
    
    Returns:
        API response containing log data
    """
    params = {
        "TopicId": topic_id,
        "Query": query,
        "From": from_time,
        "To": to_time,
        "Limit": limit,
        "Sort": sort,
        "SyntaxRule": syntax_rule
    }
    
    if offset > 0:
        params["Offset"] = offset
    
    if context:
        params["Context"] = context
    
    if sampling_rate is not None:
        params["SamplingRate"] = sampling_rate
    
    return client.call_json("SearchLog", params)


def chat_completions(
    client,
    topic_id: str,
    topic_region: str,
    question: str
) -> Dict[str, Any]:
    """
    Generate query suggestions using AI.
    
    Args:
        client: CLS API client
        topic_id: Log topic ID
        topic_region: Region of the topic
        question: Question to ask about query generation
    
    Returns:
        API response containing AI-generated query suggestions
    """
    params = {
        "Model": "text2sql",
        "Messages": [
            {
                "Content": question,
                "Role": "user"
            }
        ],
        "Stream": False,
        "Metadata": [
            {
                "Key": "topic_id",
                "Value": topic_id
            },
            {
                "Key": "topic_region",
                "Value": topic_region
            }
        ]
    }
    
    return client.call_json("ChatCompletions", params)


def describe_templates(client) -> Dict[str, Any]:
    """
    Get OpenClaw dashboard templates.
    
    API 返回结构：
    Response.Templates[].SubTypes[].TemplateItems[]
    
    其中 SubType == "CLS_Openclaw" 的 SubTypes 包含 OpenClaw 模板。
    
    Args:
        client: CLS API client
    
    Returns:
        API response containing dashboard templates (filtered to OpenClaw only)
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
    data = result
    if "Response" in data:
        data = data["Response"]
    
    # 过滤：只保留包含 CLS_Openclaw SubType 的模板
    filtered_templates = []
    for template in data.get("Templates", []):
        sub_types = template.get("SubTypes", [])
        openclaw_subs = [s for s in sub_types if s.get("SubType") == "CLS_Openclaw"]
        if openclaw_subs:
            # 只保留 OpenClaw 的 SubTypes
            template_copy = dict(template)
            template_copy["SubTypes"] = openclaw_subs
            filtered_templates.append(template_copy)
    
    data["Templates"] = filtered_templates
    
    # 保持原始包装结构返回
    if "Response" in result:
        result["Response"] = data
    else:
        result = data
    
    return result


def describe_index(client, topic_id: str) -> Dict[str, Any]:
    """
    Get index configuration for a log topic, including field schema.
    
    Returns the index rules containing:
    - KeyValue index: field names, types (text/long/double), and SQL analysis flags
    - Tag (metadata) index: metadata field names and types
    - FullText index: full-text search configuration
    - DynamicIndex: whether dynamic indexing is enabled
    
    This is useful for discovering what fields are available in a log topic
    before constructing queries.
    
    Args:
        client: CLS API client
        topic_id: Log topic ID
    
    Returns:
        API response containing index configuration with field schema
    """
    params = {
        "TopicId": topic_id
    }
    return client.call_json("DescribeIndex", params)


def describe_openclaw_applications(client) -> Dict[str, Any]:
    """
    Get OpenClaw applications with monitoring enabled.
    
    This API returns all OpenClaw instances that have monitoring enabled,
    including their ServiceRegion which indicates where monitoring data is stored.
    
    Args:
        client: CLS API client
    
    Returns:
        API response containing OpenClaw application list with ServiceRegion
    """
    params = {}
    return client.call_json("DescribeOpenClawApplications", params)


def format_output(data: Dict[str, Any], pretty: bool = True) -> str:
    """Format output as JSON."""
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False)
    return json.dumps(data, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Query OpenClaw monitoring data from Tencent Cloud CLS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--region", "-r",
        default="ap-guangzhou",
        choices=sorted(VALID_REGIONS),
        help="Tencent Cloud region (default: ap-guangzhou)"
    )
    
    parser.add_argument(
        "--action", "-a",
        required=True,
        choices=["DescribeOpenClawApplications", "DescribeTopics", "DescribeIndex", "SearchLog", "ChatCompletions", "DescribeTemplates"],
        help="API action to perform"
    )
    
    # DescribeTopics parameters
    parser.add_argument(
        "--biz-type",
        type=int,
        default=0,
        help="Topic type: 0 for log topics (default), 1 for metric topics"
    )
    
    # SearchLog parameters
    parser.add_argument(
        "--topic-id", "-t",
        help="Topic ID for SearchLog, DescribeIndex, or ChatCompletions"
    )
    
    parser.add_argument(
        "--query", "-q",
        default="*",
        help="Query string (CQL syntax recommended). Default: '*'"
    )
    
    parser.add_argument(
        "--from-time", "-f",
        type=int,
        help="Start time in milliseconds (Unix timestamp)"
    )
    
    parser.add_argument(
        "--to-time", "-T",
        type=int,
        help="End time in milliseconds (Unix timestamp)"
    )
    
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=100,
        help="Maximum number of results (default: 100, max: 1000)"
    )
    
    parser.add_argument(
        "--offset", "-o",
        type=int,
        default=0,
        help="Pagination offset (default: 0)"
    )
    
    parser.add_argument(
        "--sort", "-s",
        choices=["asc", "desc"],
        default="desc",
        help="Sort order (default: desc)"
    )
    
    parser.add_argument(
        "--syntax-rule",
        type=int,
        choices=[0, 1],
        default=1,
        help="Syntax rule: 0 for Lucene, 1 for CQL (default: 1)"
    )
    
    parser.add_argument(
        "--context",
        help="Context string for pagination continuation"
    )
    
    parser.add_argument(
        "--sampling-rate",
        type=float,
        help="Sampling rate for analysis (0-1, default: 1 for no sampling)"
    )
    
    # ChatCompletions parameters
    parser.add_argument(
        "--chat-question",
        help="Question for AI query generation"
    )
    
    # Output options
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Output compact JSON (no indentation)"
    )
    
    args = parser.parse_args()
    
    try:
        # 验证地域
        validate_region(args.region)
        
        client = create_cls_client(args.region)
        
        if args.action == "DescribeOpenClawApplications":
            result = describe_openclaw_applications(client)
        
        elif args.action == "DescribeIndex":
            if not args.topic_id:
                parser.error("--topic-id is required for DescribeIndex")
            validate_topic_id(args.topic_id)
            result = describe_index(client, args.topic_id)
        
        elif args.action == "DescribeTopics":
            result = describe_topics(client, args.biz_type, args.limit, args.offset)
        
        elif args.action == "SearchLog":
            if not args.topic_id:
                parser.error("--topic-id is required for SearchLog")
            validate_topic_id(args.topic_id)
            if args.from_time is None:
                parser.error("--from-time is required for SearchLog")
            if args.to_time is None:
                parser.error("--to-time is required for SearchLog")
            
            result = search_log(
                client,
                args.topic_id,
                args.query,
                args.from_time,
                args.to_time,
                args.limit,
                args.offset,
                args.sort,
                args.syntax_rule,
                args.context,
                args.sampling_rate
            )
        
        elif args.action == "ChatCompletions":
            if not args.topic_id:
                parser.error("--topic-id is required for ChatCompletions")
            validate_topic_id(args.topic_id)
            if not args.chat_question:
                parser.error("--chat-question is required for ChatCompletions")
            
            result = chat_completions(client, args.topic_id, args.region, args.chat_question)
        
        elif args.action == "DescribeTemplates":
            result = describe_templates(client)
        
        print(format_output(result, not args.compact))
    
    except TencentCloudSDKException as e:
        safe_error = sanitize_error_message(e)
        print(f"API Error: {safe_error}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Value Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        safe_error = sanitize_error_message(e)
        print(f"Error: {safe_error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
