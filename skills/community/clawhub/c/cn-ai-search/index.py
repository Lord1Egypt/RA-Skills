#!/usr/bin/env python3
import click
import requests
import sys
from urllib.parse import quote
from typing import List, Dict, Optional
import config

class SearchResult:
    def __init__(self, title: str, abstract: str, url: str, source: str, publish_time: str = None, hot_score: int = 0):
        self.title = title.strip()
        self.abstract = abstract.strip()
        self.url = url.strip()
        self.source = source.strip()
        self.publish_time = publish_time
        self.hot_score = hot_score

    def to_dict(self):
        return {
            "title": self.title,
            "abstract": self.abstract,
            "url": self.url,
            "source": self.source,
            "publish_time": self.publish_time,
            "hot_score": self.hot_score
        }

def search_via_jina(url: str, keyword: str, source_name: str, count: int = 5) -> List[SearchResult]:
    """通用搜索方法，通过Jina Reader获取内容然后解析"""
    results = []
    bad_titles = [
        "首页", "百度首页", "登录", "注册", "图片", "相关搜索", "换一换",
        "反馈成功", "热搜榜", "导航", "菜单", "搜索", "稍后再看", "抗击肺炎",
        "transferable skill", "blob:", "Image", "###", "[", "]", ""
    ]
    bad_urls = [
        "javascript:void", "baidu.com/img/", "voice.baidu.com/act",
        ".jpg", ".png", ".jpeg", ".gif", "blob:"
    ]
    
    try:
        jina_url = f"https://r.jina.ai/{url}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        if hasattr(config, 'JINA_API_KEY') and config.JINA_API_KEY:
            headers["Authorization"] = f"Bearer {config.JINA_API_KEY}"
        response = requests.get(jina_url, headers=headers, timeout=30)
        content = response.text
        lines = content.split('\n')
        
        for line in lines:
            if len(results) >= count:
                break
            if not line.strip():
                continue
            if line.startswith('[') and '](' in line:
                # 提取链接
                title_part = line.split(']')[0][1:]
                url_part = line.split('](')[1].split(')')[0]
                
                # 过滤垃圾标题和图片链接
                title_clean = title_part.strip().replace('#', '').replace('###', '').replace('', '').strip()
                if any(bad in title_clean for bad in bad_titles):
                    continue
                if len(title_clean) < 5:
                    continue
                if any(bad in url_part for bad in bad_urls):
                    continue
                if url_part == 'https://www.baidu.com/':
                    continue
                    
                # 找摘要
                abstract = ""
                idx = lines.index(line)
                for next_line in lines[idx + 1:]:
                    next_clean = next_line.strip()
                    if next_clean and not next_clean.startswith('['):
                        if not any(bad in next_clean for bad in bad_titles):
                            abstract = next_clean
                            break
                            
                results.append(SearchResult(
                    title=title_clean,
                    abstract=abstract,
                    url=url_part,
                    source=source_name
                ))
                
        return results
    except Exception as e:
        print(f"{source_name}搜索失败: {e}", file=sys.stderr)
        return []

def search_multi_engine(keyword: str, engines: List[str], count_per_engine: int = 5) -> List[SearchResult]:
    """多个中文搜索引擎"""
    results = []
    
    # 搜索引擎配置
    engine_configs = {
        "baidu": ("百度", f"https://www.baidu.com/s?wd={quote(keyword)}"),
        "bing_cn": ("必应中国", f"https://cn.bing.com/search?q={quote(keyword)}"),
        "360": ("360搜索", f"https://www.so.com/s?q={quote(keyword)}"),
        "sogou": ("搜狗", f"https://sogou.com/web?query={quote(keyword)}"),
        "weixin": ("微信公众号", f"https://wx.sogou.com/weixin?type=2&query={quote(keyword)}"),
        "toutiao": ("头条", f"https://so.toutiao.com/search?keyword={quote(keyword)}"),
        "zhihu": ("知乎", f"https://www.zhihu.com/search?q={quote(keyword)}"),
        "bilibili": ("B站", f"https://search.bilibili.com/all?keyword={quote(keyword)}"),
    }
    
    for engine in engines:
        if engine not in engine_configs:
            continue
        source_name, url = engine_configs[engine]
        results.extend(search_via_jina(url, keyword, source_name, count_per_engine))
    
    return results

def deduplicate_results(results: List[SearchResult]) -> List[SearchResult]:
    """去重结果，按URL和标题去重"""
    seen_urls = set()
    seen_titles = set()
    unique_results = []
    
    for result in results:
        url_key = result.url.split('?')[0]  # 去掉query参数去重
        if url_key not in seen_urls and result.title not in seen_titles:
            seen_urls.add(url_key)
            seen_titles.add(result.title)
            unique_results.append(result)
    
    return unique_results

def sort_results(results: List[SearchResult], sort_type: str) -> List[SearchResult]:
    """排序结果"""
    if sort_type == "hot":
        # 按热度排序
        return sorted(results, key=lambda x: x.hot_score, reverse=True)
    else:  # relevance / latest
        # 默认保持原顺序
        return results

def format_output(results: List[SearchResult], format_type: str = "markdown") -> str:
    """格式化输出"""
    if not results:
        return "❌ 未找到相关结果"
    
    if format_type == "markdown":
        output = f"## 🔍 搜索结果（共{len(results)}条）\n\n"
        for i, result in enumerate(results, 1):
            output += f"### {i}. [{result.title}]({result.url})\n"
            output += f"**来源**：{result.source}\n"
            if result.abstract:
                output += f"**摘要**：{result.abstract}\n"
            if result.publish_time:
                output += f"**发布时间**：{result.publish_time}\n"
            output += "\n"
        return output
    else:  # plain
        output = f"搜索结果（共{len(results)}条）\n\n"
        for i, result in enumerate(results, 1):
            output += f"{i}. {result.title}\n"
            output += f"来源：{result.source}\n"
            output += f"链接：{result.url}\n"
            if result.abstract:
                output += f"摘要：{result.abstract}\n"
            output += "\n"
        return output

@click.command()
@click.argument("keyword")
@click.option("--platforms", "-p", default="baidu,weixin,zhihu,bilibili", help="指定搜索平台，多个用逗号分隔：baidu,bing_cn,360,sogou,weixin,toutiao,zhihu,bilibili")
@click.option("--sort", "-s", default="relevance", help="排序方式：relevance(最相关)/hot(最热)")
@click.option("--format", "-f", default="markdown", help="输出格式：markdown/plain")
@click.option("--count", "-c", default=20, help="返回结果总数量")
@click.option("--count-per-platform", "-m", default=5, help="每个平台返回结果数量")
def main(keyword, platforms, sort, format, count, count_per_platform):
    """
    🇨🇳 中文AI Agent专用聚合搜索工具（轻量版）
    一次查询覆盖全网主流中文平台，自动去重过滤广告
    """
    # 解析平台
    platform_list = [p.strip() for p in platforms.split(",")]
    
    # 只支持基础平台
    supported_platforms = ["baidu", "bing_cn", "360", "sogou", "weixin", "toutiao", "zhihu", "bilibili"]
    platform_list = [p for p in platform_list if p in supported_platforms]
    
    # 执行搜索
    all_results = []
    
    # 通用引擎搜索
    if platform_list:
        results = search_multi_engine(keyword, platform_list, count_per_platform)
        all_results.extend(results)
    
    # 处理结果
    all_results = deduplicate_results(all_results)
    all_results = sort_results(all_results, sort)
    all_results = all_results[:count]
    
    # 输出
    output = format_output(all_results, format)
    click.echo(output)

if __name__ == "__main__":
    main()
