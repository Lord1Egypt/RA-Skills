"""
Claw-News Search Engine
多 API 搜索封装模块
支持 Kimi、MiniMax、Claude 搜索
"""

import os
import json
import time
import argparse
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from config import Config


class SearchResult:
    """搜索结果项"""
    
    def __init__(self, title: str, url: str, summary: str, 
                 source: str, published_at: str = None, 
                 search_api: str = None, query: str = None):
        self.title = title
        self.url = url
        self.summary = summary
        self.source = source
        self.published_at = published_at or datetime.now().isoformat()
        self.search_api = search_api
        self.query = query
        self._hash = None
    
    @property
    def hash(self) -> str:
        """生成唯一标识（用于去重）"""
        if self._hash is None:
            import hashlib
            self._hash = hashlib.md5(self.url.encode()).hexdigest()[:12]
        return self._hash
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "summary": self.summary,
            "source": self.source,
            "published_at": self.published_at,
            "search_api": self.search_api,
            "query": self.query,
            "hash": self.hash
        }


class SearchEngine:
    """搜索引擎 - 多 API 轮询"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.timeout = self.config.settings.api_timeout
        self.lookback_hours = self.config.settings.search_lookback_hours
    
    def search(self, query: str, time_range: str = None) -> Dict:
        """
        执行搜索，自动轮询多个 API
        
        Returns:
            {
                "success": bool,
                "source": str,  # 成功使用的 API
                "results": List[SearchResult],
                "error": str (可选)
            }
        """
        if time_range is None:
            # 默认搜索过去 24 小时
            end_date = datetime.now()
            start_date = end_date - timedelta(hours=self.lookback_hours)
            time_range = f"{start_date.strftime('%Y-%m-%d')}_to_{end_date.strftime('%Y-%m-%d')}"
        
        available_apis = self.config.get_available_apis()
        
        if not available_apis:
            return {
                "success": False,
                "source": None,
                "results": [],
                "error": "未配置任何 API Key"
            }
        
        # 按优先级尝试 API
        for api_name in self.config.API_PRIORITY:
            if api_name not in available_apis:
                continue
            
            try:
                print(f"🔍 尝试使用 {api_name.upper()} 搜索: {query}")
                results = self._search_with_api(api_name, query, time_range)
                
                if results and len(results) > 0:
                    print(f"✅ {api_name.upper()} 返回 {len(results)} 条结果")
                    return {
                        "success": True,
                        "source": api_name,
                        "results": results
                    }
                else:
                    print(f"⚠️ {api_name.upper()} 未返回结果，尝试下一个 API")
                    
            except Exception as e:
                print(f"❌ {api_name.upper()} 搜索失败: {e}")
                continue
        
        return {
            "success": False,
            "source": None,
            "results": [],
            "error": "所有 API 均搜索失败"
        }
    
    def _search_with_api(self, api_name: str, query: str, time_range: str) -> List[SearchResult]:
        """使用指定 API 搜索"""
        if api_name == "minimax":
            return self._search_minimax(query, time_range)
        elif api_name == "tavily":
            return self._search_tavily(query, time_range)
        else:
            raise ValueError(f"不支持的 API: {api_name}")
    
    def _search_kimi(self, query: str, time_range: str) -> List[SearchResult]:
        """使用 Kimi API 搜索"""
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=self.config.api_keys["kimi"],
                base_url="https://api.moonshot.cn/v1"
            )
            
            # 构建搜索提示
            prompt = f"""搜索关于"{query}"的最新新闻和动态。
