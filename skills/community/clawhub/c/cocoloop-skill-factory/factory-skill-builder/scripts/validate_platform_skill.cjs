#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

const {
  getDisplayName,
  getSkillSlug,
  getTargetPlatforms,
  loadYamlFile,
} = require('./_spec_common.cjs');
const { collectSpecValidationErrors } = require('./schema_rules.cjs');
const { parseFrontmatter, validateSkill } = require('./validate_skill.cjs');

const SEMVER_RE = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/;

function tryLoadYamlFile(filePath, errors, label) {
  try {
    return loadYamlFile(filePath);
  } catch (error) {
    errors.push(`${label}: ${error.message}`);
    return null;
  }
}

function isPathInside(parentDir, childPath) {
  const relativePath = path.relative(parentDir, childPath);
  return relativePath === '' || (
    !relativePath.startsWith('..') &&
    !path.isAbsolute(relativePath)
  );
}

function getSkillRelativePath(skillDir, relativePath, fieldName) {
  const normalizedPath = String(relativePath || '').trim();
  if (!normalizedPath || path.isAbsolute(normalizedPath)) {
    throw new Error(`Spec ${fieldName} must be a relative path inside the rendered skill.`);
  }
  const resolvedPath = path.resolve(skillDir, normalizedPath);
  const resolvedSkillDir = path.resolve(skillDir);
  if (!isPathInside(resolvedSkillDir, resolvedPath)) {
    throw new Error(`Spec ${fieldName} must stay inside the rendered skill directory.`);
  }
  return resolvedPath;
}

function validateGeneratedByCocoloop(frontmatter, errors) {
  if (frontmatter.generated_by_cocoloop !== true) {
    errors.push(
      'Factory-rendered SKILL.md frontmatter must include generated_by_cocoloop: true.',
    );
  }
}

function validateCodex(skillDir, errors, spec = null) {
  const filePath = path.join(skillDir, 'agents', 'openai.yaml');
  if (!fs.existsSync(filePath)) {
    return;
  }
  const manifest = tryLoadYamlFile(filePath, errors, 'agents/openai.yaml parse failed');
  if (!manifest) return;
  if (!manifest?.interface?.display_name) {
    errors.push('agents/openai.yaml is missing interface.display_name.');
  }
  if (!manifest?.interface?.short_description) {
    errors.push('agents/openai.yaml is missing interface.short_description.');
  }
  if (
    spec &&
    manifest?.interface?.display_name &&
    manifest.interface.display_name !== getDisplayName(spec)
  ) {
    errors.push('agents/openai.yaml interface.display_name must match spec skill_identity.display_name.');
  }
}

function validateClaude(skillDir, errors) {
  const skillMdPath = path.join(skillDir, 'SKILL.md');
  let frontmatter;
  try {
    frontmatter = parseFrontmatter(fs.readFileSync(skillMdPath, 'utf8'));
  } catch (error) {
    errors.push(`Claude Code frontmatter parse failed: ${error.message}`);
    return;
  }
  if (!frontmatter.when_to_use) {
    errors.push('Claude Code target requires when_to_use in SKILL.md frontmatter.');
  }
  if (
    frontmatter['allowed-tools'] !== undefined &&
    !Array.isArray(frontmatter['allowed-tools'])
  ) {
    errors.push('Claude Code frontmatter allowed-tools must be an array when present.');
  }
  if (
    frontmatter['user-invocable'] !== undefined &&
    typeof frontmatter['user-invocable'] !== 'boolean'
  ) {
    errors.push('Claude Code frontmatter user-invocable must be boolean when present.');
  }
}

function validateOpenClaw(skillDir, errors, spec = null) {
  const filePath = path.join(skillDir, 'platform-manifests', 'openclaw-publish.yaml');
  if (!fs.existsSync(filePath)) {
    errors.push('OpenClaw target requires platform-manifests/openclaw-publish.yaml.');
    return;
  }
  const manifest = tryLoadYamlFile(
    filePath,
    errors,
    'OpenClaw publish manifest parse failed',
  );
  if (!manifest) return;
  for (const field of ['slug', 'name', 'version', 'publish_command', 'changelog']) {
    if (!manifest[field]) {
      errors.push(`OpenClaw publish manifest is missing ${field}.`);
    }
  }
  if (manifest.version && !SEMVER_RE.test(String(manifest.version))) {
    errors.push('OpenClaw publish manifest version must be semver.');
  }
  if (!Array.isArray(manifest.tags)) {
    errors.push('OpenClaw publish manifest requires tags array.');
  }
  if (spec && manifest.slug && manifest.slug !== getSkillSlug(spec)) {
    errors.push('OpenClaw publish manifest slug must match spec skill_identity.slug.');
  }
  if (spec && manifest.name && manifest.name !== getDisplayName(spec)) {
    errors.push('OpenClaw publish manifest name must match spec skill_identity.display_name.');
  }
}

