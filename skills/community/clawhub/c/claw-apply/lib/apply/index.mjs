/**
 * index.mjs — Apply handler registry
 * Maps apply_type → handler module
 * To add a new ATS: create lib/apply/<name>.mjs and add one line here
 */
import * as easyApply  from './easy_apply.mjs';
import * as greenhouse from './greenhouse.mjs';
import * as lever      from './lever.mjs';
import * as workday    from './workday.mjs';
import * as ashby      from './ashby.mjs';
import * as jobvite    from './jobvite.mjs';
import * as wellfound  from './wellfound.mjs';

const ALL_HANDLERS = [
  easyApply,
  greenhouse,
  lever,
  workday,
  ashby,
  jobvite,
  wellfound,
];

// Build registry: apply_type → handler
const REGISTRY = {};
for (const handler of ALL_HANDLERS) {
  for (const type of handler.SUPPORTED_TYPES) {
    REGISTRY[type] = handler;
  }
}

/**
 * Get handler for a given apply_type
 * Returns null if not supported
 */
export function getHandler(applyType) {
  return REGISTRY[applyType] || null;
}

/**
 * List all supported apply types
 */
export function supportedTypes() {
  return Object.keys(REGISTRY);
}

/**
 * Status normalization — handlers return platform-specific statuses,
 * this map converts them to generic statuses that job_applier.mjs understands.
 *
 * Generic statuses (what handleResult expects):
 *   submitted                   — application was submitted successfully
 *   needs_answer                — blocked on unknown form question, sent to Telegram
 *   skipped_recruiter_only      — LinkedIn recruiter-only listing
 *   skipped_external_unsupported — external ATS not yet implemented
 *   skipped_no_apply            — no apply button/modal/submit found on page
 *   skipped_honeypot            — honeypot question detected, application abandoned
 *   stuck                       — modal progress stalled after retries
 *   incomplete                  — ran out of modal steps without submitting
 *
 * When adding a new handler, return any status you want — if it doesn't match
 * a generic status above, add a mapping here so job_applier doesn't need to change.
 */
const STATUS_MAP = {
  no_button:  'skipped_no_apply',
  no_submit:  'skipped_no_apply',
  no_modal:   'skipped_no_apply',
};

/**
 * Apply to a job using the appropriate handler
 * Returns result object with normalized status
 */
export async function applyToJob(page, job, formFiller) {
  const handler = getHandler(job.apply_type);
  if (!handler) {
    return {
      status: 'skipped_external_unsupported',
      meta: { title: job.title, company: job.company },
      externalUrl: job.apply_url || '',
      ats_platform: job.apply_type || 'unknown',
    };
  }
  const result = await handler.apply(page, job, formFiller);
  return { ...result, status: STATUS_MAP[result.status] || result.status };
}
