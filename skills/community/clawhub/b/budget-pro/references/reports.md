# Reports & Analysis

## Purpose
Generate comprehensive spending reports and financial insights.

## Report Types

### 1. Quick Status Check
```bash
python scripts/budget_status.py
```
One-line summary of overall budget health.

### 2. Category Deep Dive
```bash
python scripts/category_status.py --category food
```
Detailed analysis of specific category.

### 3. Weekly Report
```bash
python scripts/generate_report.py --type weekly
```
Spending patterns over past 7 days.

### 4. Monthly Report
```bash
python scripts/generate_report.py --type monthly
```
Complete month analysis with trends.

### 5. Custom Date Range
```bash
python scripts/generate_report.py \
  --start "2024-01-01" \
  --end "2024-03-31" \
  --type quarterly
```

## Output Formats

### Quick Status
```
💰 BUDGET STATUS - March 2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall: 78% of budget used ($3,900/$5,000)
Status: ✅ ON TRACK

AT RISK:
  ⚠️  Food: $420/$500 (84%)
  ⚠️  Entertainment: $170/$200 (85%)

OVERRUN:
  🚨 Shopping: $275/$250 (110%)

UNDERSPENT (reallocate opportunities):
  ✅ Transport: $90/$200 (45%)
  ✅ Utilities: $75/$250 (30%)

Days remaining: 12
Daily budget remaining: $75/day
```

### Weekly Report
```
WEEKLY SPENDING REPORT
February 25 - March 2, 2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Spent: $680
Budget Pace: Normal (on track for $2,720 month)

SPENDING BY CATEGORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Food          $240  ████████████████████  35%
Housing       $200  ████████████████      29%
Transport      $85  ███████                13%
Entertainment $100  ████████               15%
Shopping       $55  ████                    8%

DAILY BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sun: $45   (Groceries)
Mon: $120  (Rent prorated, gas)
Tue: $85   (Dinner out, coffee)
Wed: $50   (Lunch, supplies)
Thu: $200  (Concert tickets)
Fri: $120  (Groceries, drinks)
Sat: $60   (Brunch, shopping)

TOP 5 EXPENSES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. $120  Concert tickets (Entertainment)
2. $100  Weekly groceries (Food)
3. $85   Gas fill-up (Transport)
4. $65   Dinner out (Food)
5. $45   Coffee shop (Food)

INSIGHTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Food spending concentrated on dining out ($150)
   vs groceries ($90). Meal prep could save $30-40/week.

💡 Weekend spending ($260) 2x weekday average ($130)
   Consider weekend-specific budget.

💡 Entertainment spike due to concert season
   One-time expense, not concerning.

VS LAST WEEK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Spending: $680 vs $620 (+10%)
Primary difference: Concert tickets (+$120)
Without one-time: Would be 8% under last week
```

### Monthly Report
```
MONTHLY BUDGET REPORT
March 2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTIVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Income:     $5,000
Total Budgeted:   $5,000
Total Spent:      $4,200
Total Saved:        $800 (16%)

Budget Performance: ✅ EXCEEDED GOAL
Target savings: 15% | Actual: 16%

CATEGORY BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CATEGORY        BUDGET   SPENT    REMAIN   %
Housing         $1,500   $1,500   $0      100% ✅
Food              $500     $520   -$20    104% ⚠️
Transport         $200     $150    $50     75% ✅
Utilities         $250     $220    $30     88% ✅
Entertainment     $200     $245   -$45    123% 🚨
Health            $100      $80    $20     80% ✅
Shopping          $250     $325   -$75    130% 🚨
Savings           $750     $800    $50    107% ✅
Debt              $250     $250    $0     100% ✅
Gifts/Charity     $100      $110   -$10    110% ⚠️

MERCHANT ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Top 5 Merchants:
1. Costco        $340  (Food, Household)
2. Amazon        $285  (Shopping, various)
3. Whole Foods   $225  (Food)
4. Shell         $150  (Transport)
5. Netflix       $15   (Entertainment)

SPENDING PATTERNS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
By Week:
Week 1: $1,100
Week 2: $1,050
Week 3: $1,200 (concert week)
Week 4: $850

By Day of Week:
Monday:    $180 avg (groceries, gas)
Tuesday:   $120 avg
Wednesday: $140 avg
Thursday:  $160 avg
Friday:    $200 avg (dining out)
Saturday:  $250 avg (shopping, events)
Sunday:    $150 avg

RECURRING EXPENSES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Rent:        $1,200 (on time)
✅ Utilities:     $220 (avg of $215)
✅ Insurance:      $80 (auto-deducted)
✅ Subscriptions:  $45 (Netflix, Spotify, Gym)

ANOMALIES & ONE-TIMES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎵 Concert tickets:       $120 (Entertainment)
💻 New laptop accessories: $85 (Shopping)
🎁 Birthday gift:          $65 (Gifts)

Without one-time expenses:
Total would be: $3,930 (78% of budget)

TRENDS VS PREVIOUS MONTHS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          Feb    Jan    Dec    Trend
Food      $520   $480   $510   ↑ 8%
Transport $150   $180   $165   ↓ 17%
Entertain $245   $150   $200   ↑ 63%
Shopping  $325   $200   $280   ↑ 63%

YEAR-TO-DATE PROGRESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Income:     $15,000
Spent:      $12,300
Saved:       $2,700 (18%)

Goal: 15% savings rate
Actual: 18% ✅ Ahead of target

RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Entertainment trending up 63% - set stricter
   weekend dining budget or find free activities.

2. Shopping spike due to laptop accessories - 
   one-time, should normalize next month.

3. Food up 8% - review dining out frequency.
   Current: 12x/month. Try reducing to 8x.

4. Transport down 17% - good job using transit!
   Reallocate $30 to savings.

NEXT MONTH PREVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Expected changes:
• Car insurance due: +$150 (quarterly)
• No concert expenses expected
• Birthday season over

Suggested adjustments:
• Reduce Entertainment to $150
• Keep Shopping at $200 (normalizing)
• Increase Savings to $800 (maintain 16%)
```

## Export Options

### CSV Export
```bash
python scripts/export_data.py \
  --type expenses \
  --format csv \
  --month current \
  --output "march_expenses.csv"
```

### JSON Export
```bash
python scripts/export_data.py \
  --type full \
  --format json \
  --output "budget_backup_2024.json"
```

## Data Visualization

### ASCII Charts
```
SPENDING TREND (Last 6 Months)
$600 │                                    ╭──╯
$500 │                    ╭───╮          │
$400 │        ╭───╮      │   │    ╭────╮│
$300 │╭──╮   │   │ ╭────╯   ╰────╯    ╰╯
$200 ││  │╭──╯   ╰─╯
$100 ││  ╰╯
   0 ╰┴──┴───┴───┴───┴───
    Oct Nov Dec Jan Feb Mar
```

### Category Comparison
```
BUDGET VS ACTUAL - March 2024

Housing      │████████████████████████████│ 100% ✅
Food         │███████████████████████████████│ 104% ⚠️
Transport    │███████████████████│ 75% ✅
Utilities    │███████████████████████│ 88% ✅
Entertainment│███████████████████████████████████│ 123% 🚨
Health       │████████████████████│ 80% ✅
Shopping     │███████████████████████████████████████│ 130% 🚨
Savings      │███████████████████████████████│ 107% ✅

Budget  │████████████████████████████│
Actual  │█████████████████████████████████│
```
