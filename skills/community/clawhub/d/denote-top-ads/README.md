# Denote Top Ads

Find popular, fast-rising and newly spotted ads for games and utility apps, and use their creatives to plan your next user acquisition test.

EN · [ZH](README.zh.md) · [JA](README.ja.md) · [KO](README.ko.md) · [ES](README.es.md) · [NL](README.nl.md) · [DE](README.de.md) · [FR](README.fr.md)

Denote collects and refreshes ad data daily across games and utility apps. Each crawl covers more than 60 million ad records. The charts summarize this data once a week. A free account gives you three charts for games or apps from the last completed week, with up to ten creatives per chart. [Explore Denote Top Ads](https://denote.net/top-ads).

| Free chart | What it shows |
| --- | --- |
| Trending Ads | See which creatives drew the most attention last week. |
| Rising Ads | Find creatives with the biggest week-over-week gain in popularity. |
| New Ads | Discover newly spotted creatives ranked by early popularity. |

## Get your first report

Run this command in your OpenClaw workspace. The skill requires Python 3.

```sh
git clone https://github.com/denote-developer/denote-top-ads.git skills/denote-top-ads
```

1. Start a new session and ask “What can Denote Top Ads help me find?”
2. [Create a free Denote account](https://denote.net/user/register). Already registered? Sign in. Create a Denote API key with the `top_ads:read` permission or add it to an existing key.
3. Save the key as `DENOTE_API_KEY` in your agent host’s secret settings. Then ask “Show me last week’s top app ads.” Your agent will fetch all three charts. Games are the default when you leave the category open.

Chat shows the top three ads per chart, one per row, with a video or preview link and duration. Trending and New show weekly creative score; Rising shows score increment and growth rate. Open the local report at the end of the reply for all returned ads. Select a card for inline playback, overview, trends, related ads and audience. The detail button opens the matching Denote workspace chart even when detail data is unavailable.

## A closer look

Ask “Open the second ad on the rising chart.” Top Ads Pro or Business includes available creative details such as performance and audience. All three weekly charts are free.

## Product screenshots

[![Open the three weekly charts from the Top Ads sidebar.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/top-ads-navigation.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/top-ads-navigation.jpg)

*Open the three weekly charts from the Top Ads sidebar.*

[![Trending ads in games for November 9–15, 2026, ranked by weekly popularity.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/trending-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/trending-ads.jpg)

*Trending ads in games for November 9–15, 2026, ranked by weekly popularity.*

[![Rising game ads with the largest week-over-week gains in popularity.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/rising-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/rising-ads.jpg)

*Rising game ads with the largest week-over-week gains in popularity.*

[![Newly spotted game ads ranked by early popularity.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/new-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/new-ads.jpg)

*Newly spotted game ads ranked by early popularity.*

[![Overview of the Vita Mahjong creative, including its format and estimated impressions.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/overview.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/overview.jpg)

*Overview of the Vita Mahjong creative, including its format and estimated impressions.*

[![Daily creative score for Vita Mahjong alongside reference lines.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/data-trend.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/data-trend.jpg)

*Daily creative score for Vita Mahjong alongside reference lines.*

[![Other ads using the Vita Mahjong creative, with advertiser and run dates.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/related-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/related-ads.jpg)

*Other ads using the Vita Mahjong creative, with advertiser and run dates.*

[![Vita Mahjong audience reach by country, age and gender.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/audience.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/audience.jpg)

*Vita Mahjong audience reach by country, age and gender.*
