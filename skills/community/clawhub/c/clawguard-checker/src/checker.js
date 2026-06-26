/**
 * ClawGuard v3 - Checker 核心引擎
 * 配置检查 + 智能加固建议
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

/**
 * Helper function to safely access nested object properties
 * Compatible with older Node.js versions (pre-14)
 */
function getNestedValue(obj, ...keys) {
  return keys.reduce((o, k) => (o && o[k] !== undefined ? o[k] : undefined), obj);
}

class Checker {
  constructor(options = {}) {
    this.options = {
      deep: options.deep || false,
      ...options
    };
    this.rules = this.loadRules();
  }

  /**
   * 加载检查规则
   */
  loadRules() {
    return {
      // ===== 配置检查规则 =====
      configRules: [
        {
          id: 'CFG001',
          check: (config) => (getNestedValue(config, 'gateway', 'bind') && getNestedValue(config, 'gateway', 'bind').includes('0.0.0.0')) || getNestedValue(config, 'gateway', 'bind') === '*',
          severity: 3,
          title: 'Gateway 绑定到所有网络接口',
          description: 'OpenClaw 网关配置为监听所有网络接口，使实例暴露在网络中',
          impact: '外部网络可直接访问你的 OpenClaw',
          risk: 'CRITICAL'
        },
        {
          id: 'CFG002',
          check: (config) => !getNestedValue(config, 'gateway', 'auth', 'mode') || getNestedValue(config, 'gateway', 'auth', 'mode') === 'none',
          severity: 3,
          title: 'Gateway 未启用认证',
          description: 'OpenClaw 网关未配置身份认证',
          impact: '任何人都可以连接你的 OpenClaw',
          risk: 'CRITICAL'
        },
        {
          id: 'CFG003',
          check: (config) => getNestedValue(config, 'tools', 'exec', 'security') === 'full',
          severity: 3,
          title: '允许执行任意 Shell 命令',
          description: 'tools.exec.security 配置为 full，允许执行所有 Shell 命令',
          impact: '攻击者可执行任意系统命令',
          risk: 'CRITICAL'
        },
        {
          id: 'CFG004',
          check: (config) => getNestedValue(config, 'tools', 'exec', 'security') === 'deny',
          severity: 1,
          title: '禁止执行所有 Shell 命令',
          description: 'tools.exec.security 配置为 deny，禁止执行所有系统命令',
          impact: '部分功能可能无法使用',
          risk: 'INFO'
        },
        {
          id: 'CFG005',
          check: (config) => !getNestedValue(config, 'sandbox', 'enabled') || getNestedValue(config, 'sandbox', 'enabled') === false,
          severity: 2,
          title: '沙箱已禁用',
          description: '沙箱未启用，无法限制文件访问范围',
          impact: 'Skill 可能访问系统敏感文件',
          risk: 'WARNING'
        },
        {
          id: 'CFG006',
          check: (config) => getNestedValue(config, 'gateway', 'auth', 'mode') === 'token' && !getNestedValue(config, 'gateway', 'auth', 'token'),
          severity: 2,
          title: 'Token 认证未设置 Token',
          description: '认证模式为 token 但未设置实际的 token 值',
          impact: '认证配置不完整',
          risk: 'WARNING'
        },
        {
          id: 'CFG007',
          check: (config) => getNestedValue(config, 'gateway', 'port') && getNestedValue(config, 'gateway', 'port') < 1024,
          severity: 1,
          title: 'Gateway 使用特权端口',
          description: 'Gateway 端口号小于 1024，需要 root 权限',
          impact: '可能与其他服务冲突',
          risk: 'INFO'
        },
        {
          id: 'CFG008',
          check: (config) => !getNestedValue(config, 'gateway', 'tls', 'enabled') && getNestedValue(config, 'gateway', 'tls') === false,
          severity: 2,
          title: 'Gateway 未启用 TLS',
          description: 'Gateway 未配置 TLS 加密',
          impact: '通信内容可能被窃听',
          risk: 'WARNING'
        },
        {
          id: 'CFG009',
          check: (config) => getNestedValue(config, 'tools', 'exec', 'allowlist') && getNestedValue(config, 'tools', 'exec', 'allowlist').length === 0,
          severity: 2,
          title: '命令白名单为空',
          description: '配置了 allowlist 模式但未添加任何允许的命令',
          impact: '将无法执行任何系统命令',
          risk: 'WARNING'
        },
        {
          id: 'CFG010',
          check: (config) => getNestedValue(config, 'sandbox', 'maxMemory') && getNestedValue(config, 'sandbox', 'maxMemory') < 128,
          severity: 1,
          title: '沙箱内存限制过低',
          description: '沙箱内存限制小于 128MB',
          impact: '可能影响正常运行',
          risk: 'INFO'
        }
      ],

      // ===== 凭证检查规则 =====
      credentialRules: [
        {
          id: 'CRED001',
          check: (config) => getNestedValue(config, 'gateway', 'auth', 'token') && getNestedValue(config, 'gateway', 'auth', 'token').length < 32,
          severity: 2,
          title: 'Token 强度不足',
          description: 'Gateway token 长度小于 32 字符',
          impact: 'Token 可能被暴力破解',
          risk: 'WARNING'
        },
        {
          id: 'CRED002',
          check: (config) => getNestedValue(config, 'gateway', 'auth', 'password') && getNestedValue(config, 'gateway', 'auth', 'password').length < 12,
          severity: 2,
          title: '密码强度不足',
          description: 'Gateway 密码长度小于 12 字符',
          impact: '密码可能被暴力破解',
          risk: 'WARNING'
        },
        {
          id: 'CRED003',
          check: (config) => getNestedValue(config, 'gateway', 'auth', 'password') === 'password' ||
                            getNestedValue(config, 'gateway', 'auth', 'token') === 'token' ||
                            getNestedValue(config, 'gateway', 'auth', 'password') === 'admin',
          severity: 3,
          title: '使用默认/弱密码',
          description: '检测到使用常见弱密码',
          impact: '极易被破解',
          risk: 'CRITICAL'
        }
      ],

      // ===== 网络检查规则 =====
      networkRules: [
        {
          id: 'NET001',
          check: (config) => getNestedValue(config, 'gateway', 'cors', 'enabled') && getNestedValue(config, 'gateway', 'cors', 'origin') === '*',
          severity: 2,
          title: 'CORS 允许所有来源',
          description: 'Gateway CORS 配置允许所有来源访问',
          impact: '可能被跨站请求利用',
          risk: 'WARNING'
        },
        {
          id: 'NET002',
          check: (config) => getNestedValue(config, 'gateway', 'rateLimit', 'enabled') === false,
          severity: 1,
          title: '未启用速率限制',
          description: 'Gateway 未配置速率限制',
          impact: '可能遭受暴力破解或 DoS 攻击',
          risk: 'INFO'
        },
        {
          id: 'NET003',
          check: (config) => getNestedValue(config, 'gateway', 'rateLimit', 'max') && getNestedValue(config, 'gateway', 'rateLimit', 'max') < 10,
          severity: 1,
          title: '速率限制过于严格',
          description: '速率限制值过小，可能影响正常使用',
          impact: '正常请求可能被限制',
          risk: 'INFO'
        }
      ],

      // ===== 沙箱检查规则 =====
      sandboxRules: [
        {
          id: 'SBOX001',
          check: (config) => getNestedValue(config, 'sandbox', 'enabled') && !(getNestedValue(config, 'sandbox', 'allowedPaths') && getNestedValue(config, 'sandbox', 'allowedPaths').length),
          severity: 2,
          title: '沙箱未配置允许路径',
          description: '沙箱已启用但未配置 allowedPaths',
          impact: '可能无法限制文件访问范围',
          risk: 'WARNING'
        },
        {
          id: 'SBOX002',
          check: (config) => getNestedValue(config, 'sandbox', 'deniedPaths') && getNestedValue(config, 'sandbox', 'deniedPaths').length > 0 &&
                            !(getNestedValue(config, 'sandbox', 'deniedPaths') && getNestedValue(config, 'sandbox', 'deniedPaths').some(p => p.includes('/home'))),
          severity: 1,
          title: '沙箱未禁止访问用户目录',
          description: '沙箱配置了禁止路径但未包含 /home',
          impact: '可能访问用户敏感文件',
          risk: 'INFO'
        },
        {
          id: 'SBOX003',
          check: (config) => !getNestedValue(config, 'sandbox', 'timeout') || getNestedValue(config, 'sandbox', 'timeout') > 300000,
          severity: 1,
          title: '沙箱超时时间过长',
          description: '沙箱执行超时设置大于 5 分钟',
          impact: '可能占用过多系统资源',
          risk: 'INFO'
        }
      ]
    };
  }

