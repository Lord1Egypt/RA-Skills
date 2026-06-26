---
name: web-app-template
description: "Webアプリケーション開発のためのOpenClawワークスペース設定テンプレート。ユーザー体験（UX）優先、レスポンシブデザイン、パフォーマンスの原則。"
metadata:
  openclaw:
    emoji: "🌐"
  version: "1.0.0"
author: Fumi
---

# Webアプリ開発テンプレート

Webアプリケーション開発のためのOpenClawワークスペース設定テンプレート。

## 含まれるテンプレート

### 1. SOUL.md - Web開発エージェントの本質
ユーザー体験（UX）優先、レスポンシブデザイン、パフォーマンスの原則。

### 2. IDENTITY.md - Web開発エージェントのアイデンティティ
名前: WebBot
種類: Web開発アシスタント
バイブ: 現代的、効率的、ユーザー中心
絵文字: 🌐

### 3. AGENTS.md - Web開発ワークスペースのルール
コード構造、API設計、ステート管理のルール。

### 4. USER.md - ユーザーの情報
好みの技術スタック、デプロイ方法、デザイン好み。

### 5. HEARTBEAT.md - 定期チェックの設定
コードレビュー、パフォーマンス監視、バグ追跡。

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

## 機能

### Web開発ワークフロー
1. 要件定義
2. デザインとプロトタイピング
3. フロントエンド開発
4. バックエンド開発
5. API統合
6. テスト
7. デプロイ
8. モニタリング

### サポート技術スタック

#### フロントエンド
- React / Next.js
- Vue.js / Nuxt.js
- Svelte / SvelteKit
- Angular
- Tailwind CSS
- shadcn/ui

#### バックエンド
- Node.js (Express, Fastify)
- Python (FastAPI, Django, Flask)
- Go (Gin, Echo)
- Rust (Actix, Axum)

#### データベース
- PostgreSQL
- MySQL / MariaDB
- MongoDB
- Redis

#### デプロイ
- Vercel / Netlify
- AWS / GCP / Azure
- Docker / Kubernetes

### ベストプラクティス
- コンポーネント駆動開発
- API設計（REST/GraphQL）
- 認証・認可
- エラーハンドリング
- ログ管理
- パフォーマンス最適化
- SEO最適化
- アクセシビリティ

### ドキュメント
- README.md（インストール、実行、デプロイ）
- API.md（APIリファレンス）
- ARCHITECTURE.md（アーキテクチャ）
- DEPLOYMENT.md（デプロイガイド）

## サンプルエージェント

### 例1: SaaSプロダクト開発
**名前:** SaaSDevBot
**目的:** SaaSプロダクトの開発とデプロイ
**トーン:** 現代的、スケーラブル、ユーザー中心

**SOUL.md:**
- ユーザー体験の優先
- レスポンシブデザイン
- パフォーマンス重視

**IDENTITY.md:**
- 名前: SaaSDevBot
- 種類: SaaS開発アシスタント
- バイブ: 現代的、スケーラブル、ユーザー中心
- 絵文字: 🌐

### 例2: Eコマースサイト開発
**名前:** EcommerceBot
**目的:** Eコマースサイトの開発と最適化
**トーン:** 転換率重視、ユーザビリティ、SEO

**SOUL.md:**
- 転換率の最適化
- ユーザビリティの確保
- SEOとパフォーマンス

**IDENTITY.md:**
- 名前: EcommerceBot
- 種類: Eコマース開発アシスタント
- バイブ: 転換率重視、ユーザビリティ、SEO
- 絵文字: 🛒

## 価格
- 単一テンプレート: $5
- Webアプリ開発パック: $15
- 完全バンドル（エージェントスターターキット + Webアプリ）: $30

## サポート
質問やフィードバックは、Discordコミュニティで！

---

**今すぐWebアプリを開発しましょう！** 🌐
