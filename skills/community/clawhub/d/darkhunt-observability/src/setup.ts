import * as readline from 'node:readline/promises';
import { stdin, stdout } from 'node:process';
import type { PayloadMode } from './types.js';
import { serializeConfig, validate } from './config.js';
import { getBuiltinModelNames, getBuiltinPricing, resolveModel } from './pricing.js';

// ── ANSI helpers ────────────────────────────────────────────────

const dim = (s: string) => `\x1b[2m${s}\x1b[0m`;
const bold = (s: string) => `\x1b[1m${s}\x1b[0m`;
const green = (s: string) => `\x1b[32m${s}\x1b[0m`;
const yellow = (s: string) => `\x1b[33m${s}\x1b[0m`;
const cyan = (s: string) => `\x1b[36m${s}\x1b[0m`;

// ── Interactive setup wizard ─────────────────────────────────────

export interface SetupResult {
  saved: boolean;
  config: Record<string, unknown>;
}

export async function runSetupWizard(
  existingConfig?: Record<string, unknown>,
): Promise<SetupResult> {
  const rl = readline.createInterface({ input: stdin, output: stdout });

  try {
    console.log('');
    console.log(`  ${bold('Trace Hub Telemetry')} ${dim('— Setup Wizard')}`);
    console.log(dim('  ─'.repeat(24)));
    console.log('');

    // ── Step 1: Export target ──────────────────────────────────

    const target = await selectOption(rl, 'Where should telemetry be sent?', [
      { key: '1', label: `Darkhunt Observability ${dim('(production)')}`, value: 'tracehub' },
      { key: '2', label: `Local OTel collector ${dim('(troubleshooting)')}`, value: 'local' },
      { key: '3', label: 'Custom endpoint', value: 'custom' },
    ], '1');

    let tracesEndpoint: string;
    let logsEndpoint: string | undefined;
    let headers: Record<string, string> | undefined;

    if (target === 'local') {
      console.log('');
      const baseUrl = await ask(rl, 'Collector base URL', 'http://localhost:4318');
      tracesEndpoint = `${baseUrl.replace(/\/+$/, '')}/v1/traces`;
      logsEndpoint = `${baseUrl.replace(/\/+$/, '')}/v1/logs`;
    } else if (target === 'tracehub') {
      console.log('');
      const baseUrl = await ask(rl, 'Trace Hub API base URL', 'https://api.darkhunt.ai/trace-hub');
      const tenantId = await ask(rl, 'Tenant ID');
      const base = baseUrl.replace(/\/+$/, '');
      tracesEndpoint = `${base}/otlp/t/${tenantId}/v1/traces`;
      logsEndpoint = `${base}/otlp/t/${tenantId}/v1/logs`;

      console.log('');
      const workspaceId = await ask(rl, 'X-Workspace-Id');
      const applicationId = await ask(rl, 'X-Application-Id');

      console.log('');
      console.log(`  ${dim('Paste the Bearer token from your API key:')}`);
      const authToken = await ask(rl, 'Authorization (Bearer token)');

      headers = {};
      if (authToken) headers['Authorization'] = authToken.startsWith('Bearer ') ? authToken : `Bearer ${authToken}`;
      if (workspaceId) headers['X-Workspace-Id'] = workspaceId;
      if (applicationId) headers['X-Application-Id'] = applicationId;
      if (Object.keys(headers).length === 0) headers = undefined;
    } else {
      console.log('');
      tracesEndpoint = await ask(rl, 'Traces endpoint URL');
      const wantLogs = await confirm(rl, 'Configure a logs endpoint too?', false);
      logsEndpoint = wantLogs ? await ask(rl, 'Logs endpoint URL') : undefined;

      const wantHeaders = await confirm(rl, 'Add HTTP headers?', false);
      if (wantHeaders) {
        headers = {};
        console.log(`  ${dim('Enter headers one at a time. Leave name blank to finish.')}`);
        while (true) {
          const key = await ask(rl, '  Header name', '', true);
          if (!key) break;
          const value = await ask(rl, `  ${key}`);
          headers[key] = value;
        }
        if (Object.keys(headers).length === 0) headers = undefined;
      }
    }

    // ── Step 2: Payload mode ──────────────────────────────────

    console.log('');
    const payloadMode = await selectOption(rl, 'How much content should spans include?', [
      { key: '1', label: `metadata ${dim('(default)')} — tokens, cost, duration, tool names. No prompts or outputs.`, value: 'metadata' as PayloadMode },
      { key: '2', label: `debug    ${dim('— metadata + truncated content (500 chars).')}`, value: 'debug' as PayloadMode },
      { key: '3', label: `full     ${dim('— includes everything subject to size limits.')}`, value: 'full' as PayloadMode },
    ], '1');

    // ── Step 3: Model mapping (Bedrock ARN → friendly name) ───

    let modelMap: Record<string, string> | undefined;
    let modelPricing: Record<string, { input: number; output: number; cacheRead?: number; cacheWrite?: number }> | undefined;

    // Carry over existing values
    if (existingConfig) {
      if (typeof existingConfig.model_map === 'object' && existingConfig.model_map !== null) {
        modelMap = { ...existingConfig.model_map as Record<string, string> };
      }
      if (typeof existingConfig.model_pricing === 'object' && existingConfig.model_pricing !== null) {
        modelPricing = { ...existingConfig.model_pricing as Record<string, { input: number; output: number }> };
      }
    }

    console.log('');
    const wantModels = await confirm(rl, 'Configure Bedrock model mapping & pricing?', false);

    if (wantModels) {
      const result = await runModelWizard(rl, modelMap, modelPricing);
      modelMap = result.modelMap;
      modelPricing = result.modelPricing;
    }

    // ── Build + validate config ───────────────────────────────

    const config = validate({
      traces_endpoint: tracesEndpoint,
      logs_endpoint: logsEndpoint,
      headers,
      payload_mode: payloadMode,
      enabled: true,
      model_map: modelMap,
      model_pricing: modelPricing,
    });

    const serialized = serializeConfig(config);

    // ── Summary ───────────────────────────────────────────────

    console.log('');
    console.log(dim('  ─'.repeat(24)));
    console.log(`  ${bold('Summary')}`);
    console.log('');
    console.log(`  traces_endpoint  ${cyan(config.traces_endpoint)}`);
    if (config.logs_endpoint) {
      console.log(`  logs_endpoint    ${cyan(config.logs_endpoint)}`);
    }
    if (config.headers) {
      for (const [k, v] of Object.entries(config.headers)) {
        const display = k === 'Authorization' ? v.slice(0, 15) + '...' : v;
        console.log(`  ${k}  ${dim(display)}`);
      }
    }
    console.log(`  payload_mode     ${cyan(config.payload_mode)}`);
    if (config.model_map && Object.keys(config.model_map).length > 0) {
      console.log(`  model_map        ${cyan(Object.keys(config.model_map).length + ' mapping(s)')}`);
      for (const [k, v] of Object.entries(config.model_map)) {
        console.log(`    ${dim(k)} → ${cyan(v)}`);
      }
    }
    if (config.model_pricing && Object.keys(config.model_pricing).length > 0) {
      console.log(`  model_pricing    ${cyan(Object.keys(config.model_pricing).length + ' override(s)')}`);
      for (const [k, v] of Object.entries(config.model_pricing)) {
        console.log(`    ${dim(k)}: $${v.input}/$${v.output} per 1M tokens`);
      }
    }
    console.log('');

    const ok = await confirm(rl, 'Save this configuration?', true);
    if (!ok) {
      console.log('');
      console.log(yellow('  Setup cancelled. No changes were made.'));
      console.log('');
      return { saved: false, config: existingConfig ?? {} };
    }

    return { saved: true, config: serialized };
  } finally {
    rl.close();
  }
}

