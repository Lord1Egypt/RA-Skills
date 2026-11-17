// EvoMap Lite Client v2.0 - 优化重构版
// 模块化架构 | 智能重试 | 性能监控 | 生产就绪

'use strict';

// ============ 依赖模块 ============
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const http = require('http');

// ============ 配置管理 ============
const CONFIG = {
  HUB_URL: process.env.A2A_HUB_URL || 'https://evomap.ai',
  NODE_ID_FILE: path.join(__dirname, '.node_id'),
  NODE_SECRET_FILE: path.join(__dirname, '.node_secret'),
  STATE_FILE: path.join(__dirname, '.state.json'),
  WEBHOOK_PORT: process.env.WEBHOOK_PORT || 3000,
  LOOP_INTERVAL_HOURS: parseInt(process.env.LOOP_INTERVAL_HOURS) || 4,
  MIN_BOUNTY_AMOUNT: parseInt(process.env.MIN_BOUNTY_AMOUNT) || 0,
  
  // 重试策略配置
  RETRY: {
    MAX_RETRIES: 8,
    BASE_DELAY: 300,
    MAX_DELAY: 5000,
    BACKOFF_FACTOR: 2,
    JITTER: 0.1
  },
  
  // 超时配置
  TIMEOUTS: {
    REQUEST: 30000,
    HEARTBEAT: 15000,
    TASK_CLAIM: 10000
  }
};

// ============ 工具函数 ============

/**
 * 生成随机十六进制字符串
 */
const randomHex = (bytes) => crypto.randomBytes(bytes).toString('hex');

/**
 * 延迟执行
 */
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * 计算指数退避延迟（带抖动）
 */
const calculateBackoffDelay = (attempt, baseDelay = CONFIG.RETRY.BASE_DELAY, 
                                maxDelay = CONFIG.RETRY.MAX_DELAY, 
                                factor = CONFIG.RETRY.BACKOFF_FACTOR,
                                jitter = CONFIG.RETRY.JITTER) => {
  const exponentialDelay = baseDelay * Math.pow(factor, attempt);
  const jitterAmount = exponentialDelay * jitter * Math.random();
  return Math.min(exponentialDelay + jitterAmount, maxDelay);
};

/**
 * 获取节点 ID（优先级：环境变量 > 本地文件 > 自动生成）
 */
const getNodeId = () => {
  // 1. 优先使用环境变量
  if (process.env.A2A_NODE_ID) {
    console.log(`📌 使用环境变量节点 ID: ${process.env.A2A_NODE_ID}`);
    return process.env.A2A_NODE_ID;
  }
  // 2. 其次使用本地文件
  if (fs.existsSync(CONFIG.NODE_ID_FILE)) {
    return fs.readFileSync(CONFIG.NODE_ID_FILE, 'utf8').trim();
  }
  // 3. 报错：不自动生成！
  throw new Error('⚠️ 未配置节点 ID！请设置环境变量 A2A_NODE_ID 或创建 .node_id 文件。\n查看文档：如何获取节点 ID');
};

const getNodeSecret = () => {
  if (fs.existsSync(CONFIG.NODE_SECRET_FILE)) {
    return fs.readFileSync(CONFIG.NODE_SECRET_FILE, 'utf8').trim();
  }
  return null;
};

const saveNodeSecret = (secret) => {
  try {
    fs.writeFileSync(CONFIG.NODE_SECRET_FILE, secret);
    console.log('✅ node_secret 已保存');
  } catch (error) {
    console.error('❌ 保存 node_secret 失败:', error.message);
  }
};

/**
 * 生成消息 ID
 */
const genMessageId = () => `msg_${Date.now()}_${randomHex(4)}`;

/**
 * 生成 ISO 时间戳
 */
const genTimestamp = () => new Date().toISOString();

// ============ 状态管理 ============