时间范围：过去{self.lookback_hours}小时内。
请返回 5-10 条相关新闻，每条包含：标题、来源网站、URL链接、简短摘要、发布时间。
请确保结果格式化为 JSON 数组。"""

            response = client.chat.completions.create(
                model="kimi-k2-5",  # 使用正确的模型名
                messages=[
                    {"role": "system", "content": "你是一个新闻搜索助手，专门搜索和整理最新资讯。请以结构化格式返回搜索结果。"},
                    {"role": "user", "content": prompt}
                ],
                tools=[{
                    "type": "builtin_function",
                    "function": {"name": "web_search"}
                }],
                temperature=0.3,
                timeout=self.timeout
            )
            
            # 解析结果
            content = response.choices[0].message.content
            return self._parse_search_results(content, "kimi", query)
            
        except Exception as e:
            print(f"Kimi API 错误: {e}")
            return []
    
    def _search_minimax(self, query: str, time_range: str) -> List[SearchResult]:
        """使用 MiniMax MCP web_search 搜索（通过 Coding Plan）"""
        if not self.config.api_keys.get('minimax'):
            print("⚠️ MiniMax API 未配置，跳过")
            return []
        
        try:
            import subprocess
            
            # MCP client 路径
            mcp_client = os.path.join(
                os.path.expanduser("~"), ".openclaw", "workspace",
                "skills", "minimax-mcp-call", "scripts", "mcp_client.mjs"
            )
            
            if not os.path.exists(mcp_client):
                print("⚠️ MiniMax MCP client 未找到，跳过")
                return []
            
            env = os.environ.copy()
            env["MINIMAX_API_KEY"] = self.config.api_keys['minimax']
            env["MINIMAX_API_HOST"] = "https://api.minimaxi.com"
            
            result = subprocess.run(
                ["node", mcp_client, "web_search", query],
                capture_output=True, text=True, timeout=60, env=env
            )
            
            if result.returncode != 0:
                print(f"⚠️ MiniMax MCP 错误: {result.stderr[:200]}")
                return []
            
            # 解析 MCP 返回的 JSON（stdout 前面有日志行，需要精确提取）
            output = result.stdout.strip()
            # 找到最外层 JSON 对象（MCP 返回 {"content": [...], ...}）
            brace_start = output.find('{')
            if brace_start == -1:
                print("⚠️ MiniMax MCP 无 JSON 输出")
                return []
            
            # 从第一个 { 开始，找到匹配的 }
            depth = 0
            json_end = -1
            for i in range(brace_start, len(output)):
                if output[i] == '{':
                    depth += 1
                elif output[i] == '}':
                    depth -= 1
                    if depth == 0:
                        json_end = i + 1
                        break
            
            if json_end == -1:
                print("⚠️ MiniMax MCP JSON 不完整")
                return []
            
            json_str = output[brace_start:json_end]
            data = json.loads(json_str)
            
            # MCP web_search 返回格式: {"content": [{"type": "text", "text": "<json>"}]}
            # text 内部是 JSON: {"organic": [{"title", "link", "snippet", "date"}], "base_resp": ...}
            results = []
            content_items = data.get("content", [])
            for item in content_items:
                if item.get("type") != "text":
                    continue
                text = item.get("text", "")
                try:
                    inner = json.loads(text)
                    organic = inner.get("organic", [])
                    for entry in organic:
                        result = SearchResult(
                            title=entry.get("title", "").strip(),
                            url=entry.get("link", ""),
                            summary=entry.get("snippet", "").strip(),
                            source="minimax",
                            published_at=entry.get("date", ""),
                            query=query
                        )
                        if result.title and result.url:
                            results.append(result)
                except (json.JSONDecodeError, AttributeError):
                    # fallback: 用通用解析
                    parsed = self._parse_search_results(text, "minimax", query)
                    if parsed:
                        results.extend(parsed)
            
            return results
            
        except subprocess.TimeoutExpired:
            print("⚠️ MiniMax MCP 超时")
            return []
        except Exception as e:
            print(f"MiniMax MCP 错误: {e}")
            return []
    
    def _search_tavily(self, query: str, time_range: str) -> List[SearchResult]:
        """使用 Tavily AI Search API 搜索"""
        if not self.config.api_keys.get('tavily'):
            print("⚠️ Tavily API 未配置，跳过")
            return []
        
        try:
            import requests
            
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": self.config.api_keys['tavily'],
                "query": query,
                "search_depth": "basic",
                "max_results": 10,
                "include_answer": False,
                "include_raw_content": False,
            }
            
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get("results", []):
                result = SearchResult(
                    title=item.get("title", "").strip(),
                    url=item.get("url", ""),
                    summary=item.get("content", "").strip(),
                    source="tavily",
                    published_at=item.get("published_date", ""),
                    query=query
                )
                if result.title and result.url:
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Tavily API 错误: {e}")
            return []
    
    def _search_claude(self, query: str, time_range: str) -> List[SearchResult]:
        """使用 Brave Search + Claude API 搜索（已弃用）"""
        # Claude API 未配置，跳过
        if not self.config.api_keys.get('claude'):
            print("⚠️ Claude API 未配置，跳过")
            return []
        
        # 首先使用 Brave Search 获取搜索结果
        brave_results = self._brave_search(query, time_range)
        if not brave_results:
            print("⚠️ Brave 搜索未配置或无结果，跳过 Claude 搜索")
            return []
        
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.config.api_keys["claude"])
            
            # 将 Brave 结果格式化为文本供 Claude 分析
            search_context = "\n\n".join([
                f"[{i+1}] {r.get('title', '')}\nURL: {r.get('url', '')}\n{r.get('description', '')}"
                for i, r in enumerate(brave_results[:10])
            ])
            
            prompt = f"""基于以下搜索结果，提取关于"{query}"的最新新闻信息。

搜索结果：
{search_context}

请分析以上结果，提取最相关的新闻，返回 JSON 数组格式：
[
  {{
    "title": "新闻标题",
    "url": "完整URL",
    "summary": "简短摘要",
    "source": "来源网站",
    "published_at": "发布时间"
  }}
]

