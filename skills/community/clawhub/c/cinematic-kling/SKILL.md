---
name: cinematic-kling
description: Generate 5-second cinematic AI videos using Kling via ComfyDeploy. Takes a character image, item image, and location image, then produces a character sheet, item sheet, and a short cinematic video showing them interacting. Use when creating short ads, film clips, music videos, or any scene where a character interacts with an item in a specific location.
---

# Cinematic Kling

Generates a 5-second cinematic video by combining:
- A **character** (person/model)
- An **item** (product, object, prop)
- A **location** (background, environment)

Internally creates a Character Sheet and Item Sheet, then feeds them into Kling for video generation.

---

## Deployment

- **Deployment ID:** `e5258667-dec2-438f-84d0-f22049692483`
- **API:** `POST https://api.comfydeploy.com/api/run/deployment/queue`
- **Auth:** `Authorization: Bearer $COMFY_DEPLOY_API_KEY`

---

## Inputs

| Field | Type | Description |
|-------|------|-------------|
| `character_base` | URL | Public image URL of the character/person |
| `item_base` | URL | Public image URL of the item/product |
| `location_base` | URL | Public image URL of the location/environment |
| `character_sheet_prompt` | String | Character sheet prompt — **only modify the `[brackets]`** |
| `video_prompt` | String | Simple description of the 5-second scene |
| `input_seed` | Integer | `-1` for random, fixed number for reproducible results |

---

## Character Sheet Prompt Structure

The prompt has **two parts** — only the `[brackets]` part changes:

```
Create a photorealistic character sheet. Include a closeup portrait which is left aligned (the outfit must be visible in the portrait), no borders, with a neutral expression and then also include a full view shot that shows the front, right side view, left side view and back of the character. The character is placed on a white background. Don't include any text. No borders, no soft gradients. [CLOTHING DESCRIPTION HERE]
```

**Rule:** Replace `[CLOTHING DESCRIPTION HERE]` with the outfit appropriate for the scene. Everything before the brackets stays exactly as-is.

**Examples:**
- `[They are wearing a tailored black suit with a white shirt, no tie, luxury editorial style.]`
- `[They are wearing dirty damaged clothes in the style of The Last Of Us, dystopic aesthetic.]`
- `[They are wearing a red Nike tracksuit and white sneakers, athletic style.]`

---

## Video Prompt Guidelines

- Keep it **simple** — describe the action/interaction, not every detail
- Mention **character + item + location** implicitly through the action
- You can suggest 1-2 camera cuts within the 5 seconds
- Works for: ads, short films, music videos, product demos, action clips

**Good examples:**
- `"Short cinematic sequence of the character dunking a basketball in the ring while wearing the green Shaq shoes."`
- `"Character walks into the desert location, picks up the item from the sand, holds it toward camera. Quick cut to close-up of the item."`
- `"Product reveal: character turns around in the urban location, tosses the item to camera in slow motion."`

**Bad (too detailed):**
- ❌ `"Camera starts at f/1.8 aperture, golden hour light at 47 degrees, character moves exactly 3 steps forward..."`

---

## Step 0 — Verify Which Image Is Which (MANDATORY)

**ALWAYS use the `image` tool to identify each file before assigning roles. Never assume by order.**

```
image(images=[file1, file2, file3], prompt="Para cada imagen, decí brevemente si es: persona, producto/objeto, o lugar/ambiente")
```

Then assign:
- `character_base` = the **person/model**
- `item_base` = the **product/object** they interact with
- `location_base` = the **place/environment/background**

---

## Step 1 — Upload Images to ComfyDeploy Storage

**ALWAYS upload local files to ComfyDeploy's own storage first. NEVER use external/custom domains.**

```bash
source ~/clawd/.env

upload_to_comfy() {
  curl -s -X POST "https://api.comfydeploy.com/api/file/upload" \
    -H "Authorization: Bearer $COMFY_DEPLOY_API_KEY" \
    -F "file=@$1" | jq -r '.file_url'
}

URL_CHAR=$(upload_to_comfy /path/to/character.jpg)
URL_ITEM=$(upload_to_comfy /path/to/item.jpg)
URL_LOC=$(upload_to_comfy /path/to/location.jpg)
# Returns: https://comfy-deploy-output.s3.us-east-2.amazonaws.com/inputs/img_XXXX.jpg
```

## Step 2 — Submit Run

```bash
RUN_ID=$(curl -s -X POST "https://api.comfydeploy.com/api/run/deployment/queue" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $COMFY_DEPLOY_API_KEY" \
  -d "{
    \"deployment_id\": \"e5258667-dec2-438f-84d0-f22049692483\",
    \"inputs\": {
      \"character_base\": \"$URL_CHAR\",
      \"item_base\": \"$URL_ITEM\",
      \"location_base\": \"$URL_LOC\",
      \"character_sheet_prompt\": \"Create a photorealistic character sheet. Include a closeup portrait which is left aligned (the outfit must be visible in the portrait), no borders, with a neutral expression and then also include a full view shot that shows the front, right side view, left side view and back of the character. The character is placed on a white background. Don't include any text. No borders, no soft gradients. [CLOTHING DESCRIPTION]\",
      \"video_prompt\": \"VIDEO_SCENE_DESCRIPTION\",
      \"input_seed\": -1
    }
  }" | jq -r '.run_id')

echo "Run ID: $RUN_ID"
```

---

## Polling for Results

