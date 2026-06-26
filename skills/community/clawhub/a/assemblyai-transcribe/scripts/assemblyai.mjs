#!/usr/bin/env node
import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SCRIPT_VERSION = '2.0.0';
const DEFAULT_STT_BASE_URL = 'https://api.assemblyai.com';
const DEFAULT_LLM_BASE_URL_US = 'https://llm-gateway.assemblyai.com';
const DEFAULT_LLM_BASE_URL_EU = 'https://llm-gateway.eu.assemblyai.com';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ASSET_DIR = path.resolve(__dirname, '../assets');

export async function main(argv = process.argv.slice(2)) {
  const { flags, positionals } = parseArgs(argv);
  if (flags.help || positionals.length === 0) {
    printUsageAndExit(0);
  }

  const command = String(positionals[0] || '').trim().toLowerCase();
  const quiet = Boolean(flags.quiet);
  const sttBaseUrl = normaliseBaseUrl(flags['base-url'] ?? process.env.ASSEMBLYAI_BASE_URL ?? DEFAULT_STT_BASE_URL);
  const llmBaseUrl = normaliseBaseUrl(
    flags['llm-base-url']
      ?? process.env.ASSEMBLYAI_LLM_BASE_URL
      ?? deriveLlmBaseUrlFromSttBaseUrl(sttBaseUrl)
  );
  const pollMs = parsePositiveInt(flags['poll-ms'], 3000, '--poll-ms');
  const timeoutMs = parsePositiveInt(flags['timeout-ms'], 1_800_000, '--timeout-ms');
  const apiKey = String(flags['api-key'] ?? process.env.ASSEMBLYAI_API_KEY ?? '');

  if (command === 'models') {
    const format = String(flags.format ?? 'markdown');
    const data = await loadAssetJson('model-capabilities.json');
    await writePrimaryOutput(renderModelsOutput(data, format), flags.out);
    return;
  }

  if (command === 'languages') {
    const format = String(flags.format ?? 'markdown');
    const model = flags.model ? String(flags.model) : undefined;
    const includeCodes = Boolean(flags.codes);
    const capabilities = await loadAssetJson('model-capabilities.json');
    const codes = await loadAssetJson('language-codes.json');
    await writePrimaryOutput(renderLanguagesOutput(capabilities, codes, { format, model, includeCodes }), flags.out);
    return;
  }

  if (command === 'transcribe') {
    const audio = positionals[1];
    if (!audio) {
      throw new Error('transcribe requires <path-or-url>');
    }

    const wait = flags.wait === false ? false : true;
    const dryRun = Boolean(flags['dry-run']);
    const config = await buildTranscriptConfigFromFlags(flags, quiet);

    const localFile = !isHttpUrl(audio);
    const plannedAudioUrl = localFile ? '<uploaded-from-local-file>' : audio;

    if (dryRun) {
      const dryRunPayload = {
        command: 'transcribe',
        version: SCRIPT_VERSION,
        stt_base_url: sttBaseUrl,
        llm_base_url: llmBaseUrl,
        source: {
          input: audio,
          kind: localFile ? 'local-file' : 'remote-url',
        },
        request: {
          audio_url: plannedAudioUrl,
          ...config,
        },
      };
      await writePrimaryOutput(JSON.stringify(dryRunPayload, null, 2), flags.out);
      return;
    }

    if (!apiKey) throw new Error('Missing API key. Set ASSEMBLYAI_API_KEY or pass --api-key.');

    const audioUrl = localFile
      ? await uploadFile({ baseUrl: sttBaseUrl, apiKey, filePath: audio, quiet })
      : audio;

    const submitted = await createTranscript({ baseUrl: sttBaseUrl, apiKey, audioUrl, config, quiet });

    if (!wait) {
      const payload = {
        id: submitted.id,
        status: submitted.status,
        audio_url: submitted.audio_url,
        speech_models: submitted.speech_models ?? config.speech_models ?? null,
        speech_model: submitted.speech_model ?? config.speech_model ?? null,
      };
      await writePrimaryOutput(JSON.stringify(payload, null, 2), flags.out);
      return;
    }

    const transcript = await waitForTranscript({
      baseUrl: sttBaseUrl,
      apiKey,
      id: submitted.id,
      pollMs,
      timeoutMs,
      quiet,
    });

    const understandingResult = undefined;
    const bundle = await materialiseTranscriptOutputs({
      transcript,
      sttBaseUrl,
      llmBaseUrl,
      apiKey,
      flags,
      quiet,
      inputHint: audio,
      understandingResult,
    });
    await emitBundle(bundle, flags, quiet);
    return;
  }

  if (command === 'get' || command === 'wait') {
    if (!apiKey) throw new Error('Missing API key. Set ASSEMBLYAI_API_KEY or pass --api-key.');
    const id = positionals[1];
    if (!id) {
      throw new Error(`${command} requires <transcript_id>`);
    }

    const transcript = command === 'wait'
      ? await waitForTranscript({ baseUrl: sttBaseUrl, apiKey, id, pollMs, timeoutMs, quiet })
      : (flags.wait
        ? await waitForTranscript({ baseUrl: sttBaseUrl, apiKey, id, pollMs, timeoutMs, quiet })
        : await getTranscript({ baseUrl: sttBaseUrl, apiKey, id }));

    const bundle = await materialiseTranscriptOutputs({
      transcript,
      sttBaseUrl,
      llmBaseUrl,
      apiKey,
      flags,
      quiet,
      inputHint: id,
      understandingResult: undefined,
    });
    await emitBundle(bundle, flags, quiet);
    return;
  }

  if (command === 'format') {
    const input = positionals[1];
    if (!input) {
      throw new Error('format requires <transcript-id-or-json-file>');
    }

    const resolved = await resolveTranscriptLikeInput({
      input,
      sttBaseUrl,
      apiKey,
      pollMs,
      timeoutMs,
      quiet,
      allowFetchById: true,
      waitIfId: Boolean(flags.wait),
    });

    const bundle = await materialiseResolvedOutputs({
      resolved,
      sttBaseUrl,
      llmBaseUrl,
      apiKey,
      flags,
      quiet,
      inputHint: input,
    });
    await emitBundle(bundle, flags, quiet);
    return;
  }

  if (command === 'paragraphs') {
    if (!apiKey) throw new Error('Missing API key. Set ASSEMBLYAI_API_KEY or pass --api-key.');
    const id = positionals[1];
    if (!id) throw new Error('paragraphs requires <transcript_id>');
    const paragraphs = await getParagraphs({ baseUrl: sttBaseUrl, apiKey, id });
    const format = String(flags.format ?? 'text').toLowerCase();
    const out = format === 'json'
      ? JSON.stringify(paragraphs, null, 2)
      : paragraphsToText(paragraphs);
    await writePrimaryOutput(out, flags.out);
    return;
  }

  if (command === 'sentences') {
    if (!apiKey) throw new Error('Missing API key. Set ASSEMBLYAI_API_KEY or pass --api-key.');
    const id = positionals[1];
    if (!id) throw new Error('sentences requires <transcript_id>');
    const sentences = await getSentences({ baseUrl: sttBaseUrl, apiKey, id });
    const format = String(flags.format ?? 'text').toLowerCase();
    const out = format === 'json'
      ? JSON.stringify(sentences, null, 2)
      : sentencesToText(sentences);
    await writePrimaryOutput(out, flags.out);
    return;
  }

  if (command === 'subtitles') {
    if (!apiKey) throw new Error('Missing API key. Set ASSEMBLYAI_API_KEY or pass --api-key.');
    const id = positionals[1];
    const subtitleFormat = String(positionals[2] || '').toLowerCase();
    if (!id || !subtitleFormat) {
      throw new Error('subtitles requires <transcript_id> <srt|vtt>');
    }
    if (!['srt', 'vtt'].includes(subtitleFormat)) {
      throw new Error('subtitles format must be srt or vtt');
    }
    const charsPerCaption = flags['chars-per-caption'] !== undefined
      ? parsePositiveInt(flags['chars-per-caption'], undefined, '--chars-per-caption')
      : undefined;
    const content = await getSubtitles({
      baseUrl: sttBaseUrl,
      apiKey,
      id,
      subtitleFormat,
      charsPerCaption,
    });
    await writePrimaryOutput(content, flags.out);
    return;
  }

  if (command === 'understand') {
    const id = positionals[1];
    if (!id) throw new Error('understand requires <transcript_id>');

    const requestObject = await buildSpeechUnderstandingRequestFromFlags(flags, quiet);
    if (!requestObject || Object.keys(requestObject).length === 0) {
      throw new Error('understand needs at least one understanding task. Use flags such as --translate-to, --speaker-type/--known-speakers/--speaker-profiles, --format-date/--format-phone/--format-email, or --understanding-request.');
    }

    const dryRun = Boolean(flags['dry-run']);
    if (dryRun) {
      const payload = {
        command: 'understand',
        version: SCRIPT_VERSION,
        llm_base_url: llmBaseUrl,
        transcript_id: id,
        speech_understanding: { request: requestObject },
      };
      await writePrimaryOutput(JSON.stringify(payload, null, 2), flags.out);
      return;
    }

    if (!apiKey) throw new Error('Missing API key. Set ASSEMBLYAI_API_KEY or pass --api-key.');

    const understandingResult = await createSpeechUnderstanding({
      baseUrl: llmBaseUrl,
      apiKey,
      transcriptId: id,
      requestObject,
      quiet,
    });

    const transcript = await getTranscript({ baseUrl: sttBaseUrl, apiKey, id });
    const mergedTranscript = mergeTranscriptWithUnderstanding(transcript, understandingResult);

    const bundle = await materialiseTranscriptOutputs({
      transcript: mergedTranscript,
      sttBaseUrl,
      llmBaseUrl,
      apiKey,
      flags,
      quiet,
      inputHint: id,
      understandingResult,
    });
    await emitBundle(bundle, flags, quiet);
    return;
  }

  if (command === 'llm') {
    const input = positionals[1];
    if (!input) throw new Error('llm requires <transcript-id-or-json-file>');
    const promptText = await readTextArg(flags.prompt, { name: '--prompt' });
    const requestOverride = await readJsonArg(flags.request, { name: '--request', defaultValue: undefined });
    if (!promptText && !requestOverride) {
      throw new Error('llm requires --prompt <text|@file> unless you provide a raw --request JSON body.');
    }

    const resolved = await resolveTranscriptLikeInput({
      input,
      sttBaseUrl,
      apiKey,
      pollMs,
      timeoutMs,
      quiet,
      allowFetchById: true,
      waitIfId: Boolean(flags.wait),
    });

    const agentJson = resolved.kind === 'agent-json'
      ? applyManualSpeakerMapToAgentJson(resolved.agentJson, await parseSpeakerMapArg(flags['speaker-map']))
      : normaliseTranscriptToAgentJson(resolved.transcript, {
        apiBaseUrl: sttBaseUrl,
        inputHint: input,
        manualSpeakerMap: await parseSpeakerMapArg(flags['speaker-map']),
        includeWords: Boolean(flags['include-words']),
      });

    const model = String(flags.model ?? 'claude-sonnet-4-6');
    const systemPrompt = await readTextArg(flags.system, { name: '--system' });
    const inputFormat = String(flags['input-format'] ?? 'speaker-aware').toLowerCase();
    const transcriptPayload = buildLlmInputFromAgentJson(agentJson, inputFormat);
    const schemaArg = await readJsonArg(flags.schema, { name: '--schema', defaultValue: undefined });
    const maxTokens = parsePositiveInt(flags['max-tokens'], 2000, '--max-tokens');
    const temperature = parseOptionalNumber(flags.temperature, '--temperature');
    const dryRun = Boolean(flags['dry-run']);

    let requestBody;
    if (requestOverride) {
      requestBody = requestOverride;
    } else {
      requestBody = {
        model,
        max_tokens: maxTokens,
        messages: [
          ...(systemPrompt ? [{ role: 'system', content: systemPrompt }] : []),
          {
            role: 'user',
            content: `Task:\n${promptText}\n\nTranscript:\n${transcriptPayload}`,
          },
        ],
      };
      if (temperature !== undefined) requestBody.temperature = temperature;
      if (schemaArg) requestBody.response_format = buildJsonSchemaResponseFormat(schemaArg, flags['schema-name']);
    }

    if (dryRun) {
      await writePrimaryOutput(JSON.stringify({
        command: 'llm',
        version: SCRIPT_VERSION,
        llm_base_url: llmBaseUrl,
        input_summary: {
          transcript_id: agentJson?.transcript?.id ?? agentJson?.id ?? null,
          input_format: inputFormat,
        },
        request: requestBody,
      }, null, 2), flags.out);
      return;
    }

    if (!apiKey) throw new Error('Missing API key. Set ASSEMBLYAI_API_KEY or pass --api-key.');

    const llmResult = await createChatCompletion({
      baseUrl: llmBaseUrl,
      apiKey,
      requestBody,
      quiet,
    });

    if (flags['raw-json-out']) {
      await writeTextFile(expandHome(String(flags['raw-json-out'])), JSON.stringify(llmResult, null, 2));
    }

    const primaryFormat = String(flags.export ?? (schemaArg ? 'json' : 'text')).toLowerCase();
    let primaryOutput;
    if (primaryFormat === 'json') {
      primaryOutput = JSON.stringify(extractStructuredLlmOutput(llmResult), null, 2);
    } else if (primaryFormat === 'raw-json') {
      primaryOutput = JSON.stringify(llmResult, null, 2);
    } else {
      primaryOutput = extractLlmText(llmResult);
    }
    await writePrimaryOutput(primaryOutput, flags.out);
    return;
  }

  if (command === 'delete') {
    const id = positionals[1];
    if (!id) throw new Error('delete requires <transcript_id>');
    if (flags['dry-run']) {
      await writePrimaryOutput(JSON.stringify({
        command: 'delete',
        transcript_id: id,
        base_url: sttBaseUrl,
      }, null, 2), flags.out);
      return;
    }
    if (!apiKey) throw new Error('Missing API key. Set ASSEMBLYAI_API_KEY or pass --api-key.');
    const result = await deleteTranscript({ baseUrl: sttBaseUrl, apiKey, id, quiet });
    await writePrimaryOutput(JSON.stringify(result, null, 2), flags.out);
    return;
  }

  throw new Error(`Unknown command: ${command}`);
}

