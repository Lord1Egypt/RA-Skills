#!/usr/bin/env node
import { asInt, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import { buildFolderIdXml, callEwsOperation } from '../lib/ews-ops.mjs';
import { extractFolderBlocks, parseFolderBlock } from '../lib/folder-utils.mjs';
import { getAttrValue } from '../lib/xml-utils.mjs';

function normalizeTraversal(value) {
  const raw = String(value || 'Shallow').trim();
  const supported = new Set(['Shallow', 'Deep']);
  if (!supported.has(raw)) {
    throw new Error('traversal must be Shallow or Deep');
  }
  return raw;
}

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

function buildFindFolderBody({
  parentFolderXml,
  traversal,
  baseShape,
  pageSize,
  offset,
}) {
  return `<m:FindFolder Traversal="${traversal}">
      ${buildFolderShapeXml(baseShape)}
      <m:IndexedPageFolderView MaxEntriesReturned="${pageSize}" Offset="${offset}" BasePoint="Beginning" />
      <m:ParentFolderIds>
        ${parentFolderXml}
      </m:ParentFolderIds>
    </m:FindFolder>`;
}

try {
  const args = parseArgs();
  const conn = loadConnectionFromArgs(args);

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

  const traversal = normalizeTraversal(
    args.traversal || process.env.EXCHANGE_TRAVERSAL || 'Shallow'
  );

  const baseShape =
    args.baseShape || process.env.EXCHANGE_BASE_SHAPE || 'IdOnly';
  const limit = asInt(args.limit ?? process.env.EXCHANGE_LIMIT, 200);
  const pageSize = asInt(args.pageSize ?? process.env.EXCHANGE_PAGE_SIZE, 100);
  const maxPages = asInt(args.maxPages ?? process.env.EXCHANGE_MAX_PAGES, 50);

  const parentFolderXml = buildFolderIdXml({
    folderId: parentFolderId,
    distinguishedId: parentDistinguishedId,
    mailbox: parentMailbox,
  });

  const out = [];
  let offset = asInt(args.offset ?? 0, 0);
  let page = 0;

  while (out.length < limit && page < maxPages) {
    const remaining = Math.max(1, limit - out.length);
    const currentPageSize = Math.max(1, Math.min(pageSize, remaining));

    const bodyXml = buildFindFolderBody({
      parentFolderXml,
      traversal,
      baseShape,
      pageSize: currentPageSize,
      offset,
    });

    const resp = await callEwsOperation({
      conn,
      operationName: 'FindFolder',
      soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/FindFolder',
      bodyXml,
    });

    const blocks = extractFolderBlocks(resp.body);
    for (const block of blocks) {
      out.push(parseFolderBlock(block));
      if (out.length >= limit) {
        break;
      }
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
      offset += currentPageSize;
    }

    page += 1;
  }

  console.log(JSON.stringify(out, null, 2));
} catch (err) {
  console.error('find-folder failed:', err.message);
  process.exit(1);
}
