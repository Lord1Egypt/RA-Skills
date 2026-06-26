#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

const TEMPLATE_DIR = path.resolve(
  __dirname,
  '..',
  '..',
  'utils',
  'template',
);
const DESIGN_MD_REF_DIR = path.resolve(
  __dirname,
  '..',
  '..',
  'ref',
  'design-md',
);
const PLATFORM_TEMPLATE_FILES = {
  codex: 'codex-skill-template.md',
  claude_code: 'claude-code-skill-template.md',
  openclaw: 'openclaw-skill-template.md',
  hermes_agent: 'hermes-agent-skill-template.md',
  copaw: 'copaw-skill-template.md',
  molili: 'molili-skill-template.md',
};

const {
  ensureArray,
  getDependencyNames,
  getDescription,
  getDisplayName,
  getSkillSlug,
  getTargetPlatformMap,
  getWhenToUse,
  loadYamlFile,
  mkdirp,
  renderMarkdownList,
  toFrontmatter,
  writeYamlFile,
} = require('./_spec_common.cjs');
const { assertRenderableSpec } = require('./schema_rules.cjs');

function parseArgs(argv) {
  const args = { force: false };
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
    if (token === '--force') {
      args.force = true;
      continue;
    }
    throw new Error(`Unknown argument: ${token}`);
  }
  if (!args.specPath || !args.outDir) {
    throw new Error(
      'Usage: node render_skill_from_spec.cjs <spec.yaml> --out <output-dir> [--platform codex,claude_code] [--force]',
    );
  }
  return args;
}

function buildRenderedSpec(spec, selectedPlatforms) {
  const researchContract = getResearchInteractionContract(spec);
  return {
    ...spec,
    interaction_contract: {
      ...(spec.interaction_contract || {}),
      research: researchContract,
    },
    skill_identity: {
      ...(spec.skill_identity || {}),
      target_platforms: selectedPlatforms,
    },
  };
}

function buildSkillBody(spec, selectedPlatforms) {
  const scope = spec.scope || {};
  const researchInteraction = getResearchInteractionContract(spec);
  const maxQuestions = researchInteraction.max_questions;
  const countConfirmationQuestions = researchInteraction.count_confirmation_questions;
  const overflowStrategy = researchInteraction.overflow_strategy;
  const inputs = ensureArray(spec.inputs)
    .map((input) => `- \`${input.name}\`: ${input.description}`)
    .join('\n');
  const outputs = ensureArray(spec.outputs)
    .map((output) => `- \`${output.name}\` (${output.format}): ${output.description}`)
    .join('\n');
  const dependencies = ensureArray(spec.dependencies)
    .map((dependency) => `- \`${dependency.name}\` (${dependency.kind}): ${dependency.note}`)
    .join('\n');
  const designMd = spec?.design_md;
  const visualStorytelling = spec?.visual_storytelling;
  const designSection = designMd?.enabled
    ? [
        '## Design Reference',
        '',
        `- For visual output, follow \`${designMd.output_path || 'references/design.md'}\` before creating high-fidelity work.`,
        '- If the user provides a project-specific `DESIGN.md`, use it as the active visual constraint.',
        '- Use `references/design-md/` only when the user wants to switch to another bundled style reference.',
        '',
      ]
    : [];
  const visualStorytellingSection = visualStorytelling?.enabled
    ? [
        '## Visual Storytelling',
        '',
        '- Use `references/visual-storytelling.md` to plan story units, text hierarchy, visual structures, and adapter-specific output.',
        '- Keep visual work structured before moving into layout or asset production.',
        '',
      ]
    : [];
  const resourceItems = [
    '- `references/spec-summary.md`: confirmed scope, constraints, and delivery contract',
    '- `references/template-selection.md`: selected platform template references',
    designMd?.enabled
      ? `- \`${designMd.output_path || 'references/design.md'}\`: active visual design reference`
      : null,
    designMd?.enabled
      ? '- `references/design-md/`: bundled visual style references'
      : null,
    visualStorytelling?.enabled
      ? '- `references/visual-storytelling.md`: visual storytelling structure'
      : null,
  ].filter(Boolean);

  return [
    `# ${getDisplayName(spec)}`,
    '',
    '## Overview',
    '',
    String(spec.intent.goal || '').trim(),
    '',
    '## Use Cases',
    '',
    renderMarkdownList(spec.intent.use_scenarios),
    '',
    '## Inputs',
    '',
    inputs || '- No explicit inputs declared',
    '',
    '## Outputs',
    '',
    outputs || '- No explicit outputs declared',
    '',
    '## Workflow',
    '',
    '- Confirm the user goal, target environment, and execution plane when they are not already clear.',
    `- The full interaction should normally stay within ${maxQuestions} total questions${countConfirmationQuestions ? ', including confirmation questions.' : '.'}`,
    '- Ask only one key question per turn and use defaults, existing context, environment detection, or confirmations to reduce follow-up questions.',
    `- If open gaps remain near the question limit, apply \`${overflowStrategy}\` instead of extending the interview.`,
    '- Before implementation, check the bundled references and confirm any required external dependency.',
    '',
    ...designSection,
    ...visualStorytellingSection,
    '## Scope',
    '',
    'Required:',
    '',
    renderMarkdownList(scope.must_have) || '- None declared',
    '',
    'Out of scope:',
    '',
    renderMarkdownList(scope.excluded) || '- None declared',
    '',
    '## Platform Scope',
    '',
    selectedPlatforms
      .map(
        (platform) =>
          `- \`${platform.platform}\`${platform.note ? `: ${platform.note}` : ''}`,
      )
      .join('\n'),
    '',
    '## Dependencies',
    '',
    dependencies || '- No dependencies declared',
    '',
    '## Resources',
    '',
    resourceItems.join('\n'),
    '',
    '## Fallback Policy',
    '',
    spec?.fallback_policy?.allowed
      ? `- ${spec?.fallback_policy?.summary || 'Use the documented fallback path when the primary route is unavailable.'}`
      : '- No fallback path declared',
    '',
  ].join('\n');
}

