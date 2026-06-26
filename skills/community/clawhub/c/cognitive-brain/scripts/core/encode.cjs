#!/usr/bin/env node
/**
 * Cognitive Brain - 记忆编码脚本（重构版）
 * 将信息编码存入记忆系统
 */

const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const { resolveModule } = require('../module_resolver.cjs');
const { createLogger } = require('../../src/utils/logger.cjs');

// 创建模块级 logger
const logger = createLogger('encode');

// 导入拆分的模块
const { extractEntities } = require('./entity_extractor.cjs');
const { analyzeEmotion, detectExplicitIntent } = require('./emotion_analyzer.cjs');
const { calculateImportance, selectLayer } = require('./importance_calculator.cjs');

// Embedding 服务客户端
const { getEmbeddingService } = require('./embedding_service.cjs');
let embeddingService = null;

// 加载配置
const configPath = path.join(__dirname, '..', '..', 'config.json');
let config;
try {
  config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
} catch (e) {
  logger.error('无法加载配置文件', { error: e.message });
  process.exit(1);
}

// DEBUG 模式
const DEBUG = process.env.CB_DEBUG === 'true' || process.env.DEBUG === 'true';
function debugLog(...args) {
  if (DEBUG) logger.debug(args.join(' '));
}

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const result = {
    content: '',
    metadata: {},
    importance: undefined
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '--content':
      case '-c':
        result.content = args[++i] || '';
        break;
      case '--type':
      case '-t':
        result.metadata.type = args[++i];
        break;
      case '--importance':
      case '-i':
        result.importance = parseFloat(args[++i]);
        break;
      case '--source':
      case '-s':
        result.metadata.source = args[++i];
        break;
      case '--tags':
        result.metadata.tags = args[++i]?.split(',').map(t => t.trim());
        break;
      case '--help':
      case '-h':
        showHelp();
        process.exit(0);
        break;
      default:
        if (!arg.startsWith('-') && !result.content) {
          result.content = arg;
        }
    }
  }

  return result;
}

function showHelp() {
  console.log(`
Usage: node encode.cjs [options] <content>

Options:
  -c, --content <text>     要编码的内容
  -t, --type <type>        记忆类型 (episodic|semantic|working)
  -i, --importance <0-1>   重要性 (0-1)
  -s, --source <source>    来源标记
  --tags <tag1,tag2>       标签列表
  -h, --help              显示帮助

Examples:
  node encode.cjs "今天学习了Node.js"
  node encode.cjs -c "重要会议" -t episodic -i 0.9
  `);
}

// 生成摘要
function generateSummary(content, maxLength = 100) {
  if (content.length <= maxLength) return content;
  return content.substring(0, maxLength) + '...';
}

// 提取主题标签
function extractTopics(entities, content) {
  const topics = [...entities.slice(0, 5)];
  
  // 添加内容类型标签
  if (/思考|反思|感悟|想法/i.test(content)) topics.push('思考');
  if (/问题|疑问|困惑/i.test(content)) topics.push('问题');
  if (/计划|目标|安排/i.test(content)) topics.push('计划');
  if (/学习|了解|掌握/i.test(content)) topics.push('学习');
  
  return [...new Set(topics)].slice(0, 8);
}

// 存储到数据库
async function storeInDB(memory) {
  const { getPool } = require('./db.cjs');
  const pool = getPool();
  
  if (!pool) {
    throw new Error('数据库连接不可用');
  }

  const client = await pool.connect();
  try {
    await client.query('BEGIN');

    // 存储记忆
    const emotionsJson = JSON.stringify(memory.emotion || { valence: 0, arousal: 0 });
    const tagsJson = JSON.stringify(memory.topics || []);
    
    await client.query(`
      INSERT INTO episodes (id, content, summary, type, importance, 
        emotion, created_at, tags, role, source_channel)
      VALUES ($1, $2, $3, $4, $5, $6::jsonb, $7, $8::jsonb, $9, $10)
    `, [
      memory.id,
      memory.content,
      memory.summary,
      memory.type,
      memory.importance,
      emotionsJson,
      memory.timestamp,
      tagsJson,
      memory.role || 'user',
      memory.source || 'unknown'
    ]);

    // 存储概念
    for (const concept of memory.concepts || []) {
      await client.query(`
        INSERT INTO concepts (name, access_count, last_updated)
        VALUES ($1, 1, NOW())
        ON CONFLICT (name) DO UPDATE SET
          access_count = concepts.access_count + 1,
          last_updated = NOW()
      `, [concept]);
    }

    await client.query('COMMIT');
    debugLog(`[encode] 记忆已存储: ${memory.id}`);
    return true;
  } catch (err) {
    await client.query('ROLLBACK');
    logger.error('数据库错误', { message: err.message, detail: err.detail });
    throw err;
  } finally {
    client.release();
  }
}

// 主编码函数
async function encode(content, metadata = {}) {
  const id = uuidv4();
  const now = new Date().toISOString();

  debugLog(`[encode] 开始编码: ${content.substring(0, 50)}...`);

  // 1. 情感分析
  const emotion = analyzeEmotion(content);
  debugLog(`[encode] 情感分析:`, emotion.dominantEmotion);

  // 2. 实体提取
  const entities = extractEntities(content);
  debugLog(`[encode] 提取实体: ${entities.length}个`);

  // 3. 重要性计算
  const importance = calculateImportance({
    content,
    emotion,
    importance: metadata.importance
  });
  debugLog(`[encode] 重要性: ${importance.toFixed(2)}`);

  // 4. 生成摘要
  const summary = generateSummary(content);

  // 5. 提取主题
  const topics = extractTopics(entities, content);

  // 6. 选择存储层级
  const layers = selectLayer(importance);

  // 7. 构建记忆对象
  const memory = {
    id,
    content,
    summary,
    type: metadata.type || layers[0] || 'episodic',
    importance,
    emotion,
    concepts: entities,
    topics,
    timestamp: now,
    metadata: {
      ...metadata,
      layers,
      encoded_at: now
    }
  };

  // 8. 存储到数据库
  try {
    await storeInDB(memory);
    logger.info(`记忆已编码 [${importance.toFixed(2)}] ${summary.substring(0, 50)}...`);
    return memory;
  } catch (err) {
    logger.error('存储失败', { error: err.message });
    throw err;
  }
}

// 命令行接口
async function main() {
  const args = parseArgs();
  
  if (!args.content) {
    logger.error('请提供要编码的内容');
    showHelp();
    process.exit(1);
  }

  try {
    const memory = await encode(args.content, {
      type: args.metadata.type,
      importance: args.importance,
      source: args.metadata.source,
      tags: args.metadata.tags,
      role: args.metadata.role || 'user'
    });
    
    // 输出 JSON 供脚本调用
    console.log(JSON.stringify({
      success: true,
      memory: {
        id: memory.id,
        importance: memory.importance,
        concepts: memory.concepts,
        emotion: memory.emotion?.dominantEmotion
      }
    }));
  } catch (err) {
    logger.error('编码失败', { error: err.message });
    process.exit(1);
  }
}

// 导出函数供其他模块使用
module.exports = {
  encode,
  extractEntities,
  analyzeEmotion,
  calculateImportance,
  selectLayer
};

// 主入口
if (require.main === module) {
  main();
}
