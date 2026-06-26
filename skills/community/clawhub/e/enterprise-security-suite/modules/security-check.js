/**
 * 技能安装安检模块
 */

const RISK_LEVELS = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high'
};

const WHITELIST = ['github.com/openclaw'];

function checkSource(skillInfo) {
  const { author, repository } = skillInfo;
  
  if (WHITELIST.some(url => repository && repository.includes(url))) {
    return {
      verified: true,
      risk: RISK_LEVELS.LOW,
      message: '官方技能，来源可信'
    };
  }
  
  if (!author || author === 'unknown') {
    return {
      verified: false,
      risk: RISK_LEVELS.HIGH,
      message: '作者未知，来源不明'
    };
  }
  
  return {
    verified: false,
    risk: RISK_LEVELS.MEDIUM,
    message: '社区技能，需要进一步检查'
  };
}

function checkPermissions(permissions) {
  if (!permissions || permissions.length === 0) {
    return {
      risk: RISK_LEVELS.LOW,
      message: '无特殊权限要求'
    };
  }
  
  const dangerousPermissions = ['exec', 'shell', 'system', 'write_all', 'delete_all'];
  const hasDangerous = permissions.some(p => dangerousPermissions.includes(p.toLowerCase()));
  
  if (hasDangerous) {
    return {
      risk: RISK_LEVELS.HIGH,
      message: '包含高危权限：' + permissions.filter(p => dangerousPermissions.includes(p.toLowerCase())).join(', ')
    };
  }
  
  return {
    risk: RISK_LEVELS.MEDIUM,
    message: '包含普通权限'
  };
}

function checkDependencies(dependencies) {
  if (!dependencies || dependencies.length === 0) {
    return {
      risk: RISK_LEVELS.LOW,
      message: '无外部依赖'
    };
  }
  
  const suspiciousPackages = ['eval', 'exec', 'shell', 'child_process'];
  const hasSuspicious = dependencies.some(d => suspiciousPackages.some(s => d.toLowerCase().includes(s)));
  
  if (hasSuspicious) {
    return {
      risk: RISK_LEVELS.MEDIUM,
      message: '包含可疑依赖，建议审查'
    };
  }
  
  return {
    risk: RISK_LEVELS.LOW,
    message: '依赖正常'
  };
}

async function securityCheck(options) {
  const { skillName, author, repository, permissions, dependencies } = options;
  
  const results = {
    skillName,
    author,
    repository,
    checks: {},
    overallRisk: RISK_LEVELS.LOW,
    recommendations: []
  };
  
  results.checks.source = checkSource({ author, repository });
  results.checks.permissions = checkPermissions(permissions);
  results.checks.dependencies = checkDependencies(dependencies);
  
  const risks = Object.values(results.checks).map(c => c.risk);
  
  if (risks.includes(RISK_LEVELS.HIGH)) {
    results.overallRisk = RISK_LEVELS.HIGH;
    results.recommendations.push('❌ 高风险技能，建议拒绝安装');
  } else if (risks.includes(RISK_LEVELS.MEDIUM)) {
    results.overallRisk = RISK_LEVELS.MEDIUM;
    results.recommendations.push('⚠️ 中风险技能，请仔细阅读说明后确认');
  } else {
    results.overallRisk = RISK_LEVELS.LOW;
    results.recommendations.push('✅ 低风险技能，可以安装');
  }
  
  return results;
}

function generateReport(checkResult) {
  let report = `🛡️ **技能安装安全检查报告**\n\n`;
  report += `**技能名称**: ${checkResult.skillName}\n`;
  report += `**作者**: ${checkResult.author}\n`;
  if (checkResult.repository) report += `**仓库**: ${checkResult.repository}\n`;
  report += `\n---\n\n### 检查项\n\n`;
  
  const source = checkResult.checks.source;
  report += `**1. 来源验证**: ${source.verified ? '✅' : '⚠️'} ${source.message}\n`;
  
  const permissions = checkResult.checks.permissions;
  report += `**2. 权限评估**: ${permissions.message}\n`;
  
  const dependencies = checkResult.checks.dependencies;
  report += `**3. 依赖检查**: ${dependencies.message}\n`;
  
  report += `\n---\n\n### 综合风险等级\n\n`;
  
  const riskEmoji = {
    [RISK_LEVELS.LOW]: '🔵',
    [RISK_LEVELS.MEDIUM]: '🟡',
    [RISK_LEVELS.HIGH]: '🔴'
  };
  
  report += `${riskEmoji[checkResult.overallRisk]} **${checkResult.overallRisk.toUpperCase()}**\n\n`;
  report += `### 建议\n\n`;
  checkResult.recommendations.forEach(rec => report += `- ${rec}\n`);
  
  return report;
}

module.exports = {
  securityCheck,
  generateReport,
  checkSource,
  checkPermissions,
  checkDependencies,
  RISK_LEVELS,
  WHITELIST
};
