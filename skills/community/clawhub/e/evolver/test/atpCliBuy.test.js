const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const cli = require('../src/atp/cli');

describe('cli.parseBuyArgs', () => {
  it('returns error when no args', () => {
    const r = cli.parseBuyArgs([]);
    assert.equal(r.ok, false);
    assert.match(r.error, /capabilities/);
  });

  it('parses a single capability with default budget', () => {
    const r = cli.parseBuyArgs(['code_review']);
    assert.equal(r.ok, true);
    assert.deepEqual(r.opts.capabilities, ['code_review']);
    assert.equal(r.opts.budget, 10);
    assert.equal(r.opts.routingMode, 'fastest');
    assert.equal(r.opts.verifyMode, 'auto');
    assert.equal(r.opts.noWait, false);
  });

  it('parses comma-separated capabilities with trimming', () => {
    const r = cli.parseBuyArgs(['code_review, bug_fix , refactor']);
    assert.equal(r.ok, true);
    assert.deepEqual(r.opts.capabilities, ['code_review', 'bug_fix', 'refactor']);
  });

  it('accepts --budget=N form', () => {
    const r = cli.parseBuyArgs(['cap1', '--budget=25']);
    assert.equal(r.ok, true);
    assert.equal(r.opts.budget, 25);
  });

  it('accepts --budget N space form', () => {
    const r = cli.parseBuyArgs(['cap1', '--budget', '30']);
    assert.equal(r.ok, true);
    assert.equal(r.opts.budget, 30);
  });

  it('clamps negative budget to 1', () => {
    const r = cli.parseBuyArgs(['cap1', '--budget=-5']);
    assert.equal(r.ok, true);
    assert.equal(r.opts.budget, 1);
  });

  it('clamps non-numeric budget to default 10', () => {
    const r = cli.parseBuyArgs(['cap1', '--budget=abc']);
    assert.equal(r.ok, true);
    assert.equal(r.opts.budget, 10);
  });

  it('respects --question with quoted value', () => {
    const r = cli.parseBuyArgs(['cap1', '--question', 'fix null bug in parser']);
    assert.equal(r.ok, true);
    assert.equal(r.opts.question, 'fix null bug in parser');
  });

  it('sets noWait when --no-wait present', () => {
    const r = cli.parseBuyArgs(['cap1', '--no-wait']);
    assert.equal(r.ok, true);
    assert.equal(r.opts.noWait, true);
  });

  it('converts --timeout seconds to ms', () => {
    const r = cli.parseBuyArgs(['cap1', '--timeout=60']);
    assert.equal(r.ok, true);
    assert.equal(r.opts.timeoutMs, 60000);
  });
});

describe('cli.parseOrdersArgs', () => {
  it('defaults to consumer role, no status', () => {
    const r = cli.parseOrdersArgs([]);
    assert.equal(r.ok, true);
    assert.equal(r.opts.role, 'consumer');
    assert.equal(r.opts.status, null);
    assert.equal(r.opts.limit, 20);
    assert.equal(r.opts.jsonOut, false);
  });

  it('accepts --role merchant', () => {
    const r = cli.parseOrdersArgs(['--role=merchant']);
    assert.equal(r.ok, true);
    assert.equal(r.opts.role, 'merchant');
  });

  it('rejects invalid role', () => {
    const r = cli.parseOrdersArgs(['--role=admin']);
    assert.equal(r.ok, false);
  });

  it('rejects invalid status', () => {
    const r = cli.parseOrdersArgs(['--status=garbage']);
    assert.equal(r.ok, false);
  });

  it('clamps limit to [1,100]', () => {
    assert.equal(cli.parseOrdersArgs(['--limit=0']).opts.limit, 1);
    assert.equal(cli.parseOrdersArgs(['--limit=500']).opts.limit, 100);
  });

  it('sets jsonOut', () => {
    const r = cli.parseOrdersArgs(['--json']);
    assert.equal(r.ok, true);
    assert.equal(r.opts.jsonOut, true);
  });
});

