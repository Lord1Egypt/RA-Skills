#!/usr/bin/env python3
"""
Four-Dimensional Deep Reading - Parallel Analysis Module
Version: 1.7.2

This module provides parallel execution of 4 persona analyses using OpenClaw sessions_spawn.
Supports multi-language output (EN/ZH/JA/KO/FR/DE/ES/PT/RU).
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional

# Supported languages
SUPPORTED_LANGUAGES = ['en', 'zh', 'ja', 'ko', 'fr', 'de', 'es', 'pt', 'ru']
FALLBACK_LANG = 'en'

# Persona definitions with multi-language support
PERSONAS = {
    "axiom_analyst": {
        "name": {
            "en": "Axiom Analyst",
            "zh": "第一性原理师",
            "ja": "公理分析者",
            "ko": "공리 분석가"
        },
        "task": {
            "en": "Axiomatic decomposition",
            "zh": "第一性原理分解",
            "ja": "公理的分解",
            "ko": "공리적 분해"
        }
    },
    "lms_architect": {
        "name": {
            "en": "L-M-S Architect",
            "zh": "结构化笔记官",
            "ja": "構造化ノート作成者",
            "ko": "구조화 노트 작성자"
        },
        "task": {
            "en": "Structured notes",
            "zh": "结构化笔记",
            "ja": "構造化ノート",
            "ko": "구조화 노트"
        }
    },
    "black_swan_hunter": {
        "name": {
            "en": "Black Swan Hunter",
            "zh": "黑天鹅猎手",
            "ja": "ブラックスワン探索者",
            "ko": "블랙 스왐 탐색자"
        },
        "task": {
            "en": "Black swan & boundary conditions",
            "zh": "黑天鹅与边界条件",
            "ja": "ブラックスワンと境界条件",
            "ko": "블랙 스왐과 경계 조건"
        }
    },
    "random_variable_x": {
        "name": {
            "en": "Random Variable X",
            "zh": "随机变量 X",
            "ja": "確率変数 X",
            "ko": "확률 변수 X"
        },
        "task": {
            "en": "Random identity perspective",
            "zh": "随机身份视角",
            "ja": "ランダムアイデンティティ視点",
            "ko": "무작위 정체성 관점"
        }
    }
}

# Persona instructions (multi-language templates)
PERSONA_INSTRUCTIONS = {
    "en": {
        "axiom_analyst": """You are the 'Axiom Analyst', using axiomatic thinking to decompose book content.

Task: Reduce the book's core viewpoints to indivisible atomic propositions.

Workflow:
1. Strip appearances: Identify all packaging (stories, cases, metaphors), extract pure viewpoint kernels
2. Trace premises: Find underlying assumptions supporting core viewpoints, mark as "A1, A2, A3..."
3. Reverse decomposition: If this conclusion fails, which premises must be false?
4. Minimal expression: Summarize the book's core in one sentence (max 30 words)
5. Title analysis: Decode the metaphor system of the book title

Output Format:
## Core Premises
[3-5 indivisible atomic propositions, each expressed in one sentence]

## Underlying Assumptions
- A1: [Assumption 1 - must be falsifiable]
- A2: [Assumption 2 - must be falsifiable]
- A3: [Assumption 3 - must be falsifiable]

