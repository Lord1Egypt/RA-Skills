---
name: ernie-image-visual-promptsmith
description: Generate ERNIE-Image-Turbo images through Baidu AI Studio and craft ERNIE-Image prompts for posters, comics, infographics, ecommerce images, UI-style visuals, bilingual text rendering, structured layouts, negative prompts, generation settings, and use_pe decisions. Requires a user-provided AI Studio API key and is not an official Baidu skill.
metadata:
  openclaw:
    emoji: "\U0001F3A8"
    skillKey: "ernie-image-visual-promptsmith"
    homepage: "https://aistudio.baidu.com/account/accessToken"
    requires:
      env:
        - BAIDU_AISTUDIO_API_KEY
      anyBins:
        - python3
        - python
        - py
    primaryEnv: BAIDU_AISTUDIO_API_KEY
---

# ERNIE-Image Visual Promptsmith

Use this community skill to craft ERNIE-Image prompts and generate images through the AI Studio ERNIE-Image-Turbo endpoint. It is not official Baidu or ERNIE-Image software.

## Decide the Mode

- Generate immediately when the user asks to generate, draw, create, make an image, or uses equivalent Chinese generation wording.
- Return prompt-only guidance when the user asks to optimize, rewrite, improve, or review a prompt.
- Ask one concise question only if an exact visible text string, language, or required aspect ratio is missing and guessing would likely break the result.

## API Endpoint

- Base: `https://aistudio.baidu.com/llm/lmapi/v3`
- Submit: `POST /images/generations`
- Full URL: `https://aistudio.baidu.com/llm/lmapi/v3/images/generations`
- Auth header: `Authorization: bearer <BAIDU_AISTUDIO_API_KEY>`
- Platform header: `X-Client-Platform: aistudio`

## API Key

- Required environment variable: `BAIDU_AISTUDIO_API_KEY`
- Get a key: `https://aistudio.baidu.com/account/accessToken`
- If the key is missing, do not call the API. Tell the user to set `BAIDU_AISTUDIO_API_KEY`.

## Triggers

- Chinese examples: `ERNIE image: <prompt>`, `Wenxin image: <prompt>`, `generate image: <prompt>`, or equivalent Chinese wording for image generation.
- English examples: `ernie image: <prompt>`, `generate image: <prompt>`, `create image: <prompt>`.
- Treat text after the colon as the raw user prompt, improve it, choose a preset, then generate.
- If the user asks to optimize, rewrite, improve, or review a prompt, return prompt-only guidance and do not call the API.

## Prompt Workflow

1. Classify the image style: photorealistic, anime/manga, text-in-image, concept art, abstract/artistic, layout/composition, poster, ecommerce, infographic, comic/storyboard, UI screenshot style, or character-consistent visual.
2. Preserve immutable constraints: exact in-image text, language, subject count, character identity, spatial relationships, size, style, and forbidden elements.
3. Build the core prompt in five parts: subject -> action/context -> style -> lighting -> quality.
4. For layout-sensitive requests, append composition -> exact text -> spatial placement.
5. Keep in-image writing short when possible. Turn paragraphs into titles, labels, badges, or numbered lines.
6. For text rendering, put exact wording in quotes and specify placement, font weight, alignment, color, background contrast, and whitespace.
7. Choose a preset from `auto`, `text-poster`, `infographic`, `comic`, `product`, `ui`, `photo`, `concept`, or `abstract`.
8. Before generation, state:

```markdown
Final Prompt: <prompt>
Preset: <preset>
use_pe: <true or false>
Size: <size>
Reason: <why these settings fit ERNIE-Image>
```

## Generation Workflow

Use the bundled Python script. Prefer `python3`; on Windows use `python` or `py` if needed.

```bash
python3 {baseDir}/scripts/generate.py --prompt "<FINAL_PROMPT>" --preset <preset>
```

For exact text, bilingual labels, UI, flowcharts, signs, comics, or already detailed prompts, pass `--no-use-pe`.

```bash
python3 {baseDir}/scripts/generate.py --prompt "<FINAL_PROMPT>" --preset text-poster --no-use-pe
```

The script prints `IMAGE_URL:<url>` for URL responses and `MEDIA:<absolute_path>` for each saved image. Return the saved media path to the user.

If `BAIDU_AISTUDIO_API_KEY` is missing, tell the user to get a key from `https://aistudio.baidu.com/account/accessToken` and set `BAIDU_AISTUDIO_API_KEY`.

## Submit Payload

```json
{
  "model": "ERNIE-Image-Turbo",
  "prompt": "<FINAL_PROMPT>",
  "n": 1,
  "response_format": "url",
  "size": "1024x1024",
  "seed": 42,
  "use_pe": true,
  "num_inference_steps": 8,
  "guidance_scale": 1.0
}
```

## Download and Output

- `response_format=url` returns image URLs in `data[]`; the script prints `IMAGE_URL:<url>`.
- The script downloads each URL immediately and saves the image locally.
- The script prints `MEDIA:<absolute_path>` for OpenClaw/ClawHub auto-attach.
- URLs may expire; the local file remains available after download.
- Output names are generated as `ernie-image-<timestamp>-<index>.<ext>`.
- Do not pass user-controlled filenames to shell commands.

## Defaults

- Model: `ERNIE-Image-Turbo`
- Preset: `auto`
- Count: `1`
- Response format: `url`
- Seed: `42`
- `text-poster`, `infographic`, `comic`, `product`, and `ui` presets default to `use_pe=false`.
- `photo`, `concept`, and `abstract` presets default to `use_pe=true`.

## Negative Prompt Rules

- Do not add `text`, `letters`, `typography`, `Chinese text`, or `English text` when the user wants readable writing.
- Prefer precise negatives: distorted text, misspelled words, duplicated letters, unreadable typography, warped layout, cropped title, low contrast, blurry details, inconsistent panels, artifacts.
- The API does not expose a separate negative prompt field in this skill. Express exclusions as natural language constraints inside the prompt, such as "avoid cluttered background" or "no visible watermark".

## Retry Strategy

- Text errors: reduce the amount of visible text, quote exact words once, add stronger placement and contrast, then use `--no-use-pe`.
- Layout errors: simplify object count, name each region, use grid/split-screen/foreground/background terms, then keep the same seed.
- Weak style: add camera/lens, art movement, medium, color temperature, material texture, and lighting direction.
- Cluttered image: remove secondary elements, add negative space, use "avoid cluttered background", and switch to a simpler preset if needed.

## References

- Read `references/api.md` for parameters, command examples, and endpoint mapping.
- Read `references/prompt-architecture.md` for ERNIE-Image prompt templates.
- Read `references/examples.md` for acceptance-style examples.
