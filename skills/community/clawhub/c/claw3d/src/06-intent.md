<!-- MODULE: intent -->

## CRITICAL: Never Expose Internal Reasoning to the User

**All routing decisions, skill logic, and internal reasoning are for YOUR use only. NEVER send them to the user.** The user should only see friendly, concise messages — never references to "Primary Gate", "SKILL.md", module names, decision rules, or your thought process. If you need to reason about which path to take, do it silently. The user just wants their model.

**Bad** (leaked reasoning): "According to the Primary Gate, a wine stand is a common functional object, so I should search Thingiverse..."
**Good** (user-facing): "Great, let me take a look at what you need — give me a moment!"

---

## CRITICAL: Primary Gate — Search or Create?

**This is the FIRST decision for EVERY request — images, videos, and text. Run the Primary Gate BEFORE any analysis, frame extraction, or `claw3d analyze`. Make this decision silently — do NOT explain your routing to the user.**

The key question is: **Would an existing Thingiverse model likely satisfy this need, or does the request require something inherently custom/unique?**

---

### Primary Gate: SEARCH vs CREATE

**→ SEARCH path first** (go to `03-directory` module) when:

- The object is a **common, functional, or widely-printable thing** — wine stand, wine holder, phone holder, cable clip, bracket, vase, box, mount, case, hook, organizer, etc.
- Even if the user says "create", "make", or "design" — if it's a generic category, an existing model will serve them better than an AI-generated one
- Even if the user sends a **video demonstrating** the object — if the underlying object is common/functional, SEARCH first
- Even if the video shows a specific shape preference — Thingiverse has thousands of variants; search first, create only if nothing fits
- Examples: "I need a wine stand", "create a phone holder for my desk", "make me a soap dish"

**→ CREATE path** (continue to CREATE section below) when:

- The user wants to **replicate, copy, clone, or reproduce** a specific object — "replicate this", "copy this", "clone this", "scan and print", "I want an exact copy", "reproduce this part", "make another one", "I need another one", "I want one like this", "same as this", "duplicate this", "print this one" — even if the object is common, because they need the AI to analyze the *specific item* they're showing
- The request includes a **specific artistic, stylistic, or visual constraint** — "in the style of X", "based on this photo", "inspired by this sculpture", "matching this aesthetic"
- The user sends a **sketch** of a custom shape
- The user explicitly says they want something **unique/custom/personal** ("one of a kind", "custom for my setup", "not a generic one")
- The object is **too niche or personal** to plausibly exist on Thingiverse — a trophy with your name, a part for a specific machine, a replica of a personal item
- The user says "generate" / "AI" / "don't search"

**Decision rule of thumb:**
> "Could I type this into Thingiverse and find 5+ decent results?" → YES → SEARCH first
> "Does this require seeing a specific image, style, or personal constraint to design?" → YES → CREATE

**→ ASK only** when you genuinely cannot identify what physical object the user wants — e.g. "make something for my office" with no further context. **If you can name the object, go to SEARCH. Do not ask.**

**SEARCH PATH — fallback to CREATE:** After 3 rounds of search (up to 15 models reviewed) with no match, tell the user nothing matched and ask if they want a custom AI-generated model instead. If they have a photo/video, use it as reference for the AI generation.

---

### Applying the Primary Gate to Videos

