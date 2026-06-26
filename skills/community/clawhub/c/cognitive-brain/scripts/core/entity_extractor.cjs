/**
 * 实体提取模块
 * 从文本中提取有意义的概念和实体
 */

// 停用词
const STOPWORDS = new Set([
  'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
  '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
  '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
  '自己', '这', '那', '这些', '那些', '它们', '他', '她', '它', '们',
  // 更多停用词...
]);

// 概念匹配模式
const CONCEPT_PATTERNS = {
  tech: /(?:[a-zA-Z][a-zA-Z0-9]*\.js|[a-zA-Z][a-zA-Z0-9]*\.py|[a-zA-Z][a-zA-Z0-9]*\.json|node|python|redis|postgres|docker|kubernetes|react|vue|angular|express|koa|django|flask)/gi,
  properNoun: /[A-Z][a-zA-Z]*(?:[A-Z][a-zA-Z]*)*/g,
  chineseKeywords: /(?:记忆|学习|思考|反思|知识|概念|联想|遗忘|编码|检索|重要|情感|用户|系统|优化|改进|修复|问题|代码|模块|功能|数据|文件|配置|环境|测试|发布|版本)/g
};

/**
 * 从内容中提取实体
 * @param {string} content - 输入内容
 * @returns {string[]} - 提取的实体列表
 */
function extractEntities(content) {
  const entities = [];
  const seen = new Set();

  const addEntity = (term, source = 'unknown') => {
    if (!term || typeof term !== 'string') return false;

    const normalized = term.toLowerCase().trim();

    if (normalized.length < 2) return false;
    if (seen.has(normalized)) return false;
    if (STOPWORDS.has(normalized)) return false;
    if (/^[0-9]+$/.test(normalized)) return false;

    seen.add(normalized);
    entities.push({ term: term.trim(), source });
    return true;
  };

  // 1. 技术术语
  const techTerms = content.match(CONCEPT_PATTERNS.tech) || [];
  techTerms.forEach(term => addEntity(term, 'tech'));

  // 2. 英文专有名词
  const properNouns = content.match(CONCEPT_PATTERNS.properNoun) || [];
  properNouns.forEach(noun => {
    if (noun.length >= 3 && !STOPWORDS.has(noun.toLowerCase())) {
      addEntity(noun, 'proper_noun');
    }
  });

  // 3. 中文关键词
  const chineseKeywordMatches = content.match(CONCEPT_PATTERNS.chineseKeywords) || [];
  chineseKeywordMatches.forEach(word => addEntity(word, 'keyword'));

  // 4. 补充中文词组
  if (entities.length < 15) {
    const chineseWords = content.match(/[\u4e00-\u9fa5]{2,4}/g) || [];
    const genericWords = new Set(['可以', '需要', '应该', '进行', '实现', '使用', '通过',
      '一个', '这个', '那个', '一些', '每个', '所有', '其他', '之后', '之前', '已经',
      '正在', '如果', '因为', '所以', '但是', '而且', '或者', '以及', '不是', '没有',
      '什么', '怎么', '如何', '一下', '一种', '一起', '一样', '一直', '一切']);

    chineseWords.forEach(word => {
      if (genericWords.has(word)) return;
      if (word.split('').some(c => STOPWORDS.has(c))) return;
      addEntity(word, 'chinese_phrase');
    });
  }

  // 5. 从片段中提取
  if (entities.length < 10) {
    const segments = content.split(/[，。！？、；：""''（）【】\s]+/);
    segments.forEach(seg => {
      if (seg.length >= 3 && seg.length <= 8) {
        const meaningfulChars = seg.split('').filter(c => !STOPWORDS.has(c));
        if (meaningfulChars.length >= 2) {
          addEntity(seg, 'segment');
        }
      }
    });
  }

  // 按优先级排序并返回
  const sourcePriority = { tech: 1, proper_noun: 2, keyword: 3, chinese_phrase: 4, segment: 5 };
  return entities
    .sort((a, b) => (sourcePriority[a.source] || 99) - (sourcePriority[b.source] || 99))
    .slice(0, 20)
    .map(e => e.term);
}

module.exports = {
  extractEntities,
  STOPWORDS,
  CONCEPT_PATTERNS
};

