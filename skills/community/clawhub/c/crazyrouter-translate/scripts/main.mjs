import { readFile, writeFile } from "node:fs/promises";
import process from "node:process";

const DEFAULT_MODEL = "gpt-4o-mini";
const API_BASE = process.env.CRAZYROUTER_BASE_URL || "https://crazyrouter.com/v1";

function parseArgs(argv) {
  const args = { text: null, inputFile: null, output: null, from: null, to: null, model: DEFAULT_MODEL, format: "plain" };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case "--text": case "-t": args.text = argv[++i]; break;
      case "--input": case "-i": args.inputFile = argv[++i]; break;
      case "--output": case "-o": args.output = argv[++i]; break;
      case "--from": args.from = argv[++i]; break;
      case "--to": args.to = argv[++i]; break;
      case "--model": case "-m": args.model = argv[++i]; break;
      case "--format": args.format = argv[++i]; break;
      case "--help": case "-h":
        console.log(`Usage: main.mjs --text "..." --to <lang> [--from <lang>] [--model gpt-4o-mini] [--output file]
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

async function translate(args) {
  let text = args.text;
  if (!text && args.inputFile) {
    text = await readFile(args.inputFile, "utf-8");
    console.error(`Read ${text.length} characters from ${args.inputFile}`);
  }
  if (!text) { console.error("Error: --text or --input required"); process.exit(1); }
  if (!args.to) { console.error("Error: --to <language> required"); process.exit(1); }
  const apiKey = getApiKey();
  const fromHint = args.from ? `from ${args.from} ` : "";
  const formatHint = args.format === "markdown" ? " Preserve all Markdown formatting." : "";
  const systemPrompt = `You are a professional translator. Translate the following text ${fromHint}to ${args.to}. Output ONLY the translated text, nothing else.${formatHint}`;
  console.error(`Model: ${args.model} | ${args.from || "auto"} -> ${args.to}`);
  const response = await fetch(`${API_BASE}/chat/completions`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${apiKey}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      model: args.model,
      messages: [{ role: "system", content: systemPrompt }, { role: "user", content: text }],
      temperature: 0.3,
    }),
  });
  if (!response.ok) { console.error(`API Error (${response.status}): ${await response.text()}`); process.exit(1); }
  const result = await response.json();
  const translated = result.choices?.[0]?.message?.content ?? "";
  if (args.output) {
    await writeFile(args.output, translated);
    console.error(`Saved to ${args.output}`);
  } else {
    console.log(translated);
  }
  if (result.usage) console.error(`${result.usage.total_tokens} tokens`);
}

const args = parseArgs(process.argv);
translate(args).catch((err) => { console.error(`Error: ${err.message}`); process.exit(1); });
