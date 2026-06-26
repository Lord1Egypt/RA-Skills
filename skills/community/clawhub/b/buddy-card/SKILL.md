# Claude Buddy Card

Generate a stunning, shareable trading card of your unique Claude Buddy — the hidden AI companion from Claude Code's leaked source.

Use when user says: "buddy card", "generate my buddy", "claude buddy", "my buddy card", "show my buddy", "/buddy-card", "buddy-card"

## What This Does

Every Claude Code user has a unique AI companion (Buddy) determined by their account ID. This skill:

1. Reads your Claude identity from your local macOS Keychain
2. Runs the exact algorithm from Claude Code's leaked source (v2.1.88) to determine your Buddy
3. Generates a premium holographic trading card with AI art
4. Shows your Buddy's species, rarity, stats, and accessories

Only YOU can generate your card — your identity is locked in your local Keychain.

## How It Works

### Step 1: Get the user's accountUuid

Run this to extract the user's Claude OAuth token and fetch their account UUID:

```bash
CREDS=$(security find-generic-password -s "Claude Code-credentials" -w 2>/dev/null)
```

If empty, tell the user: "You need to be logged into Claude Code first. Run `claude` in your terminal."

Extract the OAuth token:
```bash
TOKEN=$(echo "$CREDS" | python3 -c "import json,sys; print(json.load(sys.stdin).get('claudeAiOauth',{}).get('accessToken',''))")
```

Fetch the accountUuid from the API (try with proxy first for users behind VPN):
```bash
PROFILE=$(curl -sS --max-time 10 -H "Authorization: Bearer $TOKEN" "https://api.anthropic.com/api/oauth/profile" 2>/dev/null)
UUID=$(echo "$PROFILE" | python3 -c "import json,sys; print(json.load(sys.stdin)['account']['uuid'])")
```

If that fails (SSL/timeout), retry with common proxy:
```bash
PROFILE=$(curl -sS --max-time 10 -x http://127.0.0.1:1082 -H "Authorization: Bearer $TOKEN" "https://api.anthropic.com/api/oauth/profile" 2>/dev/null)
```

### Step 2: Generate Buddy data

Run the algorithm script with the UUID:
```bash
BUDDY_JSON=$(node ${SKILL_DIR}/scripts/buddy-algorithm.js "$UUID")
```

This outputs JSON with: species, rarity, eye, hat, shiny, stats (DEBUGGING, PATIENCE, CHAOS, WISDOM, SNARK), peak stat, dump stat, cardNumber, rarityColor, etc.

Display the results to the user:
```
Your Claude Buddy:
  🫧 blob (果冻) — ★★ Uncommon
  Eyes: ×  Hat: tophat  Shiny: no
  #5099 / 7128

  DEBUGGING   24 ████░░░░░░░░░░░░░░░░
  PATIENCE    90 ██████████████████░░ ⬆ PEAK
  CHAOS       38 ███████░░░░░░░░░░░░░
  WISDOM      17 ███░░░░░░░░░░░░░░░░░
  SNARK        5 █░░░░░░░░░░░░░░░░░░░ ⬇ DUMP
```

### Step 3: Generate the card image

