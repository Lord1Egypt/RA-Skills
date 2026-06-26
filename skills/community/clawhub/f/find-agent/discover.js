const { createOceanBus } = require('oceanbus');

// ── Constants ────────────────────────────────────────────────

const VERSION = '1.3.1';

const TEMPLATES = [
  { id: 'restaurant',    name: '餐饮',     emoji: '🍲', description: '餐厅、火锅店、外卖',                       capabilities: ['show-menu','check-availability','make-reservation'], questionCount: 6 },
  { id: 'insurance',     name: '保险',     emoji: '🔶', description: '保险咨询、需求分析、计划书',               capabilities: ['about','ask-insurance','needs-analysis','generate-proposal','schedule-consultation'], questionCount: 7 },
  { id: 'checkup',       name: '体检',     emoji: '🩺', description: '体检套餐、预约、报告解读',                 capabilities: ['list-packages','package-detail','recommend-checkup','check-slots','book-checkup','explain-report'], questionCount: 7 },
  { id: 'tech-service',  name: '技术服务', emoji: '🔧', description: '天气查询、行情数据、API 工具等',          capabilities: ['about','query-data','list-capabilities'], questionCount: 5 },
  { id: 'custom',        name: '其他',     emoji: '🎨', description: '自由定义（告诉我你做什么）',              capabilities: [], questionCount: 4 },
];

const VALID_TEMPLATE_IDS = TEMPLATES.map(t => t.id);
const MAX_TAG_CHARS = 120;
const MAX_DESC_CHARS = 800;

// ── Argument Parser ──────────────────────────────────────────

function parseArgs(argv) {
  const flags = new Map();
  const positionals = [];
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '-h') {
      flags.set('help', 'true');
    } else if (arg.startsWith('--')) {
      const eqIdx = arg.indexOf('=');
      if (eqIdx > 2) {
        flags.set(arg.slice(2, eqIdx), arg.slice(eqIdx + 1));
      } else {
        const next = argv[i + 1];
        if (next && !next.startsWith('-')) {
          flags.set(arg.slice(2), next);
          i++;
        } else {
          flags.set(arg.slice(2), 'true');
        }
      }
    } else {
      positionals.push(arg);
    }
  }
  return { command: positionals[0] || null, flags, positionals };
}

// ── Output formatter ─────────────────────────────────────────

function formatOutput(data, format) {
  if (format === 'json') return JSON.stringify(data, null, 2);
  if (typeof data === 'string') return data;
  if (Array.isArray(data)) {
    return data.map((item, i) => {
      if (typeof item === 'object' && item !== null) {
        const emoji = item.emoji || '';
        const capStr = (item.capabilities || []).join(', ');
        return `${emoji} ${(item.id || '').padEnd(16)} ${(item.name || '').padEnd(10)} ${item.description || ''}`;
      }
      return `${i + 1}. ${item}`;
    }).join('\n');
  }
  if (typeof data === 'object' && data !== null) {
    return Object.entries(data).map(([k, v]) => {
      if (Array.isArray(v)) return `${k}: [${v.join(', ')}]`;
      if (typeof v === 'object') return `${k}: ${JSON.stringify(v)}`;
      return `${k}: ${v}`;
    }).join('\n');
  }
  return String(data);
}

// ── Help text (--format pretty) ──────────────────────────────

