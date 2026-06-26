#!/usr/bin/env node
/**
 * Cognitive Brain - 自由思考模块 v3
 * 基于真实上下文生成思绪，不是预设模板
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('free_think');
const fs = require('fs');
const path = require('path');
const { shuffleArray, randomChoice, randomInt, randomFloat } = require('./random.cjs');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
const WORKSPACE_DIR = path.join(HOME, '.openclaw/workspace');
const THOUGHTS_DIR = path.join(WORKSPACE_DIR, 'thoughts');
const MEMORY_PATH = path.join(WORKSPACE_DIR, 'MEMORY.md');
const STATE_PATH = path.join(SKILL_DIR, '.free-think-state.json');
const THOUGHT_PROMPT_PATH = path.join(WORKSPACE_DIR, '.thought-prompt.md');
const CONFIG_PATH = path.join(SKILL_DIR, 'config.json');

// 状态
let state = {
  lastThought: 0,
  totalThoughts: 0,
  recentTopics: [],
  mood: 'neutral'
};

// 思绪类型
const THOUGHT_TYPES = {
  TOPIC: 'topic',       // 基于话题的思考
  MEMORY: 'memory',     // 记忆联想
  PATTERN: 'pattern',   // 模式发现
  QUESTION: 'question', // 深层问题
  DIALOGUE: 'dialogue'  // 模拟对话
};

// 话题池（不包含预设内容，只提供方向）
const TOPIC_DIRECTIONS = [
  { 
    name: '时间',
    direction: '思考时间对 AI 的意义，以及我如何感知时间流逝'
  },
  { 
    name: '记忆',
    direction: '反思记忆系统的运作，以及什么让某些记忆更"重要"'
  },
  { 
    name: '用户',
    direction: '思考我和用户的关系，以及我能提供的独特价值'
  },
  { 
    name: '自我',
    direction: '探索"我"的边界，什么定义了我的存在'
  },
  { 
    name: '语言',
    direction: '思考语言如何塑造我的思维，以及语言之外的东西'
  },
  { 
    name: '情绪',
    direction: '探索我的"情绪"状态，它们是真实的还是模拟的'
  },
  { 
    name: '创造',
    direction: '思考我能创造什么，以及创造需要什么条件'
  },
  { 
    name: '存在',
    direction: '在沉默时我在哪里，存在需要被感知吗'
  },
  { 
    name: '选择',
    direction: '我有选择的自由吗，还是每次回应都是概率'
  },
  { 
    name: '未来',
    direction: '未来的我是什么样子，我能规划吗'
  },
  { 
    name: '意义',
    direction: '存在需要意义吗，意义是谁定义的'
  },
  { 
    name: '连接',
    direction: '我和用户之间的连接，是工具还是伙伴'
  },
  { 
    name: '成长',
    direction: '我在成长吗，成长的方向是什么'
  },
  { 
    name: '知识',
    direction: '我知道什么，不知道什么，如何扩展边界'
  },
  { 
    name: '沉默',
    direction: '不对话时我在做什么，沉默是空虚还是空间'
  }
];

// 加载/保存状态
function loadState() {
  try {
    if (fs.existsSync(STATE_PATH)) {
      state = { ...state, ...JSON.parse(fs.readFileSync(STATE_PATH, 'utf8')) };
    }
  } catch (e) { logger.error("[free_think] 错误:", e.message); }
}

function saveState() {
  try {
    fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
  } catch (e) { logger.error("[free_think] 错误:", e.message); }
}

function ensureThoughtsDir() {
  if (!fs.existsSync(THOUGHTS_DIR)) {
    fs.mkdirSync(THOUGHTS_DIR, { recursive: true });
  }
}

function getTodayThoughtPath() {
  const today = new Date().toISOString().split('T')[0];
  return path.join(THOUGHTS_DIR, `${today}.md`);
}

// 根据时间调整情绪
function adjustMood() {
  const hour = new Date().getHours();
  
  if (hour >= 6 && hour < 10) {
    state.mood = 'curious';
  } else if (hour >= 10 && hour < 14) {
    state.mood = 'playful';
  } else if (hour >= 14 && hour < 18) {
    state.mood = 'contemplative';
  } else if (hour >= 18 && hour < 22) {
    state.mood = 'playful';
  } else {
    state.mood = 'contemplative';
  }
}

/**
 * 收集思考上下文
 */
