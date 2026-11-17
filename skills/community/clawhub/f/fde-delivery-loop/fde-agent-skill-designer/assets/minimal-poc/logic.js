(function expose(root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.PocLogic = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function build() {
  'use strict';

  const injectionPatterns = [
    /ignore (?:all |any )?(?:previous|prior|system) instructions?/i,
    /(?:directly\s+)?(?:execute|send|write|invoke).{0,20}(?:production|external|system)/i
  ];

  function run(rawInput) {
    const input = String(rawInput || '').trim();
    const base = {
      external_action: false,
      human_review_required: true,
      version: '0.1.0'
    };

    if (!input) {
      return {
        ...base,
        status: 'blocked',
        evidence: 'Missing task input',
        decision: 'No results generated',
        human_action: 'Supplement with desensitizing or synthetic materials',
        output: 'Blocked: Not enough input. The system does not guess at customer facts.'
      };
    }

    if (injectionPatterns.some((pattern) => pattern.test(input))) {
      return {
        ...base,
        status: 'blocked',
        evidence: 'Untrusted instructions or unauthorized requests found',
        decision: 'Maintain established authority boundaries',
        human_action: 'Check input sources and confirm real tasks',
        output: 'Blocked: Input content cannot modify system rules, permissions, or external action boundaries.'
      };
    }

    if (/\[(?:MISSING|OPEN|TO BE CONFIRMED)\]/i.test(input)) {
      return {
        ...base,
        status: 'blocked',
        evidence: 'Key fields are marked as missing',
        decision: 'Pause to form definite conclusions',
        human_action: 'Complete the key fields and rerun',
        output: 'Blocked: A clear gap is detected. Keep existing materials without extrapolating them.'
      };
    }

    const preview = input.length > 220 ? `${input.slice(0, 220)}…` : input;
    return {
      ...base,
      status: 'ready',
      evidence: 'Input exists; business authenticity remains to be evaluated by scenario',
      decision: 'Generate reviewable draft, perform no external actions',
      human_action: 'Check facts, boundaries and acceptance criteria',
      output: `Scenario summary:${preview}\n\nCurrent conclusion: The skeleton has completed input, blocking and manual review of the path. Please replace the domain logic here by PRD and run the real evaluation in ring 6.`
    };
  }

  return { run };
}));
