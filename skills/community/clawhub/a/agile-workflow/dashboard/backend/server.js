#!/usr/bin/env node
/**
 * 可视化监控后端服务 v6.0-Phase2
 * 
 * 核心功能:
 * 1. REST API 服务
 * 2. WebSocket 实时推送
 * 3. 数据聚合处理
 * 4. 状态监控采集
 */

const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');
const fs = require('fs');

// ============ 配置 ============

const CONFIG = {
  port: process.env.DASHBOARD_PORT || 8080,
  dataDir: path.join(__dirname, '../data'),
  updateInterval: 1000, // 1 秒更新一次
  wsHeartbeat: 30000    // 30 秒心跳
};

// ============ 数据采集器 ============

class DataCollector {
  constructor() {
    this.cache = {
      overview: null,
      tasks: [],
      agents: {},
      alerts: [],
      metrics: null,
      lastUpdate: null
    };
    
    this.subscribers = new Set();
    this.startCollection();
  }

  /**
   * 开始数据采集
   */
  startCollection() {
    console.log('📊 开始数据采集...');
    
    // 定时采集数据
    setInterval(() => {
      this.collectData();
    }, CONFIG.updateInterval);
  }

  /**
   * 采集数据
   */
  collectData() {
    try {
      // 采集概览数据
      this.cache.overview = this.collectOverview();
      
      // 采集任务数据
      this.cache.tasks = this.collectTasks();
      
      // 采集 Agent 数据
      this.cache.agents = this.collectAgents();
      
      // 采集告警数据
      this.cache.alerts = this.collectAlerts();
      
      // 采集性能指标
      this.cache.metrics = this.collectMetrics();
      
      // 更新时间戳
      this.cache.lastUpdate = Date.now();
      
      // 推送给所有订阅者
      this.broadcast();
      
    } catch (error) {
      console.error('❌ 数据采集失败:', error.message);
    }
  }

  /**
   * 采集概览数据
   */
  collectOverview() {
    // 从各模块采集数据
    const taskStats = this.getTaskStats();
    const agentStats = this.getAgentStats();
    const qualityStats = this.getQualityStats();
    
    return {
      totalTasks: taskStats.total,
      runningTasks: taskStats.running,
      completedTasks: taskStats.completed,
      completionRate: taskStats.completionRate,
      activeAgents: agentStats.active,
      idleAgents: agentStats.idle,
      avgQualityScore: qualityStats.avgScore,
      testPassRate: qualityStats.passRate,
      timestamp: Date.now()
    };
  }

  /**
   * 采集任务数据
   */
  collectTasks() {
    // 模拟任务数据（实际应从工作流引擎获取）
    return [
      {
        id: 'task-001',
        name: '第 1 章创作',
        type: 'document',
        progress: 80,
        qualityScore: 85,
        status: 'running',
        agent: 'chapter_writer',
        startTime: Date.now() - 3600000,
        estimatedEnd: Date.now() + 900000
      },
      {
        id: 'task-002',
        name: '方案设计',
        type: 'design',
        progress: 60,
        qualityScore: 90,
        status: 'running',
        agent: 'designer',
        startTime: Date.now() - 1800000,
        estimatedEnd: Date.now() + 1800000
      },
      {
        id: 'task-003',
        name: '数据分析',
        type: 'analysis',
        progress: 100,
        qualityScore: 92,
        status: 'completed',
        agent: 'analyst',
        startTime: Date.now() - 7200000,
        endTime: Date.now() - 600000
      }
    ];
  }

  /**
   * 采集 Agent 数据
   */
  collectAgents() {
    // 模拟 Agent 数据（实际应从 Agent 管理器获取）
    return {
      'chapter_writer': {
        name: 'chapter_writer',
        status: 'active',
        currentTask: 'task-001',
        load: 80,
        memory: 256,
        cpu: 15,
        lastHeartbeat: Date.now()
      },
      'world_builder': {
        name: 'world_builder',
        status: 'active',
        currentTask: 'task-002',
        load: 40,
        memory: 128,
        cpu: 8,
        lastHeartbeat: Date.now()
      },
      'analyst': {
        name: 'analyst',
        status: 'idle',
        currentTask: null,
        load: 0,
        memory: 64,
        cpu: 2,
        lastHeartbeat: Date.now()
      }
    };
  }

  /**
   * 采集告警数据
   */
  collectAlerts() {
    // 模拟告警数据
    return [
      {
        id: 'alert-001',
        level: 'warning',
        message: '任务 task-005 质量评分 65 分，低于阈值',
        timestamp: Date.now() - 300000,
        handled: false
      },
      {
        id: 'alert-002',
        level: 'info',
        message: 'Token 使用率 85%，接近限制',
        timestamp: Date.now() - 600000,
        handled: true
      }
    ];
  }

  /**
   * 采集性能指标
   */
  collectMetrics() {
    const usage = process.memoryUsage();
    
    return {
      memory: {
        used: Math.round(usage.heapUsed / 1024 / 1024),
        total: Math.round(usage.heapTotal / 1024 / 1024),
        percent: Math.round(usage.heapUsed / usage.heapTotal * 100)
      },
      cpu: {
        percent: Math.round(process.cpuUsage().user / 1000)
      },
      uptime: process.uptime(),
      timestamp: Date.now()
    };
  }

