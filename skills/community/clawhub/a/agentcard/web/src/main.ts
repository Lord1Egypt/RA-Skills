import './style.css'
import {
  fetchLivePricingData,
  type CreationTierPrice as CreationTier,
  type FundingTierPrice as FundingTier,
} from './lib/pricing'

// ============================================================
// Types
// ============================================================

// ============================================================
// Live Pricing — fetched from GET /pricing on load
// ============================================================

let creationTiers: CreationTier[] = []
let fundingTiers: FundingTier[] = []
let pricingLoaded = false

async function fetchLivePricing(): Promise<void> {
  const livePricingData = await fetchLivePricingData()
  if (!livePricingData) return

  creationTiers = livePricingData.creationTiers
  fundingTiers = livePricingData.fundingTiers
  pricingLoaded = true
}

// ============================================================
// Data
// ============================================================

const FEATURES = [
  {
    icon: '⚡',
    title: 'Sub-Second Issuance',
    description: 'Card details returned in the same HTTP response. No polling, no webhooks, no waiting.',
  },
  {
    icon: '🔐',
    title: 'x402 Protocol Native',
    description: 'Built on the HTTP 402 standard. Agents pay at the protocol layer — no middleware, no wrappers.',
  },
  {
    icon: '🤖',
    title: 'Agent-First API',
    description: 'Designed for autonomous agents. No human-in-the-loop. Deterministic, stateless, fast.',
  },
]

const STEPS = [
  { num: 1, title: 'Send a Request', desc: 'Your agent hits the create endpoint. No auth headers, no API key, no pre-registration needed.', hint: 'POST /cards/create/tier/:amount' },
  { num: 2, title: 'Pay with USDC', desc: 'The server responds 402 with payment details on chain. Your x402 client auto-pays the exact USDC amount.', hint: '402 → X-Payment → retry' },
  { num: 3, title: 'Receive Card Details', desc: 'Card number, CVV, expiry, and billing address returned instantly in the response body.', hint: '201 { cardNumber, cvv, expiry }' },
  { num: 4, title: 'Start Spending', desc: 'Fund more, freeze, unfreeze — all via simple wallet-signed API calls. Full lifecycle control.', hint: '/cards/:cardId/freeze · /cards/:cardId/unfreeze' },
]

// ============================================================
// Helpers
// ============================================================

function fmtUsd(n: number): string {
  return '$' + n.toFixed(2)
}

function loadingRow(cols: number): string {
  return `<tr><td colspan="${cols}" class="text-center py-8 text-white/30 text-sm">Loading from <code class="text-asg-purple/60 font-mono text-xs">GET /pricing</code>\u2026</td></tr>`
}

function unavailableRow(cols: number): string {
  return `<tr><td colspan="${cols}" class="text-center py-8 text-white/35 text-sm">Pricing is temporarily unavailable. Please refresh in a few seconds.</td></tr>`
}

// ============================================================
// Render helpers
// ============================================================

function renderFeatureCard(f: typeof FEATURES[number]): string {
  return `
    <div class="surface p-8 text-center">
      <div class="text-2xl mb-4">${f.icon}</div>
      <h3 class="text-lg font-semibold tracking-tight mb-2">${f.title}</h3>
      <p class="text-sm text-white/50 leading-relaxed">${f.description}</p>
    </div>
  `
}

const STEP_ICONS = [
  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" class="hiw-icon"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="M12 18v-6"/><path d="M9 15l3-3 3 3"/></svg>`,
  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" class="hiw-icon"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg>`,
  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" class="hiw-icon"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg>`,
  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" class="hiw-icon"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></svg>`,
]

function renderStep(s: typeof STEPS[number], i: number): string {
  return `
    <div class="hiw-step">
      <div class="hiw-step-icon">${STEP_ICONS[i]}</div>
      <div class="hiw-step-body">
        <span class="hiw-step-num">${s.num}</span>
        <h4 class="hiw-step-title">${s.title}</h4>
        <p class="hiw-step-desc">${s.desc}</p>
      </div>
    </div>
  `
}

function renderCreationRow(t: CreationTier, highlight: boolean): string {
  const cls = highlight ? 'bg-asg-purple/[0.04]' : ''
  return `
    <tr class="${cls} border-b border-white/[0.04]">
      <td class="py-3 pl-4 pr-3 font-mono text-sm text-white/80">${fmtUsd(t.loadAmount)}</td>
      <td class="py-3 px-3 font-mono text-sm text-white/50">${fmtUsd(t.issuanceFee)}</td>
      <td class="py-3 px-3 font-mono text-sm text-white/50">${fmtUsd(t.topUpFee)}</td>
      <td class="py-3 px-3 font-mono text-sm text-white/50">${fmtUsd(t.serviceFee)}</td>
      <td class="py-3 pl-3 pr-4 font-mono text-sm font-semibold text-white/90">${fmtUsd(t.totalCost)}</td>
    </tr>
  `
}

function renderFundingRow(t: FundingTier, highlight: boolean): string {
  const cls = highlight ? 'bg-asg-purple/[0.04]' : ''
  return `
    <tr class="${cls} border-b border-white/[0.04]">
      <td class="py-3 pl-4 pr-3 font-mono text-sm text-white/80">${fmtUsd(t.fundAmount)}</td>
      <td class="py-3 px-3 font-mono text-sm text-white/50">${fmtUsd(t.topUpFee)}</td>
      <td class="py-3 px-3 font-mono text-sm text-white/50">${fmtUsd(t.serviceFee)}</td>
      <td class="py-3 pl-3 pr-4 font-mono text-sm font-semibold text-white/90">${fmtUsd(t.totalCost)}</td>
    </tr>
  `
}

