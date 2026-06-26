#!/usr/bin/env node
// Generic CLI dispatcher — parse `<action> [json-params]` from argv and run a handler.
export function cli(handlers) {
  const [action, ...rest] = process.argv.slice(2);
  if (!action || !handlers[action]) {
    const available = Object.keys(handlers).join(', ');
    console.log(JSON.stringify({
      error: action ? `Unknown action "${action}"` : 'No action specified',
      available_actions: available,
      usage: 'node <script> <action> [json-params]',
    }));
    process.exit(1);
  }
  let params = {};
  if (rest.length) {
    const raw = rest.join(' ');
    try {
      params = JSON.parse(raw);
    } catch {
      console.log(JSON.stringify({
        error: `Invalid JSON parameter: ${raw}`,
        hint: 'Parameters must be a JSON object, e.g.: \'{"symbol":"BTC","interval":"1h"}\'',
        example: `node <script> ${action} '{"key":"value"}'`,
      }));
      process.exit(1);
    }
  }
  handlers[action](params).then(r => console.log(JSON.stringify(r, null, 2))).catch(e => {
    console.error(e.message);
    process.exit(1);
  });
}
