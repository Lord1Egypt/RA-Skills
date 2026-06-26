---
name: auto-sec-blogger
version: 1.1.0
description: AI-powered security blog automation system (identical to github.com/rebugui/intelligence-agent). Collects news from Google News, arXiv, HackerNews → generates blog posts with GLM-4.7 → publishes to Notion → auto-deploys to GitHub Pages via Git. Features Human-in-the-Loop approval workflow. Use when you want to automate blog writing, news collection, or content generation with the exact functionality of the original intelligence-agent repository. Triggers: "블로그 글 작성", "보안 뉴스 발행", "깃헙 블로그 발행", "intelligence agent", "지능형 에이전트", "자동 글쓰기".
---

# Intelligence Agent

## 개요

보안 뉴스를 자동으로 수집하고, LLM(GLM-4.7)을 사용하여 전문가 수준의 블로그 글을 작성한 후, Notion과 GitHub Pages에 자동으로 게시하는 시스템입니다.

**GitHub 저장소와 동일**: https://github.com/rebugui/intelligence-agent

## 아키텍처

```
뉴스 수집 (Google News, arXiv, HackerNews)
    ↓
GLM-4.7 글 작성 (전문 보안 블로그)
    ↓
Notion Draft 저장 (상태: Draft)
    ↓
사용자 검토 및 승인 (Human-in-the-Loop)
    ↓
Git Push → GitHub Actions → GitHub Pages
```

## 주요 기능

### 1. 뉴스 수집 (News Collection)
- **Google News**: 키워드 기반 보안 뉴스 수집
- **arXiv**: 최신 보안 연구 논문 수집
- **HackerNews**: 트렌딩 기술 뉴스 수집
- **중복 제거**: URL 기반 중복 뉴스 필터링

### 2. LLM 글쓰기 (Content Generation)
- **모델**: GLM-4.7 (Zhipu AI)
- **스타일**: 전문 보안 블로그
- **구조**:
  - 제목 (헤드라인)
  - 요약 (3줄 요약)
  - 본문 (상세 분석)
  - 결론 (시사점)
  - 태그 (키워드)
- **Mermaid 다이어그램**: 공격 흐름, 아키텍처 시각화

### 3. Notion 통합 (Notion Integration)
- **상태 관리**: Draft → Review → Approved → Published
- **자동 저장**: 생성된 글 자동 저장
- **사용자 승인**: Notion에서 상태 변경으로 배포 승인

### 4. Git 기반 발행 (Git Publishing)
- **자동 커밋**: 마크다운 파일 Git에 커밋
- **GitHub Actions**: 자동 Jekyll 빌드
- **GitHub Pages**: 정적 블로그 배포

## 설치

### 1. 의존성 설치

```bash
cd ~/.openclaw/workspace/skills/intelligence-agent/scripts
pip3 install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
# ~/.openclaw/workspace/.env

# GLM API
GLM_API_KEY=your_glm_api_key
GLM_BASE_URL=https://api.z.ai/api/coding/paas/v4

# Notion
NOTION_API_KEY=ntn_xxx
NOTION_DATABASE_ID=xxx

# GitHub Pages
GITHUB_TOKEN=ghp_xxx
GITHUB_BLOG_REPO=username/username.github.io
BLOG_LOCAL_PATH=/path/to/blog/repo
```

## 사용법

### 1. 전체 파이프라인 실행 (테스트용)

```bash
cd ~/.openclaw/workspace/skills/intelligence-agent/scripts
python3 intelligence_pipeline.py --max-articles 5
```

### 2. 뉴스 수집만

```python
from collector import NewsCollector

collector = NewsCollector()
articles = collector.fetch_all(max_results_per_source=15)
```

### 3. 블로그 글 작성만

```python
from writer import BlogWriter

writer = BlogWriter()
post = writer.generate_article(article_data)
```

### 4. Notion 발행만

```python
from notion_publisher import NotionPublisher

publisher = NotionPublisher()
result = publisher.create_article(blog_post)
```

### 5. Git 발행만

```python
from git_publisher_service import GitPublisherService

git_publisher = GitPublisherService()
git_publisher.publish(blog_posts)
```

## 워크플로우 상세

### 1단계: 뉴스 수집

```python
# collector.py
class NewsCollector:
    def fetch_google_news(self, query="security vulnerability"):
        # Google News RSS 피드에서 수집
        pass

    def fetch_arxiv(self, category="cs.CR"):
        # arXiv 보안 논문 수집
        pass

    def fetch_hackernews(self):
        # HackerNews 트렌딩 기사 수집
        pass
```

### 2단계: AI 기사 선별

```python
# selector.py
class ArticleSelector:
    async def evaluate_and_select(self, articles, max_articles=5):
        # GLM-4.7으로 기사 품질 평가
        # 점수 기반 상위 기사 선별
        pass
```

### 3단계: 블로그 글 작성

