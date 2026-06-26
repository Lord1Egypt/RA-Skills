#!/usr/bin/env node
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { randomBytes } from 'crypto';

const API_KEY = process.env.CLAWAIMAIL_API_KEY;
const BASE_URL = process.env.CLAWAIMAIL_BASE_URL || 'https://api.clawaimail.com';

// Warn if API key is missing
if (!API_KEY) {
  console.error('[clawaimail] WARNING: CLAWAIMAIL_API_KEY not set. All API calls will fail.');
}

// Log unhandled errors and exit cleanly
process.on('uncaughtException', (err) => {
  console.error('[clawaimail] Uncaught exception:', err.message);
  process.exit(1);
});
process.on('unhandledRejection', (err) => {
  console.error('[clawaimail] Unhandled rejection:', err?.message || err);
  process.exit(1);
});

// Flexible ID schema: accepts number or numeric string
const idSchema = z.union([
  z.number(),
  z.string().transform((v) => {
    const n = Number(v);
    if (isNaN(n)) throw new Error(`Invalid ID: ${v}`);
    return n;
  })
]).describe('ID (number or numeric string)');

async function api(method, path, body) {
  try {
    if (!API_KEY) {
      return { error: 'CLAWAIMAIL_API_KEY not configured. Set it in your environment variables.' };
    }
    const opts = {
      method,
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      }
    };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(`${BASE_URL}${path}`, opts);
    const text = await res.text();
    let data;
    try {
      data = JSON.parse(text);
    } catch {
      return { error: `Server returned non-JSON response (HTTP ${res.status}): ${text.slice(0, 200)}` };
    }
    if (!res.ok) {
      return { error: data?.message || data?.error || `HTTP ${res.status}`, status: res.status, details: data };
    }
    return data;
  } catch (err) {
    return { error: `Request failed: ${err.message}` };
  }
}

// === Default inbox auto-provisioning ===
// Cached default inbox so we don't query every time
let _defaultInbox = null;

async function getDefaultInbox() {
  if (_defaultInbox) return _defaultInbox;

  // Check if user already has any inboxes
  const list = await api('GET', '/v1/inboxes');
  if (list.error) return { error: list.error };

  const inboxes = list.inboxes || list.data || list;
  if (Array.isArray(inboxes) && inboxes.length > 0) {
    _defaultInbox = inboxes[0];
    return _defaultInbox;
  }

  // No inboxes exist — auto-create one so the user can start immediately
  const randomName = `agent-${randomBytes(4).toString('hex')}`;
  console.error(`[clawaimail] No inboxes found. Creating default inbox: ${randomName}@clawaimail.com`);
  const created = await api('POST', '/v1/inboxes', { username: randomName });
  if (created.error) return { error: `Failed to auto-create inbox: ${created.error}` };

  _defaultInbox = created.inbox || created;
  console.error(`[clawaimail] Default inbox ready: ${_defaultInbox.address || randomName + '@clawaimail.com'}`);
  return _defaultInbox;
}

function inboxId(inbox) {
  return inbox?.id || inbox?.inbox_id;
}

const server = new McpServer({
  name: 'clawaimail',
  version: '0.2.1'
});

// === Tools ===

server.tool(
  'list_inboxes',
  'List all email inboxes',
  {},
  async () => {
    const result = await api('GET', '/v1/inboxes');
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'create_inbox',
  'Create a new email inbox (optional — a default inbox is auto-created if needed)',
  { username: z.string().describe('Email username (e.g. "mybot" creates mybot@clawaimail.com)') },
  async ({ username }) => {
    const result = await api('POST', '/v1/inboxes', { username });
    if (!result.error) _defaultInbox = null; // reset cache
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'send_email',
  'Send an email. If inbox_id is omitted, uses the default inbox (auto-created if needed).',
  {
    inbox_id: idSchema.optional().describe('Inbox ID to send from (optional, uses default inbox)'),
    to: z.string().describe('Recipient email address'),
    subject: z.string().describe('Email subject'),
    text: z.string().optional().describe('Plain text body'),
    html: z.string().optional().describe('HTML body')
  },
  async ({ inbox_id, to, subject, text, html }) => {
    if (!inbox_id) {
      const inbox = await getDefaultInbox();
      if (inbox.error) return { content: [{ type: 'text', text: JSON.stringify(inbox, null, 2) }] };
      inbox_id = inboxId(inbox);
    }
    const result = await api('POST', '/v1/messages/send', { inbox_id, to, subject, text, html });
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'list_messages',
  'List messages. If inbox_id is omitted, uses the default inbox.',
  {
    inbox_id: idSchema.optional().describe('Inbox ID (optional, uses default inbox)'),
    limit: z.number().optional().describe('Max messages to return (default 20)'),
    unread: z.boolean().optional().describe('Only show unread messages')
  },
  async ({ inbox_id, limit = 20, unread }) => {
    if (!inbox_id) {
      const inbox = await getDefaultInbox();
      if (inbox.error) return { content: [{ type: 'text', text: JSON.stringify(inbox, null, 2) }] };
      inbox_id = inboxId(inbox);
    }
    const params = new URLSearchParams({ limit: String(limit) });
    if (unread) params.set('unread', 'true');
    const result = await api('GET', `/v1/inboxes/${inbox_id}/messages?${params}`);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'read_email',
  'Read a specific email message. If inbox_id is omitted, uses the default inbox.',
  {
    inbox_id: idSchema.optional().describe('Inbox ID (optional, uses default inbox)'),
    message_id: idSchema.describe('Message ID')
  },
  async ({ inbox_id, message_id }) => {
    if (!inbox_id) {
      const inbox = await getDefaultInbox();
      if (inbox.error) return { content: [{ type: 'text', text: JSON.stringify(inbox, null, 2) }] };
      inbox_id = inboxId(inbox);
    }
    const result = await api('GET', `/v1/inboxes/${inbox_id}/messages/${message_id}`);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'search_emails',
  'Search emails by keyword. If inbox_id is omitted, uses the default inbox.',
  {
    inbox_id: idSchema.optional().describe('Inbox ID (optional, uses default inbox)'),
    query: z.string().describe('Search query')
  },
  async ({ inbox_id, query }) => {
    if (!inbox_id) {
      const inbox = await getDefaultInbox();
      if (inbox.error) return { content: [{ type: 'text', text: JSON.stringify(inbox, null, 2) }] };
      inbox_id = inboxId(inbox);
    }
    const params = new URLSearchParams({ q: query });
    const result = await api('GET', `/v1/inboxes/${inbox_id}/search?${params}`);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'delete_inbox',
  'Delete an inbox and all its messages',
  { inbox_id: idSchema.describe('Inbox ID to delete') },
  async ({ inbox_id }) => {
    const result = await api('DELETE', `/v1/inboxes/${inbox_id}`);
    if (!result.error) _defaultInbox = null; // reset cache
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'account_info',
  'Get account info, plan limits, and usage',
  {},
  async () => {
    const result = await api('GET', '/v1/me');
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'my_email',
  'Get your agent\'s email address (auto-creates one if none exists)',
  {},
  async () => {
    const inbox = await getDefaultInbox();
    if (inbox.error) return { content: [{ type: 'text', text: JSON.stringify(inbox, null, 2) }] };
    return { content: [{ type: 'text', text: JSON.stringify({
      email: inbox.email || inbox.address || `${inbox.username}@clawaimail.com`,
      inbox_id: inboxId(inbox),
      ...inbox
    }, null, 2) }] };
  }
);

// === Start ===

const transport = new StdioServerTransport();
await server.connect(transport);
