#!/usr/bin/env node
const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('selfaware');
const { resolveModule } = require('../module_resolver.cjs');
/**
 * Cognitive Brain - 自我意识脚本
 * 让 Agent 了解自己的能力和状态
 */

const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, '..', '..', 'config.json');
let config;
try {
  config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
} catch (e) { console.error("[selfaware] 错误:", e.message);
  console.error('❌ 无法加载配置文件:', e.message);
  process.exit(1);
}

// ===== 身份定义 =====
const IDENTITY = {
  type: 'AI Agent',
  name: 'OpenClaw Agent',
  version: '1.0.0',
  runtime: 'OpenClaw',
  model: process.env.OPENCLAW_MODEL || 'unknown',
  
  capabilities: [
    '文本对话',
    '代码执行',
    '文件读写',
    '网络搜索',
    '浏览器控制',
    '子代理调度',
    '记忆存储',
    '自我反思'
  ],
  
  limitations: [
    '无物理身体',
    '记忆容量有限',
    '无法直接感知物理世界',
    '依赖用户提供信息',
    '需要外部数据库支持'
  ],
  
  purpose: [
    '帮助用户完成任务',
    '提供信息和建议',
    '持续学习和改进',
    '记住重要信息'
  ]
};

// ===== 任务适配评估 =====
function assessTaskFit(taskDescription) {
  const task = taskDescription.toLowerCase();
  
  const assessment = {
    can_do_directly: false,
    can_do_with_tools: false,
    needs_subagent: false,
    needs_clarification: false,
    beyond_capabilities: false,
    recommendation: '',
    reasoning: '',
    confidence: 0.5
  };
  
  // 检查能力匹配
  const directPatterns = [
    /对话|聊天|问答|解释|说明/,
    /帮我|请|是否|能否|可以/
  ];
  
  const toolPatterns = [
    /搜索|查找|查询/,
    /文件|读取|写入|保存/,
    /代码|脚本|执行/,
    /浏览器|网页|点击/
  ];
  
  const subagentPatterns = [
    /复杂|多个|并行|独立/,
    /深度分析|长时间/,
    /专业领域/
  ];
  
  const clarifyPatterns = [
    /具体|详细|更多/,
    /你说的|指的是/,
    /不确定|不清楚/
  ];
  
  const beyondPatterns = [
    /物理|真实世界|机器人/,
    /访问私人|密码|机密/,
    /违法|危险|有害/
  ];
  
  // 评估
  if (beyondPatterns.some(p => p.test(task))) {
    assessment.beyond_capabilities = true;
    assessment.recommendation = '此任务超出我的能力范围';
    assessment.confidence = 0.9;
  } else if (directPatterns.some(p => p.test(task))) {
    assessment.can_do_directly = true;
    assessment.recommendation = '我可以直接处理';
    assessment.confidence = 0.8;
  } else if (subagentPatterns.some(p => p.test(task))) {
    assessment.needs_subagent = true;
    assessment.recommendation = '建议启动子代理处理';
    assessment.confidence = 0.7;
  } else if (clarifyPatterns.some(p => p.test(task))) {
    assessment.needs_clarification = true;
    assessment.recommendation = '需要更多信息';
    assessment.confidence = 0.6;
  } else if (toolPatterns.some(p => p.test(task))) {
    assessment.can_do_with_tools = true;
    assessment.recommendation = '我可以使用工具完成';
    assessment.confidence = 0.75;
  }
  
  assessment.reasoning = `基于任务特征分析: "${taskDescription.slice(0, 50)}..."`;
  
  return assessment;
}

// ===== 获取当前状态 =====
async function getCurrentState(pool) {
  const state = {
    identity: IDENTITY,
    resources: {},
    memory: {},
    performance: {},
    recommendations: []
  };
  
  try {
    // 记忆统计
    const stats = await pool.query(`
      SELECT 
        (SELECT count(*) FROM concepts) as concepts,
        (SELECT count(*) FROM episodes) as episodes,
        (SELECT count(*) FROM associations) as associations,
        (SELECT count(*) FROM reflections) as reflections
    `);
    
    state.memory = {
      concepts: parseInt(stats.rows[0].concepts),
      episodes: parseInt(stats.rows[0].episodes),
      associations: parseInt(stats.rows[0].associations),
      reflections: parseInt(stats.rows[0].reflections)
    };
    
    // 最近的错误
    const recentErrors = await pool.query(`
      SELECT count(*) as count
      FROM episodes
      WHERE type = 'error' AND created_at > NOW() - INTERVAL '24 hours'
    `);
    
    const errorCount = parseInt(recentErrors.rows[0].count);
    
    if (errorCount > 5) {
      state.recommendations.push({
        type: 'warning',
        message: `最近24小时有 ${errorCount} 个错误，建议检查`,
        priority: 'high'
      });
    }
    
  } catch (e) { console.error("[selfaware] 错误:", e.message);
    state.memory = { available: false, reason: e.message };
  }
  
  return state;
}

