# genspark-ralphy-cli

원본 [Ralphy CLI](https://github.com/michaelshimeles/ralphy)를 Genspark Claw 실행 엔진으로 연결합니다. Ralphy가 PRD에서 작업을 선택하고, 작업마다 새로운 Claw 세션을 생성해 구현·검증한 뒤 완료 항목을 체크합니다.

## 언제 쓰나

- 원본 Ralphy CLI의 반복 제어 로직을 그대로 쓰고 싶을 때
- 작업마다 완전히 격리된 새 세션을 보장받고 싶을 때
- Ralphy 생태계(포맷, 커뮤니티)와 호환이 필요할 때

## 사전 요구사항

이 스킬을 사용하려면 `ralphy-claw` 저장소가 로컬에 설치되어 있어야 합니다:

```sh
git clone https://github.com/kimhyejoo/ralphy-claw
cd ralphy-claw
bun run setup
bun run install-skill
```

## 사용법

Genspark Claw 대화에서:

```
genspark-ralphy-cli 스킬로 원본 Ralphy를 실행해줘.
대상 프로젝트: /내/프로젝트/경로
PRD: PRD.md
최대 3개 작업, 자동 커밋 없이
```

터미널에서 직접 실행:

```sh
cd /내/프로젝트/경로
/path/to/ralphy-claw/bin/ralphy-claw \
  --prd PRD.md --max-iterations 3 --no-commit
```

## PRD 형식

```markdown
# Tasks

- [ ] TASK-001: 작업 설명. 완료 조건: 검증 명령 또는 확인 방법.
- [ ] TASK-002: 다음 작업 설명.
```

## 동작 방식

```
Ralphy CLI (원본 4.7.2)
  └─ 작업 선택
       └─ Genspark Claw 게이트웨이로 새 세션 spawn
            └─ 구현 + 검증 (완료 마커 확인)
                 └─ PRD 체크박스 업데이트
```

각 세션은 부모 대화와 완전히 격리됩니다. 완료 마커, provider, workspace, sessionId 4중 검증을 통과해야만 작업이 완료로 처리됩니다.

## 검증 기록

2026-09-11, Genspark Claw Mac Local Computer (OpenClaw 2026.3.13)에서 라이브 검증 완료:
- 2개 작업 순차 실행, 총 25초
- 자동화 테스트 26 pass (엔진), 112 pass (upstream)

## 요구사항

- Genspark Claw Mac 앱 (Local Computer) 실행 중
- `ralphy-claw` 저장소 로컬 설치 (`bun run setup` 완료)
- Genspark 계정 크레딧
