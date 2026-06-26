<div align="center">

# 料理.skill

> 何を作るか迷ったら、まず冷蔵庫と気分を正直に言えばいい。

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Agent Skill](https://img.shields.io/badge/Skill-Cooking-green)](#)
[![Status](https://img.shields.io/badge/status-v0.1.0-orange)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`cooking.skill` は、必要なことだけを少し聞いて、実際に作れるレシピを返す料理 Skill です。

</div>

基本方針：

- 中華の家庭料理を中心にする
- 家庭の台所で再現しやすい技法を優先する
- 元気はあるが、わざとらしくはない話し方を保つ

## できること

- 「今日は何を食べたいか」から料理を提案する
- 「家にある食材」から料理を組み立てる
- 特定の料理や技法の質問にそのまま答える
- 代用品、失敗しやすい点、リカバリー方法も出す

## 基本の流れ

入力は主に3種類です：

- 何が食べたいか
- 家に何があるか
- 特定の料理 / 技法の質問

必要な場合だけ、最大2つ質問します：

1. `何人分か`
2. `食べられないもの、作れないこと、家にない条件があるか`

## 出力内容

- 何を作るか
- なぜそれが合うか
- 必要な材料
- 手順
- 重要なコツ
- 失敗しやすい点
- 代用やリカバリー方法

## インストール

共通インストール:

```bash
npx skills add zning1994/cooking-skill
```

OpenClaw / ClawHub:

```bash
openclaw skills install cooking-skill
```

現在のプロジェクトに入れる場合：

```bash
mkdir -p .claude/skills
git clone https://github.com/zning1994/cooking-skill .claude/skills/cooking-skill
```

グローバルに入れる場合：

```bash
git clone https://github.com/zning1994/cooking-skill ~/.claude/skills/cooking-skill
```

## 例

```text
今夜何を作ればいい？
鶏もも肉、じゃがいも、玉ねぎがある
牛肉を柔らかく炒めるには？
料理酒がないときはどうする？
```
