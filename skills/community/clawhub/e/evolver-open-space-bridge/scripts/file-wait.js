/**
 * file-wait.js - File write readiness detection
 * Polls for file existence and stable size
 */

const { execSync } = require('child_process');

async function waitForFile(filePath, timeoutMs = 120000, stableChecks = 3, intervalMs = 1000) {
  const start = Date.now();
  let lastSize = -1;
  let stableCount = 0;

  while (Date.now() - start < timeoutMs) {
    try {
      const stat = execSync(`stat -c %s '${filePath}' 2>/dev/null || echo MISSING`, {
        encoding: 'utf-8',
        timeout: 10,
        stdio: ['pipe', 'pipe', 'pipe']
      }).trim();

      if (stat === 'MISSING') {
        stableCount = 0;
        await new Promise(r => setTimeout(r, intervalMs));
        continue;
      }

      const size = parseInt(stat, 10);
      if (isNaN(size)) {
        stableCount = 0;
        await new Promise(r => setTimeout(r, intervalMs));
        continue;
      }

      if (size === lastSize && size > 0) {
        stableCount++;
        if (stableCount >= stableChecks) {
          return { ready: true, size, path: filePath };
        }
      } else {
        stableCount = 0;
        lastSize = size;
      }
    } catch (e) {
      stableCount = 0;
    }

    await new Promise(r => setTimeout(r, intervalMs));
  }

  return {
    ready: false,
    timeout: true,
    elapsed: Date.now() - start,
    lastSize,
    path: filePath
  };
}

function test() {
  const path = '/mnt/c/Users/Admin/.openclaw/workspace/output/test-file-wait.xlsx';
  waitForFile(path, 5000).then(result => {
    console.log('Wait result:', result);
  });
}

if (require.main === module) {
  test();
}

module.exports = { waitForFile };