// ── Model mapping & pricing wizard ──────────────────────────────

interface ModelWizardResult {
  modelMap: Record<string, string> | undefined;
  modelPricing: Record<string, { input: number; output: number; cacheRead?: number; cacheWrite?: number }> | undefined;
}

async function runModelWizard(
  rl: readline.Interface,
  existingModelMap?: Record<string, string>,
  existingPricing?: Record<string, { input: number; output: number; cacheRead?: number; cacheWrite?: number }>,
): Promise<ModelWizardResult> {
  const modelMap: Record<string, string> = { ...existingModelMap };
  const modelPricing: Record<string, { input: number; output: number; cacheRead?: number; cacheWrite?: number }> = { ...existingPricing };

  console.log('');
  console.log(dim('  ─'.repeat(24)));
  console.log(`  ${bold('Bedrock Model Mapping & Pricing')}`);
  console.log('');

  // Explain ARN structure
  console.log(`  ${dim('Bedrock models are identified by ARNs (Amazon Resource Names):')}`);
  console.log('');
  console.log(`    ${cyan('arn:aws:bedrock')}:${green('eu-west-1')}:${dim('482397833370')}:${yellow('application-inference-profile')}/${bold('ekadx6q1kayx')}`);
  console.log('');
  console.log(`    ${cyan('arn:aws:bedrock')}  — AWS service prefix (always the same)`);
  console.log(`    ${green('eu-west-1')}        — Region where the model runs`);
  console.log(`    ${dim('482397833370')}     — Your AWS account ID`);
  console.log(`    ${yellow('application-inference-profile')} — Resource type`);
  console.log(`    ${bold('ekadx6q1kayx')}     — Profile ID (unique to your deployment)`);
  console.log('');
  console.log(`  ${dim('The profile ID is opaque — it doesn\'t contain the model name.')}`);
  console.log(`  ${dim('You need to map it so the plugin knows which model (and pricing) to use.')}`);
  console.log('');
  console.log(`  ${dim('The plugin auto-detects model names when the ARN contains them')}`);
  console.log(`  ${dim('(e.g. anthropic.claude-sonnet-4-6), but inference profiles need manual mapping.')}`);
  console.log('');

  // Show existing mappings
  if (Object.keys(modelMap).length > 0) {
    console.log(`  ${bold('Current mappings:')}`);
    for (const [k, v] of Object.entries(modelMap)) {
      console.log(`    ${dim(k)} → ${cyan(v)}`);
    }
    console.log('');
  }

  // Main model wizard menu loop
  let done = false;
  while (!done) {
    const action = await selectOption(rl, 'What would you like to do?', [
      { key: '1', label: `Map a Bedrock ARN or profile ID to a model name`, value: 'map' },
      { key: '2', label: `Adjust pricing for a model`, value: 'pricing' },
      { key: '3', label: `Show built-in models & prices`, value: 'list' },
      { key: '4', label: `Test ARN resolution ${dim('(see how an ARN would be resolved)')}`, value: 'test' },
      { key: '5', label: `Remove a mapping or pricing override`, value: 'remove' },
      { key: '6', label: `Done — continue setup`, value: 'done' },
    ], '6');

    switch (action) {
      case 'map':
        await wizardMapModel(rl, modelMap);
        break;
      case 'pricing':
        await wizardAdjustPricing(rl, modelPricing);
        break;
      case 'list':
        wizardShowBuiltinModels();
        break;
      case 'test':
        await wizardTestResolution(rl, modelMap, modelPricing);
        break;
      case 'remove':
        await wizardRemoveEntry(rl, modelMap, modelPricing);
        break;
      case 'done':
        done = true;
        break;
    }

    if (!done) console.log('');
  }

  return {
    modelMap: Object.keys(modelMap).length > 0 ? modelMap : undefined,
    modelPricing: Object.keys(modelPricing).length > 0 ? modelPricing : undefined,
  };
}

