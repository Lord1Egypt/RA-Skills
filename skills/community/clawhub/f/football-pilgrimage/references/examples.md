# Examples

## Example 1: Basic pilgrimage with stories

User: "Generate a Liverpool football pilgrimage guide"

1. `curl "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/teams/364" | cat` → team name="Liverpool", crest from `logos[0].href`, stadium="Anfield" from `venue.fullName`
2. (team_id=364 is known from Common Team IDs table, or found by searching `eng.1/teams` list)
3. Web search: "Anfield history story legends", "Anfield stadium tour", "Liverpool football museum history", "Liverpool fan pubs Anfield culture"
4. For each spot found, search for its backstory: "The Kop Anfield history why famous", "Shankly Gates story"
5. Generate guide with 5-phase emotional narrative, **each spot with its story**

## Example 2: With travel planning + On This Day + Match Detection

User: "Generate a Real Madrid pilgrimage guide, departing from Shanghai, April 15, 4 days"

1. `curl "https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/teams/86" | cat` → team name="Real Madrid", stadium="Santiago Bernabéu", crest from `logos[0].href`
2. `curl "https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/teams/86/schedule?fixture=true" | cat` → filter `events[]` for April 15-18
   → Found: April 17, Real Madrid vs Atletico Madrid (Home, La Liga, 21:00)
   → 🔥 "Lucky you! On April 17, Real Madrid will face Atletico Madrid at the Bernabéu! It's the Madrid Derby!"
4. Web search On This Day for **every day**: "Real Madrid on this day April 15", "Real Madrid on this day April 16", "Real Madrid on this day April 17", "Real Madrid on this day April 18" → one event per day
6. `flyai search-flight --origin "Shanghai" --destination "Madrid" --dep-date "2026-04-15"`
7. `flyai search-hotels --city "Madrid" --check-in "2026-04-15" --nights 4`
8. Generate guide: adjust Phase 3 to April 17 (match day), Phase 2 stadium tour on April 16

## Example 3: On This Day only

User: "What happened in Liverpool's history on April 1?"

1. Web search: "Liverpool FC on this day April 1 history", "Liverpool FC April 1 famous moments"
2. Return ranked list of historic events on/near April 1st
