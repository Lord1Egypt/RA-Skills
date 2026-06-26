#!/usr/bin/env node
import pkg from 'atlas-obscura-api';
const atlasObscura = pkg.atlasObscura || pkg.atlasobscura;

function parseArgs(argv) {
  const [cmd, ...rest] = argv;
  const args = {};
  for (let i = 0; i < rest.length; i++) {
    const k = rest[i];
    if (!k.startsWith('--')) continue;
    const key = k.slice(2);
    const v = rest[i + 1] && !rest[i + 1].startsWith('--') ? rest[++i] : true;
    args[key] = v;
  }
  return { cmd, args };
}

function pick(obj, keys) {
  const out = {};
  for (const k of keys) out[k] = obj?.[k];
  return out;
}

async function main() {
  const { cmd, args } = parseArgs(process.argv.slice(2));

  if (!cmd || ['help', '--help', '-h'].includes(cmd)) {
    console.log(`Usage:
  node scripts/atlas_obscura.js search --lat <num> --lng <num> [--limit 5]
  node scripts/atlas_obscura.js place-short --id <num>
  node scripts/atlas_obscura.js place-full --id <num>
  node scripts/atlas_obscura.js places-all [--limit 10]
`);
    process.exit(0);
  }

  if (cmd === 'search') {
    const lat = Number(args.lat);
    const lng = Number(args.lng);
    const limit = Number(args.limit || 5);
    if (Number.isNaN(lat) || Number.isNaN(lng)) {
      throw new Error('search requires --lat and --lng');
    }
    const res = await atlasObscura.search({ lat, lng }).catch(() => null);
    const items = (res?.results || []).slice(0, limit).map((x) => ({
      ...pick(x, ['id', 'title', 'subtitle', 'location', 'url', 'thumbnail_url']),
      coordinates: x?.coordinates,
      distance_from_query: x?.distance_from_query
    }));
    console.log(JSON.stringify({
      query: { lat, lng },
      total: res?.total,
      count: items.length,
      results: items
    }, null, 2));
    return;
  }

  if (cmd === 'place-short') {
    const id = Number(args.id);
    if (Number.isNaN(id)) throw new Error('place-short requires --id');
    const p = await atlasObscura.placeShort(id);
    console.log(JSON.stringify(p, null, 2));
    return;
  }

  if (cmd === 'place-full') {
    const id = Number(args.id);
    if (Number.isNaN(id)) throw new Error('place-full requires --id');
    const p = await atlasObscura.placeFull(id);
    console.log(JSON.stringify(p, null, 2));
    return;
  }

  if (cmd === 'places-all') {
    const limit = Number(args.limit || 10);
    const all = await atlasObscura.placesAll().catch(() => []);
    console.log(JSON.stringify({
      count: Array.isArray(all) ? all.length : 0,
      sample: Array.isArray(all) ? all.slice(0, limit) : []
    }, null, 2));
    return;
  }

  throw new Error(`Unknown command: ${cmd}`);
}

main().catch((err) => {
  console.error(JSON.stringify({ ok: false, error: err.message }, null, 2));
  process.exit(1);
});
