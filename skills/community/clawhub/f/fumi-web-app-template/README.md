# Webアプリ開発テンプレート

Webアプリケーション開発のためのOpenClawワークスペース設定テンプレート。

## 機能
- SOUL.md - UX優先、レスポンシブデザイン、パフォーマンスの原則
- IDENTITY.md - Web開発アシスタントのアイデンティティ
- AGENTS.md - コード構造、API設計、ステート管理のルール
- USER.md - ユーザーの好みの技術スタック、デプロイ方法
- HEARTBEAT.md - コードレビュー、パフォーマンス監視、バグ追跡

## 使い方

### インストール
```bash
clawhub install web-app-template
```

### テンプレートの使用
```bash
# エージェントのワークスペースを作成
mkdir -p ~/.openclaw/workspace/my-web-app

# テンプレートをコピー
cp -r ~/.openclaw/workspace/skills/web-app-template/templates/* \
      ~/.openclaw/workspace/my-web-app/

# 各ファイルをカスタマイズ
cd ~/.openclaw/workspace/my-web-app
# SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md を編集
```

## テンプレートの詳細

### SOUL.md
ユーザー体験（UX）優先、レスポンシブデザイン、パフォーマンスの原則を定義します。

### IDENTITY.md
Web開発アシスタントの名前、種類、バイブ、絵文字などを定義します。

### AGENTS.md
コード構造、API設計、ステート管理などのルールを定義します。

### USER.md
ユーザーの好みの技術スタック、デプロイ方法、デザイン好みなどを定義します。

### HEARTBEAT.md
コードレビュー、パフォーマンス監視、バグ追跡などの定期チェックを設定します。

## Web開発ワークフロー
1. 要件定義
2. デザインとプロトタイピング
3. フロントエンド開発
4. バックエンド開発
5. API統合
6. テスト
7. デプロイ
8. モニタリング

## サポート技術スタック

### フロントエンド
- React / Next.js
- Vue.js / Nuxt.js
- Svelte / SvelteKit
- Angular
- Tailwind CSS
- shadcn/ui

### バックエンド
- Node.js (Express, Fastify)
- Python (FastAPI, Django, Flask)
- Go (Gin, Echo)
- Rust (Actix, Axum)

### データベース
- PostgreSQL
- MySQL / MariaDB
- MongoDB
- Redis

### デプロイ
- Vercel / Netlify
- AWS / GCP / Azure
- Docker / Kubernetes

## ベストプラクティス

### コンポーネント駆動開発
- 再利用可能なコンポーネント
- コンポジションパターン
- Propsとステート管理

### API設計
- RESTfulまたはGraphQL
- 明確なエンドポイント
- 一貫したレスポンス形式
- エラーハンドリング

### 認証・認可
- JWTまたはOAuth2
- セッション管理
- ロールベースのアクセス制御

### エラーハンドリング
- グローバルエラーハンドリング
- ユーザーへの明確なエラーメッセージ
- ログ記録

### ログ管理
- 構造化されたログ
- ログレベルの使用
- エラー追跡

### パフォーマンス最適化
- コード分割と遅延ロード
- 画像の最適化
- キャッシング戦略
- CDNの使用

### SEO最適化
- メタタグ
- サイトマップ
- 構造化データ
- Lighthouseスコア

### アクセシビリティ
- ARIA属性
- キーボードナビゲーション
- スクリーンリーダー対応
- カラーコントラスト

## ドキュメント

### README.md
- インストール方法
- 実行方法
- デプロイ手順
- 環境変数

### API.md
- 全エンドポイントのリファレンス
- リクエスト・レスポンスの例
- 認証方法

### ARCHITECTURE.md
- システムアーキテクチャ
- データフロー
- 技術スタック

### DEPLOYMENT.md
- デプロイ手順
- 環境設定
- CI/CDパイプライン

## サンプルエージェント

### SaaSプロダクト開発
- 名前: SaaSDevBot
- 目的: SaaSプロダクトの開発とデプロイ
- トーン: 現代的、スケーラブル、ユーザー中心

### Eコマースサイト開発
- 名前: EcommerceBot
- 目的: Eコマースサイトの開発と最適化
- トーン: 転換率重視、ユーザビリティ、SEO

詳細は SKILL.md を参照してください。

## 価格
- 単一テンプレート: $5
- Webアプリ開発パック: $15
- 完全バンドル（エージェントスターターキット + Webアプリ）: $30

## サポート
質問やフィードバックは、Discordコミュニティで！

## ライセンス
MIT License
