# Builder Agent v4 - Upgrade Plan

## 🎯 목표

기존 Builder Agent를 고도화하여 ChatDev 의존성을 제거하고, 메모리 시스템을 통합하며, Discovery 자동화를 구현한다.

## 📊 개선 현황

### ✅ 완료된 작업

1. **스킬 설치** (5개)
   - agent-browser (⭐404) - Discovery 자동화
   - self-improving (⭐72) - 자기 성찰/학습
   - elite-longterm-memory (⭐101) - 장기 기억
   - byterover (⭐76) - 컨텍스트 수집
   - memory-manager (⭐56) - 메모리 관리

2. **설계 문서 작성**
   - memory-integration.md - 메모리 시스템 통합 설계
   - acp-integration.md - ACP 하네스 통합 설계
   - discovery-integration.md - Discovery Layer 설계

### 🔄 진행 중인 작업

3. **구현 필요**
   - [ ] 메모리 시스템 초기화
   - [ ] ACP 하네스 연동 코드
   - [ ] Discovery 크롤러 구현
   - [ ] Notion 큐 연동
   - [ ] 자가 수정 루프

## 🏗️ 새로운 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                    BUILDER AGENT v4                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              DISCOVERY LAYER (agent-browser)             │  │
│  │                                                            │  │
│  │  GitHub Trending ──┐                                       │  │
│  │  CVE Database    ──┼──→ Notion Queue                      │  │
│  │  Security News   ──┘                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              ORCHESTRATION LAYER (ACP 하네스)             │  │
│  │                                                            │  │
│  │  Simple (직접) ──┐                                         │  │
│  │  Medium (Codex)──┼──→ 개발 실행                           │  │
│  │  Complex (Claude)┘                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              MEMORY LAYER (4개 스킬 통합)                 │  │
│  │                                                            │  │
│  │  self-improving ──→ 실패 학습                             │  │
│  │  elite-memory   ──→ 성공 패턴                             │  │
│  │  byterover      ──→ 컨텍스트                              │  │
│  │  memory-manager ──→ 압축/검색                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              PUBLISHING LAYER (GitHub)                    │  │
│  │                                                            │  │
│  │  저장소 생성 → README → 테스트 → 릴리즈                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 실행 로드맵

### Week 1: 메모리 시스템 구축
- Day 1-2: self-improving 초기화
- Day 3-4: elite-longterm-memory 설정
- Day 5-6: byterover 통합
- Day 7: memory-manager 자동화

### Week 2: Discovery 자동화
- Day 1-3: agent-browser 크롤러 구현
- Day 4-5: Notion 큐 연동
- Day 6-7: 스케줄러 등록

### Week 3: ACP 하네스 연동
- Day 1-3: Codex 연동
- Day 4-5: Claude Code 연동
- Day 6-7: 자가 수정 루프

### Week 4: 통합 테스트
- Day 1-3: End-to-End 테스트
- Day 4-5: 성능 최적화
- Day 6-7: 문서화 및 배포

## 📋 다음 단계

1. **self-improving 초기화**
   ```bash
   mkdir -p ~/self-improving/{projects,domains,archive}
   touch ~/self-improving/{memory.md,index.md,corrections.md,reflections.md}
   ```

2. **elite-longterm-memory 설정**
   ```bash
   mkdir -p ~/.openclaw/workspace/memory/{daily,topics,vectors}
   touch ~/.openclaw/workspace/memory/MEMORY.md
   ```

3. **첫 번째 테스트 프로젝트 실행**
   - Notion에 테스트 아이디어 등록
   - ACP 하네스로 개발 실행
   - 메모리에 결과 저장

---

**상태**: 설계 완료, 구현 대기
**예상 완료**: 4주
**책임자**: 부긔 (OpenClaw Agent)
