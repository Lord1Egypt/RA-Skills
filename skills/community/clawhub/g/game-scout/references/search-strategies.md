# Search Strategies Reference

Query formulation patterns per source and game. Read this during Phase 2 to craft effective search queries.

---

## Table of Contents
1. [Exa AI Query Patterns](#exa-ai-query-patterns)
2. [Bright Data SERP Patterns](#bright-data-serp-patterns)
3. [YouTube Discovery](#youtube-discovery)
4. [Twitter/X Search](#twitterx-search)
5. [Game-Specific Community Hubs](#game-specific-community-hubs)
6. [Query Refinement by Topic Type](#query-refinement-by-topic-type)

---

## Exa AI Query Patterns

Exa uses semantic/neural search — phrase queries naturally, like describing what you want to find. Negation works ("builds without shotguns"). Avoid keyword-stuffing.

### Effective Patterns
- **Build query**: `"best [class/weapon type] build for [game] in [current season/patch]"`
- **Meta query**: `"current meta tier list for [game] [mode] [season/patch]"`
- **Mechanic query**: `"how does [mechanic] work in [game], does it interact with [other mechanic]"`
- **Patch impact**: `"[game] [patch version] changes impact on [build/strategy/item]"`
- **Pro play**: `"what professional [game] players are using in [tournament/ranked]"`

### Exa-Specific Tips
- Use the `findSimilar` endpoint when you find one great source — it returns semantically related pages
- Use `contents` extraction to get clean text from URLs found in search
- Include date filters for recency-critical queries (set `startPublishedDate` to recent)
- Exa handles negation well: "strong weapons that aren't shotguns in Marathon" works correctly

---

## Bright Data SERP Patterns

Keyword-based Google search. Use search operators for precision. Fire up to 10 queries via `search_engine_batch`.

### Google Dork Patterns
- **Reddit targeting**: `site:reddit.com r/[subreddit] [topic] [year]`
- **Wiki targeting**: `site:fextralife.com [game] [item/build]` or `site:[game-wiki] [query]`
- **Forum targeting**: `site:forums.[game].com [topic]`
- **Recency**: `[query] after:[YYYY-MM-DD]` (Google date filter)
- **Exact phrases**: `"[exact item name]" [game] build`
- **Exclude outdated**: `[query] -"patch [old version]"` (exclude old patch discussions)

### Batch Query Strategy
Fire a batch of 3-5 complementary queries:
1. Broad: `[game] [topic] guide [year]`
2. Reddit: `site:reddit.com [game subreddit] [topic]`
3. Wiki/DB: `site:[relevant wiki] [specific item/build]`
4. YouTube: `site:youtube.com [game] [topic] guide [year]`
5. Recent: `[game] [topic] [current patch/season]`

---

## YouTube Discovery

Find video guides by searching via SERP, then extract transcripts in Phase 3.

### Search Patterns
- `site:youtube.com [game] [topic] guide [year]`
- `site:youtube.com [game] [topic] build [current season]`
- `site:youtube.com [game] best [weapon/class/character] [year]`
- `site:youtube.com [game] tier list [current patch]`

### Prioritization Signals
In SERP results, look for:
- High view counts (mentioned in snippet)
- Recent upload dates (within last 1-3 months)
- Known guide creators (channel names that appear repeatedly)
- Descriptive titles with specific build/strategy names

---

## Twitter/X Search

Use for real-time community sentiment, pro player opinions, and patch reactions.

### SERP-Based Twitter Search
- `site:twitter.com [game] [topic] [year]`
- `site:twitter.com [pro player name] [game]`
- `site:twitter.com [game] patch notes reaction`
- `site:twitter.com [game] meta [current season]`

### If `web_data_x_posts` Is Available
Search for posts directly using keywords. Focus on:
- Pro player accounts and content creators
- Posts with high engagement (likes, retweets)
- Posts from the last 2-4 weeks for recency
- Hashtags: `#[GameName]`, `#[GameAbbreviation]Meta`, `#[PatchVersion]`

---

## Game-Specific Community Hubs

### FPS / Tactical Shooters
| Game | Subreddit | Wiki/DB | Tracker |
|------|-----------|---------|---------|
| **Marathon** | r/Marathon, r/MarathonTheGame | TBD (emerging) | TBD |
| **Valorant** | r/VALORANT, r/ValorantCompetitive | liquipedia.net/valorant | tracker.gg/valorant |
| **CS2** | r/GlobalOffensive, r/cs2 | liquipedia.net/counterstrike | csstats.gg |
| **Overwatch 2** | r/Overwatch, r/OverwatchUniversity | overwatch.blizzard.com | overbuff.com |
| **Apex Legends** | r/apexlegends, r/apexuniversity | apexlegends.wiki.gg | apexlegendsstatus.com |

### Battle Royale / Warzone
| Game | Subreddit | Wiki/DB | Tracker |
|------|-----------|---------|---------|
| **Warzone** | r/CODWarzone | sym.gg | wzstats.gg, cod.tracker.gg |
| **Fortnite** | r/FortniteCompetitive | fortnite.gg | fortnitetracker.com |

### Souls-likes / Action RPG
| Game | Subreddit | Wiki/DB | Build Tools |
|------|-----------|---------|-------------|
| **Elden Ring** | r/EldenRing, r/Eldenring | fextralife.com/Elden+Ring | mugenmonkey.com |
| **Dark Souls 3** | r/darksouls3 | fextralife.com/Dark+Souls+3 | mugenmonkey.com |
| **Monster Hunter** | r/MonsterHunter, r/MonsterHunterMeta | mhworld.kiranico.com | honeyhunterworld.com |

### MOBAs
| Game | Subreddit | Wiki/DB | Tracker |
|------|-----------|---------|---------|
| **League of Legends** | r/leagueoflegends, r/summonerschool | leagueoflegends.fandom.com | op.gg, u.gg, lolalytics.com |
| **Dota 2** | r/DotA2, r/TrueDoTA2 | dota2.gamepedia.com | dotabuff.com, stratz.com |

### Looter Shooters
| Game | Subreddit | Wiki/DB | Tools |
|------|-----------|---------|-------|
| **Destiny 2** | r/DestinyTheGame, r/destiny2 | light.gg, d2foundry.gg | DIM (Destiny Item Manager) |
| **The Division 2** | r/thedivision | — | — |

### ARPGs / Loot Games
| Game | Subreddit | Wiki/DB | Build Tools |
|------|-----------|---------|-------------|
| **Path of Exile** | r/pathofexile | poedb.tw, poewiki.net | poe.ninja, pob.cool |
| **Path of Exile 2** | r/pathofexile2 | poe2db.tw | poe2.ninja |
| **Diablo 4** | r/diablo4, r/D4Builds | maxroll.gg | d4builds.gg |
| **Last Epoch** | r/LastEpoch | lastepochtools.com | — |

### Card / Roguelite
| Game | Subreddit | Wiki/DB |
|------|-----------|---------|
| **Balatro** | r/balatro | balatrogame.fandom.com |
| **Slay the Spire** | r/slaythespire | slay-the-spire.fandom.com |
| **Hades / Hades 2** | r/HadesTheGame | hades.fandom.com |

### Live Service / MMO
| Game | Subreddit | Wiki/DB | Tools |
|------|-----------|---------|-------|
| **Helldivers 2** | r/Helldivers | helldivers.wiki.gg | — |
| **FFXIV** | r/ffxiv, r/ffxivdiscussion | ffxiv.consolegameswiki.com | etro.gg (gearsets) |
| **WoW** | r/wow, r/CompetitiveWoW | wowhead.com | raidbots.com |
| **Warframe** | r/Warframe | warframe.fandom.com | overframe.gg |

---

## Query Refinement by Topic Type

### Build / Loadout Queries
- Include: class/character name, weapon type, game mode (PvP vs PvE)
- Terms: "build", "loadout", "setup", "gear", "equipment", "spec", "talents"
- Time-sensitive: Include current season/patch/league for live-service games

### Meta / Tier List Queries
- Include: game mode, rank/skill bracket if relevant
- Terms: "tier list", "meta", "best", "strongest", "S tier", "top picks"
- Filter by: current patch version or season name
- Note: Meta varies by skill level — specify if the user mentions their rank

### Mechanic / Interaction Queries
- Include: exact item/ability names in quotes for precision
- Terms: "how does X work", "does X stack with Y", "interaction", "proc", "trigger"
- Best sources: Wikis first, then Reddit for edge cases
- These queries benefit most from narrow, wiki-targeted searches

### Patch / Balance Queries
- Search official patch notes first: `site:[official game site] patch notes [version]`
- Then community reaction: `reddit [game] [patch version] thoughts`
- Check if nerfs/buffs affect the specific topic the user is asking about

### Pro Play / Esports Queries
- Include: "pro", "competitive", "tournament", "ranked", player names
- Sources: Twitter (real-time takes), Liquipedia (tournament data), tracker sites (ranked stats)
- YouTube: Look for VOD reviews, tournament highlight analysis
