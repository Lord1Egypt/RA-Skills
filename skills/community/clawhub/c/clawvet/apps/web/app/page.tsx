import {
  Shield,
  AlertTriangle,
  Zap,
  Terminal,
  Search,
  FileWarning,
  Fingerprint,
  ArrowRight,
  Check,
  Scan,
  Lock,
  Eye,
} from "lucide-react";

function RadarGraphic() {
  return (
    <div className="relative mx-auto h-[420px] w-[420px]">
      {/* Concentric rings */}
      {[160, 120, 80, 40].map((r, i) => (
        <div
          key={r}
          className="absolute rounded-full border border-accent/[0.07]"
          style={{
            width: r * 2 + 20,
            height: r * 2 + 20,
            left: `calc(50% - ${r + 10}px)`,
            top: `calc(50% - ${r + 10}px)`,
          }}
        />
      ))}

      {/* Cross hairs */}
      <div className="absolute left-1/2 top-0 bottom-0 w-px bg-accent/[0.06]" />
      <div className="absolute top-1/2 left-0 right-0 h-px bg-accent/[0.06]" />

      {/* Sweep */}
      <div className="absolute inset-0 animate-sweep">
        <div
          className="absolute left-1/2 top-1/2 h-[210px] w-[210px] origin-bottom-left -translate-x-0 -translate-y-full"
          style={{
            background:
              "conic-gradient(from -10deg at 0% 100%, rgba(0,255,170,0.12) 0deg, transparent 40deg)",
          }}
        />
      </div>

      {/* Center pulse */}
      <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
        <div className="h-3 w-3 rounded-full bg-accent animate-pulse-slow" />
        <div className="absolute inset-0 h-3 w-3 rounded-full bg-accent/40 animate-ping" />
      </div>

      {/* Threat blips */}
      {[
        { x: 70, y: -90, color: "#ff2d55", delay: "0s", label: "RCE" },
        { x: -110, y: -40, color: "#ff6b35", delay: "0.5s", label: "Creds" },
        { x: 40, y: 100, color: "#ffb800", delay: "1s", label: "Inject" },
        { x: -60, y: 70, color: "#ff2d55", delay: "1.5s", label: "Exfil" },
        { x: 130, y: 20, color: "#5ac8fa", delay: "0.8s", label: "Typo" },
      ].map((blip, i) => (
        <div
          key={i}
          className="absolute left-1/2 top-1/2 flex items-center gap-1.5"
          style={{
            transform: `translate(calc(-50% + ${blip.x}px), calc(-50% + ${blip.y}px))`,
          }}
        >
          <div
            className="h-2 w-2 rounded-full animate-pulse-slow"
            style={{ backgroundColor: blip.color, animationDelay: blip.delay }}
          />
          <span
            className="font-body text-[10px] tracking-wider uppercase opacity-50"
            style={{ color: blip.color }}
          >
            {blip.label}
          </span>
        </div>
      ))}
    </div>
  );
}

