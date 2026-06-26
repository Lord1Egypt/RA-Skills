#!/usr/bin/env node
/**
 * career-news — morning-push.js
 * 每日早 7:00 为所有注册用户生成职业新闻推送 prompt
 *
 * 用法:
 *   node scripts/morning-push.js                         # 全量推送
 *   node scripts/morning-push.js --user <userId>         # 单用户测试
 *   node scripts/morning-push.js --profession <prof>     # 覆盖职业
 *   node scripts/morning-push.js --dry-run               # 只打印，不写文件
 */

const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '..', 'data', 'users');

const args = process.argv.slice(2);
const userIdx = args.indexOf('--user');
const targetUser = userIdx !== -1 ? args[userIdx + 1] : null;
const profIdx = args.indexOf('--profession');
const profOverride = profIdx !== -1 ? args[profIdx + 1] : null;
const dryRun = args.includes('--dry-run');

const now = new Date();
const dateStr_zh = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日`;
const dateStr_en = now.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });

// 职业关键词配置（用于指导搜索）
const PROFESSION_CONFIG = {
  doctor: {
    zh: { label: '医生/医疗从业者', keywords: ['医学研究', '临床指南', '医疗政策', '新药审批', '公共卫生'], sources: ['NEJM', 'Lancet', 'JAMA', '丁香园', '健康时报'] },
    en: { label: 'Doctor / Healthcare', keywords: ['clinical research', 'FDA approvals', 'medical policy', 'public health', 'treatment guidelines'], sources: ['NEJM', 'Lancet', 'JAMA', 'Medscape', 'CDC'] }
  },
  lawyer: {
    zh: { label: '律师/法律从业者', keywords: ['司法改革', '最高法判例', '商事仲裁', '合规监管', '法律科技'], sources: ['法制日报', '人民法院报', '中国法律评论'] },
    en: { label: 'Lawyer / Legal', keywords: ['supreme court', 'regulatory changes', 'legal tech', 'compliance', 'litigation trends'], sources: ['Bloomberg Law', 'Reuters Legal', 'Law360', 'ABA Journal'] }
  },
  engineer: {
    zh: { label: '工程师', keywords: ['工程技术', '制造业', '自动化', '基础设施', '行业标准'], sources: ['IEEE', '工程师网', '机械工业信息'] },
    en: { label: 'Engineer', keywords: ['engineering innovation', 'manufacturing', 'automation', 'infrastructure', 'industry standards'], sources: ['IEEE Spectrum', 'Engineering News-Record', 'IndustryWeek'] }
  },
  developer: {
    zh: { label: '软件开发者', keywords: ['编程语言', '开源项目', 'AI工具', '框架发布', '云原生'], sources: ['GitHub', 'InfoQ', 'V2EX', '掘金'] },
    en: { label: 'Software Developer', keywords: ['programming', 'open source', 'AI tools', 'framework releases', 'cloud native'], sources: ['GitHub', 'Hacker News', 'TechCrunch', 'The Verge', 'DEV.to'] }
  },
  designer: {
    zh: { label: '设计师', keywords: ['设计趋势', 'UI/UX', '品牌设计', '设计工具', '视觉创意'], sources: ['站酷', 'Behance', 'UI中国', 'UISDC'] },
    en: { label: 'Designer', keywords: ['design trends', 'UI/UX', 'branding', 'design tools', 'visual creativity'], sources: ['Behance', 'Dribbble', 'Creative Bloq', 'Smashing Magazine'] }
  },
  'product-manager': {
    zh: { label: '产品经理', keywords: ['产品设计', '用户体验', '增长策略', 'AI产品', '行业案例'], sources: ['人人都是产品经理', '产品壹佰', '36氪'] },
    en: { label: 'Product Manager', keywords: ['product strategy', 'user experience', 'growth hacking', 'AI products', 'case studies'], sources: ['Product Hunt', 'Mind the Product', 'Lenny\'s Newsletter', 'First Round Review'] }
  },
  investor: {
    zh: { label: '投资人/金融从业者', keywords: ['A股', '港股', '美股', '宏观经济', '投资策略', '并购动态'], sources: ['财新', '华尔街见闻', '彭博', '路透'] },
    en: { label: 'Investor / Finance', keywords: ['markets', 'macro economy', 'investment strategy', 'M&A', 'earnings'], sources: ['Bloomberg', 'Reuters', 'Financial Times', 'WSJ', 'Seeking Alpha'] }
  },
  teacher: {
    zh: { label: '教师/教育从业者', keywords: ['教育改革', '课程标准', '教育技术', '高考政策', '教师发展'], sources: ['中国教育报', '人民教育', '教育部官网'] },
    en: { label: 'Teacher / Educator', keywords: ['education reform', 'curriculum', 'edtech', 'teaching methods', 'learning research'], sources: ['Education Week', 'EdSurge', 'ASCD', 'TES'] }
  },
  journalist: {
    zh: { label: '记者/媒体从业者', keywords: ['新闻业动态', '媒体转型', '新闻自由', '报道伦理', '内容创作'], sources: ['中国新闻周刊', '澎湃', 'NiemanLab'] },
    en: { label: 'Journalist / Media', keywords: ['journalism', 'media industry', 'press freedom', 'digital media', 'investigative reporting'], sources: ['NiemanLab', 'Columbia Journalism Review', 'Poynter', 'Reuters Institute'] }
  },
  entrepreneur: {
    zh: { label: '创业者', keywords: ['创投融资', '创业政策', 'AI创业', '出海机会', '商业模式'], sources: ['36氪', '创业邦', '极客公园', 'TechCrunch中文版'] },
    en: { label: 'Entrepreneur', keywords: ['startup funding', 'venture capital', 'AI startups', 'business models', 'founder stories'], sources: ['TechCrunch', 'Crunchbase', 'Y Combinator', 'First Round Review', 'Indie Hackers'] }
  },
  researcher: {
    zh: { label: '研究员/学者', keywords: ['学术前沿', '科研政策', '论文发表', '科技突破', '基金申请'], sources: ['Nature', 'Science', '中国科学院', '国家自然科学基金'] },
    en: { label: 'Researcher', keywords: ['research breakthroughs', 'academic publications', 'science policy', 'grant funding', 'peer review'], sources: ['Nature', 'Science', 'arXiv', 'Retraction Watch', 'Scholarly Kitchen'] }
  },
  marketing: {
    zh: { label: '市场营销', keywords: ['营销趋势', '广告平台', '社交媒体运营', '品牌案例', '消费者洞察'], sources: ['营销界', '广告门', '数英网', '4A广告提案'] },
    en: { label: 'Marketing', keywords: ['marketing trends', 'advertising platforms', 'social media', 'brand campaigns', 'consumer insights'], sources: ['Marketing Week', 'AdAge', 'Adweek', 'HubSpot Blog', 'MarketingProfs'] }
  },
  hr: {
    zh: { label: '人力资源', keywords: ['人才管理', '招聘趋势', '劳动法规', '员工福利', '组织文化'], sources: ['中国人力资源网', 'HR369', '智联招聘研究院'] },
    en: { label: 'HR', keywords: ['talent management', 'hiring trends', 'labor law', 'employee benefits', 'organizational culture'], sources: ['SHRM', 'HR Dive', 'Workable Blog', 'Josh Bersin'] }
  },
  sales: {
    zh: { label: '销售', keywords: ['销售方法论', '客户成功', '销售工具', '市场动态', 'CRM趋势'], sources: ['销售与市场', 'B2B圈', '36氪企服'] },
    en: { label: 'Sales', keywords: ['sales methodology', 'customer success', 'sales tools', 'CRM', 'revenue operations'], sources: ['Sales Hacker', 'HubSpot Sales Blog', 'Salesforce Blog', 'Gong.io'] }
  }
};

// Load users
let users = [];
if (targetUser) {
  const fp = path.join(USERS_DIR, `${targetUser.replace(/[^a-zA-Z0-9_-]/g, '')}.json`);
  if (!fs.existsSync(fp)) {
    console.error(`User "${targetUser}" not found.`);
    process.exit(1);
  }
  users = [JSON.parse(fs.readFileSync(fp, 'utf8'))];
} else {
  if (!fs.existsSync(USERS_DIR)) {
    console.log('No users registered yet.');
    process.exit(0);
  }
  users = fs.readdirSync(USERS_DIR)
    .filter(f => f.endsWith('.json'))
    .map(f => JSON.parse(fs.readFileSync(path.join(USERS_DIR, f), 'utf8')))
    .filter(u => u.pushEnabled !== false);
}

if (users.length === 0) {
  console.log('No active users to push.');
  process.exit(0);
}

// Helper: generate one profession brief block
function professionBlock(user, profession, lang, region, dateStr, extraKeywords, isExtra) {
  const cfg = (PROFESSION_CONFIG[profession] || PROFESSION_CONFIG['developer'])[lang] || PROFESSION_CONFIG['developer']['en'];
  const tag = isExtra ? ' ★ extra subscription' : ' ✦ primary';

  if (lang === 'en') {
    return `[Career News Morning Push | user: ${user.userId} | profession: ${profession}${tag} | lang: en | region: ${region} | ${dateStr}]

