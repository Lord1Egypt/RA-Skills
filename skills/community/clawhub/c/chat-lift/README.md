# ChatLift — AI Conversation Exporter & Archive

**Import, search, and archive your AI conversations.**

Extract ChatGPT, Claude, and Gemini conversation exports into clean, indexed formats. Full-text search. Static HTML archive with search bar. No server required.

---

## What It Does

ChatLift converts AI conversation exports into portable, searchable formats:

1. **Import** - Parse ChatGPT/Claude/Gemini exports
2. **Convert** - Generate Markdown, HTML, and JSON
3. **Search** - Full-text search across all conversations
4. **Archive** - Static HTML archive with navigation

### Why This Exists

AI chat platforms:
- Lock your conversations in proprietary formats
- Make search difficult or impossible
- Can delete your data at any time

ChatLift gives you control:
- Own your conversation history
- Search across all platforms
- Portable formats (Markdown, HTML, JSON)
- Works offline forever

---

## Quick Start

### Install

No dependencies! Python 3.7+ stdlib only.

```bash
# Copy config (optional)
cp config_example.py config.py
```

### Import Conversations

Export your conversations from ChatGPT, Claude, or Gemini, then:

```bash
# Import ChatGPT export
python3 chat_lift.py chatgpt conversations.json

# Import Claude export
python3 chat_lift.py claude claude-export.json

# Import Gemini export
python3 chat_lift.py gemini gemini-conversations.json
```

Generates:
- `chat-archive/markdown/*.md` - Human-readable markdown
- `chat-archive/html/*.html` - Styled HTML pages
- `chat-archive/json/*.json` - Structured JSON

### Search Conversations

```bash
# Search all conversations
python3 chat_search.py search --query "machine learning"

# Search with regex
python3 chat_search.py search --query "python.*async" --regex

# Search by date range
python3 chat_search.py date --start-date 2026-01-01 --end-date 2026-02-01

# Get archive statistics
python3 chat_search.py stats
```

### Generate HTML Archive

```bash
# Generate static archive website
python3 chat_archive.py

# Open chat-archive/web/index.html in browser
```

The HTML archive includes:
- **Search bar** - Filter by keyword or source
- **Navigation** - Browse all conversations
- **No server needed** - Pure static files

---

## Usage Examples

### Import Multiple Exports

```bash
# Import all your platforms
python3 chat_lift.py chatgpt chatgpt-export.json
python3 chat_lift.py claude claude-export.json
python3 chat_lift.py gemini gemini-export.json

# Generate unified archive
python3 chat_archive.py
```

### Search Across All Platforms

```python
from chat_search import ConversationSearcher

searcher = ConversationSearcher('chat-archive')

# Find all conversations mentioning "agent"
results = searcher.search('agent')

for result in results:
    print(f"{result['conversation']['title']}")
    print(f"  Source: {result['conversation']['source']}")
    print(f"  Matches: {result['total_matches']}\n")
```

### Custom Output Formats

```bash
# Only generate markdown
python3 chat_lift.py chatgpt export.json --formats markdown

# Generate all formats
python3 chat_lift.py chatgpt export.json --formats markdown html json

# Custom output directory
python3 chat_lift.py chatgpt export.json --output-dir ~/my-chats
```

### Filter Search Results

```bash
# Search only ChatGPT conversations
python3 chat_search.py search --query "python" --source chatgpt

# Search only user messages
python3 chat_search.py search --query "explain" --role user

# Case-sensitive search
python3 chat_search.py search --query "API" --case-sensitive
```

---

## Export Instructions

### ChatGPT