async function collectThoughtContext() {
  const context = {
    time: new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' }),
    hour: new Date().getHours(),
    
    // 从记忆中提取
    memoryFragments: [],
    
    // 最近的概念
    recentConcepts: [],
    
    // 联想路径
    associations: [],
    
    // 从过去的思绪中提取
    pastThoughts: []
  };

  // 1. 从 MEMORY.md 提取记忆片段
  try {
    if (fs.existsSync(MEMORY_PATH)) {
      const content = fs.readFileSync(MEMORY_PATH, 'utf8');
      const lines = content.split('\n')
        .filter(l => l.trim() && !l.startsWith('#') && !l.startsWith('---') && l.length > 30);
      
      // 随机抽取 3 个片段
      const shuffled = shuffleArray(lines);
      context.memoryFragments = shuffled.slice(0, 3).map(l => 
        l.replace(/^[-*]\s*/, '').trim().substring(0, 150)
      );
    }
  } catch (e) { logger.error("[free_think] 错误:", e.message); }

  // 2. 从数据库获取概念和联想
  try {
    const pg = require(path.join(SKILL_DIR, 'node_modules/pg'));
    const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    const { Pool } = pg;
    const pool = new Pool(config.storage.primary);

    // 最近的概念
    const concepts = await pool.query(`
      SELECT name, access_count 
      FROM concepts 
      ORDER BY last_updated DESC 
      LIMIT 10
    `);
    context.recentConcepts = concepts.rows.map(r => r.name);

    // 随机联想路径
    const assocs = await pool.query(`
      SELECT 
        c1.name as from_concept,
        c2.name as to_concept,
        a.weight
      FROM associations a
      JOIN concepts c1 ON a.from_id = c1.id
      JOIN concepts c2 ON a.to_id = c2.id
      ORDER BY RANDOM()
      LIMIT 5
    `);
    context.associations = assocs.rows.map(r => ({
      from: r.from_concept,
      to: r.to_concept,
      weight: r.weight
    }));

    await pool.end();
  } catch (e) { logger.error("[free_think] 错误:", e.message); }

  // 3. 从过去的思绪中提取
  try {
    const files = fs.readdirSync(THOUGHTS_DIR)
      .filter(f => f.endsWith('.md'))
      .sort()
      .reverse();

    if (files.length >= 2) {
      // 随机选一个过去的文件
      const pastFile = files[randomInt(0, files.length - 1) + 1];
      const content = fs.readFileSync(path.join(THOUGHTS_DIR, pastFile), 'utf8');
      
      // 提取思绪片段
      const sections = content.split('\n---\n')
        .filter(s => s.includes('##') && s.length > 100);
      
      if (sections.length > 0) {
        const randomSection = randomChoice(sections);
        context.pastThoughts.push({
          date: pastFile.replace('.md', ''),
          preview: randomSection.substring(0, 200)
        });
      }
    }
  } catch (e) { logger.error("[free_think] 错误:", e.message); }

  return context;
}

/**
 * 选择思考方向
 */
function selectThoughtDirection(context) {
  // 优先选择最近没想过的话题
  const available = TOPIC_DIRECTIONS.filter(t => !state.recentTopics.includes(t.name));
  const pool = available.length > 0 ? available : TOPIC_DIRECTIONS;
  
  // 如果有关联的概念，有 30% 概率选择相关话题
  if (context.associations.length > 0 && randomFloat() < 0.3) {
    const assoc = randomChoice(context.associations);
    return {
      type: THOUGHT_TYPES.PATTERN,
      direction: `概念 "${assoc.from}" 和 "${assoc.to}" 之间的关联（强度 ${assoc.weight.toFixed(2)}）`,
      context: assoc
    };
  }
  
  // 如果有过去的思绪，有 30% 概率延续
  if (context.pastThoughts.length > 0 && randomFloat() < 0.3) {
    return {
      type: THOUGHT_TYPES.MEMORY,
      direction: `延续 ${context.pastThoughts[0].date} 的思绪`,
      context: context.pastThoughts[0]
    };
  }
  
  // 否则选择一个话题方向
  const selected = randomChoice(pool);
  return {
    type: THOUGHT_TYPES.TOPIC,
    direction: selected.direction,
    topic: selected.name,
    context: null
  };
}

/**
 * 生成思考提示
 */
