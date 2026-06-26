#!/usr/bin/env node
import { asBool, asInt, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import {
  buildItemIdXml,
  callEwsOperation,
  ensureWriteConfirmed,
} from '../lib/ews-ops.mjs';
import { normalizeBodyType } from '../lib/mail-builders.mjs';
import { verifySentBySubject } from '../lib/sent-verify.mjs';
import {
  escapeXml,
  extractBlocks,
  getAttrValue,
  getNestedTagText,
  getResponseStatus,
  getTagText,
} from '../lib/xml-utils.mjs';

function normalizeMessageDisposition(args) {
  if (asBool(args.sendNow ?? true)) {
    return 'SendAndSaveCopy';
  }
  return 'SaveOnly';
}

async function getReferenceMessage(conn, itemId, changeKey) {
  const bodyXml = `<m:GetItem>
      <m:ItemShape>
        <t:BaseShape>IdOnly</t:BaseShape>
        <t:AdditionalProperties>
          <t:FieldURI FieldURI="item:Subject" />
          <t:FieldURI FieldURI="message:From" />
        </t:AdditionalProperties>
      </m:ItemShape>
      <m:ItemIds>
        ${buildItemIdXml(itemId, changeKey)}
      </m:ItemIds>
    </m:GetItem>`;

  const resp = await callEwsOperation({
    conn,
    operationName: 'GetItem(reference)',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/GetItem',
    bodyXml,
  });

  const block = extractBlocks(resp.body, 'Message')[0] || extractBlocks(resp.body, 'Item')[0] || '';
  if (!block) {
    return { subject: '', from_email: '', change_key: '' };
  }
  return {
    subject: getTagText(block, 'Subject'),
    from_email: getNestedTagText(block, 'From', 'EmailAddress'),
    change_key: getAttrValue(block, 'ItemId', 'ChangeKey'),
  };
}

try {
  const args = parseArgs();
  ensureWriteConfirmed(args, 'ReplyToItem');
  const conn = loadConnectionFromArgs(args);

  const itemId = args.itemId || args.id;
  if (!itemId) {
    throw new Error('itemId is required. Example: --item-id <EWS_ITEM_ID>');
  }

  const body = args.body || process.env.EXCHANGE_REPLY_BODY || '';
  if (!body) {
    throw new Error('reply body is required. Example: --body "..."');
  }

  const verifySent = asBool(args.verifySent ?? process.env.EXCHANGE_VERIFY_SENT ?? true);
  const verifyStrict = asBool(args.verifyStrict ?? process.env.EXCHANGE_VERIFY_STRICT);
  const verifyWindowMinutes = asInt(args.verifyWindowMinutes ?? process.env.EXCHANGE_VERIFY_WINDOW_MINUTES, 15);
  const verifyMaxEntries = asInt(args.verifyMaxEntries ?? process.env.EXCHANGE_VERIFY_MAX_ENTRIES, 100);

  const ref = await getReferenceMessage(conn, itemId, args.changeKey || process.env.EXCHANGE_CHANGE_KEY || '');
  const changeKey = args.changeKey || process.env.EXCHANGE_CHANGE_KEY || ref.change_key || '';
  if (!changeKey) {
    throw new Error('changeKey is required to reply to this item (missing current ChangeKey)');
  }
  const bodyType = normalizeBodyType(args.bodyType || process.env.EXCHANGE_BODY_TYPE || 'Text');
  const replyAll = asBool(args.replyAll ?? process.env.EXCHANGE_REPLY_ALL);
  const disposition = normalizeMessageDisposition(args);
  const replyNode = replyAll ? 'ReplyAllToItem' : 'ReplyToItem';
  const bodyXml = `<m:CreateItem MessageDisposition="${disposition}">
      <m:Items>
        <t:${replyNode}>
          <t:ReferenceItemId Id="${escapeXml(itemId)}" ChangeKey="${escapeXml(changeKey)}" />
          <t:NewBodyContent BodyType="${bodyType}">${escapeXml(body)}</t:NewBodyContent>
        </t:${replyNode}>
      </m:Items>
    </m:CreateItem>`;

  if (asBool(args.dryRun)) {
    console.log(
      JSON.stringify(
        {
          dry_run: true,
          operation: 'CreateItem',
          action: replyNode,
          message_disposition: disposition,
          verify_sent: verifySent,
          verify_window_minutes: verifyWindowMinutes,
          soap_action: 'http://schemas.microsoft.com/exchange/services/2006/messages/CreateItem',
          soap_body_preview: bodyXml,
        },
        null,
        2
      )
    );
    process.exit(0);
  }

  const sendStartedAt = Date.now();
  const resp = await callEwsOperation({
    conn,
    operationName: replyNode,
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/CreateItem',
    bodyXml,
  });
  const status = getResponseStatus(resp.body);
  if (status && status.response_class === 'Warning') {
    throw new Error(
      `Reply warning: ${status.code || 'Warning'} - ${status.message || 'Unknown EWS warning'}`
    );
  }

  const out = {
    ok: true,
    operation: 'CreateItem',
    action: replyNode,
    message_disposition: disposition,
    reference_item_id: itemId,
    reference_subject: ref.subject,
    reference_from_email: ref.from_email,
    item_id: '',
    change_key: '',
  };

  const replyItems = extractBlocks(resp.body, 'Message');
  if (replyItems.length > 0) {
    out.item_id = getAttrValue(replyItems[0], 'ItemId', 'Id') || '';
    out.change_key = getAttrValue(replyItems[0], 'ItemId', 'ChangeKey') || '';
  }

  if (
    verifySent &&
    (disposition === 'SendOnly' || disposition === 'SendAndSaveCopy')
  ) {
    const receipt = await verifySentBySubject({
      conn,
      subject: ref.subject,
      sentAfterMs: sendStartedAt,
      verifyWindowMinutes,
      maxEntries: verifyMaxEntries,
    });
    out.receipt_verification = receipt;
    if (verifyStrict && !receipt.verified) {
      throw new Error('Reply send completed but receipt verification failed in Sent Items');
    }
  }

  console.log(JSON.stringify(out, null, 2));
} catch (err) {
  console.error('reply-item failed:', err.message);
  process.exit(1);
}
