"""
Article Fetcher — 主程序入口
抓取文章并存档到 Notion
"""
from detector.platform_detector import detect_platform
from fetchers.wechat_fetcher import WechatFetcher
from fetchers.xhs_fetcher import XHSFetcher
from fetchers.douban_fetcher import DoubanFetcher
from fetchers.zhihu_fetcher import ZhihuFetcher
from processors.image_processor import ImageProcessor
from archiver.notion_archiver import NotionArchiver
from utils.word_counter import count_words
from utils.tag_extractor import extract_tags
from utils.logger import logger
from config import config
import uuid
import sys


# === 平台抓取器注册表 ===
# 新增平台只需在此注册，并实现对应的 Fetcher 类
FETCHER_REGISTRY = {
    'wechat': WechatFetcher,
    'xhs':    XHSFetcher,
    'douban': DoubanFetcher,
    'zhihu':  ZhihuFetcher,
    # 扩展示例: 'juejin': JuejinFetcher, 'csdn': CSDNFetcher,
}


def fetch_and_archive_article(url: str, tags: list = None) -> dict:
    """抓取文章并存档到 Notion"""
    logger.info(f"开始处理文章：{url}")

    try:
        # 1. 平台识别
        platform = detect_platform(url)
        if not platform:
            return _error('不支持的平台或无法识别平台', 'UNSUPPORTED_PLATFORM')

        logger.info(f"识别平台：{platform}")

        # 2. 实例化对应抓取器
        fetcher_cls = FETCHER_REGISTRY.get(platform)
        if not fetcher_cls:
            return _error(f'未注册平台 {platform} 的抓取器', 'FETCHER_NOT_FOUND')

        # 自动传入 cookies_file（如果配置存在）
        cookies_key = f'{platform}_cookies'
        cookies_file = getattr(config, cookies_key, None)
        fetcher = fetcher_cls(cookies_file=cookies_file) if cookies_file else fetcher_cls()

        # 3. 抓取文章
        logger.info(f"正在抓取 {platform} 平台的文章...")
        article_data = fetcher.fetch_article(url)
        if not article_data or not article_data.get('title'):
            return _error('未能成功抓取文章内容', 'FETCH_FAILED')

        article_id = str(uuid.uuid4())

        # 4. 图片上传 OSS + 替换 HTML 中的链接
        image_processor = ImageProcessor()
        image_urls = article_data.get('images', [])
        if image_urls:
            logger.info(f"发现 {len(image_urls)} 张图片，开始上传...")
            url_mapping = image_processor.upload_images(image_urls, platform, article_id)
            logger.info(f"图片上传完成：{len(url_mapping)}/{len(image_urls)} 张成功")

            content = article_data.get('content', '')
            for orig, oss in url_mapping.items():
                content = content.replace(orig, oss)
            article_data['content'] = content

        # 5. 提取关键词（LLM 优先，本地词频降级）
        content = article_data.get('content', '')
        article_title = article_data.get('title', '')
        logger.info("正在提取关键词...")
        auto_tags = extract_tags(content, title=article_title)
        all_tags = list(dict.fromkeys((tags or []) + auto_tags))
        logger.info(f"关键词：{all_tags}")

        # 6. 字数统计（剔除 HTML 标签后）
        word_count = count_words(content)
        logger.info(f"字数统计：{word_count} 字")

        # 7. 存档到 Notion
        logger.info("正在存档到 Notion...")
        archiver = NotionArchiver()
        success = archiver.archive_article({
            'title': article_data.get('title', ''),
            'source': platform,
            'author': article_data.get('author', ''),
            'link': url,
            'tags': all_tags,
            'pub_date': article_data.get('pub_date', ''),
            'content': content,
            'words': word_count,
        })

        if success:
            logger.info("文章存档成功")
            return {
                'success': True,
                'message': '文章已成功抓取并存档到 Notion',
                'article_id': article_id,
                'platform': platform,
                'title': article_data.get('title', ''),
                'tags': all_tags,
                'word_count': word_count,
            }
        return _error('文章抓取成功但存档到 Notion 失败', 'ARCHIVE_FAILED', article_data)

    except Exception as e:
        logger.exception(f"处理过程中发生异常：{e}")
        return _error(f'处理过程中发生错误：{e}', 'PROCESS_ERROR')


def _error(message: str, code: str, extra: dict = None) -> dict:
    """统一错误返回格式"""
    result = {
        'success': False,
        'message': message,
        'error_code': code,
    }
    if extra:
        result['article_data'] = extra
    logger.error(f"任务失败：{code}")
    return result


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法：python main.py <文章链接> [标签 1] [标签 2] ...")
        print("\n示例:")
        print("  python main.py https://mp.weixin.qq.com/s/xxx 技术 AI")
        print("  python main.py https://www.xiaohongshu.com/explore/xxx 教程 笔记")
        return

    url = sys.argv[1]
    tags = sys.argv[2:] if len(sys.argv) > 2 else []
    logger.info(f"命令行启动 | URL: {url} | 标签：{tags}")

    result = fetch_and_archive_article(url, tags)

    if result['success']:
        print(f"\n✅ {result['message']}")
        print(f"📰 标题：{result['title']}")
        print(f"🏷️ 平台：{result['platform']}")
        print(f"🏷️ 关键词：{', '.join(result.get('tags', []))}")
        print(f"🔢 字数：{result['word_count']}")
        logger.info("任务完成")
    else:
        print(f"\n❌ {result['message']}")
        print(f"🔧 错误代码：{result.get('error_code', 'UNKNOWN')}")


if __name__ == "__main__":
    main()
