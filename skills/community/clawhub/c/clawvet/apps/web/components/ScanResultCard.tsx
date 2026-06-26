"use client";

import { ThreatBadge } from "./ThreatBadge";
import { RiskScoreGauge } from "./RiskScoreGauge";
import { ArrowUpRight, Clock } from "lucide-react";

interface ScanSummary {
  id: string;
  skillName: string;
  riskScore: number;
  riskGrade: string;
  findingsCount: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  createdAt: string;
}

function gradeColor(grade: string) {
  const colors: Record<string, string> = {
    A: "border-threat-safe/20 hover:border-threat-safe/40",
    B: "border-lime-400/20 hover:border-lime-400/40",
    C: "border-threat-medium/20 hover:border-threat-medium/40",
    D: "border-threat-high/20 hover:border-threat-high/40",
    F: "border-threat-critical/20 hover:border-threat-critical/40",
  };
  return colors[grade] || "border-[var(--border)]";
}

function timeSince(date: string) {
  const seconds = Math.floor(
    (new Date().getTime() - new Date(date).getTime()) / 1000
  );
  if (seconds < 60) return "just now";
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return new Date(date).toLocaleDateString();
}

export function ScanResultCard({ scan }: { scan: ScanSummary }) {
  const total =
    scan.findingsCount.critical +
    scan.findingsCount.high +
    scan.findingsCount.medium +
    scan.findingsCount.low;

  return (
    <a
      href={`/dashboard/scan/${scan.id}`}
      className={`group relative block rounded-xl border bg-surface-1 p-5 transition-all duration-300 card-hover ${gradeColor(scan.riskGrade)}`}
    >
      {/* Top row: name + gauge */}
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            <h3 className="truncate font-body text-sm font-semibold tracking-tight text-ink">
              {scan.skillName}
            </h3>
            <ArrowUpRight
              size={14}
              className="shrink-0 text-ink-faint opacity-0 transition group-hover:opacity-100"
            />
          </div>
          <div className="mt-1.5 flex items-center gap-1.5 text-ink-faint">
            <Clock size={11} />
            <span className="font-body text-[11px]">
              {timeSince(scan.createdAt)}
            </span>
            <span className="text-ink-faint/50 mx-0.5">·</span>
            <span className="font-body text-[11px]">
              {total} finding{total !== 1 ? "s" : ""}
            </span>
          </div>
        </div>
        <RiskScoreGauge score={scan.riskScore} size="sm" />
      </div>

      {/* Severity badges */}
      {total > 0 && (
        <div className="mt-4 flex flex-wrap gap-1.5">
          {scan.findingsCount.critical > 0 && (
            <ThreatBadge severity="critical" count={scan.findingsCount.critical} />
          )}
          {scan.findingsCount.high > 0 && (
            <ThreatBadge severity="high" count={scan.findingsCount.high} />
          )}
          {scan.findingsCount.medium > 0 && (
            <ThreatBadge severity="medium" count={scan.findingsCount.medium} />
          )}
          {scan.findingsCount.low > 0 && (
            <ThreatBadge severity="low" count={scan.findingsCount.low} />
          )}
        </div>
      )}

      {/* Clean skill indicator */}
      {total === 0 && (
        <div className="mt-3 flex items-center gap-1.5 text-threat-safe">
          <div className="h-1.5 w-1.5 rounded-full bg-threat-safe" />
          <span className="font-body text-xs tracking-wider">CLEAN</span>
        </div>
      )}
    </a>
  );
}
