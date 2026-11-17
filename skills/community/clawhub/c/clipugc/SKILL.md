---
name: clipugc
description: ClipUGC CLI - create AI-generated UGC-style marketing videos for mobile apps from the terminal. Use when the user wants to create an AI character or AI influencer, generate character looks or reference images, create a UGC video or video clip from a look or photo, animate a photo with a driver video, put an app screen recording and a hook into a clip to make the finished UGC video, suggest hook texts for UGC videos, check ClipUGC credits or balance, manage ClipUGC characters/images/videos (list, show, rename, publish, delete, retry, download), or log in to ClipUGC with an API key.
argument-hint: "[command or description]"
---

# ClipUGC CLI Skill

You are helping the user run ClipUGC CLI commands. [ClipUGC](https://clipugc.com) makes AI-generated, influencer-style UGC (user-generated-content) marketing videos for mobile apps. The pipeline: create an AI character (structured appearance "DNA") → generate photorealistic looks (reference images) → turn a look into short video clips → put the user's app screen recording + a hook text (+ optional music) into a clip to make the finished UGC video.

Credits are consumed server-side (duration-aware; refunds return the exact amount charged): image = 2, clip (5s) = 7, clip (10s) = 13, motion control = 3 per second of driver video on the default kling engine, 2 on `--engine wan` (rounded up, capped at 30s), putting a character into your own video (`videos replace`) = 3 per second (capped at 30s), scene-staged clip (a video created with `--scene`) = 9, finished video (app recording + hook) = free (0). Prefer the live values from `clipugc credits`.

> **MCP alternative.** The same binary is an MCP server (`clipugc mcp`). If this session has the
> `clipugc` MCP server connected (tools named `list_characters`, `create_character`, `generate_image`,
> `list_images`, `create_clip`, `create_motion_clip`, `create_scene_replace_clip`, `merge_ad`, `get_video`, `download_video`,
> `get_credits`, `list_hooks`), prefer those tools over shelling out: they call the same API with the
> same API key, take the same arguments as the CLI flags (underscores instead of dashes, e.g.
> `per_page`), and return JSON. Generation tools return the job id immediately; poll `get_video`
> (clips, and finished videos with `kind: "finished"`) or `list_images` (looks) until `status` is `completed`, the way
> `--wait` would. Everything else in this skill (workspace layout, credit gates, id spaces, prompt
> rules) applies unchanged. To connect it: `claude mcp add clipugc -- npx -y clipugc@latest mcp`. When the
> MCP server is not connected, use the CLI commands below.

> **Creative direction lives in the `ugc-director` skill.** If the user asks "make a video for my app", wants hook ideas, reaction styles, casting advice, or a full concept-to-video plan, use `ugc-director` (it decides WHAT to generate: archetype, hook text, look scene, clip prompt) and come back here for command syntax. This skill is the command manual.

## Routing

Match the user's intent (from `$ARGUMENTS` or conversation context) to the right command:

| Intent | Command |
|--------|---------|
| Log in / authenticate | `clipugc auth login [--api-key <key>]` |
| Check login state | `clipugc auth status` |
| Log out | `clipugc auth logout` |
| Who am I | `clipugc whoami` |
| Check credits / balance / costs | `clipugc credits` |
| Show credit transaction history | `clipugc credits history [--per-page <n>] [--page <n>]`, paginated ledger of spends (negative), top-ups, and refunds |
| List / read / set config | `clipugc config list` / `config get <key>` / `config set <key> <value>` / `config path` |
| Delete the account | `clipugc account delete` (double confirmation; `--yes` skips) |
| Browse public characters | `clipugc characters list --discover [--search <q>]` |
| List my characters | `clipugc characters list --mine` |
| Combined character feed | `clipugc characters list --feed`, own characters newest-first, then public ones in unlock order; a Locked column marks locked rows |
| Create an AI character / influencer | `clipugc characters create --description "plain-text description of the person" [--scene "optional scene/pose"] [--inspiration img1.jpg img2.jpg] [--private] [--make-video [--motion-prompt "…"]] [--wait]`, the server extracts appearance DNA from the description and generates the first look automatically (2 credits). Public/discoverable by default; `--private` opts out. `--make-video` also stages the character's first video clip (id + status are printed; follow with `videos status <id>`), `--motion-prompt` steers its motion. Advanced structured path: `--name` + DNA flags/`--dna-json`. |
| Show / rename / publish / unpublish / delete a character | `clipugc characters show <id>` / `rename <id> --name "New"` / `publish <id>` / `unpublish <id>` / `delete <id> [--yes]` |
| Generate looks / reference images | `clipugc images generate --character <id> [--shots frontal,three_quarter,profile,back] [--template model_digitals\|scene_recreation\|specific_angle] [--scene "..."] [--resolution 0.5K\|1K\|2K\|4K] --wait`, a new look OF that character; `--scene` puts the same person in a new setting/outfit |
| List / inspect a character's images | `clipugc images list --character <id>` / `images show <id>` / `images status <id>` |
| Download a look image | `clipugc images download <id> [-o out.png]` |
| Scene variation of a look | `clipugc images variation <id> --scene "..." [--count 1-4] [--before-after] --wait`, remixes THAT specific look; `--count` returns up to 4 alternatives in one call |
| Retry / delete an image | `clipugc images retry <id> --wait` / `images delete <id> [--yes]` |
| List clips | `clipugc videos list [--character <id>] [--mergeable]`, `--character` filters to one AI character, `--mergeable` = completed clips with no finished video yet (ready for `videos merge`) |
| Create a video clip from a look or photo | `clipugc videos create (--image <lookId> \| --photo <file>) [--prompt "..."] [--scene "..."] [--duration 5\|10] [--keep-sound] --wait`, with `--scene` the server first stages that look into the new setting (same face), then animates it (scene-staged cost) |
| Animate a look/photo with a driver video | `clipugc videos motion (--image <lookId> \| --photo <file>) --driver <video.mp4> [--engine kling\|wan] [--resolution 720p] [--keep-sound] --wait`, `--engine wan` is cheaper (2/sec), keeps the look's background and ignores `--prompt`; kling (default) reads `--prompt` |
| Put the user's AI influencer into the user's own video | `clipugc videos replace --image <lookId> --driver <yourVideo.mp4> [--resolution 720p] [--keep-sound] --wait`, the AI influencer takes the place of the person in a video the user filmed or holds the rights to, in its own scene; the clip carries an "AI generated" label. Only looks of AI influencers designed in ClipUGC work, never the user's own photo. Never pass someone else's social video. |
| Add app recording + hook to a clip (finished UGC video) | `clipugc videos merge <videoId> --app-video <screenrec.mp4> --hook "..." [--music <file.mp3>] --wait`, creates a finished video with its OWN id (printed; `merged_video_id` under `--json`). `--wait` blocks until the render finishes (or fails); then `finished download <videoId>` gets the file |
| Inspect / download a clip | `clipugc videos show <id>` / `videos status <id>` / `videos download <id> [-o out.mp4]` |
| Retry / delete a clip | `clipugc videos retry <id> --wait` / `videos delete <id> [--yes]` |
| List finished videos | `clipugc finished list [--status pending\|processing\|completed\|failed]` (same as `videos list --finals`) |
| Inspect / download a finished video | `clipugc finished show <videoId>` / `finished download <videoId> [-o out.mp4]` |
| Retry / delete a finished video | `clipugc finished retry <videoId> --wait` (free; only when `can_retry`) / `finished delete <videoId> [--yes]`, deleting a finished video leaves its source clip on the profile |
| Suggest hook texts | `clipugc hooks suggest [--context "my app is a habit tracker"]` |

**Clip ids and finished video ids are different id spaces.** A clip lives at `clipugc videos …`,
the finished video made from it lives at `clipugc finished …`, and `finished download 121` is not
`videos download 121`. Always take the finished video id from the `videos merge` output
(`merged_video_id`), never assume it equals the clip id. (`clipugc ads …` is the old name of
`clipugc finished …` and still works.)

**Every picture keeps the character's face.** A character's first completed picture is its BASE
IMAGE, the identity anchor, which never moves. Every later picture, from either picture command,
is generated as an edit of that base image, so the same person carries across settings, outfits and
moods. Only a brand-new character's first picture comes from the description/DNA alone (there is
nothing to anchor to yet), and uploaded `--inspiration` images take precedence over the base image.
So choose by intent, not by identity risk:

