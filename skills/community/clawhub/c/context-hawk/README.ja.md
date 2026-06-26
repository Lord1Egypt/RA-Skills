# 🦅 Context-Hawk

> **AI コンテキスト記憶ガーディアン** — 追跡を失うことをやめ、重要ことを記憶し始める。

*どの AI agent にも、session をまたぎ、トピックをまたぎ、時間を超えて実際に機能する記憶を。*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-context--hawk-blue)](https://clawhub.com)

**English** | [中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Italiano](README.it.md) | [Русский](README.ru.md) | [Português (Brasil)](README.pt-BR.md)

---

## 何をするのか？

ほとんどの AI agent は**健忘症**に苦しんでいます — 新しい session が開始されるたびにゼロから始まります。Context-Hawk は、本番対応の記憶管理システムでこれ問題を解決します。重要なことを自動的に捕捉し、ノイズを忘れさせ、正しい時間に正しい記憶を思い出させます。

**Context-Hawk なし：**
> "もう言いましたよね — 簡潔な返信が好きだって！"
>（次の session、agent はまた忘れる）

**Context-Hawk あり：**
>（session 1 から静かにコミュニケーションの好みを適用）
> ✅ 毎回簡潔で直接的な回答を配信

---

## ❌ Context-Hawk なし vs ✅ Context-Hawk あり

| シナリオ | ❌ Context-Hawk なし | ✅ Context-Hawk あり |
|----------|------------------------|---------------------|
| **新しい session の開始** | 空白 — あなたについて何も知らない | ✅ 関連する記憶を自動注入 |
| **ユーザーが好みを繰り返す** | "前に言ったよね..." | 初日から記憶 |
| **長期間のタスクが数日間実行** | 再起動 = 最初から | Task State 持続化、`hawk resume` でシームレス |
| **コンテキストが肥大化** | Token 料金急騰、パフォーマンス低下 | 5つの圧縮戦略で軽量維持 |
| **重複情報** | 同じ事実が10回保存される | SimHash 重複排除 — 1回だけ保存 |
| **記憶のリコール** | 全て類似、繰り返し注入 | MMR 多様なリコール — 繰り返しなし |
| **記憶管理** | 全てが永久に蓄積 | 4層崩壊 — ノイズは消え、 сигナルは残る |
| **自己改善** | 同じミスを繰り返す | importance + access_count 追跡 → スマート促進 |
| **マルチエージェントチーム** | 各エージェントが最初から開始、共有コンテキストなし | 共有記憶（ LanceDB 経由）— 全エージェントが互いに学習 |

---

## 😰 痛点 & 解決策

| 痛点 | 影響 | Context-Hawk 解決策 |
|------|------|----------------------|
| **AI が各 session で忘れる** | ユーザーが同じことを何度も言う必要がある | 4層記憶崩壊 — 重要なコンテンツが自動的に保持 |
| **長時間タスクが再起動後に丢失** | 作業が無駄に、コンテキストが完全に消える | `hawk resume` — タスク状態が再起動を跨いで持続 |
| **コンテキストの膨張** | Token 料金急騰、応答が低速化 | 5つの注入戦略 + 5つの圧縮戦略 |
| **記憶ノイズ** | 重要な情報がチャット履歴に埋もれる | AI 重要度スコアリング — 低価値コンテンツを自動破棄 |
| **好みが忘れられる** | ユーザーが毎回ルールを説明し直す必要がある | 重要度 ≥ 0.9 = 永久記憶 |

**コアバリュー：** Context-Hawk は、AI agent に実際に機能する記憶を付与します — 何もかも保存するのではなく、重要なことをインテリジェントに保持し、重要でないことを忘れます。

---

## 🎯 5つのコア問題を解決

**問題 1：セッションコンテキストウィンドウの制限**
コンテキストにはトークン上限があります（例：32k）。長い履歴は重要なコンテンツを押し出します。
→ Context-Hawk は古いコンテンツを圧縮/アーカイブし、最も関連する記憶だけを注入します。

**問題 2：セッションをまたいだ記憶の消失**
セッションが終了すると、コンテキストが消えます。、次の会話はゼロから始まります。
→ 記憶は永続的に保存されます。`hawk recall` は次のセッションで関連する記憶を取得します。

**問題 3：複数のエージェントが互いに情報を共有しない**
Agent A は Agent B のコンテキストをしません。ある agent が行った決定は他の agent には見えません。
→ 共有 LanceDB 記憶庫（hawk-bridge と組み合わせて使用）：全 agent が同じ記憶を読み書き。サイロなし。

**問題 4：LLM に送信する前のコンテキストの肥大化**
最適化のないリコール = 大規模で繰り返しコンテキスト。
→ 圧縮 + SimHash 重複排除 + MMR リコール後：LLM に送信されるコンテキストは**大幅に縮小**され、token とコストを節約。

**問題 5：記憶が自ら管理しない**
管理メカニズムなし：全メッセージが堆積し、コンテキストがオーバーフローするまで蓄積。
→ 自動抽出 → 重要度スコアリング → 4層崩壊。不重要 → 削除。重要 → 長期記憶に昇格。

---

## ✨ 12 のコア機能

| # | 機能 | 説明 |
|---|---------|-------|
| 1 | **タスク状態持続性** | `hawk resume` — タスク状態を保持、再起動後も再開可能 |
| 2 | **4層記憶** | Working → Short → Long → Archive（Weibull 崩壊付） |
| 3 | **構造化 JSON** | 重要度スコア（0-10）、カテゴリ、ティア、L0/L1/L2 レイヤー |
| 4 | **AI 重要度スコアリング** | 記憶に自動スコア、低価値コンテンツは破棄 |
| 5 | **5つの注入戦略** | A(高重要度) / B(タスク関連) / C(最近) / D(Top5) / E(フル) |
| 6 | **5つの圧縮戦略** | summarize / extract / delete / promote / archive |
| 7 | **自己内省** | タスクの明確さ、欠落情報、ループ検出をチェック |
| 8 | **LanceDB ベクトル検索** | オプション — ハイブリッド vector + BM25 検索 |
| 9 | **Pure-Memory フォールバック** | LanceDB なしでも動作、JSONL ファイル永続化 |
| 10 | **自動重複排除** | SimHash 重複排除、重複記憶を削除 |
| 11 | **MMR リコール** | 最大辺縁関連性 — 多様なリコール、繰り返しなし |
| 12 | **6カテゴリ抽出** | LLM 駆動の分類抽出：事実 / 好み / 決定 / エンティティ / タスク / その他 |

---

## 🚀 クイックインストール

```bash
# ワンラインインストール（推奨）
bash <(curl -fsSL https://raw.githubusercontent.com/relunctance/context-hawk/master/install.sh)

# またはpipで直接
pip install context-hawk

# 全機能インストール（含 sentence-transformers）
pip install "context-hawk[all]"
```

---

## 🏗️ アーキテクチャ

```
┌──────────────────────────────────────────────────────────────┐
│                      Context-Hawk                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Working Memory  ←── 現在の session（最近 5-10 ターン）    │
│       ↓ Weibull 崩壊                                        │
│  Short-term      ←── 24時間コンテンツ、要約済み             │
│       ↓ access_count ≥ 10 + 重要度 ≥ 0.7                │
│  Long-term       ←── 永続的知識、ベクトルインデックス        │
│       ↓ >90 日または decay_score < 0.15                      │
│  Archive          ←── 履歴、オンデマンドでロード           │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  Task State Memory  ←── 再起動間を永続化（重要！）          │
│  - 現在のタスク / 次のステップ / 進捗 / 出力             │
├──────────────────────────────────────────────────────────────┤
│  注入エンジン       ←── 戦略 A/B/C/D/E が検索を決定       │
│  自己内省            ←── 毎回答がコンテキストをチェック     │
│  自動トリガー        ←── 毎 10 ターン（設定可能）        │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 タスク状態記憶（最も価値のある機能）

再起動、電源障害、session 切替後も、Context-Hawk は中断した正確な位置から再開します。

```json
// memory/.hawk/task_state.jsonl
{
  "task_id": "task_20260329_001",
  "description": "API 文書を完成させる",
  "status": "in_progress",
  "progress": 65,
  "next_steps": ["アーキテクチャテンプレートをレビュー", "ユーザーに報告"],
  "outputs": ["SKILL.md", "constitution.md"],
  "constraints": ["カバー率は98%必須", "APIはバージョン化管理"],
  "resumed_count": 3
}
```

```bash
hawk task "文書を完成させる"  # タスク作成
hawk task --step 1 done     # ステップ完了をマーク
hawk resume                   # 再起動後に再開 ← コア機能！
```

---

## 🧠 構造化記憶

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "完全な元のコンテンツ",
  "summary": "1行サマリー",
  "importance": 0.85,
  "tier": "working|short|long|archive",
  "created_at": "2026-03-29T00:00:00+08:00",
  "access_count": 3,
  "decay_score": 0.92
}
```

### 重要度スコアリング

| スコア | タイプ | アクション |
|-------|------|--------|
| 0.9-1.0 | 決定/規則/エラー | 永久、最も遅い崩壊 |
| 0.7-0.9 | タスク/好み/知識 | 長期記憶 |
| 0.4-0.7 | 対話/議論 | 短期、アーカイブへ崩壊 |
| 0.0-0.4 | チャット/挨拶 | **破棄、決して格納しない** |

---

## 🎯 5 つのコンテキスト注入戦略

| 戦略 | トリガー | 節約量 |
|------|---------|--------|
| **A: 高重要性** | `重要度 ≥ 0.7` | 60-70% |
| **B: タスク関連** | スコープ一致 | 30-40% ← デフォルト |
| **C: 最近** | 最後 10 ターン | 50% |
| **D: Top5 リコール** | `access_count` Top 5 | 70% |
| **E: フル** | フィルターなし | 100% |

---

## 🗜️ 5 つの圧縮戦略

`summarize` · `extract` · `delete` · `promote` · `archive`

---

## 🔔 4段階アラートシステム

| レベル | 閾値 | アクション |
|-------|---------|------|
| ✅ Normal | < 60% | サイレント |
| 🟡 Watch | 60-79% | 圧縮を提案 |
| 🔴 Critical | 80-94% | 自動書き込みを一時停止、強制提案 |
| 🚨 Danger | ≥ 95% | 書き込みをブロック、圧縮必須 |

---

## 🚀 クイックスタート

```bash
# LanceDB プラグインをインストール（推奨）
openclaw plugins install memory-lancedb-pro@beta

# スキルを有効化
openclaw skills install ./context-hawk.skill

# 初期化
hawk init

# コアコマンド
hawk task "私のタスク"    # タスク作成
hawk resume             # 最後のタスクを再開 ← 最も重要
hawk status            # コンテキスト使用状況を查看
hawk compress          # 記憶を圧縮
hawk strategy B        # タスク関連モードに切替
hawk introspect         # 自己内省レポート
```

---

## 自動トリガー：毎 N ターン

毎 **10 ターン**（デフォルト、設定可能）、Context-Hawk は自動的に：

1. コンテキスト水位を確認
2. 記憶の重要度を評価
3. ユーザーに状況を報告
4. 必要に応じて圧縮を提案

```bash
# 設定（memory/.hawk/config.json）
{
  "auto_check_rounds": 10,          # 毎 N ターン確認
  "keep_recent": 5,                 # 最後の N ターンを保持
  "auto_compress_threshold": 70      # 70% を超えたら圧縮
}
```

---

## ファイル構造

```
context-hawk/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk               # Python CLI ツール
└── references/
    ├── memory-system.md           # 4層アーキテクチャ
    ├── structured-memory.md      # 記憶フォーマットと重要度
    ├── task-state.md           # タスク状態持続性
    ├── injection-strategies.md  # 5つの注入戦略
    ├── compression-strategies.md # 5つの圧縮戦略
    ├── alerting.md             # アラートシステム
    ├── self-introspection.md   # 自己内省
    ├── lancedb-integration.md  # LanceDB 統合
    └── cli.md                  # CLI リファレンス
```

---

## 🔌 技術仕様

| | |
|---|---|
| **永続化** | JSONL ローカルファイル、データベース不要 |
| **ベクトル検索** | LanceDB（オプション）+ sentence-transformers ローカルベクトル、ファイルへの自動フォールバック |
| **検索** | BM25 + ANN ベクトル検索 + RRF フュージョン |
| **Embedding プロバイダー** | Ollama / sentence-transformers / Jina AI / Minimax / OpenAI |
| **Cross-Agent** | 汎用、ビジネスロジックなし、任意の AI agent で動作 |
| **ゼロ設定** | 優れたデフォルトで箱から出してすぐ動作（BM25-only モード） |
| **Python** | 3.12+ |

---

## ライセンス

MIT — 無償で可以使用、修正、配布できます。
