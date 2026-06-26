[简体中文](README.zh.md) · [English](README.md) · **[日本語](README.ja.md)**

# Agentify

Web ページやサイトを **AI エージェント**、**クローラ**、**自動化ツール**が理解・操作しやすくするためのスキルです。エージェント適性の分析、テンプレートの書き換え、チーム向け設計仕様の生成に対応します。

## 機能概要

| 機能 | 説明 |
|------|------|
| **Analyze** | 9 分野（セマンティック HTML、ARIA、構造化データ、フォーム、ナビゲーション、`data-testid`、セレクタの安定性、API の発見しやすさ、メタ情報など）を 0–100 点で評価し、実行可能な改善案を提示します。 |
| **Rewrite** | **既存の挙動や見た目を変えずに**、HTML/JSX/Vue/Svelte へセマンティクス、ARIA、`data-testid`、JSON-LD、アクセシビリティ／自動化向け属性を追加します。 |
| **Design Spec** | プロジェクトの技術スタックに合わせ、`agent-friendly-spec.md` 相当の設計仕様（優先度、例、アンチパターン、検証方法）を生成します。 |

想定トリガー例：*agent-friendly*、*SEO / 構造化データ*、*data-testid を追加*、*スクレイピング向け*、*a11y 監査* など。

## リポジトリ構成

```
Agentify/
├── README.md               # English（既定）
├── README.zh.md
├── README.ja.md
├── SKILL.md                # スキルエントリ（Agent Skills 互換）
└── references/
    ├── checklist.md
    ├── frameworks.md
    ├── knowledge-base.md
    ├── patterns.md
    ├── scoring.md
    ├── spec-example.md
    └── spec-template.md
```

詳細は [`SKILL.md`](SKILL.md) を参照してください。

## 使い方

読み込まれるスキルは、**同じ階層にある `SKILL.md` と `references/`** です。このリポジトリのルートをそのまま使うか、`SKILL.md` と `references/` だけを専用フォルダへコピー／シンボリックリンクしてください。

- **Cursor** — そのフォルダを Cursor の user skills に追加します。
- **OpenClaw** — `~/.openclaw/skills/` またはワークスペースの `skills/` に置きます。読み込み順や `~/.openclaw/openclaw.json` の `skills.load.extraDirs` などは [OpenClaw Skills ドキュメント](https://docs.openclaw.ai/skills/) を参照してください。

## ライセンス

`LICENSE` がない場合、著作権は留保されます。公開配布する前に `LICENSE` を追加してください。
