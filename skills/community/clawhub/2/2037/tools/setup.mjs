import { createInterface, emitKeypressEvents } from 'node:readline';
import { mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { homedir } from 'node:os';
import { resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { randomUUID } from 'node:crypto';
import { format } from 'node:util';

const root = fileURLToPath(new URL('../', import.meta.url));
export function configurations({ privateDir, node = process.execPath, gateway = root, locale = 'en', readOnly = true, platform = process.platform }) {
  const entry = { command: node, args: [join(gateway, 'src/main.mjs')], env: {
    EARTH2037_ACCOUNT_URL: 'https://new2037.earth2037.com/account-api',
    EARTH2037_CREDENTIAL_FILE: join(privateDir, 'credentials.json'),
    EARTH2037_STATE_DIR: join(privateDir, 'state'),
    EARTH2037_LOCALE: locale,
    // Account Center has no linux runtime enum; headless Linux/WSL uses its web client context.
    EARTH2037_RUNTIME_PLATFORM: platform === 'darwin' ? 'macos' : platform === 'win32' ? 'windows' : 'web',
    EARTH2037_READ_ONLY: readOnly ? '1' : '0',
  } };
  // JSON strings are valid YAML scalars, including Windows paths and spaces.
  let yaml = format('mcp_servers:\n  earth2037:\n    command: %s\n    args: %s\n    timeout: 120\n    connect_timeout: 30\n    env:\n',
    JSON.stringify(entry.command), JSON.stringify(entry.args));
  let dsh = format("- insert:\n    - id: earth2037-mcp\n      name: '@deepseek-ai/dsh-mcp-client'\n      config:\n        serverName: earth2037\n        transport: stdio\n        command: %s\n        args: %s\n        toolCallTimeoutMs: 120000\n        env:\n",
    JSON.stringify(entry.command), JSON.stringify(entry.args));
  for (const [key, value] of Object.entries(entry.env)) {
    yaml = format('%s      %s: %s\n', yaml, key, JSON.stringify(value));
    dsh = format('%s          %s: %s\n', dsh, key, JSON.stringify(value));
  }
  return { json: { mcpServers: { earth2037: entry } }, yaml, dsh };
}

function ask(label) {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolveAnswer => rl.question(label, value => { rl.close(); resolveAnswer(value); }));
}
function secret(label) {
  process.stdout.write(label);
  emitKeypressEvents(process.stdin); process.stdin.setRawMode(true); process.stdin.resume();
  return new Promise((resolveAnswer, reject) => {
    let value = '';
    function done(error) {
      process.stdin.off('keypress', onKey); process.stdin.setRawMode(false); process.stdin.pause();
      process.stdout.write('\n'); error ? reject(error) : resolveAnswer(value);
    }
    function onKey(str, key = {}) {
      if (key.ctrl && key.name === 'c') return done(new Error('Cancelled / 已取消'));
      if (key.name === 'return' || key.name === 'enter') return done();
      if (key.name === 'backspace') { value = [...value].slice(0,-1).join(''); return; }
      if (str && !key.ctrl && !key.meta && !/[\x00-\x1f\x7f]/.test(str)) value += str;
    }
    process.stdin.on('keypress', onKey);
  });
}

async function main() {
  const args = process.argv.slice(2);
  if (args.includes('--help')) {
    console.log('node tools/setup.mjs [--locale en|zh-CN] [--allow-writes] [--config-only]\nLocal terminal only. Existing credentials are preserved. No game connection is made.'); return;
  }
  for (let i=0; i<args.length; i++) {
    if (args[i] === '--locale') { if (!['en','zh-CN'].includes(args[++i])) throw new Error('Use --locale en or zh-CN'); }
    else if (!['--allow-writes','--config-only'].includes(args[i])) throw new Error(format('Unknown option: %s', args[i]));
  }
  const locale = args.includes('--locale') ? args[args.indexOf('--locale')+1] : 'en';
  const privateDir = join(homedir(), '.earth2037-agent');
  const credentials = join(privateDir, 'credentials.json');
  mkdirSync(privateDir, { recursive: true, mode: 0o700 });
  if (!existsSync(credentials) && !args.includes('--config-only')) {
    if (!process.stdin.isTTY || !process.stdout.isTTY) throw new Error('Run setup in your own interactive terminal; do not send a password in chat or a command argument.');
    const username = (await ask('Earth2037 username / 帐号: ')).trim();
    const password = await secret('Password (hidden) / 密码（不回显）: ');
    if (!username || !password) throw new Error('Username and password are required / 帐号和密码不能为空');
    writeFileSync(credentials, format('%s\n', JSON.stringify({ username, password, device_id: format('earth2037-agent-%s', randomUUID()), distribution_channel: 'direct' })), { flag: 'wx', mode: 0o600 });
  }
  const config = configurations({ privateDir, locale, readOnly: !args.includes('--allow-writes') });
  writeFileSync(join(privateDir, 'mcp.json'), format('%s\n', JSON.stringify(config.json,null,2)), {mode:0o600});
  writeFileSync(join(privateDir, 'hermes-mcp.yaml'), config.yaml, {mode:0o600});
  writeFileSync(join(privateDir, 'dsh-mcp.patch.yaml'), config.dsh, {mode:0o600});
  console.log(format('Configuration / 配置目录: %s', privateDir));
  console.log('Generic MCP: mcp.json\nHermes: hermes-mcp.yaml\nDeepSeek Harness: dsh-mcp.patch.yaml');
  console.log(args.includes('--allow-writes') ? 'Game writes enabled / 已开启游戏写操作' : 'Read-only mode / 当前只读模式');
  if (!existsSync(credentials)) console.log('Credentials not configured. Run setup without --config-only in your terminal before login.');
  console.log('Merge the generated entry into your agent configuration, then restart the agent.\n将生成的条目合并到助手配置，随后重启助手。');
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main().catch(error => { console.error(error.message); process.exitCode=1; });
