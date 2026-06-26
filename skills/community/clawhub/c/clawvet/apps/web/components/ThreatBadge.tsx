"use client";

import { AlertTriangle, AlertCircle, Info, ShieldAlert } from "lucide-react";

type Severity = "critical" | "high" | "medium" | "low";

const CONFIG: Record<
  Severity,
  { bg: string; text: string; border: string; icon: React.ReactNode }
> = {
  critical: {
    bg: "bg-threat-critical/10",
    text: "text-threat-critical",
    border: "border-threat-critical/25",
    icon: <ShieldAlert size={11} />,
  },
  high: {
    bg: "bg-threat-high/10",
    text: "text-threat-high",
    border: "border-threat-high/25",
    icon: <AlertTriangle size={11} />,
  },
  medium: {
    bg: "bg-threat-medium/10",
    text: "text-threat-medium",
    border: "border-threat-medium/25",
    icon: <AlertCircle size={11} />,
  },
  low: {
    bg: "bg-threat-low/10",
    text: "text-threat-low",
    border: "border-threat-low/25",
    icon: <Info size={11} />,
  },
};

export function ThreatBadge({
  severity,
  count,
}: {
  severity: Severity;
  count?: number;
}) {
  const c = CONFIG[severity];
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-md border px-2 py-0.5 font-body text-[11px] font-semibold uppercase tracking-wider ${c.bg} ${c.text} ${c.border}`}
    >
      {c.icon}
      {severity}
      {count !== undefined && (
        <span className="ml-0.5 opacity-70">{count}</span>
      )}
    </span>
  );
}
