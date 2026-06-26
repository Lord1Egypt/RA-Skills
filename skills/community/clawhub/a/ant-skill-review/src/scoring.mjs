/**
 * Deterministic scoring for skill security analysis results.
 *
 * Each finding carries a model-assigned `risk_score` from 0 to 5.
 * Layer score = max `risk_score` across all findings in that layer.
 * overall_risk = worst across layers 1-6 (layer 7 excluded).
 * recommendation = install (safe), caution (medium), do_not_install (high).
 */

function clampRiskScore(score) {
  const n = Number(score);
  if (!Number.isFinite(n)) return 0;
  return Math.max(0, Math.min(5, Math.round(n)));
}

function scoreToRisk(score) {
  if (score <= 0) return "safe";
  if (score <= 4) return "medium";
  return "high";
}

function scoreFindings(findings) {
  if (!findings || findings.length === 0) return 0;
  let maxScore = 0;
  for (const f of findings) {
    maxScore = Math.max(maxScore, clampRiskScore(f.risk_score));
  }
  return maxScore;
}

const LAYER_KEYS = [
  "prompt_injection",
  "malicious_behavior",
  "dynamic_code",
  "obfuscation_binary",
  "dependencies",
  "system_modification",
  "code_quality",
];

const OVERALL_LAYERS = new Set(LAYER_KEYS.slice(0, 6));

export function computeScores(result) {
  if (!result.findings) return;

  result.layer_scores = {};
  let worstOverallScore = 0;

  for (const key of LAYER_KEYS) {
    const findings = result.findings[key];
    if (!findings) continue;

    const score = scoreFindings(findings);
    const risk = scoreToRisk(score);
    result.layer_scores[key] = { score, risk };

    if (OVERALL_LAYERS.has(key)) {
      worstOverallScore = Math.max(worstOverallScore, score);
    }
  }

  result.overall_risk = scoreToRisk(worstOverallScore);

  if (worstOverallScore >= 5) {
    result.recommendation = "do_not_install";
  } else if (worstOverallScore >= 1) {
    result.recommendation = "caution";
  } else {
    result.recommendation = "install";
  }
}