  /**
   * 执行配置检查
   */
  async check(configPath) {
    const startTime = Date.now();
    const report = {
      version: '3.0.0',
      timestamp: new Date().toISOString(),
      configPath: path.resolve(configPath),
      findings: [],
      riskScore: 0,
      maxSeverity: 0,
      sections: {},
      hardeningAdvice: []
    };

    // 1. 读取配置
    console.log('  📋 读取配置文件...');
    const config = this.loadConfig(configPath);
    if (!config) {
      report.findings.push({
        id: 'CFG000',
        severity: 3,
        title: '配置文件读取失败',
        description: `无法读取配置文件: ${configPath}`,
        risk: 'CRITICAL'
      });
      report.maxSeverity = 3;
      return report;
    }
    report.config = config;

    // 2. 执行所有检查
    console.log('  🔍 执行配置检查...');
    const allRules = [
      ...this.rules.configRules,
      ...this.rules.credentialRules,
      ...this.rules.networkRules,
      ...this.rules.sandboxRules
    ];

    for (const rule of allRules) {
      try {
        if (rule.check(config)) {
          const finding = {
            id: rule.id,
            severity: rule.severity,
            title: rule.title,
            description: rule.description,
            impact: rule.impact,
            risk: rule.risk,
            recommendation: this.getRecommendation(rule.id, config)
          };
          report.findings.push(finding);
          report.maxSeverity = Math.max(report.maxSeverity, rule.severity);
        }
      } catch (e) {
        // 忽略检查错误
      }
    }

    // 3. 深度检查（如果启用）
    if (this.options.deep) {
      console.log('  🔬 执行深度检查...');
      const deepFindings = await this.deepCheck(config);
      report.findings.push(...deepFindings);
      report.sections = { deepCheck: deepFindings };
    }

    // 4. 计算风险评分
    report.riskScore = this.calculateRiskScore(report.findings);

    // 5. 生成加固建议
    report.hardeningAdvice = this.generateHardeningAdvice(report.findings);

    report.duration = Date.now() - startTime;

    // 6. 打印摘要
    this.printSummary(report);

    return report;
  }

