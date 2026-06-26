# データ分析ワークフローテンプレート

データ分析プロジェクトのためのOpenClawワークスペース設定テンプレート。

## 機能
- SOUL.md - データ駆動の意思決定、EDA、モデル開発の原則
- IDENTITY.md - データ分析エージェントのアイデンティティ
- AGENTS.md - データ管理、再現性、実験記録のルール
- USER.md - ユーザーの専門分野、ツールの好み
- HEARTBEAT.md - データ更新、実験進捗、結果記録の設定

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

## テンプレートの詳細

### SOUL.md
データ駆動の意思決定、探索的データ分析（EDA）、モデル開発の原則を定義します。

### IDENTITY.md
データ分析エージェントの名前、種類、バイブ、絵文字などを定義します。

### AGENTS.md
データ管理、再現性、実験記録などのルールを定義します。

### USER.md
ユーザーの専門分野、ツールの好み、分析の目的などを定義します。

### HEARTBEAT.md
データの更新、実験の進捗、結果の記録などの定期チェックを設定します。

## データ分析ワークフロー
1. データ収集
2. データクレンジング
3. 探索的データ分析（EDA）
4. 特徴エンジニアリング
5. モデル開発
6. モデル評価
7. 結果の可視化
8. 結果の報告

## ツール統合
- Python (Pandas, NumPy, Scikit-learn)
- SQL
- Jupyter Notebook
- Matplotlib, Seaborn, Plotly
- MLflow (実験記録)

## サンプルエージェント

### マーケティングデータアナリスト
- 名前: MarketingDataBot
- 目的: マーケティングデータの分析とインサイトの提供
- トーン: 分析的、実用的、ビジネス中心

### 機械学習エンジニア
- 名前: MLEngineeringBot
- 目的: 機械学習モデルの開発とデプロイ
- トーン: 技術的、詳細、実践的

詳細は SKILL.md を参照してください。

## 価格
- 単一テンプレート: $5
- データ分析ワークフローパック: $15
- 完全バンドル（エージェントスターターキット + データ分析）: $30

## サポート
質問やフィードバックは、Discordコミュニティで！

## ライセンス
MIT License
