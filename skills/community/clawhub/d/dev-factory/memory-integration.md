# Builder Agent Memory Integration

## 개요

Builder Agent에 4개 메모리 스킬을 통합하여 성공/실패 패턴을 학습하고 재사용한다.

## 통합 스킬

### 1. self-improving (자기 성찰)
- **용도**: 실패한 테스트 케이스, 사용자 교정 로깅
- **위치**: `~/self-improving/`
- **트리거**: 테스트 실패, 사용자 피드백

### 2. elite-longterm-memory (장기 기억)
- **용도**: 성공한 프로젝트 패턴, 아키텍처 결정 저장
- **위치**: `~/.openclaw/workspace/memory/`
- **트리거**: 프로젝트 완료, 성공적인 배포

### 3. byterover (컨텍스트 수집)
- **용도**: 프로젝트별 컨텍스트, 의존성 정보 저장
- **위치**: `~/.byterover/`
- **트리거**: 프로젝트 시작 전

### 4. memory-manager (메모리 관리)
- **용도**: 메모리 압축, 검색, 스냅샷
- **위치**: `~/.openclaw/workspace/memory/`
- **트리거**: 정기적 (매일)

## 워크플로우

```
프로젝트 시작
    ↓
byterover: 유사 프로젝트 컨텍스트 검색
    ↓
개발 실행 (ACP 하네스)
    ↓
테스트 실행
    ↓
┌─────────────────┬─────────────────┐
│   성공          │    실패         │
│                 │                 │
│ elite-memory:   │ self-improving: │
│ 패턴 저장       │ 원인 분석       │
│ 아키텍처 기록    │ 교정 로깅       │
└─────────────────┴─────────────────┘
    ↓
GitHub 배포
    ↓
memory-manager: 메모리 압축
```

## API 매핑

### 프로젝트 시작 전
```python
# 1. 유사 프로젝트 검색 (byterover)
brv search "security scanner"

# 2. 이전 실패 패턴 확인 (self-improving)
cat ~/self-improving/corrections.md | grep "scanner"

# 3. 성공 패턴 검색 (elite-memory)
memory_recall query="security scanner architecture"
```

### 프로젝트 완료 후
```python
# 1. 성공 패턴 저장 (elite-memory)
memory_store text="CVE scanner with async architecture" 
             category="pattern" 
             importance=0.9

# 2. 프로젝트 컨텍스트 저장 (byterover)
brv store "cve-scanner-v9" --context="async, pytest, github-api"

# 3. 배운 점 기록 (self-improving)
echo "CONTEXT: CVE Scanner\nREFLECTION: Async improved speed 3x\nLESSON: Use async for I/O heavy scanners" \
  >> ~/self-improving/reflections.md
```

## 설정

### 환경 변수 (.env)
```bash
# Self-Improving
SELF_IMPROVING_DIR=~/self-improving

# Elite Longterm Memory
MEMORY_DIR=~/.openclaw/workspace/memory
LANCEDB_DIR=~/.openclaw/workspace/memory/vectors

# ByteRover
BYTEROVER_DIR=~/.byterover

# Memory Manager
MEMORY_SNAPSHOT_INTERVAL=86400  # 24시간
```

## 파일 구조

```
~/.openclaw/workspace/
├── memory/
│   ├── MEMORY.md              # 큐레이션된 장기 기억
│   ├── daily/
│   │   └── 2026-03-08.md      # 일일 로그
│   ├── topics/
│   │   ├── security-scanner.md
│   │   └── automation-tools.md
│   └── vectors/               # LanceDB 벡터
│
~/self-improving/
├── memory.md                  # HOT: 항상 로드
├── corrections.md             # 교정 로그
├── reflections.md             # 성찰 로그
└── projects/
    └── builder-agent.md       # 프로젝트별 학습
```

## 구현 체크리스트

- [ ] self-improving 초기화 (`setup.md` 실행)
- [ ] elite-longterm-memory 벡터 DB 초기화
- [ ] byterover CLI 설치
- [ ] memory-manager 스냅샷 자동화
- [ ] 워크플로우에 메모리 호출 추가
- [ ] 테스트 실패 시 자동 로깅
- [ ] 프로젝트 완료 시 자동 저장
