import { describe, it, expect } from 'vitest';
import { extractCSSVariables, extractJSONBlocks } from './parser';

describe('parser helpers', () => {
  describe('extractCSSVariables', () => {
    it('extracts CSS custom properties from a css code block', () => {
      const md = [
        'Some text',
        '```css',
        ':root {',
        '  --apple-bg-white: #FFFFFF;',
        '  --apple-bg-dark: #1D1D1F;',
        '}',
        '```',
      ].join('\n');

      const vars = extractCSSVariables(md);
      expect(vars).toEqual([
        { name: '--apple-bg-white', value: '#FFFFFF' },
        { name: '--apple-bg-dark', value: '#1D1D1F' },
      ]);
    });

    it('returns empty array when no css blocks exist', () => {
      expect(extractCSSVariables('# Hello')).toEqual([]);
    });
  });

  describe('extractJSONBlocks', () => {
    it('extracts and parses JSON from json code blocks', () => {
      const md = [
        'Some text',
        '```json',
        '{ "name": "test", "version": "1.0.0" }',
        '```',
      ].join('\n');

      const blocks = extractJSONBlocks(md);
      expect(blocks).toHaveLength(1);
      expect(blocks[0]).toEqual({ name: 'test', version: '1.0.0' });
    });

    it('skips malformed JSON blocks', () => {
      const md = [
        '```json',
        '{ invalid json }',
        '```',
      ].join('\n');

      expect(extractJSONBlocks(md)).toEqual([]);
    });

    it('returns empty array when no json blocks exist', () => {
      expect(extractJSONBlocks('# Hello')).toEqual([]);
    });
  });
});
