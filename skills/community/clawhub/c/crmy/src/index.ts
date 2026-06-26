// Copyright 2026 CRMy Contributors
// SPDX-License-Identifier: Apache-2.0
//
// CRMy plugin for OpenClaw
// Exposes 12 core CRM tools backed by the CRMy REST API.
// Config is read from ~/.crmy/config.json (written by `npx @crmy/cli init`).

import { resolveConfig, CrmyClient } from './client.js';

// OpenClaw plugin API type (minimal — we only use what we need)
interface ToolDef {
  id: string;
  name: string;
  description: string;
  input: {
    type: 'object';
    properties: Record<string, { type: string; description: string; enum?: string[] }>;
    required?: string[];
  };
  handler: (input: Record<string, unknown>) => Promise<unknown>;
}

interface OpenClawApi {
  registerTool(tool: ToolDef): void;
  config?: { serverUrl?: string; apiKey?: string };
  logger?: { info(msg: string): void; error(msg: string): void };
}

export default (api: OpenClawApi) => {
  const cfg = resolveConfig(api.config);
  const client = new CrmyClient(cfg);

  // ── 1. Global search ──────────────────────────────────────────────────────
  api.registerTool({
    id: 'crmy_search',
    name: 'CRMy: Search',
    description:
      'Search across all CRMy records — contacts, accounts, opportunities, activities, and more. ' +
      'Use this as a first step when you are not sure which record type the user is referring to.',
    input: {
      type: 'object',
      properties: {
        q:     { type: 'string', description: 'Search query' },
        limit: { type: 'number', description: 'Max results (default 10)' },
      },
      required: ['q'],
    },
    handler: async (input) => client.get('/search', { q: input.q as string, limit: (input.limit as number | undefined) ?? 10 }),
  });

  // ── 2. Contact search ─────────────────────────────────────────────────────
  api.registerTool({
    id: 'crmy_contact_search',
    name: 'CRMy: Search Contacts',
    description: 'Search for contacts by name, email, company, or any keyword. Supports optional lifecycle stage filter.',
    input: {
      type: 'object',
      properties: {
        q:       { type: 'string',  description: 'Search query (name, email, company, etc.)' },
        stage:   { type: 'string',  description: 'Filter by lifecycle stage (e.g. prospect, customer, churned)' },
        limit:   { type: 'number',  description: 'Max results (default 20)' },
      },
      required: ['q'],
    },
    handler: async (input) =>
      client.get('/contacts', { q: input.q as string, stage: input.stage as string, limit: (input.limit as number) ?? 20 }),
  });

  // ── 3. Contact create ─────────────────────────────────────────────────────
  api.registerTool({
    id: 'crmy_contact_create',
    name: 'CRMy: Create Contact',
    description: 'Create a new contact in CRMy. At minimum provide a name. Email, phone, title, and account_id are optional.',
    input: {
      type: 'object',
      properties: {
        name:         { type: 'string', description: 'Full name (required)' },
        email:        { type: 'string', description: 'Email address' },
        phone:        { type: 'string', description: 'Phone number' },
        title:        { type: 'string', description: 'Job title' },
        account_id:   { type: 'string', description: 'UUID of the associated account/company' },
        lifecycle_stage: { type: 'string', description: 'Initial lifecycle stage (e.g. prospect, lead, customer)' },
        notes:        { type: 'string', description: 'Any initial notes about this contact' },
      },
      required: ['name'],
    },
    handler: async (input) => client.post('/contacts', input),
  });

  // ── 4. Contact update ─────────────────────────────────────────────────────
  api.registerTool({
    id: 'crmy_contact_update',
    name: 'CRMy: Update Contact',
    description: 'Update fields on an existing contact. Provide the contact id and any fields to change.',
    input: {
      type: 'object',
      properties: {
        id:     { type: 'string', description: 'Contact UUID (required)' },
        name:   { type: 'string', description: 'Updated name' },
        email:  { type: 'string', description: 'Updated email' },
        phone:  { type: 'string', description: 'Updated phone' },
        title:  { type: 'string', description: 'Updated job title' },
        account_id: { type: 'string', description: 'Move to a different account UUID' },
      },
      required: ['id'],
    },
    handler: async ({ id, ...rest }) => client.patch(`/contacts/${id as string}`, rest),
  });

  // ── 5. Log activity (call, email, meeting, etc.) ──────────────────────────
  api.registerTool({
    id: 'crmy_contact_log_activity',
    name: 'CRMy: Log Activity',
    description:
      'Log a call, email, meeting, or other activity against a contact, account, or opportunity. ' +
      'Provide subject_type + subject_id to attach it to the right record.',
    input: {
      type: 'object',
      properties: {
        activity_type: {
          type: 'string',
          description: 'Type of activity — e.g. call, email, meeting, demo, proposal, note',
        },
        subject_type: {
          type: 'string',
          description: 'Record type the activity is attached to: contact, account, or opportunity',
          enum: ['contact', 'account', 'opportunity'],
        },
        subject_id:   { type: 'string', description: 'UUID of the contact, account, or opportunity' },
        summary:      { type: 'string', description: 'Short summary of what happened' },
        outcome:      { type: 'string', description: 'Outcome of the activity (e.g. positive, neutral, negative)' },
        performed_at: { type: 'string', description: 'ISO 8601 timestamp (defaults to now)' },
        duration_minutes: { type: 'number', description: 'Duration in minutes (for calls and meetings)' },
        notes:        { type: 'string', description: 'Detailed notes' },
      },
      required: ['activity_type', 'subject_type', 'subject_id', 'summary'],
    },
    handler: async (input) => client.post('/activities', input),
  });

  // ── 6. Set contact lifecycle stage ────────────────────────────────────────
  api.registerTool({
    id: 'crmy_contact_set_lifecycle',
    name: 'CRMy: Set Contact Lifecycle Stage',
    description: 'Change the lifecycle stage of a contact (e.g. lead → prospect → customer → churned).',
    input: {
      type: 'object',
      properties: {
        id:    { type: 'string', description: 'Contact UUID' },
        stage: { type: 'string', description: 'New lifecycle stage (e.g. lead, prospect, customer, churned)' },
        note:  { type: 'string', description: 'Optional note explaining the stage change' },
      },
      required: ['id', 'stage'],
    },
    handler: async ({ id, ...rest }) => client.patch(`/contacts/${id as string}`, rest),
  });

  // ── 7. Account search ─────────────────────────────────────────────────────
  api.registerTool({
    id: 'crmy_account_search',
    name: 'CRMy: Search Accounts',
    description: 'Search for companies/accounts by name, industry, or keyword.',
    input: {
      type: 'object',
      properties: {
        q:        { type: 'string', description: 'Search query (company name, domain, etc.)' },
        industry: { type: 'string', description: 'Filter by industry' },
        limit:    { type: 'number', description: 'Max results (default 20)' },
      },
      required: ['q'],
    },
    handler: async (input) =>
      client.get('/accounts', { q: input.q as string, industry: input.industry as string, limit: (input.limit as number) ?? 20 }),
  });

  // ── 8. Account create ─────────────────────────────────────────────────────
  api.registerTool({
    id: 'crmy_account_create',
    name: 'CRMy: Create Account',
    description: 'Create a new company/account record in CRMy.',
    input: {
      type: 'object',
      properties: {
        name:     { type: 'string', description: 'Company name (required)' },
        domain:   { type: 'string', description: 'Company website domain (e.g. acme.com)' },
        industry: { type: 'string', description: 'Industry sector' },
        size:     { type: 'string', description: 'Company size (e.g. 1-10, 11-50, 51-200, 201-1000, 1000+)' },
        notes:    { type: 'string', description: 'Any initial notes about this company' },
      },
      required: ['name'],
    },
    handler: async (input) => client.post('/accounts', input),
  });

  // ── 9. Opportunity search ─────────────────────────────────────────────────
  api.registerTool({
    id: 'crmy_opportunity_search',
    name: 'CRMy: Search Opportunities',
    description: 'Search for deals/opportunities by name, account, or stage.',
    input: {
      type: 'object',
      properties: {
        q:          { type: 'string', description: 'Search query (deal name, account, etc.)' },
        stage:      { type: 'string', description: 'Filter by deal stage (e.g. prospecting, proposal, closed_won)' },
        account_id: { type: 'string', description: 'Filter by account UUID' },
        limit:      { type: 'number', description: 'Max results (default 20)' },
      },
      required: ['q'],
    },
    handler: async (input) =>
      client.get('/opportunities', {
        q:          input.q as string,
        stage:      input.stage as string,
        account_id: input.account_id as string,
        limit:      (input.limit as number) ?? 20,
      }),
  });

  // ── 10. Opportunity create ────────────────────────────────────────────────
  api.registerTool({
    id: 'crmy_opportunity_create',
    name: 'CRMy: Create Opportunity',
    description: 'Create a new deal/opportunity in CRMy. Provide a name and optionally an account, value, and stage.',
    input: {
      type: 'object',
      properties: {
        name:       { type: 'string', description: 'Deal name (required)' },
        account_id: { type: 'string', description: 'Associated account UUID' },
        value:      { type: 'number', description: 'Deal value in your base currency' },
        stage:      { type: 'string', description: 'Initial deal stage (defaults to prospecting)' },
        close_date: { type: 'string', description: 'Expected close date (ISO 8601, e.g. 2026-06-30)' },
        notes:      { type: 'string', description: 'Any notes about this deal' },
      },
      required: ['name'],
    },
    handler: async (input) => client.post('/opportunities', input),
  });

  // ── 11. Advance opportunity stage ─────────────────────────────────────────
  api.registerTool({
    id: 'crmy_opportunity_advance_stage',
    name: 'CRMy: Advance Opportunity Stage',
    description: 'Move a deal to a new stage (e.g. proposal → negotiation → closed_won). Optionally add a note.',
    input: {
      type: 'object',
      properties: {
        id:          { type: 'string', description: 'Opportunity UUID (required)' },
        stage:       { type: 'string', description: 'New stage name (required)' },
        note:        { type: 'string', description: 'Note explaining the stage transition' },
        lost_reason: { type: 'string', description: 'If closing as lost, the reason' },
      },
      required: ['id', 'stage'],
    },
    handler: async ({ id, ...rest }) => client.patch(`/opportunities/${id as string}`, rest),
  });

  // ── 12. Pipeline summary ──────────────────────────────────────────────────
  api.registerTool({
    id: 'crmy_pipeline_summary',
    name: 'CRMy: Pipeline Summary',
    description:
      'Get a summary of the sales pipeline — total deal count and value by stage. ' +
      'Useful for answering questions like "how many deals do we have?" or "what is our pipeline worth?"',
    input: {
      type: 'object',
      properties: {
        group_by: {
          type: 'string',
          description: 'Group results by: stage (default), owner, or forecast_cat',
          enum: ['stage', 'owner', 'forecast_cat'],
        },
      },
    },
    handler: async (input) =>
      client.get('/analytics/pipeline', { group_by: (input.group_by as string) ?? 'stage' }),
  });
};