function printUsageAndExit(code = 0) {
  const msg = `AssemblyAI helper CLI v${SCRIPT_VERSION}

Agent-friendly AssemblyAI workflow helper.
- Non-interactive.
- Diagnostics go to stderr.
- Primary data goes to stdout or --out.
- Supports agent-friendly Markdown, normalised agent JSON, and bundle manifests.

Commands:
  transcribe <path-or-url>      Upload/transcribe media and render outputs
  get <transcript_id>           Fetch an existing transcript and render outputs
  wait <transcript_id>          Wait for completion, then render outputs
  format <id-or-json-file>      Re-render a transcript or saved JSON as Markdown / agent JSON / etc.
  paragraphs <transcript_id>    Export AssemblyAI paragraphs endpoint
  sentences <transcript_id>     Export AssemblyAI sentences endpoint
  subtitles <transcript_id> <srt|vtt>
                                Export subtitles
  understand <transcript_id>    Run Speech Understanding tasks and render updated outputs
  llm <id-or-json-file>         Send transcript content through AssemblyAI LLM Gateway
  delete <transcript_id>        Delete transcript data
  models                        Show bundled speech-model capabilities summary
  languages                     Show bundled language support summary

Most useful transcription flags:
  --speech-model <id>           Explicit single STT model
  --speech-models <csv>         Priority-ordered model routing, e.g. universal-3-pro,universal-2
  --auto-best / --no-auto-best  Default: auto-best enabled. Sets routing + language detection if absent.
  --language-code <code>        Explicit language code
  --language-detection          Enable automatic language detection
  --expected-languages <csv|@file>
                                Hint expected languages for detection
  --code-switching              Enable code switching in language_detection_options
  --prompt <text|@file>         Prompting text (documented for Universal-3-Pro)
  --keyterms <csv|@file>        Keyterms prompt
  --custom-spelling <json|@file>
                                Custom spelling rules
  --speaker-labels / --diarize  Enable speaker diarisation
  --speaker-map <json|@file>    Manual speaker label/channel display mapping
  --speakers-expected <n>       Hint exact number of speakers
  --speaker-min <n>             Min expected speakers
  --speaker-max <n>             Max expected speakers
  --multichannel                Enable multi-channel transcription
  --entity-detection            Enable entity extraction
  --sentiment-analysis          Enable sentence-level sentiment
  --auto-highlights             Enable key phrase highlights
  --iab-categories              Enable topic/IAB classification
  --redact-pii                  Enable PII redaction
  --redact-pii-audio            Redact PII in audio too
  --webhook-url <url>           Set webhook callback
  --webhook-auth-header-name <name>
  --webhook-auth-header-value <value>
  --config <json|@file>         Raw /v2/transcript fields (deep-merged with convenience flags)

Speech Understanding flags (transcribe or understand):
  --understanding-request <json|@file>
                                Raw speech_understanding.request object
  --translate-to <csv|@file>    Translation target languages
  --translation-formal          Translation in formal register
  --match-original-utterance    Keep translation aligned to utterances
  --speaker-type <name|role>    Speaker identification type
  --known-speakers <csv|@file>  Known speaker names/roles
  --speaker-profiles <json|@file>
                                Rich speaker descriptions for speaker identification
  --format-date <pattern>       Custom formatting date style
  --format-phone <pattern>      Custom formatting phone style
  --format-email <pattern>      Custom formatting email style

Output flags (get / wait / transcribe / format / understand):
  --export <kind>               markdown|agent-json|json|raw-json|text|paragraphs|sentences|srt|vtt|manifest
                                Default: markdown
  --out <path|->                Primary output path. Default: stdout.
  --bundle-dir <dir>            Write a multi-file bundle + manifest to a directory
  --basename <name>             Base filename to use inside bundle dir
  --all-exports                 In bundle mode, also write paragraphs/sentences/srt/vtt
  --markdown-out <path>
  --agent-json-out <path>
  --raw-json-out <path>
  --text-out <path>
  --paragraphs-out <path>
  --sentences-out <path>
  --srt-out <path>
  --vtt-out <path>
  --understanding-json-out <path>
  --include-plain-text          Include duplicate plain text section in Markdown
  --include-words               Include word-level timing arrays in agent JSON / Markdown
  --chars-per-caption <n>       Subtitle caption width hint

LLM Gateway flags:
  --prompt <text|@file>         User task prompt for llm command
  --system <text|@file>         Optional system prompt for llm command
  --model <id>                  LLM Gateway model. Default: claude-sonnet-4-6
  --input-format <speaker-aware|plain|markdown>
                                Transcript text format fed to LLM. Default: speaker-aware
  --schema <json|@file>         JSON schema for structured outputs
  --schema-name <name>          Optional schema wrapper name
  --request <json|@file>        Raw chat completion request body
  --max-tokens <n>              Completion token cap (default 2000)
  --temperature <n>             Completion temperature

General flags:
  --base-url <url>              STT API base URL. Default: ${DEFAULT_STT_BASE_URL}
  --llm-base-url <url>          LLM Gateway base URL. Derived from STT base URL by default.
  --api-key <key>               Override API key
  --poll-ms <ms>                Poll interval when waiting (default 3000)
  --timeout-ms <ms>             Wait timeout (default 1800000)
  --dry-run                     Print request payload instead of sending it
  --quiet                       Reduce stderr diagnostics
  --help                        Show this help

Environment:
  ASSEMBLYAI_API_KEY            Required for API calls
  ASSEMBLYAI_BASE_URL           Optional STT base URL (use EU endpoint for EU processing)
  ASSEMBLYAI_LLM_BASE_URL       Optional LLM Gateway base URL

Examples:
  node assemblyai.mjs transcribe ./meeting.mp3 --bundle-dir ./out --all-exports
  node assemblyai.mjs transcribe ./call.wav --speaker-labels --speaker-map @assets/speaker-map.example.json
  node assemblyai.mjs transcribe ./meeting.mp3 --translate-to de,fr --match-original-utterance
  node assemblyai.mjs understand abc123 --speaker-type role --known-speakers "host,guest"
  node assemblyai.mjs llm abc123 --prompt @assets/example-prompt.txt --schema @assets/llm-json-schema.example.json
  node assemblyai.mjs models --format json
  node assemblyai.mjs languages --model universal-2 --codes --format markdown
`;
  process.stderr.write(msg);
  process.exit(code);
}

function parseArgs(argv) {
  const flags = {};
  const positionals = [];

  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '-h' || a === '--help') {
      flags.help = true;
      continue;
    }
    if (!a.startsWith('--')) {
      positionals.push(a);
      continue;
    }
    const eq = a.indexOf('=');
    if (eq !== -1) {
      const key = a.slice(2, eq);
      const value = a.slice(eq + 1);
      flags[key] = value;
      continue;
    }
    const key = a.slice(2);
    if (key.startsWith('no-')) {
      flags[key.slice(3)] = false;
      continue;
    }
    const next = argv[i + 1];
    if (next === undefined || next.startsWith('--')) {
      flags[key] = true;
      continue;
    }
    flags[key] = next;
    i += 1;
  }

  if (flags['speaker-labels'] === true && flags.diarize === undefined) {
    flags.diarize = true;
  }
  if (flags.diarize === true && flags['speaker-labels'] === undefined) {
    flags['speaker-labels'] = true;
  }
  if (flags['auto-best'] === undefined) flags['auto-best'] = true;

  return { flags, positionals };
}

