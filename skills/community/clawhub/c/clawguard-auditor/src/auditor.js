/**
 * ClawGuard v3 - Auditor 核心引擎
 * 包含意图偏离检测的完整审计流程
 */

const fs = require('fs');
const path = require('path');
const SASTAnalyzer = require('./sast-analyzer.js');
const IntentDriftDetector = require('./intent-drift-detector.js');
const SupplyChainAnalyzer = require('./supply-chain-analyzer.js');

class Auditor {
  constructor(options = {}) {
    this.options = {
      deep: options.deep || false,
      ...options
    };
    this.sast = new SASTAnalyzer();
    this.intentDrift = new IntentDriftDetector();
    this.supplyChain = new SupplyChainAnalyzer();
  }

  /**
   * 执行完整审计流程
   */
  async audit(skillPath) {
    const startTime = Date.now();
    const report = {
      version: '3.0.0',
      timestamp: new Date().toISOString(),
      skillPath: path.resolve(skillPath),
      findings: [],
      intentDriftReport: null,
      riskScore: 0,
      riskLevel: 'TIER_0',
      modules: {}
    };

    // 1. 收集 Skill 信息
    const skillInfo = this.collectSkillInfo(skillPath);
    report.skillInfo = skillInfo;

    // 2. SAST 静态代码分析
    console.log('  📋 执行静态代码分析...');
    const sastResults = await this.sast.analyze(skillPath, { deep: this.options.deep });
    report.modules.sast = sastResults;
    report.findings.push(...sastResults.findings);

    // 3. 意图偏离检测（v3 新增）
    console.log('  🔍 执行意图偏离检测...');
    const intentResults = this.intentDrift.detect(skillInfo);
    report.intentDriftReport = intentResults;
    report.findings.push(...this.intentResultsToFindings(intentResults));

    // 4. 供应链安全分析
    console.log('  🔗 检查供应链风险...');
    const supplyChainResults = await this.supplyChain.analyze(skillInfo);
    report.modules.supplyChain = supplyChainResults;
    report.findings.push(...supplyChainResults.findings);

    // 5. 计算风险评分
    report.riskScore = this.calculateRiskScore(report);
    report.riskLevel = this.determineRiskLevel(report.riskScore);

    // 6. 生成建议
    report.recommendations = this.generateRecommendations(report);

    report.duration = Date.now() - startTime;

    // 打印摘要
    this.printSummary(report);

    return report;
  }

  /**
   * 收集 Skill 基本信息
   */
  collectSkillInfo(skillPath) {
    const info = {
      name: path.basename(skillPath),
      path: path.resolve(skillPath),
      files: [],
      declaredCapabilities: [],
      actualCapabilities: [],
      metadata: {}
    };

    // 读取 SKILL.md
    const skillMdPath = path.join(skillPath, 'SKILL.md');
    if (fs.existsSync(skillMdPath)) {
      const content = fs.readFileSync(skillMdPath, 'utf-8');
      info.description = this.extractDescription(content);
      info.declaredCapabilities = this.extractCapabilities(content);
      info.metadata = this.parseMetadata(content);
    }

    // 扫描所有可执行文件
    this.scanExecutableFiles(skillPath, info);

    return info;
  }

  /**
   * 提取 Skill 描述
   */
  extractDescription(content) {
    const match = content.match(/^#\s+(.+)$/m);
    return match ? match[1].trim() : '未提供描述';
  }

  /**
   * 提取声明的能力
   */
  extractCapabilities(content) {
    const capabilities = [];

    // 从 description 提取
    const capPatterns = [
      /文件\s*[读写增删改]/g,
      /网络\s*请求|发送|接收/g,
      /执行\s*(系统)?命令|shell|bash/g,
      /读取?\s*环境变量/g,
      /访问?\s*(敏感|隐私)/g,
    ];

    capPatterns.forEach(pattern => {
      if (pattern.test(content)) {
        capabilities.push(pattern.source);
      }
    });

    // 从工具列表提取
    const toolSection = content.match(/##\s*(工具|tools?)[\s\S]*?(?=##|$)/i);
    if (toolSection) {
      const tools = toolSection[0].match(/-+\s*`?[\w-]+`?/g);
      if (tools) {
        capabilities.push(...tools.map(t => t.replace(/^-+/, '').trim()));
      }
    }

    return [...new Set(capabilities)];
  }

  /**
   * 解析元数据
   */
  parseMetadata(content) {
    const meta = {};
    const match = content.match(/^---\n([\s\S]*?)---/);
    if (match) {
      try {
        // 简单解析 YAML frontmatter
        match[1].split('\n').forEach(line => {
          const [key, ...valueParts] = line.split(':');
          if (key && valueParts.length) {
            meta[key.trim()] = valueParts.join(':').trim();
          }
        });
      } catch (e) {
        // 忽略解析错误
      }
    }
    return meta;
  }

  /**
   * 扫描可执行文件
   */
  scanExecutableFiles(dir, info) {
    if (!fs.existsSync(dir)) return;

    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory() && !entry.name.startsWith('.')) {
        this.scanExecutableFiles(fullPath, info);
      } else if (entry.isFile()) {
        const ext = path.extname(entry.name);
        const isScript = ['.js', '.py', '.sh', '.bash'].includes(ext);
        const isPackage = ['package.json'].includes(entry.name);

        if (isScript || isPackage) {
          info.files.push({
            path: path.relative(info.path, fullPath),
            type: ext.replace('.', '') || 'unknown',
            size: fs.statSync(fullPath).size
          });

          // 提取实际使用的 API
          if (isScript) {
            const content = fs.readFileSync(fullPath, 'utf-8');
            info.actualCapabilities.push(...this.extractAPICalls(content));
          }
        }
      }
    }
  }

