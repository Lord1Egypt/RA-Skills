#!/usr/bin/env node
/**
 * 数据真实性验证器 v7.20
 * 
 * 核心功能:
 * 1. 验证数据是否有来源标注
 * 2. 检测编造/预估数据
 * 3. 强制验证（失败抛出异常）
 */

class DataVerifier {
  constructor(config = {}) {
    this.strictMode = config.strictMode || true;
    this.alarmLog = config.alarmLog || '/home/ubutu/.openclaw/workspace/logs/violations.log';
    
    this.rules = {
      'no-fabrication': {
        name: '不编造数据',
        check: (data) => {
          // 检测是否有来源标注
          return data.source !== undefined && data.source !== null;
        },
        message: '❌ 数据必须标注来源（source 字段）'
      },
      'official-source': {
        name: '使用官方数据',
        check: (data) => {
          // 检测是否为官方来源
          return data.source === 'official';
        },
        message: '⚠️ 数据应来自官方配置，当前来源：'
      },
      'no-estimation': {
        name: '不预估数据',
        check: (data) => {
          // 检测是否包含预估标记
          const content = JSON.stringify(data);
          return !content.includes('估算') && 
                 !content.includes('预计') &&
                 !content.includes('大概') &&
                 !content.includes('约');
        },
        message: '❌ 不能使用预估数据'
      },
      'verified': {
        name: '已验证数据',
        check: (data) => {
          // 检测是否有验证标记
          return data.verified === true;
        },
        message: '❌ 数据必须经过验证'
      }
    };
  }

  /**
   * 验证数据
   */
  verify(data, type) {
    const rule = this.rules[type];
    if (!rule) {
      throw new Error(`未知规则类型：${type}。可用：${Object.keys(this.rules).join(', ')}`);
    }

    const passed = rule.check(data);
    
    return {
      passed,
      rule: rule.name,
      type,
      message: passed ? '✅ 验证通过' : rule.message + (data.source && !passed ? data.source : ''),
      data,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * 多重验证
   */
  verifyMultiple(data, types) {
    const results = [];
    
    for (const type of types) {
      results.push(this.verify(data, type));
    }
    
    const allPassed = results.every(r => r.passed);
    
    return {
      passed: allPassed,
      results,
      failedRules: results.filter(r => !r.passed).map(r => r.rule)
    };
  }

  /**
   * 强制验证（失败则抛出异常）
   */
  forceVerify(data, type) {
    const result = this.verify(data, type);
    
    if (!result.passed) {
      this.logViolation(type, data);
      throw new Error(`数据真实性违规：${result.message}`);
    }
    
    return result;
  }

  /**
   * 记录违规
   */
  logViolation(type, data) {
    const fs = require('fs');
    const violation = {
      timestamp: new Date().toISOString(),
      type,
      data: JSON.stringify(data)
    };
    
    const log = `[${violation.timestamp}] VIOLATION: ${type} - ${JSON.stringify(violation.data)}\n`;
    
    try {
      fs.appendFileSync(this.alarmLog, log);
    } catch (error) {
      console.error('记录违规日志失败:', error.message);
    }
    
    // 控制台告警
    console.error(`\n🚨 数据真实性违规`);
    console.error(`类型：${type}`);
    console.error(`数据：${JSON.stringify(data)}`);
    console.error(`时间：${violation.timestamp}\n`);
  }

  /**
   * 获取验证统计
   */
  getStats() {
    const fs = require('fs');
    
    if (!fs.existsSync(this.alarmLog)) {
      return { total: 0, byType: {} };
    }
    
    const log = fs.readFileSync(this.alarmLog, 'utf8');
    const lines = log.split('\n').filter(l => l.trim());
    
    const stats = {
      total: lines.length,
      byType: {}
    };
    
    for (const line of lines) {
      const match = line.match(/VIOLATION: (\S+)/);
      if (match) {
        const type = match[1];
        stats.byType[type] = (stats.byType[type] || 0) + 1;
      }
    }
    
    return stats;
  }
}

module.exports = DataVerifier;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const [command] = args;
  
  const verifier = new DataVerifier({ strictMode: true });
  
  if (command === 'test') {
    // 测试验证
    console.log('测试 1: 有来源标注的数据');
    try {
      verifier.forceVerify(
        { content: 'Kimi 有 200K 上下文', source: 'official' },
        'no-fabrication'
      );
      console.log('✅ 通过');
    } catch (error) {
      console.log('❌ 失败:', error.message);
    }
    
    console.log('\n测试 2: 无来源标注的数据');
    try {
      verifier.forceVerify(
        { content: 'Kimi 有 256K 上下文' },
        'no-fabrication'
      );
      console.log('✅ 通过');
    } catch (error) {
      console.log('❌ 失败:', error.message);
    }
  }
  
  if (command === 'stats') {
    const stats = verifier.getStats();
    console.log('违规统计:');
    console.log(`总次数：${stats.total}`);
    console.log('按类型:');
    for (const [type, count] of Object.entries(stats.byType)) {
      console.log(`  ${type}: ${count}`);
    }
  }
}
