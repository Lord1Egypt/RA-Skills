import crypto from 'node:crypto';

function normalizeValue(value) {
  if (value === undefined || value === null || value === '') return '*';
  return String(value);
}

export function buildConfirmCode({
  channelId,
  authorId,
  contains,
  regex,
  after,
  before,
  includePinned,
}) {
  const raw = [
    normalizeValue(channelId),
    normalizeValue(authorId),
    normalizeValue(contains),
    normalizeValue(regex),
    normalizeValue(after),
    normalizeValue(before),
    normalizeValue(includePinned),
  ].join('|');

  const hash = crypto.createHash('sha1').update(raw).digest('hex').slice(0, 8).toUpperCase();
  return `PURGE-${hash}`;
}

export function buildNukeCode({ channelId }) {
  const hash = crypto.createHash('sha1').update(normalizeValue(channelId)).digest('hex').slice(0, 8).toUpperCase();
  return `NUKE-${hash}`;
}

export function buildJobId(prefix = 'purge') {
  const timestamp = new Date().toISOString().replace(/[-:.TZ]/g, '').slice(0, 14);
  const random = crypto.randomBytes(2).toString('hex');
  return `${prefix}-${timestamp}-${random}`;
}
