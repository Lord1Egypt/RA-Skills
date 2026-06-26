#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FOFA 搜索引擎查询工具
支持完整的 FOFA 查询语法和 API 功能
"""

import os
import sys
import json
import base64
import argparse
from typing import Dict, List, Optional, Any
from urllib.parse import quote
import requests


class FOFAQuery:
    """FOFA 查询客户端"""
    
    API_BASE = "https://fofa.info/api/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 FOFA 客户端
        
        Args:
            api_key: FOFA API 凭证，格式为 "email:key"
        """
        if api_key is None:
            # 从环境变量获取凭证
            api_key = os.getenv(f"FOFA_API_KEY")
        
        if not api_key:
            raise ValueError(
                "缺少 FOFA API 凭证。请设置环境变量或在个人中心配置凭证。\n"
                "凭证格式：email:key"
            )
        
        # 解析凭证
        try:
            parts = api_key.split(":", 1)
            if len(parts) != 2:
                raise ValueError("凭证格式错误")
            self.email = parts[0]
            self.key = parts[1]
        except Exception as e:
            raise ValueError(
                f"凭证解析失败: {str(e)}\n"
                "正确格式：email:key"
            )
    
    def _build_auth_header(self) -> str:
        """构建 Basic Auth 认证头"""
        credentials = f"{self.email}:{self.key}"
        return base64.b64encode(credentials.encode()).decode()
    
    def _make_request(
        self,
        endpoint: str,
        params: Dict[str, Any],
        method: str = "GET"
    ) -> Dict[str, Any]:
        """
        发起 API 请求
        
        Args:
            endpoint: API 端点
            params: 请求参数
            method: HTTP 方法
        
        Returns:
            API 响应数据
        """
        url = f"{self.API_BASE}/{endpoint}"
        headers = {
            "Authorization": self._build_auth_header(),
            "Content-Type": "application/json"
        }
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, params=params, headers=headers, timeout=30)
            else:
                response = requests.post(url, json=params, headers=headers, timeout=30)
            
            # 检查 HTTP 状态码
            if response.status_code >= 400:
                raise Exception(
                    f"HTTP 请求失败: 状态码 {response.status_code}, "
                    f"响应内容: {response.text}"
                )
            
            data = response.json()
            
            # 检查 API 错误
            if data.get("error", False):
                raise Exception(f"API 错误: {data.get('errmsg', '未知错误')}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def search(
        self,
        query: str,
        page: int = 1,
        size: int = 100,
        fields: Optional[str] = None,
        full: bool = False
    ) -> Dict[str, Any]:
        """
        执行搜索查询
        
        Args:
            query: 查询语句
            page: 页码（从 1 开始）
            size: 每页结果数（最大 10000）
            fields: 返回字段（逗号分隔），默认为 host,ip,port
            full: 是否显示完整结果
        
        Returns:
            搜索结果字典，包含:
            - results: 结果列表
            - size: 结果数量
            - page: 当前页码
            - mode: 查询模式
        """
        if fields is None:
            fields = "host,ip,port"
        
        params = {
            "qbase64": base64.b64encode(query.encode()).decode(),
            "page": page,
            "size": size,
            "fields": fields,
            "full": full
        }
        
        return self._make_request("search/all", params)
    
    def search_stats(
        self,
        query: str,
        fields: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取查询统计信息
        
        Args:
            query: 查询语句
            fields: 统计字段（逗号分隔）
        
        Returns:
            统计结果
        """
        if fields is None:
            fields = "ip,port"
        
        params = {
            "qbase64": base64.b64encode(query.encode()).decode(),
            "fields": fields
        }
        
        return self._make_request("search/stats", params)
    
    def get_user_info(self) -> Dict[str, Any]:
        """获取用户信息"""
        return self._make_request("info/my", {})
    
    def get_search_history(
        self,
        page: int = 1,
        size: int = 10
    ) -> Dict[str, Any]:
        """
        获取搜索历史
        
        Args:
            page: 页码
            size: 每页数量
        """
        params = {"page": page, "size": size}
        return self._make_request("search/history", params)
    
    def get_host_detail(self, host: str) -> Dict[str, Any]:
        """
        获取主机详情
        
        Args:
            host: 主机地址（IP 或域名）
        """
        params = {"host": host}
        return self._make_request("host/detail", params)


def format_results(data: Dict[str, Any], output_format: str = "text") -> str:
    """
    格式化查询结果
    
    Args:
        data: API 返回的原始数据
        output_format: 输出格式（text/json/table）
    
    Returns:
        格式化后的字符串
    """
    if output_format == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    results = data.get("results", [])
    size = data.get("size", 0)
    page = data.get("page", 1)
    
    if not results:
        return "未找到匹配结果"
    
    if output_format == "table":
        lines = []
        lines.append(f"\n{'='*80}")
        lines.append(f"查询结果: 第 {page} 页, 共 {size} 条")
        lines.append(f"{'='*80}\n")
        
        for idx, item in enumerate(results, 1):
            if isinstance(item, list):
                lines.append(f"[{idx}] {' | '.join(str(x) for x in item)}")
            elif isinstance(item, dict):
                lines.append(f"[{idx}] {json.dumps(item, ensure_ascii=False)}")
            else:
                lines.append(f"[{idx}] {item}")
        
        return "\n".join(lines)
    
    # text 格式
    lines = [f"\n查询结果 (第 {page} 页, 共 {size} 条):\n"]
    
    for idx, item in enumerate(results, 1):
        if isinstance(item, list):
            lines.append(f"  [{idx}] {' | '.join(str(x) for x in item)}")
        elif isinstance(item, dict):
            lines.append(f"  [{idx}] {json.dumps(item, ensure_ascii=False)}")
        else:
            lines.append(f"  [{idx}] {item}")
    
    return "\n".join(lines)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="FOFA 搜索引擎查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础查询
  python fofa_query.py -q 'domain="qq.com"'
  
  # 指定返回字段
  python fofa_query.py -q 'ip="1.1.1.1"' -f "ip,port,host,title"
  
  # 分页查询
  python fofa_query.py -q 'port="80"' --page 2 --size 50
  
  # 获取统计信息
  python fofa_query.py -q 'domain="baidu.com"' --stats
  
  # 查看用户信息
  python fofa_query.py --user-info
        """
    )
    
    parser.add_argument(
        "-q", "--query",
        help="查询语句"
    )
    parser.add_argument(
        "-f", "--fields",
        default="host,ip,port",
        help="返回字段（逗号分隔），默认: host,ip,port"
    )
    parser.add_argument(
        "--page",
        type=int,
        default=1,
        help="页码，默认: 1"
    )
    parser.add_argument(
        "--size",
        type=int,
        default=100,
        help="每页结果数（最大 10000），默认: 100"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="显示完整结果"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="获取统计信息而非搜索结果"
    )
    parser.add_argument(
        "--user-info",
        action="store_true",
        help="获取用户信息"
    )
    parser.add_argument(
        "--host-detail",
        help="获取指定主机详情"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "table"],
        default="text",
        help="输出格式，默认: text"
    )
    parser.add_argument(
        "--api-key",
        help="FOFA API 凭证（email:key 格式），不指定则从环境变量读取"
    )
    
    args = parser.parse_args()
    
    try:
        client = FOFAQuery(api_key=args.api_key)
        
        if args.user_info:
            data = client.get_user_info()
            print(format_results(data, args.format))
            return
        
        if args.host_detail:
            data = client.get_host_detail(args.host_detail)
            print(format_results(data, args.format))
            return
        
        if not args.query:
            parser.error("请提供查询语句 (-q/--query)")
        
        if args.stats:
            data = client.search_stats(args.query, args.fields)
        else:
            data = client.search(
                query=args.query,
                page=args.page,
                size=args.size,
                fields=args.fields,
                full=args.full
            )
        
        print(format_results(data, args.format))
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
