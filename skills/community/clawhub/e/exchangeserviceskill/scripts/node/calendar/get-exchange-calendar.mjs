#!/usr/bin/env node
import { asBool, asInt, parseArgs } from '../lib/args.mjs';
import {
  loadConfig,
  normalizeAuthMode,
  readPassword,
  resolveConfigPath,
} from '../lib/config.mjs';
import { ewsPostSoap } from '../lib/ews-client.mjs';
import { extractBlocks, getAttrValue, getNestedTagText, getTagText } from '../lib/xml-utils.mjs';

function toLocalIso(value) {
  const date = new Date(value);
  if (Number.isNaN(date.valueOf())) {
    return '';
  }
  const pad = (n) => String(n).padStart(2, '0');
  const year = date.getFullYear();
  const month = pad(date.getMonth() + 1);
  const day = pad(date.getDate());
  const hour = pad(date.getHours());
  const minute = pad(date.getMinutes());
  const second = pad(date.getSeconds());
  const offsetMinutes = -date.getTimezoneOffset();
  const sign = offsetMinutes >= 0 ? '+' : '-';
  const absOffset = Math.abs(offsetMinutes);
  const offsetHours = pad(Math.floor(absOffset / 60));
  const offsetMins = pad(absOffset % 60);
  return `${year}-${month}-${day}T${hour}:${minute}:${second}${sign}${offsetHours}:${offsetMins}`;
}

function buildSoap({ mailboxXml, startUtc, endUtc, limit }) {
  return `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types" xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
  <soap:Header>
    <t:RequestServerVersion Version="Exchange2013_SP1" />
  </soap:Header>
  <soap:Body>
    <m:FindItem Traversal="Shallow">
      <m:ItemShape>
        <t:BaseShape>IdOnly</t:BaseShape>
        <t:AdditionalProperties>
          <t:FieldURI FieldURI="item:Subject" />
          <t:FieldURI FieldURI="calendar:Start" />
          <t:FieldURI FieldURI="calendar:End" />
          <t:FieldURI FieldURI="calendar:Location" />
          <t:FieldURI FieldURI="calendar:Organizer" />
        </t:AdditionalProperties>
      </m:ItemShape>
      <m:CalendarView MaxEntriesReturned="${limit}" StartDate="${startUtc}" EndDate="${endUtc}" />
      <m:ParentFolderIds>
        ${mailboxXml}
      </m:ParentFolderIds>
    </m:FindItem>
  </soap:Body>
</soap:Envelope>`;
}

try {
  const args = parseArgs();

  const configPath = resolveConfigPath(args.configPath || process.env.EXCHANGE_CONFIG_PATH);
  const cfg = loadConfig(configPath);

  const masterKey = args.masterKey || process.env.EXCHANGE_SKILL_MASTER_KEY;
  const password = readPassword({
    cfg,
    masterKey,
    passwordOverride: args.password || process.env.EXCHANGE_PASSWORD,
  });
  const authMode = normalizeAuthMode(
    args.authMode || process.env.EXCHANGE_AUTH_MODE || cfg.auth_mode
  );

  const limit = asInt(args.limit ?? process.env.EXCHANGE_LIMIT, 30);
  const daysAhead = asInt(args.daysAhead ?? process.env.EXCHANGE_DAYS_AHEAD, 7);
  const insecure = asBool(args.insecure ?? process.env.EXCHANGE_INSECURE);
  const domain = args.domain || process.env.EXCHANGE_DOMAIN || cfg.domain;
  const mailbox = args.mailbox || process.env.EXCHANGE_MAILBOX;

  const start = args.startTime ? new Date(args.startTime) : new Date();
  const end = args.endTime ? new Date(args.endTime) : new Date(Date.now() + Math.abs(daysAhead) * 24 * 60 * 60 * 1000);

  if (Number.isNaN(start.valueOf()) || Number.isNaN(end.valueOf())) {
    throw new Error('Invalid startTime or endTime');
  }

  let mailboxXml = '<t:DistinguishedFolderId Id="calendar" />';
  if (mailbox) {
    mailboxXml = `<t:DistinguishedFolderId Id="calendar"><t:Mailbox><t:EmailAddress>${mailbox}</t:EmailAddress></t:Mailbox></t:DistinguishedFolderId>`;
  }

  const soap = buildSoap({
    mailboxXml,
    startUtc: start.toISOString(),
    endUtc: end.toISOString(),
    limit,
  });

  const resp = await ewsPostSoap({
    url: cfg.exchange_url,
    username: cfg.username,
    password,
    authMode,
    domain,
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/FindItem',
    soapBody: soap,
    insecure,
  });

  const blocks = extractBlocks(resp.body, 'CalendarItem');
  const out = blocks.map((block) => {
    const startUtc = getTagText(block, 'Start');
    const endUtc = getTagText(block, 'End');
    return {
      id: getAttrValue(block, 'ItemId', 'Id'),
      subject: getTagText(block, 'Subject'),
      start: toLocalIso(startUtc),
      end: toLocalIso(endUtc),
      start_utc: startUtc,
      end_utc: endUtc,
      location: getTagText(block, 'Location'),
      organizer: getNestedTagText(block, 'Organizer', 'EmailAddress'),
    };
  });

  console.log(JSON.stringify(out, null, 2));
} catch (err) {
  console.error('get-calendar failed:', err.message);
  process.exit(1);
}