function renderCreationRows(): string {
  if (!creationTiers.length) return loadingRow(5)
  return creationTiers.map((t, i) => renderCreationRow(t, i === 2)).join('')
}

function renderFundingRows(): string {
  if (!fundingTiers.length) return loadingRow(4)
  return fundingTiers.map((t, i) => renderFundingRow(t, i === 2)).join('')
}

// ============================================================
// Render page
// ============================================================

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div class="min-h-screen">

    <!-- ─── Header ─── -->
    <header class="fixed top-0 left-0 right-0 z-50 transition-[background-color,border-color] duration-300 border-b border-transparent" id="header">
      <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <a href="/" class="flex items-center gap-2.5">
          <img src="/logo-mark.svg" alt="" class="w-7 h-7" aria-hidden="true" />
          <span class="font-semibold text-[15px] tracking-tight text-white/90">ASG Card</span>
        </a>

        <nav class="hidden md:flex items-center gap-8" aria-label="Main navigation">
          <a href="#features" class="nav-link">Features</a>
          <a href="#how-it-works" class="nav-link">How it Works</a>
          <a href="#pricing" class="nav-link">Pricing</a>
          <a href="/docs" class="nav-link">Docs</a>
        </nav>

        <div class="flex items-center gap-3">
          <a
            href="https://github.com/ASGCompute/asgcard-public"
            target="_blank"
            rel="noopener noreferrer"
            class="hidden sm:inline-flex items-center justify-center w-10 h-10 rounded-lg text-white/70 hover:text-white transition-colors"
            aria-label="GitHub"
            title="GitHub"
          >
            <svg viewBox="0 0 24 24" fill="currentColor" class="w-[18px] h-[18px]" aria-hidden="true">
              <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
            </svg>
          </a>
          <a
            href="https://x.com/ASGCardx402"
            target="_blank"
            rel="noopener noreferrer"
            class="header-x-logo-link hidden sm:inline-flex items-center justify-center w-10 h-10 rounded-lg text-white/70 hover:text-white transition-colors"
            aria-label="ASG Card on X"
            title="ASG Card on X"
          >
            <svg viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4" aria-hidden="true">
              <path d="M18.901 1.153h3.68l-8.042 9.19L24 22.847h-7.406l-5.8-7.584-6.633 7.584H.48l8.6-9.83L0 1.154h7.594l5.243 6.932 6.064-6.933Zm-1.29 19.494h2.039L6.486 3.24H4.298l13.313 17.407Z" />
            </svg>
          </a>
          <a href="/docs#sdk-quick-start" class="liquid-btn hidden sm:inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg">
            <span>Get Started</span>
          </a>
          <!-- Mobile hamburger -->
          <button id="mobile-menu-btn" class="liquid-btn liquid-btn-icon md:hidden flex flex-col items-center justify-center w-9 h-9 rounded-lg gap-[5px]" aria-label="Toggle mobile menu" aria-expanded="false" aria-controls="mobile-nav">
            <span class="block w-4 h-[1.5px] bg-white/60 rounded-full transition-transform" id="burger-top"></span>
            <span class="block w-4 h-[1.5px] bg-white/60 rounded-full transition-opacity" id="burger-mid"></span>
            <span class="block w-4 h-[1.5px] bg-white/60 rounded-full transition-transform" id="burger-bot"></span>
          </button>
        </div>
      </div>

      <!-- Mobile nav panel -->
      <div id="mobile-nav" class="md:hidden overflow-hidden transition-[max-height,opacity] duration-300 max-h-0 opacity-0 bg-asg-black/95 backdrop-blur-xl border-b border-white/[0.04]">
        <nav class="max-w-6xl mx-auto px-6 py-5 flex flex-col gap-3" aria-label="Mobile navigation">
          <a href="#features" class="mobile-nav-link text-[15px] py-2.5 text-white/50 hover:text-white transition-colors">Features</a>
          <a href="#how-it-works" class="mobile-nav-link text-[15px] py-2.5 text-white/50 hover:text-white transition-colors">How it Works</a>
          <a href="#pricing" class="mobile-nav-link text-[15px] py-2.5 text-white/50 hover:text-white transition-colors">Pricing</a>
          <a href="/docs" class="mobile-nav-link text-[15px] py-2.5 text-white/50 hover:text-white transition-colors">Docs</a>
          <a href="/docs#sdk-quick-start" class="btn-primary liquid-btn text-center text-sm mt-2">Get Started</a>
        </nav>
      </div>
    </header>

    <main class="relative z-10" id="main-content">

      <!-- ═══════════════ HERO ═══════════════ -->
      <section class="min-h-[100dvh] flex items-center pt-16">
        <div class="max-w-6xl mx-auto px-6 w-full grid lg:grid-cols-2 gap-16 lg:gap-20 items-center py-20 lg:py-0">

          <!-- Left: Copy -->
          <div class="space-y-7 animate-slide-up">
            <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-white/[0.04] border border-white/[0.06] text-xs font-medium text-asg-green tracking-wide">
              <span class="w-1.5 h-1.5 rounded-full bg-asg-green"></span>
              Powered by x402 on chain
            </div>

            <h1 class="text-4xl sm:text-5xl lg:text-[3.5rem] font-bold leading-[1.08] tracking-[-0.03em] text-white">
              Virtual Cards<br>for <span class="text-asg-purple">AI Agents.</span>
            </h1>

            <p class="text-base sm:text-lg text-white/45 max-w-lg leading-relaxed">
              Give your AI agent a spending card. Issues virtual debit cards on demand — paid with USDC on chain via x402.
              <span class="text-white/65">Card details in seconds.</span>
            </p>



            <div class="pt-1">
              <a href="/docs" class="peek-eyes-btn w-full sm:w-auto text-center">
                <span class="peek-eyes-btn__eyes" aria-hidden="true">
                  <span class="peek-eyes-btn__eye"><span class="peek-eyes-btn__pupil"></span></span>
                  <span class="peek-eyes-btn__eye"><span class="peek-eyes-btn__pupil"></span></span>
                </span>
                <span class="peek-eyes-btn__cover btn-secondary liquid-btn">
                  <span class="peek-eyes-btn__label">View Docs</span>
                </span>
              </a>
            </div>

            <!-- Easy Install -->
            <div class="hero-install">
              <span class="hero-install-label">Easy Install</span>
              <div class="hero-install-cmd">
                <code id="install-cmd">npm install @asgcard/sdk</code>
                <button class="hero-copy-btn liquid-btn liquid-btn-icon" id="copy-install-btn" aria-label="Copy install command" type="button">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Right: Card Visual -->
          <div class="flex justify-center lg:justify-end animate-slide-up" style="animation-delay: 0.1s">
            <div class="card-3d-wrapper w-full max-w-md">
              <div class="card-3d rounded-2xl">
                <div class="hero-card-frame">
                  <div class="relative w-full aspect-[1.586/1] bg-gradient-to-br from-[#111113] via-[#0e0e10] to-[#09090b] border border-white/[0.08] rounded-2xl shadow-2xl hero-card-shell">
                  <div class="relative z-10 h-full p-7 sm:p-8 flex flex-col justify-between hero-card-content">
                    <!-- Top row -->
                    <div class="flex items-start">
                      <div>
                        <div class="text-[10px] font-medium text-white/20 uppercase tracking-widest mb-1">Virtual Card</div>
                        <div class="text-sm font-semibold text-white/70 tracking-tight">ASG Card</div>
                      </div>
                    </div>
                    <!-- Chip -->
                    <div class="my-auto">
                      <div class="w-11 h-8 rounded-md bg-gradient-to-br from-yellow-600/20 to-yellow-500/5 border border-yellow-500/15"></div>
                    </div>
                    <!-- Bottom row -->
                    <div class="space-y-3">
                      <div class="font-mono text-lg sm:text-xl text-white/60 tracking-[0.15em]">5395 \u2022\u2022\u2022\u2022 \u2022\u2022\u2022\u2022 7890</div>
                      <div class="flex items-center justify-between">
                        <div>
                          <div class="text-[10px] text-white/15 uppercase tracking-wider">Expires</div>
                          <div class="font-mono text-xs text-white/40">12/28</div>
                        </div>
                        <div>
                          <div class="text-[10px] text-white/15 uppercase tracking-wider">CVV</div>
                          <div class="font-mono text-xs text-white/40">\u2022\u2022\u2022</div>
                        </div>
                        <div>
                          <div class="text-[10px] text-white/15 uppercase tracking-wider">Balance</div>
                          <div class="font-mono text-xs text-asg-green/70 font-semibold">$50.00</div>
                        </div>
                        <div class="text-right flex items-center justify-end">
                          <svg width="48" height="30" viewBox="0 0 48 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="18" cy="15" r="12" fill="#EB001B" opacity="0.7"/>
                            <circle cx="30" cy="15" r="12" fill="#F79E1B" opacity="0.7"/>
                            <path d="M24 5.04a12 12 0 0 1 0 19.92 12 12 0 0 1 0-19.92z" fill="#FF5F00" opacity="0.85"/>
                          </svg>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="hero-card-scanfx" aria-hidden="true">
                    <canvas class="hero-card-scanfx-canvas"></canvas>
                    <div class="hero-card-scanfx-zone">
                      <pre class="hero-card-scanfx-code"></pre>
                    </div>
                    <div class="hero-card-scanfx-line"></div>
                    <div class="hero-card-scanfx-glare"></div>
                    <div class="hero-card-scanfx-noise"></div>
                  </div>
                </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════ TRUST BAR ═══════════════ -->
      <section class="border-y border-white/[0.04]">
        <div class="max-w-6xl mx-auto px-6 py-12">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div class="text-center">
              <div class="text-2xl font-bold text-white/80">x402</div>
              <div class="text-[11px] text-white/30 mt-1 uppercase tracking-wider">Protocol</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-white/80">On-chain</div>
              <div class="text-[11px] text-white/30 mt-1 uppercase tracking-wider">Settlement</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-white/80">USDC</div>
              <div class="text-[11px] text-white/30 mt-1 uppercase tracking-wider">Payments</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-white/80">&lt;1s</div>
              <div class="text-[11px] text-white/30 mt-1 uppercase tracking-wider">Issuance</div>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════ FEATURES ═══════════════ -->
      <section id="features" class="py-24 md:py-32">
        <div class="max-w-6xl mx-auto px-6">
          <div class="text-center max-w-xl mx-auto mb-16">
            <span class="section-label">Features</span>
            <h2 class="text-3xl sm:text-4xl font-bold tracking-tight leading-tight">Built for autonomous agents</h2>
            <p class="text-white/40 text-base mt-4">Streamlined card infrastructure. Get started in minutes.</p>
          </div>

          <div class="grid md:grid-cols-3 gap-5">
            ${FEATURES.map(renderFeatureCard).join('')}
          </div>
        </div>
      </section>

      <!-- ═══════════════ HOW IT WORKS ═══════════════ -->
      <section id="how-it-works" class="hiw-section">
        <div class="hiw-container">
          <div class="hiw-header">
            <span class="hiw-label">How it works</span>
            <h2 class="hiw-heading">Get a card in seconds, <span class="hiw-heading-muted">not days.</span></h2>
            <p class="hiw-subheading">From first request to first purchase — we've reduced the entire flow to four deterministic steps.</p>
          </div>
          <div class="hiw-grid">
            ${STEPS.map((s, i) => renderStep(s, i)).join('')}
          </div>
        </div>
      </section>

      <!-- ═══════════════ PRICING ═══════════════ -->
      <section id="pricing" class="py-24 md:py-32 border-t border-white/[0.04]">
        <div class="max-w-6xl mx-auto px-6">
          <div class="text-center max-w-xl mx-auto mb-16">
            <span class="section-label">Pricing</span>
            <h2 class="text-3xl sm:text-4xl font-bold tracking-tight leading-tight">Transparent, tier-based</h2>
            <p class="text-white/40 text-base mt-4">Transparent, usage-based pricing. Pay only for the cards you create.</p>
          </div>

          <div class="grid lg:grid-cols-2 gap-6 max-w-5xl mx-auto">

            <!-- Create Card -->
            <div class="surface p-6 sm:p-8 overflow-x-auto">
              <div class="flex items-center gap-3 mb-1">
                <h3 class="text-lg font-semibold tracking-tight">Create Card</h3>
                <span class="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-asg-purple/10 text-asg-purple border border-asg-purple/20">One-time</span>
              </div>
              <p class="text-white/30 text-sm mb-6">via <code class="text-asg-purple/60 font-mono text-xs">POST /cards/create/tier/:amount</code></p>
              <table class="w-full text-left" id="creation-table">
                <thead>
                  <tr class="border-b border-white/[0.08] text-[11px] text-white/30 uppercase tracking-wider">
                    <th class="pb-3 pl-4 pr-3 font-medium">Load</th>
                    <th class="pb-3 px-3 font-medium">Issuance</th>
                    <th class="pb-3 px-3 font-medium">Top-up</th>
                    <th class="pb-3 px-3 font-medium">Service</th>
                    <th class="pb-3 pl-3 pr-4 font-medium">Total</th>
                  </tr>
                </thead>
                <tbody id="creation-tbody">
                  ${renderCreationRows()}
                </tbody>
              </table>
            </div>

            <!-- Fund Card -->
            <div class="surface p-6 sm:p-8 overflow-x-auto">
              <div class="flex items-center gap-3 mb-1">
                <h3 class="text-lg font-semibold tracking-tight">Fund Card</h3>
                <span class="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-asg-green/10 text-asg-green border border-asg-green/20">Reload</span>
              </div>
              <p class="text-white/30 text-sm mb-6">via <code class="text-asg-green/60 font-mono text-xs">POST /cards/fund/tier/:amount</code></p>
              <table class="w-full text-left" id="funding-table">
                <thead>
                  <tr class="border-b border-white/[0.08] text-[11px] text-white/30 uppercase tracking-wider">
                    <th class="pb-3 pl-4 pr-3 font-medium">Amount</th>
                    <th class="pb-3 px-3 font-medium">Top-up</th>
                    <th class="pb-3 px-3 font-medium">Service</th>
                    <th class="pb-3 pl-3 pr-4 font-medium">Total</th>
                  </tr>
                </thead>
                <tbody id="funding-tbody">
                  ${renderFundingRows()}
                </tbody>
              </table>
            </div>

          </div>


        </div>
      </section>

      <!-- ═══════════════ CTA ═══════════════ -->
      <section class="py-24 md:py-32 border-t border-white/[0.04]">
        <div class="max-w-2xl mx-auto px-6 text-center">
          <h2 class="text-3xl sm:text-4xl font-bold tracking-tight leading-tight mb-5">Ready to give your<br>agent a card?</h2>
          <p class="text-white/40 text-base mb-10 max-w-lg mx-auto">Join developers using ASG Card to pay for SaaS, infrastructure, and services autonomously on-chain.</p>
          <div class="flex flex-col sm:flex-row items-center justify-center gap-3">
            <a href="/docs#sdk-quick-start" class="btn-primary liquid-btn text-base px-8 py-3.5 w-full sm:w-auto">Get Started</a>
            <a href="/docs" class="peek-eyes-btn w-full sm:w-auto">
              <span class="peek-eyes-btn__eyes" aria-hidden="true">
                <span class="peek-eyes-btn__eye"><span class="peek-eyes-btn__pupil"></span></span>
                <span class="peek-eyes-btn__eye"><span class="peek-eyes-btn__pupil"></span></span>
              </span>
              <span class="peek-eyes-btn__cover btn-secondary liquid-btn text-base px-8 py-3.5 w-full sm:w-auto">
                <span class="peek-eyes-btn__label">Read the Docs</span>
              </span>
            </a>
          </div>
        </div>
      </section>

    </main>

    <!-- ─── Footer ─── -->
    <footer class="border-t border-white/[0.04] py-12">
      <div class="max-w-6xl mx-auto px-6">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 mb-10">
          <!-- Product -->
          <div>
            <div class="text-[11px] font-semibold uppercase tracking-wider text-white/30 mb-4">Product</div>
            <div class="flex flex-col gap-2.5">
              <a href="/docs" class="text-sm text-white/50 hover:text-white transition-colors">Docs</a>
              <a href="/docs#pricing" class="text-sm text-white/50 hover:text-white transition-colors">Pricing</a>
              <a href="/docs#sdk-quick-start" class="text-sm text-white/50 hover:text-white transition-colors">SDK</a>
            </div>
          </div>
          <!-- Tools -->
          <div>
            <div class="text-[11px] font-semibold uppercase tracking-wider text-white/30 mb-4">Tools</div>
            <div class="flex flex-col gap-2.5">
              <a href="https://www.npmjs.com/package/@asgcard/sdk" target="_blank" rel="noopener" class="text-sm text-white/50 hover:text-white transition-colors">@asgcard/sdk</a>
              <a href="https://www.npmjs.com/package/@asgcard/mcp-server" target="_blank" rel="noopener" class="text-sm text-white/50 hover:text-white transition-colors">@asgcard/mcp-server</a>
              <a href="https://www.npmjs.com/package/@asgcard/cli" target="_blank" rel="noopener" class="text-sm text-white/50 hover:text-white transition-colors">@asgcard/cli</a>
            </div>
          </div>
          <!-- Community -->
          <div>
            <div class="text-[11px] font-semibold uppercase tracking-wider text-white/30 mb-4">Community</div>
            <div class="flex flex-col gap-2.5">
              <a href="https://github.com/ASGCompute/asgcard-public" target="_blank" rel="noopener" class="text-sm text-white/50 hover:text-white transition-colors">GitHub</a>
              <a href="https://x.com/ASGCardx402" target="_blank" rel="noopener" class="text-sm text-white/50 hover:text-white transition-colors">X (Twitter)</a>
              <a href="https://t.me/ASGCardbot" target="_blank" rel="noopener" class="text-sm text-white/50 hover:text-white transition-colors">Telegram Bot</a>
            </div>
          </div>
          <!-- Resources -->
          <div>
            <div class="text-[11px] font-semibold uppercase tracking-wider text-white/30 mb-4">Resources</div>
            <div class="flex flex-col gap-2.5">
              <a href="/openapi.json" class="text-sm text-white/50 hover:text-white transition-colors">OpenAPI Spec</a>
              <a href="/docs.md" class="text-sm text-white/50 hover:text-white transition-colors">LLM Docs</a>
              <a href="/agent.txt" class="text-sm text-white/50 hover:text-white transition-colors">agent.txt</a>
            </div>
          </div>
        </div>
        <div class="flex flex-col sm:flex-row items-center justify-between gap-4 pt-8 border-t border-white/[0.04]">
          <div class="flex items-center gap-2">
            <img src="/logo-mark.svg" alt="" class="w-5 h-5" aria-hidden="true" />
            <span class="text-sm text-white/30">ASG Card</span>
          </div>
          <div class="text-xs text-white/25">&copy; 2026 Autonomous Service Group</div>
        </div>
      </div>
    </footer>
  </div>
