import path from 'node:path';
import process from 'node:process';

import { FlowClient } from './flow-webapi/index.js';
import { set_log_level } from './flow-webapi/utils/logger.js';
import { resolveFlowWebChromeProfileDir, resolveFlowWebCookiePath } from './flow-webapi/utils/paths.js';
import { sleep } from './flow-webapi/utils/http.js';

type CliArgs = {
  prompts: string[];
  model: string;
  aspect: string;
  count: number;
  login: boolean;
  projectId: string | null;
  cookiePath: string | null;
  profileDir: string | null;
  verbose: boolean;
  help: boolean;
};

function formatScriptCommand(fallback: string): string {
  const raw = process.argv[1];
  const displayPath = raw
    ? (() => {
        const relative = path.relative(process.cwd(), raw);
        return relative && !relative.startsWith('..') ? relative : raw;
      })()
    : fallback;
  const quotedPath = displayPath.includes(' ')
    ? `"${displayPath.replace(/"/g, '\\"')}"`
    : displayPath;
  return `npx -y bun ${quotedPath}`;
}

function printUsage(cookiePath: string, profileDir: string): void {
  const cmd = formatScriptCommand('scripts/main.ts');
  console.log(`Usage:
  ${cmd} --prompt "A cute cat"
  ${cmd} "A sunset" --model NANO_BANANA_PRO --aspect 9:16 --count 2

Batch mode (multiple prompts in one project, 5s interval):
  ${cmd} --prompt "A cute cat" --prompt "A sunset" --prompt "A mountain"

Default behavior:
  Creates a new Flow project through the UI, then submits the prompt.
  Use --project-id only when you intentionally want to reuse an existing project.

Options:
  -p, --prompt <text>         Prompt text (repeat for batch mode)
  -m, --model <id>            NARWHAL (default), NANO_BANANA_PRO
  -a, --aspect <ratio>        16:9 (default), 9:16
  --count <n>                 Number of images: 1-4 (default: 2)
  --project-id <id>           Reuse existing project
  --login                     Only authenticate, then exit
  --verbose                   Enable debug logging
  --cookie-path <path>        Cookie file path (default: ${cookiePath})
  --profile-dir <path>        Chrome profile dir (default: ${profileDir})
  -h, --help                  Show help

Models:
  NARWHAL              Nano Banana 2 (default, fast)
  NANO_BANANA_PRO      Nano Banana Pro

Env overrides:
  FLOW_WEB_DATA_DIR, FLOW_WEB_COOKIE_PATH, FLOW_WEB_CHROME_PROFILE_DIR, FLOW_WEB_CHROME_PATH`);
}

function parseArgs(argv: string[]): CliArgs {
  const out: CliArgs = {
    prompts: [],
    model: 'NARWHAL',
    aspect: '16:9',
    count: 2,
    login: false,
    projectId: null,
    cookiePath: null,
    profileDir: null,
    verbose: false,
    help: false,
  };

  const positional: string[] = [];

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]!;

    if (a === '--help' || a === '-h') { out.help = true; continue; }
    if (a === '--login') { out.login = true; continue; }
    if (a === '--verbose') { out.verbose = true; continue; }

    if (a === '--prompt' || a === '-p') {
      const v = argv[++i];
      if (!v) throw new Error(`Missing value for ${a}`);
      out.prompts.push(v);
      continue;
    }

    if (a === '--model' || a === '-m') {
      const v = argv[++i];
      if (!v) throw new Error(`Missing value for ${a}`);
      out.model = v;
      continue;
    }

    if (a === '--aspect' || a === '-a') {
      const v = argv[++i];
      if (!v) throw new Error(`Missing value for ${a}`);
      out.aspect = v;
      continue;
    }

    if (a === '--count') {
      const v = argv[++i];
      if (!v) throw new Error('Missing value for --count');
      out.count = parseInt(v, 10);
      continue;
    }

    if (a === '--project-id') {
      const v = argv[++i];
      if (!v) throw new Error('Missing value for --project-id');
      out.projectId = v;
      continue;
    }

    if (a === '--cookie-path') {
      const v = argv[++i];
      if (!v) throw new Error('Missing value for --cookie-path');
      out.cookiePath = v;
      continue;
    }

    if (a === '--profile-dir') {
      const v = argv[++i];
      if (!v) throw new Error('Missing value for --profile-dir');
      out.profileDir = v;
      continue;
    }

    if (a.startsWith('-')) {
      throw new Error(`Unknown option: ${a}`);
    }

    positional.push(a);
  }

  if (out.prompts.length === 0 && positional.length > 0) {
    out.prompts.push(positional.join(' '));
  }

  return out;
}

async function readPromptFromStdin(): Promise<string | null> {
  if (process.stdin.isTTY) return null;
  try {
    const t = await Bun.stdin.text();
    const v = t.trim();
    return v.length > 0 ? v : null;
  } catch {
    return null;
  }
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));

  if (args.cookiePath) process.env.FLOW_WEB_COOKIE_PATH = args.cookiePath;
  if (args.profileDir) process.env.FLOW_WEB_CHROME_PROFILE_DIR = args.profileDir;
  if (args.verbose) set_log_level('DEBUG');

  const cookiePath = resolveFlowWebCookiePath();
  const profileDir = resolveFlowWebChromeProfileDir();

  if (args.help) {
    printUsage(cookiePath, profileDir);
    return;
  }

  const client = new FlowClient({
    verbose: args.verbose,
  });

  try {
    // --login mode
    if (args.login) {
      process.env.FLOW_WEB_LOGIN = '1';
      await client.init();
      await client.close();
      console.error(`Authenticated. Cookie saved: ${cookiePath}`);
      return;
    }

    // Normal generation mode — need at least one prompt
    const prompts: string[] = [...args.prompts];
    if (prompts.length === 0) {
      const stdinPrompt = await readPromptFromStdin();
      if (stdinPrompt) prompts.push(stdinPrompt);
    }

    if (prompts.length === 0) {
      printUsage(cookiePath, profileDir);
      process.exitCode = 1;
      return;
    }

    await client.init();

    if (prompts.length === 1) {
      // Single prompt mode
      await client.generateImages({
        prompt: prompts[0]!,
        model: args.model,
        aspect: args.aspect,
        count: args.count,
        projectId: args.projectId ?? undefined,
      });
    } else {
      // Batch mode: create one project, submit prompts sequentially with 5s intervals
      let projectId = args.projectId ?? undefined;

      for (let i = 0; i < prompts.length; i++) {
        if (i > 0) {
          console.error(`Waiting 5s before next prompt (${i + 1}/${prompts.length})...`);
          await sleep(5000);
        }

        console.error(`Generating prompt ${i + 1}/${prompts.length}: "${prompts[i]!.slice(0, 60)}..."`);

        const result = await client.generateImages({
          prompt: prompts[i]!,
          model: args.model,
          aspect: args.aspect,
          count: args.count,
          projectId,
        });

        // Reuse the project created by the first generation
        if (!projectId) projectId = result.projectId;
      }
    }
  } finally {
    await client.close();
  }
}

main().then(() => process.exit(0)).catch((e) => {
  const msg = e instanceof Error ? e.message : String(e);
  console.error(msg);
  process.exit(1);
});
