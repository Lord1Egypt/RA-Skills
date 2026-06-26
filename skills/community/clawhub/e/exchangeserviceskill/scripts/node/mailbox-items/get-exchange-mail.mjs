#!/usr/bin/env node
import { asBool, asInt, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import { buildFolderIdXml, callEwsOperation } from '../lib/ews-ops.mjs';
import {
  escapeXml,
  extractBlocks,
  getAttrValue,
  getNestedTagText,
  getTagText,
} from '../lib/xml-utils.mjs';

function normalizeScope(value) {
  const raw = String(value || 'all').trim().toLowerCase();
  if (raw === 'all' || raw === 'root' || raw === 'msgfolderroot') {
    return 'msgfolderroot';
  }
  if (raw === 'inbox') {
    return 'inbox';
  }
  return raw;
}

function buildRootRefXml({ rootFolderId, rootDistinguishedId, mailbox }) {
  return buildFolderIdXml({
    folderId: rootFolderId,
    distinguishedId: rootDistinguishedId,
    mailbox,
  });
}

function buildFindFolderBody({ parentRefXml, maxEntries, offset }) {
  return `<m:FindFolder Traversal="Deep">
      <m:FolderShape>
        <t:BaseShape>IdOnly</t:BaseShape>
        <t:AdditionalProperties>
          <t:FieldURI FieldURI="folder:DisplayName" />
        </t:AdditionalProperties>
      </m:FolderShape>
      <m:IndexedPageFolderView MaxEntriesReturned="${maxEntries}" Offset="${offset}" BasePoint="Beginning" />
      <m:ParentFolderIds>
        ${parentRefXml}
      </m:ParentFolderIds>
    </m:FindFolder>`;
}

function buildFindItemBody({ parentFolderIdsXml, fetchSize, offset }) {
  return `<m:FindItem Traversal="Shallow">
      <m:ItemShape>
        <t:BaseShape>IdOnly</t:BaseShape>
        <t:AdditionalProperties>
          <t:FieldURI FieldURI="item:Subject" />
          <t:FieldURI FieldURI="message:From" />
          <t:FieldURI FieldURI="item:DateTimeReceived" />
          <t:FieldURI FieldURI="message:IsRead" />
          <t:FieldURI FieldURI="item:ParentFolderId" />
        </t:AdditionalProperties>
      </m:ItemShape>
      <m:IndexedPageItemView MaxEntriesReturned="${fetchSize}" Offset="${offset}" BasePoint="Beginning" />
      <m:ParentFolderIds>
        ${parentFolderIdsXml}
      </m:ParentFolderIds>
    </m:FindItem>`;
}

function buildGetFolderBody({ folderIdsXml }) {
  return `<m:GetFolder>
      <m:FolderShape>
        <t:BaseShape>IdOnly</t:BaseShape>
        <t:AdditionalProperties>
          <t:FieldURI FieldURI="folder:DisplayName" />
        </t:AdditionalProperties>
      </m:FolderShape>
      <m:FolderIds>
        ${folderIdsXml}
      </m:FolderIds>
    </m:GetFolder>`;
}

function parseFolderBlocks(xml) {
  return [...extractBlocks(xml, 'Folder'), ...extractBlocks(xml, 'SearchFolder')];
}

function getFolderBlockId(block) {
  return getAttrValue(block, 'FolderId', 'Id') ||
    getAttrValue(block, 'SearchFolderId', 'Id') ||
    '';
}

function splitChunks(items, size) {
  const out = [];
  for (let i = 0; i < items.length; i += size) {
    out.push(items.slice(i, i + size));
  }
  return out;
}

function formatAddress(name, email) {
  const n = String(name || '').trim();
  const e = String(email || '').trim();
  if (n && e && n.toLowerCase() !== e.toLowerCase()) {
    return `${n}(${e})`;
  }
  return e || n;
}

function parseMailBlock(block, folderNames, includeFolderInfo) {
  const parentFolderId = getAttrValue(block, 'ParentFolderId', 'Id');
  const receivedRaw = getTagText(block, 'DateTimeReceived');
  const fromName = getNestedTagText(block, 'From', 'Name');
  const fromEmail = getNestedTagText(block, 'From', 'EmailAddress');

  const out = {
    id: getAttrValue(block, 'ItemId', 'Id'),
    subject: getTagText(block, 'Subject'),
    from: formatAddress(fromName, fromEmail),
    from_name: fromName,
    from_email: fromEmail,
    received: receivedRaw,
    is_read: String(getTagText(block, 'IsRead')).toLowerCase() === 'true',
  };

  if (includeFolderInfo) {
    out.parent_folder_id = parentFolderId;
    if (parentFolderId && folderNames.has(parentFolderId)) {
      out.parent_folder_name = folderNames.get(parentFolderId);
      out.folder_name = folderNames.get(parentFolderId);
    }
  }

  return out;
}

async function resolveFolderDisplayNames({
  conn,
  folderIds,
  folderNames,
  batchSize,
}) {
  const missing = [];
  const seen = new Set();

  for (const folderId of folderIds) {
    if (!folderId || folderNames.has(folderId) || seen.has(folderId)) {
      continue;
    }
    seen.add(folderId);
    missing.push(folderId);
  }

  if (missing.length === 0) {
    return;
  }

  const batches = splitChunks(missing, Math.max(1, batchSize));
  for (const batch of batches) {
    const folderIdsXml = batch
      .map((folderId) => `<t:FolderId Id="${escapeXml(folderId)}" />`)
      .join('\n');

    const bodyXml = buildGetFolderBody({ folderIdsXml });
    const resp = await callEwsOperation({
      conn,
      operationName: 'GetFolder',
      soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/GetFolder',
      bodyXml,
    });

    const blocks = parseFolderBlocks(resp.body);
    for (const block of blocks) {
      const id = getFolderBlockId(block);
      if (!id) {
        continue;
      }
      folderNames.set(id, getTagText(block, 'DisplayName') || '');
    }
  }
}

async function findSubfolders({
  conn,
  parentRefXml,
  maxFolders,
  pageSize,
}) {
  const out = [];
  const seen = new Set();
  let offset = 0;

  while (out.length < maxFolders) {
    const remaining = maxFolders - out.length;
    const currentPage = Math.max(1, Math.min(pageSize, remaining));

    const bodyXml = buildFindFolderBody({
      parentRefXml,
      maxEntries: currentPage,
      offset,
    });

    const resp = await callEwsOperation({
      conn,
      operationName: 'FindFolder',
      soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/FindFolder',
      bodyXml,
    });

    const blocks = parseFolderBlocks(resp.body);
    for (const block of blocks) {
      const id = getFolderBlockId(block);
      if (!id || seen.has(id)) {
        continue;
      }
      seen.add(id);
      out.push({
        id,
        display_name: getTagText(block, 'DisplayName'),
      });
      if (out.length >= maxFolders) {
        break;
      }
    }

    const includesLast = String(getAttrValue(resp.body, 'RootFolder', 'IncludesLastItemInRange')).toLowerCase() === 'true';
    if (includesLast || blocks.length === 0) {
      break;
    }
    offset += currentPage;
  }

  return out;
}

try {
  const args = parseArgs();
  const conn = loadConnectionFromArgs(args);

  const limit = asInt(args.limit ?? process.env.EXCHANGE_LIMIT, 10);
  const daysBack = asInt(args.daysBack ?? process.env.EXCHANGE_DAYS_BACK, 3650);
  const unreadOnly = asBool(args.unreadOnly ?? process.env.EXCHANGE_UNREAD_ONLY);

  const includeSubfolders = args.includeSubfolders === undefined &&
    process.env.EXCHANGE_INCLUDE_SUBFOLDERS === undefined
      ? true
      : asBool(args.includeSubfolders ?? process.env.EXCHANGE_INCLUDE_SUBFOLDERS);

  const includeFolderInfo = asBool(args.includeFolderInfo ?? process.env.EXCHANGE_INCLUDE_FOLDER_INFO ?? includeSubfolders);
  const maxFolders = asInt(args.maxFolders ?? process.env.EXCHANGE_MAX_FOLDERS, 500);
  const folderPageSize = asInt(args.folderPageSize ?? process.env.EXCHANGE_FOLDER_PAGE_SIZE, 100);
  const folderBatchSize = asInt(args.folderBatchSize ?? process.env.EXCHANGE_FOLDER_BATCH_SIZE, 30);
  const maxItemPages = asInt(args.maxItemPages ?? process.env.EXCHANGE_MAX_ITEM_PAGES, 200);
  const fetchSize = asInt(
    args.fetchSize ?? process.env.EXCHANGE_FETCH_SIZE,
    includeSubfolders ? Math.max(limit * 20, 200) : Math.max(limit * 5, 50)
  );

  const cutoff = new Date(Date.now() - Math.abs(daysBack) * 24 * 60 * 60 * 1000);
  const mailbox = args.mailbox || process.env.EXCHANGE_MAILBOX;
  const rootFolderId = args.rootFolderId || args.parentFolderId || process.env.EXCHANGE_ROOT_FOLDER_ID;
  const rootDistinguishedId =
    args.rootDistinguishedId ||
    args.parentDistinguishedId ||
    process.env.EXCHANGE_ROOT_DISTINGUISHED_ID ||
    normalizeScope(args.scope ?? process.env.EXCHANGE_SEARCH_SCOPE ?? 'all');
  const rootRefXml = buildRootRefXml({
    rootFolderId,
    rootDistinguishedId,
    mailbox,
  });

  const parentFolderXmlList = [rootRefXml];
  const folderNames = new Map();

  if (includeSubfolders) {
    const folders = await findSubfolders({
      conn,
      parentRefXml: rootRefXml,
      maxFolders,
      pageSize: folderPageSize,
    });

    for (const folder of folders) {
      parentFolderXmlList.push(`<t:FolderId Id="${escapeXml(folder.id)}" />`);
      folderNames.set(folder.id, folder.display_name || '');
    }
  }

  const allItems = [];
  const seenItemIds = new Set();

  for (const parentFolderXml of parentFolderXmlList) {
    let offset = 0;
    let page = 0;

    while (page < maxItemPages) {
      const bodyXml = buildFindItemBody({
        parentFolderIdsXml: parentFolderXml,
        fetchSize,
        offset,
      });

      const resp = await callEwsOperation({
        conn,
        operationName: 'FindItem',
        soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/FindItem',
        bodyXml,
      });

      const blocks = extractBlocks(resp.body, 'Message');
      for (const block of blocks) {
        const id = getAttrValue(block, 'ItemId', 'Id');
        if (!id || seenItemIds.has(id)) {
          continue;
        }
        seenItemIds.add(id);
        allItems.push(parseMailBlock(block, folderNames, includeFolderInfo));
      }

      const includesLast = String(
        getAttrValue(resp.body, 'RootFolder', 'IncludesLastItemInRange')
      ).toLowerCase() === 'true';
      if (includesLast || blocks.length === 0) {
        break;
      }

      const nextOffsetRaw = getAttrValue(resp.body, 'RootFolder', 'IndexedPagingOffset');
      const nextOffset = Number.parseInt(nextOffsetRaw, 10);
      if (Number.isFinite(nextOffset) && nextOffset > offset) {
        offset = nextOffset;
      } else {
        offset += fetchSize;
      }

      page += 1;
    }
  }

  if (includeFolderInfo) {
    await resolveFolderDisplayNames({
      conn,
      folderIds: allItems.map((item) => item.parent_folder_id),
      folderNames,
      batchSize: folderBatchSize,
    });

    for (const item of allItems) {
      if (!item.parent_folder_id) {
        continue;
      }
      if (!item.parent_folder_name && folderNames.has(item.parent_folder_id)) {
        item.parent_folder_name = folderNames.get(item.parent_folder_id);
      }
      if (!item.folder_name && folderNames.has(item.parent_folder_id)) {
        item.folder_name = folderNames.get(item.parent_folder_id);
      }
    }
  }

  allItems.sort((a, b) => {
    const ta = a.received ? Date.parse(a.received) : 0;
    const tb = b.received ? Date.parse(b.received) : 0;
    return tb - ta;
  });

  const out = [];
  for (const item of allItems) {
    const receivedAt = item.received ? new Date(item.received) : null;
    if (receivedAt && !Number.isNaN(receivedAt.valueOf()) && receivedAt < cutoff) {
      continue;
    }
    if (unreadOnly && item.is_read) {
      continue;
    }
    out.push(item);
    if (out.length >= limit) {
      break;
    }
  }

  console.log(JSON.stringify(out, null, 2));
} catch (err) {
  console.error('get-mail failed:', err.message);
  process.exit(1);
}
