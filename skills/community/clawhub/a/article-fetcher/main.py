"""
Article Fetcher — 主程序入口
抓取文章并存档到 Obsidian / Notion
"""
from detector.platform_detector import detect_platform
from fetchers.wechat_fetcher import WechatFetcher
from fetchers.xhs_fetcher import XHSFetcher
from fetchers.douban_fetcher import DoubanFetcher
from fetchers.zhihu_fetcher import ZhihuFetcher
from fetchers.offline_parser import parse_html_to_article, parse_mhtml_to_article
from processors.image_processor import ImageProcessor
from archiver.notion_archiver import NotionArchiver
from archiver.obsidian_archiver import ObsidianArchiver
from utils.word_counter import count_words
from utils.tag_extractor import extract_tags
from utils.logger import logger
from config import config
from bs4 import BeautifulSoup
import uuid
import sys
import os


# === 平台抓取器注册表 ===
# 新增平台只需在此注册，并实现对应的 Fetcher 类
FETCHER_REGISTRY = {
    'wechat': WechatFetcher,
    'xhs':    XHSFetcher,
    'douban': DoubanFetcher,
    'zhihu':  ZhihuFetcher,
    # 扩展示例: 'juejin': JuejinFetcher, 'csdn': CSDNFetcher,
}


def process_and_archive(article_data: dict, platform: str, url: str, tags: list = None) -> dict:
    """后半段管线（与输入来源解耦）：图片上传 OSS → 替换 URL → 关键词 → 字数 → 归档（4 场景动态调度）"""
    article_id = str(uuid.uuid4())

    # 1. 图片上传 OSS + 替换 HTML 中的链接
    image_processor = ImageProcessor()
    image_urls = article_data.get('images', [])
    if image_urls:
        logger.info(f"发现 {len(image_urls)} 张图片，开始上传...")
        url_mapping = image_processor.upload_images(image_urls, platform, article_id, article_url=url)
        logger.info(f"图片上传完成：{len(url_mapping)}/{len(image_urls)} 张成功")

        content = article_data.get('content', '')
        for orig, oss in url_mapping.items():
            content = content.replace(orig, oss)
        article_data['content'] = content

        # 兜底：修复个别 data-src 懒加载残留（离线解析已处理，此处兼容 URL 抓取路径）
        _content_soup = BeautifulSoup(content, 'html.parser')
        _fixed = False
        for img in _content_soup.find_all('img'):
            if not img.get('src') and img.get('data-src'):
                img['src'] = img['data-src']
                _fixed = True
        if _fixed:
            article_data['content'] = str(_content_soup)
            logger.debug(f"修复 {_fixed} 处 data-src → src")

    # 2. 提取关键词（LLM 优先，本地词频降级）
    content = article_data.get('content', '')
    article_title = article_data.get('title', '')
    logger.info("正在提取关键词...")
    auto_tags = extract_tags(content, title=article_title)
    # 手动标签也清洗为 Obsidian 兼容格式（空格→`-`）
    manual_tags = [t.strip().replace(' ', '-').lstrip('#') for t in (tags or []) if t.strip()]
    all_tags = list(dict.fromkeys(manual_tags + auto_tags))
    logger.info(f"关键词：{all_tags}")

    # 3. 字数统计（剔除 HTML 标签后）
    word_count = count_words(content)
    logger.info(f"字数统计：{word_count} 字")

    # 4. 存档（4 场景动态调度：Obsidian / Notion / 双写 / 仅预览）
    archive_payload = {
        'title': article_data.get('title', ''),
        'source': platform,
        'author': article_data.get('author', ''),
        'link': url,
        'tags': all_tags,
        'pub_date': article_data.get('pub_date', ''),
        'content': content,
        'words': word_count,
    }

    archived_to = []

    # Obsidian 存档（推荐默认）
    if config.obsidian_available:
        logger.info("正在存档到 Obsidian...")
        obsidian = ObsidianArchiver()
        if obsidian.archive_article(archive_payload):
            archived_to.append('Obsidian')

    # Notion 存档（可选）
    if config.notion_available:
        logger.info("正在存档到 Notion...")
        notion = NotionArchiver()
        if notion.archive_article(archive_payload):
            archived_to.append('Notion')

    # 5. 返回结果
    if archived_to:
        logger.info(f"文章存档成功 → {', '.join(archived_to)}")
        return {
            'success': True,
            'message': f"文章已成功抓取并存档到 {', '.join(archived_to)}",
            'article_id': article_id,
            'platform': platform,
            'title': article_data.get('title', ''),
            'tags': all_tags,
            'word_count': word_count,
            'archived_to': archived_to,
        }

    if config.archive_available:
        # 配置了存档但均失败
        return _error('文章抓取成功但所有存档目标均失败', 'ARCHIVE_FAILED', article_data)

    # 无存档配置 → 预览模式
    logger.info("未配置存档目标，仅终端输出")
    return {
        'success': True,
        'message': '文章已成功抓取（预览模式，未配置存档目标）',
        'article_id': article_id,
        'platform': platform,
        'title': article_data.get('title', ''),
        'tags': all_tags,
        'word_count': word_count,
        'archived_to': [],
    }


