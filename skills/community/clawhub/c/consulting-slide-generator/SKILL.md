---
name: consulting-slide-generator
description: "コンサルティングファーム品質のスライド図解をHTML+Tailwindで生成。McKinsey/BCG風のビジネス資料、提案書、プレゼンテーション用の図解を作成する際に使用。対応: (1) 課題提起スライド（数字+プログレスバー）, (2) ソリューションフロー（ステップ図）, (3) 2x2マトリクス（軸に意味あり）, (4) 比較表・Do/Don't, (5) プロセスフロー（ゲート付き）。出力はHTML→Chrome headlessでPNG変換。"
---

# Consulting Slide Generator

コンサルファーム品質のスライド図解をHTML+Tailwindで生成する。

## 生成ワークフロー

### Step 1: スライドタイプを特定

| タイプ | 用途 | テンプレート |
|--------|------|-------------|
| problem | 課題提起（数字で説得） | [assets/templates/problem.html](assets/templates/problem.html) |
| solution | ソリューションフロー | [assets/templates/solution.html](assets/templates/solution.html) |
| matrix | 2x2マトリクス | [assets/templates/matrix.html](assets/templates/matrix.html) |
| compare | 比較・Do/Don't | [assets/templates/compare.html](assets/templates/compare.html) |
| process | プロセスフロー | [assets/templates/process.html](assets/templates/process.html) |

### Step 2: テンプレートを読み込み、内容を置換

### Step 3: HTMLを保存
```
slides/<project-name>/<slide-name>.html
```

### Step 4: PNGに変換
```bash
bash scripts/html2png.sh input.html output.png
```

## デザイン原則

詳細は [references/design-principles.md](references/design-principles.md) を参照。

### 必須ルール
1. **12カラムグリッド** - `grid-cols-12` で構成
2. **3レベル階層** - Eyebrow → Title → Body
3. **2-3色配色** - Navy + Accent (Red/Green/Gold)
4. **意図的な余白** - 詰め込まない
5. **数字は大きく** - `text-5xl font-black` + プログレスバー

### 配色
```
Navy:   #0f172a, #1e293b, #334155
Red:    #dc2626
Green:  #059669
Gold:   #ca8a04
```

### フォント
- Noto Sans JP (Google Fonts CDN)
- ウェイト: 300, 400, 500, 700, 900

## スライドタイプ別ガイド

### Problem（課題提起）
- 左: メッセージ / 右: 数字+プログレスバー
- 推定値には注釈

### Solution（ソリューション）
- ステップ横並び（5段階）
- Navy→Greenグラデーション
- 下部に効果3カラム

### Matrix（2x2）
- 軸に意味を持たせる
- 各セルに優先度バッジ

### Compare（比較）
- Do/Don't 2カラム
- ✓/✗ アイコン

### Process（プロセス）
- 縦フロー + ゲート
- Yes/No分岐

## 出力仕様
- 解像度: 1200 x 675 px
- フォーマット: HTML → PNG
