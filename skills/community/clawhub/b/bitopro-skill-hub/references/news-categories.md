# Tool 8 News Classification Keywords

Keyword lists for `get_bitopro_relevant_news` classification. Matching is **case-insensitive substring**, applied against `title + description` after they have been (a) translated to 繁中 if source was English, and (b) compared against original English text as well (so that `SEC` / `BlackRock` / `ETF` etc. are caught regardless of translation).

> Each article may match multiple categories. If none match, label as `other`. **No sentiment scoring** is computed — these are topical labels only.

## Category Definitions

### `regulation` — 監管 / 法規

Regulatory actions, government policy, lawsuits, enforcement. Used when the news is primarily about how authorities (national or supranational) shape the crypto industry.

| Lang | Keywords |
|------|----------|
| EN   | `SEC `, `CFTC`, `DOJ`, `FinCEN`, `regulator`, `regulation`, `lawsuit`, `sue`, `subpoena`, `ban `, `banned`, `enforcement`, `compliance`, `MiCA`, `executive order` |
| 繁中 | `監管`, `法規`, `金管會`, `央行`, `證交會`, `訴訟`, `禁止`, `禁令`, `法案`, `違規`, `處罰`, `罰款`, `查緝` |

### `institution` — 機構 / ETF

Institutional adoption, ETF flows, public-company treasury moves, large-fund accumulation.

| Lang | Keywords |
|------|----------|
| EN   | `ETF`, `BlackRock`, `Fidelity`, `Grayscale`, `MicroStrategy`, ` Strategy `, `treasury`, `institutional`, `pension fund`, `sovereign`, `ARK Invest`, `Coinbase Institutional` |
| 繁中 | `機構`, `上市公司`, `持倉`, `財庫`, `基金`, `主權基金`, `退休基金`, `現貨 ETF` |

### `listing` — 上架 / 交易所

Coin listings / delistings, exchange operational events, liquidity migrations.

| Lang | Keywords |
|------|----------|
| EN   | `listing`, ` list `, `delist`, `delisting`, `exchange`, `liquidity migration`, `pair launch` |
| 繁中 | `上架`, `下架`, `上線`, `交易所`, `掛牌`, `交易對` |

### `tech` — 技術 / 網路

Protocol upgrades, hard forks, mainnet launches, scaling, cryptography research.

| Lang | Keywords |
|------|----------|
| EN   | `hard fork`, `soft fork`, `upgrade`, `mainnet`, `testnet`, `halving`, `protocol`, `L2`, `layer 2`, `rollup`, `zk`, `sharding`, `consensus` |
| 繁中 | `升級`, `主網`, `硬分叉`, `軟分叉`, `減半`, `協議`, `共識`, `分片`, `第二層` |

### `market` — 市場 / 價格

Pure price action, breakouts, sell-offs, ATH/ATL events, technical analysis (without prediction).

| Lang | Keywords |
|------|----------|
| EN   | `surge`, `plunge`, `rally`, `all-time high`, ` ATH `, `breakout`, `sell-off`, `crash`, `pump`, `dump`, `support`, `resistance` |
| 繁中 | `飆漲`, `暴跌`, `突破`, `新高`, `創高`, `崩盤`, `拉升`, `回檔`, `支撐`, `阻力` |

### `defi` — DeFi

Decentralized finance: lending, staking yield, AMM, liquidity provision.

| Lang | Keywords |
|------|----------|
| EN   | `DeFi`, `lending`, `borrow`, `yield`, `liquidity`, `TVL`, `AMM`, `vault`, `Aave`, `Uniswap`, `Maker`, `liquid staking` |
| 繁中 | `去中心化金融`, `借貸`, `流動性`, `收益農場`, `挖礦`, `質押` |

### `nft` — NFT / GameFi

NFT marketplaces, collections, GameFi, metaverse projects.

| Lang | Keywords |
|------|----------|
| EN   | `NFT`, `GameFi`, `metaverse`, `Pudgy Penguins`, `Bored Ape`, `Magic Eden`, `OpenSea` |
| 繁中 | `遊戲`, `鏈遊`, `元宇宙`, `數位藏品` |

### `security` — 安全 / 攻擊

Hacks, exploits, rug pulls, scams, phishing, vulnerability disclosures.

| Lang | Keywords |
|------|----------|
| EN   | `hack`, `exploit`, `rug pull`, ` rug `, `scam`, `phishing`, `vulnerability`, `breach`, `stolen`, `drain` |
| 繁中 | `駭客`, `攻擊`, `詐騙`, `盜竊`, `漏洞`, `釣魚`, `跑路`, `被駭` |

### `other`

Articles that match no category above. Often: industry general commentary, opinion pieces, conference recaps.

## Matching Algorithm (reference implementation)

```python
def classify(title: str, description: str, title_en: str = '', desc_en: str = '') -> list[str]:
    """Return list of matched categories. Empty list → use ['other']."""
    text = f"{title} {description} {title_en} {desc_en}".lower()
    matched = []
    for cat, keywords in CATEGORY_MAP.items():
        for kw in keywords:
            if kw.lower() in text:
                matched.append(cat)
                break
    return matched if matched else ['other']
```

## Maintenance Notes

- **Adding a new keyword**: pick the category most likely to be the article's *primary* topic. Avoid adding generic terms that fire across many categories (e.g. `crypto`, `coin`, `market`).
- **Multi-language matching**: always think about both English and 繁中 forms. After T8 pre-translation, the article will have both fields available — match against both to maximize recall.
- **Avoid sentiment terms**: `bullish`, `bearish`, `breakout` (positive) etc. should be in `market` (neutral topical label), NOT split into "bullish news" / "bearish news". Sentiment classification is explicitly out of scope (see `CLAUDE.md`).
- **Avoid ML drift**: this is a **deterministic keyword matcher**, not an LLM classifier. If recall is poor, expand the keyword list. Do NOT introduce embedding-based or LLM-based classifiers (transparency + reproducibility requirements).

## Periodic Review

Review this file when:
- Adding a new RSS source (may surface new vocabularies)
- BitoPro listing additions create new topical clusters (e.g., a Layer-2 native token)
- 監管 landscape shifts (new acronyms / agencies emerge)

Last review: 2026-04-27 (initial v1.4.0 release).
