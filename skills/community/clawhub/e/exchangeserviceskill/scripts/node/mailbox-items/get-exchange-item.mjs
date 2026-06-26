#!/usr/bin/env node
import { asBool, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import { buildItemIdXml, callEwsOperation } from '../lib/ews-ops.mjs';
import {
  extractBlocks,
  getAttrValue,
  getNestedTagText,
  getTagText,
} from '../lib/xml-utils.mjs';

function getParentBlock(xml, localName) {
  const pattern = new RegExp(
    `<(?:\\w+:)?${localName}\\b[\\s\\S]*?<\\/(?:\\w+:)?${localName}>`,
    'i'
  );
  const m = String(xml || '').match(pattern);
  return m ? m[0] : '';
}

function parseRecipients(itemBlock, parentTag) {
  const parent = getParentBlock(itemBlock, parentTag);
  if (!parent) {
    return [];
  }

  return extractBlocks(parent, 'Mailbox').map((mailbox) => ({
    name: getTagText(mailbox, 'Name'),
    email: getTagText(mailbox, 'EmailAddress'),
    routing_type: getTagText(mailbox, 'RoutingType'),
    mailbox_type: getTagText(mailbox, 'MailboxType'),
  }));
}

function parseAttachments(itemBlock) {
  const files = extractBlocks(itemBlock, 'FileAttachment').map((block) => ({
    kind: 'file',
    id: getAttrValue(block, 'AttachmentId', 'Id'),
    name: getTagText(block, 'Name'),
    content_type: getTagText(block, 'ContentType'),
    size: Number.parseInt(getTagText(block, 'Size') || '0', 10) || 0,
    inline: String(getTagText(block, 'IsInline')).toLowerCase() === 'true',
  }));

  const items = extractBlocks(itemBlock, 'ItemAttachment').map((block) => ({
    kind: 'item',
    id: getAttrValue(block, 'AttachmentId', 'Id'),
    name: getTagText(block, 'Name'),
    size: Number.parseInt(getTagText(block, 'Size') || '0', 10) || 0,
  }));

  return [...files, ...items];
}

function formatAddress(name, email) {
  const n = String(name || '').trim();
  const e = String(email || '').trim();
  if (n && e && n.toLowerCase() !== e.toLowerCase()) {
    return `${n}(${e})`;
  }
  return e || n;
}

function pickItemBlock(xml) {
  const candidates = ['Message', 'CalendarItem', 'Task', 'Contact', 'MeetingRequest', 'Item'];
  for (const name of candidates) {
    const block = extractBlocks(xml, name)[0];
    if (block) {
      return { kind: name, block };
    }
  }
  return { kind: '', block: '' };
}

try {
  const args = parseArgs();
  const conn = loadConnectionFromArgs(args);

  const itemId = args.itemId || args.id;
  if (!itemId) {
    throw new Error('itemId is required. Example: --item-id <EWS_ITEM_ID>');
  }

  const includeMime = asBool(args.includeMimeContent);
  const bodyType = args.bodyType || process.env.EXCHANGE_BODY_TYPE || 'Best';
  const baseShape = args.baseShape || process.env.EXCHANGE_BASE_SHAPE || 'AllProperties';

  const bodyXml = `<m:GetItem>
      <m:ItemShape>
        <t:BaseShape>${baseShape}</t:BaseShape>
        <t:BodyType>${bodyType}</t:BodyType>
        <t:IncludeMimeContent>${includeMime ? 'true' : 'false'}</t:IncludeMimeContent>
      </m:ItemShape>
      <m:ItemIds>
        ${buildItemIdXml(itemId, args.changeKey)}
      </m:ItemIds>
    </m:GetItem>`;

  const resp = await callEwsOperation({
    conn,
    operationName: 'GetItem',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/GetItem',
    bodyXml,
  });

  const picked = pickItemBlock(resp.body);
  if (!picked.block) {
    throw new Error('No item payload found in GetItem response');
  }

  const itemBlock = picked.block;
  const fromName = getNestedTagText(itemBlock, 'From', 'Name');
  const fromEmail = getNestedTagText(itemBlock, 'From', 'EmailAddress');
  const senderName = getNestedTagText(itemBlock, 'Sender', 'Name');
  const senderEmail = getNestedTagText(itemBlock, 'Sender', 'EmailAddress');

  const out = {
    kind: picked.kind,
    id: getAttrValue(itemBlock, 'ItemId', 'Id'),
    change_key: getAttrValue(itemBlock, 'ItemId', 'ChangeKey'),
    subject: getTagText(itemBlock, 'Subject'),
    item_class: getTagText(itemBlock, 'ItemClass'),
    from: formatAddress(fromName, fromEmail),
    from_name: fromName,
    from_email: fromEmail,
    sender: formatAddress(senderName, senderEmail),
    sender_name: senderName,
    sender_email: senderEmail,
    received: getTagText(itemBlock, 'DateTimeReceived'),
    created: getTagText(itemBlock, 'DateTimeCreated'),
    sent: getTagText(itemBlock, 'DateTimeSent'),
    is_read: String(getTagText(itemBlock, 'IsRead')).toLowerCase() === 'true',
    body_type: getAttrValue(itemBlock, 'Body', 'BodyType'),
    body: getTagText(itemBlock, 'Body'),
    to_recipients: parseRecipients(itemBlock, 'ToRecipients'),
    cc_recipients: parseRecipients(itemBlock, 'CcRecipients'),
    bcc_recipients: parseRecipients(itemBlock, 'BccRecipients'),
    attachments: parseAttachments(itemBlock),
    has_attachments: String(getTagText(itemBlock, 'HasAttachments')).toLowerCase() === 'true',
  };

  if (includeMime) {
    out.mime_content_b64 = getTagText(itemBlock, 'MimeContent');
  }

  console.log(JSON.stringify(out, null, 2));
} catch (err) {
  console.error('get-item failed:', err.message);
  process.exit(1);
}
