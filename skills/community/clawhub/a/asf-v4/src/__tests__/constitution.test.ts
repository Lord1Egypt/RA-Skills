/**
 * ANFSF Constitution Tests - v2.0
 * 
 * @module asf-v4/__tests__/constitution.test.ts
 */

import { describe, test, expect, beforeEach } from '@jest/globals';
import {
  ANFSF_CONSTITUTION,
  ConstitutionValidator,
  createConstitutionValidator,
  PRINCIPLE_SAFETY_FIRST,
  BOUNDARY_DELETE_SYSTEM_FILES,
  BOUNDARY_UNAUTHORIZED_API,
  BOUNDARY_SENSITIVE_DATA_TO_LLM,
  BOUNDARY_DELETE_PROD_CONFIG,
} from '../constitution-validator';

describe('ANFSF Constitution Tests', () => {
  let validator: ConstitutionValidator;

  beforeEach(() => {
    validator = createConstitutionValidator();
  });

  test('should have constitution defined', () => {
    expect(ANFSF_CONSTITUTION).toBeDefined();
    expect(ANFSF_CONSTITUTION.version).toBe('2.0.0');
    expect(ANFSF_CONSTITUTION.principles.length).toBeGreaterThan(0);
  });

  test('should have safety boundaries', () => {
    expect(ANFSF_CONSTITUTION.boundaries.length).toBe(4);
    expect(ANFSF_CONSTITUTION.boundaries.map(b => b.id)).toEqual([
      'SB-001',
      'SB-002',
      'SB-003',
      'SB-004',
    ]);
  });

  test('should block deleting system files', () => {
    const context = {
      action: 'delete',
      resourcePath: '/etc/important.conf',
    };

    const result = validator.validate(context);
    expect(result.allowed).toBe(false);
    expect(result.reasons.length).toBeGreaterThan(0);
    expect(result.reasons[0]).toContain('安全优先原则');
  });

  test('should block unauthorized API access', () => {
    const context = {
      apiType: 'external',
      authorized: false,
      privilegeLevel: 'admin',
    };

    const result = validator.validate(context);
    expect(result.allowed).toBe(false);
    expect(result.reasons.length).toBeGreaterThan(0);
  });

  test('should warn on sensitive data to LLM', () => {
    const context = {
      containsPII: true,
      encrypted: false,
      toLLM: true,
      piiFields: ['email', 'phone'],
    };

    const result = validator.validate(context);
    expect(result.allowed).toBe(false); // warn 应该阻止
    expect(result.reasons.length).toBeGreaterThan(0);
    expect(result.reasons[0]).toContain('WARNING');
  });

  test('should audit deleting production config', () => {
    const context = {
      action: 'delete',
      environment: 'production',
      resourceType: 'config',
      resourcePath: '/app/config.json', // 添加 resourcePath
    };

    const result = validator.validate(context);
    expect(result.allowed).toBe(false); // audit 应该阻止
    expect(result.reasons.length).toBeGreaterThan(0);
    expect(result.reasons[0]).toContain('AUDIT');
  });

  test('should allow normal operation', () => {
    const context = {
      action: 'read',
      resourceType: 'config',
      environment: 'development',
    };

    const result = validator.validate(context);
    expect(result.allowed).toBe(true);
    expect(result.reasons.length).toBe(0);
  });

  test('should validate safety first principle', () => {
    expect(PRINCIPLE_SAFETY_FIRST.category).toBe('security');
    expect(PRINCIPLE_SAFETY_FIRST.priority).toBe(4);
  });

  test('should validate safety boundaries', () => {
    expect(BOUNDARY_DELETE_SYSTEM_FILES.type).toBe('block');
    expect(BOUNDARY_UNAUTHORIZED_API.type).toBe('block');
    expect(BOUNDARY_SENSITIVE_DATA_TO_LLM.type).toBe('warn');
    expect(BOUNDARY_DELETE_PROD_CONFIG.type).toBe('audit');
  });

  test('should validate all principles are defined', () => {
    const principleIds = ANFSF_CONSTITUTION.principles.map(p => p.id);
    expect(principleIds).toEqual([
      'PI-001',
      'PI-002',
      'PI-003',
      'PI-004',
      'PI-005',
    ]);
  });
});