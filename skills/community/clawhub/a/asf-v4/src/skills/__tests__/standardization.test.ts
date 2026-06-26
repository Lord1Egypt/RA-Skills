/**
 * Skills Standardization Tests - ANFSF v2.0
 * 
 * @module asf-v4/skills/__tests__/standardization.test.ts
 */

import { describe, test, expect, beforeEach } from '@jest/globals';
import { StandardizedSkill, DefaultSkillsRegistry, createSkillsRegistry } from '../standardization';

describe('Skills Standardization Tests', () => {
  let registry: DefaultSkillsRegistry;

  beforeEach(() => {
    registry = createSkillsRegistry() as DefaultSkillsRegistry;
  });

  test('should create StandardizedSkill', () => {
    const skill = new StandardizedSkill({
      name: 'test-skill',
      version: '1.0.0',
      description: 'Test skill',
      usage: ['Use test-skill for testing'],
      examples: [
        { query: 'test query', result: 'test result' },
      ],
    });
    
    expect(skill.name).toBe('test-skill');
    expect(skill.version).toBe('1.0.0');
    expect(skill.description).toBe('Test skill');
    expect(skill.usage.length).toBe(1);
    expect(skill.examples.length).toBe(1);
  });

  test('should add usage', () => {
    const skill = new StandardizedSkill({
      name: 'test-skill',
      version: '1.0.0',
      description: 'Test skill',
      usage: [],
      examples: [],
    });
    
    skill.addUsage('New usage');
    expect(skill.usage.length).toBe(1);
    expect(skill.usage[0]).toBe('New usage');
  });

  test('should add example', () => {
    const skill = new StandardizedSkill({
      name: 'test-skill',
      version: '1.0.0',
      description: 'Test skill',
      usage: [],
      examples: [],
    });
    
    skill.addExample('query1', 'result1');
    expect(skill.examples.length).toBe(1);
    expect(skill.examples[0].query).toBe('query1');
  });

  test('should format SKILLmd', () => {
    const skill = new StandardizedSkill({
      name: 'test-skill',
      version: '1.0.0',
      description: 'Test skill',
      usage: ['Usage 1', 'Usage 2'],
      examples: [
        { query: 'query1', result: 'result1' },
      ],
    });
    
    const md = skill.formatSKILLmd();
    expect(md).toContain('# test-skill');
    expect(md).toContain('**Version**: 1.0.0');
    expect(md).toContain('**Description**: Test skill');
    expect(md).toContain('## Usage');
    expect(md).toContain('## Examples');
    expect(md).toContain('query1');
  });

  test('should register skill', () => {
    const skill = new StandardizedSkill({
      name: 'test-skill',
      version: '1.0.0',
      description: 'Test skill',
      usage: [],
      examples: [],
    });
    
    registry.register(skill);
    expect(registry.get('test-skill')).toBeDefined();
    expect(registry.get('test-skill')?.name).toBe('test-skill');
  });

  test('should get skill', () => {
    const skill = new StandardizedSkill({
      name: 'test-skill',
      version: '1.0.0',
      description: 'Test skill',
      usage: [],
      examples: [],
    });
    
    registry.register(skill);
    const retrieved = registry.get('test-skill');
    expect(retrieved).toBeDefined();
    expect(retrieved?.name).toBe('test-skill');
  });

  test('should list skills', () => {
    const skill1 = new StandardizedSkill({
      name: 'skill-1',
      version: '1.0.0',
      description: 'Skill 1',
      usage: [],
      examples: [],
    });
    
    const skill2 = new StandardizedSkill({
      name: 'skill-2',
      version: '1.0.0',
      description: 'Skill 2',
      usage: [],
      examples: [],
    });
    
    registry.register(skill1);
    registry.register(skill2);
    
    const skills = registry.list();
    expect(skills.length).toBe(2);
  });

  test('should generate SKILLmds', () => {
    const skill = new StandardizedSkill({
      name: 'test-skill',
      version: '1.0.0',
      description: 'Test skill',
      usage: [],
      examples: [],
    });
    
    registry.register(skill);
    
    const mdMap = registry.generateSKILLmds();
    expect(mdMap['test-skill']).toBeDefined();
    expect(mdMap['test-skill']).toContain('# test-skill');
  });
});