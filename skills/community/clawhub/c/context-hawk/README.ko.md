# 🦅 Context-Hawk

> **AI 컨텍스트 메모리 가디언** — 추적을 잃는 것을 멈추고, 중요한 것을 기억하기 시작하세요.

*어떤 AI 에이전트에게도 session을 넘어, 주제를 넘어, 시간을超越하여 실제로 작동하는 기억을 제공하세요.*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-context--hawk-blue)](https://clawhub.com)

**English** | [中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Italiano](README.it.md) | [Русский](README.ru.md) | [Português (Brasil)](README.pt-BR.md)

---

## 무엇을 하나요?

대부분의 AI 에이전트는 **건망증**으로 고통받습니다 — 새로운 session이 시작될 때마다零에서 시작합니다. Context-Hawk는 생산グレード 메모리 관리 시스템으로 이것을 해결합니다. 중요한 것을 자동으로 캡처하고, 노이즈를 희석시키며, 올바른 시간에 올바른 기억을思い出します.

**Context-Hawk 없이:**
> "이미 말했잖아요 — 간결한 답장을 좋아한다고!"
> (다음 session, 에이전트가 다시 잊어버림)

**Context-Hawk 사용 시:**
> (session 1에서 자동으로 커뮤니케이션 선호도를 적용)
> ✅ 매번 간결하고 직접적인 응답을 제공

---

## ❌ Context-Hawk 없음 vs ✅ Context-Hawk 있음

| 시나리오 | ❌ Context-Hawk 없음 | ✅ Context-Hawk 있음 |
|----------|------------------------|---------------------|
| **새 session 시작** |空白 — 당신에 대해 아무것도 모름 | ✅ 관련 기억을 자동으로 주입 |
| **사용자가 선호도를 반복** | "전에 말했잖아..." | 첫날부터 기억 |
| **며칠 동안 장기 작업 실행** | 재시작 = 처음부터 | Task State 지속화, `hawk resume`으로 완벽 연결 |
| **컨텍스트가 커짐** | Token 비용 급등, 성능 저하 | 5가지 압축 전략으로 가벼움 유지 |
| **중복 정보** | 같은 사실이 10번 저장됨 | SimHash 중복 제거 — 1번만 저장 |
| **기억 리콜** | 모두 유사, 반복 주입 | MMR 다양한 리콜 — 반복 없음 |
| **기억 관리** | 모든 것이 영구적으로 누적 | 4계층衰减 — 노이즈는 사라지고, 시그널은 유지 |
| **자기 개선** | 같은 실수를 반복 | importance + access_count 추적 → 스마트 승격 |
| **멀티 에이전트 팀** | 각 에이전트가 처음부터 시작, 공유 컨텍스트 없음 | 공유 기억 (LanceDB 통해) — 모든 에이전트가 서로 학습 |

---

## 😰 문제점 & 해결책

| 문제점 | 영향 | Context-Hawk 해결책 |
|------|------|----------------------|
| **AI가 각 session마다 기억을 잃음** | 사용자가 같은 말을 반복해서 해야 함 | 4계층 기억衰减 — 중요한 콘텐츠가 자동으로 유지 |
| **장기 작업이 재시작 후丢失** | 작업이 낭비되고, 컨텍스트가 완전히 사라짐 | `hawk resume` — 작업 상태가 재시작을 넘어 지속 |
| **컨텍스트膨胀** | Token 비용이 급등하고, 응답이 느려짐 | 5가지 주입 전략 + 5가지 압축 전략 |
| **기억 노이즈** | 중요한 정보가 채팅 이력에 묻힘 | AI 중요도 점수화 — 저가치 콘텐츠를 자동으로 폐기 |
| **선호도가 잊혀짐** | 사용자가 매번 규칙을 다시 설명해야 함 | 중요도 ≥ 0.9 = 영구 기억 |

**핵심 가치:** Context-Hawk는 AI 에이전트에 실제로 작동하는 기억을 제공합니다 — 모든 것을 저장하는 것이 아니라, 중요한 것을 지능적으로 유지하고 중요하지 않은 것은 잊어버립니다.

---

## 🎯 5가지 핵심 문제를 해결

**문제 1: 세션 컨텍스트 창 제한**
컨텍스트에는 토큰 제한이 있습니다(예: 32k). 긴 이력은 중요한 콘텐츠를 밀어냅니다.
→ Context-Hawk는古い 콘텐츠를 압축/보관하고 가장 관련된 기억만 주입합니다.

**문제 2: 세션을またいだ기억 상실**
세션이 종료되면 컨텍스트가 사라집니다. 다음 대화는零から始まります。
→ 기억은 영구적으로 저장됩니다. `hawk recall`은 다음 세션에서 관련된 기억을 검색합니다.

**문제 3: 여러 에이전트가 서로 정보를 공유하지 않음**
Agent A는 Agent B의 컨텍스트를 모릅니다. 한 에이전트가 내린 결정은 다른 에이전트에게 보이지 않습니다.
→ 공유 LanceDB 기억소( hawk-bridge와 함께 사용): 모든 에이전트가 같은 기억을 읽고 씁니다. 사일로 없음.

**문제 4: LLM에送信前 컨텍스트가 이미膨胀함**
최적화 없는 리콜 = 크고 반복적인 컨텍스트.
→ 압축 + SimHash 중복 제거 + MMR 리콜 후: LLM에送信される 컨텍스트는**대폭缩小**되어 토큰과 비용을 절약합니다.

**문제 5: 기억이 스스로管理하지 않음**
관리 메커니즘 없음: 모든 메시지가 쌓여서 컨텍스트가 overflow될 때까지.
→ 자동 추출 → 중요도 점수화 → 4계층衰减. 중요하지 않음 → 삭제. 중요함 → 장기 기억으로 승격.

---

## ✨ 12가지 핵심 기능

| # | 기능 | 설명 |
|---|---------|-------|
| 1 | **작업 상태 지속성** | `hawk resume` — 작업 상태 보존, 재시작 후 계속 |
| 2 | **4계층 메모리** | Working → Short → Long → Archive, Weibull衰减 적용 |
| 3 | **구조화된 JSON** | 중요도 점수(0-10), 카테고리, 티어, L0/L1/L2 레이어 |
| 4 | **AI 중요도 점수화** | 기억에 자동 점수 부여, 저가치 콘텐츠 폐기 |
| 5 | **5가지 주입 전략** | A(높은 중요도) / B(작업 관련) / C(최근) / D(Top5) / E(전체) |
| 6 | **5가지 압축 전략** | summarize / extract / delete / promote / archive |
| 7 | **자기 성찰** | 작업 명확성, 누락된 정보, 루프 감지 확인 |
| 8 | **LanceDB 벡터 검색** | 선택 사항 — 하이브리드 vector + BM25 검색 |
| 9 | **순수 메모리 폴백** | LanceDB 없이 동작, JSONL 파일 지속성 |
| 10 | **자동 중복 제거** | SimHash 중복 제거, 중복 기억을 제거 |
| 11 | **MMR 리콜** | 최대 한계 관련성 — 다양한 리콜, 반복 없음 |
| 12 | **6카테고리 추출** | LLM 기반 분류 추출: 사실 / 선호도 / 결정 / 엔티티 / 작업 / 기타 |

---

## 🚀 빠른 설치

```bash
# 원라인 설치 (권장)
bash <(curl -fsSL https://raw.githubusercontent.com/relunctance/context-hawk/master/install.sh)

# 또는 pip로 직접
pip install context-hawk

# 전체 기능 설치 (sentence-transformers 포함)
pip install "context-hawk[all]"
```

---

## 🏗️ 아키텍처

```
┌──────────────────────────────────────────────────────────────┐
│                      Context-Hawk                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Working Memory  ←── 현재 session (최근 5-10턴)           │
│       ↓ Weibull衰减                                         │
│  Short-term      ←── 24시간 콘텐츠, 요약됨               │
│       ↓ access_count ≥ 10 + 중요도 ≥ 0.7                │
│  Long-term       ←── 영구 지식, 벡터 인덱싱               │
│       ↓ >90일 또는 decay_score < 0.15                     │
│  Archive          ←── 이력, 요청 시 로드                   │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  Task State Memory  ←── 재시작 간 지속 (핵심!)            │
│  - 현재 작업 / 다음 단계 / 진행률 / 출력물                  │
├──────────────────────────────────────────────────────────────┤
│  주입 엔진       ←── 전략 A/B/C/D/E가 리콜 결정           │
│  자기 성찰        ←── 매 답변 시 컨텍스트 확인              │
│  자동 트리거      ←── 매 10턴 (설정 가능)                │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 작업 상태 메모리 (가장 가치 있는 기능)

재시작, 정전 또는 session 전환 후에도 Context-Hawk는 정확한 중단 지점에서 재개합니다.

```json
// memory/.hawk/task_state.jsonl
{
  "task_id": "task_20260329_001",
  "description": "API 문서 완료",
  "status": "in_progress",
  "progress": 65,
  "next_steps": ["아키텍처 템플릿 검토", "사용자에게 보고"],
  "outputs": ["SKILL.md", "constitution.md"],
  "constraints": ["커버율 98% 필수", "API는 버전化管理"],
  "resumed_count": 3
}
```

```bash
hawk task "문서 완료"        # 작업 생성
hawk task --step 1 done  # 단계 완료 표시
hawk resume               # 재시작 후 재개 ← 핵심!
```

---

## 🧠 구조화된 메모리

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "완전한 원본 콘텐츠",
  "summary": "한 줄 요약",
  "importance": 0.85,
  "tier": "working|short|long|archive",
  "created_at": "2026-03-29T00:00:00+08:00",
  "access_count": 3,
  "decay_score": 0.92
}
```

### 중요도 점수화

| 점수 | 유형 | 행동 |
|-------|------|------|
| 0.9-1.0 | 결정/규칙/오류 | 영구, 가장 느린衰减 |
| 0.7-0.9 | 작업/선호도/지식 | 장기 기억 |
| 0.4-0.7 | 대화/논의 | 단기, archive로衰减 |
| 0.0-0.4 | 채팅/인사 | **폐기, 절대 저장 안 함** |

---

## 🎯 5가지 컨텍스트 주입 전략

| 전략 | 트리거 | 절약 |
|------|---------|------|
| **A: 높은 중요도** | `중요도 ≥ 0.7` | 60-70% |
| **B: 작업 관련** | scope 일치 | 30-40% ← 기본값 |
| **C: 최근** | 마지막 10턴 | 50% |
| **D: Top5 리콜** | `access_count` Top 5 | 70% |
| **E: 전체** | 필터 없음 | 100% |

---

## 🗜️ 5가지 압축 전략

`summarize` · `extract` · `delete` · `promote` · `archive`

---

## 🔔 4단계 알림 시스템

| 레벨 | 임계값 | 행동 |
|-------|---------|------|
| ✅ Normal | < 60% | 자동 |
| 🟡 Watch | 60-79% | 압축 제안 |
| 🔴 Critical | 80-94% | 자동 쓰기 일시 중지, 강제 제안 |
| 🚨 Danger | ≥ 95% | 쓰기 차단, 압축 필수 |

---

## 🚀 빠른 시작

```bash
# LanceDB 플러그인 설치 (권장)
openclaw plugins install memory-lancedb-pro@beta

# 스킬 활성화
openclaw skills install ./context-hawk.skill

# 초기화
hawk init

# 핵심 명령
hawk task "내 작업"    # 작업 생성
hawk resume             # 마지막 작업 재개 ← 가장 중요
hawk status            # 컨텍스트 사용량 확인
hawk compress          # 메모리 압축
hawk strategy B        # 작업 관련 모드로 전환
hawk introspect         # 자기 성찰 보고서
```

---

## 자동 트리거: 매 N턴

매 **10턴** (기본값, 설정 가능), Context-Hawk가 자동으로:

1. 컨텍스트 수위 확인
2. 기억 중요도 평가
3. 사용자에게 상태 보고
4. 필요 시 압축 제안

```bash
# 설정 (memory/.hawk/config.json)
{
  "auto_check_rounds": 10,          # 매 N턴 확인
  "keep_recent": 5,                 # 마지막 N턴 보존
  "auto_compress_threshold": 70      # 70% 초과 시 압축
}
```

---

## 파일 구조

```
context-hawk/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk               # Python CLI 도구
└── references/
    ├── memory-system.md           # 4계층 아키텍처
    ├── structured-memory.md      # 메모리 형식 및 중요도
    ├── task-state.md           # 작업 상태 지속성
    ├── injection-strategies.md  # 5가지 주입 전략
    ├── compression-strategies.md # 5가지 압축 전략
    ├── alerting.md             # 알림 시스템
    ├── self-introspection.md   # 자기 성찰
    ├── lancedb-integration.md  # LanceDB 통합
    └── cli.md                  # CLI 참조
```

---

## 🔌 기술 사양

| | |
|---|---|
| **지속성** | JSONL 로컬 파일, 데이터베이스 불필요 |
| **벡터 검색** | LanceDB (선택) + sentence-transformers 로컬 벡터, 파일로 자동 폴백 |
| **검색** | BM25 + ANN 벡터 검색 + RRF 퓨전 |
| **Embedding 제공자** | Ollama / sentence-transformers / Jina AI / Minimax / OpenAI |
| **Cross-Agent** | 범용, 비지니스 로직 없음, 모든 AI 에이전트와 동작 |
| **제로 설정** | 스마트 기본값, 즉시 사용 가능 (BM25-only 모드) |
| **Python** | 3.12+ |

---

## 라이선스

MIT — 무료로 사용, 수정, 배포 가능.
