import { ewsPostSoap } from './ews-client.mjs';
import { asBool } from './args.mjs';
import { escapeXml, getResponseError } from './xml-utils.mjs';

export function buildEnvelope(bodyXml, serverVersion = 'Exchange2013_SP1') {
  return `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types" xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
  <soap:Header>
    <t:RequestServerVersion Version="${escapeXml(serverVersion)}" />
  </soap:Header>
  <soap:Body>
    ${bodyXml}
  </soap:Body>
</soap:Envelope>`;
}

export async function callEwsOperation({
  conn,
  operationName,
  soapAction,
  bodyXml,
}) {
  const soapBody = buildEnvelope(bodyXml, conn.serverVersion);
  const resp = await ewsPostSoap({
    url: conn.url,
    username: conn.username,
    password: conn.password,
    authMode: conn.authMode,
    domain: conn.domain,
    soapAction,
    soapBody,
    insecure: conn.insecure,
  });

  const err = getResponseError(resp.body);
  if (err) {
    throw new Error(`${operationName} failed: ${err.code} - ${err.message}`);
  }

  return {
    status: resp.status,
    body: resp.body,
    soapBody,
  };
}

export function buildItemIdXml(itemId, changeKey = '') {
  if (!itemId) {
    throw new Error('itemId is required');
  }
  const escapedId = escapeXml(itemId);
  if (changeKey) {
    return `<t:ItemId Id="${escapedId}" ChangeKey="${escapeXml(changeKey)}" />`;
  }
  return `<t:ItemId Id="${escapedId}" />`;
}

export function buildFolderIdXml({
  folderId,
  distinguishedId,
  mailbox,
  nodeName = 't:DistinguishedFolderId',
}) {
  if (folderId) {
    return `<t:FolderId Id="${escapeXml(folderId)}" />`;
  }

  if (!distinguishedId) {
    throw new Error('Either folderId or distinguishedId is required');
  }

  if (mailbox) {
    return `<${nodeName} Id="${escapeXml(distinguishedId)}"><t:Mailbox><t:EmailAddress>${escapeXml(mailbox)}</t:EmailAddress></t:Mailbox></${nodeName}>`;
  }

  return `<${nodeName} Id="${escapeXml(distinguishedId)}" />`;
}

export function parseDeleteType(value) {
  const raw = String(value || 'MoveToDeletedItems').trim();
  const supported = new Set(['HardDelete', 'SoftDelete', 'MoveToDeletedItems']);
  if (!supported.has(raw)) {
    throw new Error('deleteType must be one of HardDelete, SoftDelete, MoveToDeletedItems');
  }
  return raw;
}

export function ensureWriteConfirmed(args, operationName) {
  const confirmed = asBool(args.confirm ?? process.env.EXCHANGE_WRITE_CONFIRM);
  const dryRun = asBool(args.dryRun);

  if (dryRun) {
    return;
  }
  if (!confirmed) {
    throw new Error(
      `${operationName} is a write operation. Re-run with --confirm true (or EXCHANGE_WRITE_CONFIRM=true).`
    );
  }
}
