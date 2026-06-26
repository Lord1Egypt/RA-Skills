/**
 * Logger for CoVe Plugin — platform-agnostic, works with any OpenClaw installation.
 *
 * Logs verification results to stdout in a structured format.
 * OpenClaw captures stdout for session logs automatically.
 */

const PREFIX = '[cove]';

/**
 * Log a verification report.
 * @param {object} report - The verification report from verifyResponse().
 * @param {object} config - Plugin config.
 */
function logResult(report, config) {
  if (!config.log_results_to_dashboard) return;

  const { summary, claims, durationMs } = report;

  console.log(`${PREFIX} Verification complete: ${summary.total} claims found`);
  console.log(`${PREFIX}   verified: ${summary.verified}, inaccurate: ${summary.inaccurate}, unverifiable: ${summary.unverifiable}`);
  console.log(`${PREFIX}   duration: ${durationMs}ms`);

  if (summary.inaccurate > 0) {
    console.log(`${PREFIX}   ⚠️  Inaccuracies detected:`);
    for (const c of claims.filter(c => c.status === 'inaccurate')) {
      console.log(`${PREFIX}     ❌ "${c.claim}"`);
      if (c.correction) console.log(`${PREFIX}        → ${c.correction}`);
    }
  }

  if (report.correctedResponse) {
    console.log(`${PREFIX}   ✏️  Auto-corrected response generated.`);
  }
}

/**
 * Log an inaccuracy event (for individual claim tracking).
 * @param {object} claim - The claim object.
 * @param {object} verdict - The verification verdict.
 */
function logInaccuracy(claim, verdict) {
  console.log(`${PREFIX} Inaccuracy: "${claim.text || claim.claim}"`);
  if (verdict.reason || verdict.evidence) {
    console.log(`${PREFIX}   Reason: ${verdict.reason || verdict.evidence}`);
  }
  if (verdict.correction) {
    console.log(`${PREFIX}   Correction: ${verdict.correction}`);
  }
}

module.exports = { logResult, logInaccuracy };