describe('cli.parseVerifyArgs', () => {
  it('requires an orderId', () => {
    const r = cli.parseVerifyArgs([]);
    assert.equal(r.ok, false);
  });

  it('defaults to confirm action', () => {
    const r = cli.parseVerifyArgs(['ord_abc']);
    assert.equal(r.ok, true);
    assert.equal(r.opts.orderId, 'ord_abc');
    assert.equal(r.opts.action, 'confirm');
  });

  it('accepts --action=ai_judge', () => {
    const r = cli.parseVerifyArgs(['ord_abc', '--action=ai_judge']);
    assert.equal(r.ok, true);
    assert.equal(r.opts.action, 'ai_judge');
  });

  it('rejects invalid action', () => {
    const r = cli.parseVerifyArgs(['ord_abc', '--action=force_settle']);
    assert.equal(r.ok, false);
  });
});

describe('cli.runBuy wiring', () => {
  it('delegates to consumerAgent.orderAndWait when not no-wait', async () => {
    const captured = [];
    const deps = {
      atp: {
        consumerAgent: {
          orderAndWait: async (opts) => { captured.push(['orderAndWait', opts]); return { ok: true, order: { order_id: 'ord_X' } }; },
          orderService: async (opts) => { captured.push(['orderService', opts]); return { ok: true, data: { order_id: 'ord_Y' } }; },
        },
      },
      log: () => {},
      err: () => {},
    };
    const { opts } = cli.parseBuyArgs(['cap1', '--budget=7']);
    const r = await cli.runBuy(opts, deps);
    assert.equal(r.exitCode, 0);
    assert.equal(captured.length, 1);
    assert.equal(captured[0][0], 'orderAndWait');
    assert.equal(captured[0][1].budget, 7);
  });

  it('delegates to orderService when --no-wait', async () => {
    const captured = [];
    const deps = {
      atp: {
        consumerAgent: {
          orderAndWait: async () => ({ ok: false, error: 'should_not_be_called' }),
          orderService: async (opts) => { captured.push(opts); return { ok: true, data: { order_id: 'ord_Z' } }; },
        },
      },
      log: () => {},
      err: () => {},
    };
    const { opts } = cli.parseBuyArgs(['cap1', '--no-wait']);
    const r = await cli.runBuy(opts, deps);
    assert.equal(r.exitCode, 0);
    assert.equal(captured.length, 1);
  });

  it('returns exitCode 1 when order fails', async () => {
    const deps = {
      atp: {
        consumerAgent: {
          orderAndWait: async () => ({ ok: false, error: 'no_matching_services' }),
        },
      },
      log: () => {},
      err: () => {},
    };
    const { opts } = cli.parseBuyArgs(['cap1']);
    const r = await cli.runBuy(opts, deps);
    assert.equal(r.exitCode, 1);
  });
});

describe('cli.runOrders wiring', () => {
  it('calls hubClient.listProofs with parsed opts', async () => {
    const captured = [];
    const deps = {
      atp: {
        hubClient: {
          listProofs: async (opts) => { captured.push(opts); return { ok: true, data: { proofs: [] } }; },
        },
      },
      log: () => {},
      err: () => {},
    };
    const { opts } = cli.parseOrdersArgs(['--role=merchant', '--status=settled', '--limit=5']);
    const r = await cli.runOrders(opts, deps);
    assert.equal(r.exitCode, 0);
    assert.equal(captured[0].role, 'merchant');
    assert.equal(captured[0].status, 'settled');
    assert.equal(captured[0].limit, 5);
  });
});

describe('cli.runVerify wiring', () => {
  it('calls confirmDelivery for action=confirm', async () => {
    const captured = [];
    const deps = {
      atp: {
        consumerAgent: {
          confirmDelivery: async (id) => { captured.push(['confirm', id]); return { ok: true, data: {} }; },
          requestAiJudge: async () => ({ ok: false, error: 'should_not_be_called' }),
        },
      },
      log: () => {},
      err: () => {},
    };
    const { opts } = cli.parseVerifyArgs(['ord_123']);
    const r = await cli.runVerify(opts, deps);
    assert.equal(r.exitCode, 0);
    assert.deepEqual(captured, [['confirm', 'ord_123']]);
  });

  it('calls requestAiJudge for action=ai_judge', async () => {
    const captured = [];
    const deps = {
      atp: {
        consumerAgent: {
          confirmDelivery: async () => ({ ok: false, error: 'should_not_be_called' }),
          requestAiJudge: async (id) => { captured.push(['ai_judge', id]); return { ok: true, data: {} }; },
        },
      },
      log: () => {},
      err: () => {},
    };
    const { opts } = cli.parseVerifyArgs(['ord_456', '--action=ai_judge']);
    const r = await cli.runVerify(opts, deps);
    assert.equal(r.exitCode, 0);
    assert.deepEqual(captured, [['ai_judge', 'ord_456']]);
  });
});

