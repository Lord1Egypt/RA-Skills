---
name: dev-factory
version: 1.1.0
description: Automated software development agent using ChatDev 2.0 and GLM-5. Discovers topics from GitHub Trending, CVE databases, and security news → generates code with 7-agent ChatDev team → tests automatically → publishes to GitHub. Self-correction loop (error → fix → retry, max 3 times). Use when you want to automate development, create security tools, or generate DevOps utilities. Triggers: "자동 개발", "도구 생성", "builder agent", "chatdev".
---

# Builder Agent

## 개요

보안 도구와 DevOps 유틸리티를 자동으로 생성하는 개발 에이전트입니다. ChatDev 2.0의 7개 에이전트가 협업하여 요구사항 분석부터 배포까지 전 과정을 자동화합니다.

**자가 수정 루프**: 에러 발생 시 자동으로 수정 후 재시도 (최대 3회)

## 워크플로우

```
아이디어 발굴 (GitHub Trending, CVE, Security News)
    ↓
Notion 큐 등록 (아이디어 데이터베이스)
    ↓
ChatDev 2.0 개발 (7개 에이전트 협업)
    ├─ CEO: 요구사항 분석
    ├─ CPO: 제품 기획
    ├─ CTO: 아키텍처 설계
    ├─ Programmer: 코드 생성
    ├─ Reviewer: 코드 리뷰
    ├─ Tester: 테스트 생성
    └─ CTO Final: 최종 검증
    ↓
자동 테스트 실행
    ↓
에러 발생? → 수정 → 재시도 (최대 3회)
    ↓
GitHub 저장소 생성 및 배포
```

## 주요 기능

### 1. 아이디어 발굴 (Discovery)
- **GitHub Trending**: 인기 프로젝트 분석
- **CVE 데이터베이스**: 최신 취약점 기반 도구
- **Security News**: 보안 뉴스 기반 유틸리티
- **Notion 큐**: 아이디어 자동 등록

### 2. ChatDev 2.0 개발 (Development)
**7개 에이전트 협업**:

| 에이전트 | 역할 | 담당 업무 |
|---------|------|----------|
| CEO | 최고경영자 | 요구사항 분석, 방향성 결정 |
| CPO | 최고제품책임자 | 제품 기획, 기능 정의 |
| CTO | 최고기술책임자 | 아키텍처 설계, 기술 스택 결정 |
| Programmer | 개발자 | 코드 생성, 구현 |
| Reviewer | 리뷰어 | 코드 리뷰, 품질 검증 |
| Tester | 테스터 | 테스트 코드 작성, 실행 |
| CTO Final | 최종검토자 | 최종 검증, 배포 승인 |

### 3. 자가 수정 루프 (Self-Correction)
```
테스트 실행
    ↓
에러 발견
    ↓
에러 분석 → 수정 방안 도출
    ↓
코드 수정
    ↓
재테스트
    ↓
성공? → 배포 / 실패? → 재시도 (최대 3회)
```

### 4. GitHub 자동 배포 (Publishing)
- **저장소 생성**: 자동으로 GitHub 저장소 생성
- **코드 업로드**: 완성된 코드 자동 푸시
- **README 생성**: 자동 문서화
- **릴리즈 생성**: v1.0.0 자동 릴리즈

## 설치 방법

### 1. 저장소 클론
```bash
git clone --recursive https://github.com/rebugui/OpenClaw.git
cd OpenClaw/submodules/builder-agent
```

### 2. ChatDev 2.0 설정
```bash
cd ../chatdev-v2
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 의존성 설치
```bash
cd ../builder-agent
pip install -r requirements.txt
```

### 4. 환경 변수 설정
```bash
cp .env.example .env
```

`.env` 파일 수정:
```bash
# GLM API (Zhipu AI)
GLM_API_KEY=your_glm_api_key
GLM_BASE_URL=https://api.z.ai/api/coding/paas/v4

# GitHub
GITHUB_TOKEN=your_github_token
GITHUB_USERNAME=your_username

# Notion
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_database_id

# ChatDev
CHATDEV_URL=http://localhost:6400
```

### 5. ChatDev 서버 시작
```bash
cd ../chatdev-v2
python server_main.py --port 6400
# API: http://localhost:6400
```

## 사용법

### 수동 실행

#### 1. 아이디어 발굴
```bash
python main.py discovery
```

#### 2. 개발 실행
```bash
# Notion 큐에서 아이디어 가져와서 개발
python main.py develop

