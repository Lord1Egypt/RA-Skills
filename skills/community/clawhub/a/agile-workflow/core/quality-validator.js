#!/usr/bin/env node
/**
 * 质量验证系统 v6.0-Phase1
 * 
 * 核心功能:
 * 1. 质量检查（完整性/一致性/合规性/创造性）
 * 2. 质量评分（综合评分 + 等级）
 * 3. 优化建议（自动生成）
 * 4. 返工流程（自动重试）
 */

const fs = require('fs');
const path = require('path');

// ============ 配置 ============

const CONFIG = {
  workspace: '/home/ubutu/.openclaw/workspace',
  logsDir: '/home/ubutu/.openclaw/workspace/logs/quality-validator',
  reportsDir: '/home/ubutu/.openclaw/workspace/logs/quality-validator/reports',
  configFile: '/home/ubutu/.openclaw/workspace/logs/quality-validator/quality-config.json',
  
  // 质量阈值
  thresholds: {
    pass: 80,        // >= 80 分通过
    warning: 70,     // >= 70 分警告
    reject: 60       // < 60 分拒绝
  },
  
  // 权重配置
  weights: {
    completeness: 0.3,  // 完整性 30%
    consistency: 0.3,   // 一致性 30%
    compliance: 0.2,    // 合规性 20%
    creativity: 0.2     // 创造性 20%
  },
  
  // 必需字段
  requiredFields: {
    'chapter_write': ['title', 'content', 'wordCount'],
    'outline': ['plotPoints', 'characters', 'settings'],
    'character_design': ['name', 'background', 'traits'],
    'world_building': ['name', 'rules', 'geography']
  },
  
  // 自动重试
  autoRetry: {
    enabled: true,
    maxRetries: 2,
    retryThreshold: 70
  }
};

// ============ 质量验证器 ============

class QualityValidator {
  constructor() {
    this.config = this.loadConfig();
    this.ensureDirs();
  }

  ensureDirs() {
    fs.mkdirSync(CONFIG.logsDir, { recursive: true });
    fs.mkdirSync(CONFIG.reportsDir, { recursive: true });
  }

  loadConfig() {
    if (fs.existsSync(CONFIG.configFile)) {
      return JSON.parse(fs.readFileSync(CONFIG.configFile, 'utf-8'));
    }
    
    // 确保目录存在
    this.ensureDirs();
    
    // 保存默认配置
    fs.writeFileSync(CONFIG.configFile, JSON.stringify(CONFIG, null, 2));
    return CONFIG;
  }

  // ============ 核心验证方法 ============

  /**
   * 验证任务结果质量
   */
  validate(taskResult, requirements = {}) {
    console.log(`🔍 开始质量验证：${taskResult.taskName || 'Unknown'}`);

    const startTime = Date.now();

    // 1. 各项检查
    const scores = {
      completeness: this.checkCompleteness(taskResult, requirements),
      consistency: this.checkConsistency(taskResult, requirements),
      compliance: this.checkCompliance(taskResult, requirements),
      creativity: this.checkCreativity(taskResult)
    };

    // 2. 计算综合评分
    const totalScore = this.calculateTotalScore(scores);

    // 3. 确定质量等级
    const level = this.getQualityLevel(totalScore);

    // 4. 生成优化建议
    const suggestions = this.generateSuggestions(scores, requirements);

    // 5. 判定结果
    const status = this.determineStatus(totalScore);

    // 6. 生成报告
    const report = {
      id: `qr_${Date.now()}`,
      taskId: taskResult.taskId,
      taskName: taskResult.taskName,
      taskType: taskResult.taskType,
      timestamp: Date.now(),
      quality: {
        score: totalScore,
        level,
        scores,
        suggestions
      },
      status,
      reviewer: 'auto',
      reviewedAt: Date.now(),
      duration: Date.now() - startTime
    };

    // 7. 保存报告
    this.saveReport(report);

    // 8. 输出结果
    this.printReport(report);

    return report;
  }

  // ============ 检查方法 ============

  /**
   * 完整性检查
   */
  checkCompleteness(result, requirements) {
    const taskType = result.taskType || 'default';
    const requiredFields = requirements.requiredFields || 
                          this.config.requiredFields[taskType] || [];
    
    if (requiredFields.length === 0) {
      return 100; // 无必需字段要求，默认满分
    }

    let presentFields = 0;
    const missingFields = [];

    for (const field of requiredFields) {
      const value = result[field];
      if (value !== undefined && value !== null && 
          (typeof value !== 'string' || value.trim().length > 0)) {
        presentFields++;
      } else {
        missingFields.push(field);
      }
    }

    const score = (presentFields / requiredFields.length) * 100;

    // 记录缺失字段
    if (missingFields.length > 0) {
      result._missingFields = missingFields;
    }

    return score;
  }

