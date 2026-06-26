#!/usr/bin/env node
import { asBool, asInt, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import {
  buildFolderIdXml,
  buildItemIdXml,
  callEwsOperation,
  ensureWriteConfirmed,
} from '../lib/ews-ops.mjs';
import { verifySentBySubject } from '../lib/sent-verify.mjs';
import { extractBlocks, getAttrValue, getResponseStatus, getTagText } from '../lib/xml-utils.mjs';

async function getDraftInfo(conn, itemId, changeKey) {
  const bodyXml = `<m:GetItem>
      <m:ItemShape>
        <t:BaseShape>IdOnly</t:BaseShape>
        <t:AdditionalProperties>
          <t:FieldURI FieldURI="item:Subject" />
        </t:AdditionalProperties>
      </m:ItemShape>
      <m:ItemIds>
        ${buildItemIdXml(itemId, changeKey)}
      </m:ItemIds>
    </m:GetItem>`;

  const resp = await callEwsOperation({
    conn,
    operationName: 'GetItem(draft)',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/GetItem',
    bodyXml,
  });

  const block = extractBlocks(resp.body, 'Message')[0] || extractBlocks(resp.body, 'Item')[0] || '';
  if (!block) {
    return { subject: '', change_key: '' };
  }
  return {
    subject: getTagText(block, 'Subject'),
    change_key: getAttrValue(block, 'ItemId', 'ChangeKey'),
  };
}

try {
  const args = parseArgs();
  ensureWriteConfirmed(args, 'SendItem');
  const conn = loadConnectionFromArgs(args);

  const itemId = args.itemId || args.id;
  if (!itemId) {
    throw new Error('itemId is required (draft message ID)');
  }
  const draft = await getDraftInfo(conn, itemId, args.changeKey);
  const subject = draft.subject;
  const changeKey = args.changeKey || draft.change_key;
  if (!changeKey) {
    throw new Error('changeKey is required to send this draft (missing current ChangeKey)');
  }

  const saveCopy = asBool(args.saveCopy ?? true);
  let savedFolderXml = '';
  if (saveCopy) {
    const folderXml = buildFolderIdXml({
      folderId: args.saveFolderId,
      distinguishedId: args.saveDistinguishedId || 'sentitems',
      mailbox: args.saveMailbox,
    });
    savedFolderXml = `<m:SavedItemFolderId>${folderXml}</m:SavedItemFolderId>`;
  }

  const bodyXml = `<m:SendItem SaveItemToFolder="${saveCopy ? 'true' : 'false'}">
      <m:ItemIds>
        ${buildItemIdXml(itemId, changeKey)}
      </m:ItemIds>
      ${savedFolderXml}
    </m:SendItem>`;

  if (asBool(args.dryRun)) {
    console.log(
      JSON.stringify(
        {
          dry_run: true,
          operation: 'SendItem',
          soap_action: 'http://schemas.microsoft.com/exchange/services/2006/messages/SendItem',
          soap_body_preview: bodyXml,
        },
        null,
        2
      )
    );
    process.exit(0);
  }

  const sendStartedAt = Date.now();
  const sendResp = await callEwsOperation({
    conn,
    operationName: 'SendItem',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/SendItem',
    bodyXml,
  });

  const status = getResponseStatus(sendResp.body);
  if (status && status.response_class === 'Warning') {
    throw new Error(
      `SendItem warning: ${status.code || 'Warning'} - ${status.message || 'Unknown EWS warning'}`
    );
  }

  console.log(
    JSON.stringify(await (async () => {
      const out = {
        ok: true,
        operation: 'SendItem',
        item_id: itemId,
        save_copy: saveCopy,
        subject,
      };

      const verifySent = asBool(args.verifySent ?? process.env.EXCHANGE_VERIFY_SENT ?? true);
      const verifyStrict = asBool(args.verifyStrict ?? process.env.EXCHANGE_VERIFY_STRICT);
      const verifyWindowMinutes = asInt(args.verifyWindowMinutes ?? process.env.EXCHANGE_VERIFY_WINDOW_MINUTES, 15);
      const verifyMaxEntries = asInt(args.verifyMaxEntries ?? process.env.EXCHANGE_VERIFY_MAX_ENTRIES, 100);

      if (verifySent && saveCopy) {
        const receipt = await verifySentBySubject({
          conn,
          subject,
          sentAfterMs: sendStartedAt,
          verifyWindowMinutes,
          maxEntries: verifyMaxEntries,
        });
        out.receipt_verification = receipt;
        if (verifyStrict && !receipt.verified) {
          throw new Error('SendItem completed but receipt verification failed in Sent Items');
        }
      }

      return out;
    })(), null, 2)
  );
} catch (err) {
  console.error('send-item failed:', err.message);
  process.exit(1);
}
