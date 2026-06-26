# Finance Calendar

Trading-day calendar utilities for financial markets (US, CN, HK).

## Overview

This skill provides trading-day-aware scheduling helpers. It helps you:
- Check if a date is a trading day
- Show upcoming trading days
- Sync latest holiday calendar data
- Plan when to schedule tasks (trading-day-aware)

**Important**: This skill identifies trading days and calculates optimal run times, but does NOT execute scheduled tasks. Use with `/loop` for actual task scheduling.

## Commands

### Check Trading Day
```
/finance-cron check <market> [date]
```
Check if a date is a trading day for a market.

Example:
```
/finance-cron check US           # Check today
/finance-cron check CN 2024-12-25  # Check specific date
```

### Show Next Trading Days
```
/finance-cron next <market> [n]
```
Show next N trading days for a market.

Example:
```
/finance-cron next US 5  # Show next 5 US trading days
```

### Sync Calendar
```
/finance-cron sync [market]
```
Sync latest trading calendar from data sources.

Example:
```
/finance-cron sync    # Sync all markets
/finance-cron sync US  # Sync US market only
```

### Plan Task Schedule
```
/finance-cron add <market> <time> <command>
```
Plan a trading-day-aware task and get the next execution time.

**Note**: This command calculates and displays when the task should run, but does NOT execute it. To actually run tasks on schedule, combine with `/loop`:

Example workflow:
```
# First, plan the task
/finance-cron add US 09:30 echo "US market opening"
# Output: Next Run: 2024-01-15 (Mon) 09:30

# Then, use /loop for actual scheduling
/loop 0 9 * * 1-5 /finance-cron check US && echo "US market opening"
```

### List Planned Tasks
```
/finance-cron list
```
List all planned tasks with their next scheduled times.

## Markets

| Code | Name | Exchanges | Timezone | Hours |
|------|------|-----------|----------|-------|
| US | US Stock Market | NYSE, NASDAQ | America/New_York | 09:30-16:00 |
| CN | China A-Share | SSE, SZSE | Asia/Shanghai | 09:30-15:00 |
| HK | Hong Kong | HKEX | Asia/Hong_Kong | 09:30-16:00 |

## Integration with /loop

For actual scheduled execution, use `/loop` with trading day checks:

```bash
# Run command only on US trading days at 9:30 AM
/loop 30 9 * * 1-5 /finance-cron check US --quiet && your_command

# The --quiet flag (if implemented) would suppress output for clean scheduling
```

## API for Other Skills

This skill also exports programmatic APIs:

```typescript
import { isTradingDay, getNextTradingDay, getDueTasks } from 'finance-cron';

// Check if today is a US trading day
const canTrade = isTradingDay('US');

// Get next US trading day
const nextDay = getNextTradingDay('US');

// Get tasks due for execution (for external schedulers)
const dueTasks = getDueTasks();
```
