#!/usr/bin/env python3
"""
Intelligence Agent - 전체 파이프라인 실행
Security News Module + GLM-5 + Notion + Tistory + Notifications
"""

import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
import argparse
from datetime import datetime, timedelta

# 환경 변수 로드
from dotenv import load_dotenv
env_file = Path.home() / '.openclaw' / 'workspace' / '.env'
load_dotenv(env_file)

# Security News Module 경로 추가 (security-news-feed 사용)
skill_path = Path(__file__).parent.parent.parent / 'security-news-feed'
sys.path.insert(0, str(skill_path))

import os
os.chdir(str(skill_path))  # working directory 변경

print("="*70)
print("INTELLIGENCE AGENT - FULL PIPELINE")
print("="*70)

def collect_and_publish():
    """Security News Module로 수집 및 발행"""
    from modules.crawlers.krcert import KRCERTCrawler
    from modules.crawlers.dailysecu import DailySecuCrawler
    from modules.crawlers.boannews import BoanNewsCrawler
    from modules.crawlers.ahnlab import AhnLabCrawler
    from modules.crawlers.boho import BohoCrawler
    from modules.crawlers.igloo import IglooCrawler
    from modules.crawlers.kisa import KISACrawler
    from modules.crawlers.ncsc import NCSCCrawler
    from modules.crawlers.skshieldus import SKShieldusCrawler
    from modules.publisher_service import PublisherService
    from modules.llm_handler import summarize_text, details_text
    from config import BOANISSUE_DATABASE_ID
    import time

    print("\n🔄 Step 1: 기사 수집 (9개 크롤러)")

    crawlers = [
        ("KRCERT", KRCERTCrawler),
        ("데일리시큐", DailySecuCrawler),
        ("보안뉴스", BoanNewsCrawler),
        ("AhnLab", AhnLabCrawler),
        ("Boho", BohoCrawler),
        ("Igloo", IglooCrawler),
        ("KISA", KISACrawler),
        ("NCSC", NCSCCrawler),
        ("SKShieldus", SKShieldusCrawler),
    ]

    publisher = PublisherService(
        enable_notion=True,
        enable_tistory=False,
        notion_database_id=BOANISSUE_DATABASE_ID
    )

    total_collected = 0
    total_published = 0

    for name, crawler_class in crawlers:
        print(f"\n{name}...")

        try:
            crawler = crawler_class()
            result = crawler.run(publisher_service=None)

            collected = len(result.get('queue', []))
            print(f"  ✅ 수집: {collected}개")

            if collected > 0:
                total_collected += collected

                # 발행
                for i, article in enumerate(result['queue'], 1):
                    print(f"  [{i}/{collected}] {article['title'][:40]}...")

                    try:
                        # GLM-5 요약
                        summary = summarize_text(article['content'], article['title'])
                        time.sleep(1)  # Rate limit 방지

                        # GLM-5 상세 분석
                        details = details_text(article['content'], article['title'])
                        time.sleep(1)

                        # Notion 발행
                        pub_result = publisher.publish_article(
                            title=article['title'],
                            content=summary,
                            url=article['url'],
                            date=article['posting_date'].strftime('%Y-%m-%d'),
                            category=article['category'],
                            details=details,
                            database_id=BOANISSUE_DATABASE_ID
                        )

                        if pub_result.get('notion'):
                            total_published += 1
                            print("    ✅ 발행 성공")
                        else:
                            print("    ❌ 발행 실패")

                        time.sleep(2)  # Rate limit 방지

                    except Exception as e:
                        print(f"    ❌ Error: {str(e)[:50]}")
                        continue

        except Exception as e:
            print(f"  ❌ Error: {str(e)[:50]}")

    print("\n" + "="*70)
    print("수집 및 발행 완료")
    print("="*70)
    print(f"📰 수집: {total_collected}개")
    print(f"✅ 발행: {total_published}개")
    print(f"📊 성공률: {total_published/total_collected*100:.1f}%" if total_collected > 0 else "N/A")

    return total_collected, total_published

def send_notifications(collected, published):
    """알림 발송"""
    print("\n🔄 Step 2: 알림 발송")

    # Slack 알림 (구현 필요)
    print("  ⏳ Slack 알림 - 구현 예정")

    # Email 알림 (구현 필요)
    print("  ⏳ Email 알림 - 구현 예정")

    print("  ✅ 알림 발송 완료 (준비 중)")

def generate_weekly_report():
    """주간 리포트 생성"""
    print("\n🔄 Step 3: 주간 리포트 생성")

    # Notion에서 지난 주 데이터 가져오기 (구현 필요)
    print("  ⏳ 데이터 분석 - 구현 예정")

    # 리포트 생성 (구현 필요)
    print("  ⏳ 리포트 작성 - 구현 예정")

    # 발송 (구현 필요)
    print("  ⏳ 발송 - 구현 예정")

    print("  ✅ 주간 리포트 완료 (준비 중)")

def publish_to_github_pages(articles):
    """GitHub Pages 발행"""
    print("\n🔄 Step 4: GitHub Pages 발행")

    if not articles:
        print("  ❌ 발행할 기사가 없습니다.")
        return False

    try:
        # GitHub Pages Publisher 임포트
        sys.path.insert(0, str(Path(__file__).parent))
        from publish_github import GitHubPagesPublisher

        publisher = GitHubPagesPublisher()
        result = publisher.publish_batch(articles)

        if result:
            print(f"  ✅ GitHub Pages 발행 완료: {len(articles)}개")
        else:
            print("  ❌ GitHub Pages 발행 실패")

        return result

    except Exception as e:
        print(f"  ❌ Error: {str(e)[:50]}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(description='Intelligence Agent Pipeline')
    parser.add_argument('--full', action='store_true', help='전체 파이프라인 (수집 + 발행 + 알림)')
    parser.add_argument('--publish', action='store_true', help='발행만')
    parser.add_argument('--notify', action='store_true', help='알림만')
    parser.add_argument('--weekly', action='store_true', help='주간 리포트만')
    parser.add_argument('--tistory', action='store_true', help='Tistory 발행만')

    args = parser.parse_args()

    if not any([args.full, args.publish, args.notify, args.weekly, args.tistory]):
        parser.print_help()
        return

    start_time = datetime.now()
    print(f"\n시작: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    collected, published = 0, 0

    if args.full or args.publish:
        collected, published = collect_and_publish()

    if args.full or args.notify:
        send_notifications(collected, published)

    if args.weekly:
        generate_weekly_report()

    if args.tistory:
        publish_to_tistory()

    end_time = datetime.now()
    duration = end_time - start_time

    print("\n" + "="*70)
    print("파이프라인 완료")
    print("="*70)
    print(f"시작: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"종료: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"소요 시간: {duration}")

if __name__ == '__main__':
    main()