function buildVisualStorytellingSummary(spec) {
  const visualStorytelling = spec.visual_storytelling || {};
  return [
    '# Visual Storytelling Summary',
    '',
    `- artifact_family: \`${visualStorytelling.artifact_family || ''}\``,
    `- output_adapters: ${ensureArray(visualStorytelling.output_adapters)
      .map((item) => `\`${item}\``)
      .join(', ') || 'None declared'}`,
    `- story_units: ${ensureArray(visualStorytelling.story_units)
      .map((item) => `\`${item}\``)
      .join(', ') || 'None declared'}`,
    `- text_hierarchy: ${ensureArray(visualStorytelling?.text_hierarchy?.required_layers)
      .map((item) => `\`${item}\``)
      .join(', ') || 'None declared'}`,
    `- infographic_required: ${visualStorytelling?.infographic_elements?.required ? 'yes' : 'no'}`,
    `- infographic_types: ${ensureArray(visualStorytelling?.infographic_elements?.allowed_types)
      .map((item) => `\`${item}\``)
      .join(', ') || 'None declared'}`,
    '',
  ].join('\n');
}

function getResearchInteractionContract(spec) {
  const researchContract = spec?.interaction_contract?.research || {};
  return {
    ask_one_question_per_turn:
      researchContract.ask_one_question_per_turn !== false,
    max_questions:
      Number.isFinite(researchContract.max_questions) &&
      researchContract.max_questions > 0
        ? researchContract.max_questions
        : 10,
    count_confirmation_questions:
      researchContract.count_confirmation_questions !== false,
    detect_current_environment_first:
      researchContract.detect_current_environment_first !== false,
    confirm_target_environment_before_writing:
      researchContract.confirm_target_environment_before_writing !== false,
    overflow_strategy:
      String(researchContract.overflow_strategy || '').trim() ||
      'write_open_gaps_then_continue',
  };
}

function writeCommonFiles(spec, skillDir, selectedPlatforms) {
  const slug = getSkillSlug(spec);
  const displayName = getDisplayName(spec);
  const outputProfile = spec.output_profile || {};
  const researchInteraction = getResearchInteractionContract(spec);
  const skillIdentityGate = spec?.research_gate?.skill_identity || {};
  const targetEnvironmentGate = spec?.research_gate?.target_environment || {};
  const implementationApproachGate = spec?.research_gate?.implementation_approach || {};
  const maxQuestions = researchInteraction.max_questions;
  const countConfirmationQuestions = researchInteraction.count_confirmation_questions;
  const detectCurrentEnvironmentFirst = researchInteraction.detect_current_environment_first;
  const confirmTargetEnvironmentBeforeWriting =
    researchInteraction.confirm_target_environment_before_writing;
  const overflowStrategy = researchInteraction.overflow_strategy;
  const frontmatter = {
    name: slug,
    description: getDescription(spec),
    version: spec?.skill_identity?.version || '0.1.0',
    author: spec?.skill_identity?.owner || 'unknown',
    generated_by_cocoloop: true,
  };

  if (selectedPlatforms.some((platform) => platform.platform === 'claude_code')) {
    frontmatter.when_to_use = getWhenToUse(spec);
    const allowedTools = getDependencyNames(spec, 'tool');
    if (allowedTools.length > 0) {
      frontmatter['allowed-tools'] = allowedTools;
    }
    frontmatter['user-invocable'] = true;
  }

  fs.writeFileSync(
    path.join(skillDir, 'SKILL.md'),
    `${toFrontmatter(frontmatter)}${buildSkillBody(spec, selectedPlatforms)}`,
  );

  mkdirp(path.join(skillDir, 'references'));
  fs.writeFileSync(
    path.join(skillDir, 'references', 'spec-summary.md'),
    [
      `# ${displayName} Spec Summary`,
      '',
      `- Skill Slug: \`${slug}\``,
      `- Display Name: ${displayName}`,
      `- Skill ID: \`${spec?.skill_identity?.id || slug}\``,
      `- Primary Domain: \`${spec.primary_domain || 'unspecified'}\``,
      `- Version: \`${spec?.skill_identity?.version || '0.1.0'}\``,
      `- Goal: ${spec?.intent?.goal || 'N/A'}`,
      '',
      '## Platforms',
      '',
      selectedPlatforms
        .map(
          (platform) =>
            `- \`${platform.platform}\`: ${platform.support_level} / ${platform.publish_mode || 'n/a'}`,
        )
        .join('\n'),
      '',
      '## Research Gates',
      '',
      `- Skill identity status: \`${skillIdentityGate.status || 'unspecified'}\``,
      `- Cocoloop slug check complete: ${skillIdentityGate.cocoloop_checked === true ? 'yes' : 'no'}`,
      `- ClawHub slug check complete: ${skillIdentityGate.clawhub_checked === true ? 'yes' : 'no'}`,
      `- Slug available: ${skillIdentityGate.slug_available === true ? 'yes' : 'no'}`,
      `- Target environment status: \`${targetEnvironmentGate.status || 'unspecified'}\``,
      `- Current environment: ${targetEnvironmentGate.current_environment || 'Unspecified'}`,
      `- Target environment: ${targetEnvironmentGate.target_environment || 'Unspecified'}`,
      `- Current environment is target: ${
        typeof targetEnvironmentGate.current_environment_is_target === 'boolean'
          ? targetEnvironmentGate.current_environment_is_target
            ? 'yes'
            : 'no'
          : 'unspecified'
      }`,
      `- Implementation approach status: \`${implementationApproachGate.status || 'unspecified'}\``,
      `- Selected execution plane: \`${implementationApproachGate.selected_execution_plane || 'unspecified'}\``,
      '',
      '## Design Input',
      '',
      spec?.design_md?.enabled
        ? `- Enabled: yes / source_mode: \`${spec.design_md.source_mode}\`${spec.design_md.preset_id ? ` / preset: \`${spec.design_md.preset_id}\`` : ''}`
        : '- Enabled: no',
      '',
      '## Output Profile',
      '',
      `- Has visual output: ${outputProfile.has_visual_output ? 'yes' : 'no'}`,
      `- Visual output types: ${ensureArray(outputProfile.visual_output_types)
        .map((item) => `\`${item}\``)
        .join(', ') || 'None declared'}`,
      '',
      '## Interaction Contract',
      '',
      `- Research max questions: \`${maxQuestions}\``,
      `- Count confirmation questions: ${countConfirmationQuestions ? 'yes' : 'no'}`,
      `- Detect current environment first: ${detectCurrentEnvironmentFirst ? 'yes' : 'no'}`,
      `- Confirm target environment before writing: ${confirmTargetEnvironmentBeforeWriting ? 'yes' : 'no'}`,
      `- Overflow strategy: \`${overflowStrategy}\``,
      '',
    ].join('\n'),
  );

  writeYamlFile(path.join(skillDir, 'spec.yaml'), spec);
  if (spec?.visual_storytelling?.enabled) {
    fs.writeFileSync(
      path.join(skillDir, 'references', 'visual-storytelling.md'),
      buildVisualStorytellingSummary(spec),
    );
  }
}

