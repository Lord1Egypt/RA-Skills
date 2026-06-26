# ACP Harness Integration Test

## 목표
OpenClaw의 sessions_spawn을 사용하여 실제 Codex/Claude Code 호출

## 현재 설정
```json
{
  "acp": {
    "defaultAgent": "codex",
    "allowedAgents": ["codex", "claude-code", "gemini"]
  }
}
```

## 테스트 계획

### Test 1: Simple Task (Codex)
- 프로젝트: Hello World CLI
- 예상 시간: 30초
- 목적: ACP 기본 작동 확인

### Test 2: Medium Task (Codex)
- 프로젝트: CVE Scanner 수정
- 예상 시간: 2분
- 목적: 실제 수정 작업 확인

### Test 3: Complex Task (Claude Code)
- 프로젝트: Security Dashboard
- 예상 시간: 10분
- 목적: 복잡한 프로젝트 생성 능력 확인

## 호출 방식

### Python (subprocess)
```python
import subprocess
result = subprocess.run([
    'openclaw', 'agent', 'spawn',
    '--agent', 'codex',
    '--task', 'Create a simple hello world CLI in Python',
    '--cwd', '/tmp/builder-projects'
], capture_output=True, text=True)
```

### 또는 직접 Tool 호출
```
sessions_spawn(
    agentId="codex",
    mode="run",
    task="Create a simple hello world CLI",
    cwd="/tmp/builder-projects",
    runTimeoutSeconds=60
)
```

## 제약사항
- 현재 세션에서 직접 sessions_spawn 호출 가능 여부 확인 필요
- 가능하다면 즉시 테스트 진행
- 불가능하다면 Python subprocess 방식 사용
