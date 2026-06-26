---
name: f1-summary
description: "Summarize Formula 1 sessions (FP1, Qualifying, Race) using web search and fetch"
---

# F1 Session Summary Skill

Use this skill to get a quick summary of any Formula 1 session (FP1, FP2, FP3, Qualifying, Sprint, Race) for any Grand Prix.

## Workflow

1. Determine session type from user request (FP1, Qualifying, Race, etc.) and construct appropriate web_search query like "{Grand Prix} {session} results {date}"
2. Search for recent session results using web_search
3. Fetch detailed content from authoritative sources (formula1.com, motorsport sites)
4. Extract key information:
   - Top 3 finishers with times/gaps (or grid positions for qualifying)
   - Notable incidents (red flags, crashes, penalties)
   - Team performance highlights
   - Relevant context (Sprint weekend, upgrades, weather, championship implications)
5. Format concise summary in user's language (Italian by default for Ale)

## Example Usage

User asks: "Mi fai un riassunto delle fp1 di Canada di oggi"
- Search: "Canada Grand Prix FP1 results May 22 2026"
- Produce summary like: "Kimi Antonelli led Mercedes 1-2 in disrupted FP1..."

User asks: "Com'è andata la qualifica a Monaco?"
- Search: "Monaco Grand Prix Qualifying results May 25 2026" (or appropriate date)
- Produce summary like: "Verstappen ha preso la pole a Monaco con..."

User asks: "Come è andata la gara a Silverstone?"
- Search: "British Grand Prix Race results July 6 2026" (or appropriate date)
- Produce summary like: "Hamilton ha vinto a Silverstone dopo..."