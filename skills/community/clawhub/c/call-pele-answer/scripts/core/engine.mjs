// engine.mjs — assembles the registry from built-ins, config and plugins, and runs the two pipelines:
//   build:  draft → IR → lint → output            (the model wrote the draft)
//   route:  answer → blocks → router → compose → scaffold draft   (the model wrote a plain answer)
import { readFileSync, existsSync } from 'node:fs';
import { join, dirname, resolve, isAbsolute } from 'node:path';
import { homedir } from 'node:os';
import { pathToFileURL } from 'node:url';
import { createRegistry } from './registry.mjs';
import { NOTRACE } from './trace.mjs';
import { withCache } from './cache.mjs';
import { parseDraft } from './markdown.mjs';
import { compose, scaffold, splitAnswer, DERIVERS } from './compose.mjs';
import forms from '../forms/index.mjs';
import routers, { makeRouter } from '../routers/index.mjs';
import { nativeAdapter, shimAdapter } from '../routers/systemone.mjs';
import theme from '../themes/pele.mjs';
import palettes from '../themes/palettes.mjs';
import outputs from '../outputs/index.mjs';
import rules, { docLang } from '../lint/index.mjs';
import components from './components.mjs';
import { admit, logUsage } from './admit.mjs';

export const USER_CONFIG = join(homedir(), '.call-pele-answer', 'config.json');
const OLD_USER_CONFIG = join(homedir(), '.pele-explain', 'config.json'); // read once if the new one is missing
const PROJECT_CONFIG = '.call-pele-answer.json';

// Config precedence (later wins): built-in defaults < ~/.call-pele-answer/config.json < ./.call-pele-answer.json
// < environment (PE_ROUTER, PE_THEME) < CLI flags.
// A project config comes from whatever repository the agent happens to be in, so it is untrusted: it may
// set presentation (router name, theme, output, policy) but not code (plugins) or network endpoints
// (adapters). PE_TRUST_PROJECT=1, set by the user, lifts that for a repository they trust.
const CODE_KEYS = ['plugins', 'adapters'];
export function loadConfig(cwd = process.cwd()) {
  const read = p => { try { return { ...JSON.parse(readFileSync(p, 'utf8')), __dir: dirname(p) }; } catch { return null; } };
  const user = read(USER_CONFIG) || read(OLD_USER_CONFIG), project = read(join(cwd, PROJECT_CONFIG));
  const ignored = [];
  if (project && process.env.PE_TRUST_PROJECT !== '1') for (const k of CODE_KEYS) if (project[k]?.length) { ignored.push(k); delete project[k]; }
  const layers = [user, project].filter(Boolean);
  const cfg = { router: 'auto', theme: 'pele', output: 'html', palette: true, annotate: true, plugins: [], adapters: [], routers: [], policy: {}, ignored };
  for (const l of layers) {
    for (const k of ['router', 'theme', 'output', 'ste']) if (l[k]) cfg[k] = l[k];
    cfg.plugins.push(...(l.plugins || []).map(p => ({ spec: p, dir: l.__dir })));
    cfg.adapters.push(...(l.adapters || []));
    cfg.routers.push(...(l.routers || []));
    Object.assign(cfg.policy, l.policy || {});
    if ('annotate' in l) cfg.annotate = l.annotate !== false && l.annotate !== 'off';
    if ('palette' in l) cfg.palette = l.palette !== false && l.palette !== 'off';
  }
  if (process.env.PE_ROUTER) cfg.router = process.env.PE_ROUTER;
  if (process.env.PE_THEME) cfg.theme = process.env.PE_THEME;
  if (process.env.PE_ANNOTATE) cfg.annotate = !/^(0|off|false|no)$/i.test(process.env.PE_ANNOTATE);
  if (process.env.PE_PALETTE) cfg.palette = !/^(0|off|false|no)$/i.test(process.env.PE_PALETTE);
  cfg.layers = layers.map(l => l.__dir);
  return cfg;
}

export async function createEngine({ cwd = process.cwd(), config, trace = NOTRACE } = {}) {
  const cfg = config || trace.span('config', () => loadConfig(cwd));
  if (cfg.ignored?.length) console.error(`! 忽略了 ./${PROJECT_CONFIG} 里的 ${cfg.ignored.join('、')}：项目配置不能加载代码或网络端点（信任这个仓库时设 PE_TRUST_PROJECT=1）`);
  const reg = createRegistry();
  trace.span('builtins', () => { for (const p of [forms, routers, theme, palettes, outputs, rules, components]) reg.use(p); });
  // declarative adapters and routers from config: no code needed to plug in a new System One provider
  for (const a of cfg.adapters) { try { reg.api.adapter((a.kind === 'shim' ? shimAdapter : nativeAdapter)(a)); } catch (e) { console.error(`! 跳过适配器：${e.message}`); } }
  for (const r of cfg.routers) reg.api.routerSpec(r);
  // code plugins: a module whose default export is { name, apiVersion, setup(api) } or a setup function
  for (const { spec, dir } of cfg.plugins) {
    const target = spec.startsWith('.') || isAbsolute(spec) ? pathToFileURL(resolve(dir, spec)).href : spec;
    await trace.span(`plugin:${spec}`, async () => { const mod = await import(target); reg.use(mod.default || mod, spec); });
  }
  for (const [n, a] of reg.adapters) reg.adapters.set(n, withCache(a, trace));
  return new Engine(reg, cfg, trace);
}

