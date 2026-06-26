const fs = require("fs");
const path = require("path");
const { VERSION } = require("./version");

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function formatFinding(finding) {
  const extras = [];
  if (finding.context) extras.push(`context=${finding.context}`);
  if (finding.scored === false) extras.push("unscored");
  if (finding.confidence) extras.push(`confidence=${finding.confidence}`);
  const suffix = extras.length ? ` [${extras.join(", ")}]` : "";
  return `${finding.severity.toUpperCase()} ${finding.ruleId} ${finding.file}:${finding.lineNumber || "?"}${suffix}`;
}

function severityExplanation(severity) {
  switch (severity) {
    case "critical":
      return "Critical means the pattern can directly expose credentials or execute remote/untrusted code with little friction.";
    case "high":
      return "High means the pattern can enable code execution, credential exposure, or instruction hijacking if misused.";
    case "medium":
      return "Medium means the pattern adds a risky capability that can be legitimate, but needs review in context.";
    case "low":
      return "Low means the pattern is usually informational or noisy, but can matter when combined with other signals.";
    default:
      return "Severity is based on the likely impact and how directly the pattern enables risky behavior.";
  }
}

function quoteUntrustedEvidence(value) {
  return JSON.stringify(String(value || ""));
}

function renderFindingDetails(lines, finding, options = {}) {
  const indent = options.indent || "";
  const includeLine = options.includeLine !== false;
  lines.push(`${indent}- Why ${String(finding.severity || "unknown").toUpperCase()}: ${finding.rationale || severityExplanation(finding.severity)}`);
  if (finding.review) lines.push(`${indent}- What to check: ${finding.review}`);
  if (finding.confidence) lines.push(`${indent}- Confidence: ${finding.confidence}`);
  if (finding.scored === false) lines.push(`${indent}- Scoring: context only, does not increase risk score`);
  if (includeLine && finding.line) {
    lines.push(`${indent}- Evidence line (quoted, untrusted data): ${quoteUntrustedEvidence(finding.line)}`);
  }
}

function renderDriftList(lines, title, items, limit = 25) {
  lines.push(`${title} (${items.length})`);
  if (items.length === 0) {
    lines.push("- (none)");
    return;
  }
  const visible = items.slice(0, limit);
  for (const item of visible) {
    const value = typeof item === "string" ? item : item.file;
    lines.push(`- ${value}`);
  }
  if (items.length > limit) {
    lines.push(`- ...and ${items.length - limit} more`);
  }
}

function renderFindingList(lines, title, items, limit = 15) {
  lines.push(`${title} (${items.length})`);
  if (items.length === 0) {
    lines.push("- (none)");
    return;
  }
  const visible = items.slice(0, limit);
  for (const finding of visible) {
    lines.push(`- ${formatFinding(finding)}`);
  }
  if (items.length > limit) {
    lines.push(`- ...and ${items.length - limit} more`);
  }
}

function renderSymlinkList(lines, items, limit = 25) {
  lines.push(`Symlinks (${items.length})`);
  if (items.length === 0) {
    lines.push("- (none)");
    return;
  }
  const visible = items.slice(0, limit);
  for (const item of visible) {
    const target = item.target === null || item.target === undefined ? "(unknown)" : item.target;
    const broken =
      item.broken === true ? " [broken]" : item.broken === false ? "" : " [unknown]";
    lines.push(`- ${item.path} -> ${target}${broken}`);
  }
  if (items.length > limit) {
    lines.push(`- ...and ${items.length - limit} more`);
  }
}

function exitCodeForLevel(level) {
  if (level === "low") return 0;
  if (level === "medium") return 1;
  return 2;
}