def fetch_and_archive_article(url: str, tags: list = None) -> dict:
    """抓取文章（URL 模式）并存档到 Obsidian / Notion（4 场景动态调度）"""
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

        # 4. 后半段管线（复用 process_and_archive）
        return process_and_archive(article_data, platform, url, tags)

    except Exception as e:
        logger.exception(f"处理过程中发生异常：{e}")
        return _error(f'处理过程中发生错误：{e}', 'PROCESS_ERROR')


def archive_from_html(html_text: str, tags: list = None, platform: str = 'wechat', url: str = '') -> dict:
    """离线模式：直接解析 HTML 文本 → 后半段管线（图片上传 OSS + 归档）"""
    logger.info("离线模式：直接解析 HTML 文本")
    article_data = parse_html_to_article(html_text, platform, url)
    if not article_data or not article_data.get('title'):
        return _error('HTML 解析未能提取到有效文章', 'PARSE_FAILED')
    return process_and_archive(article_data, platform, url, tags)


def archive_from_mhtml(path: str, tags: list = None, platform: str = 'wechat', url: str = '') -> dict:
    """离线模式：解析 .mhtml 文件 → 后半段管线"""
    logger.info(f"离线模式：解析 MHTML 文件 {path}")
    if not os.path.isfile(path):
        return _error(f'MHTML 文件不存在：{path}', 'FILE_NOT_FOUND')
    article_data = parse_mhtml_to_article(path, platform, url)
    if not article_data or not article_data.get('title'):
        return _error('MHTML 解析未能提取到有效文章', 'PARSE_FAILED')
    return process_and_archive(article_data, platform, url, tags)


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
    """命令行入口（sys.argv 手动解析，保持安全合规约定，不使用 argparse）"""
    argv = sys.argv[1:]
    if not argv:
        print("用法：python main.py <文章链接|选项> [标签...]")
        print("\n选项：")
        print("  --html <html文本|-|>   直接传入 HTML（'-' 表示读取 stdin）")
        print("  --mhtml <文件路径>      直接传入 .mhtml 文件")
        print("  --platform <平台>       指定平台（默认 wechat）")
        print("  --url <原文链接>        原文链接，用于图片 Referer 与归档（可选）")
        print("\n示例:")
        print("  python main.py https://mp.weixin.qq.com/s/xxx 技术 AI")
        print("  cat page.html | python main.py --html - --url https://mp.weixin.qq.com/s/xxx")
        print("  python main.py --mhtml page.mhtml --url https://mp.weixin.qq.com/s/xxx 教程")
        return

    html_text = None
    mhtml_path = None
    platform = 'wechat'
    article_url = ''
    positional = []

    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--html':
            v = argv[i + 1] if i + 1 < len(argv) else ''
            html_text = sys.stdin.read() if v == '-' else v
            i += 2
        elif a == '--mhtml':
            mhtml_path = argv[i + 1] if i + 1 < len(argv) else ''
            i += 2
        elif a == '--platform':
            platform = argv[i + 1] if i + 1 < len(argv) else platform
            i += 2
        elif a == '--url':
            article_url = argv[i + 1] if i + 1 < len(argv) else ''
            i += 2
        else:
            positional.append(a)
            i += 1

    # 路由：MHTML > HTML > URL
    if mhtml_path:
        logger.info(f"命令行启动 | MHTML: {mhtml_path} | 平台：{platform} | 标签：{positional}")
        result = archive_from_mhtml(mhtml_path, positional, platform, article_url)
    elif html_text is not None:
        logger.info(f"命令行启动 | HTML 文本 | 平台：{platform} | 标签：{positional}")
        result = archive_from_html(html_text, positional, platform, article_url)
    else:
        url = positional[0] if positional else ''
        tags = positional[1:]
        logger.info(f"命令行启动 | URL: {url} | 标签：{tags}")
        result = fetch_and_archive_article(url, tags)

    if result['success']:
        print(f"\n✅ {result['message']}")
        print(f"📰 标题：{result['title']}")
        print(f"🏷️ 平台：{result['platform']}")
        print(f"🏷️ 关键词：{', '.join(result.get('tags', []))}")
        print(f"🔢 字数：{result['word_count']}")
        archived = result.get('archived_to', [])
        if archived:
            print(f"📁 存档目标：{', '.join(archived)}")
        elif not config.archive_available:
            print("💡 提示：配置 OBSIDIAN_VAULT_PATH 或 NOTION_API_KEY 启用存档")
        logger.info("任务完成")
    else:
        print(f"\n❌ {result['message']}")
        print(f"🔧 错误代码：{result.get('error_code', 'UNKNOWN')}")


if __name__ == "__main__":
    main()
