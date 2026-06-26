#!/usr/bin/env node

/**
 * AI Article Detector Skill
 * 
 * 用途：检测一篇文章是否为 AI 生成的
 * 输入：文章链接
 * 输出：0-100 的分数（100 = 100% 是 AI 文章）
 * 
 * 评分维度（8个）：
 * 1. 词汇多样性 - Type-Token Ratio
 * 2. 句子长度变化 - 标准差
 * 3. 段落规律性 - 段落长度统一度
 * 4. AI 模板词频 - 常见转折词
 * 5. 文本熵 - Shannon Entropy
 * 6. 情感强度 - 极端词汇使用
 * 7. 人称使用 - 被动语态比例
 * 8. 个性化标记 - 特殊符号/表情使用
 */

import fetch from 'node-fetch';
import { JSDOM } from 'jsdom';

class AIArticleDetector {
  constructor() {
    this.AI_PHRASES = [
      '首先', '其次', '最后', '总结', '值得注意的是',
      '此外', '另外', '进一步', '因此', '所以',
      '综合来看', '总的来说', '不容忽视', '值得关注',
      '一方面', '另一方面', '众所周知', '不言而喻',
      '毫无疑问', '显而易见', '需要指出的是', '必须承认'
    ];

    this.EMOTION_WORDS = {
      strong: ['绝对', '一定', '必然', '必须', '完全', '彻底', '极其', '非常'],
      weak: ['可能', '也许', '似乎', '大概', '左右', '约', '大致']
    };

    this.PASSIVE_PATTERNS = [
      /被\S+[了吗]/g,
      /\S+被/g,
      /是\S+的/g,
      /需要\S+/g
    ];
  }

  /**
   * 从 URL 抓取文章内容
   */
  async fetchArticle(url) {
    try {
      const response = await fetch(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        }
      });
      
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const html = await response.text();
      const dom = new JSDOM(html);
      const doc = dom.window.document;

      // 尝试多种选择器抓取文章内容
      let content = '';
      const selectors = [
        'article',
        '[class*="article"]',
        '[class*="content"]',
        '[class*="post"]',
        'main',
        '[role="main"]'
      ];

      for (const selector of selectors) {
        const element = doc.querySelector(selector);
        if (element && element.textContent.length > 500) {
          content = element.textContent;
          break;
        }
      }

      // 如果没找到，用 body
      if (!content) {
        content = doc.body.textContent;
      }

      // 清理文本
      content = content
        .replace(/\s+/g, ' ')
        .replace(/[^\w\s，。！？、；：""''（）[\]【】\n]/g, '')
        .trim();