function buildNextSteps(report) {
  const steps = [];
  const level = report.risk ? report.risk.level : "low";
  const findings = report.stats ? report.stats.findings : 0;
  const comboFindings = report.stats ? report.stats.comboFindings || 0 : 0;
  const drift = report.drift;
  const trustedFindings = report.stats ? report.stats.trustedFindings || 0 : 0;

  if (comboFindings > 0) {
    steps.push("Review combo risks first; they indicate stacked capabilities.");
  }

  if (findings > 0) {
    steps.push("Inspect top findings in the report and confirm or suppress with ignore rules.");
  }

  if (level === "high" || level === "critical") {
    steps.push("Treat as high risk: pause automation and review suspicious files before running.");
  }

  if (drift) {
    const symlinkDrift = drift.symlinks;
    const symlinkCount = symlinkDrift
      ? symlinkDrift.added.length + symlinkDrift.removed.length + symlinkDrift.changed.length
      : 0;
    const driftCount =
      drift.added.length + drift.removed.length + drift.changed.length + symlinkCount;
    if (drift.rootMismatch) {
      steps.push("Baseline was created for a different root; confirm you are comparing the right target.");
    }
    if (drift.configChanged) {
      steps.push("Baseline config differs from the current config; reconcile ignore paths/rules before re-trusting.");
    }
    if (driftCount > 0) {
      steps.push("Review added/removed/changed files to explain the drift.");
      if (level === "high" || level === "critical") {
        steps.push("Do not re-trust until high-risk changes are fully explained.");
      }
      steps.push("Once changes are reviewed, run `driftguard trust <path>` to update the baseline.");
    } else {
      steps.push("No drift detected; the current baseline is still valid.");
    }
    if (trustedFindings > 0 && findings === 0) {
      steps.push("All findings match the trusted baseline; re-trust only if you intentionally changed those files.");
    }
  } else if (report.savedBaseline) {
    steps.push("Trusted baseline saved; use compare after future changes to review drift.");
  } else if (level === "low" && findings === 0) {
    steps.push("Run `driftguard trust <path>` to save a baseline for future comparisons.");
  } else {
    steps.push("Re-scan after fixes to confirm risk reduction.");
  }

  return Array.from(new Set(steps));
}

function buildVerdict(report) {
  const level = report.risk ? report.risk.level : "low";
  const score = report.risk ? report.risk.score : 0;
  const drift = report.drift
    ? {
        baseline: report.drift.baselinePath,
        added: report.drift.added.length,
        removed: report.drift.removed.length,
        changed: report.drift.changed.length,
        unchanged: report.drift.unchangedCount,
        symlinks: report.drift.symlinks
          ? {
              added: report.drift.symlinks.added.length,
              removed: report.drift.symlinks.removed.length,
              changed: report.drift.symlinks.changed.length,
              unchanged: report.drift.symlinks.unchangedCount
            }
          : null
      }
    : null;
  const riskDiff = report.drift && report.drift.riskDiff ? report.drift.riskDiff : null;
  const symlinkDrift = report.drift ? report.drift.symlinks : null;
  const driftCount = report.drift
    ? report.drift.added.length +
      report.drift.removed.length +
      report.drift.changed.length +
      (symlinkDrift
        ? symlinkDrift.added.length + symlinkDrift.removed.length + symlinkDrift.changed.length
        : 0)
    : 0;
  const effectiveLevel = driftCount > 0 && level === "low" ? "medium" : level;
  const status =
    effectiveLevel === "low"
      ? "pass"
      : effectiveLevel === "medium"
        ? "warn"
        : "fail";

  return {
    status,
    level: effectiveLevel,
    score,
    exitCode: exitCodeForLevel(effectiveLevel),
    mode: report.drift ? "compare" : "scan",
    findings: report.stats ? report.stats.findings : 0,
    comboRisks: report.stats ? report.stats.comboFindings || 0 : 0,
    drift,
    riskDiff,
    nextSteps: buildNextSteps(report)
  };
}

function attachVerdict(report) {
  report.trust = buildTrustSummary(report);
  report.verdict = buildVerdict(report);
  return report;
}