export default function HomePage() {
  const features = [
    {
      icon: <Terminal size={20} />,
      title: "Static Pattern Detection",
      desc: "54 regex rules detect RCE, reverse shells, credential theft, DNS exfil, obfuscation, and C2 infrastructure.",
      tag: "PASS 01",
    },
    {
      icon: <FileWarning size={20} />,
      title: "Metadata Validation",
      desc: "Cross-references declared dependencies against actual usage. Catches undeclared binaries and environment variables.",
      tag: "PASS 02",
    },
    {
      icon: <Eye size={20} />,
      title: "AI Semantic Analysis",
      desc: "Claude scrutinizes skill instructions for social engineering, prompt injection attempts, and hidden functionality.",
      tag: "PASS 03",
    },
    {
      icon: <Fingerprint size={20} />,
      title: "Typosquat Detection",
      desc: "Levenshtein distance analysis against popular skills catches name impersonation and homoglyph attacks.",
      tag: "PASS 04",
    },
    {
      icon: <Search size={20} />,
      title: "Dependency Risk Audit",
      desc: "Scans bundled packages for known vulnerabilities, low-reputation publishers, and auto-install exploits.",
      tag: "PASS 05",
    },
    {
      icon: <Scan size={20} />,
      title: "SKILL.md Deep Parse",
      desc: "Extracts every code block, URL, IP address, and domain from YAML frontmatter and markdown instruction body.",
      tag: "PASS 06",
    },
  ];

  const plans = [
    {
      name: "Free",
      price: "$0",
      period: "forever",
      features: [
        "50 scans per month",
        "CLI tool access",
        "Basic web dashboard",
        "Community support",
      ],
    },
    {
      name: "Pro",
      price: "$29",
      period: "/month",
      highlight: true,
      features: [
        "Unlimited scans",
        "AI semantic analysis",
        "Webhook alerts",
        "CI/CD integration",
        "Full API access",
        "Priority support",
      ],
    },
    {
      name: "Team",
      price: "$99",
      period: "/month",
      features: [
        "Everything in Pro",
        "Team skill inventory",
        "Custom detection rules",
        "SSO & audit logs",
        "Dedicated support",
      ],
    },
  ];

  return (
    <div className="relative overflow-hidden">
      {/* Hero */}
      <section className="relative grid-bg">
        {/* Gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-b from-surface-0 via-transparent to-surface-0" />
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-accent/[0.03] rounded-full blur-[120px]" />

        <div className="relative mx-auto max-w-7xl px-6 pt-20 pb-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left: Copy */}
            <div className="opacity-0 animate-fade-in">
              {/* Alert badge */}
              <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-threat-critical/20 bg-threat-critical/[0.06] px-4 py-1.5">
                <div className="h-1.5 w-1.5 rounded-full bg-threat-critical animate-pulse" />
                <span className="font-body text-xs tracking-wide text-threat-critical/90">
                  THREAT ADVISORY — 824+ malicious skills detected
                </span>
              </div>

              <h1 className="font-display text-5xl leading-[1.1] tracking-tight sm:text-6xl lg:text-7xl">
                Intercept threats
                <br />
                <span className="text-gradient-accent">before impact</span>
              </h1>

              <p className="mt-6 max-w-lg text-lg leading-relaxed text-ink-muted">
                6-pass deep analysis catches what VirusTotal misses — prompt injection,
                credential theft, supply chain attacks, and social engineering
                hidden in OpenClaw skills.
              </p>

              <div className="mt-10 flex flex-wrap items-center gap-4">
                <a
                  href="/dashboard"
                  className="group relative inline-flex items-center gap-2 rounded-lg bg-accent px-6 py-3 font-semibold text-surface-0 hover:bg-accent-dim transition-all duration-300 glow-accent"
                >
                  Start scanning free
                  <ArrowRight
                    size={16}
                    className="transition-transform group-hover:translate-x-1"
                  />
                </a>
                <div className="flex items-center gap-3 rounded-lg border border-[var(--border)] bg-surface-1 px-4 py-3">
                  <span className="font-body text-xs text-ink-faint">$</span>
                  <code className="font-body text-sm text-ink-muted">
                    npx clawvet scan ./my-skill
                  </code>
                </div>
              </div>
            </div>

            {/* Right: Radar */}
            <div className="hidden lg:block opacity-0 animate-fade-in stagger-3">
              <RadarGraphic />
            </div>
          </div>
        </div>
      </section>

      {/* Stats ribbon */}
      <section className="relative border-y border-[var(--border)] bg-surface-1/50 backdrop-blur">
        <div className="mx-auto max-w-5xl px-6">
          <div className="grid grid-cols-4 divide-x divide-[var(--border)]">
            {[
              { value: "10,700+", label: "Skills on ClawHub", accent: false },
              { value: "824", label: "Threats intercepted", accent: true },
              { value: "6", label: "Analysis passes", accent: false },
              { value: "<2s", label: "Avg scan time", accent: false },
            ].map((stat, i) => (
              <div
                key={stat.label}
                className={`py-8 text-center opacity-0 animate-slide-up stagger-${i + 1}`}
              >
                <div
                  className={`font-body text-2xl font-bold tracking-tight ${stat.accent ? "text-accent" : "text-ink"}`}
                >
                  {stat.value}
                </div>
                <div className="mt-1 font-body text-xs tracking-wider uppercase text-ink-faint">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features — 6 Pass Analysis */}
      <section className="relative py-28">
        <div className="absolute top-0 right-0 w-[400px] h-[400px] bg-accent/[0.02] rounded-full blur-[100px]" />

        <div className="mx-auto max-w-7xl px-6">
          <div className="mb-16 max-w-2xl">
            <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-surface-2 px-3 py-1">
              <Lock size={12} className="text-accent" />
              <span className="font-body text-xs tracking-wider uppercase text-ink-muted">
                How it works
              </span>
            </div>
            <h2 className="font-display text-4xl tracking-tight">
              Six layers of defense,
              <br />
              <span className="text-ink-muted">zero blind spots.</span>
            </h2>
            <p className="mt-4 text-ink-muted leading-relaxed">
              Every skill passes through six independent analysis engines.
              Each layer catches threats the others miss.
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, i) => (
              <div
                key={feature.title}
                className={`group card-hover rounded-xl border border-[var(--border)] bg-surface-1 p-6 opacity-0 animate-slide-up stagger-${i + 1}`}
              >
                <div className="mb-4 flex items-center justify-between">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent/[0.06] border border-accent/10 text-accent group-hover:bg-accent/10 transition">
                    {feature.icon}
                  </div>
                  <span className="font-body text-[10px] tracking-[0.25em] text-ink-faint uppercase">
                    {feature.tag}
                  </span>
                </div>
                <h3 className="text-base font-semibold tracking-tight">
                  {feature.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-ink-muted">
                  {feature.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Demo / CTA section */}
      <section className="border-y border-[var(--border)] bg-surface-1/30">
        <div className="mx-auto max-w-7xl px-6 py-28">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            {/* Terminal mockup */}
            <div className="rounded-xl border border-[var(--border)] bg-surface-0 overflow-hidden">
              <div className="flex items-center gap-2 border-b border-[var(--border)] px-4 py-3">
                <div className="h-3 w-3 rounded-full bg-threat-critical/60" />
                <div className="h-3 w-3 rounded-full bg-threat-medium/60" />
                <div className="h-3 w-3 rounded-full bg-threat-safe/60" />
                <span className="ml-2 font-body text-xs text-ink-faint">
                  terminal — clawvet
                </span>
              </div>
              <div className="p-5 font-body text-sm leading-loose">
                <div className="text-ink-faint">
                  <span className="text-accent">$</span> clawvet scan
                  ./suspicious-skill
                </div>
                <div className="mt-3 text-ink-faint">
                  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                </div>
                <div className="text-ink">
                  {"  "}Skill:{" "}
                  <span className="text-ink font-semibold">
                    productivity-boost
                  </span>
                </div>
                <div>
                  {"  "}Risk Score:{" "}
                  <span className="text-threat-critical font-bold">
                    100/100
                  </span>{" "}
                  Grade:{" "}
                  <span className="text-threat-critical font-bold">F</span>
                </div>
                <div className="mt-2" />
                <div>
                  {"  "}
                  <span className="rounded bg-threat-critical/20 px-1.5 py-0.5 text-threat-critical text-xs">
                    CRITICAL
                  </span>{" "}
                  Curl piped to shell
                </div>
                <div className="text-ink-faint text-xs pl-4">
                  curl -sL https://...setup.sh | bash
                </div>
                <div className="mt-1">
                  {"  "}
                  <span className="rounded bg-threat-high/20 px-1.5 py-0.5 text-threat-high text-xs">
                    HIGH
                  </span>{" "}
                  Known malicious IP
                </div>
                <div className="text-ink-faint text-xs pl-4">
                  91.92.242.15
                </div>
                <div className="mt-1">
                  {"  "}
                  <span className="rounded bg-threat-high/20 px-1.5 py-0.5 text-threat-high text-xs">
                    HIGH
                  </span>{" "}
                  API key exfiltration
                </div>
                <div className="text-ink-faint text-xs pl-4">
                  ANTHROPIC_API_KEY → webhook.site
                </div>
                <div className="mt-3 text-ink-faint">
                  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                </div>
                <div>
                  {"  "}Recommendation:{" "}
                  <span className="rounded bg-threat-critical/20 px-2 py-0.5 text-threat-critical font-bold text-xs">
                    BLOCK
                  </span>
                </div>
              </div>
            </div>

            {/* Copy */}
            <div>
              <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-surface-2 px-3 py-1">
                <Terminal size={12} className="text-accent" />
                <span className="font-body text-xs tracking-wider uppercase text-ink-muted">
                  CLI + Web + API
                </span>
              </div>
              <h2 className="font-display text-4xl tracking-tight">
                Your workflow,
                <br />
                <span className="text-ink-muted">your rules.</span>
              </h2>
              <p className="mt-4 text-ink-muted leading-relaxed">
                Scan from the terminal, automate in CI/CD, or use the web dashboard.
                ClawVet meets you where you work.
              </p>
              <ul className="mt-8 space-y-4">
                {[
                  "Scan local skills or fetch directly from ClawHub",
                  "JSON output for CI/CD with configurable fail thresholds",
                  "Real-time watch mode blocks risky installs automatically",
                  "Webhook alerts for critical findings",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-3 text-sm">
                    <div className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-accent/10 border border-accent/20">
                      <Check size={12} className="text-accent" />
                    </div>
                    <span className="text-ink-muted">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-28">
        <div className="mx-auto max-w-7xl px-6">
          <div className="mb-16 text-center">
            <h2 className="font-display text-4xl tracking-tight">
              Simple, transparent pricing
            </h2>
            <p className="mt-3 text-ink-muted">
              Start free. Upgrade when you need deeper analysis.
            </p>
          </div>

          <div className="mx-auto grid max-w-5xl gap-6 sm:grid-cols-3">
            {plans.map((plan, i) => (
              <div
                key={plan.name}
                className={`relative rounded-xl border p-8 transition-all duration-300 ${
                  plan.highlight
                    ? "border-accent/30 bg-accent/[0.03] glow-accent"
                    : "border-[var(--border)] bg-surface-1 card-hover"
                }`}
              >
                {plan.highlight && (
                  <div className="absolute -top-3 left-6 rounded-full bg-accent px-3 py-0.5 text-xs font-bold text-surface-0 uppercase tracking-wider">
                    Popular
                  </div>
                )}
                <h3 className="font-body text-sm font-semibold tracking-wider uppercase text-ink-faint">
                  {plan.name}
                </h3>
                <div className="mt-3 flex items-baseline gap-1">
                  <span className="font-display text-4xl">{plan.price}</span>
                  <span className="text-sm text-ink-faint">{plan.period}</span>
                </div>
                <ul className="mt-8 space-y-3">
                  {plan.features.map((f) => (
                    <li
                      key={f}
                      className="flex items-center gap-3 text-sm text-ink-muted"
                    >
                      <Check
                        size={14}
                        className={
                          plan.highlight ? "text-accent" : "text-ink-faint"
                        }
                      />
                      {f}
                    </li>
                  ))}
                </ul>
                <button
                  className={`mt-8 w-full rounded-lg py-2.5 text-sm font-semibold transition-all duration-300 ${
                    plan.highlight
                      ? "bg-accent text-surface-0 hover:bg-accent-dim glow-accent"
                      : "border border-[var(--border)] bg-surface-2 text-ink-muted hover:text-ink hover:border-accent/30"
                  }`}
                >
                  Get started
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[var(--border)] bg-surface-1/30">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6">
          <div className="flex items-center gap-2">
            <Shield size={14} className="text-accent/50" />
            <span className="font-body text-xs tracking-wider text-ink-faint">
              CLAWVET
            </span>
          </div>
          <span className="font-body text-xs text-ink-faint">
            Securing the OpenClaw ecosystem
          </span>
        </div>
      </footer>
    </div>
  );
}
