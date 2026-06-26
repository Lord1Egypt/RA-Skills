#!/usr/bin/env python3
"""
Build from Notion Queue
Notion의 "개발 시작" 상태 프로젝트를 자동으로 빌드
"""

import sys
import logging
from pathlib import Path

# Add builder-agent to path
sys.path.insert(0, str(Path(__file__).parent))

from config import load_config, setup_logging
from builder.pipeline import BuilderPipeline
from builder.integration.notion_sync import NotionSync

logger = logging.getLogger('builder-agent.build-from-notion')


def main():
    """Notion 큐에서 프로젝트 빌드"""

    # 설정 로드
    config = load_config()
    setup_logging(config)

    logger.info("="*70)
    logger.info("BUILD FROM NOTION QUEUE")
    logger.info("="*70)

    # Notion DB ID 확인
    notion_db_id = config.notion.database_id
    if not notion_db_id or notion_db_id.startswith('${'):
        logger.error("Notion DB ID not configured")
        return 1

    # NotionSync 초기화
    notion = NotionSync(notion_db_id)

    # "개발중" 상태 프로젝트 조회
    logger.info("Fetching projects with status '개발중'...")
    projects = notion.get_ready_projects()

    if not projects:
        logger.info("No projects ready for development")
        return 0

    logger.info(f"Found {len(projects)} project(s) to build")

    # Build Pipeline 초기화 (새로운 기능들 활성화)
    use_adaptive = config.features.get('adaptive_scoring', True) if hasattr(config, 'features') else True
    use_checkpoints = config.features.get('checkpoint_resume', True) if hasattr(config, 'features') else True
    pipeline = BuilderPipeline(config, use_adaptive_scoring=use_adaptive)

    # 각 프로젝트 빌드
    for i, project in enumerate(projects, 1):
        logger.info(f"\n[{i}/{len(projects)}] Building: {project['title'][:50]}")

        try:
            # 상태를 "테스트중"으로 변경
            notion.update_status(project['notion_page_id'], "테스트중")
            logger.info("  Status → 테스트중")

            # 프로젝트 경로 생성
            project_slug = project['title'].lower().replace(' ', '-').replace('/', '-')[:50]
            project_path = Path(f"/tmp/builder-projects/{project_slug}")
            project_path.mkdir(parents=True, exist_ok=True)

            # Build 실행 (체크포인트 및 재개 지원)
            logger.info(f"  Starting build pipeline...")
            result = pipeline.run_build_pipeline(project, project_path, resume=use_checkpoints)

            if result.get('success'):
                # 성공
                logger.info(f"  ✅ Build succeeded!")
                notion.update_status(project['notion_page_id'], "배포 완료")
                logger.info("  Status → 배포 완료")

                # TODO: GitHub 배포
                # github_url = publish_to_github(project_path, project['title'])
                # notion.update_url(project['notion_page_id'], github_url)

            else:
                # 실패 처리
                error_msg = result.get('error', 'Unknown error')
                can_resume = result.get('can_resume', False)
                retry_count = result.get('retry_count', 0)

                if can_resume and retry_count < 3:
                    logger.warning(f"  ⚠️ Build failed (retry {retry_count}/3): {error_msg}")
                    logger.info(f"  Can resume from last checkpoint")
                    notion.update_status(project['notion_page_id'], "재시도 대기")
                else:
                    logger.error(f"  ❌ Build failed: {error_msg}")
                    notion.update_status(project['notion_page_id'], "개발 실패")
                    logger.info("  Status → 개발 실패")

        except Exception as e:
            logger.error(f"  ❌ Build error: {e}")
            notion.update_status(project['notion_page_id'], "개발 실패")

    logger.info("\n" + "="*70)
    logger.info("BUILD QUEUE COMPLETED")
    logger.info("="*70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
