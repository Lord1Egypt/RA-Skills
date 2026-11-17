import type { Snapshot } from "./types";

export function formatSnapshot(s: Snapshot): string {
  if (s.error) {
    return `❌ ${s.provider}: ${s.error}${s.authHint ? ` → ${s.authHint}` : ""}`;
  }
  const bits: string[] = [];
  if (typeof s.balance === "number") {
    const cur = s.currency ?? "";
    bits.push(cur === "CREDITS" ? `${s.balance.toLocaleString()} credits` : `${cur} ${s.balance}`.trim());
  }
  if (typeof s.usedPercent === "number") bits.push(`${s.usedPercent}% used`);
  if (typeof s.monthCost === "number" && s.monthCost > 0) {
    bits.push(`month ${(s.currency ?? "USD") === "USD" ? "$" : ""}${s.monthCost}`);
  }
  if (s.resetsAt) bits.push(`resets ${s.resetsAt}`);
  return `✅ ${s.provider}: ${bits.join(" · ") || "ok"}`;
}

export function formatTrend(t: {
  provider: string;
  basis: string;
  balance?: number;
  currency?: string;
  remainingPercent?: number;
  dailyRate: number | null;
  estimatedDaysLeft: number | null;
  lowBalance: boolean;
  samples: number;
  spanHours: number;
}): string {
  const status = t.lowBalance ? "⚠️ LOW" : "✅";
  const meta = t.samples ? ` (n=${t.samples}·${Math.round(t.spanHours)}h)` : "";
  const money = (v: number): string => {
    const cur = t.currency ?? "USD";
    if (cur === "USD") return `$${v.toFixed(2)}`;
    if (cur === "CREDITS") return `${v.toFixed(0)} credits`;
    return `${v.toFixed(2)} ${cur}`;
  };
  const days = t.estimatedDaysLeft !== null ? `~${t.estimatedDaysLeft}d` : "N/A";
  if (t.basis === "balance") {
    if (t.dailyRate === null || typeof t.balance !== "number") {
      return `${status} ${t.provider}: balance ${money(t.balance ?? 0)} (history too short for a rate)${meta}`;
    }
    return `${status} ${t.provider}: balance ${money(t.balance)}, burn ${money(t.dailyRate)}/day, ${days} to exhaust${meta}`;
  }
  return `${status} ${t.provider}: ${t.remainingPercent ?? 0}% left, ${t.dailyRate ?? 0}/day, ${days} to exhaust${meta}`;
}
