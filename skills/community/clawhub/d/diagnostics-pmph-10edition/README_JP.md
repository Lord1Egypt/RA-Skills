# 診断学 Diagnostic Medicine-PMPH-10edition
<div align="center">

> *「21世紀の医学生のための診断スキルガイド」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 人民衛生出版社『診断学』第10版に基づく臨床スキルハンドブック — **183 の核心的診断スキル**
<br>
<br>
<img src="/assets/Diagnostics.png" width="260px">
<br>

教科書を丸ごと読む必要はありません<br>
質問を入力するだけで、教科書から解決策を自動的に取得

<br>

**他の言語 / Other Languages:**

[中文](README.md) · [English](README_EN.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## プロジェクト概要

本プロジェクトは、臨床診断学の核心領域を体系的に統合し、**183 の重要な診断スキル**を 14 のカテゴリに分類して提供します。人民衛生出版社の国家計画教科書『診断学』第 10 版に基づき、病歴聴取、身体診察、臨床検査の解釈、心電図・画像診断分析、一般的症状の鑑別診断、専門的手技、臨床推論方法をカバーします。

**対象読者**：臨床医、医学生、初期研修医、検査技師、放射線技師、看護師、公衆衛生従事者

**参考教科書**：人民衛生出版社『診断学』第 10 版（ISBN: 978-7-117-35276-8）

**⚠️ 注意事項 ⚠️**
- 本プロジェクトは**教育参考**および**臨床トレーニング**のみを目的としており、専門的な医療判断を代替するものではありません。
- すべての診断判断は、資格を持つ臨床医が患者の個別状況に基づいて行う必要があります。
- ソースコンテンツは最新の臨床ガイドラインを反映していない可能性があります。最新の公式ガイドライン、地域プロトコル、専門医の意見と照合してください。
- 診断、処方、救急処置の決定を資格を持つ医師にエスカレーションするシステムレベルの医療安全ポリシーを展開してください。

## プロジェクト構造

```
Diagnostic-Medicine-PMPH-10edition/
├── SKILL.md              # 核心設定 — 183 スキルレジストリ
├── README.md             # このドキュメント
├── <skill-name>/         # 個別スキル定義
│   └── SKILL.md          #   スキル詳細（使用タイミング、手順、注意点、参考資料）
├── scripts/              # 実行可能ツールスクリプト
├── config/               # 設定ファイル
└── tests/                # 検証とテスト
```

## スキルカテゴリ一覧

| カテゴリ | スキル数 | 説明 |
|----------|---------|------|
| 📋 病歴聴取とコミュニケーション | 8 | 構造化問診、重点的問診、医患コミュニケーション、カルテ作成 |
| 🩺 身体診察技術 | 22 | 全身診察、4 基本検査法、特殊患者適応、各系統専門診察 |
| ❤️ 心血管系診断 | 16 | 心電図分期・局在、心音分析、不整脈、運動負荷試験、心筋マーカー |
| 🫁 呼吸器系診断 | 7 | 異常呼吸音、打診音判読、気管支鏡準備、肺機能・血液ガス |
| 🫃 消化器系と腹部評価 | 10 | 腹部腫瘤、腹痛メカニズム、嘔吐物分析、腸閉塞、Murphy 徴候 |
| 🩸 血液・凝固系 | 21 | 貧血分類、骨髄鉄染色、凝固因子、溶血スクリーニング、PNH フローサイトメトリー |
| ⚖️ 内分泌・代謝 | 11 | 浮腫鑑別、栄養評価、血糖・OGTT、甲状腺機能、先天性黄疸症候群 |
| 🫘 肝胆膵・泌尿器系 | 15 | 黄疸鑑別、肝酵素パターン、血中アンモニア、尿中赤血球形態、RTA 試験 |
| 🦠 感染・免疫 | 14 | 薬剤感受性試験、耐性機構、梅毒血清学、ツベルクリン反応、補体・自己抗体 |
| 🧠 神経・精神系 | 4 | めまい分類、うつ病識別、乳頭浮腫測定、眼底全身疾患兆候 |
| 🔬 臨床検査と品質管理 | 10 | 検体採取、基準範囲解釈、QC システム、便・精液検査、膣清潔度 |
| 🏥 専門手技と穿刺術 | 10 | 腹水穿刺、胸腔穿刺、腰椎穿刺、肝生検、リンパ節穿刺、カテーテル挿入 |
| 🧩 臨床推論と診断法 | 11 | 4 段階診断法、仮説演繹的推論、診断思考原則、症状鑑別、病態生理分類 |
| 📚 教科書・リソース利用 | 5 | 版確認、改訂ガイドライン、デジタルリソースアクセス、核心的枠組み |

> **合計：183 スキル** — 基礎から応用までの完全な診断能力体系

## クイックスタート

### インストール

CLI：
```bash
openclaw skills install diagnostics-pmph-10edition
```

### 使用例

**クエリ例：**
- 「**acute-myocardial-infarction-ecg-staging** スキルを使用して、この患者の心電図を分析してください。」
- 「**mcv-rdw-anemia-classification** を適用して、この貧血症例を分類してください。」
- 「**clinical-diagnostic-four-step-method** を参考に、この発熱患者の考えられる原因を推論してください。」
- 「**bilirubin-metabolism-and-jaundice-classification** を使用して、黄疸患者の病因を分析してください。」

## 作者について

**xllgreen** ([xllgreen.github.io](https://xllgreen.github.io)) — 九江学院臨床医学院の医学生 · テクノロジーギーク

## テクニカルサポート

<br>
PDF2App: https://pdf2app.cn
<br>
Microsoft Visual Studio Code: https://code.visualstudio.com/
<br>
Claude Code for VS Code: https://claude.com/
<br>
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API: https://platform.deepseek.com/
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API: https://platform.xiaomimimo.com/
<br>
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved
<br>

## ライセンス

本プロジェクトは人民衛生出版社『診断学』第 10 版に基づき、学習目的で整理されたものです。

## Star History

<a href="https://www.star-history.com/#xllgreen%2FDiagnostic-Medicine-PMPH-10edition&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=xllgreen/Diagnostic-Medicine-PMPH-10edition&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=xllgreen/Diagnostic-Medicine-PMPH-10edition&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=xllgreen/Diagnostic-Medicine-PMPH-10edition&type=Date" />
 </picture>
</a>
