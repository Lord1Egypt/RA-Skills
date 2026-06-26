#!/usr/bin/env node
import { asBool, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import {
  callEwsOperation,
  ensureWriteConfirmed,
} from '../lib/ews-ops.mjs';
import { escapeXml, getAttrValue } from '../lib/xml-utils.mjs';

function buildUpdates(args) {
  const updates = [];

  if (args.displayName !== undefined || args.name !== undefined) {
    const displayName = args.displayName ?? args.name ?? '';
    updates.push(`<t:SetFolderField>
          <t:FieldURI FieldURI="folder:DisplayName" />
          <t:Folder>
            <t:DisplayName>${escapeXml(displayName)}</t:DisplayName>
          </t:Folder>
        </t:SetFolderField>`);
  }

  if (args.folderClass !== undefined) {
    updates.push(`<t:SetFolderField>
          <t:FieldURI FieldURI="folder:FolderClass" />
          <t:Folder>
            <t:FolderClass>${escapeXml(args.folderClass)}</t:FolderClass>
          </t:Folder>
        </t:SetFolderField>`);
  }

  return updates;
}

try {
  const args = parseArgs();
  ensureWriteConfirmed(args, 'UpdateFolder');
  const conn = loadConnectionFromArgs(args);

  const folderId = args.folderId || args.id;
  const changeKey = args.changeKey;
  if (!folderId || !changeKey) {
    throw new Error('folderId and changeKey are required');
  }

  const updates = buildUpdates(args);
  if (updates.length === 0) {
    throw new Error('No updates requested. Use --display-name or --folder-class.');
  }

  const conflictResolution =
    args.conflictResolution || process.env.EXCHANGE_CONFLICT_RESOLUTION || 'AutoResolve';

  const bodyXml = `<m:UpdateFolder ConflictResolution="${conflictResolution}">
      <m:FolderChanges>
        <t:FolderChange>
          <t:FolderId Id="${escapeXml(folderId)}" ChangeKey="${escapeXml(changeKey)}" />
          <t:Updates>
            ${updates.join('\n')}
          </t:Updates>
        </t:FolderChange>
      </m:FolderChanges>
    </m:UpdateFolder>`;

  if (asBool(args.dryRun)) {
    console.log(
      JSON.stringify(
        {
          dry_run: true,
          operation: 'UpdateFolder',
          soap_action: 'http://schemas.microsoft.com/exchange/services/2006/messages/UpdateFolder',
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
    operationName: 'UpdateFolder',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/UpdateFolder',
    bodyXml,
  });

  const out = {
    ok: true,
    operation: 'UpdateFolder',
    folder_id: getAttrValue(resp.body, 'FolderId', 'Id'),
    change_key: getAttrValue(resp.body, 'FolderId', 'ChangeKey'),
  };
  console.log(JSON.stringify(out, null, 2));
} catch (err) {
  console.error('update-folder failed:', err.message);
  process.exit(1);
}
