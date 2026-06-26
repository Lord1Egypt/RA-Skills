# Troubleshooting

## `ModuleNotFoundError: requests`

Run:

```bash
python3 -m pip install -r requirements.txt
```

## Binance or CoinGecko request failures

- Check your network
- Re-run later in case of rate limits or transient 5xx responses
- Reduce scheduler frequency if you are polling too aggressively

## Discord delivery fails

- Confirm `"discord.enabled": true`
- Confirm `DISCORD_TOKEN` is exported in the environment used by the process
- Confirm the bot has permission to post in the configured channel
- Confirm `channel_id` is correct

## Cron job does not run

- Run `crontab -l` and verify the installed entry
- Check `logs/monitor.log`
- Make sure the machine timezone matches your expected schedule