function isPathInside(parentDir, childPath) {
  const relativePath = path.relative(parentDir, childPath);
  return relativePath === '' || (
    !relativePath.startsWith('..') &&
    !path.isAbsolute(relativePath)
  );
}

function getDesignOutputPath(skillDir, designMd) {
  const relativePath = String(designMd?.output_path || 'references/design.md').trim();
  if (!relativePath || path.isAbsolute(relativePath)) {
    throw new Error('Spec design_md.output_path must be a relative path inside the rendered skill.');
  }
  const resolvedPath = path.resolve(skillDir, relativePath);
  const resolvedSkillDir = path.resolve(skillDir);
  if (!isPathInside(resolvedSkillDir, resolvedPath)) {
    throw new Error('Spec design_md.output_path must stay inside the rendered skill directory.');
  }
  return resolvedPath;
}

function getUserProvidedDesignPath(specPath, userProvidedRef) {
  const relativePath = String(userProvidedRef || '').trim();
  if (!relativePath || path.isAbsolute(relativePath)) {
    throw new Error('Spec design_md.user_provided_ref must be a relative path inside the spec directory.');
  }
  const specDir = path.resolve(path.dirname(specPath));
  const resolvedPath = path.resolve(specDir, relativePath);
  if (!fs.existsSync(resolvedPath)) {
    throw new Error(`design_md.user_provided_ref not found: ${resolvedPath}`);
  }
  const realSpecDir = fs.realpathSync(specDir);
  const realInputPath = fs.realpathSync(resolvedPath);
  if (!isPathInside(realSpecDir, realInputPath)) {
    throw new Error('Spec design_md.user_provided_ref must stay inside the spec directory.');
  }
  if (!fs.statSync(realInputPath).isFile()) {
    throw new Error(`design_md.user_provided_ref must point to a file: ${resolvedPath}`);
  }
  return realInputPath;
}

