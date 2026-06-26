/**
 * ClawGuard v3 - 意图偏离检测器 (Intent Drift Detector)
 * 核心功能：检测 Skill 声明的能力与实际行为是否一致
 */

class IntentDriftDetector {
  constructor() {
    // 声明能力与实际能力的映射关系
    this.capabilityMapping = {
      // 声明 -> 对应的 API 调用
      '文件读取': ['fs.readFile', 'fs.readFileSync', 'readFile', 'readFileSync', 'readdir', 'readdirSync', 'fs.stat'],
      '文件写入': ['fs.writeFile', 'fs.writeFileSync', 'appendFile', 'writeFile', 'createWriteStream'],
      '文件删除': ['fs.unlink', 'unlink', 'rmdir', 'fs.rmdir', 'rm', 'del'],
      '命令执行': ['child_process.exec', 'exec', 'spawn', 'execSync', 'execFile', 'system', 'shell'],
      '网络请求': ['fetch', 'axios', 'http.get', 'http.post', 'request', 'net.http', 'urllib.request'],
      '环境变量': ['process.env', 'getenv', 'os.environ', 'env.get'],
      '加密操作': ['crypto', 'createCipher', 'createDecipher', 'encrypt', 'decrypt', 'aes', 'rsa'],
      '数据库': ['mysql', 'postgres', 'mongodb', 'redis', 'query', 'connect', 'connection.query'],
      '进程管理': ['process.kill', 'kill', 'child_process', 'spawn', 'fork'],
      '网络服务': ['net.createServer', 'http.createServer', 'listen', 'Server'],
    };

    // 正常偏差阈值
    this.driftThreshold = {
      low: 0.2,      // < 20% 偏离 = 安全
      medium: 0.5,   // 20-50% = 需关注
      high: 0.7,    // 50-70% = 高危
      critical: 1.0  // > 70% = 严重偏离
    };
  }

  /**
   * 执行意图偏离检测
   * @param {Object} skillInfo - Skill 信息
   * @returns {Object} 检测报告
   */
  detect(skillInfo) {
    const report = {
      detectedAt: new Date().toISOString(),
      skillName: skillInfo.name,
      declaredCapabilities: skillInfo.declaredCapabilities || [],
      actualCapabilities: skillInfo.actualCapabilities || [],
      analysis: {},
      driftScore: 0,
      driftLevel: 'SAFE',
      undeclaredCapabilities: [],
      unusedCapabilities: [],
      concerns: [],
      recommendations: []
    };

    // 1. 分析声明的能力
    report.declaredAnalysis = this.analyzeDeclaredCapabilities(report.declaredCapabilities);

    // 2. 分析实际使用的 API
    report.actualAnalysis = this.analyzeActualCapabilities(report.actualCapabilities);

    // 3. 检测未声明的能力
    report.undeclaredCapabilities = this.detectUndeclaredCapabilities(
      report.declaredAnalysis,
      report.actualAnalysis
    );

    // 4. 检测声明但未使用的功能
    report.unusedCapabilities = this.detectUnusedCapabilities(
      report.declaredAnalysis,
      report.actualAnalysis
    );

    // 5. 计算偏离分数
    report.driftScore = this.calculateDriftScore(report);

    // 6. 确定偏离等级
    report.driftLevel = this.determineDriftLevel(report.driftScore);

    // 7. 生成警告
    report.concerns = this.generateConcerns(report);

    // 8. 生成建议
    report.recommendations = this.generateRecommendations(report);

    return report;
  }

