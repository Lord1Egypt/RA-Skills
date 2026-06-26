#!/usr/bin/env node

/**
 * Failure Monitor - 主监控脚本
 * 
 * 功能：
 * 1. 检查所有 cron jobs 状态
 * 2. 检测失败的任务
 * 3. 分析错误类型
 * 4. 自动修复可修复的问题
 * 5. 需要人工时推送确认请求
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const CONFIG = {
  jobsFile: '/Users/xufan65/.openclaw/cron/jobs.json',
  logFile: '/Users/xufan65/.openclaw/workspace/memory/failure-monitor-log.json',
  rulesFile: '/Users/xufan65/.openclaw/workspace/skills/failure-monitor/config/rules.json',
  notifyChannel: 'discord',
  notifyTo: 'channel:1478698808631361647'
};

// 错误类型和修复方案
const AUTO_FIX_RULES = [
  {
    pattern: /job execution timed out/i,
    type: 'timeout',
    action: 'increaseTimeout',
    params: { from: 120, to: 300 },
    description: '增加超时时间'
  },
  {
    pattern: /Channel is required/i,
    type: 'config',
    action: 'updateDeliveryChannel',
    params: { channel: 'discord' },
    description: '更新推送频道配置'
  },
  {
    pattern: /Permission denied/i,
    type: 'permission',
    action: 'fixPermissions',
    description: '修复文件权限'
  }
];

// 需要人工确认的错误
const NEEDS_CONFIRMATION = [
  {
    pattern: /API key invalid|API key expired/i,
    type: 'api-key',
    description: 'API Key 失效'
  },
  {
    pattern: /Script not found|Syntax error/i,
    type: 'script-error',
    description: '脚本错误'
  },
  {
    pattern: /Network timeout|Connection refused/i,
    type: 'network',
    description: '网络问题'
  }
];

class FailureMonitor {
  constructor() {
    this.jobs = [];
    this.failedJobs = [];
    this.log = this.loadLog();
  }

  /**
   * 加载日志
   */
  loadLog() {
    try {
      if (fs.existsSync(CONFIG.logFile)) {
        return JSON.parse(fs.readFileSync(CONFIG.logFile, 'utf8'));
      }
    } catch (e) {
      console.error('加载日志失败:', e.message);
    }
    return { entries: [] };
  }

  /**
   * 保存日志
   */
  saveLog() {
    try {
      fs.writeFileSync(CONFIG.logFile, JSON.stringify(this.log, null, 2));
    } catch (e) {
      console.error('保存日志失败:', e.message);
    }
  }

  /**
   * 加载 cron jobs
   */
  loadJobs() {
    try {
      const data = JSON.parse(fs.readFileSync(CONFIG.jobsFile, 'utf8'));
      this.jobs = data.jobs || [];
      console.log(`✅ 加载了 ${this.jobs.length} 个定时任务`);
    } catch (e) {
      console.error('❌ 加载 jobs 失败:', e.message);
      process.exit(1);
    }
  }

  /**
   * 检查失败的任务
   */
  checkFailedJobs() {
    this.failedJobs = this.jobs.filter(job => {
      const status = job.state?.lastStatus || 'idle';
      const consecutiveErrors = job.state?.consecutiveErrors || 0;
      return status === 'error' || consecutiveErrors > 0;
    });

    console.log(`\n📊 检查结果:`);
    console.log(`   总任务数: ${this.jobs.length}`);
    console.log(`   失败任务: ${this.failedJobs.length}`);

    if (this.failedJobs.length === 0) {
      console.log('\n✅ 所有任务运行正常！');
      return;
    }

    console.log('\n❌ 失败的任务:');
    this.failedJobs.forEach(job => {
      const error = job.state?.lastError || 'Unknown error';
      const errors = job.state?.consecutiveErrors || 0;
      console.log(`   • ${job.name} (${errors} 次失败)`);
      console.log(`     错误: ${error.substring(0, 80)}...`);
    });
  }

  /**
   * 诊断错误类型
   */
  diagnose(job) {
    const error = job.state?.lastError || '';
    console.log(`\n🔍 诊断任务: ${job.name}`);
    console.log(`   错误信息: ${error}`);

    // 检查是否可以自动修复
    for (const rule of AUTO_FIX_RULES) {
      if (rule.pattern.test(error)) {
        console.log(`   ✅ 可自动修复: ${rule.description}`);
        return { canAutoFix: true, rule, job };
      }
    }

    // 检查是否需要人工确认
    for (const rule of NEEDS_CONFIRMATION) {
      if (rule.pattern.test(error)) {
        console.log(`   ⚠️  需要人工介入: ${rule.description}`);
        return { canAutoFix: false, rule, job };
      }
    }

    // 未知错误类型
    console.log(`   ❓ 未知错误类型`);
    return { canAutoFix: false, rule: { type: 'unknown', description: '未知错误' }, job };
  }

  /**
   * 自动修复
   */
  async autoFix(diagnosis) {
    const { job, rule } = diagnosis;
    console.log(`\n🔧 自动修复: ${job.name}`);
    console.log(`   操作: ${rule.description}`);

    try {
      switch (rule.action) {
        case 'increaseTimeout':
          await this.increaseTimeout(job, rule.params);
          break;
        case 'updateDeliveryChannel':
          await this.updateDeliveryChannel(job, rule.params);
          break;
        case 'fixPermissions':
          await this.fixPermissions(job);
          break;
        default:
          console.log(`   ⚠️  未知的修复操作: ${rule.action}`);
          return false;
      }

      // 记录修复
      this.log.entries.push({
        timestamp: new Date().toISOString(),
        jobName: job.name,
        jobId: job.id,
        error: job.state?.lastError,
        fix: rule.description,
        status: 'success'
      });
      this.saveLog();

      console.log(`   ✅ 修复成功！`);
      return true;
    } catch (e) {
      console.error(`   ❌ 修复失败:`, e.message);
      
      this.log.entries.push({
        timestamp: new Date().toISOString(),
        jobName: job.name,
        jobId: job.id,
        error: job.state?.lastError,
        fix: rule.description,
        status: 'failed',
        reason: e.message
      });
      this.saveLog();
      
      return false;
    }
  }

  /**
   * 增加超时时间
   */
  async increaseTimeout(job, params) {
    const cmd = `openclaw cron edit ${job.id} --timeout-seconds ${params.to}`;
    console.log(`   执行: ${cmd}`);
    execSync(cmd, { encoding: 'utf8' });
  }

  /**
   * 更新推送频道
   */
  async updateDeliveryChannel(job, params) {
    const cmd = `openclaw cron edit ${job.id} --channel ${params.channel} --to "${job.delivery?.to || 'last'}"`;
    console.log(`   执行: ${cmd}`);
    execSync(cmd, { encoding: 'utf8' });
  }

  /**
   * 修复文件权限
   */
  async fixPermissions(job) {
    // 从 payload.message 中提取脚本路径
    const message = job.payload?.message || '';
    const scriptMatch = message.match(/(\/[\w\/\-\.]+\.(?:sh|py|js|cjs|mjs))/);
    
    if (scriptMatch) {
      const scriptPath = scriptMatch[1];
      const cmd = `chmod +x ${scriptPath}`;
      console.log(`   执行: ${cmd}`);
      execSync(cmd, { encoding: 'utf8' });
    } else {
      throw new Error('无法从任务配置中提取脚本路径');
    }
  }

  /**
   * 推送通知
   */
  async notify(diagnosis, fixResult) {
    const { job, rule, canAutoFix } = diagnosis;
    
    let message;
    if (canAutoFix && fixResult) {
      // 自动修复成功
      message = this.formatAutoFixSuccess(job, rule);
    } else if (canAutoFix && !fixResult) {
      // 自动修复失败
      message = this.formatAutoFixFailed(job, rule);
    } else {
      // 需要人工介入
      message = this.formatNeedsConfirmation(job, rule);
    }

    console.log('\n📤 推送通知到 Discord...');
    console.log(message);
    
    // TODO: 调用 message tool 推送到 Discord
    // 需要在 OpenClaw 环境中运行才能使用 message tool
  }

  /**
   * 格式化自动修复成功消息
   */
  formatAutoFixSuccess(job, rule) {
    const timestamp = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    return `# ✅ 自动修复成功

**任务**: ${job.name}
**问题**: ${rule.description}
**修复**: ${rule.action}
**时间**: ${timestamp}

**详情**:
- 错误: ${job.state?.lastError?.substring(0, 100)}
- 已自动执行修复操作
- 下次运行应该正常`;
  }

  /**
   * 格式化自动修复失败消息
   */
  formatAutoFixFailed(job, rule) {
    const timestamp = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    return `# ❌ 自动修复失败

**任务**: ${job.name}
**问题**: ${rule.description}
**时间**: ${timestamp}

**详情**:
- 错误: ${job.state?.lastError?.substring(0, 100)}
- 尝试自动修复失败
- 可能需要手动检查

**建议操作**:
1. 检查任务配置
2. 查看详细日志
3. 手动修复问题`;
  }

  /**
   * 格式化需要人工确认消息
   */
  formatNeedsConfirmation(job, rule) {
    const timestamp = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    return `# ⚠️ 需要人工介入

**任务**: ${job.name}
**问题**: ${rule.description}
**时间**: ${timestamp}

**错误详情**:
\`\`\`
${job.state?.lastError || 'Unknown error'}
\`\`\`

**建议操作**:
1. 检查相关配置和环境变量
2. 查看任务详情
3. 手动修复问题

**回复 "确认" 执行修复，或 "忽略" 跳过**`;
  }

  /**
   * 主运行函数
   */
  async run() {
    console.log('🚀 Failure Monitor 启动\n');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

    // 1. 加载任务
    this.loadJobs();

    // 2. 检查失败任务
    this.checkFailedJobs();

    if (this.failedJobs.length === 0) {
      return;
    }

    // 3. 诊断每个失败任务
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🔍 开始诊断...\n');

    for (const job of this.failedJobs) {
      const diagnosis = this.diagnose(job);

      if (diagnosis.canAutoFix) {
        // 自动修复
        const fixResult = await this.autoFix(diagnosis);
        await this.notify(diagnosis, fixResult);
      } else {
        // 推送确认请求
        await this.notify(diagnosis, false);
      }
    }

    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('✅ Failure Monitor 完成\n');
  }
}

// 运行
if (require.main === module) {
  const monitor = new FailureMonitor();
  monitor.run().catch(e => {
    console.error('❌ 运行失败:', e);
    process.exit(1);
  });
}

module.exports = FailureMonitor;
