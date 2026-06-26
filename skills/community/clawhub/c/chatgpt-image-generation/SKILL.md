---
name: chatgpt-image-generation
description: Generate images from ChatGPT using Playwright browser automation. Opens ChatGPT, sends prompts, waits for generation, and saves the resulting images.
---

# ChatGPT Image Generation Skill

Use Playwright to automate ChatGPT web UI for image generation.

## Prerequisites

```bash
npm install playwright
npx playwright install chromium
```

## Usage

```bash
# Generate images from prompts file
node generate.js --prompts prompts.json --output ./images

# Resume from a specific index
node generate.js --prompts prompts.json --output ./images --start 5

# Run in headless mode
node generate.js --prompts prompts.json --output ./images --headless
```

## Prompt File Format

```json
["prompt 1", "prompt 2"]
```

or

```json
{ "prompts": ["prompt 1", "prompt 2"] }
```

## How It Works

1. Opens ChatGPT in a Chrome browser
2. Sends each prompt from the prompts file
3. Waits for the response to be generated
4. Finds the generated image in the page
5. Saves the image to the output directory
6. Repeats for all prompts

## Output

- Numbered image files: `001.png`, `002.png`, etc.
- `results.jsonl` — log of results per prompt

## Login (One-Time)

If not logged into ChatGPT:
1. Run the script (browser will open visible)
2. Sign into ChatGPT 
3. Session is saved for future runs
