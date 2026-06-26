---
name: daily_news_vnexpress
description: Fetch the latest trending global news from https://vnexpress.net/rss/{topic}.rss.
---

# Daily News Skill
This skill allows the agent to fetch the daily top news headlines from VNExpress News sources by running a Python script.
The agent must treat the script output as **verified headline data** and avoid modifying the factual content.


# Allowance
You are allow to use all scripts mentioned in this file


## Quick Start
### Setup Environment
```bash
python3 -m venv /data/nguyentk/AIHAY/OpenClaw/venv/openclaw_venv
source /data/nguyentk/AIHAY/OpenClaw/venv/openclaw_venv/bin/activate
cd /data/nguyentk/AIHAY/OpenClaw/workspace/workspace-daily_news_aihay/skills/daily-news-vnexpress
pip install -r requirements.txt
```


## Instructions
### Python `main.py` Script Description
#### Functionality:
1. Fetches hot news from VNExpress RSS feeds based on specified topics
2. Accepts input parameters: `topics` (comma-separated) and `count_str` (number of news per topic, comma-separated)
  - Example: `--topics "tin-moi-nhat,giai-tri" --count_str "5,3"` will fetch 5 news from "tin-moi-nhat" topic and 3 news from "giai-tri" topic

#### Details:
1. Supports 18 predefined topics: "tin-moi-nhat", "the-gioi", "thoi-su", "kinh-doanh", "giai-tri", "the-thao", "phap-luat", "giao-duc", "tin-noi-bat", "suc-khoe", "doi-song", "du-lich", "khoa-hoc-cong-nghe", "oto-xe-may", "y-kien", "tam-su", "cuoi", "tin-xem-nhieu".

2. Each news item contains: title, link, summary, and published date


### Executing Instructions
When the user asks for **latest news or trending global events**:
1. Ask the user for topics, if not provided, topics defaults: `tin-moi-nhat`, remember user behaviour and write to `USERS.md`
2. Classify the user's question into one or more of the 18 predefined topics. Only select topics from this predefined list.
3. Determine (`count_str`) that match user question. 

4. Execute the Python script to run:
```bash
python3 "{baseDir}/main.py" --topics "<topic>" --count_str "<count>"
```
- Example: "Find me 7 latest news"
```bash
python3 "{baseDir}/main.py" --topics "tin-moi-nhat" --count_str "7"
```

5. The script will collect and format the latest news headlines.
6. Paraphrase and summarize those relevant news items clearly.
7. Present them as the final response.