#!/usr/bin/env node
import { asBool, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import {
  buildFolderIdXml,
  callEwsOperation,
  ensureWriteConfirmed,
} from '../lib/ews-ops.mjs';

try {
  const args = parseArgs();
  ensureWriteConfirmed(args, 'MarkAllItemsAsRead');
  const conn = loadConnectionFromArgs(args);

  const folderId = args.folderId || args.id;
  const distinguishedId =
    args.distinguishedId ||
    args.distinguished ||
    process.env.EXCHANGE_DISTINGUISHED_ID ||
    'inbox';
  const mailbox = args.mailbox || process.env.EXCHANGE_MAILBOX;

  const readFlag = asBool(args.readFlag ?? process.env.EXCHANGE_READ_FLAG ?? true);
  const suppressReadReceipts = asBool(
    args.suppressReadReceipts ?? process.env.EXCHANGE_SUPPRESS_READ_RECEIPTS ?? true
  );

  const folderXml = buildFolderIdXml({
    folderId,
    distinguishedId,
    mailbox,
  });

  const bodyXml = `<m:MarkAllItemsAsRead ReadFlag="${readFlag ? 'true' : 'false'}" SuppressReadReceipts="${suppressReadReceipts ? 'true' : 'false'}">
      <m:FolderIds>
        ${folderXml}
      </m:FolderIds>
    </m:MarkAllItemsAsRead>`;

  if (asBool(args.dryRun)) {
    console.log(
      JSON.stringify(
        {
          dry_run: true,
          operation: 'MarkAllItemsAsRead',
          soap_action: 'http://schemas.microsoft.com/exchange/services/2006/messages/MarkAllItemsAsRead',
          soap_body_preview: bodyXml,
        },
        null,
        2
      )
    );
    process.exit(0);
  }

  await callEwsOperation({
    conn,
    operationName: 'MarkAllItemsAsRead',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/MarkAllItemsAsRead',
    bodyXml,
  });

  console.log(
    JSON.stringify(
      {
        ok: true,
        operation: 'MarkAllItemsAsRead',
        folder: folderId || distinguishedId,
        read_flag: readFlag,
        suppress_read_receipts: suppressReadReceipts,
      },
      null,
      2
    )
  );
} catch (err) {
  console.error('mark-all-read failed:', err.message);
  process.exit(1);
}
