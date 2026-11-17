---
name: genspark-ralphy-cli
description: Genspark Claw Local Computer에서 원본 Ralphy CLI를 Genspark 실행 엔진으로 호출하여 PRD 개발 작업을 순차 처리한다. 원본 Ralphy 실행, ralphy-claw 실행, 이 스킬을 지정한 Ralph loop 요청에 사용한다.
---

# 원본 Ralphy를 Genspark Claw로 실행

이 스킬의 `scripts/run.sh`는 설치된 ralphy-claw 저장소의 원본 Ralphy CLI 실행본을 호출한다. Ralphy가 작업을 선택하고, 매 작업마다 새 Claw 세션을 만들고, 완료 후 PRD를 체크한다.

## 실행

대상 프로젝트와 PRD를 사용자 요청 또는 현재 작업 맥락에서 정한다. 개발 요구사항이 없으면 임의로 만들지 말고 필요한 내용만 질문한다. 프로젝트의 지침과 PRD를 확인한 뒤 프로젝트 디렉터리에서 다음 명령을 실행한다. 경로는 실제 절대 경로로 바꾸고 셸 인자는 안전하게 인용한다.

```sh
"/이/스킬의/절대경로/scripts/run.sh" --prd PRD.md --max-iterations 3 --no-commit
```

사용자가 정한 반복 한도를 우선한다. 정하지 않았다면 우선 최대 3개 작업으로 시작한다. 커밋을 요청한 경우에는 `--no-commit`을 생략할 수 있다. 테스트와 lint는 기본 활성화 상태로 둔다. 작업별 제한 시간은 `RALPHY_CLAW_TIMEOUT_SECONDS`이며 기본 600초다.

- exec가 실행 중인 프로세스 ID를 반환하면 해당 프로세스를 계속 poll하여 종료 코드와 요약을 확인한다. 작업 사이에 사용자의 추가 지시를 기다릴 필요는 없다. 실행기를 다시 호출하면 중복 작업이 생길 수 있으므로 기존 프로세스의 상태부터 확인한다.
- 이 스킬의 부모는 Ralphy를 한 번 실행하고 결과를 기다린다. 부모가 별도로 `sessions_spawn`을 호출하거나 PRD를 완료 처리하지 않는다.
- 실패하면 미완료 PRD와 프로젝트의 `.ralphy/claw/runs/*.json`을 확인한다. 크레딧·인증 오류나 완료 불확실 상태에서 반복 호출하지 않는다. `cancellation: unconfirmed`가 있으면 해당 세션이 끝났는지 확인한 뒤 재개한다.
- 중단 요청은 실행 중인 Ralphy 프로세스에 SIGINT/SIGTERM을 전달한다. 실행기는 자신이 만든 세션의 중단을 요청한다. 강제 종료나 Mac 종료 후 자동 재개는 지원하지 않는다.
- 최종 보고는 실제 완료/실패 수, 실행 종료 코드, 검증 결과를 근거로 작성한다. 실패한 작업의 코드를 부모가 대신 수정하고 Ralphy가 성공했다고 보고하지 않는다.

이 연결은 Mac 앱의 Local Computer 및 번들 OpenClaw 2026.3.13을 대상으로 검증했다. 앱이 실행 중이어야 한다. Genspark 모델 호출에는 계정의 사용 권한과 크레딧이 적용된다. 별도 Claude Code/Codex 실행으로 자동 전환하지 않는다. 병렬 실행은 지원하지 않는다.

Claw 런타임은 새 프로젝트에 `AGENTS.md`, `SOUL.md`, `TOOLS.md` 같은 초기 파일과 `.openclaw/`를 생성할 수 있다. 기존 프로젝트 지침을 덮어쓰거나 생성 파일을 임의로 삭제하지 않는다.
