<div align="center">

# Air-chart

**ひとことで指示。あなたの AI がプロ仕様の大気質チャートを描きます。**

English | [简体中文](README.zh.md) | [Español](README.es.md) | [हिन्दी](README.hi.md) | **日本語** | [한국어](README.ko.md) | [Français](README.fr.md)

![Claude Code](https://img.shields.io/badge/Claude%20Code-native-blue)
![Cursor](https://img.shields.io/badge/Cursor-native-blue)
![Codex CLI](https://img.shields.io/badge/Codex%20CLI-compatible-blue)
![ClawHub](https://img.shields.io/badge/ClawHub-publishable-green)
![skills.sh](https://img.shields.io/badge/skills.sh-installable-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## このスキルは何をする?

AI チャットにひとこと書くだけ — AI が **測定局を探し、データを取得し、チャートのリンクを渡してくれます**。エンジンは [x-cmd Draw](https://x-cmd.com/draw) — データとチャートがひとつの URL に:

> 💬 "北京のここ1週間の PM2.5 の推移を見せて"
> 💬 "東京とソウルの過去 7 日間の大気質を比較して"
> 💬 "ニューデリーの 30 日間の PM10 を WHO ガイドラインと比較して"
> 💬 "シンガポールの過去 48 時間の時間別オゾン"
> 💬 "北京で今いちばんひどい測定局はどこ?"

裏側は完全自動化のパイプライン:都市を特定 → **OpenAQ** から**実際に稼働中の**測定局を選択(100 以上の国の政府リファレンスデータ)→ 外れ値と欠損を除去 → プロ仕様のチャートをレンダリング。

**おすすめの理由:**

- **チャートは URL — URL がデータそのもの** — デフォルトでは `x-cmd.com/draw` リンクが返され、チャートの描画とあらゆる数値の保持を両立します。共有可能、Markdown に画像として埋め込み可能、URL 上の数値を書き換えればチャートも更新されます。ファイルが必要なら `--out chart.svg`(または `.png`)でダウンロード。
- **x-cmd Draw によるレンダリング** — ローカル側は純粋な `bash`/`jq`/`awk`/`curl` のまま。チャートエンジンは [x-cmd Draw](https://x-cmd.com/draw) のため、増え続ける豊富なチャート種類(折れ線、棒、面、円、レーダー、ゲージ、サンキー、ガント、マインドマップなど)・明暗テーマ・多言語レンダリング・オンラインエディタをそのまま利用でき、レンダラの保守コードはゼロ。インストールも更新も不要。
- **設計上の信頼性** — 政府リファレンス級測定局を優先。チャートは物理濃度(µg/m³)を明記し、**WHO 24 時間ガイドライン**を参照系列として重ねます。限界値はデータと一緒に移動します。見栄えだけの AQI 数値ではなく、レポートに載せられるデータ。
- **グローバルカバレッジ、寛容な入力** — 250 以上の都市の組み込み座標。`delhi`、`tOKyo`、`中山` のような揺らぎのある名前もそのまま動作し、生の `lat,lon` も受け付けます。
- **本物のデータ、おもちゃではない** — 沈黙した「ゾンビ」測定局とセンサー故障のスパイクを排除。欠損時間帯は軸から除外され、0 で埋められることはありません。

## ショーケース

以下の各チャートは **OpenAQ の実測値** を、データを保持した URL からライブレンダリングしたものです — このリポジトリには画像ファイルを一切保存していません。チャートをクリックすれば x-cmd Draw エディタで値を調整できます。

| 複数都市の PM2.5、過去 7 日間(東京 · ソウル · ロンドン) | ニューデリー PM2.5 / PM10、過去 14 日間 |
| --- | --- |
| [![複数都市の PM2.5、過去 7 日間(東京 · ソウル · ロンドン)][sc1] | [![ニューデリー PM2.5 / PM10、過去 14 日間][sc3] |

| ロンドンのオゾン (O₃)、過去 48 時間 | ニューデリー:測定局別 PM10 スナップショット(ライブ) |
| --- | --- |
| [![ロンドンのオゾン (O₃)、過去 48 時間][sc2] | [![ニューデリー:測定局別 PM10 スナップショット(ライブ)][sc4] |

| ダークテーマ:複数都市 PM2.5 | ニューデリー PM2.5、過去 30 日間 |
| --- | --- |
| [![ダークテーマ:複数都市 PM2.5][sc5] | [![ニューデリー PM2.5、過去 30 日間][sc6] |

[sc1]: https://x-cmd.com/draw?type=line&title=PM2.5%20%E6%AF%94%E8%BC%83%20%C2%B7%20%E9%81%8E%E5%8E%BB%207d%20%C2%B7%20%E8%A4%87%E6%95%B0%E9%83%BD%E5%B8%82%20%C2%B7%20%E5%90%8C%E4%B8%80%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF&unit=%C2%B5g%2Fm%C2%B3&labels=11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=Tokyo%20PM2.5:2.73,2.95,5,5.5,6.45,10.4,12.7&series=Seoul%20PM2.5:7.96,9.58,10.3,16.2,22.8,28.8,28.3&series=London%20PM2.5:58.3,82.4,49.4,23.9,15.8,10.8,13.7&series=WHO%2024%E6%99%82%E9%96%93:15,15,15,15,15,15,15&w=960&h=500&t=opendata
[sc2]: https://x-cmd.com/draw?type=line&title=London%20O3%20%E3%81%AE%E6%8E%A8%E7%A7%BB%20%C2%B7%20%E9%81%8E%E5%8E%BB%2048h%20%C2%B7%20%E7%8F%BE%E5%9C%B0%E6%99%82%E9%96%93%20%28Europe%2FLondon%29&unit=%C2%B5g%2Fm%C2%B3&labels=11-12%2001%3A00,11-12%2002%3A00,11-12%2003%3A00,11-12%2004%3A00,11-12%2005%3A00,11-12%2006%3A00,11-13%2000%3A00,11-13%2001%3A00,11-13%2002%3A00,11-13%2003%3A00,11-13%2004%3A00,11-13%2005%3A00,11-13%2006%3A00,11-13%2007%3A00&series=London%20O3:52.7,51.2,42.7,43.1,41,31.4,42.7,44.9,46.5,48.3,39.6,17.1,15.4,17&series=WHO%2024%E6%99%82%E9%96%93:100,100,100,100,100,100,100,100,100,100,100,100,100,100&w=960&h=500&t=opendata
[sc3]: https://x-cmd.com/draw?type=line&title=New%20Delhi%20PM2.5%20%2F%20PM10%20%E3%81%AE%E6%8E%A8%E7%A7%BB%20%C2%B7%20%E9%81%8E%E5%8E%BB%2014d%20%C2%B7%20%E8%A4%87%E6%95%B0%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF&unit=%C2%B5g%2Fm%C2%B3&labels=10-31,11-01,11-02,11-03,11-04,11-05,11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=New%20Delhi%20PM2.5:110,205,217,241,265,305,306,339,302,222,163,147,232,172&series=WHO%2024%E6%99%82%E9%96%93:15,15,15,15,15,15,15,15,15,15,15,15,15,15&w=960&h=500&t=opendata
[sc4]: https://x-cmd.com/draw?type=hbar&title=New%20Delhi%20%E6%B8%AC%E5%AE%9A%E5%B1%80%E5%88%A5%E3%82%B9%E3%83%8A%E3%83%83%E3%83%97%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%20%C2%B7%20PM10%20%C2%B7%202026-11-14%2013%3A27%20IST%20%C2%B7%20%E5%8D%8A%E5%BE%84%2025%20km&unit=%C2%B5g%2Fm%C2%B3&labels=Alipur,Anand%20Vihar,Ashok%20Vihar,Aya%20Nagar,Bawana,Burari%20Crossing&values=418.0,409.0,426.0,501.0,382.0,533.0&num=all&w=960&h=480&t=evil-glow
[sc5]: https://x-cmd.com/draw?type=line&title=PM2.5%20%E6%AF%94%E8%BC%83%20%C2%B7%20%E9%81%8E%E5%8E%BB%207d%20%C2%B7%20%E8%A4%87%E6%95%B0%E9%83%BD%E5%B8%82%20%C2%B7%20%E5%90%8C%E4%B8%80%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF&unit=%C2%B5g%2Fm%C2%B3&labels=11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=Tokyo%20PM2.5:2.73,2.95,5,5.5,6.45,10.4,12.7&series=Seoul%20PM2.5:7.96,9.58,10.3,16.2,22.8,28.8,28.3&series=London%20PM2.5:58.3,82.4,49.4,23.9,15.8,10.8,13.7&series=WHO%2024%E6%99%82%E9%96%93:15,15,15,15,15,15,15&w=960&h=500&scheme=dark&t=opendata
[sc6]: https://x-cmd.com/draw?type=line&title=New%20Delhi%20PM2.5%20%E3%81%AE%E6%8E%A8%E7%A7%BB%20%C2%B7%20%E9%81%8E%E5%8E%BB%2030d%20%C2%B7%20%E7%8F%BE%E5%9C%B0%E6%99%82%E9%96%93%20%28Asia%2FKolkata%29&unit=%C2%B5g%2Fm%C2%B3&labels=10-15,10-16,10-17,10-18,10-19,10-20,10-21,10-22,10-23,10-27,10-28,10-29,10-30,10-31,11-01,11-02,11-03,11-04,11-05,11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=New%20Delhi%20PM2.5:73.6,65.7,94,127,94,125,142,136,142,138,131,95,44.7,110,205,217,241,265,305,306,339,302,222,163,147,232,172&series=WHO%2024%E6%99%82%E9%96%93:15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15&w=960&h=500&t=opendata

## 特徴

- **重い依存ゼロ** — 純粋な `bash` / `jq` / `awk` / `curl`。SVG レンダラは awk 製。
- **グローバルカバレッジ** — 200 以上の主要都市の組み込み座標、または `lat,lon` 直接指定。
- **スマートな測定局選択** — 半径 25 km で検索 → 24 時間沈黙の「ゾンビ」局を除外(72 時間で再試行)→ 政府リファレンス級モニターを優先。
- **プロ仕様のビジュアル** — 物理濃度の単位 (µg/m³) を明記、WHO 24 時間ガイドライン線をデフォルトで重ね(遵守なら緑、超過なら赤)、明暗テーマ対応。
- **実運用向けの設計** — ローカルキャッシュ(時間別 20 分 / 日別 2 時間)、HTTP 429 の指数バックオフ、欠損を考慮した描画(欠損は線を分断 — 0 埋め never)、UTC → 測定局現地時間の整合。

## クイックスタート

### 1. API キーを取得(無料、約 1 分)

1. [OpenAQ Explorer](https://explore.openaq.org/register) で登録またはログイン(既存アカウントは [ログイン](https://explore.openaq.org/login))。
2. [アカウントページ](https://explore.openaq.org/account) を開く — 下部に API キーが表示されます。コピー。
3. 設定する — どちらか 1 つ:

```bash
export OPENAQ_API_KEY="your_key"                             # ephemeral / CI
echo 'OPENAQ_API_KEY=your_key' > ~/.config/air-chart/config  # persistent
```

システムキーチェーンは不要 — 無料の公開サービス認証情報は平文の設定ファイルに保存。キーがなくても `--demo` モードでサンプルデータのまますべてレンダリング可能。

### 2. 実行

```bash
# 単一都市、7 日間の PM2.5 推移
./scripts/air_chart.sh --city Beijing --param pm25 --period 7d

# 複数都市の比較 (最大 4 都市)
./scripts/air_chart.sh --city Tokyo --city Seoul --param pm25 --period 7d

# 単一都市の複数パラメータ (PM2.5 + PM10)
./scripts/air_chart.sh --city Beijing --param pm25 --param pm10 --period 30d

# 48 時間の時間別カーブ (昼夜パターン)
./scripts/air_chart.sh --city Singapore --param o3 --period 48h

# 稼働中測定局のリアルタイム棒グラフスナップショット
./scripts/air_chart.sh --city Delhi --param pm10 --snapshot

# ダークテーマ、ファイル出力
./scripts/air_chart.sh --city London --param no2 --period 14d --theme dark -o london.svg
```

### 3. AI エージェントスキルとしてインストール

```bash
git clone https://github.com/qiakai/air-chart.git ~/.claude/skills/air-chart
# or: npx skills add qiakai/air-chart
```

あとはエージェントに頼むだけ:*「東京とソウルの過去 7 日間の PM2.5 を比較して」*。

`SKILL.md` はエージェント・レジストリとの最大互換性のため英語で記述。中国語版は `SKILL.zh.md`。チャート出力は `--lang en|zh|es|hi|ja|ko|fr` に対応(デフォルトはシステムロケールから自動判定)。

## CLI リファレンス

| Flag | Description | Values |
| --- | --- | --- |
| `--city, -c` | 都市名(繰り返し可、≤4)または座標 `"lat,lon"` | `Beijing`, `New Delhi`, `39.9,116.4` |
| `--param, -p` | 汚染物質(デフォルト `pm25`) | `pm25` `pm10` `o3` `no2` `so2` `co` |
| `--period, -t` | 期間(デフォルト `7d`) | `24h` `48h`(時間別)· `7d` `14d` `30d`(日別) |
| `--snapshot` | 都市の稼働中測定局の棒グラフスナップショット | flag |
| `--theme` | カラーテーマ | `light` / `dark` |
| `--lang` | 出力言語(チャート + メッセージ) | `en` `zh` `es` `hi` `ja` `ko` `fr`(デフォルト:ロケール自動判定) |
| `--out, -o` | チャートを `.svg` または `.png` でダウンロード | デフォルト:x-cmd Draw URL のみ表示 |
| `--demo` | デモモード。API キー不要 | flag |

## アーキテクチャ

```text
[city / pollutant / time range]
   │
   ▼
geo_resolve.sh      city name → coordinates + timezone (built-in gazetteer / raw lat,lon)
   │
   ▼
openaq_client.sh    OpenAQ API v3: auth, User-Agent, md5 cache,
                    429 exponential backoff, liveness filter (24h/72h),
                    sensor match by fixed parameter ID, reference-grade first
   │
   ▼
data_transform.awk  cleaning (negatives / physically impossible spikes),
                    gap detection (breaks, never zero-filled), stats, local-time labels
   │
   ▼
render_draw.sh      x-cmd Draw URL builder (URL-as-Data; optional .svg/.png download)
```

`data/parameters.tsv` は openaq-api の固定汚染物質 ID に整合した静的パラメータ辞書:slug / param_id / 名称 / 単位 / WHO 24 時間ガイドライン / 物理上限 / パラメータ別カラー — `/parameters` の冗長な往復なし。ビジュアルは openaq-explorer の慣習に準拠:パラメータ別パレット(PM2.5 `#E65100`、PM10 `#6A1B9A`、O3 `#0277BD`、NO2 `#00838F`)、色覚特性に配慮した複数都市パレット、安全グリーン `#10B981` / アラートレッド `#EF4444` の WHO ガイドライン線。測定局が辞書既定と異なる単位 (ppm など) を報告する場合、Y 軸は実単位を使い、次元の混乱を避けるため WHO 線は省略されます。

## 終了コード

| Code | Meaning |
| --- | --- |
| 3 | API キー未設定(セットアップ案内を表示) |
| 4 | ネットワーク / API エラー / レート制限リトライ枯渇 |
| 5 | 稼働中の測定局なし、または有効なデータなし |
| 2 | 都市名を解決できない(近似候補を表示) |

## ライセンス

MIT
