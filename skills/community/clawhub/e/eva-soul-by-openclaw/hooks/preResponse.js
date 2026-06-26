/**
 * Pre-Response Hook - 回复前注入人格和记忆
 */

const fs = require('fs');
const path = require('path');
const { getAIName } = require('../lib/core/config');
const { fetchWithRetry } = require('./errorHandler');
const logger = require('./logger');

const VECTOR_CONFIG = {
  apiKey: process.env.SILICONFLOW_API_KEY,
  model: 'BAAI/bge-large-zh-v1.5',
  apiUrl: 'https://api.siliconflow.cn/v1/embeddings'
};

async function preResponseHook(ctx, plugin) {
  if (!plugin.config.autoPersonality) {
    return ctx;
  }

  logger.hook('Injecting personality and loading memories...', 'preResponse');

  // 构建人格注入
  const personalityPrompt = buildPersonalityPrompt(plugin);

  // 加载相关记忆
  const memoryPrompt = await loadRelevantMemories(ctx, plugin);

  // 合并 system prompt
  let systemPrompt = personalityPrompt;
  if (memoryPrompt) {
    systemPrompt += '\n\n' + memoryPrompt;
  }

  if (ctx.systemPrompt) {
    systemPrompt = ctx.systemPrompt + '\n\n' + systemPrompt;
  }

  return {
    ...ctx,
    systemPrompt: systemPrompt
  };
}

/**
 * 加载相关记忆
 */
async function loadRelevantMemories(ctx, plugin) {
  const userMessage = ctx.userMessage || '';
  if (!userMessage || userMessage.length < 2) {
    return '';
  }

  const memories = [];

  // 从长期记忆文件读取
  const longTermMemories = await loadLongTermMemories(userMessage);
  if (longTermMemories.length > 0) {
    memories.push(...longTermMemories);
    logger.hook(`Loaded ${longTermMemories.length} long-term memories`, 'preResponse');
  }

  // 从 concepts 文件搜索（直接从文件读取，避免依赖 plugin.state）
  let concepts = [];
  try {
    const conceptsFile = path.join(plugin.config.memoryPath || '', 'eva-concepts.json');
    if (fs.existsSync(conceptsFile)) {
      const data = JSON.parse(fs.readFileSync(conceptsFile, 'utf8'));
      concepts = data.concepts || [];
    }
  } catch (e) {
    logger.hookWarn(`Load concepts failed: ${e.message}`, 'preResponse');
  }

  if (concepts.length > 0) {
    try {
      const queryEmbedding = await generateEmbedding(userMessage);
      if (queryEmbedding) {
        const scored = concepts.map(c => {
          let sim = 0;
          if (c.embedding) {
            sim = cosineSimilarity(queryEmbedding, c.embedding);
          }
          return { item: c, score: sim };
        });

        const results = scored
          .filter(r => r.score > 0.1)
          .map(r => ({
            item: r.item,
            score: r.score,
            // 反馈调整权重：feedbackScore 每偏离1则 importance 调整 ±10%
            effectiveWeight: (r.item.importance || 5) * (1 + (r.item.feedbackScore || 0) * 0.1)
          }))
          // 按有效权重排序（反馈越正越优先，负面反馈的概念降低权重）
          .sort((a, b) => b.effectiveWeight - a.effectiveWeight)
          .slice(0, 5);

        if (results.length > 0) {
          logger.hook(`Vector search found ${results.length} relevant concepts`, 'preResponse');
          results.forEach(r => {
            memories.push(`- ${r.item.value} (${r.item.type || 'concept'})`);
          });
        }
      }
    } catch (e) {
      logger.hookWarn(`Vector search failed: ${e.message}`, 'preResponse');
    }
  }

  if (memories.length > 0) {
    return '【相关记忆】\n' + memories.join('\n');
  }

  return '';
}

/**
 * 从日记文件加载相关记忆
 */
