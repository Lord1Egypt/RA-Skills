---
name: aviation-web-scraper
description: "항공 기관(ICAO, FAA, EASA, 국토교통부 등) 웹사이트에서 정보를 수집하여 JSON으로 구조화하고 태깅한 뒤, Word/Excel/PDF/Markdown 문서로 변환하는 스킬. 일회성 수집과 정기 스케줄 수집 모두 지원."
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "✈️"
    tags:
      - aviation
      - web-scraping
      - faa
      - icao
      - document-generation
---

# Aviation Web Scraper & Document Generator

항공 기관 공식 웹사이트에서 정보를 수집하고, 구조화된 JSON으로 저장한 뒤, 다양한 형식의 문서로 변환하는 종합 스킬.

## 워크플로우

```
[1. 대상 사이트 확인] → [2. 웹 정보 수집] → [3. JSON 구조화 & 태깅] → [4. 문서 생성] → [5. (선택) 스케줄 등록]
```

## Step 1: 대상 사이트 확인

사용자에게 어떤 항공 기관의 어떤 정보를 수집할지 확인한다.

### 주요 항공 기관 사이트

| 기관 | URL | 주요 정보 |
|------|-----|-----------|
| ICAO | https://www.icao.int | 국제 항공 표준, SARPS, 안전 보고서 |
| FAA | https://www.faa.gov | AD(Airworthiness Directives), NOTAM, 규정 |
| EASA | https://www.easa.europa.eu | 유럽 항공 안전, AD, 인증 |
| 국토교통부 | https://www.molit.go.kr | 국내 항공 정책, 고시, 규정 |
| 항공안전기술원 | https://www.kiast.or.kr | 항공 안전 기술, 인증 |
| NTSB | https://www.ntsb.gov | 항공 사고 조사 보고서 |
| IATA | https://www.iata.org | 항공 산업 통계, 정책 |

### 수집 가능한 정보 유형

- **규정/고시 (Regulations)**: AD, AC, STC, 기술기준
- **안전 정보 (Safety)**: NOTAM, 안전 권고, 사고 보고서
- **뉴스/공지 (News)**: 보도자료, 공지사항, 정책 변경
- **통계 데이터 (Statistics)**: 운항 통계, 사고 통계
- **인증/승인 (Certification)**: 형식증명, 부품승인

## Step 2: 웹 정보 수집

### 수집 방법

OpenClaw 환경에서 사용 가능한 도구를 순서대로 시도한다:

1. **웹 브라우징 스킬** (기본): OpenClaw의 브라우저 통합이 있으면 사용
2. **Python 스크립트**: `scripts/scraper.py`로 검색 패턴 생성 후, 쉘에서 `curl`이나 `requests`로 수집
3. **수동 안내**: 위 방법이 모두 불가하면 사용자에게 직접 URL 접근을 안내

### 수집 시 주의사항

- robots.txt를 존중하고 과도한 요청을 보내지 않는다
- 저작권 콘텐츠는 원문 전체 복사 대신 요약 + 출처 링크를 저장한다
- 수집 날짜/시간과 페이지 URL을 반드시 기록한다

### 검색 패턴 참고

`scripts/scraper.py --list-agencies`로 기관별 검색 패턴을 확인할 수 있다.

예시:
```bash
# FAA 규정 검색 패턴
site:faa.gov airworthiness directive {검색어}

# ICAO 안전 보고서
site:icao.int safety report {검색어}
```

## Step 3: JSON 구조화 & 태깅

수집한 데이터를 아래 스키마에 맞춰 구조화한다.

### JSON 스키마

```json
{
  "metadata": {
    "collection_id": "uuid",
    "collected_at": "ISO 8601 timestamp",
    "source_agency": "FAA",
    "source_url": "https://...",
    "collector": "aviation-web-scraper",
    "version": "1.0"
  },
  "items": [
    {
      "id": "item-001",
      "title": "항목 제목",
      "content": "본문 내용 또는 요약",
      "original_url": "https://...",
      "published_date": "2026-04-01",
      "category": "regulation",
      "tags": ["AD", "airworthiness", "boeing-737"],
      "priority": "high",
      "language": "en",
      "attachments": []
    }
  ],
  "summary": {
    "total_items": 15,
    "categories": {"regulation": 5, "safety": 3, "news": 7},
    "date_range": {"from": "2026-03-01", "to": "2026-04-05"}
  }
}
```

