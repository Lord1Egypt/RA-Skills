import { asList } from './args.mjs';
import { escapeXml } from './xml-utils.mjs';

export function parseRecipients(value) {
  return asList(value).map((entry) => {
    const raw = String(entry).trim();
    const idx = raw.indexOf('<');
    const end = raw.indexOf('>');

    if (idx > 0 && end > idx) {
      const name = raw.slice(0, idx).trim().replace(/^"|"$/g, '');
      const email = raw.slice(idx + 1, end).trim();
      return { name, email };
    }

    return { name: '', email: raw };
  });
}

export function buildMailboxXml({ name, email }) {
  if (!email) {
    return '';
  }
  if (name) {
    return `<t:Mailbox><t:Name>${escapeXml(name)}</t:Name><t:EmailAddress>${escapeXml(email)}</t:EmailAddress></t:Mailbox>`;
  }
  return `<t:Mailbox><t:EmailAddress>${escapeXml(email)}</t:EmailAddress></t:Mailbox>`;
}

export function buildRecipientsXml(tagName, recipients) {
  if (!recipients || recipients.length === 0) {
    return '';
  }
  const boxes = recipients.map((r) => buildMailboxXml(r)).join('');
  if (!boxes) {
    return '';
  }
  return `<t:${tagName}>${boxes}</t:${tagName}>`;
}

export function normalizeBodyType(value) {
  const type = String(value || 'Text').trim();
  const supported = new Set(['Text', 'HTML', 'Best']);
  if (!supported.has(type)) {
    throw new Error('bodyType must be one of Text, HTML, Best');
  }
  return type;
}
