const isTTY = process.stdout.isTTY;

export function output(data, flags = {}) {
  if (flags.json || !isTTY) {
    console.log(JSON.stringify(data, null, 2));
  } else {
    prettyPrint(data);
  }
}

export function error(msg, code = 1) {
  const e = new Error(msg);
  e.exitCode = code;
  throw e;
}

export function log(msg) {
  const ts = new Date().toISOString().replace('T', ' ').slice(0, 19);
  process.stderr.write(`${ts} ${msg}\n`);
}

function prettyPrint(data) {
  if (Array.isArray(data)) {
    for (const item of data) {
      if (item.name) {
        const alive = item.alive ? '✅' : '❌';
        const delay = item.delay ? `${item.delay}ms` : '-';
        console.log(`  ${alive} ${item.name}: ${delay} [${item.type || ''}]`);
      } else {
        console.log(JSON.stringify(item));
      }
    }
    return;
  }
  for (const [k, v] of Object.entries(data)) {
    if (typeof v === 'object' && v !== null) {
      console.log(`${k}:`);
      for (const [k2, v2] of Object.entries(v)) {
        console.log(`  ${k2}: ${v2}`);
      }
    } else {
      console.log(`${k}: ${v}`);
    }
  }
}
