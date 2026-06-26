/**
 * Security Sandbox Tests - ANFSF v2.0
 * 
 * @module asf-v4/sandbox/__tests__/sandbox.test.ts
 */

import { describe, test, expect, beforeEach } from '@jest/globals';
import {
  SecuritySandbox,
  createSecuritySandbox,
  DEFAULT_SANDBOX_CONFIG,
  SandboxConfig,
  globalSandboxMonitor,
} from '../../security-sandbox';

describe('Security Sandbox Tests', () => {
  let sandbox: SecuritySandbox;

  beforeEach(() => {
    sandbox = createSecuritySandbox();
  });

  test('should create security sandbox', () => {
    expect(sandbox).toBeDefined();
  });

  test('should have default config', () => {
    const status = sandbox.getStatus();
    expect(status.config.memoryLimitMB).toBe(256);
    expect(status.config.timeoutSeconds).toBe(30);
    expect(status.config.cpuQuota).toBe(0.5);
  });

  test('should execute code successfully', async () => {
    const result = await sandbox.executeCode('console.log("hello");');
    expect(result.success).toBe(true);
    expect(result.result).toBeDefined();
  });

  test('should check file access - allowed path', () => {
    const allowed = sandbox.checkFileAccess('/tmp/test.txt', 'read');
    expect(allowed).toBe(true);
  });

  test('should check file access - denied path', () => {
    const allowed = sandbox.checkFileAccess('/root/.ssh/id_rsa', 'read');
    expect(allowed).toBe(false);
    
    const status = sandbox.getStatus();
    expect(status.violations.length).toBeGreaterThan(0);
    expect(status.violations[0]).toContain('File access denied');
  });

  test('should check file access - read-only write', () => {
    const allowed = sandbox.checkFileAccess('/etc/passwd', 'write');
    expect(allowed).toBe(false);
    
    const status = sandbox.getStatus();
    expect(status.violations.length).toBeGreaterThan(0);
    expect(status.violations[0]).toContain('Write access denied to read-only path');
  });

  test('should check network access - allowed', () => {
    const allowed = sandbox.checkNetworkAccess('localhost', 80);
    expect(allowed).toBe(true);
  });

  test('should check network access - disallowed host', () => {
    const allowed = sandbox.checkNetworkAccess('google.com', 80);
    expect(allowed).toBe(false);
    
    const status = sandbox.getStatus();
    expect(status.violations.length).toBeGreaterThan(0);
    expect(status.violations[0]).toContain('Network access to disallowed host');
  });

  test('should check network access - disallowed port', () => {
    const allowed = sandbox.checkNetworkAccess('localhost', 22);
    expect(allowed).toBe(false);
    
    const status = sandbox.getStatus();
    expect(status.violations.length).toBeGreaterThan(0);
    expect(status.violations[0]).toContain('Network access to disallowed port');
  });

  test('should check env var access - allowed', () => {
    const value = sandbox.checkEnvVarAccess('PATH');
    // PATH 应该返回实际值或 null，但不会是 [MASKED]
    expect(value).not.toBe('[MASKED]');
  });

  test('should check env var access - masked', () => {
    const value = sandbox.checkEnvVarAccess('API_KEY');
    expect(value).toBe('[MASKED]');
  });

  test('should check env var access - denied', () => {
    const value = sandbox.checkEnvVarAccess('CUSTOM_VAR_NOT_ALLOWED');
    expect(value).toBeNull();
  });

  test('should get sandbox status', () => {
    const status = sandbox.getStatus();
    expect(status.id).toBeDefined();
    expect(status.startTime).toBeDefined();
    expect(status.fileOperations).toBe(0);
    expect(status.networkCalls).toBe(0);
    expect(status.violations).toEqual([]);
  });

  test('should create sandbox with custom config', () => {
    const customConfig: Partial<SandboxConfig> = {
      memoryLimitMB: 512,
      timeoutSeconds: 60,
      allowedPaths: ['/custom'],
    };
    
    const customSandbox = createSecuritySandbox(customConfig);
    const status = customSandbox.getStatus();
    
    expect(status.config.memoryLimitMB).toBe(512);
    expect(status.config.timeoutSeconds).toBe(60);
    expect(status.config.allowedPaths).toContain('/custom');
  });

  test('should register sandbox in global monitor', () => {
    globalSandboxMonitor.registerSandbox(sandbox);
    expect(globalSandboxMonitor.getActiveSandboxes()).toBe(1);
    
    const status = sandbox.getStatus();
    const retrieved = globalSandboxMonitor.getSandbox(status.id);
    expect(retrieved).toBeDefined();
  });

  test('should kill sandbox from global monitor', () => {
    // Create a new sandbox for this test to avoid conflicts
    const testSandbox = createSecuritySandbox();
    
    globalSandboxMonitor.registerSandbox(testSandbox);
    expect(globalSandboxMonitor.getActiveSandboxes()).toBeGreaterThanOrEqual(1);
    
    const status = testSandbox.getStatus();
    const killed = globalSandboxMonitor.killSandbox(status.id);
    expect(killed).toBe(true);
  });
});