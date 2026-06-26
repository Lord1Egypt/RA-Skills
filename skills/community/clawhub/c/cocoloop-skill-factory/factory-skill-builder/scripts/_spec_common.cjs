/**
 * Shared helpers for spec-driven skill rendering and validation.
 */

const fs = require('node:fs');
const path = require('node:path');

let yaml;
try {
  yaml = require('yaml');
} catch (error) {
  throw new Error(
    'Missing "yaml" package in the current Node environment. Install it or use an environment that provides it.',
  );
}

const SUPPORT_LEVELS = [
  'supported_public',
  'supported_authoring_only',
  'supported_local_only',
  'planned',
  'unverified',
];

const VALID_TARGET_PLATFORMS = [
  'codex',
  'claude_code',
  'openclaw',
  'hermes_agent',
  'copaw',
  'molili',
];

function ensureArray(value) {
  return Array.isArray(value) ? value : [];
}

function loadYamlFile(filePath) {
  const absolutePath = path.resolve(filePath);
  const raw = fs.readFileSync(absolutePath, 'utf8');
  const parsed = yaml.parse(raw);
  if (!parsed || typeof parsed !== 'object') {
    throw new Error(`Invalid YAML object in ${absolutePath}`);
  }
  return parsed;
}

function writeYamlFile(filePath, value) {
  fs.writeFileSync(
    filePath,
    yaml.stringify(value, {
      indent: 2,
      lineWidth: 0,
      defaultStringType: 'QUOTE_DOUBLE',
    }),
  );
}

function mkdirp(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function slugify(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/-{2,}/g, '-');
}

function isValidSkillSlug(value) {
  return /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(String(value || '').trim());
}

function titleCase(value) {
  return String(value || '')
    .split(/[-_\s]+/)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

function getSkillSlug(spec) {
  const candidates = [
    spec?.skill_identity?.slug,
    spec?.skill_identity?.id,
    spec?.skill_identity?.name,
    spec?.intent?.goal,
  ];
  for (const candidate of candidates) {
    const slug = slugify(candidate);
    if (slug) return slug;
  }
  throw new Error('Unable to derive skill slug from spec.');
}

function getDisplayName(spec) {
  return (
    spec?.skill_identity?.display_name ||
    spec?.skill_identity?.name ||
    titleCase(spec?.skill_identity?.id || '') ||
    titleCase(getSkillSlug(spec))
  );
}

function getDescription(spec) {
  const goal = String(spec?.intent?.goal || '').trim();
  if (goal) return goal;
  const scenarios = ensureArray(spec?.intent?.use_scenarios).filter(Boolean);
  if (scenarios.length) return `Use when the task matches: ${scenarios[0]}`;
  return `Use ${getDisplayName(spec)} to help with this task.`;
}

function getWhenToUse(spec) {
  const parts = [];
  const goal = String(spec?.intent?.goal || '').trim();
  if (goal) parts.push(goal);
  const scenarios = ensureArray(spec?.intent?.use_scenarios)
    .filter(Boolean)
    .slice(0, 3);
  if (scenarios.length) {
    parts.push(`Typical scenarios: ${scenarios.join('; ')}`);
  }
  return parts.join('. ').trim() || getDescription(spec);
}

function getTargetPlatforms(spec) {
  return ensureArray(spec?.skill_identity?.target_platforms);
}

function getTargetPlatformMap(spec) {
  return new Map(
    getTargetPlatforms(spec)
      .filter((item) => item && item.platform)
      .map((item) => [item.platform, item]),
  );
}

function getDuplicatePlatforms(spec) {
  const counts = new Map();
  for (const target of getTargetPlatforms(spec)) {
    if (!target?.platform) continue;
    counts.set(target.platform, (counts.get(target.platform) || 0) + 1);
  }
  return Array.from(counts.entries())
    .filter(([, count]) => count > 1)
    .map(([platform]) => platform);
}

function isKnownPlatform(platform) {
  return VALID_TARGET_PLATFORMS.includes(platform);
}

function isSupportedLevel(level) {
  return typeof level === 'string' && level.startsWith('supported_');
}

function getDependencyNames(spec, kind) {
  return ensureArray(spec?.dependencies)
    .filter((item) => item && (!kind || item.kind === kind))
    .map((item) => item.name)
    .filter(Boolean);
}

function toFrontmatter(frontmatter) {
  return `---\n${yaml.stringify(frontmatter, {
    indent: 2,
    lineWidth: 0,
    defaultStringType: 'QUOTE_DOUBLE',
  })}---\n`;
}

function renderMarkdownList(items) {
  return ensureArray(items)
    .filter(Boolean)
    .map((item) => `- ${item}`)
    .join('\n');
}

module.exports = {
  SUPPORT_LEVELS,
  VALID_TARGET_PLATFORMS,
  ensureArray,
  getDependencyNames,
  getDescription,
  getDuplicatePlatforms,
  getDisplayName,
  getSkillSlug,
  getTargetPlatformMap,
  getTargetPlatforms,
  getWhenToUse,
  isKnownPlatform,
  isSupportedLevel,
  loadYamlFile,
  mkdirp,
  renderMarkdownList,
  isValidSkillSlug,
  slugify,
  titleCase,
  toFrontmatter,
  writeYamlFile,
  yaml,
};