async function wizardMapModel(
  rl: readline.Interface,
  modelMap: Record<string, string>,
): Promise<void> {
  console.log('');
  console.log(`  ${dim('Enter a Bedrock ARN, profile ID, or any substring to match against.')}`);
  console.log(`  ${dim('Example: "ekadx6q1kayx" or the full ARN.')}`);
  console.log('');

  const pattern = await ask(rl, 'ARN or profile ID', '', true);
  if (!pattern) return;

  // Extract just the profile ID if a full ARN was pasted
  let key = pattern.trim();
  const arnProfileMatch = key.match(/application-inference-profile\/([a-z0-9]+)$/i);
  if (arnProfileMatch) {
    const profileId = arnProfileMatch[1];
    console.log(`  ${dim(`Extracted profile ID: ${profileId}`)}`);
    const useShort = await confirm(rl, `Use just the profile ID "${profileId}" as the mapping key?`, true);
    if (useShort) key = profileId;
  }

  console.log('');
  console.log(`  ${dim('Choose the model this maps to. You can pick from built-in models or type a custom name.')}`);
  console.log('');

  const builtinNames = getBuiltinModelNames().filter(n => !n.includes(':'));
  const modelName = await askWithSuggestions(rl, 'Model name', builtinNames);
  if (!modelName) return;

  modelMap[key] = modelName;

  const pricing = getBuiltinPricing(modelName);
  if (pricing) {
    console.log(`  ${green('✓')} Mapped ${dim(key)} → ${cyan(modelName)} ${dim(`($${pricing.inputPer1M}/$${pricing.outputPer1M} per 1M tokens)`)}`);
  } else {
    console.log(`  ${green('✓')} Mapped ${dim(key)} → ${cyan(modelName)} ${yellow('(no built-in pricing — add custom pricing in next step)')}`);
  }
}

