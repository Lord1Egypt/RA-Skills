#!/usr/bin/env node

/**
 * 干饭.skill — 饭点提醒（Nudge）
 *
 * 到点了提醒你吃饭，随机推荐品类或餐馆。
 * 有餐馆库时推荐具体餐馆，空库时随机推荐美食品类。
 * 如果有 user-profile.json 则结合用户偏好推荐。
 * 设计为被 cron / Claude Code scheduled tasks / OpenClaw 定时调用。
 *
 * 用法：
 *   node nudge.mjs                    # 自动判断当前是哪顿
 *   node nudge.mjs --meal lunch       # 午餐提醒
 *   node nudge.mjs --meal dinner      # 晚餐提醒
 *   node nudge.mjs --meal late_night  # 宵夜提醒
 *   node nudge.mjs --style serious    # 正经模式
 *   node nudge.mjs --style chaotic    # 混沌模式（更离谱）
 *   node nudge.mjs --json             # JSON 输出（给 AI 消费）
 */

import { readdirSync, readFileSync, existsSync } from "fs";
import { resolve, dirname, join } from "path";
import { fileURLToPath } from "url";
import { parseArgs } from "util";

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(__dirname, "..");

const { values: args } = parseArgs({
  options: {
    meal: { type: "string", short: "m" },
    style: { type: "string", short: "s" },
    json: { type: "boolean", short: "j" },
    help: { type: "boolean", short: "h" },
  },
});

if (args.help) {
  console.log(`
🍜 干饭.skill — 饭点提醒

用法：
  node nudge.mjs [--meal lunch|dinner|late_night] [--style normal|chaotic] [--json]

定时任务示例：
  # crontab
  0 12 * * 1-5  cd /path/to/eat-skill && node schedule/nudge.mjs --meal lunch
  0 18 * * 1-5  cd /path/to/eat-skill && node schedule/nudge.mjs --meal dinner

  # Claude Code
  claude schedule "每天中午12点提醒我吃饭" --command "node schedule/nudge.mjs --meal lunch"
  `);
  process.exit(0);
}

// ═══════════════════════════════════════════
// 趣味文案库
// ═══════════════════════════════════════════

const OPENERS = {
  lunch: [
    "⏰ 中午了！你的胃发来一条消息：「在？」",
    "🔔 午饭铃响了！再不动筷子，下午要靠意念续命了。",
    "📢 友情提醒：你已经盯着屏幕 4 小时了，该给身体充个电了。",
    "🍜 11:50 警告：食堂座位正在以每秒 3 个的速度消失。",
    "⚡ 检测到你的血糖即将触及下限，建议立即进食。",
    "🎯 中午吃什么？这可能是今天你做的最重要的决定。",
    "📊 据统计，纠结午饭吃什么平均浪费 17 分钟。让我帮你省掉。",
    "🧠 你的大脑发来工单：「CPU 过热，请求午休 + 进食维护」",
    "💼 再不去吃饭，你的工位要被外卖盒子淹没了。",
    "🎪 午间美食抽奖开始！请看大屏幕——",
  ],
  dinner: [
    "🌆 太阳要下班了，你呢？先把晚饭解决了。",
    "🔔 晚饭铃！今天加班的话更要好好吃。",
    "🌙 晚上 6 点，你的胃准时打卡下班。",
    "🍽️ 一天辛苦了！晚饭是对自己最好的犒赏。",
    "📱 你的外卖 App 已经在后台蠢蠢欲动了。",
    "🏠 回家路上顺便吃？还是点外卖窝着？你说了算。",
    "⭐ 晚饭时间到！今天你值得吃顿好的。",
    "🎬 晚饭 + 下饭综艺，完美组合等你解锁。",
  ],
  late_night: [
    "🌙 夜深了还在肝？来点夜宵补补。",
    "🦉 猫头鹰模式已激活，夜宵加载中...",
    "🍜 深夜食堂上线。减肥的事明天再说。",
    "⚠️ 检测到深夜饥饿信号。减肥？那是明天的事。",
    "🌃 深夜觅食指南加载完毕。",
  ],
  breakfast: [
    "☀️ 早安！别空腹上班，先吃点东西。",
    "🥐 早餐是今天第一个好决定。",
    "☕ 新的一天从吃饱开始。",
  ],
};

