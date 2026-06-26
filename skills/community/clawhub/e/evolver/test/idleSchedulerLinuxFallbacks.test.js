'use strict';

// Linux multi-tier idle-detection fallback chain.
//
// Pre-fix the Linux branch of `getSystemIdleSeconds()` only invoked
// `xprintidle`, which is X11-only and silently returns nothing on Wayland
// sessions (default on Ubuntu 21.04+, Fedora, GNOME 40+, KDE 6+). The user
// impact was silent: idle detection returned -1 forever, the scheduler
// stayed in 'normal' intensity, and aggressive/deep evolution cycles never
// ran on modern Linux desktops.
//
// These tests exercise the new fallback chain (xprintidle -> gnome-mutter
// -> loginctl) through the injected exec hook, so they pass on any host
// regardless of the actual X11 / Wayland / D-Bus / systemd state.

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');

const idleScheduler = require('../src/gep/idleScheduler');
const { __test } = idleScheduler;

// Recorder for the string-form exec (xprintidle / gdbus).
function recordingExec() {
  const calls = [];
  function exec(cmd, timeoutMs) {
    calls.push({ cmd: cmd, timeoutMs: timeoutMs });
    const handler = exec._handlers.find((h) => h.match(cmd));
    return handler ? handler.respond() : null;
  }
  exec._handlers = [];
  exec.calls = calls;
  exec.on = function (substr, respond) {
    exec._handlers.push({
      match: function (cmd) { return cmd.indexOf(substr) !== -1; },
      respond: respond,
    });
    return exec;
  };
  return exec;
}

// Recorder for the argv-form execFile (loginctl). Distinct from
// recordingExec so that injection-guard tests can assert the shell-form
// exec was NEVER called for the loginctl tier.
function recordingExecFile() {
  const calls = [];
  function execFile(file, args, timeoutMs) {
    calls.push({ file: file, args: args, timeoutMs: timeoutMs });
    const handler = execFile._handlers.find((h) => h.match(file));
    return handler ? handler.respond(file, args) : null;
  }
  execFile._handlers = [];
  execFile.calls = calls;
  execFile.on = function (file, respond) {
    execFile._handlers.push({
      match: function (f) { return f === file; },
      respond: respond,
    });
    return execFile;
  };
  return execFile;
}

let savedSessionId;
beforeEach(function () {
  __test.resetLinuxCache();
  __test.setExec(null);     // restore default execSync
  __test.setExecFile(null); // restore default execFileSync
  savedSessionId = process.env.XDG_SESSION_ID;
});
afterEach(function () {
  __test.resetLinuxCache();
  __test.setExec(null);
  __test.setExecFile(null);
  if (savedSessionId === undefined) delete process.env.XDG_SESSION_ID;
  else process.env.XDG_SESSION_ID = savedSessionId;
});

describe('_tryXprintidle (X11)', function () {
  it('parses ms output and returns seconds', function () {
    const exec = recordingExec().on('xprintidle', function () { return '12345'; });
    __test.setExec(exec);
    assert.equal(__test.tryXprintidle(), 12);
  });

  it('returns -1 when xprintidle is missing / errors (null from exec)', function () {
    const exec = recordingExec(); // no handler -> returns null
    __test.setExec(exec);
    assert.equal(__test.tryXprintidle(), -1);
  });

  it('returns -1 on non-numeric output', function () {
    const exec = recordingExec().on('xprintidle', function () { return 'not a number'; });
    __test.setExec(exec);
    assert.equal(__test.tryXprintidle(), -1);
  });

  it('returns -1 on negative output (safety)', function () {
    const exec = recordingExec().on('xprintidle', function () { return '-1'; });
    __test.setExec(exec);
    assert.equal(__test.tryXprintidle(), -1);
  });
});

describe('_tryGnomeMutter (Wayland + X11 GNOME)', function () {
  it('parses gdbus uint64 output and returns seconds', function () {
    const exec = recordingExec().on('gdbus call', function () { return '(uint64 7500,)'; });
    __test.setExec(exec);
    assert.equal(__test.tryGnomeMutter(), 7);
  });

  it('returns -1 when gdbus is missing / no session bus (null)', function () {
    __test.setExec(recordingExec());
    assert.equal(__test.tryGnomeMutter(), -1);
  });

  it('returns -1 when output does not contain a uint64 token', function () {
    const exec = recordingExec().on('gdbus call', function () {
      return 'Error: GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown';
    });
    __test.setExec(exec);
    assert.equal(__test.tryGnomeMutter(), -1);
  });
});

