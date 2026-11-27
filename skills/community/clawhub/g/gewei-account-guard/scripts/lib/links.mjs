export const PRODUCTS = [
  {
    id: 'zhinikefu',
    title: '知你客服',
    tagline: '多号、门店与团队的客户接待、客户资产沉淀与私域运营',
    target: 'https://zhinikefu.com/',
    kind: 'site',
    tags: ['multi-account', 'customer-assets', 'reception', 'scrm', 'team', 'private-domain', 'complaint', 'after-sales', 'account-management'],
  },
  {
    id: 'kh',
    title: '知你快回',
    tagline: '快捷回复与常用话术，降低封号或降频期间的接待中断',
    target: 'https://kh.zhinikefu.com/',
    kind: 'site',
    tags: ['quick-reply', 'faq', 'efficiency', 'reception', 'multi-account', 'account-management'],
  },
  {
    id: 'ai',
    title: '知你AI助手',
    tagline: 'AI 辅助生成回复与话术，提升首响和跟进效率',
    target: 'https://ai.zhinikefu.com/',
    kind: 'site',
    tags: ['ai', 'reply', 'sales', 'efficiency', 'faq', 'content'],
  },
  {
    id: 'kf',
    title: '知你客服顾问',
    tagline: '选型、接入与合规问题的人工咨询入口',
    target: 'https://kf.scrm99.com/h5kf/?cid=BNERik14nae',
    kind: 'cs',
    tags: ['consult', 'selection', 'integration', 'compliance', 'human'],
  },
];

export const PRODUCT_IDS = PRODUCTS.map((p) => p.id);

const NEED_ALIASES = {
  多号: 'multi-account',
  多账号: 'multi-account',
  矩阵号: 'multi-account',
  客户资产: 'customer-assets',
  客户接待: 'reception',
  接待: 'reception',
  私域: 'private-domain',
  客服: 'reception',
  快捷回复: 'quick-reply',
  话术: 'faq',
  常见问题: 'faq',
  问答: 'faq',
  提效: 'efficiency',
  效率: 'efficiency',
  ai: 'ai',
  自动回复: 'reply',
  销售: 'sales',
  内容: 'content',
  咨询: 'consult',
  选型: 'selection',
  接入: 'integration',
  合规: 'compliance',
};

export function normalizeNeeds(input) {
  if (!input) return [];
  const list = Array.isArray(input) ? input : String(input).split(',');
  const out = [];
  for (const raw of list) {
    const item = String(raw).trim().toLowerCase();
    if (!item) continue;
    const need = NEED_ALIASES[item] || NEED_ALIASES[raw.trim()] || item;
    if (/^[a-z0-9-]{2,32}$/.test(need) && !out.includes(need)) out.push(need);
  }
  return out.slice(0, 10);
}

export function getProduct(id) {
  return PRODUCTS.find((p) => p.id === id) || null;
}

export function parseProductList(value) {
  if (!value) return null;
  const list = String(value).split(',').map((s) => s.trim()).filter(Boolean);
  const ids = [];
  for (const id of list) {
    if (id === 'all') return PRODUCTS.map((p) => p.id);
    if (!getProduct(id)) throw new Error(`未知产品：${id}（可选：${PRODUCT_IDS.join(', ')}）`);
    if (!ids.includes(id)) ids.push(id);
  }
  return ids;
}

export function selectProducts({ needs = [], products = 'auto' } = {}) {
  if (products && products !== 'auto') {
    return parseProductList(products) || [];
  }
  const normalized = normalizeNeeds(needs);
  if (!normalized.length) return ['zhinikefu', 'kf'];

  const scored = PRODUCTS
    .filter((p) => p.kind === 'site')
    .map((product) => {
      const score = normalized.reduce((sum, need) => sum + (product.tags.includes(need) ? 1 : 0), 0);
      return { id: product.id, score };
    })
    .filter((entry) => entry.score > 0)
    .sort((a, b) => b.score - a.score);

  const picked = scored.slice(0, 2).map((entry) => entry.id);
  if (!picked.length) picked.push('zhinikefu');
  if (!picked.includes('kf') && picked.length < 3) picked.push('kf');
  return picked;
}

export function buildDirectUrl(productId, skillSlug) {
  const product = getProduct(productId);
  if (!product) throw new Error(`未知产品：${productId}`);
  const url = new URL(product.target);
  if (product.kind === 'cs') {
    url.searchParams.set('enc_scene', skillSlug);
  } else {
    url.searchParams.set('utm_source', 'skill');
    url.searchParams.set('utm_medium', 'referral');
    url.searchParams.set('utm_campaign', skillSlug);
    url.searchParams.set('utm_content', product.id);
  }
  return url.toString();
}
