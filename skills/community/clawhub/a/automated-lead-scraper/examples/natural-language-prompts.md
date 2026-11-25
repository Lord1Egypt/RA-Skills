# Example requests that should trigger this skill

- "Scrape these websites and extract publicly available business contact emails: acmeplumbing.com, bobsroofing.net …"
- "Here's a CSV of 120 company sites — find their contact emails."
- "Resume the lead scraping run in ./lead-scraper-runs/q4-plumbers."
- "Start over on that list, but keep the old results."

Expected agent flow: ask for URLs if missing → `validate-input.js` → `npm install` → run → monitor `PROGRESS` lines
→ resume if interrupted → `summarize-run.js` → hand over `output.csv` (+ `suspicious.csv`).
