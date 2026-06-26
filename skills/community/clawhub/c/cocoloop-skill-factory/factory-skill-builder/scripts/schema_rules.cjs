/**
 * Shared spec validation rules for rendering, platform validation, and tests.
 */

const {
  SUPPORT_LEVELS,
  getDisplayName,
  getDuplicatePlatforms,
  getTargetPlatforms,
  isKnownPlatform,
  isSupportedLevel,
  isValidSkillSlug,
} = require('./_spec_common.cjs');

const ALLOWED_GATE_STATUSES = new Set(['blocked', 'caution', 'ready']);
const ALLOWED_EXECUTION_PLANES = new Set([
  'Skill-only',
  'Skill + CLI',
  'Skill + API/MCP',
  'Skill + CLI + API/MCP',
]);

function pushRequiredString(errors, value, message) {
  if (!String(value || '').trim()) {
    errors.push(message);
  }
}

function validateTargetPlatforms(spec, errors, options = {}) {
  const targets = getTargetPlatforms(spec);
  const duplicates = getDuplicatePlatforms(spec);
  if (targets.length === 0) {
    errors.push('Spec must declare at least one target platform.');
    return;
  }
  if (duplicates.length > 0) {
    errors.push(`Spec declares duplicate target platforms: ${duplicates.join(', ')}`);
  }

  for (const target of targets) {
    if (!isKnownPlatform(target.platform)) {
      errors.push(`Unknown platform "${target.platform}" in spec target_platforms.`);
      continue;
    }
    if (options.requirePlatformSupportDetails) {
      if (!SUPPORT_LEVELS.includes(target.support_level)) {
        errors.push(
          `Platform "${target.platform}" uses unsupported support_level "${target.support_level}".`,
        );
      }
      if (isSupportedLevel(target.support_level)) {
        if (!target.standard_source) {
          errors.push(`Platform "${target.platform}" is missing standard_source.`);
        }
        if (!target.validation_mode) {
          errors.push(`Platform "${target.platform}" is missing validation_mode.`);
        }
        if (!target.publish_mode) {
          errors.push(`Platform "${target.platform}" is missing publish_mode.`);
        }
      }
    }
  }
}

function validateResearchGate(spec, errors, label) {
  const skillIdentityGate = spec?.research_gate?.skill_identity;
  const targetEnvironmentGate = spec?.research_gate?.target_environment;
  const implementationApproachGate = spec?.research_gate?.implementation_approach;

  if (!skillIdentityGate) {
    errors.push(`Spec must declare research_gate.skill_identity before ${label}.`);
  } else {
    if (!ALLOWED_GATE_STATUSES.has(String(skillIdentityGate.status || '').trim())) {
      errors.push('Spec research_gate.skill_identity.status must be blocked, caution, or ready.');
    } else if (String(skillIdentityGate.status || '').trim() !== 'ready') {
      errors.push(`Spec research_gate.skill_identity.status must be ready before ${label}.`);
    }
    if (typeof skillIdentityGate.cocoloop_checked !== 'boolean') {
      errors.push('Spec research_gate.skill_identity.cocoloop_checked must be boolean.');
    } else if (skillIdentityGate.cocoloop_checked !== true) {
      errors.push(`Spec research_gate.skill_identity.cocoloop_checked must be true before ${label}.`);
    }
    if (typeof skillIdentityGate.clawhub_checked !== 'boolean') {
      errors.push('Spec research_gate.skill_identity.clawhub_checked must be boolean.');
    } else if (skillIdentityGate.clawhub_checked !== true) {
      errors.push(`Spec research_gate.skill_identity.clawhub_checked must be true before ${label}.`);
    }
    if (typeof skillIdentityGate.slug_available !== 'boolean') {
      errors.push('Spec research_gate.skill_identity.slug_available must be boolean.');
    } else if (skillIdentityGate.slug_available !== true) {
      errors.push(`Spec research_gate.skill_identity.slug_available must be true before ${label}.`);
    }
  }

  if (!targetEnvironmentGate) {
    errors.push(`Spec must declare research_gate.target_environment before ${label}.`);
  } else {
    if (!ALLOWED_GATE_STATUSES.has(String(targetEnvironmentGate.status || '').trim())) {
      errors.push('Spec research_gate.target_environment.status must be blocked, caution, or ready.');
    } else if (String(targetEnvironmentGate.status || '').trim() !== 'ready') {
      errors.push(`Spec research_gate.target_environment.status must be ready before ${label}.`);
    }
    pushRequiredString(
      errors,
      targetEnvironmentGate.current_environment,
      `Spec research_gate.target_environment.current_environment is required before ${label}.`,
    );
    pushRequiredString(
      errors,
      targetEnvironmentGate.target_environment,
      `Spec research_gate.target_environment.target_environment is required before ${label}.`,
    );
    if (typeof targetEnvironmentGate.current_environment_is_target !== 'boolean') {
      errors.push('Spec research_gate.target_environment.current_environment_is_target must be boolean.');
    }
  }

  if (!implementationApproachGate) {
    errors.push(`Spec must declare research_gate.implementation_approach before ${label}.`);
  } else {
    if (!ALLOWED_GATE_STATUSES.has(String(implementationApproachGate.status || '').trim())) {
      errors.push('Spec research_gate.implementation_approach.status must be blocked, caution, or ready.');
    } else if (String(implementationApproachGate.status || '').trim() !== 'ready') {
      errors.push(`Spec research_gate.implementation_approach.status must be ready before ${label}.`);
    }
    if (!ALLOWED_EXECUTION_PLANES.has(String(implementationApproachGate.selected_execution_plane || '').trim())) {
      errors.push(
        'Spec research_gate.implementation_approach.selected_execution_plane must be one of Skill-only, Skill + CLI, Skill + API/MCP, or Skill + CLI + API/MCP.',
      );
    }
  }
}

