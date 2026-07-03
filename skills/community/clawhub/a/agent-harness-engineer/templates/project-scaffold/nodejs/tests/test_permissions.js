/**
 * 测试权限系统
 */

const { PermissionManager } = require('../src/permissions/models');
const { SandboxManager } = require('../src/permissions/sandbox');

describe('PermissionManager', () => {
  let manager;
  
  beforeEach(() => {
    manager = new PermissionManager({
      mode: 'ask',
      rules: [
        { pattern: 'Bash\\(rm -rf \\*\\)', action: 'deny' }
      ]
    });
  });
  
  test('should deny dangerous commands', () => {
    const result = manager.checkPermission('Bash(rm -rf /)', {});
    expect(result).toBe(false);
  });
  
  test('should allow safe commands', () => {
    const result = manager.checkPermission('Bash(ls -la)', {});
    expect(result).toBe(true);
  });
});

describe('SandboxManager', () => {
  let manager;
  
  beforeEach(() => {
    manager = new SandboxManager({
      enabled: true,
      allowedDirectories: ['workspace/'],
      deniedPatterns: ['.env']
    });
  });
  
  test('should validate allowed path', () => {
    const result = manager.validatePath('workspace/test.txt');
    expect(result).toBe(true);
  });
  
  test('should reject denied pattern', () => {
    const result = manager.validatePath('workspace/.env');
    expect(result).toBe(false);
  });
  
  test('should validate safe command', () => {
    const result = manager.validateCommand('ls -la');
    expect(result).toBe(true);
  });
  
  test('should reject dangerous command', () => {
    const result = manager.validateCommand('rm -rf /');
    expect(result).toBe(false);
  });
});
