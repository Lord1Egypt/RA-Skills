#!/usr/bin/env node
/**
 * career-news — news-query.js
 * Instant query for latest news by profession.
 *
 * Usage:
 *   node scripts/news-query.js <profession>
 *   node scripts/news-query.js developer
 *   node scripts/news-query.js investor --lang en --region us
 *   node scripts/news-query.js doctor --keywords "癌症研究,新药"
 *   node scripts/news-query.js --userId <id>              # query all of user's subscribed professions
 *   node scripts/news-query.js --userId <id> --all-professions
 *
 * Professions: doctor, lawyer, engineer, developer, designer,
 *   product-manager, investor, teacher, journalist, entrepreneur,
 *   researcher, marketing, hr, sales
 */

const fs = require('fs');
const path = require('path');
const USERS_DIR = path.join(__dirname, '..', 'data', 'users');

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const langArg = langIdx !== -1 ? args[langIdx + 1] : null;
const regionIdx = args.indexOf('--region');
const regionArg = regionIdx !== -1 ? args[regionIdx + 1] : null;
const kwIdx = args.indexOf('--keywords');
const kwArg = kwIdx !== -1 ? args[kwIdx + 1] : null;
const userIdx = args.indexOf('--userId');
const userIdArg = userIdx !== -1 ? args[userIdx + 1] : null;
const allProfsFlag = args.includes('--all-professions');

const rawProf = args.filter(a => !a.startsWith('--') && a !== langArg && a !== regionArg && a !== kwArg && a !== userIdArg)[0] || '';

const PROFESSION_ZH_MAP = {
  '医生': 'doctor', '医疗': 'doctor', '律师': 'lawyer', '法律': 'lawyer',
  '工程师': 'engineer', '开发者': 'developer', '开发': 'developer', '程序员': 'developer',
  '设计师': 'designer', '设计': 'designer', '产品经理': 'product-manager', '产品': 'product-manager',
  '投资': 'investor', '投资人': 'investor', '金融': 'investor', '教师': 'teacher', '教育': 'teacher',
  '记者': 'journalist', '媒体': 'journalist', '创业': 'entrepreneur', '创业者': 'entrepreneur',
  '研究员': 'researcher', '学者': 'researcher', '营销': 'marketing', '市场': 'marketing',
  '人力资源': 'hr', 'HR': 'hr', '销售': 'sales'
};

const VALID_PROFESSIONS = new Set([
  'doctor','lawyer','engineer','developer','designer','product-manager',
  'investor','teacher','journalist','entrepreneur','researcher','marketing','hr','sales'
]);

// --userId mode: query all of user's subscribed professions
if (userIdArg && (allProfsFlag || !rawProf)) {
  const safeId = userIdArg.replace(/[^a-zA-Z0-9_-]/g, '');
  const fp = path.join(USERS_DIR, `${safeId}.json`);
  if (!fs.existsSync(fp)) {
    console.error(`User "${userIdArg}" not found.`);
    process.exit(1);
  }
  const u = JSON.parse(fs.readFileSync(fp, 'utf8'));
  const userLang = langArg === 'en' ? 'en' : (u.language || 'zh');
  const userRegion = regionArg || u.region || (userLang === 'zh' ? 'cn' : 'us');
  const userKw = kwArg ? kwArg.split(',').map(k => k.trim()) : (u.keywords || []);
  const allProfs = [u.profession, ...(u.extraProfessions || [])].filter(Boolean);
  const now2 = new Date();
  const ds = userLang === 'en'
    ? now2.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })
    : `${now2.getFullYear()}年${now2.getMonth()+1}月${now2.getDate()}日`;

  if (userLang === 'en') {
    console.log(`Querying all ${allProfs.length} profession(s) for ${u.userId}: ${allProfs.join(', ')}\n`);
  } else {
    console.log(`为 ${u.userId} 查询全部 ${allProfs.length} 个订阅职业：${allProfs.join('、')}\n`);
  }

  allProfs.forEach((prof, idx) => {
    // Inline PROFESSION_CONFIG lookup will be done in the block below via re-invocation hint
    if (idx > 0) console.log('\n' + '─'.repeat(60) + '\n');
    const isExtra = idx > 0;
    const profLabel = userLang === 'en' ? `${prof}${isExtra ? ' ★ extra' : ' ✦ primary'}` : `${prof}${isExtra ? ' ★ 额外订阅' : ' ✦ 主职业'}`;
    if (userLang === 'en') {
      console.log(`[Career News Query | user: ${u.userId} | profession: ${profLabel} | lang: en | region: ${userRegion.toUpperCase()} | ${ds}]\n→ Run: node scripts/news-query.js ${prof} --lang en --region ${userRegion}${userKw.length ? ' --keywords "' + userKw.join(',') + '"' : ''}`);
    } else {
      console.log(`[职业新闻即时查询 | 用户：${u.userId} | 职业：${profLabel} | 语言：zh | 地区：${userRegion.toUpperCase()} | ${ds}]\n→ 执行：node scripts/news-query.js ${prof} --region ${userRegion}${userKw.length ? ' --keywords "' + userKw.join(',') + '"' : ''}`);
    }
  });
  process.exit(0);
}

