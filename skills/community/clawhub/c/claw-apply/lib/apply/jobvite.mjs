/**
 * jobvite.mjs — Jobvite ATS handler
 * TODO: implement
 */
export const SUPPORTED_TYPES = ['jobvite'];

export async function apply(page, job, formFiller) {
  return { status: 'skipped_external_unsupported', meta: { title: job.title, company: job.company },
           externalUrl: job.apply_url, ats_platform: 'jobvite' };
}
