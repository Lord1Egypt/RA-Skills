/**
 * 产品演示视频生成器单元测试
 */

import { ProductDemoGenerator } from '../product-demo-generator';

describe('ProductDemoGenerator', () => {
  let generator: ProductDemoGenerator;
  let mockVideoSkill: any;
  let mockMcpBus: any;

  beforeEach(() => {
    mockVideoSkill = {
      submitTask: jest.fn().mockReturnValue({ success: true, taskId: 'test-task' }),
    };

    mockMcpBus = {
      createGenerateRequest: jest.fn().mockReturnValue({ headers: {}, body: {} }),
      send: jest.fn().mockResolvedValue({ status: 'success' }),
    };

    generator = new ProductDemoGenerator(mockVideoSkill, mockMcpBus);
  });

  describe('analyzeProductAndGenerateScenes', () => {
    it('should create intro, feature, and outro scenes', () => {
      const product = {
        name: 'Test Product',
        description: 'Test description',
        features: ['Feature 1', 'Feature 2'],
      };

      // @ts-ignore - accessing private method for testing
      const scenes = generator.analyzeProductAndGenerateScenes(product, {
        durationSeconds: 30,
        style: 'professional',
        language: 'zh-CN',
        backgroundMusic: true,
        showSubtitles: true,
        aspectRatio: '16:9',
        resolution: '1080P',
      });

      expect(scenes.length).toBe(4); // intro + 2 features + outro
      expect(scenes[0].description).toContain('介绍');
      expect(scenes[scenes.length - 1].description).toContain('结尾');
    });
  });

  describe('generateDemo', () => {
    it('should generate demo video from product info', async () => {
      const product = {
        name: 'Test Product',
        description: 'A great product',
        features: ['Feature 1'],
      };

      const result = await generator.generateDemo(product);

      expect(result.taskId).toContain('Test_Product');
      expect(result.metadata.totalScenes).toBeGreaterThan(0);
    }, 15000);
  });

  describe('analyzeProductAndGenerateScenes', () => {
    it('should create intro, feature, and outro scenes', () => {
      const product = {
        name: 'Test Product',
        description: 'Test description',
        features: ['Feature 1', 'Feature 2'],
      };

      // @ts-ignore - accessing private method for testing
      const scenes = generator.analyzeProductAndGenerateScenes(product, {
        durationSeconds: 30,
        style: 'professional',
        language: 'zh-CN',
        backgroundMusic: true,
        showSubtitles: true,
        aspectRatio: '16:9',
        resolution: '1080P',
      });

      expect(scenes.length).toBe(4); // intro + 2 features + outro
      expect(scenes[0].description).toContain('介绍');
      expect(scenes[scenes.length - 1].description).toContain('结尾');
    });
  });
});