function validateHermes(skillDir, errors) {
  const filePath = path.join(skillDir, 'platform-manifests', 'hermes-agent.yaml');
  if (!fs.existsSync(filePath)) {
    errors.push('Hermes target requires platform-manifests/hermes-agent.yaml.');
    return;
  }
  const manifest = tryLoadYamlFile(filePath, errors, 'Hermes manifest parse failed');
  if (!manifest) return;
  for (const field of ['name', 'version', 'author']) {
    if (!manifest[field]) {
      errors.push(`Hermes manifest is missing ${field}.`);
    }
  }
  if (!Array.isArray(manifest.required_environment_variables)) {
    errors.push('Hermes manifest requires required_environment_variables array.');
  }
  if (!Array.isArray(manifest.required_credential_files)) {
    errors.push('Hermes manifest requires required_credential_files array.');
  }
  if (!Array.isArray(manifest.preflight_checks) || manifest.preflight_checks.length === 0) {
    errors.push('Hermes manifest requires preflight_checks array.');
  }
}

function validateCopaw(skillDir, errors) {
  const filePath = path.join(skillDir, 'platform-manifests', 'copaw-authoring.yaml');
  if (!fs.existsSync(filePath)) {
    errors.push('CoPaw target requires platform-manifests/copaw-authoring.yaml.');
    return;
  }
  const manifest = tryLoadYamlFile(filePath, errors, 'CoPaw manifest parse failed');
  if (!manifest) return;
  if (!Array.isArray(manifest.required_files) || !manifest.required_files.includes('SKILL.md')) {
    errors.push('CoPaw manifest must declare SKILL.md in required_files.');
  }
}

function validateMolili(skillDir, errors) {
  const filePath = path.join(skillDir, 'platform-manifests', 'molili-install.yaml');
  if (!fs.existsSync(filePath)) {
    errors.push('Molili target requires platform-manifests/molili-install.yaml.');
    return;
  }
  const manifest = tryLoadYamlFile(filePath, errors, 'Molili manifest parse failed');
  if (!manifest) return;
  for (const field of ['source_root', 'active_root', 'activation_strategy']) {
    if (!manifest[field]) {
      errors.push(`Molili install manifest is missing ${field}.`);
    }
  }
  if (!Array.isArray(manifest.verification_steps) || manifest.verification_steps.length === 0) {
    errors.push('Molili install manifest requires verification_steps.');
  }
}