注意：
- 只返回 JSON 数组，不要其他说明文字
- 最多返回 5 条最相关的结果
- 确保 URL 是完整的"""

            response = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            content = response.content[0].text if response.content else ""
            return self._parse_search_results(content, "claude", query)
            
        except Exception as e:
            print(f"Claude API 错误: {e}")
            # 如果 Claude 处理失败，直接返回 Brave 结果
            return self._brave_results_to_search_results(brave_results, query)
    
    def _brave_search(self, query: str, time_range: str) -> List[Dict]:
        """使用 Brave Search API 搜索"""
        api_key = os.getenv("BRAVE_API_KEY", "")
        if not api_key:
            return []
        
        try:
            import requests
            
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                "X-Subscription-Token": api_key,
                "Accept": "application/json"
            }
            
            params = {
                "q": query,
                "count": 10,
                "freshness": "day"  # 过去 24 小时
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get("web", {}).get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "description": item.get("description", ""),
                    "source": item.get("meta", {}).get("domain", "")
                })
            
            return results
            
        except Exception as e:
            print(f"Brave Search 错误: {e}")
            return []
    
    def _brave_results_to_search_results(self, brave_results: List[Dict], query: str) -> List[SearchResult]:
        """将 Brave 结果直接转换为 SearchResult"""
        results = []
        for item in brave_results:
            result = SearchResult(
                title=item.get("title", "未知标题"),
                url=item.get("url", ""),
                summary=item.get("description", ""),
                source=item.get("source", "web"),
                search_api="brave",
                query=query
            )
            results.append(result)
        return results
    
    def _parse_search_results(self, content: str, api_name: str, query: str) -> List[SearchResult]:
        """解析搜索结果文本为结构化数据"""
        results = []
        
        if not content:
            return results
        
        # 尝试提取 JSON
        try:
            # 查找 JSON 代码块
            import re
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', content)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = content
            
            # 尝试解析 JSON
            data = json.loads(json_str.strip())
            
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict) and "results" in data:
                items = data["results"]
            elif isinstance(data, dict) and "news" in data:
                items = data["news"]
            else:
                items = [data]
            
            for item in items:
                if isinstance(item, dict):
                    result = SearchResult(
                        title=item.get("title", item.get("标题", "未知标题")),
                        url=item.get("url", item.get("link", item.get("URL", "#"))),
                        summary=item.get("summary", item.get("摘要", item.get("description", ""))),
                        source=item.get("source", item.get("来源", api_name)),
                        published_at=item.get("published_at", item.get("时间", item.get("date", ""))),
                        search_api=api_name,
                        query=query
                    )
                    results.append(result)
                    
        except json.JSONDecodeError:
            # JSON 解析失败，尝试文本解析
            print(f"⚠️ JSON 解析失败，尝试文本解析...")
            results = self._parse_text_results(content, api_name, query)
        
        return results
    
    def _parse_text_results(self, content: str, api_name: str, query: str) -> List[SearchResult]:
        """从文本中提取搜索结果"""
        results = []
        import re
        
        # 简单的标题-URL 匹配模式
        lines = content.split('\n')
        current_item = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 匹配 URL
            url_match = re.search(r'https?://[^\s\)]+', line)
            if url_match:
                if current_item.get('title'):
                    results.append(SearchResult(
                        title=current_item.get('title', '未知标题'),
                        url=url_match.group(),
                        summary=current_item.get('summary', ''),
                        source=api_name,
                        search_api=api_name,
                        query=query
                    ))
                    current_item = {}
                current_item['url'] = url_match.group()
            elif len(line) > 10 and not line.startswith('http'):
                if not current_item.get('title'):
                    current_item['title'] = line[:100]
                else:
                    current_item['summary'] = line[:500]
        
        return results


def main():
    """命令行测试"""
    parser = argparse.ArgumentParser(description="Claw-News Search Engine")
    parser.add_argument("--query", "-q", type=str, required=True, help="搜索关键词")
    parser.add_argument("--api", "-a", type=str, choices=["minimax", "tavily"],
                       help="指定 API (默认自动轮询)")
    
    args = parser.parse_args()
    
    engine = SearchEngine()
    result = engine.search(args.query)
    
    if result["success"]:
        print(f"\n✅ 搜索成功 (使用 {result['source']})")
        print(f"找到 {len(result['results'])} 条结果:\n")
        
        for i, r in enumerate(result['results'][:5], 1):
            print(f"{i}. {r.title}")
            print(f"   来源: {r.source}")
            print(f"   URL: {r.url}")
            print(f"   摘要: {r.summary[:100]}..." if len(r.summary) > 100 else f"   摘要: {r.summary}")
            print()
    else:
        print(f"❌ 搜索失败: {result.get('error', '未知错误')}")


if __name__ == "__main__":
    main()
