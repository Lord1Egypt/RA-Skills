import { writeFile } from "node:fs/promises";
import process from "node:process";

const DEFAULT_MODEL = "sora-2";
const API_BASE = process.env.CRAZYROUTER_BASE_URL || "https://crazyrouter.com/v1";

function parseArgs(argv) {
  const args = { prompt: null, output: null, model: DEFAULT_MODEL };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case "--prompt": case "-p": args.prompt = argv[++i]; break;
      case "--output": case "-o": args.output = argv[++i]; break;
      case "--model": case "-m": args.model = argv[++i]; break;
      case "--help": case "-h":
        console.log(`Usage: main.mjs --prompt "..." --output video.mp4 [--model sora-2]
Models: sora-2, kling-v2-1, veo3, doubao-seedance-1-5-pro_720p, pika-1.5, MiniMax-Hailuo-2.3, runway-vip-video
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

async function generateVideo(args) {
  if (!args.prompt) { console.error("Error: --prompt required"); process.exit(1); }
  if (!args.output) { console.error("Error: --output required"); process.exit(1); }
  const apiKey = getApiKey();
  console.error(`Model: ${args.model}`);
  console.error(`Generating video... (this may take 30-120 seconds)`);
  const response = await fetch(`${API_BASE}/chat/completions`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${apiKey}`, "Content-Type": "application/json" },
    body: JSON.stringify({ model: args.model, messages: [{ role: "user", content: args.prompt }] }),
  });
  if (!response.ok) { console.error(`API Error (${response.status}): ${await response.text()}`); process.exit(1); }
  const result = await response.json();
  const content = result.choices?.[0]?.message?.content ?? "";
  const videoUrl = result.video_url;
  const urlMatch = content.match(/https?:\/\/[^\s"']+\.(mp4|webm|mov)[^\s"']*/i)
    || content.match(/https?:\/\/[^\s"']+video[^\s"']*/i)
    || (videoUrl ? [videoUrl] : null);
  if (urlMatch) {
    const url = urlMatch[0] || urlMatch[1];
    console.error(`Downloading video from: ${url}`);
    const videoResponse = await fetch(url);
    if (videoResponse.ok) {
      const buffer = Buffer.from(await videoResponse.arrayBuffer());
      await writeFile(args.output, buffer);
      console.log(`Saved: ${args.output} (${(buffer.length / 1024 / 1024).toFixed(1)}MB)`);
    } else {
      console.error(`Failed to download video: ${videoResponse.status}`);
      console.log(`Video URL: ${url}`);
    }
  } else {
    console.log(content || "(empty response)");
    if (content.includes("task") || content.includes("id")) {
      console.error("Note: Video may be processing asynchronously.");
    }
  }
}

const args = parseArgs(process.argv);
generateVideo(args).catch((err) => { console.error(`Error: ${err.message}`); process.exit(1); });
