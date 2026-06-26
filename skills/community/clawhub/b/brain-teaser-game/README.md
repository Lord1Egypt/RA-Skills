# 🧠 Brain Teaser Game Skill

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://openclaw.ai)
[![Python 3](https://img.shields.io/badge/Python-3.6+-green.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-Published-purple.svg)](https://clawhub.com)

> 🎮 Multi-language Brain Teaser Interactive Game - OpenClaw Skill

---

## 🇨🇳 中文 | 🇺🇸 English | 🇯🇵 日本語

---

### 🇨🇳 中文

一个支持中文、英文、日语的脑筋急转弯互动游戏 OpenClaw Skill，拥有 600+ 题库。

## ✨ 特性

- 🌍 **多语言支持** - 自动检测用户语言（中文/英文/日语）
- 📚 **600+ 题库** - 每种语言 200 道精选题目
- 🎲 **随机出题** - 智能随机抽取题目
- 💡 **提示系统** - 提供递进式提示帮助思考
- ✅ **智能匹配** - 支持模糊答案匹配
- 🔄 **历史记录** - 做过的题目不会重复出现
- 🤖 **AI 扩展** - 可选的 AI 动态生成新题功能

## 🚀 快速开始

### 安装

#### 方式一：通过 ClawHub 安装（推荐）

```bash
clawhub search brain-teaser-game
clawhub install brain-teaser-game
```

#### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/你的用户名/brain-teaser-game-skill.git

# 复制到 OpenClaw Skills 目录
cp -r brain-teaser-game-skill ~/.openclaw/skills/
```

### 使用方法

```bash
# 开始游戏
./invoke.sh start "来个脑筋急转弯"
```

#### 游戏中操作

| 操作 | 命令 |
|------|------|
| 回答 | 直接输入答案 |
| 提示 | 输入"提示" |
| 答案 | 输入"答案" |
| 下一题 | 输入"下一题" |

## 📖 命令参考

```bash
# 开始新游戏
./invoke.sh start "用户输入"

# 提交答案
./invoke.sh answer <session_id> "你的答案"

# 获取提示
./invoke.sh hint <session_id>

# 查看答案
./invoke.sh reveal <session_id>

# 下一题
./invoke.sh next <session_id>

# 交互模式（自动检测意图）
./invoke.sh interactive <session_id> "提示"
./invoke.sh interactive <session_id> "你的答案"

# 重置历史记录
./invoke.sh reset-history

# 查看状态
./invoke.sh status
```

## 📊 题库统计

| 语言 | 题目数 | 难度分布 |
|------|--------|---------|
| 中文 | 200 | 简单 160 / 中等 40 |
| English | 200 | Easy 160 / Medium 40 |
| 日本語 | 200 | 簡単 160 / 普通 40 |

## 🎮 示例对话

```
用户：来个脑筋急转弯
Skill：## 🧠 脑筋急转弯
       **题目**：什么东西越洗越脏？
       ---
       - 直接回答
       - 输入"提示"获取提示

用户：提示
Skill：**提示**：生活中最常见的液体

用户：水
Skill：✅ 正确！
       **答案**：水
       **解释**：水洗东西会带走污垢，因此越洗越脏。
```

## 🤖 AI 动态生成（可选）

当基础题库用完时，可以配置 AI 自动生成新题目。

```bash
# 环境变量配置
export BRAIN_TEASER_API_KEY=your-api-key
export BRAIN_TEASER_API_BASE=https://api.example.com/v1  # 可选
export BRAIN_TEASER_MODEL=gpt-4  # 可选
```

### 配置读取优先级

1. 环境变量 `BRAIN_TEASER_API_KEY`
2. `~/.claude/settings.json`
3. `~/.openclaw/openclaw.json`

### 支持的 API

- OpenAI API
- 智谱 AI (GLM)
- DeepSeek
- 其他兼容 OpenAI 格式的 API

## 📁 文件结构

```
brain-teaser-game-skill/
├── SKILL.md           # Skill 定义（含 YAML frontmatter）
├── _meta.json         # 元数据配置
├── invoke.sh          # Bash 入口脚本
├── invoke.py          # 核心实现
├── language.py        # 语言检测模块
├── answer.py          # 答案判断模块
├── session.py         # 会话管理模块
├── ai_generator.py    # AI 题目生成器
├── README.md          # 本文件
├── LICENSE            # MIT License
├── .gitignore         # Git 忽略规则
└── data/
    ├── zh.json        # 中文题库 (200题)
    ├── en.json        # 英文题库 (200题)
    └── ja.json        # 日文题库 (200题)
```

## 🔧 依赖

- **Python 3.6+**
- **无外部依赖** - 仅使用 Python 标准库

## 🛠️ 开发

### 运行测试

```bash
# 测试语言检测
python3 language.py

# 测试答案判断
python3 answer.py

# 测试会话管理
python3 session.py
```

### 添加新题目

编辑 `data/{lang}.json` 文件：

```json
{
  "id": 201,
  "question": "问题内容",
  "answer": "答案",
  "hint": "提示",
  "explain": "解释",
  "difficulty": 1
}
```

## 📝 数据存储

- **位置**: `~/.cache/brain-teaser/`
- **会话文件**: `sessions/{session_id}.json`
- **历史记录**: `history.json`

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

### 🇺🇸 English

A multi-language brain teaser interactive game OpenClaw Skill supporting Chinese, English, and Japanese with 600+ questions.

## ✨ Features

- 🌍 **Multi-language Support** - Auto-detect user language (Chinese/English/Japanese)
- 📚 **600+ Questions** - 200 curated questions per language
- 🎲 **Random Selection** - Smart random question picking
- 💡 **Hint System** - Progressive hints to help thinking
- ✅ **Smart Matching** - Fuzzy answer matching support
- 🔄 **History Tracking** - No repeated questions
- 🤖 **AI Extension** - Optional AI dynamic question generation

## 🚀 Quick Start

### Installation

#### Option 1: Install via ClawHub (Recommended)

```bash
clawhub search brain-teaser-game
clawhub install brain-teaser-game
```

#### Option 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/your-username/brain-teaser-game-skill.git

# Copy to OpenClaw Skills directory
cp -r brain-teaser-game-skill ~/.openclaw/skills/
```

### Usage

```bash
# Start game
./invoke.sh start "Give me a brain teaser"
```

#### In-Game Operations

| Action | Command |
|--------|---------|
| Answer | Type your answer directly |
| Hint | Type "hint" |
| Reveal Answer | Type "answer" |
| Next Question | Type "next" |

## 📖 Command Reference

```bash
# Start new game
./invoke.sh start "user input"

# Submit answer
./invoke.sh answer <session_id> "your answer"

# Get hint
./invoke.sh hint <session_id>

# Reveal answer
./invoke.sh reveal <session_id>

# Next question
./invoke.sh next <session_id>

# Interactive mode (auto-detect intent)
./invoke.sh interactive <session_id> "hint"
./invoke.sh interactive <session_id> "your answer"

# Reset history
./invoke.sh reset-history

# Check status
./invoke.sh status
```

## 📊 Question Statistics

| Language | Questions | Difficulty |
|----------|-----------|------------|
| 中文 | 200 | Easy 160 / Medium 40 |
| English | 200 | Easy 160 / Medium 40 |
| 日本語 | 200 | Easy 160 / Medium 40 |

## 🎮 Example Conversation

```
User: Give me a brain teaser
Skill: ## 🧠 Brain Teaser
       **Question**: What has keys but can't open locks?
       ---
       - Answer directly
       - Type 'hint' for a hint

User: piano
Skill: ✅ Correct!
       **Answer**: piano
       **Explanation**: A piano has keys but they are for playing music.
```

## 🤖 AI Dynamic Generation (Optional)

Configure AI to auto-generate new questions when the base pool is exhausted.

```bash
# Environment variable configuration
export BRAIN_TEASER_API_KEY=your-api-key
export BRAIN_TEASER_API_BASE=https://api.example.com/v1  # optional
export BRAIN_TEASER_MODEL=gpt-4  # optional
```

### Configuration Priority

1. Environment variable `BRAIN_TEASER_API_KEY`
2. `~/.claude/settings.json`
3. `~/.openclaw/openclaw.json`

### Supported APIs

- OpenAI API
- Zhipu AI (GLM)
- DeepSeek
- Other OpenAI-compatible APIs

## 📁 File Structure

```
brain-teaser-game-skill/
├── SKILL.md           # Skill definition (with YAML frontmatter)
├── _meta.json         # Metadata configuration
├── invoke.sh          # Bash entry script
├── invoke.py          # Core implementation
├── language.py        # Language detection module
├── answer.py          # Answer matching module
├── session.py         # Session management module
├── ai_generator.py    # AI question generator
├── README.md          # This file
├── LICENSE            # MIT License
├── .gitignore         # Git ignore rules
└── data/
    ├── zh.json        # Chinese questions (200)
    ├── en.json        # English questions (200)
    └── ja.json        # Japanese questions (200)
```

## 🔧 Dependencies

- **Python 3.6+**
- **No external dependencies** - Uses only Python standard library

## 🛠️ Development

### Running Tests

```bash
# Test language detection
python3 language.py

# Test answer matching
python3 answer.py

# Test session management
python3 session.py
```

### Adding New Questions

Edit `data/{lang}.json` files:

```json
{
  "id": 201,
  "question": "Question content",
  "answer": "Answer",
  "hint": "Hint",
  "explain": "Explanation",
  "difficulty": 1
}
```

## 📝 Data Storage

- **Location**: `~/.cache/brain-teaser/`
- **Session files**: `sessions/{session_id}.json`
- **History**: `history.json`

## 🤝 Contributing

Issues and Pull Requests are welcome!

1. Fork this repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Create Pull Request

---

### 🇯🇵 日本語

中国語、英語、日本語に対応したなぞなぞインタラクティブゲーム OpenClaw Skill。600問以上の問題を収録。

## ✨ 機能

- 🌍 **多言語対応** - ユーザーの言語を自動検出（中国語/英語/日本語）
- 📚 **600問以上** - 各言語200問の厳選問題
- 🎲 **ランダム出題** - スマートなランダム問題選択
- 💡 **ヒント機能** - 思考を助ける段階的なヒント
- ✅ **スマートマッチング** - 曖昧な回答にも対応
- 🔄 **履歴管理** - 出題済みの問題は再表示されません
- 🤖 **AI拡張** - オプションのAI動的問題生成機能

## 🚀 はじめに

### インストール

#### 方法1：ClawHub経由でインストール（推奨）

```bash
clawhub search brain-teaser-game
clawhub install brain-teaser-game
```

#### 方法2：手動インストール

```bash
# リポジトリをクローン
git clone https://github.com/your-username/brain-teaser-game-skill.git

# OpenClaw Skillsディレクトリにコピー
cp -r brain-teaser-game-skill ~/.openclaw/skills/
```

### 使い方

```bash
# ゲーム開始
./invoke.sh start "なぞなぞをください"
```

#### ゲーム中の操作

| 操作 | コマンド |
|------|----------|
| 回答 | 答えを直接入力 |
| ヒント | 「ヒント」と入力 |
| 答えを見る | 「答え」と入力 |
| 次の問題 | 「次」と入力 |

## 📖 コマンドリファレンス

```bash
# 新しいゲームを開始
./invoke.sh start "ユーザー入力"

# 回答を送信
./invoke.sh answer <session_id> "あなたの答え"

# ヒントを取得
./invoke.sh hint <session_id>

# 答えを表示
./invoke.sh reveal <session_id>

# 次の問題
./invoke.sh next <session_id>

# インタラクティブモード（意図を自動検出）
./invoke.sh interactive <session_id> "ヒント"
./invoke.sh interactive <session_id> "あなたの答え"

# 履歴をリセット
./invoke.sh reset-history

# ステータス確認
./invoke.sh status
```

## 📊 問題数統計

| 言語 | 問題数 | 難易度 |
|------|--------|--------|
| 中文 | 200 | 簡単 160 / 普通 40 |
| English | 200 | Easy 160 / Medium 40 |
| 日本語 | 200 | 簡単 160 / 普通 40 |

## 🎮 会話例

```
ユーザー：なぞなぞをください
Skill：## 🧠 なぞなぞ
       **問題**：鍵があるのに、鍵を開けられないものは何？
       ---
       - 直接回答
       - 「ヒント」でヒントを取得

ユーザー：ピアノ
Skill：✅ 正解！
       **答え**：ピアノ
       **解説**：ピアノには鍵盤（キー）がありますが、鍵を開けることはできません。
```

## 🤖 AI動的生成（オプション）

基本問題が尽きた場合、AIが自動的に新しい問題を生成するよう設定できます。

```bash
# 環境変数の設定
export BRAIN_TEASER_API_KEY=your-api-key
export BRAIN_TEASER_API_BASE=https://api.example.com/v1  # オプション
export BRAIN_TEASER_MODEL=gpt-4  # オプション
```

### 設定優先順位

1. 環境変数 `BRAIN_TEASER_API_KEY`
2. `~/.claude/settings.json`
3. `~/.openclaw/openclaw.json`

### 対応API

- OpenAI API
- Zhipu AI (GLM)
- DeepSeek
- その他OpenAI互換API

## 📁 ファイル構成

```
brain-teaser-game-skill/
├── SKILL.md           # Skill定義（YAML frontmatter付き）
├── _meta.json         # メタデータ設定
├── invoke.sh          # Bashエントリスクリプト
├── invoke.py          # コア実装
├── language.py        # 言語検出モジュール
├── answer.py          # 回答判定モジュール
├── session.py         # セッション管理モジュール
├── ai_generator.py    # AI問題ジェネレーター
├── README.md          # このファイル
├── LICENSE            # MIT License
├── .gitignore         # Git無視ルール
└── data/
    ├── zh.json        # 中国語問題 (200問)
    ├── en.json        # 英語問題 (200問)
    └── ja.json        # 日本語問題 (200問)
```

## 🔧 依存関係

- **Python 3.6+**
- **外部依存なし** - Python標準ライブラリのみ使用

## 🛠️ 開発

### テスト実行

```bash
# 言語検出テスト
python3 language.py

# 回答判定テスト
python3 answer.py

# セッション管理テスト
python3 session.py
```

### 新しい問題の追加

`data/{lang}.json` ファイルを編集：

```json
{
  "id": 201,
  "question": "問題内容",
  "answer": "答え",
  "hint": "ヒント",
  "explain": "解説",
  "difficulty": 1
}
```

## 📝 データ保存

- **場所**: `~/.cache/brain-teaser/`
- **セッションファイル**: `sessions/{session_id}.json`
- **履歴**: `history.json`

## 🤝 貢献

Issue や Pull Request をお待ちしています！

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. Pull Request を作成

---

## 📄 License

[MIT License](LICENSE)

## 🔗 Links

- [OpenClaw](https://openclaw.ai)
- [ClawHub](https://clawhub.com)
- [OpenClaw Docs](https://docs.openclaw.ai)

---

Made with ❤️ for OpenClaw
