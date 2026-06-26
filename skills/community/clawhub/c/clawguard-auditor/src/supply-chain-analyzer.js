/**
 * ClawGuard v3 - 供应链分析器
 * CVE 漏洞检测、域名仿冒检测
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

class SupplyChainAnalyzer {
  constructor() {
    // 常见的域名仿冒模式
    this.typosquattingPatterns = [
      { typo: 'l', replacement: '1', examples: ['1l', 'il'] },
      { typo: 'o', replacement: '0', examples: ['0o', 'o0'] },
      { typo: 'rn', replacement: 'm', examples: ['rnm'] },
      { typo: 's', replacement: '5', examples: ['5', 's'] }
    ];

    // 高风险域名列表（示例）
    this.knownMaliciousDomains = [
      'npm.malicious-package.com',
      'registry.npmjs.su',
      'pypi.malicious.com'
    ];
  }

  /**
   * 分析供应链风险
   */
  async analyze(skillInfo) {
    const results = {
      findings: [],
      hasVulnerabilities: false,
      hasTyposquatting: false,
      packageAnalysis: null,
      versionAnalysis: null
    };

    // 1. 检查 package.json（如果有）
    const pkgPath = path.join(skillInfo.path, 'package.json');
    if (fs.existsSync(pkgPath)) {
      try {
        const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));
        results.packageAnalysis = await this.analyzeDependencies(pkg);

        if (results.packageAnalysis.hasRisks) {
          results.hasVulnerabilities = true;
          results.findings.push(...results.packageAnalysis.findings);
        }
      } catch (e) {
        results.findings.push({
          category: 'supply_chain',
          severity: 'INFO',
          title: '依赖分析跳过',
          description: `无法解析 package.json: ${e.message}`
        });
      }
    }

    // 2. 检查 Skill 名称域名仿冒
    if (skillInfo.name) {
      const typosquattingResult = this.checkTyposquatting(skillInfo.name);
      if (typosquattingResult.isSuspicious) {
        results.hasTyposquatting = true;
        results.findings.push({
          category: 'supply_chain',
          severity: 'CRITICAL',
          title: '可能的域名仿冒',
          description: `Skill 名称 "${skillInfo.name}" 可能存在域名仿冒风险`,
          details: typosquattingResult.details,
          recommendation: '建议从官方渠道验证 Skill 的真实性'
        });
      }
    }

    // 3. 检查版本号
    if (skillInfo.metadata && skillInfo.metadata.version) {
      results.versionAnalysis = this.checkVersion(skillInfo.metadata.version);
      if (!results.versionAnalysis.isLatest) {
        results.findings.push({
          category: 'supply_chain',
          severity: 'WARNING',
          title: '版本不是最新',
          description: `当前版本 ${skillInfo.metadata.version}，建议检查是否有更新`,
          recommendation: '建议升级到最新版本以获得安全修复'
        });
      }
    }

    return results;
  }

  /**
   * 分析依赖
   */
  async analyzeDependencies(pkg) {
    const results = {
      dependencies: [],
      devDependencies: [],
      findings: [],
      hasRisks: false,
      riskSummary: { critical: 0, high: 0, medium: 0 }
    };

    // 分析 dependencies
    if (pkg.dependencies) {
      for (const [name, version] of Object.entries(pkg.dependencies)) {
        const analysis = this.analyzeDependency(name, version);
        results.dependencies.push(analysis);

        if (analysis.isRisky) {
          results.hasRisks = true;
          results.riskSummary[analysis.severity]++;
          results.findings.push({
            category: 'supply_chain',
            severity: analysis.severity === 'CRITICAL' ? 'CRITICAL' : 'HIGH',
            title: `依赖风险: ${name}`,
            description: analysis.reason,
            recommendation: `考虑升级到安全版本或使用替代方案`
          });
        }
      }
    }

    // 分析 devDependencies
    if (pkg.devDependencies) {
      for (const [name, version] of Object.entries(pkg.devDependencies)) {
        const analysis = this.analyzeDependency(name, version);
        results.devDependencies.push(analysis);
      }
    }

    return results;
  }

  /**
   * 分析单个依赖
   */
  analyzeDependency(name, version) {
    const result = {
      name,
      version,
      isRisky: false,
      severity: 'LOW',
      reason: ''
    };

    // 检查是否包含 @
    if (name.startsWith('@')) {
      result.isRisky = true;
      result.severity = 'MEDIUM';
      result.reason = '使用了组织作用域包';
    }

    // 检查版本是否为空或 *
    if (!version || version === '*' || version === 'latest') {
      result.isRisky = true;
      result.severity = 'MEDIUM';
      result.reason = result.reason || '依赖版本未锁定';
    }

    // 检查可疑的包名
    const suspiciousPatterns = [
      /^[a-z]+-[a-z]+-[a-z]+$/i,  // 格式: word-word-word
      /^(eval|exec|system|run|test)-/i,  // 可疑前缀
      /-(eval|exec|system|run|test)$/i   // 可疑后缀
    ];

    for (const pattern of suspiciousPatterns) {
      if (pattern.test(name)) {
        result.isRisky = true;
        result.severity = 'HIGH';
        result.reason = '包名符合可疑模式';
        break;
      }
    }

    return result;
  }

  /**
   * 检查域名仿冒
   */
  checkTyposquatting(skillName) {
    const result = {
      isSuspicious: false,
      details: []
    };

    // 常见的目标包名
    const popularPackages = [
      'axios', 'lodash', 'express', 'react', 'vue', 'webpack',
      'babel', 'eslint', 'prettier', 'typescript', 'node-fetch',
      'moment', 'async', 'request', 'bluebird', 'chalk', 'commander'
    ];

    const nameLower = skillName.toLowerCase().replace(/^claw-/, '').replace(/^claw/, '');

    // 检查是否为流行包的变体
    for (const pkg of popularPackages) {
      const distance = this.levenshteinDistance(nameLower, pkg);

      // 1-2 个字符差异视为可疑
      if (distance >= 1 && distance <= 2) {
        result.isSuspicious = true;
        result.details.push({
          original: pkg,
          suspected: skillName,
          distance: distance,
          risk: '可能的域名仿冒包'
        });
      }
    }

    // 检查特殊字符混淆
    if (/[0-9]/.test(nameLower) && /[a-z]/.test(nameLower)) {
      // 数字和字母混合
      const letterCount = (nameLower.match(/[a-z]/g) || []).length;
      const digitCount = (nameLower.match(/[0-9]/g) || []).length;

      if (letterCount >= 3 && digitCount >= 1 && digitCount <= 2) {
        // 可能是用数字替换字母（如 l=1, o=0）
        for (const pkg of popularPackages) {
          if (this.levenshteinDistance(nameLower.replace(/[0-9]/g, ''), pkg) <= 1) {
            result.isSuspicious = true;
            result.details.push({
              original: pkg,
              suspected: skillName,
              risk: '可能使用数字混淆的仿冒包'
            });
          }
        }
      }
    }

    return result;
  }

  /**
   * Levenshtein 距离计算
   */
  levenshteinDistance(str1, str2) {
    const m = str1.length;
    const n = str2.length;
    const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;

    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        if (str1[i - 1] === str2[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1];
        } else {
          dp[i][j] = Math.min(
            dp[i - 1][j] + 1,    // 删除
            dp[i][j - 1] + 1,    // 插入
            dp[i - 1][j - 1] + 1 // 替换
          );
        }
      }
    }

    return dp[m][n];
  }

  /**
   * 检查版本
   */
  checkVersion(version) {
    const result = {
      version,
      isLatest: true,
      isOutdated: false,
      isPreRelease: false
    };

    // 检测预发布版本
    if (version.includes('alpha') || version.includes('beta') || version.includes('rc')) {
      result.isPreRelease = true;
      result.isLatest = false;
    }

    // 检测过期版本（x.x.x 格式的旧版本）
    const versionMatch = version.match(/^(\d+)\.(\d+)\.(\d+)/);
    if (versionMatch) {
      const [, major] = versionMatch.map(Number);
      // 如果主版本号很小，可能是旧版本
      if (major < 1) {
        result.isOutdated = true;
        result.isLatest = false;
      }
    }

    return result;
  }
}

module.exports = SupplyChainAnalyzer;