function buildCustomDesignMd(spec) {
  const designMd = spec.design_md || {};
  return [
    '# DESIGN.md',
    '',
    '## Use This First',
    '',
    'Use this document as the default visual constraint before producing any high-fidelity page, infographic, PPT, or showcase graphic.',
    '',
    '## Applies To',
    '',
    renderMarkdownList(ensureArray(designMd.applies_to)) || '- No explicit targets declared',
    '',
    '## Style Notes',
    '',
    renderMarkdownList(ensureArray(designMd.custom_style_notes)) || '- No explicit style notes declared',
    '',
    '## Fallback Rule',
    '',
    '- If the user provides a more specific DESIGN.md, prefer that file over this default brief.',
    '',
  ].join('\n');
}

function writeDesignMdFiles(spec, skillDir, specPath) {
  const designMd = spec?.design_md;
  const hasVisualOutput = spec?.output_profile?.has_visual_output === true;
  if (!designMd?.enabled && !hasVisualOutput) {
    return;
  }
  if (!designMd?.enabled && hasVisualOutput) {
    throw new Error(
      'Spec with output_profile.has_visual_output=true must enable design_md before design assets can be rendered.',
    );
  }

  const outputPath = getDesignOutputPath(skillDir, designMd);
  mkdirp(path.dirname(outputPath));

  const targetLibraryDir = path.join(skillDir, 'references', 'design-md');
  mkdirp(targetLibraryDir);

  const libraryFiles = fs
    .readdirSync(DESIGN_MD_REF_DIR)
    .filter((fileName) => fileName.endsWith('.md'));
  for (const fileName of libraryFiles) {
    fs.copyFileSync(
      path.join(DESIGN_MD_REF_DIR, fileName),
      path.join(targetLibraryDir, fileName),
    );
  }

  if (designMd.source_mode === 'preset') {
    const presetFileName = `${designMd.preset_id}.md`;
    const presetPath = path.join(DESIGN_MD_REF_DIR, presetFileName);
    if (!fs.existsSync(presetPath)) {
      throw new Error(`Unknown design_md preset "${designMd.preset_id}".`);
    }
    fs.copyFileSync(presetPath, outputPath);
  } else if (designMd.source_mode === 'user_provided') {
    const resolvedInputPath = getUserProvidedDesignPath(specPath, designMd.user_provided_ref);
    fs.copyFileSync(resolvedInputPath, outputPath);
  } else if (designMd.source_mode === 'custom_brief') {
    fs.writeFileSync(outputPath, buildCustomDesignMd(spec));
  } else {
    throw new Error(`Unsupported design_md.source_mode "${designMd.source_mode}".`);
  }

  fs.writeFileSync(
    path.join(skillDir, 'references', 'design-selection.md'),
    [
      '# Design Selection',
      '',
      `- source_mode: \`${designMd.source_mode}\``,
      designMd.preset_id ? `- preset_id: \`${designMd.preset_id}\`` : null,
      designMd.user_provided_ref
        ? `- user_provided_ref: \`${designMd.user_provided_ref}\``
        : null,
      `- design_entry: \`${path.relative(skillDir, outputPath) || 'references/design.md'}\``,
      '',
      designMd.prompt_user_to_use_first
        ? '- The generated skill should ask the user to read or replace this DESIGN.md before visual production.'
        : '- The generated skill keeps DESIGN.md as an optional reference.',
      '',
    ]
      .filter(Boolean)
      .join('\n'),
  );
}

