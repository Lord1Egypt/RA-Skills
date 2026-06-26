"use strict";
const U = require("./utils");

const CATEGORY_WEIGHTS = {
  completeness: 0.25,
  accuracy:     0.23,
  consistency:  0.17,
  validity:     0.15,
  uniqueness:   0.15,
  timeliness:   0.05,
};

const CATEGORY_NAMES = {
  completeness: "Completeness",
  accuracy:     "Accuracy",
  consistency:  "Consistency",
  validity:     "Validity",
  uniqueness:   "Uniqueness",
  timeliness:   "Timeliness",
};

// Severity multiplier — makes critical/high issues hit harder in the score.
// Modules already encode severity into deduction values, but this adds a
// scorer-level amplification to ensure severity is consistently reflected.
const SEVERITY_MULT = { critical: 1.5, high: 1.2, medium: 1.0, low: 0.7, info: 0 };

// Category sensitivity scale — compensates for categories with fewer modules
// or more conservative per-module deduction caps. Higher scale = each raw
// deduction point costs more category-score points.
//
// Rationale:
//   completeness  2.5 — well-quantified by modules (nulls can produce large deductions)
//   accuracy      5.0 — few modules, small deductions; each finding is significant
//   consistency   2.0 — many modules, deductions accumulate naturally
//   validity      2.5 — moderate module count, balanced amplification
//   uniqueness    3.0 — few modules, each duplicate finding is impactful
//   timeliness   10.0 — single module, any date anomaly should be noticeable
const CATEGORY_SCALE = {
  completeness: 2.5,
  accuracy:     5.0,
  consistency:  2.0,
  validity:     2.5,
  uniqueness:   3.0,
  timeliness:  10.0,
};

const MAX_CATEGORY_DEDUCTION = 80;

function calculate(issues) {
  const categoryIssues = {};
  for (const cat of Object.keys(CATEGORY_WEIGHTS)) categoryIssues[cat] = [];
  for (const issue of issues) {
    const cat = issue.category;
    if (categoryIssues[cat]) categoryIssues[cat].push(issue);
  }

  const breakdowns = [];
  let weightedScore = 0;

  for (const [cat, weight] of Object.entries(CATEGORY_WEIGHTS)) {
    const catIssues = categoryIssues[cat] || [];

    // Sum deductions with severity multipliers
    let rawDeduction = 0;
    for (const issue of catIssues) {
      const ded = issue.deduction || 0;
      const mult = SEVERITY_MULT[issue.severity] || 1.0;
      rawDeduction += ded * mult;
    }

    // Apply category sensitivity scale and cap
    const scale = CATEGORY_SCALE[cat] || 1.0;
    const scaledDeduction = Math.min(U.round(rawDeduction * scale, 2), MAX_CATEGORY_DEDUCTION);
    const catScore = Math.max(0, U.round(100 - scaledDeduction, 2));

    breakdowns.push({
      category: cat,
      categoryName: CATEGORY_NAMES[cat],
      weight,
      rawDeduction: U.round(rawDeduction, 2),
      scaledDeduction,
      finalScore: catScore,
      issueCount: catIssues.length,
    });

    weightedScore += catScore * weight;
  }

  const totalScore = U.round(weightedScore, 1);
  const [grade, gradeColor] = getGrade(totalScore);

  const severityCounts = { critical: 0, high: 0, medium: 0, low: 0, info: 0 };
  for (const issue of issues) {
    const sev = issue.severity || "medium";
    severityCounts[sev] = (severityCounts[sev] || 0) + 1;
  }

  return {
    totalScore,
    grade,
    gradeColor,
    issueCount: issues.length,
    severityCounts,
    breakdowns,
    summary: generateSummary(totalScore, issues, breakdowns),
  };
}

function getGrade(score) {
  if (score >= 90) return ["Excellent", "green"];
  if (score >= 80) return ["Good", "blue"];
  if (score >= 70) return ["Fair", "yellow"];
  if (score >= 60) return ["Poor", "orange"];
  return ["Very Poor", "red"];
}

function generateSummary(totalScore, issues, breakdowns) {
  let summary;
  if (totalScore >= 90) summary = "Data quality is excellent, safe to use directly.";
  else if (totalScore >= 80) summary = "Data quality is good with minor issues worth noting.";
  else if (totalScore >= 70) summary = "Data quality is fair; recommend addressing issues before use.";
  else if (totalScore >= 60) summary = "Data quality is poor; multiple issues require attention.";
  else summary = "Data quality is very poor; strongly recommend comprehensive cleaning.";

  const worst = breakdowns.reduce((a, b) => a.finalScore < b.finalScore ? a : b);
  if (worst.finalScore < 80) {
    summary += ` Weakest dimension: ${worst.categoryName} (${worst.finalScore}).`;
  }

  const crit = issues.filter(i => i.severity === "critical").length;
  const high = issues.filter(i => i.severity === "high").length;
  if (crit > 0) summary += ` ${crit} critical issue(s) require immediate attention.`;
  if (high > 0) summary += ` ${high} high-priority issue(s) to address.`;

  return summary;
}

module.exports = { calculate };
