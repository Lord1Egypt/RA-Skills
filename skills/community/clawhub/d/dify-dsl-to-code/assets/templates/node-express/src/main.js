/**
 * Express entrypoint.
 * POST /run        {inputs} -> {outputs}  (one-shot)
 * POST /run/stream {inputs} -> SSE stream of answer chunks + a final event
 * GET  /healthz    liveness probe
 */
import 'dotenv/config';
import express from 'express';
import { DEFINITION, buildHandlers } from './workflow/definition.js';
import { Engine } from './workflow/runner.js';

const app = express();
app.use(express.json({ limit: '10mb' }));

app.post('/run', async (req, res) => {
  try {
    const engine = new Engine(DEFINITION, buildHandlers());
    const outputs = await engine.run(req.body.inputs || {});
    res.json({ outputs });
  } catch (e) {
    const notImpl = String(e.message || '').includes('no handler registered');
    res.status(notImpl ? 501 : 500).json({ detail: `${e.name}: ${e.message}` });
  }
});

app.post('/run/stream', async (req, res) => {
  res.set({
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    Connection: 'keep-alive',
  });
  res.flushHeaders();
  const engine = new Engine(DEFINITION, buildHandlers());
  try {
    for await (const [event, payload] of engine.runStream(req.body.inputs || {})) {
      res.write(`event: ${event}\ndata: ${JSON.stringify(payload)}\n\n`);
    }
  } catch (e) {
    res.write(`event: error\ndata: ${JSON.stringify(`${e.name}: ${e.message}`)}\n\n`);
  }
  res.end();
});

app.get('/healthz', (_req, res) => res.json({ status: 'ok' }));

const port = Number(process.env.PORT || 8000);
app.listen(port, () => {
  console.log(`${process.env.APP_NAME || 'dify-workflow-service'} listening on :${port}`);
});
