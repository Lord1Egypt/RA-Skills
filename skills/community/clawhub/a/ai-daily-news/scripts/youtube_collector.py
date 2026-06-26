#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube AI博主视频收集模块
收集指定AI博主最近一周的视频信息并总结描述内容

使用 yt-dlp 或 YouTube RSS Feed 获取数据
"""

import json
import logging
import re
import subprocess
from datetime import datetime, timedelta

import requests

logger = logging.getLogger(__name__)

# YouTube博主配置 - 使用channel handle或自定义URL
YOUTUBE_CREATORS = {
    "andrew_ng": {
        "name": "吴恩达 (Andrew Ng)",
        "handle": "@Deeplearningai",
        "url": "https://www.youtube.com/@Deeplearningai",
        "description": "DeepLearning.AI创始人，AI教育领域权威"
    },
    "matt_wolfe": {
        "name": "Matt Wolfe", 
        "handle": "@mreflow",
        "url": "https://www.youtube.com/@mreflow",
        "description": "AI工具和生产力内容创作者"
    },
    "ai_explained": {
        "name": "AI Explained",
        "handle": "@ai-explained",
        "url": "https://www.youtube.com/@ai-explained",
        "description": "AI新闻和技术解读"
    },
    "ai_with_oliver": {
        "name": "AI with Oliver",
        "handle": "@aiwitholiver",
        "url": "https://www.youtube.com/@aiwitholiver",
        "description": "AI工具和实用教程"
    },
    "greg_isenberg": {
        "name": "Greg Isenberg",
        "handle": "@gregisenberg", 
        "url": "https://www.youtube.com/@gregisenberg",
        "description": "产品策略和AI创业"
    }
}


def get_channel_videos_with_ytdlp(creator_config, max_results=3):
    """
    使用 yt-dlp 获取频道最近视频
    这是目前最可靠的方法
    """
    videos = []
    handle = creator_config.get('handle', '').lstrip('@')
    
    try:
        # 尝试导入 yt_dlp
        try:
            import yt_dlp
        except ImportError:
            logger.warning("yt-dlp 未安装，尝试使用pip安装...")
            subprocess.check_call(['pip', 'install', '-q', 'yt-dlp'])
            import yt_dlp
        
        channel_url = f"https://www.youtube.com/{creator_config.get('handle', '')}/videos"
        
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'playlistend': max_results * 2,  # 多获取一些以便筛选时间
            'skip_download': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"正在获取 {creator_config['name']} 的视频列表...")
            result = ydl.extract_info(channel_url, download=False)
            
            if not result or 'entries' not in result:
                logger.warning(f"未获取到 {creator_config['name']} 的视频")
                return videos
            
            entries = result['entries']
            cutoff_date = datetime.now() - timedelta(days=7)
            
            for entry in entries[:max_results * 2]:
                if not entry:
                    continue
                
                try:
                    # 获取详细视频信息
                    video_url = f"https://www.youtube.com/watch?v={entry.get('id')}"
                    
                    video_ydl_opts = {
                        'quiet': True,
                        'skip_download': True,
                    }
                    
                    with yt_dlp.YoutubeDL(video_ydl_opts) as video_ydl:
                        video_info = video_ydl.extract_info(video_url, download=False)
                        
                        # 检查发布时间
                        upload_date_str = video_info.get('upload_date', '')  # format: YYYYMMDD
                        if upload_date_str:
                            upload_date = datetime.strptime(upload_date_str, '%Y%m%d')
                            if upload_date < cutoff_date:
                                continue
                        
                        video = {
                            "creator": creator_config['name'],
                            "title": video_info.get('title', ''),
                            "description": video_info.get('description', ''),
                            "url": video_url,
                            "video_id": entry.get('id'),
                            "published": upload_date_str[:4] + '-' + upload_date_str[4:6] + '-' + upload_date_str[6:8] if upload_date_str else '',
                            "published_datetime": upload_date.isoformat() if upload_date_str else '',
                            "duration": video_info.get('duration_string', ''),
                            "view_count": video_info.get('view_count', 0)
                        }
                        videos.append(video)
                        
                        if len(videos) >= max_results:
                            break
                            
                except Exception as e:
                    logger.warning(f"获取视频详情失败: {e}")
                    continue
                    
    except Exception as e:
        logger.error(f"获取 {creator_config['name']} 视频失败: {e}")
    
    logger.info(f"获取到 {creator_config['name']} 的 {len(videos)} 个视频")
    return videos[:max_results]


def get_channel_videos_with_rss(creator_config, max_results=3):
    """
    使用RSS Feed获取频道视频（备用方案）
    注意：YouTube的RSS需要正确的channel_id
    """
    videos = []
    
    try:
        import feedparser
        
        # 尝试通过handle获取channel_id（这里使用一个简化的方法）
        # 实际上我们需要先解析频道页面获取channel_id
        handle = creator_config.get('handle', '').lstrip('@')
        
        # 使用第三方RSS服务
        rss_url = f"https://www.youtube.com/feeds/videos.xml?user={handle}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(rss_url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            # 尝试其他格式
            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={creator_config.get('channel_id', '')}"
            if creator_config.get('channel_id'):
                response = requests.get(rss_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            
            cutoff_date = datetime.now() - timedelta(days=7)
            
            for entry in feed.entries[:max_results * 2]:
                try:
                    published_str = entry.get('published', '')
                    if published_str:
                        published = datetime.strptime(published_str[:19], '%Y-%m-%dT%H:%M:%S')
                        if published < cutoff_date:
                            continue
                    
                    video_id = entry.get('yt_videoid', '')
                    link = entry.get('link', '')
                    if not video_id and link:
                        match = re.search(r'v=([^&]+)', link)
                        if match:
                            video_id = match.group(1)
                    
                    from bs4 import BeautifulSoup
                    description = entry.get('summary', '')
                    description = BeautifulSoup(description, 'html.parser').get_text()
                    
                    video = {
                        "creator": creator_config['name'],
                        "title": entry.get('title', ''),
                        "description": description,
                        "url": link or f"https://www.youtube.com/watch?v={video_id}",
                        "video_id": video_id,
                        "published": published.strftime('%Y-%m-%d') if published_str else '',
                    }
                    videos.append(video)
                    
                    if len(videos) >= max_results:
                        break
                        
                except Exception as e:
                    logger.warning(f"解析视频条目失败: {e}")
                    continue
    
    except Exception as e:
        logger.error(f"RSS获取失败: {e}")
    
    return videos[:max_results]


def fetch_youtube_videos(creator_key, days_back=7, max_videos=3):
    """
    获取指定博主的YouTube视频
    优先使用yt-dlp，失败则回退到RSS
    """
    creator = YOUTUBE_CREATORS.get(creator_key)
    if not creator:
        logger.error(f"未知的博主: {creator_key}")
        return []
    
    # 首先尝试yt-dlp方法
    videos = get_channel_videos_with_ytdlp(creator, max_videos)
    
    # 如果yt-dlp失败，尝试RSS
    if not videos:
        logger.info(f"尝试使用RSS获取 {creator['name']} 的视频...")
        videos = get_channel_videos_with_rss(creator, max_videos)
    
    return videos


def summarize_description(description, max_length=150):
    """
    智能总结视频描述
    """
    if not description:
        return "暂无描述"
    
    # 过滤时间戳
    description = re.sub(r'\d{1,2}:\d{2}(?::\d{2})?', '', description)
    description = re.sub(r'\n?\s*\d{1,2}:\d{2}\s+.+?(?=\n|$)', '', description)
    
    # 过滤链接
    description = re.sub(r'http[s]?://\S+', '', description)
    
    # 过滤hashtags
    description = re.sub(r'#\w+', '', description)
    
    # 清理空白
    description = re.sub(r'\n+', ' ', description)
    description = re.sub(r'\s+', ' ', description).strip()
    
    # 提取前几句话
    sentences = re.split(r'[.!?。！？]+', description)
    
    summary = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 10:
            continue
        if len(summary) + len(sentence) > max_length:
            if not summary:
                summary = sentence[:max_length] + "..."
            break
        summary += sentence + "。"
    
    return summary if summary else description[:max_length] + "..."


def fetch_all_youtube_content(creators=None, days_back=7, max_per_creator=2):
    """
    获取所有指定博主的YouTube内容
    """
    if creators is None:
        creators = list(YOUTUBE_CREATORS.keys())
    
    all_videos = []
    
    for creator_key in creators:
        videos = fetch_youtube_videos(creator_key, days_back, max_per_creator)
        all_videos.extend(videos)
    
    # 转换为统一的新闻格式
    news_items = []
    for video in all_videos:
        summary = summarize_description(video.get('description', ''), max_length=200)
        
        news_item = {
            "type": "视频",
            "tag": f"[视频·{video['creator'].split('(')[0].strip()}]",
            "title": video['title'],
            "summary": summary,
            "url": video['url'],
            "published": video['published'],
            "creator": video['creator'],
            "source": "youtube"
        }
        news_items.append(news_item)
    
    logger.info(f"YouTube内容总计: {len(news_items)} 条")
    return news_items


# 兼容旧版配置的映射
def get_creator_by_name(name):
    """根据名称查找博主配置"""
    name_lower = name.lower().replace(' ', '_')
    
    if name_lower in YOUTUBE_CREATORS:
        return name_lower
    
    aliases = {
        '吴恩达': 'andrew_ng',
        'andrew_ng': 'andrew_ng',
        'andrewng': 'andrew_ng',
        'matt_wolfe': 'matt_wolfe',
        'mattwolf': 'matt_wolfe',
        'ai_explained': 'ai_explained',
        'aiexplained': 'ai_explained',
        'angel_kapasi': 'angelina_kapasi',
        'angelkapasi': 'angelina_kapasi',
        'angelina_kapasi': 'angelina_kapasi',
        'greek_asimberg': 'greg_isenberg',
        'greg_isenberg': 'greg_isenberg',
        'gregisenberg': 'greg_isenberg',
    }
    
    return aliases.get(name_lower)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("测试获取YouTube视频...")
    items = fetch_all_youtube_content(days_back=7, max_per_creator=2)
    
    print(f"\n获取到 {len(items)} 条内容:\n")
    for item in items:
        print(f"[{item['tag']}] {item['title']}")
        print(f"发布时间: {item['published']}")
        print(f"摘要: {item['summary'][:100]}...")
        print(f"链接: {item['url']}")
        print("-" * 50)