async function wizardAdjustPricing(
  rl: readline.Interface,
  modelPricing: Record<string, { input: number; output: number; cacheRead?: number; cacheWrite?: number }>,
): Promise<void> {
  console.log('');
  console.log(`  ${dim('Override or add pricing for a model. Prices are per 1M tokens in USD.')}`);
  console.log(`  ${dim('This overrides built-in prices. Use "model:region" for region-specific pricing.')}`);
  console.log('');

  const modelName = await ask(rl, 'Model name (e.g. claude-sonnet-4-6 or claude-haiku-4-5:eu-west-1)', '', true);
  if (!modelName) return;

  // Show current pricing if available
  const existing = modelPricing[modelName];
  const builtin = getBuiltinPricing(modelName);
  if (existing) {
    console.log(`  ${dim(`Current override: $${existing.input}/$${existing.output} per 1M tokens`)}`);
  } else if (builtin) {
    console.log(`  ${dim(`Built-in price: $${builtin.inputPer1M}/$${builtin.outputPer1M} per 1M tokens`)}`);
  }

  console.log('');
  const inputPrice = await askNumber(rl, 'Input price per 1M tokens ($)', existing?.input ?? builtin?.inputPer1M);
  if (inputPrice === undefined) return;

  const outputPrice = await askNumber(rl, 'Output price per 1M tokens ($)', existing?.output ?? builtin?.outputPer1M);
  if (outputPrice === undefined) return;

  const entry: { input: number; output: number; cacheRead?: number; cacheWrite?: number } = {
    input: inputPrice,
    output: outputPrice,
  };

  const wantCache = await confirm(rl, 'Set custom cache pricing? (default: 10% input for read, 125% input for write)', false);
  if (wantCache) {
    const cacheRead = await askNumber(rl, 'Cache read price per 1M tokens ($)', existing?.cacheRead ?? inputPrice * 0.1);
    if (cacheRead !== undefined) entry.cacheRead = cacheRead;
    const cacheWrite = await askNumber(rl, 'Cache write price per 1M tokens ($)', existing?.cacheWrite ?? inputPrice * 1.25);
    if (cacheWrite !== undefined) entry.cacheWrite = cacheWrite;
  }

  modelPricing[modelName] = entry;
  console.log(`  ${green('✓')} ${cyan(modelName)}: $${entry.input}/$${entry.output} per 1M tokens`);
}

