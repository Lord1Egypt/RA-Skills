# Genspark 로컬 런타임 연결

2026-09-11에 이 Mac의 Genspark Claw에 포함된 `openclaw` 패키지를 확인했다. `package.json`의 버전은 `2026.3.13`이다. 다음 내용은 해당 설치본의 문서와 코드에 근거한다. 다른 버전에서는 현재 도구 스키마를 우선한다.

## 확인한 구현

설치본 패키지 경로:

```text
/Users/kimhyejoo/Library/Application Support/Genspark Claw/bundled-resources/openclaw/node_modules/openclaw
```

이 경로 아래의 확인 지점:

- `docs/concepts/session-tool.md`: `sessions_spawn`이 격리된 세션을 만들고 `{status, runId, childSessionKey}`를 반환한다는 설명.
- `dist/reply-Bm8VrLQh.js:93096`: 호출마다 `agent:<agentId>:subagent:<새 UUID>` 세션 키 생성.
- 같은 파일 `:93252`, `:93296`: 새 자식에게 전달하는 작업 메시지와 Gateway 실행 요청. 이 실행 경로는 부모 transcript를 복사하지 않고 작업 및 시스템 지침·라우팅 정보를 전달한다.
- 같은 파일 `:93453`: 실제 `sessions_spawn` 입력 스키마. 이 버전에는 `context`와 `forkContext` 인자가 없다.
- 같은 파일 `:93530`: 네이티브 subagent에는 부모 workspace를 전달한다. 스키마의 `cwd`는 이 버전의 ACP 분기에서만 사용된다.
- 같은 파일 `:93566`: `sessions_yield`의 입력은 선택적 `message` 문자열. 실행 문맥에 `onYield`가 없으면 `Yield not supported in this context` 오류를 반환한다.
- 같은 파일 `:94195` 및 `docs/tools/subagents.md`: `subagents`로 현재 세션의 자식 작업을 조회·중단할 수 있다. 실제 호출 인자는 현재 도구 스키마로 확인한다.

이것은 새 작업자의 대화 이력에 대한 근거다. 파일 시스템, 프로젝트 지침, 모델 설정, 인증까지 별개라는 의미는 아니다. 이 코드 확인과 앱에서의 실제 실행 검증을 구분한다.

## 한 번의 작업 실행

다음은 **도구 호출 인자 예시**이며 터미널 명령이 아니다. `task`와 `label`을 실제 작업 내용으로 바꾼다.

```json
{
  "runtime": "subagent",
  "mode": "run",
  "thread": false,
  "cleanup": "keep",
  "runTimeoutSeconds": 600,
  "label": "ralph-실행ID-반복번호-작업ID",
  "task": "대상 프로젝트의 절대 경로, 작업 하나의 요구사항과 완료 조건, 관련 지침, 반환할 결과를 전달한다."
}
```

- `runtime: subagent`로 Genspark의 네이티브 작업자를 사용한다. `acp`는 이 연결에서 사용하지 않는다.
- `agentId`와 `model`은 기존 Genspark 설정을 이용하도록 생략한다. 사용자 모델 지정이 있으면 지원되는 방식으로 적용한다. 실제 사용 모델을 확인할 수 있으면 결과에 기록한다.
- 매 반복 및 재시도마다 `sessions_spawn`을 새로 호출한다. 이전 `childSessionKey`에 `sessions_send`로 다음 작업을 보내면 새 컨텍스트 반복이 되지 않는다.
- 이 설치본에 `context: isolated` 또는 `forkContext`를 전달하지 않는다. 최신 웹 문서에 나오는 옵션을 구버전에 추가하지 않는다.
- 자식에게 프로젝트의 절대 경로를 명시하고 모든 파일·검사 작업에서 그 경로를 사용하도록 한다. 네이티브 실행의 `cwd` 인자에 기대지 않는다. 부모가 선택한 workspace와 대상 프로젝트가 다르면 먼저 파일 접근 가능 여부를 확인한다.
- 자식은 지정된 작업만 수행한다. PRD, `.ralph-claw/` 제어 상태 갱신과 다음 반복 생성은 부모가 맡는다. 자식이 스킬을 다시 실행하거나 추가 작업자를 만들지 않도록 한다.

