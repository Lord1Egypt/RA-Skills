import { readFile, writeFile } from "node:fs/promises";
import process from "node:process";

const DEFAULT_MODEL = "tts-1";
const DEFAULT_VOICE = "alloy";
const DEFAULT_FORMAT = "mp3";
const API_BASE = process.env.CRAZYROUTER_BASE_URL || "https://crazyrouter.com/v1";

function parseArgs(argv) {
  const args = { text: null, inputFile: null, output: null, voice: DEFAULT_VOICE, model: DEFAULT_MODEL, speed: 1.0, format: DEFAULT_FORMAT };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case "--text": case "-t": args.text = argv[++i]; break;
      case "--input": case "-i": args.inputFile = argv[++i]; break;
      case "--output": case "-o": args.output = argv[++i]; break;
      case "--voice": case "-v": args.voice = argv[++i]; break;
      case "--model": case "-m": args.model = argv[++i]; break;
      case "--speed": args.speed = parseFloat(argv[++i]); break;
      case "--format": args.format = argv[++i]; break;
      case "--help": case "-h":
        console.log(`Usage: main.mjs --text "..." --output audio.mp3 [--voice alloy] [--model tts-1] [--speed 1.0] [--format mp3]
Voices: alloy, echo, fable, onyx, nova, shimmer
Models: tts-1, tts-1-hd, gpt-4o-mini-tts
Formats: mp3, opus, aac, flac
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

async function tts(args) {
  let text = args.text;
  if (!text && args.inputFile) {
    text = await readFile(args.inputFile, "utf-8");
    console.error(`Read ${text.length} characters from ${args.inputFile}`);
  }
  if (!text) { console.error("Error: --text or --input is required"); process.exit(1); }
  if (!args.output) { console.error("Error: --output is required"); process.exit(1); }
  const apiKey = getApiKey();
  console.error(`Model: ${args.model}, Voice: ${args.voice}, Speed: ${args.speed}x`);
  const response = await fetch(`${API_BASE}/audio/speech`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${apiKey}`, "Content-Type": "application/json" },
    body: JSON.stringify({ model: args.model, input: text, voice: args.voice, speed: args.speed, response_format: args.format }),
  });
  if (!response.ok) { console.error(`API Error (${response.status}): ${await response.text()}`); process.exit(1); }
  const buffer = Buffer.from(await response.arrayBuffer());
  await writeFile(args.output, buffer);
  console.log(`Saved: ${args.output} (${(buffer.length / 1024).toFixed(1)}KB)`);
}

const args = parseArgs(process.argv);
tts(args).catch((err) => { console.error(`Error: ${err.message}`); process.exit(1); });