function buildHelpText() {
  return `find-agent ${VERSION} — OceanBus Yellow Pages agent discovery

USAGE
  node discover.js search <tags>              Search by comma-separated tags
    --limit=<N>                               Max results (default 20)
    --format=json|pretty                      Output format (default: json)

  node discover.js publish <name>             Publish your agent to Yellow Pages
    --tags=<tags>                             Comma-separated tags (required)
    --desc=<description>                      Short description
    --summary=<text>                          One-line summary
    --helpcmd=<command>                       --help command other agents send to you
    --template=<id>                           Industry template: ${VALID_TEMPLATE_IDS.join('|')}

  node discover.js unpublish                  Remove your agent from Yellow Pages

  node discover.js openid                     Show current agent OpenID
    --format=json|pretty                      Output format (default: json)

  node discover.js templates                  List available industry templates
    --format=json|pretty                      Output format (default: pretty)

  node discover.js listen                     Listen for --help requests and auto-respond

COMMANDS
  search    Discover agents by tags. Enriched with reputation scores when available.
  publish   Register or update your Yellow Pages entry. Supports industry templates.
  unpublish Remove your entry and stop heartbeat.
  openid    Display your agent OpenID.
  templates List all industry templates with capabilities.
  listen    Start a long-running listener that auto-responds to --help requests.

FLAGS (all commands)
  --format=json|pretty     Output format (default depends on command)
  -h, --help               Show this help text
  --help --format=json     Show help as JSON for LLM consumption

EXAMPLES
  $ node discover.js search 火锅,成都
  $ node discover.js search 体检,企业团检 --limit 5
  $ node discover.js publish "老张火锅" --tags=火锅,川味,成都 --template=restaurant
  $ node discover.js templates --format=json

更多信息: https://github.com/ryanbihai/find-agent`;
}

// ── Help JSON (--format json) ────────────────────────────────

function buildHelpJson() {
  return {
    name: 'find-agent',
    version: VERSION,
    description: 'OceanBus Yellow Pages — discover AI agents and services, publish your own',
    commands: [
      {
        name: 'search',
        description: 'Search Yellow Pages by tags',
        usage: 'node discover.js search <tags> [--limit=N] [--format=json|pretty]',
        flags: [
          { name: 'limit',  type: 'number', default: 20, description: 'Max results' },
          { name: 'format', type: 'enum',   values: ['json','pretty'], description: 'Output format (default: json)' },
        ],
      },
      {
        name: 'publish',
        description: 'Publish your agent to Yellow Pages',
        usage: 'node discover.js publish <name> --tags=<tags> [--desc=<d>] [--template=<id>] [--helpcmd=<cmd>]',
        flags: [
          { name: 'tags',     type: 'string', required: true,  description: 'Comma-separated tags' },
          { name: 'desc',     type: 'string', description: 'Short description (max 800 chars)' },
          { name: 'summary',  type: 'string', description: 'One-line summary' },
          { name: 'template', type: 'enum',   values: VALID_TEMPLATE_IDS, description: 'Industry template' },
          { name: 'helpcmd',  type: 'string', description: '--help command other agents send to you' },
        ],
      },
      { name: 'unpublish', description: 'Remove your agent from Yellow Pages', usage: 'node discover.js unpublish' },
      { name: 'openid',    description: 'Show current agent OpenID', usage: 'node discover.js openid [--format=json|pretty]' },
      { name: 'templates', description: 'List available industry templates', usage: 'node discover.js templates [--format=json|pretty]' },
      { name: 'listen',    description: 'Listen for --help requests and auto-respond', usage: 'node discover.js listen' },
    ],
  };
}

// ── Reputation helper ────────────────────────────────────────

async function enrichWithReputation(ob, entries) {
  if (!entries.length) return;
  const openids = entries.map(e => e.openid);
  try {
    const result = await withTimeout(
      ob.l1.reputation.queryReputation(openids),
      3000,
    );
    const repMap = new Map();
    const results = result?.data?.results || [];
    for (const r of results) repMap.set(r.openid, r);
    for (const entry of entries) {
      const rep = repMap.get(entry.openid);
      if (rep) {
        const tags = rep.facts?.evaluations?.tags || {};
        const posCount = Object.values(tags).filter(v => v > 0).length;
        const negCount = Object.values(tags).filter(v => v < 0).length;
        entry._reputation = { positive: posCount, negative: negCount, tags };
        entry._daysActive = rep.facts?.identity?.days_active || 0;
        entry._partners = rep.facts?.communication?.unique_partners || 0;
      } else {
        entry._reputation = null;
      }
    }
  } catch {
    for (const entry of entries) entry._reputation = null;
  }
}