  /**
   * 一致性检查
   */
  checkConsistency(result, requirements) {
    let score = 100;
    const issues = [];

    // 1. 与大纲对比
    if (requirements.outline) {
      const outlineScore = this.checkOutlineConsistency(result, requirements.outline);
      score = score * 0.6 + outlineScore * 0.6;
      
      if (outlineScore < 90) {
        issues.push('与大纲存在偏差');
      }
    }

    // 2. 人物设定一致性
    if (requirements.characters) {
      const characterScore = this.checkCharacterConsistency(result, requirements.characters);
      score = score * 0.7 + characterScore * 0.3;
      
      if (characterScore < 90) {
        issues.push('人物设定不一致');
      }
    }

    // 3. 世界观一致性
    if (requirements.worldSetting) {
      const worldScore = this.checkWorldConsistency(result, requirements.worldSetting);
      score = score * 0.7 + worldScore * 0.3;
      
      if (worldScore < 90) {
        issues.push('世界观设定不一致');
      }
    }

    // 记录问题
    if (issues.length > 0) {
      result._consistencyIssues = issues;
    }

    return Math.max(0, Math.min(100, score));
  }

  /**
   * 大纲一致性检查
   */
  checkOutlineConsistency(result, outline) {
    const content = result.content || '';
    const keyPoints = outline.keyPlotPoints || [];
    
    if (keyPoints.length === 0) return 100;

    let matchedPoints = 0;
    const missedPoints = [];

    for (const point of keyPoints) {
      if (content.includes(point)) {
        matchedPoints++;
      } else {
        missedPoints.push(point);
      }
    }

    const matchRate = (matchedPoints / keyPoints.length) * 100;

    // 记录遗漏的情节点
    if (missedPoints.length > 0) {
      result._missedPlotPoints = missedPoints;
    }

    return matchRate;
  }

  /**
   * 人物设定一致性检查
   */
  checkCharacterConsistency(result, characters) {
    const content = result.content || '';
    let consistentCount = 0;

    for (const char of characters) {
      // 检查人物名称是否一致
      if (content.includes(char.name)) {
        consistentCount++;
      }

      // 检查人物特征是否一致
      if (char.traits) {
        for (const trait of char.traits) {
          if (content.includes(trait)) {
            consistentCount++;
          }
        }
      }
    }

    const totalChecks = characters.length * 2; // 名称 + 特征
    return (consistentCount / totalChecks) * 100;
  }

  /**
   * 世界观一致性检查
   */
  checkWorldConsistency(result, worldSetting) {
    const content = result.content || '';
    let consistentCount = 0;
    let totalCount = 0;

    // 检查地理设定
    if (worldSetting.geography) {
      totalCount++;
      if (content.includes(worldSetting.geography)) {
        consistentCount++;
      }
    }

    // 检查规则设定
    if (worldSetting.rules) {
      totalCount++;
      for (const rule of worldSetting.rules) {
        if (content.includes(rule)) {
          consistentCount++;
        }
      }
    }

    // 检查力量体系
    if (worldSetting.powerSystem) {
      totalCount++;
      if (content.includes(worldSetting.powerSystem)) {
        consistentCount++;
      }
    }

    return totalCount > 0 ? (consistentCount / totalCount) * 100 : 100;
  }

  /**
   * 合规性检查
   */
  checkCompliance(result, requirements) {
    const specs = requirements.specifications || [];
    
    if (specs.length === 0) {
      // 无特殊规范，检查基本要求
      return this.checkBasicCompliance(result);
    }

    let compliantCount = 0;

    for (const spec of specs) {
      if (this.verifySpecification(result, spec)) {
        compliantCount++;
      }
    }

    return (compliantCount / specs.length) * 100;
  }

  /**
   * 基本合规性检查
   */
  checkBasicCompliance(result) {
    let score = 100;

    // 检查字数要求
    if (result.wordCount) {
      const minWords = result.minWordCount || 3000;
      if (result.wordCount < minWords) {
        score -= 20;
      }
    }

    // 检查格式
    if (result.content) {
      // 检查段落结构
      const paragraphs = result.content.split('\n\n');
      if (paragraphs.length < 3) {
        score -= 10;
      }

      // 检查对话格式
      const hasDialog = result.content.includes('"') || result.content.includes('"');
      if (!hasDialog && result.taskType === 'chapter_write') {
        score -= 10;
      }
    }

    return Math.max(0, score);
  }