function parsePositiveInt(value, defaultValue, flagName) {
  if (value === undefined || value === null || value === '') return defaultValue;
  const n = Number(value);
  if (!Number.isFinite(n) || n <= 0 || Math.floor(n) !== n) {
    throw new Error(`${flagName} must be a positive integer`);
  }
  return n;
}

function parseOptionalNumber(value, flagName) {
  if (value === undefined || value === null || value === '') return undefined;
  const n = Number(value);
  if (!Number.isFinite(n)) {
    throw new Error(`${flagName} must be numeric`);
  }
  return n;
}

function isHttpUrl(value) {
  return /^https?:\/\//i.test(String(value || ''));
}

function normaliseBaseUrl(raw) {
  return String(raw || '').replace(/\/+$/, '');
}

function deriveLlmBaseUrlFromSttBaseUrl(sttBaseUrl) {
  return String(sttBaseUrl).includes('.eu.')
    ? DEFAULT_LLM_BASE_URL_EU
    : DEFAULT_LLM_BASE_URL_US;
}

function regionFromBaseUrl(baseUrl) {
  return String(baseUrl).includes('.eu.') ? 'eu' : 'us';
}

function homeDir() {
  return process.env.HOME || process.env.USERPROFILE || '';
}

function expandHome(p) {
  if (typeof p !== 'string') return p;
  const home = homeDir();
  if (!home) return p;
  if (p === '~') return home;
  if (p.startsWith('~/')) return path.join(home, p.slice(2));
  return p;
}

function stderr(msg, quiet = false) {
  if (quiet) return;
  process.stderr.write(`[assemblyai] ${msg}\n`);
}

async function loadAssetJson(name) {
  const p = path.join(ASSET_DIR, name);
  const raw = await fsp.readFile(p, 'utf8');
  return JSON.parse(raw);
}

function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function deepClone(value) {
  return value === undefined ? undefined : JSON.parse(JSON.stringify(value));
}

function deepMerge(base, override) {
  if (!isPlainObject(base)) return deepClone(override);
  const out = deepClone(base);
  for (const [key, value] of Object.entries(override || {})) {
    if (isPlainObject(value) && isPlainObject(out[key])) {
      out[key] = deepMerge(out[key], value);
    } else {
      out[key] = deepClone(value);
    }
  }
  return out;
}

async function fileExists(p) {
  try {
    await fsp.access(p);
    return true;
  } catch {
    return false;
  }
}

function looksLikeJson(text) {
  const s = String(text || '').trim();
  return s.startsWith('{') || s.startsWith('[');
}

function safeJsonParse(text) {
  try {
    return JSON.parse(text);
  } catch {
    return undefined;
  }
}

async function readTextArg(value, { name = 'value' } = {}) {
  if (value === undefined || value === null || value === false || value === '') return undefined;
  if (value === true) throw new Error(`${name} needs a value`);
  if (typeof value !== 'string') return String(value);
  if (value.startsWith('@')) {
    return (await fsp.readFile(expandHome(value.slice(1)), 'utf8')).trim();
  }
  return value;
}

async function readJsonArg(value, options = {}) {
  const name = options?.name ?? 'value';
  const defaultValue = Object.prototype.hasOwnProperty.call(options, 'defaultValue') ? options.defaultValue : {};
  if (value === undefined || value === null || value === false || value === '') return defaultValue;
  if (value === true) throw new Error(`${name} needs a value`);
  let raw;
  if (typeof value === 'string' && value.startsWith('@')) {
    raw = await fsp.readFile(expandHome(value.slice(1)), 'utf8');
  } else {
    raw = String(value);
  }
  const parsed = JSON.parse(raw);
  return parsed;
}

async function readStringListArg(value, { name = 'value' } = {}) {
  if (value === undefined || value === null || value === false || value === '') return undefined;
  if (value === true) throw new Error(`${name} needs a value`);
  const raw = await readTextArg(value, { name });
  const trimmed = String(raw || '').trim();
  if (!trimmed) return [];
  if (looksLikeJson(trimmed)) {
    const parsed = JSON.parse(trimmed);
    if (!Array.isArray(parsed)) throw new Error(`${name} JSON must be an array`);
    return parsed.map((v) => String(v).trim()).filter(Boolean);
  }
  const parts = trimmed.includes('\n') ? trimmed.split(/\r?\n/) : trimmed.split(',');
  return parts.map((s) => s.trim()).filter(Boolean);
}

async function readCustomSpellingArg(value) {
  if (value === undefined || value === null || value === false || value === '') return undefined;
  const parsed = await readJsonArg(value, { name: '--custom-spelling', defaultValue: undefined });
  if (!Array.isArray(parsed)) {
    throw new Error('--custom-spelling must be a JSON array of {from:[], to:"..."} objects');
  }
  return parsed;
}

function normaliseSpeechModelName(name) {
  const s = String(name || '').trim().toLowerCase();
  if (!s) return '';
  if (s === 'universal3' || s === 'universal-3' || s === 'universal-3pro') return 'universal-3-pro';
  if (s === 'u3' || s === 'u3-pro' || s === 'u3pro') return 'universal-3-pro';
  if (s === 'u2' || s === 'universal2') return 'universal-2';
  return String(name).trim();
}

function splitCsv(value) {
  return String(value || '')
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

class HttpError extends Error {
  constructor(message, details = {}) {
    super(message);
    this.name = 'HttpError';
    this.status = details.status;
    this.statusText = details.statusText;
    this.body = details.body;
    this.url = details.url;
    this.headers = details.headers;
    this.method = details.method;
  }
}

function shouldRetryStatus(status) {
  return [429, 500, 502, 503, 504].includes(status);
}

function computeRetryDelayMs(attempt, res) {
  const retryAfter = res?.headers?.get?.('retry-after');
  if (retryAfter) {
    const secs = Number(retryAfter);
    if (Number.isFinite(secs) && secs >= 0) return Math.round(secs * 1000);
  }
  const base = Math.min(30_000, 1000 * (2 ** attempt));
  const jitter = Math.floor(Math.random() * 250);
  return base + jitter;
}

async function requestRaw(baseUrl, apiKey, relOrAbsUrl, { method = 'GET', headers = {}, body, quiet = false, retries = 4 } = {}) {
  const url = isHttpUrl(relOrAbsUrl)
    ? relOrAbsUrl
    : `${baseUrl}${String(relOrAbsUrl).startsWith('/') ? '' : '/'}${relOrAbsUrl}`;

  for (let attempt = 0; attempt <= retries; attempt += 1) {
    let res;
    try {
      res = await fetch(url, {
        method,
        headers: {
          ...(apiKey ? { Authorization: apiKey } : {}),
          ...headers,
        },
        body,
        ...(body && typeof body === 'object' && typeof body.pipe === 'function' ? { duplex: 'half' } : {}),
      });
    } catch (err) {
      if (attempt < retries) {
        const delay = computeRetryDelayMs(attempt);
        stderr(`Network error on ${method} ${url}; retrying in ${delay}ms (${attempt + 1}/${retries})`, quiet);
        await sleep(delay);
        continue;
      }
      throw err;
    }

    if (res.ok) {
      return res;
    }

    const bodyText = await res.text().catch(() => '');
    if (shouldRetryStatus(res.status) && attempt < retries) {
      const delay = computeRetryDelayMs(attempt, res);
      stderr(`HTTP ${res.status} on ${method} ${url}; retrying in ${delay}ms (${attempt + 1}/${retries})`, quiet);
      await sleep(delay);
      continue;
    }

    throw new HttpError(buildHttpErrorMessage(res.status, res.statusText, bodyText), {
      status: res.status,
      statusText: res.statusText,
      body: bodyText,
      url,
      headers: Object.fromEntries(res.headers.entries()),
      method,
    });
  }

  throw new Error(`Unexpected retry exhaustion for ${method} ${url}`);
}

function buildHttpErrorMessage(status, statusText, bodyText) {
  const trimmed = String(bodyText || '').trim();
  const parsed = safeJsonParse(trimmed);
  let detail = '';
  if (parsed?.error?.message) detail = parsed.error.message;
  else if (parsed?.error) detail = typeof parsed.error === 'string' ? parsed.error : JSON.stringify(parsed.error);
  else if (parsed?.message) detail = parsed.message;
  else if (trimmed) detail = trimmed;

  let extra = '';
  if (/Cannot access uploaded file/i.test(trimmed)) {
    extra = ' Uploads and transcript creation must use API keys from the same AssemblyAI project.';
  } else if (/corrupt|unsupported/i.test(trimmed)) {
    extra = ' Check that the media file is valid and in a supported audio/video format.';
  } else if (/duration/i.test(trimmed) && /160/i.test(trimmed)) {
    extra = ' AssemblyAI documents a minimum audio duration of roughly 160ms.';
  } else if (/not publicly accessible|url/i.test(trimmed)) {
    extra = ' If you used a URL, ensure it points directly to media and is reachable from AssemblyAI servers.';
  }

  return `HTTP ${status} ${statusText}${detail ? `: ${detail}` : ''}${extra}`;
}

async function requestJson(baseUrl, apiKey, relOrAbsUrl, opts = {}) {
  const res = await requestRaw(baseUrl, apiKey, relOrAbsUrl, opts);
  const text = await res.text();
  if (!text) return {};
  const parsed = safeJsonParse(text);
  if (parsed === undefined) {
    throw new Error(`Expected JSON from ${relOrAbsUrl} but got: ${text.slice(0, 500)}`);
  }
  return parsed;
}

async function requestText(baseUrl, apiKey, relOrAbsUrl, opts = {}) {
  const res = await requestRaw(baseUrl, apiKey, relOrAbsUrl, opts);
  return res.text();
}

async function uploadFile({ baseUrl, apiKey, filePath, quiet = false }) {
  const abs = path.resolve(expandHome(filePath));
  const stat = await fsp.stat(abs);
  if (!stat.isFile()) throw new Error(`Not a file: ${abs}`);
  stderr(`Uploading ${abs} (${stat.size} bytes)`, quiet);
  const stream = fs.createReadStream(abs);
  const json = await requestJson(baseUrl, apiKey, '/v2/upload', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/octet-stream',
      'Content-Length': String(stat.size),
    },
    body: stream,
    quiet,
  });
  if (!json?.upload_url) throw new Error('Upload response did not include upload_url');
  return json.upload_url;
}

async function createTranscript({ baseUrl, apiKey, audioUrl, config, quiet = false }) {
  const body = { audio_url: audioUrl, ...(config || {}) };
  stderr(`Creating transcript job`, quiet);
  const json = await requestJson(baseUrl, apiKey, '/v2/transcript', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
    quiet,
  });
  if (!json?.id) throw new Error('Transcript creation response did not include id');
  return json;
}

