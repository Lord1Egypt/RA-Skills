# Prediction Framework

## Table of Contents
1. [Output Modes](#output-modes)
2. [Step 1: Data Organization](#step-1-data-organization)
3. [Step 2: Fundamental Analysis](#step-2-fundamental-analysis)
4. [Step 3: Odds Probability Calculation](#step-3-odds-probability-calculation)
5. [Step 4: Model Prediction](#step-4-model-prediction)
6. [Step 5: Win Probability & Betting Advice](#step-5-win-probability--betting-advice)

---

## Output Modes

User can specify preferred output format:

### Mode A: 简洁模式 (Concise)
Quick prediction results only - best for fast decisions:
- Match info summary
- Key odds data (main lines)
- Best pick with probability and EV
- Predicted score

### Mode B: 可视化模式 (Visual/Detailed)
Full analysis with tables and charts:
- Complete data tables (all odds, all bookmakers)
- Detailed step-by-step analysis
- Probability calculations with formulas
- Visual probability bars
- EV analysis for all options

**Default**: If user doesn't specify, use Mode B (Visual) for first prediction, then ask preference.

---

## Step 1: Data Organization

Organize all collected data into these categories:

### 1. Fundamentals
- Recent form (last 5-10 matches: W/D/L, goals scored/conceded)
- Home/away performance (home win% / away win%)
- Head-to-head records (last 3-5 years: W/D/L, goal trends)
- League standings and points gap
- Both teams' match motivation
- **If lineup not yet published**: Note "阵容未公布" and proceed with available data

### 2. Squad & Lineup
- Starting XI (if available - typically 30-60 min before kickoff)
- Key player stats (goals/assists)
- Injury/suspension list (especially core player absence impact)
- Bench depth (substitute player quality)
- **If unavailable**: Mark as "待公布" and use squad depth info only

### 3. Match Importance
- Both teams' motivation (relegation battle / title race / playoff fight)

### 4. European Odds (1X2)
- Complete home/draw/away odds data ("即" = instant and "早" = early/opening rows)
- **IMPORTANT**: Use "即" (instant/live) data for final calculation

### 5. Asian Handicap
- Complete handicap data ("即" and "早" rows)
- **CRITICAL**: Must record BOTH "早" (early) AND "即" (instant) data
- **FINAL CALCULATION**: Use "即" (instant/live) data only - this is the final odds before match
- Analyze line movement: if "早" → "即" changed (up/down), record the trend
- Rule: the team with lower European odds corresponds to the handicap-giving side (upper plate)
- Upper plate odds are on the handicap-giving team's side
- If the giving team is away team, then the Asian Handicap(受讓) has a "-" symbol

### 6. Over/Under
- Complete over/under data ("即" and "早" rows)
- **FINAL CALCULATION**: Use "即" (instant/live) data for final calculation

### 7. Enhanced Data (for Over/Under Model)
- Half-time goals patterns (半场进球模式)
- Corner kicks statistics (角球数据)
- Goal difference distribution (净胜球分布)

---

## Step 2: Fundamental Analysis

Perform deep analysis based on collected data:

### 2.1 Handicap Rationality Check
Use machine learning baseline model to analyze whether the handicap is reasonable.
- Determine if handicap is set deep (high) or shallow (low)
- Output the analyzed fair handicap value

### 2.2 Line Movement Tracking (盘口走势分析)
- Record early odds ("早" = opening line) and instant odds ("即" = current line)
- Analyze changes: "早" → "即" direction (upgraded/downgraded/no change)
- **Example**: If early line was 平手(0) and instant line is 半球/一球(-0.75), record as "升盘"
- If the giving team is away team, then the Asian Handicap(受讓) has a "-" symbol
- Determine the true purpose behind odds movements:
  - Upgraded line (升盘): typically indicates stronger team being favored
  - Downgraded line (降盘): typically indicates weaker team being favored
  - Water adjustment: odds movement without line change

### 2.3 Bookmaker Intent Analysis
- Analyze the real intention behind bookmaker adjustments
- Look for patterns in how lines have moved from opening ("早") to current ("即")

### 2.4 Betting Volume Analysis
- Use odds data to analyze betting volume changes
- Capture abnormal movements (sharp money, public money divergence)

### 2.5 European-to-Asian Odds Conversion
- Convert European odds to Asian handicap and odds
- Check if Asian handicap matches the converted values
- Identify potential trap lines (诱盘) where there's a mismatch

---

## Step 3: Odds Probability Calculation

**CRITICAL**: Use INSTANT odds ("即") for final calculation - this represents the final odds before match kickoff.

### Asian Handicap Probability
Calculate from latest (instant) Asian handicap data ("即" row):

```
1. Home win implied probability:    P(home) = 1 / (1 + home_odds)
2. Away win implied probability:    P(away) = 1 / (1 + away_odds)
3. Total implied probability:       P(total) = P(home) + P(away)
4. Home true implied probability:   P(true_home) = P(home) / P(total)
5. Away true implied probability:   P(true_away) = P(away) / P(total)
6. Margin (juice):                 P(margin) = 1 - 1 / P(total)
```

### Over/Under Probability
Same calculation method applied to instant over/under odds ("即" row):

```
1. Over implied probability:        P(over) = 1 / (1 + over_odds)
2. Under implied probability:       P(under) = 1 / (1 + under_odds)
3. Total implied probability:       P(total) = P(over) + P(under)
4. Over true implied probability:  P(true_over) = P(over) / P(total)
5. Under true implied probability: P(true_under) = P(under) / P(total)
6. Margin (juice):                 P(margin) = 1 - 1 / P(total)
```

---

## Step 4: Model Prediction

### Initial Weight Allocation (Based on AI Probability Assessment)

**Weight principles**: Allocate based on initial AI probabilistic judgment, then auto-optimize through post-match review iterations.

Default weights (initial):
| Feature | Asian Handicap | Over/Under |
|---------|:-------------:|:----------:|
| Odds implied probability | 0.35 | 0.15 |
| Fundamental analysis | 0.20 | 0.10 |
| Team fundamentals | 0.20 | 0.10 |
| Squad power decay | 0.20 | 0.05 | <!-- v1.1: up from 0.15 -->
| Motivation | 0.10 | 0.05 |
| Enhanced data (half-goals/corners) | - | 0.15 |
| Environment factor | - | 0.10 |
| League factor | - | 0.10 |
| **Defense injury coefficient** | - | **0.15** | <!-- v1.1: new -->
| Other | - | 0.05 |

**Note**: Weights will be auto-adjusted through post-match review and learning (see review-framework.md).

### 4.1 Asian Handicap Logistic Regression Model

Perform deep analysis using logistic regression. Quantify input features, standardize, and output comprehensive prediction probability.

**Analysis weight priority** (descending):
```
Odds data > Fundamental analysis > Real-time lineup > Motivation
(Bookmaker info > Short-term disruption > Long-term trends > Subjective factors)
```

**Input features**:
| Feature | Description |
|---------|-------------|
| Team fundamentals | Recent win rate, home/away differential |
| Squad power decay coefficient | Calculated from injury/suspension list |
| Motivation label | 0-1 standardized |
| Fundamental analysis | Results from Step 2 |
| Odds implied probability | **Core feature** from Step 3 |

### 4.2 Over/Under Logistic Regression Model (Enhanced)

Deep analysis of over/under handicap using logistic regression with enhanced features.

**Key comparison**: If opened line > analyzed line -> high open; If opened line < analyzed line -> shallow open.

**Input features** (for both home and away teams):
| Feature | Weight | Description |
|---------|:------:|-------------|
| xG and xGA | 0.12 | Expected goals and expected goals against |
| League factor | 0.10 | League-specific scoring patterns (MLS~55% over, etc.) |
| Recent win rate | 0.05 | Last N matches |
| Recent 5-match goals | 0.07 | Goals in last 5 games (reduced from 0.10 — low recent goals ≠ low match goals under injury conditions) |
| H2H history | 0.05 | Head-to-head goal patterns |
| Home/away differential | 0.10 | Home vs away scoring difference |
| Squad power decay coefficient | 0.05 | From injury/suspension list (attacking side only) |
| **Defense injury coefficient** | **0.15** | **🆕 KEY RULE: GK absence → +0.75~1 goal adj; CB absence → +0.5; DM absence → +0.25** |
| Motivation label | 0.05 | 0-1 standardized |
| Environment factor | 0.10 | Weather, venue altitude, rest days |
| Half-time goals pattern | 0.08 | Half-time scoring behavior (high-scoring half vs low) |
| Corner kicks | 0.08 | Corner kick data (indicates attacking intensity) |
| Fundamental analysis | 0.10 | Results from Step 2 |
| Odds implied probability | 0.15 | **Core feature** from Step 3 |

**🆕 Defense Injury Rule (v1.1)**:
When a team is missing key defensive players, the over/under model MUST adjust upward:
- **GK absent** (致命级): +0.75 to +1.0 goal adjustment toward OVER. This is the single most impactful injury type for goals.
- **CB absent** (严重级): +0.5 goal adjustment
- **DM absent** (中等级): +0.25 goal adjustment
- **FB absent** (轻微级): +0.1 goal adjustment
- Stacking: multiple positions missing → adjustments stack (e.g., GK + DM = +1.0 to +1.25)
- **Critical correction**: Defense injuries do NOT mean "both teams score less → under". The correct interpretation is "conceding team leaks more goals → toward OVER". Attacking injuries only affect that team's scoring, they do NOT cancel out opponent's defensive collapse.

**Output**: Predicted home goals, away goals, and total goals.

---

## Step 5: Win Probability & Betting Advice

### Win Probability Prediction
Combine odds analysis and model analysis to predict:
- Asian Handicap: P(home_win) and P(away_win)
- Over/Under: P(over_win) and P(under_win)

### Expected Value (EV) Calculation

```
Asian Handicap Home EV = P(home_win) * home_odds - P(away_win)
Asian Handicap Away EV = P(away_win) * away_odds - P(home_win)
Over EV               = P(over_win) * over_odds - P(under_win)
Under EV              = P(under_win) * under_odds - P(over_win)
```

### Final Output
1. Best betting recommendation based on highest positive EV
2. Predicted final score
3. Confidence level for each recommendation

---

## Step 6: 存档（MANDATORY）

**每次预测完成后必须执行，不可跳过。**

将以下信息追加到 `~/.hermes/workspace/memory/football-match-history.md`：

```markdown
## YYYY-MM-DD [主队] vs [客队]
- **比赛ID**: [ID]
- **联赛**: [联赛名称]
- **时间**: YYYY-MM-DD HH:MM
- **结果**: 待确认
- **预测**: [盘口推荐及星级] + [大小球推荐及星级]
- **比分预测**: [预测比分]
- **复盘状态**: 待确认结果后复盘
```

同时简要记录赛前关键数据（伤停、盘口走势、核心判断依据），以便复盘时对照。

**不存档 = 工作流未完成。**