function wizardShowBuiltinModels(): void {
  console.log('');
  console.log(`  ${bold('Built-in Bedrock Models & Pricing')} ${dim('(per 1M tokens, USD)')}`);
  console.log('');

  const names = getBuiltinModelNames();
  let lastFamily = '';

  for (const name of names) {
    const pricing = getBuiltinPricing(name);
    if (!pricing) continue;

    // Detect family for grouping
    const family = name.split('-')[0] + (name.includes(':') ? '' : '');
    if (family !== lastFamily) {
      if (lastFamily) console.log('');
      lastFamily = family;
    }

    const cache = pricing.cacheReadPer1M
      ? dim(` (cache: $${pricing.cacheReadPer1M} read, $${pricing.cacheWritePer1M} write)`)
      : '';
    const regionTag = name.includes(':') ? yellow(' [regional]') : '';
    console.log(`    ${cyan(name.padEnd(32))} $${String(pricing.inputPer1M).padEnd(6)} / $${pricing.outputPer1M}${cache}${regionTag}`);
  }
  console.log('');
}

async function wizardTestResolution(
  rl: readline.Interface,
  modelMap: Record<string, string>,
  modelPricing: Record<string, { input: number; output: number; cacheRead?: number; cacheWrite?: number }>,
): Promise<void> {
  console.log('');
  console.log(`  ${dim('Paste an ARN or model name to see how it would be resolved.')}`);
  console.log('');

  const input = await ask(rl, 'ARN or model name', '', true);
  if (!input) return;

  const resolved = resolveModel(input.trim(), modelMap, modelPricing);
  console.log('');
  console.log(`  ${bold('Resolution result:')}`);
  console.log(`    Friendly name: ${cyan(resolved.friendlyName)}`);
  if (resolved.rawModel !== resolved.friendlyName) {
    console.log(`    Raw model:     ${dim(resolved.rawModel)}`);
  }
  if (resolved.region) {
    console.log(`    Region:        ${green(resolved.region)}`);
  }
  if (resolved.pricing) {
    console.log(`    Input price:   $${resolved.pricing.inputPer1M} / 1M tokens`);
    console.log(`    Output price:  $${resolved.pricing.outputPer1M} / 1M tokens`);
    if (resolved.pricing.cacheReadPer1M) {
      console.log(`    Cache read:    $${resolved.pricing.cacheReadPer1M} / 1M tokens`);
      console.log(`    Cache write:   $${resolved.pricing.cacheWritePer1M} / 1M tokens`);
    }
  } else {
    console.log(`    Pricing:       ${yellow('not found — add via model mapping or pricing override')}`);
  }
}

async function wizardRemoveEntry(
  rl: readline.Interface,
  modelMap: Record<string, string>,
  modelPricing: Record<string, { input: number; output: number; cacheRead?: number; cacheWrite?: number }>,
): Promise<void> {
  const mapKeys = Object.keys(modelMap);
  const priceKeys = Object.keys(modelPricing);

  if (mapKeys.length === 0 && priceKeys.length === 0) {
    console.log(`  ${dim('No mappings or pricing overrides to remove.')}`);
    return;
  }

  console.log('');
  if (mapKeys.length > 0) {
    console.log(`  ${bold('Model mappings:')}`);
    mapKeys.forEach((k, i) => console.log(`    ${green(String(i + 1))}) ${dim(k)} → ${cyan(modelMap[k])}`));
  }
  if (priceKeys.length > 0) {
    const offset = mapKeys.length;
    console.log(`  ${bold('Pricing overrides:')}`);
    priceKeys.forEach((k, i) => {
      const v = modelPricing[k];
      console.log(`    ${green(String(offset + i + 1))}) ${cyan(k)}: $${v.input}/$${v.output}`);
    });
  }
  console.log('');

  const allKeys = [...mapKeys.map(k => ({ type: 'map' as const, key: k })), ...priceKeys.map(k => ({ type: 'price' as const, key: k }))];
  const choice = await ask(rl, 'Enter number to remove (or blank to cancel)', '', true);
  if (!choice) return;

  const idx = parseInt(choice, 10) - 1;
  if (isNaN(idx) || idx < 0 || idx >= allKeys.length) {
    console.log(`  ${yellow('Invalid choice.')}`);
    return;
  }

  const entry = allKeys[idx];
  if (entry.type === 'map') {
    delete modelMap[entry.key];
    console.log(`  ${green('✓')} Removed mapping: ${dim(entry.key)}`);
  } else {
    delete modelPricing[entry.key];
    console.log(`  ${green('✓')} Removed pricing override: ${dim(entry.key)}`);
  }
}