function validateResearchContract(spec, errors) {
  const researchContract = spec?.interaction_contract?.research;
  if (!researchContract) return;

  if (
    researchContract.ask_one_question_per_turn !== undefined &&
    typeof researchContract.ask_one_question_per_turn !== 'boolean'
  ) {
    errors.push('Spec interaction_contract.research.ask_one_question_per_turn must be boolean when present.');
  }
  if (
    researchContract.count_confirmation_questions !== undefined &&
    typeof researchContract.count_confirmation_questions !== 'boolean'
  ) {
    errors.push('Spec interaction_contract.research.count_confirmation_questions must be boolean when present.');
  }
  if (
    researchContract.detect_current_environment_first !== undefined &&
    typeof researchContract.detect_current_environment_first !== 'boolean'
  ) {
    errors.push('Spec interaction_contract.research.detect_current_environment_first must be boolean when present.');
  }
  if (
    researchContract.confirm_target_environment_before_writing !== undefined &&
    typeof researchContract.confirm_target_environment_before_writing !== 'boolean'
  ) {
    errors.push('Spec interaction_contract.research.confirm_target_environment_before_writing must be boolean when present.');
  }
  if (researchContract.max_questions !== undefined) {
    if (!Number.isInteger(researchContract.max_questions) || researchContract.max_questions <= 0) {
      errors.push('Spec interaction_contract.research.max_questions must be a positive integer when present.');
    } else if (researchContract.max_questions > 10) {
      errors.push('Spec interaction_contract.research.max_questions must not exceed 10 for the current factory rules.');
    }
  }
  if (
    researchContract.overflow_strategy !== undefined &&
    !String(researchContract.overflow_strategy || '').trim()
  ) {
    errors.push('Spec interaction_contract.research.overflow_strategy must be a non-empty string when present.');
  }
}