# 특정 프로젝트 개발
python main.py develop --project "cve-scanner"
```

#### 3. 큐 모니터링
```bash
python queue_monitor.py
```

### 스케줄러 등록

OpenClaw 스케줄러에 등록하여 자동 실행:

```yaml
# config.yaml
jobs:
  # 아이디어 발굴 (매일 08:00, 20:00)
  - id: "builder_discovery"
    name: "Builder Discovery - 매일 오전 8시/오후 8시 아이디어 발굴"
    enabled: true
    module: "submodules.builder-agent.main"
    class: "BuilderAgentV3"
    method: "run_discovery"
    trigger:
      type: "cron"
      day_of_week: "mon-sun"
      hour: "8,20"
      minute: 0

  # 개발 큐 처리 (6시간마다)
  - id: "builder_queue_processor"
    name: "Builder Queue Processor - 6시간마다 개발/개선 큐 처리"
    enabled: true
    module: "submodules.builder-agent.main"
    class: "BuilderAgentV3"
    method: "run_development_from_notion"
    trigger:
      type: "interval"
      hours: 6

  # 큐 모니터링 (6시간마다)
  - id: "builder_queue_monitor"
    name: "Builder Queue Monitor - 6시간마다 큐 상태 체크 및 알림"
    enabled: true
    module: "modules.builder.queue_monitor"
    function: "main"
    trigger:
      type: "interval"
      hours: 6
```

## 설정 파일

### `config.yaml`
```yaml
discovery:
  sources:
    - github_trending
    - cve_database
    - security_news
  max_ideas: 5
  keywords:
    - vulnerability
    - scanner
    - automation

development:
  max_retries: 3
  test_timeout: 300
  output_dir: "./projects"

chatdev:
  url: "http://localhost:6400"
  model: "glm-5"
  timeout: 1800

github:
  auto_publish: true
  private: false
  license: "MIT"
```

## 파일 구조

```
builder-agent/
├── main.py              # 메인 실행 파일
├── config.yaml          # 설정 파일
├── .env.example         # 환경 변수 예시
├── requirements.txt     # 의존성
│
├── discoverer/          # 아이디어 발굴
│   ├── github_trending.py
│   ├── cve_analyzer.py
│   └── news_monitor.py
│
├── orchestrator/        # 개발 오케스트레이션
│   ├── chatdev_client.py
│   ├── test_runner.py
│   └── github_publisher.py
│
├── improvement/         # 개선 시스템
│   └── improvement_pipeline.py
│
├── models/              # 데이터 모델
│   └── project.py
│
└── logs/                # 로그
    └── builder.log
```

## Notion 데이터베이스 설정

### 아이디어 데이터베이스
- `Title` (제목)
- `Status` (선택: Idea, Developing, Testing, Completed, Failed)
- `Priority` (선택: High, Medium, Low)
- `Source` (선택: GitHub, CVE, News)
- `Created` (생성일)
- `Repository` (URL)

## 예시 프로젝트

### 생성된 프로젝트들
1. **secure_app** - 보안 설정 자동화 도구
2. **cve-scanner-v2** - CVE 취약점 스캐너
3. **file-integrity-monitor** - 파일 무결성 모니터링

### 프로젝트 구조
```
cve-scanner-v2/
├── README.md
├── requirements.txt
├── setup.py
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── utils.py
└── tests/
    ├── __init__.py
    └── test_main.py
```

## 성공/실패 기록

### 성공한 프로젝트 (2026-02-22 ~ 2026-02-23)
1. **secure_app** ✅ (2026-02-22 18:08)
2. **cve-scanner-v2** ✅ (2026-02-23 12:17)
3. **cve-scanner-v6** ✅ (2026-02-23 13:41)
4. **cve-scanner-v7** ✅ (2026-02-23 13:46)
5. **cve-scanner-v8** ✅ (2026-02-23 14:10)

### 실패한 프로젝트
1. **file-integrity-monitor** ❌ - 테스트 실패
2. **cve-scanner-v3** ❌ - 테스트 실패
3. **cve-scanner-v5** ❌ - 테스트 실패

**공통 문제**: 테스트 코드가 구현 로직과 일치하지 않음 → 프롬프트 개선 필요

## 문제 해결

### ChatDev 연결 실패
```bash
# ChatDev 서버 상태 확인
curl http://localhost:6400/health

# 서버 재시작
cd ../chatdev-v2
python server_main.py --port 6400
```

### 테스트 실패
```bash
# 로그 확인
tail -f logs/builder.log

# 수동 테스트 실행
cd projects/cve-scanner-v2
pytest tests/
```

### GitHub 배포 실패
```bash
# Git 권한 확인
ssh -T git@github.com

# 토큰 권한 확인
curl -H "Authorization: token {GITHUB_TOKEN}" https://api.github.com/user
```

## 의존성

- Python 3.11+
- ChatDev 2.0
- GLM-5 API
- GitHub Personal Access Token
- Notion API

## 라이선스

MIT License

## 참고

- **저장소**: https://github.com/rebugui/builder-agent
- **ChatDev 2.0**: https://github.com/OpenBMB/ChatDev
- **메인 저장소**: https://github.com/rebugui/OpenClaw