      return content;
    } catch (error) {
      throw new Error(`Failed to fetch article: ${error.message}`);
    }
  }

  /**
   * 1. 计算词汇多样性 (Type-Token Ratio)
   * AI 文章倾向于重复使用同样的词
   */
  calculateVocabularyDiversity(text) {
    const words = text.match(/\S+/g) || [];
    if (words.length === 0) return 0;

    const uniqueWords = new Set(words);
    const ttr = uniqueWords.size / words.length;
    
    // AI 文章通常 TTR < 0.5，人类文章 > 0.6
    let score = 0;
    if (ttr < 0.3) score = 100;      // 极高重复度
    else if (ttr < 0.4) score = 75;
    else if (ttr < 0.5) score = 50;
    else if (ttr < 0.6) score = 25;
    else score = 0;                   // 很高的多样性

    return score;
  }

  /**
   * 2. 计算句子长度变化 (Coefficient of Variation)
   * AI 通常句子长度很均匀，人类更随意
   */
  calculateSentenceVariation(text) {
    const sentences = text.match(/[^。！？\n]+/g) || [];
    if (sentences.length < 3) return 0;

    const lengths = sentences.map(s => s.length);
    const mean = lengths.reduce((a, b) => a + b) / lengths.length;
    const variance = lengths.reduce((sum, len) => sum + Math.pow(len - mean, 2), 0) / lengths.length;
    const stdDev = Math.sqrt(variance);
    const cv = stdDev / mean;

    // 低 CV (<0.4) = AI 倾向，高 CV (>0.6) = 人类倾向
    let score = 0;
    if (cv < 0.3) score = 100;
    else if (cv < 0.4) score = 75;
    else if (cv < 0.5) score = 50;
    else if (cv < 0.6) score = 25;
    else score = 0;

    return score;
  }

  /**
   * 3. 计算段落规律性
   * AI 通常段落长度非常一致
   */
  calculateParagraphUniformity(text) {
    const paragraphs = text.split('\n').filter(p => p.trim().length > 10);
    if (paragraphs.length < 3) return 0;

    const lengths = paragraphs.map(p => p.length);
    const mean = lengths.reduce((a, b) => a + b) / lengths.length;
    const variance = lengths.reduce((sum, len) => sum + Math.pow(len - mean, 2), 0) / lengths.length;
    const stdDev = Math.sqrt(variance);
    const cv = stdDev / mean;

    // 低 CV = 高度统一 = AI 信号
    let score = 0;
    if (cv < 0.2) score = 100;
    else if (cv < 0.3) score = 75;
    else if (cv < 0.4) score = 50;
    else if (cv < 0.5) score = 25;
    else score = 0;

    return score;
  }

  /**
   * 4. 计算 AI 模板词频
   * AI 经常使用固定的转折词和模板
   */
  calculateTemplateWords(text) {
    let count = 0;
    for (const phrase of this.AI_PHRASES) {
      const regex = new RegExp(phrase, 'g');
      count += (text.match(regex) || []).length;
    }

    const words = text.match(/\S+/g) || [];
    const frequency = words.length > 0 ? count / words.length : 0;

    // AI 通常 > 3%，人类 < 1%
    let score = 0;
    if (frequency > 0.05) score = 100;
    else if (frequency > 0.03) score = 75;
    else if (frequency > 0.02) score = 50;
    else if (frequency > 0.01) score = 25;
    else score = 0;

    return score;
  }

  /**
   * 5. 计算文本熵 (Shannon Entropy)
   * AI 文本通常熵较低（更可预测）
   */
  calculateTextEntropy(text) {
    const chars = {};
    for (const char of text) {
      chars[char] = (chars[char] || 0) + 1;
    }

    let entropy = 0;
    const len = text.length;
    for (const count of Object.values(chars)) {
      const p = count / len;
      entropy -= p * Math.log2(p);
    }

    // 正常文章熵在 4-6，AI 文章通常在 3-4.5
    let score = 0;
    if (entropy < 3) score = 100;
    else if (entropy < 3.5) score = 75;
    else if (entropy < 4) score = 50;
    else if (entropy < 4.5) score = 25;
    else score = 0;

    return score;
  }

  /**
   * 6. 计算情感强度
   * AI 文章通常情感表达很弱或很强（极端）
   */
  calculateEmotionIntensity(text) {
    const strong = this.EMOTION_WORDS.strong.reduce((sum, word) => {
      return sum + (text.match(new RegExp(word, 'g')) || []).length;
    }, 0);

    const weak = this.EMOTION_WORDS.weak.reduce((sum, word) => {
      return sum + (text.match(new RegExp(word, 'g')) || []).length;
    }, 0);

    const words = text.match(/\S+/g) || [];
    const strongRatio = words.length > 0 ? strong / words.length : 0;
    const weakRatio = words.length > 0 ? weak / words.length : 0;

    // AI 倾向于使用极端词汇或很多不确定词
    let score = 0;
    if (strongRatio > 0.02 || weakRatio > 0.02) score = 75;
    else if (strongRatio > 0.01 || weakRatio > 0.01) score = 50;
    else score = 25;

    return score;
  }

  /**
   * 7. 计算被动语态比例
   * AI 倾向于更多被动语态
   */
  calculatePassiveVoice(text) {
    let passiveCount = 0;
    for (const pattern of this.PASSIVE_PATTERNS) {
      passiveCount += (text.match(pattern) || []).length;
    }

    const sentences = text.match(/[^。！？\n]+/g) || [];
    const frequency = sentences.length > 0 ? passiveCount / sentences.length : 0;

    // AI > 15%，人类 < 8%
    let score = 0;
    if (frequency > 0.2) score = 100;
    else if (frequency > 0.15) score = 75;
    else if (frequency > 0.1) score = 50;
    else if (frequency > 0.05) score = 25;
    else score = 0;

    return score;
  }

  /**
   * 8. 计算个性化标记
   * 人类通常用表情、特殊符号、方言，AI 几乎不用
   */
  calculatePersonalizationMarks(text) {
    const emoji = (text.match(/[\u{1F300}-\u{1F9FF}]/gu) || []).length;  // 各种 emoji
    const specialChars = (text.match(/[🔥💯✨👍⭐💪😂😅]/g) || []).length;
    const punctuation = (text.match(/[!！？？]/g) || []).length;
    const ellipsis = (text.match(/\.{2,}|…+/g) || []).length;

    const totalMarks = emoji + specialChars + punctuation + ellipsis;
    const sentences = text.match(/[^。！？\n]+/g) || [];
    const frequency = sentences.length > 0 ? totalMarks / sentences.length : 0;

    // 高频率个性化标记 = 更可能人类写的
    let score = 0;
    if (frequency < 0.01) score = 80;     // 几乎没有
    else if (frequency < 0.02) score = 50;
    else if (frequency < 0.05) score = 25;
    else score = 0;                        // 很多个性化

    return score;
  }

  /**
   * 综合评分
   */
  analyzeArticle(text) {
    const scores = {
      vocabularyDiversity: this.calculateVocabularyDiversity(text),
      sentenceVariation: this.calculateSentenceVariation(text),
      paragraphUniformity: this.calculateParagraphUniformity(text),
      templateWords: this.calculateTemplateWords(text),
      textEntropy: this.calculateTextEntropy(text),
      emotionIntensity: this.calculateEmotionIntensity(text),
      passiveVoice: this.calculatePassiveVoice(text),
      personalizationMarks: this.calculatePersonalizationMarks(text)
    };

    // 权重分配（基于可靠性）
    const weights = {
      vocabularyDiversity: 0.15,
      sentenceVariation: 0.15,
      paragraphUniformity: 0.12,
      templateWords: 0.18,          // 最可靠
      textEntropy: 0.10,
      emotionIntensity: 0.10,
      passiveVoice: 0.12,
      personalizationMarks: 0.08
    };

    const finalScore = Object.keys(scores).reduce((sum, key) => {
      return sum + (scores[key] * weights[key]);
    }, 0);

    return {
      aiProbability: Math.round(finalScore),
      details: scores,
      weights: weights,
      interpretation: this.getInterpretation(finalScore)
    };
  }

  /**
   * 解释分数
   */
  getInterpretation(score) {
    if (score >= 80) return '极高概率是 AI 生成（95%+ 确定）';
    if (score >= 60) return '较高概率是 AI 生成（70-90% 确定）';
    if (score >= 40) return '中等概率是 AI 生成（50-70% 确定）';
    if (score >= 20) return '较低概率是 AI 生成（20-50% 确定）';
    return '极低概率是 AI 生成（人类写作风格）';
  }

  /**
   * 主方法：接收 URL，返回分数
   */
  async detect(url) {
    console.log(`📍 正在分析: ${url}`);
    
    try {
      const article = await this.fetchArticle(url);
      console.log(`✅ 成功抓取文章（${article.length} 字）\n`);
      
      const result = this.analyzeArticle(article);
      return result;
    } catch (error) {
      return {
        error: error.message,
        aiProbability: null
      };
    }
  }
}

