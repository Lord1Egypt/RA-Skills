const fs = require('fs');
const path = require('path');

function toMarkdown(input) {
  return String(input).trim() + '\n';
}

const root = process.cwd();
const dataDir = path.join(root, 'data');
const resume = process.argv.slice(2).join(' ').trim();

if (!resume) {
  console.error('Usage: node init-job-profile.js "<resume text or latex>"');
  process.exit(1);
}

fs.mkdirSync(dataDir, { recursive: true });
fs.writeFileSync(path.join(dataDir, 'resume.md'), toMarkdown(resume));
console.log('Wrote data/resume.md');
