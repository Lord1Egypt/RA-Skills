/**
 * GEO-Shield 单元测试
 */

import { detectGEOPatterns, calculateDomainTrust, analyzeContentQuality, extractDomain } from '../src/index';

describe('GEO-Shield', () => {
  describe('extractDomain', () => {
    it('should extract domain from URL', () => {
      expect(extractDomain('https://www.example.com/article')).toBe('www.example.com');
      expect(extractDomain('http://test.gov.cn/page')).toBe('test.gov.cn');
    });

    it('should return empty for invalid URL', () => {
      expect(extractDomain('not-a-url')).toBe('');
      expect(extractDomain('')).toBe('');
    });
  });

  describe('detectGEOPatterns', () => {
    it('should detect over-optimization patterns', () => {
      const content = '最佳产品 2026，100% 有效，专家一致推荐！';
      const results = detectGEOPatterns(content);
      expect(results.overOptimization).toBeGreaterThan(0);
    });

    it('should detect emotional manipulation patterns', () => {
      const content = '立即行动！限时优惠，最后机会，千万不要错过！';
      const results = detectGEOPatterns(content);
      expect(results.emotionalManipulation).toBeGreaterThan(0);
    });

    it('should detect false authority patterns', () => {
      const content = '哈佛研究表明，斯坦福科学家确认，NASA 警告！';
      const results = detectGEOPatterns(content);
      expect(results.falseAuthority).toBeGreaterThan(0);
    });

    it('should detect AI-generated content patterns', () => {
      const content = '总之，综上所述，需要注意的是，总的来说，希望这些信息对你有帮助。';
      const results = detectGEOPatterns(content);
      expect(results.aiGenerated).toBeGreaterThan(0);
    });

    it('should detect link manipulation patterns', () => {
      const content = '点击这里，立即访问，点击下方链接，扫码获取！';
      const results = detectGEOPatterns(content);
      expect(results.linkManipulation).toBeGreaterThan(0);
    });

    it('should return zero for clean content', () => {
      const content = '这是一个普通的陈述句。没有特殊特征。';
      const results = detectGEOPatterns(content);
      expect(results.overOptimization).toBe(0);
      expect(results.emotionalManipulation).toBe(0);
    });
  });

  describe('calculateDomainTrust', () => {
    it('should return 1.0 for government domains', () => {
      expect(calculateDomainTrust('www.gov.cn')).toBe(1.0);
      expect(calculateDomainTrust('agency.gov')).toBe(1.0);
    });

    it('should return 1.0 for education domains', () => {
      expect(calculateDomainTrust('www.edu.cn')).toBe(1.0);
      expect(calculateDomainTrust('university.edu')).toBe(1.0);
    });

    it('should return 1.0 for trusted media', () => {
      expect(calculateDomainTrust('people.com.cn')).toBe(1.0);
      expect(calculateDomainTrust('xinhuanet.com')).toBe(1.0);
    });

    it('should return 0.3 for suspicious domains', () => {
      expect(calculateDomainTrust('health-info.com')).toBe(0.3);
      expect(calculateDomainTrust('news-daily.net')).toBe(0.3);
    });

    it('should return 0.6 for unknown domains', () => {
      expect(calculateDomainTrust('example.com')).toBe(0.6);
      expect(calculateDomainTrust('unknown-site.org')).toBe(0.6);
    });
  });

  describe('analyzeContentQuality', () => {
    it('should analyze paragraph and sentence counts', () => {
      const content = '第一段。第二段。\n\n第三段。第四段。';
      const metrics = analyzeContentQuality(content);
      expect(metrics.paragraphCount).toBe(2);
      expect(metrics.sentenceCount).toBe(4);
    });

    it('should detect citations', () => {
      const contentWithCitation = '根据研究显示 [1]，来源：权威机构。';
      const contentWithoutCitation = '这是一个普通陈述。';
      
      expect(analyzeContentQuality(contentWithCitation).hasCitations).toBe(true);
      expect(analyzeContentQuality(contentWithoutCitation).hasCitations).toBe(false);
    });

    it('should detect author info', () => {
      const contentWithAuthor = '作者：张三 撰稿。';
      const contentWithoutAuthor = '这是一个普通文章。';
      
      expect(analyzeContentQuality(contentWithAuthor).hasAuthor).toBe(true);
      expect(analyzeContentQuality(contentWithoutAuthor).hasAuthor).toBe(false);
    });

    it('should detect date', () => {
      const contentWithDate = '发布于 2024 年 1 月 15 日。';
      const contentWithoutDate = '这是一个普通文章。';
      
      expect(analyzeContentQuality(contentWithDate).hasDate).toBe(true);
      expect(analyzeContentQuality(contentWithoutDate).hasDate).toBe(false);
    });
  });
});