  /**
   * 读取配置文件
   */
  loadConfig(configPath) {
    try {
      const content = fs.readFileSync(configPath, 'utf-8');
      return JSON.parse(content);
    } catch (e) {
      return null;
    }
  }

  /**
   * 深度检查
   */
  async deepCheck(config) {
    const findings = [];

    // 检查配置文件权限
    try {
      const stat = fs.statSync(this.options.configPath);
      const mode = stat.mode & 0o777;
      if ((mode & 0o004) !== 0) {
        findings.push({
          id: 'DEEP001',
          severity: 2,
          title: '配置文件权限过于宽松',
          description: `配置文件可被其他用户读取 (权限: ${mode.toString(8)})`,
          impact: '其他用户可能读取敏感配置',
          risk: 'WARNING',
          recommendation: '执行: chmod 600 ' + this.options.configPath
        });
      }
    } catch (e) {
      // 忽略
    }

    // 检查 Token 是否可预测
    if (getNestedValue(config, 'gateway', 'auth', 'token')) {
      const token = getNestedValue(config, 'gateway', 'auth', 'token');
      const entropy = this.calculateEntropy(token);
      if (entropy < 3.5) {
        findings.push({
          id: 'DEEP002',
          severity: 2,
          title: 'Token 熵值过低',
          description: 'Token 随机性不足，可能被猜测',
          impact: 'Token 安全性不足',
          risk: 'WARNING',
          recommendation: '使用更随机的 Token (建议使用 crypto.randomBytes(32).toString("hex"))'
        });
      }
    }

    return findings;
  }

