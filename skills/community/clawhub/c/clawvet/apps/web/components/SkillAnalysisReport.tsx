"use client";

import { ThreatBadge } from "./ThreatBadge";
import { RiskScoreGauge } from "./RiskScoreGauge";
import {
  ShieldBan,
  ShieldAlert,
  ShieldCheck,
  FileCode2,
  ChevronDown,
} from "lucide-react";
import { useState } from "react";

interface Finding {
  category: string;
  severity: "critical" | "high" | "medium" | "low";
  title: string;
  description: string;
  evidence?: string;
  lineNumber?: number | null;
  analysisPass: string;
}

interface ScanResult {
  skillName: string;
  skillVersion?: string;
  riskScore: number;
  riskGrade: string;
  recommendation?: string;
  findingsCount: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  findings: Finding[];
}

function RecBanner({ rec }: { rec: string }) {
  const config: Record<
    string,
    { icon: React.ReactNode; bg: string; border: string; text: string; label: string }
  > = {
    block: {
      icon: <ShieldBan size={18} />,
      bg: "bg-threat-critical/[0.06]",
      border: "border-threat-critical/20",
      text: "text-threat-critical",
      label: "Block Installation — This skill contains dangerous patterns",
    },
    warn: {
      icon: <ShieldAlert size={18} />,
      bg: "bg-threat-medium/[0.06]",
      border: "border-threat-medium/20",
      text: "text-threat-medium",
      label: "Review Required — Suspicious patterns detected",
    },
    approve: {
      icon: <ShieldCheck size={18} />,
      bg: "bg-threat-safe/[0.06]",
      border: "border-threat-safe/20",
      text: "text-threat-safe",
      label: "Safe to Install — No significant threats detected",
    },
  };

  const c = config[rec] || config.warn;

  return (
    <div
      className={`flex items-center gap-3 rounded-xl border ${c.border} ${c.bg} px-5 py-4`}
    >
      <span className={c.text}>{c.icon}</span>
      <span className={`text-sm font-medium ${c.text}`}>{c.label}</span>
    </div>
  );
}

