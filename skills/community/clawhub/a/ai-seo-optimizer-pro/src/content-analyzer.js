/**
 * 内容分析与优化建议模块
 */

class ContentAnalyzer {
  constructor() {
    this.optimalDensity = {
      min: 0.5,
      max: 2.5,
      ideal: 1.5
    };
  }

  /**
   * 分析内容
   * @param {string} content - 文章内容或 URL
   * @returns {Promise<Object>} 分析报告
   */
  async analyze(content) {
    const isUrl = content.startsWith('http');
    const text = isUrl ? await this._fetchContent(content) : content;
    
    const analysis = {
      score: 0,
      wordCount: 0,
      readability: {},
      structure: {},
      keywords: {},
      meta: {},
      issues: [],
      suggestions: []
    };
    
    // 基础统计
    analysis.wordCount = this._countWords(text);
    analysis.charCount = text.length;
    analysis.paragraphCount = this._countParagraphs(text);
    analysis.sentenceCount = this._countSentences(text);
    
    // 可读性分析
    analysis.readability = this._analyzeReadability(text);
    
    // 结构分析
    analysis.structure = this._analyzeStructure(text);
    
    // 计算分数
    analysis.score = this._calculateScore(analysis);
    
    return analysis;
  }

  /**
   * 获取优化建议
   * @param {string} content - 内容
   * @param {string[]} targetKeywords - 目标关键词
   * @returns {Promise<Object>} 优化建议
   */
  async getOptimizationSuggestions(content, targetKeywords = []) {
    const analysis = await this.analyze(content);
    const suggestions = [];
    
    // 内容长度建议
    if (analysis.wordCount < 1000) {
      suggestions.push({
        priority: 'high',
        category: 'content',
        title: '增加内容长度',
        description: `当前 ${analysis.wordCount} 字，建议至少 1000 字`,
        action: `需要增加 ${1000 - analysis.wordCount} 字`,
        impact: 'high'
      });
    } else if (analysis.wordCount < 2000) {
      suggestions.push({
        priority: 'medium',
        category: 'content',
        title: '考虑扩展内容',
        description: `当前 ${analysis.wordCount} 字，优质内容通常 2000+ 字`,
        action: '添加更多深度内容和示例',
        impact: 'medium'
      });
    }
    
    // 可读性建议
    if (analysis.readability.fleschScore < 60) {
      suggestions.push({
        priority: 'medium',
        category: 'readability',
        title: '提高可读性',
        description: `可读性分数 ${analysis.readability.fleschScore}，建议简化句子`,
        action: '使用更短的句子和简单词汇',
        impact: 'medium'
      });
    }
    
    // 结构建议
    if (analysis.structure.headings && analysis.structure.headings.length < 3) {
      suggestions.push({
        priority: 'high',
        category: 'structure',
        title: '添加更多标题',
        description: '内容结构不够清晰，建议添加小标题',
        action: '每 300-500 字添加一个小标题',
        impact: 'high'
      });
    }
    
    // 关键词建议
    if (targetKeywords.length > 0) {
      const keywordSuggestions = await this._analyzeKeywordUsage(content, targetKeywords);
      suggestions.push(...keywordSuggestions);
    }
    
    // 元标签建议
    suggestions.push({
      priority: 'high',
      category: 'meta',
      title: '优化元标签',
      description: '确保标题标签包含主要关键词（50-60 字符）',
      action: '编写吸引人的 SEO 标题和描述',
      impact: 'high'
    });
    
    // 图片建议
    suggestions.push({
      priority: 'medium',
      category: 'media',
      title: '添加相关图片',
      description: '每 500 字建议添加 1 张相关图片',
      action: `建议添加 ${Math.ceil(analysis.wordCount / 500)} 张图片`,
      impact: 'medium'
    });
    
    // 内链建议
    suggestions.push({
      priority: 'medium',
      category: 'links',
      title: '添加内部链接',
      description: '链接到相关的内部内容',
      action: '添加 3-5 个相关内链',
      impact: 'medium'
    });
    
    // 外链建议
    suggestions.push({
      priority: 'low',
      category: 'links',
      title: '添加权威外链',
      description: '链接到权威来源增加可信度',
      action: '添加 2-3 个高质量外链',
      impact: 'low'
    });
    
    return {
      currentScore: analysis.score,
      potentialScore: Math.min(100, analysis.score + 25),
      totalSuggestions: suggestions.length,
      highPriority: suggestions.filter(s => s.priority === 'high').length,
      suggestions: suggestions.sort((a, b) => {
        const priorityOrder = { high: 0, medium: 1, low: 2 };
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      })
    };
  }

  /**
   * 计算内容分数
   * @private
   */
  _calculateScore(analysis) {
    let score = 0;
    
    // 内容长度分数 (30 分)
    const lengthScore = Math.min(30, (analysis.wordCount / 2000) * 30);
    score += lengthScore;
    
    // 可读性分数 (25 分)
    const readabilityScore = (analysis.readability.fleschScore / 100) * 25;
    score += readabilityScore;
    
    // 结构分数 (25 分)
    const structureScore = Math.min(25, (analysis.structure.headings?.length || 0) * 5);
    score += structureScore;
    
    // 段落分数 (20 分)
    const paragraphScore = Math.min(20, (analysis.paragraphCount / 10) * 20);
    score += paragraphScore;
    
    return Math.round(score);
  }

