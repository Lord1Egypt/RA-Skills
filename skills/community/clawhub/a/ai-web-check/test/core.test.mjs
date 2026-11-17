import assert from 'node:assert/strict';
import test from 'node:test';
import http from 'node:http';
import { scan, runJourney, toMarkdown } from '../src/core.mjs';

let server; let origin;
test.before(async () => { server = http.createServer((req, res) => { const pages = { '/': '<!doctype html><title>Demo</title><main><nav><a href="/pricing">Pricing</a></nav><h1>Agent-ready demo</h1><img alt="logo" src="x"><form><label for="email">Email</label><input id="email"></form><button data-action-id="create_draft">Create draft</button><script type="application/ld+json">{}</script></main>', '/pricing': '<title>Pricing</title><main><h1>Plans</h1></main>', '/robots.txt': 'User-agent: *', '/sitemap.xml': '<urlset/>', '/llms.txt': '# demo' }; const body = pages[req.url]; res.writeHead(body === undefined ? 404 : 200, { 'content-type': req.url.endsWith('.txt') ? 'text/plain' : 'text/html' }); res.end(body || 'not found'); }); await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve)); origin = `http://127.0.0.1:${server.address().port}`; });
test.after(() => server.close());
test('scan records evidence and does not claim actions were tested', async () => { const result = await scan(`${origin}/`); assert.equal(result.checks.find((item) => item.id === 'find').status, 'PASS'); assert.equal(result.checks.find((item) => item.id === 'read').status, 'PASS'); assert.equal(result.profiles.accessibility, 'PASS'); assert.equal(result.checks.find((item) => item.id === 'act').status, 'NOT_TESTED'); assert.match(toMarkdown(result), /NOT_TESTED/); });
test('journey allows same-origin GET pages and rejects cross-origin steps', async () => { const good = await runJourney(origin, { steps: ['/', '/pricing'] }); assert.equal(good.status, 'PASS'); const bad = await runJourney(origin, { steps: ['https://example.com/'] }); assert.equal(bad.status, 'FAIL'); assert.match(bad.steps[0].error, /same-origin/); });
