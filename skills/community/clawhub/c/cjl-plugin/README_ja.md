---
languages:
  - en
  - zh
  - ja
---

# CJL スキルコレクション

研究、コンテンツ制作、プレゼンテーション設計、ワークフロー自動化 위한 17 のプロダクション対応スキルを備えた个人用 Claude Code プラグイン。

**English** | [简体中文](./README_zh.md) | [日本語](./README_ja.md)

---

## スキル一覧

| スキル | コマンド | 説明 |
|--------|----------|------|
| `cjl-card` | `/cjl-card` | コンテンツ → PNG ビジュアル（ロングカード、情報グラフィック、ポスター） |
| `cjl-paper` | `/cjl-paper` | 学術論文分析パイプライン |
| `cjl-paper-flow` | `/cjl-paper-flow` | 論文分析 + PNG カード ワークフロー |
| `cjl-paper-river` | `/cjl-paper-river` | 学術論文の系譜図 / 引用追跡 |
| `cjl-plain` | `/cjl-plain` | プレーンバゲージライター |
| `cjl-rank` | `/cjl-rank` | 次元削減分析 |
| `cjl-relationship` | `/cjl-relationship` | 関係性分析 |
| `cjl-roundtable` | `/cjl-roundtable` | マルチパースペクティブ円卓討議 |
| `cjl-skill-map` | `/cjl-skill-map` | インストール済みスキル可視化マップ |
| `cjl-travel` | `/cjl-travel` | 都市旅行研究ワークフロー |
| `cjl-word` | `/cjl-word` | 語源を含む英単語深掘り |
| `cjl-word-flow` | `/cjl-word-flow` | 単語分析 → 情報graphicカード |
| `cjl-writes` | `/cjl-writes` | アイデア整理のためのライティングエンジン |
| `cjl-x-download` | `/cjl-x-download` | X/Twitter メディアダウンローダー |
| `cjl-learn` | `/cjl-learn` | コンセプト解剖と学習 |
| `cjl-invest` | `/cjl-invest` | 投資調査と分析 |
| `cjl-slides` | `/cjl-slides` | 24 種類の国際デザインスタイルによる HTML プレゼンテーション |

---

## デザインの理念

各スキルは以下の原則に従います：

- **アトミック**: 1 スキル、1 責任
- **観察可能**: 明確な入力 → 出力契約
- **自己完結型**: 外部状態依存なし
- **ユーザー起動可能**: `/スキル名` または自然言語で起動

---

## 使用方法

### プラグインインストール

```bash
/install-plugin https://github.com/0xcjl/cjl-plugin
```

### 手動インストール

```bash
git clone https://github.com/0xcjl/cjl-plugin ~/.claude/plugins/cjl-plugin
```

---

## 依存関係

| スキル | 依存関係 | インストール |
|--------|----------|-------------|
| `cjl-card` | Node.js + Playwright | [cjl-card docs](https://github.com/0xcjl/cjl-plugin/tree/main/skills/cjl-card) を参照 |

---

## クレジット

[lijigang/ljg-skills](https://github.com/lijigang/ljg-skills) から改编。スキル名の変更（`ljg-` → `cjl-`）を実施し、`cjl-slides` を新規追加。

---

## ライセンス

MIT
