#!/usr/bin/env node
import { asBool, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import {
  buildFolderIdXml,
  callEwsOperation,
  ensureWriteConfirmed,
} from '../lib/ews-ops.mjs';
import { escapeXml, getAttrValue } from '../lib/xml-utils.mjs';

try {
  const args = parseArgs();
  ensureWriteConfirmed(args, 'CreateFolder');
  const conn = loadConnectionFromArgs(args);

  const displayName =
    args.displayName ||
    args.name ||
    process.env.EXCHANGE_FOLDER_NAME ||
    '';
  if (!displayName) {
    throw new Error('displayName is required. Example: --display-name "My Folder"');
  }

  const folderClass = args.folderClass || process.env.EXCHANGE_FOLDER_CLASS;

  const parentFolderId =
    args.parentFolderId ||
    args.parentId ||
    process.env.EXCHANGE_PARENT_FOLDER_ID;
  const parentDistinguishedId =
    args.parentDistinguishedId ||
    args.parentDistinguished ||
    process.env.EXCHANGE_PARENT_DISTINGUISHED_ID ||
    'msgfolderroot';
  const parentMailbox =
    args.parentMailbox ||
    process.env.EXCHANGE_PARENT_MAILBOX;

  const parentFolderXml = buildFolderIdXml({
    folderId: parentFolderId,
    distinguishedId: parentDistinguishedId,
    mailbox: parentMailbox,
  });

  const classXml = folderClass
    ? `<t:FolderClass>${escapeXml(folderClass)}</t:FolderClass>`
    : '';

  const bodyXml = `<m:CreateFolder>
      <m:ParentFolderId>
        ${parentFolderXml}
      </m:ParentFolderId>
      <m:Folders>
        <t:Folder>
          <t:DisplayName>${escapeXml(displayName)}</t:DisplayName>
          ${classXml}
        </t:Folder>
      </m:Folders>
    </m:CreateFolder>`;

  if (asBool(args.dryRun)) {
    console.log(
      JSON.stringify(
        {
          dry_run: true,
          operation: 'CreateFolder',
          soap_action: 'http://schemas.microsoft.com/exchange/services/2006/messages/CreateFolder',
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
    operationName: 'CreateFolder',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/CreateFolder',
    bodyXml,
  });

  const out = {
    ok: true,
    operation: 'CreateFolder',
    folder_id: getAttrValue(resp.body, 'FolderId', 'Id'),
    change_key: getAttrValue(resp.body, 'FolderId', 'ChangeKey'),
  };

  console.log(JSON.stringify(out, null, 2));
} catch (err) {
  console.error('create-folder failed:', err.message);
  process.exit(1);
}
