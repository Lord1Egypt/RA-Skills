import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const DEFAULT_MODEL = "whisper-1";
const API_BASE = process.env.CRAZYROUTER_BASE_URL || "https://crazyrouter.com/v1";

function parseArgs(argv) {
  const args = { input: null, output: null, language: null, translate: false, model: DEFAULT_MODEL };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case "--input": case "-i": args.input = argv[++i]; break;
      case "--output": case "-o": args.output = argv[++i]; break;
      case "--language": case "-l": args.language = argv[++i]; break;
      case "--translate": args.translate = true; break;
      case "--model": case "-m": args.model = argv[++i]; break;
      case "--help": case "-h":
        console.log(`Usage: main.mjs --input audio.mp3 [--output transcript.txt] [--language en] [--translate]
Formats: mp3, mp4, mpeg, mpga, m4a, wav, webm
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

async function transcribe(args) {
  if (!args.input) { console.error("Error: --input required"); process.exit(1); }
  const apiKey = getApiKey();
  const fileBuffer = await readFile(args.input);
  const fileName = path.basename(args.input);
  console.error(`Transcribing: ${fileName} (${(fileBuffer.length / 1024).toFixed(1)}KB)`);
  console.error(`Model: ${args.model}${args.translate ? " (translate to English)" : ""}`);
  const endpoint = args.translate ? "translations" : "transcriptions";
  const formData = new FormData();
  formData.append("file", new Blob([fileBuffer]), fileName);
  formData.append("model", args.model);
  if (args.language) formData.append("language", args.language);
  const response = await fetch(`${API_BASE}/audio/${endpoint}`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${apiKey}` },
    body: formData,
  });
  if (!response.ok) { console.error(`API Error (${response.status}): ${await response.text()}`); process.exit(1); }
  const result = await response.json();
  const text = result.text ?? "";
  if (args.output) {
    await writeFile(args.output, text);
    console.error(`Saved to ${args.output} (${text.length} chars)`);
  } else {
    console.log(text);
  }
}

const args = parseArgs(process.argv);
transcribe(args).catch((err) => { console.error(`Error: ${err.message}`); process.exit(1); });