function buildTrustSummary(report) {
  if (!report || !report.drift) return null;
  const highlights = report.drift.highlights || {};
  const reasons = [];
  const notes = [];
  const baselineVersion = report.drift.baselineVersion || null;
  const currentVersion = report.version || null;
  const versionMismatch =
    baselineVersion && currentVersion && baselineVersion !== currentVersion;

  if (report.drift.rootMismatch) reasons.push("Baseline root mismatch.");
  if (report.drift.configChanged) reasons.push("Baseline config changed.");
  if (versionMismatch) reasons.push("Baseline version mismatch.");
  if (highlights.newCapabilities && highlights.newCapabilities.length) {
    reasons.push(...highlights.newCapabilities);
  }
  if (highlights.dependencyChanges && highlights.dependencyChanges.length) {
    reasons.push("Dependency changes detected.");
  }
  if (
    highlights.installHooks &&
    (highlights.installHooks.added.length || highlights.installHooks.removed.length)
  ) {
    reasons.push("Install hooks changed.");
  }
  if (highlights.notes && highlights.notes.length) {
    notes.push(...highlights.notes);
  }

  const symlinkDrift = report.drift.symlinks;
  const driftCount =
    report.drift.added.length +
    report.drift.removed.length +
    report.drift.changed.length +
    (symlinkDrift
      ? symlinkDrift.added.length + symlinkDrift.removed.length + symlinkDrift.changed.length
      : 0);

  let recommendation = "review";
  if (report.drift.rootMismatch || report.drift.configChanged) {
    recommendation = "do-not-trust";
  } else if (driftCount === 0) {
    recommendation = "safe-to-trust";
  } else if (
    (highlights.newCapabilities && highlights.newCapabilities.length) ||
    (highlights.installHooks && highlights.installHooks.added.length)
  ) {
    recommendation = "do-not-trust";
  }

  if (report.drift.trustMode === "all-findings" && recommendation === "safe-to-trust") {
    recommendation = "review";
  }

  const label =
    recommendation === "safe-to-trust"
      ? "SAFE TO TRUST"
      : recommendation === "do-not-trust"
        ? "DO NOT TRUST"
        : "REVIEW";

  const summary =
    recommendation === "safe-to-trust"
      ? "No new drift detected; baseline remains trusted."
      : recommendation === "do-not-trust"
        ? "High-risk drift detected; do not refresh the baseline yet."
        : "Drift detected; review changes before trusting.";

  return {
    recommendation,
    label,
    summary,
    reasons: Array.from(new Set(reasons)),
    notes: Array.from(new Set(notes))
  };
}

