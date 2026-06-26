# Data Sources Reference

## TheSportsDB (Free)
- **URL:** https://www.thesportsdb.com/
- **Cost:** Free, no API key required
- **Data:** Fixtures, results, teams, leagues, H2H
- **Rate Limit:** Reasonable (be nice)
- **Endpoints used:**
  - `/searchteams.php` — Find team by name
  - `/eventsnext.php` — Upcoming fixtures
  - `/eventslast.php` — Past results
  - `/searchevents.php` — H2H history

## API-Football (Free tier)
- **URL:** https://www.api-football.com/
- **Cost:** 100 calls/day free
- **Data:** Lineups, injuries, xG, player stats, live scores
- **Rate Limit:** 100/day free, paid plans available
- **Signup:** https://www.api-football.com/pricing
- **Key storage:** `~/.config/api-football/config.json`

## Open-Meteo (Free)
- **URL:** https://open-meteo.com/
- **Cost:** Free, no API key
- **Data:** Weather forecasts (rain, wind, temp)
- **Rate Limit:** None (be reasonable)
- **Used for:** Match day weather conditions

## The Odds API (Free tier)
- **URL:** https://the-odds-api.com/
- **Cost:** 500 calls/month free
- **Data:** Current odds from major bookmakers
- **Rate Limit:** 500/month free
- **Key storage:** `~/.config/the-odds-api/key`

## Call Budget Example

Researching "Liverpool vs Everton":
- Search team (Liverpool): 1 call (TheSportsDB - free)
- Get fixtures: 1 call (TheSportsDB - free)
- Get recent form: 1 call (TheSportsDB - free)
- Get H2H: 1 call (TheSportsDB - free)
- Get weather: 1 call (Open-Meteo - free)
- Get odds: 1 call (Odds API - counts toward 500/mo)
- Get lineups: 1 call (API-Football - counts toward 100/day)

**Total: 7 calls, 2 count toward limits**

## Fallbacks

If API-Football hits limit:
- Still get form, fixtures, H2H from TheSportsDB
- Still get weather from Open-Meteo
- Still get odds from Odds API
- Missing: lineups, injuries, xG

If Odds API hits limit:
- Use cached odds from earlier in day
- Focus on form/historical analysis
