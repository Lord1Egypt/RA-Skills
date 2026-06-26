// Simple gh-triage prototype
require('dotenv').config();
const { Octokit } = require('@octokit/rest');
const cron = require('node-cron');

const token = process.env.GH_TOKEN;
if (!token) {
  console.error('GH_TOKEN not set — exiting');
  process.exit(1);
}
const octokit = new Octokit({ auth: token });

const config = require('./config.example.json');

async function processRepo(fullName) {
  const [owner, repo] = fullName.split('/');
  const issues = await octokit.issues.listForRepo({ owner, repo, state: 'open', per_page: 50 });
  for (const issue of issues.data) {
    // skip pull requests here
    if (issue.pull_request) continue;
    const title = issue.title.toLowerCase();
    // simple label rule
    if (/typo|docs/.test(title)) {
      await octokit.issues.addLabels({ owner, repo, issue_number: issue.number, labels: ['documentation'] }).catch(()=>{});
    }
    // assign maintainers if enabled and unassigned
    if (config.rules.auto_assign && (!issue.assignee || issue.assignee==null)) {
      const assignees = config.rules.maintainers || [];
      if (assignees.length) await octokit.issues.addAssignees({ owner, repo, issue_number: issue.number, assignees }).catch(()=>{});
    }
  }
}

async function run() {
  for (const repo of config.repos) {
    try { await processRepo(repo); } catch (e) { console.error('repo error', repo, e.message); }
  }
}

cron.schedule(config.cron || '0 */1 * * *', () => {
  console.log(new Date().toISOString(), 'running gh-triage');
  run();
});

// allow manual run
if (require.main === module) run();
