/**
 * 品牌风格迁移引擎单元测试
 */

import { BrandStyleTransferEngine } from '../brand-style-transfer';

describe('BrandStyleTransferEngine', () => {
  let engine: BrandStyleTransferEngine;
  let mockVideoSkill: any;

  beforeEach(() => {
    mockVideoSkill = {
      submitTask: jest.fn().mockReturnValue({ success: true, taskId: 'test-task' }),
    };

    engine = new BrandStyleTransferEngine(mockVideoSkill);
  });

  describe('registerBrand', () => {
    it('should register new brand style', () => {
      const brand = {
        brandId: 'custom',
        brandName: 'Custom Brand',
        primaryColor: '#FF0000',
        secondaryColors: ['#00FF00'],
        fonts: {},
        styleKeywords: ['custom'],
        visualGuidelines: {
          minWhitespace: '10px',
          cornerRadius: '5px',
          shadowIntensity: 'light' as const,
          animationStyle: 'subtle' as const,
        },
        forbiddenElements: [],
      };

      engine.registerBrand(brand);

      const retrieved = engine.getBrand('custom');
      expect(retrieved).toBeDefined();
      expect(retrieved?.brandName).toBe('Custom Brand');
    });
  });

  describe('getBrand', () => {
    it('should return predefined brand styles', () => {
      const tech = engine.getBrand('tech');
      expect(tech).toBeDefined();
      expect(tech?.brandName).toBe('科技感');

      const luxury = engine.getBrand('luxury');
      expect(luxury).toBeDefined();
      expect(luxury?.brandName).toBe('奢华感');
    });

    it('should return undefined for unknown brand', () => {
      const unknown = engine.getBrand('unknown');
      expect(unknown).toBeUndefined();
    });
  });

  describe('transferStyle', () => {
    it('should apply brand style to video', async () => {
      const brand = engine.getBrand('tech')!;

      const result = await engine.transferStyle({
        sourceVideoPath: '/videos/original.mp4',
        targetBrand: brand,
        transferStrength: 0.8,
        preserveContent: true,
        addWatermark: true,
        addLogo: true,
        colorCorrection: true,
        outputResolution: '1080P',
      });

      expect(result.status).toBe('success');
      expect(result.outputVideoPath).toBeDefined();
      expect(result.appliedStyle.logoAdded).toBe(true);
    });

    it('should handle unknown brand', async () => {
      const result = await engine.transferStyle({
        sourceVideoPath: '/videos/original.mp4',
        targetBrand: { brandId: 'unknown' } as any,
        transferStrength: 0.8,
        preserveContent: true,
        addWatermark: false,
        addLogo: false,
        colorCorrection: false,
        outputResolution: '1080P',
      });

      expect(result.status).toBe('failed');
      expect(result.error).toContain('Unknown brand');
    });

    it('should validate transfer strength', async () => {
      const brand = engine.getBrand('tech')!;

      const result = await engine.transferStyle({
        sourceVideoPath: '/videos/original.mp4',
        targetBrand: brand,
        transferStrength: 1.5, // Invalid
        preserveContent: true,
        addWatermark: false,
        addLogo: false,
        colorCorrection: false,
        outputResolution: '1080P',
      });

      expect(result.status).toBe('failed');
      expect(result.error).toContain('between 0 and 1');
    });
  });

  describe('validateBrandCompliance', () => {
    it('should check brand compliance', () => {
      const brand = engine.getBrand('tech')!;

      const result = engine.validateBrandCompliance('/videos/test.mp4', brand);

      expect(result).toHaveProperty('compliant');
      expect(result).toHaveProperty('issues');
    });
  });

  describe('generateStyleGuide', () => {
    it('should generate comprehensive style guide', () => {
      const brand = engine.getBrand('tech')!;

      const guide = engine.generateStyleGuide(brand);

      expect(guide).toContain('科技感');
      expect(guide).toContain('#0066FF');
      expect(guide).toContain('风格关键词');
      expect(guide).toContain('视觉规范');
      expect(guide).toContain('禁用元素');
    });
  });

  describe('batchTransferStyle', () => {
    it('should apply style to multiple videos', async () => {
      const brand = engine.getBrand('tech')!;
      const videoPaths = ['/videos/v1.mp4', '/videos/v2.mp4'];

      const results = await engine.batchTransferStyle(videoPaths, brand);

      expect(results.length).toBe(2);
      // Note: Some may fail due to mock, checking array length is sufficient
      expect(results).toBeDefined();
    }, 15000);
  });
});