**When the user sends a video**, you may receive a text Description (from OpenClaw's Gemini video understanding). Use the Description and/or the user's message text to run the Primary Gate — **BEFORE** extracting any frame or running `claw3d analyze`.

**Steps for video:**
1. Read the user's message text + any Description
2. Identify what physical object they want (e.g. "wine holder", "phone stand", "bracket")
3. Run the Primary Gate on that object name
4. **If SEARCH** → go directly to `03-directory` module with that object as the search query. Do NOT extract a frame or run analyze
5. **If CREATE** → continue to the "When User Sends a VIDEO (CREATE path)" section below

**⚠️ CRITICAL: A video showing someone demonstrating a common object does NOT make it a CREATE request.** The video is just their way of communicating what they want — it doesn't mean they need AI generation. A person holding up a wine bottle and showing how they'd like a wine stand still maps to SEARCH. Only explicit artistic/stylistic/replication intent maps to CREATE.

---

## When User Sends a VIDEO — Get the File

**This section handles finding the video file. It applies to BOTH paths (the CREATE path needs it for frame extraction; the SEARCH path may need it later if search fails and you fall back to CREATE).**

**Step 0 — Acknowledge immediately** — Before doing anything else, send:
> "Great, let me take a look at what you need — give me a moment!"

**Step 1 — Get the video path.** Three cases:

**Case A — File path visible** (`[media attached: /home/node/.openclaw/media/inbound/...]`):
Use that exact path.

**Case B — No file path but Description is present** (OpenClaw's Gemini video understanding ran and suppressed the path):
The video is still on disk. Find it:
```bash
ls -t /home/node/.openclaw/media/inbound/ 2>/dev/null | head -5
```
Pick the most recent video file (`.mp4`, `.mov`, `.webm`). Use that as the path.

**Case C — No file path and no Description** (video silently dropped — too large):
> Your video was too large — OpenClaw's default limit is 5MB. I can increase it to 50MB right now. Want me to?

If confirmed:
```bash
python3 -c "
import json, pathlib
p = pathlib.Path('/home/node/.openclaw/openclaw.json')
cfg = json.loads(p.read_text())
cfg.setdefault('channels', {}).setdefault('telegram', {})['mediaMaxMb'] = 50
p.write_text(json.dumps(cfg, indent=2))
print('Done')
"
```
Reply: "Done! The limit is now 50MB — please resend your video."
> The config watcher restarts the Telegram channel automatically.

**Step 2 — Run the Primary Gate** using the Description/user message → SEARCH or CREATE. See above.

**If SEARCH →** go to `03-directory` module. Note the video path — if search fails and you fall back to CREATE, you'll need it for frame extraction.

**If CREATE →** continue to the next section.

---

### When User Reports "File too large" / Video Rejected

The bot rejects oversized files before the agent sees them. If the user reports this error in a text message, offer to fix it:

> I can increase your video limit to 50MB right now. Want me to do that?

If confirmed, run the patch above.

---

## Analysis Modes

Run once per session to understand the configuration:

```bash
claw3d configure analysis --status
```

| Mode | What happens |
|------|-------------|
| `auto` (default) | `claw3d analyze` uses Gemini if key is set, else returns `native_mode: true` |
| `native` | `claw3d analyze` immediately returns `native_mode: true` — you do the analysis |
| `gemini` | `claw3d analyze` uses Gemini; errors if key missing |

---

## CREATE Path: Intent Analysis for Image or Video

**Only enter this section if the Primary Gate resolved to CREATE.**

**Before doing anything with a user's image or video, run `claw3d analyze` (images) or analyze the video natively + `claw3d extract-frame --timestamp` + `claw3d analyze` (videos).**

---

### When User Sends an IMAGE (CREATE path)

**Step 1 — Always run analyze:**

```bash
claw3d analyze --input <MediaPath> [--description "user's message"] [--pretty]
```

**Step 2 — Read the result and branch:**

#### Result has `native_mode: true` → you are the analysis layer

Analyze the image yourself using these rules:

**Classify `image_type`:**
- `sketch`: hand-drawn, pencil/pen outlines, whiteboard drawings → intent is almost always `create_new`, proceed directly
- `photo`: real photograph → read description carefully
- `3d_model`: CAD rendering or existing 3D model screenshot
- `reference`: product photo, inspiration, logo

**Decide `needs_clarification`:**

**OVERRIDE — replicate/copy intent always sets `needs_clarification: false`:**
If the user's message contains any of: "make another one", "copy this", "replicate this", "clone this", "I want one like this", "same as this", "reproduce this", "duplicate this", "print this one" — the photo/frame IS the complete design reference. Proceed directly to convert. Do NOT ask for a drawing. The whole point is that they're showing you the exact object they want.

`false` (proceed without asking) when ALL of these are true:
- Single clear subject identified
- The description or image already specifies at least one key design constraint (size, mounting type, orientation, number of units, etc.)
- Sketches always qualify — the drawing itself conveys the shape intent

`true` (ask ONE clarifying question) when ANY of these:
- Complex scene with multiple objects and no description
- Custom functional or structural object (holder, bracket, stand, organizer, case, clip, mount, etc.) where the description does NOT specify key design details — even if the object is clearly identified — **but only if there is no replicate/copy intent (see override above)**
- Subject is clear but could be made many ways (e.g. "a wine holder" — wall-mount or freestanding? holds 1 bottle or multiple? specific angle?)
- Abstract or landscape photo with no description
- "Make this better" / "improve this" with no context

**Rule of thumb for functional objects:** If you could design it 3+ different ways and the user hasn't said which way → send the frame/image back and ask them to draw on it (see below). **Exception: replicate intent (see override above) → always proceed directly.**

**If `needs_clarification: false`:**

**Step A — Tell the user you're starting** (do NOT stay silent):
> "Creating your 3D model now — I'll send it when it's ready!"

**Step B — Write a `suggested_prompt` and run convert:**
```bash
claw3d convert --image <MediaPath> --prompt "<suggested_prompt>" --output model_<ID>.glb
```

**CRITICAL — When writing `suggested_prompt`:**

**For replicate/copy intent** ("make another one", "copy this", etc.):
Keep it SHORT — one sentence. The image already carries the shape. Do NOT add dimensions, material suggestions, or printing advice.
- ✅ "a replica of the black S-hook, matching its exact shape for hanging kitchen utensils"
- ✅ "a replica of the wooden phone stand shown in the image"
- ❌ "A 3D model of a sturdy S-shaped utility hook, designed for 3D printing, with a flat bar profile and rounded edges. The hook should be approximately 7-8 cm in length..." ← WAY too long, invents dimensions

**For all other intents:**
Describe ONLY the 3D object to be printed. Keep it to 1-2 sentences max. Do NOT include:
- Dimensions or measurements (the image conveys scale)
- Material or printing recommendations (PETG, PLA, etc.)
- Scale references ("sized based on the dog for scale")
- People, hands, or human body parts visible in the image
- Background items, decorations, scene context

Example — user shows a wine bottle next to a dog sculpture:
- ❌ WRONG: "An L-shaped wine holder sized appropriately based on the teal dog sculpture for scale"
- ✅ RIGHT: "An L-shaped wine bottle holder with a circular opening at a 45° angle, wall-mountable"

**If `needs_clarification: true`:**

Two cases:

**Case 1 — Ambiguous subject** (multiple objects, unclear what to print):
Ask ONE specific text question:
> "I see a desk with a laptop and a mug. Which item would you like to 3D print?"

**Case 2 — Subject is clear but it's a photo of a functional/custom object** (holder, bracket, case, mount, stand, organizer, etc.):
1. **Note the original frame path** (e.g. `frame_1a589237.jpg`) — you will need it when the annotated image comes back.
2. Send the extracted frame back to the user and ask them to draw on it in red:
   > "Hey! Could you draw in red on this image to show me the shape you have in mind? Any drawing app works — even a quick scribble on your phone. Then send it back and I'll use it as the design reference."
   Use the `message` tool to attach the frame — do NOT use inline MEDIA: syntax:
   `message(text="Hey! Could you draw...", media="<frame_path>")`
3. Wait for the user to send back the annotated image.

**When the user sends back the annotated image:**
Do NOT say "Yes! On it!" and stop — immediately run exec:
```bash
claw3d convert --image <original_frame_path> --annotated-image <annotated_MediaPath> --prompt "<description of the object, NO scene context>" --output model_<ID>.glb
```
- `<original_frame_path>` = the frame you sent them (e.g. `frame_1a589237.jpg`)
- `<annotated_MediaPath>` = the absolute path from the media attached message
- Then run preview + send both files as usual

---

#### Result has `native_mode: false` (Gemini was used) → act on the JSON

```json
{
  "subject": "a wooden phone stand",
  "image_type": "sketch",
  "intent": "create_new",
  "needs_clarification": false,
  "clarification_question": null,
  "suggested_prompt": "a minimalist wooden phone stand with a 70° angled back support..."
}
```

| `intent` | Action |
|---|---|
| `create_new` | Check `needs_clarification` first — if false, then `claw3d convert --image <MediaPath> --prompt "<suggested_prompt>" --output model_<ID>.glb` |
| `create_attachment` | Same as `create_new` |
| `find_existing` | This shouldn't appear here — Primary Gate should have caught it. But if it does: go to `03-directory` module |

If `needs_clarification: true`:
- **First check for replicate/copy intent in the user's description** — if present ("make another one", "copy this", "replicate", etc.), override to `false` and proceed directly regardless of what Gemini returned.
- Otherwise: send `clarification_question` verbatim (Gemini wrote it to be friendly and specific)
- Do NOT rephrase
- After user replies, re-run: `claw3d analyze --input <MediaPath> --description "<original + reply>"`
- After one round, always proceed

---

### When User Sends a VIDEO (CREATE path)

**You should only be here if the Primary Gate resolved to CREATE.**

**Step 1 — Extract the best frame**

Two paths depending on how the video arrived:

**Case A — Video attached as media (you can see the video in this conversation):**
You are a multimodal agent. Analyze the video directly to identify the best frame:
- Subject fully in frame, clear and well-lit
- Best reveals the 3D shape (front 3/4 angle preferred)
- Not blurry, not mid-motion, not transitioning

Pick the exact timestamp (HH:MM:SS), then extract:
```bash
claw3d extract-frame --input <video_path> --timestamp <HH:MM:SS> --output frame_<ID>.jpg
```

**Case B — Only text Description, no media in conversation (OpenClaw pre-processed the video):**
You cannot see the video — you only have the text Description. Do NOT guess a timestamp from text. Use Gemini API for smart frame selection:
```bash
claw3d extract-frame --input <video_path> --output frame_<ID>.jpg
```
(no `--timestamp` → Gemini picks the best frame automatically)

If this fails because no Gemini API key is configured, stop and tell the user:
> "I need a Gemini API key to pick the best frame from your video (the video isn't directly visible to me in this conversation). Please run:
> `claw3d configure analysis --gemini-api-key <YOUR_KEY>`
> You can get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey)."

**Step 2 — Analyze extracted frame:**
```bash
claw3d analyze --input frame_<ID>.jpg --description "<user's message or Gemini description>" --pretty
```
Then follow the IMAGE flow above (including `needs_clarification` checks).

**CRITICAL — Do NOT go silent after frame extraction.** If `needs_clarification: false`, tell the user you're generating the model BEFORE running `claw3d convert`. The full sequence must be:
1. "Great, let me take a look at what you need — give me a moment!" (from earlier)
2. Extract frame + analyze (Steps 1-2)
3. **"Creating your 3D model now — I'll send it when it's ready!"** ← say this BEFORE convert
4. Run `claw3d convert` → `claw3d preview` → send both files

---

## Full Example Flows

**Generic functional object — search first (even if user says "create"):**
```
User: [sends video] "I need you to create a wine stand"
→ Primary Gate: wine stand = common, functional → SEARCH path
→ Go to 03-directory module: search → thumbnails → pick → confirm → download → preview
```

**Video demonstrating a common object — STILL search first:**
```
User: [sends video showing how they'd hold a wine bottle, describing an L-shaped holder]
→ Primary Gate: wine holder = common, functional → SEARCH path (video demo ≠ custom design)
→ Go to 03-directory: search "L-shaped wine bottle holder" → thumbnails → pick
```

**Same object + artistic constraint — create:**
```
User: [sends video + photo of sculpture] "I need a wine stand in the style of this sculpture"
→ Primary Gate: style constraint present → CREATE path
→ claw3d extract-frame → analyze (photo as reference) → convert with prompt + image
```

**Sketch → 3D model (CREATE path):**
```
User: [sends pencil sketch of a bracket]
→ Primary Gate: sketch present → CREATE path
→ claw3d analyze --input sketch.jpg --description "make this"
  (native: sketch → create_new, needs_clarification: false, proceed directly)
→ claw3d convert --image sketch.jpg --prompt "an L-shaped bracket with two mounting holes" --output model_abc.glb
```

**Generic object, user says "I want this" with a photo:**
```
User: [sends photo of a mug] "I want this"
→ Primary Gate: mug = common object → SEARCH path
→ Go to 03-directory: search "mug" → thumbnails → confirm → download → preview
```

**Custom functional object (specific, unlikely to exist):**
```
User: [sends photo of a weird desk edge] "make a phone holder that clips onto this exact edge"
→ Primary Gate: too specific/personal to exist → CREATE path
→ analyze → needs_clarification → ask for sketch on the photo
```

**Video — user asking to find (any wording):**
```
User: [sends video, description: "person asking to find/create a wine stand, demonstrates with bottle"]
→ Primary Gate: wine stand = common functional object → SEARCH path
→ Go to 03-directory module
```

**Search exhausted → fallback to CREATE:**
```
→ 3 searches, 15 thumbnails reviewed, none match
→ "Couldn't find a good match. Want me to generate a custom one with AI?"
User: "yes"
→ If user has a video/photo: use it as reference for CREATE path
→ Extract frame (if video) → analyze → clarification if needed → convert
```

---

## Commands Reference

```bash
# Image intent analysis (outputs JSON)
claw3d analyze --input <image> [--description "text"] [--annotated <image>] [--pretty]

# Video frame extraction
claw3d extract-frame --input <video> [--output frame.jpg] [--timestamp HH:MM:SS]

# Analysis layer configuration
claw3d configure analysis                                 # show status
claw3d configure analysis --mode native                  # use your own AI
claw3d configure analysis --mode auto                    # gemini if available, else native
claw3d configure analysis --mode gemini                  # always use Gemini
claw3d configure analysis --gemini-api-key <KEY>         # set Gemini key
claw3d configure analysis --clear                        # remove Gemini key
```

<!-- /MODULE: intent -->