function renderMarkdown(report) {
  if (!report.verdict) attachVerdict(report);
  const lines = [];
  lines.push(`# DriftGuard Security Scanner+ Integrity Report`);
  lines.push("");
  lines.push(`- Version: ${report.version || VERSION}`);
  lines.push(`- Root: ${report.rootPath}`);
  if (report.savedBaseline) {
    lines.push(`- Saved baseline: ${report.savedBaseline.path}`);
  }
  lines.push(`- Overall Risk: ${report.risk.level.toUpperCase()} (score ${report.risk.score})`);
  lines.push(`- Findings: ${report.stats.findings}`);
  lines.push(`- Combo Risks: ${report.stats.comboFindings || 0}`);
  if (report.trust && report.verdict.mode === "compare") {
    lines.push(`- Trust Recommendation: ${report.trust.label}`);
  }
  lines.push("");

  if (report.trust && report.verdict.mode === "compare") {
    lines.push("## Trust Summary");
    lines.push("");
    lines.push(`- Recommendation: ${report.trust.label}`);
    lines.push(`- Summary: ${report.trust.summary}`);
    if (report.trust.reasons.length) {
      lines.push(`- Reasons: ${report.trust.reasons.join("; ")}`);
    }
    if (report.trust.notes.length) {
      lines.push(`- Notes: ${report.trust.notes.join("; ")}`);
    }
    lines.push("");
  }

  lines.push("## Verdict");
  lines.push("");
  lines.push(`- Status: ${report.verdict.status.toUpperCase()}`);
  lines.push(`- Mode: ${report.verdict.mode}`);
  lines.push(`- Exit code: ${report.verdict.exitCode}`);
  lines.push("");
  lines.push("```json");
  lines.push(JSON.stringify(report.verdict, null, 2));
  lines.push("```");
  lines.push("");

  if (report.config) {
    lines.push("## Config");
    lines.push("");
    lines.push(`- Config path: ${report.config.path || "(none)"}`);
    lines.push(`- Ignored paths: ${(report.config.ignorePaths || []).length}`);
    lines.push(`- Ignored rules: ${(report.config.ignoreRules || []).length}`);
    lines.push("");
  }

  lines.push("## Summary");
  lines.push("");
  lines.push(`- Total files: ${report.stats.totalFiles}`);
  lines.push(`- Scanned files: ${report.stats.scannedFiles}`);
  lines.push(`- Skipped files: ${report.stats.skippedFiles}`);
  lines.push(`- Ignored files: ${report.stats.ignoredFiles || 0}`);
  if (report.stats.symlinks !== undefined) {
    lines.push(`- Symlinks: ${report.stats.symlinks}`);
  }
  if (report.stats.totalFindings !== undefined) {
    lines.push(`- Total findings: ${report.stats.totalFindings}`);
  }
  if (report.stats.unscoredFindings !== undefined) {
    lines.push(`- Unscored findings: ${report.stats.unscoredFindings}`);
  }
  if (report.stats.trustedFindings !== undefined) {
    lines.push(`- Trusted findings: ${report.stats.trustedFindings}`);
  }
  lines.push("");

  if (report.symlinks) {
    lines.push("## Symlinks");
    lines.push("");
    renderSymlinkList(lines, report.symlinks);
    lines.push("");
  }

  if (report.drift) {
    lines.push("## What Changed Since Trust");
    lines.push("");
    lines.push(`- Baseline: ${report.drift.baselinePath}`);
    if (report.drift.baselineRoot !== undefined) {
      lines.push(`- Baseline root: ${report.drift.baselineRoot || "(unknown)"}`);
    }
    if (report.drift.currentRoot !== undefined) {
      lines.push(`- Current root: ${report.drift.currentRoot || "(unknown)"}`);
    }
    if (report.drift.baselineVersion !== undefined) {
      lines.push(`- Baseline version: ${report.drift.baselineVersion || "(unknown)"}`);
    }
    if (report.drift.trust) {
      const trust = report.drift.trust;
      lines.push(`- Trusted at: ${trust.approvedAt || "(unknown)"}`);
      lines.push(`- Trusted by: ${trust.approvedBy || "(unknown)"}`);
      if (trust.gitCommit) lines.push(`- Trusted git commit: ${trust.gitCommit}`);
      if (trust.packageVersion) lines.push(`- Trusted package version: ${trust.packageVersion}`);
      if (trust.note) lines.push(`- Trust note: ${trust.note}`);
    }
    if (report.drift.configChanged !== undefined) {
      lines.push(`- Config changed: ${report.drift.configChanged ? "yes" : "no"}`);
    }
    lines.push(`- Added files: ${report.drift.added.length}`);
    lines.push(`- Removed files: ${report.drift.removed.length}`);
    lines.push(`- Changed files: ${report.drift.changed.length}`);
    lines.push(`- Unchanged files: ${report.drift.unchangedCount}`);
    if (report.drift.symlinks) {
      lines.push(`- Symlink adds: ${report.drift.symlinks.added.length}`);
      lines.push(`- Symlink removes: ${report.drift.symlinks.removed.length}`);
      lines.push(`- Symlink changes: ${report.drift.symlinks.changed.length}`);
    }
    if (report.drift.highlights) {
      const highlights = report.drift.highlights;
      if (highlights.newCapabilities && highlights.newCapabilities.length) {
        lines.push(`- New capability signals: ${highlights.newCapabilities.join("; ")}`);
      }
      if (highlights.dependencyChanges && highlights.dependencyChanges.length) {
        lines.push(`- Dependency changes: ${highlights.dependencyChanges.join("; ")}`);
      }
      if (highlights.installHooks) {
        if (highlights.installHooks.added.length) {
          lines.push(
            `- New install hooks: ${highlights.installHooks.added.join(", ")}`
          );
        }
        if (highlights.installHooks.removed.length) {
          lines.push(
            `- Removed install hooks: ${highlights.installHooks.removed.join(", ")}`
          );
        }
      }
    }
    if (report.drift.riskDiff) {
      const diff = report.drift.riskDiff;
      lines.push(`- Baseline risk: ${(diff.baseline.level || "unknown").toUpperCase()} (score ${diff.baseline.score === null ? "unknown" : diff.baseline.score})`);
      lines.push(`- Current full-scan risk: ${(diff.current.level || "unknown").toUpperCase()} (score ${diff.current.score === null ? "unknown" : diff.current.score})`);
      if (diff.scoreDelta !== null) lines.push(`- Risk score delta: ${diff.scoreDelta}`);
      if (diff.findingDelta !== null) lines.push(`- Finding delta: ${diff.findingDelta}`);
      if (diff.capabilities.added.length) {
        lines.push(`- New risk capabilities: ${diff.capabilities.added.join(", ")}`);
      }
      if (diff.capabilities.removed.length) {
        lines.push(`- Removed risk capabilities: ${diff.capabilities.removed.join(", ")}`);
      }
    }
    lines.push("");
    renderDriftList(lines, "Added files", report.drift.added);
    lines.push("");
    renderDriftList(lines, "Removed files", report.drift.removed);
    lines.push("");
    renderDriftList(lines, "Changed files", report.drift.changed);
    lines.push("");
    if (report.drift.symlinks) {
      renderDriftList(lines, "Symlink adds", report.drift.symlinks.added);
      lines.push("");
      renderDriftList(lines, "Symlink removes", report.drift.symlinks.removed);
      lines.push("");
      renderDriftList(lines, "Symlink changes", report.drift.symlinks.changed);
      lines.push("");
    }
  }

  if (report.comboRisks && report.comboRisks.length) {
    lines.push("## Combo Risks");
    lines.push("");
    for (const combo of report.comboRisks) {
      lines.push(`- ${combo.severity.toUpperCase()} ${combo.id}: ${combo.description}`);
      if (combo.evidence && combo.evidence.length) {
        lines.push(`Evidence: ${combo.evidence.join(", ")}`);
      }
      lines.push("");
    }
  }

  lines.push("## Findings");
  lines.push("");
  if (
    report.stats &&
    report.stats.unscoredFindings > 0 &&
    report.stats.findings === 0
  ) {
    lines.push("Note: unscored findings are shown for context only.");
    lines.push("");
  }
  if (report.findings.length === 0) {
    if (report.stats.trustedFindings) {
      lines.push("No new findings since the baseline.");
      lines.push(`Trusted findings: ${report.stats.trustedFindings}.`);
    } else {
      lines.push("No findings.");
    }
  } else {
    for (const finding of report.findings) {
      lines.push(`- ${formatFinding(finding)}`);
      if (finding.line) {
        lines.push(`Description: ${finding.description}`);
        lines.push(`Line: ${finding.line}`);
      }
      renderFindingDetails(lines, finding);
      lines.push("");
    }
  }

  if (report.trustedFindings && report.trustedFindings.length) {
    lines.push("");
    lines.push("## Trusted Findings");
    lines.push("");
    renderFindingList(lines, "Trusted findings", report.trustedFindings, 20);
    lines.push("");
  }

  if (report.verdict && report.verdict.nextSteps.length) {
    lines.push("");
    lines.push("## Next Steps");
    lines.push("");
    for (const step of report.verdict.nextSteps) {
      lines.push(`- ${step}`);
    }
  }

  lines.push("");
  lines.push("## Manifests");
  lines.push("");
  if (Object.keys(report.manifests).length === 0) {
    lines.push("No manifests detected.");
  } else {
    lines.push("```json");
    lines.push(JSON.stringify(report.manifests, null, 2));
    lines.push("```");
  }

  lines.push("");
  lines.push("## File Hashes");
  lines.push("");
  lines.push("```json");
  lines.push(JSON.stringify(report.hashes, null, 2));
  lines.push("```");

  return lines.join("\n");
}