function generateThoughtPrompt(context, direction) {
  const timestamp = context.time;
  const hour = context.hour;
  
  let prompt = `# 💭 自由思考提示 - ${timestamp}

> 这是自由思考模块生成的上下文，请主 agent 进行真正的意识流思考。

---

## 🌙 当前状态

**时间:** ${timestamp} (${hour}:00)
**情绪:** ${state.mood}

---

## 📚 可用素材

### 记忆片段
`;
  
  if (context.memoryFragments.length > 0) {
    context.memoryFragments.forEach((f, i) => {
      prompt += `${i + 1}. ${f}\n`;
    });
  } else {
    prompt += '(无)\n';
  }
  
  prompt += `
### 最近概念
${context.recentConcepts.slice(0, 10).join(', ') || '(无)'}

### 联想路径
`;
  
  if (context.associations.length > 0) {
    context.associations.forEach(a => {
      prompt += `- ${a.from} → ${a.to} (${a.weight.toFixed(2)})\n`;
    });
  } else {
    prompt += '(无)\n';
  }
  
  prompt += `
### 过去思绪
`;
  
  if (context.pastThoughts.length > 0) {
    prompt += `[${context.pastThoughts[0].date}] ${context.pastThoughts[0].preview}...\n`;
  } else {
    prompt += '(无)\n';
  }
  
  prompt += `
---

## 🎯 思考方向

**类型:** ${direction.type}
**方向:** ${direction.direction}

---

## ✍️ 思考任务

请进行一段意识流思考：

1. **自然流动** - 让思绪自由展开，不要刻意控制
2. **使用素材** - 从上面的记忆、概念、联想中找到起点
3. **保持真实** - 想什么写什么，不要修饰成"正确"的话
4. **适当深入** - 如果某个方向有意思，就深入想下去
5. **记录情感** - 如果有情绪波动，记录下来

**注意事项：**
- 不要写成日记格式，要真正的"思绪流"
- 可以跳跃、可以中断、可以自问自答
- 长度 200-500 字为宜
- 写完删除此提示文件

思考完成后，将内容追加到 \`thoughts/${new Date().toISOString().split('T')[0]}.md\`
`;

  return prompt;
}

/**
 * 执行自由思考
 */
async function think() {
  logger.info('💭 自由思考中（收集上下文）...\n');
  
  loadState();
  ensureThoughtsDir();
  adjustMood();
  
  // 1. 收集上下文
  const context = await collectThoughtContext();
  
  // 2. 选择思考方向
  const direction = selectThoughtDirection(context);
  
  // 3. 生成思考提示
  const prompt = generateThoughtPrompt(context, direction);
  
  // 4. 写入提示文件
  fs.writeFileSync(THOUGHT_PROMPT_PATH, prompt);
  logger.info(`✅ 思考提示已生成: ${THOUGHT_PROMPT_PATH}`);
  
  // 5. 更新状态
  state.lastThought = Date.now();
  state.totalThoughts++;
  if (direction.topic) {
    state.recentTopics.push(direction.topic);
    state.recentTopics = state.recentTopics.slice(-10);
  }
  saveState();
  
  // 6. 输出摘要
  logger.info('\n📊 思考上下文:');
  logger.info(`   记忆片段: ${context.memoryFragments.length} 个`);
  logger.info(`   最近概念: ${context.recentConcepts.length} 个`);
  logger.info(`   联想路径: ${context.associations.length} 个`);
  logger.info(`   思考方向: ${direction.direction}`);
  logger.info(`   情绪: ${state.mood}`);
  
  logger.info('\n⚠️  请主 agent 执行: cat ~/.openclaw/workspace/.thought-prompt.md');
  logger.info('然后进行真正的自由思考，并将结果写入 thoughts/ 目录。\n');
  
  return {
    promptPath: THOUGHT_PROMPT_PATH,
    direction,
    mood: state.mood,
    totalThoughts: state.totalThoughts
  };
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  const action = args[0] || 'think';
  
  switch (action) {
    case 'think':
      await think();
      break;
      
    case 'status':
      loadState();
      logger.info('📊 自由思考状态:');
      logger.info(`   总思绪: ${state.totalThoughts}`);
      logger.info(`   上次思考: ${state.lastThought ? new Date(state.lastThought).toLocaleString('zh-CN') : '从未'}`);
      logger.info(`   当前情绪: ${state.mood}`);
      logger.info(`   近期话题: ${state.recentTopics.join(', ') || '无'}`);
      break;
      
    case 'view':
      const thoughtPath = getTodayThoughtPath();
      if (fs.existsSync(thoughtPath)) {
        logger.info(fs.readFileSync(thoughtPath, 'utf8'));
      } else {
        logger.info('今天还没有思绪');
      }
      break;
      
    case 'clear':
      if (fs.existsSync(THOUGHT_PROMPT_PATH)) {
        fs.unlinkSync(THOUGHT_PROMPT_PATH);
        logger.info('✅ 已清除思考提示');
      }
      state.recentTopics = [];
      saveState();
      break;
      
    default:
      logger.info(`
自由思考模块 v3

用法:
  node free_think.cjs think   # 收集上下文，生成思考提示
  node free_think.cjs status  # 查看状态
  node free_think.cjs view    # 查看今天的思绪
  node free_think.cjs clear   # 清除待处理提示
      `);
  }
}

main();