class Engine {
  constructor(registry, config, trace = NOTRACE) { this.registry = registry; this.config = config; this.trace = trace; }

  resolveRouter(name) {
    if (name === 'auto') name = 'jev';
    const r = this.registry.router(name);
    if (r) return r;
    const spec = this.registry.routerSpec(name);
    if (spec) return makeRouter(spec, this.registry.adapters);
    throw new Error(`未知 router：${name}（可选 auto | ${this.registry.routers().join(' | ')}）`);
  }

  // Walk the fallback chain until a router answers; local always answers.
  async route(answer, { router = this.config.router, policy = {}, auto = false, options = true } = {}) {
    const T = this.trace;
    const t0 = Date.now(); const ans = T.span('split', () => splitAnswer(answer)); const notes = [];
    const texts = ans.blocks.map(b => b.text);
    let name = router, res = null; const tried = new Set();
    while (name && !tried.has(name)) {
      tried.add(name);
      const r = this.resolveRouter(name);
      const rn = name === 'auto' ? 'jev' : name;
      try { res = await T.span(`router:${rn}`, () => r.route(texts)); T.set('router', rn); T.count('blocks', texts.length); break; }
      catch (e) { notes.push(`${name} 不可用（${e.message}）`); name = r.fallback || (name !== 'local' ? 'local' : null); }
    }
    if (res.note) notes.push(res.note);
    res.blocks.forEach((b, i) => (b.title = ans.blocks[i].title));
    const P = { ...this.config.policy, ...policy };
    T.span('compose', () => compose(res.blocks, P));
    // component options: every registered component whose conditions pass, for the agent to combine
    if (options) {
      const an = res.by === 'local' ? null : this.registry.adapters.get(process.env.TYPESAFE_API_KEY ? 'typesafe' : 'classifier-systemone');
      const note = await T.span('admit', () => admit(res.blocks, this.registry.components(), an, { log: !process.env.PE_NO_LOG }));
      if (note) notes.push(note);
    }
    const derivers = { ...DERIVERS };
    for (const [fam, fns] of Object.entries(this.registry.derivers())) derivers[fam] = [...(derivers[fam] || []), ...fns];
    const draft = T.span('scaffold', () => scaffold({ title: ans.title, frontMatter: auto ? ans.frontMatter : null, lead: ans.lead, blocks: res.blocks, derivers, policy: P, auto }));
    T.set('by', res.by); T.set('families', res.blocks.map(b => b.family).join(','));
    T.count('todo', (draft.match(/<!-- TODO/g) || []).length);
    return { draft, blocks: res.blocks, by: res.by, ms: Date.now() - t0, notes };
  }

  build(draft, { output = this.config.output, theme = this.config.theme, ste = this.config.ste, palette = this.config.palette, annotate = this.config.annotate, mode, lean } = {}) {
    const T = this.trace;
    const { doc, errors, warns, embedded } = T.span('parse', () => parseDraft(draft, this.registry, T));
    if (!process.env.PE_NO_LOG && !errors.length) logUsage(draft, this.registry.components());
    const found = [...warns];
    const report = (l, r, m, f) => found.push([l, r, m, f]);
    const ctx = { registry: this.registry, ste, draft, error: (l, r, m, f) => errors.push([l, r, m, f]) };
    for (const rule of this.registry.rules()) T.span(`lint:${rule.id}`, () => rule.check(doc, report, ctx));
    T.count('warnings', found.length); T.count('errors', errors.length);
    found.sort((a, b) => a[0] - b[0]);
    const lang = docLang(doc);
    if (errors.length) return { doc, errors: errors.sort((a, b) => a[0] - b[0]), warnings: found, embedded, lang };
    const out = this.registry.output(output);
    if (!out) throw new Error(`未知 output：${output}（可选 ${this.registry.outputs().join(' | ')}）`);
    const text = T.span(`output:${output}`, () => out.write(doc, { registry: this.registry, theme, lang, mode, lean, palette, annotate }));
    T.count('bytes', text.length);
    return { doc, errors: [], warnings: found, embedded, lang, ext: out.ext, text };
  }

  info() {
    const reg = this.registry;
    return {
      config: { router: this.config.router, theme: this.config.theme, output: this.config.output, layers: this.config.layers },
      plugins: reg.loaded,
      forms: reg.forms().map(f => ({ name: f.name, fences: f.fences.filter(Boolean).slice(0, 6), outputs: Object.keys(f.render) })),
      routers: reg.routers().map(n => ({ name: n, describe: (reg.router(n) || reg.routerSpec(n))?.describe || '' })),
      adapters: [...reg.adapters.values()].map(a => ({ name: a.name, kind: a.kind, available: a.available?.(), describe: a.describe || '' })),
      themes: reg.themes(), outputs: reg.outputs(),
      rules: reg.rules().map(r => r.id),
    };
  }
}
