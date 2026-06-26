import * as fs from 'node:fs';
import * as path from 'node:path';
import * as os from 'node:os';
import { runSetupWizard } from './setup.js';

const PLUGIN_ID = 'darkhunt-observability';

/** Minimal Commander-like interface — the real Commander is provided by OpenClaw at runtime */
interface CommandLike {
  command(name: string): CommandLike;
  description(desc: string): CommandLike;
  action(fn: (...args: any[]) => any): CommandLike;
}

interface CliContext {
  program: CommandLike;
  config: Record<string, unknown>;
  logger: { info: (...args: unknown[]) => void; error: (...args: unknown[]) => void };
}

export function registerTracehubCli(ctx: CliContext): void {
  const cmd = ctx.program
    .command('tracehub')
    .description('Trace Hub telemetry plugin');

  // ── tracehub setup ──────────────────────────────────────────────

  cmd
    .command('setup')
    .description('Interactive setup wizard for Trace Hub telemetry')
    .action(async () => {
      const existing = getPluginConfig(ctx.config);
      const result = await runSetupWizard(existing);

      if (!result.saved) return;

      // Auto-save to openclaw.json
      try {
        savePluginConfig(result.config);
        printRestartBanner();
      } catch (err: any) {
        console.log('');
        console.log('  Could not auto-save configuration:');
        console.log(`  ${err.message}`);
        console.log('');
        console.log('  You can apply it manually — paste this JSON into your openclaw.json at');
        console.log(`  plugins.entries.${PLUGIN_ID}.config:`);
        console.log('');
        console.log(JSON.stringify(result.config, null, 2));
        console.log('');
      }
    });

  // ── tracehub config ─────────────────────────────────────────────

  cmd
    .command('config')
    .description('Show current Trace Hub telemetry configuration')
    .action(() => {
      const pluginConfig = getPluginConfig(ctx.config);
      if (!pluginConfig || Object.keys(pluginConfig).length === 0) {
        console.log('No configuration found. Run "openclaw tracehub setup" to configure.');
        return;
      }
      console.log(JSON.stringify(pluginConfig, null, 2));
    });

  // ── tracehub set <key> <value> ────────────────────────────────

  cmd
    .command('set <key> <value>')
    .description('Update a single config field (e.g. "set payload_mode full")')
    .action((key: string, value: string) => {
      const pluginConfig = getPluginConfig(ctx.config) ?? {};

      const parsed = parseValue(value);
      setNestedKey(pluginConfig, key, parsed);

      try {
        savePluginConfig(pluginConfig);
        const dim = (s: string) => `\x1b[2m${s}\x1b[0m`;
        const green = (s: string) => `\x1b[32m${s}\x1b[0m`;
        console.log('');
        console.log(green(`  ${key} = ${JSON.stringify(parsed)}`));
        printRestartBanner();
      } catch (err: any) {
        console.error(`  Could not save: ${err.message}`);
      }
    });

  // ── tracehub status ─────────────────────────────────────────────

  cmd
    .command('status')
    .description('Show plugin status and connection info')
    .action(() => {
      const pluginConfig = getPluginConfig(ctx.config);
      const entry = getPluginEntry(ctx.config);

      console.log('');
      console.log('Trace Hub Telemetry Plugin');
      console.log('─'.repeat(40));

      if (!entry) {
        console.log('Status:    not installed');
        return;
      }

      console.log(`Status:    ${entry.enabled !== false ? 'enabled' : 'disabled'}`);

      if (pluginConfig) {
        const cfg = pluginConfig as Record<string, unknown>;
        console.log(`Traces:    ${cfg.traces_endpoint ?? 'not configured'}`);
        if (cfg.logs_endpoint) console.log(`Logs:      ${cfg.logs_endpoint}`);
        console.log(`Mode:      ${cfg.payload_mode ?? 'metadata'}`);
        const headers = cfg.headers as Record<string, string> | undefined;
        if (headers) {
          console.log(`Auth:      ${headers.Authorization ? 'configured' : 'none'}`);
          if (headers['X-Workspace-Id']) console.log(`Workspace: ${headers['X-Workspace-Id']}`);
          if (headers['X-Application-Id']) console.log(`App:       ${headers['X-Application-Id']}`);
        }
        console.log(`Debug:     ${cfg.debug ? 'enabled' : 'disabled'}`);
      } else {
        console.log('Config:    not configured — run "openclaw tracehub setup"');
      }
      console.log('');
    });
}

