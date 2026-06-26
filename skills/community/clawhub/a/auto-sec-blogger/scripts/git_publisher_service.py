#!/usr/bin/env python3
"""
Git Publisher Service - launchd용 백그라운드 서비스

Notion에서 '검토 완료' 상태의 글을 자동으로 감지하고 배포합니다.
launchd를 통해 시스템 부팅 시 자동 시작되고, 프로세스가 종료되면 재시작됩니다.
"""

import sys
import os
import time
import logging
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "submodules" / "intelligence-agent" / "src"))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/nabang/Documents/OpenClaw/logs/git-publisher-service.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    from notion_publisher import NotionPublisher
    from publisher_git import GitPublisher
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(f"PYTHONPATH: {sys.path}")
    sys.exit(1)


def main():
    """메인 서비스 루프"""

    logger.info("=" * 70)
    logger.info("Git Publisher Service 시작")
    logger.info("=" * 70)

    try:
        # 초기화
        notion_pub = NotionPublisher()
        git_pub = GitPublisher(notion_publisher=notion_pub)

        logger.info(f"설정된 확인 간격: 300초 (5분)")
        logger.info(f"블로그 저장소: {git_pub.blog_repo_path}")
        logger.info(f"블로그 URL: {git_pub.blog_url}")

        # 모니터링 시작
        git_pub.monitor_and_publish(interval_seconds=300)

    except KeyboardInterrupt:
        logger.info("\n⏸️ 서비스 중지 (KeyboardInterrupt)")
    except Exception as e:
        logger.error(f"❌ 서비스 에러: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
