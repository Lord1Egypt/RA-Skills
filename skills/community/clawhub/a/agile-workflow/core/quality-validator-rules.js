#!/usr/bin/env node
/**
 * 质量验证规则库 v6.0-Phase1-Stage2
 * 
 * 增强功能:
 * 1. 完整性检查（嵌套字段/条件必需）
 * 2. 一致性检查（语义/时间线/逻辑）
 * 3. 合规性检查（敏感内容/格式/字数）
 */

const fs = require('fs');
const path = require('path');

// ============ 完整性检查增强 ============

class CompletenessChecker {
  constructor() {
    this.requiredFields = {
      'chapter_write': [
        'title',
        'content',
        'wordCount'
      ],
      'outline': [
        'plotPoints',
        'characters',
        'settings',
        'conflicts'
      ],
      'character_design': [
        'name',
        'background',
        'traits',
        'goals',
        'conflicts'
      ],
      'world_building': [
        'name',
        'rules',
        'geography',
        'history',
        'factions'
      ]
    };
  }

  /**
   * 检查完整性（支持嵌套字段）
   */
  checkCompleteness(result, requirements = {}) {
    const taskType = result.taskType || 'default';
    const requiredFields = requirements.requiredFields || 
                          this.requiredFields[taskType] || [];
    
    const report = {
      score: 100,
      missingFields: [],
      invalidFields: [],
      nestedIssues: []
    };

    // 检查必需字段
    for (const field of requiredFields) {
      const fieldReport = this.checkField(result, field);
      
      if (!fieldReport.present) {
        report.missingFields.push(field);
      } else if (!fieldReport.valid) {
        report.invalidFields.push({
          field,
          reason: fieldReport.reason
        });
      }

      // 检查嵌套字段
      if (field.includes('.')) {
        const nestedReport = this.checkNestedField(result, field);
        if (!nestedReport.valid) {
          report.nestedIssues.push({
            field,
            issues: nestedReport.issues
          });
        }
      }
    }

    // 计算分数
    const totalFields = requiredFields.length;
    const validFields = totalFields - report.missingFields.length - report.invalidFields.length;
    report.score = (validFields / totalFields) * 100;

    return report;
  }

  /**
   * 检查单个字段
   */
  checkField(result, field) {
    const value = this.getFieldValue(result, field);

    // 检查是否存在
    if (value === undefined || value === null) {
      return { present: false, valid: false, reason: '字段不存在' };
    }

    // 检查是否为空
    if (typeof value === 'string' && value.trim().length === 0) {
      return { present: true, valid: false, reason: '字段为空' };
    }

    // 检查数组
    if (Array.isArray(value) && value.length === 0) {
      return { present: true, valid: false, reason: '数组为空' };
    }

    // 检查对象
    if (typeof value === 'object' && Object.keys(value).length === 0) {
      return { present: true, valid: false, reason: '对象为空' };
    }

    return { present: true, valid: true };
  }

  /**
   * 检查嵌套字段
   */
  checkNestedField(result, nestedField) {
    const parts = nestedField.split('.');
    let current = result;
    const issues = [];

    for (let i = 0; i < parts.length; i++) {
      const part = parts[i];
      
      if (current === undefined || current === null) {
        issues.push(`路径 ${parts.slice(0, i + 1).join('.')} 不存在`);
        break;
      }

      if (typeof current !== 'object') {
        issues.push(`路径 ${parts.slice(0, i + 1).join('.')} 不是对象`);
        break;
      }

      current = current[part];
    }

    return {
      valid: issues.length === 0,
      issues
    };
  }

  /**
   * 获取字段值（支持嵌套）
   */
  getFieldValue(obj, field) {
    const parts = field.split('.');
    let current = obj;

    for (const part of parts) {
      if (current === undefined || current === null) {
        return undefined;
      }
      current = current[part];
    }

    return current;
  }

