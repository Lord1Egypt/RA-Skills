"""搜索模块

提供牛客网内容搜索和详情获取功能。
"""

import re
import time
import ssl
from typing import Dict, List, Optional
from dataclasses import dataclass

import requests
import urllib3
from pydantic import BaseModel, Field

# ==================== OpenSSL 3.0 兼容性修复 ====================
# Python 3.13 使用 OpenSSL 3.0，默认 SECLevel=2 过于严格
# 降低安全级别以兼容某些旧服务器

# 全局设置 SSL 安全级别
try:
    import os
    os.environ['OPENSSL_CONF'] = ''
except Exception:
    pass

# 禁用 SSL 验证警告（仅用于调试）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 创建自定义 SSL Adapter
class SSLAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        # 创建兼容 OpenSSL 3.0 的 SSL 上下文
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        # 降低安全级别
        try:
            context.set_ciphers('DEFAULT@SECLEVEL=0')
        except Exception:
            context.set_ciphers('ALL')
        # 不验证证书
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        kwargs['ssl_context'] = context
        kwargs['assert_hostname'] = False
        return super().init_poolmanager(*args, **kwargs)

# 使用自定义 Session
session = requests.Session()
session.mount('https://', SSLAdapter())


# ==================== 数据模型 ====================


class SearchRecord(BaseModel):
    """搜索记录（搜索结果）"""

    title: str = Field(description="文章标题")
    rc_type: int = Field(
        description="内容类型：201=Feed（动态），207=讨论帖"
    )
    uuid: str = Field(default="", description="文章UUID（rc_type=201时使用）")
    content_id: str = Field(default="", description="内容ID（rc_type=207时使用）")
    created_at: int = Field(default=0, description="创建时间戳（毫秒）")
    edit_time: int = Field(default=0, description="修改时间戳（毫秒）")
    view_count: int = Field(default=0, description="浏览量")
    like_count: int = Field(default=0, description="点赞数")
    comment_count: int = Field(default=0, description="评论数")
    company: str = Field(default="", description="认证公司名称")
    job_title: str = Field(default="", description="认证岗位名称")


class FeedDetail(BaseModel):
    """Feed详情（动态类型）"""

    title: str = Field(description="文章标题")
    content: str = Field(description="文章完整内容")
    uuid: str = Field(default="", description="文章UUID")
    url: str = Field(default="", description="文章访问链接")


class DiscussDetail(BaseModel):
    """讨论帖详情（rcType=207）"""

    title: str = Field(description="帖子标题")
    content: str = Field(description="帖子完整内容")
    content_id: str = Field(default="", description="内容ID")
    url: str = Field(default="", description="帖子访问链接")


class SearchResult(BaseModel):
    """搜索结果"""

    current: int = Field(description="当前页码")
    size: int = Field(description="当页文章数量")
    total: int = Field(description="文章总数")
    total_page: int = Field(description="总页数")
    records: List[SearchRecord] = Field(description="搜索结果列表")


# ==================== API 配置 ====================

NOWCODER_API_URL = "https://gw-c.nowcoder.com/api/sparta/pc/search"
NOWCODER_DETAIL_URL = "https://www.nowcoder.com/feed/main/detail"
NOWCODER_DISCUSS_API_URL = "https://gw-c.nowcoder.com/api/sparta/detail/content-data/detail"
NOWCODER_DISCUSS_URL = "https://www.nowcoder.com/discuss"
REQUEST_TIMEOUT = 30

TAG_OPTIONS = {
    818: "面经",
    861: "求职进度",
    823: "内推",
    856: "公司评价",
}

VALID_TAG_IDS = list(TAG_OPTIONS.keys())
VALID_ORDER_VALUES = ["", "create"]


# ==================== 工具函数 ====================


def html_to_text(html: str) -> str:
    """将 HTML 内容转换为纯文本

    Args:
        html: HTML 格式的内容

    Returns:
        纯文本内容
    """
    if not html:
        return ""

    # 移除 script 和 style 标签及其内容
    html = re.sub(
        r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE
    )
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)

    # 将常见的块级标签转换为换行
    html = re.sub(r"</?(p|div|br|h[1-6]|li|tr)[^>]*>", "\n", html, flags=re.IGNORECASE)

    # 移除所有其他 HTML 标签
    html = re.sub(r"<[^>]+>", "", html)

    # 处理 HTML 实体
    html = html.replace("&nbsp;", " ")
    html = html.replace("&amp;", "&")
    html = html.replace("&lt;", "<")
    html = html.replace("&gt;", ">")
    html = html.replace("&quot;", '"')
    html = html.replace("&#39;", "'")
    html = html.replace("\xa0", " ")

    # 合并多个连续换行为最多两个
    html = re.sub(r"\n\s*\n", "\n\n", html)

    # 去除首尾空白
    return html.strip()


