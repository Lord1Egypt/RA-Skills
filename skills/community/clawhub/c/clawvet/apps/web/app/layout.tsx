import type { Metadata } from "next";
import { Shield, LayoutDashboard, Settings, Github } from "lucide-react";
import "./globals.css";

export const metadata: Metadata = {
  title: "ClawVet — Skill Security for OpenClaw",
  description:
    "Scan OpenClaw skills for security threats before you install them.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen antialiased">
        {/* Ambient scanline overlay */}
        <div className="scanline-overlay fixed inset-0 pointer-events-none z-50 opacity-50" />

        <nav className="sticky top-0 z-40 border-b border-[var(--border)] bg-[var(--bg)]/80 backdrop-blur-xl">
          <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3">
            {/* Logo */}
            <a href="/" className="group flex items-center gap-3">
              <div className="relative flex h-9 w-9 items-center justify-center rounded-lg bg-accent/10 border border-accent/20 group-hover:glow-accent transition-all duration-300">
                <Shield size={18} className="text-accent" />
                <div className="absolute inset-0 rounded-lg bg-accent/5 group-hover:bg-accent/10 transition" />
              </div>
              <div className="flex flex-col">
                <span className="font-body text-sm font-semibold tracking-wide text-ink">
                  CLAWVET
                </span>
                <span className="font-body text-[10px] tracking-[0.2em] text-ink-faint uppercase">
                  Threat Intelligence
                </span>
              </div>
            </a>

            {/* Nav links */}
            <div className="flex items-center gap-1">
              <a
                href="/dashboard"
                className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-ink-muted hover:text-ink hover:bg-surface-3 transition-all"
              >
                <LayoutDashboard size={15} />
                Dashboard
              </a>
              <a
                href="/dashboard/settings"
                className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-ink-muted hover:text-ink hover:bg-surface-3 transition-all"
              >
                <Settings size={15} />
                Settings
              </a>
              <div className="mx-2 h-5 w-px bg-[var(--border)]" />
              <a
                href="/api/auth/github"
                className="group flex items-center gap-2 rounded-lg border border-[var(--border)] bg-surface-2 px-4 py-2 text-sm font-medium text-ink-muted hover:text-ink hover:border-accent/30 hover:bg-accent/5 transition-all duration-300"
              >
                <Github size={15} />
                Sign in
              </a>
            </div>
          </div>
        </nav>

        <main>{children}</main>
      </body>
    </html>
  );
}
