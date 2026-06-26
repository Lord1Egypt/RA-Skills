#!/usr/bin/env python3
"""
百度财经搜索 - 基于超哥方法论定制
使用百度千帆 AI 搜索 web_summary 接口
"""

import os
import sys
import json
import urllib.request
import urllib.error
import ssl
from datetime import datetime, timedelta
from typing import Optional, List, Dict

# API 配置
API_URL = "https://qianfan.baidubce.com/v2/ai_search/web_summary"

# 预设站点
SITES = {
    "xueqiu": "xueqiu.com",
    "eastmoney": "www.eastmoney.com",
    "10jqka": "www.10jqka.com.cn",
    "zhihu": "www.zhihu.com",
    "sina": "finance.sina.com.cn"
}

# 默认金融站点（雪球、知乎、东方财富、同花顺）
DEFAULT_FINANCE_SITES = ["xueqiu.com", "www.zhihu.com", "www.eastmoney.com", "www.10jqka.com.cn"]

# 默认系统指令
DEFAULT_INSTRUCTION = "金融情报专家，INTJ人格，擅长收集财经新闻，突发情况，重大事件，各个中文社区对大A和股票的讨论，重点关注雪球，知乎，东方财富，同花顺等"


def get_api_key() -> str:
    """获取百度 API Key"""
    api_key = os.environ.get("BAIDU_API_KEY")
    
    if not api_key:
        env_file = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        if os.path.exists(env_file):
            with open(env_file, "r") as f:
                for line in f:
                    if line.startswith("BAIDU_API_KEY="):
                        api_key = line.strip().split("=", 1)[1]
                        break
    
    if not api_key:
        raise ValueError("未配置 BAIDU_API_KEY")
    
    return api_key


def build_time_range(time_range: str) -> dict:
    """构建时间范围过滤"""
    if not time_range:
        return {}
    
    now = datetime.now()
    
    if time_range == "1d":
        gt = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    elif time_range == "3d":
        gt = (now - timedelta(days=3)).strftime("%Y-%m-%d")
    elif time_range == "1w":
        gt = (now - timedelta(weeks=1)).strftime("%Y-%m-%d")
    elif time_range == "1m":
        gt = (now - timedelta(days=30)).strftime("%Y-%m-%d")
    else:
        return {}
    
    return {
        "range": {
            "page_time": {
                "gt": gt
            }
        }
    }


def search(
    query: str,
    sites: List[str] = None,
    time_range: str = None,
    top_k: int = 10,
    instruction: str = None,
    messages: List[dict] = None
) -> Dict:
    """
    执行财经搜索
    
    Args:
        query: 搜索问题
        sites: 站点列表
        time_range: 时间范围（1d/3d/1w/1m）
        top_k: 返回结果数量
        instruction: 系统指令
        messages: 对话历史
    
    Returns:
        搜索结果字典
    """
    api_key = get_api_key()
    
    # 默认站点
    if sites is None:
        sites = DEFAULT_FINANCE_SITES
    
    # 默认指令
    if instruction is None:
        instruction = DEFAULT_INSTRUCTION
    
    # 构建 messages
    if messages is None:
        messages = [{"role": "user", "content": query}]
    
    # 构建请求体
    request_body = {
        "instruction": instruction,
        "messages": messages,
        "resource_type_filter": [
            {"type": "web", "top_k": top_k}
        ]
    }
    
    # 站点过滤
    if sites:
        request_body["search_filter"] = {
            "match": {
                "site": sites
            }
        }
        
        # 时间范围
        time_filter = build_time_range(time_range)
        if time_filter:
            request_body["search_filter"].update(time_filter)
    
    # 发送请求
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = json.dumps(request_body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")
    
    # 禁用 SSL 验证
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, timeout=60, context=ctx) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return {"error": f"HTTP {e.code}", "message": error_body}
    except urllib.error.URLError as e:
        return {"error": "网络错误", "message": str(e.reason)}
    
    return result


def format_output(result: Dict) -> str:
    """格式化输出"""
    if "error" in result:
        return f"❌ 搜索失败: {result['error']}\n{result.get('message', '')}"
    
    lines = []
    lines.append("\n" + "=" * 60)
    lines.append("💹 百度财经搜索结果")
    lines.append("=" * 60 + "\n")
    
    # AI 分析结果
    if "choices" in result and result["choices"]:
        content = result["choices"][0].get("message", {}).get("content", "")
        if content:
            lines.append("### AI 分析")
            lines.append(content[:3000])
            if len(content) > 3000:
                lines.append("\n... (内容已截断)")
            lines.append("")
    
    # 参考来源
    if "references" in result and result["references"]:
        lines.append("### 参考来源\n")
        for i, ref in enumerate(result["references"][:5], 1):
            title = ref.get("title", "无标题")
            url = ref.get("url", "")
            date = ref.get("date", "")
            source = ref.get("website", "")
            
            lines.append(f"{i}. **{title}**")
            if source:
                lines.append(f"   来源: {source}")
            if date:
                lines.append(f"   时间: {date}")
            if url:
                lines.append(f"   链接: {url}")
            
            # 图片
            images = []
            if ref.get("image"):
                img_data = ref["image"]
                if isinstance(img_data, dict):
                    img_url = img_data.get("url", "")
                else:
                    img_url = str(img_data)
                if img_url and not img_url.startswith("http"):
                    img_url = "http://" + img_url
                images.append(img_url)
            if ref.get("web_extensions", {}).get("images"):
                for img in ref["web_extensions"]["images"][:2]:
                    if isinstance(img, dict):
                        img_url = img.get("url", "")
                    else:
                        img_url = str(img)
                    if img_url and not img_url.startswith("http"):
                        img_url = "http://" + img_url
                    images.append(img_url)
            
            if images:
                lines.append(f"   📷 图片:")
                for img_url in images:
                    if img_url:
                        lines.append(f"   - {img_url}")
            
            lines.append("")
    
    return "\n".join(lines)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python3 search.py '<JSON参数>'")
        print()
        print("示例:")
        print('  python3 search.py \'{"query":"如何看待今日A股行情"}\'')
        print('  python3 search.py \'{"query":"半导体板块分析","sites":["xueqiu.com"],"time_range":"3d"}\'')
        sys.exit(1)
    
    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        sys.exit(1)
    
    query = params.get("query")
    if not query:
        print("错误: 缺少 query 参数")
        sys.exit(1)
    
    result = search(
        query=query,
        sites=params.get("sites"),
        time_range=params.get("time_range"),
        top_k=params.get("top_k", 10),
        instruction=params.get("instruction"),
        messages=params.get("messages")
    )
    
    print(format_output(result))
    
    # 同时输出 JSON
    print("\n" + "=" * 60)
    print("JSON 输出:")
    print("=" * 60)
    
    # 简化 JSON 输出
    output = {
        "success": "error" not in result,
        "query": query
    }
    
    if "choices" in result:
        output["ai_analysis"] = result["choices"][0].get("message", {}).get("content", "")[:500]
    
    if "references" in result:
        output["references_count"] = len(result["references"])
        output["references"] = [
            {"title": r.get("title"), "url": r.get("url"), "date": r.get("date")}
            for r in result["references"][:5]
        ]
    
    if "error" in result:
        output["error"] = result["error"]
        output["message"] = result.get("message")
    
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()