if (!rawProf && !userIdArg) {
  console.error('Usage: node scripts/news-query.js <profession> [--lang zh|en] [--region cn|us|global] [--keywords "kw1,kw2"]');
  console.error('       node scripts/news-query.js --userId <id>   # query all subscribed professions');
  console.error('');
  console.error('Professions: doctor, lawyer, engineer, developer, designer, product-manager,');
  console.error('             investor, teacher, journalist, entrepreneur, researcher, marketing, hr, sales');
  process.exit(1);
}

let profession = PROFESSION_ZH_MAP[rawProf] || (VALID_PROFESSIONS.has(rawProf) ? rawProf : null);
if (!profession) {
  for (const [key, val] of Object.entries(PROFESSION_ZH_MAP)) {
    if (rawProf.includes(key)) { profession = val; break; }
  }
}
if (!profession) profession = 'developer';

const lang = langArg === 'en' ? 'en' : 'zh';
const region = regionArg || (lang === 'zh' ? 'cn' : 'us');
const extraKw = kwArg ? kwArg.split(',').map(k => k.trim()) : [];

const now = new Date();
const dateStr = lang === 'en'
  ? now.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })
  : `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日`;

const PROFESSION_CONFIG = {
  doctor: {
    zh: { label: '医生/医疗从业者', kw: ['医学研究', '临床指南', '医疗政策', '新药审批', '公共卫生'], src: ['NEJM', 'Lancet', '丁香园'] },
    en: { label: 'Doctor / Healthcare', kw: ['clinical research', 'FDA approvals', 'medical policy', 'public health'], src: ['NEJM', 'Lancet', 'Medscape'] }
  },
  lawyer: {
    zh: { label: '律师/法律从业者', kw: ['司法改革', '最高法判例', '商事仲裁', '合规监管'], src: ['法制日报', '人民法院报'] },
    en: { label: 'Lawyer / Legal', kw: ['supreme court', 'regulatory changes', 'legal tech', 'compliance'], src: ['Bloomberg Law', 'Law360'] }
  },
  engineer: {
    zh: { label: '工程师', kw: ['工程技术', '制造业', '自动化', '行业标准'], src: ['IEEE', '机械工业信息'] },
    en: { label: 'Engineer', kw: ['engineering innovation', 'manufacturing', 'automation'], src: ['IEEE Spectrum', 'IndustryWeek'] }
  },
  developer: {
    zh: { label: '软件开发者', kw: ['编程语言', '开源项目', 'AI工具', '框架发布'], src: ['GitHub', 'InfoQ', '掘金'] },
    en: { label: 'Software Developer', kw: ['programming', 'open source', 'AI tools', 'framework releases'], src: ['GitHub', 'Hacker News', 'TechCrunch'] }
  },
  designer: {
    zh: { label: '设计师', kw: ['设计趋势', 'UI/UX', '设计工具'], src: ['站酷', 'UISDC'] },
    en: { label: 'Designer', kw: ['design trends', 'UI/UX', 'design tools'], src: ['Behance', 'Smashing Magazine'] }
  },
  'product-manager': {
    zh: { label: '产品经理', kw: ['产品设计', '用户体验', '增长策略', 'AI产品'], src: ['人人都是产品经理', '36氪'] },
    en: { label: 'Product Manager', kw: ['product strategy', 'user experience', 'growth', 'AI products'], src: ['Product Hunt', 'Lenny\'s Newsletter'] }
  },
  investor: {
    zh: { label: '投资人/金融从业者', kw: ['A股', '宏观经济', '投资策略', '并购动态'], src: ['财新', '华尔街见闻'] },
    en: { label: 'Investor / Finance', kw: ['markets', 'macro economy', 'M&A', 'earnings'], src: ['Bloomberg', 'Financial Times', 'WSJ'] }
  },
  teacher: {
    zh: { label: '教师/教育从业者', kw: ['教育改革', '课程标准', '教育技术'], src: ['中国教育报', '人民教育'] },
    en: { label: 'Teacher / Educator', kw: ['education reform', 'curriculum', 'edtech'], src: ['Education Week', 'EdSurge'] }
  },
  journalist: {
    zh: { label: '记者/媒体从业者', kw: ['新闻业动态', '媒体转型', '新闻自由'], src: ['澎湃', 'NiemanLab'] },
    en: { label: 'Journalist / Media', kw: ['journalism', 'media industry', 'press freedom'], src: ['NiemanLab', 'Poynter'] }
  },
  entrepreneur: {
    zh: { label: '创业者', kw: ['创投融资', '创业政策', 'AI创业', '出海机会'], src: ['36氪', '极客公园'] },
    en: { label: 'Entrepreneur', kw: ['startup funding', 'venture capital', 'AI startups'], src: ['TechCrunch', 'Crunchbase', 'Y Combinator'] }
  },
  researcher: {
    zh: { label: '研究员/学者', kw: ['学术前沿', '科研政策', '论文发表', '科技突破'], src: ['Nature', 'Science', '中国科学院'] },
    en: { label: 'Researcher', kw: ['research breakthroughs', 'publications', 'science policy'], src: ['Nature', 'Science', 'arXiv'] }
  },
  marketing: {
    zh: { label: '市场营销', kw: ['营销趋势', '广告平台', '社交媒体运营'], src: ['广告门', '数英网'] },
    en: { label: 'Marketing', kw: ['marketing trends', 'advertising platforms', 'social media'], src: ['Marketing Week', 'AdAge'] }
  },
  hr: {
    zh: { label: '人力资源', kw: ['人才管理', '招聘趋势', '劳动法规'], src: ['中国人力资源网', '智联招聘研究院'] },
    en: { label: 'HR', kw: ['talent management', 'hiring trends', 'labor law'], src: ['SHRM', 'HR Dive'] }
  },
  sales: {
    zh: { label: '销售', kw: ['销售方法论', '客户成功', '销售工具'], src: ['销售与市场', 'B2B圈'] },
    en: { label: 'Sales', kw: ['sales methodology', 'customer success', 'CRM'], src: ['Sales Hacker', 'HubSpot Sales Blog'] }
  }
};

