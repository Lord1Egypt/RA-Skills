# OpenClaw용 Aviation Web Scraper 설치 가이드

## 설치 방법

### 방법 1: 수동 설치

`aviation-web-scraper` 폴더 전체를 OpenClaw 스킬 디렉토리에 복사합니다:

```bash
# 글로벌 설치 (모든 세션에서 사용)
cp -r aviation-web-scraper/ ~/.openclaw/skills/aviation-web-scraper/

# 또는 프로젝트별 설치
cp -r aviation-web-scraper/ ./skills/aviation-web-scraper/
```

OpenClaw용 SKILL.md를 사용하려면:
```bash
# OpenClaw 버전의 SKILL.md로 교체
cp openclaw-version/SKILL.md ~/.openclaw/skills/aviation-web-scraper/SKILL.md
```

### 방법 2: ClawHub 등록 (커뮤니티 공유)

ClawHub에 등록하려면 [ClawHub 문서](https://clawhub.ai)를 참고하세요.

## 필수 요구사항

- **python3** (스크립트 실행에 필요)
- 선택: `openpyxl` (Excel 생성), `python-docx` (Word 생성), `reportlab` (PDF 생성)

```bash
pip install openpyxl python-docx reportlab
```

## 사용 예시

OpenClaw 채팅(Signal, Telegram, Discord 등)에서:

```
FAA에서 최근 Boeing 737 관련 AD를 수집해서 엑셀로 정리해줘

ICAO와 EASA의 최근 안전 권고를 모아서 마크다운 보고서 만들어줘

국토교통부 항공 관련 최신 고시를 JSON으로 정리해줘
```

## 정기 수집 설정 (cron 활용)

```bash
# crontab -e 로 편집
# 매주 월요일 오전 9시: FAA/ICAO 안전 정보 수집
0 9 * * 1 openclaw run "FAA와 ICAO의 이번 주 항공 안전 정보를 수집하고 마크다운 보고서로 만들어줘. aviation-data/에 JSON 저장."

# 매일 오전 8시: NOTAM 모니터링
0 8 * * * openclaw run "FAA NOTAM 업데이트를 확인하고 요약해줘."

# 매월 1일: 종합 통계 보고서
0 10 1 * * openclaw run "IATA 항공 산업 통계를 수집해서 PDF 보고서로 만들어줘."
```

## Claude Cowork 버전과의 차이

| 항목 | Claude Cowork | OpenClaw |
|------|---------------|----------|
| SKILL.md `name` | kebab-case | snake_case |
| 스킬 위치 | `.claude/skills/` | `~/.openclaw/skills/` |
| 웹 수집 | WebSearch/WebFetch + Chrome MCP | 브라우저 스킬 또는 curl/requests |
| 스케줄 | `create_scheduled_task` 도구 | 시스템 cron + `openclaw run` |
| 문서 생성 | docx/xlsx/pdf 전용 스킬 연동 | Python 라이브러리 직접 사용 |
| 메시지 인터페이스 | 데스크톱 앱 | Signal, Telegram, Discord 등 |

## 디렉토리 구조

설치 후 스킬 디렉토리에 다음 파일들이 위치합니다:

```
~/.openclaw/skills/aviation-web-scraper/
├── SKILL.md                    ← OpenClaw용 (openclaw-version/SKILL.md 복사)
├── scripts/
│   ├── scraper.py              ← 수집 + JSON 구조화
│   └── json_to_docs.py         ← 문서 변환
├── references/
│   └── aviation_glossary.md    ← 항공 용어 사전
└── templates/
    └── report_template.md      ← 보고서 템플릿
```
