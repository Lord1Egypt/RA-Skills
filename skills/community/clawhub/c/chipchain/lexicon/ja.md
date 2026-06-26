# Japanese Semiconductor Terminology (日本語)

Full lexicon compiled from research.

## Key Language Pattern

Japanese semiconductor industry uses a MIX of kanji, katakana, and English acronyms. The pattern is NOT random:
- **Process acronyms stay English:** ALD, CVD, PVD, CMP, EUV
- **Traditional chemistry uses kanji:** フッ酸 (HF), 硫酸, 過酸化水素
- **Newer concepts get katakana:** フォトレジスト, エッチング, スパッタリング
- **Business terms are kanji:** 歩留まり (yield), 計測 (metrology), 仕入先 (supplier)

## Critical Spelling Trap

**Silicon wafer = ウェーハ** (weehaa), NOT ウエハー. Shin-Etsu and SUMCO both use ウェーハ. Wrong spelling = zero search results.

## Must-Know Terms

| English | Japanese | Notes |
|---|---|---|
| Semiconductor materials | **半導体材料** | The standard term |
| Supplier (in filings) | **仕入先** | NOT サプライヤー in EDINET filings |
| Supplier (in press) | **サプライヤー** | Katakana loanword in press |
| Major customers | **主要販売先** | Mandatory >10% disclosure |
| Major suppliers | **主要仕入先** | |
| Yield | **歩留まり** (budomari) | Distinctive native term |
| Front-end process | **前工程** | |
| Back-end process | **後工程** | |
| Metrology | **計測** | NOT メトロロジー |
| Inspection | **検査** | NOT インスペクション |
| Ultra-pure water | **超純水** | |
| HF (hydrofluoric acid) | **フッ酸** | THE central term in 2019 Japan-Korea dispute |
| High-purity HF | **高純度フッ酸** / 超高純度フッ酸 | |
| Photoresist | **フォトレジスト** / レジスト | |
| EUV resist | **EUVレジスト** | |
| ArF immersion | **ArF液浸** レジスト | 液浸 (ekishin) preferred over イマージョン |
| Deposition | **成膜** (general) | More common than 堆積 |
| Export control | **輸出管理** (neutral) / **輸出規制** (restriction) | |
| Economic security | **経済安全保障** / 経済安保 | Key policy term |

## EDINET Filing Search Sections

When searching Japanese company filings (有価証券報告書):

| Section (Japanese) | English | What it reveals |
|---|---|---|
| **主要販売先** | Major customers | Customers >10% of revenue |
| **主要仕入先** | Major suppliers | Key procurement sources |
| **事業等のリスク** | Business risks | Supplier dependency, concentration risk |
| **関連当事者との取引** | Related party transactions | Intra-group supply |
| **事業の内容** | Business description | What the company does |
| セグメント情報 | Segment information | Revenue by business |

## Search Query Patterns

```
# Who supplies X to Company Y?
{Y社}に{X}を供給
{X}の供給元
{Y社}向け{X}

# Major manufacturers of X
{X}の主要メーカー

# Japan-Korea export controls
フッ化水素 輸出規制 韓国
フォトレジスト 輸出規制

# Rapidus / Japan semiconductor revival
ラピダス 2nm
JASM 熊本
半導体 復活
```

## Key Company Names in Japanese

| English | Japanese | Ticker |
|---|---|---|
| Shin-Etsu Chemical | 信越化学工業 (short: 信越) | 4063.T |
| SUMCO | SUMCO (English used) | 3436.T |
| Tokyo Electron | 東京エレクトロン | 8035.T |
| TOK | 東京応化工業 | 4186.T |
| SCREEN | SCREENホールディングス | 7735.T |
| Lasertec | レーザーテック | 6920.T |
| Resonac | レゾナック (ex-昭和電工) | 4004.T |
| Stella Chemifa | ステラ ケミファ | 4109.T |
| Fujifilm | 富士フイルム (note: フイルム not フィルム) | 4901.T |