// ── Config file I/O ─────────────────────────────────────────────

function getConfigPath(): string {
  return path.join(os.homedir(), '.openclaw', 'openclaw.json');
}

function savePluginConfig(pluginConfig: Record<string, unknown>): void {
  const configPath = getConfigPath();
  const raw = fs.readFileSync(configPath, 'utf-8');
  const config = JSON.parse(raw);

  // Ensure path exists: plugins.entries.<PLUGIN_ID>.config
  if (!config.plugins) config.plugins = {};
  if (!config.plugins.entries) config.plugins.entries = {};
  if (!config.plugins.entries[PLUGIN_ID]) config.plugins.entries[PLUGIN_ID] = { enabled: true };

  config.plugins.entries[PLUGIN_ID].config = pluginConfig;

  // Create backup before writing
  const backupPath = configPath + '.bak';
  fs.copyFileSync(configPath, backupPath);

  fs.writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n', 'utf-8');
}

function printRestartBanner(): void {
  const red = (s: string) => `\x1b[31m${s}\x1b[0m`;
  const bold = (s: string) => `\x1b[1m${s}\x1b[0m`;
  const dim = (s: string) => `\x1b[2m${s}\x1b[0m`;
  const green = (s: string) => `\x1b[32m${s}\x1b[0m`;

  console.log('');
  console.log(green('  Configuration saved to ~/.openclaw/openclaw.json'));
  console.log('');
  console.log(red('  ┌──────────────────────────────────────────────────┐'));
  console.log(red('  │                                                  │'));
  console.log(red(`  │  ${bold('Restart the gateway to apply changes:')}             │`));
  console.log(red('  │                                                  │'));
  console.log(red(`  │    ${bold('openclaw gateway restart')}                        │`));
  console.log(red('  │                                                  │'));
  console.log(red('  └──────────────────────────────────────────────────┘'));
  console.log('');
  console.log(dim('  Run "openclaw tracehub setup" anytime to reconfigure.'));
  console.log('');
}

// ── Config helpers ──────────────────────────────────────────────

function getPluginEntry(config: Record<string, unknown>): Record<string, unknown> | undefined {
  const plugins = config.plugins as Record<string, unknown> | undefined;
  const entries = plugins?.entries as Record<string, unknown> | undefined;
  return entries?.[PLUGIN_ID] as Record<string, unknown> | undefined;
}

function getPluginConfig(config: Record<string, unknown>): Record<string, unknown> | undefined {
  const entry = getPluginEntry(config);
  return entry?.config as Record<string, unknown> | undefined;
}

// ── Value parsing + nested key helpers ──────────────────────────

function parseValue(raw: string): string | number | boolean {
  if (raw === 'true') return true;
  if (raw === 'false') return false;
  const num = Number(raw);
  if (!isNaN(num) && raw.trim() !== '') return num;
  return raw;
}

function setNestedKey(obj: Record<string, unknown>, key: string, value: unknown): void {
  const parts = key.split('.');
  let current: Record<string, unknown> = obj;
  for (let i = 0; i < parts.length - 1; i++) {
    const part = parts[i];
    if (typeof current[part] !== 'object' || current[part] === null) {
      current[part] = {};
    }
    current = current[part] as Record<string, unknown>;
  }
  current[parts[parts.length - 1]] = value;
}
