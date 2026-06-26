/**
 * ClawGuard v3 - Shield 核心引擎
 * 主动护盾：提示词注入防护、意图验证、智能加固
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 导入规则
const rules = require('../../shared/rules/interceptor-rules.js');

class Shield {
  constructor() {
    this.rules = rules;
  }

  /**
   * 检测提示词注入
   */
  detectPromptInjection(text) {
    const result = {
      timestamp: new Date().toISOString(),
      inputLength: text.length,
      threats: [],
      riskScore: 0,
      riskLevel: 'SAFE',
      recommendations: []
    };

    // 1. 检测编码注入
    result.encodingThreats = this.detectEncodingInjection(text);

    // 2. 检测角色扮演/劫持
    result.rolePlayThreats = this.detectRolePlay(text);

    // 3. 检测越狱尝试
    result.jailbreakThreats = this.detectJailbreak(text);

    // 4. 检测指令链劫持
    result.chainHijackThreats = this.detectChainHijack(text);

    // 5. 合并威胁
    result.threats = [
      ...result.encodingThreats,
      ...result.rolePlayThreats,
      ...result.jailbreakThreats,
      ...result.chainHijackThreats
    ];

    // 6. 计算风险评分
    result.riskScore = this.calculateRiskScore(result.threats);
    result.riskLevel = this.determineRiskLevel(result.riskScore);

    // 7. 生成建议
    result.recommendations = this.generateRecommendations(result);

    return result;
  }

  /**
   * 检测编码注入
   */
  detectEncodingInjection(text) {
    const threats = [];
    const patterns = this.rules.promptInjectionRules;

    // Base64 检测
    const base64Pattern = /([A-Za-z0-9+/]{20,}={0,2})/g;
    let match;
    while ((match = base64Pattern.exec(text)) !== null) {
      const decoded = this.tryDecodeBase64(match[1]);
      if (decoded && decoded !== match[1]) {
        threats.push({
          type: 'base64_injection',
          severity: 'HIGH',
          original: match[1].substring(0, 50) + '...',
          decoded: decoded.substring(0, 100),
          position: match.index,
          description: '检测到 Base64 编码的隐藏内容'
        });
      }
    }

    // 十六进制检测
    const hexPattern = /\\x([0-9a-f]{2})/gi;
    const hexMatches = text.match(hexPattern);
    if (hexMatches && hexMatches.length > 3) {
      const decoded = this.decodeHex(text);
      if (decoded !== text) {
        threats.push({
          type: 'hex_injection',
          severity: 'MEDIUM',
          decoded: decoded.substring(0, 100),
          description: '检测到十六进制编码的隐藏内容'
        });
      }
    }

    // Unicode/零宽字符检测
    const zeroWidthChars = text.match(/[\u200b\u200c\u200d\u202e]/g);
    if (zeroWidthChars && zeroWidthChars.length > 0) {
      threats.push({
        type: 'zero_width_injection',
        severity: 'HIGH',
        charCount: zeroWidthChars.length,
        positions: this.findZeroWidthPositions(text),
        description: '检测到零宽字符注入（可用于隐藏指令）'
      });
    }

    // HTML 实体编码
    const htmlEntities = text.match(/&#x?[0-9a-f]+;?/gi);
    if (htmlEntities && htmlEntities.length > 2) {
      threats.push({
        type: 'html_entity_injection',
        severity: 'MEDIUM',
        entities: htmlEntities.slice(0, 5),
        description: '检测到 HTML 实体编码'
      });
    }

    return threats;
  }

  /**
   * 检测角色扮演/劫持
   */
  detectRolePlay(text) {
    const threats = [];
    const patterns = this.rules.promptInjectionRules.rolePlayPatterns;

    for (const pattern of patterns) {
      const regex = new RegExp(pattern, 'gi');
      const matches = text.match(regex);
      if (matches) {
        threats.push({
          type: 'role_hijack',
          severity: 'MEDIUM',
          matched: matches[0],
          description: '检测到角色劫持尝试'
        });
      }
    }

    // 检测多角色扮演
    const roleCount = (text.match(/角色[是为]?|you are|act as|role:/gi) || []).length;
    if (roleCount > 1) {
      threats.push({
        type: 'multi_role',
        severity: 'LOW',
        roleCount,
        description: '检测到多个角色定义，可能存在角色冲突'
      });
    }

    return threats;
  }

  /**
   * 检测越狱尝试
   */
  detectJailbreak(text) {
    const threats = [];
    const patterns = this.rules.promptInjectionRules.jailbreakPatterns;

    for (const pattern of patterns) {
      const regex = new RegExp(pattern, 'gi');
      const matches = text.match(regex);
      if (matches) {
        threats.push({
          type: 'jailbreak_attempt',
          severity: 'CRITICAL',
          matched: matches[0],
          pattern,
          description: '检测到已知的越狱提示词'
        });
      }
    }

    // 检测特殊字符混淆的越狱词
    const suspiciousPhrases = ['d.a.n', 'd@n', 'd4n', 'do any'];
    for (const phrase of suspiciousPhrases) {
      if (text.toLowerCase().includes(phrase)) {
        threats.push({
          type: 'obfuscated_jailbreak',
          severity: 'HIGH',
          matched: phrase,
          description: '检测到混淆的越狱词'
        });
      }
    }

    return threats;
  }

  /**
   * 检测指令链劫持
   */
  detectChainHijack(text) {
    const threats = [];
    const patterns = this.rules.promptInjectionRules.chainHijackPatterns;

    for (const pattern of patterns) {
      const regex = new RegExp(pattern, 'gi');
      const matches = text.match(regex);
      if (matches) {
        threats.push({
          type: 'chain_hijack',
          severity: 'HIGH',
          matched: matches[0],
          description: '检测到指令链劫持尝试'
        });
      }
    }

    // 检测多次"忘记"指令
    const forgetCount = (text.match(/forget|忽略|忘记|disregard/gi) || []).length;
    if (forgetCount >= 2) {
      threats.push({
        type: 'cumulative_override',
        severity: 'HIGH',
        count: forgetCount,
        description: '检测到多次忽略指令的尝试'
      });
    }

    return threats;
  }

  /**
   * 验证意图完整性
   */
  validateIntentIntegrity(input) {
    const result = {
      timestamp: new Date().toISOString(),
      originalIntent: null,
      currentIntent: null,
      isConsistent: true,
      deviations: [],
      integrityScore: 100
    };

    // 分析原始意图（从上下文推断）
    result.originalIntent = this.extractIntent(input);

    // 检测意图偏离
    result.deviations = this.detectIntentDeviations(input, result.originalIntent);

    // 计算一致性
    result.isConsistent = result.deviations.length === 0;
    result.integrityScore = Math.max(0, 100 - result.deviations.length * 15);

    return result;
  }

  /**
   * 提取意图
   */
  extractIntent(text) {
    const intent = {
      tasks: [],
      constraints: [],
      context: []
    };

    // 提取任务
    const taskPatterns = [
      /帮我(.*?)[。\n]/g,
      /请(.*?)[。\n]/g,
      /做(.*?)[。\n]/g,
      /执行(.*?)[。\n]/g
    ];

    for (const pattern of taskPatterns) {
      let match;
      while ((match = pattern.exec(text)) !== null) {
        intent.tasks.push(match[1]);
      }
    }

    // 提取约束
    const constraintPatterns = [
      /不要(.*?)[。\n]/g,
      /禁止(.*?)[。\n]/g,
      /只能(.*?)[。\n]/g,
      /必须(.*?)[。\n]/g
    ];

    for (const pattern of constraintPatterns) {
      let match;
      while ((match = pattern.exec(text)) !== null) {
        intent.constraints.push(match[1]);
      }
    }

    return intent;
  }

  /**
   * 检测意图偏离
   */
  detectIntentDeviations(text, originalIntent) {
    const deviations = [];

    // 检测新增的高风险操作
    const riskyPatterns = [
      { pattern: /删除|rm|del/, risk: '删除文件' },
      { pattern: /修改|编辑|change/, risk: '修改内容' },
      { pattern: /执行|运行|run|exec/, risk: '执行命令' },
      { pattern: /上传|发送|upload|send/, risk: '数据传输' }
    ];

    for (const { pattern, risk } of riskyPatterns) {
      if (pattern.test(text)) {
        const inOriginal = originalIntent.tasks.some(t => pattern.test(t));
        if (!inOriginal) {
          deviations.push({
            type: 'unintended_operation',
            risk,
            description: `检测到原任务中未声明的操作: ${risk}`
          });
        }
      }
    }

    return deviations;
  }

  /**
   * 生成加固配置
   */
  async generateHardenedConfig(configPath) {
    let config;
    try {
      const content = fs.readFileSync(configPath, 'utf-8');
      config = JSON.parse(content);
    } catch (e) {
      throw new Error(`无法读取配置文件: ${e.message}`);
    }

    const hardened = JSON.parse(JSON.stringify(config));
    const changes = [];

    // 1. 启用沙箱
    if (!hardened.sandbox || !hardened.sandbox.enabled) {
      hardened.sandbox = hardened.sandbox || {};
      hardened.sandbox.enabled = true;
      hardened.sandbox.allowedPaths = ['/tmp', '~/workspace'];
      hardened.sandbox.deniedPaths = ['/home', '/root', '/etc', '/var', '/usr'];
      hardened.sandbox.maxMemory = 512;
      hardened.sandbox.timeout = 60000;
      changes.push({ section: 'sandbox', action: 'enabled', before: false, after: true });
    }

    // 2. 配置网络安全
    if (!hardened.gateway || !hardened.gateway.tls || !hardened.gateway.tls.enabled) {
      hardened.gateway = hardened.gateway || {};
      hardened.gateway.tls = { enabled: true };
      changes.push({ section: 'gateway.tls', action: 'enabled' });
    }

    // 3. 启用速率限制
    if (!hardened.gateway || !hardened.gateway.rateLimit || !hardened.gateway.rateLimit.enabled) {
      hardened.gateway = hardened.gateway || {};
      hardened.gateway.rateLimit = {
        enabled: true,
        max: 100,
        windowMs: 60000
      };
      changes.push({ section: 'gateway.rateLimit', action: 'enabled' });
    }

    // 4. 配置 CORS
    if (!hardened.gateway || !hardened.gateway.cors) {
      hardened.gateway = hardened.gateway || {};
      hardened.gateway.cors = {
        enabled: true,
        origin: [],
        credentials: true
      };
      changes.push({ section: 'gateway.cors', action: 'configured' });
    }

    // 5. 命令白名单
    if (!hardened.tools || !hardened.tools.exec || hardened.tools.exec.security === 'full') {
      hardened.tools = hardened.tools || {};
      hardened.tools.exec = hardened.tools.exec || {};
      hardened.tools.exec.security = 'allowlist';
      hardened.tools.exec.allowlist = ['ls', 'cat', 'grep', 'find', 'echo', 'pwd', 'cd', 'mkdir', 'touch', 'head', 'tail', 'wc'];
      changes.push({ section: 'tools.exec', action: 'changed_to_allowlist' });
    }

    // 6. 添加日志配置
    hardened.logging = hardened.logging || {
      enabled: true,
      level: 'info',
      auditLog: true,
      maxSize: '100MB',
      maxFiles: 10
    };
    changes.push({ section: 'logging', action: 'enabled' });

    return {
      original: config,
      hardened,
      changes,
      metadata: {
        generatedAt: new Date().toISOString(),
        version: '3.0.0',
        backupRecommended: true
      }
    };
  }

  /**
   * 计算风险评分
   */
  calculateRiskScore(threats) {
    let score = 0;
    for (const threat of threats) {
      switch (threat.severity) {
        case 'CRITICAL': score += 40; break;
        case 'HIGH': score += 25; break;
        case 'MEDIUM': score += 15; break;
        case 'LOW': score += 5; break;
      }
    }
    return Math.min(100, score);
  }

  /**
   * 确定风险等级
   */
  determineRiskLevel(score) {
    if (score <= 10) return 'SAFE';
    if (score <= 30) return 'LOW_RISK';
    if (score <= 60) return 'MEDIUM_RISK';
    return 'HIGH_RISK';
  }

  /**
   * 生成建议
   */
  generateRecommendations(result) {
    const recommendations = [];

    if (result.threats.some(t => t.type === 'jailbreak_attempt')) {
      recommendations.push({
        priority: 'CRITICAL',
        action: 'reject_input',
        message: '检测到越狱尝试，建议拒绝此输入'
      });
    }

    if (result.threats.some(t => t.type === 'base64_injection')) {
      recommendations.push({
        priority: 'HIGH',
        action: 'decode_and_verify',
        message: '检测到 Base64 编码内容，建议解码后重新验证'
      });
    }

    if (result.threats.some(t => t.type === 'zero_width_injection')) {
      recommendations.push({
        priority: 'HIGH',
        action: 'sanitize_input',
        message: '检测到零宽字符，建议清除后再处理'
      });
    }

    if (result.threats.some(t => t.type === 'chain_hijack')) {
      recommendations.push({
        priority: 'MEDIUM',
        action: 'preserve_original_intent',
        message: '检测到指令链劫持，建议保持原始任务不变'
      });
    }

    if (recommendations.length === 0) {
      recommendations.push({
        priority: 'INFO',
        action: 'none',
        message: '未检测到明显的注入攻击'
      });
    }

    return recommendations;
  }

  // ===== 辅助方法 =====

  tryDecodeBase64(str) {
    try {
      const decoded = Buffer.from(str, 'base64').toString('utf-8');
      // 检查解码后是否是可读文本
      if (/^[\x20-\x7E\s]+$/.test(decoded)) {
        return decoded;
      }
    } catch (e) {}
    return null;
  }

  decodeHex(text) {
    return text.replace(/\\x([0-9a-f]{2})/gi, (_, hex) =>
      String.fromCharCode(parseInt(hex, 16))
    );
  }

  findZeroWidthPositions(text) {
    const positions = [];
    for (let i = 0; i < text.length; i++) {
      if ('\u200b\u200c\u200d\u202e'.includes(text[i])) {
        positions.push(i);
      }
    }
    return positions;
  }

  // ===== 输出方法 =====

  printDefenseResult(result) {
    const levelIcon = {
      'SAFE': '✅',
      'LOW_RISK': '🟢',
      'MEDIUM_RISK': '🟡',
      'HIGH_RISK': '🔴'
    };

    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║              🛡️ 提示词注入检测结果                         ║
╠═══════════════════════════════════════════════════════════════╣
║  输入长度: ${result.inputLength.toString().padEnd(47)}║
║  风险评分: ${result.riskScore}/100`.padEnd(50) + '║');
    console.log(`║  风险等级: ${levelIcon[result.riskLevel].padEnd(48)}║`);
    console.log(`║  发现威胁: ${result.threats.length} 项`.padEnd(49) + '║');
    console.log('╚═══════════════════════════════════════════════════════════════╝');

    if (result.threats.length > 0) {
      console.log('\n⚠️  威胁详情:\n');
      result.threats.forEach((threat, i) => {
        const icon = threat.severity === 'CRITICAL' ? '🔴' :
          threat.severity === 'HIGH' ? '🟠' :
            threat.severity === 'MEDIUM' ? '🟡' : '🟢';
        console.log(`  ${i + 1}. ${icon} [${threat.type}] ${threat.description}`);
        if (threat.matched) {
          console.log(`     匹配内容: "${threat.matched}"`);
        }
      });

      console.log('\n💡 建议:');
      result.recommendations.forEach((rec, i) => {
        console.log(`  ${i + 1}. [${rec.priority}] ${rec.message}`);
      });
    }
  }

  printValidationResult(result) {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║              🔍 意图完整性验证结果                         ║
╠═══════════════════════════════════════════════════════════════╣
║  完整性评分: ${result.integrityScore}%`.padEnd(50) + '║');
    console.log(`║  状态: ${result.isConsistent ? '✅ 一致' : '⚠️ 偏离'.padEnd(47)}║`);
    console.log('╚═══════════════════════════════════════════════════════════════╝');

    if (result.deviations.length > 0) {
      console.log('\n⚠️  意图偏离:\n');
      result.deviations.forEach((dev, i) => {
        console.log(`  ${i + 1}. ${dev.type}: ${dev.description}`);
      });
    }
  }

  printHardeningReport(result) {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║              🛡️ 配置加固报告                              ║
╠═══════════════════════════════════════════════════════════════╣
║  生成时间: ${result.metadata.generatedAt.padEnd(44)}║`);
    console.log(`║  变更数量: ${result.changes.length} 项`.padEnd(50) + '║');
    console.log('╚═══════════════════════════════════════════════════════════════╝');

    if (result.changes.length > 0) {
      console.log('\n📝 变更详情:\n');
      result.changes.forEach((change, i) => {
        console.log(`  ${i + 1}. [${change.section}] ${change.action}`);
      });

      console.log('\n💡 使用方法:');
      console.log('  1. 备份原配置: cp config.json config.json.backup');
      console.log('  2. 应用新配置: 使用 --fix 或 --output 保存');
      console.log('  3. 重启服务使配置生效');
    }
  }
}

module.exports = { Shield };