def search_nowcoder_api(
    query: str,
    page: int = 1,
    tag: Optional[int] = None,
    order: str = "",
) -> dict:
    """调用牛客网搜索 API

    Args:
        query: 搜索关键词
        page: 页码，从1开始
        tag: 标签筛选 ID
        order: 排序方式

    Returns:
        API 响应数据
    """
    # 构建 tag 参数
    tag_list = []
    if tag and tag in TAG_OPTIONS:
        tag_list = [{"name": TAG_OPTIONS[tag], "id": tag, "count": None}]

    payload = {
        "type": "all",
        "query": query,
        "page": page,
        "tag": tag_list,
        "order": order,
        "gioParams": {
            "searchFrom_var": "顶部导航栏",
            "searchEnter_var": "主站",
        },
    }

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    response = session.post(
        NOWCODER_API_URL, json=payload, headers=headers, timeout=REQUEST_TIMEOUT, verify=False
    )
    response.raise_for_status()
    return response.json()


def parse_search_response(response_data: dict, time_window_days: Optional[int] = None) -> SearchResult:
    """解析搜索响应数据

    Args:
        response_data: API 响应数据
        time_window_days: 时间窗口（天），用于过滤结果

    Returns:
        解析后的搜索结果
    """
    data = response_data.get("data", {})
    records_raw = data.get("records", [])

    records = []
    for record in records_raw:
        rc_type = record.get("rc_type", 0)
        record_data = record.get("data", {})

        # 跳过 data 不是 dict 的记录（如职位推荐 rc_type=213）
        if not isinstance(record_data, dict):
            continue

        user_brief = record_data.get("userBrief", {})
        frequency_data = record_data.get("frequencyData", {})

        # 提取认证信息
        identity_list = user_brief.get("identityList") or []
        company = ""
        job_title = ""
        if identity_list and len(identity_list) > 0:
            first_identity = identity_list[0]
            company = first_identity.get("companyName", "")
            job_title = first_identity.get("jobName", "")

        # 根据 rc_type 处理不同类型
        if rc_type == 201:
            # Feed类型
            moment_data = record_data.get("momentData", {})
            if not moment_data:
                continue
            records.append(
                SearchRecord(
                    title=moment_data.get("title", ""),
                    rc_type=rc_type,
                    uuid=moment_data.get("uuid", ""),
                    content_id="",
                    created_at=moment_data.get("createdAt", 0),
                    edit_time=moment_data.get("editTime", 0),
                    view_count=frequency_data.get("viewCnt", 0),
                    like_count=frequency_data.get("likeCnt", 0),
                    comment_count=frequency_data.get("commentCnt", 0),
                    company=company,
                    job_title=job_title,
                )
            )
        elif rc_type == 207:
            # 讨论帖类型
            content_data = record_data.get("contentData", {})
            if not content_data:
                continue
            records.append(
                SearchRecord(
                    title=content_data.get("title", ""),
                    rc_type=rc_type,
                    uuid="",
                    content_id=str(content_data.get("id", "")),
                    created_at=content_data.get("createTime", 0),
                    edit_time=content_data.get("editTime", 0),
                    view_count=frequency_data.get("viewCnt", 0),
                    like_count=frequency_data.get("likeCnt", 0),
                    comment_count=frequency_data.get("commentCnt", 0),
                    company=company,
                    job_title=job_title,
                )
            )

    # 应用时间窗口过滤
    if time_window_days and time_window_days > 0:
        from datetime import datetime, timedelta
        cutoff_time = int((datetime.now() - timedelta(days=time_window_days)).timestamp() * 1000)
        records = [r for r in records if r.created_at >= cutoff_time]

    return SearchResult(
        current=data.get("current", 1),
        size=data.get("size", 0),
        total=data.get("total", 0),
        total_page=data.get("totalPage", 0),
        records=records,
    )