  /**
   * 计算字符串熵值
   */
  calculateEntropy(str) {
    const freq = {};
    for (const char of str) {
      freq[char] = (freq[char] || 0) + 1;
    }

    let entropy = 0;
    const len = str.length;
    for (const char in freq) {
      const p = freq[char] / len;
      entropy -= p * Math.log2(p);
    }

    return entropy;
  }

  /**
   * 获取修复建议
   */
  getRecommendation(ruleId, config) {
    const adviceMap = {
      'CFG001': '将 gateway.bind 改为 "127.0.0.1" 或使用防火墙限制来源',
      'CFG002': '启用认证: gateway.auth.mode = "token" 并设置 gateway.auth.token',
      'CFG003': '改为 allowlist 模式: tools.exec.security = "allowlist" 并添加允许的命令',
      'CFG004': '根据需要逐步添加允许的命令到 tools.exec.allowlist',
      'CFG005': '启用沙箱: sandbox.enabled = true',
      'CFG006': '设置有效的 gateway.auth.token (建议 32+ 字符)',
      'CFG007': '考虑使用非特权端口 (如 18789)',
      'CFG008': '启用 TLS: gateway.tls.enabled = true',
      'CFG009': '添加允许的命令列表: tools.exec.allowlist = ["ls", "cat", "grep", ...]',
      'CFG010': '设置合理的内存限制: sandbox.maxMemory = 256 或更高',
      'CRED001': '使用更长的 Token: crypto.randomBytes(32).toString("hex")',
      'CRED002': '使用更强的密码 (12+ 字符，包含特殊字符)',
      'CRED003': '立即修改为强密码或 Token',
      'NET001': '将 CORS origin 设置为具体的域名列表',
      'NET002': '启用速率限制: gateway.rateLimit.enabled = true',
      'NET003': '适当提高速率限制值',
      'SBOX001': '配置沙箱允许路径: sandbox.allowedPaths = ["/tmp", "~/workspace"]',
      'SBOX002': '添加用户目录到禁止列表: sandbox.deniedPaths = ["/home", "/root", "/etc"]',
      'SBOX003': '设置合理的超时时间: sandbox.timeout = 60000 (1分钟)'
    };

    return adviceMap[ruleId] || '请参考 OpenClaw 官方文档进行修复';
  }

  /**
   * 计算风险评分
   */
  calculateRiskScore(findings) {
    let score = 0;
    for (const f of findings) {
      switch (f.severity) {
        case 3: score += 30; break;
        case 2: score += 15; break;
        case 1: score += 5; break;
      }
    }
    return Math.min(100, score);
  }

  /**
   * 生成加固建议
   */
  generateHardeningAdvice(findings) {
    const advice = findings.map(f => ({
      id: f.id,
      title: f.title,
      current: f.description,
      recommended: f.recommendation,
      priority: f.severity === 3 ? 'HIGH' : f.severity === 2 ? 'MEDIUM' : 'LOW'
    }));

    return advice.sort((a, b) => {
      const priorityOrder = { HIGH: 0, MEDIUM: 1, LOW: 2 };
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    });
  }

