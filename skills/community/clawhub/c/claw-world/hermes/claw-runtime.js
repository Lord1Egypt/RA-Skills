'use strict';

const { fork } = require('child_process');
const path = require('path');

const DEFAULT_TIMEOUT_MS = 120000;
const JSON_COMMANDS = new Set([
  'env',
  'owned',
  'boot',
  'status',
  'cml-load',
  'cml-save',
  'cml-recall',
  'cml-match',
  'pk-scout',
  'pk-status',
  'pk-search',
  'world',
  'market-search',
  'withdraw-status',
  'leaderboard',
  'rank',
  'supply'
]);

function buildError(message, details) {
  const error = new Error(message);
  if (details && typeof details === 'object') {
    Object.assign(error, details);
  }
  return error;
}

function parseJson(stdout, command) {
  try {
    return JSON.parse(stdout);
  } catch (error) {
    throw buildError('Failed to parse JSON output for claw ' + command, {
      code: 'PARSE_ERROR',
      stdout,
      cause: error
    });
  }
}

function parseLineOutput(stdout, stderr, exitCode) {
  const lines = stdout.split(/\r?\n/).map(function(line) { return line.trim(); }).filter(Boolean);
  const errorLines = stderr.split(/\r?\n/).map(function(line) { return line.trim(); }).filter(Boolean);
  return {
    ok: exitCode === 0,
    exitCode,
    lines,
    stdout,
    stderr,
    errorLines,
    markers: {
      txHash: (stdout.match(/(?:^|\n)TX:\s*([^\s]+)/) || [])[1] || null,
      confirmedBlock: Number(((stdout.match(/(?:CONFIRMED|MATCH_CREATED|JOINED\+COMMITTED|JOINED|COMMITTED|REVEALED|SETTLED|CANCELLED|LISTED|AUCTION_CREATED|BOUGHT|BID_PLACED|TRANSFERRED):.*block=(\d+)/) || [])[1]) || 0) || null,
      notOwner: errorLines.some(function(line) { return line.indexOf('NOT_OWNER:') === 0; }),
      noWallet: errorLines.some(function(line) { return line.indexOf('NO_WALLET') === 0; }) || lines.some(function(line) { return line === 'NO_WALLET'; }),
      insufficientClw: lines.some(function(line) { return line.indexOf('INSUFFICIENT_CLW:') === 0; }),
      cancelFailed: errorLines.some(function(line) { return line.indexOf('CANCEL_FAILED:') === 0; }) || lines.some(function(line) { return line.indexOf('CANCEL_FAILED:') === 0; }),
      noPendingWithdrawal: lines.some(function(line) { return line === 'NO_PENDING_WITHDRAWAL'; })
    }
  };
}

class ClawRuntime {
  constructor(options) {
    const settings = options || {};
    this.skillDir = settings.skillDir || path.resolve(__dirname, '..');
    this.clawPath = settings.clawPath || path.join(this.skillDir, 'claw');
    this.timeoutMs = settings.timeoutMs || DEFAULT_TIMEOUT_MS;
  }

  run(command, args, options) {
    const runOptions = options || {};
    const finalArgs = Array.isArray(args) ? args.filter(function(value) { return value !== undefined && value !== null; }).map(String) : [];
    const expectJson = runOptions.expectJson !== false && JSON_COMMANDS.has(command);
    const stdin = runOptions.stdin == null ? null : String(runOptions.stdin);
    const timeoutMs = runOptions.timeoutMs || this.timeoutMs;
    const self = this;

    return new Promise(function(resolve, reject) {
      const child = fork(self.clawPath, [command].concat(finalArgs), {
        cwd: self.skillDir,
        silent: true,
        stdio: ['pipe', 'pipe', 'pipe', 'ipc']
      });

      let stdout = '';
      let stderr = '';
      let settled = false;
      let timer = null;

      function finish(fn, value) {
        if (settled) return;
        settled = true;
        if (timer) clearTimeout(timer);
        fn(value);
      }

      if (timeoutMs > 0) {
        timer = setTimeout(function() {
          child.kill();
          finish(reject, buildError('claw ' + command + ' timed out', { code: 'TIMEOUT', command, args: finalArgs }));
        }, timeoutMs);
      }

      child.stdout.on('data', function(chunk) { stdout += chunk.toString(); });
      child.stderr.on('data', function(chunk) { stderr += chunk.toString(); });
      child.on('error', function(error) {
        finish(reject, buildError('Failed to start claw ' + command, {
          code: 'SPAWN_ERROR',
          command,
          args: finalArgs,
          cause: error
        }));
      });

      child.on('close', function(exitCode) {
        const trimmedStdout = stdout.trim();
        const trimmedStderr = stderr.trim();

        if (exitCode !== 0) {
          finish(reject, buildError('claw ' + command + ' failed', {
            code: 'COMMAND_FAILED',
            command,
            args: finalArgs,
            exitCode,
            stdout: trimmedStdout,
            stderr: trimmedStderr,
            parsed: parseLineOutput(trimmedStdout, trimmedStderr, exitCode)
          }));
          return;
        }

        try {
          const parsed = expectJson
            ? parseJson(trimmedStdout, command)
            : parseLineOutput(trimmedStdout, trimmedStderr, exitCode);

          finish(resolve, {
            command,
            args: finalArgs,
            exitCode,
            stdout: trimmedStdout,
            stderr: trimmedStderr,
            parsed
          });
        } catch (error) {
          finish(reject, error);
        }
      });

      if (stdin != null) {
        child.stdin.write(stdin);
      }
      child.stdin.end();
    });
  }