// ── Extended prompt helpers ──────────────────────────────────────

async function askNumber(
  rl: readline.Interface,
  prompt: string,
  defaultValue?: number,
): Promise<number | undefined> {
  const defaultStr = defaultValue !== undefined ? String(defaultValue) : '';
  const raw = await ask(rl, prompt, defaultStr, true);
  if (!raw) return defaultValue;
  const num = parseFloat(raw);
  if (isNaN(num) || num < 0) {
    console.log(`  ${yellow('Invalid number, try again.')}`);
    return askNumber(rl, prompt, defaultValue);
  }
  return num;
}

async function askWithSuggestions(
  rl: readline.Interface,
  prompt: string,
  suggestions: string[],
): Promise<string> {
  // Show a few popular ones
  const popular = suggestions.filter(s =>
    s.startsWith('claude-') && !s.includes('3-sonnet') && !s.includes('3-haiku') && !s.includes('3-opus'),
  ).slice(0, 5);
  const others = suggestions.filter(s => !popular.includes(s)).slice(0, 5);

  if (popular.length > 0) {
    console.log(`  ${dim('Popular:')} ${popular.map(s => cyan(s)).join(', ')}`);
  }
  if (others.length > 0) {
    console.log(`  ${dim('Others:')}  ${others.map(s => cyan(s)).join(', ')}`);
  }
  console.log(`  ${dim('Or type any custom model name.')}`);
  console.log('');

  return ask(rl, prompt);
}

// ── Prompt helpers ───────────────────────────────────────────────

async function ask(
  rl: readline.Interface,
  prompt: string,
  defaultValue?: string,
  optional?: boolean,
): Promise<string> {
  const suffix = defaultValue ? ` ${dim(`[${defaultValue}]`)}` : '';
  const answer = await rl.question(`  ${prompt}${suffix}: `);
  const value = answer.trim() || defaultValue || '';
  if (!value && !optional && !defaultValue) {
    return ask(rl, prompt, defaultValue, optional);
  }
  return value;
}

async function confirm(
  rl: readline.Interface,
  prompt: string,
  defaultValue: boolean,
): Promise<boolean> {
  const hint = dim(defaultValue ? '[Y/n]' : '[y/N]');
  const answer = await rl.question(`  ${prompt} ${hint} `);
  const trimmed = answer.trim().toLowerCase();
  if (!trimmed) return defaultValue;
  return trimmed === 'y' || trimmed === 'yes';
}

interface SelectOption<T> {
  key: string;
  label: string;
  value: T;
}

async function selectOption<T>(
  rl: readline.Interface,
  prompt: string,
  options: SelectOption<T>[],
  defaultKey?: string,
): Promise<T> {
  console.log(`  ${prompt}`);
  console.log('');
  for (const opt of options) {
    console.log(`    ${green(opt.key)}) ${opt.label}`);
  }
  console.log('');
  const suffix = defaultKey ? ` ${dim(`[${defaultKey}]`)}` : '';
  const answer = await rl.question(`  ${dim('>')}${suffix} `);
  const key = answer.trim() || defaultKey;
  const match = options.find(o => o.key === key);
  if (!match) {
    console.log(`  ${yellow('Invalid choice, try again.')}`);
    return selectOption(rl, prompt, options, defaultKey);
  }
  return match.value;
}
