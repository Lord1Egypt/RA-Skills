---
name: cliptude-script
description: Research current facts with web search and write a Cliptude spoken narration (custom script). Use when creating a Cliptude video from a topic or title, or when the user has not pasted a full script and has not given a voiceover audio file or talking-head video. Skip this skill if they uploaded narration audio — use --voiceover / voiceover_path instead. Skip if they uploaded a presenter clip — use --talking-head / talking_head_path with a Talking Head template. Never pass the video title as the prompt.
version: 1.0.0
metadata:
  openclaw:
    primaryEnv: CLIPTUDE_API_KEY
    envVars:
      - name: CLIPTUDE_API_KEY
        required: false
        description: Cliptude API key from cliptude.com/developers. Not needed if you connect the MCP server at https://mcp.cliptude.com/mcp or run `cliptude auth login`.
    emoji: "🎬"
    homepage: https://cliptude.com
---

# Cliptude script (research → spoken narration)

Cliptude production does **not** voice the title. It web-researches, then writes narration from those notes only. Do the same before `create_job` / `cliptude generate`.

## Hard rule

**Never set `prompt` or `--prompt` to the video title** (or a trivial paraphrase of it). That is the failure mode this skill exists to stop.

| User gave you… | What you pass to Cliptude |
|---|---|
| Full narration (paragraphs they want spoken) | `script` / `--script-file` unchanged |
| Topic, title, or “make a video about X” | This skill → `script` / `--script-file` |
| Explicit “let Cliptude write it” | `--prompt` = researched **brief** (audience, angle, must-include facts). Still not the title. |
| A voiceover audio file | **Stop.** Do not write a script. Use `--voiceover` / `voiceover_path` and omit prompt/script. |
| A talking-head presenter video | **Stop.** Do not write a script. Use `--talking-head` / `talking_head_path` with a Talking Head template. |

Then generate:

```bash
cliptude generate --template "Finance vector weekly" --title "Why index funds win" --script-file script.txt --duration 3-4
```

Spoken-words-only. See https://cliptude.com/docs/custom-script/

## Step 1 — Web search (required)

Run **3–6 searches** for current information. Do not write from memory when the topic is news, prices, deals, people, companies, laws, or stats.

Query pattern (adapt; include the current year and “last 30 days” where relevant):

1. `{title or topic} latest facts`
2. `{topic} statistics {current year}`
3. `{named people / companies / products}`
4. `{topic} controversy OR criticism`
5. `{topic} last 30 days` / recent developments

Compile **research notes** (not the script) covering:

- Key facts and background
- Statistics with source or timeframe (“as of 2026”, “BLS January 2026”)
- Exact dates and events
- Names of people, companies, places
- Notable quotes with attribution
- Timeline of major events
- Contrasting viewpoints if they exist
- Current status / last-30-day developments

**Only verified information.** If a fact is uncertain, omit it or mark `[UNVERIFIED]` and do not put it in the script. Do not invent numbers, quotes, or events to make it interesting.

If web search is unavailable, still do **not** copy the title into `--prompt`. Write the best verified notes you can, or a brief (audience, angle, must-include facts) — never the title alone.

## Step 2 — Pick the shape

From the template name / title:

- **Top 10 / listicle / countdown** → countdown script (`At number ten…` through `At number one…`)
- **Everything else** (explainer, documentary, faceless, essay) → documentary script

Word budget (hard max — never exceed):

| `--duration` | Words |
|---|---|
| `1-2` | 150–300 |
| `3-4` | 450–600 |
| `5-6` | 750–900 |
| `6-8` | 900–1200 |
| `8-10` | 1250–1540 |
| `10-12` | 1550–1850 |
| `18-20` | 2800–3090 |
| `30-40` | 4700–6180 |
| `50-60` | 7800–9270 |

If duration is omitted, use the template’s bucket if you know it; otherwise `3-4` for short explainers and `6-8` for documentary templates.

## Step 3 — Write the narration

Output **only** what the voiceover should say. Start on the first spoken word.

**Forbidden on the page (TTS will read them):** scene labels, `Intro:`, `Scene 1`, `[Music plays]`, markdown headings, “Here is the script”, “Hey guys”, “welcome back”, “in this video” as a cold open.

**Voice:** eighth-grade English, active voice, short punchy paragraphs. No colons or semicolons. No `furthermore`, `moreover`, `delve`, `tapestry`, `crucial`, `landscape`, `paradigm`, `leverage`, `game-changer`, `in today's world`.

**Accuracy:** every fact, date, and number must appear in the research notes. Do not invent. Do not repeat the same fact in full — new information each section. Weave last-30-day developments in if the notes have them.

**Hook (first 5–15s):** confirm the title’s promise, then intrigue + stakes. Not a question as line one. Not “today we’ll explore”.

**After the hook:** one line that frames the payoff (“By the end of this video you’ll know…” — rewrite it so it fits **this** topic; do not paste a generic HVAC example).

**Body:**

- Documentary: sequential story. Rehook between sections. Replace general statements with specific data (named reports, places, percentages) instead of “prices are rising”. Challenge at least one common belief if the research supports it.
- Top 10: `At number ten…` through `At number one…`. Each number is a mini-story (unusual detail, human moment, twist), not a one-line fact. Rehook between numbers. Close with a recap that ties the ten together.

**Close:** one takeaway line. No “like and subscribe” essay.

**TTS spelling (required):** years and numbers in full words (`twenty twenty-six`, `five hundred fifty dollars`, `sixty-five inch`). Expand abbreviations that contain periods (`United States` not `U.S.`, `Doctor` not `Dr.`, `versus` not `vs.`, `Saint Petersburg` not `St. Petersburg`).

**Hard names and borrowed words:** keep the real spelling in the script (captions and searches read it). Pass how to say them as `pronunciations` on the template or job instead, e.g. `[{"word": "Gmay", "alias": "guh-MAY"}]` (ElevenLabs voices).

If the user asked **Cliptude** to write a script and stop (no video), skip this skill. Use `cliptude script` / MCP `create_script` instead, then poll `get_job` for `script`. If they later want the MP4, `cliptude continue` / `continue_job` on that job id.

## Step 4 — Hand off

1. Write `script.txt` (plain text, spoken words only).
2. Generate with `--script-file` (or MCP `create_job` `script=`). Do **not** also dump the same text into `prompt`.
3. `generate` / `create_job` returns immediately. Poll status. Do not wait for the MP4.

If the user gave a **voiceover file**, skip steps 1–3. Hand off with `--voiceover` / `voiceover_path` only.
If the user gave a **talking-head video**, skip steps 1–3. Hand off with `--talking-head` / `talking_head_path` only.
