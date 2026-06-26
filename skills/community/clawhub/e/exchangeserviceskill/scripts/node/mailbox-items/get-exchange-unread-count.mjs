#!/usr/bin/env node
import { asInt, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import { callEwsOperation } from '../lib/ews-ops.mjs';
import { escapeXml, extractBlocks, getAttrValue, getTagText } from '../lib/xml-utils.mjs';

function buildRootRefXml(scope) {
  const raw = String(scope || 'inbox').trim().toLowerCase();
  const map = {
    inbox: 'inbox',
    msgfolderroot: 'msgfolderroot',
    root: 'msgfolderroot',
    all: 'msgfolderroot',
  };
  const id = map[raw] || raw;
  return `<t:DistinguishedFolderId Id="${escapeXml(id)}" />`;
}

function buildFindFolderBody({ rootXml, offset, pageSize }) {
  return `<m:FindFolder Traversal="Deep">
      <m:FolderShape>
        <t:BaseShape>IdOnly</t:BaseShape>
        <t:AdditionalProperties>
          <t:FieldURI FieldURI="folder:DisplayName" />
          <t:FieldURI FieldURI="folder:UnreadCount" />
          <t:FieldURI FieldURI="folder:TotalCount" />
          <t:FieldURI FieldURI="folder:ParentFolderId" />
        </t:AdditionalProperties>
      </m:FolderShape>
      <m:IndexedPageFolderView MaxEntriesReturned="${pageSize}" Offset="${offset}" BasePoint="Beginning" />
      <m:ParentFolderIds>
        ${rootXml}
      </m:ParentFolderIds>
    </m:FindFolder>`;
}

function buildGetFolderBody({ rootXml }) {
  return `<m:GetFolder>
      <m:FolderShape>
        <t:BaseShape>IdOnly</t:BaseShape>
        <t:AdditionalProperties>
          <t:FieldURI FieldURI="folder:DisplayName" />
          <t:FieldURI FieldURI="folder:UnreadCount" />
          <t:FieldURI FieldURI="folder:TotalCount" />
          <t:FieldURI FieldURI="folder:ParentFolderId" />
        </t:AdditionalProperties>
      </m:FolderShape>
      <m:FolderIds>
        ${rootXml}
      </m:FolderIds>
    </m:GetFolder>`;
}

function folderIdOf(block) {
  return getAttrValue(block, 'FolderId', 'Id') || getAttrValue(block, 'SearchFolderId', 'Id') || '';
}

try {
  const args = parseArgs();
  const conn = loadConnectionFromArgs(args);

  const scope = args.scope || process.env.EXCHANGE_UNREAD_SCOPE || 'inbox';
  const pageSize = asInt(args.pageSize ?? process.env.EXCHANGE_FOLDER_PAGE_SIZE, 200);
  const maxPages = asInt(args.maxPages ?? process.env.EXCHANGE_MAX_FOLDER_PAGES, 200);
  const nameFilter = args.folderName || process.env.EXCHANGE_FOLDER_NAME || '';

  const rootXml = buildRootRefXml(scope);
  const folders = [];
  let offset = 0;
  let page = 0;

  {
    const rootResp = await callEwsOperation({
      conn,
      operationName: 'GetFolder',
      soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/GetFolder',
      bodyXml: buildGetFolderBody({ rootXml }),
    });
    const rootBlock = [...extractBlocks(rootResp.body, 'Folder'), ...extractBlocks(rootResp.body, 'SearchFolder')][0];
    if (rootBlock) {
      const rootId = folderIdOf(rootBlock);
      if (rootId) {
        folders.push({
          id: rootId,
          parent_id: getAttrValue(rootBlock, 'ParentFolderId', 'Id'),
          name: getTagText(rootBlock, 'DisplayName'),
          unread: Number.parseInt(getTagText(rootBlock, 'UnreadCount') || '0', 10) || 0,
          total: Number.parseInt(getTagText(rootBlock, 'TotalCount') || '0', 10) || 0,
        });
      }
    }
  }

  while (page < maxPages) {
    const resp = await callEwsOperation({
      conn,
      operationName: 'FindFolder',
      soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/FindFolder',
      bodyXml: buildFindFolderBody({ rootXml, offset, pageSize }),
    });

    const blocks = [...extractBlocks(resp.body, 'Folder'), ...extractBlocks(resp.body, 'SearchFolder')];
    for (const block of blocks) {
      const id = folderIdOf(block);
      if (!id) {
        continue;
      }
      folders.push({
        id,
        parent_id: getAttrValue(block, 'ParentFolderId', 'Id'),
        name: getTagText(block, 'DisplayName'),
        unread: Number.parseInt(getTagText(block, 'UnreadCount') || '0', 10) || 0,
        total: Number.parseInt(getTagText(block, 'TotalCount') || '0', 10) || 0,
      });
    }

    const includesLast = String(getAttrValue(resp.body, 'RootFolder', 'IncludesLastItemInRange')).toLowerCase() === 'true';
    if (includesLast || blocks.length === 0) {
      break;
    }

    const nextOffsetRaw = getAttrValue(resp.body, 'RootFolder', 'IndexedPagingOffset');
    const nextOffset = Number.parseInt(nextOffsetRaw, 10);
    if (Number.isFinite(nextOffset) && nextOffset > offset) {
      offset = nextOffset;
    } else {
      offset += pageSize;
    }
    page += 1;
  }

  const totalUnread = folders.reduce((sum, f) => sum + f.unread, 0);
  const filtered = nameFilter
    ? folders.filter((f) => f.name.includes(nameFilter))
    : folders;

  const top = filtered
    .filter((f) => f.unread > 0)
    .sort((a, b) => b.unread - a.unread)
    .slice(0, 20)
    .map((f) => ({
      name: f.name,
      unread: f.unread,
      total: f.total,
      id: f.id,
    }));

  console.log(
    JSON.stringify(
      {
        scope,
        total_folders: folders.length,
        unread_total: totalUnread,
        filter: nameFilter || '',
        filtered_folder_count: filtered.length,
        top_unread_folders: top,
      },
      null,
      2
    )
  );
} catch (err) {
  console.error('get-unread-count failed:', err.message);
  process.exit(1);
}
