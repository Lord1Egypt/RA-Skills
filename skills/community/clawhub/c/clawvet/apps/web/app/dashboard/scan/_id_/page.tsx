"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { SkillAnalysisReport } from "@/components/SkillAnalysisReport";
import { ArrowLeft, Download, Share2, Loader2 } from "lucide-react";

export default function ScanDetailPage() {
  const params = useParams();
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchScan() {
      try {
        const res = await fetch(`/api/scans/${params.id}`);
        if (!res.ok) throw new Error("Scan not found");
        const data = await res.json();
        setResult(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load scan");
      } finally {
        setLoading(false);
      }
    }
    fetchScan();
  }, [params.id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <Loader2 size={24} className="animate-spin text-accent" />
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="mx-auto max-w-4xl px-6 py-8">
        <a
          href="/dashboard"
          className="group inline-flex items-center gap-2 rounded-lg px-3 py-1.5 text-sm text-ink-muted hover:text-ink hover:bg-surface-3 transition-all"
        >
          <ArrowLeft size={14} className="transition-transform group-hover:-translate-x-0.5" />
          Dashboard
        </a>
        <div className="mt-8 flex flex-col items-center justify-center rounded-xl border border-dashed border-[var(--border)] py-16">
          <p className="text-sm text-ink-faint">{error || "Scan not found"}</p>
          <p className="mt-1 text-xs text-ink-faint/50">
            The scan may have been run without a database connection.
          </p>
        </div>
      </div>
    );
  }

  function handleShare() {
    navigator.clipboard.writeText(window.location.href);
  }

  function handleExport() {
    const blob = new Blob([JSON.stringify(result, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `clawvet-${result.skillName || "scan"}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="mx-auto max-w-4xl px-6 py-8">
      <div className="mb-6 flex items-center justify-between">
        <a
          href="/dashboard"
          className="group inline-flex items-center gap-2 rounded-lg px-3 py-1.5 text-sm text-ink-muted hover:text-ink hover:bg-surface-3 transition-all"
        >
          <ArrowLeft size={14} className="transition-transform group-hover:-translate-x-0.5" />
          Dashboard
        </a>
        <div className="flex items-center gap-2">
          <button
            onClick={handleShare}
            className="inline-flex items-center gap-1.5 rounded-lg border border-[var(--border)] bg-surface-2 px-3 py-1.5 text-xs text-ink-muted hover:text-ink hover:border-accent/30 transition"
          >
            <Share2 size={12} />
            Share
          </button>
          <button
            onClick={handleExport}
            className="inline-flex items-center gap-1.5 rounded-lg border border-[var(--border)] bg-surface-2 px-3 py-1.5 text-xs text-ink-muted hover:text-ink hover:border-accent/30 transition"
          >
            <Download size={12} />
            Export JSON
          </button>
        </div>
      </div>

      <div className="opacity-0 animate-fade-in">
        <SkillAnalysisReport result={result} />
      </div>
    </div>
  );
}
