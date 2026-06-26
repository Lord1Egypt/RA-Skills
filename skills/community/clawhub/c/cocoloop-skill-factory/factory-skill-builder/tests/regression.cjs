#!/usr/bin/env node

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { renderSkillFromSpec } = require('../scripts/render_skill_from_spec.cjs');
const { validatePlatformOutput } = require('../scripts/validate_platform_skill.cjs');

const skillRoot = path.resolve(__dirname, '..', '..');
const outputRoot = path.join(skillRoot, 'output');

function walk(dir, results = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(fullPath, results);
    } else if (entry.isFile() && entry.name === 'spec.yaml') {
      results.push(fullPath);
    }
  }
  return results;
}

function isSourceSpec(specPath) {
  return !fs.existsSync(path.join(path.dirname(specPath), 'SKILL.md'));
}

function runRegression() {
  const specs = walk(outputRoot).filter(isSourceSpec).sort();
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'cocoloop-factory-regression-'));
  const failures = [];

  for (const specPath of specs) {
    const relative = path.relative(skillRoot, specPath);
    try {
      const result = renderSkillFromSpec(specPath, tempDir, { force: true });
      const validation = validatePlatformOutput(result.skillDir, result.renderedSpecPath);
      if (!validation.valid) {
        failures.push(`${relative}\n  ${validation.errors.join('\n  ')}`);
      } else {
        console.log(`ok ${relative}`);
      }
    } catch (error) {
      failures.push(`${relative}\n  ${error.message}`);
    }
  }

  if (failures.length > 0) {
    console.error(`\n${failures.length} regression spec(s) failed:`);
    for (const failure of failures) {
      console.error(`- ${failure}`);
    }
    process.exit(1);
  }

  console.log(`\nRendered and validated ${specs.length} source spec(s).`);
}

runRegression();
