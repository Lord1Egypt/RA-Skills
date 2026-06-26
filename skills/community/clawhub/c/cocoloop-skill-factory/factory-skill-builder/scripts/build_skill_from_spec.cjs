#!/usr/bin/env node

const path = require('node:path');

const { loadYamlFile } = require('./_spec_common.cjs');
const { renderSkillFromSpec } = require('./render_skill_from_spec.cjs');
const { validatePlatformOutput } = require('./validate_platform_skill.cjs');
const { packageSkill } = require('./package_skill.cjs');

function parseArgs(argv) {
  const args = { force: false, package: false };
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!args.specPath) {
      args.specPath = token;
      continue;
    }
    if (token === '--out') {
      args.outDir = argv[index + 1];
      index += 1;
      continue;
    }
    if (token === '--platform') {
      args.platforms = argv[index + 1];
      index += 1;
      continue;
    }
    if (token === '--package') {
      args.package = true;
      continue;
    }
    if (token === '--force') {
      args.force = true;
      continue;
    }
    throw new Error(`Unknown argument: ${token}`);
  }
  if (!args.specPath || !args.outDir) {
    throw new Error(
      'Usage: node build_skill_from_spec.cjs <spec.yaml> --out <output-dir> [--platform codex,claude_code] [--package] [--force]',
    );
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const renderResult = renderSkillFromSpec(args.specPath, args.outDir, {
    force: args.force,
    platforms: args.platforms
      ? args.platforms.split(',').map((value) => value.trim()).filter(Boolean)
      : null,
  });

  const validation = validatePlatformOutput(
    renderResult.skillDir,
    renderResult.renderedSpecPath,
  );
  if (!validation.valid) {
    for (const error of validation.errors) {
      console.error(`❌ ${error}`);
    }
    process.exit(1);
  }

  console.log(`✅ Rendered and validated ${renderResult.skillName}`);

  if (args.package) {
    const renderedSpec = loadYamlFile(renderResult.renderedSpecPath);
    const nonPublicTargets = (renderedSpec?.skill_identity?.target_platforms || []).filter(
      (target) => target.support_level !== 'supported_public',
    );
    if (nonPublicTargets.length > 0) {
      throw new Error(
        `Packaging is only allowed for supported_public targets. Non-public targets: ${nonPublicTargets.map((target) => target.platform).join(', ')}`,
      );
    }
    const packagedPath = packageSkill(renderResult.skillDir, path.resolve(args.outDir), {
      specPath: renderResult.renderedSpecPath,
    });
    console.log(`📦 Packaged to ${packagedPath}`);
  }
}

main().catch((error) => {
  console.error(`❌ ${error.message}`);
  process.exit(1);
});
