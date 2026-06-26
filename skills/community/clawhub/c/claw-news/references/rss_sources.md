# News Sources Configuration

Default RSS/Atom sources for the newsman skill.

Add, remove, or modify sources as needed. Each source needs:
- `name`: Unique identifier
- `url`: RSS/Atom feed URL
- `category`: Category for filtering (tech, finance, world, science, sports)
- `language`: Language code (optional, default: en)

## Technology

```yaml
- name: techcrunch
  url: https://techcrunch.com/feed/
  category: tech
  language: en

- name: the-verge
  url: https://www.theverge.com/rss/index.xml
  category: tech
  language: en

- name: ars-technica
  url: http://feeds.arstechnica.com/arstechnica/index
  category: tech
  language: en

- name: wired
  url: https://www.wired.com/feed/rss
  category: tech
  language: en

- name: bbc-tech
  url: http://feeds.bbci.co.uk/news/technology/rss.xml
  category: tech
  language: en
```

## Finance

```yaml
- name: bloomberg
  url: https://feeds.bloomberg.com/bloomberg/markets.rss
  category: finance
  language: en

- name: reuters-finance
  url: https://www.reutersagency.com/feed/?taxonomy=markets&post_type=reuters-best
  category: finance
  language: en

- name: coindesk
  url: https://www.coindesk.com/arc/outboundfeeds/rss/
  category: finance
  language: en
```

## World News

```yaml
- name: bbc-world
  url: http://feeds.bbci.co.uk/news/world/rss.xml
  category: world
  language: en

- name: reuters-world
  url: https://www.reutersagency.com/feed/?taxonomy=markets&post_type=reuters-best
  category: world
  language: en
```

## Science

```yaml
- name: nature-news
  url: https://www.nature.com/nature.rss
  category: science
  language: en

- name: scientific-american
  url: https://www.scientificamerican.com/rss/news.cfm
  category: science
  language: en

- name: arxiv-cs
  url: http://export.arxiv.org/rss/cs
  category: science
  language: en
```

## Sports

```yaml
- name: espn
  url: https://www.espn.com/espn/rss/news
  category: sports
  language: en

- name: bbc-sport
  url: http://feeds.bbci.co.uk/sport/rss.xml
  category: sports
  language: en
```

## Chinese Sources

```yaml
- name: 36kr
  url: https://36kr.com/feed
  category: tech
  language: zh

- name: solidot
  url: https://www.solidot.org/index.rss
  category: tech
  language: zh
```

## Notes

- Some feeds may require custom parsing due to format variations
- Rate limiting: Most RSS servers accept 1 request per minute per feed
- Cache recommended: Store fetched items to avoid re-fetching
- Fallback: Use `web_search` or `web_fetch` for sites without RSS
