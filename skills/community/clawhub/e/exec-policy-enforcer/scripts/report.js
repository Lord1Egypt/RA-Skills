const fs = require('fs');
const path = require('path');

const reportPath = process.argv[2] || path.join(process.env.WORKSPACE_ROOT || process.cwd(), 'memory/evolution/exec-policy-report.json');

function ensureDir(file) {
  const dir = path.dirname(file);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function main() {
  ensureDir(reportPath);
  const payload = {
    generated_at: new Date().toISOString(),
    note: 'exec-policy enforcer local report stub'
  };
  fs.writeFileSync(reportPath, JSON.stringify(payload, null, 2) + '\n', 'utf8');
  console.log('wrote ' + reportPath);
  return 0;
}

if (require.main === module) {
  process.exit(main());
}

module.exports = { main };