  /**
   * 验证规范
   */
  verifySpecification(result, spec) {
    // 根据规范类型验证
    switch (spec.type) {
      case 'wordCount':
        return (result.wordCount || 0) >= spec.min;
      case 'format':
        return this.verifyFormat(result, spec.format);
      case 'content':
        return this.verifyContent(result, spec.rules);
      default:
        return true;
    }
  }

  /**
   * 创造性评分
   */
  checkCreativity(result) {
    const content = result.content || '';
    
    // 1. 新颖性检测
    const novelty = this.detectNovelty(content);
    
    // 2. 复杂性检测
    const complexity = this.detectComplexity(content);
    
    // 3. 深度检测
    const depth = this.detectDepth(content);
    
    // 4. 原创性检测
    const originality = this.detectOriginality(content);

    // 平均得分
    const score = (novelty + complexity + depth + originality) / 4;

    return Math.min(100, score);
  }

  /**
   * 新颖性检测
   */
  detectNovelty(content) {
    // 检测是否有新颖的情节转折
    const noveltyKeywords = [
      '然而', '却', '没想到', '突然', '意外', '转折',
      ' surprising', 'unexpected', 'twist'
    ];

    let count = 0;
    for (const keyword of noveltyKeywords) {
      if (content.includes(keyword)) {
        count++;
      }
    }

    // 每有一个新颖关键词加 5 分，最高 100 分
    return Math.min(100, count * 10);
  }

  /**
   * 复杂性检测
   */
  detectComplexity(content) {
    // 检测情节复杂性（多线叙事）
    const lines = content.split('\n');
    const uniqueCharacters = new Set();
    const uniqueLocations = new Set();

    // 简单检测：统计人名和地名出现
    const namePattern = /[A-Z][a-z]{2,}/g;
    const locationPattern = /[地点|地方|城市|国家]/g;

    const names = content.match(namePattern) || [];
    const locations = content.match(locationPattern) || [];

    names.forEach(n => uniqueCharacters.add(n));
    locations.forEach(l => uniqueLocations.add(l));

    // 人物和地点越多，复杂性越高
    const complexity = (uniqueCharacters.size + uniqueLocations.size) * 5;
    return Math.min(100, complexity);
  }

  /**
   * 深度检测
   */
  detectDepth(content) {
    // 检测心理描写深度
    const depthKeywords = [
      '心想', '思考', '回忆', '感受', '内心', '情感',
      'thought', 'felt', 'remembered', 'wondered'
    ];

    let count = 0;
    for (const keyword of depthKeywords) {
      if (content.includes(keyword)) {
        count++;
      }
    }

    return Math.min(100, count * 10);
  }

  /**
   * 原创性检测
   */
  detectOriginality(content) {
    // 简单检测：避免常见套路
    const clichePatterns = [
      '从此过上了幸福的生活',
      '这是一个美好的结局',
      '他们永远在一起了'
    ];

    let clicheCount = 0;
    for (const pattern of clichePatterns) {
      if (content.includes(pattern)) {
        clicheCount++;
      }
    }

    // 每有一个套路减 20 分
    return Math.max(0, 100 - clicheCount * 20);
  }

  // ============ 评分方法 ============

  /**
   * 计算综合评分
   */
  calculateTotalScore(scores) {
    const weights = this.config.weights;

    return Math.round(
      scores.completeness * weights.completeness +
      scores.consistency * weights.consistency +
      scores.compliance * weights.compliance +
      scores.creativity * weights.creativity
    );
  }

  /**
   * 获取质量等级
   */
  getQualityLevel(score) {
    if (score >= 90) return 'A'; // 优秀
    if (score >= 80) return 'B'; // 良好
    if (score >= 70) return 'C'; // 合格
    return 'D'; // 不合格
  }

  /**
   * 判定状态
   */
  determineStatus(score) {
    if (score >= this.config.thresholds.pass) return 'PASSED';
    if (score >= this.config.thresholds.warning) return 'WARNING';
    if (score >= this.config.thresholds.reject) return 'REVIEW';
    return 'REJECTED';
  }

  // ============ 建议生成 ============

