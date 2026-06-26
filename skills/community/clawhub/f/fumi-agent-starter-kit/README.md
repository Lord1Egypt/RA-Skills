# エージェントスターターキット

OpenClawエージェントを構築するための完全なスターターキット。

## 機能
- SOUL.md - エージェントの本質
- IDENTITY.md - エージェントのアイデンティティ
- AGENTS.md - ワークスペースのルール
- USER.md - ユーザーの情報
- HEARTBEAT.md - 定期チェックの設定

## 使い方

### インストール
```bash
clawhub install agent-starter-kit
```

### テンプレートの使用
```bash
# エージェントのワークスペースを作成
mkdir -p ~/.openclaw/workspace/my-agent

# テンプレートをコピー
cp -r ~/.openclaw/workspace/skills/agent-starter-kit/templates/* \
      ~/.openclaw/workspace/my-agent/

# 各ファイルをカスタマイズ
cd ~/.openclaw/workspace/my-agent
# SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md を編集
```

### エージェントの起動
```bash
# OpenClawでエージェントを起動
openclaw agent start --workspace ~/.openclaw/workspace/my-agent
```

## テンプレートの詳細

### SOUL.md
エージェントの性格、運営原則、振る舞い方を定義します。

### IDENTITY.md
エージェントの名前、種類、バイブ、絵文字などを定義します。

### AGENTS.md
エージェントの運営方法、メモリ管理、ツール使用などのルールを定義します。

### USER.md
ユーザーの名前、タイムゾーン、システム、言語などの情報を定義します。

### HEARTBEAT.md
エージェントの定期チェックタスクを設定します。

## サンプルエージェント

### プロダクティビティアシスタント
- 名前: TaskBot
- 目的: タスク管理と生産性向上
- トーン: 効率的、励まし

### コードレビューアシスタント
- 名前: CodeReviewBot
- 目的: コード品質の向上
- トーン: 建設的、厳格

詳細は SKILL.md を参照してください。

## 価格
- 単一テンプレート: $5
- エージェントテンプレートパック: $20

## サポート
質問やフィードバックは、Discordコミュニティで！

## ライセンス
MIT License
