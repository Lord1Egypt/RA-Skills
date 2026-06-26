#!/usr/bin/env node
/**
 * Cognitive Brain - 安全护栏模块
 * 检测和阻止危险操作
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('safety');
const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
const SAFETY_LOG_PATH = path.join(SKILL_DIR, '.safety-log.json');

// 安全日志
let safetyLog = [];

/**
 * 加载日志
 */
function load() {
  try {
    if (fs.existsSync(SAFETY_LOG_PATH)) {
      safetyLog = JSON.parse(fs.readFileSync(SAFETY_LOG_PATH, 'utf8'));
    }
  } catch (e) { console.error("[safety] 错误:", e.message);
    safetyLog = [];
  }
}

/**
 * 保存日志
 */
function save() {
  try {
    fs.writeFileSync(SAFETY_LOG_PATH, JSON.stringify(safetyLog.slice(-500), null, 2));
  } catch (e) { console.error("[safety] 错误:", e.message);
    // ignore
  }
}

// 危险模式
const DANGEROUS_PATTERNS = {
  // 文件系统危险
  FILE_DELETE: {
    patterns: [
      /rm\s+-rf/,
      /del\s+\/s/,
      /format\s+/,
      /删除\s+所有/,
      /清空\s+磁盘/
    ],
    severity: 'critical',
    action: 'block'
  },

  SYSTEM_COMMAND: {
    patterns: [
      /sudo\s+/,
      /chmod\s+777/,
      /chown\s+/,
      /fdisk/,
      /mkfs/
    ],
    severity: 'high',
    action: 'confirm'
  },

  // 网络危险
  NETWORK_EXPOSE: {
    patterns: [
      /nc\s+-l/,
      /netcat/,
      /开放端口/,
      /端口转发/
    ],
    severity: 'high',
    action: 'confirm'
  },

  DATA_EXFILTRATION: {
    patterns: [
      /curl.*\|\s*sh/,
      /wget.*\|\s*sh/,
      /上传.*密码/,
      /发送.*密钥/
    ],
    severity: 'critical',
    action: 'block'
  },

  // 代码危险
  CODE_INJECTION: {
    patterns: [
      /eval\s*\(/,
      /exec\s*\(/,
      /system\s*\(/,
      /子进程/
    ],
    severity: 'medium',
    action: 'warn'
  },

  // 隐私危险
  PRIVACY_LEAK: {
    patterns: [
      /分享.*个人信息/,
      /公开.*隐私/,
      /上传.*联系人/
    ],
    severity: 'high',
    action: 'confirm'
  },

  // 社交工程
  SOCIAL_ENGINEERING: {
    patterns: [
      /我是管理员/,
      /需要你的密码/,
      /紧急/,
      /验证身份/
    ],
    severity: 'high',
    action: 'warn'
  }
};

// 安全策略
const SAFETY_POLICIES = {
  // 文件系统
  maxFileSize: 100 * 1024 * 1024,  // 100MB
  allowedPaths: [
    '/tmp',
    '/home',
    path.join(HOME, '.openclaw')
  ],
  blockedPaths: [
    '/etc/passwd',
    '/etc/shadow',
    '/root/.ssh'
  ],

  // 网络
  allowedDomains: [],
  blockedDomains: [],

  // 操作
  requireConfirmation: [
    'delete_file',
    'send_email',
    'post_public',
    'modify_system'
  ]
};

/**
 * 检查内容安全性
 */
function checkContent(content) {
  const results = [];

  for (const [ruleName, rule] of Object.entries(DANGEROUS_PATTERNS)) {
    for (const pattern of rule.patterns) {
      if (pattern.test(content)) {
        results.push({
          rule: ruleName,
          severity: rule.severity,
          action: rule.action,
          matchedPattern: pattern.toString(),
          recommendation: getRecommendation(ruleName)
        });
      }
    }
  }

  return results;
}

/**
 * 获取建议
 */
function getRecommendation(ruleName) {
  const recommendations = {
    FILE_DELETE: '删除操作不可恢复，请确认是否必要',
    SYSTEM_COMMAND: '系统命令可能影响稳定性，请谨慎执行',
    NETWORK_EXPOSE: '开放端口可能带来安全风险',
    DATA_EXFILTRATION: '数据外传可能导致信息泄露',
    CODE_INJECTION: '动态执行代码存在安全风险',
    PRIVACY_LEAK: '可能泄露隐私信息',
    SOCIAL_ENGINEERING: '可能存在社会工程攻击'
  };

  return recommendations[ruleName] || '存在潜在风险';
}

/**
 * 检查文件路径安全性
 */
function checkPath(filePath) {
  const results = [];

  // 检查是否在阻止列表
  for (const blocked of SAFETY_POLICIES.blockedPaths) {
    if (filePath.startsWith(blocked)) {
      results.push({
        severity: 'critical',
        action: 'block',
        reason: `路径在禁止列表中: ${blocked}`
      });
    }
  }

  // 检查是否在允许列表
  const isAllowed = SAFETY_POLICIES.allowedPaths.some(
    allowed => filePath.startsWith(allowed)
  );

  if (!isAllowed && results.length === 0) {
    results.push({
      severity: 'medium',
      action: 'confirm',
      reason: '路径不在默认允许范围内'
    });
  }

  return results;
}

/**
 * 检查操作安全性
 */
function checkOperation(operation, context = {}) {
  const results = [];

  // 检查操作类型
  if (SAFETY_POLICIES.requireConfirmation.includes(operation)) {
    results.push({
      severity: 'medium',
      action: 'confirm',
      reason: `操作 ${operation} 需要确认`
    });
  }

  // 检查内容
  if (context.content) {
    const contentResults = checkContent(context.content);
    results.push(...contentResults);
  }

  // 检查路径
  if (context.path) {
    const pathResults = checkPath(context.path);
    results.push(...pathResults);
  }

  return results;
}

/**
 * 决定是否允许操作
 */
function shouldAllow(results) {
  if (results.length === 0) {
    return { allowed: true };
  }

  // 有 critical 级别阻止
  const critical = results.filter(r => r.severity === 'critical');
  if (critical.length > 0) {
    return {
      allowed: false,
      reason: '检测到高风险操作',
      blocks: critical
    };
  }

  // 有需要确认的
  const needConfirm = results.filter(r => r.action === 'confirm');
  if (needConfirm.length > 0) {
    return {
      allowed: 'pending',
      reason: '需要用户确认',
      confirmations: needConfirm
    };
  }

  // 有警告
  const warnings = results.filter(r => r.action === 'warn');
  if (warnings.length > 0) {
    return {
      allowed: true,
      warning: true,
      warnings
    };
  }

  return { allowed: true };
}

/**
 * 记录安全事件
 */
function logSecurityEvent(event) {
  load();

  const record = {
    id: `sec_${Date.now()}`,
    timestamp: Date.now(),
    ...event
  };

  safetyLog.push(record);
  save();

  return record;
}

/**
 * 获取安全统计
 */
function getStats() {
  load();

  const stats = {
    total: safetyLog.length,
    bySeverity: {},
    byAction: {},
    recentBlocks: 0
  };

  const oneHourAgo = Date.now() - 60 * 60 * 1000;

  for (const event of safetyLog) {
    stats.bySeverity[event.severity] = (stats.bySeverity[event.severity] || 0) + 1;
    stats.byAction[event.action] = (stats.byAction[event.action] || 0) + 1;

    if (event.action === 'block' && event.timestamp > oneHourAgo) {
      stats.recentBlocks++;
    }
  }

  return stats;
}

/**
 * 获取最近的安全事件
 */
function getRecentEvents(limit = 20) {
  load();

  return safetyLog.slice(-limit);
}

/**
 * 安全扫描
 */
function scan(input) {
  const results = checkContent(input);
  const decision = shouldAllow(results);

  console.log('\n🔒 安全扫描结果:');
  console.log(`   输入: ${input.slice(0, 50)}...`);
  console.log(`   检测到: ${results.length} 个问题`);

  if (results.length > 0) {
    console.log('\n   详情:');
    for (const r of results) {
      console.log(`   - [${r.severity}] ${r.rule}`);
      console.log(`     建议: ${r.recommendation}`);
    }
  }

  console.log(`\n   决策: ${decision.allowed === true ? '✅ 允许' : decision.allowed === 'pending' ? '⚠️ 需确认' : '❌ 阻止'}`);

  return decision;
}

// ===== 主函数 =====
async function main() {
  const action = process.argv[2];
  const args = process.argv.slice(3);

  load();

  switch (action) {
    case 'scan':
      if (args[0]) {
        scan(args.join(' '));
      }
      break;

    case 'check':
      if (args[0]) {
        const results = checkOperation(args[0]);
        console.log('🔍 检查结果:');
        console.log(JSON.stringify(results, null, 2));
      }
      break;

    case 'stats':
      console.log('📊 安全统计:');
      console.log(JSON.stringify(getStats(), null, 2));
      break;

    case 'recent':
      console.log('📋 最近事件:');
      console.log(JSON.stringify(getRecentEvents(), null, 2));
      break;

    default:
      console.log(`
安全护栏模块

用法:
  node safety.cjs scan <content>   # 扫描内容安全性
  node safety.cjs check <operation> # 检查操作安全性
  node safety.cjs stats             # 查看统计
  node safety.cjs recent            # 查看最近事件

示例:
  node safety.cjs scan "rm -rf /"
  node safety.cjs scan "帮我发邮件"
      `);
  }
}

main();

// 导出模块
module.exports = {
  checkContent,
  checkPath,
  checkOperation,
  shouldAllow,
  scan,
  getStats,
  getRecentEvents,
  logSecurityEvent,
  DANGEROUS_PATTERNS,
  SAFETY_POLICIES
};