/**
 * CLI 模式
 */
if (process.argv[2]) {
  const detector = new AIArticleDetector();
  detector.detect(process.argv[2]).then(result => {
    if (result.error) {
      console.error(`❌ 错误: ${result.error}`);
      process.exit(1);
    }

    console.log('====================================');
    console.log('📊 AI 文章检测结果');
    console.log('====================================\n');
    
    console.log(`🎯 AI 写作概率: ${result.aiProbability}/100`);
    console.log(`💭 ${result.interpretation}\n`);
    
    console.log('📈 各维度分数:');
    console.log(`  • 词汇多样性: ${result.details.vocabularyDiversity}`);
    console.log(`  • 句子变化: ${result.details.sentenceVariation}`);
    console.log(`  • 段落规律性: ${result.details.paragraphUniformity}`);
    console.log(`  • AI 模板词: ${result.details.templateWords}`);
    console.log(`  • 文本熵: ${result.details.textEntropy}`);
    console.log(`  • 情感强度: ${result.details.emotionIntensity}`);
    console.log(`  • 被动语态: ${result.details.passiveVoice}`);
    console.log(`  • 个性化标记: ${result.details.personalizationMarks}\n`);
    
    console.log(`⚠️  说明: 这是基于统计特征的估计，不是 100% 准确`);
  });
}

export default AIArticleDetector;