```python
# writer.py
class BlogWriter:
    async def generate_article(self, article):
        # GLM-4.7으로 블로그 글 작성
        # Mermaid 다이어그램 생성
        # 마크다운 형식 출력
        pass
```

### 4단계: Notion 발행

```python
# notion_publisher.py
class NotionPublisher:
    def create_article(self, blog_post):
        # Notion DB에 Draft 상태로 저장
        # 상태: Draft → Review → Approved
        pass
```

### 5단계: Git 발행 (사용자 승인 후)

```python
# git_publisher_service.py
class GitPublisherService:
    def publish(self, blog_posts):
        # 마크다운 파일 생성
        # Git commit & push
        # GitHub Actions 트리거
        pass
```

## Cron 스케줄링

### 매일 08:30 자동 실행

```python
# intelligence_pipeline.py
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
scheduler.add_job(run_pipeline, 'cron', hour=8, minute=30)
scheduler.start()
```

## Notion 데이터베이스 구조

### 필수 속성

| 속성명 | 타입 | 설명 |
|--------|------|------|
| 제목 | title | 블로그 글 제목 |
| 상태 | select | Draft/Review/Approved/Published |
| 날짜 | date | 발행일 |
| 태그 | multi_select | 키워드 |
| URL | url | 원문 URL |
| 카테고리 | select | 취약점/연구/트렌드 |

## Jekyll 블로그 구조

```
blog/
├── _posts/
│   ├── 2025-03-09-cve-2025-xxxx-analysis.md
│   ├── 2025-03-09-ai-security-trends.md
│   └── ...
├── _layouts/
│   ├── post.html
│   └── default.html
├── _config.yml
└── .github/
    └── workflows/
        └── jekyll.yml
```

## 트러블슈팅

### GLM API Rate Limit

```
❌ Error: Rate limit reached (429)
```

**해결**:
- 자동 재시도 3회
- 60초 대기 후 재시도

### Notion API Error

```
❌ Error: Notion API error
```

**해결**:
- API 키 확인
- Database ID 확인
- Integration 권한 확인

### Git Push 실패

```
❌ Error: Git push failed
```

**해결**:
- GitHub Token 확인
- 원격 저장소 권한 확인
- 브랜치 확인

## 파일 구조

```
intelligence-agent/
├── SKILL.md (이 파일)
├── scripts/
│   ├── intelligence_pipeline.py (메인 파이프라인)
│   ├── collector.py (뉴스 수집)
│   ├── selector.py (AI 기사 선별)
│   ├── writer.py (블로그 글 작성)
│   ├── notion_publisher.py (Notion 발행)
│   ├── git_publisher_service.py (Git 발행)
│   ├── llm_client.py (GLM API 클라이언트)
│   ├── llm_client_async.py (비동기 GLM 클라이언트)
│   ├── prompt_manager.py (프롬프트 관리)
│   ├── prompts.yaml (프롬프트 템플릿)
│   ├── models.py (데이터 모델)
│   ├── utils.py (유틸리티)
│   ├── config.py (설정)
│   └── requirements.txt (의존성)
└── references/
    ├── architecture.md (상세 아키텍처)
    ├── prompts_guide.md (프롬프트 가이드)
    └── api_reference.md (API 레퍼런스)
```

## 환경 변수

### 필수

```bash
GLM_API_KEY          # GLM-4.7 API 키
NOTION_API_KEY       # Notion API 키
NOTION_DATABASE_ID   # Notion 데이터베이스 ID
```

### 선택사항

```bash
GITHUB_TOKEN         # GitHub 개인 액세스 토큰
GITHUB_BLOG_REPO     # GitHub 블로그 저장소 (username/repo)
BLOG_LOCAL_PATH      # 로컬 블로그 경로
```

## 테스트

### 전체 파이프라인 테스트

```bash
python3 test_full_pipeline.py
```

### Mermaid 다이어그램 테스트

```bash
python3 test_mermaid_fix.py
```

## 참고자료

- [GitHub 저장소](https://github.com/rebugui/intelligence-agent)
- [GLM API 문서](https://open.bigmodel.cn/dev/api)
- [Notion API 문서](https://developers.notion.com/)
- [Jekyll 문서](https://jekyllrb.com/docs/)

## 리소스

### scripts/
원본 저장소의 모든 Python 스크립트 포함:
- `intelligence_pipeline.py` - 전체 파이프라인 실행
- `collector.py` - 뉴스 수집기
- `selector.py` - AI 기사 선별
- `writer.py` - 블로그 글 작성
- `notion_publisher.py` - Notion 발행
- `git_publisher_service.py` - Git 발행
- `llm_client.py` - GLM API 클라이언트
- `prompts.yaml` - 프롬프트 템플릿

### references/
- `architecture.md` - 상세 아키텍처 설명
- `prompts_guide.md` - 프롬프트 작성 가이드
- `api_reference.md` - API 레퍼런스
