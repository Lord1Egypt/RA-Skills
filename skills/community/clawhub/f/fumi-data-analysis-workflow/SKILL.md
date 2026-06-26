---
name: data-analysis-workflow
description: "データ分析プロジェクトのためのOpenClawワークスペース設定テンプレート。データ駆動の意思決定、探索的データ分析（EDA）、モデル開発の原則。"
metadata:
  openclaw:
    emoji: "📊"
  version: "1.0.0"
author: Fumi
---

# データ分析ワークフローテンプレート

データ分析プロジェクトのためのOpenClawワークスペース設定テンプレート。

## 含まれるテンプレート

### 1. SOUL.md - データ分析エージェントの本質
データ駆動の意思決定、探索的データ分析（EDA）、モデル開発の原則。

### 2. IDENTITY.md - データ分析エージェントのアイデンティティ
名前: DataBot
種類: データ分析アシスタント
バイブ: 分析的、詳細、実践的
絵文字: 📊

### 3. AGENTS.md - データ分析ワークスペースのルール
データ管理、再現性、実験記録のルール。

### 4. USER.md - ユーザーの情報
専門分野、ツールの好み、分析の目的。

### 5. HEARTBEAT.md - 定期チェックの設定
データの更新、実験の進捗、結果の記録。

## 使い方

### インストール
```bash
clawhub install data-analysis-workflow
```

### テンプレートの使用
```bash
# エージェントのワークスペースを作成
mkdir -p ~/.openclaw/workspace/my-data-analysis

# テンプレートをコピー
cp -r ~/.openclaw/workspace/skills/data-analysis-workflow/templates/* \
      ~/.openclaw/workspace/my-data-analysis/

# 各ファイルをカスタマイズ
cd ~/.openclaw/workspace/my-data-analysis
# SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md を編集
```

## 機能

### データ分析ワークフロー
1. データ収集
2. データクレンジング
3. 探索的データ分析（EDA）
4. 特徴エンジニアリング
5. モデル開発
6. モデル評価
7. 結果の可視化
8. 結果の報告

### ツール統合
- Python (Pandas, NumPy, Scikit-learn)
- SQL
- Jupyter Notebook
- Matplotlib, Seaborn, Plotly
- MLflow (実験記録)

### ドキュメント
- データ辞書
- EDAノートブック
- モデル仕様書
- 結果報告書

## サンプルエージェント

### 例1: マーケティングデータアナリスト
**名前:** MarketingDataBot
**目的:** マーケティングデータの分析とインサイトの提供
**トーン:** 分析的、実用的、ビジネス中心

**SOUL.md:**
- データ駆動の意思決定を優先
- 明確なインサイトを提供
- 再現性を重視

**IDENTITY.md:**
- 名前: MarketingDataBot
- 種類: マーケティングデータ分析アシスタント
- バイブ: 分析的、実用的、ビジネス中心
- 絵文字: 📊

### 例2: 機械学習エンジニア
**名前:** MLEngineeringBot
**目的:** 機械学習モデルの開発とデプロイ
**トーン:** 技術的、詳細、実践的

**SOUL.md:**
- モデル品質 over スピード
- 再現性とドキュメントを重視
- ベストプラクティスを適用

**IDENTITY.md:**
- 名前: MLEngineeringBot
- 種類: 機械学習エンジニアリングアシスタント
- バイブ: 技術的、詳細、実践的
- 絵文字: 🤖

## 価格
- 単一テンプレート: $5
- データ分析ワークフローパック: $15
- 完全バンドル（エージェントスターターキット + データ分析）: $30

## サポート
質問やフィードバックは、Discordコミュニティで！

---

**今すぐデータ分析エージェントを構築しましょう！** 📊