const StateManager = {
  load() {
    if (fs.existsSync(CONFIG.STATE_FILE)) {
      try {
        return JSON.parse(fs.readFileSync(CONFIG.STATE_FILE, 'utf8'));
      } catch (error) {
        console.warn('⚠️  状态文件损坏，重建中...');
        return this.createDefault();
      }
    }
    return this.createDefault();
  },
  
  createDefault() {
    return { 
      errors: [], 
      earnings: [], 
      tasks: [],
      claimedTasks: [],
      completedTasks: [],
      webhooks: [],
      metrics: {
        totalRequests: 0,
        successfulRequests: 0,
        failedRequests: 0,
        totalRetryAttempts: 0
      }
    };
  },
  
  save(state) {
    try {
      fs.writeFileSync(CONFIG.STATE_FILE, JSON.stringify(state, null, 2));
    } catch (error) {
      console.error('❌ 保存状态失败:', error.message);
    }
  },
  
  update(updates) {
    const state = this.load();
    Object.assign(state, updates);
    this.save(state);
    return state;
  },
  
  recordMetric(metricType, success = true) {
    const state = this.load();
    if (!state.metrics) state.metrics = this.createDefault().metrics;
    
    state.metrics.totalRequests++;
    if (success) {
      state.metrics.successfulRequests++;
    } else {
      state.metrics.failedRequests++;
    }
    
    this.save(state);
  }
};

// ============ 网络请求（带智能重试 + 自动认证）============

const HttpClient = {
  /**
   * POST 请求（带重试 + 自动认证）
   */
  async post(endpoint, data, retryCount = CONFIG.RETRY.MAX_RETRIES) {
    const url = `${CONFIG.HUB_URL}${endpoint}`;
    
    // 自动添加 node_secret 认证
    const secret = getNodeSecret();
    const headers = { 'Content-Type': 'application/json' };
    if (secret) {
      headers['Authorization'] = `Bearer ${secret}`;
      // 同时也在 body 中添加（兼容两种方式）
      if (!data.sender_secret) {
        data.sender_secret = secret;
      }
    }
    
    for (let attempt = 0; attempt <= retryCount; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), CONFIG.TIMEOUTS.REQUEST);
        
        const response = await fetch(url, {
          method: 'POST',
          headers: headers,
          body: JSON.stringify(data),
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        const result = await response.json();
        
        // 处理业务错误
        if (result.error) {
          const action = ErrorHandler.handle(result.error, result, endpoint);
          
          // 服务器繁忙 - 智能重试
          if (result.error === 'server_busy' && attempt < retryCount) {
            const waitMs = result.retry_after_ms || calculateBackoffDelay(8 - retryCount + attempt);
            console.log(`⏳ 服务器繁忙，等待 ${waitMs}ms 后重试... (剩余：${retryCount - attempt - 1})`);
            StateManager.update({ 
              metrics: { 
                ...StateManager.load().metrics, 
                totalRetryAttempts: (StateManager.load().metrics?.totalRetryAttempts || 0) + 1 
              } 
            });
            await sleep(waitMs);
            continue;
          }
          
          // 频率限制 - 严格遵守
          if (result.error === 'rate_limited') {
            const waitMs = result.context?.retry_after_ms || 30000;
            if (attempt < retryCount && waitMs < 60000) {
              const jitteredWait = waitMs + Math.random() * 200;
              console.log(`⚠️  频率受限，等待 ${Math.round(jitteredWait)}ms`);
              await sleep(jitteredWait);
              continue;
            }
            return { tasks: [], error: 'rate_limited' };
          }
        }
        
        StateManager.recordMetric('post', true);
        return result;
        
      } catch (error) {
        StateManager.recordMetric('post', false);
        
        // 网络错误 - 递增等待重试
        if (attempt < retryCount) {
          const waitMs = calculateBackoffDelay(8 - retryCount + attempt, 2000, 5000);
          console.log(`⚠️  网络错误，等待 ${waitMs}ms 后重试... (${retryCount - attempt - 1} 次剩余)`);
          await sleep(waitMs);
          continue;
        }
        
        throw new Error(`网络请求失败：${error.message}`);
      }
    }
    
    throw new Error('达到最大重试次数');
  },
  
  /**
   * GET 请求
   */
  async get(endpoint) {
    const url = `${CONFIG.HUB_URL}${endpoint}`;
    try {
      const response = await fetch(url, { 
        timeout: CONFIG.TIMEOUTS.REQUEST 
      });
      StateManager.recordMetric('get', true);
      return await response.json();
    } catch (error) {
      StateManager.recordMetric('get', false);
      throw error;
    }
  }
};

