# 🌍 Daily Geopolitical TikTok Reporter

Generate daily TikTok scripts about geopolitical news using free RSS sources.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Option A: Using virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option B: System-wide (if allowed)
pip install --break-system-packages -r requirements.txt

# Option C: Using pipx
pipx install feedparser pyyaml python-dateutil requests
```

### 2. Generate Your First TikTok Script

```bash
# Basic usage - last 24 hours
python3 generate_daily_report.py

# Custom options
python3 generate_daily_report.py --hours 12 --scripts 5 --region middle_east

# Focus on specific topics
python3 generate_daily_report.py --topic conflicts --hours 6
```

### 3. Review Generated Scripts

Scripts are saved in `generated_scripts_[timestamp]/` directory:
- Individual story scripts (1_second_story_title.txt, etc.)
- Daily report script (daily_report.txt)
- Metadata JSON file

## 📋 Usage Examples

### Generate scripts for last 12 hours:
```bash
python3 generate_daily_report.py --hours 12
```

### Focus on Middle East conflicts:
```bash
python3 generate_daily_report.py --region middle_east --topic conflicts
```

### Generate 5 high-importance stories:
```bash
python3 generate_daily_report.py --scripts 5 --hours 48
```

## ⛙ Configuration

Edit `config/config.yaml` to customize:

- **News sources**: Add custom RSS feeds
- **Regional focus**: Prioritize specific geographic areas  
- **Topic preferences**: Focus on conflicts, diplomacy, elections, etc.
- **TikTok style**: Adjust script timing, tone, and hashtags
- **Scheduling**: Set up automated daily reports

## 📤 Automating Daily Reports

### Using Cron (Linux/macOS):
```bash
# Edit crontab
crontab -e

# Add this line (runs every day at 8 AM UTC)
0 8 * * * cd /path/to/skill && python3 generate_daily_report.py --scripts 3
```

### Using Systemd Timer (Linux):
```bash
# Create service file at /etc/systemd/system/geo-tiktok.service
# See config/config.yaml for example
```

### Using OpenClaw Heartbeat:
Add to your workspace HEARTBEAT.md:
```markdown
- Check for new geopolitical news
- Generate daily TikTok scripts if significant events found
```

## 📊 Sample Output

Each generated TikTok script includes:

- 🎵 **Hook** (3-5 seconds): Attention-grabbing opening
- 🌍 **Context** (10-15 seconds): Background and significance  
- 📰 **News** (30-45 seconds): Main story and developments
- 💡 **Impact** (10-15 seconds): Why it matters
- 📈 **Next** (5 seconds): What to watch for
- 🏷️ **Hashtags**: Optimized for TikTok discovery

## 🎯 Next Steps

1. **Review generated scripts** in output directory
2. **Customize content** to match your style
3. **Create TikTok videos** using the scripts
4. **Post strategically** during peak hours
5. **Engage with audience** in comments
6. **Schedule daily generation** for consistent content

## 💡 Pro Tips

- **Peak posting times**: 12 PM, 7 PM local time
- **Trending sounds**: Search "news," "break," "intense" in TikTok library
- **Visuals**: Use stock footage, maps, news clips
- **Engagement**: Reply to comments in first 30 minutes
- **Consistency**: Post daily for algorithm favorability

## 🛠️ Troubleshooting

### ModuleNotFoundError: No module named 'feedparser'
```bash
# Install dependencies properly
pip install -r requirements.txt
```

### No news articles found
- Check your internet connection
- Verify RSS sources are accessible
- Try increasing --hours parameter
- Check if news sources require authentication

### Scripts too long/short
- Edit `config/config.yaml` timing section
- Adjust individual segment durations
- Target total 60-90 seconds for optimal TikTok performance

## 📚 Advanced Usage

### Custom RSS Sources
Edit `config/config.yaml`:
```yaml
news_gathering:
  custom_sources:
    my_source:
      url: "https://example.com/rss.xml"
      region: "asia"
      name: "My Custom News"
```

### Custom Hashtag Strategy
Edit `content_gen/tiktok_generator.py`:
- Add custom hooks in `HOOKS` list
- Add hashtags to `HASHTAGS` dictionary
- Modify transition phrases in `TRANSITIONS`

### Regional Filtering
Available regions:
- `middle_east`, `europe`, `asia`, `americas`, `africa`

### Topic Filtering  
Available topics:
- `conflicts`, `diplomacy`, `sanctions`, `elections`, `alliances`, `crisis`

## 🌐 Integration with Other Platforms

### Blog Integration
Modify script to also generate blog posts in Markdown format.

### YouTube Shorts
Use same scripts but format for YouTube Shorts (max 60 seconds).

### Custom Website
Generate JSON/HTML output for your own website.

## 📞 Support

For issues or questions:
1. Check this README
2. Review config files
3. Examine error logs
4. Check network connectivity

---

**Skill Version:** 1.0.0  
**Created for:** TikTok content creators focused on geopolitics  
**License:** MIT

Enjoy creating engaging geopolitical content! 🌍🎬