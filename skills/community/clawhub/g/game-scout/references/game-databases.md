# Game Database Directory

Known interactive databases, wikis, and tools per game. Consult this when a query involves specific game data, item stats, or build planners.

For each entry: URL, what data it provides, and whether standard scraping works or if the site requires JS interaction.

---

## Table of Contents
1. [FPS / Tactical Shooters](#fps--tactical-shooters)
2. [Battle Royale](#battle-royale)
3. [Souls-likes / Action RPG](#souls-likes--action-rpg)
4. [MOBAs](#mobas)
5. [Looter Shooters](#looter-shooters)
6. [ARPGs / Loot Games](#arpgs--loot-games)
7. [Card / Roguelite](#card--roguelite)
8. [Live Service / MMO](#live-service--mmo)
9. [Navigation Tips](#navigation-tips)

---

## FPS / Tactical Shooters

### Marathon
- **Community hubs**: Emerging — check r/Marathon, r/MarathonTheGame
- **Wiki**: TBD (game is new — community resources are still forming)
- **Strategy**: Rely heavily on YouTube guides and Reddit for now
- **Scrape method**: Standard scrape for Reddit/forums

### Valorant
- **tracker.gg/valorant** — Agent stats, weapon stats, map analytics, player profiles
  - Scrape: Works with standard scrape for most pages
  - JS-heavy: Try bright-scrape for filtered stat views and comparison tools
- **blitz.gg/valorant** — Live game overlay data, tier lists
  - Scrape: Standard scrape works
- **liquipedia.net/valorant** — Esports data, tournament results, team rosters
  - Scrape: Clean static content, standard scrape

### CS2
- **csstats.gg** — Player stats, weapon economy, map stats
  - Scrape: Standard scrape for most data
- **liquipedia.net/counterstrike** — Esports, tournament brackets, team info
  - Scrape: Standard scrape

### Overwatch 2
- **overbuff.com** — Hero stats, win rates, pick rates by rank
  - Scrape: Standard scrape, some JS rendering
  - JS-heavy: Try bright-scrape for rank-filtered views
- **overwatch.blizzard.com/heroes** — Official hero pages with abilities
  - Scrape: Standard scrape

### Apex Legends
- **apexlegendsstatus.com** — Player stats, legend stats, map rotation
  - Scrape: Standard scrape
- **apexlegends.wiki.gg** — Comprehensive wiki
  - Scrape: Standard scrape

---

## Battle Royale

### Warzone / Call of Duty
- **sym.gg** — Detailed weapon stats, TTK data, damage profiles, recoil patterns
  - Scrape: Some data loads dynamically
  - JS-heavy: Try bright-scrape for weapon comparison tools
- **wzstats.gg** — Loadout popularity, meta weapons
  - Scrape: Standard scrape
- **cod.tracker.gg** — Player stats, weapon usage stats
  - Scrape: Standard scrape for overview pages

### Fortnite
- **fortnite.gg** — Item shop, map, weapons, upcoming content
  - Scrape: Standard scrape
- **fortnitetracker.com** — Player stats, weapon stats, leaderboards
  - Scrape: Standard scrape

---

## Souls-likes / Action RPG

### Elden Ring
- **eldenring.wiki.fextralife.com** — Comprehensive wiki: weapons, armor, spells, builds, bosses
  - Scrape: Standard scrape — clean stat tables
  - Key pages: `/Weapons`, `/Builds`, `/[Specific Item Name]`
- **mugenmonkey.com** — Build planner / character calculator
  - JS-heavy: Interactive tool — try bright-scrape, may return partial stat allocation tool
- **eldenring.fandom.com** — Alternative wiki
  - Scrape: Standard scrape (more ads than Fextralife)

### Monster Hunter (Wilds / Rise / World)
- **mhworld.kiranico.com** — Item/monster database
  - Scrape: Standard scrape
- **honeyhunterworld.com** — Equipment builder, set search
  - JS-heavy: Interactive tool — try bright-scrape, may return partial armor set builder
  - Scrape: Static pages work for individual item lookups

---

## MOBAs

### League of Legends
- **op.gg** — Champion builds, runes, win rates, tier lists by rank
  - Scrape: Most data renders server-side, standard scrape works
  - JS-heavy: Try bright-scrape for filtered views (specific rank, role, patch)
- **u.gg** — Champion analytics, builds, counters, tier lists
  - Scrape: Similar to op.gg — most data accessible via standard scrape
- **lolalytics.com** — Deep statistical analysis, win rate by build path
  - Scrape: Heavy JS rendering
  - JS-heavy: Try bright-scrape for filtered data
- **mobalytics.gg** — Guides, tier lists, pre-game assistant
  - Scrape: Standard scrape for guide pages

### Dota 2
- **dotabuff.com** — Hero stats, item builds, player profiles
  - Scrape: Standard scrape
- **stratz.com** — Match analytics, hero meta, draft analysis
  - Scrape: Some JS, but key data scrapes OK
- **dota2protracker.com** — Pro player builds and picks
  - Scrape: Standard scrape

---

## Looter Shooters

### Destiny 2
- **light.gg** — Weapon database, perk recommendations, community ratings, god rolls
  - Scrape: Standard scrape for individual weapon pages
  - JS-heavy: Try bright-scrape for perk comparison views, community voting data
  - Key feature: Community "god roll" ratings and perk popularity
- **d2foundry.gg** — Weapon stats, damage calculations, perk analysis
  - Scrape: Standard scrape
- **d2armorpicker.com** — Armor stat optimization
  - JS-heavy: Interactive tool — try bright-scrape, may return partial stat allocation
- **destinytracker.com** — Player stats, weapon usage meta
  - Scrape: Standard scrape
- **todayindestiny.com** — Daily/weekly rotations, vendor inventory
  - Scrape: Standard scrape

---

## ARPGs / Loot Games

### Path of Exile / Path of Exile 2
- **poe.ninja** — Build aggregator, economy data, popular skills/items
  - Scrape: Standard scrape for overview pages
  - JS-heavy: Try bright-scrape for build list filtering (class, skill, level range)
  - Key feature: Shows what top players are actually using
- **poewiki.net** — Community wiki, item/skill/mechanic data
  - Scrape: Standard scrape — excellent structured data
- **poedb.tw** (PoE 1) / **poe2db.tw** (PoE 2) — Datamined item/mod databases
  - Scrape: Standard scrape — deep technical data
- **pob.cool** — Path of Building online viewer
  - JS-heavy: Try bright-scrape for loading specific build codes
- **maxroll.gg/poe** — Build guides (written format)
  - Scrape: Standard scrape

### Diablo 4
- **maxroll.gg/d4** — Build guides, tier lists, leveling guides
  - Scrape: Standard scrape — well-structured guide pages
  - Key feature: Guides are regularly updated with patch tags
- **d4builds.gg** — Build planner, item database
  - JS-heavy: Try bright-scrape for interactive build planner
  - Scrape: Item database pages work with standard scrape
- **diablo4.wiki.fextralife.com** — Wiki with stats and lore
  - Scrape: Standard scrape

### Last Epoch
- **lastepochtools.com** — Build planner, item database, loot filter builder
  - JS-heavy: Interactive tool — try bright-scrape, may return partial build planner
  - Scrape: Database pages work with standard scrape

---

## Card / Roguelite

### Balatro
- **balatrogame.fandom.com** — Jokers, strategies, seed exploration
  - Scrape: Standard scrape
- **balatrodb.com** — Joker database (if available)
  - Scrape: Standard scrape

### Slay the Spire
- **slay-the-spire.fandom.com** — Cards, relics, events, strategies
  - Scrape: Standard scrape
- **spirelogs.com** — Run analytics, card win rates
  - Scrape: Standard scrape

### Hades / Hades 2
- **hades.fandom.com** — Boons, weapons, keepsakes, strategies
  - Scrape: Standard scrape

---

## Live Service / MMO

### Helldivers 2
- **helldivers.wiki.gg** — Weapons, stratagems, enemies, missions
  - Scrape: Standard scrape — well-maintained community wiki
- **helldiverscompanion.com** — Loadout sharing (if available)
  - Scrape: Standard scrape

### Final Fantasy XIV
- **ffxiv.consolegameswiki.com** — Comprehensive wiki
  - Scrape: Standard scrape
- **etro.gg** — Gearset builder, BiS (Best in Slot) sets
  - JS-heavy: Interactive tool — try bright-scrape, may return partial gear selection with stat calculations
- **ffxivteamcraft.com** — Crafting/gathering optimizer
  - JS-heavy: Interactive tool — try bright-scrape, may return partial tool
- **thebalanceFFXIV** (Discord-based guides) — Access via search, not direct scrape

### World of Warcraft
- **wowhead.com** — Items, quests, guides, talent calculator
  - Scrape: Standard scrape for most pages (some JS widgets)
  - JS-heavy: Try bright-scrape for talent calculator interaction
  - Key feature: Comment sections often have community tips
- **raidbots.com** — DPS simulation, gear comparison
  - JS-heavy: Interactive simulation tool — scraping returns limited data
- **subcreation.net** — M+ and raid tier lists based on data
  - Scrape: Standard scrape
- **raider.io** — M+ rankings, player scores
  - Scrape: Standard scrape

### Warframe
- **warframe.fandom.com** — Extremely detailed wiki
  - Scrape: Standard scrape — one of the best game wikis
- **overframe.gg** — Build sharing, tier lists, mod configs
  - Scrape: Standard scrape for viewing builds
  - JS-heavy: Try bright-scrape for build creation tool

---

## Navigation Tips

### When Standard Scrape Is Enough
Most wiki pages, static guide articles, forum threads, and overview/stats pages render content server-side. Try `node {baseDir}/scripts/bright-scrape.mjs` first — Bright Data's Web Unlocker handles most cases including JS-rendered sites.

### When Scraping Returns Incomplete Data
Some sites require clicking filters or submitting input. In these cases:
- Try adding URL parameters instead of clicking (many sites support filter params)
- Try `node {baseDir}/scripts/exa-contents.mjs` as an alternative extractor
- If the data is truly interactive-only, search for the same information on an alternative source from this directory

### Fallback Chain
1. Try `node {baseDir}/scripts/bright-scrape.mjs` first
2. If content is missing/incomplete, try `node {baseDir}/scripts/exa-contents.mjs`
3. If both fail, search for the same data on an alternative source from this directory