```bash
while true; do
  RESULT=$(curl -s "https://api.comfydeploy.com/api/run/$RUN_ID" \
    -H "Authorization: Bearer $COMFY_DEPLOY_API_KEY")
  STATUS=$(echo $RESULT | jq -r '.status')
  echo "Status: $STATUS"
  if [ "$STATUS" = "success" ]; then
    echo $RESULT | jq '.outputs'
    break
  elif [ "$STATUS" = "failed" ]; then
    echo "Failed!"
    break
  fi
  sleep 10
done
```

---

## Step 3 — Poll & Download Results

```bash
# Poll until success
while true; do
  RESULT=$(curl -s "https://api.comfydeploy.com/api/run/$RUN_ID" \
    -H "Authorization: Bearer $COMFY_DEPLOY_API_KEY")
  STATUS=$(echo $RESULT | jq -r '.status')
  [ "$STATUS" = "success" ] && break
  [ "$STATUS" = "failed" ] && echo "FAILED" && break
  sleep 15
done

# Download outputs to allowed directory
mkdir -p ~/clawd/output/cinematic-kling
BASE_URL="https://comfy-deploy-output.s3.us-east-2.amazonaws.com/outputs/runs/$RUN_ID"
curl -sL "$BASE_URL/CS_2_00001_.png" -o ~/clawd/output/cinematic-kling/character-sheet.png
curl -sL "$BASE_URL/ITEM_00001_.png" -o ~/clawd/output/cinematic-kling/item-sheet.png
curl -sL "$BASE_URL/LOCATION_00001_.png" -o ~/clawd/output/cinematic-kling/location-sheet.png
curl -sL "$BASE_URL/ComfyUI_00001_.mp4" -o ~/clawd/output/cinematic-kling/video.mp4
```

## Step 4 — Send Results as Files

**ALWAYS send as file attachments using filePath — NEVER send raw URLs.**

```
message(action=send, channel=telegram, target=USER_ID, filePath=~/clawd/output/cinematic-kling/character-sheet.png, message="Character Sheet")
message(action=send, channel=telegram, target=USER_ID, filePath=~/clawd/output/cinematic-kling/item-sheet.png, message="Item Sheet")
message(action=send, channel=telegram, target=USER_ID, filePath=~/clawd/output/cinematic-kling/location-sheet.png, message="Location Sheet")
message(action=send, channel=telegram, target=USER_ID, filePath=~/clawd/output/cinematic-kling/video.mp4, message="🎬 Video")
```

## Output Structure

| Node | File | Action |
|------|------|--------|
| 4 | `CS_2_00001_.png` | Send as file (Character Sheet) |
| 14 | `ITEM_00001_.png` | Send as file (Item Sheet) |
| 25 | `LOCATION_00001_.png` | Send as file (Location Sheet) |
| 22 | `ComfyUI_00001_.mp4` | **Send as file — main output** |
| 38 | text | Internal video prompt used by Kling (ignore) |

---

## Python Helper

```python
import requests, os, time

def cinematic_kling(character_url, item_url, location_url, clothing_desc, video_prompt, seed=-1):
    """
    character_url: public URL of character image
    item_url: public URL of item image
    location_url: public URL of location image
    clothing_desc: description for [brackets] in character sheet prompt
    video_prompt: simple scene description
    Returns: dict with 'images' list and 'video' URL
    """
    API_KEY = os.environ['COMFY_DEPLOY_API_KEY']
    
    character_sheet_prompt = (
        "Create a photorealistic character sheet. Include a closeup portrait which is left aligned "
        "(the outfit must be visible in the portrait), no borders, with a neutral expression and then "
        "also include a full view shot that shows the front, right side view, left side view and back "
        "of the character. The character is placed on a white background. Don't include any text. "
        f"No borders, no soft gradients. [{clothing_desc}]"
    )
    
    # Submit job
    r = requests.post(
        "https://api.comfydeploy.com/api/run/deployment/queue",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
        json={
            "deployment_id": "e5258667-dec2-438f-84d0-f22049692483",
            "inputs": {
                "character_base": character_url,
                "item_base": item_url,
                "location_base": location_url,
                "character_sheet_prompt": character_sheet_prompt,
                "video_prompt": video_prompt,
                "input_seed": seed
            }
        }
    )
    run_id = r.json()['run_id']
    print(f"Run ID: {run_id}")
    
    # Poll
    while True:
        result = requests.get(
            f"https://api.comfydeploy.com/api/run/{run_id}",
            headers={"Authorization": f"Bearer {API_KEY}"}
        ).json()
        status = result.get('status')
        print(f"Status: {status}")
        if status == 'success':
            return result.get('outputs', {})
        elif status == 'failed':
            raise Exception(f"Run failed: {result}")
        time.sleep(10)
```

---

## Typical Run Time

~3–5 minutes (character sheet generation + Kling video generation)

---

## Use Cases

- **Product ads:** character using/wearing the item in a branded location
- **Short films:** character interacting with a prop in a cinematic environment
- **Music videos:** artist + instrument/prop + stage/location
- **Fashion:** model wearing clothing item in a specific setting
- **Gaming/dystopian:** character in Last-of-Us style with game item in post-apocalyptic location

---

## Notes

- The `character_sheet_prompt` fixed portion must never be modified — only the `[brackets]`
- `input_seed: -1` = random each time; set a fixed integer to reproduce results
- 5 seconds is the fixed video length
- Outputs come from ComfyDeploy's built-in S3 storage — no manual upload needed
