import { writeFile } from "node:fs/promises";
import process from "node:process";

const DEFAULT_MODEL = "suno_music";
const API_BASE = process.env.CRAZYROUTER_BASE_URL || "https://crazyrouter.com/v1";

function parseArgs(argv) {
  const args = { prompt: null, output: null, lyrics: null, title: null, model: DEFAULT_MODEL };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case "--prompt": case "-p": args.prompt = argv[++i]; break;
      case "--output": case "-o": args.output = argv[++i]; break;
      case "--lyrics": case "-l": args.lyrics = argv[++i]; break;
      case "--title": case "-t": args.title = argv[++i]; break;
      case "--model": case "-m": args.model = argv[++i]; break;
      case "--help": case "-h":
        console.log(`Usage: main.mjs --prompt "music description" --output song.mp3 [--lyrics "..."] [--title "..."]
Models: suno_music, suno-v3
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

async function generateMusic(args) {
  if (!args.prompt) { console.error("Error: --prompt required"); process.exit(1); }
  const apiKey = getApiKey();
  console.error(`Model: ${args.model}`);
  console.error(`Generating music... (this may take 30-120 seconds)`);
  const userContent = [args.prompt, args.lyrics ? `\nLyrics:\n${args.lyrics}` : "", args.title ? `\nTitle: ${args.title}` : ""].join("");
  const response = await fetch(`${API_BASE}/chat/completions`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${apiKey}`, "Content-Type": "application/json" },
    body: JSON.stringify({ model: args.model, messages: [{ role: "user", content: userContent }] }),
  });
  if (!response.ok) { console.error(`API Error (${response.status}): ${await response.text()}`); process.exit(1); }
  const result = await response.json();
  const content = result.choices?.[0]?.message?.content ?? "";
  const audioUrl = result.audio_url;
  const urlMatch = content.match(/https?:\/\/[^\s"'<>]+\.(mp3|wav|m4a|ogg|flac)[^\s"'<>]*/i)
    || content.match(/https?:\/\/[^\s"'<>]+audio[^\s"'<>]*/i)
    || (audioUrl ? [audioUrl] : null);
  if (urlMatch && args.output) {
    const url = urlMatch[0];
    console.error(`Downloading audio from: ${url}`);
    const audioResponse = await fetch(url);
    if (audioResponse.ok) {
      const buffer = Buffer.from(await audioResponse.arrayBuffer());
      await writeFile(args.output, buffer);
      console.error(`Saved: ${args.output} (${(buffer.length / 1024 / 1024).toFixed(1)}MB)`);
    } else {
      console.error(`Failed to download: ${audioResponse.status}`);
      console.log(`Audio URL: ${url}`);
    }
  } else {
    console.log(content || "(empty response)");
    if (urlMatch) console.log(`Audio URL: ${urlMatch[0]}`);
  }
}

const args = parseArgs(process.argv);
generateMusic(args).catch((err) => { console.error(`Error: ${err.message}`); process.exit(1); });
