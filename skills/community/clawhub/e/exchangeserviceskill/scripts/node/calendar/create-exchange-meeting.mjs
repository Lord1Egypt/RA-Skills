#!/usr/bin/env node
import { asBool, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import {
  buildFolderIdXml,
  callEwsOperation,
  ensureWriteConfirmed,
} from '../lib/ews-ops.mjs';
import {
  buildMailboxXml,
  normalizeBodyType,
  parseRecipients,
} from '../lib/mail-builders.mjs';
import { escapeXml, getAttrValue } from '../lib/xml-utils.mjs';

function normalizeSendInvitations(value) {
  if (value === undefined || value === null || value === '') {
    return 'SendToNone';
  }
  if (value === true || asBool(value)) {
    return 'SendToAllAndSaveCopy';
  }
  const raw = String(value || '').trim();
  const supported = new Set([
    'SendToNone',
    'SendOnlyToAll',
    'SendToAllAndSaveCopy',
    'SendToChangedAndSaveCopy',
  ]);
  if (!supported.has(raw)) {
    throw new Error('sendInvitations must be SendToNone, SendOnlyToAll, SendToAllAndSaveCopy, or SendToChangedAndSaveCopy');
  }
  return raw;
}

function buildAttendeesXml(tagName, recipients) {
  if (!recipients || recipients.length === 0) {
    return '';
  }
  const attendees = recipients
    .map((r) => {
      const mailboxXml = buildMailboxXml(r);
      if (!mailboxXml) {
        return '';
      }
      return `<t:Attendee>${mailboxXml}</t:Attendee>`;
    })
    .filter(Boolean)
    .join('');
  if (!attendees) {
    return '';
  }
  return `<t:${tagName}>${attendees}</t:${tagName}>`;
}

try {
  const args = parseArgs();
  ensureWriteConfirmed(args, 'CreateItem');
  const conn = loadConnectionFromArgs(args);

  const subject = args.subject || process.env.EXCHANGE_MEETING_SUBJECT || '';
  const body = args.body || process.env.EXCHANGE_MEETING_BODY || '';
  const bodyType = normalizeBodyType(args.bodyType || process.env.EXCHANGE_BODY_TYPE || 'Text');
  const location = args.location || process.env.EXCHANGE_MEETING_LOCATION || '';

  const startRaw = args.start || args.startTime || process.env.EXCHANGE_MEETING_START;
  const endRaw = args.end || args.endTime || process.env.EXCHANGE_MEETING_END;

  if (!startRaw || !endRaw) {
    throw new Error('start and end are required (use --start and --end)');
  }

  const start = new Date(startRaw);
  const end = new Date(endRaw);
  if (Number.isNaN(start.valueOf()) || Number.isNaN(end.valueOf())) {
    throw new Error('Invalid start or end time');
  }
  if (end <= start) {
    throw new Error('end must be after start');
  }

  const requiredAttendees = parseRecipients(
    args.required || args.to || process.env.EXCHANGE_MEETING_REQUIRED
  );
  const optionalAttendees = parseRecipients(
    args.optional || args.cc || process.env.EXCHANGE_MEETING_OPTIONAL
  );

  const sendInvitations = normalizeSendInvitations(
    args.sendInvitations || args.sendInvites || args.send || process.env.EXCHANGE_SEND_MEETING_INVITATIONS
  );

  const saveFolderId = args.saveFolderId || process.env.EXCHANGE_SAVE_FOLDER_ID;
  const saveDistinguishedId = args.saveDistinguishedId || process.env.EXCHANGE_SAVE_DISTINGUISHED_ID || 'calendar';
  const saveMailbox = args.saveMailbox || process.env.EXCHANGE_SAVE_MAILBOX;
  const savedFolderXml = `<m:SavedItemFolderId>${buildFolderIdXml({
    folderId: saveFolderId,
    distinguishedId: saveDistinguishedId,
    mailbox: saveMailbox,
  })}</m:SavedItemFolderId>`;

  const bodyXml = `<m:CreateItem SendMeetingInvitations="${sendInvitations}">
      ${savedFolderXml}
      <m:Items>
        <t:CalendarItem>
          <t:Subject>${escapeXml(subject)}</t:Subject>
          <t:Body BodyType="${bodyType}">${escapeXml(body)}</t:Body>
          <t:Start>${escapeXml(start.toISOString())}</t:Start>
          <t:End>${escapeXml(end.toISOString())}</t:End>
          ${location ? `<t:Location>${escapeXml(location)}</t:Location>` : ''}
          ${buildAttendeesXml('RequiredAttendees', requiredAttendees)}
          ${buildAttendeesXml('OptionalAttendees', optionalAttendees)}
        </t:CalendarItem>
      </m:Items>
    </m:CreateItem>`;

  if (asBool(args.dryRun)) {
    console.log(
      JSON.stringify(
        {
          dry_run: true,
          operation: 'CreateItem',
          send_meeting_invitations: sendInvitations,
          soap_action: 'http://schemas.microsoft.com/exchange/services/2006/messages/CreateItem',
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
    operationName: 'CreateItem',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/CreateItem',
    bodyXml,
  });

  const out = {
    ok: true,
    operation: 'CreateItem',
    send_meeting_invitations: sendInvitations,
    item_id: getAttrValue(resp.body, 'ItemId', 'Id'),
    change_key: getAttrValue(resp.body, 'ItemId', 'ChangeKey'),
  };

  console.log(JSON.stringify(out, null, 2));
} catch (err) {
  console.error('create-meeting failed:', err.message);
  process.exit(1);
}
