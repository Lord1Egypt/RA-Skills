const { analyze } = require('../src/analyzer');

describe('First Principle Analyzer', () => {
  describe('analyze function', () => {
    test('should throw error for empty input', () => {
      expect(() => analyze('')).toThrow('Problem must be a non-empty string');
    });

    test('should throw error for non-string input', () => {
      expect(() => analyze(123)).toThrow('Problem must be a non-empty string');
    });

    test('should return valid analysis result', () => {
      const result = analyze('如何降低火箭发射成本？');
      expect(result).toHaveProperty('problem');
      expect(result).toHaveProperty('category');
      expect(result).toHaveProperty('assumptions');
      expect(result).toHaveProperty('basicTruths');
      expect(result).toHaveProperty('solutions');
      expect(result).toHaveProperty('timestamp');
    });

    test('should identify at least 3 assumptions', () => {
      const result = analyze('如何降低火箭发射成本？');
      expect(result.assumptions.length).toBeGreaterThanOrEqual(3);
    });

    test('should generate at least 2 solutions', () => {
      const result = analyze('如何降低火箭发射成本？');
      expect(result.solutions.length).toBeGreaterThanOrEqual(2);
    });

    test('should categorize technical problems correctly', () => {
      const result = analyze('如何设计更好的技术架构？');
      expect(result.category).toBe('technical');
    });

    test('should categorize business problems correctly', () => {
      const result = analyze('如何进入新市场？');
      expect(result.category).toBe('business');
    });
  });

  describe('categorizeProblem function', () => {
    test('should categorize technical keywords', () => {
      expect(categorizeProblem('系统架构设计')).toBe('technical');
    });

    test('should categorize business keywords', () => {
      expect(categorizeProblem('市场竞争策略')).toBe('business');
    });

    test('should return general for unknown categories', () => {
      expect(categorizeProblem('今天天气如何')).toBe('general');
    });
  });
});

// Import helper functions for testing
const { categorizeProblem } = require('../src/analyzer');
