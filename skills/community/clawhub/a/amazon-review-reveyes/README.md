# amazon-review-reveyes — OpenClaw Skill

An OpenClaw Skill that fetches Amazon product reviews via the [Reveyes API](https://www.reveyes.cn).

Submit an ASIN → get star distribution, critical review summaries, and full review data.  
Supports **20 marketplaces**: US · CA · MX · UK · DE · FR · IT · ES · NL · SE · PL · BE · IE · JP · IN · SG · AE · SA · AU · BR

---

## Installation

### From ClawHub

```bash
clawhub install amazon-review-reveyes
```

### Manual

```bash
git clone https://github.com/zhuojiuya/Amazon-Review.git
cp -r Amazon-Review/reveyes-skill ~/.openclaw/workspace/skills/amazon-review-reveyes
```

Then install the Python dependency:

```bash
pip install reveyes
```

---

## Setup

Set your Reveyes API key as an environment variable.  
Get your key free at **[www.reveyes.cn](https://www.reveyes.cn)** → Dashboard → API Keys.

```bash
# Add to ~/.zshrc or ~/.bashrc
export REVEYES_API_KEY="your_api_key_here"
```

Or configure in `~/.openclaw/openclaw.json`:

```json
{
  "env": {
    "REVEYES_API_KEY": "your_api_key_here"
  }
}
```

---

## Usage

Just talk to your OpenClaw agent naturally:

```
帮我抓一下 B08N5WRWNW 美国站的评论
```

```
查一下 B09G9FPHY6 德国站的差评，抓3页
```

```
分析这个 ASIN 在日本站的用户反馈：B07XJ8C8F7
```

```
B08N5WRWNW US 站好评有多少？
```

### Output Example

```
📦 ASIN: B08N5WRWNW  |  站点: US  |  共 87 条评论

⭐ 评分分布：
  ★★★★★  42 条 (48%)  ████████████
  ★★★★☆  18 条 (21%)  █████
  ★★★☆☆   8 条  (9%)  ██
  ★★☆☆☆   5 条  (6%)  █
  ★☆☆☆☆  14 条 (16%)  ████

📝 典型差评（最近 5 条）：
1. ★★ "Stopped working after 2 weeks"
   Bought this expecting quality but it broke down...

2. ★★ "Not as described"
   The color is completely different from the photos...
```

---

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `asin` | Amazon ASIN (10-char, required) | — |
| `marketplace` | Site code (US/UK/DE/JP...) | `US` |
| `pages` | Pages to scrape, 1 page ≈ 10 reviews | `2` |
| `filter_star` | `all_stars` `positive` `critical` `five_star`…`one_star` | `all_stars` |

---

## Credits

- 1 credit per page scraped
- Unused credits are automatically refunded
- View balance & top up: [www.reveyes.cn](https://www.reveyes.cn)

---

## Links

- Reveyes official site: https://www.reveyes.cn
- Python SDK on PyPI: https://pypi.org/project/reveyes/
- GitHub: https://github.com/zhuojiuya/Amazon-Review

## License

MIT