const ROLL_EFFECTS = [
  "🎰 转盘转起来了...... 停！",
  "🎲 骰子在空中翻转...... 落地！",
  "🎯 飞镖扔出去了...... 中！",
  "🃏 洗牌中...... 翻！",
  "🎪 命运之轮开始旋转...... 锁定！",
  "🔮 水晶球正在显示...... 看到了！",
  "📡 美食雷达扫描中...... 捕获目标！",
  "🎡 摩天轮转了一圈...... 到站！",
];

const CLOSERS = [
  "不满意？回复「换一个」。但我建议别犹豫了，去吃！",
  "犹豫就会败北，果断就会白给——等等这不对。果断就能吃饱！",
  "人生苦短，少纠结，多干饭。",
  "选择困难？那就听我的。我从不后悔（因为我不用吃）。",
  "温馨提示：看着看着就不饿了，是假的。快去吃。",
  "这顿不吃，下顿更饿。经济学叫「沉没成本」。",
  "去吧！晚了就要排队了。",
  "别收藏了，收藏 = 再也不看。现在就去吃。",
];

const CHAOTIC_EXTRAS = [
  "🎭 今日隐藏任务：用你不常用的手吃饭。",
  "🎲 附加挑战：闭眼在菜单上指一个，就点那个。",
  "💀 极限操作：问同事「你吃什么」然后点一样的。",
  "🧪 实验性建议：今天试试你从没吃过的东西。",
  "🎪 社交任务：拉一个你不太熟的同事一起吃。",
  "📸 记录任务：今天的饭拍照发朋友圈，标题用 AI 帮你写。",
  "🏆 成就系统：连续 5 天不重样可以解锁「美食探险家」称号。",
];

// ═══════════════════════════════════════════
// 餐馆库读取
// ═══════════════════════════════════════════

function loadRestaurants() {
  const restaurantsDir = join(PROJECT_ROOT, "restaurants");
  if (!existsSync(restaurantsDir)) return [];

  const results = [];
  for (const dir of readdirSync(restaurantsDir, { withFileTypes: true })) {
    if (!dir.isDirectory()) continue;
    const skillPath = join(restaurantsDir, dir.name, "SKILL.md");
    if (!existsSync(skillPath)) continue;

    const content = readFileSync(skillPath, "utf-8");
    const info = parseSkillMd(content);
    if (info.name) {
      info.slug = dir.name;
      results.push(info);
    }
  }

  return results;
}

