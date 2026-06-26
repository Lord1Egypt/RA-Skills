#!/usr/bin/env node

/**
 * @license
 * Copyright 2026 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Skill Packager - Creates a distributable .skill file of a skill folder
 *
 * Usage:
 *     node package_skill.cjs <path/to/skill-folder> [output-directory]
 */

const path = require('node:path');
const fs = require('node:fs');
const { spawnSync } = require('node:child_process');
const { loadYamlFile } = require('./_spec_common.cjs');
const { validateSkill } = require('./validate_skill.cjs');
const { validatePlatformOutput } = require('./validate_platform_skill.cjs');

function packageSkill(skillPathArg, outputDirArg, options = {}) {
  const skillPath = path.resolve(skillPathArg);
  const outputDir = outputDirArg ? path.resolve(outputDirArg) : process.cwd();
  const skillName = path.basename(skillPath);
  const inferredSpecPath =
    options.specPath ||
    (fs.existsSync(path.join(skillPath, 'spec.yaml'))
      ? path.join(skillPath, 'spec.yaml')
      : null);

  if (!inferredSpecPath) {
    throw new Error(
      'factory-skill-builder/package_skill.cjs requires a rendered skill with spec.yaml. Use a standalone packager outside factory-skill-builder for generic non-factory packaging.',
    );
  }

  const result = validateSkill(skillPath);
  if (!result.valid) {
    throw new Error(`Validation failed: ${result.message}`);
  }

  if (result.warning) {
    throw new Error(`${result.warning}. Please resolve all TODOs before packaging.`);
  }
  const platformValidation = validatePlatformOutput(skillPath, inferredSpecPath);
  if (!platformValidation.valid) {
    throw new Error(`Platform validation failed: ${platformValidation.errors.join('; ')}`);
  }
  const spec = loadYamlFile(inferredSpecPath);
  const nonPublicTargets = (spec?.skill_identity?.target_platforms || []).filter(
    (target) => target.support_level !== 'supported_public',
  );
  if (nonPublicTargets.length > 0) {
    throw new Error(
      `Packaging is only allowed for supported_public targets. Non-public targets: ${nonPublicTargets.map((target) => target.platform).join(', ')}`,
    );
  }

  fs.mkdirSync(outputDir, { recursive: true });

  const outputFilename = path.join(outputDir, `${skillName}.skill`);

  const zipExcludes = [
    '.git/*',
    '*/.git/*',
    '__pycache__/*',
    '*/__pycache__/*',
    '*.pyc',
    '.DS_Store',
    'node_modules/*',
    '*/node_modules/*',
    '.clawhub/*',
    '*/.clawhub/*',
  ];

  let zipProcess = spawnSync('zip', ['-r', outputFilename, '.', '-x', ...zipExcludes], {
    cwd: skillPath,
    stdio: 'inherit',
  });

  if (zipProcess.error || zipProcess.status !== 0) {
    console.log('zip command not found, falling back to tar...');
    zipProcess = spawnSync(
      'tar',
      [
        '--exclude=.git',
        '--exclude=*/.git',
        '--exclude=__pycache__',
        '--exclude=*/__pycache__',
        '--exclude=*.pyc',
        '--exclude=.DS_Store',
        '--exclude=node_modules',
        '--exclude=*/node_modules',
        '--exclude=.clawhub',
        '--exclude=*/.clawhub',
        '-a',
        '-c',
        '--format=zip',
        '-f',
        outputFilename,
        '.',
      ],
      {
        cwd: skillPath,
        stdio: 'inherit',
      },
    );
  }

  if (zipProcess.error) {
    throw zipProcess.error;
  }

  if (zipProcess.status !== 0) {
    throw new Error(`Packaging command failed with exit code ${zipProcess.status}`);
  }

  return outputFilename;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.log(
      'Usage: node package_skill.cjs <path/to/skill-folder> [output-directory]',
    );
    process.exit(1);
  }

  const skillPathArg = args[0];
  const outputDirArg = args[1];

  if (
    skillPathArg.includes('..') ||
    (outputDirArg && outputDirArg.includes('..'))
  ) {
    console.error('❌ Error: Path traversal detected in arguments.');
    process.exit(1);
  }

  try {
    console.log('🔍 Validating skill...');
    const outputFilename = packageSkill(skillPathArg, outputDirArg);
    console.log('✅ Skill is valid!');
    console.log(`✅ Successfully packaged skill to: ${outputFilename}`);
  } catch (err) {
    console.error(`❌ Error packaging: ${err.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { packageSkill };