def get_feed_detail_from_page(uuid: str) -> FeedDetail:
    """从网页获取Feed详情

    Args:
        uuid: 文章UUID

    Returns:
        Feed详情
    """
    if not uuid:
        raise ValueError("需要提供 uuid 参数")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    url = f"{NOWCODER_DETAIL_URL}/{uuid}"

    response = session.get(url, headers=headers, timeout=REQUEST_TIMEOUT, verify=False)
    response.raise_for_status()
    html = response.text

    # 检查内容是否存在
    if "内容不存在!" in html:
        raise ValueError(
            f"内容不存在! 请检查输入的uuid是否正确。"
            f"注意：此工具仅适用于Feed类型（动态），如果是讨论帖类型（rcType=207），请使用 get_discuss_details 工具。"
        )

    # 提取 title
    title_match = re.search(r'"title":"([^"]+)"', html)
    title = title_match.group(1) if title_match else ""

    # 提取正文
    content = ""

    # 直接从页面中的 feed-content-text 区块提取
    content_match = re.search(
        r'<div[^>]*class="[^"]*feed-content-text[^"]*"[^>]*>(.*?)</div>',
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if content_match:
        content_html = content_match.group(1)
        content = html_to_text(content_html)

    # 回退到 JSON 片段提取
    if not content:
        content_matches = re.findall(r'"content":"([^"]+)"', html)
        for match in content_matches:
            if len(match) > 100 and "..." not in match:
                content = match
                break
        if content:
            content = (
                content.replace("\\n", "\n")
                .replace("\\u002F", "/")
                .replace("\\t", "\t")
            )

    return FeedDetail(
        title=title,
        content=content,
        uuid=uuid,
        url=url,
    )


def get_discuss_detail_from_api(content_id: str) -> DiscussDetail:
    """从API获取讨论帖详情

    Args:
        content_id: 内容ID

    Returns:
        讨论帖详情
    """
    if not content_id:
        raise ValueError("需要提供 content_id 参数")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    api_url = f"{NOWCODER_DISCUSS_API_URL}/{content_id}"
    page_url = f"{NOWCODER_DISCUSS_URL}/{content_id}"

    response = requests.get(api_url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    data = response.json()

    # 检查API响应是否成功
    if not data.get("success"):
        raise ValueError(
            f"内容不存在或请求失败! 请检查输入的content_id是否正确。"
            f"注意：此工具仅适用于讨论帖类型（rcType=207）。"
        )

    content_data = data.get("data", {})

    # 将HTML内容转换为纯文本
    rich_text = content_data.get("richText", "") or content_data.get("content", "")
    plain_content = html_to_text(rich_text)

    return DiscussDetail(
        title=content_data.get("title", ""),
        content=plain_content,
        content_id=content_id,
        url=page_url,
    )


# ==================== 高级搜索函数 ====================


def search_posts(
    keywords: List[str],
    max_pages: int = 1,
    tag: Optional[int] = None,
    order: str = "create",
    delay: float = 2.0,
    max_results: int = 10,
    time_window_days: Optional[int] = None,
) -> Dict[str, SearchResult]:
    """搜索多个关键词的帖子

    Args:
        keywords: 关键词列表
        max_pages: 每个关键词最大获取页数
        tag: 标签筛选ID
        order: 排序方式
        delay: 请求延迟（秒）
        max_results: 每个关键词最大返回结果数，默认为10
        time_window_days: 时间窗口（天），用于过滤结果

    Returns:
        字典，键为关键词，值为搜索结果
    """
    results = {}

    # 校验参数
    if tag is not None and tag not in VALID_TAG_IDS:
        raise ValueError(f"无效的标签ID，可选值：{VALID_TAG_IDS}")
    if order not in VALID_ORDER_VALUES:
        raise ValueError(f"无效的排序方式，可选值：{VALID_ORDER_VALUES}")

    for idx, keyword in enumerate(keywords):
        try:
            # 添加延迟（第一个请求不需要）
            if idx > 0 and delay > 0:
                time.sleep(delay)

            # 先获取第一页
            first_response = search_nowcoder_api(keyword, page=1, tag=tag, order=order)
            if not first_response.get("success"):
                results[keyword] = SearchResult(
                    current=1, size=0, total=0, total_page=0, records=[]
                )
                continue

            first_result = parse_search_response(first_response, time_window_days)
            total_page = first_result.total_page

            # 收集所有记录
            all_records = list(first_result.records)
            seen_ids = set()
            for record in all_records:
                if record.uuid:
                    seen_ids.add(record.uuid)
                elif record.content_id:
                    seen_ids.add(record.content_id)

            # 如果已经达到 max_results，直接返回
            if len(all_records) >= max_results:
                results[keyword] = SearchResult(
                    current=1,
                    size=max_results,
                    total=first_result.total,
                    total_page=total_page,
                    records=all_records[:max_results],
                )
                continue

            # 确定需要获取的页数
            if max_pages <= 0:
                pages_to_fetch = total_page
            else:
                pages_to_fetch = min(max_pages, total_page)

            # 获取剩余页面，直到达到 max_results
            for page in range(2, pages_to_fetch + 1):
                try:
                    if delay > 0:
                        time.sleep(delay)

                    response_data = search_nowcoder_api(keyword, page=page, tag=tag, order=order)
                    if response_data.get("success"):
                        page_result = parse_search_response(response_data, time_window_days)
                        for record in page_result.records:
                            record_id = record.uuid if record.uuid else record.content_id
                            if record_id and record_id not in seen_ids:
                                seen_ids.add(record_id)
                                all_records.append(record)
                                # 达到 max_results 时停止
                                if len(all_records) >= max_results:
                                    break
                        if len(all_records) >= max_results:
                            break
                except Exception:
                    continue

            results[keyword] = SearchResult(
                current=1,
                size=min(len(all_records), max_results),
                total=first_result.total,
                total_page=total_page,
                records=all_records[:max_results],
            )

        except Exception as e:
            results[keyword] = SearchResult(
                current=1, size=0, total=0, total_page=0, records=[]
            )

    return results


def get_post_detail(record: SearchRecord) -> Optional[FeedDetail | DiscussDetail]:
    """获取帖子详情

    Args:
        record: 搜索记录

    Returns:
        帖子详情，失败返回 None
    """
    try:
        if record.rc_type == 201:
            return get_feed_detail_from_page(uuid=record.uuid)
        elif record.rc_type == 207:
            return get_discuss_detail_from_api(content_id=record.content_id)
    except Exception:
        return None

    return None
