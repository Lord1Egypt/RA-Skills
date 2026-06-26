---
name: bid_proposal_manager
description: "입찰/사업/연구 공모 안내문을 파싱하여 벡터화하고, 제출서류 검증 및 관련 정보를 자동 추출하여 Notion 프로젝트 페이지를 생성하는 스킬. PDF, HWP, HWPX, DOCX, 웹페이지(URL) 형식을 지원하며 PostgreSQL + pgvector로 벡터 저장. 사용자가 '입찰 공고 분석', '공모 안내문 정리', '제출서류 체크리스트', '사업 공고 Notion 정리', 'RFP 분석', '제안서 준비 지원' 등을 요청할 때 사용."
---

# Bid/Proposal Manager (Claude Cowork 버전)

입찰, 사업, 연구 공모 안내문을 분석하여 핵심 정보를 추출하고,
벡터화(PostgreSQL + pgvector)한 뒤 Notion 프로젝트 페이지로 정리하는 스킬.

## 사용 가능 도구

- **Read/Write/Edit**: 파일 읽기/쓰기
- **Bash**: Python 스크립트 실행, DB 접속
- **WebSearch/WebFetch**: 웹 공고 페이지 수집
- **Notion MCP**: `mcp__notion__*` 도구로 Notion 직접 연동 (연결 시)

## 워크플로우

### Step 1: 공고문 입력 및 파싱

사용자가 제공하는 입력 유형에 따라 처리:

| 입력 유형 | 처리 방법 |
|-----------|-----------|
| PDF 파일 | `Read`로 읽기 또는 `Bash`에서 pdfplumber 실행 |
| HWP/HWPX | `Bash`에서 document_parser.py 실행 |
| DOCX 파일 | `Read`로 읽기 또는 python-docx로 파싱 |
| URL | `WebFetch`로 페이지 수집 후 파싱 |
| 텍스트 | 직접 분석 (스크립트 불필요) |

```bash
# 스크립트 실행
python3 scripts/document_parser.py parse --input uploaded_file.pdf --output parsed.json

# 또는 URL 파싱
python3 scripts/document_parser.py parse --url "https://www.g2b.go.kr/..." --output parsed.json
```

### Step 2: 핵심 정보 추출

```bash
python3 scripts/proposal_analyzer.py analyze --input parsed.json --output analysis.json
```

**추출 필드 (자동):**

| 카테고리 | 항목 | 패턴 |
|----------|------|------|
| 기본 | 사업명, 공고번호, 발주기관, 사업유형 | "사업명:", "공고번호:" 등 |
| 일정 | 마감일, 설명회, 질의마감, 결과발표 | 날짜 패턴 + 키워드 |
| 자격 | 필수/우대/제한 요건 | "참가자격" 섹션 분석 |
| 서류 | 필수/선택 서류 목록 | "제출서류" 섹션 분석 |
| 예산 | 총사업비, 출연금, 부담금 | 금액 패턴 변환 |
| 평가 | 배점표, 가중치 | "평가기준" 섹션+표 |
| 작성 | 목차, 분량, 형식 | "작성요령" 섹션 |

### Step 3: 벡터화 (PostgreSQL + pgvector)

```bash
# DB 초기화 (최초 1회)
python3 scripts/vectorizer.py init-db

# 분석 결과 벡터화 및 저장
python3 scripts/vectorizer.py store --input analysis.json

# 유사 공고 검색
python3 scripts/vectorizer.py search --query "AI 교통 분석 연구" --top 5

# 특정 프로젝트와 유사 공고 비교
python3 scripts/vectorizer.py similar --project-id "UUID" --top 3
```

### Step 4: Notion 페이지 생성

**Notion MCP 연결 시 (권장):**

Notion MCP(`mcp__notion__*`)가 연결되어 있으면 직접 API를 호출하여:
1. 프로젝트 DB에 새 항목 생성 (속성: 사업명, 마감일, 상태, 예산 등)
2. 하위 페이지에 상세 정보 블록 생성

```
사용 순서:
1. notion-search → 대상 DB 찾기
2. notion-create-pages → 프로젝트 페이지 생성
3. notion-update-page → 속성 업데이트
```

**Notion MCP 미연결 시:**

```bash
# 스크립트로 직접 API 호출
python3 scripts/notion_builder.py create \
  --input analysis.json \
  --database-id "NOTION_DB_ID" \
  --create-subpages
```

**Notion 페이지 구조:**

```
📁 입찰/공모 프로젝트 DB
├── 속성: 사업명 | 발주기관 | 마감일 | 상태 | 예산 | 유형
│
├── 📄 [사업명] 상세 페이지
│   ├── 📋 기본 정보
│   ├── 📅 주요 일정 (표)
│   ├── ✅ 제출서류 체크리스트 (체크박스)
│   ├── 📝 자격요건 (필수/우대/제한)
│   ├── 💰 예산/규모 (표)
│   ├── 📖 제안서 작성 요령 (목차+지침)
│   ├── 🔍 평가기준 (배점표)
│   └── 📎 원본 링크
```

### Step 5: 제출서류 검증

사용자가 준비한 서류를 공고 요구사항과 대조:

```bash
python3 scripts/proposal_analyzer.py verify \
  --requirements analysis.json \
  --prepared-dir ./my_documents/
```

결과 예시:
```
✅ 사업계획서.pdf — 준비 완료 (18/20 페이지)
✅ 사업자등록증.pdf — 준비 완료
❌ 재무제표 — 미제출!
⚠️ 참여인력이력서.docx — 분량 초과 (25/20 페이지)
```

## 사용자 결과 출력 형식

Claude가 분석 결과를 사용자에게 보여줄 때:

```
📋 **[사업명] 공고 분석 결과**

기본 정보: 사업명, 발주기관, 공고번호
📅 마감일: 2026-04-30 18:00 (D-25) ⚠️

✅ 제출서류 (총 8건):
  - [ ] 사업계획서 (필수, A4 20페이지 이내)
  - [ ] 사업자등록증 (필수)
  ...

📝 자격요건: 필수 3건, 우대 2건, 제한 1건

💰 예산: 총 5억원 (정부 3억, 민간 2억)
```

## 환경변수

```bash
DATABASE_URL="postgresql://user:pass@localhost:5432/biddb"
EMBEDDING_PROVIDER=sentence_transformers
NOTION_API_KEY=ntn_...
```

## 참고 파일

- `scripts/document_parser.py` — 다중 포맷 문서 파서
- `scripts/proposal_analyzer.py` — 공고문 분석기 + 검증기
- `scripts/vectorizer.py` — pgvector 벡터화 엔진
- `scripts/notion_builder.py` — Notion 자동 생성기
- `references/db_schema.sql` — DB 스키마
- `references/field_taxonomy.json` — 필드 분류 체계
- `templates/notion_template.json` — Notion 템플릿
