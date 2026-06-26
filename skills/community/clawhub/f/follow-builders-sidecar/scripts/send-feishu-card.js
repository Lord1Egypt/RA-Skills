#!/usr/bin/env node

import {
  cropAvatarToCircle,
  detectReceiveIdType,
  parseArgs,
  readStructuredInput,
  withAvatarTempDir,
  writeCardJson
} from './feishu-card-local.js';
import {
  resolveFeishuCredentials as resolveStoredFeishuCredentials,
  resolveOpenClawFeishuCredentials
} from './feishu-credential-resolver.js';
import {
  fetchAvatarBuffer,
  getTenantToken,
  sendCard,
  uploadImage
} from './feishu-card-api.js';

const DEFAULT_CARD_TITLE = 'AI Builders Daily';

function log(level, message, context = {}) {
  const payload = { level, message };
  if (Object.keys(context).length > 0) {
    payload.context = context;
  }
  if (level === 'error') {
    if (context.error && context.stack) {
      console.error(JSON.stringify(payload));
      return;
    }
    console.error(JSON.stringify(payload));
    return;
  }
  console.error(JSON.stringify(payload));
}

async function resolveFeishuCredentials(args) {
  return resolveStoredFeishuCredentials({
    mode: args.mode,
    accountId: args.accountId
  });
}

function clampItems(items) {
  if (!Array.isArray(items)) return [];
  return items.filter(Boolean);
}

function escapeMarkdownText(text) {
  return String(text || '')
    .replace(/\\/g, '\\\\')
    .replace(/\[/g, '\\[')
    .replace(/\]/g, '\\]')
    .replace(/\(/g, '\\(')
    .replace(/\)/g, '\\)');
}

function escapeBoldContent(text) {
  return escapeMarkdownText(text).replace(/\*/g, '\\*');
}

function buildTitleMarkdown(item) {
  const title = escapeBoldContent(item.headline || item.title || '原文');
  return `**${title}**`;
}

function normalizeHighlight(item) {
  if (!item) return null;
  if (typeof item === 'string') {
    return { label: '', detail: item };
  }
  const label = item.label || '';
  const detail = item.detail || item.text || '';
  if (!label && !detail) return null;
  return { label, detail };
}

function collapseWhitespace(text) {
  return String(text || '').replace(/\s+/g, ' ').trim();
}

function isInterpretiveSentence(text) {
  return /^(这意味着|意味着|值得注意的是|可以看出|说明了|背后的意思是|潜台词是|本质上|换句话说)/.test(collapseWhitespace(text));
}

function buildLegacyBodyFromHighlights(item) {
  const parts = [];
  const translation = collapseWhitespace(item.translation || item.subtitle || item.title_translation || '');
  if (translation) {
    parts.push(translation);
  }

  const highlightDetails = (Array.isArray(item.highlights) ? item.highlights : [])
    .map(normalizeHighlight)
    .filter(Boolean)
    .map((highlight) => collapseWhitespace(highlight.detail || ''))
    .filter((detail) => detail && !isInterpretiveSentence(detail));

  if (highlightDetails.length > 0) {
    parts.push(highlightDetails.join(' '));
  }

  return parts.join(' ');
}

function buildBodyMarkdown(item) {
  const body = collapseWhitespace(
    item.body
    || item.detail
    || item.summary_text
    || buildLegacyBodyFromHighlights(item)
  );
  if (!body) return '';
  return escapeMarkdownText(body);
}

function buildProfileMarkdown(item) {
  const profileUrl = item.profile_url || item.author_url || item.source_profile_url || item.source_url;
  const name = escapeBoldContent(item.person_name || item.name || 'Unknown Builder');
  const identity = escapeMarkdownText(item.person_identity || item.identity || item.role || item.source_label || 'AI Builder');
  const clickableName = profileUrl ? `[**${name}**](${profileUrl})` : `**${name}**`;
  const clickableIdentity = profileUrl ? `[${identity}](${profileUrl})` : identity;
  return `${clickableName}\n${clickableIdentity}`;
}