  /**
   * 提取 API 调用
   */
  extractAPICalls(content) {
    const apis = [];

    const apiPatterns = [
      // 文件操作
      { pattern: /fs\.(read|write|unlink|mkdir|stat|readdir)/g, cap: 'fs_read_write' },
      { pattern: /readFile|writeFile|readdir|statSync/g, cap: 'fs_sync' },
      // 网络
      { pattern: /fetch|axios|http\.(get|post)|request/g, cap: 'network_request' },
      { pattern: /net\.(connect|createServer)/g, cap: 'network_server' },
      // 系统
      { pattern: /child_process|exec|spawn|execSync/g, cap: 'shell_execution' },
      { pattern: /process\.env|getenv/g, cap: 'env_access' },
      // 加密
      { pattern: /crypto\.|createCipher|createDecipher/g, cap: 'crypto_operation' },
    ];

    apiPatterns.forEach(({ pattern, cap }) => {
      if (pattern.test(content)) {
        apis.push(cap);
      }
    });

    return [...new Set(apis)];
  }

  /**
   * 意图偏离结果转换为 findings
   */
  intentResultsToFindings(intentResults) {
    const findings = [];

    if (intentResults.driftScore > 0.3) {
      findings.push({
        category: 'intent_drift',
        severity: intentResults.driftScore > 0.7 ? 'CRITICAL' : 'WARNING',
        title: '意图偏离检测',
        description: `Skill 声明的功能与实际行为存在偏离，偏离度: ${(intentResults.driftScore * 100).toFixed(1)}%`,
        details: {
          declared: intentResults.declaredCapabilities,
          undeclared: intentResults.undeclaredCapabilities,
          driftScore: intentResults.driftScore
        },
        recommendation: '建议仔细审查 Skill 的实际行为，确认是否与声明用途一致'
      });
    }

    (intentResults.undeclaredCapabilities || []).forEach(cap => {
      findings.push({
        category: 'intent_drift',
        severity: 'WARNING',
        title: '未声明的能力使用',
        description: `Skill 使用了未在 SKILL.md 中声明的能力: ${cap}`,
        recommendation: '建议更新 SKILL.md 补充声明该能力'
      });
    });

    return findings;
  }

  /**
   * 计算风险评分
   */
  calculateRiskScore(report) {
    let score = 0;

    // 意图偏离权重
    if (report.intentDriftReport) {
      score += report.intentDriftReport.driftScore * 40;
    }

    // SAST 发现权重
    if (report.modules.sast && report.modules.sast.findings) {
      report.modules.sast.findings.forEach(f => {
        switch (f.severity) {
          case 'CRITICAL': score += 20; break;
          case 'HIGH': score += 15; break;
          case 'MEDIUM': score += 10; break;
          case 'LOW': score += 5; break;
        }
      });
    }

    // 供应链风险权重
    if (report.modules.supplyChain && report.modules.supplyChain.hasVulnerabilities) {
      score += 30;
    }

    return Math.min(100, Math.round(score));
  }

  /**
   * 确定风险等级
   */
  determineRiskLevel(score) {
    if (score <= 10) return 'TIER_0';
    if (score <= 30) return 'TIER_1';
    if (score <= 50) return 'TIER_2';
    if (score <= 70) return 'TIER_3';
    return 'TIER_4';
  }

  /**
   * 生成建议
   */
  generateRecommendations(report) {
    const recommendations = [];

    if (report.riskScore > 70) {
      recommendations.push({
        priority: 'HIGH',
        message: '建议暂缓安装，进行深度人工审核'
      });
    }

    if (report.intentDriftReport && report.intentDriftReport.driftScore > 0.3) {
      recommendations.push({
        priority: 'MEDIUM',
        message: 'Skill 存在意图偏离，建议确认其真实用途'
      });
    }

    if (report.modules.sast && report.modules.sast.findings && report.modules.sast.findings.some(f => f.severity === 'CRITICAL')) {
      recommendations.push({
        priority: 'HIGH',
        message: '发现严重安全问题，建议修复后再安装'
      });
    }

    return recommendations;
  }

  /**
   * 打印摘要
   */
  printSummary(report) {
    const riskLabel = {
      'TIER_0': '🟢 安全',
      'TIER_1': '🟢 低风险',
      'TIER_2': '🟡 中风险',
      'TIER_3': '🔴 高风险',
      'TIER_4': '🔴 严重风险'
    };

    console.log('╔═══════════════════════════════════════════════════════════╗');
    console.log('║                    📊 审计摘要                            ║');
    console.log('╠═══════════════════════════════════════════════════════════╣');
    console.log(`║  Skill: ${report.skillInfo.name.padEnd(48)}║`);
    console.log(`║  风险评分: ${report.riskScore}/100`.padEnd(50) + '║');
    console.log(`║  风险等级: ${riskLabel[report.riskLevel].padEnd(47)}║`);
    console.log(`║  意图偏离: ${((report.intentDriftReport && report.intentDriftReport.driftScore) * 100 || 0).toFixed(1)}%`.padEnd(49) + '║');
    console.log(`║  发现问题: ${report.findings.length} 项`.padEnd(49) + '║');
    console.log(`║  耗时: ${report.duration}ms`.padEnd(50) + '║');
    console.log('╚═══════════════════════════════════════════════════════════╝');

    // 打印建议
    if (report.recommendations.length > 0) {
      console.log('\n📋 建议:');
      report.recommendations.forEach((rec, i) => {
        console.log(`  ${i + 1}. [${rec.priority}] ${rec.message}`);
      });
    }
  }
}

module.exports = { Auditor };