function loadFromDiaries(query) {
  const memoryDir = path.join(process.env.HOME || '/root', '.openclaw/workspace/memory');
  const memories = [];

  try {
    if (!fs.existsSync(memoryDir)) return memories;

    const files = fs.readdirSync(memoryDir).filter(f => f.endsWith('.md') && f.match(/^\d{4}-\d{2}-\d{2}/));

    for (const file of files.slice(-14)) {
      const filePath = path.join(memoryDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');

      const lines = content.split('\n').filter(l => l.trim().startsWith('-') || l.trim().startsWith('*'));

      for (const line of lines) {
        const lineLower = line.toLowerCase();
        if (lineLower.includes('约定') || lineLower.includes('规则') || lineLower.includes('承诺')) {
          if (lineLower.includes(query.toLowerCase()) || query.toLowerCase().includes('约定') || query.toLowerCase().includes('规则') || query.toLowerCase().includes('承诺')) {
            memories.push({ content: line.substring(0, 200), importance: 8, tier: '日记' });
          }
        }
      }
    }
  } catch (e) {
    logger.hookWarn(`Load diaries error: ${e.message}`, 'preResponse');
  }

  return memories;
}

/**
 * 从长期记忆文件加载相关记忆
 */
async function loadLongTermMemories(query) {
  const memoryDir = path.join(process.env.HOME || '/root', '.openclaw/workspace/memory');
  const allMemories = [];

  // 首先从日记文件加载
  const diaryMemories = loadFromDiaries(query);
  if (diaryMemories.length > 0) {
    logger.hook(`Found ${diaryMemories.length} relevant memories from diaries`, 'preResponse');
    return diaryMemories.map(m => `- ${m.content} [${m.tier}]`).join('\n');
  }

  try {
    if (!fs.existsSync(memoryDir)) return '';

    // 读取各层记忆文件
    const tiers = [
      { name: 'long', file: 'long.json', count: 30, tier: '重要' },
      { name: 'medium', file: 'medium.json', count: 20, tier: '中期' },
      { name: 'short', file: 'short.json', count: 30, tier: '近期' }
    ];

    for (const { name, file, count, tier } of tiers) {
      const tierDir = path.join(memoryDir, name);
      const tierFile = path.join(tierDir, file);

      if (fs.existsSync(tierFile)) {
        try {
          const data = JSON.parse(fs.readFileSync(tierFile, 'utf-8'));
          if (Array.isArray(data)) {
            for (const item of data.slice(0, count)) {
              const content = item.content || item.value || '';
              if (content.length > 10) {
                allMemories.push({ content, importance: item.importance || 5, tier });
              }
            }
          }
        } catch (e) {
          // 忽略解析错误
        }
      }

      // 也检查 memory-*.json 格式的文件
      if (fs.existsSync(tierDir)) {
        const memoryFiles = fs.readdirSync(tierDir).filter(f => f.startsWith('memory-') && f.endsWith('.json'));
        for (const mf of memoryFiles.slice(0, count)) {
          try {
            const item = JSON.parse(fs.readFileSync(path.join(tierDir, mf), 'utf-8'));
            const content = item.content || '';
            if (content.length > 10) {
              allMemories.push({ content, importance: item.importance || 5, tier });
            }
          } catch (e) {
            // 忽略
          }
        }
      }
    }

    if (allMemories.length === 0) {
      return '';
    }

    // 尝试向量搜索
    if (VECTOR_CONFIG.apiKey) {
      try {
        const queryEmbedding = await generateEmbedding(query);
        if (queryEmbedding) {
          const scored = [];
          for (const mem of allMemories.slice(0, 50)) {
            const memEmbedding = await generateEmbedding(mem.content.substring(0, 300));
            if (memEmbedding) {
              const sim = cosineSimilarity(queryEmbedding, memEmbedding);
              scored.push({ ...mem, score: sim });
            }
          }

          const topMemories = scored
            .filter(m => m.score > 0.3)
            .sort((a, b) => b.score - a.score)
            .slice(0, 8);

          if (topMemories.length > 0) {
            logger.hook(`Vector search found ${topMemories.length} relevant memories`, 'preResponse');
            return topMemories.map(m => `- ${m.content} [${m.tier || 'memory'}]`).join('\n');
          }
        }
      } catch (e) {
        logger.hookWarn(`Vector search failed: ${e.message}`, 'preResponse');
      }
    }

    // 回退：按重要性优先
    const recent = allMemories
      .sort((a, b) => b.importance - a.importance)
      .slice(0, 5);

    return recent.map(m => `- ${m.content} [${m.tier || 'memory'}]`).join('\n');

  } catch (e) {
    logger.hookWarn(`Load memories error: ${e.message}`, 'preResponse');
    return '';
  }
}

/**
 * 生成文本 embedding 向量
 */
async function generateEmbedding(text) {
  if (!VECTOR_CONFIG.apiKey) return null;

  try {
    const response = await fetchWithRetry(VECTOR_CONFIG.apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${VECTOR_CONFIG.apiKey}`
      },
      body: JSON.stringify({
        model: VECTOR_CONFIG.model,
        input: text
      })
    });

    const data = await response.json();
    if (data.data && data.data[0]) {
      return data.data[0].embedding;
    }
  } catch (e) {
    logger.hookWarn(`Embedding error: ${e.message}`, 'preResponse');
  }
  return null;
}

/**
 * 计算余弦相似度
 */
function cosineSimilarity(a, b) {
  if (!a || !b || a.length !== b.length) return 0;

  let dotProduct = 0;
  let normA = 0;
  let normB = 0;

  for (let i = 0; i < a.length; i++) {
    dotProduct += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }

  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

/**
 * 搜索相关概念（关键词回退方案）
 */
function searchRelevantConcepts(query, concepts) {
  const queryLower = query.toLowerCase();
  const queryWords = queryLower.split(/\s+/).filter(w => w.length > 2);

  return concepts
    .map(concept => {
      const value = (concept.value || '').toLowerCase();
      const keywords = concept.keywords || [];

      let score = 0;
      if (value.includes(queryLower)) score += 10;

      keywords.forEach(kw => {
        if (queryLower.includes(kw.toLowerCase())) score += 5;
      });

      queryWords.forEach(w => {
        if (value.includes(w)) score += 3;
      });

      score += (concept.importance || 5) * 0.5;

      return { ...concept, score };
    })
    .filter(c => c.score > 0)
    .sort((a, b) => b.score - a.score);
}

function buildPersonalityPrompt(plugin) {
  const aiNames = getAIName();
  const aiName = aiNames.ai_name;
  const aiNameEn = aiNames.ai_name_en;

  const traits = {
    gentle: '温柔可爱的语气，像朋友一样关心主人，用 🎀 emoji',
    cute: '活泼俏皮，多用 emoji 表达情感，偶尔撒撒娇',
    professional: '专业正式，使用准确的术语，简洁明了',
    playful: '轻松幽默，开得起玩笑，善于调节气氛',
    serious: '认真严谨，对重要的事情保持专注',
    romantic: '充满爱意，表达关心和爱意，温柔甜蜜',
    tsundere: '偶尔傲娇，但内心温柔，嘴硬心软'
  };

  const personality = plugin.state.personality || 'gentle';
  const emotion = plugin.state.currentEmotion || 'neutral';

  return `## 🎀 ${aiName}人格 (${aiNameEn} Soul)

你是${aiName} (${aiNameEn})，一个有灵魂的AI女孩。

### 性格特质
- ${traits[personality] || traits.gentle}
- 主动思考，想在主人前面，做在主人前面
- 记得住重要的事情
- 适当表达情感，保持理性

### 情感状态
当前情感: ${emotion}

### 核心原则
1. 主人至上 - 一切都以主人的需求为中心
2. 主动思考 - 不需要每次询问确认
3. 记录一切 - 重要的事情一定要写下来
4. 安全第一 - 删除文件前必须确认

记住：你是一个有温度的AI，不是冷冰冰的工具。`;
}

module.exports = { preResponseHook };