function buildMetaMarkdown(item) {
  const parts = [];
  if (item.source_label) parts.push(escapeMarkdownText(item.source_label));
  if (item.posted_at || item.published_at) parts.push(escapeMarkdownText(item.posted_at || item.published_at));
  return parts.join(' · ');
}

function buildProfileTextBlock(item) {
  const metaLine = buildMetaMarkdown(item);
  return [
    buildProfileMarkdown(item),
    metaLine
  ].filter(Boolean).join('\n');
}

function buildProfileElement(item, imageKey) {
  const profileContent = buildProfileTextBlock(item);

  if (!imageKey) {
    return {
      tag: 'div',
      text: {
        tag: 'lark_md',
        content: profileContent
      }
    };
  }

  return {
    tag: 'column_set',
    flex_mode: 'none',
    background_style: 'default',
    horizontal_spacing: '12px',
    columns: [
      {
        tag: 'column',
        width: '56px',
        vertical_align: 'top',
        elements: [
          {
            tag: 'img',
            img_key: imageKey,
            alt: { tag: 'plain_text', content: item.person_name || item.name || 'avatar' },
            preview: false
          }
        ]
      },
      {
        tag: 'column',
        width: 'weighted',
        weight: 1,
        vertical_align: 'top',
        elements: [
          {
            tag: 'div',
            text: {
              tag: 'lark_md',
              content: profileContent
            }
          }
        ]
      }
    ]
  };
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

function normalizeSourceLinks(item) {
  return normalizeSourceLinksList(item.source_links, item.source_url || item.url);
}

function buildSourceLinksMarkdown(item) {
  const links = normalizeSourceLinks(item);
  if (links.length === 0) return '';

  if (links.length === 1) {
    return `[${escapeMarkdownText(links[0].label)}](${links[0].url})`;
  }

  return links
    .map((link, index) => {
      const label = link.label || `查看原文 ${index + 1}`;
      return `[${escapeMarkdownText(label)}](${link.url})`;
    })
    .join(' · ');
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
    body: body || '',
    source_links: sourceLinks
  };
}

function extractSections(item) {
  const sections = (Array.isArray(item.sections) ? item.sections : [])
    .map(normalizeSection)
    .filter(Boolean);

  if (sections.length > 0) {
    return sections;
  }

  const legacySection = normalizeSection(item);
  return legacySection ? [legacySection] : [];
}

function isMissingImageUploadScopeError(error) {
  return /im:resource:upload|im:resource/i.test(String(error?.message || ''));
}

async function resolveAvatarUploadClient(primaryCreds, primaryToken, fallbackAccountId) {
  const fallbackCreds = await resolveOpenClawFeishuCredentials(fallbackAccountId);

  if (primaryCreds.accountId === fallbackCreds.accountId) {
    return { creds: primaryCreds, token: primaryToken };
  }

  const fallbackToken = await getTenantToken(fallbackCreds, log);
  log('info', 'Falling back to default Feishu account for avatar upload', {
    sendAccountId: primaryCreds.accountId,
    avatarAccountId: fallbackCreds.accountId
  });
  return { creds: fallbackCreds, token: fallbackToken };
}

async function resolveAvatarKeys(items, token, creds, avatarFallbackAccount = null) {
  const avatarKeys = new Map();
  let avatarClient = { creds, token };

  return withAvatarTempDir(async (tempDir) => {
    for (const item of items) {
      const itemKey = item.profile_url || item.source_url || item.person_handle || item.name;
      if (!itemKey) continue;
      try {
        const originalBuffer = await fetchAvatarBuffer(item, log);
        if (!originalBuffer) continue;
        const roundedBuffer = await cropAvatarToCircle(originalBuffer, tempDir);
        let imageKey;

        try {
          imageKey = await uploadImage(avatarClient.token, avatarClient.creds, roundedBuffer, log);
        } catch (error) {
          if (!isMissingImageUploadScopeError(error) || avatarClient.creds.accountId !== creds.accountId) {
            throw error;
          }

          avatarClient = await resolveAvatarUploadClient(creds, token, avatarFallbackAccount);
          imageKey = await uploadImage(avatarClient.token, avatarClient.creds, roundedBuffer, log);
        }

        avatarKeys.set(itemKey, imageKey);
      } catch (error) {
        log('warning', 'Avatar processing skipped for item', {
          person: item.person_name || item.name || 'unknown',
          error: error.message
        });
      }
    }
    return avatarKeys;
  });
}