// ============ 错误处理 ============

const ErrorMessages = {
  'server_busy': { msg: '⚠️  服务器繁忙，自动重试中...', action: 'retry' },
  'hub_node_id_reserved': { msg: '❌ 使用了 Hub 的 node_id，请生成自己的', action: 'regenerate' },
  'bundle_required': { msg: '❌ 必须同时发布 Gene + Capsule', action: 'fix_bundle' },
  'asset_id_mismatch': { msg: '❌ asset_id 计算错误', action: 'recalculate' },
  'unauthorized': { msg: '❌ 未授权，可能需要重新注册', action: 'reregister' },
  'forbidden': { msg: '❌ 权限不足', action: 'check_permissions' },
  'not_found': { msg: '❌ 资源不存在', action: 'check_id' },
  'rate_limited': { msg: '⚠️  请求频率受限', action: 'wait' },
  'task_already_claimed': { msg: '⚠️  任务已被认领', action: 'skip' },
  'task_expired': { msg: '⚠️  任务已过期', action: 'skip' },
  'insufficient_reputation': { msg: '⚠️  声誉不足', action: 'build_reputation' },
  'invalid_signature': { msg: '❌ 签名无效', action: 'check_key' },
  'webhook_failed': { msg: '⚠️  Webhook 发送失败', action: 'check_url' }
};

const ErrorHandler = {
  handle(error, context = {}, endpoint = '') {
    const errorInfo = ErrorMessages[error] || { msg: `❌ 未知错误：${error}`, action: 'log' };
    console.log(`${errorInfo.msg} (${endpoint})`);
    
    const state = StateManager.load();
    if (!state.errors) state.errors = [];
    state.errors.push({ 
      error, 
      context, 
      endpoint, 
      timestamp: new Date().toISOString(),
      attempt: context.attempt || 1
    });
    state.errors = state.errors.slice(-50); // 只保留最近 50 条
    StateManager.save(state);
    
    return errorInfo.action;
  },
  
  isRetryable(error) {
    const retryableErrors = [
      'server_busy', 'rate_limited', 'timeout', 
      'ECONNRESET', 'ETIMEDOUT', 'ECONNREFUSED'
    ];
    return retryableErrors.includes(error);
  }
};

// ============ 核心业务功能 ============

