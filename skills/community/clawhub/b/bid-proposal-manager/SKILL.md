---
name: bid-proposal-manager
description: "입찰/사업/연구 공모 안내문을 파싱하여 벡터화하고, 제출서류 검증 및 관련 정보를 자동 추출하여 Notion 프로젝트 페이지를 생성하는 스킬. PDF, HWP, HWPX, DOCX, 웹페이지 형식의 공고문을 지원하며, PostgreSQL + pgvector로 시맨틱 검색 가능."
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - psql
    emoji: "📋"
    tags:
      - bid-management
      - rfp
      - proposal
      - notion
      - vector-search
---

# Bid/Proposal Manager (입찰·공모 관리 스킬)

입찰, 사업, 연구 공모 안내문을 다양한 포맷(PDF, HWP, HWPX, DOCX, 웹페이지)에서 파싱하여,
핵심 정보를 자동 추출하고 벡터화(PostgreSQL + pgvector)한 뒤,
Notion 프로젝트 DB와 하위 페이지로 체계적으로 정리하는 종합 스킬.

## 아키텍처

```
┌──────────────────────────────────────────────────────────────┐
│                    입력 소스 (Input Sources)                   │
│  PDF │ HWP/HWPX │ DOCX │ 웹페이지(URL)                        │
└────────────┬─────────────────────────────────────────────────┘
             ▼
┌──────────────────────────────────────────────────────────────┐
│             문서 파서 (document_parser.py)                     │
│  포맷 자동 감지 → 텍스트 추출 → 구조화된 섹션 분리              │
└────────────┬─────────────────────────────────────────────────┘
             ▼
┌──────────────────────────────────────────────────────────────┐
│           공고문 분석기 (proposal_analyzer.py)                  │
│  핵심 필드 추출: 사업명, 기한, 자격요건, 제출서류, 예산 등       │
│  제출서류 체크리스트 자동 생성                                   │
│  작성 요령(목차, 분량, 형식) 추출                               │
└────────────┬─────────────┬───────────────────────────────────┘
             │             ▼
             │  ┌──────────────────────────────────────────────┐
             │  │       벡터화 엔진 (vectorizer.py)              │
             │  │  텍스트 → 임베딩 → PostgreSQL + pgvector 저장  │
             │  │  시맨틱 검색, 유사 공고 비교, RAG 지원           │
             │  └──────────────────────────────────────────────┘
             ▼
┌──────────────────────────────────────────────────────────────┐
│          Notion 빌더 (notion_builder.py)                       │
│  프로젝트 DB 생성/업데이트 + 상세 하위 페이지 자동 생성          │
│  제출서류 체크리스트, 일정표, 자격요건 정리                       │
└──────────────────────────────────────────────────────────────┘
```

## 워크플로우

### Step 1: 공고문 입력

사용자로부터 입찰/공모 안내문을 받는다:

```bash
# PDF 파일
python3 scripts/document_parser.py parse --input announcement.pdf --output parsed.json

# HWP/HWPX 파일
python3 scripts/document_parser.py parse --input announcement.hwp --output parsed.json

# DOCX 파일
python3 scripts/document_parser.py parse --input announcement.docx --output parsed.json

# 웹페이지 URL
python3 scripts/document_parser.py parse --url "https://www.g2b.go.kr/..." --output parsed.json

# 여러 파일 일괄 처리
python3 scripts/document_parser.py batch --dir ./announcements/ --output batch_parsed.json
```

### Step 2: 핵심 정보 추출

공고문에서 구조화된 정보를 자동 추출한다:

```bash
python3 scripts/proposal_analyzer.py analyze --input parsed.json --output analysis.json
```

**추출 필드:**

| 카테고리 | 추출 항목 |
|----------|-----------|
| 기본 정보 | 사업명, 공고번호, 발주기관, 공고일, 사업유형 |
| 일정 | 제출마감일, 설명회일, 질의응답 기한, 선정발표일 |
| 자격요건 | 참가자격, 필수조건, 우대조건, 제한사항 |
| 제출서류 | 필수서류 목록, 선택서류, 서류별 양식/형식 요구사항 |
| 예산/규모 | 총 사업비, 정부출연금, 민간부담금, 사업 기간 |
| 작성 요령 | 제안서 목차, 분량 제한, 평가 기준, 배점표 |
| 연락처 | 담당자, 전화번호, 이메일, 접수처 |

### Step 3: 벡터화 및 저장

추출된 텍스트를 임베딩하여 PostgreSQL + pgvector에 저장한다:

```bash
# 단일 공고 벡터화
python3 scripts/vectorizer.py store --input analysis.json

# 유사 공고 검색
python3 scripts/vectorizer.py search --query "AI 기반 교통 분석 연구" --top 5

# 특정 공고와 유사한 과거 공고 비교
python3 scripts/vectorizer.py similar --project-id "BID-2026-0042" --top 3
```

**벡터화 대상:**
- 사업명 + 사업 개요 (핵심 벡터)
- 자격요건 텍스트
- 제출서류 상세 설명
- 평가 기준 / 작성 요령 전문

### Step 4: 제출서류 검증

사용자가 준비한 서류와 공고 요구사항을 대조 검증:

```bash
python3 scripts/proposal_analyzer.py verify \
  --requirements analysis.json \
  --prepared-dir ./my_documents/ \
  --output verification.json
```

**검증 항목:**
- 필수서류 누락 여부 ✅/❌
- 파일명 규칙 준수 여부
- 분량(페이지 수) 준수 여부
- 필수 포함 항목(목차) 확인
- 제출 기한 경과 여부

### Step 5: Notion 페이지 생성

분석 결과를 Notion 프로젝트 DB와 하위 페이지로 자동 생성:

```bash
python3 scripts/notion_builder.py create \
  --input analysis.json \
  --database-id "YOUR_NOTION_DB_ID" \
  --create-subpages
```

**Notion 구조:**

```
📁 입찰/공모 프로젝트 DB (데이터베이스)
├── 속성: 사업명, 발주기관, 마감일, 상태, 예산, 유형, 자격충족여부
│
├── 📄 [사업명] 상세 페이지
│   ├── 📋 기본 정보 (callout)
│   ├── 📅 주요 일정 (table)
│   ├── ✅ 제출서류 체크리스트 (to-do list)
│   ├── 📝 자격요건 (bulleted list)
│   ├── 💰 예산/규모 (table)
│   ├── 📖 제안서 작성 요령
│   │   ├── 목차 구조
│   │   ├── 분량 제한
│   │   └── 평가 기준/배점표
│   ├── 🔍 유사 공고 (벡터 검색 결과)
│   └── 📎 원본 파일 링크
│
├── 📄 [다른 사업명] 상세 페이지
│   └── ...
```

---

## 문서 파싱 상세

### PDF 파싱
```bash
# pdfplumber 사용 (표 추출에 강함)
pip install pdfplumber
# 또는 PyMuPDF (fitz) 사용 (일반 텍스트 추출에 빠름)
pip install PyMuPDF
```

### HWP/HWPX 파싱
```bash
# hwp5 (한글 파일 텍스트 추출)
pip install pyhwp
# HWPX는 ZIP 기반 XML이므로 직접 파싱
# hwpx → unzip → content.xml → XML 파싱
```

### DOCX 파싱
```bash
pip install python-docx
```

### 웹페이지 파싱
```bash
# requests + BeautifulSoup
pip install requests beautifulsoup4
# 또는 Playwright (JS 렌더링 필요 시)
```

포맷을 자동 감지하여 적합한 파서를 선택한다. `document_parser.py`가 이를 처리.

---

## PostgreSQL + pgvector 설정

### 사전 요구사항

```bash
# PostgreSQL 15+ 설치 확인
psql --version

# pgvector 확장 설치
# macOS (Homebrew)
brew install pgvector

# Ubuntu/Debian
sudo apt install postgresql-15-pgvector

# 설치 확인
psql -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### DB 스키마 생성

```bash
psql -f references/db_schema.sql
```

또는 스크립트로:
```bash
python3 scripts/vectorizer.py init-db --db-url "postgresql://user:pass@localhost:5432/biddb"
```

### 임베딩 방식

| 방식 | 설명 | 비고 |
|------|------|------|
| OpenAI API | `text-embedding-3-small` (1536 dim) | API 키 필요 |
| Sentence Transformers | `all-MiniLM-L6-v2` (384 dim) | 로컬 무료 |
| Ollama | `nomic-embed-text` (768 dim) | 로컬 무료 |

기본값은 Sentence Transformers (로컬). 환경변수 `EMBEDDING_PROVIDER`로 변경 가능.

---

## CLI 명령어 요약

```bash
# === 문서 파싱 ===
python3 scripts/document_parser.py parse --input FILE --output parsed.json
python3 scripts/document_parser.py parse --url URL --output parsed.json
python3 scripts/document_parser.py batch --dir DIR --output batch.json

# === 공고 분석 ===
python3 scripts/proposal_analyzer.py analyze --input parsed.json --output analysis.json
python3 scripts/proposal_analyzer.py verify --requirements analysis.json --prepared-dir DIR
python3 scripts/proposal_analyzer.py checklist --input analysis.json

# === 벡터화 ===
python3 scripts/vectorizer.py init-db
python3 scripts/vectorizer.py store --input analysis.json
python3 scripts/vectorizer.py search --query "검색어" --top N
python3 scripts/vectorizer.py similar --project-id ID --top N

# === Notion 연동 ===
python3 scripts/notion_builder.py create --input analysis.json --database-id DB_ID
python3 scripts/notion_builder.py update --project-id ID --input analysis.json
python3 scripts/notion_builder.py dashboard --database-id DB_ID
```

---

## 환경변수

```bash
# PostgreSQL 연결
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=biddb
export PGUSER=your_user
export PGPASSWORD=your_password
# 또는 통합 URL
export DATABASE_URL="postgresql://user:pass@localhost:5432/biddb"

# 임베딩 설정
export EMBEDDING_PROVIDER=sentence_transformers  # 또는 openai, ollama
export OPENAI_API_KEY=sk-...                      # OpenAI 사용 시
export OLLAMA_BASE_URL=http://localhost:11434      # Ollama 사용 시

# Notion API
export NOTION_API_KEY=ntn_...
export NOTION_DATABASE_ID=...                      # 기본 프로젝트 DB ID (선택)
```

---

## 보안 및 주의사항

- **개인정보**: 공고문 내 개인정보(담당자 연락처 등)는 벡터화하지 않음
- **API 키**: 환경변수로만 관리, 코드에 하드코딩 금지
- **저작권**: 공고문 원문은 요약+출처 링크 방식으로 Notion에 기록
- **DB 백업**: 정기적으로 `pg_dump`를 권장

## 참고 파일

- `scripts/document_parser.py` — 다중 포맷 문서 파서
- `scripts/proposal_analyzer.py` — 공고문 분석기 + 제출서류 검증기
- `scripts/vectorizer.py` — pgvector 벡터화 엔진
- `scripts/notion_builder.py` — Notion 페이지 자동 생성기
- `references/db_schema.sql` — PostgreSQL + pgvector 스키마
- `references/field_taxonomy.json` — 입찰 분야 분류 및 필드 정의
- `references/setup_guide.md` — 환경 설정 가이드
- `templates/notion_template.json` — Notion 페이지 템플릿 구조