  /**
   * 条件必需字段检查
   */
  checkConditionalFields(result, conditions) {
    const report = {
      score: 100,
      missingConditionals: []
    };

    for (const condition of conditions) {
      // 检查条件是否满足
      const conditionMet = this.checkCondition(result, condition.when);
      
      if (conditionMet) {
        // 条件满足，检查必需字段
        for (const field of condition.required) {
          const fieldReport = this.checkField(result, field);
          
          if (!fieldReport.present || !fieldReport.valid) {
            report.missingConditionals.push({
              condition: condition.when,
              field,
              reason: '条件满足但字段缺失'
            });
          }
        }
      }
    }

    // 计算分数
    if (report.missingConditionals.length > 0) {
      report.score = 100 - (report.missingConditionals.length * 10);
    }

    return report;
  }

  /**
   * 检查条件
   */
  checkCondition(result, condition) {
    const { field, operator, value } = condition;
    const fieldValue = this.getFieldValue(result, field);

    switch (operator) {
      case 'equals':
        return fieldValue === value;
      case 'not_equals':
        return fieldValue !== value;
      case 'exists':
        return fieldValue !== undefined && fieldValue !== null;
      case 'greater_than':
        return fieldValue > value;
      case 'less_than':
        return fieldValue < value;
      case 'includes':
        return Array.isArray(fieldValue) && fieldValue.includes(value);
      default:
        return false;
    }
  }
}

// ============ 一致性检查增强 ============

class ConsistencyChecker {
  constructor() {
    this.timelineEvents = [];
    this.characterTraits = {};
    this.worldRules = {};
  }

  /**
   * 检查一致性（语义/时间线/逻辑）
   */
  checkConsistency(result, requirements = {}) {
    const report = {
      score: 100,
      semanticIssues: [],
      timelineIssues: [],
      logicIssues: [],
      characterIssues: [],
      worldIssues: []
    };

    // 语义一致性
    if (requirements.outline) {
      const semanticReport = this.checkSemanticConsistency(result, requirements.outline);
      report.semanticIssues = semanticReport.issues;
      report.score -= semanticReport.penalty;
    }

    // 时间线一致性
    if (requirements.timeline) {
      const timelineReport = this.checkTimelineConsistency(result, requirements.timeline);
      report.timelineIssues = timelineReport.issues;
      report.score -= timelineReport.penalty;
    }

    // 逻辑一致性
    const logicReport = this.checkLogicConsistency(result);
    report.logicIssues = logicReport.issues;
    report.score -= logicReport.penalty;

    // 人物一致性
    if (requirements.characters) {
      const characterReport = this.checkCharacterConsistency(result, requirements.characters);
      report.characterIssues = characterReport.issues;
      report.score -= characterReport.penalty;
    }

    // 世界观一致性
    if (requirements.worldSetting) {
      const worldReport = this.checkWorldConsistency(result, requirements.worldSetting);
      report.worldIssues = worldReport.issues;
      report.score -= worldReport.penalty;
    }

    // 确保分数不低于 0
    report.score = Math.max(0, report.score);

    return report;
  }

  /**
   * 语义一致性检查
   */
  checkSemanticConsistency(result, outline) {
    const issues = [];
    let penalty = 0;

    const content = result.content || '';
    const keyPoints = outline.keyPlotPoints || [];

    // 检查关键情节点
    let matchedPoints = 0;
    for (const point of keyPoints) {
      if (!content.includes(point)) {
        issues.push(`缺少关键情节：${point}`);
        penalty += 5;
      } else {
        matchedPoints++;
      }
    }

    // 检查情节顺序
    if (outline.plotOrder) {
      for (let i = 0; i < outline.plotOrder.length - 1; i++) {
        const current = outline.plotOrder[i];
        const next = outline.plotOrder[i + 1];
        
        const currentIndex = content.indexOf(current);
        const nextIndex = content.indexOf(next);
        
        if (currentIndex !== -1 && nextIndex !== -1 && currentIndex > nextIndex) {
          issues.push(`情节顺序错误：${current} 应该在 ${next} 之前`);
          penalty += 10;
        }
      }
    }

    return { issues, penalty };
  }

