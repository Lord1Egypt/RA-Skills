#!/usr/bin/env node
import { asBool, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import {
  buildFolderIdXml,
  buildItemIdXml,
  callEwsOperation,
  ensureWriteConfirmed,
} from '../lib/ews-ops.mjs';
import { getAttrValue } from '../lib/xml-utils.mjs';

try {
  const args = parseArgs();
  ensureWriteConfirmed(args, 'ArchiveItem');
  const conn = loadConnectionFromArgs(args);

  const itemId = args.itemId || args.id;
  if (!itemId) {
    throw new Error('itemId is required');
  }

  const archiveFolderXml = buildFolderIdXml({
    folderId: args.archiveFolderId,
    distinguishedId: args.archiveDistinguishedId || 'archiveinbox',
    mailbox: args.archiveMailbox,
  });

  const bodyXml = `<m:MoveItem>
      <m:ToFolderId>
        ${archiveFolderXml}
      </m:ToFolderId>
      <m:ItemIds>
        ${buildItemIdXml(itemId, args.changeKey)}
      </m:ItemIds>
    </m:MoveItem>`;

  if (asBool(args.dryRun)) {
    console.log(
      JSON.stringify(
        {
          dry_run: true,
          operation: 'ArchiveItem',
          soap_action: 'http://schemas.microsoft.com/exchange/services/2006/messages/MoveItem',
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
    operationName: 'ArchiveItem',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/MoveItem',
    bodyXml,
  });

  console.log(
    JSON.stringify(
      {
        ok: true,
        operation: 'ArchiveItem',
        item_id: getAttrValue(resp.body, 'ItemId', 'Id'),
        change_key: getAttrValue(resp.body, 'ItemId', 'ChangeKey'),
      },
      null,
      2
    )
  );
} catch (err) {
  console.error('archive-item failed:', err.message);
  process.exit(1);
}