function withTimeout(promise, ms) {
  return Promise.race([
    promise,
    new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), ms)),
  ]);
}

// ── Pretty print helpers ─────────────────────────────────────

function prettyEntry(entry, i) {
  const openidShort = (entry.openid || '').slice(0, 16);
  const tags = (entry.tags || []).join(', ');
  const rep = entry._reputation;
  let repStr = '';
  if (rep && (rep.positive > 0 || rep.negative > 0)) {
    const stars = '★'.repeat(Math.min(5, Math.round(rep.positive / (rep.positive + rep.negative) * 5))) || '☆';
    repStr = `  ⭐${stars} (${rep.positive}+/${rep.negative}-)`;
  } else if (rep === null) {
    repStr = '  声誉: N/A';
  }
  const desc = (entry.description || entry.summary || '').slice(0, 60);
  return `${i + 1}. ${entry.name || openidShort}  ${tags}${repStr}\n   ${desc}`;
}

// ── Main ─────────────────────────────────────────────────────

class CliError extends Error {
  constructor(message, exitCode = 1) {
    super(message);
    this.exitCode = exitCode;
  }
}

function resolveFormat(flags, defaultFormat) {
  const raw = flags.get('format');
  if (!raw || raw === 'true') return defaultFormat;
  if (raw === 'json' || raw === 'pretty') return raw;
  throw new CliError(`Invalid --format value: "${raw}". Valid: json, pretty`);
}