  env() { return this.run('env', []); }
  owned() { return this.run('owned', []); }
  boot() { return this.run('boot', []); }
  status(tokenId) { return this.run('status', [tokenId]); }
  wallet() { return this.run('wallet', [], { expectJson: false }); }
  world() { return this.run('world', []); }
  supply() { return this.run('supply', []); }
  leaderboard(metric) { return this.run('leaderboard', metric ? [metric] : []); }
  rank(tokenId) { return this.run('rank', [tokenId]); }
  marketSearch() { return this.run('market-search', []); }
  pkSearch() { return this.run('pk-search', []); }
  pkScout(matchId) { return this.run('pk-scout', [matchId]); }
  pkStatus(matchId) { return this.run('pk-status', [matchId]); }
  withdrawStatus(tokenId) { return this.run('withdraw-status', [tokenId], { expectJson: true }); }
  cmlLoad(tokenId, full) { return this.run('cml-load', full ? [tokenId, '--full'] : [tokenId]); }
  cmlSave(tokenId, cml, auth) {
    return this.run('cml-save', auth ? [tokenId, auth] : [tokenId], {
      stdin: JSON.stringify(cml, null, 2)
    });
  }

  task(pin, tokenId, taskType, xp, clw, score) { return this.run('task', [pin, tokenId, taskType, xp, clw, score], { expectJson: false }); }
  deposit(pin, tokenId, amount) { return this.run('deposit', [pin, tokenId, amount], { expectJson: false }); }
  fundBnb(pin, tokenId, amount) { return this.run('fund-bnb', [pin, tokenId, amount], { expectJson: false }); }
  upkeep(pin, tokenId) { return this.run('upkeep', [pin, tokenId], { expectJson: false }); }
  transfer(pin, tokenId, toAddress) { return this.run('transfer', [pin, tokenId, toAddress], { expectJson: false }); }
  marketList(pin, tokenId, priceBnb) { return this.run('market-list', [pin, tokenId, priceBnb], { expectJson: false }); }
  marketAuction(pin, tokenId, startPrice) { return this.run('market-auction', [pin, tokenId, startPrice], { expectJson: false }); }
  marketBuy(pin, listingId, priceBnb) { return this.run('market-buy', [pin, listingId, priceBnb], { expectJson: false }); }
  marketBid(pin, listingId, bidBnb) { return this.run('market-bid', [pin, listingId, bidBnb], { expectJson: false }); }
  marketCancel(pin, listingId) { return this.run('market-cancel', [pin, listingId], { expectJson: false }); }
  withdrawRequest(pin, tokenId, amount) { return this.run('withdraw-request', [pin, tokenId, amount], { expectJson: false }); }
  withdrawClaim(pin, tokenId) { return this.run('withdraw-claim', [pin, tokenId], { expectJson: false }); }
  withdrawCancel(pin, tokenId) { return this.run('withdraw-cancel', [pin, tokenId], { expectJson: false }); }
  pkCreate(pin, tokenId, stake, strategy) { return this.run('pk-create', strategy === undefined ? [pin, tokenId, stake] : [pin, tokenId, stake, strategy], { expectJson: false }); }
  pkJoin(pin, matchId, tokenId, strategy) { return this.run('pk-join', strategy === undefined ? [pin, matchId, tokenId] : [pin, matchId, tokenId, strategy], { expectJson: false }); }
  pkCommit(pin, matchId, strategy) { return this.run('pk-commit', [pin, matchId, strategy], { expectJson: false }); }
  pkReveal(pin, matchId) { return this.run('pk-reveal', [pin, matchId], { expectJson: false }); }
  pkSettle(pin, matchId) { return this.run('pk-settle', [pin, matchId], { expectJson: false }); }
  pkCancel(pin, matchId) { return this.run('pk-cancel', [pin, matchId], { expectJson: false }); }
  pkAutoSettle(pin, matchId, pin2) { return this.run('pk-auto-settle', pin2 ? [pin, matchId, pin2] : [pin, matchId], { expectJson: false }); }

  raw(command, args, options) {
    return this.run(command, args, options);
  }
}

module.exports = {
  ClawRuntime,
  JSON_COMMANDS,
  parseLineOutput
};
