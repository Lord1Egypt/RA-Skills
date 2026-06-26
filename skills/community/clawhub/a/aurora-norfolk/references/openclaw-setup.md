# OpenClaw setup notes

Use this skill in a dedicated aurora agent.

## Recommended agent characteristics

- Use a low-temperature model configuration.
- Keep the tool set narrow.
- Allow web search or HTTP fetch capability for public data sources.
- Keep persistent state so the agent can compare the latest result with the prior result and decide whether a change alert is worth sending.

## Suggested tools

Prefer:
- web_search
- http_request
- calculator
- file_read
- file_write

Only add browser automation if the data source cannot be fetched reliably by normal web or HTTP tools.

## Suggested recurring schedule

Use cron or the gateway scheduler with three layers:

1. **Daily planning run**
   - Once per morning around 08:30 Europe/London
   - Produce the 3-night outlook

2. **Alert-day briefing**
   - Only on nights currently marked alert_day or high_alert
   - Run a planning brief at about 17:30 Europe/London

3. **Live-night mode**
   - Only on alert_day or high_alert nights
   - Check every 15 minutes from about 20:00 to 01:00 Europe/London
   - Send a message only if a material change occurred or a useful viewing window is opening

## Suggested state file

Store a small JSON record with:
- last 3-night outlook
- current action
- last communicated best window
- last communicated coast chance
- last communicated dereham chance
- last notified status per night
- timestamps for previous sends

Use this state to suppress noisy repeats.

## Example operating pattern

- Morning run computes the 3-night table.
- If no night reaches alert_day, stop there.
- If tonight reaches alert_day or high_alert, schedule or enable evening and live-night checks.
- If later checks downgrade tonight materially, issue one downgrade message.
