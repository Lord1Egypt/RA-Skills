<div align="center">

# 요리.skill

> 뭘 해 먹을지 모르겠으면, 냉장고 상태랑 입맛부터 솔직하게 말하면 된다.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Agent Skill](https://img.shields.io/badge/Skill-Cooking-green)](#)
[![Status](https://img.shields.io/badge/status-v0.1.0-orange)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`cooking.skill` 은 필요한 것만 조금 물어보고, 실제로 따라 할 수 있는 레시피를 주는 요리 Skill 입니다.

</div>

기본 방향:

- 중국식 가정요리 중심
- 집 주방에서 가능한 실전 기술
- 살짝 생동감은 있지만 과장하지 않는 말투

## 하는 일

- 오늘 뭘 먹을지 추천
- 집에 있는 재료로 메뉴 구성
- 특정 요리나 조리 기술 질문에 바로 답변
- 대체 재료, 망하기 쉬운 지점, 복구 팁 제공

## 기본 흐름

입력을 자동으로 세 가지로 나눕니다:

- `뭘 먹고 싶은지`
- `집에 뭐가 있는지`
- `이 요리 / 기술을 어떻게 하는지`

필요할 때만 최대 두 가지를 묻습니다:

1. `몇 명이 먹는지`
2. `못 먹는 것, 못 하는 것, 없는 재료나 도구가 있는지`

## 기본 출력

- 뭘 만들지
- 왜 이 요리가 맞는지
- 필요한 재료
- 만드는 방법
- 핵심 포인트
- 망하기 쉬운 지점
- 대체안 / 복구 방법

## 설치

공통 설치:

```bash
npx skills add zning1994/cooking-skill
```

OpenClaw / ClawHub:

```bash
openclaw skills install cooking-skill
```

```bash
mkdir -p .claude/skills
git clone https://github.com/zning1994/cooking-skill .claude/skills/cooking-skill
```

전역 설치:

```bash
git clone https://github.com/zning1994/cooking-skill ~/.claude/skills/cooking-skill
```