function validatePlatformOutput(skillDir, specPath = null) {
  const result = validateSkill(skillDir);
  const errors = [];
  const warnings = [];

  if (!result.valid) {
    errors.push(result.message);
  }
  if (result.warning) {
    warnings.push(result.warning);
  }

  let resolvedSpecPath = specPath;
  if (!resolvedSpecPath) {
    const inferredSpecPath = path.join(skillDir, 'spec.yaml');
    if (fs.existsSync(inferredSpecPath)) {
      resolvedSpecPath = inferredSpecPath;
    } else {
      errors.push('Platform validation requires spec.yaml or an explicit --spec path.');
    }
  }

  let spec = null;
  if (resolvedSpecPath) {
    spec = tryLoadYamlFile(resolvedSpecPath, errors, 'Spec parse failed');
    if (spec) {
      errors.push(
        ...collectSpecValidationErrors(spec, {
          label: 'rendering or packaging',
          requirePlatformSupportDetails: true,
        }),
      );
    }
  }

  const skillMdPath = path.join(skillDir, 'SKILL.md');
  if (!fs.existsSync(path.join(skillDir, 'references', 'spec-summary.md'))) {
    errors.push('Rendered skill is missing references/spec-summary.md.');
  }
  if (!fs.existsSync(path.join(skillDir, 'references', 'template-selection.md'))) {
    errors.push('Rendered skill is missing references/template-selection.md.');
  }
  if (!fs.existsSync(path.join(skillDir, 'spec.yaml'))) {
    errors.push('Rendered skill is missing spec.yaml copy.');
  }
  if (!fs.existsSync(skillMdPath)) {
    errors.push('Rendered skill is missing SKILL.md.');
  } else {
    try {
      const frontmatter = parseFrontmatter(fs.readFileSync(skillMdPath, 'utf8'));
      validateGeneratedByCocoloop(frontmatter, errors);
    } catch (error) {
      errors.push(`Rendered SKILL.md frontmatter parse failed: ${error.message}`);
    }
  }

  if (spec) {
    let designEntry = null;
    if (spec?.design_md?.enabled || spec?.output_profile?.has_visual_output === true) {
      try {
        designEntry = getSkillRelativePath(
          skillDir,
          spec?.design_md?.output_path || 'references/design.md',
          'design_md.output_path',
        );
      } catch (error) {
        errors.push(error.message);
      }
    }
    if (spec?.design_md?.enabled) {
      if (designEntry && !fs.existsSync(designEntry)) {
        errors.push(`Rendered skill is missing ${path.relative(skillDir, designEntry)}.`);
      }
      if (!fs.existsSync(path.join(skillDir, 'references', 'design-md', 'index.md'))) {
        errors.push('Rendered skill is missing references/design-md/index.md.');
      }
      if (!fs.existsSync(path.join(skillDir, 'references', 'design-selection.md'))) {
        errors.push('Rendered skill is missing references/design-selection.md.');
      }
    }
    if (spec?.output_profile?.has_visual_output === true) {
      if (designEntry && !fs.existsSync(designEntry)) {
        errors.push(
          `Rendered skill with visual output is missing ${path.relative(skillDir, designEntry)}.`,
        );
      }
      if (!fs.existsSync(path.join(skillDir, 'references', 'design-md', 'index.md'))) {
        errors.push('Rendered skill with visual output is missing references/design-md/index.md.');
      }
    }
    if (spec?.visual_storytelling?.enabled) {
      if (!fs.existsSync(path.join(skillDir, 'references', 'visual-storytelling.md'))) {
        errors.push('Rendered skill is missing references/visual-storytelling.md.');
      }
    }
    for (const target of getTargetPlatforms(spec)) {
      switch (target.platform) {
        case 'codex':
          validateCodex(skillDir, errors, spec);
          break;
        case 'claude_code':
          validateClaude(skillDir, errors);
          break;
        case 'openclaw':
          validateOpenClaw(skillDir, errors, spec);
          break;
        case 'hermes_agent':
          validateHermes(skillDir, errors);
          break;
        case 'copaw':
          validateCopaw(skillDir, errors);
          break;
        case 'molili':
          validateMolili(skillDir, errors);
          break;
        default:
          errors.push(`No platform validator registered for "${target.platform}".`);
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
  };
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error(
      'Usage: node validate_platform_skill.cjs <skill-directory> [--spec <spec.yaml>]',
    );
    process.exit(1);
  }

  const skillDir = path.resolve(args[0]);
  let specPath = null;
  for (let index = 1; index < args.length; index += 1) {
    if (args[index] === '--spec') {
      specPath = path.resolve(args[index + 1]);
      index += 1;
      continue;
    }
    console.error(`Unknown argument: ${args[index]}`);
    process.exit(1);
  }

  if (!specPath) {
    const inferredSpecPath = path.join(skillDir, 'spec.yaml');
    if (!fs.existsSync(inferredSpecPath)) {
      console.error(
        '❌ Platform validation requires spec.yaml. Pass --spec <spec.yaml> or validate a rendered skill directory that already contains spec.yaml.',
      );
      process.exit(1);
    }
    specPath = inferredSpecPath;
  }

  const result = validatePlatformOutput(skillDir, specPath);
  for (const warning of result.warnings) {
    console.warn(`⚠️  ${warning}`);
  }
  if (!result.valid) {
    for (const error of result.errors) {
      console.error(`❌ ${error}`);
    }
    process.exit(1);
  }
  console.log('✅ Platform validation passed.');
}

module.exports = { validatePlatformOutput };