  /**
   * 获取任务统计
   */
  getTaskStats() {
    const tasks = this.cache.tasks || [];
    const total = tasks.length;
    const completed = tasks.filter(t => t.status === 'completed').length;
    const running = tasks.filter(t => t.status === 'running').length;
    const completionRate = total > 0 ? Math.round(completed / total * 100) : 0;
    
    return { total, running, completed, completionRate };
  }

  /**
   * 获取 Agent 统计
   */
  getAgentStats() {
    const agents = Object.values(this.cache.agents || {});
    const active = agents.filter(a => a.status === 'active').length;
    const idle = agents.filter(a => a.status === 'idle').length;
    
    return { active, idle, total: agents.length };
  }

  /**
   * 获取质量统计
   */
  getQualityStats() {
    const tasks = this.cache.tasks || [];
    const scoredTasks = tasks.filter(t => t.qualityScore);
    const avgScore = scoredTasks.length > 0
      ? Math.round(scoredTasks.reduce((sum, t) => sum + t.qualityScore, 0) / scoredTasks.length)
      : 0;
    const passRate = 100; // 模拟值
    
    return { avgScore, passRate };
  }

  /**
   * 订阅数据更新
   */
  subscribe(callback) {
    this.subscribers.add(callback);
    return () => this.subscribers.delete(callback);
  }

  /**
   * 广播数据更新
   */
  broadcast() {
    const data = this.getCache();
    this.subscribers.forEach(callback => {
      try {
        callback(data);
      } catch (error) {
        console.error('❌ 广播失败:', error.message);
      }
    });
  }

  /**
   * 获取缓存数据
   */
  getCache() {
    return {
      overview: this.cache.overview,
      tasks: this.cache.tasks,
      agents: this.cache.agents,
      alerts: this.cache.alerts,
      metrics: this.cache.metrics,
      lastUpdate: this.cache.lastUpdate
    };
  }
}

// ============ 创建服务 ============

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST']
  }
});

// 创建数据采集器
const collector = new DataCollector();

// ============ 中间件 ============

app.use(express.json());
app.use(express.static(path.join(__dirname, '../frontend/dist')));

// ============ REST API ============

/**
 * 获取系统概览
 */
app.get('/api/overview', (req, res) => {
  const data = collector.getCache();
  res.json(data.overview || { error: '暂无数据' });
});

/**
 * 获取任务列表
 */
app.get('/api/tasks', (req, res) => {
  const data = collector.getCache();
  res.json(data.tasks || []);
});

/**
 * 获取任务详情
 */
app.get('/api/tasks/:id', (req, res) => {
  const data = collector.getCache();
  const task = (data.tasks || []).find(t => t.id === req.params.id);
  
  if (task) {
    res.json(task);
  } else {
    res.status(404).json({ error: '任务不存在' });
  }
});

/**
 * 获取 Agent 列表
 */
app.get('/api/agents', (req, res) => {
  const data = collector.getCache();
  res.json(Object.values(data.agents || {}));
});

/**
 * 获取 Agent 详情
 */
app.get('/api/agents/:name', (req, res) => {
  const data = collector.getCache();
  const agent = data.agents[req.params.name];
  
  if (agent) {
    res.json(agent);
  } else {
    res.status(404).json({ error: 'Agent 不存在' });
  }
});

/**
 * 启动 Agent
 */
app.post('/api/agents/:name/start', (req, res) => {
  // TODO: 实际启动 Agent 逻辑
  res.json({ success: true, message: `Agent ${req.params.name} 启动中...` });
});

/**
 * 停止 Agent
 */
app.post('/api/agents/:name/stop', (req, res) => {
  // TODO: 实际停止 Agent 逻辑
  res.json({ success: true, message: `Agent ${req.params.name} 停止中...` });
});

/**
 * 获取告警列表
 */
app.get('/api/alerts', (req, res) => {
  const data = collector.getCache();
  res.json(data.alerts || []);
});

/**
 * 获取性能指标
 */
app.get('/api/metrics', (req, res) => {
  const data = collector.getCache();
  res.json(data.metrics || { error: '暂无数据' });
});

// ============ WebSocket ============

io.on('connection', (socket) => {
  console.log(`🔌 客户端连接：${socket.id}`);
  
  // 发送初始数据
  socket.emit('init', collector.getCache());
  
  // 订阅数据更新
  const unsubscribe = collector.subscribe((data) => {
    socket.emit('update', data);
  });
  
  // 心跳
  socket.on('ping', () => {
    socket.emit('pong', Date.now());
  });
  
  // 断开连接
  socket.on('disconnect', () => {
    console.log(`🔌 客户端断开：${socket.id}`);
    unsubscribe();
  });
});

// ============ 启动服务 ============

server.listen(CONFIG.port, () => {
  console.log('═'.repeat(60));
  console.log('🚀 可视化监控服务已启动');
  console.log('═'.repeat(60));
  console.log(`端口：${CONFIG.port}`);
  console.log(`API: http://localhost:${CONFIG.port}/api`);
  console.log(`WebSocket: ws://localhost:${CONFIG.port}`);
  console.log(`仪表盘：http://localhost:${CONFIG.port}`);
  console.log('═'.repeat(60));
});

// ============ 优雅关闭 ============

process.on('SIGTERM', () => {
  console.log('\n🛑 收到 SIGTERM 信号，正在关闭服务...');
  server.close(() => {
    console.log('✅ 服务已关闭');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('\n🛑 收到 SIGINT 信号，正在关闭服务...');
  server.close(() => {
    console.log('✅ 服务已关闭');
    process.exit(0);
  });
});

// 导出 API
module.exports = { app, server, io, collector, CONFIG };
