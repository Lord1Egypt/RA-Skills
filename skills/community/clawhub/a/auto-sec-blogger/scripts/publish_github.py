#!/usr/bin/env python3
"""
GitHub Pages 블로그 발행
Jekyll 기반 정적 블로그에 마크다운 포스트 발행
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess
import re

print("="*70)
print("GITHUB PAGES PUBLISHER")
print("="*70)

class GitHubPagesPublisher:
    def __init__(self):
        self.blog_path = Path(os.getenv('BLOG_LOCAL_PATH', Path.home() / '.openclaw' / 'workspace' / 'blog'))
        self.posts_dir = self.blog_path / 'content' / 'post'
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_repo = os.getenv('GITHUB_BLOG_REPO')

    def sanitize_filename(self, title):
        """파일명으로 사용 가능한 문자열로 변환"""
        # 특수문자 제거
        filename = re.sub(r'[^\w\s-]', '', title)
        # 공백을 하이픈으로 변환
        filename = re.sub(r'[\s]+', '-', filename)
        # 최대 길이 제한
        return filename[:100]

    def create_hugo_post(self, article):
        """Hugo 마크다운 포스트 생성"""
        date_str = article['posting_date'].strftime('%Y-%m-%d')
        time_str = article['posting_date'].strftime('%H:%M:%S')
        filename_slug = self.sanitize_filename(article['title'])
        
        # Hugo content 구조: content/post/category/filename/index.md
        category = article.get('category', 'security')
        post_dir = self.posts_dir / category / filename_slug
        post_dir.mkdir(parents=True, exist_ok=True)
        filepath = post_dir / 'index.md'

        # Hugo Front Matter
        front_matter = f"""---
title: "{article['title']}"
date: {date_str}T{time_str}+09:00
draft: false
categories: ["{category}"]
tags: {self._extract_tags(article)}
author: "Intelligence Agent"
---

"""

        # 본문 (마크다운)
        content = article.get('details', article.get('content', ''))

        # 출처 추가
        source = f"\n\n---\n\n**출처**: [{article['category']}]({article['url']})"

        # 파일 작성
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(front_matter + content + source)

        return f"{category}/{filename_slug}/index.md"

    def _extract_tags(self, article):
        """태그 추출 (간단 버전)"""
        # 카테고리 기반 태그
        tags = [article.get('category', 'security')]

        # 제목에서 키워드 추출 (간단 버전)
        title = article['title'].lower()
        keywords = ['cve', 'rce', 'xss', '취약점', '보안', '해킹', '랜섬웨어']
        for keyword in keywords:
            if keyword in title:
                tags.append(keyword)

        return str(tags[:5])  # 최대 5개

    def git_commit_and_push(self, filenames):
        """Git commit & push"""
        try:
            # Git 상태 확인
            subprocess.run(['git', 'status'], cwd=self.blog_path, check=True)

            # 파일 추가
            for filename in filenames:
                filepath = self.posts_dir / filename
                subprocess.run(['git', 'add', str(filepath)], cwd=self.blog_path, check=True)

            # 커밋
            commit_msg = f"Add {len(filenames)} security posts ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
            subprocess.run(['git', 'commit', '-m', commit_msg], cwd=self.blog_path, check=True)

            # 푸시
            subprocess.run(['git', 'push', 'origin', 'main'], cwd=self.blog_path, check=True)

            print(f"✅ Git push 완료: {len(filenames)}개 포스트")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Git 작업 실패: {e}")
            return False

    def publish_batch(self, articles):
        """여러 기사 일괄 발행"""
        print(f"\n🔄 GitHub Pages 발행 시작... ({len(articles)}개)")

        # _posts 디렉토리 확인
        if not self.posts_dir.exists():
            print(f"❌ _posts 디렉토리 없음: {self.posts_dir}")
            print("   블로그 저장소를 먼저 클론하세요:")
            print(f"   git clone https://github.com/{self.github_repo}.git {self.blog_path}")
            return False

        filenames = []
        for i, article in enumerate(articles, 1):
            print(f"  [{i}/{len(articles)}] {article['title'][:40]}...")

            try:
                filename = self.create_jekyll_post(article)
                filenames.append(filename)
                print(f"    ✅ 생성: {filename}")
            except Exception as e:
                print(f"    ❌ 실패: {str(e)[:50]}")

        if filenames:
            return self.git_commit_and_push(filenames)

        return False

def main():
    # 테스트용 샘플 데이터
    sample_article = {
        'title': 'Cisco 제품 보안 업데이트 권고',
        'posting_date': datetime.now(),
        'category': 'KRCERT',
        'url': 'https://knvd.krcert.or.kr/info/vuln/notice/detail?id=xxx',
        'content': 'Cisco 제품의 보안 업데이트 권고...',
        'details': '## 🔍 핵심 요약\n\nCisco 제품의 취약점...\n\n## 📋 상세 분석\n\n...'
    }

    publisher = GitHubPagesPublisher()

    print("\n📝 샘플 포스트 생성 테스트...")
    filename = publisher.create_hugo_post(sample_article)
    print(f"✅ 생성됨: {filename}")

    print("\n📂 블로그 경로:", publisher.blog_path)
    print("📂 Posts 경로:", publisher.posts_dir)

    print("\n" + "="*70)
    print("GitHub Pages Publisher 준비 완료 (Hugo)")
    print("="*70)

if __name__ == '__main__':
    main()