  /**
   * 分析可读性
   * @private
   */
  _analyzeReadability(text) {
    const words = this._countWords(text);
    const sentences = this._countSentences(text);
    const syllables = this._estimateSyllables(text);
    
    // Flesch Reading Ease
    const fleschScore = sentences === 0 ? 0 : 
      206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words);
    
    // Flesch-Kincaid Grade Level
    const gradeLevel = sentences === 0 ? 0 :
      0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59;
    
    return {
      fleschScore: Math.max(0, Math.min(100, Math.round(fleschScore))),
      gradeLevel: Math.max(0, Math.round(gradeLevel)),
      avgWordsPerSentence: sentences > 0 ? (words / sentences).toFixed(1) : 0,
      avgSyllablesPerWord: words > 0 ? (syllables / words).toFixed(2) : 0,
      difficulty: this._getDifficultyLevel(fleschScore)
    };
  }

  /**
   * 分析内容结构
   * @private
   */
  _analyzeStructure(text) {
    const headings = [];
    const headingPattern = /^(#{1,6})\s+(.+)$/gm;
    let match;
    
    while ((match = headingPattern.exec(text)) !== null) {
      headings.push({
        level: match[1].length,
        text: match[2].trim()
      });
    }
    
    return {
      headings,
      hasH1: headings.some(h => h.level === 1),
      hasH2: headings.some(h => h.level === 2),
      hasH3: headings.some(h => h.level === 3),
      headingCount: headings.length,
      structureScore: this._calculateStructureScore(headings)
    };
  }

  /**
   * 分析关键词使用
   * @private
   */
  async _analyzeKeywordUsage(content, keywords) {
    const suggestions = [];
    const contentLower = content.toLowerCase();
    
    for (const keyword of keywords) {
      const keywordLower = keyword.toLowerCase();
      const occurrences = (contentLower.match(new RegExp(keywordLower, 'g')) || []).length;
      const density = (occurrences / this._countWords(content)) * 100;
      
      if (density < this.optimalDensity.min) {
        suggestions.push({
          priority: 'high',
          category: 'keywords',
          title: `增加关键词 "${keyword}" 使用`,
          description: `当前密度 ${density.toFixed(2)}%，建议 ${this.optimalDensity.min}-${this.optimalDensity.max}%`,
          action: `再使用 ${Math.ceil(this._countWords(content) * (this.optimalDensity.min - density) / 100)} 次`,
          impact: 'high'
        });
      } else if (density > this.optimalDensity.max) {
        suggestions.push({
          priority: 'high',
          category: 'keywords',
          title: `减少关键词 "${keyword}" 堆砌`,
          description: `当前密度 ${density.toFixed(2)}%，可能被视为关键词堆砌`,
          action: '减少关键词使用，保持自然',
          impact: 'high'
        });
      }
    }
    
    return suggestions;
  }

  /**
   * 计算结构分数
   * @private
   */
  _calculateStructureScore(headings) {
    if (headings.length === 0) return 0;
    
    let score = 0;
    
    // 有 H1 标题
    if (headings.some(h => h.level === 1)) score += 30;
    
    // 有 H2 标题
    const h2Count = headings.filter(h => h.level === 2).length;
    score += Math.min(30, h2Count * 10);
    
    // 有 H3 标题
    const h3Count = headings.filter(h => h.level === 3).length;
    score += Math.min(20, h3Count * 5);
    
    // 层级合理
    const hasProperHierarchy = headings.every((h, i) => {
      if (i === 0) return h.level === 1;
      return h.level <= headings[i - 1].level + 1;
    });
    
    if (hasProperHierarchy) score += 20;
    
    return score;
  }

  /**
   * 获取难度级别
   * @private
   */
  _getDifficultyLevel(score) {
    if (score >= 90) return 'very_easy';
    if (score >= 80) return 'easy';
    if (score >= 70) return 'fairly_easy';
    if (score >= 60) return 'standard';
    if (score >= 50) return 'fairly_difficult';
    if (score >= 30) return 'difficult';
    return 'very_difficult';
  }

  /**
   * 统计单词数
   * @private
   */
  _countWords(text) {
    return (text.match(/[\u4e00-\u9fa5a-zA-Z0-9]+/g) || []).length;
  }

  /**
   * 统计段落数
   * @private
   */
  _countParagraphs(text) {
    return text.split(/\n\s*\n/).filter(p => p.trim().length > 0).length;
  }

  /**
   * 统计句子数
   * @private
   */
  _countSentences(text) {
    return (text.match(/[。！？.!?]/g) || []).length;
  }

  /**
   * 估算音节数
   * @private
   */
  _estimateSyllables(text) {
    // 中文每个字算一个音节
    const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
    // 英文单词估算
    const englishWords = (text.match(/[a-zA-Z]+/g) || []);
    const englishSyllables = englishWords.reduce((sum, word) => {
      return sum + Math.max(1, word.length / 3);
    }, 0);
    
    return chineseChars + englishSyllables;
  }

  /**
   * 获取内容
   * @private
   */
  async _fetchContent(url) {
    // 实际实现会调用 web_fetch
    return '示例内容...';
  }
}

module.exports = new ContentAnalyzer();
