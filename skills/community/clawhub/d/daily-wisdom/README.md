# 📜 Daily Wisdom

![banner](./banner.png)

> AI-generated historical anecdotes from 100+ sources across every major civilization. A new story every day, never repeats.

A prompt system that turns any LLM into a cultural historian. Each day it generates a unique story with an original-language quote, a vivid narrative, and a surprising modern connection.

## 🚀 Use It Anywhere

### With ChatGPT / Claude / any LLM
Copy the prompt from [`SKILL.md`](./SKILL.md#standard-daily-recommended) and paste it into any AI chat. That's it. No install, no dependencies.

### With OpenClaw (automated daily delivery)
Set it up as a cron skill for automated daily messages to WhatsApp, Telegram, Slack, or Discord. See [setup instructions](#automated-setup-openclaw).

### With any cron + LLM API
Use the prompt template with any scheduling system + API call (GitHub Actions, n8n, Make, etc.).

## ✨ What It Does

- **Generates a new story every day** from a pool of 100+ historical figures, epics, and traditions
- **Research-backed** — the agent web-searches to verify quotes, dates, and facts before writing (no hallucinated quotes)
- **Original-language quotes** — Latin, Arabic, Japanese, Ancient Greek, Old Norse, Sanskrit, Mandinka, and more
- **Modern connections** — each story links to something relevant today
- **Never repeats** — a history file tracks what's been covered
- **Multiple formats** — standard, Twitter thread, minimal, deep dive

## 🔍 How It Works

1. Agent reads the **history file** to see what's already been covered
2. Picks a source from the pool, maximizing variety across civilizations
3. **Searches the web** to find accurate quotes, dates, and lesser-known details
4. Writes the story with original-language quote, narrative, and modern connection
5. Delivers via your preferred channel
6. Appends today's topic to the history file

No database, no API, no dependencies — just a prompt template + an LLM with web search access.

## 📦 Example Output

```
📜 Anansi the Spider — Ashanti Oral Tradition, West Africa

> "Ananse, the spider, owns all stories that are told."
> — Ashanti saying

The Story: Long ago, all stories belonged to Nyame, the Sky God.
Anansi asked to buy them. Nyame named an impossible price: capture
a python, hornets, an invisible fairy, and a leopard. Anansi used
no force — only cleverness. He tricked each one into trapping
themselves...

💡 Modern Connection: Anansi is the original hacker — he doesn't
fight stronger opponents, he exploits their assumptions. Every
social engineering attack follows the Anansi pattern...
```

See 11 examples across civilizations in [`examples/`](./examples/).

## 📂 Repository

```
daily-wisdom/
├── README.md       ← You are here
├── SKILL.md        ← Prompt templates (the actual product)
├── history.md      ← Repeat tracker template
└── examples/       ← 11 sample outputs
    ├── african-sundiata.md          ← Mali Empire
    ├── classical-marcus-aurelius.md ← Rome
    ├── classical-seneca.md          ← Rome
    ├── fareast-musashi.md           ← Japan
    ├── indian-chanakya.md           ← India
    ├── islamic-ibn-sina.md          ← Persia
    ├── mythology-anansi.md          ← West Africa
    ├── mythology-gilgamesh.md       ← Sumer
    ├── norse-havamal.md             ← Scandinavia
    ├── turkic-nasreddin.md          ← Anatolia
    └── format-thread.md             ← Twitter thread format
```

## 🎯 Source Pool

All traditions drawn equally — the agent maximizes variety across the full pool.

| Region | Key Sources |
|--------|-------------|
| **Classical** | Seneca, Marcus Aurelius, Epictetus, Heraclitus, Diogenes, Socrates |
| **Far East** | Sun Tzu, Musashi, Confucius, Laozi, Chanakya, Zen koans |
| **African** | Sundiata Keita, Mansa Musa, Anansi, Ubuntu, Timbuktu scholars |
| **Islamic Golden Age** | Ibn Sina, Al-Khwarizmi, Ibn Khaldun, Mevlana, Ibn Battuta |
| **Ancient & Myth** | Gilgamesh, Prometheus, Egyptian wisdom, Zoroastrian, Sumerian proverbs |
| **Norse & Celtic** | Hávamál, Odin, Ragnarök, Viking sagas |
| **Turkic & Central Asian** | Dede Korkut, Orhon inscriptions, Manas, Nasreddin Hoca |
| **Polynesian & Indigenous** | Māui, Aboriginal Dreamtime |
| **Renaissance & Modern** | Machiavelli, Montaigne, Leonardo, Ada Lovelace, Tesla |

## ⚙️ Customization

### Favor a region
```
PREFERENCE: Favor [Classical/Far East/African/Norse/etc.] sources,
but still mix in other traditions regularly.
```

### Change language
```
Write entirely in [Spanish/German/French/etc.].
Translate all quotes to [target language].
```

### Weekend deep dives
Use the Deep Dive variant in SKILL.md — longer stories, multiple quotes, more context.

## <a name="automated-setup-openclaw"></a>🤖 Automated Setup (OpenClaw)

1. Copy this repo into your workspace: `git clone https://github.com/AytuncYildizli/daily-wisdom.git skills/daily-wisdom`
2. Create history file: `cp skills/daily-wisdom/history.md memory/anecdote-history.md`
3. Ask your agent: *"Set up a daily wisdom cron at 07:30 using the daily-wisdom skill"*

See [`SKILL.md`](./SKILL.md) for full cron configuration and all prompt templates.

## 🧪 Quality Philosophy

1. **Specificity > generality**: "In 1235, at the Battle of Kirina..." beats "An African king once..."
2. **Original language = impact**: Even unreadable scripts create emotional resonance
3. **Modern connections must surprise**: Not "this is relevant" but *how* it's relevant
4. **Vary the register**: Profound → funny → dark → tactical → minimal

## 🤝 Contributing

Add examples: `examples/{region}-{subject}.md`

PRs welcome for new traditions, better modern connections, translations, and format variants.

## 📄 License

MIT

---

*Works with any LLM. Optionally integrates with [OpenClaw](https://github.com/openclaw/openclaw) for automated daily delivery.*
