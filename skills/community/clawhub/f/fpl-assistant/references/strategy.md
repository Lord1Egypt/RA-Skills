# FPL Player Selection Strategy

## Analysis Framework

Do NOT rely on a single metric. Layer multiple factors for robust decisions.

### Factor 1: Fixture Context (Beyond FDR)

FDR is a season-long aggregate. Supplement with:

- **Recent form (last 5-6 GWs)**: Is the team on a hot streak or in freefall? A "FDR 2" fixture means nothing if the opponent just hit form.
- **Home/away split**: Some teams have dramatically different records. Check if the fixture is home or away for YOUR player.
- **Clean sheet trends**: DEF/GKP value depends heavily on the opponent's scoring form, not just the team's overall strength.
- **Expected goals (xG)**: Teams generating high xG but underperforming are due for regression (positive). Teams overperforming xG are likely to regress.

### Factor 2: Motivation & League Context

- **Title race / Top 4 / Top 6**: Teams fighting for European spots are more motivated and likely to field full-strength sides.
- **Relegation battle**: Bottom-3 teams fighting for survival can be dangerous opponents (no easy games) BUT also more likely to concede pushing forward.
- **Mid-table with nothing to play for**: Lower intensity, more rotation risk, less reliable output.
- **Dead rubber at season end**: High rotation risk for established teams.

### Factor 3: Fixture Congestion

- **Midweek European matches**: UCL/UEL midweek → likely rotation for weekend PL match. Check if the player's team played midweek.
- **FA Cup / League Cup**: Extra matches = fatigue + rotation risk.
- **Travel**: European away trips (Eastern Europe, long flights) increase fatigue more than home European matches.
- **Key rule**: Premium players (Haaland, Salah tier) rarely rotated. Mid-tier players (6-9m) are at highest rotation risk during congestion.

### Factor 4: Head-to-Head & Style Matchups

- Some teams consistently struggle against specific opponents regardless of overall strength
- Defensive teams vs attacking teams: matters for CS probability
- Set-piece reliant teams vs teams weak at defending set pieces

### Factor 5: Player-Specific Factors

- **Minutes security**: Will the player start AND play 60+? Check recent starts, manager comments, injury news.
- **Set-piece duty**: Penalty takers, corner takers, free-kick takers have higher ceilings.
- **Underlying stats vs returns**: A player creating lots of chances but not converting is "due." A player overperforming xG may regress.
- **Price trajectory**: Rising in price = high demand, likely good pick. Falling = consider if it's a short-term blip or a real decline.

## Positional Strategy

### Goalkeepers (GKP)

- Value position: don't overspend (4.5-5.5m range is optimal)
- Prioritize: CS potential > save points > bonus points
- Consider a rotating pair (two 4.5m keepers with alternating good fixtures)
- Set-and-forget premium (5.5m+) only if truly elite (e.g., Alisson, Raya)

### Defenders (DEF)

- Full-backs with attacking returns > center-backs (higher ceiling)
- Look for: nailed starters + set-piece involvement + CS potential
- 4.0-4.5m bench fodder is fine for 4th/5th defender
- Best value range: 4.5-5.5m

### Midfielders (MID)

- Widest price range, most points potential
- Premium (10m+): captain candidates, fixture-proof
- Mid-range (7-10m): best value zone, strong starters
- Budget (5-7m): enablers, look for form + fixture combo
- Penalty takers in MID are gold (goals = 5 pts each)

### Forwards (FWD)

- Fewer elite options vs MID, but premium FWDs are essential
- Haaland-tier: always own, captain in good fixtures
- Mid-range (7-9m): look for nailed starters with good fixtures
- Budget (5-7m): rotation risk, only if genuinely starting

## Transfer Decision Tree

```
Need a transfer?
├── Do I have an injured/suspended player? → YES → Transfer (mandatory)
├── Do I have a player with FDR 5 + bad form? → YES → Strong candidate
├── Can I roll the transfer (max 2 banked)? → YES → Consider rolling
│   ├── No clear upgrade available → Roll
│   └── Clear upgrade available → Make the move
└── Is it worth a -4 hit?
    ├── Expected gain over next 3+ GWs > 4 pts? → Maybe
    └── Only expecting gain this GW? → Probably not
```

## Captain Selection Matrix

| Factor | Weight |
|--------|--------|
| Fixture (FDR ≤ 2 preferred) | High |
| Form (recent returns) | High |
| Home/away | Medium |
| Set-piece duty (pens, FKs) | Medium |
| Minutes security | Medium |
| Ownership (protection vs differential) | Low-Medium |

**Default approach**: Captain the player with the best fixture AND form combination. When in doubt, captain the most-owned premium option (safety in numbers for rank protection).

## Chip Timing

### Wildcard
- Best windows: GW3-5 (early season adjustments), GW20-22 (second half setup)
- Use when: squad needs 5+ changes, or a major fixture swing is coming

### Free Hit
- Best for: Blank Gameweeks (BGW) where many teams don't play
- Strategy: Build a squad of 11 players who ALL play that week
- Don't waste on normal GWs

### Bench Boost
- Best for: Double Gameweeks (DGW) where teams play twice
- Prep: Ensure bench players have 2 fixtures that week
- Can combine with Wildcard the week BEFORE to set up

### Triple Captain
- Best for: DGW with premium captain having 2 good fixtures
- Alternative: Single GW with an elite fixture (FDR 1, home)
- Don't use on a single GW unless the fixture is truly exceptional

## Season Arc

- **GW1-8**: Be patient, don't kneejerk. Early form can be misleading.
- **GW9-19**: First Wildcard window. Solidify squad structure.
- **GW20-25**: Second half Wildcard. Plan for DGW/BGW.
- **GW26-30**: Chip planning begins. Save transfers for DGW setups.
- **GW31-38**: Execute chips. End-of-season rotation increases. Target teams still motivated.