Please search and compile a morning news brief for this user.

Profession: ${cfg.label}
Search keywords: ${cfg.keywords.join(', ')}${extraKeywords ? ', ' + extraKeywords : ''}
Priority sources: ${cfg.sources.join(', ')}
Region focus: ${region.toUpperCase()}

Search steps (execute ALL):
1. Search X (Twitter): "${cfg.keywords[0]} OR ${cfg.keywords[1]}" — last 24h, min 100 likes/retweets
2. Google News: "${cfg.label} news ${dateStr}" site:reuters.com OR site:bloomberg.com OR site:techcrunch.com
3. Ask Grok: "What are the 3 most important developments for ${cfg.label} professionals today, ${dateStr}?"
4. Scan priority sources: ${cfg.sources.slice(0, 3).join(', ')} for top stories

Compile rules:
- Select exactly 5 stories: mix of breaking news, analysis, and one forward-looking item
- Each story: headline + 2-sentence summary + source + URL
- Flag stories from X with 🐦, Grok synthesis with 🤖, major media with 📰
- Do NOT include stories older than 48 hours
- Do NOT include opinion pieces unless author has direct field experience

Output format:
📰 Morning Brief · ${cfg.label} · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[source flag] Story 1 headline
  → Summary (2 sentences). Source · URL

