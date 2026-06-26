# 📚 Daily Literature Search Skill

**Version:** 1.0.0  
**Author:** Your Name  
**License:** MIT  

Automated literature search system for academic researchers. Performs scheduled searches across multiple databases (PubMed, OpenAlex, Semantic Scholar), automatically deduplicates results, downloads open-access papers, and generates daily reports.

## 🚀 Quick Start

### 1. Install

```bash
# Clone or download the skill
cd daily-literature

# Run installer
./install.sh

# Configure
cp config.example.yaml config.yaml
# Edit config.yaml with your keywords and settings

# Set environment variables
cp .env.example .env
# Edit .env with your email and API keys
source .env
```

### 2. Test Run

```bash
# Manual test run
python3 scripts/daily_literature_search.py

# Check output
cat logs/daily_search_$(date +%Y-%m-%d).log
```

### 3. Enable Automation

The installer automatically sets up a cron job for daily execution at 6:30 AM.

```bash
# Verify cron job
crontab -l | grep daily_literature

# Or manually add:
# 30 6 * * * python3 /path/to/scripts/daily_literature_search.py
```

## 📋 Features

### Core Features

- ✅ **Multi-Source Search**: PubMed, OpenAlex, Semantic Scholar
- ✅ **Automatic Deduplication**: Batch + library comparison by DOI
- ✅ **OA Detection & Download**: Unpaywall integration
- ✅ **Smart Categorization**: Keyword-based classification
- ✅ **Daily Reports**: Markdown reports with statistics
- ✅ **Scheduled Execution**: Cron-based automation
- ✅ **Upload Analysis**: Auto-categorize manually uploaded papers

### Advanced Features

- 🔧 **Configurable**: YAML configuration file
- 🔧 **Environment Variables**: Secure API key management
- 🔧 **Logging**: Configurable log levels and rotation
- 🔧 **Notifications**: Email/Slack/DingTalk support (optional)

## 📁 Directory Structure

```
daily-literature/
├── SKILL.md                    # Skill metadata
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── install.sh                  # Installation script
├── config.example.yaml         # Configuration template
├── .env.example               # Environment variables template
│
├── scripts/
│   ├── daily_literature_search.py  # Main search script
│   ├── analyze_uploaded.py         # Upload analyzer
│   ├── utils.py                    # Utilities
│   └── classifier.py               # Paper classifier
│
├── tests/
│   └── test_classifier.py          # Unit tests
│
└── logs/                        # Generated logs (created by install)
```

## ⚙️ Configuration

### Basic Configuration (config.yaml)

```yaml
# Search keywords
search_keywords:
  - '"inotuzumab ozogamicin"'
  - '"CAR-T" AND "B-ALL"'
  - '"multiple myeloma"'

# Categories for classification
categories:
  B-ALL:
    directory: "B-ALL/raw"
    keywords:
      - "cd19"
      - "blinatumomab"
  MM:
    directory: "MM/raw"
    keywords:
      - "bcma"
      - "elranatamab"

# Search settings
max_results_per_keyword: 10
date_range_days: 7
sources:
  - pm  # PubMed
  - oa  # OpenAlex
  - s2  # Semantic Scholar
```

### Environment Variables (.env)

```bash
# Required for polite API access
USER_EMAIL="your@email.com"

# Optional: API keys for higher rate limits
SEMANTIC_SCHOLAR_API_KEY="your-s2-key"
OPENALEX_API_KEY="your-oa-key"

# Optional: Notifications
EMAIL_USERNAME="smtp-username"
EMAIL_PASSWORD="smtp-password"
NOTIFICATION_WEBHOOK="slack-or-discord-webhook"
```

## 📊 Usage Examples

### Manual Search

```bash
# Run search manually
python3 scripts/daily_literature_search.py

# With custom config
python3 scripts/daily_literature_search.py --config /path/to/config.yaml

# Dry run (no downloads)
python3 scripts/daily_literature_search.py --dry-run
```

### Analyze Uploads

