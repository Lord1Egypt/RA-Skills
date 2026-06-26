# 中医学 Chinese Medicine-PMPH-10版
<div align="center">

> *「21世紀の中医学徒ガイド」*

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![ClawHub](https://img.shields.io/badge/ClawHub-Skill-orange)](https://clawhub.ai)

<br>
> 人民衛生出版社刊『中医学』第10版に基づく臨床スキルハンドブック — 172の中核的中医臨床スキル
<br>
<br>
<img src="assets/Chinese Medicine-10edition.jpg" width="260px">
<br>

一冊の本を丸ごと読む必要はありません<br>
質問を入力するだけで、教科書から自動的に解決策を導き出します

<br>

**その他の言語 / Other Languages:**

[简体中文](README.md) · [English](README_EN.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## プロジェクト概要

本プロジェクトは、中医の基礎理論、弁証論治、方薬応用、鍼灸推拿、婦科・小児科、温病・傷寒、腫瘍調治、体質識別、中西医結合などの中核領域を体系的に統合し、**172の重要臨床スキル**を**20大分類**にまとめています。

**対象読者**：中医師、中西医結合医師、医学生、中医薬研究者、養生保健従事者

**参考教科書**：人民衛生出版社『中医学』第10版（全国高等学校五年制本科臨床医学専業規画教材）

**⚠️ リスク ⚠️**：ユーザーが中医の診断・処方・鍼灸・塗油内容を独立した医療アドバイスと解釈する可能性があります。

**対策**：出力はあくまで教育参考資料、または有資格臨床医のレビュー用とし、推奨事項が現行の公式ガイドラインおよび地域規制に適合することを確認してください。

**⚠️ リスク ⚠️**：実行可能な手順や治療ガイダンスは、自己診断、緊急時、妊娠、出血、呼吸器疾患、鍼灸、手技療法、手術類似手順、薬物・臨床検査には適さない場合があります。

**対策**：自己治療を防止し、緊急・高リスク・手続き的シナリオを資格ある専門家の監督下に委ねる独立した医療安全ポリシーを実施しています。

## プロジェクト構成

```
Chinese-Medicine-PMPH-10edition/
├── SKILL.md                    # 中核設定 — 172スキルレジストリ
├── README.md                   # 本ドキュメント — プロジェクト説明・利用ガイド（多言語）
│   ├── README_EN.md            # 英語版
│   ├── README_JP.md            # 日本語版
│   ├── README_FR.md            # フランス語版
│   └── README_RU.md            # ロシア語版
├── <skill-name>/               # 各スキルの詳細定義
│   └── SKILL.md                #   スキル詳細（使用タイミング、実行手順、参考資料）
├── index.md                    # スキルナビゲーション索引
├── scripts/                    # 実行可能ツールスクリプト
├── config/                     # 設定ファイル
├── tests/                      # 検証とテスト
└── assets/                     # プロジェクト資産ファイル
```

## スキル分類一覧

| 分類 | スキル数 | 説明 |
|------|---------|------|
| 🧬 中医基礎理論 | 18 | 陰陽五行、臓腑経絡、気血津液、体質 |
| 🔍 弁証論治通則 | 8 | 弁証の中核原則、治則治法 |
| 🫀 臓腑経絡と生理病理 | 13 | 心・肝・脾・肺・腎、経絡の機能と病理 |
| 🔬 診法と四診合参 | 6 | 舌診、脈診、望診、小児指紋 |
| 🌡️ 外感病証辨治 | 10 | 六淫、温病、傷寒弁証 |
| 🩺 内科雑病辨治 | 14 | 便秘、痔、眩暈、不眠、泄瀉、痺証など |
| 👩 婦科病証辨治 | 9 | 月経不順、帯下、崩漏、産後缺乳 |
| 🚽 泌尿と淋証 | 3 | 淋証六型弁証、血淋尿血 |
| 💧 消渇と水腫 | 2 | 三消弁証、陽水陰水 |
| 🟡 黄疸と積聚 | 2 | 陽黄陰黄、聚星障 |
| 🩸 瘀血と出血証 | 3 | 血瘀証、血府逐瘀 |
| 💊 方剤学と薬物応用 | 26 | 経方応用、中薬配伍、毒性管理 |
| 📍 鍼灸療法 | 8 | 毫鍼、灸法、耳穴、腧穴 |
| ✋ 推拿手技 | 5 | 八法、扳法、拍法、補瀉 |
| 🫳 外治法とその他の療法 | 3 | 抜罐、金黄散、中薬外治 |
| 🤝 中西医結合と現代的応用 | 7 | 中西医協同、糖尿病前期介入 |
| 📚 古典文献と学術源流 | 4 | 四大古典、『新修本草』、葛洪 |
| 🎗️ 腫瘍と難治重症 | 5 | 腫瘍弁証、扶正祛邪、癌性腹水 |
| 👶 小児専門病 | 1 | 性早熟 |
| ⚙️ 治法分類 | 4 | 下法、解表剤、温裏剤、通降原則 |

## クイックスタート

### インストール

CLI：
```bash
openclaw skills install chinese-medicine-10edition
```

プロンプト（Claude Code）：
```bash
インストール前に、ClawHubのスキルメタデータとセットアップ要件を確認してください。
サードパーティのパッケージやCLIのインストールを求められた場合は、そのソース、メンテナー、パッケージ内容をインストール前に検証してください。
それらのチェックが完了した後にのみ、ClawHubからスキル「Chinese Medicine 10th Edition」（xllgreen/chinese-medicine-10edition）をインストールしてください。
スキルページ: https://clawhub.ai/xllgreen/chinese-medicine-10edition
作業範囲はこのスキルのみに限定してください。
インストール後、検証済みのスキルメタデータに基づいてセットアップを完了するのを支援してください。
ClawHubで検証できるメタデータのみを使用し、不足する要件をでっち上げないでください。
広範な環境変更を行う前に確認を取ってください。
```

### 使用方法

各スキルは4つのパートで構成されています：
1. **使用タイミング** — このスキルを発動する状況
2. **実行手順** — 標準化された操作フロー
3. **注意事項** — 禁忌と警告
4. **参考資料** — 詳細な補足資料

### 質問戦略

#### 1. **概念**
質問：
```bash
肝主疏泄の五大生理機能とは何ですか
```
回答：
```bash
「肝疎泄五大生理機能」スキルによる：肝主疏泄とは、肝気が全身の気機を疏通・暢達させる作用を指し、具体的には：
1. **気機の調暢**：全身の気機を疏通し、滞りなく散鬱させない
2. **血液と津液の運行促進**：気行すれば血行し、気行すれば津行する
3. **脾胃の運化と胆汁分泌排泄の促進**：脾胃の気機昇降を補助する
4. **情志の調暢**：疏泄が正常であれば気血が調和し、心情が舒畅になる
5. **生殖機能の調節**：女性の月経、男性の射精と密接に関係する
```

#### 2. **臨床ケース分析**
質問：
```bash
患者、45歳男性、季肋部脹痛が3年間反復発作、情志不遂により増悪、胸悶・嘆息を好む・納食減少・脘腹部脹満を伴う。舌淡紅・苔薄白・脈弦。弁証分析を行ってください。
```
回答：
```bash
「肝気鬱結証弁証」スキルによる分析と治療...
```

#### 3. **方剤応用**
質問：
```bash
患者に発熱、微悪風寒、頭痛口渴、咽痛咳嗽、舌尖紅、苔薄黄、脈浮数が認められます。方剤を推奨してください。
```
回答：
```bash
「銀翹散方剤応用」スキルによる — 診断：風熱感冒（温病初起衛分証）。銀翹散の加减を推奨...
```

#### 4. **鍼灸取穴**
質問：
```bash
患者に胃脘疼痛が反復発作し、空腹時に特に酷く、食事でやや軽減、反酸・噯気を伴います。鍼灸処方を推奨してください。
```
回答：
```bash
「腧穴分類と主治规律」および「鍼灸選穴原則」スキルによる...
```

## スキル索引

全172スキルの完全な索引は [index.md](index.md) をご参照ください。

## 著者について

**xllgreen (https://xllgreen.github.io)** — 九江学院臨床医学院 学生 · テック愛好家

## テクニカルサポート
<br>
PDF2Appプロジェクト：https://pdf2app.cn
<br>
Microsoft Visual Studio Code：https://code.visualstudio.com/
<br>
Claude Code for VS Code：https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API：https://platform.deepseek.com/
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API：https://platform.xiaomimimo.com/
Copyright © 2010 — 2026 Xiaomi. All Rights Reserved
<br>

## ライセンス

本プロジェクトの内容は人民衛生出版社『中医学』第10版に基づいて整理されており、学習参考のみを目的としています。

## Star History

<a href="https://www.star-history.com/?repos=xllgreen%2FChinese-Medicine-10edition&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=xllgreen/Chinese-Medicine-10edition&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=xllgreen/Chinese-Medicine-10edition&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=xllgreen/Chinese-Medicine-10edition&type=date&legend=top-left" />
 </picture>
</a>