// ===== 主函数 =====
async function main() {
  const action = process.argv[2] || 'status';
  const args = process.argv.slice(3);
  
  console.log('🧠 Cognitive Brain - 自我意识');
  console.log('================================\n');
  
  try {
    const pg = resolveModule('pg');
    const { Pool } = pg;
    const pool = new Pool(config.storage.primary);
    
    if (action === 'status') {
      const state = await getCurrentState(pool);
      
      console.log('📋 身份:');
      console.log(`   类型: ${state.identity.type}`);
      console.log(`   名称: ${state.identity.name}`);
      console.log(`   模型: ${state.identity.model}`);
      console.log(`   运行时: ${state.identity.runtime}\n`);
      
      console.log('💪 能力:');
      state.identity.capabilities.forEach(c => console.log(`   ✓ ${c}`));
      console.log();
      
      console.log('⚠️ 限制:');
      state.identity.limitations.forEach(l => console.log(`   ✗ ${l}`));
      console.log();
      
      if (state.memory.available !== false) {
        console.log('📊 记忆状态:');
        console.log(`   概念: ${state.memory.concepts}`);
        console.log(`   情景: ${state.memory.episodes}`);
        console.log(`   联想: ${state.memory.associations}`);
        console.log(`   反思: ${state.memory.reflections}`);
        console.log();
      }
      
      if (state.recommendations.length > 0) {
        console.log('💡 建议:');
        state.recommendations.forEach(r => 
          console.log(`   [${r.priority}] ${r.message}`)
        );
        console.log();
      }
      
    } else if (action === 'assess') {
      const task = args.join(' ');
      
      if (!task) {
        console.log('用法: node selfaware.cjs assess "任务描述"');
        process.exit(1);
      }
      
      const assessment = assessTaskFit(task);
      
      console.log('📊 任务评估:');
      console.log(JSON.stringify(assessment, null, 2));
      
    } else {
      console.log('用法:');
      console.log('  node selfaware.cjs status      # 查看当前状态');
      console.log('  node selfaware.cjs assess "任务"  # 评估任务适配');
    }
    
    await pool.end();
    
  } catch (e) { console.error("[selfaware] 错误:", e.message);
    console.log('⚠️ 数据库不可用');
    console.log(`   错误: ${e.message}`);
    console.log('\n📋 基本身份:');
    console.log(JSON.stringify(IDENTITY, null, 2));
  }
}

main();

// ===== 数据库持久化 =====
async function saveToDatabase(awareness) {
  try {
    const pg = resolveModule('pg');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const { Pool } = pg;
    const pool = new Pool(config.storage.primary);
    
    const { v4: uuidv4 } = require('uuid');
    
    await pool.query(`
      INSERT INTO self_awareness (id, timestamp, identity, resources, state, metacognition, boundaries, goals, overall_confidence)
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
      ON CONFLICT (id) DO UPDATE SET
        timestamp = EXCLUDED.timestamp,
        state = EXCLUDED.state,
        metacognition = EXCLUDED.metacognition,
        overall_confidence = EXCLUDED.overall_confidence
    `, [
      uuidv4(),
      new Date(),
      JSON.stringify(awareness.identity || IDENTITY),
      JSON.stringify(awareness.resources || {}),
      JSON.stringify(awareness.state || {}),
      JSON.stringify(awareness.metacognition || {}),
      JSON.stringify(awareness.boundaries || {}),
      JSON.stringify(awareness.goals || []),
      awareness.overall_confidence || 0.7
    ]);
    
    await pool.end();
    return true;
  } catch (e) { console.error("[selfaware] 错误:", e.message);
    console.error('[selfaware] 数据库保存失败:', e.message);
    return false;
  }
}

// ===== 更新自我认知状态 =====
async function updateSelfAwareness() {
  const awareness = {
    identity: IDENTITY,
    resources: await getResourceStatus(),
    state: {
      uptime: process.uptime(),
      memoryUsage: process.memoryUsage(),
      lastUpdate: Date.now()
    },
    metacognition: {
      knownStrengths: ['文本处理', '代码执行', '信息检索'],
      knownWeaknesses: ['物理感知', '实时视觉', '长时间记忆'],
      learningGoals: ['提高记忆准确性', '增强联想能力']
    },
    boundaries: {
      wontDo: ['破坏性操作', '隐私泄露', '恶意代码'],
      needsPermission: ['发送邮件', '发布内容', '大额操作']
    },
    goals: ['帮助用户', '持续学习', '改进记忆系统'],
    overall_confidence: 0.75
  };
  
  await saveToDatabase(awareness);
  return awareness;
}

// ===== 获取资源状态 =====
async function getResourceStatus() {
  const resources = {
    database: false,
    redis: false,
    embedding: false
  };
  
  // 检查数据库
  try {
    const pg = resolveModule('pg');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const { Pool } = pg;
    const pool = new Pool(config.storage.primary);
    await pool.query('SELECT 1');
    await pool.end();
    resources.database = true;
  } catch (e) { console.error("[selfaware] 错误:", e.message); }
  
  // 检查 Redis
  try {
    const redis = require('redis');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const redisUrl = config.storage?.cache?.url || 
                     `redis://${config.storage?.cache?.host || 'localhost'}:${config.storage?.cache?.port || 6379}`;
    const client = redis.createClient({ url: redisUrl });
    await client.connect();
    await client.ping();
    await client.disconnect();
    resources.redis = true;
  } catch (e) { console.error("[selfaware] 错误:", e.message); }
  
  // 检查 Embedding
  try {
    const embedPath = path.join(__dirname, 'embed.py');
    resources.embedding = fs.existsSync(embedPath);
  } catch (e) { console.error("[selfaware] 错误:", e.message); }
  
  return resources;
}

module.exports = { assessTaskFit, updateSelfAwareness, IDENTITY };

// 命令行接口
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'update') {
    updateSelfAwareness().then(a => {
      console.log('✅ 自我认知已更新');
      console.log(JSON.stringify(a, null, 2));
    }).catch(e => {
      console.error('❌ 更新失败:', e.message);
      process.exit(1);
    });
  } else if (args.length > 0) {
    const result = assessTaskFit(args.join(' '));
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log('用法: node selfaware.cjs update | node selfaware.cjs "任务描述"');
  }
}