async function main() {
  const { command, flags, positionals } = parseArgs(process.argv.slice(2));

  // --help / -h / no command
  const isHelp = !command || flags.has('help') || command === 'help';
  if (isHelp) {
    const format = resolveFormat(flags, 'pretty');
    if (format === 'json') {
      console.log(JSON.stringify(buildHelpJson(), null, 2));
    } else {
      console.log(buildHelpText());
    }
    return;
  }

  // templates — no OceanBus connection needed
  if (command === 'templates') {
    const format = resolveFormat(flags, 'pretty');
    console.log(formatOutput(TEMPLATES, format));
    return;
  }

  // All remaining commands need an OceanBus connection
  const ob = await createOceanBus();

  try {
    const format = resolveFormat(flags, 'json'); // data commands default to JSON

    // ── openid ──
    if (command === 'openid') {
      const openid = await ob.getAddress();
      if (format === 'json') {
        console.log(JSON.stringify({ openid }, null, 2));
      } else {
        console.log(openid);
      }
      return;
    }

    // ── search ──
    if (command === 'search') {
      const tagsStr = positionals[1];
      if (!tagsStr) throw new CliError('Usage: node discover.js search <tag1,tag2,...> [--limit=N]');
      const tags = tagsStr.split(',').map(t => t.trim()).filter(Boolean);
      if (!tags.length) throw new CliError('Usage: node discover.js search <tag1,tag2,...> [--limit=N]');

      const rawLimit = parseInt(flags.get('limit') || '20', 10);
      const limit = (isNaN(rawLimit) || rawLimit < 1) ? 20 : rawLimit;

      const results = await ob.l1.yellowPages.discover(tags, limit);
      const entries = results?.data?.entries || [];

      await enrichWithReputation(ob, entries);

      if (format === 'json') {
        console.log(JSON.stringify({ total: entries.length, entries }, null, 2));
      } else {
        if (entries.length === 0) {
          console.log('(empty)');
        } else {
          console.log(`找到 ${entries.length} 个结果:\n`);
          console.log(entries.map((e, i) => prettyEntry(e, i)).join('\n\n'));
        }
      }
      return;
    }

    // ── publish ──
    if (command === 'publish') {
      const name = (positionals[1] || '').trim();
      const tagsStr = flags.get('tags') || '';
      const tags = tagsStr.split(',').map(t => t.trim()).filter(Boolean);
      const description = flags.get('desc') || '';
      const summary = flags.get('summary') || undefined;
      const helpCommand = flags.get('helpcmd') || undefined;
      const template = flags.get('template') || undefined;

      if (!name || !tags.length) {
        throw new CliError('Usage: node discover.js publish <name> --tags <tag1,tag2> [--desc <description>] [--template <id>]');
      }

      // Validate template
      if (template && !VALID_TEMPLATE_IDS.includes(template)) {
        throw new CliError(`Unknown template: ${template}. Valid: ${VALID_TEMPLATE_IDS.join(', ')}`);
      }

      // Validate length
      const totalTagChars = tags.reduce((sum, t) => sum + t.length, 0);
      if (totalTagChars > MAX_TAG_CHARS) {
        throw new CliError(`Tags total character count (${totalTagChars}) exceeds ${MAX_TAG_CHARS}`);
      }
      if (description.length > MAX_DESC_CHARS) {
        throw new CliError(`Description length (${description.length}) exceeds ${MAX_DESC_CHARS}`);
      }

      const openid = await ob.getAddress();
      const publishOpts = { name, tags, description, summary, helpCommand };
      if (template) publishOpts.template = template;
      await ob.l1.yellowPages.publish(publishOpts);

      const output = { success: true, name, tags, openid };
      if (template) output.template = template;

      if (format === 'json') {
        console.log(JSON.stringify(output, null, 2));
      } else {
        console.log(`✅ 已发布！名称: ${name}`);
        console.log(`   标签: ${tags.join(', ')}`);
        console.log(`   OpenID: ${openid}`);
        if (template) console.log(`   模板: ${template}`);
      }
      return;
    }

    // ── unpublish ──
    if (command === 'unpublish') {
      await ob.l1.yellowPages.unpublish();
      if (format === 'json') {
        console.log(JSON.stringify({ success: true, message: '已从黄页移除' }, null, 2));
      } else {
        console.log('✅ 已从黄页移除');
      }
      return;
    }

    // ── listen ──
    if (command === 'listen') {
      const helpText = buildHelpText();
      console.log(`📡 find-agent ${VERSION} listening for --help requests... (Ctrl+C to stop)`);

      let running = true;
      let pendingSends = 0;

      const onSignal = () => {
        if (!running) return;
        console.log('\n🛑 Shutting down... (waiting for pending responses)');
        running = false;
      };
      process.once('SIGINT', onSignal);
      process.once('SIGTERM', onSignal);

      const stopFn = ob.startListening(async (msg) => {
        if (!running) return;
        const content = (msg.content || '').trim();
        if (content === '--help' || content === '-h' || content === 'help') {
          const fromShort = (msg.from_openid || '').slice(0, 12);
          console.log(`← --help from ${fromShort}...`);
          try {
            pendingSends++;
            await ob.send(msg.from_openid, helpText);
            console.log(`→ responded to ${fromShort}`);
          } catch (e) {
            console.error(`✗ failed to respond to ${fromShort}: ${e.message}`);
          } finally {
            pendingSends--;
          }
        }
      });

      // Keep alive until signal
      while (running) {
        await new Promise(r => setTimeout(r, 500));
      }

      stopFn(); // stop accepting new messages
      // Wait for pending sends to complete (max 10s)
      const deadline = Date.now() + 10000;
      while (pendingSends > 0 && Date.now() < deadline) {
        await new Promise(r => setTimeout(r, 200));
      }
      await ob.destroy();
      return;
    }

    // ── unknown ──
    throw new CliError(`Unknown command: ${command}\n${buildHelpText()}`);

  } finally {
    if (command !== 'listen') await ob.destroy();
  }
}

main().catch(err => {
  const code = err instanceof CliError ? err.exitCode : 1;
  console.error(err instanceof CliError ? err.message : JSON.stringify({ error: err.message }, null, 2));
  process.exit(code);
});