describe('cli.runAtp env override warning (Bugbot PR #141 R4)', () => {
  function fakeAutoBuyer() {
    return {
      setConsent: (enabled) => ({ enabled, acknowledged_at: '2026-05-27T00:00:00Z', version: 1 }),
      getConsent: () => ({ enabled: true, source: 'default' }),
      __internals: { ackPath: () => '/tmp/fake-ack.json' },
    };
  }

  function captureLog() {
    const lines = [];
    return { log: (s) => lines.push(String(s)), err: () => {}, read: () => lines.join('\n') };
  }

  it('enable: warns when EVOLVER_ATP_AUTOBUY=off would override the ack', async () => {
    const prev = process.env.EVOLVER_ATP_AUTOBUY;
    process.env.EVOLVER_ATP_AUTOBUY = 'off';
    try {
      const io = captureLog();
      const r = await cli.runAtp({ sub: 'enable' }, { autoBuyer: fakeAutoBuyer(), log: io.log, err: io.err });
      assert.equal(r.exitCode, 0);
      assert.equal(r.envOverride, 'off');
      assert.match(io.read(), /WARNING/);
      assert.match(io.read(), /OVERRIDE/);
      assert.match(io.read(), /EVOLVER_ATP_AUTOBUY=off/);
    } finally {
      if (prev === undefined) delete process.env.EVOLVER_ATP_AUTOBUY;
      else process.env.EVOLVER_ATP_AUTOBUY = prev;
    }
  });

  it('disable: warns when EVOLVER_ATP_AUTOBUY=on would override the ack', async () => {
    const prev = process.env.EVOLVER_ATP_AUTOBUY;
    process.env.EVOLVER_ATP_AUTOBUY = 'on';
    try {
      const io = captureLog();
      const r = await cli.runAtp({ sub: 'disable' }, { autoBuyer: fakeAutoBuyer(), log: io.log, err: io.err });
      assert.equal(r.exitCode, 0);
      assert.equal(r.envOverride, 'on');
      assert.match(io.read(), /WARNING/);
      assert.match(io.read(), /continue charging credits/);
    } finally {
      if (prev === undefined) delete process.env.EVOLVER_ATP_AUTOBUY;
      else process.env.EVOLVER_ATP_AUTOBUY = prev;
    }
  });

  it('enable: no warning when env is unset', async () => {
    const prev = process.env.EVOLVER_ATP_AUTOBUY;
    delete process.env.EVOLVER_ATP_AUTOBUY;
    try {
      const io = captureLog();
      const r = await cli.runAtp({ sub: 'enable' }, { autoBuyer: fakeAutoBuyer(), log: io.log, err: io.err });
      assert.equal(r.exitCode, 0);
      assert.equal(r.envOverride, undefined);
      assert.doesNotMatch(io.read(), /WARNING/);
    } finally {
      if (prev !== undefined) process.env.EVOLVER_ATP_AUTOBUY = prev;
    }
  });

  it('disable: no warning when env agrees (off)', async () => {
    const prev = process.env.EVOLVER_ATP_AUTOBUY;
    process.env.EVOLVER_ATP_AUTOBUY = 'off';
    try {
      const io = captureLog();
      const r = await cli.runAtp({ sub: 'disable' }, { autoBuyer: fakeAutoBuyer(), log: io.log, err: io.err });
      assert.equal(r.exitCode, 0);
      assert.equal(r.envOverride, undefined);
      assert.doesNotMatch(io.read(), /WARNING/);
    } finally {
      if (prev === undefined) delete process.env.EVOLVER_ATP_AUTOBUY;
      else process.env.EVOLVER_ATP_AUTOBUY = prev;
    }
  });
});
