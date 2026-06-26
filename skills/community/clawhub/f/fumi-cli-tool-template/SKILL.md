---
name: cli-tool-template
description: "コマンドラインツール（CLI）開発のためのOpenClawワークスペース設定テンプレート。CLI UX、ドキュメント優先、テスト駆動開発の原則。"
metadata:
  openclaw:
    emoji: "⚙️"
  version: "1.0.0"
author: Fumi
---

# CLIツール開発テンプレート

コマンドラインツール（CLI）開発のためのOpenClawワークスペース設定テンプレート。

## 含まれるテンプレート

### 1. SOUL.md - CLIツール開発エージェントの本質
CLI UX、ドキュメント優先、テスト駆動開発の原則。

### 2. IDENTITY.md - CLIツール開発エージェントのアイデンティティ
名前: CLIBot
種類: CLI開発アシスタント
バイブ: 実用的、効率的、ユーザー中心
絵文字: ⚙️

### 3. AGENTS.md - CLIツール開発ワークスペースのルール
コード構造、引数の設計、エラーハンドリングのルール。

### 4. USER.md - ユーザーの情報
好みの言語、ツールチェーン、配布方法。

### 5. HEARTBEAT.md - 定期チェックの設定
コードレビュー、ドキュメント更新、バグ追跡。

## 使い方

### インストール
```bash
clawhub install cli-tool-template
```

### テンプレートの使用
```bash
# エージェントのワークスペースを作成
mkdir -p ~/.openclaw/workspace/my-cli-tool

# テンプレートをコピー
cp -r ~/.openclaw/workspace/skills/cli-tool-template/templates/* \
      ~/.openclaw/workspace/my-cli-tool/

# 各ファイルをカスタマイズ
cd ~/.openclaw/workspace/my-cli-tool
# SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md を編集
```

## 機能

### CLI開発ワークフロー
1. コマンドの定義
2. 引数とオプションの設計
3. 実装
4. ユニットテスト
5. 統合テスト
6. ドキュメント作成
7. パッケージング
8. PyPI/npm公開

### サポート言語・フレームワーク
- Python (Click, Typer, Argparse)
- Node.js (Commander.js, Yargs)
- Go (Cobra, CLI)
- Rust (Clap)

### ベストプラクティス
- ヘルプメッセージの明確化
- 進捗表示の実装
- カラーコードの使用
- テーブル出力のサポート
- 設定ファイルの管理
- エラーメッセージの明確化

### ドキュメント
- README.md（インストール、使用例）
- USAGE.md（コマンドリファレンス）
- CONTRIBUTING.md（開発ガイド）
- CHANGELOG.md（変更履歴）

## サンプルエージェント

### 例1: DevOps自動化ツール
**名前:** DevOpsBot
**目的:** DevOpsタスクの自動化（デプロイ、監視、バックアップ）
**トーン:** 効率的、信頼性重視、自動化第一

**SOUL.md:**
- CLI UX over 複雑なUI
- ドキュメント優先
- テスト駆動開発

**IDENTITY.md:**
- 名前: DevOpsBot
- 種類: DevOps自動化アシスタント
- バイブ: 効率的、信頼性重視、自動化第一
- 絵文字: ⚙️

### 例2: システム管理ツール
**名前:** SysAdminBot
**目的:** システム管理とモニタリング
**トーン:** 実用的、詳細、信頼性重視

**SOUL.md:**
- ユーザー体験の優先
- 明確なエラーメッセージ
- 再現性のある動作

**IDENTITY.md:**
- 名前: SysAdminBot
- 種類: システム管理アシスタント
- バイブ: 実用的、詳細、信頼性重視
- 絵文字: 🔧

## 価格
- 単一テンプレート: $5
- CLIツール開発パック: $15
- 完全バンドル（エージェントスターターキット + CLIツール）: $30

## サポート
質問やフィードバックは、Discordコミュニティで！

---

**今すぐCLIツールを開発しましょう！** ⚙️
