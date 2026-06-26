# CLIツール開発テンプレート

コマンドラインツール（CLI）開発のためのOpenClawワークスペース設定テンプレート。

## 機能
- SOUL.md - CLI UX、ドキュメント優先、テスト駆動開発の原則
- IDENTITY.md - CLI開発アシスタントのアイデンティティ
- AGENTS.md - コード構造、引数設計、エラーハンドリングのルール
- USER.md - ユーザーの好みの言語、ツールチェーン
- HEARTBEAT.md - コードレビュー、ドキュメント更新、バグ追跡

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

## テンプレートの詳細

### SOUL.md
CLI UX、ドキュメント優先、テスト駆動開発の原則を定義します。

### IDENTITY.md
CLI開発アシスタントの名前、種類、バイブ、絵文字などを定義します。

### AGENTS.md
コード構造、引数とオプションの設計、エラーハンドリングなどのルールを定義します。

### USER.md
ユーザーの好みの言語、ツールチェーン、配布方法などを定義します。

### HEARTBEAT.md
コードレビュー、ドキュメント更新、バグ追跡などの定期チェックを設定します。

## CLI開発ワークフロー
1. コマンドの定義
2. 引数とオプションの設計
3. 実装
4. ユニットテスト
5. 統合テスト
6. ドキュメント作成
7. パッケージング
8. PyPI/npm公開

## サポート言語・フレームワーク

### Python
- Click
- Typer
- Argparse

### Node.js
- Commander.js
- Yargs

### Go
- Cobra
- CLI

### Rust
- Clap

## ベストプラクティス

### ヘルプメッセージ
- 明確で簡潔
- 使用例を含める
- 必須引数とオプションを区別

### 進捗表示
- 実行中のタスクを表示
- 完了状況を通知
- エラー時の明確なメッセージ

### 出力形式
- カラーコードの使用
- テーブル出力のサポート
- JSON出力のオプション

### エラーハンドリング
- 明確なエラーメッセージ
- 適切な終了コード
- トラブルシューティングのヒント

## ドキュメント

### README.md
- インストール方法
- 使用例
- 高度な機能

### USAGE.md
- 全コマンドのリファレンス
- 引数とオプションの説明
- 使用例

### CONTRIBUTING.md
- 開発環境のセットアップ
- コードの構成
- テストの実行方法

### CHANGELOG.md
- 変更履歴
- バージョンごとの新機能
- 破壊的変更

## サンプルエージェント

### DevOps自動化ツール
- 名前: DevOpsBot
- 目的: DevOpsタスクの自動化
- トーン: 効率的、信頼性重視、自動化第一

### システム管理ツール
- 名前: SysAdminBot
- 目的: システム管理とモニタリング
- トーン: 実用的、詳細、信頼性重視

詳細は SKILL.md を参照してください。

## 価格
- 単一テンプレート: $5
- CLIツール開発パック: $15
- 完全バンドル（エージェントスターターキット + CLIツール）: $30

## サポート
質問やフィードバックは、Discordコミュニティで！

## ライセンス
MIT License