const cfg = (PROFESSION_CONFIG[profession] || PROFESSION_CONFIG['developer'])[lang];
const allKw = [...cfg.kw, ...extraKw];

if (lang === 'en') {
  console.log(`[Career News Query | profession: ${profession} | lang: en | region: ${region.toUpperCase()} | ${dateStr}]

Please find the latest news for a ${cfg.label} professional right now.

Keywords: ${allKw.join(', ')}
Priority sources: ${cfg.src.join(', ')}
Region: ${region.toUpperCase()}

Search steps:
1. X (Twitter): Search "${allKw[0]} OR ${allKw[1]}" — most recent posts with engagement
2. Google News: "${cfg.label} latest news today" — filter last 24h
3. Grok: "What's happening right now in ${cfg.label} field? Top 3 developments."
4. Check priority sources: ${cfg.src.slice(0,3).join(', ')}

Return exactly 5 stories. Format each as:
[source flag] Headline
  → 2-sentence summary. Source · URL

Source flags: 🐦 X/Twitter  🤖 Grok  📰 Media

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📰 ${cfg.label} News · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);

} else {
  console.log(`[职业新闻即时查询 | 职业：${profession} | 语言：zh | 地区：${region.toUpperCase()} | ${dateStr}]

请立即为${cfg.label}查找最新行业新闻。

关键词：${allKw.join('、')}
优先信源：${cfg.src.join('、')}
地区：${region.toUpperCase()}

搜索步骤：
1. X（Twitter）：搜索「${allKw[0]}」「${allKw[1]}」— 最新帖子，优先高互动
2. Google 新闻：「${cfg.label} 最新 今天」— 过去 24 小时
3. 询问 Grok：「${cfg.label}今天最重要的3条新闻是什么？」
4. 扫描优先信源：${cfg.src.slice(0,3).join('、')}

精选5条，格式：
[来源标注] 新闻标题
  → 2句摘要。来源 · 链接

来源标注：🐦 X/Twitter  🤖 Grok  📰 媒体

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📰 ${cfg.label} 新闻 · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
}
