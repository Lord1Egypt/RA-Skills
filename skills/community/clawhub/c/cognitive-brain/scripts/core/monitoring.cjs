#!/usr/bin/env node
/**
 * Cognitive Brain - 性能监控模块
 * 监控系统性能和资源使用
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('monitoring');
const fs = require('fs');
const path = require('path');
const os = require('os');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
const MONITORING_DATA_PATH = path.join(SKILL_DIR, '.monitoring.json');

// 监控数据
let monitoringData = {
  metrics: [],
  alerts: [],
  config: {
    collectionInterval: 60000,  // 1 分钟
    retentionDays: 7,
    alertThresholds: {
      memoryUsage: 0.9,        // 90% 内存使用
      cpuUsage: 0.8,           // 80% CPU 使用
      responseTime: 5000,      // 5 秒响应时间
      errorRate: 0.1           // 10% 错误率
    }
  }
};

/**
 * 加载数据
 */
function load() {
  try {
    if (fs.existsSync(MONITORING_DATA_PATH)) {
      monitoringData = JSON.parse(fs.readFileSync(MONITORING_DATA_PATH, 'utf8'));
    }
  } catch (e) { console.error("[monitoring] 错误:", e.message);
    // ignore
  }
}

/**
 * 保存数据
 */
function save() {
  try {
    // 清理过期数据
    const cutoff = Date.now() - monitoringData.config.retentionDays * 24 * 60 * 60 * 1000;
    monitoringData.metrics = monitoringData.metrics.filter(m => m.timestamp > cutoff);

    fs.writeFileSync(MONITORING_DATA_PATH, JSON.stringify(monitoringData, null, 2));
  } catch (e) { console.error("[monitoring] 错误:", e.message);
    // ignore
  }
}

/**
 * 收集系统指标
 */
function collectSystemMetrics() {
  const metrics = {
    timestamp: Date.now(),
    system: {
      cpuUsage: getCpuUsage(),
      memoryUsage: getMemoryUsage(),
      freeMemory: os.freemem(),
      totalMemory: os.totalmem(),
      loadAvg: os.loadavg(),
      uptime: os.uptime()
    },
    process: {
      memoryUsage: process.memoryUsage(),
      cpuUsage: process.cpuUsage(),
      uptime: process.uptime()
    }
  };

  return metrics;
}

/**
 * 获取 CPU 使用率
 */
function getCpuUsage() {
  const cpus = os.cpus();
  let totalIdle = 0;
  let totalTick = 0;

  for (const cpu of cpus) {
    for (const type in cpu.times) {
      totalTick += cpu.times[type];
    }
    totalIdle += cpu.times.idle;
  }

  return 1 - (totalIdle / totalTick);
}

/**
 * 获取内存使用率
 */
function getMemoryUsage() {
  const free = os.freemem();
  const total = os.totalmem();
  return (total - free) / total;
}

/**
 * 收集应用指标
 */
function collectAppMetrics(appData = {}) {
  const metrics = {
    timestamp: Date.now(),
    app: {
      responseTime: appData.responseTime || null,
      requestCount: appData.requestCount || 0,
      errorCount: appData.errorCount || 0,
      errorRate: appData.errorRate || 0,
      activeConnections: appData.activeConnections || 0,
      cacheHitRate: appData.cacheHitRate || null,
      dbQueryTime: appData.dbQueryTime || null
    }
  };

  return metrics;
}

/**
 * 记录指标
 */
function recordMetric(category, name, value, metadata = {}) {
  load();

  const metric = {
    timestamp: Date.now(),
    category,
    name,
    value,
    metadata
  };

  monitoringData.metrics.push(metric);
  save();

  // 检查阈值
  checkThresholds(metric);

  return metric;
}

/**
 * 检查阈值并生成告警
 */
function checkThresholds(metric) {
  const thresholds = monitoringData.config.alertThresholds;

  let alert = null;

  switch (metric.name) {
    case 'memoryUsage':
      if (metric.value > thresholds.memoryUsage) {
        alert = {
          level: 'warning',
          message: `内存使用率过高: ${(metric.value * 100).toFixed(1)}%`,
          threshold: thresholds.memoryUsage,
          value: metric.value,
          timestamp: Date.now()
        };
      }
      break;

    case 'cpuUsage':
      if (metric.value > thresholds.cpuUsage) {
        alert = {
          level: 'warning',
          message: `CPU 使用率过高: ${(metric.value * 100).toFixed(1)}%`,
          threshold: thresholds.cpuUsage,
          value: metric.value,
          timestamp: Date.now()
        };
      }
      break;

    case 'responseTime':
      if (metric.value > thresholds.responseTime) {
        alert = {
          level: 'warning',
          message: `响应时间过长: ${metric.value}ms`,
          threshold: thresholds.responseTime,
          value: metric.value,
          timestamp: Date.now()
        };
      }
      break;

    case 'errorRate':
      if (metric.value > thresholds.errorRate) {
        alert = {
          level: 'error',
          message: `错误率过高: ${(metric.value * 100).toFixed(1)}%`,
          threshold: thresholds.errorRate,
          value: metric.value,
          timestamp: Date.now()
        };
      }
      break;
  }

  if (alert) {
    monitoringData.alerts.push(alert);
    save();
    console.log(`[monitoring] ⚠️ Alert: ${alert.message}`);
  }

  return alert;
}

/**
 * 获取性能报告
 */