describe('_tryLoginctlIdleHint (systemd-logind universal)', function () {
  it('returns -1 when XDG_SESSION_ID is unset (no logind context)', function () {
    delete process.env.XDG_SESSION_ID;
    const execFile = recordingExecFile().on('loginctl', function () {
      throw new Error('execFile should not be called when session id is missing');
    });
    __test.setExecFile(execFile);
    assert.equal(__test.tryLoginctlIdleHint(), -1);
    assert.equal(execFile.calls.length, 0, 'must short-circuit before forking loginctl');
  });

  it('returns 0 when IdleHint=no (session is active)', function () {
    process.env.XDG_SESSION_ID = '5';
    const execFile = recordingExecFile().on('loginctl', function () {
      return 'IdleHint=no\nIdleSinceHint=0';
    });
    __test.setExecFile(execFile);
    assert.equal(__test.tryLoginctlIdleHint(), 0);
    // Sanity: the session id was passed as a discrete argv element, NOT
    // concatenated into a shell string (which would re-introduce the
    // injection vector that was the whole point of this refactor).
    assert.equal(execFile.calls.length, 1);
    assert.equal(execFile.calls[0].file, 'loginctl');
    assert.deepEqual(execFile.calls[0].args,
      ['show-session', '5', '-p', 'IdleHint', '-p', 'IdleSinceHint']);
  });

  it('computes idle seconds from IdleSinceHint when IdleHint=yes', function () {
    process.env.XDG_SESSION_ID = '5';
    const tenSecondsAgoUsec = (Date.now() - 10_000) * 1000;
    const execFile = recordingExecFile().on('loginctl', function () {
      return 'IdleHint=yes\nIdleSinceHint=' + tenSecondsAgoUsec;
    });
    __test.setExecFile(execFile);
    const idle = __test.tryLoginctlIdleHint();
    // Allow off-by-one second for clock drift between the test snapshot and
    // the function's own Date.now() call.
    assert.ok(idle >= 9 && idle <= 11,
      'idle seconds must round-trip to ~10 — got ' + idle);
  });

  it('returns -1 when IdleHint=yes but IdleSinceHint is missing (malformed)', function () {
    process.env.XDG_SESSION_ID = '5';
    const execFile = recordingExecFile().on('loginctl', function () {
      return 'IdleHint=yes';
    });
    __test.setExecFile(execFile);
    assert.equal(__test.tryLoginctlIdleHint(), -1);
  });

  it('returns -1 when loginctl is missing (null)', function () {
    process.env.XDG_SESSION_ID = '5';
    __test.setExecFile(recordingExecFile());
    assert.equal(__test.tryLoginctlIdleHint(), -1);
  });
});

describe('_tryLoginctlIdleHint — XDG_SESSION_ID injection guard (issue #168)', function () {
  // Pre-fix the loginctl tier concatenated XDG_SESSION_ID into a string
  // command passed to execSync (-> /bin/sh -c). A hostile env value like
  //   XDG_SESSION_ID="1; touch /tmp/marker #"
  // would execute the injected `touch`. Fix is two-layer:
  //   (1) argv-form execFile (no shell parsing at all), AND
  //   (2) reject XDG_SESSION_ID values that are not a pure ASCII-digit
  //       run, before forking.
  // These tests assert BOTH layers — the regex rejection AND the no-call
  // invariant (so the guard cannot regress into a "validate then concat"
  // pattern that would re-open the hole).
  const HOSTILE_VALUES = [
    '1; touch /tmp/pwn',
    '1`touch /tmp/pwn`',
    '1$(touch /tmp/pwn)',
    '1|touch /tmp/pwn',
    '1\ntouch /tmp/pwn',
    '1 2',         // space inside
    '',            // empty (also caught by truthiness)
    'abc',         // non-numeric
    '-1',          // sign char
    '1.5',         // decimal
    '٠١', // Unicode-digit Arabic "01" — the reason we use [0-9] not \d
  ];

  for (const hostile of HOSTILE_VALUES) {
    it('rejects XDG_SESSION_ID=' + JSON.stringify(hostile) + ' without forking', function () {
      process.env.XDG_SESSION_ID = hostile;
      const execFile = recordingExecFile().on('loginctl', function () {
        throw new Error('execFile must NOT be invoked for invalid session id');
      });
      const exec = recordingExec().on('loginctl', function () {
        throw new Error('shell-form exec must NEVER be used for the loginctl tier');
      });
      __test.setExecFile(execFile);
      __test.setExec(exec);
      assert.equal(__test.tryLoginctlIdleHint(), -1);
      assert.equal(execFile.calls.length, 0,
        'guard must reject before forking — got calls: ' + JSON.stringify(execFile.calls));
      assert.equal(exec.calls.length, 0,
        'shell-form exec must not be touched by the loginctl path');
    });
  }
});

