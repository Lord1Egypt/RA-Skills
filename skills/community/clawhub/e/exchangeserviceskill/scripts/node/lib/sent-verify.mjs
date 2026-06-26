import { callEwsOperation } from './ews-ops.mjs';
import { extractBlocks, getAttrValue, getTagText } from './xml-utils.mjs';

function stripReplyPrefixes(subject) {
  let out = String(subject || '').trim();
  const prefix = /^(?:(?:re|fw|fwd|答复|回复|转发)\s*[:：]\s*)+/i;
  while (prefix.test(out)) {
    out = out.replace(prefix, '').trim();
  }
  return out;
}

function normalizeSubject(subject) {
  return stripReplyPrefixes(subject).replace(/\s+/g, ' ').trim().toLowerCase();
}

function buildFindSentItemsBody(maxEntries) {
  return `<m:FindItem Traversal="Shallow">
      <m:ItemShape>
        <t:BaseShape>IdOnly</t:BaseShape>
        <t:AdditionalProperties>
          <t:FieldURI FieldURI="item:Subject" />
          <t:FieldURI FieldURI="item:DateTimeSent" />
        </t:AdditionalProperties>
      </m:ItemShape>
      <m:IndexedPageItemView MaxEntriesReturned="${maxEntries}" Offset="0" BasePoint="Beginning" />
      <m:SortOrder>
        <t:FieldOrder Order="Descending">
          <t:FieldURI FieldURI="item:DateTimeSent" />
        </t:FieldOrder>
      </m:SortOrder>
      <m:ParentFolderIds>
        <t:DistinguishedFolderId Id="sentitems" />
      </m:ParentFolderIds>
    </m:FindItem>`;
}

export async function verifySentBySubject({
  conn,
  subject,
  sentAfterMs,
  verifyWindowMinutes = 15,
  maxEntries = 100,
}) {
  const bodyXml = buildFindSentItemsBody(Math.max(1, maxEntries));
  const resp = await callEwsOperation({
    conn,
    operationName: 'FindItem(sentitems)',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/FindItem',
    bodyXml,
  });

  const now = Date.now();
  const lowerBoundMs = Math.max(
    0,
    Number.isFinite(sentAfterMs) ? sentAfterMs - 60 * 1000 : now - verifyWindowMinutes * 60 * 1000
  );
  const upperBoundMs = now + 60 * 1000;
  const expected = normalizeSubject(subject);

  const rows = extractBlocks(resp.body, 'Message').map((block) => {
    const sent = getTagText(block, 'DateTimeSent');
    return {
      id: getAttrValue(block, 'ItemId', 'Id'),
      subject: getTagText(block, 'Subject'),
      sent,
      sent_ms: sent ? Date.parse(sent) : Number.NaN,
    };
  });

  const candidates = rows.filter((row) => Number.isFinite(row.sent_ms) && row.sent_ms >= lowerBoundMs && row.sent_ms <= upperBoundMs);

  const matched = candidates.filter((row) => {
    const got = normalizeSubject(row.subject);
    if (!expected) {
      return true;
    }
    return got === expected || got.includes(expected) || expected.includes(got);
  });

  return {
    checked: true,
    verified: matched.length > 0,
    expected_subject: subject || '',
    expected_subject_normalized: expected,
    sent_after_utc: new Date(lowerBoundMs).toISOString(),
    window_minutes: verifyWindowMinutes,
    scanned_count: rows.length,
    candidate_count: candidates.length,
    matched_count: matched.length,
    matched: matched.slice(0, 5).map((row) => ({
      id: row.id,
      subject: row.subject,
      sent: row.sent,
    })),
  };
}
