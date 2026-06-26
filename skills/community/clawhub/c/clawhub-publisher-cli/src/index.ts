#!/usr/bin/env node
import path from 'node:path';
import fs from 'node:fs';
import { Command } from 'commander';
import { createInterface } from 'node:readline/promises';
import yaml from 'js-yaml';
import fse from 'fs-extra';
import chalk from 'chalk';
import archiver from 'archiver';
import { execa } from 'execa';

const DEFAULT_OUTPUT_ROOT = '.clawhub-publisher';
const TEXT_EXTENSIONS = new Set([
  '.md', '.txt', '.json', '.yaml', '.yml', '.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx', '.css', '.scss', '.html',
  '.sh', '.bash', '.zsh', '.py', '.rb', '.php', '.java', '.kt', '.kts', '.xml', '.gradle', '.properties', '.toml',
  '.ini', '.env', '.gitignore', '.npmrc', '.editorconfig'
]);
const BINARY_EXTENSIONS = new Set(['.png', '.jpg', '.jpeg', '.gif', '.webp', '.pdf', '.zip', '.ico']);
const EXCLUDED_DIRS = new Set(['.git', 'node_modules', 'dist', 'build', '.next', '.clawhub', '.DS_Store']);
const EXCLUDED_FILES = new Set(['.DS_Store', 'Thumbs.db']);
const SEMVER_RE = /^v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z-.]+)?(?:\+[0-9A-Za-z-.]+)?$/;

type Severity = 'error' | 'warning' | 'info';

type Issue = {
  severity: Severity;
  code: string;
  message: string;
  file?: string;
  hint?: string;
};

type ValidationResult = {
  skillDir: string;
  issues: Issue[];
  stats: {
    fileCount: number;
    emptyFiles: number;
    likelyHookFiles: number;
    binaryFiles: number;
    docsFiles: number;
  };
  metadata: {
    name?: string;
    description?: string;
    tags?: string[];
    hooks?: string[];
    frontmatterRaw?: Record<string, unknown>;
  };
};

type PrepareResult = {
  outputDir: string;
  zipPath?: string;
  copiedFiles: string[];
  removedFiles: string[];
  reportPath: string;
  validation: ValidationResult;
};

function resolvePath(input: string) {
  return path.resolve(process.cwd(), input);
}

async function exists(p: string) {
  return fse.pathExists(p);
}

async function readText(p: string) {
  return fse.readFile(p, 'utf8');
}

function normalizeLines(text: string) {
  return text.replace(/\r\n/g, '\n').replace(/[ \t]+$/gm, '') + (text.endsWith('\n') ? '' : '\n');
}

function parseFrontmatter(markdown: string): { data: Record<string, unknown> | null; body: string; error?: string } {
  if (!markdown.startsWith('---\n')) return { data: null, body: markdown };
  const end = markdown.indexOf('\n---\n', 4);
  if (end === -1) {
    return { data: null, body: markdown, error: 'Frontmatter start found, but closing --- block is missing.' };
  }
  const raw = markdown.slice(4, end);
  const body = markdown.slice(end + 5);
  try {
    const parsed = yaml.load(raw);
    if (parsed && typeof parsed !== 'object') {
      return { data: null, body, error: 'Frontmatter must be a YAML object.' };
    }
    return { data: (parsed as Record<string, unknown>) ?? {}, body };
  } catch (error) {
    return { data: null, body, error: `Invalid YAML frontmatter: ${(error as Error).message}` };
  }
}

async function walk(dir: string, root = dir): Promise<string[]> {
  const entries = await fse.readdir(dir, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    const abs = path.join(dir, entry.name);
    const rel = path.relative(root, abs);
    if (entry.isDirectory()) {
      if (EXCLUDED_DIRS.has(entry.name)) continue;
      files.push(...await walk(abs, root));
    } else {
      if (EXCLUDED_FILES.has(entry.name)) continue;
      files.push(rel);
    }
  }
  return files.sort();
}

