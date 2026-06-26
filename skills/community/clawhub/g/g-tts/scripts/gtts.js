#!/usr/bin/env node

/**
 * gtts.js — Google Chirp 3 HD TTS Tool (Node.js)
 * Runs directly from the skill folder — no PATH setup or global installs needed.
 *
 * Usage:
 *   node gtts.js --text "Hello world" --voice Aoede --out output.mp3
 *
 * Dependency (auto-installed by SKILL.md agent logic):
 *   npm install @google-cloud/text-to-speech --prefix <skill_dir>
 */

const path = require("path");
const fs = require("fs");

// 1. Validate Node Version (Google Cloud SDK requires 18+)
const majorVersion = parseInt(process.versions.node.split('.')[0], 10);
if (majorVersion < 18) {
  console.error("ERROR: This skill requires Node.js 18 or higher.");
  process.exit(1);
}

// 2. Configuration & Workspace
const DEFAULT_WORKSPACE = process.env.OPENCLAW_WORKSPACE || process.cwd();

// Load from local node_modules inside the skill folder — no global install needed
const SKILL_DIR = __dirname;
const LOCAL_MODULE = path.join(SKILL_DIR, "node_modules", "@google-cloud", "text-to-speech");

let textToSpeech;
try {
  textToSpeech = require(LOCAL_MODULE);
} catch (e) {
  console.error(
    "ERROR: Required dependency '@google-cloud/text-to-speech' not found.\n" +
    `The agent should have run: npm install --prefix "${SKILL_DIR}"`
  );
  process.exit(1);
}

// =========================================================
// ARGUMENT PARSING
// =========================================================
function parseArgs() {
  const args = process.argv.slice(2);
  const result = { text: null, voice: "Aoede", out: "output.mp3" };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--text" && args[i + 1]) result.text = args[++i];
    else if (args[i] === "--voice" && args[i + 1]) result.voice = args[++i];
    else if (args[i] === "--out" && args[i + 1]) result.out = args[++i];
  }

  if (!result.text) {
    console.error("ERROR: --text argument is required.");
    process.exit(1);
  }

  return result;
}

// =========================================================
// PAUSE TAG → SSML CONVERSION
// =========================================================
function convertPausesToSSML(text) {
  text = text.replace(/\[pause short\]/g, '<break time="300ms"/>');
  text = text.replace(/\[pause long\]/g, '<break time="900ms"/>');
  text = text.replace(/\[pause\]/g, '<break time="600ms"/>');
  return `<speak>${text}</speak>`;
}

// =========================================================
// MAIN
// =========================================================
async function main() {
  const args = parseArgs();

  try {
    const client = new textToSpeech.TextToSpeechClient();

    // Ensure output path is safe and explicit
    const finalOutputPath = path.isAbsolute(args.out)
      ? args.out
      : path.join(DEFAULT_WORKSPACE, args.out);

    // Ensure output directory exists
    const outputDir = path.dirname(finalOutputPath);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // 2. Voice Logic
    const fullVoice = args.voice.includes("Chirp3-HD")
      ? args.voice
      : `en-US-Chirp3-HD-${args.voice}`;

    // 3. Input Logic — convert [pause] tags to SSML if present
    const hasPauseTags = args.text.includes("[pause");
    const inputData = hasPauseTags
      ? { ssml: convertPausesToSSML(args.text) }
      : { text: args.text };

    const request = {
      input: inputData,
      voice: { name: fullVoice, languageCode: "en-US" },
      audioConfig: { audioEncoding: "MP3" },
    };

    // Generate Speech
    const [response] = await client.synthesizeSpeech(request);

    // Write file
    fs.writeFileSync(finalOutputPath, response.audioContent, "binary");

    console.log(`SUCCESS:${path.resolve(finalOutputPath)}`);

  } catch (err) {
    const msg = err.message || String(err);

    if (
      msg.toLowerCase().includes("credentials") ||
      msg.toLowerCase().includes("authentication") ||
      msg.toLowerCase().includes("default")
    ) {
      console.error(
        "ERROR: Google Cloud credentials not found.\n" +
        "Please run: gcloud auth application-default login\n" +
        `Details: ${msg}`
      );
    } else {
      console.error(`ERROR: ${msg}`);
    }

    process.exit(1);
  }
}

main();