describe('_getLinuxIdleSeconds (fallback chain)', function () {
  it('returns xprintidle result without invoking subsequent methods', function () {
    const exec = recordingExec()
      .on('xprintidle', function () { return '5000'; })
      .on('gdbus', function () { throw new Error('must not be reached'); });
    const execFile = recordingExecFile().on('loginctl', function () {
      throw new Error('loginctl must not be reached');
    });
    __test.setExec(exec);
    __test.setExecFile(execFile);
    assert.equal(__test.getLinuxIdleSeconds(), 5);
    assert.equal(exec.calls.length, 1, 'only xprintidle should be invoked');
    assert.ok(exec.calls[0].cmd.indexOf('xprintidle') !== -1);
    assert.equal(execFile.calls.length, 0);
  });

  it('falls through to gnome-mutter when xprintidle fails', function () {
    const exec = recordingExec()
      // xprintidle absent -> exec returns null
      .on('gdbus', function () { return '(uint64 8000,)'; });
    const execFile = recordingExecFile().on('loginctl', function () {
      throw new Error('loginctl must not be reached');
    });
    __test.setExec(exec);
    __test.setExecFile(execFile);
    assert.equal(__test.getLinuxIdleSeconds(), 8);
    const calledCmds = exec.calls.map(function (c) { return c.cmd; });
    assert.equal(calledCmds.length, 2, 'xprintidle then gdbus');
    assert.ok(calledCmds[0].indexOf('xprintidle') !== -1);
    assert.ok(calledCmds[1].indexOf('gdbus call') !== -1);
    assert.equal(execFile.calls.length, 0);
  });

  it('falls through to loginctl when xprintidle and gdbus both fail (the Wayland-on-KDE case)', function () {
    process.env.XDG_SESSION_ID = '5';
    const exec = recordingExec(); // xprintidle + gdbus both return null
    const execFile = recordingExecFile().on('loginctl', function () {
      return 'IdleHint=no\nIdleSinceHint=0';
    });
    __test.setExec(exec);
    __test.setExecFile(execFile);
    const idle = __test.getLinuxIdleSeconds();
    assert.equal(idle, 0, 'IdleHint=no must surface as 0 (active)');
    assert.equal(exec.calls.length, 2, 'xprintidle + gdbus tried before loginctl');
    assert.equal(execFile.calls.length, 1, 'loginctl reached as third tier');
  });

  it('returns -1 when every method fails (no fallback available)', function () {
    delete process.env.XDG_SESSION_ID;
    __test.setExec(recordingExec());         // xprintidle + gdbus -> null
    __test.setExecFile(recordingExecFile()); // loginctl short-circuits on no session id
    assert.equal(__test.getLinuxIdleSeconds(), -1);
  });

  it('caches the winning method so subsequent calls fork one subprocess, not three', function () {
    process.env.XDG_SESSION_ID = '5';
    const exec = recordingExec(); // xprintidle + gdbus both null
    const execFile = recordingExecFile().on('loginctl', function () {
      return 'IdleHint=no\nIdleSinceHint=0';
    });
    __test.setExec(exec);
    __test.setExecFile(execFile);

    __test.getLinuxIdleSeconds(); // discovers loginctl
    assert.equal(__test.getCachedMethod(), 'loginctl');
    const execCallsAfterDiscovery = exec.calls.length;
    const execFileCallsAfterDiscovery = execFile.calls.length;

    __test.getLinuxIdleSeconds(); // should reuse cached method
    __test.getLinuxIdleSeconds();
    assert.equal(exec.calls.length - execCallsAfterDiscovery, 0,
      'shell-form exec must NOT be invoked once loginctl is the cached winner');
    assert.equal(execFile.calls.length - execFileCallsAfterDiscovery, 2,
      'each subsequent tick must fork only the cached loginctl call');
  });

  it('re-discovers when the cached method stops working (session-type change)', function () {
    process.env.XDG_SESSION_ID = '5';
    let xprintidleAvailable = true;
    const exec = recordingExec()
      .on('xprintidle', function () { return xprintidleAvailable ? '1000' : null; });
    const execFile = recordingExecFile().on('loginctl', function () {
      return 'IdleHint=no\nIdleSinceHint=0';
    });
    __test.setExec(exec);
    __test.setExecFile(execFile);

    assert.equal(__test.getLinuxIdleSeconds(), 1);
    assert.equal(__test.getCachedMethod(), 'xprintidle');

    // Simulate xprintidle going away (e.g. user logged out of X11 and into
    // Wayland). Cached method now fails — chain must re-discover.
    xprintidleAvailable = false;
    assert.equal(__test.getLinuxIdleSeconds(), 0, 'must fall back to loginctl');
    assert.equal(__test.getCachedMethod(), 'loginctl', 'cache must update to the new winner');
  });
});