[source flag] Story 2 headline
  → Summary (2 sentences). Source · URL

[source flag] Story 3 headline
  → Summary (2 sentences). Source · URL

[source flag] Story 4 headline
  → Summary (2 sentences). Source · URL

[source flag] Story 5 headline
  → Summary (2 sentences). Source · URL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 One sentence on the most important trend to watch today.`;

  } else {
    return `[职业新闻早报 | 用户：${user.userId} | 职业：${profession}${isExtra ? ' ★ 额外订阅' : ' ✦ 主职业'} | 语言：zh | 地区：${region} | ${dateStr}]

请为该用户搜索并整合今日职业新闻早报。

职业：${cfg.label}
搜索关键词：${cfg.keywords.join('、')}${extraKeywords ? '、' + extraKeywords : ''}
优先信源：${cfg.sources.join('、')}
地区聚焦：${region.toUpperCase()}

搜索步骤（必须全部执行）：
1. 搜索 X（Twitter）：关键词「${cfg.keywords[0]}」「${cfg.keywords[1]}」— 过去 24 小时内，互动量 100+ 的帖子
2. Google 新闻：搜索「${cfg.label} 最新动态 ${dateStr}」，优先 ${cfg.sources.slice(0,2).join('、')} 等媒体
3. 询问 Grok：「${dateStr}，${cfg.label}最重要的3条行业进展是什么？」
4. 扫描优先信源：${cfg.sources.slice(0, 3).join('、')} 的今日头条

整合规则：
- 精选5条：包含突发、深度分析、至少1条前瞻性内容
- 每条：标题 + 2句摘要 + 来源 + 链接
- X 来源标注 🐦，Grok 综合标注 🤖，主流媒体标注 📰
- 不收录 48 小时以前的内容
- 不收录与职业无直接关联的内容

输出格式：
📰 职业早报 · ${cfg.label} · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[来源标注] 新闻标题 1
  → 摘要（2句）。来源 · 链接

[来源标注] 新闻标题 2
  → 摘要（2句）。来源 · 链接

[来源标注] 新闻标题 3
  → 摘要（2句）。来源 · 链接

[来源标注] 新闻标题 4
  → 摘要（2句）。来源 · 链接

[来源标注] 新闻标题 5
  → 摘要（2句）。来源 · 链接

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 今日最值得关注的一个趋势（一句话）。`;
  }
}

users.forEach((user, i) => {
  const lang = user.language || 'zh';
  const region = user.region || (lang === 'zh' ? 'cn' : 'us');
  const extraKeywords = (user.keywords || []).join(lang === 'en' ? ', ' : '、');
  const dateStr = lang === 'en' ? dateStr_en : dateStr_zh;

  // Build ordered profession list: primary first, then extras
  const primaryProf = profOverride || user.profession || 'developer';
  const extraProfs = profOverride ? [] : (user.extraProfessions || []);
  const allProfs = [primaryProf, ...extraProfs];

  if (i > 0) console.log('\n' + '═'.repeat(60) + '\n');

  // Header when user has multiple subscriptions
  if (allProfs.length > 1) {
    if (lang === 'en') {
      console.log(`╔══ ${user.userId} · ${allProfs.length} profession briefs · ${dateStr} ══╗\n`);
    } else {
      console.log(`╔══ ${user.userId} · 今日 ${allProfs.length} 个职业早报 · ${dateStr} ══╗\n`);
    }
  }

  // One block per profession
  allProfs.forEach((prof, j) => {
    if (j > 0) console.log('\n' + '─'.repeat(60) + '\n');
    const isExtra = j > 0;
    console.log(professionBlock(user, prof, lang, region, dateStr, extraKeywords, isExtra));
  });

  // Tail hint when multiple professions
  if (allProfs.length > 1) {
    if (lang === 'en') {
      console.log(`\n╚══ End of ${user.userId}'s ${allProfs.length} briefs. To manage subscriptions: node scripts/manage-professions.js --userId ${user.userId} --list ══╝`);
    } else {
      console.log(`\n╚══ ${user.userId} 的 ${allProfs.length} 份早报推送完毕。管理订阅：node scripts/manage-professions.js --userId ${user.userId} --list ══╝`);
    }
  }
});
