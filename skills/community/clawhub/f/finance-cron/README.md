# finance-calendar-skill

A CodeBuddy skill providing trading-day calendar utilities for financial markets. Supports US, China A-share, and Hong Kong markets with automatic holiday detection.

## Important Note

This skill provides **trading day identification and calendar utilities**. It helps you:
- Check if a date is a trading day
- Show upcoming trading days
- Sync latest holiday calendar data
- Plan when to schedule tasks

**This skill does NOT execute scheduled tasks by itself.** For actual task execution, combine with `/loop` or other scheduling mechanisms.

## Features

- **Trading Day Detection**: Check if any date is a valid trading day
- **Multi-Market Support**: US (NYSE/NASDAQ), CN (SSE/SZSE), HK (HKEX)
- **Automatic Calendar Sync**: Sync latest holiday data from data sources
- **A-Share Special Handling**: Supports Chinese 调休 (workdays on weekends)
- **Task Planning**: Calculate optimal run times for trading-day-aware tasks

## Installation

```bash
cd finance-cron-skill
npm install
npm run build
```

## Commands

### Check Trading Day
```
/finance-cron check <market> [date]
```

Example:
```
/finance-cron check US           # Check today
/finance-cron check CN 2024-12-25  # Check specific date
```

### Show Next Trading Days
```
/finance-cron next <market> [n]
```

Example:
```
/finance-cron next US 5  # Show next 5 US trading days
```

### Sync Calendar
```
/finance-cron sync [market]
```

Example:
```
/finance-cron sync    # Sync all markets
/finance-cron sync US  # Sync US market only
```

### Plan Task Schedule
```
/finance-cron add <market> <time> <command>
```

Plans a trading-day-aware task and shows when it should run next. Use with `/loop` for actual scheduling.

Example:
```
/finance-cron add US 09:30 echo "US market opening"
# Output includes suggested /loop command for actual execution
```

### List Planned Tasks
```
/finance-cron list
```

## Integration with /loop

For actual scheduled execution, use `/loop`:

```bash
# Run command only on US trading days at 9:30 AM
/loop 30 9 * * 1-5 /finance-cron check US && your_command
```

## Markets

| Code | Name | Exchanges | Timezone | Hours |
|------|------|-----------|----------|-------|
| US | US Stock Market | NYSE, NASDAQ | America/New_York | 09:30-16:00 |
| CN | China A-Share | SSE, SZSE | Asia/Shanghai | 09:30-15:00 |
| HK | Hong Kong | HKEX | Asia/Hong_Kong | 09:30-16:00 |

## API Usage

```typescript
import { isTradingDay, getNextTradingDay, executeCommand } from 'finance-cron-skill';

// Check if today is a trading day
const isUS = isTradingDay('US');

// Get next trading day
const nextDay = getNextTradingDay('CN');

// Execute command
const result = await executeCommand({
  action: 'check',
  market: 'HK',
  date: '2024-12-25'
});
```

## Python Dependencies (for calendar sync)

Install Python dependencies for automatic calendar sync:

```bash
pip install pandas-market-calendars exchange-calendars chinese-calendar
```

## Data Sources

- **US/HK**: pandas_market_calendars (NYSE, HKEX)
- **CN**: chinese_calendar (with 调休 support)

## Data Files

- `data/us-holidays.json` - US market holidays
- `data/cn-holidays.json` - China A-share holidays with workdays
- `data/hk-holidays.json` - Hong Kong market holidays

## License

MIT