  /**
   * 时间线一致性检查
   */
  checkTimelineConsistency(result, timeline) {
    const issues = [];
    let penalty = 0;

    const content = result.content || '';
    
    // 提取时间信息
    const timeReferences = this.extractTimeReferences(content);
    
    // 检查时间冲突
    for (const ref of timeReferences) {
      if (timeline.events) {
        for (const event of timeline.events) {
          if (ref.event === event.name && ref.time !== event.time) {
            issues.push(`时间冲突：${event.name} 应该是 ${event.time}，文中是 ${ref.time}`);
            penalty += 15;
          }
        }
      }
    }

    // 检查时间逻辑
    if (timeReferences.length > 1) {
      for (let i = 0; i < timeReferences.length - 1; i++) {
        const current = timeReferences[i];
        const next = timeReferences[i + 1];
        
        if (current.order > next.order) {
          issues.push(`时间顺序错误：${current.event} 应该在 ${next.event} 之后`);
          penalty += 10;
        }
      }
    }

    return { issues, penalty };
  }

  /**
   * 提取时间引用
   */
  extractTimeReferences(content) {
    const references = [];
    
    // 简单实现：查找时间相关关键词
    const timePatterns = [
      /(\d+) 年后？/g,
      /(\d+) 个月前？/g,
      /(\d+) 天后？/g,
      /第 (\d+) 章/g,
      /(\d+) 岁时？/g
    ];

    for (const pattern of timePatterns) {
      let match;
      while ((match = pattern.exec(content)) !== null) {
        references.push({
          text: match[0],
          value: parseInt(match[1]),
          type: this.getTimeType(pattern),
          order: match.index
        });
      }
    }

    return references.sort((a, b) => a.order - b.order);
  }

  /**
   * 获取时间类型
   */
  getTimeType(pattern) {
    const patternStr = pattern.toString();
    if (patternStr.includes('年')) return 'year';
    if (patternStr.includes('月')) return 'month';
    if (patternStr.includes('天')) return 'day';
    if (patternStr.includes('章')) return 'chapter';
    if (patternStr.includes('岁')) return 'age';
    return 'unknown';
  }

  /**
   * 逻辑一致性检查
   */
  checkLogicConsistency(result) {
    const issues = [];
    let penalty = 0;

    const content = result.content || '';

    // 检查因果关系
    const causeEffectPatterns = [
      { cause: '因为', effect: '所以' },
      { cause: '由于', effect: '因此' },
      { cause: '既然', effect: '就' }
    ];

    for (const pattern of causeEffectPatterns) {
      const hasCause = content.includes(pattern.cause);
      const hasEffect = content.includes(pattern.effect);
      
      if (hasCause && !hasEffect) {
        issues.push(`逻辑不完整：有"${pattern.cause}"但缺少"${pattern.effect}"`);
        penalty += 5;
      }
    }

    // 检查矛盾陈述
    const contradictions = this.detectContradictions(content);
    issues.push(...contradictions);
    penalty += contradictions.length * 10;

    return { issues, penalty };
  }

  /**
   * 检测矛盾陈述
   */
  detectContradictions(content) {
    const contradictions = [];
    
    // 简单实现：查找矛盾关键词
    const contradictionPairs = [
      ['活着', '死了'],
      ['喜欢', '讨厌'],
      ['同意', '反对'],
      ['成功', '失败'],
      ['开始', '结束']
    ];

    for (const [word1, word2] of contradictionPairs) {
      if (content.includes(word1) && content.includes(word2)) {
        // 检查是否在同一上下文中
        const index1 = content.indexOf(word1);
        const index2 = content.indexOf(word2);
        
        // 如果在同一段落中
        const paragraph1 = this.getParagraph(content, index1);
        const paragraph2 = this.getParagraph(content, index2);
        
        if (paragraph1 === paragraph2) {
          contradictions.push(`可能矛盾：同一段落中包含"${word1}"和"${word2}"`);
        }
      }
    }

    return contradictions;
  }

  /**
   * 获取段落
   */
  getParagraph(content, index) {
    const paragraphs = content.split('\n\n');
    let currentIndex = 0;
    
    for (let i = 0; i < paragraphs.length; i++) {
      const paragraph = paragraphs[i];
      const paragraphEnd = currentIndex + paragraph.length;
      
      if (index >= currentIndex && index <= paragraphEnd) {
        return i;
      }
      
      currentIndex = paragraphEnd + 2; // \n\n
    }
    
    return -1;
  }