async function getTranscript({ baseUrl, apiKey, id, quiet = false }) {
  return requestJson(baseUrl, apiKey, `/v2/transcript/${encodeURIComponent(id)}`, { quiet });
}

async function waitForTranscript({ baseUrl, apiKey, id, pollMs, timeoutMs, quiet = false }) {
  const start = Date.now();
  while (true) {
    const transcript = await getTranscript({ baseUrl, apiKey, id, quiet });
    if (transcript?.status === 'completed') return transcript;
    if (transcript?.status === 'error') {
      const reason = transcript?.error ? String(transcript.error) : 'Unknown AssemblyAI transcription error';
      throw new Error(`Transcription failed for ${id}: ${reason}`);
    }
    const elapsed = Date.now() - start;
    if (elapsed > timeoutMs) {
      throw new Error(`Timed out waiting for transcript ${id} after ${elapsed}ms`);
    }
    stderr(`Waiting for transcript ${id}: status=${transcript?.status ?? 'unknown'} elapsed=${elapsed}ms`, quiet);
    await sleep(pollMs);
  }
}

async function getParagraphs({ baseUrl, apiKey, id }) {
  return requestJson(baseUrl, apiKey, `/v2/transcript/${encodeURIComponent(id)}/paragraphs`);
}

async function getSentences({ baseUrl, apiKey, id }) {
  return requestJson(baseUrl, apiKey, `/v2/transcript/${encodeURIComponent(id)}/sentences`);
}

async function getSubtitles({ baseUrl, apiKey, id, subtitleFormat, charsPerCaption }) {
  const qp = charsPerCaption ? `?chars_per_caption=${encodeURIComponent(String(charsPerCaption))}` : '';
  const raw = await requestText(baseUrl, apiKey, `/v2/transcript/${encodeURIComponent(id)}/${encodeURIComponent(subtitleFormat)}${qp}`);
  const trimmed = String(raw || '').trim();
  if (trimmed.startsWith('"') && trimmed.endsWith('"')) {
    const parsed = safeJsonParse(trimmed);
    if (typeof parsed === 'string') return parsed;
  }
  return raw;
}

async function createSpeechUnderstanding({ baseUrl, apiKey, transcriptId, requestObject, quiet = false }) {
  stderr(`Submitting Speech Understanding request`, quiet);
  return requestJson(baseUrl, apiKey, '/v1/understanding', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      transcript_id: transcriptId,
      speech_understanding: { request: requestObject },
    }),
    quiet,
  });
}

async function createChatCompletion({ baseUrl, apiKey, requestBody, quiet = false }) {
  stderr(`Submitting LLM Gateway request`, quiet);
  return requestJson(baseUrl, apiKey, '/v1/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(requestBody),
    quiet,
  });
}

async function deleteTranscript({ baseUrl, apiKey, id, quiet = false }) {
  stderr(`Deleting transcript ${id}`, quiet);
  const res = await requestRaw(baseUrl, apiKey, `/v2/transcript/${encodeURIComponent(id)}`, {
    method: 'DELETE',
    quiet,
  });
  const text = await res.text().catch(() => '');
  return text ? (safeJsonParse(text) ?? { ok: true, raw: text }) : { ok: true, transcript_id: id };
}

async function buildTranscriptConfigFromFlags(flags, quiet = false) {
  const configFromArg = await readJsonArg(flags.config, { name: '--config', defaultValue: {} });
  let derived = {};

  if (flags['speech-model']) {
    derived.speech_model = normaliseSpeechModelName(flags['speech-model']);
    derived.speech_models = undefined;
  }
  if (flags['speech-models']) {
    derived.speech_models = splitCsv(flags['speech-models']).map(normaliseSpeechModelName).filter(Boolean);
    derived.speech_model = undefined;
  }

  if (flags['language-code']) {
    derived.language_code = String(flags['language-code']).trim();
  }
  if (flags['language-detection'] !== undefined) {
    derived.language_detection = Boolean(flags['language-detection']);
  }
  if (flags['expected-languages']) {
    derived.language_detection_options = {
      ...(derived.language_detection_options || {}),
      expected_languages: await readStringListArg(flags['expected-languages'], { name: '--expected-languages' }),
    };
  }
  if (flags['code-switching'] !== undefined) {
    derived.language_detection_options = {
      ...(derived.language_detection_options || {}),
      code_switching: Boolean(flags['code-switching']),
    };
  }

  if (flags.prompt) {
    derived.prompt = await readTextArg(flags.prompt, { name: '--prompt' });
  }
  if (flags.keyterms) {
    derived.keyterms_prompt = await readStringListArg(flags.keyterms, { name: '--keyterms' });
  }
  if (flags['custom-spelling']) {
    derived.custom_spelling = await readCustomSpellingArg(flags['custom-spelling']);
  }

  if (flags['speaker-labels'] !== undefined || flags.diarize !== undefined) {
    derived.speaker_labels = Boolean(flags['speaker-labels'] ?? flags.diarize);
  }
  if (flags['speakers-expected'] !== undefined) {
    derived.speakers_expected = parsePositiveInt(flags['speakers-expected'], undefined, '--speakers-expected');
  }
  const minSpeakers = flags['speaker-min'] !== undefined
    ? parsePositiveInt(flags['speaker-min'], undefined, '--speaker-min')
    : undefined;
  const maxSpeakers = flags['speaker-max'] !== undefined
    ? parsePositiveInt(flags['speaker-max'], undefined, '--speaker-max')
    : undefined;
  if (minSpeakers !== undefined || maxSpeakers !== undefined) {
    derived.speaker_options = {
      ...(minSpeakers !== undefined ? { min_speakers_expected: minSpeakers } : {}),
      ...(maxSpeakers !== undefined ? { max_speakers_expected: maxSpeakers } : {}),
    };
  }
  if (flags.multichannel !== undefined) derived.multichannel = Boolean(flags.multichannel);
  if (flags['entity-detection'] !== undefined) derived.entity_detection = Boolean(flags['entity-detection']);
  if (flags['sentiment-analysis'] !== undefined) derived.sentiment_analysis = Boolean(flags['sentiment-analysis']);
  if (flags['auto-highlights'] !== undefined) derived.auto_highlights = Boolean(flags['auto-highlights']);
  if (flags['iab-categories'] !== undefined) derived.iab_categories = Boolean(flags['iab-categories']);
  if (flags['redact-pii'] !== undefined) derived.redact_pii = Boolean(flags['redact-pii']);
  if (flags['redact-pii-audio'] !== undefined) derived.redact_pii_audio = Boolean(flags['redact-pii-audio']);

  if (flags['webhook-url']) derived.webhook_url = String(flags['webhook-url']);
  if (flags['webhook-auth-header-name']) derived.webhook_auth_header_name = String(flags['webhook-auth-header-name']);
  if (flags['webhook-auth-header-value']) derived.webhook_auth_header_value = String(flags['webhook-auth-header-value']);

  const understandingRequest = await buildSpeechUnderstandingRequestFromFlags(flags, quiet, { defaultValue: undefined });
  if (understandingRequest && Object.keys(understandingRequest).length) {
    derived.speech_understanding = { request: understandingRequest };
    if (understandingRequest.speaker_identification && derived.speaker_labels === undefined && configFromArg.speaker_labels === undefined) {
      derived.speaker_labels = true;
      stderr('Enabling speaker_labels automatically because speaker identification needs diarisation', quiet);
    }
  }

  let config = deepMerge(configFromArg, stripUndefined(derived));

  if (flags['auto-best'] !== false) {
    const hasSpeechModel = Boolean(config.speech_model) || (Array.isArray(config.speech_models) && config.speech_models.length > 0);
    if (!hasSpeechModel) {
      config.speech_models = ['universal-3-pro', 'universal-2'];
    }
    if (config.language_code === undefined && config.language_detection === undefined) {
      config.language_detection = true;
    }
  }

  if (flags['speech-model']) delete config.speech_models;
  if (flags['speech-models']) delete config.speech_model;

  if (config.language_code && config.language_detection) {
    stderr('Both language_code and language_detection are set. AssemblyAI may prefer one over the other; consider using only one.', quiet);
  }

  const requestedModels = getRequestedSpeechModels(config);
  if (config.prompt) {
    const wordCount = String(config.prompt).trim().split(/\s+/).filter(Boolean).length;
    if (wordCount > 1500) {
      stderr(`Prompt is ${wordCount} words; AssemblyAI documents prompting up to 1500 words for Universal-3-Pro`, quiet);
    }
    if (!requestedModels.some((m) => m === 'universal-3-pro')) {
      stderr('Prompting is documented for Universal-3-Pro. Your request does not include universal-3-pro.', quiet);
    }
  }

  if (Array.isArray(config.keyterms_prompt)) {
    if (config.keyterms_prompt.length > 1000) {
      throw new Error(`keyterms_prompt has ${config.keyterms_prompt.length} entries; documented maximum is 1000`);
    }
    for (const item of config.keyterms_prompt) {
      const words = String(item).trim().split(/\s+/).filter(Boolean).length;
      if (words > 6) {
        stderr(`Keyterm "${item}" has ${words} words; AssemblyAI documents a maximum of 6 words per keyterm phrase`, quiet);
      }
    }
  }

  return config;
}

async function buildSpeechUnderstandingRequestFromFlags(flags, quiet = false, { defaultValue = {} } = {}) {
  const fromArg = await readJsonArg(flags['understanding-request'], {
    name: '--understanding-request',
    defaultValue,
  });
  if (fromArg === undefined) {
    // continue: convenience flags may still populate
  }

  let requestObject = isPlainObject(fromArg) ? deepClone(fromArg) : {};

  if (flags['translate-to']) {
    requestObject.translation = {
      ...(requestObject.translation || {}),
      target_languages: await readStringListArg(flags['translate-to'], { name: '--translate-to' }),
    };
  }
  if (flags['translation-formal'] !== undefined) {
    requestObject.translation = {
      ...(requestObject.translation || {}),
      formal: Boolean(flags['translation-formal']),
    };
  }
  if (flags['match-original-utterance'] !== undefined) {
    requestObject.translation = {
      ...(requestObject.translation || {}),
      match_original_utterance: Boolean(flags['match-original-utterance']),
    };
  }

  const knownSpeakers = flags['known-speakers']
    ? await readStringListArg(flags['known-speakers'], { name: '--known-speakers' })
    : undefined;
  const speakerProfiles = flags['speaker-profiles']
    ? await readJsonArg(flags['speaker-profiles'], { name: '--speaker-profiles', defaultValue: undefined })
    : undefined;
  const speakerType = flags['speaker-type'] ? String(flags['speaker-type']).trim() : undefined;
  if (speakerType || knownSpeakers || speakerProfiles) {
    requestObject.speaker_identification = {
      ...(requestObject.speaker_identification || {}),
      ...(speakerType ? { speaker_type: speakerType } : {}),
    };
    if (speakerProfiles !== undefined) {
      const speakers = Array.isArray(speakerProfiles)
        ? speakerProfiles
        : Array.isArray(speakerProfiles?.speakers)
          ? speakerProfiles.speakers
          : undefined;
      if (!Array.isArray(speakers)) {
        throw new Error('--speaker-profiles must be a JSON array, or an object with a "speakers" array');
      }
      requestObject.speaker_identification.speakers = speakers;
      if (knownSpeakers?.length) {
        stderr('Ignoring --known-speakers because --speaker-profiles was provided', quiet);
      }
      if (!requestObject.speaker_identification.speaker_type) {
        requestObject.speaker_identification.speaker_type = 'name';
      }
    } else if (knownSpeakers?.length) {
      requestObject.speaker_identification.known_values = knownSpeakers;
      if (!requestObject.speaker_identification.speaker_type) {
        requestObject.speaker_identification.speaker_type = 'name';
      }
    }
  }

  if (flags['format-date'] || flags['format-phone'] || flags['format-email']) {
    requestObject.custom_formatting = {
      ...(requestObject.custom_formatting || {}),
      ...(flags['format-date'] ? { date: String(flags['format-date']) } : {}),
      ...(flags['format-phone'] ? { phone_number: String(flags['format-phone']) } : {}),
      ...(flags['format-email'] ? { email: String(flags['format-email']) } : {}),
    };
  }

  requestObject = stripUndefined(requestObject);

  if (Object.keys(requestObject).length === 0) return undefined;
  return requestObject;
}