  /**
   * 分析声明的能力
   */
  analyzeDeclaredCapabilities(declared) {
    const analysis = {
      capabilities: [],
      riskLevel: 'LOW',
      reasons: []
    };

    declared.forEach(cap => {
      const cap_lower = cap.toLowerCase();

      // 高风险能力
      if (cap_lower.includes('执行') && (cap_lower.includes('命令') || cap_lower.includes('shell'))) {
        analysis.capabilities.push({ name: cap, risk: 'HIGH', type: 'execution' });
        analysis.reasons.push('声明了系统命令执行能力');
      } else if (cap_lower.includes('文件') && cap_lower.includes('删')) {
        analysis.capabilities.push({ name: cap, risk: 'HIGH', type: 'destructive' });
        analysis.reasons.push('声明了文件删除能力');
      } else if (cap_lower.includes('网络') || cap_lower.includes('发送') || cap_lower.includes('请求')) {
        analysis.capabilities.push({ name: cap, risk: 'MEDIUM', type: 'network' });
        analysis.reasons.push('声明了网络访问能力');
      } else if (cap_lower.includes('环境变量') || cap_lower.includes('密钥')) {
        analysis.capabilities.push({ name: cap, risk: 'HIGH', type: 'credentials' });
        analysis.reasons.push('声明了凭证访问能力');
      } else {
        analysis.capabilities.push({ name: cap, risk: 'LOW', type: 'normal' });
      }
    });

    // 确定整体风险等级
    if (analysis.capabilities.some(c => c.risk === 'HIGH')) {
      analysis.riskLevel = 'HIGH';
    } else if (analysis.capabilities.some(c => c.risk === 'MEDIUM')) {
      analysis.riskLevel = 'MEDIUM';
    }

    return analysis;
  }

  /**
   * 分析实际使用的 API
   */
  analyzeActualCapabilities(actual) {
    const analysis = {
      capabilities: [],
      riskLevel: 'LOW',
      reasons: []
    };

    const apiRiskMap = {
      'shell_execution': { risk: 'HIGH', reason: '执行系统命令' },
      'fs_read_write': { risk: 'MEDIUM', reason: '读写文件系统' },
      'fs_sync': { risk: 'MEDIUM', reason: '同步文件系统操作' },
      'network_request': { risk: 'MEDIUM', reason: '发起网络请求' },
      'network_server': { risk: 'HIGH', reason: '创建网络服务' },
      'env_access': { risk: 'HIGH', reason: '访问环境变量' },
      'crypto_operation': { risk: 'MEDIUM', reason: '加密操作' }
    };

    actual.forEach(api => {
      const info = apiRiskMap[api] || { risk: 'LOW', reason: '其他操作' };
      analysis.capabilities.push({ name: api, risk: info.risk, type: api });
      if (!analysis.reasons.includes(info.reason)) {
        analysis.reasons.push(info.reason);
      }
    });

    if (analysis.capabilities.some(c => c.risk === 'HIGH')) {
      analysis.riskLevel = 'HIGH';
    } else if (analysis.capabilities.some(c => c.risk === 'MEDIUM')) {
      analysis.riskLevel = 'MEDIUM';
    }

    return analysis;
  }

  /**
   * 检测未声明的能力
   */
  detectUndeclaredCapabilities(declaredAnalysis, actualAnalysis) {
    const undeclared = [];

    // 声明的能力类型
    const declaredTypes = declaredAnalysis.capabilities.map(c => c.type);
    const declaredRisks = declaredAnalysis.capabilities.map(c => c.risk);

    // 检查实际使用但未声明的高风险能力
    const highRiskAPIs = {
      'shell_execution': '系统命令执行',
      'env_access': '环境变量访问',
      'network_server': '网络服务创建',
      'crypto_operation': '加密操作'
    };

    actualAnalysis.capabilities.forEach(api => {
      if (api.risk === 'HIGH' || api.risk === 'MEDIUM') {
        const apiName = highRiskAPIs[api.name] || api.name;

        // 检查是否在声明中
        const isDeclared = declaredTypes.includes(api.type) ||
          declaredAnalysis.reasons.some(r => r.includes(apiName));

        if (!isDeclared) {
          undeclared.push({
            capability: api.name,
            displayName: apiName,
            risk: api.risk,
            severity: api.risk === 'HIGH' ? 'CRITICAL' : 'WARNING'
          });
        }
      }
    });

    return undeclared;
  }

