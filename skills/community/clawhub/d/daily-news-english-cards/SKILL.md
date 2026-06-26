Generate daily news English learning cards with comic illustrations.

Search the latest 24-hour news across 5 categories (Politics, Finance, Sports,
Entertainment, Technology), create vocabulary-rich learning cards with AI-generated
comic art and bilingual summaries.

Use when the user asks to "generate English learning cards", "create news cards",
"daily English cards", "新闻英语卡片", "每日英语学习", "生成学习卡片",
or similar requests related to news-based English learning content.

---

## Prerequisites

Three API keys are required. Set them as environment variables before running:

| Variable | Service | Get Key |
|---|---|---|
| `TAVILY_API_KEY` | Tavily Search (news) | https://tavily.com |
| `DEEPSEEK_API_KEY` | DeepSeek (text gen) | https://platform.deepseek.com |
| `OPENROUTER_API_KEY` | OpenRouter (image gen) | https://openrouter.ai |

Optional:

| Variable | Default | Description |
|---|---|---|
| `IMAGE_MODEL` | `google/gemini-3.1-flash-image-preview` | OpenRouter image model (Nano Banana 2) |

## Steps

1. **Verify environment variables are set**

   Check that `TAVILY_API_KEY`, `DEEPSEEK_API_KEY`, and `OPENROUTER_API_KEY` are
   configured. If any are missing, prompt the user to set them.

2. **Install dependencies**

   ```bash
   pip install -q tavily-python openai Pillow requests
   ```

3. **Run the generator script**

   ```bash
   python daily-news-english-cards/scripts/generate_cards.py
   ```

   The script will:
   - Search 5 categories of news via Tavily
   - Generate vocabulary & summaries via DeepSeek
   - Create comic illustrations via OpenRouter (Nano Banana 2)
   - Composite final learning cards via Pillow

4. **Present results**

   Show the user the generated card images from `output/daily-news-cards/{date}/`.

## Customization

```bash
# Custom categories
python daily-news-english-cards/scripts/generate_cards.py --categories politics sports technology

# Custom output directory
python daily-news-english-cards/scripts/generate_cards.py --output-dir ./my-cards
```

## Output

Each run produces in `output/daily-news-cards/{date}/`:
- `card_{category}_{date}.png` — Final learning cards (1080×1440px)
- `comic_{category}_{date}.png` — Raw comic illustrations
- `content_{date}.json` — Structured learning content data

## Architecture

```
daily-news-english-cards/
├── SKILL.md                    # This file
├── requirements.txt            # Python dependencies
└── scripts/
    └── generate_cards.py       # Self-contained generator (all logic in one file)
```

The script is fully portable — works with Cursor, OpenClaw, or standalone CLI.
No IDE-specific tools are used; all external calls go through standard APIs.
