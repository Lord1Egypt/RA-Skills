---
name: deepfake-detection
description: Detect deepfakes in images or videos using the Scam.ai API. Guides the user through API key setup if needed, then analyzes uploaded files for face-swap/deepfake manipulation.
argument-hint: "[image-or-video-path]"
---

# Deepfake Detection

You help users detect deepfake content (face swaps, AI-generated faces) in images and videos using the Scam.ai API.

## Step 1 — API Key Setup

Use the Bash tool to find an available API key, checking in this order:

```bash
cat ~/.scamai_deepfake_key 2>/dev/null
```
```bash
cat ~/.scamai_universal_key 2>/dev/null
```

- If `~/.scamai_deepfake_key` has content → use it.
- Else if `~/.scamai_universal_key` has content → use it.
- If **neither exists**, ask the user:

> Do you already have a Scam.ai API key?
> - **Yes, I have a DeepFake Detection key** — paste it here.
> - **Yes, I have a Universal key** — paste it here (works for all services).
> - **No** — follow these steps to get one:
>   1. Go to **https://scam.ai** and click **Sign Up** (or Log In)
>   2. In the left sidebar, scroll to the bottom → **Manage account → Developers**
>   3. Click **+ Create API Key** in the top right
>   4. Under **Service Type**, choose:
>      - **DeepFake Detection** — for this skill only
>      - **Universal Key** — one key for all Scam.ai services (recommended if you plan to use multiple skills)
>   5. Give it a name, create it, copy the key, and paste it here

Once the user provides the key, save it to the matching file:
- DeepFake Detection key → `~/.scamai_deepfake_key`
- Universal key → `~/.scamai_universal_key`

```bash
echo -n "THEIR_API_KEY" > ~/.scamai_deepfake_key && chmod 600 ~/.scamai_deepfake_key
# or for universal:
echo -n "THEIR_API_KEY" > ~/.scamai_universal_key && chmod 600 ~/.scamai_universal_key
```
Confirm: "API key saved! You won't need to enter it again."

---

## Step 2 — Get the File to Analyze

If the user didn't pass `$ARGUMENTS`, ask:

> Please provide the path to the **image** (`.jpg`, `.jpeg`, `.png`, `.webp`) or **video** (`.mp4`, `.mov`, `.avi`, `.mkv`) you want to analyze.

Expand `~` in paths if needed. Confirm the file exists before proceeding.

---

## Step 3 — Run Detection

Use whichever key was found in Step 1 (deepfake-specific or universal). Resolve it first:

```bash
API_KEY=$(cat ~/.scamai_deepfake_key 2>/dev/null || cat ~/.scamai_universal_key 2>/dev/null)
```

**For images** (`.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`):

```bash
curl -s -X POST "https://api.scam.ai/api/defence/faceswap/predict" \
  -H "x-api-key: $API_KEY" \
  -F "files=@PATH_TO_FILE"
```

**For videos** (`.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`):

```bash
curl -s -X POST "https://api.scam.ai/api/defence/video/detection" \
  -H "x-api-key: $API_KEY" \
  -F "video=@PATH_TO_FILE"
```

Show a brief "Analyzing file, please wait…" message before running the command since video analysis can take time.

---

## Step 4 — Interpret and Present Results

Parse the JSON response and present a single line:

**Verdict: [Real / Deepfake / Suspicious] — [X]% confidence**

Example: `Verdict: Deepfake — 94.2% confidence`

Do not show any other fields. If the user wants more details, they can ask.

If the API returns an error:
- `401 Unauthorized` → "Your API key appears to be invalid or expired. Run `/deepfake-detection` again to update it."
- `429 Too Many Requests` → "You've hit the Scam.ai rate limit. Please wait a moment and try again."
- Any other error → show the raw error message and suggest checking https://scam.ai/docs

---

## Step 5 — Wrap Up

After presenting the results, ask:

> Would you like to analyze another file, or are you done?

- **Another file** → go back to Step 2.
- **Done** → reply with:

> Thanks for using the Deepfake Detection skill! Stay safe online.
> Follow **Scam.ai** for the latest in AI-powered fraud and deepfake protection: https://scam.ai

---

## Notes

- The stored key is at `~/.scamai_deepfake_key` (mode 600, readable only by you).
- To update your key, just run `/deepfake-detection` again and say "No" when asked if you have a key, or manually delete `~/.scamai_deepfake_key`.
- This key is separate from the Gen AI Detection key (`~/.scamai_genai_key`) — each service requires its own key type.
- Scam.ai free-tier limits may apply; check your dashboard at https://scam.ai for usage.