function validateVisualSections(spec, errors) {
  const outputProfile = spec?.output_profile || {};

  if (typeof outputProfile.has_visual_output !== 'boolean') {
    errors.push('Spec output_profile.has_visual_output must be boolean before rendering or packaging.');
  }
  if (!Array.isArray(outputProfile.visual_output_types)) {
    errors.push('Spec output_profile.visual_output_types must be an array before rendering or packaging.');
  }
  if (outputProfile.has_visual_output && !spec?.design_md?.enabled) {
    errors.push('Spec with output_profile.has_visual_output=true must also enable design_md.');
  }

  if (spec?.design_md?.enabled) {
    if (!String(spec.design_md.source_mode || '').trim()) {
      errors.push('Spec must declare design_md.source_mode when design_md.enabled is true.');
    }
    if (!Array.isArray(spec.design_md.applies_to)) {
      errors.push('Spec must declare design_md.applies_to as an array when design_md.enabled is true.');
    }
    if (
      spec.design_md.source_mode === 'preset' &&
      !String(spec.design_md.preset_id || '').trim()
    ) {
      errors.push('Spec must declare design_md.preset_id when design_md.source_mode is preset.');
    }
    if (
      spec.design_md.source_mode === 'user_provided' &&
      !String(spec.design_md.user_provided_ref || '').trim()
    ) {
      errors.push(
        'Spec must declare design_md.user_provided_ref when design_md.source_mode is user_provided.',
      );
    }
  }

  if (spec?.visual_storytelling?.enabled) {
    if (!String(spec.visual_storytelling.artifact_family || '').trim()) {
      errors.push(
        'Spec must declare visual_storytelling.artifact_family when visual_storytelling.enabled is true.',
      );
    }
    if (!Array.isArray(spec.visual_storytelling.story_units) || spec.visual_storytelling.story_units.length === 0) {
      errors.push(
        'Spec must declare visual_storytelling.story_units as a non-empty array when visual_storytelling.enabled is true.',
      );
    }
    if (
      !Array.isArray(spec.visual_storytelling.output_adapters) ||
      spec.visual_storytelling.output_adapters.length === 0
    ) {
      errors.push(
        'Spec must declare visual_storytelling.output_adapters as a non-empty array when visual_storytelling.enabled is true.',
      );
    }
    if (
      !Array.isArray(spec?.visual_storytelling?.text_hierarchy?.required_layers) ||
      spec.visual_storytelling.text_hierarchy.required_layers.length === 0
    ) {
      errors.push(
        'Spec must declare visual_storytelling.text_hierarchy.required_layers as a non-empty array when visual_storytelling.enabled is true.',
      );
    }
    if (
      spec?.visual_storytelling?.infographic_elements?.required &&
      (!Array.isArray(spec.visual_storytelling.infographic_elements.allowed_types) ||
        spec.visual_storytelling.infographic_elements.allowed_types.length === 0)
    ) {
      errors.push(
        'Spec visual_storytelling.infographic_elements.allowed_types must be non-empty when infographic elements are required.',
      );
    }
  }
}

function collectSpecValidationErrors(spec, options = {}) {
  const errors = [];
  const label = options.label || 'rendering or packaging';

  if (!String(spec?.skill_identity?.slug || '').trim()) {
    errors.push(`Spec must declare skill_identity.slug before ${label}.`);
  } else if (!isValidSkillSlug(spec.skill_identity.slug)) {
    errors.push(
      'Spec skill_identity.slug must use lowercase English letters, digits, and hyphen separators only.',
    );
  }
  if (!String(spec?.skill_identity?.display_name || '').trim()) {
    errors.push(`Spec must declare skill_identity.display_name before ${label}.`);
  } else if (getDisplayName(spec).length > 20) {
    errors.push('Spec skill_identity.display_name must not exceed 20 characters.');
  }

  validateTargetPlatforms(spec, errors, options);

  pushRequiredString(errors, spec?.intent?.goal, `Spec intent.goal is required before ${label}.`);
  pushRequiredString(errors, spec?.primary_domain, `Spec primary_domain is required before ${label}.`);
  pushRequiredString(
    errors,
    spec?.research_evidence?.coverage_status?.status,
    `Spec research_evidence.coverage_status.status is required before ${label}.`,
  );

  if (!Array.isArray(spec?.peer_domains)) {
    errors.push(`Spec peer_domains must be an array before ${label}.`);
  }
  if (!Array.isArray(spec?.research_evidence?.open_gaps)) {
    errors.push(`Spec research_evidence.open_gaps must be an array before ${label}.`);
  }

  validateVisualSections(spec, errors);
  validateResearchGate(spec, errors, label);
  validateResearchContract(spec, errors);

  return errors;
}

function assertRenderableSpec(spec) {
  const errors = collectSpecValidationErrors(spec, {
    label: 'rendering',
    requirePlatformSupportDetails: false,
  });
  if (errors.length > 0) {
    throw new Error(errors.join('\n'));
  }
}

module.exports = {
  ALLOWED_EXECUTION_PLANES,
  ALLOWED_GATE_STATUSES,
  assertRenderableSpec,
  collectSpecValidationErrors,
};
