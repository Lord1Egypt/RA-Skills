import { writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const DEFAULT_MODEL = "dall-e-3";
const DEFAULT_SIZE = "1024x1024";
const API_BASE = process.env.CRAZYROUTER_BASE_URL || "https://crazyrouter.com/v1";

function parseArgs(argv) {
  const args = { prompt: null, imagePath: null, model: DEFAULT_MODEL, size: DEFAULT_SIZE, n: 1, quality: "standard" };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case "--prompt": case "-p": args.prompt = argv[++i]; break;
      case "--image": args.imagePath = argv[++i]; break;
      case "--model": case "-m": args.model = argv[++i]; break;
      case "--size": args.size = argv[++i]; break;
      case "--n": args.n = parseInt(argv[++i], 10) || 1; break;
      case "--quality": args.quality = argv[++i]; break;
      case "--help": case "-h":
        console.log(`Usage: main.mjs --prompt "..." --image output.png [--model dall-e-3] [--size 1024x1024] [--n 1] [--quality standard]
Models: dall-e-3, midjourney, flux-pro-1.1-ultra, flux-kontext-pro, sd3.5-large, imagen-4.0-generate-001
Env: CRAZYROUTER_API_KEY (required), CRAZYROUTER_BASE_URL (optional)`);
        process.exit(0);
    }
  }
  return args;
}

function getApiKey() {
  const key = process.env.CRAZYROUTER_API_KEY;
  if (!key) { console.error("Error: CRAZYROUTER_API_KEY not set. Get your key at https://crazyrouter.com"); process.exit(1); }
  return key;
}

async function generateImage(args) {
  if (!args.prompt) { console.error("Error: --prompt is required"); process.exit(1); }
  if (!args.imagePath) { console.error("Error: --image is required"); process.exit(1); }
  const apiKey = getApiKey();
  console.log(`Generating image with ${args.model}...`);
  const body = { model: args.model, prompt: args.prompt, size: args.size, n: args.n };
  if (args.quality !== "standard") body.quality = args.quality;
  const response = await fetch(`${API_BASE}/images/generations`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${apiKey}`, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) { console.error(`API Error (${response.status}): ${await response.text()}`); process.exit(1); }
  const result = await response.json();
  if (!result.data || result.data.length === 0) { console.error("No images returned"); process.exit(1); }
  for (let i = 0; i < result.data.length; i++) {
    const img = result.data[i];
    const outputPath = args.n > 1 ? args.imagePath.replace(/(\.\w+)$/, `_${i + 1}$1`) : args.imagePath;
    if (img.url) {
      const imgResponse = await fetch(img.url);
      if (!imgResponse.ok) { console.error(`Failed to download image: ${imgResponse.status}`); continue; }
      const buffer = Buffer.from(await imgResponse.arrayBuffer());
      await writeFile(outputPath, buffer);
      console.log(`Saved: ${outputPath} (${(buffer.length / 1024).toFixed(1)}KB)`);
    } else if (img.b64_json) {
      const buffer = Buffer.from(img.b64_json, "base64");
      await writeFile(outputPath, buffer);
      console.log(`Saved: ${outputPath} (${(buffer.length / 1024).toFixed(1)}KB)`);
    }
    if (img.revised_prompt) console.log(`Revised prompt: ${img.revised_prompt}`);
  }
}

const args = parseArgs(process.argv);
generateImage(args).catch((err) => { console.error(`Error: ${err.message}`); process.exit(1); });
