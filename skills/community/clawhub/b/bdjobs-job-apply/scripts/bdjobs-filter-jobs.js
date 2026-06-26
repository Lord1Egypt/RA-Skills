const fs = require('fs');
const path = require('path');

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

(async () => {
  const root = process.cwd();
  const dataDir = path.join(root, 'data');
  const appliedIds = new Set((readJson(path.join(dataDir, 'appliedJobIds.json')) || []).map(String));
  const input = JSON.parse(fs.readFileSync(0, 'utf8'));
  const filtered = input.filter(job => !appliedIds.has(String(job.jobId)));
  console.log(JSON.stringify(filtered, null, 2));
})().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});
