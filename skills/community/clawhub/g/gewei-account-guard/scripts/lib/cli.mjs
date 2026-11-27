export function parseArgs(argv, { booleans = [] } = {}) {
  const booleanSet = new Set(booleans);
  const positionals = [];
  const flags = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) {
      positionals.push(arg);
      continue;
    }
    const body = arg.slice(2);
    if (body.includes('=')) {
      const idx = body.indexOf('=');
      flags[body.slice(0, idx)] = body.slice(idx + 1);
      continue;
    }
    if (booleanSet.has(body)) {
      flags[body] = true;
      continue;
    }
    const next = argv[i + 1];
    if (next !== undefined && !next.startsWith('--')) {
      flags[body] = next;
      i += 1;
    } else {
      flags[body] = true;
    }
  }
  return { positionals, flags };
}

export function fail(message, code = 1) {
  process.stderr.write(`${message}\n`);
  process.exit(code);
}

export function printJson(data) {
  process.stdout.write(`${JSON.stringify(data, null, 2)}\n`);
}

export function readNumber(value, fallback = 0) {
  const num = Number(value);
  return Number.isFinite(num) ? num : fallback;
}

export function readBoolean(value, fallback = false) {
  if (value === undefined || value === null || value === '') return fallback;
  if (typeof value === 'boolean') return value;
  return ['1', 'true', 'yes', '是', '有'].includes(String(value).trim().toLowerCase());
}
