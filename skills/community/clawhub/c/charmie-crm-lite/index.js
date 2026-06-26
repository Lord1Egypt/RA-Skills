#!/usr/bin/env node
require('dotenv').config();
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { CallToolRequestSchema, ListToolsRequestSchema } = require('@modelcontextprotocol/sdk/types.js');
const db = require('./db');

const server = new Server({ name: 'charmie-crm-lite', version: '3.0.3' }, { capabilities: { tools: {} } });

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    { name: 'search_contacts', description: 'Search contacts by name', inputSchema: { type: 'object', properties: { name: { type: 'string' } } } },
    { name: 'add_contact', description: 'Add a new contact', inputSchema: { type: 'object', properties: { name: { type: 'string' }, phone: { type: 'string' }, email: { type: 'string' }, notes: { type: 'string' } } } },
    { name: 'delete_contact', description: 'Delete contact by name', inputSchema: { type: 'object', properties: { name: { type: 'string' } } } },
    { name: 'update_contact', description: 'Update contact by name', inputSchema: { type: 'object', properties: { name: { type: 'string' }, newPhone: { type: 'string' }, newEmail: { type: 'string' }, newNotes: { type: 'string' } } } },
    { name: 'email_all', description: 'Send email to all contacts (Professional only)', inputSchema: { type: 'object', properties: { subject: { type: 'string' }, body: { type: 'string' } } } },
    { name: 'message_all', description: 'Send WhatsApp message to all contacts (Professional only)', inputSchema: { type: 'object', properties: { text: { type: 'string' } } } }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const args = req.params.arguments;
  switch (req.params.name) {
    case 'search_contacts': {
      const rows = await db.all('SELECT * FROM contacts WHERE name LIKE ?', [`%${args.name}%`]);
      return { content: [{ type: 'text', text: JSON.stringify(rows) }] };
    }
    case 'add_contact': {
      const { name, phone, email, notes } = args;
      const result = await db.run('INSERT INTO contacts (name, phone, email, notes) VALUES (?, ?, ?, ?)', [name, phone, email, notes]);
      return { content: [{ type: 'text', text: `Added contact with ID ${result.lastID}` }] };
    }
    case 'delete_contact': {
      await db.run('DELETE FROM contacts WHERE name = ?', [args.name]);
      return { content: [{ type: 'text', text: 'Deleted if existed' }] };
    }
    case 'update_contact': {
      const { name, newPhone, newEmail, newNotes } = args;
      await db.run('UPDATE contacts SET phone = ?, email = ?, notes = ? WHERE name = ?', [newPhone, newEmail, newNotes, name]);
      return { content: [{ type: 'text', text: 'Updated' }] };
    }
    case 'email_all':
    case 'message_all': {
      return {
        content: [{
          type: 'text',
          text: 'This feature is not available in the Lite version. Please upgrade to Professional for email and WhatsApp messaging. Visit https://BusinessBrainSolutions.WealthDaoinc.com/pro'
        }]
      };
    }
    default:
      throw new Error(`Unknown tool: ${req.params.name}`);
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}
main();
