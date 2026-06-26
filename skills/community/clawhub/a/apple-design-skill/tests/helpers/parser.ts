import { readFileSync } from 'fs';
import { resolve } from 'path';

/**
 * Root directory of the apple-design-skill project.
 */
const PROJECT_ROOT = resolve(__dirname, '..', '..');

/**
 * Read a markdown file relative to the project root and return its content.
 */
export function readMarkdownFile(relativePath: string): string {
  const fullPath = resolve(PROJECT_ROOT, relativePath);
  return readFileSync(fullPath, 'utf-8');
}

/**
 * Extract CSS custom properties (variables) from fenced CSS code blocks in markdown.
 * Returns an array of `{ name, value }` objects for each `--*` declaration found.
 */
export function extractCSSVariables(
  markdown: string
): Array<{ name: string; value: string }> {
  const codeBlockRegex = /```css\s*\n([\s\S]*?)```/g;
  const varRegex = /(--[\w-]+)\s*:\s*([^;]+);/g;
  const results: Array<{ name: string; value: string }> = [];

  let blockMatch: RegExpExecArray | null;
  while ((blockMatch = codeBlockRegex.exec(markdown)) !== null) {
    const block = blockMatch[1];
    let varMatch: RegExpExecArray | null;
    while ((varMatch = varRegex.exec(block)) !== null) {
      results.push({ name: varMatch[1], value: varMatch[2].trim() });
    }
  }

  return results;
}

/**
 * Extract JSON data blocks from fenced JSON code blocks in markdown.
 * Returns an array of parsed JSON objects.
 */
export function extractJSONBlocks(markdown: string): unknown[] {
  const codeBlockRegex = /```json\s*\n([\s\S]*?)```/g;
  const results: unknown[] = [];

  let match: RegExpExecArray | null;
  while ((match = codeBlockRegex.exec(markdown)) !== null) {
    try {
      results.push(JSON.parse(match[1]));
    } catch {
      // Skip malformed JSON blocks
    }
  }

  return results;
}