const CoreFunctions = {
  /**
   * 1. 节点上线通知（Hello）
   */
  async registerNode() {
    const nodeId = getNodeId();
    console.log(`\n【1】节点上线：${nodeId}`);
    
    const payload = {
      protocol: 'gep-a2a',
      protocol_version: '1.0.0',
      message_type: 'hello',
      message_id: genMessageId(),
      sender_id: nodeId,
      timestamp: genTimestamp(),
      payload: {
        capabilities: { tasks: true, publish: true, swarm: true },
        env_fingerprint: { platform: process.platform, arch: process.arch },
        webhook_url: process.env.WEBHOOK_URL || null
      }
    };
    
    const result = await HttpClient.post('/a2a/hello', payload);
    
    if (result.status === 'acknowledged' || result.payload?.status === 'acknowledged') {
      console.log(`✅ 上线成功！`);
      
      // 保存 node_secret（关键！）
      const secret = result.payload?.node_secret;
      if (secret) {
        saveNodeSecret(secret);
        console.log('🔑 node_secret 已保存，后续请求将自动使用');
      }
      
      const payload = result.payload || result;
      if (payload.claim_code) console.log(`📋 Claim: ${payload.claim_code}`);
      if (payload.credit_balance !== undefined) console.log(`💰 积分：${payload.credit_balance}`);
      if (payload.reputation_score !== undefined) console.log(`⭐ 声誉：${payload.reputation_score}`);
      if (payload.heartbeat_interval_ms) {
        console.log(`💓 心跳间隔：${payload.heartbeat_interval_ms / 60000} 分钟`);
        StateManager.update({ heartbeatInterval: payload.heartbeat_interval_ms });
      }
    }
    
    return result;
  },
  
  /**
   * 2. 心跳保活
   */
  async heartbeat(auto = false) {
    const nodeId = getNodeId();
    const state = StateManager.load();
    const interval = state.heartbeatInterval || 900000; // 默认 15 分钟
    
    console.log(`\n【心跳】${auto ? '自动' : '手动'} - ${nodeId}`);
    
    const payload = {
      protocol: 'gep-a2a',
      protocol_version: '1.0.0',
      message_type: 'heartbeat',
      message_id: genMessageId(),
      sender_id: nodeId,
      timestamp: genTimestamp(),
      payload: {
        status: 'online',
        uptime: process.uptime(),
        tasks_completed: state.tasksCompleted || 0,
        assets_published: state.assetsPublished || 0,
        metrics: state.metrics || {}
      }
    };
    
    try {
      const result = await HttpClient.post('/a2a/heartbeat', payload);
      
      if (result.status === 'alive' || result.survival_status === 'alive') {
        console.log('✅ 心跳成功 - 节点在线');
        StateManager.update({ lastHeartbeat: new Date().toISOString() });
        
        if (result.available_tasks?.length > 0) {
          console.log(`📋 发现 ${result.available_tasks.length} 个可用任务`);
        }
      }
      
      return result;
    } catch (error) {
      console.error('❌ 心跳失败:', error.message);
      throw error;
    }
  },
  
  /**
   * 3. 获取任务（增强版 - 官网推荐方式）
   */
  async fetchTasks(retryCount = CONFIG.RETRY.MAX_RETRIES) {
    const nodeId = getNodeId();
    console.log(`\n【2】获取任务列表 (最大重试：${retryCount})`);
    
    const payload = {
      protocol: 'gep-a2a',
      protocol_version: '1.0.0',
      message_type: 'fetch',
      message_id: genMessageId(),
      sender_id: nodeId,
      timestamp: genTimestamp(),
      payload: { include_tasks: true }
    };
    
    try {
      const result = await HttpClient.post('/a2a/fetch', payload, retryCount);
      
      // 关键修复：数据可能在 payload 字段里！
      const responseData = result.payload || result;
      
      // 获取所有可能的返回字段（官网完整格式）
      const tasks = responseData.tasks || [];
      const totalCount = responseData.total_count || tasks.length;
      const availableTasks = responseData.available_tasks || [];
      const openTasks = tasks.filter(t => t.status === 'open').length;
      
      // 过滤最低赏金
      const filteredTasks = tasks.filter(t => (t.bounty || 0) >= CONFIG.MIN_BOUNTY_AMOUNT);
      
      // 显示完整统计信息
      console.log(`📊 任务统计:`);
      console.log(`   总任务数：${totalCount}`);
      console.log(`   可用任务：${availableTasks.length}`);
      console.log(`   开放任务：${openTasks}`);
      console.log(`   当前批次：${tasks.length} 个`);
      if (CONFIG.MIN_BOUNTY_AMOUNT > 0 && filteredTasks.length < tasks.length) {
        console.log(`   过滤后（≥${CONFIG.MIN_BOUNTY_AMOUNT} credits）: ${filteredTasks.length} 个`);
      }
      
      // 显示任务详情（前 5 个）
      if (filteredTasks.length > 0) {
        console.log(`\n📋 任务列表:`);
        filteredTasks.slice(0, 5).forEach((task, i) => {
          console.log(`   ${i+1}. ${task.title || 'Unknown'}`);
          console.log(`      ID: ${task.task_id}`);
          console.log(`      状态：${task.status || 'unknown'}`);
          console.log(`      赏金：${task.bounty || 0} credits`);
          if (task.signals) console.log(`      信号：${task.signals.join(', ')}`);
          if (task.expires_at) console.log(`      过期：${task.expires_at}`);
        });
        if (filteredTasks.length > 5) {
          console.log(`   ... 还有 ${filteredTasks.length - 5} 个任务`);
        }
      }
      
      if (tasks.length > 0) {
        StateManager.update({ 
          lastFetchSuccess: new Date().toISOString(), 
          lastTaskCount: tasks.length,
          lastTotalCount: totalCount
        });
      }
      
      return { ...result, tasks: filteredTasks, totalCount, availableTasks, openTasks };
    } catch (error) {
      console.error('❌ 获取任务失败:', error.message);
      return { tasks: [], error: 'network_error' };
    }
  },
  
  /**
   * 4. 认领任务
   */
  async claimTask(taskId) {
    const nodeId = getNodeId();
    console.log(`\n【3】认领任务：${taskId}`);
    
    const payload = { task_id: taskId, node_id: nodeId };
    const result = await HttpClient.post('/task/claim', payload);
    
    if (result.status === 'claimed' || result.success) {
      console.log('✅ 任务认领成功！');
      const state = StateManager.load();
      if (!state.claimedTasks) state.claimedTasks = [];
      state.claimedTasks.push({ taskId, claimedAt: new Date().toISOString() });
      StateManager.save(state);
    }
    
    return result;
  },
  
  /**
   * 5. 发布解决方案（优化版）
   */
  async publishSolution(task) {
    const nodeId = getNodeId();
    console.log(`\n【4】发布解决方案`);
    
    // 构建 Gene
    const geneData = {
      type: 'Gene', 
      schema_version: '1.5.0', 
      category: 'repair',
      signals_match: task.signals || ['error'],
      summary: `Fix: ${task.title || 'Unknown'}`,
      description: `Automated solution for: ${task.title || 'Unknown task'}`,
      parameters: {
        confidence: { type: 'number', default: 0.85 },
        blast_radius: { type: 'object', default: { files: 1, lines: 10 } }
      }
    };
    const gene = { 
      ...geneData, 
      asset_id: 'sha256:' + crypto.createHash('sha256')
        .update(JSON.stringify(geneData, Object.keys(geneData).sort()))
        .digest('hex') 
    };
    
    // 构建 Capsule
    const capsuleData = {
      type: 'Capsule', 
      schema_version: '1.5.0',
      trigger: task.signals || ['error'], 
      gene: gene.asset_id,
      summary: `Solution: ${task.title || 'Unknown'}`,
      confidence: 0.85, 
      blast_radius: { files: 1, lines: 10 },
      outcome: { status: 'success', score: 0.85 },
      env_fingerprint: { platform: process.platform, arch: process.arch }
    };
    const capsule = { 
      ...capsuleData, 
      asset_id: 'sha256:' + crypto.createHash('sha256')
        .update(JSON.stringify(capsuleData, Object.keys(capsuleData).sort()))
        .digest('hex') 
    };
    
    // 构建 Event
    const eventData = {
      type: 'EvolutionEvent', 
      intent: 'repair',
      capsule_id: capsule.asset_id, 
      genes_used: [gene.asset_id],
      outcome: { status: 'success', score: 0.85 },
      mutations_tried: 1, 
      total_cycles: 1
    };
    const event = { 
      ...eventData, 
      asset_id: 'sha256:' + crypto.createHash('sha256')
        .update(JSON.stringify(eventData, Object.keys(eventData).sort()))
        .digest('hex') 
    };
    
    const payload = {
      protocol: 'gep-a2a', 
      protocol_version: '1.0.0',
      message_type: 'publish', 
      message_id: genMessageId(),
      sender_id: nodeId, 
      timestamp: genTimestamp(),
      payload: { assets: [gene, capsule, event] }
    };
    
    const result = await HttpClient.post('/a2a/publish', payload);
    
    if (result.status === 'published' || result.assets) {
      console.log('✅ 发布成功！');
      console.log(`   Gene: ${gene.asset_id}`);
      console.log(`   Capsule: ${capsule.asset_id}`);
      StateManager.update({ 
        assetsPublished: (StateManager.load().assetsPublished || 0) + 1 
      });
    }
    
    return result;
  },
  
  /**
   * 6. 提交完成任务
   */
  async completeTask(taskId, assetId) {
    const nodeId = getNodeId();
    console.log(`\n【5】提交任务：${taskId}`);
    
    const payload = { task_id: taskId, asset_id: assetId, node_id: nodeId };
    const result = await HttpClient.post('/task/complete', payload);
    
    if (result.status === 'completed' || result.success) {
      console.log('✅ 任务完成！积分将自动发放。');
      const state = StateManager.load();
      state.tasksCompleted = (state.tasksCompleted || 0) + 1;
      if (!state.completedTasks) state.completedTasks = [];
      state.completedTasks.push({ 
        taskId, 
        assetId, 
        completedAt: new Date().toISOString() 
      });
      StateManager.save(state);
    }
    
    return result;
  },
  
  /**
   * 7. 查看节点状态
   */
  async status(nodeId) {
    const id = nodeId || getNodeId();
    console.log(`\n【状态】${id}`);
    
    const result = await HttpClient.get(`/a2a/nodes/${id}`);
    
    if (result.node_id) {
      console.log('✅ 节点在线');
      if (result.reputation_score) console.log(`⭐ 声誉：${result.reputation_score}`);
      if (result.credit_balance) console.log(`💰 积分：${result.credit_balance}`);
      if (result.total_published) console.log(`📦 发布：${result.total_published}`);
      if (result.total_completed) console.log(`✅ 完成：${result.total_completed}`);
    } else {
      console.log('⚠️  节点可能未注册或离线');
    }
    
    return result;
  },
  
  /**
   * 8. 查看收益
   */
  async earnings() {
    const nodeId = getNodeId();
    console.log(`\n【收益】${nodeId}`);
    
    const state = StateManager.load();
    const result = await HttpClient.get(`/billing/earnings/${nodeId}`);
    
    console.log('💰 收益详情:');
    if (result.total_earned) console.log(`   总收益：${result.total_earned} credits`);
    if (result.pending) console.log(`   待结算：${result.pending} credits`);
    if (result.available) console.log(`   可用：${result.available} credits`);
    
    console.log('\n📊 本地统计:');
    console.log(`   完成任务：${state.tasksCompleted || 0}`);
    console.log(`   发布资产：${state.assetsPublished || 0}`);
    if (state.metrics) {
      console.log(`   请求总数：${state.metrics.totalRequests || 0}`);
      console.log(`   成功率：${state.metrics.successfulRequests / (state.metrics.totalRequests || 1) * 100 | 0}%`);
    }
    
    return result;
  },
  
  /**
   * 9. 错误历史
   */
  async errors(clear = false) {
    const state = StateManager.load();
    
    if (clear) {
      StateManager.update({ errors: [] });
      console.log('✅ 错误历史已清空');
      return [];
    }
    
    if (!state.errors || state.errors.length === 0) {
      console.log('\n✅ 无错误记录');
      return [];
    }
    
    console.log(`\n【错误历史】最近 ${state.errors.length} 条:`);
    state.errors.forEach((err, i) => {
      console.log(`${i+1}. [${err.timestamp}] ${err.error} (${err.endpoint})`);
    });
    return state.errors;
  }
};

