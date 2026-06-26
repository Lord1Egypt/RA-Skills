"use client";

import { useState, useEffect } from "react";
import {
  Key,
  Bell,
  ShieldCheck,
  Copy,
  RefreshCw,
  Plus,
  Trash2,
  Globe,
  Lock,
  Eye,
  EyeOff,
  Loader2,
  Check,
} from "lucide-react";

interface User {
  id: string;
  githubUsername: string;
  email: string | null;
  plan: string;
  apiKey: string | null;
}

interface Webhook {
  id: string;
  url: string;
  events: string[];
  active: boolean;
  createdAt: string;
}

export default function SettingsPage() {
  const [showKey, setShowKey] = useState(false);
  const [copied, setCopied] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [webhooks, setWebhooks] = useState<Webhook[]>([]);
  const [newWebhookUrl, setNewWebhookUrl] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch("/api/auth/me");
        if (res.ok) {
          const data = await res.json();
          if (data.user) {
            setUser(data.user);
            if (data.user.apiKey) {
              const whRes = await fetch("/api/webhooks", {
                headers: { "x-api-key": data.user.apiKey },
              });
              if (whRes.ok) {
                const whData = await whRes.json();
                setWebhooks(whData.webhooks || []);
              }
            }
          }
        }
      } catch {
        // not authenticated
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  function handleCopy() {
    if (!user?.apiKey) return;
    navigator.clipboard.writeText(user.apiKey);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  async function handleAddWebhook() {
    if (!newWebhookUrl || !user?.apiKey) return;
    try {
      const res = await fetch("/api/webhooks", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": user.apiKey,
        },
        body: JSON.stringify({
          url: newWebhookUrl,
          events: ["scan.complete", "scan.critical"],
        }),
      });
      if (res.ok) {
        const hook = await res.json();
        setWebhooks((prev) => [...prev, hook]);
        setNewWebhookUrl("");
      }
    } catch {
      // failed
    }
  }

  const displayKey = user?.apiKey || "cg_••••••••••••••••••••••••••••••";
  const maskedKey = user?.apiKey
    ? `cg_${"•".repeat(user.apiKey.length - 3)}`
    : "cg_••••••••••••••••••••••••••••••";

  return (
    <div className="mx-auto max-w-3xl px-6 py-8">
      <h1 className="font-display text-3xl tracking-tight">Settings</h1>
      <p className="mt-1 text-sm text-ink-muted">
        Manage API keys, webhooks, and security preferences
      </p>

      {/* API Key */}
      <section className="mt-8 rounded-xl border border-[var(--border)] bg-surface-1 overflow-hidden">
        <div className="flex items-center gap-2 border-b border-[var(--border)] px-5 py-3 bg-surface-2/30">
          <Key size={14} className="text-accent" />
          <span className="font-body text-xs font-semibold tracking-[0.2em] uppercase text-ink-faint">
            API Key
          </span>
        </div>
        <div className="p-5">
          <p className="text-sm text-ink-muted">
            Use this key to authenticate CLI and CI/CD integrations.
          </p>
          <div className="mt-4 flex gap-2">
            <div className="flex flex-1 items-center gap-2 rounded-lg border border-[var(--border)] bg-surface-0 px-4 py-2.5">
              <Lock size={12} className="text-ink-faint shrink-0" />
              <code className="flex-1 font-body text-sm text-ink truncate">
                {showKey ? displayKey : maskedKey}
              </code>
              <button
                onClick={() => setShowKey(!showKey)}
                className="text-ink-faint hover:text-ink transition"
              >
                {showKey ? <EyeOff size={14} /> : <Eye size={14} />}
              </button>
            </div>
            <button
              onClick={handleCopy}
              className="flex items-center gap-1.5 rounded-lg border border-[var(--border)] bg-surface-2 px-3 py-2.5 text-xs text-ink-muted hover:text-ink hover:border-accent/30 transition"
            >
              {copied ? <Check size={12} /> : <Copy size={12} />}
              {copied ? "Copied!" : "Copy"}
            </button>
          </div>
          {!user && !loading && (
            <p className="mt-3 text-xs text-ink-faint">
              <a href="/api/auth/github" className="text-accent hover:underline">
                Sign in with GitHub
              </a>{" "}
              to get your API key.
            </p>
          )}
        </div>
      </section>

      {/* Webhooks */}
      <section className="mt-4 rounded-xl border border-[var(--border)] bg-surface-1 overflow-hidden">
        <div className="flex items-center justify-between border-b border-[var(--border)] px-5 py-3 bg-surface-2/30">
          <div className="flex items-center gap-2">
            <Bell size={14} className="text-accent" />
            <span className="font-body text-xs font-semibold tracking-[0.2em] uppercase text-ink-faint">
              Webhooks
            </span>
          </div>
          <span className="rounded bg-accent/10 px-2 py-0.5 font-body text-[10px] text-accent tracking-wider">
            PRO
          </span>
        </div>
        <div className="p-5">
          <p className="text-sm text-ink-muted">
            Get notified when scans complete or critical threats are found.
          </p>
          <div className="mt-4 flex gap-2">
            <div className="flex flex-1 items-center gap-2 rounded-lg border border-[var(--border)] bg-surface-0 px-4 py-2.5">
              <Globe size={12} className="text-ink-faint shrink-0" />
              <input
                type="url"
                value={newWebhookUrl}
                onChange={(e) => setNewWebhookUrl(e.target.value)}
                placeholder="https://your-server.com/webhook"
                className="flex-1 bg-transparent font-body text-sm text-ink placeholder:text-ink-faint/40 focus:outline-none"
              />
            </div>
            <button
              onClick={handleAddWebhook}
              disabled={!newWebhookUrl || !user?.apiKey}
              className="flex items-center gap-1.5 rounded-lg bg-accent px-4 py-2.5 text-sm font-semibold text-surface-0 hover:bg-accent-dim transition glow-accent disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <Plus size={14} />
              Add
            </button>
          </div>

          {webhooks.length > 0 ? (
            <div className="mt-4 space-y-2">
              {webhooks.map((hook) => (
                <div
                  key={hook.id}
                  className="flex items-center justify-between rounded-lg border border-[var(--border)] bg-surface-0 px-4 py-3"
                >
                  <div className="min-w-0 flex-1">
                    <code className="truncate font-body text-xs text-ink">
                      {hook.url}
                    </code>
                    <div className="mt-1 flex gap-1.5">
                      {hook.events.map((e) => (
                        <span
                          key={e}
                          className="rounded bg-surface-3 px-1.5 py-0.5 font-body text-[10px] text-ink-faint"
                        >
                          {e}
                        </span>
                      ))}
                    </div>
                  </div>
                  <button className="ml-3 text-ink-faint hover:text-threat-critical transition">
                    <Trash2 size={14} />
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="mt-6 flex flex-col items-center rounded-lg border border-dashed border-[var(--border)] py-8">
              <Bell size={24} className="text-ink-faint/30" />
              <p className="mt-2 text-sm text-ink-faint">No webhooks configured</p>
              <p className="text-xs text-ink-faint/50">
                Events: scan.complete, scan.critical
              </p>
            </div>
          )}
        </div>
      </section>

      {/* Allowlist / Blocklist */}
      <section className="mt-4 rounded-xl border border-[var(--border)] bg-surface-1 overflow-hidden">
        <div className="flex items-center justify-between border-b border-[var(--border)] px-5 py-3 bg-surface-2/30">
          <div className="flex items-center gap-2">
            <ShieldCheck size={14} className="text-accent" />
            <span className="font-body text-xs font-semibold tracking-[0.2em] uppercase text-ink-faint">
              Allowlist / Blocklist
            </span>
          </div>
          <span className="rounded bg-accent/10 px-2 py-0.5 font-body text-[10px] text-accent tracking-wider">
            TEAM
          </span>
        </div>
        <div className="p-5">
          <p className="text-sm text-ink-muted">
            Automatically approve or block specific skills or publishers.
          </p>
          <div className="mt-6 grid grid-cols-2 gap-4">
            <div className="rounded-lg border border-[var(--border)] bg-surface-0 p-4">
              <div className="mb-3 flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-threat-safe" />
                <span className="font-body text-xs font-semibold tracking-wider uppercase text-ink-faint">
                  Allowed
                </span>
              </div>
              <div className="flex flex-col items-center py-6">
                <ShieldCheck size={20} className="text-ink-faint/20" />
                <p className="mt-2 text-xs text-ink-faint">No entries</p>
              </div>
            </div>
            <div className="rounded-lg border border-[var(--border)] bg-surface-0 p-4">
              <div className="mb-3 flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-threat-critical" />
                <span className="font-body text-xs font-semibold tracking-wider uppercase text-ink-faint">
                  Blocked
                </span>
              </div>
              <div className="flex flex-col items-center py-6">
                <ShieldCheck size={20} className="text-ink-faint/20" />
                <p className="mt-2 text-xs text-ink-faint">No entries</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Plan info */}
      <section className="mt-4 rounded-xl border border-accent/15 bg-accent/[0.02] p-5">
        <div className="flex items-center justify-between">
          <div>
            <span className="font-body text-xs font-semibold tracking-[0.2em] uppercase text-accent/70">
              Current Plan
            </span>
            <h3 className="mt-0.5 font-display text-xl capitalize">
              {user?.plan || "Free"}
            </h3>
            <p className="mt-1 text-sm text-ink-muted">
              {user?.plan === "pro"
                ? "Unlimited scans · AI analysis · Webhooks · API access"
                : user?.plan === "team"
                  ? "Everything in Pro · Team inventory · Custom rules · SSO"
                  : "50 scans/month · Basic dashboard · CLI tool"}
            </p>
          </div>
          <a
            href="/#pricing"
            className="rounded-lg border border-accent/20 bg-accent/5 px-4 py-2 text-sm font-semibold text-accent hover:bg-accent/10 transition"
          >
            Upgrade
          </a>
        </div>
      </section>
    </div>
  );
}
