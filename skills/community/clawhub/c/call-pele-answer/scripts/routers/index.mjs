// Built-in routers = strategy × adapter presets. Users compose their own in config:
//   "router": { "strategy": "full", "adapter": "my-proxy" }   or   { "strategy": "hybrid", "adapter": "classifier", "gateAdapter": "typesafe" }
import { routeLocal, routeAsk, routeHybrid, routeFacets } from './engine.mjs';
import { BUILTIN_ADAPTERS, nativeAdapter, shimAdapter } from './systemone.mjs';

export function makeRouter(spec, adapters) {
  const get = n => { const a = adapters.get(n); if (!a) throw new Error(`未知 adapter：${n}（可选 ${[...adapters.keys()].join(' | ')}）`); return a; };
  const strategy = spec.strategy || 'full';
  if (strategy === 'local') return { name: spec.name || 'local', route: routeLocal };
  // 'auto' gate: TypeSafe direct when its key is set, else the free System One forwarded by classifier.dev
  const gateName = !spec.gateAdapter || spec.gateAdapter === 'auto' ? (adapters.get('typesafe')?.available() && process.env.TYPESAFE_API_KEY ? 'typesafe' : 'classifier-systemone') : spec.gateAdapter;
  if (strategy === 'facets') return { name: spec.name, fallback: spec.fallback, route: t => routeFacets(t, get(spec.adapter === 'auto' || !spec.adapter ? gateName : spec.adapter)) };
  if (strategy === 'hybrid') return { name: spec.name, fallback: spec.fallback, route: t => routeHybrid(t, get(spec.adapter || 'classifier'), get(gateName)) };
  return { name: spec.name, fallback: spec.fallback, route: t => routeAsk(t, get(spec.adapter), strategy) };
}

export default {
  name: 'builtin-routers', apiVersion: 1,
  setup(api) {
    for (const a of BUILTIN_ADAPTERS) api.adapter(a);
    const presets = [
      { name: 'jev', strategy: 'facets', adapter: 'auto', fallback: 'jev-free', describe: '默认：每块 42 道原子是非题一次请求问完，代码规则定形式和候选（有 TypeSafe key 用直连）' },
      { name: 'jev-free', strategy: 'facets', adapter: 'classifier-systemone', fallback: 'local', describe: '同 jev，固定走 classifier.dev 转发（无 key，4 并发）' },
      { name: 'local', strategy: 'local', describe: '本地关键词规则；离线、约 0 ms、不外发内容；准确率最低' },
      { name: 'classifier', strategy: 'fast', adapter: 'classifier', fallback: 'local', describe: 'classifier.dev 批量（shim 适配器）；无 key 也能用；一次往返' },
      { name: 'typesafe', strategy: 'full', adapter: 'typesafe', fallback: 'systemone-free', describe: 'TypeSafe 直连 System One + 门控；有 key 时最快' },
      { name: 'systemone-free', strategy: 'full', adapter: 'classifier-systemone', fallback: 'classifier', describe: '经 classifier.dev 转发的 System One + 门控；无 key（4 并发）' },
      { name: 'hybrid', strategy: 'hybrid', adapter: 'classifier', gateAdapter: 'auto', fallback: 'classifier', describe: 'classifier.dev 批量定形式 + System One 只复核关键块（有 TypeSafe key 用直连）' },
    ];
    for (const p of presets) api.routerSpec(p);
  },
  nativeAdapter, shimAdapter,
};