```bash
# Analyze uploaded papers
python3 scripts/analyze_uploaded.py

# Custom upload directory
python3 scripts/analyze_uploaded.py --input /path/to/pdfs
```

### View Reports

```bash
# Today's report
cat logs/daily_search_$(date +%Y-%m-%d).md

# Search statistics
grep "检索汇总" logs/daily_search_*.md
```

## 🔍 How It Works

### Search Flow

```
1. Load configuration
   ↓
2. For each keyword:
   - Search PubMed
   - Search OpenAlex
   - Search Semantic Scholar
   ↓
3. Collect all results
   ↓
4. Deduplicate:
   - Remove batch duplicates (same DOI)
   - Remove library duplicates (existing papers)
   ↓
5. Filter by date (recent N days)
   ↓
6. For each unique paper:
   - Classify into category
   - Check OA status (Unpaywall)
   - Download if OA
   ↓
7. Generate report
```

### Classification Logic

Papers are classified using keyword matching:

```python
# Example: B-ALL classification
if "cd19" in title or "blinatumomab" in title:
    category = "B-ALL"
elif "bcma" in title or "elranatamab" in title:
    category = "MM"
else:
    category = "OTHER"
```

### Deduplication

Two-level deduplication:

1. **Batch Dedup**: Remove duplicates within search results
2. **Library Dedup**: Compare against existing papers by DOI

```python
# DOI normalization
doi = normalize_doi(paper_doi)  # lowercase, remove prefixes

# Check existence
if doi in existing_dois:
    skip_paper()
```

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest

# Run tests
cd daily-literature
python3 -m pytest tests/ -v
```

## 🛠️ Troubleshooting

### Common Issues

**Issue: No results found**
- Check search keywords in config.yaml
- Verify API access (try manual search)
- Check date_range_days (might be too restrictive)

**Issue: Papers not downloading**
- Check if papers are OA (Unpaywall API)
- Verify network connectivity
- Check disk space

**Issue: Cron job not running**
- Verify cron daemon: `systemctl status cron`
- Check cron logs: `grep CRON /var/log/syslog`
- Test manual execution first

**Issue: Classification errors**
- Review classification keywords in config.yaml
- Add domain-specific keywords
- Check paper titles/abstracts for matching terms

### Logs

```bash
# View latest logs
tail -f logs/daily_search_$(date +%Y-%m-%d).log

# Search for errors
grep ERROR logs/*.log

# Check cron execution
grep daily_literature logs/cron.log
```

## 📈 Performance

### Typical Execution Time

- **Search phase**: 30-60 seconds (depends on keywords)
- **Deduplication**: <5 seconds
- **Download phase**: 1-2 minutes per OA paper
- **Report generation**: <5 seconds

**Total**: ~5-10 minutes for 10 keywords

### Resource Usage

- **Memory**: <100MB
- **Disk**: Varies (1-5MB per PDF)
- **Network**: ~100MB per search session

## 🔒 Security

### API Keys

- Store in `.env` file (not committed to git)
- Use environment variables
- Never hardcode in scripts

### Rate Limits

| Source | Free Tier | With API Key |
|--------|-----------|--------------|
| PubMed | 10/sec | 10/sec |
| OpenAlex | Polite pool | Higher limits |
| Semantic Scholar | 100/min | 1000/min |

### Privacy

- All data stored locally
- No telemetry or analytics
- Email only used for API politeness

## 🤝 Contributing

### Development Setup

```bash
# Fork and clone
git clone https://github.com/yourusername/daily-literature.git
cd daily-literature

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # for testing

# Make changes and test
python3 -m pytest tests/ -v

# Submit PR
```

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings
- Add tests for new features

## 📄 License

MIT License - See LICENSE file for details.

## 🙏 Acknowledgments

- **PubMed** - Biomedical literature database
- **OpenAlex** - Open catalog of research papers
- **Semantic Scholar** - AI-powered research tool
- **Unpaywall** - Open-access database
- **literature-review skill** - Inspiration and API integration

## 📬 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: your@email.com

---

**Happy Researching! 🎓📚**