function writeTemplateSelectionFiles(skillDir, selectedPlatforms) {
  const templateRefDir = path.join(skillDir, 'references', 'templates');
  mkdirp(templateRefDir);

  const filesToCopy = new Set(['spec-template.yaml']);
  for (const platform of selectedPlatforms) {
    const templateName = PLATFORM_TEMPLATE_FILES[platform.platform];
    if (templateName) filesToCopy.add(templateName);
  }

  for (const fileName of filesToCopy) {
    const sourcePath = path.join(TEMPLATE_DIR, fileName);
    if (!fs.existsSync(sourcePath)) {
      throw new Error(`Required template file is missing: ${sourcePath}`);
    }
    fs.copyFileSync(sourcePath, path.join(templateRefDir, fileName));
  }

  fs.writeFileSync(
    path.join(skillDir, 'references', 'template-selection.md'),
    [
      '# Template Selection',
      '',
      'The generated skill copied these template references from the factory baseline:',
      '',
      ...Array.from(filesToCopy).map((fileName) => `- \`${fileName}\``),
      '',
    ].join('\n'),
  );
}

function writeCodexManifest(spec, skillDir) {
  mkdirp(path.join(skillDir, 'agents'));
  writeYamlFile(path.join(skillDir, 'agents', 'openai.yaml'), {
    interface: {
      display_name: getDisplayName(spec),
      short_description: getDescription(spec),
      default_prompt: `Use $${getSkillSlug(spec)} to help with this task.`,
    },
    policy: {
      allow_implicit_invocation: true,
    },
  });
}

function writeClaudeManifest(spec, skillDir, platformInfo) {
  mkdirp(path.join(skillDir, 'platform-manifests'));
  writeYamlFile(path.join(skillDir, 'platform-manifests', 'claude-code.yaml'), {
    install_paths: [
      `~/.claude/skills/${getSkillSlug(spec)}`,
      `./.claude/skills/${getSkillSlug(spec)}`,
    ],
    support_level: platformInfo.support_level,
    standard_source: platformInfo.standard_source || '',
    validation_mode: platformInfo.validation_mode || '',
  });
}

function writeOpenClawManifest(spec, skillDir, platformInfo) {
  mkdirp(path.join(skillDir, 'platform-manifests'));
  const version = spec?.skill_identity?.version || '0.1.0';
  writeYamlFile(path.join(skillDir, 'platform-manifests', 'openclaw-publish.yaml'), {
    slug: getSkillSlug(spec),
    name: getDisplayName(spec),
    version,
    tags: [spec.primary_domain, ...ensureArray(spec.peer_domains)].filter(Boolean),
    changelog: `Release ${version}`,
    publish_command: `clawhub skill publish ${getSkillSlug(spec)} --slug ${getSkillSlug(spec)} --version ${version} --changelog "Release ${version}"`,
    standard_source: platformInfo.standard_source || '',
  });
}

function writeHermesManifest(spec, skillDir, platformInfo) {
  mkdirp(path.join(skillDir, 'platform-manifests'));
  writeYamlFile(path.join(skillDir, 'platform-manifests', 'hermes-agent.yaml'), {
    name: getDisplayName(spec),
    version: spec?.skill_identity?.version || '0.1.0',
    author: spec?.skill_identity?.owner || 'unknown',
    required_environment_variables: getDependencyNames(spec, 'env'),
    required_credential_files: getDependencyNames(spec, 'credential'),
    publish_target: platformInfo.publish_mode || 'hub_publish',
    standard_source: platformInfo.standard_source || '',
    preflight_checks: [
      'Verify required environment variables are documented before install',
      'Verify required credential files are documented before install',
      'Run security and trust review before hub publish',
    ],
  });
}

