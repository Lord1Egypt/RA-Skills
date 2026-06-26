import { parse as parseYaml } from "yaml";
import type { ParsedSkill, SkillFrontmatter, CodeBlock } from "../types.js";

const FRONTMATTER_RE = /^---\r?\n([\s\S]*?)\r?\n---/;
const CODE_BLOCK_RE = /```(\w*)\r?\n([\s\S]*?)```/g;
const URL_RE = /https?:\/\/[^\s"'<>\])+]+/gi;
const IP_RE = /\b(?:\d{1,3}\.){3}\d{1,3}\b/g;
const DOMAIN_RE = /\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b/gi;

export function parseSkill(content: string): ParsedSkill {
  let frontmatter: SkillFrontmatter = {};
  let body = content;

  const fmMatch = content.match(FRONTMATTER_RE);
  if (fmMatch) {
    try {
      frontmatter = parseYaml(fmMatch[1]) as SkillFrontmatter;
    } catch {
      frontmatter = {};
    }
    body = content.slice(fmMatch[0].length).trim();
  }

  const codeBlocks: CodeBlock[] = [];
  let match: RegExpExecArray | null;
  const cbRe = new RegExp(CODE_BLOCK_RE.source, CODE_BLOCK_RE.flags);

  while ((match = cbRe.exec(content)) !== null) {
    const before = content.slice(0, match.index);
    const lineStart = before.split("\n").length;
    const blockLines = match[0].split("\n").length;
    codeBlocks.push({
      language: match[1] || "unknown",
      content: match[2],
      lineStart,
      lineEnd: lineStart + blockLines - 1,
    });
  }

  const urls = [...new Set(content.match(URL_RE) || [])];
  const ipAddresses = [...new Set(content.match(IP_RE) || [])];
  const domains = [...new Set(content.match(DOMAIN_RE) || [])];

  return {
    frontmatter,
    body,
    codeBlocks,
    urls,
    ipAddresses,
    domains,
    rawContent: content,
  };
}
