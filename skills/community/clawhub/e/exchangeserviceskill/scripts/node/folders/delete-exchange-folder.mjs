#!/usr/bin/env node
import { asBool, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import {
  buildFolderIdXml,
  callEwsOperation,
  ensureWriteConfirmed,
  parseDeleteType,
} from '../lib/ews-ops.mjs';

try {
  const args = parseArgs();
  ensureWriteConfirmed(args, 'DeleteFolder');
  const conn = loadConnectionFromArgs(args);

  const folderId = args.folderId || args.id;
  const distinguishedId =
    args.distinguishedId ||
    args.distinguished ||
    process.env.EXCHANGE_DISTINGUISHED_ID;
  const mailbox = args.mailbox || process.env.EXCHANGE_MAILBOX;

  const deleteType = parseDeleteType(
    args.deleteType || process.env.EXCHANGE_DELETE_TYPE || 'MoveToDeletedItems'
  );

  const folderIdXml = buildFolderIdXml({
    folderId,
    distinguishedId,
    mailbox,
  });

  const bodyXml = `<m:DeleteFolder DeleteType="${deleteType}">
      <m:FolderIds>
        ${folderIdXml}
      </m:FolderIds>
    </m:DeleteFolder>`;

  if (asBool(args.dryRun)) {
    console.log(
      JSON.stringify(
        {
          dry_run: true,
          operation: 'DeleteFolder',
          delete_type: deleteType,
          soap_action: 'http://schemas.microsoft.com/exchange/services/2006/messages/DeleteFolder',
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
    operationName: 'DeleteFolder',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/DeleteFolder',
    bodyXml,
  });

  console.log(
    JSON.stringify(
      {
        ok: true,
        operation: 'DeleteFolder',
        delete_type: deleteType,
      },
      null,
      2
    )
  );
} catch (err) {
  console.error('delete-folder failed:', err.message);
  process.exit(1);
}
