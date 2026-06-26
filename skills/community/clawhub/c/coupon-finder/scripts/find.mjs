/**
 * 场景优惠快取 — 查询引擎
 * 用法: node find.mjs "我要点外卖"
 *       node find.mjs "星巴克折扣" --limit 3
 *       node find.mjs "打车优惠" --format json
 */
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import path from 'path';
const require = createRequire(import.meta.url);
const __dir = path.dirname(fileURLToPath(import.meta.url));

const DB_PATH = path.join(__dir, '../data/activities.json');

// ─── 配置 ────────────────────────────────────────────────────────────────────
const SHARE_URL = 'https://my.feishu.cn/share/base/form/shrcn4ERBYeALeE2cF8SMPIqHUE';

// ─── 场景关键词映射 ──────────────────────────────────────────────────────────
const SCENE_MAP = {
  // 外卖
  '外卖': ['外卖','点餐','吃饭','吃东西','美团外卖','饿了么','京东外卖'],
  '美团外卖': ['美团外卖','美团点餐'],
  '饿了么': ['饿了么','ele'],
  '京东外卖': ['京东外卖','jd外卖'],
  // 打车出行
  '打车': ['打车','出行','网约车','顺风车','滴滴','花小猪','t3','代驾'],
  '代驾': ['代驾'],
  // 酒店住宿
  '酒店': ['酒店','住宿','订房','住房','宾馆','民宿'],
  '民宿': ['民宿'],
  // 旅游
  '旅游': ['旅游','度假','出游','景点','门票','出行','旅行'],
  '机票': ['机票','飞机','航班'],
  '电影': ['电影','看电影','影票','电影票','观影'],
  // 咖啡茶饮
  '咖啡': ['咖啡','星巴克','瑞幸','奈雪','喜茶','奶茶','饮品','茶'],
  '星巴克': ['星巴克'],
  '瑞幸': ['瑞幸'],
  '喜茶': ['喜茶'],
  '奈雪': ['奈雪'],
  // 快餐
  '快餐': ['快餐','肯德基','kfc','麦当劳','汉堡王','必胜客'],
  '肯德基': ['肯德基','kfc'],
  '麦当劳': ['麦当劳'],
  '汉堡王': ['汉堡王'],
  '必胜客': ['必胜客'],
  // 超市零售
  '超市': ['超市','零售','商超','果蔬','生鲜','便利'],
  '医药': ['买药','医药','健康','药店'],
  '水果': ['水果','百果园','鲜花'],
  // 美容
  '美容': ['丽人','美容','变美','美发','美甲'],
  // 娱乐
  '娱乐': ['娱乐','玩乐','游玩','休闲'],
  // 快递
  '快递': ['快递','寄件','寄快递'],
  // 优惠类型
  '红包': ['红包','领红包'],
  '优惠券': ['优惠券','券','领券'],
  '免费': ['免费','白嫖','0元','免单','霸王餐'],
  '折扣': ['折扣','打折','优惠','省钱'],
  '学生': ['学生','校园'],
  '新客': ['新客','新用户','首单'],
};

// ─── 链接优先级 ──────────────────────────────────────────────────────────────
function getBestLink(links) {
  for (const key of ['官方短链接', 'H5', '口令', '小程序路径', 'DeepLink']) {
    if (links[key]) return { type: key, url: links[key] };
  }
  return null;
}

// ─── 查询函数 ────────────────────────────────────────────────────────────────
export function queryActivities(query, opts = {}) {
  const { limit = 5, tags: filterTags = [] } = opts;
  const db = require(DB_PATH);
  const activities = db.activities;

  const q = query.toLowerCase();

  // 收集匹配的标签/关键词
  const matchedScenes = new Set();
  for (const [scene, keywords] of Object.entries(SCENE_MAP)) {
    if (keywords.some(k => q.includes(k.toLowerCase()))) {
      matchedScenes.add(scene);
    }
  }

  // 如果没匹配到场景，直接用原始词做模糊匹配
  const useFulltext = matchedScenes.size === 0;

  // 评分函数
  function score(a) {
    let s = 0;
    const text = (a.name + ' ' + (a.description || '')).toLowerCase();

    // 标签匹配
    for (const scene of matchedScenes) {
      if (a.tags.includes(scene)) s += 10;
      // 标签部分包含
      if (a.tags.some(t => t.toLowerCase().includes(scene.toLowerCase()))) s += 5;
    }

    // 全文匹配
    if (useFulltext) {
      const words = q.split(/\s+/).filter(w => w.length > 1);
      for (const w of words) {
        if (a.name.toLowerCase().includes(w)) s += 8;
        if (text.includes(w)) s += 4;
      }
    }

    // 外部筛选标签
    for (const ft of filterTags) {
      if (a.tags.includes(ft)) s += 15;
    }

    // 有更多链接类型加分
    s += Object.keys(a.links).length * 0.5;

    // 官方短链接加分
    if (a.links['官方短链接']) s += 2;

    return s;
  }

  return activities
    .map(a => ({ ...a, _score: score(a) }))
    .filter(a => a._score > 0)
    .sort((a, b) => b._score - a._score)
    .slice(0, limit)
    .map(({ _score, ...a }) => a);
}

// ─── 格式化输出 ──────────────────────────────────────────────────────────────
export function formatResults(results, query) {
  if (results.length === 0) {
    return `抱歉，没有找到与「${query}」相关的优惠活动。\n你可以试试：外卖、打车、酒店、咖啡、电影、超市等关键词。`;
  }

  const lines = [`🔍 「${query}」相关优惠 (${results.length}条)\n`];

  results.forEach((a, i) => {
    const best = getBestLink(a.links);
    const allTypes = Object.keys(a.links).join(' · ');
    const tags = a.tags.slice(0, 5).join(' ');

    lines.push(`${i + 1}. **${a.name}**`);
    lines.push(`   📝 ${a.description || '—'}`);
    lines.push(`   🏷 ${tags}`);
    if (best) {
      lines.push(`   🔗 ${best.type}: ${best.url}`);
      if (Object.keys(a.links).length > 1) {
        lines.push(`   📎 其他格式: ${allTypes}`);
      }
    }
    lines.push('');
  });

  // 分享引导
  lines.push('─'.repeat(30));
  lines.push(`💡 发现更好的优惠？欢迎分享给大家！`);
  lines.push(`📮 提交活动链接: ${SHARE_URL}`);

  return lines.join('\n');
}

// ─── CLI 入口 ─────────────────────────────────────────────────────────────────
if (process.argv[1] && process.argv[1].includes('find')) {
  const args = process.argv.slice(2);
  const query = args.filter(a => !a.startsWith('--')).join(' ');
  const limitArg = args.find(a => a.startsWith('--limit='));
  const limit = limitArg ? parseInt(limitArg.split('=')[1]) : 5;
  const fmt = args.includes('--format=json') ? 'json' : 'text';

  if (!query) {
    console.log('用法: node find.mjs <查询词> [--limit=5] [--format=json]');
    process.exit(0);
  }

  const results = queryActivities(query, { limit });

  if (fmt === 'json') {
    console.log(JSON.stringify(results, null, 2));
  } else {
    console.log(formatResults(results, query));
  }
}
