# Baseline Kit

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> OpenClaw 설정을 더 안전한 기본값으로 시작하고 오프라인 감사를 수행할 수 있게 돕는 베이스라인 생성 및 감사 도구입니다.

| 항목 | 내용 |
| --- | --- |
| 패키지 | `@mike007jd/openclaw-baseline-kit` |
| 런타임 | Node.js 18+ |
| 인터페이스 | CLI + JavaScript 모듈 |
| 주요 명령 | `generate`, `audit` |

## 왜 필요한가

많은 OpenClaw 사고는 코드보다 설정에서 시작됩니다. Baseline Kit은 더 안전한 기본 프로필을 생성하고, 기존 설정 파일에서 네트워크 노출, 제어 누락, 기본적인 시크릿 위생 문제를 찾아내도록 설계되었습니다.

## 제공 기능

- `development`, `team`, `enterprise`, `airgapped` 프로필 생성
- 리뷰 가능한 JSON 파일 작성
- 기존 `openclaw.json` 스타일 설정 감사
- 인증 rate limit 누락, 과도한 소스 허용, 감사 로그 누락 등 탐지
- SOC2, ISO27001, NIST CSF 같은 컴플라이언스 태그 연결

## 대표 워크플로

1. 환경에 맞는 프로필을 생성합니다.
2. 생성된 JSON 을 검토하고 버전 관리에 포함합니다.
3. 릴리스 전이나 변경 리뷰 후 기존 설정을 감사합니다.
4. findings 를 바탕으로 노출 범위, 로깅, 소스 제어를 강화합니다.

## 빠른 시작

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/baseline-kit
npm install
node ./bin/baseline-kit.js generate --profile enterprise --out /tmp/openclaw.json
node ./bin/baseline-kit.js audit --config ./fixtures/insecure-openclaw.json
```

## 명령어

| 명령 | 설명 |
| --- | --- |
| `baseline-kit generate --profile <development|team|enterprise|airgapped> --out <path>` | 베이스라인 JSON 생성 |
| `baseline-kit audit --config <path>` | 기존 설정 파일 감사 |

## 프로필

| 프로필 | 초점 |
| --- | --- |
| `development` | 로컬 개발 속도에 맞춘 가벼운 보존 기간과 rate limit |
| `team` | 소규모 팀 공유 환경을 위한 기본값 |
| `enterprise` | 더 엄격한 인증 창, 긴 감사 보존 기간, 복구 힌트 |
| `airgapped` | loopback-only 와 로컬 미러 중심 설정 |

## 감사 범위

- 게이트웨이 바인드 주소와 네트워크 노출
- 인증 rate limit 구성 완전성
- 스킬 소스 제한 품질
- 감사 로깅 존재 여부
- 백업 힌트
- 설정 트리 안의 시크릿 유사 값

## 프로젝트 구조

```text
baseline-kit/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## 현재 상태

Baseline Kit은 현재 JSON 프로필 생성과 오프라인 설정 감사에 초점을 맞춥니다. 완전한 설정 관리 플랫폼이라기보다 시작용 베이스라인과 정책 lint 단계에 적합합니다.
