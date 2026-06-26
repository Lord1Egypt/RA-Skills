# Flova Video Generator -- OpenClaw Skill

[English](README.md) | [中文](README.zh-CN.md) | **日本語**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skill Version](https://img.shields.io/badge/skill_version-0.2.9-green.svg)](SKILL.md)
[![ClawHub](https://img.shields.io/badge/ClawHub-marketplace-brightgreen.svg)](https://clawhub.com)
[![Flova](https://img.shields.io/badge/Flova-video_platform-00bcd4.svg)](https://www.flova.ai)

AI エージェントが [Flova](https://www.flova.ai) を通じて動画の作成・編集・エクスポートを行えるようにする [OpenClaw](https://openclaw.ai) スキルプラグインです。Flova は世界初のオールインワン AI 動画制作プラットフォームで、構想・絵コンテ・撮影・編集を統合し、クリエイティビティを自由に表現できます。

> *誰もが自分自身のクリエイティブディレクター -- 素晴らしいストーリーを手軽に創作。*

**対応ツール：** OpenClaw | Claude Code | Codex | Cursor | Windsurf | Cline | その他

## 概要

これは [OpenClaw](https://openclaw.ai) スキル -- AI エージェントに Flova API を呼び出す能力を与える Markdown ベースの指示ファイルです。スキルを読み込むと、AI アシスタントが動画プロジェクトの作成、クリエイティブな指示の送信、ファイルアップロード、完成動画のエクスポート、サブスクリプション管理をすべて自然な会話で行えるようになります。ツール使用や URL 取得に対応するすべての AI コーディングアシスタントで動作します。

## インストール

### ClawHub 経由（推奨）

[ClawHub](https://clawhub.com) で **flova** を検索してインストールをクリック。

### AI アシスタントに直接伝える

以下のメッセージを AI アシスタントに直接送信してください：

> https://s.flova.ai/SKILL.md を読んで、Skill の手順に従って動画を作成してください。

### 手動インストール

`SKILL.md` をダウンロードしてプロジェクトのスキルディレクトリに配置：

```bash
curl -o SKILL.md https://s.flova.ai/SKILL.md
```

## クイックスタート

1. **API Token を取得：** [flova.ai/openclaw](https://www.flova.ai/openclaw/?action=token) にアクセス
2. **環境変数を設定：**
   ```bash
   export FLOVA_API_TOKEN="your_token_here"
   ```
3. **作成開始：** AI アシスタントに作りたい動画を伝えましょう！

## 機能

- **自然言語での動画作成** -- やりたいことを説明するだけで動画を生成
- **ファイルアップロード** -- 画像、動画、音声、ドキュメントに対応
- **エクスポートとダウンロード** -- 完成した動画のエクスポートとプロジェクト素材のダウンロード
- **プロジェクト管理** -- 動画プロジェクトの一覧表示、再開、切り替え
- **サブスクリプションとクレジット** -- ステータス確認、プラン登録、クレジット購入

## ワークフロー概要

```
プロジェクト作成 -> チャット（動画の説明） -> ストリーミング応答（SSE）
    -> 動画エクスポート -> ステータスポーリング -> 動画 URL 取得
```

すべてのクリエイティブなやり取り（スクリプト作成、モデル選択、絵コンテ編集など）は対話型の `/chat` エンドポイントを通じて行われます -- 別のエンドポイントは不要です。

## リポジトリ構成

| ファイル | 説明 |
|---|---|
| `SKILL.md` | API リファレンスとワークフロー手順を含むスキル定義 |
| `api_curl_commands.md` | 手動 API テスト用のデバッグ curl コマンド |
| `LICENSE` | MIT ライセンス |

## API エンドポイント

| エンドポイント | 説明 |
|---|---|
| `POST /user` | ユーザープロフィールとクレジットを取得 |
| `POST /create` | 動画プロジェクトを作成 |
| `POST /projects` | 既存プロジェクトを一覧表示 |
| `POST /project_info` | プロジェクトメタデータと絵コンテを取得 |
| `POST /chat_history` | 会話履歴を取得（ページネーション） |
| `POST /upload` | ファイルをアップロード（画像、動画、音声） |
| `POST /chat` | クリエイティブな指示を送信 |
| `POST /chat_stream` | SSE レスポンスストリームを取得 |
| `POST /export_video` | 動画エクスポートを開始 |
| `POST /export_status` | エクスポート進捗をポーリング |
| `POST /download_all` | プロジェクトリソースをダウンロード |
| `POST /download_status` | ダウンロード進捗をポーリング |
| `POST /products` | 利用可能なプランとクレジットパックを一覧表示 |
| `POST /subscribe` | サブスクリプション決済を開始 |
| `POST /credits_buy` | クレジットを購入 |

## コントリビュート

1. このリポジトリを Fork
2. フィーチャーブランチを作成（`git checkout -b feature/your-change`）
3. 変更をコミットして Pull Request を送信

**注意：** `SKILL.md` は ASCII 文字のみ使用してください。

## リンク

- [Flova プラットフォーム](https://www.flova.ai)
- [料金プラン](https://www.flova.ai/pricing/)
- [ドキュメント](https://www.flova.ai/docs/)
- [Token 管理](https://www.flova.ai/openclaw/?action=token)

## ライセンス

[MIT](LICENSE)