`

// ============================================================
// Interactivity
// ============================================================

// Header: subtle bg on scroll
const header = document.getElementById('header')
window.addEventListener('scroll', () => {
  if (window.scrollY > 20) {
    header?.classList.add('bg-asg-black/80', 'backdrop-blur-lg', 'border-white/[0.04]')
    header?.classList.remove('border-transparent')
  } else {
    header?.classList.remove('bg-asg-black/80', 'backdrop-blur-lg', 'border-white/[0.04]')
    header?.classList.add('border-transparent')
  }
}, { passive: true })

// ── Mobile menu ──
const menuBtn = document.getElementById('mobile-menu-btn')
const mobileNav = document.getElementById('mobile-nav')
const burgerTop = document.getElementById('burger-top')
const burgerMid = document.getElementById('burger-mid')
const burgerBot = document.getElementById('burger-bot')
let menuOpen = false

function setMobileMenu(open: boolean) {
  menuOpen = open
  menuBtn?.setAttribute('aria-expanded', String(open))
  if (open) {
    mobileNav?.classList.remove('max-h-0', 'opacity-0')
    mobileNav?.classList.add('max-h-96', 'opacity-100')
    burgerTop?.style.setProperty('transform', 'translateY(3.25px) rotate(45deg)')
    burgerMid?.style.setProperty('opacity', '0')
    burgerBot?.style.setProperty('transform', 'translateY(-3.25px) rotate(-45deg)')
  } else {
    mobileNav?.classList.remove('max-h-96', 'opacity-100')
    mobileNav?.classList.add('max-h-0', 'opacity-0')
    burgerTop?.style.setProperty('transform', 'none')
    burgerMid?.style.setProperty('opacity', '1')
    burgerBot?.style.setProperty('transform', 'none')
  }
}

menuBtn?.addEventListener('click', () => setMobileMenu(!menuOpen))

mobileNav?.querySelectorAll('.mobile-nav-link').forEach((link) => {
  link.addEventListener('click', () => setMobileMenu(false))
})

// ── Copy install command ──
const copyBtn = document.getElementById('copy-install-btn') as HTMLButtonElement | null
const installCmd = document.getElementById('install-cmd') as HTMLElement | null

copyBtn?.addEventListener('click', () => {
  const text = installCmd?.textContent ?? ''
  navigator.clipboard.writeText(text).then(() => {
    const original = copyBtn.innerHTML
    copyBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="#14F195" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><path d="M20 6L9 17l-5-5"/></svg>'
    setTimeout(() => { copyBtn.innerHTML = original }, 1500)
  })
})

// ── Card hover tilt ──
const card3d = document.querySelector('.card-3d') as HTMLElement | null
const cardWrapper = document.querySelector('.card-3d-wrapper') as HTMLElement | null
const heroCardShell = document.querySelector('.hero-card-shell') as HTMLElement | null

function clamp(n: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, n))
}

type ScanParticle = {
  x: number
  y: number
  vx: number
  vy: number
  r: number
  alpha: number
  life: number
  decay: number
}

type LegacyMediaQueryList = MediaQueryList & {
  addEventListener?: (type: 'change', listener: (this: MediaQueryList, ev: MediaQueryListEvent) => unknown) => void
  addListener?: (listener: (this: MediaQueryList, ev: MediaQueryListEvent) => unknown) => void
  removeEventListener?: (type: 'change', listener: (this: MediaQueryList, ev: MediaQueryListEvent) => unknown) => void
  removeListener?: (listener: (this: MediaQueryList, ev: MediaQueryListEvent) => unknown) => void
}

class HeroCardScanEffect {
  private root: HTMLElement
  private overlay: HTMLElement
  private codeEl: HTMLElement
  private canvas: HTMLCanvasElement
  private ctx: CanvasRenderingContext2D
  private width = 0
  private height = 0
  private dpr = Math.min(window.devicePixelRatio || 1, 2)
  private rafId = 0
  private lastTime = 0
  private progress = 0
  private direction: 1 | -1 = 1
  private speed = 0.28
  private codeLines: string[] = []
  private particles: ScanParticle[] = []
  private codeMutateAccumulator = 0
  private resizeObserver?: ResizeObserver
  private mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
  private onReducedMotionChange = () => this.applyStaticStateIfNeeded()
  private isHovering = false
  private mode: 'off' | 'idle' | 'hover' = 'off'
  private idleCooldown = 1.2
  private readonly idleDelayMin = 4.5
  private readonly idleDelayMax = 8
  private readonly idleScanSpeed = 0.95
  private readonly hoverScanSpeed = 0.42

  private readonly codeChars =
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789(){}[]<>;:,._-+=!@#$%^&*|\\\\/'`~?"

  private readonly codeSnippets = [
    'const scanX = lerp(prevX, nextX, dt)',
    'ctx.globalCompositeOperation = "lighter"',
    'particle.alpha *= 0.98',
    'if (x > width) resetParticle()',
    'requestAnimationFrame(renderFrame)',
    'glow += Math.sin(time * 2.2) * 0.05',
    'clipLeft = clamp(progress, 0, 1)',
    'stream.write(chunk)',
    'verifySignature(payload, nonce)',
    'response.headers.set("X-Payment", proof)',
    'wallet.sign(txEnvelope)',
    'scanner.intensity = target * 0.85',
  ]

  constructor(root: HTMLElement) {
    const overlay = root.querySelector('.hero-card-scanfx') as HTMLElement | null
    const codeEl = root.querySelector('.hero-card-scanfx-code') as HTMLElement | null
    const canvas = root.querySelector('.hero-card-scanfx-canvas') as HTMLCanvasElement | null
    const ctx = canvas?.getContext('2d') ?? null

    if (!overlay || !codeEl || !canvas || !ctx) {
      throw new Error('Hero card scan effect markup is incomplete')
    }

    this.root = root
    this.overlay = overlay
    this.codeEl = codeEl
    this.canvas = canvas
    this.ctx = ctx

    this.setup()
  }

  private setup(): void {
    this.syncSize()
    this.seedCode()
    this.setOverlayProgress(0)
    this.scheduleNextIdleCycle(1.3)
    this.applyStaticStateIfNeeded()

    window.addEventListener('resize', this.handleWindowResize)
    this.root.addEventListener('mouseenter', this.handlePointerEnter)
    this.root.addEventListener('mouseleave', this.handlePointerLeave)

    if ('ResizeObserver' in window) {
      this.resizeObserver = new ResizeObserver(() => {
        this.syncSize()
        this.seedCode()
      })
      this.resizeObserver.observe(this.root)
    }

    const mediaQuery = this.mediaQuery as LegacyMediaQueryList
    if (typeof mediaQuery.addEventListener === 'function') {
      mediaQuery.addEventListener('change', this.onReducedMotionChange)
    } else {
      mediaQuery.addListener?.(this.onReducedMotionChange)
    }

    this.rafId = window.requestAnimationFrame((t) => this.animate(t))
  }

  private handleWindowResize = (): void => {
    this.syncSize()
    this.seedCode()
  }

  private handlePointerEnter = (): void => {
    this.isHovering = true
    if (this.mediaQuery.matches) return
    this.startHoverMode()
  }

  private handlePointerLeave = (): void => {
    this.isHovering = false
    if (this.mediaQuery.matches) return
    if (this.mode === 'hover') {
      this.stopScanMode()
      this.scheduleNextIdleCycle(2.8)
    }
  }

  private syncSize(): void {
    this.width = Math.max(1, Math.round(this.root.clientWidth))
    this.height = Math.max(1, Math.round(this.root.clientHeight))

    this.canvas.width = Math.round(this.width * this.dpr)
    this.canvas.height = Math.round(this.height * this.dpr)
    this.canvas.style.width = `${this.width}px`
    this.canvas.style.height = `${this.height}px`

    this.ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0)
  }

  private randomInt(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min
  }

  private randomFloat(min: number, max: number): number {
    return Math.random() * (max - min) + min
  }

  private makeCodeLine(targetLen: number, idx: number): string {
    const seed = this.codeSnippets[(idx + this.randomInt(0, this.codeSnippets.length - 1)) % this.codeSnippets.length]
    let line = seed
    while (line.length < targetLen + 12) {
      const extra = this.codeSnippets[this.randomInt(0, this.codeSnippets.length - 1)]
      line += (Math.random() < 0.3 ? ' // ' : ' ; ') + extra
    }
    return line.slice(0, targetLen)
  }

  private seedCode(): void {
    const charWidth = 6.1
    const lineHeight = 11
    const cols = Math.max(36, Math.floor((this.width - 18) / charWidth))
    const rows = Math.max(10, Math.floor((this.height - 14) / lineHeight))

    this.codeLines = Array.from({ length: rows }, (_, i) => this.makeCodeLine(cols, i))
    this.codeEl.textContent = this.codeLines.join('\n')
  }

  private mutateCode(): void {
    if (!this.codeLines.length) return
    const mutations = this.randomInt(1, 3)
    for (let i = 0; i < mutations; i++) {
      const rowIndex = this.randomInt(0, this.codeLines.length - 1)
      const line = this.codeLines[rowIndex]
      if (!line) continue
      const chars = line.split('')
      const edits = this.randomInt(2, 8)
      for (let j = 0; j < edits; j++) {
        const colIndex = this.randomInt(0, chars.length - 1)
        if (Math.random() < 0.35 && colIndex < chars.length - 1) {
          chars[colIndex] = ' '
          continue
        }
        chars[colIndex] = this.codeChars[this.randomInt(0, this.codeChars.length - 1)]
      }
      this.codeLines[rowIndex] = chars.join('')
    }
    this.codeEl.textContent = this.codeLines.join('\n')
  }

  private setOverlayProgress(progress: number): void {
    const p = clamp(progress, 0, 1)
    this.root.style.setProperty('--scan-progress', p.toFixed(4))
    this.root.style.setProperty('--scan-direction', this.direction > 0 ? '1' : '-1')
    this.overlay.style.setProperty('--scan-progress', p.toFixed(4))
    this.overlay.style.setProperty('--scan-direction', this.direction > 0 ? '1' : '-1')
  }

  private setVisualActive(active: boolean): void {
    this.root.classList.toggle('is-scanning', active)
  }

  private scheduleNextIdleCycle(delay?: number): void {
    this.idleCooldown = delay ?? this.randomFloat(this.idleDelayMin, this.idleDelayMax)
  }

  private startIdleCycle(): void {
    if (this.mediaQuery.matches || this.isHovering) return
    this.mode = 'idle'
    this.direction = 1
    this.progress = 0
    this.speed = this.idleScanSpeed
    this.setOverlayProgress(this.progress)
    this.setVisualActive(true)
    this.codeMutateAccumulator = 0
    this.mutateCode()
  }

  private startHoverMode(): void {
    this.mode = 'hover'
    this.speed = this.hoverScanSpeed
    if (this.progress <= 0 || this.progress >= 1) {
      this.progress = 0
      this.direction = 1
      this.setOverlayProgress(this.progress)
    }
    this.setVisualActive(true)
  }

  private stopScanMode(): void {
    this.mode = 'off'
    this.progress = 0
    this.direction = 1
    this.setOverlayProgress(this.progress)
    this.setVisualActive(false)
    this.particles.length = 0
    this.ctx.clearRect(0, 0, this.width, this.height)
  }

  private applyStaticStateIfNeeded(): void {
    if (!this.mediaQuery.matches) {
      this.scheduleNextIdleCycle(1.3)
      return
    }
    this.mode = 'off'
    this.isHovering = false
    this.progress = 0
    this.direction = 1
    this.setVisualActive(false)
    this.setOverlayProgress(this.progress)
    this.particles.length = 0
    this.ctx.clearRect(0, 0, this.width, this.height)
  }

  private spawnParticle(scanX: number): void {
    if (this.particles.length > 160) return

    const movingRight = this.direction > 0
    this.particles.push({
      x: scanX + this.randomFloat(-1.5, 1.5),
      y: this.randomFloat(6, this.height - 6),
      vx: this.randomFloat(0.5, 1.9) * (movingRight ? 1 : -1),
      vy: this.randomFloat(-0.35, 0.35),
      r: this.randomFloat(0.8, 2.4),
      alpha: this.randomFloat(0.35, 0.95),
      life: 1,
      decay: this.randomFloat(0.015, 0.045),
    })
  }

  private updateAndDrawParticles(): void {
    this.ctx.clearRect(0, 0, this.width, this.height)
    if (!this.particles.length) return

    this.ctx.globalCompositeOperation = 'lighter'

    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i]
      p.x += p.vx
      p.y += p.vy
      p.life -= p.decay
      p.alpha *= 0.988

      if (p.life <= 0 || p.x < -10 || p.x > this.width + 10 || p.y < -8 || p.y > this.height + 8) {
        this.particles.splice(i, 1)
        continue
      }

      const edgeFadeTop = p.y < 20 ? p.y / 20 : 1
      const edgeFadeBottom = p.y > this.height - 20 ? (this.height - p.y) / 20 : 1
      const alpha = clamp(p.alpha * p.life * edgeFadeTop * edgeFadeBottom, 0, 1)
      if (alpha <= 0.01) continue

      const gradient = this.ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 4)
      gradient.addColorStop(0, `rgba(255,255,255,${alpha})`)
      gradient.addColorStop(0.28, `rgba(216,180,254,${alpha * 0.95})`)
      gradient.addColorStop(0.62, `rgba(153,69,255,${alpha * 0.65})`)
      gradient.addColorStop(0.86, `rgba(110,44,190,${alpha * 0.28})`)
      gradient.addColorStop(1, 'rgba(110,44,190,0)')

      this.ctx.fillStyle = gradient
      this.ctx.beginPath()
      this.ctx.arc(p.x, p.y, p.r * 4, 0, Math.PI * 2)
      this.ctx.fill()
    }

    this.ctx.globalCompositeOperation = 'source-over'
  }

  private animate(time: number): void {
    if (!this.lastTime) this.lastTime = time
    const dt = Math.min(0.04, (time - this.lastTime) / 1000)
    this.lastTime = time

    if (!this.mediaQuery.matches) {
      if (this.mode === 'off') {
        this.idleCooldown -= dt
        if (this.idleCooldown <= 0) {
          this.startIdleCycle()
        }
      } else {
        let effectActive = true
        this.progress += this.direction * this.speed * dt

        if (this.mode === 'hover') {
          if (this.progress >= 1) {
            this.progress = 1
            this.direction = -1
          } else if (this.progress <= 0) {
            this.progress = 0
            this.direction = 1
          }
        } else if (this.mode === 'idle' && this.progress >= 1) {
          this.stopScanMode()
          this.scheduleNextIdleCycle()
          effectActive = false
        }

        if (effectActive) {
          this.setOverlayProgress(this.progress)

          const scanX = this.progress * this.width
          const spawnCount = this.mode === 'hover' ? this.randomInt(3, 7) : this.randomInt(2, 5)
          for (let i = 0; i < spawnCount; i++) this.spawnParticle(scanX)

          this.codeMutateAccumulator += dt
          const mutateInterval = this.mode === 'hover' ? 0.14 : 0.2
          if (this.codeMutateAccumulator >= mutateInterval) {
            this.codeMutateAccumulator = 0
            this.mutateCode()
          }
        }
      }
    }

    this.updateAndDrawParticles()
    this.rafId = window.requestAnimationFrame((t) => this.animate(t))
  }

  destroy(): void {
    window.cancelAnimationFrame(this.rafId)
    this.resizeObserver?.disconnect()
    window.removeEventListener('resize', this.handleWindowResize)
    this.root.removeEventListener('mouseenter', this.handlePointerEnter)
    this.root.removeEventListener('mouseleave', this.handlePointerLeave)
    const mediaQuery = this.mediaQuery as LegacyMediaQueryList
    if (typeof mediaQuery.removeEventListener === 'function') {
      mediaQuery.removeEventListener('change', this.onReducedMotionChange)
    } else {
      mediaQuery.removeListener?.(this.onReducedMotionChange)
    }
  }
}

