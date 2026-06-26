# CostLens

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> OpenClaw 워크플로의 토큰 사용 이벤트를 비용과 예산 상태로 바꿔주는 비용 모니터링 CLI입니다.

| 항목 | 내용 |
| --- | --- |
| 패키지 | `@mike007jd/openclaw-costlens` |
| 런타임 | Node.js 18+ |
| 인터페이스 | CLI + JavaScript 모듈 |
| 주요 명령 | `monitor`, `report`, `budget check` |

## 왜 필요한가

토큰 비용 문제는 대개 워크플로가 커진 뒤에야 드러납니다. CostLens는 모델별 사용량, 비용, 예산 임계값을 조기에 보여 줘서 운영자가 더 빨리 대응할 수 있게 합니다.

## 제공 기능

- prompt/completion 토큰 수가 포함된 JSON 이벤트 배열 로드
- 내장 모델 요율 적용 및 이벤트별 요율 오버라이드 지원
- 모델별, 일자별 비용 집계
- 잘못된 이벤트를 안전하게 건너뛰고 그 사실을 명시
- 예산 사용률을 계산해 warning/critical 상태 반환
- 인수인계와 감사에 사용할 구조화된 보고서 생성

## 대표 워크플로

1. 워크플로 로그에서 토큰 이벤트를 추출합니다.
2. `costlens monitor` 로 빠른 운영 요약을 확인합니다.
3. `--budget`, `--threshold` 로 지출 가드레일을 적용합니다.
4. `costlens report` 로 보고서 파일을 저장합니다.

## 빠른 시작

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/costlens
npm install
node ./bin/costlens.js monitor --events ./fixtures/events.json --budget 0.1 --threshold 75
```

## 명령어

| 명령 | 설명 |
| --- | --- |
| `costlens monitor --events <path>` | 요약 테이블 또는 JSON 출력 |
| `costlens report --events <path> --out <path>` | 전체 JSON 보고서 저장 |
| `costlens budget check --events <path> --budget <amount>` | 예산 상태 확인 및 임계 초과 시 차단 코드 반환 |

## 이벤트 형식

```json
{
  "model": "gpt-4.1",
  "promptTokens": 1200,
  "completionTokens": 300,
  "timestamp": "2026-03-10T10:00:00Z"
}
```

## 출력 동작

- `monitor` 는 정상/경고 상태에서 `0`, 심각한 예산 초과 시 `2` 를 반환합니다
- `report` 는 총합, 모델별 집계, 날짜별 집계, 예산 상태를 담은 JSON 파일을 생성합니다
- 잘못된 이벤트는 실행을 중단시키지 않고 건너뜁니다

## 프로젝트 구조

```text
costlens/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## 현재 상태

현재 구현은 오프라인 이벤트 분석과 예산 관리에 초점을 둡니다. 실시간 과금 시스템이라기보다 실용적인 비용 리포팅 레이어에 가깝습니다.