function parseSkillMd(content) {
  const info = {};
  const lines = content.split("\n");

  for (const line of lines) {
    if (line.startsWith("| 餐厅名称")) info.name = line.split("|")[2]?.trim();
    if (line.startsWith("| 品类")) info.category = line.split("|")[2]?.trim();
    if (line.startsWith("| 人均")) info.price = line.split("|")[2]?.trim();
    if (line.startsWith("| 地址")) info.address = line.split("|")[2]?.trim();
    if (line.startsWith("| 营业时间")) info.hours = line.split("|")[2]?.trim();
    if (line.startsWith("| 评分")) info.rating = line.split("|")[2]?.trim();
  }

  const dishMatch = content.match(/## 推荐菜\n\n([\s\S]*?)(?=\n##|\n---|\n$)/);
  if (dishMatch) {
    info.dishes = dishMatch[1]
      .split("\n")
      .filter((l) => l.startsWith("- **"))
      .map((l) => l.replace(/^- \*\*/, "").replace(/\*\*.*/, "").trim());
  }

  return info;
}

// ═══════════════════════════════════════════
// 美食品类库（空库时的随机推荐来源）
// ═══════════════════════════════════════════

const FOOD_CATEGORIES = {
  lunch: [
    { name: "川菜", emoji: "🌶️", dishes: "回锅肉、水煮鱼、宫保鸡丁", budget: "¥35-60" },
    { name: "面食", emoji: "🍜", dishes: "牛肉面、刀削面、炸酱面", budget: "¥15-30" },
    { name: "饺子", emoji: "🥟", dishes: "猪肉白菜、鲅鱼、虾仁三鲜", budget: "¥25-40" },
    { name: "盖浇饭", emoji: "🍚", dishes: "鱼香肉丝、番茄鸡蛋、红烧排骨", budget: "¥15-25" },
    { name: "日料", emoji: "🍱", dishes: "鳗鱼饭、拉面、寿司定食", budget: "¥40-80" },
    { name: "黄焖鸡", emoji: "🍗", dishes: "黄焖鸡米饭、加土豆、加宽粉", budget: "¥18-25" },
    { name: "麻辣烫", emoji: "🍲", dishes: "自选菜品+粉丝/面条", budget: "¥20-35" },
    { name: "汉堡", emoji: "🍔", dishes: "鸡腿堡、牛肉堡、薯条套餐", budget: "¥25-45" },
    { name: "粤菜", emoji: "🥘", dishes: "烧腊双拼饭、煲仔饭、云吞面", budget: "¥30-50" },
    { name: "韩餐", emoji: "🥓", dishes: "石锅拌饭、部队锅、韩式炸鸡", budget: "¥35-60" },
    { name: "沙拉轻食", emoji: "🥗", dishes: "鸡胸肉沙拉、牛油果碗、三明治", budget: "¥30-50" },
    { name: "西北菜", emoji: "🫓", dishes: "肉夹馍、油泼面、羊肉泡馍", budget: "¥20-40" },
  ],
  dinner: [
    { name: "火锅", emoji: "🍲", dishes: "毛肚、鸭肠、嫩牛肉、虾滑", budget: "¥60-100" },
    { name: "烧烤", emoji: "🔥", dishes: "羊肉串、烤鱼、烤韭菜、生蚝", budget: "¥50-80" },
    { name: "川菜", emoji: "🌶️", dishes: "酸菜鱼、毛血旺、麻婆豆腐", budget: "¥40-70" },
    { name: "东北菜", emoji: "🥘", dishes: "锅包肉、铁锅炖、地三鲜", budget: "¥40-60" },
    { name: "日料", emoji: "🍣", dishes: "居酒屋、刺身拼盘、烤串", budget: "¥80-150" },
    { name: "湘菜", emoji: "🌶️", dishes: "剁椒鱼头、小炒肉、辣椒炒肉", budget: "¥40-60" },
    { name: "串串", emoji: "🍢", dishes: "牛肉串、脑花、藕片、贡菜", budget: "¥40-70" },
    { name: "小龙虾", emoji: "🦞", dishes: "蒜蓉、十三香、麻辣", budget: "¥80-120" },
    { name: "披萨", emoji: "🍕", dishes: "玛格丽特、培根、夏威夷", budget: "¥50-80" },
    { name: "江浙菜", emoji: "🐟", dishes: "红烧肉、西湖醋鱼、龙井虾仁", budget: "¥50-80" },
  ],
  late_night: [
    { name: "烧烤", emoji: "🔥", dishes: "烤串+啤酒，深夜标配", budget: "¥40-70" },
    { name: "小龙虾", emoji: "🦞", dishes: "麻辣小龙虾+毛豆+花生", budget: "¥60-100" },
    { name: "麻辣烫", emoji: "🍲", dishes: "深夜暖胃之选", budget: "¥15-30" },
    { name: "泡面", emoji: "🍜", dishes: "没错，泡面加蛋加火腿肠", budget: "¥5" },
    { name: "炒饭炒面", emoji: "🍳", dishes: "蛋炒饭、炒河粉、炒年糕", budget: "¥15-25" },
  ],
  breakfast: [
    { name: "包子油条", emoji: "🥟", dishes: "肉包、豆浆、油条、茶叶蛋", budget: "¥8-15" },
    { name: "煎饼果子", emoji: "🫓", dishes: "加蛋加肠加脆片", budget: "¥8-12" },
    { name: "粥", emoji: "🥣", dishes: "皮蛋瘦肉粥、小米粥+咸菜", budget: "¥10-15" },
    { name: "咖啡面包", emoji: "☕", dishes: "美式+可颂、拿铁+贝果", budget: "¥20-35" },
  ],
};

// ═══════════════════════════════════════════
// 用户画像读取
// ═══════════════════════════════════════════

function loadUserProfile() {
  const profilePath = join(PROJECT_ROOT, "user-profile.json");
  if (!existsSync(profilePath)) return null;
  try {
    return JSON.parse(readFileSync(profilePath, "utf-8"));
  } catch {
    return null;
  }
}

function filterByProfile(categories, profile) {
  if (!profile) return categories;
  return categories.filter((cat) => {
    if (profile.taste?.hate?.some((h) => cat.name.includes(h) || cat.dishes.includes(h))) {
      return false;
    }
    return true;
  });
}

function getRecentFoods(profile) {
  if (!profile?.history) return [];
  const threeDaysAgo = Date.now() - 3 * 24 * 60 * 60 * 1000;
  return profile.history
    .filter((h) => new Date(h.date).getTime() > threeDaysAgo)
    .map((h) => h.food);
}

// ═══════════════════════════════════════════
// 推荐引擎
// ═══════════════════════════════════════════

function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function detectMeal() {
  const hour = new Date().getHours();
  if (hour >= 6 && hour < 10) return "breakfast";
  if (hour >= 10 && hour < 14) return "lunch";
  if (hour >= 14 && hour < 20) return "dinner";
  return "late_night";
}

function formatRecommendation(restaurant) {
  let card = `\n   👉 **${restaurant.name}**\n`;
  if (restaurant.category) card += `   🏷️ ${restaurant.category}`;
  if (restaurant.price) card += ` | 💰 ${restaurant.price}`;
  card += "\n";
  if (restaurant.address) card += `   📍 ${restaurant.address}\n`;
  if (restaurant.dishes && restaurant.dishes.length > 0) {
    card += `   🍽️ 推荐：${restaurant.dishes.slice(0, 3).join("、")}\n`;
  }
  return card;
}

// ═══════════════════════════════════════════
// 输出
// ═══════════════════════════════════════════

function pickFoodCategory(meal, profile) {
  const pool = FOOD_CATEGORIES[meal] || FOOD_CATEGORIES.lunch;
  let candidates = filterByProfile(pool, profile);
  const recentFoods = getRecentFoods(profile);
  if (recentFoods.length > 0) {
    const filtered = candidates.filter((c) => !recentFoods.includes(c.name));
    if (filtered.length > 0) candidates = filtered;
  }
  return pick(candidates);
}

function formatFoodRecommendation(food) {
  let card = `\n   ${food.emoji} 今天的命运之味是——${food.name}！\n\n`;
  card += `   🍽️ 推荐：${food.dishes}\n`;
  card += `   💰 预算：${food.budget}\n`;
  return card;
}

function main() {
  const meal = args.meal || detectMeal();
  const style = args.style || "normal";
  const restaurants = loadRestaurants();
  const profile = loadUserProfile();

  const opener = pick(OPENERS[meal] || OPENERS.lunch);
  const rollEffect = pick(ROLL_EFFECTS);
  const closer = pick(CLOSERS);

  if (args.json) {
    const chosenRestaurant = restaurants.length > 0 ? pick(restaurants) : null;
    const chosenFood = pickFoodCategory(meal, profile);
    console.log(
      JSON.stringify({
        meal,
        opener,
        foodCategory: chosenFood,
        restaurant: chosenRestaurant,
        closer,
        restaurantCount: restaurants.length,
        hasProfile: !!profile,
        timestamp: new Date().toISOString(),
      }, null, 2)
    );
    return;
  }

  console.log("");
  console.log(opener);
  console.log("");
  console.log(rollEffect);
  console.log("");

  if (restaurants.length > 0) {
    const chosen = pick(restaurants);
    console.log(`   🎯 今天就它了！`);
    console.log(formatRecommendation(chosen));

    if (style === "chaotic") {
      console.log(`   ${pick(CHAOTIC_EXTRAS)}\n`);
    }

    console.log(closer);
    console.log("");

    if (restaurants.length > 1) {
      const others = restaurants.filter((r) => r.slug !== chosen.slug);
      if (others.length > 0) {
        const alt = pick(others);
        console.log(`   💡 备选：${alt.name}${alt.price ? "（" + alt.price + "）" : ""}`);
        console.log("");
      }
    }
  } else {
    const food = pickFoodCategory(meal, profile);
    console.log(`   🎯 今天就吃这个！`);
    console.log(formatFoodRecommendation(food));

    if (style === "chaotic") {
      console.log(`   ${pick(CHAOTIC_EXTRAS)}\n`);
    }

    console.log(closer);
    console.log("");
    console.log("   💡 想找具体的店？用 /eat-discover 搜搜附近，或 /eat-create 把你知道的店加进来。");
    console.log("");
  }
}

main();
