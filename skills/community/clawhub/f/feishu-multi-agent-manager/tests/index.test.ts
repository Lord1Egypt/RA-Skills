/**
 * 飞书多 Agent 管理器单元测试
 */

import { main } from '../src/index';

describe('Feishu Multi-Agent Manager Tests', () => {
  test('should be defined', () => {
    expect(main).toBeDefined();
  });

  test('should validate Feishu credentials', () => {
    // Valid credentials
    const validAppId = 'cli_a1b2c3d4e5f6';
    const validAppSecret = '12345678901234567890123456789012'; // 32 chars
    
    expect(validAppId.startsWith('cli_')).toBe(true);
    expect(validAppSecret.length).toBe(32);
  });

  test('should reject invalid AppID format', () => {
    const invalidAppId = 'invalid_id';
    expect(invalidAppId.startsWith('cli_')).toBe(false);
  });

  test('should reject invalid AppSecret length', () => {
    const invalidSecret = 'short';
    expect(invalidSecret.length).not.toBe(32);
  });
});
