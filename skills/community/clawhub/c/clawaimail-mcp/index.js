#!/usr/bin/env node
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

const API_KEY = process.env.CLAWAIMAIL_API_KEY;
const BASE_URL = process.env.CLAWAIMAIL_BASE_URL || 'https://api.clawaimail.com';

async function api(method, path, body) {
  const opts = {
    method,
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json'
    }
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(`${BASE_URL}${path}`, opts);
  return res.json();
}

const server = new McpServer({
  name: 'clawaimail',
  version: '0.1.0'
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
  'Create a new email inbox',
  { username: z.string().describe('Email username (e.g. "mybot" creates mybot@clawaimail.com)') },
  async ({ username }) => {
    const result = await api('POST', '/v1/inboxes', { username });
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'send_email',
  'Send an email from an inbox',
  {
    inbox_id: z.number().describe('Inbox ID to send from'),
    to: z.string().describe('Recipient email address'),
    subject: z.string().describe('Email subject'),
    text: z.string().optional().describe('Plain text body'),
    html: z.string().optional().describe('HTML body')
  },
  async ({ inbox_id, to, subject, text, html }) => {
    const result = await api('POST', '/v1/messages/send', { inbox_id, to, subject, text, html });
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'list_messages',
  'List messages in an inbox',
  {
    inbox_id: z.number().describe('Inbox ID'),
    limit: z.number().optional().describe('Max messages to return (default 20)'),
    unread: z.boolean().optional().describe('Only show unread messages')
  },
  async ({ inbox_id, limit = 20, unread }) => {
    const params = new URLSearchParams({ limit });
    if (unread) params.set('unread', 'true');
    const result = await api('GET', `/v1/inboxes/${inbox_id}/messages?${params}`);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'read_email',
  'Read a specific email message',
  {
    inbox_id: z.number().describe('Inbox ID'),
    message_id: z.number().describe('Message ID')
  },
  async ({ inbox_id, message_id }) => {
    const result = await api('GET', `/v1/inboxes/${inbox_id}/messages/${message_id}`);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'search_emails',
  'Search emails by keyword',
  {
    inbox_id: z.number().describe('Inbox ID'),
    query: z.string().describe('Search query')
  },
  async ({ inbox_id, query }) => {
    const params = new URLSearchParams({ q: query });
    const result = await api('GET', `/v1/inboxes/${inbox_id}/search?${params}`);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'delete_inbox',
  'Delete an inbox and all its messages',
  { inbox_id: z.number().describe('Inbox ID to delete') },
  async ({ inbox_id }) => {
    const result = await api('DELETE', `/v1/inboxes/${inbox_id}`);
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

// === Start ===

const transport = new StdioServerTransport();
await server.connect(transport);
