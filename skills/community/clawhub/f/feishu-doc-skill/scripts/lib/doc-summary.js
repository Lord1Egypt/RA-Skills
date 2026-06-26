#!/usr/bin/env node

const MAX_SECTIONS = 12;
const MAX_LINES = 80;

function getTextFromElement(element) {
  for (const key of ['text_run', 'mention_user', 'mention_doc', 'equation', 'reminder']) {
    const value = element[key];
    if (!value || typeof value !== 'object') {
      continue;
    }
    if (Object.prototype.hasOwnProperty.call(value, 'content')) {
      return value.content || '';
    }
    if (Object.prototype.hasOwnProperty.call(value, 'text')) {
      return value.text || '';
    }
  }
  return '';
}

function blockToText(block) {
  const blockType = block.block_type;
  const typeName =
    {
      2: 'text',
      3: 'heading1',
      4: 'heading2',
      5: 'heading3',
      12: 'bullet',
      13: 'ordered',
      14: 'code',
      19: 'quote',
      31: 'table',
      32: 'callout',
      43: 'board',
    }[blockType] || `block_${blockType}`;

  let payload = null;
  for (const key of ['text', 'heading1', 'heading2', 'heading3', 'bullet', 'ordered', 'code', 'quote', 'callout', 'page']) {
    if (Object.prototype.hasOwnProperty.call(block, key)) {
      payload = block[key];
      break;
    }
  }

  if (!payload) {
    return [typeName, ''];
  }

  const elements = Array.isArray(payload.elements) ? payload.elements : [];
  const text = elements.map((element) => getTextFromElement(element)).join('').trim();
  return [typeName, text.replace(/\s+/g, ' ')];
}

function normalizeBlocks(blocks) {
  return blocks
    .map((block) => blockToText(block))
    .filter(([, text]) => Boolean(text));
}

function summarizeLines(lines) {
  const headings = [];
  const contentLines = [];
  const stats = {};

  for (const [kind, text] of lines) {
    if (!text) {
      continue;
    }
    stats[kind] = (stats[kind] || 0) + 1;
    if (kind.startsWith('heading')) {
      headings.push(text);
    } else if (['text', 'bullet', 'ordered', 'quote', 'callout'].includes(kind)) {
      contentLines.push(text);
    }
  }

  const preview = contentLines.slice(0, Math.min(8, contentLines.length));
  const keywords = [];
  for (const heading of headings) {
    if (heading.length >= 2 && !keywords.includes(heading)) {
      keywords.push(heading);
    }
    if (keywords.length >= 8) {
      break;
    }
  }

  return {
    headings: headings.slice(0, MAX_SECTIONS),
    preview,
    keywords,
    stats,
  };
}

function renderLine(kind, text) {
  if (kind === 'heading1') {
    return `## ${text}`;
  }
  if (kind === 'heading2') {
    return `### ${text}`;
  }
  if (kind === 'heading3') {
    return `#### ${text}`;
  }
  if (kind === 'bullet') {
    return `- ${text}`;
  }
  if (kind === 'ordered') {
    return `1. ${text}`;
  }
  if (kind === 'quote') {
    return `> ${text}`;
  }
  if (kind === 'code') {
    return `\`\`\`text\n${text}\n\`\`\``;
  }
  return text;
}

function compactPreview(lines) {
  return lines.filter(([, text]) => Boolean(text)).map(([kind, text]) => renderLine(kind, text));
}

function createReadUrlOutput(url, readDocData) {
  const metadata = readDocData?.metadata?.data?.document || {};
  const node = readDocData?.resolved_wiki_node?.data?.node || {};
  const blocks = readDocData?.blocks?.data?.items || [];
  const normalizedLines = normalizeBlocks(blocks);
  const summary = summarizeLines(normalizedLines);

  return {
    url,
    title: metadata.title || node.title || null,
    wiki_token: node.node_token || readDocData.input_token || null,
    doc_token: metadata.document_id || node.obj_token || null,
    token_source: readDocData.token_source || null,
    summary,
    content_preview: normalizedLines.slice(0, MAX_LINES),
  };
}

function renderMarkdownDocument(data) {
  const summary = data.summary || {};
  const contentPreview = Array.isArray(data.content_preview) ? data.content_preview : [];
  const lines = compactPreview(contentPreview);
  const parts = [
    `# ${data.title || '飞书文档'}`,
    '',
    '## 文档信息',
    `- 来源链接：${data.url || ''}`,
    `- Wiki Token：${data.wiki_token || ''}`,
    `- Doc Token：${data.doc_token || ''}`,
    `- Token 来源：${data.token_source || ''}`,
    '',
    '## 快速摘要',
  ];

  for (const item of summary.preview || []) {
    parts.push(`- ${item}`);
  }

  if ((summary.headings || []).length > 0) {
    parts.push('', '## 主要章节');
    for (const heading of summary.headings) {
      parts.push(`- ${heading}`);
    }
  }

  const stats = summary.stats || {};
  if (Object.keys(stats).length > 0) {
    parts.push('', '## 结构统计');
    for (const [key, value] of Object.entries(stats)) {
      parts.push(`- ${key}: ${value}`);
    }
  }

  parts.push('', '## 内容预览');
  parts.push(...lines);
  parts.push('');
  return parts.join('\n');
}

module.exports = {
  MAX_SECTIONS,
  MAX_LINES,
  getTextFromElement,
  blockToText,
  normalizeBlocks,
  summarizeLines,
  renderLine,
  compactPreview,
  createReadUrlOutput,
  renderMarkdownDocument,
};
