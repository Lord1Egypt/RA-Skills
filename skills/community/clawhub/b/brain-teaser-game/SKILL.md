---
name: brain-teaser-game
description: |
  [中文] 多语言脑筋急转弯互动游戏，支持中文、英文、日文。自动检测用户语言，支持随机出题、答案判断、提示系统、不重复题目历史记录。
  [English] Multi-language brain teaser interactive game supporting Chinese, English, and Japanese. Auto-detects user language with random questions, answer matching, hint system, and no-repeat history.
  [日本語] 多言語なぞなぞインタラクティブゲーム。中国語、英語、日本語に対応。ユーザーの言語を自動検出し、ランダム出題、回答判定、ヒント機能、履歴管理を提供。
---

# 🧠 Brain Teaser / 脑筋急转弯 / なぞなぞ

---

## 🇨🇳 中文

多语言脑筋急转弯互动游戏，支持中文、英文、日文。

### 功能

- 自动检测用户语言（中文/英文/日文）
- 200+ 题目库（每种语言）
- 智能答案匹配（模糊匹配）
- 提示系统
- 历史记录（不重复题目）

### 使用方法

#### 开始游戏

```bash
./invoke.sh start "来个脑筋急转弯"
```

#### 游戏中操作

| 操作 | 命令 |
|------|------|
| 回答 | 直接输入答案 |
| 提示 | 输入"提示" |
| 答案 | 输入"答案" |
| 下一题 | 输入"下一题" |

#### 命令行接口

```bash
# 提交答案
./invoke.sh answer {session_id} "你的答案"

# 获取提示
./invoke.sh hint {session_id}

# 查看答案
./invoke.sh reveal {session_id}

# 下一题
./invoke.sh next {session_id}

# 交互模式（自动检测意图）
./invoke.sh interactive {session_id} "提示"
./invoke.sh interactive {session_id} "你的答案"

# 重置历史记录
./invoke.sh reset-history
```

### 输出格式

所有输出为 Markdown 格式，包含：
- 当前题目
- 提示（如请求）
- 答案反馈
- 游戏统计
- 会话 ID

### AI 题目生成（可选）

配置环境变量启用 AI 动态生成新题：

```bash
export BRAIN_TEASER_API_KEY=your-api-key
export BRAIN_TEASER_API_BASE=https://api.example.com/v1  # 可选
export BRAIN_TEASER_MODEL=gpt-4  # 可选
```

API 配置读取优先级：
1. 环境变量 `BRAIN_TEASER_API_KEY`
2. `~/.claude/settings.json`
3. `~/.openclaw/openclaw.json`

---

## 🇺🇸 English

Multi-language brain teaser interactive game supporting Chinese, English, and Japanese.

### Features

- Auto-detect user language (Chinese/English/Japanese)
- 200+ question pool per language
- Smart answer matching (fuzzy matching)
- Hint system
- History tracking (no repeated questions)

### Usage

#### Start Game

```bash
./invoke.sh start "Give me a brain teaser"
```

#### In-Game Operations

| Action | Command |
|--------|---------|
| Answer | Type your answer directly |
| Hint | Type "hint" |
| Reveal Answer | Type "answer" |
| Next Question | Type "next" |

#### Command Line Interface

```bash
# Submit answer
./invoke.sh answer {session_id} "your answer"

# Get hint
./invoke.sh hint {session_id}

# Reveal answer
./invoke.sh reveal {session_id}

# Next question
./invoke.sh next {session_id}

# Interactive mode (auto-detect intent)
./invoke.sh interactive {session_id} "hint"
./invoke.sh interactive {session_id} "your answer"

# Reset history
./invoke.sh reset-history
```

### Output Format

All output is in Markdown format, including:
- Current question
- Hint (if requested)
- Answer feedback
- Game statistics
- Session ID

### AI Question Generation (Optional)

Configure environment variables to enable AI dynamic question generation:

```bash
export BRAIN_TEASER_API_KEY=your-api-key
export BRAIN_TEASER_API_BASE=https://api.example.com/v1  # optional
export BRAIN_TEASER_MODEL=gpt-4  # optional
```

API configuration priority:
1. Environment variable `BRAIN_TEASER_API_KEY`
2. `~/.claude/settings.json`
3. `~/.openclaw/openclaw.json`

---

## 🇯🇵 日本語

中国語、英語、日本語に対応したなぞなぞインタラクティブゲーム。

### 機能

- ユーザーの言語を自動検出（中国語/英語/日本語）
- 各言語200問以上の問題
- スマートな回答マッチング（曖昧検索対応）
- ヒント機能
- 履歴管理（重複なし）

### 使い方

#### ゲーム開始

```bash
./invoke.sh start "なぞなぞをください"
```

#### ゲーム中の操作

| 操作 | コマンド |
|------|----------|
| 回答 | 答えを直接入力 |
| ヒント | 「ヒント」と入力 |
| 答えを見る | 「答え」と入力 |
| 次の問題 | 「次」と入力 |

#### コマンドラインインターフェース

```bash
# 回答を送信
./invoke.sh answer {session_id} "あなたの答え"

# ヒントを取得
./invoke.sh hint {session_id}

# 答えを表示
./invoke.sh reveal {session_id}

# 次の問題
./invoke.sh next {session_id}

# インタラクティブモード（意図を自動検出）
./invoke.sh interactive {session_id} "ヒント"
./invoke.sh interactive {session_id} "あなたの答え"

# 履歴をリセット
./invoke.sh reset-history
```

### 出力形式

すべての出力はMarkdown形式で、以下を含みます：
- 現在の問題
- ヒント（リクエスト時）
- 回答フィードバック
- ゲーム統計
- セッションID

### AI問題生成（オプション）

AI動的問題生成を有効にするには環境変数を設定：

```bash
export BRAIN_TEASER_API_KEY=your-api-key
export BRAIN_TEASER_API_BASE=https://api.example.com/v1  # オプション
export BRAIN_TEASER_MODEL=gpt-4  # オプション
```

API設定の優先順位：
1. 環境変数 `BRAIN_TEASER_API_KEY`
2. `~/.claude/settings.json`
3. `~/.openclaw/openclaw.json`

---

## 📁 File Structure / 文件结构 / ファイル構成

```
brainTeaser/
├── SKILL.md           # This file / 本文件 / このファイル
├── invoke.sh          # Bash entry / Bash入口 / Bashエントリ
├── invoke.py          # Core implementation / 核心实现 / コア実装
├── language.py        # Language detection / 语言检测 / 言語検出
├── answer.py          # Answer matching / 答案判断 / 回答判定
├── session.py         # Session management / 会话管理 / セッション管理
├── ai_generator.py    # AI generation (optional) / AI生成（可选） / AI生成（オプション）
└── data/
    ├── zh.json        # Chinese questions / 中文题库 / 中国語問題
    ├── en.json        # English questions / 英文题库 / 英語問題
    └── ja.json        # Japanese questions / 日文题库 / 日本語問題
```

## 🔧 Dependencies / 依赖 / 依存関係

- Python 3.6+
- No external dependencies (standard library only) / 无外部依赖（标准库）/ 外部依存なし（標準ライブラリのみ）
