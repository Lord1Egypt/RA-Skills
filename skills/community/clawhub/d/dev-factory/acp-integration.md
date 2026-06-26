# Builder Agent ACP Integration

## 개요

ChatDev 2.0 의존성을 제거하고 OpenClaw의 ACP(Async Control Protocol) 하네스를 사용하여 Codex, Claude Code를 직접 호출한다.

## 기존 vs 새로운 방식

### 기존 (ChatDev 2.0)
```
Builder Agent → ChatDev 서버 (localhost:6400) → 7개 에이전트 협업
```
**문제점:**
- 별도 서버 실행 필요
- 느린 응답 (7개 에이전트 순차 실행)
- GLM-5만 지원

### 새로운 (ACP 하네스)
```
Builder Agent → ACP 하네스 → Codex/Claude Code 직접 실행
```
**장점:**
- 서버 불필요
- 빠른 응답
- 다중 LLM 지원 (Codex, Claude, Gemini)

## 복잡도 기반 라우팅

### Level 1: Simple (직접 실행)
- **조건**: 단일 파일, < 100줄
- **도구**: `edit` 또는 `write`
- **시간**: < 30초
- **예시**: 설정 파일, 간단한 스크립트

### Level 2: Medium (ACP - Codex)
- **조건**: 다중 파일, 100-500줄
- **도구**: `sessions_spawn` (agentId: codex)
- **시간**: 1-3분
- **예시**: CLI 도구, 간단한 API

### Level 3: Complex (ACP - Claude Code)
- **조건**: 복잡한 아키텍처, > 500줄
- **도구**: `sessions_spawn` (agentId: claude-code)
- **시간**: 5-15분
- **예시**: 웹 앱, 분산 시스템

## ACP 하네스 워크플로우

### 1. 복잡도 분석
```python
def analyze_complexity(project_idea: dict) -> str:
    """프로젝트 아이디어 분석 → 복잡도 레벨 반환"""
    
    # 키워드 기반 분석
    if any(kw in project_idea['title'].lower() for kw in ['scanner', 'cli', 'tool']):
        return 'medium'
    elif any(kw in project_idea['title'].lower() for kw in ['web', 'api', 'dashboard']):
        return 'complex'
    else:
        return 'simple'
```

### 2. ACP 실행 (sessions_spawn)
```python
async def develop_via_acp(project_idea: dict, complexity: str):
    """ACP 하네스로 개발 실행"""
    
    if complexity == 'simple':
        # 직접 실행
        return await develop_simple(project_idea)
    
    elif complexity == 'medium':
        # Codex 호출
        result = await sessions_spawn(
            agentId="codex",
            mode="run",
            task=f"""
            Develop: {project_idea['title']}
            
            Requirements:
            {project_idea['description']}
            
            Tech Stack: Python, pytest
            Output: Complete working project with tests
            """,
            cwd="/tmp/builder-projects",
            runTimeoutSeconds=300
        )
        
    elif complexity == 'complex':
        # Claude Code 호출
        result = await sessions_spawn(
            agentId="claude-code",
            mode="run",
            task=f"""
            Build: {project_idea['title']}
            
            Full Requirements:
            {project_idea['description']}
            
            Architecture: Modular, testable, documented
            Output: Production-ready codebase
            """,
            cwd="/tmp/builder-projects",
            runTimeoutSeconds=900
        )
    
    return result
```

### 3. 자가 수정 루프
```python
async def develop_with_retry(project: dict, max_retries: int = 3):
    """자가 수정 루프"""
    
    for attempt in range(max_retries):
        # 1. 개발 실행
        result = await develop_via_acp(project, project['complexity'])
        
        # 2. 테스트 실행
        test_result = await run_tests(result['project_path'])
        
        if test_result['success']:
            # 성공 → 메모리에 저장
            await save_success_pattern(project, result)
            return {'success': True, 'project': result}
        
        else:
            # 실패 → 원인 분석
            error_analysis = analyze_error(test_result['errors'])
            
            # self-improving에 로깅
            log_failure(project, error_analysis)
            
            # 다음 시도를 위한 컨텍스트 준비
            project['context'] = error_analysis['fix_suggestions']
    
    # 최대 재시도 초과
    return {'success': False, 'errors': test_result['errors']}
```

## ACP 하네스 설정

### OpenClaw 설정 (openclaw.json)
```json
{
  "acp": {
    "allowedAgents": ["codex", "claude-code", "gemini"],
    "defaultAgent": "codex",
    "timeouts": {
      "simple": 60,
      "medium": 300,
      "complex": 900
    }
  }
}
```

### 환경 변수 (.env)
```bash
# ACP 하네스
ACP_DEFAULT_AGENT=codex
ACP_TIMEOUT_SIMPLE=60
ACP_TIMEOUT_MEDIUM=300
ACP_TIMEOUT_COMPLEX=900

# Codex
CODEX_API_KEY=your_codex_key

# Claude Code
ANTHROPIC_API_KEY=your_claude_key
```

## Codex/Claude Code 프롬프트 템플릿

### Codex (Medium 복잡도)
```
You are developing: {project_name}

## Requirements
{requirements}

## Tech Stack
- Python 3.11+
- pytest for testing
- GitHub-ready structure

## Output Structure
```
{project_name}/
├── README.md
├── requirements.txt
├── setup.py
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── utils.py
└── tests/
    ├── __init__.py
    └── test_main.py
```

## Success Criteria
- All tests pass
- Code is documented
- README includes usage examples

## Previous Failures (learn from these)
{memory_context}
```

### Claude Code (Complex 복잡도)
```
Build a production-ready: {project_name}

## Full Specification
{full_spec}

## Architecture Requirements
- Modular design
- Comprehensive error handling
- Full test coverage (>80%)
- API documentation
- CI/CD ready

## Tech Stack
- Python 3.11+ (backend)
- FastAPI (if web API needed)
- pytest + coverage
- Docker (optional)

## Memory Context
Similar successful projects:
{elite_memory_patterns}

Previous mistakes to avoid:
{self_improving_corrections}

## Output
Complete codebase ready for GitHub publishing.
```

## 구현 체크리스트

- [ ] 복잡도 분석 로직 구현
- [ ] ACP 하네스 연동 (sessions_spawn)
- [ ] Codex 에이전트 설정
- [ ] Claude Code 에이전트 설정
- [ ] 자가 수정 루프 구현
- [ ] 프롬프트 템플릿 최적화
- [ ] 실패 로깅 (self-improving)
- [ ] 성공 패턴 저장 (elite-memory)
