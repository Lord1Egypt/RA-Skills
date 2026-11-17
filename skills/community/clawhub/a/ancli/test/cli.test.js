const { test } = require('node:test');
const assert = require('node:assert/strict');
const { htmlToText, parseArgs } = require('../lib/cli');

test('Notes HTML becomes plain text, lists and entities included', () => {
  const html =
    '<div><b><span style="font-size: 24px">Shopping list</span></b></div>\n<div>Milk &amp eggs</div>\n<div><br></div>\n' +
    '<ul><li>Bread</li><li>Tea &lt;green&gt;</li></ul><ol><li>One</li><li>Two</li></ol>';
  assert.equal(htmlToText(html), 'Shopping list\nMilk & eggs\n\n- Bread\n- Tea <green>\n1. One\n2. Two');
});

test('flags, short flags and a dash for stdin parse; a flag without its value does not', () => {
  const { result } = parseArgs(['create', 'Meeting notes', '-', '--folder=Work', '-y', '--json']);
  assert.deepEqual(result, {
    command: 'create',
    positional: ['Meeting notes', '-'],
    flags: { folder: 'Work', yes: true, json: true },
  });
  assert.equal(parseArgs(['list', '--limit']).ok, false);
});
