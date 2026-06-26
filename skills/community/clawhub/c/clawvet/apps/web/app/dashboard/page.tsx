"use client";

import { useState, useEffect } from "react";
import { ScanResultCard } from "@/components/ScanResultCard";
import { SkillAnalysisReport } from "@/components/SkillAnalysisReport";
import {
  Search,
  Scan,
  Shield,
  AlertTriangle,
  Activity,
  Loader2,
  RefreshCw,
} from "lucide-react";

interface ScanSummary {
  id: string;
  skillName: string;
  riskScore: number;
  riskGrade: string;
  findingsCount: { critical: number; high: number; medium: number; low: number };
  createdAt: string;
}

interface Stats {
  skillsScanned: number;
  threatsFound: number;
  avgRiskScore: number;
}

export default function DashboardPage() {
  const [skillInput, setSkillInput] = useState("");
  const [scanning, setScanning] = useState(false);
  const [scanResult, setScanResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [recentScans, setRecentScans] = useState<ScanSummary[]>([]);
  const [stats, setStats] = useState<Stats>({ skillsScanned: 0, threatsFound: 0, avgRiskScore: 0 });
  const [loading, setLoading] = useState(true);

  async function fetchData() {
    setLoading(true);
    try {
      const [scansRes, statsRes] = await Promise.all([
        fetch("/api/scans?limit=12"),
        fetch("/api/stats"),
      ]);

      if (scansRes.ok) {
        const data = await scansRes.json();
        setRecentScans(data.scans || []);
      }
      if (statsRes.ok) {
        const data = await statsRes.json();
        setStats(data);
      }
    } catch {
      // API unavailable — keep empty state
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchData();
  }, []);

  async function handleScan(e: React.FormEvent) {
    e.preventDefault();
    if (!skillInput.trim()) return;

    setScanning(true);
    setError(null);
    setScanResult(null);

    try {
      const res = await fetch("/api/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: skillInput }),
      });
      if (!res.ok) throw new Error(`Scan failed: ${res.statusText}`);
      const result = await res.json();
      setScanResult(result);
      fetchData();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Scan failed");
    } finally {
      setScanning(false);
    }
  }

  return (
    <div className="mx-auto max-w-7xl px-6 py-8">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="font-display text-3xl tracking-tight">Dashboard</h1>
          <p className="mt-1 text-sm text-ink-muted">
            Scan, analyze, and track skill security
          </p>
        </div>
        <button
          onClick={fetchData}
          className="flex items-center gap-1.5 rounded-lg border border-[var(--border)] bg-surface-2 px-3 py-1.5 text-xs text-ink-muted hover:text-ink hover:border-accent/30 transition"
        >
          <RefreshCw size={12} className={loading ? "animate-spin" : ""} />
          Refresh
        </button>
      </div>

      {/* Stats row */}
      <div className="mt-6 grid grid-cols-3 gap-4">
        <div className="rounded-xl border border-[var(--border)] bg-surface-1 px-5 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-accent/[0.06] border border-accent/10">
              <Scan size={16} className="text-accent" />
            </div>
            <div>
              <div className="font-body text-xl font-bold text-ink">
                {stats.skillsScanned}
              </div>
              <div className="font-body text-[11px] tracking-wider uppercase text-ink-faint">
                Skills scanned
              </div>
            </div>
          </div>
        </div>
        <div className="rounded-xl border border-[var(--border)] bg-surface-1 px-5 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-threat-medium/[0.08] border border-threat-medium/15">
              <AlertTriangle size={16} className="text-threat-medium" />
            </div>
            <div>
              <div className="font-body text-xl font-bold text-ink">
                {stats.threatsFound}
              </div>
              <div className="font-body text-[11px] tracking-wider uppercase text-ink-faint">
                Total findings
              </div>
            </div>
          </div>
        </div>
        <div className="rounded-xl border border-[var(--border)] bg-surface-1 px-5 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-threat-critical/[0.08] border border-threat-critical/15">
              <Shield size={16} className="text-threat-critical" />
            </div>
            <div>
              <div className="font-body text-xl font-bold text-ink">
                {stats.avgRiskScore}
              </div>
              <div className="font-body text-[11px] tracking-wider uppercase text-ink-faint">
                Avg risk score
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Scan input */}
      <form onSubmit={handleScan} className="mt-8">
        <div className="rounded-xl border border-[var(--border)] bg-surface-1 overflow-hidden">
          <div className="flex items-center gap-2 border-b border-[var(--border)] px-4 py-2.5">
            <Search size={14} className="text-ink-faint" />
            <span className="font-body text-xs tracking-wider uppercase text-ink-faint">
              Scan Skill
            </span>
          </div>
          <textarea
            value={skillInput}
            onChange={(e) => setSkillInput(e.target.value)}
            className="w-full border-0 bg-transparent p-4 font-body text-sm text-ink placeholder:text-ink-faint/50 resize-none focus:outline-none focus:ring-0"
            rows={6}
            placeholder={`Paste SKILL.md content here...\n\n---\nname: my-skill\ndescription: A cool skill\nversion: 1.0.0\n---\n# My Skill\n...`}
          />
          <div className="flex items-center justify-between border-t border-[var(--border)] px-4 py-3 bg-surface-2/30">
            <span className="font-body text-[11px] text-ink-faint">
              {skillInput.length > 0
                ? `${skillInput.split("\n").length} lines`
                : "Supports YAML frontmatter + markdown body"}
            </span>
            <button
              type="submit"
              disabled={scanning || !skillInput.trim()}
              className="inline-flex items-center gap-2 rounded-lg bg-accent px-5 py-2 text-sm font-semibold text-surface-0 transition-all duration-300 hover:bg-accent-dim disabled:opacity-30 disabled:cursor-not-allowed glow-accent"
            >
              {scanning ? (
                <>
                  <Loader2 size={14} className="animate-spin" />
                  Scanning...
                </>
              ) : (
                <>
                  <Scan size={14} />
                  Analyze
                </>
              )}
            </button>
          </div>
        </div>
      </form>

      {error && (
        <div className="mt-4 flex items-center gap-3 rounded-xl border border-threat-critical/20 bg-threat-critical/[0.06] px-5 py-4 text-sm text-threat-critical">
          <AlertTriangle size={16} />
          {error}
        </div>
      )}

      {scanResult && (
        <div className="mt-8 opacity-0 animate-fade-in">
          <SkillAnalysisReport result={scanResult} />
        </div>
      )}

      {/* Recent scans */}
      <div className="mt-12">
        <div className="mb-4 flex items-center gap-2">
          <Activity size={14} className="text-ink-faint" />
          <h2 className="font-body text-xs font-semibold tracking-[0.2em] uppercase text-ink-faint">
            Recent Scans
          </h2>
        </div>
        {recentScans.length > 0 ? (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {recentScans.map((scan, i) => (
              <div
                key={scan.id}
                className={`opacity-0 animate-slide-up stagger-${Math.min(i + 1, 6)}`}
              >
                <ScanResultCard scan={scan} />
              </div>
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-[var(--border)] py-16">
            <Scan size={32} className="text-ink-faint/20" />
            <p className="mt-3 text-sm text-ink-faint">No scans yet</p>
            <p className="text-xs text-ink-faint/50">
              Paste a SKILL.md above to run your first scan
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
