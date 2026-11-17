# US market calendar (NYSE / Nasdaq)

## Regular session

| Segment | Eastern time | UTC (EDT) | UTC (EST) |
| --- | --- | --- | --- |
| Pre-market | 4:00 AM - 9:30 AM | 08:00 - 13:30 | 09:00 - 14:30 |
| Regular | 9:30 AM - 4:00 PM | 13:30 - 20:00 | 14:30 - 21:00 |
| After-hours | 4:00 PM - 8:00 PM | 20:00 - 24:00 | 21:00 - 01:00 (+1d) |
| Options close (standard) | 4:00 PM | 20:00 | 21:00 |

US daylight saving time runs from the second Sunday in March to the first
Sunday in November. Always compute with `America/New_York`, never a fixed
offset.

## Settlement

- **T+1** for US equities since May 28, 2024.
- Cash account good faith violations can still occur - flag settlement risk in
  plans that assume immediate reinvestment.

## 2026 market holidays (NYSE / Nasdaq)

| Date | Holiday | Notes |
| --- | --- | --- |
| Jan 1 (Thu) | New Year's Day | Full close |
| Jan 9 (Fri) | National Day of Mourning | One-off closure for President Carter - verify with NYSE before trading |
| Jan 19 (Mon) | Martin Luther King Jr. Day | Full close |
| Feb 16 (Mon) | Washington's Birthday | Full close |
| Apr 3 (Fri) | Good Friday | Full close |
| May 25 (Mon) | Memorial Day | Full close |
| Jun 19 (Fri) | Juneteenth | Full close |
| Jul 3 (Fri) | Independence Day (observed) | July 4 falls on Saturday - market closed Friday Jul 3 |
| Sep 7 (Mon) | Labor Day | Full close |
| Nov 26 (Thu) | Thanksgiving | Full close |
| Dec 25 (Fri) | Christmas Day | Full close |

## Early closes (1:00 PM ET)

| Date | Reason |
| --- | --- |
| Jul 2, 2026 (Thu) | Day before Independence Day observed |
| Nov 27, 2026 (Fri) | Day after Thanksgiving |
| Dec 24, 2026 (Thu) | Christmas Eve |

**Verify against the official NYSE calendar before relying on it:**
<https://www.nyse.com/markets/hours-calendars>

## How to check "is the market open right now"

```python
from datetime import datetime
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
now = datetime.now(ET)
# then check: is it a weekday, is it 9:30-16:00, and is today not a holiday
```

Never state "the market is open" from memory - check the clock and the holiday
list, then say which of the three states you are in: pre-market, open, closed.

## Time-relative language for US users

Use ET and name the zone: "as of 3:42 PM ET", "the 4:00 PM ET close", "the
9:30 AM ET open". Add the calendar date every time, because ET shifts relative
to a user's local clock.

## Other US market dates worth knowing

- **Index rebalances**: quarterly S&P 500 rebalance effective after the close on
  the third Friday of March, June, September, December.
- **Triple witching**: third Friday of March, June, September, December -
  large volume and volatility.
- **FOMC meetings**: eight scheduled meetings a year, statement at 2:00 PM ET,
  press conference 2:30 PM ET. Always check the current schedule.
- **Monthly options expiry**: third Friday - verify, US equity options expiry
  moved to Thursday after a holiday in recent years.
