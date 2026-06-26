const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const janitor = require('./janitor.js');
const { isSafeToClean, getDirSize, safeRemoveDir, VALID_GROUPS } = janitor.__private;

function mkTmp(name) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `cj-${name}-`));
}

function runTests() {
  // 1) Blacklist tree protection
  {
    const blocked = path.resolve(path.join(os.homedir(), '.openclaw', 'workspace', 'x'));
    assert.strictEqual(isSafeToClean(blocked), false, 'workspace subtree must be blocked');
  }

  // 2) Regex protection (.env/.git)
  {
    const envPath = path.resolve('/tmp/project/.env');
    const gitPath = path.resolve('/tmp/project/.git/config');
    assert.strictEqual(isSafeToClean(envPath), false, '.env path must be blocked');
    assert.strictEqual(isSafeToClean(gitPath), false, '.git path must be blocked');
  }

  // 3) Symlink safety in getDirSize
  {
    const base = mkTmp('symlink');
    const target = path.join(base, 'target.txt');
    const link = path.join(base, 'link.txt');
    fs.writeFileSync(target, '1234567890');
    fs.symlinkSync(target, link);
    const size = getDirSize(base);
    assert(size >= 10, 'real file should count');
    assert(size < 1000, 'symlink should not explode size');
    fs.rmSync(base, { recursive: true, force: true });
  }

  // 4) safeRemoveDir basic behavior
  {
    const base = mkTmp('remove');
    const child = path.join(base, 'a', 'b');
    fs.mkdirSync(child, { recursive: true });
    fs.writeFileSync(path.join(child, 'f.txt'), 'ok');
    const dev = fs.lstatSync(base).dev;
    safeRemoveDir(base, dev);
    assert.strictEqual(fs.existsSync(base), false, 'safeRemoveDir should remove tree on same device');
  }

  // 5) CWD sealing
  {
    const cwdChild = path.join(process.cwd(), 'tmp-test-child');
    assert.strictEqual(isSafeToClean(cwdChild), false, 'cwd subtree must be blocked');
  }

  // 6) Dry-run snapshot sanity
  {
    const out = execFileSync(process.execPath, [path.join(__dirname, 'janitor.js'), '--dry-run'], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe']
    });
    assert(out.includes('DRY RUN MODE'), 'dry-run banner missing');
    assert(out.includes('Total Space Can Be Reclaimed'), 'dry-run summary missing');
  }

  // 7) no-color output should not contain ANSI escapes
  {
    const out = execFileSync(process.execPath, [path.join(__dirname, 'janitor.js'), '--dry-run', '--no-color'], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe']
    });
    assert(!/\x1b\[[0-9;]*m/.test(out), 'no-color output contains ANSI escape codes');
  }

  // 8) json mode should be parseable and stable keys present
  {
    const out = execFileSync(process.execPath, [path.join(__dirname, 'janitor.js'), '--dry-run', '--json'], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe']
    });
    const parsed = JSON.parse(out);
    assert(Array.isArray(parsed.actions), 'json actions must be an array');
    assert(Object.prototype.hasOwnProperty.call(parsed, 'reclaimedBytes'), 'json reclaimedBytes missing');
  }

  // 9) only/skip groups and report file
  {
    assert(VALID_GROUPS.has('packages'), 'packages group missing');
    const reportPath = path.join(mkTmp('report'), 'out.json');
    execFileSync(process.execPath, [
      path.join(__dirname, 'janitor.js'),
      '--dry-run',
      '--json',
      '--only', 'packages',
      '--skip', 'docker',
      '--report-file', reportPath
    ], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });

    const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
    assert.strictEqual(report.onlyGroup, 'packages', 'onlyGroup not set in report');
    assert.strictEqual(report.skipGroup, 'docker', 'skipGroup not set in report');
  }

  // 10) safeRemoveDir should re-check blacklist during recursion
  {
    const base = mkTmp('nested-blacklist');
    const safeDir = path.join(base, 'cache');
    const blockedDir = path.join(safeDir, '.git');
    fs.mkdirSync(blockedDir, { recursive: true });
    fs.writeFileSync(path.join(blockedDir, 'config'), 'protected');
    fs.writeFileSync(path.join(safeDir, 'normal.txt'), 'normal');

    const dev = fs.lstatSync(base).dev;
    safeRemoveDir(safeDir, dev);

    assert.strictEqual(fs.existsSync(path.join(blockedDir, 'config')), true, '.git subtree must remain protected');
    // cleanup tmp root to avoid leftovers
    fs.rmSync(base, { recursive: true, force: true });
  }

  // 11) help output
  {
    const out = execFileSync(process.execPath, [path.join(__dirname, 'janitor.js'), '--help'], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe']
    });
    assert(out.includes('Usage:'), 'help usage missing');
    assert(out.includes('--report-file'), 'help options missing');
  }

  console.log('claw-janitor tests: PASS');
}

runTests();