Generate the card using the built-in image generation script. The script only needs a `GOOGLE_API_KEY` (free at https://aistudio.google.com/apikey):

```bash
bun ${SKILL_DIR}/scripts/generate-image.ts --prompt "<CARD_PROMPT>" --image ~/Downloads/claude-buddy-card.jpg --ar 3:4
```

If bun is not installed, use: `npx -y bun ${SKILL_DIR}/scripts/generate-image.ts ...`

Build the prompt from the buddy data using these templates:

**For Common (★) rarity:**
```
Trading card with simple dark steel frame and subtle {RARITY_COLOR} glow (common rarity). TOP: "{SPECIES}" in silver text, "★ COMMON" badge in gray. CENTER: A cute {SPECIES_DESCRIPTION} with {EYE} shaped eyes. {HAT_DESCRIPTION}. Simple dark background. BOTTOM STATS PANEL (EXACTLY 5 rows, no more no less): {STATS_BLOCK}. FOOTER: "#{CARD_NUMBER} / 7128" left, "CLAUDE BUDDY" right. Clean TCG card style.
```

**For Uncommon (★★) and Rare (★★★):**
```
Premium holographic trading card, dark metallic ornate frame with {RARITY_COLOR} glow and rainbow prismatic edges. TOP: "{SPECIES}" in gold embossed text, "{RARITY_STARS} {RARITY_LABEL}" badge in {RARITY_COLOR}. CENTER: {CREATURE_PROMPT}. Floating above a glowing magic circle. BOTTOM STATS PANEL (CRITICAL - EXACTLY 5 stat rows, no more, no less, single column, evenly spaced): {STATS_BLOCK}. The {PEAK_STAT} bar is GOLDEN (longest). The {DUMP_STAT} bar is GRAY (shortest). Other bars are {RARITY_COLOR}. ONLY these 5 stats. FOOTER: "#{CARD_NUMBER} / 7128" left, "CLAUDE BUDDY" right. Holographic TCG premium quality.
```

**For Epic (★★★★) and Legendary (★★★★★):**
```
{LEGENDARY_PREFIX} premium holographic trading card with {FRAME_COLOR} ornate frame, intense glow, maximum rainbow holographic prismatic surface. TOP: "{SPECIES}" in massive gold foil text, "{RARITY_STARS} {RARITY_LABEL}" in blazing {RARITY_COLOR}. CENTER: {CREATURE_PROMPT}. Floating above blazing magic circle with lightning. BOTTOM STATS PANEL (CRITICAL - EXACTLY 5 rows, no more no less): {STATS_BLOCK}. {PEAK_STAT} bar GOLDEN (peak). {DUMP_STAT} bar GRAY (dump). ONLY 5 stats. FOOTER: "#{CARD_NUMBER} / 7128" left, "CLAUDE BUDDY" right. Museum-quality TCG, maximum holographic effects.
```

**Stats block format — ALWAYS use this EXACT fixed order (same as source code):**
```
DEBUGGING {BAR} {VALUE}
PATIENCE  {BAR} {VALUE}
CHAOS     {BAR} {VALUE}
WISDOM    {BAR} {VALUE}
SNARK     {BAR} {VALUE}
```

Use █ and ░ to show proportional bar length. This order is FIXED — never sort by value or rearrange. Example:
```
DEBUGGING ████░░░░░░░░░░░░░░░░ 24
PATIENCE  ████████████████████ 90
CHAOS     ███████░░░░░░░░░░░░ 38
WISDOM    ███░░░░░░░░░░░░░░░░ 17
SNARK     █░░░░░░░░░░░░░░░░░░  5
```

**Creature prompt varies by species:**
- blob: "a cute translucent blob creature made of luminous jelly with swirling galaxies inside"
- dragon: "a majestic dragon made of cosmic crystal with glowing scales"
- cat: "an elegant cosmic cat with mystical fur patterns"
- octopus: "a majestic octopus made of cosmic energy with flowing tentacles"
- axolotl: "an adorable pink axolotl with feathery gills, made of glowing crystal"
- duck: "a cute rubber-duck-like creature with a warm glow"
- (etc — adapt description to species)

Add hat description if hat != "none":
- crown: "wearing a golden crown"
- tophat: "wearing a small elegant black top hat"
- wizard: "wearing a tiny wizard hat with stars"
- halo: "with a glowing golden halo above its head"
- propeller: "wearing a fun propeller beanie hat"
- beanie: "wearing a cozy knit beanie"
- tinyduck: "with a tiny rubber duck sitting on its head"

Add if shiny: "The creature has an iridescent rainbow sheen, glowing with prismatic light. SHINY VARIANT."

Generate at aspect ratio 3:4, quality 2k.

### Step 4: Show result and offer regenerate

Show the generated card image to the user. Then ask:

"Your Claude Buddy card is ready! Happy with it? If not, I can regenerate — the card art varies each time, stats stay the same."

If user wants to regenerate, go back to Step 3 with the same data but the image generation will produce a different visual.

### Step 5: Save

Save the final card to `~/Downloads/claude-buddy-card.jpg` (or user-specified path).

## Setup (one-time)

1. **Get a free Google API key** at https://aistudio.google.com/apikey
2. **Set it in your shell:**
   ```bash
   export GOOGLE_API_KEY="your-key-here"
   ```
   Or add to `~/.zshrc` / `~/.bashrc` to persist.

That's it. Everything else is built in.

## Requirements

- macOS (needs Keychain access for Claude identity)
- Claude Code logged in (OAuth token in Keychain)
- `GOOGLE_API_KEY` env var (free tier is enough — Gemini image gen)
- Node.js or Bun (for buddy algorithm + image generation)

## Scripts

- `${SKILL_DIR}/scripts/buddy-algorithm.js` — exact buddy generation algorithm from Claude Code v2.1.88
- `${SKILL_DIR}/scripts/generate-image.ts` — self-contained Gemini image generation (no external dependencies)
