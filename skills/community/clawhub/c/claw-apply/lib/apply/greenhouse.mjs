/**
 * greenhouse.mjs — Greenhouse ATS handler
 * Applies directly to greenhouse.io application forms
 * TODO: implement
 */
export const SUPPORTED_TYPES = ['greenhouse'];

export async function apply(page, job, formFiller) {
  return { status: 'skipped_external_unsupported', meta: { title: job.title, company: job.company },
           externalUrl: job.apply_url, ats_platform: 'greenhouse' };
}
