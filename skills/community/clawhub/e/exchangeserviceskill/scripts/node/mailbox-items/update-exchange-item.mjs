#!/usr/bin/env node
import { asBool, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import {
  buildItemIdXml,
  callEwsOperation,
  ensureWriteConfirmed,
} from '../lib/ews-ops.mjs';
import { normalizeBodyType } from '../lib/mail-builders.mjs';
import { escapeXml, getAttrValue } from '../lib/xml-utils.mjs';

async function fetchChangeKey(conn, itemId) {
  const bodyXml = `<m:GetItem>
      <m:ItemShape>
        <t:BaseShape>IdOnly</t:BaseShape>
      </m:ItemShape>
      <m:ItemIds>
        <t:ItemId Id="${escapeXml(itemId)}" />
      </m:ItemIds>
    </m:GetItem>`;

  const resp = await callEwsOperation({
    conn,
    operationName: 'GetItem',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/GetItem',
    bodyXml,
  });

  const changeKey = getAttrValue(resp.body, 'ItemId', 'ChangeKey');
  if (!changeKey) {
    throw new Error('ChangeKey not found for item');
  }
  return changeKey;
}

function buildUpdates(args) {
  const updates = [];

  if (args.subject !== undefined) {
    updates.push(`<t:SetItemField>
          <t:FieldURI FieldURI="item:Subject" />
          <t:Message>
            <t:Subject>${escapeXml(args.subject)}</t:Subject>
          </t:Message>
        </t:SetItemField>`);
  }

  if (args.body !== undefined) {
    const bodyType = normalizeBodyType(args.bodyType || process.env.EXCHANGE_BODY_TYPE || 'Text');
    updates.push(`<t:SetItemField>
          <t:FieldURI FieldURI="item:Body" />
          <t:Message>
            <t:Body BodyType="${bodyType}">${escapeXml(args.body)}</t:Body>
          </t:Message>
        </t:SetItemField>`);
  }

  if (args.isRead !== undefined) {
    const isRead = asBool(args.isRead) ? 'true' : 'false';
    updates.push(`<t:SetItemField>
          <t:FieldURI FieldURI="message:IsRead" />
          <t:Message>
            <t:IsRead>${isRead}</t:IsRead>
          </t:Message>
        </t:SetItemField>`);
  }

  return updates;
}

try {
  const args = parseArgs();
  ensureWriteConfirmed(args, 'UpdateItem');
  const conn = loadConnectionFromArgs(args);

  const itemId = args.itemId || args.id;
  let changeKey = args.changeKey;
  if (!itemId) {
    throw new Error('itemId is required');
  }
  if (!changeKey) {
    changeKey = await fetchChangeKey(conn, itemId);
  }

  const updates = buildUpdates(args);
  if (updates.length === 0) {
    throw new Error('No updates requested. Use --subject, --body, or --is-read.');
  }

  const conflictResolution = args.conflictResolution || 'AutoResolve';
  const messageDisposition = args.messageDisposition || 'SaveOnly';

  const bodyXml = `<m:UpdateItem ConflictResolution="${conflictResolution}" MessageDisposition="${messageDisposition}" SendMeetingInvitationsOrCancellations="SendToNone">
      <m:ItemChanges>
        <t:ItemChange>
          ${buildItemIdXml(itemId, changeKey)}
          <t:Updates>
            ${updates.join('\n')}
          </t:Updates>
        </t:ItemChange>
      </m:ItemChanges>
    </m:UpdateItem>`;

  if (asBool(args.dryRun)) {
    console.log(
      JSON.stringify(
        {
          dry_run: true,
          operation: 'UpdateItem',
          soap_action: 'http://schemas.microsoft.com/exchange/services/2006/messages/UpdateItem',
          soap_body_preview: bodyXml,
        },
        null,
        2
      )
    );
    process.exit(0);
  }

  const resp = await callEwsOperation({
    conn,
    operationName: 'UpdateItem',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/UpdateItem',
    bodyXml,
  });

  const out = {
    ok: true,
    operation: 'UpdateItem',
    item_id: getAttrValue(resp.body, 'ItemId', 'Id'),
    change_key: getAttrValue(resp.body, 'ItemId', 'ChangeKey'),
  };
  console.log(JSON.stringify(out, null, 2));
} catch (err) {
  console.error('update-item failed:', err.message);
  process.exit(1);
}