### 태깅 체계

`scripts/scraper.py`의 `auto_tag()`와 `auto_priority()` 함수를 활용하거나, 아래 규칙을 수동으로 적용한다.

**카테고리** (하나 선택): `regulation`, `safety`, `news`, `statistics`, `certification`, `notice`

**도메인 태그** (복수 가능): 기관명, 항공기 모델(boeing-737 등), 주제(airworthiness, maintenance 등)

**우선순위 자동 판별**:
- `critical`: Emergency AD, 긴급 안전 경보, 치명적 사고
- `high`: 일반 AD, 안전 권고
- `medium`: Advisory Circular, 정책 변경
- `low`: 일반 뉴스, 참고 정보

용어가 헷갈릴 때는 `references/aviation_glossary.md`를 참고한다.

### JSON 저장

```
aviation-data/
├── collections/
│   ├── 2026-04-05_FAA_regulations.json
│   └── ...
├── index.json
└── tags/
    └── tag_index.json
```

Python으로 저장할 경우:
```python
from scripts.scraper import create_collection, save_collection
collection = create_collection('FAA', items_list, 'regulation')
save_collection(collection, './aviation-data')
```

## Step 4: 문서 생성

### Markdown (.md)
`scripts/json_to_docs.py`를 사용한다:
```bash
python3 scripts/json_to_docs.py --input collection.json --format md --output ./reports/
```

### Excel (.xlsx)
xlsx 데이터를 준비한 뒤 Python `openpyxl`로 생성:
```bash
python3 scripts/json_to_docs.py --input collection.json --format xlsx-data --output ./reports/
# 생성된 JSON을 바탕으로 openpyxl 스크립트 실행
```

### Word (.docx) / PDF
보고서 구조: 표지 → 목차 → 요약 → 카테고리별 상세 → 태그 인덱스 → 출처

Python의 `python-docx`나 `reportlab` 등을 활용하여 생성한다.

## Step 5: 스케줄 수집 (선택)

사용자가 정기적 수집을 원할 경우:

### OpenClaw에서의 스케줄링

1. **시스템 cron 활용**: OpenClaw CLI를 cron에 등록
```bash
# 매주 월요일 오전 9시 실행
0 9 * * 1 cd ~/aviation-scraper && openclaw run "FAA와 ICAO에서 이번 주 안전 정보를 수집해서 보고서 만들어줘"
```

2. **OpenClaw 자체 스케줄** (지원 시): 에이전트에게 반복 작업을 요청
3. **수동 반복**: 동일 프롬프트를 주기적으로 실행

### 정기 수집 시 추가 처리

- 이전 수집 결과와 diff를 계산하여 신규/변경/삭제 항목 식별
- 변경 이력을 `aviation-data/changelog.json`에 기록
- 문서에 "신규" / "변경" 마크 추가

Python으로 diff:
```python
from scripts.scraper import diff_collections
changes = diff_collections('이전_파일.json', new_collection)
# changes = {"new": [...], "changed": [...], "removed": [...]}
```

## 에러 처리

| 상황 | 대응 |
|------|------|
| 웹사이트 접근 차단 | curl/requests로 재시도 → 불가 시 사용자 안내 |
| 사이트 구조 변경 | 수집 실패 항목 로그 기록 후 사용자 알림 |
| 데이터 파싱 실패 | 원본 HTML 저장, 수동 확인 요청 |
| 네트워크 오류 | 1회 재시도 후 실패 기록 |

## 참고 파일

- `scripts/scraper.py` — 웹 수집 유틸리티 (기관 설정, 자동 태깅, JSON 저장)
- `scripts/json_to_docs.py` — JSON → 마크다운/Excel 데이터 변환
- `references/aviation_glossary.md` — 항공 용어 사전
- `templates/report_template.md` — 보고서 마크다운 템플릿