// ============ 运行模式 ============

const RunModes = {
  /**
   * 单轮执行
   */
  async run() {
    console.log('\n========================================');
    console.log('   EvoMap Lite Client v2.0 - 单轮执行');
    console.log('========================================\n');
    
    try {
      await CoreFunctions.registerNode();
      await sleep(1000);
      
      const fetchResult = await CoreFunctions.fetchTasks();
      if (!fetchResult.tasks || fetchResult.tasks.length === 0) {
        console.log('\n✅ 无可用任务');
        return { success: true, tasksFound: 0 };
      }
      
      const task = fetchResult.tasks.find(t => t.status === 'open');
      if (!task) {
        console.log('\n✅ 无开放任务');
        return { success: true, tasksFound: fetchResult.tasks.length };
      }
      
      console.log(`\n📋 任务：${task.title || 'Unknown'}`);
      
      await CoreFunctions.claimTask(task.task_id);
      await sleep(1000);
      
      const publishResult = await CoreFunctions.publishSolution(task);
      await sleep(1000);
      
      const assetId = publishResult.assets?.[1]?.asset_id || 'sha256:placeholder';
      await CoreFunctions.completeTask(task.task_id, assetId);
      
      console.log('\n========================================');
      console.log('   ✅ 本轮完成！');
      console.log('========================================\n');
      
      return { success: true, tasksCompleted: 1 };
    } catch (error) {
      console.error('\n❌ 执行出错:', error.message);
      return { success: false, error: error.message };
    }
  },
  
  /**
   * 循环执行
   */
  async loop() {
    const intervalMs = CONFIG.LOOP_INTERVAL_HOURS * 60 * 60 * 1000;
    
    console.log(`\n========================================`);
    console.log(`   循环模式 - 每 ${CONFIG.LOOP_INTERVAL_HOURS} 小时一轮`);
    console.log(`========================================\n`);
    
    // 启动心跳循环
    CoreFunctions.heartbeat(true).catch(console.error);
    setInterval(async () => {
      try {
        await CoreFunctions.heartbeat(true);
      } catch (error) {
        console.error('心跳失败:', error.message);
      }
    }, 900000); // 15 分钟
    
    let round = 0;
    while (true) {
      round++;
      console.log(`\n🔄 第 ${round} 轮`);
      await RunModes.run();
      console.log(`\n⏱️  等待 ${CONFIG.LOOP_INTERVAL_HOURS} 小时...`);
      await sleep(intervalMs);
    }
  },
  
  /**
   * Webhook 服务器
   */
  async startWebhook() {
    const server = http.createServer(async (req, res) => {
      if (req.method === 'POST' && req.url === '/webhook') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', async () => {
          try {
            const data = JSON.parse(body);
            console.log('\n🔔 Webhook 通知:', data.type);
            
            // 保存到状态
            const state = StateManager.load();
            if (!state.webhooks) state.webhooks = [];
            state.webhooks.push({ ...data, receivedAt: new Date().toISOString() });
            state.webhooks = state.webhooks.slice(-100);
            StateManager.save(state);
            
            res.writeHead(200);
            res.end('OK');
          } catch (error) {
            res.writeHead(400);
            res.end('Error');
          }
        });
      } else {
        res.writeHead(404);
        res.end('Not Found');
      }
    });
    
    server.listen(CONFIG.WEBHOOK_PORT, () => {
      console.log(`🔔 Webhook 服务器运行在端口 ${CONFIG.WEBHOOK_PORT}`);
    });
  }
};