function inferSlug(skillDir: string, metadataName?: string) {
  const base = metadataName || path.basename(skillDir);
  return base.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

function getExtension(rel: string) {
  const base = path.basename(rel);
  if (base.startsWith('.')) return base;
  return path.extname(rel).toLowerCase();
}

function isTextFile(rel: string) {
  const ext = getExtension(rel);
  return TEXT_EXTENSIONS.has(ext) || !BINARY_EXTENSIONS.has(ext);
}

function isBinaryFile(rel: string) {
  return BINARY_EXTENSIONS.has(getExtension(rel));
}

function countBySeverity(issues: Issue[]) {
  return {
    errors: issues.filter(issue => issue.severity === 'error').length,
    warnings: issues.filter(issue => issue.severity === 'warning').length,
    info: issues.filter(issue => issue.severity === 'info').length,
  };
}

function collectStringPaths(input: unknown): string[] {
  if (typeof input === 'string') return input.trim() ? [input.trim()] : [];
  if (!Array.isArray(input)) return [];
  return input.flatMap(item => typeof item === 'string' && item.trim() ? [item.trim()] : []);
}

function isLikelyHookFile(rel: string) {
  return rel.startsWith('hooks/') || /(^|\/)(hooks?|preinstall|postinstall|install)(\.|$)/i.test(rel);
}

function formatIssue(issue: Issue) {
  const color = issue.severity === 'error' ? chalk.red : issue.severity === 'warning' ? chalk.yellow : chalk.blue;
  const head = `${issue.severity.toUpperCase()} [${issue.code}] ${issue.file ? `${issue.file}: ` : ''}${issue.message}`;
  return color(issue.hint ? `${head}\n  hint: ${issue.hint}` : head);
}

function formatIssues(issues: Issue[]) {
  if (!issues.length) return chalk.green('No issues found.');
  return issues.map(formatIssue).join('\n');
}

function printValidationOverview(result: ValidationResult) {
  const counts = countBySeverity(result.issues);
  console.log(chalk.bold(`Validation summary: ${result.stats.fileCount} files scanned`));
  console.log(`Errors: ${counts.errors}  Warnings: ${counts.warnings}  Info: ${counts.info}`);
  console.log(`Hooks: ${result.stats.likelyHookFiles}  Docs: ${result.stats.docsFiles}  Binary: ${result.stats.binaryFiles}  Empty: ${result.stats.emptyFiles}`);
  if (result.metadata.name || result.metadata.description) {
    console.log(`Metadata: ${result.metadata.name || '(missing name)'}${result.metadata.description ? ` — ${result.metadata.description}` : ''}`);
  }
  console.log(formatIssues(result.issues));
  if (!counts.errors) {
    const nextStep = counts.warnings ? 'You can prepare/publish now, but fixing warnings will make the package cleaner.' : 'Ready to prepare or publish.';
    console.log(chalk.green(nextStep));
  }
}

async function validateSkill(skillDir: string): Promise<ValidationResult> {
  const issues: Issue[] = [];
  const absDir = resolvePath(skillDir);
  if (!(await exists(absDir))) throw new Error(`Skill folder not found: ${absDir}`);
  const stat = await fse.stat(absDir);
  if (!stat.isDirectory()) throw new Error(`Expected a directory: ${absDir}`);

  const skillMdPath = path.join(absDir, 'SKILL.md');
  let metadata: ValidationResult['metadata'] = {};
  if (!(await exists(skillMdPath))) {
    issues.push({ severity: 'error', code: 'missing-skill-md', message: 'SKILL.md is required at the skill root.', hint: 'Create /SKILL.md at the skill root before publishing.' });
  } else {
    const skillMd = await readText(skillMdPath);
    if (!skillMd.trim()) {
      issues.push({ severity: 'error', code: 'empty-skill-md', message: 'SKILL.md exists but is blank.', file: 'SKILL.md', hint: 'Add frontmatter and usage content.' });
    } else {
      const parsed = parseFrontmatter(skillMd);
      if (parsed.error) {
        issues.push({ severity: 'error', code: 'bad-frontmatter', message: parsed.error, file: 'SKILL.md', hint: 'Make sure the YAML block opens with --- and closes with --- on its own line.' });
      }
      metadata.frontmatterRaw = parsed.data ?? undefined;
      if (parsed.data) {
        const name = typeof parsed.data.name === 'string' ? parsed.data.name.trim() : undefined;
        const description = typeof parsed.data.description === 'string' ? parsed.data.description.trim() : undefined;
        const tags = Array.isArray(parsed.data.tags) ? parsed.data.tags.filter((x): x is string => typeof x === 'string' && !!x.trim()) : undefined;
        const openclaw = parsed.data.metadata && typeof parsed.data.metadata === 'object'
          ? (parsed.data.metadata as Record<string, unknown>).openclaw
          : undefined;
        const hooks = openclaw && typeof openclaw === 'object'
          ? collectStringPaths((openclaw as Record<string, unknown>).hooks)
          : [];
        metadata = { ...metadata, name, description, tags, hooks };
        if (!name) issues.push({ severity: 'warning', code: 'missing-name', message: 'Frontmatter has no name field.', file: 'SKILL.md', hint: 'Add name: <skill name> for a better ClawHub listing.' });
        if (!description) issues.push({ severity: 'warning', code: 'missing-description', message: 'Frontmatter has no description field.', file: 'SKILL.md', hint: 'Add a one-line description that tells people what the skill does.' });
        if (description && description.length < 24) {
          issues.push({ severity: 'info', code: 'short-description', message: 'Description is very short and may under-sell the skill.', file: 'SKILL.md', hint: 'Consider a clearer one-line value proposition.' });
        }
        if (tags && tags.length === 0) {
          issues.push({ severity: 'info', code: 'empty-tags', message: 'tags exists but is empty.', file: 'SKILL.md', hint: 'Useful tags improve discoverability.' });
        }
      } else {
        issues.push({ severity: 'warning', code: 'missing-frontmatter', message: 'SKILL.md has no YAML frontmatter. Publish will still work, but discovery metadata may be weaker.', file: 'SKILL.md', hint: 'Add name and description frontmatter at minimum.' });
      }
    }
  }

  const files = await walk(absDir);
  const emptyFiles: string[] = [];
  const likelyHookFiles: string[] = [];
  const binaryFiles: string[] = [];
  const docsFiles: string[] = [];

  for (const rel of files) {
    const abs = path.join(absDir, rel);
    if (isBinaryFile(rel)) binaryFiles.push(rel);
    if (/^(README|CHANGELOG|LICENSE)(\.|$)/i.test(path.basename(rel))) docsFiles.push(rel);
    const isHook = isLikelyHookFile(rel);
    if (isHook) likelyHookFiles.push(rel);

    if (!isTextFile(rel)) continue;
    const content = await readText(abs).catch(() => '');
    if (!content.trim()) {
      emptyFiles.push(rel);
      if (isHook) {
        issues.push({ severity: 'warning', code: 'blank-hook-file', message: 'Likely hook file is blank and should be removed or implemented.', file: rel, hint: 'If this hook is intentional, add script contents. Otherwise remove the file and any metadata references.' });
      } else if (rel !== 'SKILL.md') {
        issues.push({ severity: 'info', code: 'blank-file', message: 'Blank file can usually be removed before publish.', file: rel });
      }
    }
  }

  if (files.length === 0) {
    issues.push({ severity: 'error', code: 'empty-skill-folder', message: 'Skill folder contains no publishable files.' });
  }
  if (!files.includes('SKILL.md')) {
    issues.push({ severity: 'error', code: 'missing-skill-md-root', message: 'SKILL.md must live at the root, not a nested folder.', hint: 'Move SKILL.md to the skill root.' });
  }
  if (!files.some(rel => /^README(\.|$)/i.test(path.basename(rel)))) {
    issues.push({ severity: 'info', code: 'missing-readme', message: 'No README file found.', hint: 'A README is optional, but it makes the listing and package more credible.' });
  }
  if (metadata.hooks?.length) {
    for (const hook of metadata.hooks) {
      if (path.isAbsolute(hook)) {
        issues.push({ severity: 'warning', code: 'absolute-hook-path', message: 'Hook path should be relative, not absolute.', file: 'SKILL.md', hint: `Use a relative path like hooks/${path.basename(hook)}.` });
        continue;
      }
      if (!files.includes(hook)) {
        issues.push({ severity: 'error', code: 'missing-hook-target', message: `Frontmatter references hook file that does not exist: ${hook}`, file: 'SKILL.md', hint: 'Create the file or remove the hook reference.' });
      }
    }
  }
  for (const rel of files) {
    if (rel.includes('..')) {
      issues.push({ severity: 'warning', code: 'suspicious-relative-name', message: 'File path contains .. which is unusual for a packaged skill.', file: rel });
    }
    if (/\s{2,}/.test(rel)) {
      issues.push({ severity: 'info', code: 'double-space-path', message: 'File path has repeated spaces.', file: rel, hint: 'Consider renaming for cleaner packaging.' });
    }
  }

  return {
    skillDir: absDir,
    issues,
    stats: {
      fileCount: files.length,
      emptyFiles: emptyFiles.length,
      likelyHookFiles: likelyHookFiles.length,
      binaryFiles: binaryFiles.length,
      docsFiles: docsFiles.length,
    },
    metadata,
  };
}

async function prepareSkill(skillDir: string, options?: { outputRoot?: string; zip?: boolean }) : Promise<PrepareResult> {
  const validation = await validateSkill(skillDir);
  const absDir = validation.skillDir;
  const outputRoot = resolvePath(options?.outputRoot || DEFAULT_OUTPUT_ROOT);
  const slug = inferSlug(absDir, validation.metadata.name);
  const outputDir = path.join(outputRoot, slug);
  await fse.remove(outputDir);
  await fse.ensureDir(outputDir);

  const sourceFiles = await walk(absDir);
  const removedFiles: string[] = [];
  const copiedFiles: string[] = [];

  for (const rel of sourceFiles) {
    const source = path.join(absDir, rel);
    const dest = path.join(outputDir, rel);
    const raw = isTextFile(rel) ? await readText(source).catch(() => '') : '';
    const likelyBlank = isTextFile(rel) && !raw.trim();
    const shouldSkip = likelyBlank && rel !== 'SKILL.md';
    if (shouldSkip) {
      removedFiles.push(rel);
      continue;
    }
    await fse.ensureDir(path.dirname(dest));
    if (isTextFile(rel)) {
      await fse.writeFile(dest, normalizeLines(raw), 'utf8');
    } else {
      await fse.copy(source, dest);
    }
    copiedFiles.push(rel);
  }

  const severityCounts = countBySeverity(validation.issues);
  const report = {
    createdAt: new Date().toISOString(),
    sourceDir: absDir,
    outputDir,
    slug,
    summary: {
      filesCopied: copiedFiles.length,
      filesRemoved: removedFiles.length,
      errors: severityCounts.errors,
      warnings: severityCounts.warnings,
      info: severityCounts.info,
    },
    copiedFiles,
    removedFiles,
    issues: validation.issues,
    stats: validation.stats,
    metadata: validation.metadata,
    recommendations: buildRecommendations(validation),
  };
  const reportPath = path.join(outputDir, 'publish-report.json');
  await fse.writeJson(reportPath, report, { spaces: 2 });

  let zipPath: string | undefined;
  if (options?.zip) {
    zipPath = `${outputDir}.zip`;
    await zipDirectory(outputDir, zipPath);
  }

  return { outputDir, zipPath, copiedFiles, removedFiles, reportPath, validation };
}

function buildRecommendations(validation: ValidationResult) {
  const recommendations: string[] = [];
  const counts = countBySeverity(validation.issues);
  if (counts.errors > 0) recommendations.push('Fix all validation errors before publishing.');
  if (validation.issues.some(issue => issue.code === 'missing-readme')) recommendations.push('Add a README with usage and examples to improve trust and install success.');
  if (validation.issues.some(issue => issue.code === 'missing-description' || issue.code === 'short-description')) recommendations.push('Improve the description so the ClawHub listing explains the value quickly.');
  if (validation.issues.some(issue => issue.code === 'blank-hook-file' || issue.code === 'missing-hook-target')) recommendations.push('Double-check hook metadata and script files before publish.');
  if (recommendations.length === 0) recommendations.push('Package looks healthy. Consider shipping a zip alongside the publish for manual backup/testing.');
  return recommendations;
}

function printPrepareSummary(result: PrepareResult) {
  const counts = countBySeverity(result.validation.issues);
  console.log(chalk.bold.green('Prepared publish-ready skill output'));
  console.log(`Source: ${result.validation.skillDir}`);
  console.log(`Output: ${result.outputDir}`);
  if (result.zipPath) console.log(`Zip: ${result.zipPath}`);
  console.log(`Copied: ${result.copiedFiles.length} file(s)`);
  console.log(`Removed blank files: ${result.removedFiles.length}`);
  if (result.removedFiles.length) {
    console.log(chalk.gray(`Removed: ${result.removedFiles.slice(0, 8).join(', ')}${result.removedFiles.length > 8 ? ' …' : ''}`));
  }
  console.log(`Report: ${result.reportPath}`);
  console.log(`Errors: ${counts.errors}  Warnings: ${counts.warnings}  Info: ${counts.info}`);
  console.log(formatIssues(result.validation.issues));
}

async function zipDirectory(sourceDir: string, outPath: string) {
  await fse.ensureDir(path.dirname(outPath));
  const output = fs.createWriteStream(outPath);
  const archive = archiver('zip', { zlib: { level: 9 } });
  const done = new Promise<void>((resolve, reject) => {
    output.on('close', () => resolve());
    output.on('error', reject);
    archive.on('error', reject);
  });
  archive.pipe(output);
  archive.directory(sourceDir, false);
  archive.finalize();
  await done;
}

async function ensureClawhubAvailable() {
  try {
    await execa('clawhub', ['--help']);
  } catch {
    throw new Error('clawhub CLI is not installed. Install it first with: npm i -g clawhub');
  }
}

async function ask(question: string, defaultValue = '') {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  try {
    const suffix = defaultValue ? ` [${defaultValue}]` : '';
    const answer = (await rl.question(`${question}${suffix}: `)).trim();
    return answer || defaultValue;
  } finally {
    rl.close();
  }
}

async function askConfirm(question: string, defaultYes = true) {
  const fallback = defaultYes ? 'Y/n' : 'y/N';
  const answer = (await ask(`${question} (${fallback})`, '')).toLowerCase();
  if (!answer) return defaultYes;
  return ['y', 'yes'].includes(answer);
}

function requireNonEmpty(value: string, field: string) {
  if (!value.trim()) throw new Error(`${field} is required.`);
  return value.trim();
}

function validateVersion(version: string) {
  if (!SEMVER_RE.test(version)) {
    throw new Error(`Version must be a valid semver value like 0.1.1. Received: ${version}`);
  }
  return version.startsWith('v') ? version.slice(1) : version;
}

async function promptPublishAnswers(skillDir: string, validation: ValidationResult, flags: Record<string, unknown>) {
  const slugDefault = typeof flags.slug === 'string' ? flags.slug : inferSlug(skillDir, validation.metadata.name);
  const nameDefault = typeof flags.name === 'string' ? flags.name : validation.metadata.name || path.basename(skillDir);
  const versionDefault = typeof flags.skillVersion === 'string' ? flags.skillVersion : typeof flags.version === 'string' ? flags.version : '0.1.0';
  const changelogDefault = typeof flags.changelog === 'string' ? flags.changelog : 'Initial publish';
  const tagsDefault = typeof flags.tags === 'string' ? flags.tags : 'latest';
  return {
    slug: requireNonEmpty(await ask('ClawHub slug', slugDefault), 'Slug'),
    name: requireNonEmpty(await ask('Display name', nameDefault), 'Display name'),
    version: validateVersion(await ask('Version', versionDefault)),
    changelog: requireNonEmpty(await ask('Changelog', changelogDefault), 'Changelog'),
    tags: requireNonEmpty(await ask('Tags (comma-separated)', tagsDefault), 'Tags'),
  };
}

async function publishPreparedDirectory(preparedDir: string, publishArgs: { slug: string; name: string; version: string; changelog: string; tags: string; dryRun?: boolean; }) {
  await ensureClawhubAvailable();
  let whoami = 'not logged in';
  try {
    const result = await execa('clawhub', ['whoami']);
    whoami = result.stdout.trim() || whoami;
  } catch {
    whoami = 'not logged in';
  }

  const args = ['publish', preparedDir, '--slug', publishArgs.slug, '--name', publishArgs.name, '--version', publishArgs.version, '--changelog', publishArgs.changelog, '--tags', publishArgs.tags];
  console.log(chalk.cyan(`Using ClawHub identity: ${whoami}`));
  console.log(chalk.gray(`Running: clawhub ${args.map(quoteArg).join(' ')}`));
  if (publishArgs.dryRun) {
    console.log(chalk.yellow('Dry run enabled: publish command was not executed.'));
    return;
  }
  const subprocess = execa('clawhub', args, { stdio: 'inherit' });
  await subprocess;
}

function quoteArg(arg: string) {
  return /\s/.test(arg) ? JSON.stringify(arg) : arg;
}

function summarize(validation: ValidationResult) {
  const counts = countBySeverity(validation.issues);
  return `${validation.stats.fileCount} files, ${counts.errors} errors, ${counts.warnings} warnings, ${counts.info} info`;
}

function buildPublishAnswers(prepared: PrepareResult, opts: Record<string, unknown>) {
  return {
    slug: requireNonEmpty(String(opts.slug || inferSlug(prepared.validation.skillDir, prepared.validation.metadata.name)), 'Slug'),
    name: requireNonEmpty(String(opts.name || prepared.validation.metadata.name || path.basename(prepared.validation.skillDir)), 'Display name'),
    version: validateVersion(String(opts.skillVersion || opts.version || '0.1.0')),
    changelog: requireNonEmpty(String(opts.changelog || ''), 'Changelog'),
    tags: requireNonEmpty(String(opts.tags || 'latest'), 'Tags'),
  };
}

async function confirmPublish(answers: { slug: string; name: string; version: string; changelog: string; tags: string }, opts: Record<string, unknown>) {
  if (opts.yes === true) return;
  console.log(chalk.bold('\nPublish summary'));
  console.log(`Slug: ${answers.slug}`);
  console.log(`Name: ${answers.name}`);
  console.log(`Version: ${answers.version}`);
  console.log(`Changelog: ${answers.changelog}`);
  console.log(`Tags: ${answers.tags}`);
  const confirmed = await askConfirm('Continue and publish this release?', true);
  if (!confirmed) throw new Error('Publish cancelled.');
}

const program = new Command();
program
  .name('clawhub-publisher')
  .description('Validate, clean, package, and publish OpenClaw skills to ClawHub.')
  .version('0.1.1')
  .showHelpAfterError('(run with --help for usage examples)');

program.addHelpText('after', `
Examples:
  $ clawhub-publisher validate ./my-skill
  $ clawhub-publisher prepare ./my-skill --zip
  $ clawhub-publisher publish ./my-skill --no-prompt --slug my-skill --name "My Skill" --skill-version 0.1.1 --changelog "Polished validation and docs" --tags latest
`);

program.command('validate')
  .argument('<skillDir>', 'Path to the skill folder')
  .description('Inspect a skill folder and report packaging issues before publish.')
  .action(async (skillDir) => {
    const result = await validateSkill(skillDir);
    printValidationOverview(result);
  });

program.command('prepare')
  .argument('<skillDir>', 'Path to the skill folder')
  .description('Create a cleaned publish-ready bundle without touching the source folder.')
  .option('-o, --output <dir>', 'Output root directory', DEFAULT_OUTPUT_ROOT)
  .option('--zip', 'Also export a zip package')
  .action(async (skillDir, opts) => {
    const result = await prepareSkill(skillDir, { outputRoot: opts.output, zip: !!opts.zip });
    printPrepareSummary(result);
  });

program.command('publish')
  .argument('<skillDir>', 'Path to the skill folder')
  .description('Prepare and publish a skill to ClawHub with validation and safer prompts.')
  .option('-o, --output <dir>', 'Output root directory', DEFAULT_OUTPUT_ROOT)
  .option('--slug <slug>', 'ClawHub slug')
  .option('--name <name>', 'ClawHub display name')
  .option('--skill-version <version>', 'Semver version for the skill release')
  .option('--changelog <text>', 'Version changelog text')
  .option('--tags <tags>', 'Comma separated tags', 'latest')
  .option('--zip', 'Also export a zip package')
  .option('--dry-run', 'Do everything except execute clawhub publish')
  .option('--no-prompt', 'Disable interactive field prompts and use flags/defaults only')
  .option('-y, --yes', 'Skip final publish confirmation')
  .action(async (skillDir, opts) => {
    const prepared = await prepareSkill(skillDir, { outputRoot: opts.output, zip: !!opts.zip });
    const hasErrors = prepared.validation.issues.some(issue => issue.severity === 'error');
    printPrepareSummary(prepared);
    if (hasErrors) {
      throw new Error('Fix validation errors before publishing.');
    }
    const answers = opts.prompt === false
      ? buildPublishAnswers(prepared, opts as Record<string, unknown>)
      : await promptPublishAnswers(prepared.validation.skillDir, prepared.validation, opts as Record<string, unknown>);

    await confirmPublish(answers, opts as Record<string, unknown>);
    await publishPreparedDirectory(prepared.outputDir, { ...answers, dryRun: !!opts.dryRun });
    if (prepared.zipPath) console.log(chalk.green(`Zip package ready at ${prepared.zipPath}`));
  });

program.command('wizard')
  .description('Interactive guided flow for validate -> prepare -> optional zip -> optional publish')
  .action(async () => {
    const skillDir = await ask('Skill folder path', process.cwd());
    const zip = await askConfirm('Export a zip package too?', true);
    const publish = await askConfirm('Publish to ClawHub after prepare?', false);
    const prepared = await prepareSkill(skillDir, { zip });
    printPrepareSummary(prepared);
    if (prepared.validation.issues.some(issue => issue.severity === 'error')) {
      console.log(chalk.red('Wizard stopped because the skill still has validation errors.'));
      return;
    }
    if (publish) {
      const publishAnswers = await promptPublishAnswers(prepared.validation.skillDir, prepared.validation, {});
      await confirmPublish(publishAnswers, {});
      await publishPreparedDirectory(prepared.outputDir, publishAnswers);
    }
  });

program.parseAsync(process.argv)
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(chalk.red(error instanceof Error ? error.message : String(error)));
    process.exit(1);
  });
