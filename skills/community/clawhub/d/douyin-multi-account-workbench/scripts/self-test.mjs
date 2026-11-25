import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { aggregateResults, ATOMIC_SCRIPTS, buildScriptDraft, createExecutionPlan, dependencyStatus, DEPENDENCY_INSTALLS, OPTIONAL_SKILLS, renderMarkdown, runWorkbench, validateDependencies, validateInput } from './workbench.mjs';

const success = JSON.parse(fs.readFileSync(new URL('../fixtures/success.json', import.meta.url)));
const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'douyin-multi-account-workbench-'));
const result = validateInput(success);
if (result.accounts.length !== 2 || result.mode !== 'mock') process.exit(1);
const plan = createExecutionPlan(success);
if (!plan[0].tasks.some((task) => task.skill === 'douyin-account-diagnosis') || !plan[0].session) process.exit(1);
if (!plan[0].tasks.some((task) => task.task === 'hot-topic') || !plan[0].tasks.some((task) => task.task === 'script')) process.exit(1);
const report = aggregateResults(success, [
  { accountId: 'account-a', status: 'completed', results: [{ task: 'diagnosis' }], evidence: ['https://www.douyin.com/video/1'] },
  { accountId: 'account-b', status: 'needs_user_action', results: [], evidence: [], error: '登录失效' }
]);
if (report.summary.completed !== 1 || report.summary.needsUserAction !== 1 || !report.accounts[0].scriptDraft?.hook || !renderMarkdown(report).includes('account-a')) process.exit(1);
if (!buildScriptDraft(success.accounts[0], { topic: 'AI 工具' }).title.includes('account-a')) process.exit(1);
const missingRoot = path.join(temp, 'missing-skills');
const missingStatus = await validateDependencies(missingRoot);
if (!OPTIONAL_SKILLS.every((skill) => !missingStatus[skill]?.installed && DEPENDENCY_INSTALLS[skill]?.repository && DEPENDENCY_INSTALLS[skill]?.installCommand)) process.exit(1);
const installedRoot = path.join(temp, 'installed-skills');
for (const skill of OPTIONAL_SKILLS) {
  const dir = path.join(installedRoot, skill);
  const script = path.join(dir, ATOMIC_SCRIPTS[skill]);
  fs.mkdirSync(path.dirname(script), { recursive: true });
  fs.writeFileSync(path.join(dir, 'SKILL.md'), `---\nname: ${skill}\n---\n`);
  fs.writeFileSync(script, '// offline dependency fixture\n');
}
const installedStatus = await dependencyStatus(installedRoot);
if (!OPTIONAL_SKILLS.every((skill) => installedStatus[skill]?.installed)) process.exit(1);
const runOutput = path.join(temp, 'workbench-run');
const runReport = await runWorkbench(success, { outputDir: runOutput, rootDir: missingRoot, runAtoms: false });
if (!runReport.accounts.every((account) => account.scriptDraft?.title) || !fs.existsSync(path.join(runOutput, 'multi-account-workbench.json')) || !fs.existsSync(path.join(runOutput, 'multi-account-workbench.md'))) process.exit(1);
const optionalOutput = path.join(temp, 'optional-dependencies-run');
const optionalReport = await runWorkbench({ ...success, tasks: ['diagnosis', 'script'] }, { outputDir: optionalOutput, rootDir: missingRoot, runAtoms: true });
if (!optionalReport.accounts.every((account) => account.status === 'partial' && account.results.some((item) => item.task === 'diagnosis' && item.status === 'unavailable') && account.results.some((item) => item.task === 'script' && item.status === 'completed'))) process.exit(1);
if (optionalReport.summary.unavailableTasks !== success.accounts.length || !renderMarkdown(optionalReport).includes('npx skills add xxjrq/douyin-account-diagnosis')) process.exit(1);
let failed = false;
try { validateInput(JSON.parse(fs.readFileSync(new URL('../fixtures/failure.json', import.meta.url)))); } catch { failed = true; }
if (!failed) process.exit(1);
fs.rmSync(temp, { recursive: true, force: true });
console.log('douyin-multi-account-workbench self-test passed');