## 완료 대기와 이어가기

1. `sessions_spawn` 응답이 `accepted`인지 확인한다. `runId`와 `childSessionKey`를 저장하고 `waiting_child`로 체크포인트를 남긴다. 수락은 작업 완료가 아니다.
2. `sessions_yield`를 호출하여 현재 부모 턴을 양보한다. 선택적 `message`에는 기다리는 작업을 짧게 설명한다. 대기 목적으로 shell sleep이나 상태 조회 반복을 만들지 않는다.
3. 이 런타임은 완료 결과를 부모에게 push한다. 부모가 다시 실행되면 `state.json`을 읽고, 이벤트의 실행 ID 또는 자식 세션 키가 기록된 `active_child`와 일치하는지 확인한다. 다른 작업의 이벤트나 이미 처리한 이벤트로 다음 반복을 시작하지 않는다.
4. 실제 결과와 필수 검사를 확인한 다음 PRD와 상태를 갱신한다. 한도와 STOP 조건을 확인하고, 남은 작업이 있으면 **다음 자식을 생성한 뒤 다시 yield**한다. 개별 자식의 완료를 전체 루프 완료로 해석하지 않는다.
5. 필요한 경우 종료된 자식에 대해 `sessions_history`를 한 번 조회하여 실행과 검증 근거를 확인한다. 이 조회는 대기용 polling이 아니다. 조회 권한이나 로그 길이 제한으로 확인할 수 없는 부분은 미확인으로 남긴다.

`sessions_yield`가 오류를 반환하면 해당 오류와 실행 ID를 기록한다. 자식이 실행 중일 수 있으므로 같은 작업을 다시 spawn하거나 부모가 대신 수행하지 않는다. 이 경우 자동 대기·재개가 검증되지 않았다고 보고하고, 사용자의 재개 요청 때 기존 작업의 종료 상태부터 확인한다. 자동 완료 이벤트가 먼저 도착하면 기록된 실행 ID에 대해 정상 완료 절차로 처리할 수 있다.

취소 요청에서는 노출된 `subagents` 도구의 스키마와 반환된 ID를 사용한다. 이 버전 문서는 `/subagents kill <id>`와 `/stop`을 설명한다. 최신 문서의 `cancel` 동작을 확인 없이 전달하지 않는다.

## 이 설치본의 실제 검증 결과

2026-09-11 18:08–18:10 KST에 서로 다른 자식 세션 두 개가 순차 실행되었고, 각 자식 완료 후 `sessions_yield`를 통해 부모가 사용자 추가 입력 없이 재개되었다. 두 자식 모두 `genspark-llm-proxy/claude-sonnet-4-6`로 실행되었다. 보존된 전체 자식 transcript는 각각 해당 작업의 `[Subagent Task]` 메시지로 시작했으며 부모 대화의 복사는 관찰되지 않았다. 최종 파일은 `hello\nralph\n` 12바이트로 일치했다.

다만 부모가 최종 상태의 임시 파일을 쓴 직후 Genspark가 무료 플랜 크레딧의 API / LLM proxy 사용을 거부하여, 원자적 교체와 전체 보고를 마치지 못했다. 이 오류는 해당 실행의 관찰 사실이며 모든 계정의 요금·사용 가능 여부를 의미하지 않는다. 모델 호출이 거부되어도 이미 성공한 작업을 다시 실행하지 말고 저장된 실행 결과를 확인한다.

상태 저장은 스킬에 포함된 `scripts/save-state.py`로 한 번의 명령 호출 안에서 마친다. 중단된 상태의 수동 복구와 제공자 오류의 해결을 구분해서 보고한다.
