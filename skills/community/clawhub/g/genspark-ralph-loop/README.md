# genspark-ralph-loop

Genspark Claw에서 PRD의 개발 작업을 하나씩 구현하고 검증하며 결과를 파일에 기록해 반복하거나 재개합니다.

## 언제 쓰나

- PRD(요구사항 문서)의 작업 목록을 순차 실행하고 싶을 때
- 실패 시 로그를 분석해 자동으로 수정·재시도하고 싶을 때
- 중단된 개발 작업을 이어서 재개하고 싶을 때

## 사용법

Genspark Claw 대화에서 다음처럼 요청합니다:

```
genspark-ralph-loop 스킬로 PRD 작업을 실행해줘.
대상 프로젝트: /내/프로젝트/경로
PRD: PRD.md
최대 5회 반복
```

PRD 형식 예시:

```markdown
# Tasks

- [ ] TASK-001: 로그인 폼에서 빈 이메일 제출을 막고 오류 문구를 표시한다.
- [ ] TASK-002: 메인 페이지에 헤더 컴포넌트를 추가한다.
```

## 동작 방식

1. PRD에서 미완료 작업 하나 선택
2. `sessions_spawn`으로 새 Claw 세션 생성 (가능한 경우)
3. 작업 구현 및 검증
4. 성공 시 PRD 체크박스 `[ ]` → `[x]` 업데이트
5. 실패 시 실패 로그 전달 후 재시도
6. 다음 작업으로 이동

## 상태 파일

프로젝트의 `.ralph-claw/` 디렉터리에 상태를 기록합니다:
- `state.json`: 현재 진행 상태, 시도 수, 한도
- `progress.md`: 작업별 실행 기록 및 검증 결과

## 요구사항

- Genspark Claw Mac 앱 (Local Computer)
- 앱이 실행 중이어야 함
- Genspark 계정 크레딧
