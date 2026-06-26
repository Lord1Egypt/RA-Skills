#!/usr/bin/env node

import { readFile } from 'fs/promises';
import { fileURLToPath } from 'url';

function collapseWhitespace(value) {
  return String(value || '').replace(/\s+/g, ' ').trim();
}

function normalizeSourceLinksList(entries = [], fallbackUrl = null) {
  const links = [];
  if (Array.isArray(entries)) {
    for (const entry of entries) {
      if (!entry) continue;
      if (typeof entry === 'string') {
        links.push({ label: '查看原文', url: entry });
        continue;
      }
      if (entry.url) {
        links.push({
          label: entry.label || '查看原文',
          url: entry.url
        });
      }
    }
  }

  if (links.length === 0 && fallbackUrl) {
    links.push({ label: '查看原文', url: fallbackUrl });
  }

  return links;
}

function buildLegacyBodyFromHighlights(item) {
  const translation = collapseWhitespace(
    item.translation
    || item.subtitle
    || item.title_translation
    || ''
  );
  const highlights = (Array.isArray(item.highlights) ? item.highlights : [])
    .map((highlight) => {
      if (!highlight) return '';
      if (typeof highlight === 'string') return collapseWhitespace(highlight);
      return collapseWhitespace(highlight.detail || highlight.text || '');
    })
    .filter(Boolean)
    .join(' ');

  return [translation, highlights].filter(Boolean).join(' ');
}

function normalizeSection(item) {
  if (!item || typeof item !== 'object') return null;
  const sourceLinks = normalizeSourceLinksList(item.source_links, item.source_url || item.url);
  const body = collapseWhitespace(
    item.body
    || item.detail
    || item.summary_text
    || buildLegacyBodyFromHighlights(item)
  );
  const headline = collapseWhitespace(item.headline || item.title || '');

  if (!headline && !body && sourceLinks.length === 0) return null;

  return {
    headline: headline || sourceLinks[0]?.label || '原文',
    body,
    sourceLinks
  };
}

function extractSections(item) {
  const sections = (Array.isArray(item.sections) ? item.sections : [])
    .map((section) => normalizeSection(section))
    .filter(Boolean);

  if (sections.length > 0) {
    return sections;
  }

  const fallback = normalizeSection(item);
  return fallback ? [fallback] : [];
}

function renderSourceLinks(sourceLinks) {
  if (!Array.isArray(sourceLinks) || sourceLinks.length === 0) {
    return [];
  }
  return sourceLinks.map((link) => `${link.label || '查看原文'}：${link.url}`);
}

function renderItem(item, index) {
  const lines = [];
  const title = collapseWhitespace(item.person_name || item.name || `来源 ${index + 1}`);
  const identity = [
    collapseWhitespace(item.person_identity || item.identity || item.role || ''),
    collapseWhitespace(item.source_label || ''),
    collapseWhitespace(item.posted_at || item.published_at || '')
  ].filter(Boolean).join(' · ');

  lines.push(`${index + 1}. ${title}`);
  if (identity) {
    lines.push(identity);
  }

  const sections = extractSections(item);
  sections.forEach((section, sectionIndex) => {
    if (sectionIndex === 0) {
      lines.push('');
    } else {
      lines.push('');
      lines.push('---');
      lines.push('');
    }
    lines.push(section.headline);
    if (section.body) {
      lines.push(section.body);
    }
    lines.push(...renderSourceLinks(section.sourceLinks));
  });

  return lines.join('\n');
}

function renderDigestText(payload) {
  if (!payload || typeof payload !== 'object') {
    throw new Error('Payload must be a JSON object');
  }
  if (!Array.isArray(payload.items) || payload.items.length === 0) {
    throw new Error('Payload.items must contain at least one item');
  }

  const lines = [];
  lines.push(collapseWhitespace(payload.title || 'AI Builders Daily'));

  const summary = collapseWhitespace(payload.summary || payload.top_takeaway || payload.subtitle || '');
  if (summary) {
    lines.push('');
    lines.push(summary);
  }

  payload.items.forEach((item, index) => {
    lines.push('');
    lines.push('');
    lines.push(renderItem(item, index));
  });

  return `${lines.join('\n').trim()}\n`;
}

async function main() {
  const filePath = process.argv[2];
  if (!filePath) {
    throw new Error('Usage: node render-openclaw-digest.js <payload.json>');
  }
  const payload = JSON.parse(await readFile(filePath, 'utf-8'));
  process.stdout.write(renderDigestText(payload));
}

export {
  renderDigestText
};

const IS_ENTRYPOINT = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];

if (IS_ENTRYPOINT) {
  main().catch((error) => {
    console.error(JSON.stringify({
      status: 'error',
      message: error.message
    }));
    process.exit(1);
  });
}