  /**
   * 人物一致性检查
   */
  checkCharacterConsistency(result, characters) {
    const issues = [];
    let penalty = 0;

    const content = result.content || '';

    for (const char of characters) {
      // 检查人物名称一致性
      if (!content.includes(char.name)) {
        issues.push(`人物${char.name}未在文中出现`);
        penalty += 5;
        continue;
      }

      // 检查人物特征一致性
      if (char.traits) {
        for (const trait of char.traits) {
          // 检查是否有矛盾行为
          if (trait.type === 'positive' && this.hasNegativeBehavior(content, char.name, trait)) {
            issues.push(`人物${char.name}行为与特征"${trait.name}"矛盾`);
            penalty += 10;
          }
          if (trait.type === 'negative' && this.hasPositiveBehavior(content, char.name, trait)) {
            issues.push(`人物${char.name}行为与特征"${trait.name}"矛盾`);
            penalty += 10;
          }
        }
      }

      // 检查人物目标一致性
      if (char.goals) {
        for (const goal of char.goals) {
          if (!this.supportsGoal(content, char.name, goal)) {
            issues.push(`人物${char.name}的行为不支持目标"${goal}"`);
            penalty += 5;
          }
        }
      }
    }

    return { issues, penalty };
  }

  /**
   * 检查是否有负面行为
   */
  hasNegativeBehavior(content, character, trait) {
    // 简单实现：查找负面行为关键词
    const negativeKeywords = ['背叛', '欺骗', '伤害', '逃跑', '放弃'];
    const charIndex = content.indexOf(character);
    
    if (charIndex === -1) return false;

    // 检查人物出现位置附近是否有负面行为
    const context = content.substring(Math.max(0, charIndex - 100), charIndex + 100);
    
    for (const keyword of negativeKeywords) {
      if (context.includes(keyword)) {
        return true;
      }
    }

    return false;
  }

  /**
   * 检查是否有正面行为
   */
  hasPositiveBehavior(content, character, trait) {
    // 简单实现：查找正面行为关键词
    const positiveKeywords = ['帮助', '保护', '拯救', '勇敢', '诚实'];
    const charIndex = content.indexOf(character);
    
    if (charIndex === -1) return false;

    const context = content.substring(Math.max(0, charIndex - 100), charIndex + 100);
    
    for (const keyword of positiveKeywords) {
      if (context.includes(keyword)) {
        return true;
      }
    }

    return false;
  }

  /**
   * 检查是否支持目标
   */
  supportsGoal(content, character, goal) {
    const charIndex = content.indexOf(character);
    const goalIndex = content.indexOf(goal);
    
    if (charIndex === -1 || goalIndex === -1) return false;

    // 检查人物和目标是否在同一上下文中
    const distance = Math.abs(charIndex - goalIndex);
    return distance < 500; // 500 字符内
  }

  /**
   * 世界观一致性检查
   */
  checkWorldConsistency(result, worldSetting) {
    const issues = [];
    let penalty = 0;

    const content = result.content || '';

    // 检查地理设定
    if (worldSetting.geography) {
      if (!content.includes(worldSetting.geography)) {
        issues.push(`未提及地理设定：${worldSetting.geography}`);
        penalty += 5;
      }
    }

    // 检查规则设定
    if (worldSetting.rules) {
      for (const rule of worldSetting.rules) {
        if (this.violatesRule(content, rule)) {
          issues.push(`违反世界观规则：${rule}`);
          penalty += 15;
        }
      }
    }

    // 检查力量体系
    if (worldSetting.powerSystem) {
      if (!content.includes(worldSetting.powerSystem)) {
        issues.push(`未提及力量体系：${worldSetting.powerSystem}`);
        penalty += 5;
      }
    }

    return { issues, penalty };
  }

  /**
   * 检查是否违反规则
   */
  violatesRule(content, rule) {
    // 简单实现：查找规则违反关键词
    const violationKeywords = ['不可能', '无法', '不能', '禁止', '违反'];
    
    for (const keyword of violationKeywords) {
      if (content.includes(keyword) && content.includes(rule)) {
        return true;
      }
    }

    return false;
  }
}

// ============ 导出 ============

module.exports = {
  CompletenessChecker,
  ConsistencyChecker
};