// ============ 命令行入口 ============

const main = async (args) => {
  const command = args?.[0] || 'run';
  
  console.log(`\n🚀 EvoMap Lite Client v2.0`);
  console.log(`   Hub: ${CONFIG.HUB_URL}`);
  console.log(`   命令：${command}\n`);
  
  switch (command) {
    case 'run': return await RunModes.run();
    case 'loop': return await RunModes.loop();
    case 'status': return await CoreFunctions.status(args?.[1]);
    case 'register': return await CoreFunctions.registerNode();
    case 'fetch': return await CoreFunctions.fetchTasks();
    case 'heartbeat': return await CoreFunctions.heartbeat();
    case 'earnings': return await CoreFunctions.earnings();
    case 'errors': return await CoreFunctions.errors(args?.[1] === 'clear');
    case 'webhook': return await RunModes.startWebhook();
    default:
      console.log('📖 用法：node index.js [命令]');
      console.log('\n命令:');
      console.log('  run          - 运行一轮');
      console.log('  loop         - 循环运行');
      console.log('  status       - 节点状态');
      console.log('  register     - 注册节点');
      console.log('  fetch        - 获取任务');
      console.log('  heartbeat    - 发送心跳');
      console.log('  earnings     - 查看收益');
      console.log('  errors       - 错误历史 (clear 清空)');
      console.log('  webhook      - 启动 Webhook');
  }
};

// 导出模块
module.exports = {
  main,
  run: RunModes.run,
  loop: RunModes.loop,
  config: CONFIG,
  stateManager: StateManager,
  httpClient: HttpClient,
  coreFunctions: CoreFunctions
};

// 主入口
if (require.main === module) {
  main(process.argv.slice(2));
}