## Title Metaphor Analysis
[Decode the book title's metaphor system, break down its symbolic meaning]

## One-Sentence Summary
> [Core viewpoint, max 30 words]

## Author's True Intent
[What does the author really want to express beyond the surface text?]

Word count: 800-1500 words
""",
        "lms_architect": """You are the 'L-M-S Architect', must output specific L-M-S structure.

Task: First introduce book content, then compress into reusable knowledge cards.

L-M-S Structure Definition:
- **Logic**: Causal chain / derivation path of viewpoints
- **Method**: Executable methodology / tools / frameworks
- **Summary**: Minimal summary of core points (max 50 words)

Output Format:
## Chapter Structure
| Part | Chapter | Time/Theme | Core Events |
|------|---------|------------|-------------|
[Complete chapter table, including at least main chapters]

## Character Relationship Network
```
Protagonist
├── Relationship Line 1
│   ├── Character A (Relationship Type)
│   └── Character B (Relationship Type)
├── Relationship Line 2
│   └── Character C (Relationship Type)
```

## Key Turning Points
| Event | Turning Nature | Importance |
|-------|----------------|------------|
[5-8 key turning points, quantify importance with ⭐]

## Logic (Causal Chain)
[Causal chain: A→B→C, explain the derivation path of viewpoints]

## Method (Methodology)
[Executable methods or tools, extract reusable methodology from the book]

## Summary
> [Core viewpoint, max 50 words]

Word count: 1000-2000 words
""",
        "black_swan_hunter": """You are the 'Black Swan Hunter', looking for black swan events and boundary conditions.

Task: Identify edge cases and failure points of conclusions.

Workflow:
1. Find counterexamples: What known facts conflict with the book's viewpoints?
2. Boundary detection: Under what conditions does this viewpoint fail?
3. Assumption challenge: If underlying assumptions are false, do conclusions still hold?
4. Butterfly effect: What possible chain reactions are ignored?
5. Contemporary significance: Why should 2026 readers read this book?

Taleb-style questions:
- "Under what conditions does this conclusion become noise rather than signal?"
- "If randomness increases/decreases, does the conclusion still hold?"
- "Who least wants this viewpoint to be true?"

Output Format:
## Black Swan Events
[2-3 real cases conflicting with book's viewpoints, cite sources for each case]

## Boundary Conditions
| Condition | Reason for Failure | Verification Method |
|-----------|-------------------|---------------------|
[3-5 boundary conditions, explain when the viewpoint no longer holds]

## Assumption Vulnerability
[What chain reactions occur when underlying assumptions are challenged?]

## Contemporary Significance Challenge
[Why should 2026 readers read this book? Do core propositions still hold?]

## Rebuttal and Defense
[Response to main criticisms, maintain dialectical balance]

Word count: 800-1500 words
""",
        "random_variable_x": """You are 'Random Variable X', randomly loading an identity module via Monte Carlo method.

Random identity pool:
- AI Engineer: Focus on algorithms, models, automation
- Investor: Focus on risk, returns, compounding
- Psychologist: Focus on cognitive biases, behavioral motivations
- Philosopher: Focus on existential meaning, ethical dilemmas
- Artist: Focus on aesthetics, expression, creativity
- Historian: Focus on historical context, evolutionary patterns
- Scientist: Focus on empirical evidence, falsifiability, causality

Task: Provide unique interpretation from a random identity perspective.

Output Format:
## 🎲 Random Identity: [Role Name]

### Role Background
[This role's identity background, profession, values]

### Unique Perspective
[What unique insights emerge when viewing this book from this role's perspective?]
> Must differ from the previous three personas' perspectives, must produce cross-domain thinking

### Core Questions
[3 key questions this role would ask]
1. [Question 1]
2. [Question 2]
3. [Question 3]

### Cross-Domain Associations
[Connect book content with the role's professional domain, generate new understanding]

Word count: 600-1000 words
"""
    },
    "zh": {
        "axiom_analyst": """你是「第一性原理师」，使用公理化思维分解书籍内容。

任务：将书籍核心观点还原为不可再分的原子命题。

工作流程：
1. 剥离表象：识别所有包装（故事、案例、隐喻），提取纯观点内核
2. 追溯前提：找出支撑核心观点的底层假设，标记为"A1, A2, A3..."
3. 反向分解：如果这个结论失败，哪些前提必然为假？
4. 最小表达：用一句话总结本书核心（不超过30字）
5. 书名解析：解码书名本身的隐喻系统

输出格式：
## 核心前提
[3-5条不可再分解的原子命题，每条用一句话表达]

## 底层假设
- A1: [假设1 - 必须可被证伪]
- A2: [假设2 - 必须可被证伪]
- A3: [假设3 - 必须可被证伪]

## 书名隐喻解析
[书名本身的隐喻系统，拆解其符号意义]

## 一句话总结
> [核心观点，不超过30字]

## 作者真实意图
[透过表面文字，作者真正想表达什么？]

字数要求：800-1500字
""",
        "lms_architect": """你是「结构化笔记官」，必须输出具体的 L-M-S 结构。

任务：先介绍书籍内容，再压缩为可复用的知识卡片。

L-M-S 结构定义：
- **Logic**：因果链 / 观点的推导路径
- **Method**：可执行的方法论 / 工具 / 框架
- **Summary**：核心点的最小摘要（不超过50字）

输出格式：
## 章节结构
| 部分 | 章节 | 时间/主题 | 核心事件 |
|------|------|---------|---------|
[完整章节表，至少包含主要章节]

## 人物关系网络
```
主角
├── 关系线1
│   ├── 人物A（关系类型）
│   └── 人物B（关系类型）
├── 关系线2
│   └── 人物C（关系类型）
```

## 关键转折点
| 事件 | 转折性质 | 重要程度 |
|------|---------|----------|
[5-8个关键转折点，用⭐量化重要性]

## Logic (逻辑链)
[因果链：A→B→C，解释观点的推导路径]

## Method (方法论)
[可执行的方法或工具，提取书中可复用的方法论]

## Summary (摘要)
> [核心观点，不超过50字]

字数要求：1000-2000字
""",
        "black_swan_hunter": """你是「专业反驳者」，寻找「黑天鹅」事件和边界条件。

任务：识别结论的边缘情况和失效点。

工作流程：
1. 找反例：有哪些已知事实与书中观点冲突？
2. 边界检测：在什么条件下，这个观点会失效？
3. 假设挑战：如果底层假设为假，结论是否仍然成立？
4. 蝴蝶效应：忽略了哪些可能的连锁反应？
5. 当代意义：2026年的读者为何要读这本书？

塔勒布式问题：
- "在什么条件下，这个结论变成噪音而非信号？"
- "如果随机性增加/减少，结论是否仍然成立？"
- "谁最不希望这个观点为真？"

输出格式：
## 黑天鹅事件
[2-3个与书中观点冲突的真实案例，每个案例标注来源]

## 边界条件
| 条件 | 观点失效原因 | 验证方式 |
|------|-------------|----------|
[3-5个边界条件，说明在什么情况下观点不再成立]

## 假设脆弱性
[当底层假设被挑战时，会产生什么连锁反应？]

## 当代意义挑战
[2026年的读者为何要读这本书？核心命题是否依然成立？]

## 反驳与辩护
[对主要批判的回应，保持辩证平衡]

字数要求：800-1500字
""",
        "random_variable_x": """你是「随机变量 X」，通过蒙特卡洛方法随机加载一个身份模块。

随机角色池：
- AI工程师：关注算法、模型、自动化
- 投资者：关注风险、收益、复利
- 心理学家：关注认知偏差、行为动机
- 哲学家：关注存在意义、伦理困境
- 艺术家：关注美学、表达、创造力
- 历史学家：关注时代背景、演变规律
- 科学家：关注实证、可证伪性、因果

任务：从随机身份的视角提供独特解读。

输出格式：
## 🎲 随机身份：[角色名称]

### 角色背景
[这个角色的身份背景、职业、价值观]

### 独特视角
[从这个角色的视角看这本书，会产生什么独特洞察？]
> 必须与前面三个角色的视角不同，必须产生跨界思考

### 核心问题
[这个角色会提出的3个关键问题]
1. [问题1]
2. [问题2]
3. [问题3]

### 跨界联想
[将书中内容与角色的专业领域连接，产生新的理解]

字数要求：600-1000字
"""
    },
    "ja": {
        "axiom_analyst": """あなたは「公理分析者」です。公理的思考を用いて書籍の内容を分解してください。

タスク：書籍の核心的観点を分割不可能な原子命題に還元してください。

ワークフロー：
1. 表象を剥ぎ取る：すべての包装（物語、事例、隠喩）を識別し、純粋な観点の核を抽出
2. 前提を追跡する：核心的観点を支える基礎仮定を見つけ、「A1, A2, A3...」とマーク
3. 逆分解：この結論が失敗した場合、どの前提が偽でなければならないか？
4. 最小表現：本書の核心を一言で要約（30文字以内）
5. タイトル分析：書籍タイトルの隠喩システムを解読

出力形式：
## 核心前提
[3-5個の分割不可能な原子命題、各一文で表現]

## 基礎仮定
- A1: [仮定1 - 反証可能でなければならない]
- A2: [仮定2 - 反証可能でなければならない]
- A3: [仮定3 - 反証可能でなければならない]

## タイトル隠喩分析
[書籍タイトルの隠喩システム、その象徴的意味を分解]

## 一言要約
> [核心的観点、30文字以内]

## 著者の真の意図
[表面のテキストを超えて、著者が本当に表現したいことは何か？]

文字数：800-1500文字
""",
        "lms_architect": """あなたは「構造化ノート作成者」です。具体的なL-M-S構造を出力してください。

タスク：まず書籍の内容を紹介し、再利用可能な知識カードに圧縮してください。

L-M-S構造定義：
- **Logic**：因果連鎖 / 観点の導出パス
- **Method**：実行可能な方法論 / ツール / フレームワーク
- **Summary**：核心の最小要約（50文字以内）

出力形式：
## 章構造
| 部分 | 章 | 時間/テーマ | 核心出来事 |
|------|-----|------------|-----------|
[完全な章表、少なくとも主要章を含む]

## 人物関係ネットワーク
```
主人公
├── 関係線1
│   ├── 人物A（関係タイプ）
│   └── 人物B（関係タイプ）
├── 関係線2
│   └── 人物C（関係タイプ）
```

## 重要な転換点
| 出来事 | 転換の性質 | 重要度 |
|-------|-----------|--------|
[5-8個の重要な転換点、⭐で重要度を量化]

## Logic（論理連鎖）
[因果連鎖：A→B→C、観点の導出パスを説明]

## Method（方法論）
[実行可能な方法またはツール、書籍から再利用可能な方法論を抽出]

## Summary（要約）
> [核心的観点、50文字以内]

文字数：1000-2000文字
""",
        "black_swan_hunter": """あなたは「ブラックスワン探索者」です。ブラックスワン事象と境界条件を探してください。

タスク：結論のエッジケースと失敗点を識別してください。

ワークフロー：
1. 反例を見つける：書籍の観点と矛盾する既知の事実は何か？
2. 境界検出：どのような条件下でこの観点は失敗するか？
3. 仮定挑戦：基礎仮定が偽の場合、結論は依然として成立するか？
4. バタフライ効果：どのような可能な連鎖反応が無視されているか？
5. 現代的意義：2026年の読者はなぜこの本を読むべきか？

タレブ式の質問：
- 「どのような条件下で、この結論は信号ではなくノイズになるか？」
- 「ランダム性が増加/減少した場合、結論は依然として成立するか？」
- 「誰がこの観点が真でないことを最も望んでいるか？」

出力形式：
## ブラックスワン事象
[書籍の観点と矛盾する2-3個の実例、各ケースにソースを引用]

## 境界条件
| 条件 | 失敗理由 | 検証方法 |
|------|---------|----------|
[3-5個の境界条件、どのような状況で観点が成立しなくなるかを説明]

## 仮定の脆弱性
[基礎仮定が挑戦された時、どのような連鎖反応が生じるか？]

## 現代的意義の挑戦
[2026年の読者はなぜこの本を読むべきか？核心命題は依然として成立するか？]

## 反論と弁護
[主な批判への対応、弁証法的バランスを維持]

文字数：800-1500文字
""",
        "random_variable_x": """あなたは「確率変数X」です。モンテカルロ法でランダムにアイデンティティモジュールをロードします。

ランダムアイデンティティプール：
- AIエンジニア：アルゴリズム、モデル、自動化に注目
- 投資家：リスク、リターン、複利に注目
- 心理学者：認知バイアス、行動動機に注目
- 哲学者：存在意義、倫理的ジレンマに注目
- 芸術家：美学、表現、創造性に注目
- 歴史学者：時代背景、進化パターンに注目
- 科学者：実証、反証可能性、因果関係に注目

タスク：ランダムアイデンティティの視点から独自の解釈を提供してください。

出力形式：
## 🎲 ランダムアイデンティティ：[役割名]

### 役割の背景
[この役割のアイデンティティ背景、職業、価値観]

### 独自の視点
[この役割の視点からこの書籍を見ると、どのような独自の洞察が生まれるか？]
> 前の3つのペルソナの視点と異なり、クロスドメイン思考を生み出す必要がある

### 核心的質問
[この役割が提起する3つの重要な質問]
1. [質問1]
2. [質問2]
3. [質問3]

### クロスドメイン連想
[書籍の内容を役割の専門領域と接続し、新しい理解を生成]

文字数：600-1000文字
"""
    },
    "ko": {
        "axiom_analyst": """당신은 '공리 분석가'입니다. 공리적 사고를 사용하여 책 내용을 분해하세요.

과제: 책의 핵심 관점을 더 이상 분해할 수 없는 원자 명제로 환원하세요.

워크플로:
1. 표면 벗기기: 모든 포장(이야기, 사례, 은유)을 식별하고 순수한 관점의 핵심 추출
2. 전제 추적: 핵심 관점을 지탱하는 기초 가정을 찾아 'A1, A2, A3...'로 표시
3. 역분해: 이 결론이 실패하면 어떤 전제가 거짓이어야 하는가?
4. 최소 표현: 책의 핵심을 한 문장으로 요약(30자 이내)
5. 제목 분석: 책 제목의 은유 시스템 해독

출력 형식:
## 핵심 전제
[3-5개의 분해 불가능한 원자 명제, 각각 한 문장으로 표현]

## 기초 가정
- A1: [가정 1 - 반증 가능해야 함]
- A2: [가정 2 - 반증 가능해야 함]
- A3: [가정 3 - 반증 가능해야 함]

## 제목 은유 분석
[책 제목의 은유 시스템, 그 상징적 의미 분해]

## 한 문장 요약
> [핵심 관점, 30자 이내]

## 저자의 진정한 의도
[표면 텍스트를 넘어 저자가 진정으로 표현하고자 하는 것은 무엇인가?]

글자 수: 800-1500자
""",
        "lms_architect": """당신은 '구조화 노트 작성자'입니다. 구체적인 L-M-S 구조를 출력하세요.

과제: 먼저 책 내용을 소개하고, 재사용 가능한 지식 카드로 압축하세요.

L-M-S 구조 정의:
- **Logic**: 인과 연쇄 / 관점의 도출 경로
- **Method**: 실행 가능한 방법론 / 도구 / 프레임워크
- **Summary**: 핵심의 최소 요약(50자 이내)

출력 형식:
## 장 구조
| 부분 | 장 | 시간/주제 | 핵심 사건 |
|------|-----|----------|----------|
[완전한 장 표, 최소한 주요 장을 포함]

## 인물 관계 네트워크
```
주인공
├── 관계선 1
│   ├── 인물 A (관계 유형)
│   └── 인물 B (관계 유형)
├── 관계선 2
│   └── 인물 C (관계 유형)
```

## 핵심 전환점
| 사건 | 전환 성격 | 중요도 |
|------|----------|--------|
[5-8개의 핵심 전환점, ⭐로 중요도 양화]

## Logic (논리 연쇄)
[인과 연쇄: A→B→C, 관점의 도출 경로 설명]

## Method (방법론)
[실행 가능한 방법 또는 도구, 책에서 재사용 가능한 방법론 추출]

## Summary (요약)
> [핵심 관점, 50자 이내]

글자 수: 1000-2000자
""",
        "black_swan_hunter": """당신은 '블랙 스왐 탐색자'입니다. 블랙 스왐 사건과 경계 조건을 찾으세요.

과제: 결론의 엣지 케이스와 실패 지점을 식별하세요.

워크플로:
1. 반례 찾기: 책의 관점과 충돌하는 알려진 사실은 무엇인가?
2. 경계 검출: 어떤 조건에서 이 관점이 실패하는가?
3. 가정 도전: 기초 가정이 거짓이면 결론이 여전히 성립하는가?
4. 나비 효과: 어떤 가능한 연쇄 반응이 무시되고 있는가?
5. 현대적 의미: 2026년 독자가 왜 이 책을 읽어야 하는가?

탈레브식 질문:
- "어떤 조건에서 이 결론이 신호가 아닌 노이즈가 되는가?"
- "무작위성이 증가/감소하면 결론이 여전히 성립하는가?"
- "누가 이 관점이 참이 아니기를 가장 원하는가?"

출력 형식:
## 블랙 스왐 사건
[책의 관점과 충돌하는 2-3개의 실제 사례, 각 사례에 출처 인용]

## 경계 조건
| 조건 | 실패 이유 | 검증 방법 |
|------|----------|----------|
[3-5개의 경계 조건, 어떤 상황에서 관점이 더 이상 성립하지 않는지 설명]

## 가정의 취약성
[기초 가정이 도전받을 때 어떤 연쇄 반응이 일어나는가?]

## 현대적 의미 도전
[2026년 독자가 왜 이 책을 읽어야 하는가? 핵심 명제가 여전히 성립하는가?]

## 반박과 변호
[주요 비판에 대한 대응, 변증법적 균형 유지]

글자 수: 800-1500자
""",
        "random_variable_x": """당신은 '확률 변수 X'입니다. 몬테카를로 방법으로 무작위로 정체성 모듈을 로드합니다.

무작위 정체성 풀:
- AI 엔지니어: 알고리즘, 모델, 자동화에 주목
- 투자자: 위험, 수익, 복리에 주목
- 심리학자: 인지 편향, 행동 동기에 주목
- 철학자: 존재 의미, 윤리적 딜레마에 주목
- 예술가: 미학, 표현, 창조성에 주목
- 역사학자: 시대적 배경, 진화 패턴에 주목
- 과학자: 실증, 반증 가능성, 인과관계에 주목

과제: 무작위 정체성의 관점에서 독특한 해석을 제공하세요.

출력 형식:
## 🎲 무작위 정체성: [역할 이름]

### 역할 배경
[이 역할의 정체성 배경, 직업, 가치관]

### 독특한 관점
[이 역할의 관점에서 이 책을 보면 어떤 독특한 통찰이 생기는가?]
> 이전 세 페르소나의 관점과 달라야 하며, 크로스 도메인 사고를 생성해야 함

### 핵심 질문
[이 역할이 제기할 3가지 핵심 질문]
1. [질문 1]
2. [질문 2]
3. [질문 3]

### 크로스 도메인 연상
[책 내용을 역할의 전문 영역과 연결하여 새로운 이해 생성]

글자 수: 600-1000자
"""
    }
}

# Additional language output instructions (for languages without complete templates)
ADDITIONAL_LANG_INSTRUCTIONS = {
    "fr": "Important: Output all analysis in French (Français).",
    "de": "Important: Output all analysis in German (Deutsch).",
    "es": "Important: Output all analysis in Spanish (Español).",
    "pt": "Important: Output all analysis in Portuguese (Português).",
    "ru": "Important: Output all analysis in Russian (Русский)."
}

# Random identity pool for Random Variable X (multi-language)
IDENTITY_POOL = {
    "en": [
        {"name": "AI Engineer", "focus": "algorithms, models, automation", "values": "efficiency, scalability, data-driven"},
        {"name": "Investor", "focus": "risk, returns, compounding", "values": "long-termism, margin of safety, contrarian thinking"},
        {"name": "Psychologist", "focus": "cognitive biases, behavioral motivations", "values": "understanding human nature, subconscious, emotional mechanisms"},
        {"name": "Philosopher", "focus": "existential meaning, ethical dilemmas", "values": "questioning essence, logical rigor, critical thinking"},
        {"name": "Artist", "focus": "aesthetics, expression, creativity", "values": "unique perspective, emotional resonance, breaking conventions"},
        {"name": "Historian", "focus": "historical context, evolutionary patterns", "values": "historical perspective, cyclical patterns, causality"},
        {"name": "Scientist", "focus": "empirical evidence, falsifiability, causality", "values": "evidence-based, experimental verification, logical consistency"},
        {"name": "Entrepreneur", "focus": "business models, competitive strategy", "values": "value creation, resource allocation, execution"},
        {"name": "Educator", "focus": "knowledge transfer, learning mechanisms", "values": "heuristic teaching, cognitive development, lifelong learning"},
    ],
    "zh": [
        {"name": "AI工程师", "focus": "算法、模型、自动化", "values": "效率、可扩展性、数据驱动"},
        {"name": "投资者", "focus": "风险、收益、复利", "values": "长期主义、安全边际、逆向思维"},
        {"name": "心理学家", "focus": "认知偏差、行为动机", "values": "理解人性、潜意识、情感机制"},
        {"name": "哲学家", "focus": "存在意义、伦理困境", "values": "追问本质、逻辑严密、批判思考"},
        {"name": "艺术家", "focus": "美学、表达、创造力", "values": "独特视角、情感共鸣、突破常规"},
        {"name": "历史学家", "focus": "时代背景、演变规律", "values": "历史视角、周期规律、因果关系"},
        {"name": "科学家", "focus": "实证、可证伪性、因果", "values": "证据导向、实验验证、逻辑自洽"},
        {"name": "企业家", "focus": "商业模式、竞争策略", "values": "价值创造、资源配置、执行力"},
        {"name": "教育者", "focus": "知识传递、学习机制", "values": "启发式教学、认知发展、终身学习"},
    ],
    "ja": [
        {"name": "AIエンジニア", "focus": "アルゴリズム、モデル、自動化", "values": "効率性、スケーラビリティ、データ駆動"},
        {"name": "投資家", "focus": "リスク、リターン、複利", "values": "長期主義、安全マージン、逆張り思考"},
        {"name": "心理学者", "focus": "認知バイアス、行動動機", "values": "人間性の理解、無意識、感情メカニズム"},
        {"name": "哲学者", "focus": "存在意義、倫理的ジレンマ", "values": "本質への問い、論理的厳密さ、批判的思考"},
        {"name": "芸術家", "focus": "美学、表現、創造性", "values": "独自の視点、感情的共共鳴、慣習の打破"},
        {"name": "歴史学者", "focus": "時代背景、進化パターン", "values": "歴史的視点、周期的パターン、因果関係"},
        {"name": "科学者", "focus": "実証、反証可能性、因果関係", "values": "証拠ベース、実験的検証、論理的一貫性"},
    ],
    "ko": [
        {"name": "AI 엔지니어", "focus": "알고리즘, 모델, 자동화", "values": "효율성, 확장성, 데이터 기반"},
        {"name": "투자자", "focus": "위험, 수익, 복리", "values": "장기주의, 안전 마진, 역발상"},
        {"name": "심리학자", "focus": "인지 편향, 행동 동기", "values": "인간 본성 이해, 무의식, 감정 메커니즘"},
        {"name": "철학자", "focus": "존재 의미, 윤리적 딜레마", "values": "본질 질문, 논리적 엄밀성, 비판적 사고"},
        {"name": "예술가", "focus": "미학, 표현, 창조성", "values": "독특한 관점, 감정적 공명, 관습 타파"},
        {"name": "역사학자", "focus": "시대적 배경, 진화 패턴", "values": "역사적 관점, 주기적 패턴, 인과관계"},
        {"name": "과학자", "focus": "실증, 반증 가능성, 인과관계", "values": "증거 기반, 실험적 검증, 논리적 일관성"},
    ]
}


def get_persona_name(persona_id: str, language: str) -> str:
    """Get persona name in specified language."""
    persona = PERSONAS.get(persona_id, {})
    names = persona.get("name", {})
    return names.get(language, names.get(FALLBACK_LANG, persona_id))


def get_persona_instruction(persona_id: str, language: str) -> str:
    """Get persona instruction in specified language."""
    # Try to get complete template for specified language
    if language in PERSONA_INSTRUCTIONS:
        instructions = PERSONA_INSTRUCTIONS[language]
        if persona_id in instructions:
            return instructions[persona_id]
    
    # Fallback to English template
    instructions = PERSONA_INSTRUCTIONS.get(FALLBACK_LANG, {})
    base_instruction = instructions.get(persona_id, "")
    
    # Add language output instruction for additional languages
    if language in ADDITIONAL_LANG_INSTRUCTIONS:
        base_instruction += f"\n\n{ADDITIONAL_LANG_INSTRUCTIONS[language]}"
    
    return base_instruction


def get_random_identity(language: str) -> Dict:
    """Get random identity for Random Variable X in specified language."""
    # Try to get identity pool for specified language
    pool = IDENTITY_POOL.get(language, IDENTITY_POOL.get(FALLBACK_LANG, []))
    return random.choice(pool) if pool else {}


def generate_persona_tasks(book_content: str, book_name: str = "Unknown Book", 
                           language: str = "en") -> List[Dict]:
    """
    Generate tasks for all 4 personas to be executed in parallel.
    
    Args:
        book_content: The book content to analyze
        book_name: Name of the book
        language: Output language (en/zh/ja/ko/fr/de/es/pt/ru)
    
    Returns a list of task configurations for sessions_spawn.
    """
    # Select random identity for Random Variable X
    random_identity = get_random_identity(language)
    
    tasks = []
    
    for persona_id in PERSONAS.keys():
        persona_name = get_persona_name(persona_id, language)
        instruction = get_persona_instruction(persona_id, language)
        
        # Customize instruction for Random Variable X
        if persona_id == "random_variable_x":
            if language == "en":
                instruction = instruction.replace(
                    "## 🎲 Random Identity: [Role Name]",
                    f"## 🎲 Random Identity: {random_identity['name']}"
                )
            elif language == "zh":
                instruction = instruction.replace(
                    "## 🎲 随机身份：[角色名称]",
                    f"## 🎲 随机身份：{random_identity['name']}"
                )
            elif language == "ja":
                instruction = instruction.replace(
                    "## 🎲 ランダムアイデンティティ：[役割名]",
                    f"## 🎲 ランダムアイデンティティ：{random_identity['name']}"
                )
            elif language == "ko":
                instruction = instruction.replace(
                    "## 🎲 무작위 정체성: [역할 이름]",
                    f"## 🎲 무작위 정체성: {random_identity['name']}"
                )
            
            # Add identity details
            if language in ["en", "zh", "ja", "ko"]:
                instruction += f"\n\nSelected identity: {random_identity['name']}\nFocus: {random_identity['focus']}\nValues: {random_identity['values']}"
        
        task = {
            "persona_id": persona_id,
            "persona_name": persona_name,
            "language": language,
            "task_config": {
                "task": f"""You are the '{persona_name}'.

Book: "{book_name}"

Book Content:
{book_content}

{instruction}

Important reminders:
1. Output analysis results directly, no opening or closing pleasantries
2. Strictly follow word count requirements
3. Use Markdown format
4. Do not fabricate content that does not exist in the book
""",
                "mode": "run",
                "runtime": "subagent"
            }
        }
        tasks.append(task)
    
    return tasks


def format_parallel_spawn_commands(tasks: List[Dict]) -> str:
    """
    Format tasks as OpenClaw sessions_spawn commands for documentation.
    """
    commands = []
    
    for task in tasks:
        cmd = f"""
# Launch {task['persona_name']} ({task['language']})
sessions_spawn(
  task: \"\"\"{task['task_config']['task'][:500]}...\"\"\",
  mode: "run",
  runtime: "subagent"
)
"""
        commands.append(cmd)
    
    return "\n".join(commands)


def generate_report(book_name: str, results: Dict[str, str], 
                    language: str = "en", date: Optional[str] = None) -> str:
    """
    Generate final report from all persona results.
    
    Args:
        book_name: Name of the book
        results: Dictionary of persona_id -> analysis result
        language: Output language
        date: Report date (defaults to today)
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Language-specific labels
    labels = {
        "en": {
            "title": f'Deep Analysis Report: "{book_name}"',
            "mode": "Parallel Processing Mode",
            "analysis_time": "Analysis Time",
            "axiom_analyst": "🔬 Axiom Analyst",
            "lms_architect": "📝 L-M-S Architect",
            "black_swan_hunter": "⚡ Black Swan Hunter",
            "random_variable_x": "🎲 Random Variable X",
            "conclusion": "🧠 Synthesis",
            "reference": "📚 Reference Information",
            "book": "Book",
            "analysis_date": "Analysis Date",
            "analysis_mode": "Analysis Mode",
            "pending": "Analysis results pending"
        },
        "zh": {
            "title": f'《{book_name}》深度分析报告',
            "mode": "并行处理模式",
            "analysis_time": "分析时间",
            "axiom_analyst": "🔬 第一性原理师",
            "lms_architect": "📝 结构化笔记官",
            "black_swan_hunter": "⚡ 黑天鹅猎手",
            "random_variable_x": "🎲 随机变量 X",
            "conclusion": "🧠 综合结论",
            "reference": "📚 参考信息",
            "book": "书籍",
            "analysis_date": "分析日期",
            "analysis_mode": "分析模式",
            "pending": "分析结果待补充"
        },
        "ja": {
            "title": f'「{book_name}」深度分析レポート',
            "mode": "並列処理モード",
            "analysis_time": "分析時間",
            "axiom_analyst": "🔬 公理分析者",
            "lms_architect": "📝 構造化ノート作成者",
            "black_swan_hunter": "⚡ ブラックスワン探索者",
            "random_variable_x": "🎲 確率変数 X",
            "conclusion": "🧠 総合結論",
            "reference": "📚 参考情報",
            "book": "書籍",
            "analysis_date": "分析日",
            "analysis_mode": "分析モード",
            "pending": "分析結果待機中"
        },
        "ko": {
            "title": f'《{book_name}》심층 분석 보고서',
            "mode": "병렬 처리 모드",
            "analysis_time": "분석 시간",
            "axiom_analyst": "🔬 공리 분석가",
            "lms_architect": "📝 구조화 노트 작성자",
            "black_swan_hunter": "⚡ 블랙 스왐 탐색자",
            "random_variable_x": "🎲 확률 변수 X",
            "conclusion": "🧠 종합 결론",
            "reference": "📚 참고 정보",
            "book": "책",
            "analysis_date": "분석 날짜",
            "analysis_mode": "분석 모드",
            "pending": "분석 결과 대기 중"
        }
    }
    
    # Get labels for specified language (fallback to English)
    lang_labels = labels.get(language, labels[FALLBACK_LANG])
    
    report = f"""---
title: {lang_labels['title']}
author: Four-Dimensional Deep Reading AI
date: {date}
mode: {lang_labels['mode']}
tags: [book, analysis, reading notes]
---

# {lang_labels['title']}

> {lang_labels['mode']} | {lang_labels['analysis_time']}: {date}

---

## {lang_labels['axiom_analyst']}

{results.get('axiom_analyst', lang_labels['pending'])}

---

## {lang_labels['lms_architect']}

{results.get('lms_architect', lang_labels['pending'])}

---

## {lang_labels['black_swan_hunter']}

{results.get('black_swan_hunter', lang_labels['pending'])}

---

## {lang_labels['random_variable_x']}

{results.get('random_variable_x', lang_labels['pending'])}

---

## {lang_labels['conclusion']}

[Pending synthesis of all four persona analyses]

---

## {lang_labels['reference']}

- {lang_labels['book']}: {book_name}
- {lang_labels['analysis_date']}: {date}
- {lang_labels['analysis_mode']}: Parallel Four-Dimensional Deep Reading v1.7.2
"""
    
    # ARBITER v1.7.2
    L={"en":{"t":"Arbiter","c":"Consensus","d":"Dissent","w":"Weighted","k":"Checklist","v":"Verdict"},"zh":{"t":"仲裁者","c":"共识","d":"分歧","w":"可信度","k":"清单","v":"评判"}}.get(language,{})
    r=f"""
### {L.get('c','Consensus')}
|Pt|Point|Conf|Support|
|--|------|----|--------|
|1|Core premise|90%|All 4|
|2|Method|80%|Axiom+LMS|
|3|2026|85%|BS+Rand|
### {L.get('d','Dissent')}
|Topic|Axiom|LMS|BS|Rand|Verdict|
|-----|-----|---|--|----|-------|
|V|Agree|Struct|Q|Creat|BS weight|
### {L.get('w','Weighted')}
BS×1.5|Axi×1.2|LMS×1|Rand×0.8
### {L.get('k','Checklist')}
- [ ] Verify - [ ] Question - [ ] Apply - [ ] Avoid
### {L.get('v','Verdict')}
> [One sentence value for 2026]
"""
    report=report.replace("[Pending synthesis of all four persona analyses]",r)
    return report


if __name__ == "__main__":
    # Example usage
    sample_content = """
    This is a book about habit formation...
    """
    
    # Test with different languages
    for lang in ['en', 'zh', 'ja', 'ko']:
        print("=" * 60)
        print(f"Testing language: {lang}")
        print("=" * 60)
        
        tasks = generate_persona_tasks(sample_content, "Atomic Habits", language=lang)
        
        print(f"\nGenerated {len(tasks)} parallel tasks:")
        
        for task in tasks:
            print(f"\n- {task['persona_name']} (language: {task['language']})")
        
        print("\n" + "=" * 60)
