# Data Collection Guide

## Table of Contents
1. [Data Source](#data-source)
2. [Input Formats](#input-formats)
3. [Data Points to Extract](#data-points-to-extract)
4. [Extraction Procedure](#extraction-procedure)

## Data Source

Base URL: `https://m.nowscore.com/Analy/Analysis/{match_id}.htm`

Use 捷報比分 (Nowscore) data provider on the page.

## Input Formats

Accept either format from user:
- **Match ID only**: e.g. `2908467` -> construct URL `https://m.nowscore.com/Analy/Analysis/2908467.htm`
- **Match description**: e.g. `2026.3.15 09:30 美职业 皇家盐湖城vs奥斯丁` -> search or confirm match ID with user

## Data Points to Extract

### 1. Asian Handicap (让球盘)
- Extract only rows labeled "即" (instant/live) and "早" (early/opening)
- Fields: home odds, handicap line, away odds
- Note which team is giving the handicap (If the giving team is away team, then the Asian Handicap(受讓) has a "-" symbol)
- Record all available bookmaker data

### 2. Over/Under (大小球盘)
- Extract only rows labeled "即" (instant/live) and "早" (early/opening)
- Fields: over odds, total goals line, under odds
- Record all available bookmaker data

### 3. European Odds (欧赔胜平负)
- Extract only rows labeled "即" (instant/live) and "早" (early/opening)
- Fields: home win odds, draw odds, away win odds
- Record all available bookmaker data (at least top 10)

### 4. Team Fundamentals & History (基本面信息)

#### Core Fundamentals (核心基本面)
- Recent form (last 5-10 matches: W/D/L, goals scored/conceded)
- Home/away performance (home win rate / away win rate)
- Season total goals scored / conceded (and per-game average)
- Home/away goals scored / conceded separately
- Last 10 same-venue matches (home team: last 10 home; away team: last 10 away)

#### Head-to-Head History (历史交锋)
- All available historical matches between these two teams
- Recent 3-5 years of H2H records: W/D/L, goal trends
- Average goals in H2H matches

#### League Standings (联赛排名)
- Current league table position for both teams
- Points gap between teams
- Games played difference

#### Match Importance (比赛重要性)
- Both teams' motivation for this match
- Relegation battle / title race / playoff implications
- Recent scheduling (double headers, fatigue factors)

### 5. Lineups & Detailed Data (首发阵容与详细数据)

#### IMPORTANT: Lineup Timing
- **Note**: Starting lineups are typically published 30-60 minutes before match kickoff
- If collecting data earlier than this window, mark lineup data as "not yet available"
- Re-check for lineups closer to kickoff time if user requests update
- If lineup not available, proceed with prediction using available squad depth info from bench

#### When Available, Extract:
- Starting XI for both teams
- Key player stats (goals/assists this season)
- Injury/suspension list (especially core players - impact assessment)
- Bench strength / notable substitutes

#### Enhanced Data for Over/Under (大小球增强)
- Half-time goals data (半场进球数/模式)
- Corner kicks statistics (角球数据)
- Goal difference distribution (净胜球分布: 净胜2+/1/0/-1/-2+)

## Extraction Procedure

1. Navigate to the match analysis page using `browser navigate`
2. Extract basic match info (teams, league, time, venue, weather)
3. Extract Asian handicap data from the "亚让" tab/section
4. Extract over/under data from the "进球数" tab/section
5. Extract European odds from the "胜平负" tab/section
6. Extract team fundamentals from the main analysis page
7. If available (near match time), extract lineup data from "阵容" section
8. If lineup not yet published, note this and proceed with available data
9. Compile all data into a structured format before proceeding to prediction

### Browser Navigation Tips
- The page may have multiple tabs for different data sections
- Use `browser act` to click between tabs if needed
- Use `browser console exec` with JavaScript to extract table data
- If data is loaded dynamically, wait for page to fully render before extraction

### Tabs to Navigate
- Main page: Team fundamentals, recent form, H2H
- 亚让 (Asian Handicap): Asian handicap odds
- 进球数 (Goals): Over/under odds
- 胜平负 (1X2): European odds
- 角球 (Corners): Corner kick data (if available)
- 阵容 (Lineups): Starting XI (timing-dependent)