function renderJson(report) {
  return JSON.stringify(report, null, 2);
}

function renderReviewTicket(report) {
  if (!report.verdict) attachVerdict(report);
  const lines = [];
  const hasDrift = Boolean(report.drift);
  const trust = report.trust || null;

  lines.push(`# DriftGuard Security Scanner+ Review Ticket`);
  lines.push("");
  lines.push(`Generated: ${new Date().toISOString()}`);
  lines.push(`Target: ${report.rootPath}`);
  lines.push(`Mode: ${report.verdict.mode}`);
  lines.push(`Verdict: ${report.verdict.status.toUpperCase()} (${report.verdict.level.toUpperCase()}, score ${report.verdict.score})`);
  if (trust) {
    lines.push(`Trust recommendation: ${trust.label}`);
    lines.push(`Summary: ${trust.summary}`);
  }
  lines.push("");

  lines.push(`## Reviewer decision`);
  lines.push("");
  lines.push(`- [ ] Approved, update baseline`);
  lines.push(`- [ ] Rejected, changes need remediation`);
  lines.push(`- [ ] Needs deeper manual review`);
  lines.push("");
  lines.push(`Reviewer:`);
  lines.push(`Date:`);
  lines.push(`Notes:`);
  lines.push("");

  lines.push(`## Required checks`);
  lines.push("");
  const requiredChecks = [];
  if (hasDrift && report.drift.rootMismatch) requiredChecks.push(`Confirm this baseline belongs to the scanned target.`);
  if (hasDrift && report.drift.configChanged) requiredChecks.push(`Review config changes before trusting.`);
  if (hasDrift && report.drift.highlights) {
    const h = report.drift.highlights;
    if (h.newCapabilities && h.newCapabilities.length) requiredChecks.push(`Review new capability signals.`);
    if (h.dependencyChanges && h.dependencyChanges.length) requiredChecks.push(`Review dependency changes.`);
    if (h.installHooks && h.installHooks.added.length) requiredChecks.push(`Review new install hooks.`);
  }
  if (report.stats.findings > 0) requiredChecks.push(`Review all new scored findings.`);
  if (!requiredChecks.length) requiredChecks.push(`No mandatory blockers detected. Confirm intended change set before trusting.`);
  for (const check of requiredChecks) lines.push(`- [ ] ${check}`);
  lines.push("");

  if (trust) {
    lines.push(`## Trust recommendation`);
    lines.push("");
    lines.push(`- Recommendation: ${trust.label}`);
    if (trust.reasons && trust.reasons.length) {
      lines.push(`- Reasons:`);
      for (const reason of trust.reasons) lines.push(`  - ${reason}`);
    }
    if (trust.notes && trust.notes.length) {
      lines.push(`- Notes:`);
      for (const note of trust.notes) lines.push(`  - ${note}`);
    }
    lines.push("");
  }

  lines.push(`## Risk summary`);
  lines.push("");
  lines.push(`- Overall risk: ${report.risk.level.toUpperCase()} (score ${report.risk.score})`);
  lines.push(`- Findings: ${report.stats.findings}`);
  lines.push(`- Combo risks: ${report.stats.comboFindings || 0}`);
  if (report.stats.trustedFindings !== undefined) {
    lines.push(`- Trusted unchanged findings: ${report.stats.trustedFindings}`);
  }
  lines.push("");

  if (hasDrift) {
    lines.push(`## Change summary since trust`);
    lines.push("");
    lines.push(`- Baseline: ${report.drift.baselinePath}`);
    lines.push(`- Files added: ${report.drift.added.length}`);
    lines.push(`- Files removed: ${report.drift.removed.length}`);
    lines.push(`- Files changed: ${report.drift.changed.length}`);
    lines.push(`- Files unchanged: ${report.drift.unchangedCount}`);
    if (report.drift.symlinks) {
      lines.push(`- Symlinks added: ${report.drift.symlinks.added.length}`);
      lines.push(`- Symlinks removed: ${report.drift.symlinks.removed.length}`);
      lines.push(`- Symlinks changed: ${report.drift.symlinks.changed.length}`);
    }
    if (report.drift.riskDiff) {
      const diff = report.drift.riskDiff;
      lines.push(`- Baseline risk: ${(diff.baseline.level || "unknown").toUpperCase()} (score ${diff.baseline.score === null ? "unknown" : diff.baseline.score})`);
      lines.push(`- Current full-scan risk: ${(diff.current.level || "unknown").toUpperCase()} (score ${diff.current.score === null ? "unknown" : diff.current.score})`);
      if (diff.scoreDelta !== null) lines.push(`- Score delta: ${diff.scoreDelta}`);
      if (diff.capabilities.added.length) lines.push(`- New capabilities: ${diff.capabilities.added.join(", ")}`);
    }
    lines.push("");
  }

  const scoredFindings = report.findings.filter((finding) => finding.scored !== false);
  const contextFindings = report.findings.filter((finding) => finding.scored === false);

  if (scoredFindings.length) {
    lines.push(`## New findings to review`);
    lines.push("");
    for (const finding of scoredFindings.slice(0, 30)) {
      lines.push(`- [ ] ${formatFinding(finding)}`);
      if (finding.description) lines.push(`  - ${finding.description}`);
      renderFindingDetails(lines, finding, { indent: "  ", includeLine: false });
    }
    if (scoredFindings.length > 30) lines.push(`- ...and ${scoredFindings.length - 30} more scored findings in the full report`);
    lines.push("");
  }

  if (contextFindings.length) {
    lines.push(`## Context signals, not scored`);
    lines.push("");
    lines.push(`These are shown for reviewer awareness only. They do not increase the risk score.`);
    lines.push("");
    for (const finding of contextFindings.slice(0, 20)) {
      lines.push(`- ${formatFinding(finding)}`);
      if (finding.description) lines.push(`  - ${finding.description}`);
      renderFindingDetails(lines, finding, { indent: "  ", includeLine: false });
    }
    if (contextFindings.length > 20) lines.push(`- ...and ${contextFindings.length - 20} more context signals in the full report`);
    lines.push("");
  }

  if (report.verdict.nextSteps && report.verdict.nextSteps.length) {
    lines.push(`## Suggested next steps`);
    lines.push("");
    for (const step of report.verdict.nextSteps) lines.push(`- ${step}`);
    lines.push("");
  }

  lines.push(`## Copy-paste approval note`);
  lines.push("");
  lines.push("```");
  lines.push(`Reviewed with DriftGuard Security Scanner+.`);
  lines.push(`Verdict: ${report.verdict.status.toUpperCase()} (${report.verdict.level.toUpperCase()}, score ${report.verdict.score}).`);
  if (trust) lines.push(`Trust recommendation: ${trust.label}.`);
  if (hasDrift) lines.push(`Drift: +${report.drift.added.length} files, -${report.drift.removed.length} files, ~${report.drift.changed.length} files.`);
  lines.push(`Decision: <approved/rejected/needs-review>.`);
  lines.push("```");

  return lines.join("\n");
}

