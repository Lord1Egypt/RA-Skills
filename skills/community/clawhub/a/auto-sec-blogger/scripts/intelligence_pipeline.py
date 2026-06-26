#!/usr/bin/env python3
"""
Intelligence Agent - 전체 파이프라인 스크립트 (Async)
"""

import sys
import argparse
import asyncio
from collections import defaultdict
from modules.intelligence.utils import setup_logger
from modules.intelligence.collector import NewsCollector
from modules.intelligence.writer import BlogWriter
from modules.intelligence.notion_publisher import NotionPublisher
from modules.intelligence.selector import ArticleSelector

logger = setup_logger(__name__, "pipeline.log")

async def run_pipeline_async(max_articles: int = 5):
    logger.info("=== Intelligence Pipeline (Async) Started ===")

    try:
        # 1. 뉴스 수집 (Collector)
        # Collector는 동기식이므로 그대로 실행 (추후 비동기화 가능)
        logger.info("[1/4] Collecting news from various sources...")
        collector = NewsCollector()
        raw_articles = collector.fetch_all(max_results_per_source=15)
        
        if not raw_articles:
            logger.info("No new articles found. Terminating pipeline.")
            return
        
        logger.info(f"Total candidates collected: {len(raw_articles)}")

        # 2. AI 기반 기사 선별 (Async Selector)
        logger.info(f"[2/4] AI evaluating and selecting best {max_articles} articles (Async)...")
        selector = ArticleSelector()
        selected_articles = await selector.evaluate_and_select(
            raw_articles, 
            max_articles=max_articles,
            min_score=6  # 품질 관리 (6점 미만 탈락)
        )

        if not selected_articles:
            logger.warning("No articles passed the selection criteria (Score >= 6).")
            return

        # 3. 블로그 글 작성 (Async Writer)
        logger.info(f"[3/4] Writing blog posts for {len(selected_articles)} articles (Parallel)...")
        writer = BlogWriter()
        
        # 병렬 실행
        blog_posts_results = await writer.generate_article_batch(selected_articles)
        
        valid_posts = []
        for res in blog_posts_results:
            if isinstance(res, dict) and 'title' in res:
                valid_posts.append(res)
                logger.info(f"   ✅ Done: {res['title'][:40]}")
            elif isinstance(res, Exception):
                logger.error(f"   ❌ Writing failed: {res}")

        # 4. Notion 저장 (Publisher)
        # Notion API는 순차적으로 호출 (Rate Limit 고려)
        logger.info(f"[4/4] Publishing {len(valid_posts)} posts to Notion...")
        notion_pub = NotionPublisher()
        
        success_count = 0
        for i, post in enumerate(valid_posts, 1):
            try:
                logger.info(f"   ({i}/{len(valid_posts)}) Sending to Notion: {post['title'][:40]}...")
                result = notion_pub.create_article(post)
                if result.get('id'):
                    success_count += 1
                    logger.info(f"   ✅ Success: {result.get('url')}")
            except Exception as e:
                logger.error(f"   ❌ Failed to publish to Notion: {e}")
        
        logger.info(f"=== Pipeline Completed: {success_count}/{len(valid_posts)} articles published successfully ===")

    except Exception as e:
        logger.error(f"Critical Pipeline Error: {e}", exc_info=True)
        raise

def main():
    parser = argparse.ArgumentParser(description='Intelligence Agent Pipeline (Async)')
    parser.add_argument('--max-articles', type=int, default=5, help='최종 생성할 블로그 글 수')
    args = parser.parse_args()

    asyncio.run(run_pipeline_async(max_articles=args.max_articles))

if __name__ == "__main__":
    main()