function getPerformanceReport(hours = 24) {
  load();

  const cutoff = Date.now() - hours * 60 * 60 * 1000;
  const recent = monitoringData.metrics.filter(m => m.timestamp > cutoff);

  if (recent.length === 0) {
    return { message: '没有最近的数据' };
  }

  // 按类别分组
  const byCategory = {};
  for (const m of recent) {
    if (!byCategory[m.category]) {
      byCategory[m.category] = {};
    }
    if (!byCategory[m.category][m.name]) {
      byCategory[m.category][m.name] = [];
    }
    byCategory[m.category][m.name].push(m.value);
  }

  // 计算统计
  const stats = {};
  for (const category in byCategory) {
    stats[category] = {};
    for (const name in byCategory[category]) {
      const values = byCategory[category][name];
      stats[category][name] = {
        count: values.length,
        avg: values.reduce((a, b) => a + b, 0) / values.length,
        min: Math.min(...values),
        max: Math.max(...values),
        latest: values[values.length - 1]
      };
    }
  }

  return {
    period: `${hours} 小时`,
    collectedAt: Date.now(),
    stats,
    alerts: monitoringData.alerts.filter(a => a.timestamp > cutoff)
  };
}

/**
 * 获取系统健康状态
 */
function getHealthStatus() {
  const current = collectSystemMetrics();

  const health = {
    status: 'healthy',
    checks: [],
    timestamp: Date.now()
  };

  // 内存检查
  if (current.system.memoryUsage > monitoringData.config.alertThresholds.memoryUsage) {
    health.status = 'degraded';
    health.checks.push({
      name: 'memory',
      status: 'warning',
      value: current.system.memoryUsage,
      message: '内存使用率过高'
    });
  } else {
    health.checks.push({
      name: 'memory',
      status: 'ok',
      value: current.system.memoryUsage
    });
  }

  // CPU 检查
  if (current.system.cpuUsage > monitoringData.config.alertThresholds.cpuUsage) {
    health.status = 'degraded';
    health.checks.push({
      name: 'cpu',
      status: 'warning',
      value: current.system.cpuUsage,
      message: 'CPU 使用率过高'
    });
  } else {
    health.checks.push({
      name: 'cpu',
      status: 'ok',
      value: current.system.cpuUsage
    });
  }

  // 最近告警检查
  const recentAlerts = monitoringData.alerts.filter(
    a => a.timestamp > Date.now() - 60 * 60 * 1000
  );
  if (recentAlerts.length > 5) {
    health.status = 'unhealthy';
    health.checks.push({
      name: 'alerts',
      status: 'error',
      value: recentAlerts.length,
      message: '最近 1 小时有多个告警'
    });
  }

  return health;
}

/**
 * 清理旧数据
 */
function cleanup() {
  load();

  const cutoff = Date.now() - monitoringData.config.retentionDays * 24 * 60 * 60 * 1000;

  const before = monitoringData.metrics.length;
  monitoringData.metrics = monitoringData.metrics.filter(m => m.timestamp > cutoff);
  monitoringData.alerts = monitoringData.alerts.filter(a => a.timestamp > cutoff);

  save();

  return {
    removed: before - monitoringData.metrics.length,
    remaining: monitoringData.metrics.length
  };
}

// ===== 主函数 =====
async function main() {
  const action = process.argv[2];
  const args = process.argv.slice(3);

  load();

  switch (action) {
    case 'collect':
      const metrics = collectSystemMetrics();
      console.log('📊 系统指标:');
      console.log(`   CPU 使用: ${(metrics.system.cpuUsage * 100).toFixed(1)}%`);
      console.log(`   内存使用: ${(metrics.system.memoryUsage * 100).toFixed(1)}%`);
      console.log(`   空闲内存: ${(metrics.system.freeMemory / 1024 / 1024).toFixed(0)} MB`);
      console.log(`   系统运行: ${(metrics.system.uptime / 3600).toFixed(1)} 小时`);
      break;

    case 'record':
      if (args[0] && args[1] && args[2]) {
        const metric = recordMetric(args[0], args[1], parseFloat(args[2]));
        console.log('✅ 指标已记录');
      }
      break;

    case 'report':
      const hours = parseInt(args[0]) || 24;
      console.log(JSON.stringify(getPerformanceReport(hours), null, 2));
      break;

    case 'health':
      const health = getHealthStatus();
      console.log(`状态: ${health.status}`);
      health.checks.forEach(c => {
        console.log(`  ${c.name}: ${c.status} (${typeof c.value === 'number' ? (c.value * 100).toFixed(1) + '%' : c.value})`);
      });
      break;

    case 'alerts':
      const recentAlerts = monitoringData.alerts.slice(-10);
      console.log(`📋 最近 ${recentAlerts.length} 个告警:`);
      recentAlerts.forEach(a => {
        console.log(`   [${a.level}] ${a.message}`);
      });
      break;

    case 'cleanup':
      const result = cleanup();
      console.log(`✅ 清理完成: 移除 ${result.removed} 条，保留 ${result.remaining} 条`);
      break;

    default:
      console.log(`
性能监控模块

用法:
  node monitoring.cjs collect              # 收集系统指标
  node monitoring.cjs record <cat> <name> <value>  # 记录指标
  node monitoring.cjs report [hours]       # 性能报告
  node monitoring.cjs health               # 健康状态
  node monitoring.cjs alerts               # 查看告警
  node monitoring.cjs cleanup              # 清理旧数据
      `);
  }
}

main();
