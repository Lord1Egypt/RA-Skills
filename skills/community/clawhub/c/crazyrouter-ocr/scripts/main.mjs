import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const DEFAULT_MODEL = "gpt-4o";
const DEFAULT_PROMPT = "Describe this image in detail";
const API_BASE = process.env.CRAZYROUTER_BASE_URL || "https://crazyrouter.com/v1";

function parseArgs(argv) {
  const args = { image: null, prompt: DEFAULT_PROMPT, model: DEFAULT_MODEL, output: null };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case "--image": case "-i": args.image = argv[++i]; break;
      case "--prompt": case "-p": args.prompt = argv[++i]; break;
      case "--model": case "-m": args.model = argv[++i]; break;
      case "--output": case "-o": args.output = argv[++i]; break;
      case "--help": case "-h":
        console.log(`Usage: main.mjs --image photo.jpg [--prompt "Describe this"] [--model gpt-4o] [--output text.md]
Models: gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-3-pro, claude-sonnet-4
Env: CRAZYROUTER_API_KEY (required)`);
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

function getMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const types = { ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp" };
  return types[ext] || "image/png";
}

async function analyze(args) {
  if (!args.image) { console.error("Error: --image required"); process.exit(1); }
  const apiKey = getApiKey();
  const imageBuffer = await readFile(args.image);
  const mimeType = getMimeType(args.image);
  const base64 = imageBuffer.toString("base64");
  console.error(`Image: ${path.basename(args.image)} (${(imageBuffer.length / 1024).toFixed(1)}KB)`);
  console.error(`Model: ${args.model}`);
  const response = await fetch(`${API_BASE}/chat/completions`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${apiKey}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      model: args.model,
      messages: [{ role: "user", content: [
        { type: "text", text: args.prompt },
        { type: "image_url", image_url: { url: `data:${mimeType};base64,${base64}` } },
      ]}],
      max_tokens: 4096,
    }),
  });
  if (!response.ok) { console.error(`API Error (${response.status}): ${await response.text()}`); process.exit(1); }
  const result = await response.json();
  const text = result.choices?.[0]?.message?.content ?? "";
  if (args.output) {
    await writeFile(args.output, text);
    console.error(`Saved to ${args.output}`);
  } else {
    console.log(text);
  }
  if (result.usage) console.error(`${result.usage.total_tokens} tokens`);
}

const args = parseArgs(process.argv);
analyze(args).catch((err) => { console.error(`Error: ${err.message}`); process.exit(1); });
