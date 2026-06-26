const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { loadYamlFile } = require('../scripts/_spec_common.cjs');
const { renderSkillFromSpec } = require('../scripts/render_skill_from_spec.cjs');
const { collectSpecValidationErrors } = require('../scripts/schema_rules.cjs');
const { validatePlatformOutput } = require('../scripts/validate_platform_skill.cjs');

const skillRoot = path.resolve(__dirname, '..', '..');
const validSpecPath = path.join(
  skillRoot,
  'output',
  'preset-system-hardening',
  'spec.yaml',
);

function loadValidSpec() {
  return loadYamlFile(validSpecPath);
}

test('shared schema rules accept a known valid spec', () => {
  const errors = collectSpecValidationErrors(loadValidSpec(), {
    label: 'rendering or packaging',
    requirePlatformSupportDetails: true,
  });
  assert.deepEqual(errors, []);
});

test('shared schema rules reject unavailable slugs', () => {
  const spec = loadValidSpec();
  spec.research_gate.skill_identity.slug_available = false;

  const errors = collectSpecValidationErrors(spec, {
    label: 'rendering',
    requirePlatformSupportDetails: true,
  });

  assert.match(errors.join('\n'), /slug_available must be true/);
});

test('shared schema rules require design_md for visual output', () => {
  const spec = loadValidSpec();
  spec.output_profile.has_visual_output = true;
  spec.output_profile.visual_output_types = ['ppt'];
  spec.design_md = { enabled: false };

  const errors = collectSpecValidationErrors(spec, {
    label: 'rendering',
    requirePlatformSupportDetails: true,
  });

  assert.match(errors.join('\n'), /has_visual_output=true must also enable design_md/);
});

test('render rejects design output paths that escape the skill directory', () => {
  const specPath = path.join(
    skillRoot,
    'output',
    'design-md-hardening',
    'spec.yaml',
  );
  const spec = loadYamlFile(specPath);
  spec.design_md.output_path = '../design.md';

  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'cocoloop-schema-test-'));
  const badSpecPath = path.join(tempDir, 'spec.yaml');
  fs.writeFileSync(badSpecPath, require('yaml').stringify(spec));

  assert.throws(
    () => renderSkillFromSpec(badSpecPath, tempDir, { force: true }),
    /design_md\.output_path must stay inside the rendered skill directory/,
  );
});

test('rendered design skill passes platform validation', () => {
  const specPath = path.join(
    skillRoot,
    'output',
    'design-md-hardening',
    'spec.yaml',
  );
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'cocoloop-render-test-'));
  const result = renderSkillFromSpec(specPath, tempDir, { force: true });
  const validation = validatePlatformOutput(result.skillDir, result.renderedSpecPath);

  assert.deepEqual(validation.errors, []);
  assert.equal(validation.valid, true);
});
