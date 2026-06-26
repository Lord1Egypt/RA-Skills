#!/usr/bin/env node
import { parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import { buildFolderIdXml, callEwsOperation } from '../lib/ews-ops.mjs';
import { extractFolderBlocks, parseFolderBlock } from '../lib/folder-utils.mjs';

function buildFolderShapeXml(baseShape) {
  return `<m:FolderShape>
      <t:BaseShape>${baseShape}</t:BaseShape>
      <t:AdditionalProperties>
        <t:FieldURI FieldURI="folder:DisplayName" />
        <t:FieldURI FieldURI="folder:FolderClass" />
        <t:FieldURI FieldURI="folder:ParentFolderId" />
        <t:FieldURI FieldURI="folder:TotalCount" />
        <t:FieldURI FieldURI="folder:UnreadCount" />
        <t:FieldURI FieldURI="folder:ChildFolderCount" />
      </t:AdditionalProperties>
    </m:FolderShape>`;
}

try {
  const args = parseArgs();
  const conn = loadConnectionFromArgs(args);

  const folderId = args.folderId || args.id;
  const distinguishedId =
    args.distinguishedId ||
    args.distinguished ||
    process.env.EXCHANGE_DISTINGUISHED_ID ||
    'inbox';
  const mailbox = args.mailbox || process.env.EXCHANGE_MAILBOX;
  const baseShape =
    args.baseShape || process.env.EXCHANGE_BASE_SHAPE || 'IdOnly';

  const folderIdXml = buildFolderIdXml({
    folderId,
    distinguishedId,
    mailbox,
  });

  const bodyXml = `<m:GetFolder>
      ${buildFolderShapeXml(baseShape)}
      <m:FolderIds>
        ${folderIdXml}
      </m:FolderIds>
    </m:GetFolder>`;

  const resp = await callEwsOperation({
    conn,
    operationName: 'GetFolder',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/GetFolder',
    bodyXml,
  });

  const blocks = extractFolderBlocks(resp.body);
  if (blocks.length === 0) {
    throw new Error('No folder payload found in GetFolder response');
  }

  const out = parseFolderBlock(blocks[0]);
  console.log(JSON.stringify(out, null, 2));
} catch (err) {
  console.error('get-folder failed:', err.message);
  process.exit(1);
}
