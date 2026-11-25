// registry.mjs — the five extension points. Everything built in registers through the same API a
// third-party plugin uses, so a plugin can add or replace any piece without touching the core.
//
//   form    a content form: a fenced block (```steps) with parse → IR, render per output, lint, assets
//   router  a block classifier: route(texts) → { blocks, by }. Usually declared as a spec
//           { strategy, adapter, gateAdapter?, fallback? } over a System One adapter (see routers/).
//   adapter a System One answerer: ask(states[], questions) → answers[] (native or shim)
//   theme   design tokens + page CSS (and optional JS) for the html output
//   output  a target: html page, json IR, chat markdown, … : write(doc, ctx) → string
//   rule    a lint rule over the IR: check(doc, report)
//   annotation a 批注 kind {name, label, color}: the reader tags a block with it
//   palette a page preset {kind:'page', light, dark} or a swatch {kind:'swatch', l, m, d}: the 调色器 offers them
//   component a thing the agent may put in a block {name, desc, fence, skeleton, ask, min, requires}: offered
//           when its conditions pass (see core/components.mjs); combinations are the agent's call
//   deriver (family, block → {label, md} | null): turns a routed block into a form without the model
//
// Contract versions. Bump IR_VERSION on a breaking change to node shapes; bump API_VERSION when the
// registration API changes. Plugins declare `apiVersion` and are refused when it does not match.
export const IR_VERSION = 1;
export const API_VERSION = 1;

export function createRegistry() {
  const forms = new Map(), fences = new Map(), routers = new Map(), specs = new Map(), adapters = new Map(), themes = new Map(), outputs = new Map(), rules = new Map(), palettes = new Map(), annotations = new Map();
  const loaded = []; const derivers = {}; const components = new Map();
  const need = (o, keys, what) => { for (const k of keys) if (!(k in o)) throw new Error(`${what} 缺少字段 ${k}`); };
  const api = {
    apiVersion: API_VERSION,
    irVersion: IR_VERSION,
    form(def) {
      need(def, ['name', 'fences', 'render'], `form`);
      forms.set(def.name, def);
      for (const f of def.fences) fences.set(f, def.name); // later registration wins: plugins can override built-ins
      return api;
    },
    router(def) { need(def, ['name', 'route'], 'router'); routers.set(def.name, def); return api; },
    routerSpec(spec) { need(spec, ['name', 'strategy'], 'routerSpec'); specs.set(spec.name, spec); return api; },
    adapter(def) { need(def, ['name', 'ask'], 'adapter'); adapters.set(def.name, def); return api; },
    theme(def) { need(def, ['name', 'css'], 'theme'); themes.set(def.name, def); return api; },
    output(def) { need(def, ['name', 'write'], 'output'); outputs.set(def.name, def); return api; },
    annotation(def) { need(def, ['name', 'label', 'color'], 'annotation'); annotations.set(def.name, def); return api; },
    palette(def) { need(def, ['name', 'kind', 'label'], 'palette'); if (def.kind === 'swatch') need(def, ['l', 'm', 'd'], 'swatch'); palettes.set(def.name, def); return api; },
    rule(def) { need(def, ['id', 'check'], 'rule'); rules.set(def.id, def); return api; },
    component(def) { need(def, ['name', 'desc', 'fence', 'skeleton'], 'component'); components.set(def.name, def); return api; },
    deriver(family, fn, { first = false } = {}) { (derivers[family] ||= [])[first ? 'unshift' : 'push'](fn); return api; },
  };
  return {
    api, loaded,
    formFor: lang => forms.get(fences.get(lang)),
    form: name => forms.get(name),
    forms: () => [...forms.values()],
    router: name => routers.get(name), routerSpec: name => specs.get(name), routers: () => [...new Set([...routers.keys(), ...specs.keys()])],
    adapters,
    theme: name => themes.get(name), themes: () => [...themes.keys()],
    output: name => outputs.get(name), outputs: () => [...outputs.keys()],
    rules: () => [...rules.values()],
    annotations: () => [...annotations.values()],
    palettes: kind => [...palettes.values()].filter(p => !kind || p.kind === kind),
    derivers: () => derivers,
    components: () => [...components.values()],
    use(plugin, source = 'inline') {
      const def = typeof plugin === 'function' ? { name: source, apiVersion: API_VERSION, setup: plugin } : plugin;
      if ((def.apiVersion ?? API_VERSION) !== API_VERSION) throw new Error(`插件 ${def.name} 需要 apiVersion ${def.apiVersion}，当前是 ${API_VERSION}`);
      def.setup(api);
      loaded.push(def.name || source);
    },
  };
}