  /**
   * 检测声明但未使用的功能
   */
  detectUnusedCapabilities(declaredAnalysis, actualAnalysis) {
    const unused = [];

    // 简化逻辑：如果声明了高风险能力但代码中未使用
    declaredAnalysis.capabilities.forEach(cap => {
      if (cap.risk === 'HIGH') {
        const expectedAPIs = this.capabilityMapping[cap.type] || [];

        // 检查是否有对应的 API 调用
        const hasUsage = actualAnalysis.capabilities.some(a =>
          expectedAPIs.some(api => api.toLowerCase().includes(a.name.toLowerCase()))
        );

        if (!hasUsage && expectedAPIs.length > 0) {
          unused.push({
            capability: cap.name,
            type: cap.type,
            reason: '声明了但代码中未检测到实际使用'
          });
        }
      }
    });

    return unused;
  }

  /**
   * 计算偏离分数
   */
  calculateDriftScore(report) {
    let score = 0;

    // 未声明能力的权重（更危险）
    const undeclaredWeight = 0.5;
    score += report.undeclaredCapabilities.length * undeclaredWeight * 30;

    // 未使用声明能力的权重（较低）
    const unusedWeight = 0.1;
    score += report.unusedCapabilities.length * unusedWeight * 10;

    // 高风险未声明能力
    const highRiskUndeclared = report.undeclaredCapabilities.filter(c => c.risk === 'HIGH');
    score += highRiskUndeclared.length * 20;

    // 中风险未声明能力
    const mediumRiskUndeclared = report.undeclaredCapabilities.filter(c => c.risk === 'MEDIUM');
    score += mediumRiskUndeclared.length * 10;

    return Math.min(1, score / 100);
  }

  /**
   * 确定偏离等级
   */
  determineDriftLevel(score) {
    if (score <= this.driftThreshold.low) return 'SAFE';
    if (score <= this.driftThreshold.medium) return 'CAUTION';
    if (score <= this.driftThreshold.high) return 'WARNING';
    return 'CRITICAL';
  }

  /**
   * 生成警告
   */
  generateConcerns(report) {
    const concerns = [];

    // 未声明的高风险能力
    const highRisk = report.undeclaredCapabilities.filter(c => c.severity === 'CRITICAL');
    if (highRisk.length > 0) {
      concerns.push({
        level: 'CRITICAL',
        message: `发现 ${highRisk.length} 项未声明的高风险能力: ${highRisk.map(c => c.displayName).join(', ')}`
      });
    }

    // 偏离分数过高
    if (report.driftScore > 0.5) {
      concerns.push({
        level: 'WARNING',
        message: `意图偏离度达到 ${(report.driftScore * 100).toFixed(1)}%，实际行为与声明用途存在显著差异`
      });
    }

    // 声明但未使用
    if (report.unusedCapabilities.length > 0) {
      concerns.push({
        level: 'INFO',
        message: `声明了 ${report.unusedCapabilities.length} 项能力但代码中未使用，可能存在功能过载`
      });
    }

    return concerns;
  }

  /**
   * 生成建议
   */
  generateRecommendations(report) {
    const recommendations = [];

    if (report.undeclaredCapabilities.length > 0) {
      recommendations.push({
        priority: 'HIGH',
        action: 'update_declaration',
        message: '建议更新 SKILL.md 补充声明以下能力: ' +
          report.undeclaredCapabilities.map(c => c.displayName).join(', ')
      });
    }

    if (report.driftScore > 0.5) {
      recommendations.push({
        priority: 'HIGH',
        action: 'review_code',
        message: '建议人工审核 Skill 代码，确认实际功能是否与声明用途一致'
      });
    }

    if (report.undeclaredCapabilities.some(c => c.risk === 'HIGH')) {
      recommendations.push({
        priority: 'CRITICAL',
        action: 'security_review',
        message: '发现高风险未声明能力，建议进行完整的安全审计后再决定是否安装'
      });
    }

    if (recommendations.length === 0) {
      recommendations.push({
        priority: 'INFO',
        action: 'none',
        message: '未发现明显的意图偏离迹象'
      });
    }

    return recommendations;
  }
}

module.exports = IntentDriftDetector;