1. Go to [chat.openai.com](https://chat.openai.com)
2. Settings → Data controls → Export data
3. Wait for email with download link
4. Download `conversations.json`

### Claude

1. Go to [claude.ai](https://claude.ai)
2. Settings → Privacy → Export your data
3. Download export file
4. Extract JSON from archive

### Gemini

1. Go to [gemini.google.com](https://gemini.google.com)
2. Account settings → Download your data
3. Select Gemini conversations
4. Download export file

---

## File Formats

### Markdown

```markdown
# Conversation Title

**Source:** chatgpt  
**ID:** abc123def456  
**Created:** 2026-02-21 10:30:00  

---

## USER

How do I deploy a Flask app?

*2026-02-21 10:30:15*

---

## ASSISTANT

Here's how to deploy a Flask application...

*2026-02-21 10:30:45*

---
```

### JSON

```json
{
  "id": "abc123def456",
  "title": "Conversation Title",
  "source": "chatgpt",
  "create_time": 1708512600,
  "messages": [
    {
      "role": "user",
      "content": "How do I deploy a Flask app?",
      "timestamp": 1708512615
    },
    {
      "role": "assistant",
      "content": "Here's how to deploy a Flask application...",
      "timestamp": 1708512645
    }
  ]
}
```

### HTML

Clean, styled HTML with:
- Responsive design
- Color-coded messages
- Timestamps
- Source badges

---

## Archive Structure

```
chat-archive/
├── markdown/          # Human-readable markdown
│   ├── abc123.md
│   └── def456.md
├── html/              # Styled HTML pages
│   ├── abc123.html
│   └── def456.html
├── json/              # Structured JSON
│   ├── abc123.json
│   └── def456.json
└── web/               # Static HTML archive
    ├── index.html     # Browse/search interface
    ├── abc123.html    # Conversation pages
    ├── def456.html
    ├── style.css      # Styling
    └── search.js      # Search functionality
```

---

## Search Features

### Full-Text Search

```bash
# Simple text search
python3 chat_search.py search --query "machine learning"

# Case-sensitive
python3 chat_search.py search --query "API" --case-sensitive

# Regex patterns
python3 chat_search.py search --query "python.*async" --regex
```

### Filters

```bash
# Filter by source platform
python3 chat_search.py search --query "code" --source chatgpt

# Filter by message role
python3 chat_search.py search --query "explain" --role assistant

# Combine filters
python3 chat_search.py search --query "deploy" --source claude --role user
```

### Date Range

```bash
# Conversations from specific date range
python3 chat_search.py date --start-date 2026-01-01 --end-date 2026-02-01

# All conversations after date
python3 chat_search.py date --start-date 2026-02-01

# All conversations before date
python3 chat_search.py date --end-date 2026-02-01
```

### Statistics

```bash
python3 chat_search.py stats
```

Shows:
- Total conversations
- Total messages
- Word count
- Breakdown by source
- Breakdown by role

---

## HTML Archive

### Features

- **Search bar** - Real-time filter as you type
- **Source filter** - Filter by ChatGPT, Claude, Gemini
- **Clean design** - Responsive, mobile-friendly
- **No server** - Pure static HTML/CSS/JS
- **Works offline** - Archive travels with you

### Customization

Edit `chat-archive/web/style.css` to customize:
- Colors
- Fonts
- Layout
- Message styling

The archive is pure HTML/CSS/JS - modify freely.

---

## Integration

### Python API

```python
from chat_lift import ConversationImporter
from chat_search import ConversationSearcher
from chat_archive import ArchiveGenerator

# Import conversations
importer = ConversationImporter('chat-archive')
conversations = importer.import_chatgpt('export.json')

for conv in conversations:
    importer.save_conversation(conv, formats=['markdown', 'json'])

# Search
searcher = ConversationSearcher('chat-archive')
results = searcher.search('python programming')

# Generate HTML archive
generator = ArchiveGenerator('chat-archive')
generator.generate_archive()
```

### Batch Processing

```python
import glob
from chat_lift import ConversationImporter

importer = ConversationImporter('chat-archive')

# Import all ChatGPT exports in directory
for export_file in glob.glob('exports/chatgpt-*.json'):
    conversations = importer.import_chatgpt(export_file)
    for conv in conversations:
        importer.save_conversation(conv)

print("All exports imported!")
```

---

## Limitations

See [LIMITATIONS.md](LIMITATIONS.md) for details.

**Key constraints:**
- Export formats vary by platform version
- No real-time sync (manual export/import)
- Search is text-based (not semantic)
- Large archives (10,000+ conversations) may be slow

---

## License

MIT License - See [LICENSE](LICENSE)

**Author:** Shadow Rose

---

## Why This Exists

Your AI conversations are valuable:
- Learning history
- Project documentation
- Personal knowledge base

But they're locked in proprietary platforms that:
- Can change or delete your data
- Make search difficult
- Don't export cleanly

ChatLift gives you:
- **Ownership** - Your data, your formats
- **Portability** - Markdown, HTML, JSON
- **Search** - Find anything instantly
- **Permanence** - Works offline forever

Take back your conversation history.


---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.
---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
