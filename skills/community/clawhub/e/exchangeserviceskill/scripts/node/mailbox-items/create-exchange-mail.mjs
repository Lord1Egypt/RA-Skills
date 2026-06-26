#!/usr/bin/env node
import { asBool, asInt, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import {
  buildFolderIdXml,
  callEwsOperation,
  ensureWriteConfirmed,
} from '../lib/ews-ops.mjs';
import {
  buildRecipientsXml,
  normalizeBodyType,
  parseRecipients,
} from '../lib/mail-builders.mjs';
import { verifySentBySubject } from '../lib/sent-verify.mjs';
import { escapeXml, getAttrValue } from '../lib/xml-utils.mjs';

function normalizeMessageDisposition(args) {
  if (asBool(args.sendNow)) {
    return 'SendAndSaveCopy';
  }
  const raw = String(args.messageDisposition || 'SaveOnly').trim();
  const supported = new Set(['SaveOnly', 'SendOnly', 'SendAndSaveCopy']);
  if (!supported.has(raw)) {
    throw new Error('messageDisposition must be SaveOnly, SendOnly, or SendAndSaveCopy');
  }
  return raw;
}

try {
  const args = parseArgs();
  ensureWriteConfirmed(args, 'CreateItem');
  const conn = loadConnectionFromArgs(args);

  const subject = args.subject || process.env.EXCHANGE_MAIL_SUBJECT || '';
  const body = args.body || process.env.EXCHANGE_MAIL_BODY || '';
  const bodyType = normalizeBodyType(args.bodyType || process.env.EXCHANGE_BODY_TYPE || 'Text');

  const toRecipients = parseRecipients(args.to || process.env.EXCHANGE_TO);
  const ccRecipients = parseRecipients(args.cc || process.env.EXCHANGE_CC);
  const bccRecipients = parseRecipients(args.bcc || process.env.EXCHANGE_BCC);

  if (!subject && !body) {
    throw new Error('At least one of subject or body is required');
  }
  if (toRecipients.length === 0 && asBool(args.requireTo ?? true)) {
    throw new Error('At least one --to recipient is required');
  }

  const disposition = normalizeMessageDisposition(args);

  let savedFolderXml = '';
  if (disposition === 'SaveOnly' || disposition === 'SendAndSaveCopy') {
    const saveFolderId = args.saveFolderId || process.env.EXCHANGE_SAVE_FOLDER_ID;
    const saveDistinguishedId = args.saveDistinguishedId || process.env.EXCHANGE_SAVE_DISTINGUISHED_ID || 'drafts';
    const saveMailbox = args.saveMailbox || process.env.EXCHANGE_SAVE_MAILBOX;
    savedFolderXml = `<m:SavedItemFolderId>${buildFolderIdXml({
      folderId: saveFolderId,
      distinguishedId: saveDistinguishedId,
      mailbox: saveMailbox,
    })}</m:SavedItemFolderId>`;
  }

  const bodyXml = `<m:CreateItem MessageDisposition="${disposition}">
      ${savedFolderXml}
      <m:Items>
        <t:Message>
          <t:Subject>${escapeXml(subject)}</t:Subject>
          <t:Body BodyType="${bodyType}">${escapeXml(body)}</t:Body>
          ${buildRecipientsXml('ToRecipients', toRecipients)}
          ${buildRecipientsXml('CcRecipients', ccRecipients)}
          ${buildRecipientsXml('BccRecipients', bccRecipients)}
        </t:Message>
      </m:Items>
    </m:CreateItem>`;

  if (asBool(args.dryRun)) {
    console.log(
      JSON.stringify(
        {
          dry_run: true,
          operation: 'CreateItem',
          message_disposition: disposition,
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
    operationName: 'CreateItem',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/CreateItem',
    bodyXml,
  });

  const out = {
    ok: true,
    operation: 'CreateItem',
    message_disposition: disposition,
    item_id: getAttrValue(resp.body, 'ItemId', 'Id'),
    change_key: getAttrValue(resp.body, 'ItemId', 'ChangeKey'),
  };

  const verifySent = asBool(args.verifySent ?? process.env.EXCHANGE_VERIFY_SENT ?? true);
  const verifyStrict = asBool(args.verifyStrict ?? process.env.EXCHANGE_VERIFY_STRICT);
  const verifyWindowMinutes = asInt(args.verifyWindowMinutes ?? process.env.EXCHANGE_VERIFY_WINDOW_MINUTES, 15);
  const verifyMaxEntries = asInt(args.verifyMaxEntries ?? process.env.EXCHANGE_VERIFY_MAX_ENTRIES, 100);

  if (
    verifySent &&
    (disposition === 'SendOnly' || disposition === 'SendAndSaveCopy')
  ) {
    const receipt = await verifySentBySubject({
      conn,
      subject,
      sentAfterMs: sendStartedAt,
      verifyWindowMinutes,
      maxEntries: verifyMaxEntries,
    });
    out.receipt_verification = receipt;
    if (verifyStrict && !receipt.verified) {
      throw new Error('CreateItem send completed but receipt verification failed in Sent Items');
    }
  }

  console.log(JSON.stringify(out, null, 2));
} catch (err) {
  console.error('create-mail failed:', err.message);
  process.exit(1);
}