function FindingCard({ finding, index }: { finding: Finding; index: number }) {
  const [expanded, setExpanded] = useState(index < 3);

  const severityLeftBorder: Record<string, string> = {
    critical: "border-l-threat-critical",
    high: "border-l-threat-high",
    medium: "border-l-threat-medium",
    low: "border-l-threat-low",
  };

  const passLabels: Record<string, string> = {
    "static-analysis": "Static",
    "metadata-validator": "Metadata",
    "semantic-analysis": "AI",
    "dependency-checker": "Deps",
    "typosquat-detector": "Typosquat",
  };

  return (
    <div
      className={`rounded-lg border border-[var(--border)] border-l-2 ${severityLeftBorder[finding.severity]} bg-surface-1 overflow-hidden transition-all`}
    >
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex w-full items-center justify-between gap-3 px-4 py-3 text-left hover:bg-surface-2/50 transition"
      >
        <div className="flex items-center gap-3 min-w-0">
          <ThreatBadge severity={finding.severity} />
          <span className="truncate text-sm font-medium text-ink">
            {finding.title}
          </span>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          {finding.lineNumber && (
            <span className="font-body text-[10px] text-ink-faint">
              L{finding.lineNumber}
            </span>
          )}
          <span className="rounded bg-surface-3 px-1.5 py-0.5 font-body text-[10px] text-ink-faint">
            {passLabels[finding.analysisPass] || finding.analysisPass}
          </span>
          <ChevronDown
            size={14}
            className={`text-ink-faint transition-transform ${expanded ? "rotate-180" : ""}`}
          />
        </div>
      </button>
      {expanded && (
        <div className="border-t border-[var(--border)] px-4 py-3 space-y-3">
          <p className="text-sm text-ink-muted leading-relaxed">
            {finding.description}
          </p>
          {finding.evidence && (
            <div className="evidence-code rounded-lg px-4 py-3 font-body text-xs text-ink overflow-x-auto">
              <div className="flex items-center gap-2 mb-1.5">
                <FileCode2 size={12} className="text-ink-faint" />
                <span className="text-[10px] uppercase tracking-wider text-ink-faint">
                  Evidence
                </span>
              </div>
              <pre className="whitespace-pre-wrap break-all">{finding.evidence}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export function SkillAnalysisReport({ result }: { result: ScanResult }) {
  const severityOrder = ["critical", "high", "medium", "low"] as const;
  const total =
    result.findingsCount.critical +
    result.findingsCount.high +
    result.findingsCount.medium +
    result.findingsCount.low;

  return (
    <div className="space-y-6">
      {/* Header card */}
      <div className="rounded-xl border border-[var(--border)] bg-surface-1 p-6">
        <div className="flex items-start justify-between gap-6">
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-3">
              <h1 className="font-display text-2xl tracking-tight">
                {result.skillName}
              </h1>
              {result.skillVersion && (
                <span className="rounded bg-surface-3 px-2 py-0.5 font-body text-xs text-ink-faint">
                  v{result.skillVersion}
                </span>
              )}
            </div>

            {/* Severity summary bar */}
            <div className="mt-5 flex items-center gap-4">
              <div className="flex-1">
                <div className="flex h-2 rounded-full overflow-hidden bg-surface-3">
                  {result.findingsCount.critical > 0 && (
                    <div
                      className="bg-threat-critical severity-bar"
                      style={{
                        "--bar-width": `${(result.findingsCount.critical / Math.max(total, 1)) * 100}%`,
                      } as React.CSSProperties}
                    />
                  )}
                  {result.findingsCount.high > 0 && (
                    <div
                      className="bg-threat-high severity-bar"
                      style={{
                        "--bar-width": `${(result.findingsCount.high / Math.max(total, 1)) * 100}%`,
                      } as React.CSSProperties}
                    />
                  )}
                  {result.findingsCount.medium > 0 && (
                    <div
                      className="bg-threat-medium severity-bar"
                      style={{
                        "--bar-width": `${(result.findingsCount.medium / Math.max(total, 1)) * 100}%`,
                      } as React.CSSProperties}
                    />
                  )}
                  {result.findingsCount.low > 0 && (
                    <div
                      className="bg-threat-low severity-bar"
                      style={{
                        "--bar-width": `${(result.findingsCount.low / Math.max(total, 1)) * 100}%`,
                      } as React.CSSProperties}
                    />
                  )}
                  {total === 0 && <div className="bg-threat-safe w-full" />}
                </div>
                <div className="mt-2 flex gap-3">
                  {severityOrder.map((sev) => {
                    const count =
                      result.findingsCount[sev as keyof typeof result.findingsCount];
                    if (!count) return null;
                    return (
                      <ThreatBadge key={sev} severity={sev} count={count} />
                    );
                  })}
                  {total === 0 && (
                    <span className="font-body text-xs text-threat-safe tracking-wider">
                      NO THREATS
                    </span>
                  )}
                </div>
              </div>
              <RiskScoreGauge score={result.riskScore} size="lg" />
            </div>
          </div>
        </div>
      </div>

      {/* Recommendation */}
      {result.recommendation && <RecBanner rec={result.recommendation} />}

      {/* Findings list */}
      {result.findings.length > 0 && (
        <div>
          <h2 className="mb-3 font-body text-xs font-semibold tracking-[0.2em] uppercase text-ink-faint">
            Findings ({total})
          </h2>
          <div className="space-y-2">
            {result.findings.map((finding, i) => (
              <FindingCard key={i} finding={finding} index={i} />
            ))}
          </div>
        </div>
      )}

      {result.findings.length === 0 && (
        <div className="flex flex-col items-center justify-center rounded-xl border border-threat-safe/20 bg-threat-safe/[0.03] py-16">
          <ShieldCheck size={48} className="text-threat-safe/50" />
          <p className="mt-4 font-display text-xl text-threat-safe">
            All clear
          </p>
          <p className="mt-1 text-sm text-ink-muted">
            No threats detected — this skill looks clean.
          </p>
        </div>
      )}
    </div>
  );
}