function writeReports(report, outDir, jsonFile, mdFile) {
  if (!report.verdict) attachVerdict(report);
  ensureDir(outDir);
  const jsonPath = jsonFile || path.join(outDir, "report.json");
  const mdPath = mdFile || path.join(outDir, "report.md");
  ensureDir(path.dirname(jsonPath));
  ensureDir(path.dirname(mdPath));
  fs.writeFileSync(jsonPath, renderJson(report));
  fs.writeFileSync(mdPath, renderMarkdown(report));
  return { jsonPath, mdPath };
}

function writeReviewTicket(report, reviewFile) {
  if (!report.verdict) attachVerdict(report);
  ensureDir(path.dirname(reviewFile));
  fs.writeFileSync(reviewFile, renderReviewTicket(report));
  return reviewFile;
}

function printSummary(report) {
  if (!report.verdict) attachVerdict(report);
  const scoredFindings = report.findings.filter((finding) => finding.scored !== false);
  const bySeverity = scoredFindings.reduce((acc, finding) => {
    acc[finding.severity] = (acc[finding.severity] || 0) + 1;
    return acc;
  }, {});

  const lines = [];
  lines.push("DriftGuard Security Scanner+ Summary");
  lines.push(`Root: ${report.rootPath}`);
  if (report.savedBaseline) {
    lines.push(`Saved baseline: ${report.savedBaseline.path}`);
  }
  lines.push(`Risk: ${report.risk.level.toUpperCase()} (score ${report.risk.score})`);
  lines.push(
    `Severity: critical=${bySeverity.critical || 0} high=${bySeverity.high || 0} medium=${bySeverity.medium || 0} low=${bySeverity.low || 0}`
  );
  lines.push(`Findings: ${report.stats.findings}`);
  lines.push(`Combo Risks: ${report.stats.comboFindings || 0}`);
  if (report.stats.symlinks !== undefined) {
    lines.push(`Symlinks: ${report.stats.symlinks}`);
  }

  if (report.drift) {
    lines.push("");
    lines.push("--- What Changed Since Trust ---");
    if (report.trust) {
      lines.push(`Trust: ${report.trust.label}`);
      if (report.trust.reasons.length) {
        for (const reason of report.trust.reasons) lines.push(`  - ${reason}`);
      }
    }
    lines.push(
      `Files: +${report.drift.added.length} added, -${report.drift.removed.length} removed, ~${report.drift.changed.length} changed, ${report.drift.unchangedCount} unchanged`
    );
    if (report.drift.symlinks) {
      const sl = report.drift.symlinks;
      if (sl.added.length || sl.removed.length || sl.changed.length) {
        lines.push(
          `Symlinks: +${sl.added.length} added, -${sl.removed.length} removed, ~${sl.changed.length} changed`
        );
      }
    }
    if (report.drift.trust) {
      const trust = report.drift.trust;
      const approved = [trust.approvedBy || "unknown", trust.approvedAt || "unknown"];
      lines.push(`Trusted baseline: ${approved.join(" at ")}`);
      if (trust.gitCommit) lines.push(`  commit: ${trust.gitCommit.slice(0, 12)}`);
      if (trust.note) lines.push(`  note: ${trust.note}`);
    }
    if (report.drift.riskDiff) {
      const diff = report.drift.riskDiff;
      const baselineLevel = diff.baseline.level || "unknown";
      const currentLevel = diff.current.level || "unknown";
      const scoreDelta = diff.scoreDelta === null ? "unknown" : diff.scoreDelta;
      lines.push(
        `Risk diff: ${baselineLevel.toUpperCase()} -> ${currentLevel.toUpperCase()} full scan (score delta ${scoreDelta})`
      );
      if (diff.capabilities.added.length) {
        lines.push(`  ! New risk capabilities: ${diff.capabilities.added.join(", ")}`);
      }
    }
    if (report.drift.highlights) {
      const h = report.drift.highlights;
      if (h.newCapabilities && h.newCapabilities.length) {
        for (const cap of h.newCapabilities) lines.push(`  ! ${cap}`);
      }
      if (h.dependencyChanges && h.dependencyChanges.length) {
        lines.push(`  ! Dependency changes: ${h.dependencyChanges.join(", ")}`);
      }
    }
    if (report.drift.configChanged) {
      lines.push(`  ! Baseline config differs from current config`);
    }
    if (report.drift.rootMismatch) {
      lines.push(`  ! Baseline was created for a different root path`);
    }
    if (report.stats.trustedFindings) {
      lines.push(`Trusted (unchanged) findings: ${report.stats.trustedFindings}`);
    }
  }

  const topFindings = scoredFindings.slice(0, 5).map(formatFinding);
  if (topFindings.length) {
    lines.push("");
    lines.push("Top findings:");
    for (const line of topFindings) lines.push(`  ${line}`);
  }

  if (report.comboRisks && report.comboRisks.length) {
    lines.push("Combo risks:");
    for (const combo of report.comboRisks.slice(0, 3)) {
      lines.push(`  ${combo.severity.toUpperCase()} ${combo.id}: ${combo.description}`);
    }
  }

  if (report.verdict && report.verdict.nextSteps.length) {
    lines.push("");
    lines.push("Next steps:");
    for (const step of report.verdict.nextSteps) {
      lines.push(`  - ${step}`);
    }
  }

  lines.push(`VERDICT_JSON: ${JSON.stringify(report.verdict)}`);

  return lines.join("\n");
}

module.exports = {
  attachVerdict,
  buildVerdict,
  writeReports,
  printSummary,
  renderMarkdown,
  renderJson,
  renderReviewTicket,
  writeReviewTicket
};