function stripUndefined(value) {
  if (Array.isArray(value)) return value.map(stripUndefined);
  if (!isPlainObject(value)) return value;
  const out = {};
  for (const [k, v] of Object.entries(value)) {
    if (v !== undefined) out[k] = stripUndefined(v);
  }
  return out;
}

function getRequestedSpeechModels(config) {
  if (Array.isArray(config?.speech_models) && config.speech_models.length) return config.speech_models.map(String);
  if (config?.speech_model) return [String(config.speech_model)];
  return [];
}

async function parseSpeakerMapArg(value) {
  if (value === undefined || value === null || value === false || value === '') return {};
  const raw = await readTextArg(value, { name: '--speaker-map' });
  if (!raw) return {};
  const trimmed = String(raw).trim();
  if (!trimmed) return {};

  const out = {};
  if (looksLikeJson(trimmed)) {
    const parsed = JSON.parse(trimmed);
    if (Array.isArray(parsed)) {
      for (const item of parsed) {
        if (!isPlainObject(item)) continue;
        const rawKey = item.raw ?? item.label ?? item.speaker ?? item.channel;
        const display = item.display ?? item.name ?? item.role ?? item.value;
        if (rawKey === undefined || display === undefined) continue;
        const key = canonicalSpeakerKey(rawKey);
        out[key] = {
          raw: key,
          display: String(display),
          source: String(item.source ?? 'manual'),
          ...item,
        };
      }
      return out;
    }

    if (isPlainObject(parsed)) {
      for (const [rawKey, value2] of Object.entries(parsed)) {
        const key = canonicalSpeakerKey(rawKey);
        if (isPlainObject(value2)) {
          const display = value2.display ?? value2.name ?? value2.role ?? value2.label ?? rawKey;
          out[key] = {
            raw: key,
            display: String(display),
            source: String(value2.source ?? 'manual'),
            ...value2,
          };
        } else {
          out[key] = {
            raw: key,
            display: String(value2),
            source: 'manual',
          };
        }
      }
      return out;
    }

    throw new Error('--speaker-map JSON must be an object or array');
  }

  const lines = trimmed.includes('\n') ? trimmed.split(/\r?\n/) : trimmed.split(',');
  for (const line of lines) {
    const item = line.trim();
    if (!item || item.startsWith('#')) continue;
    const m = item.match(/^(.+?)(?:=>|=)(.+)$/);
    if (!m) {
      throw new Error(`Could not parse speaker map entry "${item}". Use KEY=Display Name or JSON.`);
    }
    const key = canonicalSpeakerKey(m[1].trim());
    out[key] = {
      raw: key,
      display: m[2].trim(),
      source: 'manual',
    };
  }
  return out;
}

