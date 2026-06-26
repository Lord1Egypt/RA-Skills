#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

const { toFrontmatter } = require('./_spec_common.cjs');
const { parseFrontmatter } = require('./validate_skill.cjs');

function parseArgs(argv) {
  const args = { mode: 'check' };
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === '--check') {
      args.mode = 'check';
      continue;
    }
    if (token === '--fix') {
      args.mode = 'fix';
      continue;
    }
    if (!args.targetPath) {
      args.targetPath = token;
      continue;
    }
    throw new Error(`Unknown argument: ${token}`);
  }
  if (!args.targetPath) {
    throw new Error(
      'Usage: node ensure_generated_by_cocoloop.cjs <skill-or-directory> [--check|--fix]',
    );
  }
  return args;
}

function collectSkillMdFiles(targetPath) {
  const absolutePath = path.resolve(targetPath);
  if (!fs.existsSync(absolutePath)) {
    throw new Error(`Path does not exist: ${absolutePath}`);
  }
  const stat = fs.statSync(absolutePath);
  if (stat.isFile()) {
    if (path.basename(absolutePath) !== 'SKILL.md') {
      throw new Error(`Expected SKILL.md or a directory, got file: ${absolutePath}`);
    }
    return [absolutePath];
  }

  const skillFiles = [];
  walkForSkillMd(absolutePath, skillFiles);
  return skillFiles;
}

function walkForSkillMd(dirPath, skillFiles) {
  const directSkillMdPath = path.join(dirPath, 'SKILL.md');
  const directSpecPath = path.join(dirPath, 'spec.yaml');
  if (fs.existsSync(directSkillMdPath) && fs.existsSync(directSpecPath)) {
    skillFiles.push(directSkillMdPath);
  }

  for (const entry of fs.readdirSync(dirPath, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name === '.git' || entry.name === '__pycache__') {
      continue;
    }
    const fullPath = path.join(dirPath, entry.name);
    if (entry.isDirectory()) {
      walkForSkillMd(fullPath, skillFiles);
    }
  }
}

function readSkillFrontmatter(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const match = content.match(/^(---\r?\n[\s\S]*?\r?\n---)(\r?\n|$)([\s\S]*)$/);
  if (!match) {
    throw new Error('No YAML frontmatter found');
  }
  return {
    content,
    frontmatter: parseFrontmatter(content),
    body: match[3],
  };
}

function ensureGeneratedByCocoloop(filePath, mode) {
  const { frontmatter, body } = readSkillFrontmatter(filePath);
  if (frontmatter.generated_by_cocoloop === true) {
    return { changed: false, valid: true };
  }
  if (mode === 'check') {
    return { changed: false, valid: false };
  }

  const nextFrontmatter = {
    ...frontmatter,
    generated_by_cocoloop: true,
  };
  fs.writeFileSync(filePath, `${toFrontmatter(nextFrontmatter)}${body}`);
  return { changed: true, valid: true };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const skillFiles = collectSkillMdFiles(args.targetPath);
  if (skillFiles.length === 0) {
    throw new Error(
      `No generated SKILL.md files found under ${path.resolve(args.targetPath)}. Expected directories that contain both SKILL.md and spec.yaml.`,
    );
  }

  const invalidFiles = [];
  let changedCount = 0;

  for (const filePath of skillFiles) {
    const result = ensureGeneratedByCocoloop(filePath, args.mode);
    if (!result.valid) {
      invalidFiles.push(filePath);
      continue;
    }
    if (result.changed) {
      changedCount += 1;
      console.log(`fixed ${filePath}`);
    }
  }

  if (invalidFiles.length > 0) {
    for (const filePath of invalidFiles) {
      console.error(`missing generated_by_cocoloop=true: ${filePath}`);
    }
    process.exit(1);
  }

  if (args.mode === 'fix') {
    console.log(`checked ${skillFiles.length} SKILL.md files, updated ${changedCount}.`);
    return;
  }

  console.log(`checked ${skillFiles.length} SKILL.md files, all passed.`);
}

main();
