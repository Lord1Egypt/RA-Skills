/**
 * Local validation helpers for factory-rendered skills.
 * Kept inside factory-skill-builder so the spec-driven build chain
 * can run without depending on repository-root scaffold files.
 */

const fs = require('node:fs');
const path = require('node:path');
const yaml = require('yaml');
const TODO_MARKER = ['TODO', ':'].join('');

function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!match) {
    throw new Error('No YAML frontmatter found');
  }
  const frontmatterText = match[1];
  const frontmatter = yaml.parse(frontmatterText);
  if (!frontmatter || typeof frontmatter !== 'object') {
    throw new Error('Invalid YAML frontmatter');
  }
  return frontmatter;
}

function isTextLikeFile(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return !['.png', '.jpg', '.jpeg', '.gif', '.webp', '.pdf', '.zip', '.skill'].includes(ext);
}

function getAllFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  files.forEach((file) => {
    const name = path.join(dir, file);
    if (fs.statSync(name).isDirectory()) {
      if (!['node_modules', '.git', '__pycache__'].includes(file)) {
        getAllFiles(name, fileList);
      }
    } else {
      fileList.push(name);
    }
  });
  return fileList;
}

function validateSkill(skillPath) {
  if (!fs.existsSync(skillPath) || !fs.statSync(skillPath).isDirectory()) {
    return { valid: false, message: `Path is not a directory: ${skillPath}` };
  }

  const skillMdPath = path.join(skillPath, 'SKILL.md');
  if (!fs.existsSync(skillMdPath)) {
    return { valid: false, message: 'SKILL.md not found' };
  }

  const content = fs.readFileSync(skillMdPath, 'utf8');
  let frontmatter;
  try {
    frontmatter = parseFrontmatter(content);
  } catch (error) {
    return { valid: false, message: error.message };
  }

  const name = String(frontmatter.name || '').trim();
  const descriptionValue = frontmatter.description;

  if (!name) return { valid: false, message: 'Missing "name" in frontmatter' };
  if (typeof descriptionValue !== 'string') {
    return {
      valid: false,
      message: 'Description must be a single-line string: description: ...',
    };
  }

  const description = descriptionValue.trim();
  if (!description) {
    return {
      valid: false,
      message: 'Description must be a single-line string: description: ...',
    };
  }

  if (description.includes('\n')) {
    return {
      valid: false,
      message: 'Description must be a single line (no newlines)',
    };
  }

  if (!/^[a-z0-9-]+$/.test(name)) {
    return { valid: false, message: `Name "${name}" should be hyphen-case` };
  }

  if (description.length > 1024) {
    return { valid: false, message: 'Description is too long (max 1024)' };
  }

  const files = getAllFiles(skillPath);
  for (const file of files) {
    if (!isTextLikeFile(file)) {
      continue;
    }
    const fileContent = fs.readFileSync(file, 'utf8');
    if (fileContent.includes(TODO_MARKER)) {
      return {
        valid: true,
        message: 'Skill has unresolved TODOs',
        warning: `Found unresolved TODO in ${path.relative(skillPath, file)}`,
      };
    }
  }

  return { valid: true, message: 'Skill is valid!' };
}

module.exports = { parseFrontmatter, validateSkill };
