/*
  auto_fix.js
  - Clone a repo, run lint/format/fix commands (eslint --fix, prettier --write), run tests,
    commit and push changes, and open a PR with the fixes.
  - Minimal, opinionated: expects a Node.js repo with package.json scripts:
      - lint (optional) -> will run "npm run lint -- --fix" if present
      - format (optional) -> will run "npm run format" if present
      - test -> runs "npm test"
  - Requires GH_TOKEN and GIT_AUTHOR_NAME / GIT_AUTHOR_EMAIL in env for commits.
*/

require('dotenv').config();
const { Octokit } = require('@octokit/rest');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const token = process.env.GH_TOKEN;
if (!token) throw new Error('GH_TOKEN required');
const octokit = new Octokit({ auth: token });

const tmpBase = process.env.TMPDIR || '/tmp';

async function autoFixRepo(fullName, options = {}) {
  const [owner, repo] = fullName.split('/');
  const cloneUrl = `https://x-access-token:${token}@github.com/${owner}/${repo}.git`;
  const workdir = path.join(tmpBase, `gh-autofix-${owner}-${repo}-${Date.now()}`);
  fs.mkdirSync(workdir, { recursive: true });

  console.log('cloning', fullName, 'to', workdir);
  execSync(`git clone --depth 1 ${cloneUrl} ${workdir}`, { stdio: 'inherit' });

  // install deps if package.json exists
  const pkgPath = path.join(workdir, 'package.json');
  const hasPkg = fs.existsSync(pkgPath);
  try {
    if (hasPkg) {
      console.log('Installing dependencies...');
      execSync('npm ci --no-audit --no-fund', { cwd: workdir, stdio: 'inherit' });

      // run lint with --fix if available
      const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
      if (pkg.scripts && pkg.scripts.lint) {
        try {
          console.log('Running lint --fix');
          execSync('npm run lint -- --fix', { cwd: workdir, stdio: 'inherit' });
        } catch (e) { console.warn('lint failed or not fixable'); }
      }

      // run format if present, otherwise try prettier --write if installed
      if (pkg.scripts && pkg.scripts.format) {
        try { console.log('Running format'); execSync('npm run format', { cwd: workdir, stdio: 'inherit' }); } catch (e) { console.warn('format failed'); }
      } else {
        // try npx prettier
        try { console.log('Running prettier --write .'); execSync('npx prettier --write .', { cwd: workdir, stdio: 'inherit' }); } catch (e) { /* ignore */ }
      }

      // run tests
      let testsOk = false;
      if (pkg.scripts && pkg.scripts.test) {
        try {
          console.log('Running tests');
          execSync('npm test -- --silent', { cwd: workdir, stdio: 'inherit' });
          testsOk = true;
        } catch (e) { console.warn('tests failed or missing'); }
      }
    }

    // check git status
    const status = execSync('git status --porcelain', { cwd: workdir }).toString().trim();
    if (!status) {
      console.log('No changes to commit. Nothing to do.');
      return { changed: false };
    }

    // commit and push
    const branch = options.branch || `auto-fix/${Date.now()}`;
    execSync(`git checkout -b ${branch}`, { cwd: workdir });

    // set author if provided
    const authorName = process.env.GIT_AUTHOR_NAME || 'autofix-bot';
    const authorEmail = process.env.GIT_AUTHOR_EMAIL || 'autofix-bot@example.com';
    execSync(`git config user.name "${authorName}"`, { cwd: workdir });
    execSync(`git config user.email "${authorEmail}"`, { cwd: workdir });

    execSync('git add -A', { cwd: workdir });
    execSync('git commit -m "chore: automated lint/format fixes" || true', { cwd: workdir, stdio: 'inherit' });
    execSync(`git push origin HEAD:${branch}`, { cwd: workdir, stdio: 'inherit' });

    // open PR
    const title = options.title || 'Automated lint/format fixes';
    const body = options.body || 'This PR applies automated fixes (eslint --fix, prettier, minor formatting). Please review.';

    const pr = await octokit.pulls.create({ owner, repo, title, head: branch, base: options.base || 'main', body });
    console.log('PR created:', pr.data.html_url);
    return { changed: true, pr: pr.data.html_url };
  } catch (err) {
    console.error('autoFix failed', err.message);
    return { changed: false, error: err.message };
  } finally {
    // cleanup: leave for inspection, or uncomment to remove
    // fs.rmSync(workdir, { recursive: true, force: true });
  }
}

module.exports = { autoFixRepo };

// allow CLI usage: node auto_fix.js owner/repo
if (require.main === module) {
  const repo = process.argv[2];
  if (!repo) { console.error('usage: node auto_fix.js owner/repo'); process.exit(2); }
  autoFixRepo(repo).then(r => { console.log('done', r); }).catch(e => { console.error(e); process.exit(1); });
}