if (heroCardShell) {
  new HeroCardScanEffect(heroCardShell)
}

cardWrapper?.addEventListener('mousemove', (e: MouseEvent) => {
  if (!card3d) return
  const rect = cardWrapper.getBoundingClientRect()
  const x = (e.clientX - rect.left) / rect.width
  const y = (e.clientY - rect.top) / rect.height
  const rotateX = (0.5 - y) * 16
  const rotateY = (x - 0.5) * 16
  card3d.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`
})

cardWrapper?.addEventListener('mouseleave', () => {
  if (!card3d) return
  card3d.style.transform = 'rotateX(6deg) rotateY(-4deg)'
})

// ── Creepy "peek eyes" for docs buttons ──
function bindPeekEyesButtons(): void {
  const buttons = Array.from(document.querySelectorAll<HTMLElement>('.peek-eyes-btn'))
  if (!buttons.length) return

  const updateEyes = (button: HTMLElement, clientX: number, clientY: number) => {
    const eyes = button.querySelector<HTMLElement>('.peek-eyes-btn__eyes')
    if (!eyes) return

    const rect = eyes.getBoundingClientRect()
    const cx = rect.left + rect.width / 2
    const cy = rect.top + rect.height / 2
    const dx = clientX - cx
    const dy = clientY - cy

    // Normalize and clamp movement so pupils stay inside the whites.
    const nx = clamp(dx / 44, -1, 1)
    const ny = clamp(dy / 28, -1, 1)

    button.style.setProperty('--peek-eye-x', nx.toFixed(3))
    button.style.setProperty('--peek-eye-y', ny.toFixed(3))
  }

  const resetEyes = (button: HTMLElement) => {
    button.style.setProperty('--peek-eye-x', '0')
    button.style.setProperty('--peek-eye-y', '0')
  }

  for (const button of buttons) {
    button.addEventListener('mousemove', (e: MouseEvent) => {
      updateEyes(button, e.clientX, e.clientY)
    })

    button.addEventListener('touchmove', (e: TouchEvent) => {
      const touch = e.touches[0]
      if (!touch) return
      updateEyes(button, touch.clientX, touch.clientY)
    }, { passive: true })

    button.addEventListener('mouseleave', () => resetEyes(button))
    button.addEventListener('blur', () => resetEyes(button))
  }
}

bindPeekEyesButtons()

// ── Fetch live pricing and update tables ──
fetchLivePricing().then(() => {
  const creationTbody = document.getElementById('creation-tbody')
  const fundingTbody = document.getElementById('funding-tbody')

  if (!pricingLoaded) {
    if (creationTbody) creationTbody.innerHTML = unavailableRow(5)
    if (fundingTbody) fundingTbody.innerHTML = unavailableRow(4)
    return
  }

  if (creationTbody) creationTbody.innerHTML = renderCreationRows()
  if (fundingTbody) fundingTbody.innerHTML = renderFundingRows()
})
