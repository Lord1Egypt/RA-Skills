#!/usr/bin/env node
/**
 * 汇报验证器 v7.20
 * 
 * 核心功能:
 * 1. 验证汇报内容是否已验证
 * 2. 验证数据来源
 * 3. 阻止未验证汇报
 */

const DataVerifier = require('./data-verifier');

class ReportValidator {
  constructor(config = {}) {
    this.verifier = new DataVerifier(config);
    this.strictMode = config.strictMode || true;
  }

  /**
   * 验证汇报内容
   */
  async validateReport(report) {
    const validations = [];

    // 1. 验证进度数据
    if (report.progress !== undefined) {
      const progressValid = this.verifyProgress(report.progress);
      validations.push(progressValid);
    }

    // 2. 验证状态数据
    if (report.status !== undefined) {
      const statusValid = this.verifyStatus(report.status);
      validations.push(statusValid);
    }

    // 3. 验证 token 数据
    if (report.tokenUsage !== undefined) {
      const tokenValid = this.verifyTokenData(report.tokenUsage);
      validations.push(tokenValid);
    }

    // 4. 验证整体标记
    if (report.verified !== true) {
      validations.push({
        type: 'report-verified',
        passed: false,
        message: '❌ 汇报必须标记为已验证（verified: true）'
      });
    }

    // 汇总结果
    const allPassed = validations.every(v => v.passed);
    
    return {
      passed: allPassed,
      validations,
      canReport: allPassed,
      blockedReason: allPassed ? null : '数据未通过真实性验证',
      failedRules: validations.filter(v => !v.passed).map(v => v.type)
    };
  }

  /**
   * 验证进度数据
   */
  verifyProgress(progress) {
    // 检查是否有验证标记
    if (!progress.verified) {
      return {
        type: 'progress-verified',
        passed: false,
        message: '❌ 进度数据未验证（缺少 verified: true）'
      };
    }

    // 检查是否有验证时间
    if (!progress.verifiedAt) {
      return {
        type: 'progress-timestamp',
        passed: false,
        message: '❌ 进度数据缺少验证时间（verifiedAt）'
      };
    }

    // 检查数据来源
    if (!progress.source) {
      return {
        type: 'progress-source',
        passed: false,
        message: '❌ 进度数据缺少来源标注（source）'
      };
    }

    return {
      type: 'progress',
      passed: true,
      message: '✅ 进度数据已验证'
    };
  }

  /**
   * 验证状态数据
   */
  verifyStatus(status) {
    // 检查是否有验证标记
    if (!status.verified) {
      return {
        type: 'status-verified',
        passed: false,
        message: '❌ 状态数据未验证'
      };
    }

    return {
      type: 'status',
      passed: true,
      message: '✅ 状态数据已验证'
    };
  }

  /**
   * 验证 token 数据
   */
  verifyTokenData(tokenData) {
    // 检查数据来源
    if (!tokenData.source) {
      return {
        type: 'token-source',
        passed: false,
        message: '❌ Token 数据必须标注来源（source）'
      };
    }

    // 检查是否为官方数据
    if (tokenData.source !== 'official') {
      return {
        type: 'token-official',
        passed: false,
        message: '⚠️ Token 数据非官方来源：' + tokenData.source
      };
    }

    return {
      type: 'token',
      passed: true,
      message: '✅ Token 数据来自官方'
    };
  }

  /**
   * 强制验证（失败则抛出异常）
   */
  forceValidate(report) {
    return this.validateReport(report).then(result => {
      if (!result.passed) {
        const failedRules = result.failedRules.join(', ');
        throw new Error(`汇报验证失败：${failedRules}`);
      }
      return result;
    });
  }
}

module.exports = ReportValidator;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const [command] = args;
  
  const validator = new ReportValidator({ strictMode: true });
  
  if (command === 'test') {
    // 测试 1: 已验证的汇报
    console.log('测试 1: 已验证的汇报');
    validator.validateReport({
      progress: { value: 50, verified: true, verifiedAt: new Date().toISOString(), source: 'actual' },
      status: { verified: true },
      tokenUsage: { source: 'official' },
      verified: true
    }).then(result => {
      console.log(result.canReport ? '✅ 允许汇报' : '❌ 阻止汇报');
      console.log(result.validations.map(v => `  ${v.message}`).join('\n'));
    });
    
    // 测试 2: 未验证的汇报
    console.log('\n测试 2: 未验证的汇报');
    validator.validateReport({
      progress: { value: 50 },
      status: {},
      tokenUsage: {},
      verified: false
    }).then(result => {
      console.log(result.canReport ? '✅ 允许汇报' : '❌ 阻止汇报');
      console.log(result.blockedReason);
      console.log('失败规则:', result.failedRules.join(', '));
    });
  }
}