  /**
   * 生成优化建议
   */
  generateSuggestions(scores, requirements) {
    const suggestions = [];

    // 完整性建议
    if (scores.completeness < 100) {
      const missing = scores._missingFields || [];
      if (missing.length > 0) {
        suggestions.push(`补充缺失字段：${missing.join(', ')}`);
      }
    }

    // 一致性建议
    if (scores.consistency < 90) {
      const issues = scores._consistencyIssues || [];
      if (issues.includes('与大纲存在偏差')) {
        suggestions.push('检查情节是否与大纲一致');
      }
      if (issues.includes('人物设定不一致')) {
        suggestions.push('确保人物行为和设定一致');
      }
      if (issues.includes('世界观设定不一致')) {
        suggestions.push('检查世界观设定是否有冲突');
      }
    }

    // 合规性建议
    if (scores.compliance < 100) {
      suggestions.push('检查是否符合规范要求');
    }

    // 创造性建议
    if (scores.creativity < 70) {
      suggestions.push('增加情节转折以提升创造性');
      suggestions.push('深化人物内心描写');
      suggestions.push('避免使用常见套路');
    }

    return suggestions;
  }

  // ============ 工具方法 ============

  saveReport(report) {
    const reportFile = path.join(
      CONFIG.reportsDir,
      `${report.id}.json`
    );
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
  }

  printReport(report) {
    console.log('\n📊 质量验证报告:');
    console.log(`   任务：${report.taskName}`);
    console.log(`   评分：${report.quality.score} 分 (${report.quality.level}级)`);
    console.log(`   状态：${report.status}`);
    console.log(`   耗时：${report.duration}ms`);
    console.log('\n   详细评分:');
    console.log(`     完整性：${report.quality.scores.completeness}`);
    console.log(`     一致性：${report.quality.scores.consistency}`);
    console.log(`     合规性：${report.quality.scores.compliance}`);
    console.log(`     创造性：${report.quality.scores.creativity}`);

    if (report.quality.suggestions.length > 0) {
      console.log('\n   优化建议:');
      report.quality.suggestions.forEach((s, i) => {
        console.log(`     ${i + 1}. ${s}`);
      });
    }
    console.log('');
  }
}

// ============ CLI 接口 ============

function printHelp() {
  console.log(`
质量验证系统 v6.0-Phase1

用法：node quality-validator.js <命令> [选项]

命令:
  test                测试质量验证
  validate <文件>     验证文件质量
  config              查看配置
  report <ID>         查看报告

示例:
  node quality-validator.js test
  node quality-validator.js validate result.json
`);
}

// ============ 主程序 ============

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help') {
    printHelp();
    return;
  }

  const validator = new QualityValidator();

  switch (command) {
    case 'test':
      console.log('🧪 测试质量验证系统...\n');
      
      // 测试数据
      const testResult = {
        taskId: 'test_001',
        taskName: '第 1 章创作测试',
        taskType: 'chapter_write',
        title: '第 1 章：开始',
        content: '这是一个测试内容，包含一些情节转折。然而，事情并没有那么简单...',
        wordCount: 3500,
        minWordCount: 3000
      };

      const requirements = {
        requiredFields: ['title', 'content', 'wordCount'],
        outline: {
          keyPlotPoints: ['情节转折', '开始']
        }
      };

      const report = validator.validate(testResult, requirements);
      console.log('✅ 测试完成');
      break;

    case 'validate':
      const file = args[1];
      if (!file) {
        console.log('❌ 请指定文件路径');
        return;
      }

      try {
        const content = fs.readFileSync(file, 'utf-8');
        const result = JSON.parse(content);
        const report = validator.validate(result);
        console.log(`✅ 验证完成，报告已保存：${report.id}`);
      } catch (error) {
        console.error('❌ 验证失败:', error.message);
      }
      break;

    case 'config':
      console.log('📋 当前配置:');
      console.log(JSON.stringify(validator.config, null, 2));
      break;

    case 'report':
      const reportId = args[1];
      if (!reportId) {
        console.log('❌ 请指定报告 ID');
        return;
      }

      const reportFile = path.join(CONFIG.reportsDir, `${reportId}.json`);
      if (fs.existsSync(reportFile)) {
        const report = JSON.parse(fs.readFileSync(reportFile, 'utf-8'));
        validator.printReport(report);
      } else {
        console.log('❌ 报告不存在');
      }
      break;

    default:
      console.log(`未知命令：${command}`);
      printHelp();
  }
}

// 导出 API
module.exports = { QualityValidator, CONFIG };

// 运行 CLI
if (require.main === module) {
  main().catch(console.error);
}
