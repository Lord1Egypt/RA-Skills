const { test } = require('node:test');
const assert = require('node:assert/strict');
const { appleDate, toAppleNanos, decodeAttributedBody, messageText } = require('../lib/decode');

// The shape Messages writes: an NSAttributedString typedstream whose NSString
// payload is `+`, a length, then UTF-8 bytes.
function blob(text) {
  const bytes = Buffer.from(text, 'utf8');
  const len =
    bytes.length < 0x80 ? Buffer.from([bytes.length]) : Buffer.concat([Buffer.from([0x81]), u16(bytes.length)]);
  return Buffer.concat([
    Buffer.from('\x04\x0bstreamtyped\x81\xe8\x03\x84\x01@\x84\x84\x84\x12NSAttributedString\x00\x84\x84\x08NSObject\x00\x85\x92\x84\x84\x84\x08NSString\x01\x94\x84\x01+', 'latin1'),
    len,
    bytes,
    Buffer.from('\x86\x84\x02iI\x01\x05\x92\x84\x84\x84\x0cNSDictionary\x00', 'latin1'),
  ]);
}

function u16(n) {
  const b = Buffer.alloc(2);
  b.writeUInt16LE(n);
  return b;
}

test('apple dates convert from nanoseconds and from legacy seconds', () => {
  assert.equal(appleDate(0n), null);
  assert.equal(appleDate(784025377000000000n).toISOString(), '2025-11-05T08:49:37.000Z');
  assert.equal(appleDate(784025377).toISOString(), '2025-11-05T08:49:37.000Z');
  assert.equal(toAppleNanos(new Date('2025-11-05T08:49:37Z')), 784025377000000000n);
});

test('attributedBody decodes short, long and non-ASCII text', () => {
  assert.equal(decodeAttributedBody(blob('Running late')), 'Running late');
  const long = 'Running late, ' .repeat(20) + 'see you at 7 ☕';
  assert.equal(decodeAttributedBody(new Uint8Array(blob(long))), long);
  assert.equal(decodeAttributedBody(Buffer.from('nothing here')), null);
  assert.equal(messageText(null, blob('￼Running late')), 'Running late');
  assert.equal(messageText('On my way', blob('ignored')), 'On my way');
});