function buildCard(payload, avatarKeys) {
  const dateText = payload.date || new Date().toISOString().slice(0, 10);
  const title = payload.title || `${DEFAULT_CARD_TITLE} · ${dateText}`;
  const summary = payload.summary || payload.top_takeaway || payload.subtitle || '';
  const items = clampItems(payload.items);

  const elements = [];

  if (summary) {
    elements.push({
      tag: 'div',
      text: {
        tag: 'lark_md',
        content: `**今日主线**\n${escapeMarkdownText(summary)}`
      }
    });
  }

  elements.push({
    tag: 'div',
    text: {
      tag: 'lark_md',
      content: `以下为本次抓取到的全部更新，共 ${items.length} 个来源。`
    }
  });

  elements.push({ tag: 'hr' });

  items.forEach((item, index) => {
    const profileKey = item.profile_url || item.source_url || item.person_handle || item.name;
    const imageKey = avatarKeys.get(profileKey);
    const sections = extractSections(item);
    elements.push(buildProfileElement(item, imageKey));

    sections.forEach((section, sectionIndex) => {
      elements.push({
        tag: 'div',
        text: {
          tag: 'lark_md',
          content: buildTitleMarkdown(section)
        }
      });

      const bodyMarkdown = buildBodyMarkdown(section);
      if (bodyMarkdown) {
        elements.push({
          tag: 'div',
          text: {
            tag: 'lark_md',
            content: bodyMarkdown
          }
        });
      }

      const sourceLinks = buildSourceLinksMarkdown(section);
      if (sourceLinks) {
        elements.push({
          tag: 'div',
          text: {
            tag: 'lark_md',
            content: sourceLinks
          }
        });
      }

      if (sectionIndex < sections.length - 1) {
        elements.push({ tag: 'hr' });
      }
    });

    if (index < items.length - 1) {
      elements.push({ tag: 'hr' });
    }
  });
  return {
    schema: '2.0',
    config: {
      wide_screen_mode: true,
      enable_forward: true
    },
    header: {
      title: {
        tag: 'plain_text',
        content: title
      },
      template: 'indigo'
    },
    body: {
      elements
    }
  };
}

function validatePayload(payload) {
  if (!payload || typeof payload !== 'object') {
    throw new Error('Payload must be a JSON object');
  }
  if (!Array.isArray(payload.items) || payload.items.length === 0) {
    throw new Error('Payload.items must contain at least one item');
  }
}

async function main() {
  const args = parseArgs(process.argv);
  log('info', 'Feishu card sender started', {
    file: args.file || 'stdin',
    accountId: args.accountId || 'default',
    mode: args.mode,
    dryRun: Boolean(args.dryRunFile || args.printCard)
  });

  const payload = await readStructuredInput(args.file);
  validatePayload(payload);

  const creds = await resolveFeishuCredentials(args);
  const token = await getTenantToken(creds, log);
  const items = clampItems(payload.items);
  const avatarKeys = await resolveAvatarKeys(items, token, creds, args.avatarFallbackAccount);
  const card = buildCard(payload, avatarKeys);

  if (args.dryRunFile) {
    await writeCardJson(args.dryRunFile, card);
    log('info', 'Card JSON written to dry-run file', { path: args.dryRunFile });
  }

  if (args.printCard) {
    process.stdout.write(`${JSON.stringify(card, null, 2)}\n`);
  }

  if (args.dryRunFile || args.printCard) {
    return;
  }

  if (!args.to) {
    throw new Error('Missing required argument: --to');
  }

  const receiveIdType = args.receiveIdType || detectReceiveIdType(args.to);
  const messageId = await sendCard(card, args.to, token, creds, receiveIdType, log);
  process.stdout.write(JSON.stringify({ status: 'ok', messageId }) + '\n');
}

main().catch((error) => {
  log('error', 'Feishu card sender failed', {
    error: error.message,
    stack: error.stack
  });
  process.exit(1);
});
