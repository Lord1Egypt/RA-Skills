#!/usr/bin/env python3
"""
Auto-Sec-Blogger 자동 발행 스크립트
3시간마다 Notion에서 "검토 완료" 상태인 글을 찾아 블로그에 발행
"""

import os
import sys
import requests
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# .env 로드
load_dotenv('/Users/rebugui/.openclaw/workspace/.env')

notion_token = os.getenv('NOTION_API_KEY')
database_id = os.getenv('BLOG_DATABASE_ID')
blog_path = Path.home() / '.openclaw' / 'workspace' / 'blog'
posts_dir = blog_path / 'content' / 'post'

# 로그 파일
log_file = Path.home() / '.openclaw' / 'logs' / 'auto-publish-approved.log'

def log(message):
    """로그 기록"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    
    # 로그 파일에도 기록
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

def get_approved_articles():
    """Notion에서 "검토 완료" 상태인 글 조회"""
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # "검토 완료" 상태인 글 조회
    query_url = f"https://api.notion.com/v1/databases/{database_id}/query"
    payload = {
        "filter": {
            "property": "상태",
            "status": {
                "equals": "검토 완료"
            }
        },
        "sorts": [{"timestamp": "created_time", "direction": "descending"}],
        "page_size": 50
    }
    
    try:
        response = requests.post(query_url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        results = data['results']
        
        log(f"📊 '검토 완료' 상태인 글: {len(results)}개 발견")
        
        articles = []
        for page in results:
            # 제목 추출
            title = "제목 없음"
            title_prop = page['properties'].get('내용')
            if title_prop and title_prop.get('title'):
                title = title_prop['title'][0]['plain_text']
            
            # 카테고리 추출
            category = "security"
            category_prop = page['properties'].get('카테고리')
            if category_prop and category_prop.get('select'):
                category = category_prop['select']['name']
            
            # URL 추출
            url = ""
            url_prop = page['properties'].get('URL')
            if url_prop and url_prop.get('url'):
                url = url_prop['url']
            
            # 본문 추출 (간단 버전)
            content = "내용 없음"
            
            articles.append({
                'title': title,
                'category': category,
                'url': url,
                'content': content,
                'posting_date': datetime.now(),
                'page_id': page['id']
            })
        
        return articles
        
    except Exception as e:
        log(f"❌ Notion 조회 실패: {e}")
        return []

def sanitize_filename(title):
    """파일명으로 사용 가능한 문자열로 변환"""
    import re
    # 특수문자 제거
    filename = re.sub(r'[^\w\s-]', '', title)
    # 공백을 하이픈으로 변환
    filename = re.sub(r'[\s]+', '-', filename)
    # 최대 길이 제한
    return filename[:100]

def create_hugo_post(article):
    """Hugo 마크다운 포스트 생성"""
    import re
    
    date_str = article['posting_date'].strftime('%Y-%m-%d')
    time_str = article['posting_date'].strftime('%H:%M:%S')
    filename_slug = sanitize_filename(article['title'])
    
    # Hugo content 구조: content/post/category/filename/index.md
    category = article['category']
    post_dir = posts_dir / category / filename_slug
    post_dir.mkdir(parents=True, exist_ok=True)
    filepath = post_dir / 'index.md'
    
    # 이미 존재하는 경우 스킵
    if filepath.exists():
        log(f"  ⏭️  이미 존재: {category}/{filename_slug}")
        return None
    
    # Hugo Front Matter
    front_matter = f"""---
title: "{article['title']}"
date: {date_str}T{time_str}+09:00
draft: false
categories: ["{category}"]
tags: ["{category}"]
author: "Intelligence Agent"
---

"""
    
    # 본문
    content = article['content']
    
    # 출처 추가
    source = ""
    if article['url']:
        source = f"\n\n---\n\n**출처**: [{article['category']}]({article['url']})"
    
    # 파일 작성
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(front_matter + content + source)
    
    return f"{category}/{filename_slug}/index.md"

def git_commit_and_push(filenames):
    """Git commit & push"""
    try:
        # Git add
        for filename in filenames:
            filepath = posts_dir / filename
            subprocess.run(['git', 'add', str(filepath)], cwd=blog_path, check=True, capture_output=True)
        
        # 커밋
        commit_msg = f"feat: 블로그 글 추가 - {len(filenames)}개 ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
        subprocess.run(['git', 'commit', '-m', commit_msg], cwd=blog_path, check=True, capture_output=True)
        
        # 푸시
        subprocess.run(['git', 'push', 'origin', 'main'], cwd=blog_path, check=True, capture_output=True)
        
        log(f"✅ Git push 완료: {len(filenames)}개 포스트")
        return True
        
    except subprocess.CalledProcessError as e:
        log(f"❌ Git 작업 실패: {e}")
        return False

def main():
    log("=" * 70)
    log("🚀 Auto-Sec-Blogger 자동 발행 시작")
    log("=" * 70)
    
    # 1. "검토 완료" 상태인 글 조회
    articles = get_approved_articles()
    
    if not articles:
        log("📭 발행할 글이 없습니다.")
        return
    
    # 2. Hugo 포스트 생성
    log(f"\n📝 Hugo 포스트 생성 중...")
    filenames = []
    for i, article in enumerate(articles, 1):
        log(f"  [{i}/{len(articles)}] {article['title'][:50]}")
        
        try:
            filename = create_hugo_post(article)
            if filename:
                filenames.append(filename)
                log(f"    ✅ 생성: {filename}")
        except Exception as e:
            log(f"    ❌ 실패: {str(e)[:50]}")
    
    # 3. Git commit & push
    if filenames:
        log(f"\n🔄 Git commit & push 중...")
        git_commit_and_push(filenames)
    else:
        log("\n📭 새로 발행할 글이 없습니다 (모두 이미 발행됨)")
    
    log("\n" + "=" * 70)
    log("✅ 자동 발행 완료")
    log("=" * 70)

if __name__ == "__main__":
    main()
