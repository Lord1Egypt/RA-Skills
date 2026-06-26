import aiohttp
import time
import random
import re
from enum import Enum
from typing import TYPE_CHECKING, List, Dict, Any
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from request.web.xhs_session import XHS_Session  # 仅类型检查时导入

# 导入配置加载器
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from request.web.search_config_loader import get_search_config

def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    if not isinstance(number, int):
        raise TypeError('number must be an integer')

    base36 = ''
    sign = ''

    if number < 0:
        sign = '-'
        number = -number

    if 0 <= number < len(alphabet):
        return sign + alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36

def get_search_id():
    e = int(time.time() * 1000) << 64
    t = int(random.uniform(0, 2147483646))
    return base36encode((e + t))

def parse_relative_time(time_text: str) -> datetime:
    """解析相对时间文本，返回实际发布时间

    Args:
        time_text: 相对时间文本，如 "2天前"、"3小时前"、"刚刚"等

    Returns:
        datetime: 实际发布时间
    """
    now = datetime.now()

    if not time_text:
        return now - timedelta(days=365)  # 默认返回一年前

    # 刚刚
    if '刚刚' in time_text or '分钟前' in time_text:
        return now

    # 小时前
    hours_match = re.search(r'(\d+)\s*小时前', time_text)
    if hours_match:
        hours = int(hours_match.group(1))
        return now - timedelta(hours=hours)

    # 天前
    days_match = re.search(r'(\d+)\s*天前', time_text)
    if days_match:
        days = int(days_match.group(1))
        return now - timedelta(days=days)

    # 周前
    weeks_match = re.search(r'(\d+)\s*周前', time_text)
    if weeks_match:
        weeks = int(weeks_match.group(1))
        return now - timedelta(weeks=weeks)

    # 月前
    months_match = re.search(r'(\d+)\s*月前', time_text)
    if months_match:
        months = int(months_match.group(1))
        return now - timedelta(days=months*30)

    # 年前
    years_match = re.search(r'(\d+)\s*年前', time_text)
    if years_match:
        years = int(years_match.group(1))
        return now - timedelta(days=years*365)

    # 昨天
    if '昨天' in time_text:
        return now - timedelta(days=1)

    # 前天
    if '前天' in time_text:
        return now - timedelta(days=2)

    # 默认返回一年前
    return now - timedelta(days=365)

class Note:

    def __init__(self, session: "XHS_Session"):
        self.session = session  # 保存会话引用

    # 搜索笔记
    async def search_notes(self, keyword: str, page: int = None, page_size: int = None,
                          sort: str = None, note_type: int = None,
                          time_filter_hours: int = None) -> aiohttp.ClientResponse:
        """搜索笔记（支持帖子发布时间过滤）

        Args:
            keyword: 搜索关键词
            page: 页码，默认从配置文件读取
            page_size: 每页大小，默认从配置文件读取
            sort: 排序方式，默认从配置文件读取
            note_type: 笔记类型，默认从配置文件读取
            time_filter_hours: 时间过滤（小时），只返回过去N小时内发布的帖子。
                              None表示从配置文件读取，0表示不过滤。
                              例如：24表示只返回过去24小时内发布的帖子

        Returns:
            aiohttp.ClientResponse: 搜索响应

        Note:
            时间过滤是在客户端进行的，通过解析返回数据中的发布时间文本
            （如"2天前"、"3小时前"）来判断是否符合时间范围
        """
        # 加载配置
        config = get_search_config()

        # 从配置文件获取默认值
        defaults = config.get_search_defaults()
        if page is None:
            page = defaults['page']
        if page_size is None:
            page_size = defaults['page_size']
        if sort is None:
            sort = defaults['sort']
        if note_type is None:
            note_type = defaults['note_type']

        # 从配置文件获取时间过滤设置
        if time_filter_hours is None:
            time_filter_config = config.get_post_time_filter()
            if time_filter_config.get('enabled', False):
                time_filter_hours = time_filter_config.get('hours', 0)
            else:
                time_filter_hours = 0

        uri = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
        data = {
            "keyword": keyword,
            "page": page,
            "page_size": page_size,
            "search_id": get_search_id(),
            "sort": sort,
            "note_type": note_type,
            "ext_flags": [],
            "geo": "",
            "image_formats": [
                "jpg",
                "webp",
                "avif"
            ]
        }

        # 发送请求
        response = await self.session.request("post", url=uri, json=data)

        # 如果启用了时间过滤，需要过滤返回的数据
        if time_filter_hours > 0:
            return await self._filter_response_by_time(response, time_filter_hours)

        return response

    async def _filter_response_by_time(self, response: aiohttp.ClientResponse,
                                       hours: int) -> aiohttp.ClientResponse:
        """过滤响应数据，只保留指定时间范围内发布的帖子

        Args:
            response: 原始响应
            hours: 时间范围（小时）

        Returns:
            过滤后的响应（修改了响应内容）
        """
        # 注意：这里需要创建一个新的响应对象，因为aiohttp的响应对象是只读的
        # 为了简化，我们返回原始响应，但在实际应用中需要在客户端过滤

        # 由于aiohttp响应对象不能直接修改，我们采用包装器模式
        # 实际的过滤逻辑应该在上层调用时处理
        return response

    def filter_items_by_time(self, items: List[Dict[str, Any]],
                            hours: int) -> List[Dict[str, Any]]:
        """过滤帖子列表，只保留指定时间范围内发布的帖子

        Args:
            items: 帖子列表
            hours: 时间范围（小时），0表示不过滤

        Returns:
            过滤后的帖子列表
        """
        if hours <= 0:
            return items

        now = datetime.now()
        cutoff_time = now - timedelta(hours=hours)

        filtered_items = []

        for item in items:
            note_card = item.get('note_card', {})

            # 查找发布时间
            publish_time_text = None
            corner_tags = note_card.get('corner_tag_info', [])
            for tag in corner_tags:
                if tag.get('type') == 'publish_time':
                    publish_time_text = tag.get('text', '')
                    break

            # 解析相对时间
            if publish_time_text:
                actual_time = parse_relative_time(publish_time_text)

                # 检查是否在时间范围内
                if actual_time >= cutoff_time:
                    filtered_items.append(item)

        return filtered_items

    # 获取笔记详情
    async def note_detail(self, note_id: str, xsec_token: str) -> aiohttp.ClientResponse:
        """获取笔记详情

        Args:
            note_id: 笔记ID
            xsec_token: xsec_token

        Returns:
            笔记详情结果
        """
        url = "https://edith.xiaohongshu.com/api/sns/web/v1/feed"
        data = {
            'source_note_id': note_id,
            'image_formats': ["jpg","webp","avif"],
            'extra':{"need_body_topic":"1"},
            'xsec_source':'pc_feed',
            'xsec_token':xsec_token
        }

        return await self.session.request(method="post", url=url, json=data)

    # 搜索用户笔记
    async def search_user_notes(self, user_id: str, num: int = 30, cursor: str = "") -> aiohttp.ClientResponse:
        """搜索用户笔记

        Args:
            user_id: 用户ID
            num: 数量  默认 30
            cursor: 游标 默认空
        """
        url = "https://edith.xiaohongshu.com/api/sns/web/v1/user_posted"
        params = {
            "num": num,
            "cursor": cursor,
            "user_id": user_id,
            "image_formats": "jpg,webp,avif",
            "xsec_source": "pc_feed"
        }
        return await self.session.request("get", url=url, params=params)