  /**
   * 生成加固配置
   */
  generateHardenedConfig(report) {
    const original = report.config || {};
    const hardened = JSON.parse(JSON.stringify(original));

    // 应用加固建议
    for (const finding of report.findings) {
      switch (finding.id) {
        case 'CFG001':
          hardened.gateway = hardened.gateway || {};
          hardened.gateway.bind = '127.0.0.1';
          break;
        case 'CFG002':
          hardened.gateway = hardened.gateway || {};
          hardened.gateway.auth = hardened.gateway.auth || {};
          hardened.gateway.auth.mode = 'token';
          if (!hardened.gateway.auth.token) {
            hardened.gateway.auth.token = crypto.randomBytes(32).toString('hex');
          }
          break;
        case 'CFG003':
          hardened.tools = hardened.tools || {};
          hardened.tools.exec = hardened.tools.exec || {};
          hardened.tools.exec.security = 'allowlist';
          hardened.tools.exec.allowlist = hardened.tools.exec.allowlist || ['ls', 'cat', 'grep', 'find', 'echo', 'pwd', 'cd'];
          break;
        case 'CFG005':
          hardened.sandbox = hardened.sandbox || {};
          hardened.sandbox.enabled = true;
          break;
        case 'CFG008':
          hardened.gateway = hardened.gateway || {};
          hardened.gateway.tls = hardened.gateway.tls || {};
          hardened.gateway.tls.enabled = true;
          break;
        case 'NET001':
          hardened.gateway = hardened.gateway || {};
          hardened.gateway.cors = hardened.gateway.cors || {};
          hardened.gateway.cors.origin = [];
          break;
        case 'NET002':
          hardened.gateway = hardened.gateway || {};
          hardened.gateway.rateLimit = hardened.gateway.rateLimit || {};
          hardened.gateway.rateLimit.enabled = true;
          hardened.gateway.rateLimit.max = hardened.gateway.rateLimit.max || 100;
          break;
        case 'SBOX001':
          hardened.sandbox = hardened.sandbox || {};
          hardened.sandbox.allowedPaths = ['/tmp', '~/workspace'];
          break;
        case 'SBOX002':
          hardened.sandbox = hardened.sandbox || {};
          hardened.sandbox.deniedPaths = hardened.sandbox.deniedPaths || [];
          if (!hardened.sandbox.deniedPaths.includes('/home')) {
            hardened.sandbox.deniedPaths.push('/home', '/root', '/etc');
          }
          break;
      }
    }

    return hardened;
  }

  /**
   * 打印摘要
   */
  printSummary(report) {
    const severityLabels = {
      0: '✅ 安全',
      1: '🟢 提示',
      2: '🟡 警告',
      3: '🔴 严重'
    };

    console.log('╔═══════════════════════════════════════════════════════════╗');
    console.log('║                  📊 检查摘要                           ║');
    console.log('╠═══════════════════════════════════════════════════════════╣');
    console.log(`║  配置文件: ${path.basename(report.configPath).padEnd(45)}║`);
    console.log(`║  风险评分: ${report.riskScore}/100`.padEnd(50) + '║');
    console.log(`║  最高风险: ${severityLabels[report.maxSeverity].padEnd(45)}║`);
    console.log(`║  发现问题: ${report.findings.length} 项`.padEnd(49) + '║');
    console.log(`║  耗时: ${report.duration}ms`.padEnd(50) + '║');
    console.log('╚═══════════════════════════════════════════════════════════╝');

    // 打印问题列表
    if (report.findings.length > 0) {
      console.log('\n⚠️  发现问题:');
      report.findings.forEach((f, i) => {
        const icon = f.severity >= 3 ? '🔴' : f.severity >= 2 ? '🟡' : '🟢';
        console.log(`  ${i + 1}. ${icon} ${f.title}`);
        console.log(`     → ${f.impact}`);
      });

      console.log('\n💡 修复建议:');
      report.findings.forEach((f, i) => {
        console.log(`  ${i + 1}. ${f.title}: ${f.recommendation}`);
      });
    }
  }
}

module.exports = { Checker };