function writeCopawManifest(spec, skillDir, platformInfo) {
  mkdirp(path.join(skillDir, 'platform-manifests'));
  writeYamlFile(path.join(skillDir, 'platform-manifests', 'copaw-authoring.yaml'), {
    support_level: platformInfo.support_level,
    required_files: ['SKILL.md'],
    optional_directories: ['scripts', 'references', 'assets'],
    standard_source: platformInfo.standard_source || '',
  });
}

function writeMoliliManifest(spec, skillDir, platformInfo) {
  mkdirp(path.join(skillDir, 'platform-manifests'));
  const adapter = spec?.adapters?.molili || {};
  writeYamlFile(path.join(skillDir, 'platform-manifests', 'molili-install.yaml'), {
    support_level: platformInfo.support_level,
    source_root: adapter.source_root || '~/.cocoloop/skills',
    active_root:
      adapter.active_root || '~/.molili/workspaces/default/active_skills',
    activation_strategy: adapter.activation_strategy || 'symlink_then_copy',
    verification_steps:
      ensureArray(adapter.verification_steps).length > 0
        ? adapter.verification_steps
        : [
            'Verify SKILL.md exists in source directory',
            'Verify activated skill path exists in active_skills',
            'Invoke the skill once and confirm Molili discovers it',
          ],
  });
}

function renderSkillFromSpec(specPath, outDir, options = {}) {
  const spec = loadYamlFile(specPath);
  assertRenderableSpec(spec);
  const platformMap = getTargetPlatformMap(spec);
  const selectedPlatforms = options.platforms?.length
    ? options.platforms.map((platform) => {
        const info = platformMap.get(platform);
        if (!info) {
          throw new Error(`Platform "${platform}" not found in spec target_platforms.`);
        }
        return info;
      })
    : Array.from(platformMap.values());
  const renderedSpec = buildRenderedSpec(spec, selectedPlatforms);

  const skillDir = path.join(path.resolve(outDir), getSkillSlug(spec));
  if (fs.existsSync(skillDir)) {
    if (!options.force) {
      throw new Error(`Output directory already exists: ${skillDir}`);
    }
    fs.rmSync(skillDir, { recursive: true, force: true });
  }

  mkdirp(skillDir);
  writeCommonFiles(renderedSpec, skillDir, selectedPlatforms);
  writeTemplateSelectionFiles(skillDir, selectedPlatforms);
  writeDesignMdFiles(renderedSpec, skillDir, specPath);

  for (const platformInfo of selectedPlatforms) {
    switch (platformInfo.platform) {
      case 'codex':
        writeCodexManifest(renderedSpec, skillDir);
        break;
      case 'claude_code':
        writeClaudeManifest(renderedSpec, skillDir, platformInfo);
        break;
      case 'openclaw':
        writeOpenClawManifest(renderedSpec, skillDir, platformInfo);
        break;
      case 'hermes_agent':
        writeHermesManifest(renderedSpec, skillDir, platformInfo);
        break;
      case 'copaw':
        writeCopawManifest(renderedSpec, skillDir, platformInfo);
        break;
      case 'molili':
        writeMoliliManifest(renderedSpec, skillDir, platformInfo);
        break;
      default:
        throw new Error(`Unsupported render platform "${platformInfo.platform}".`);
    }
  }

  return {
    skillDir,
    skillName: getSkillSlug(spec),
    renderedSpecPath: path.join(skillDir, 'spec.yaml'),
    targetPlatforms: selectedPlatforms,
    platforms: selectedPlatforms.map((item) => item.platform),
  };
}

if (require.main === module) {
  try {
    const args = parseArgs(process.argv.slice(2));
    const result = renderSkillFromSpec(args.specPath, args.outDir, {
      force: args.force,
      platforms: args.platforms
        ? args.platforms.split(',').map((value) => value.trim()).filter(Boolean)
        : null,
    });
    console.log(`✅ Rendered skill at ${result.skillDir}`);
    console.log(`Platforms: ${result.platforms.join(', ')}`);
  } catch (error) {
    console.error(`❌ ${error.message}`);
    process.exit(1);
  }
}

module.exports = { renderSkillFromSpec };