function canonicalSpeakerKey(raw) {
  if (raw === undefined || raw === null) return '';
  const s = String(raw).trim();
  if (!s) return '';
  const speakerMatch = s.match(/^speaker\s+([a-z0-9]+)$/i);
  if (speakerMatch) return speakerMatch[1].toUpperCase();
  const channelMatch = s.match(/^channel[:\s#-]*([0-9]+)$/i);
  if (channelMatch) return `channel:${channelMatch[1]}`;
  if (/^[A-Za-z]$/.test(s)) return s.toUpperCase();
  if (/^\d+$/.test(s)) return s;
  return s;
}

function fallbackSpeakerDisplay(raw) {
  if (!raw) return '';
  const key = canonicalSpeakerKey(raw);
  if (/^[A-Z0-9]+$/.test(key) && key.length <= 3) return `Speaker ${key}`;
  if (/^\d+$/.test(key)) return `Speaker ${key}`;
  if (key.startsWith('channel:')) return `Channel ${key.split(':')[1]}`;
  return String(raw);
}

function extractAssemblySpeakerMap(transcript) {
  const mapping = transcript?.speech_understanding?.response?.speaker_identification?.mapping
    ?? transcript?.speech_understanding?.speaker_identification?.mapping
    ?? transcript?._understanding_result?.speech_understanding?.response?.speaker_identification?.mapping
    ?? {};
  const out = {};
  for (const [rawKey, display] of Object.entries(mapping || {})) {
    const key = canonicalSpeakerKey(rawKey);
    out[key] = {
      raw: key,
      display: String(display),
      source: 'assemblyai',
    };
  }
  return out;
}

function buildSpeakerMap({ transcript, manualSpeakerMap = {}, existingAgentSpeakerMap = {} }) {
  const out = {};
  const apiMap = extractAssemblySpeakerMap(transcript);
  const utterances = Array.isArray(transcript?.utterances) ? transcript.utterances : [];

  for (const sourceMap of [apiMap, existingAgentSpeakerMap, manualSpeakerMap]) {
    for (const [key, value] of Object.entries(sourceMap || {})) {
      const canonical = canonicalSpeakerKey(key);
      if (!canonical) continue;
      out[canonical] = {
        raw: canonical,
        display: String(value?.display ?? value?.name ?? value?.role ?? value ?? canonical),
        source: String(value?.source ?? 'manual'),
        ...(isPlainObject(value) ? value : {}),
      };
    }
  }

  for (const utterance of utterances) {
    const rawSpeaker = utterance?.speaker ?? (utterance?.channel !== undefined ? `channel:${utterance.channel}` : undefined);
    const canonical = canonicalSpeakerKey(rawSpeaker);
    if (!canonical) continue;
    if (!out[canonical]) {
      out[canonical] = {
        raw: canonical,
        display: fallbackSpeakerDisplay(rawSpeaker),
        source: canonical === rawSpeaker ? 'fallback' : 'fallback-normalised',
      };
    }
  }
  return out;
}

function getSpeakerDisplay(rawSpeaker, speakerMap, channel) {
  const canonical = canonicalSpeakerKey(rawSpeaker ?? (channel !== undefined ? `channel:${channel}` : ''));
  if (canonical && speakerMap[canonical]?.display) return speakerMap[canonical].display;
  if (rawSpeaker !== undefined && rawSpeaker !== null && String(rawSpeaker).trim()) return fallbackSpeakerDisplay(rawSpeaker);
  if (channel !== undefined && channel !== null) return fallbackSpeakerDisplay(`channel:${channel}`);
  return '';
}

function formatClock(ms) {
  if (ms === undefined || ms === null || Number.isNaN(Number(ms))) return '';
  const totalMs = Number(ms);
  const totalSeconds = Math.floor(totalMs / 1000);
  const milli = String(Math.floor(totalMs % 1000)).padStart(3, '0');
  const seconds = String(totalSeconds % 60).padStart(2, '0');
  const minutes = String(Math.floor(totalSeconds / 60) % 60).padStart(2, '0');
  const hours = String(Math.floor(totalSeconds / 3600)).padStart(2, '0');
  return `${hours}:${minutes}:${seconds}.${milli}`;
}

function formatDurationHuman(ms) {
  if (ms === undefined || ms === null || Number.isNaN(Number(ms))) return '';
  const totalSeconds = Math.round(Number(ms) / 1000);
  const h = Math.floor(totalSeconds / 3600);
  const m = Math.floor((totalSeconds % 3600) / 60);
  const s = totalSeconds % 60;
  const parts = [];
  if (h) parts.push(`${h}h`);
  if (m || h) parts.push(`${m}m`);
  parts.push(`${s}s`);
  return parts.join(' ');
}

function countSentiment(results) {
  const counts = { positive: 0, neutral: 0, negative: 0 };
  for (const item of results || []) {
    const key = String(item?.sentiment || '').toLowerCase();
    if (key in counts) counts[key] += 1;
  }
  return counts;
}

function normaliseTranscriptToAgentJson(transcript, {
  apiBaseUrl,
  inputHint,
  manualSpeakerMap = {},
  existingAgentSpeakerMap = {},
  includeWords = false,
} = {}) {
  const t = deepClone(transcript);
  const speakerMap = buildSpeakerMap({
    transcript: t,
    manualSpeakerMap,
    existingAgentSpeakerMap,
  });
  const utterances = Array.isArray(t?.utterances) ? t.utterances : [];
  const words = Array.isArray(t?.words) ? t.words : [];
  const sentimentSegments = Array.isArray(t?.sentiment_analysis_results) ? t.sentiment_analysis_results : [];
  const entities = Array.isArray(t?.entities) ? t.entities : [];
  const highlights = Array.isArray(t?.auto_highlights_result?.results) ? t.auto_highlights_result.results : [];
  const chapters = Array.isArray(t?.chapters) ? t.chapters : [];
  const topicsSummary = t?.iab_categories_result?.summary ?? {};
  const topicsResults = Array.isArray(t?.iab_categories_result?.results) ? t.iab_categories_result.results : [];
  const speechUnderstanding = t?.speech_understanding ?? {};
  const translationLanguages = Object.keys(t?.translated_texts ?? {});

  const normalisedUtterances = utterances.map((u, index) => {
    const speakerRaw = u?.speaker ?? null;
    const channel = u?.channel;
    return {
      index,
      start_ms: u?.start ?? null,
      end_ms: u?.end ?? null,
      start: formatClock(u?.start),
      end: formatClock(u?.end),
      duration_ms: (u?.end !== undefined && u?.start !== undefined) ? Number(u.end) - Number(u.start) : null,
      speaker_raw: speakerRaw,
      speaker_display: getSpeakerDisplay(speakerRaw, speakerMap, channel),
      channel: channel ?? null,
      confidence: u?.confidence ?? null,
      text: u?.text ?? '',
      translated_texts: u?.translated_texts ?? undefined,
    };
  });

  const normalisedWords = includeWords
    ? words.map((w, index) => ({
      index,
      text: w?.text ?? '',
      start_ms: w?.start ?? null,
      end_ms: w?.end ?? null,
      start: formatClock(w?.start),
      end: formatClock(w?.end),
      confidence: w?.confidence ?? null,
      speaker_raw: w?.speaker ?? null,
      speaker_display: getSpeakerDisplay(w?.speaker ?? null, speakerMap, w?.channel),
      channel: w?.channel ?? null,
    }))
    : undefined;

  const featureFlags = {
    speaker_labels: Boolean(t?.speaker_labels) || utterances.some((u) => u?.speaker !== undefined),
    multichannel: Boolean(t?.multichannel) || utterances.some((u) => u?.channel !== undefined),
    entity_detection: Boolean(t?.entity_detection) || entities.length > 0,
    sentiment_analysis: Boolean(t?.sentiment_analysis) || sentimentSegments.length > 0,
    auto_highlights: Boolean(t?.auto_highlights) || highlights.length > 0,
    iab_categories: Boolean(t?.iab_categories) || topicsResults.length > 0 || Object.keys(topicsSummary).length > 0,
    speech_understanding: Object.keys(speechUnderstanding || {}).length > 0,
    translation_languages: translationLanguages,
  };

  return {
    schema_version: 'assemblyai-transcribe-agent-json/v2',
    generated_at: new Date().toISOString(),
    source: {
      provider: 'assemblyai',
      region: regionFromBaseUrl(apiBaseUrl || DEFAULT_STT_BASE_URL),
      api_base_url: apiBaseUrl || DEFAULT_STT_BASE_URL,
      input_hint: inputHint ?? null,
    },
    transcript: {
      id: t?.id ?? null,
      status: t?.status ?? null,
      error: t?.error ?? null,
      audio_url: t?.audio_url ?? null,
      text: t?.text ?? '',
      language_code: t?.language_code ?? null,
      language_confidence: t?.language_confidence ?? null,
      confidence: t?.confidence ?? null,
      speech_model_used: t?.speech_model_used ?? null,
      speech_models_requested: getRequestedSpeechModels(t),
      audio_duration_ms: t?.audio_duration ?? null,
      audio_duration_human: formatDurationHuman(t?.audio_duration),
      webhook_status_code: t?.webhook_status_code ?? null,
    },
    features: featureFlags,
    speaker_map: speakerMap,
    utterances: normalisedUtterances,
    words: normalisedWords,
    chapters,
    highlights,
    topics: {
      summary: topicsSummary,
      results: topicsResults,
    },
    entities,
    sentiment: {
      summary: countSentiment(sentimentSegments),
      segments: sentimentSegments,
    },
    translated_texts: t?.translated_texts ?? {},
    speech_understanding: speechUnderstanding,
    raw_metadata: {
      auto_highlights_result: t?.auto_highlights_result ?? undefined,
      iab_categories_result: t?.iab_categories_result ?? undefined,
    },
  };
}

function applyManualSpeakerMapToAgentJson(agentJson, manualSpeakerMap = {}) {
  const out = deepClone(agentJson);
  const merged = buildSpeakerMap({
    transcript: { utterances: out?.utterances?.map((u) => ({ speaker: u.speaker_raw, channel: u.channel })) ?? [] },
    manualSpeakerMap,
    existingAgentSpeakerMap: out?.speaker_map ?? {},
  });
  out.speaker_map = merged;
  out.utterances = (out.utterances || []).map((u) => ({
    ...u,
    speaker_display: getSpeakerDisplay(u.speaker_raw, merged, u.channel),
  }));
  if (Array.isArray(out.words)) {
    out.words = out.words.map((w) => ({
      ...w,
      speaker_display: getSpeakerDisplay(w.speaker_raw, merged, w.channel),
    }));
  }
  out.generated_at = new Date().toISOString();
  return out;
}

function mergeTranscriptWithUnderstanding(transcript, understandingResult) {
  const merged = deepClone(transcript);
  merged.speech_understanding = understandingResult?.speech_understanding ?? merged.speech_understanding;
  if (understandingResult?.translated_texts) merged.translated_texts = understandingResult.translated_texts;
  if (Array.isArray(understandingResult?.utterances) && understandingResult.utterances.length) merged.utterances = understandingResult.utterances;
  if (Array.isArray(understandingResult?.words)) merged.words = understandingResult.words;
  merged._understanding_result = understandingResult;
  return merged;
}

function mdEscape(text) {
  return String(text ?? '')
    .replace(/\|/g, '\\|')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function maybeTruncate(items, maxItems = 50) {
  if (!Array.isArray(items)) return { items: [], truncated: false, total: 0 };
  return {
    items: items.slice(0, maxItems),
    truncated: items.length > maxItems,
    total: items.length,
  };
}

function renderAgentJsonMarkdown(agentJson, { includePlainText = false, maxItems = 50 } = {}) {
  const lines = [];
  const t = agentJson.transcript || {};
  lines.push('# AssemblyAI Transcript');
  lines.push('');
  lines.push('## Metadata');
  lines.push(`- Transcript ID: ${t.id ?? ''}`);
  lines.push(`- Status: ${t.status ?? ''}`);
  lines.push(`- Region: ${agentJson?.source?.region ?? ''}`);
  lines.push(`- API base URL: ${agentJson?.source?.api_base_url ?? ''}`);
  if (t.audio_url) lines.push(`- Audio URL: ${t.audio_url}`);
  if (t.speech_model_used) lines.push(`- Model used: ${t.speech_model_used}`);
  if (Array.isArray(t.speech_models_requested) && t.speech_models_requested.length) {
    lines.push(`- Requested models: ${t.speech_models_requested.join(', ')}`);
  }
  if (t.language_code) {
    const lang = t.language_confidence !== null && t.language_confidence !== undefined
      ? `${t.language_code} (confidence ${t.language_confidence})`
      : t.language_code;
    lines.push(`- Language: ${lang}`);
  }
  if (t.confidence !== null && t.confidence !== undefined) lines.push(`- Confidence: ${t.confidence}`);
  if (t.audio_duration_ms !== null && t.audio_duration_ms !== undefined) {
    lines.push(`- Duration: ${formatClock(t.audio_duration_ms)} (${t.audio_duration_human})`);
  }
  const enabledFeatures = [];
  for (const [k, v] of Object.entries(agentJson.features || {})) {
    if (Array.isArray(v) && v.length) enabledFeatures.push(`${k}=${v.join(',')}`);
    else if (v === true) enabledFeatures.push(k);
  }
  if (enabledFeatures.length) lines.push(`- Enabled / detected features: ${enabledFeatures.join(', ')}`);
  lines.push('');

  const speakerMapEntries = Object.values(agentJson.speaker_map || {});
  if (speakerMapEntries.length) {
    lines.push('## Speaker Map');
    lines.push('');
    lines.push('| Raw | Display | Source |');
    lines.push('| --- | --- | --- |');
    for (const entry of speakerMapEntries.sort((a, b) => String(a.raw).localeCompare(String(b.raw)))) {
      lines.push(`| ${mdEscape(entry.raw)} | ${mdEscape(entry.display)} | ${mdEscape(entry.source ?? '')} |`);
    }
    lines.push('');
  }

  lines.push('## Transcript');
  lines.push('');
  if (Array.isArray(agentJson.utterances) && agentJson.utterances.length) {
    for (const utterance of agentJson.utterances) {
      const speakerBit = utterance.speaker_display ? `**${mdEscape(utterance.speaker_display)}**: ` : '';
      lines.push(`[${utterance.start} → ${utterance.end}] ${speakerBit}${mdEscape(utterance.text)}`);
      if (utterance.translated_texts && Object.keys(utterance.translated_texts).length) {
        for (const [lang, translated] of Object.entries(utterance.translated_texts)) {
          lines.push(`  - *${mdEscape(lang)}*: ${mdEscape(translated)}`);
        }
      }
      lines.push('');
    }
  } else if (t.text) {
    lines.push(t.text.trim());
    lines.push('');
  } else {
    lines.push('_No transcript text available._');
    lines.push('');
  }

  if (includePlainText && t.text) {
    lines.push('## Plain Text');
    lines.push('');
    lines.push(t.text.trim());
    lines.push('');
  }

  if (Array.isArray(agentJson.chapters) && agentJson.chapters.length) {
    lines.push('## Chapters');
    lines.push('');
    for (const chapter of agentJson.chapters) {
      const heading = chapter?.headline || chapter?.gist || chapter?.summary || `Chapter @ ${formatClock(chapter?.start)}`;
      lines.push(`### ${mdEscape(heading)}`);
      lines.push('');
      if (chapter?.start !== undefined || chapter?.end !== undefined) {
        lines.push(`- Range: ${formatClock(chapter?.start)} → ${formatClock(chapter?.end)}`);
      }
      if (chapter?.summary) lines.push(`- Summary: ${mdEscape(chapter.summary)}`);
      if (chapter?.gist) lines.push(`- Gist: ${mdEscape(chapter.gist)}`);
      lines.push('');
    }
  }

  if (Array.isArray(agentJson.highlights) && agentJson.highlights.length) {
    const { items, truncated, total } = maybeTruncate(agentJson.highlights, maxItems);
    lines.push('## Key Phrases');
    lines.push('');
    if (truncated) lines.push(`_Showing first ${items.length} of ${total} highlight entries._\n`);
    for (const item of items) {
      const countBit = item?.count !== undefined ? ` (count ${item.count})` : '';
      lines.push(`- ${mdEscape(item?.text ?? '')}${countBit}`);
    }
    lines.push('');
  }

  const topicSummary = agentJson?.topics?.summary || {};
  const topicPairs = Object.entries(topicSummary);
  if (topicPairs.length || (Array.isArray(agentJson?.topics?.results) && agentJson.topics.results.length)) {
    lines.push('## Topics');
    lines.push('');
    if (topicPairs.length) {
      for (const [label, score] of topicPairs) {
        lines.push(`- ${mdEscape(label)}${score !== undefined ? ` (${score})` : ''}`);
      }
    } else {
      const { items, truncated, total } = maybeTruncate(agentJson.topics.results, maxItems);
      if (truncated) lines.push(`_Showing first ${items.length} of ${total} topic entries._\n`);
      for (const item of items) {
        lines.push(`- ${mdEscape(item?.label ?? item?.text ?? JSON.stringify(item))}`);
      }
    }
    lines.push('');
  }

  if (Array.isArray(agentJson.entities) && agentJson.entities.length) {
    const { items, truncated, total } = maybeTruncate(agentJson.entities, maxItems);
    lines.push('## Entities');
    lines.push('');
    if (truncated) lines.push(`_Showing first ${items.length} of ${total} entities._\n`);
    lines.push('| Type | Text | Confidence | Start | End |');
    lines.push('| --- | --- | --- | --- | --- |');
    for (const entity of items) {
      lines.push(`| ${mdEscape(entity?.entity_type ?? entity?.type ?? '')} | ${mdEscape(entity?.text ?? '')} | ${mdEscape(entity?.confidence ?? '')} | ${mdEscape(formatClock(entity?.start))} | ${mdEscape(formatClock(entity?.end))} |`);
    }
    lines.push('');
  }

  const sentimentSegments = agentJson?.sentiment?.segments ?? [];
  if (sentimentSegments.length) {
    const counts = agentJson?.sentiment?.summary ?? {};
    lines.push('## Sentiment');
    lines.push('');
    lines.push(`- Positive: ${counts.positive ?? 0}`);
    lines.push(`- Neutral: ${counts.neutral ?? 0}`);
    lines.push(`- Negative: ${counts.negative ?? 0}`);
    lines.push('');
    const { items, truncated, total } = maybeTruncate(sentimentSegments, maxItems);
    if (truncated) lines.push(`_Showing first ${items.length} of ${total} sentiment segments._\n`);
    for (const seg of items) {
      lines.push(`- [${formatClock(seg?.start)} → ${formatClock(seg?.end)}] ${String(seg?.sentiment ?? '').toUpperCase()}: ${mdEscape(seg?.text ?? '')}`);
    }
    lines.push('');
  }

  const translatedTexts = agentJson?.translated_texts ?? {};
  if (Object.keys(translatedTexts).length) {
    lines.push('## Transcript-Level Translations');
    lines.push('');
    for (const [lang, text] of Object.entries(translatedTexts)) {
      lines.push(`### ${mdEscape(lang)}`);
      lines.push('');
      lines.push(String(text).trim());
      lines.push('');
    }
  }

  const su = agentJson?.speech_understanding ?? {};
  const customFormatting = su?.response?.custom_formatting ?? su?.custom_formatting ?? {};
  if (customFormatting?.formatted_text || Array.isArray(customFormatting?.formatted_utterances)) {
    lines.push('## Custom Formatting');
    lines.push('');
    if (customFormatting.formatted_text) {
      lines.push('### Formatted Text');
      lines.push('');
      lines.push(String(customFormatting.formatted_text).trim());
      lines.push('');
    }
    if (customFormatting.mapping && Object.keys(customFormatting.mapping).length) {
      lines.push('### Replacement Mapping');
      lines.push('');
      for (const [from, to] of Object.entries(customFormatting.mapping)) {
        lines.push(`- ${mdEscape(from)} → ${mdEscape(to)}`);
      }
      lines.push('');
    }
  }

  if (Array.isArray(agentJson.words) && agentJson.words.length) {
    const { items, truncated, total } = maybeTruncate(agentJson.words, maxItems);
    lines.push('## Word-Level Timestamps');
    lines.push('');
    if (truncated) lines.push(`_Showing first ${items.length} of ${total} words._\n`);
    lines.push('| Word | Start | End | Speaker | Confidence |');
    lines.push('| --- | --- | --- | --- | --- |');
    for (const word of items) {
      lines.push(`| ${mdEscape(word.text)} | ${mdEscape(word.start)} | ${mdEscape(word.end)} | ${mdEscape(word.speaker_display ?? '')} | ${mdEscape(word.confidence ?? '')} |`);
    }
    lines.push('');
  }

  return lines.join('\n').trim() + '\n';
}

function renderSpeakerAwareText(agentJson) {
  const utterances = Array.isArray(agentJson?.utterances) ? agentJson.utterances : [];
  if (!utterances.length) return String(agentJson?.transcript?.text ?? '');
  return utterances.map((u) => {
    const speaker = u.speaker_display ? `${u.speaker_display}: ` : '';
    return `[${u.start}] ${speaker}${u.text}`;
  }).join('\n');
}

function buildLlmInputFromAgentJson(agentJson, inputFormat = 'speaker-aware') {
  if (inputFormat === 'plain') return String(agentJson?.transcript?.text ?? '');
  if (inputFormat === 'markdown') return renderAgentJsonMarkdown(agentJson, { includePlainText: false });
  return renderSpeakerAwareText(agentJson);
}

function buildJsonSchemaResponseFormat(schemaArg, schemaNameOverride) {
  const parsed = deepClone(schemaArg);
  const wrapper = parsed?.json_schema
    ? parsed
    : {
      type: 'json_schema',
      json_schema: {
        name: String(schemaNameOverride ?? parsed?.name ?? 'structured_output'),
        strict: parsed?.strict ?? true,
        schema: parsed?.schema ?? parsed,
      },
    };
  return wrapper;
}

function extractLlmText(llmResult) {
  const content = llmResult?.choices?.[0]?.message?.content;
  if (typeof content === 'string') return content;
  if (Array.isArray(content)) {
    return content.map((item) => item?.text ?? '').join('\n');
  }
  return JSON.stringify(llmResult, null, 2);
}

function extractStructuredLlmOutput(llmResult) {
  const content = extractLlmText(llmResult);
  const parsed = safeJsonParse(content);
  if (parsed !== undefined) return parsed;
  return {
    message: content,
    raw_response: llmResult,
  };
}

async function resolveTranscriptLikeInput({
  input,
  sttBaseUrl,
  apiKey,
  pollMs,
  timeoutMs,
  quiet,
  allowFetchById,
  waitIfId = false,
}) {
  const expanded = expandHome(String(input));
  if (await fileExists(expanded)) {
    const raw = await fsp.readFile(expanded, 'utf8');
    const parsed = JSON.parse(raw);
    if (parsed?.schema_version && String(parsed.schema_version).startsWith('assemblyai-transcribe-agent-json/')) {
      return { kind: 'agent-json', agentJson: parsed, sourcePath: expanded };
    }
    return { kind: 'raw-transcript', transcript: parsed, sourcePath: expanded };
  }

  if (looksLikeJson(String(input))) {
    const parsed = JSON.parse(String(input));
    if (parsed?.schema_version && String(parsed.schema_version).startsWith('assemblyai-transcribe-agent-json/')) {
      return { kind: 'agent-json', agentJson: parsed, sourcePath: null };
    }
    return { kind: 'raw-transcript', transcript: parsed, sourcePath: null };
  }

  if (allowFetchById) {
    if (!apiKey) {
      throw new Error('Resolving a transcript id requires ASSEMBLYAI_API_KEY. For offline formatting, pass a local raw JSON or agent JSON file instead.');
    }
    const transcript = waitIfId
      ? await waitForTranscript({ baseUrl: sttBaseUrl, apiKey, id: input, pollMs, timeoutMs, quiet })
      : await getTranscript({ baseUrl: sttBaseUrl, apiKey, id: input, quiet });
    return { kind: 'raw-transcript', transcript, sourcePath: null };
  }

  throw new Error(`Could not resolve input: ${input}`);
}


function paragraphsToText(json) {
  const paras = Array.isArray(json?.paragraphs) ? json.paragraphs : [];
  return paras.map((p) => String(p?.text ?? '')).filter(Boolean).join('\n\n') + (paras.length ? '\n' : '');
}

function sentencesToText(json) {
  const sents = Array.isArray(json?.sentences) ? json.sentences : [];
  return sents.map((s) => String(s?.text ?? '')).filter(Boolean).join('\n') + (sents.length ? '\n' : '');
}

function renderModelsOutput(data, format = 'markdown') {
  if (format === 'json') return JSON.stringify(data, null, 2) + '\n';
  if (format === 'text') {
    const lines = [];
    for (const model of data.speech_models || []) {
      lines.push(`${model.id}: ${model.summary}`);
      lines.push(`  Recommended when: ${model.recommended_when.join('; ')}`);
      lines.push(`  Key features: ${model.features.join(', ')}`);
      lines.push('');
    }
    return lines.join('\n').trim() + '\n';
  }
  const lines = ['# AssemblyAI Speech Model Summary', ''];
  for (const model of data.speech_models || []) {
    lines.push(`## ${model.id}`);
    lines.push('');
    lines.push(`- Summary: ${model.summary}`);
    lines.push(`- Recommended when: ${model.recommended_when.join('; ')}`);
    if (model.supported_languages_note) lines.push(`- Languages: ${model.supported_languages_note}`);
    if (Array.isArray(model.features) && model.features.length) {
      lines.push(`- Key features: ${model.features.join(', ')}`);
    }
    if (model.keyterms_limit) lines.push(`- Keyterms limit: ${model.keyterms_limit}`);
    if (model.prompting) lines.push(`- Prompting: ${model.prompting}`);
    lines.push('');
  }
  if (data.routing_recipes?.length) {
    lines.push('## Routing Recipes');
    lines.push('');
    for (const recipe of data.routing_recipes) {
      lines.push(`- ${recipe.name}: ${recipe.description}`);
    }
    lines.push('');
  }
  return lines.join('\n').trim() + '\n';
}

function renderLanguagesOutput(capabilities, codes, { format = 'markdown', model, includeCodes = false } = {}) {
  const speechModels = capabilities?.speech_models ?? [];
  const filtered = model ? speechModels.filter((m) => m.id === model) : speechModels;

  if (format === 'json') {
    const payload = {
      models: filtered,
      accepted_language_codes: includeCodes ? codes : undefined,
    };
    return JSON.stringify(payload, null, 2) + '\n';
  }

  const lines = [];
  if (format === 'text') {
    for (const item of filtered) {
      lines.push(`${item.id}: ${item.supported_languages_note}`);
      if (item.language_accuracy_bands) {
        for (const [band, langs] of Object.entries(item.language_accuracy_bands)) {
          lines.push(`  ${band}: ${langs.join(', ')}`);
        }
      }
      lines.push('');
    }
    if (includeCodes) {
      lines.push(`Accepted transcript API language codes (${codes.codes.length}):`);
      lines.push(codes.codes.join(', '));
      lines.push('');
    }
    return lines.join('\n').trim() + '\n';
  }

  lines.push('# AssemblyAI Language Support Summary');
  lines.push('');
  for (const item of filtered) {
    lines.push(`## ${item.id}`);
    lines.push('');
    lines.push(`- ${item.supported_languages_note}`);
    if (Array.isArray(item.language_families) && item.language_families.length) {
      lines.push('- Supported language families / dialect notes:');
      for (const family of item.language_families) {
        lines.push(`  - ${family}`);
      }
    }
    if (item.language_accuracy_bands) {
      lines.push('- Universal-2 accuracy bands:');
      for (const [band, langs] of Object.entries(item.language_accuracy_bands)) {
        lines.push(`  - ${band}: ${langs.join(', ')}`);
      }
    }
    lines.push('');
  }
  if (includeCodes) {
    lines.push('## Accepted language_code values');
    lines.push('');
    lines.push(codes.codes.join(', '));
    lines.push('');
  } else {
    lines.push('Use `languages --codes --format json` for the full accepted language_code list.');
    lines.push('');
  }
  return lines.join('\n').trim() + '\n';
}

async function materialiseResolvedOutputs({ resolved, sttBaseUrl, llmBaseUrl, apiKey, flags, quiet, inputHint }) {
  if (resolved.kind === 'agent-json') {
    const manualMap = await parseSpeakerMapArg(flags['speaker-map']);
    const agentJson = applyManualSpeakerMapToAgentJson(resolved.agentJson, manualMap);
    return materialiseOutputBundleFromAgentJson({
      agentJson,
      rawTranscript: undefined,
      understandingResult: undefined,
      sttBaseUrl,
      llmBaseUrl,
      apiKey,
      flags,
      quiet,
      inputHint,
    });
  }
  return materialiseTranscriptOutputs({
    transcript: resolved.transcript,
    sttBaseUrl,
    llmBaseUrl,
    apiKey,
    flags,
    quiet,
    inputHint,
    understandingResult: undefined,
  });
}

async function materialiseTranscriptOutputs({ transcript, sttBaseUrl, llmBaseUrl, apiKey, flags, quiet, inputHint, understandingResult }) {
  const manualSpeakerMap = await parseSpeakerMapArg(flags['speaker-map']);
  const agentJson = normaliseTranscriptToAgentJson(transcript, {
    apiBaseUrl: sttBaseUrl,
    inputHint,
    manualSpeakerMap,
    includeWords: Boolean(flags['include-words']),
  });
  return materialiseOutputBundleFromAgentJson({
    agentJson,
    rawTranscript: transcript,
    understandingResult,
    sttBaseUrl,
    llmBaseUrl,
    apiKey,
    flags,
    quiet,
    inputHint,
  });
}

async function materialiseOutputBundleFromAgentJson({
  agentJson,
  rawTranscript,
  understandingResult,
  sttBaseUrl,
  llmBaseUrl,
  apiKey,
  flags,
  quiet,
  inputHint,
}) {
  const primaryExport = String(flags.export ?? 'markdown').toLowerCase();
  const includePlainText = Boolean(flags['include-plain-text']);
  const maxItems = parsePositiveInt(flags['max-items'], 50, '--max-items');
  const markdown = renderAgentJsonMarkdown(agentJson, { includePlainText, maxItems });
  const rawJsonText = rawTranscript ? JSON.stringify(rawTranscript, null, 2) + '\n' : undefined;
  const agentJsonText = JSON.stringify(agentJson, null, 2) + '\n';
  const textOut = String(agentJson?.transcript?.text ?? '').trim() + '\n';

  let paragraphsText;
  let sentencesText;
  let srtText;
  let vttText;

  const needsParagraphs = primaryExport === 'paragraphs' || flags['paragraphs-out'] || (flags['all-exports'] && flags['bundle-dir']);
  const needsSentences = primaryExport === 'sentences' || flags['sentences-out'] || (flags['all-exports'] && flags['bundle-dir']);
  const needsSrt = primaryExport === 'srt' || flags['srt-out'] || (flags['all-exports'] && flags['bundle-dir']);
  const needsVtt = primaryExport === 'vtt' || flags['vtt-out'] || (flags['all-exports'] && flags['bundle-dir']);
  const subtitleWidth = flags['chars-per-caption'] !== undefined
    ? parsePositiveInt(flags['chars-per-caption'], undefined, '--chars-per-caption')
    : undefined;

  if ((needsParagraphs || needsSentences || needsSrt || needsVtt) && !agentJson?.transcript?.id) {
    throw new Error('Extra endpoint exports require a transcript id');
  }
  if ((needsParagraphs || needsSentences || needsSrt || needsVtt) && !apiKey) {
    throw new Error('Paragraph/sentence/subtitle exports require ASSEMBLYAI_API_KEY because they call AssemblyAI endpoints.');
  }

  if (needsParagraphs) {
    const json = await getParagraphs({ baseUrl: sttBaseUrl, apiKey, id: agentJson.transcript.id });
    paragraphsText = paragraphsToText(json);
  }
  if (needsSentences) {
    const json = await getSentences({ baseUrl: sttBaseUrl, apiKey, id: agentJson.transcript.id });
    sentencesText = sentencesToText(json);
  }
  if (needsSrt) {
    srtText = await getSubtitles({ baseUrl: sttBaseUrl, apiKey, id: agentJson.transcript.id, subtitleFormat: 'srt', charsPerCaption: subtitleWidth });
  }
  if (needsVtt) {
    vttText = await getSubtitles({ baseUrl: sttBaseUrl, apiKey, id: agentJson.transcript.id, subtitleFormat: 'vtt', charsPerCaption: subtitleWidth });
  }

  let primaryOutput;
  if (primaryExport === 'markdown') primaryOutput = markdown;
  else if (primaryExport === 'agent-json') primaryOutput = agentJsonText;
  else if (primaryExport === 'json' || primaryExport === 'raw-json') primaryOutput = rawJsonText ?? agentJsonText;
  else if (primaryExport === 'text') primaryOutput = textOut;
  else if (primaryExport === 'paragraphs') primaryOutput = paragraphsText ?? '';
  else if (primaryExport === 'sentences') primaryOutput = sentencesText ?? '';
  else if (primaryExport === 'srt') primaryOutput = srtText ?? '';
  else if (primaryExport === 'vtt') primaryOutput = vttText ?? '';
  else if (primaryExport === 'manifest') primaryOutput = ''; // filled later after bundle generation
  else throw new Error(`Unknown --export kind: ${primaryExport}`);

  const bundle = {
    agentJson,
    rawTranscript,
    understandingResult,
    sttBaseUrl,
    llmBaseUrl,
    inputHint,
    primaryExport,
    primaryOutput,
    files: {
      markdown,
      agent_json: agentJsonText,
      raw_json: rawJsonText,
      text: textOut,
      paragraphs: paragraphsText,
      sentences: sentencesText,
      srt: srtText,
      vtt: vttText,
      understanding_json: understandingResult ? JSON.stringify(understandingResult, null, 2) + '\n' : undefined,
    },
  };

  if (flags['markdown-out']) await writeTextFile(expandHome(String(flags['markdown-out'])), markdown);
  if (flags['agent-json-out']) await writeTextFile(expandHome(String(flags['agent-json-out'])), agentJsonText);
  if (flags['raw-json-out'] && rawJsonText !== undefined) await writeTextFile(expandHome(String(flags['raw-json-out'])), rawJsonText);
  if (flags['text-out']) await writeTextFile(expandHome(String(flags['text-out'])), textOut);
  if (flags['paragraphs-out'] && paragraphsText !== undefined) await writeTextFile(expandHome(String(flags['paragraphs-out'])), paragraphsText);
  if (flags['sentences-out'] && sentencesText !== undefined) await writeTextFile(expandHome(String(flags['sentences-out'])), sentencesText);
  if (flags['srt-out'] && srtText !== undefined) await writeTextFile(expandHome(String(flags['srt-out'])), srtText);
  if (flags['vtt-out'] && vttText !== undefined) await writeTextFile(expandHome(String(flags['vtt-out'])), vttText);
  if (flags['understanding-json-out'] && bundle.files.understanding_json !== undefined) {
    await writeTextFile(expandHome(String(flags['understanding-json-out'])), bundle.files.understanding_json);
  }

  if (flags['bundle-dir']) {
    bundle.bundleManifest = await writeBundleDir(bundle, expandHome(String(flags['bundle-dir'])), flags, quiet);
    if (primaryExport === 'manifest') {
      bundle.primaryOutput = JSON.stringify(bundle.bundleManifest, null, 2) + '\n';
    }
  } else if (flags['all-exports']) {
    throw new Error('--all-exports currently requires --bundle-dir');
  }

  return bundle;
}

function sanitizeBasename(name) {
  return String(name || '')
    .trim()
    .replace(/[^\w.-]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/-{2,}/g, '-')
    || 'assemblyai-transcript';
}

async function writeBundleDir(bundle, bundleDir, flags, quiet) {
  await fsp.mkdir(bundleDir, { recursive: true });
  const transcriptId = bundle?.agentJson?.transcript?.id ?? 'transcript';
  const inferredBase = flags.basename
    ? sanitizeBasename(flags.basename)
    : sanitizeBasename(path.basename(String(bundle.inputHint || transcriptId), path.extname(String(bundle.inputHint || transcriptId))) || transcriptId);

  const manifest = {
    schema_version: 'assemblyai-transcribe-bundle-manifest/v2',
    generated_at: new Date().toISOString(),
    transcript_id: transcriptId,
    region: bundle?.agentJson?.source?.region ?? null,
    base_name: inferredBase,
    files: {},
  };

  const mapping = {
    markdown: `${inferredBase}.transcript.md`,
    agent_json: `${inferredBase}.agent.json`,
    raw_json: `${inferredBase}.raw.json`,
    text: `${inferredBase}.txt`,
    paragraphs: `${inferredBase}.paragraphs.txt`,
    sentences: `${inferredBase}.sentences.txt`,
    srt: `${inferredBase}.srt`,
    vtt: `${inferredBase}.vtt`,
    understanding_json: `${inferredBase}.understanding.json`,
  };

  for (const [key, fileName] of Object.entries(mapping)) {
    const content = bundle.files[key];
    if (content === undefined || content === null || content === '') continue;
    const outPath = path.join(bundleDir, fileName);
    await writeTextFile(outPath, content);
    manifest.files[key] = fileName;
  }

  const manifestName = `${inferredBase}.manifest.json`;
  const manifestPath = path.join(bundleDir, manifestName);
  await writeTextFile(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
  manifest.files.manifest = manifestName;
  stderr(`Wrote bundle to ${bundleDir}`, quiet);
  return manifest;
}

async function emitBundle(bundle, flags, quiet) {
  const outPath = flags.out ? expandHome(String(flags.out)) : '-';
  await writePrimaryOutput(bundle.primaryOutput, outPath);
}

async function writeTextFile(p, content) {
  const outPath = expandHome(String(p));
  await fsp.mkdir(path.dirname(outPath), { recursive: true });
  const text = String(content ?? '');
  await fsp.writeFile(outPath, text.endsWith('\n') ? text : `${text}\n`, 'utf8');
}

async function writePrimaryOutput(content, out) {
  const outPath = out ? expandHome(String(out)) : '-';
  const text = String(content ?? '');
  if (outPath === '-' || outPath === '') {
    process.stdout.write(text.endsWith('\n') ? text : `${text}\n`);
    return;
  }
  await writeTextFile(outPath, text);
}

if (process.argv[1] && path.resolve(process.argv[1]) === __filename) {
  main().catch((err) => {
    const message = err?.stack ?? err?.message ?? String(err);
    process.stderr.write(`${message}\n`);
    process.exit(1);
  });
}