- `images generate --character <id> --scene "…"`: a new look OF this character. The default for
  building out a character (new setting, outfit, mood) and for extra angles via `--shots`.
- `images variation <lookId> --scene "…"`: remix THAT specific look, or when you want `--count 1-4`
  alternatives in a single call, or a `--before-after` pair.

If the intent is unclear, ask the user what they want to do and show the available commands.

Constraints to enforce before running: `--scene` max 600 chars; `--prompt` max 1500 chars; `--hook` max 150 chars; driver video mp4/mov max 50MB and max 30s; `--per-page` max 50. File formats, photo: png/jpg/jpeg/webp; app screen recording (`--app-video`): mp4, mov, m4v, 3gp or webm, max 100MB; driver video: mp4/mov; music: mp3/wav/m4a. Uploads are auto-presigned; just pass local file paths.

## Prerequisites Check

Before running ANY command, always check:

0. **MCP connected?** If the `clipugc` MCP tools are available in this session, call `get_credits` instead of steps 1-3: a successful reply proves the server is installed and authenticated and gives the balance in one call. If it returns an auth error, the message tells the user to run `clipugc auth login` (or set `CLIPUGC_API_KEY` for the server).
1. **CLI installed**: Run `which clipugc`. If missing, run `npm install -g clipugc` (requires Node >= 20).
2. **Authenticated**: Run `clipugc auth status`. If not logged in, tell the user to create an API key in the ClipUGC dashboard (https://clipugc.com/dashboard → API keys) and run `clipugc auth login`. Do NOT ask the user to paste the key into chat, `auth login` prompts for it securely in the terminal.
**Credits packs**: `clipugc credits packs` lists purchasable packs (buy on the web dashboard / mobile IAP).

3. **Credits**: Before any generation command (`images generate`, `images variation`, `videos create`, `videos motion`, `videos replace`, `videos merge`), run `clipugc credits` to check the balance against the action's cost (image 2, clip 5s 7, clip 10s 13, motion control 3 per second of driver video, scene-staged clip 9, finished video free). Costs are duration-aware, so prefer the live values from `clipugc credits` over hard-coded numbers.

## Project workspace: organized output & resuming

Keep every artifact and id in a predictable workspace so a later session (or another agent) can resume without archaeology. Root: `./clipugc/` in the user's project cwd, unless the user names another location.

```
clipugc/
├── assets/                     # user inputs kept for reuse: app screen recordings, music, inspiration photos
└── influencers/
    └── <id>-<kebab-name>/      # e.g. 12-isabella-romero
        ├── influencer.json     # manifest, source of truth for resuming
        ├── pictures/           # looks: <imageId>-<short-desc>.<ext>
        ├── clips/              # raw clips: <videoId>-<mode>-<duration>s.mp4   (mode: i2v | motion)
        └── finished/           # finished videos: <videoId>-<hook-slug>.mp4   (videoId = merged_video_id)
```

Rules:

1. **Record ids immediately.** Append each new id + the exact prompt to `influencer.json` right after the API call returns, BEFORE any `--wait`, so an interrupted session loses nothing.
2. **Update the manifest after EVERY step** (create / generate / variation / videos create / motion / videos merge / download): statuses, file paths, finished-video state.
3. **Copy user inputs into `clipugc/assets/`** before uploading them, so hook A/B variants reuse the same recording/music.
4. **Download with explicit output paths** into the folders (`-o` creates missing parent directories):
   ```bash
   clipugc images download 87 -o clipugc/influencers/12-isabella-romero/pictures/87-cafe-selfie.png
   clipugc videos download 91 -o clipugc/influencers/12-isabella-romero/clips/91-i2v-5s.mp4
   # `videos merge 91 …` returns a finished video with its own id (merged_video_id, e.g. 121).
   # Download it by that id into finished/:
   clipugc finished download 121 -o clipugc/influencers/12-isabella-romero/finished/121-fixed-my-morning-routine.mp4
   ```

Compact `influencer.json` shape (extend as needed, keep these fields):

```json
{
  "id": 12,
  "name": "Isabella Romero",
  "description": "casual gen-z woman in her early 20s, brown hair, friendly smile",
  "created_at": "2026-07-23",
  "visibility": "public",
  "pictures": [
    { "id": 87, "prompt": "golden-hour cafe selfie", "file": "pictures/87-cafe-selfie.png", "status": "completed" }
  ],
  "clips": [
    { "id": 91, "mode": "i2v", "duration": 5, "prompt": "…a smirk slowly spreads, lips closed…", "source_image_id": 87, "file": "clips/91-i2v-5s.mp4", "status": "completed", "merged": true }
  ],
  "finished": [
    { "merged_video_id": 121, "video_id": 91, "hook_text": "this app fixed my morning routine", "app_video": "../../../assets/screenrec.mp4", "file": "finished/121-fixed-my-morning-routine.mp4", "status": "completed" }
  ]
}
```

Older workspaces may have an `ads/` folder and an `"ads"` array instead. Read them the same way and keep using them for that influencer.

**Resuming**: when asked to continue work on an influencer or video, FIRST read `clipugc/influencers/*/influencer.json`. Then reconcile with the server before doing new work: `clipugc characters show <id> --json`, `clipugc videos list --character <id> --json`, `clipugc finished list --json`, and `images status <id>` / `videos status <id>` / `finished show <videoId>` on anything the manifest still marks pending/processing, update the manifest with what you learn. If no manifest exists but the user references an existing influencer, find it (`characters list --mine`), then create the folder + manifest from server state (`characters show`, `images list --character <id>`, `videos list --character <id>`).

## Typical Workflows

Use `--json` on any command when you need to parse output, capture ids (character id, image id, video id) from command output and reuse them in the next step. Use `--wait` on generation commands so they block until the job is `completed` or `failed`. Route every id, prompt, and download through the project workspace above.

**Picture before clip.** Generate the look first, show it to the user, and wait for an explicit yes before running `videos create`, a rejected look costs 2 credits, a rejected clip costs 9.

### Workflow A: Create a character with looks

1. Create the character from the user's description (map traits to DNA flags):
   ```bash
   clipugc characters create --description "casual gen-z woman in her early 20s, brown hair, friendly smile" --json
   ```
   Capture the character id from the output, create `clipugc/influencers/<id>-<kebab-name>/`, and start its `influencer.json`.
2. Generate reference looks (2 credits per image; check credits first):
   ```bash
   clipugc images generate --character <characterId> --shots frontal,three_quarter --wait --json
   ```
3. Add looks in other settings whenever the plan needs them, same face, new scene (2 credits each):
   ```bash
   clipugc images generate --character <characterId> --scene "front-camera phone selfie in a parked car, daylight through the windshield, natural skin texture" --wait --json
   ```
   Reach for `images variation <lookId> --scene "…"` instead when the user points at ONE existing
   look to remix, or when `--count 1-4` / `--before-after` is wanted.
4. Show the results and let the user pick:
   ```bash
   clipugc images list --character <characterId>
   ```
   There is no separate "select" step, pass the chosen look's ID straight to `videos create --image <ID>`. Record each look's id + prompt in `influencer.json` and download keepers into `pictures/`.

### Workflow B: Make a UGC video for an app end-to-end

1. Pick a look: `clipugc images list --character <characterId>` and note its ID (or use `--photo <file>` if the user supplies their own photo). No separate select step, the chosen ID is passed straight to `videos create --image <ID>`.
2. Create the clip (7 credits for 5s, 13 for 10s; a `--scene` staged clip is 9). Prefer a SILENT reaction, mouth closed, no talking, because lip-sync is the biggest AI giveaway; the hook text overlay does the talking:
   ```bash
   clipugc videos create --image <imageId> --prompt "Handheld selfie framing, tiny wobble. Her eyebrows lift, eyes widen, a delighted grin slowly spreads, she nods twice holding eye contact. Lips closed, no talking. Hair moves subtly." --duration 5 --wait --json
   ```
   Capture the video id (record it + the prompt in `influencer.json` before waiting). For archetype-specific reaction prompts (smirk, jaw-drop, crying, side-eye, deadpan…), hook formulas, and casting guidance, use the `ugc-director` skill, it turns an app idea into a full UGC video plan.
3. Get hook suggestions if the user doesn't have one:
   ```bash
   clipugc hooks suggest --context "my app is a habit tracker"
   ```
   Let the user pick a hook (max 150 chars).
4. Add the app screen recording and the hook (free). Copy the recording into `clipugc/assets/` first so hook variants reuse it:
   ```bash
   clipugc videos merge <videoId> --app-video clipugc/assets/screenrec.mp4 --hook "This app fixed my morning routine" --wait --json
   ```
   Capture `merged_video_id` from the output. That is the finished video id, and it is what every
   later `clipugc finished` command takes. Record it in the manifest's `finished` array immediately.
5. Download the finished video into the workspace, named by its id:
   ```bash
   clipugc finished download <videoId> -o clipugc/influencers/<id>-<name>/finished/<videoId>-<hook-slug>.mp4
   ```

## Troubleshooting

Exit codes: 0 ok, 1 generic, 2 validation, 3 auth, 4 not found, 5 premium required, 6 insufficient credits, 7 network/server unreachable.

| Symptom | Fix |
|---------|-----|
| Exit 6 / "Insufficient credits" | Run `clipugc credits` to show the balance and per-action costs. Tell the user to top up credits in the ClipUGC dashboard (https://clipugc.com/dashboard). |
| Exit 3 / auth error | The stored key is missing, invalid, or revoked. Tell the user to create a fresh API key in the dashboard and re-run `clipugc auth login`. |
| Exit 7 / network error | Check `clipugc config get apiBaseUrl` (and the `CLIPUGC_API_BASE_URL` env var), the API base URL may be wrong or the server unreachable. Retry after verifying connectivity. |
| Exit 5 / premium required | The action needs a paid plan. Tell the user to upgrade their plan in the ClipUGC dashboard. |
| "plan" error on `characters create` or `stories` | Plan limits: character creation is capped per month by plan (Professional 3, Business 10), and Stories need the Business plan. Relay the server's message and suggest upgrading, do not retry. |
| Exit 2 / validation error | An input broke a constraint (scene > 600 chars, prompt > 1500, hook > 150, driver video > 50MB or > 30s, wrong file format, per-page > 50). Fix the input and re-run. |
| A generation ended `failed` | Retry it: `clipugc images retry <id> --wait` or `clipugc videos retry <id> --wait`. Check details first with `images show <id>` / `videos show <id>`. |
| Not sure what state a job is in | `clipugc images status <id>` / `clipugc videos status <id>` (no credits consumed). |
