import '../style.css'

// ============================================================
// ASG Card Owner Portal — Telegram Link Management
// ============================================================

const API_BASE = 'https://api.asgcard.dev'

// ── State ──────────────────────────────────────────────────

interface PortalState {
    walletAddress: string | null
    isConnected: boolean
    telegramLinked: boolean
    telegramUserId: number | null
    linkedAt: string | null
    deepLink: string | null
    deepLinkExpires: string | null
    error: string | null
    loading: boolean
}

const state: PortalState = {
    walletAddress: null,
    isConnected: false,
    telegramLinked: false,
    telegramUserId: null,
    linkedAt: null,
    deepLink: null,
    deepLinkExpires: null,
    error: null,
    loading: false,
}

// ── Render ─────────────────────────────────────────────────

function render(): void {
    const app = document.getElementById('portal-app')!

    app.innerHTML = `
    <div class="min-h-screen">
      <!-- Header -->
      <header class="fixed top-0 left-0 right-0 z-50 bg-asg-black/80 backdrop-blur-lg border-b border-white/[0.04]">
        <div class="max-w-4xl mx-auto px-6 h-16 flex items-center justify-between">
          <a href="/" class="flex items-center gap-2.5">
            <img src="/logo-mark.svg" alt="" class="w-7 h-7" aria-hidden="true" />
            <span class="font-semibold text-[15px] tracking-tight text-white/90">ASG Card</span>
            <span class="text-xs text-white/30 ml-1">/ Portal</span>
          </a>
          ${state.isConnected ? `
            <div class="flex items-center gap-3">
              <span class="text-xs font-mono text-white/40">${truncateWallet(state.walletAddress!)}</span>
              <button id="disconnect-btn" class="text-xs text-red-400/60 hover:text-red-400 transition-colors">Disconnect</button>
            </div>
          ` : ''}
        </div>
      </header>

      <main class="relative z-10 pt-24 pb-16" id="main-content">
        <div class="max-w-2xl mx-auto px-6">
          ${state.error ? renderError() : ''}
          ${!state.isConnected ? renderConnectWallet() : renderDashboard()}
        </div>
      </main>

      <!-- Footer -->
      <footer class="border-t border-white/[0.04] py-8">
        <div class="max-w-4xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div class="flex items-center gap-2">
            <img src="/logo-mark.svg" alt="" class="w-5 h-5" aria-hidden="true" />
            <span class="text-sm text-white/30">ASG Card</span>
          </div>
          <div class="flex items-center gap-6 text-xs text-white/25">
            <span>&copy; 2026 Autonomous Service Group</span>
          </div>
        </div>
      </footer>
    </div>
  `

    attachHandlers()
}

// ── Sections ───────────────────────────────────────────────

function renderConnectWallet(): string {
    return `
    <div class="text-center space-y-8 py-16">
      <div class="space-y-3">
        <h1 class="text-3xl font-bold tracking-tight">Owner Portal</h1>
        <p class="text-white/40 text-base max-w-md mx-auto">
          Connect your Stellar wallet to manage your ASG Card Telegram bot access.
        </p>
      </div>

      <button id="connect-wallet-btn"
        class="btn-primary liquid-btn text-base px-8 py-3.5 ${state.loading ? 'opacity-50 pointer-events-none' : ''}">
        ${state.loading ? 'Connecting...' : '🔐 Connect Wallet'}
      </button>

      <!-- Security Notice -->
      <div class="surface p-6 text-left max-w-md mx-auto">
        <div class="flex items-start gap-3">
          <span class="text-lg">🛡️</span>
          <div class="space-y-2">
            <h3 class="text-sm font-semibold text-white/80">Security Notice</h3>
            <ul class="text-xs text-white/40 space-y-1.5">
              <li>• Your wallet is used only for authentication</li>
              <li>• No funds are transferred during sign-in</li>
              <li>• Card details (PAN/CVV) are never sent via Telegram</li>
              <li>• You can revoke bot access at any time</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  `
}

function renderDashboard(): string {
    return `
    <div class="space-y-8">
      <div class="space-y-2">
        <h1 class="text-2xl font-bold tracking-tight">Telegram Bot Access</h1>
        <p class="text-white/40 text-sm">Manage your ASGAgentBot connection</p>
      </div>

      <!-- Status Card -->
      <div class="surface p-6 space-y-5">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <span class="w-3 h-3 rounded-full ${state.telegramLinked ? 'bg-asg-green animate-pulse' : 'bg-white/20'}"></span>
            <span class="text-sm font-medium text-white/80">
              ${state.telegramLinked ? 'Connected' : 'Not Connected'}
            </span>
          </div>
          ${state.telegramLinked ? `
            <span class="text-xs text-white/30 font-mono">
              TG ID: ${state.telegramUserId}
            </span>
          ` : ''}
        </div>

        ${state.telegramLinked ? renderLinkedState() : renderUnlinkedState()}
      </div>

      <!-- Security Info -->
      <div class="surface p-6">
        <h3 class="text-sm font-semibold text-white/80 mb-4">🛡️ Security & Privacy</h3>
        <div class="grid sm:grid-cols-2 gap-4">
          <div class="space-y-1">
            <div class="text-xs font-medium text-white/60">Card Reveal</div>
            <div class="text-xs text-white/35">Secure one-time HTTPS link (60s TTL). PAN/CVV displayed in browser only — never via Telegram.</div>
          </div>
          <div class="space-y-1">
            <div class="text-xs font-medium text-white/60">Access Revocation</div>
            <div class="text-xs text-white/35">Disconnect immediately revokes bot access. No cached data remains. Re-linking requires new token.</div>
          </div>
          <div class="space-y-1">
            <div class="text-xs font-medium text-white/60">Token Security</div>
            <div class="text-xs text-white/35">Link tokens are single-use, expire in 10 minutes, and stored as SHA-256 hashes.</div>
          </div>
          <div class="space-y-1">
            <div class="text-xs font-medium text-white/60">Audit Trail</div>
            <div class="text-xs text-white/35">All link/revoke/action events are logged for your protection.</div>
          </div>
        </div>
      </div>
    </div>
  `
}

function renderLinkedState(): string {
    const linkedDate = state.linkedAt ? new Date(state.linkedAt).toLocaleDateString('en-US', {
        year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
    }) : 'Unknown'

    return `
    <div class="border-t border-white/[0.06] pt-4 space-y-4">
      <div class="grid grid-cols-2 gap-4 text-sm">
        <div>
          <div class="text-xs text-white/30 mb-1">Status</div>
          <div class="text-asg-green font-medium">Active</div>
        </div>
        <div>
          <div class="text-xs text-white/30 mb-1">Linked Since</div>
          <div class="text-white/70 font-mono text-xs">${linkedDate}</div>
        </div>
      </div>

      <div class="flex flex-col sm:flex-row gap-3 pt-2">
        <button id="revoke-btn"
          class="flex-1 px-4 py-2.5 rounded-lg border border-red-500/20 text-red-400 text-sm font-medium
                 hover:bg-red-500/10 transition-colors ${state.loading ? 'opacity-50 pointer-events-none' : ''}">
          ${state.loading ? 'Revoking...' : '❌ Disconnect Telegram'}
        </button>
      </div>

      <div class="text-xs text-white/25 flex items-center gap-2">
        <span>⚠️</span>
        <span>Disconnecting immediately revokes bot access. You'll need to re-link to use the bot again.</span>
      </div>
    </div>
  `
}

function renderUnlinkedState(): string {
    if (state.deepLink) {
        return `
      <div class="border-t border-white/[0.06] pt-4 space-y-4">
        <div class="surface p-4 text-center space-y-3">
          <div class="text-sm text-white/70">Open this link in Telegram to connect:</div>
          <a href="${state.deepLink}" target="_blank" rel="noopener"
             class="btn-primary liquid-btn inline-flex items-center gap-2 px-6 py-3 text-sm">
            <span>💬</span>
            <span>Open in Telegram</span>
          </a>
          <div class="text-xs text-white/30 font-mono">
            ${state.deepLink}
          </div>
          <div class="text-xs text-white/25">
            ⏱️ Expires: ${state.deepLinkExpires ? new Date(state.deepLinkExpires).toLocaleTimeString() : '10 minutes'}
          </div>
        </div>

        <button id="refresh-status-btn"
          class="w-full px-4 py-2 rounded-lg border border-white/[0.08] text-white/50 text-sm
                 hover:bg-white/[0.04] transition-colors">
          🔄 Check Connection Status
        </button>
      </div>
    `
    }

    return `
    <div class="border-t border-white/[0.06] pt-4 space-y-4">
      <p class="text-sm text-white/40">
        Link your Telegram account to receive card notifications and manage your cards via bot.
      </p>
      <button id="generate-link-btn"
        class="w-full btn-primary liquid-btn px-6 py-3 text-sm ${state.loading ? 'opacity-50 pointer-events-none' : ''}">
        ${state.loading ? 'Generating...' : '🔗 Connect Telegram'}
      </button>
    </div>
  `
}

function renderError(): string {
    return `
    <div class="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/20 flex items-start gap-3">
      <span class="text-red-400 text-sm">⚠️</span>
      <div>
        <div class="text-sm text-red-400">${state.error}</div>
        <button id="dismiss-error" class="text-xs text-red-400/50 hover:text-red-400 mt-1">Dismiss</button>
      </div>
    </div>
  `
}

// ── Event Handlers ─────────────────────────────────────────

function attachHandlers(): void {
    document.getElementById('connect-wallet-btn')?.addEventListener('click', handleConnectWallet)
    document.getElementById('disconnect-btn')?.addEventListener('click', handleDisconnect)
    document.getElementById('generate-link-btn')?.addEventListener('click', handleGenerateLink)
    document.getElementById('revoke-btn')?.addEventListener('click', handleRevoke)
    document.getElementById('refresh-status-btn')?.addEventListener('click', handleRefreshStatus)
    document.getElementById('dismiss-error')?.addEventListener('click', () => {
        state.error = null
        render()
    })
}

// ── Wallet Auth (Ed25519 signature challenge) ──────────────

async function handleConnectWallet(): Promise<void> {
    state.loading = true
    state.error = null
    render()

    try {
        // For MVP: prompt user to enter their wallet address
        // In production: integrate Freighter or Albedo wallet extension
        const walletAddress = prompt('Enter your Stellar wallet address (G...):')
        if (!walletAddress || !walletAddress.startsWith('G')) {
            throw new Error('Invalid wallet address')
        }

        state.walletAddress = walletAddress
        state.isConnected = true

        // Fetch current link status
        await fetchLinkStatus()
    } catch (error) {
        state.error = (error as Error).message
    } finally {
        state.loading = false
        render()
    }
}

function handleDisconnect(): void {
    state.walletAddress = null
    state.isConnected = false
    state.telegramLinked = false
    state.telegramUserId = null
    state.linkedAt = null
    state.deepLink = null
    state.deepLinkExpires = null
    state.error = null
    render()
}

async function handleGenerateLink(): Promise<void> {
    if (!state.walletAddress) return

    state.loading = true
    state.error = null
    render()

    try {
        const resp = await fetch(`${API_BASE}/portal/telegram/link-token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Wallet-Address': state.walletAddress,
                // In production: include Ed25519 signature for wallet auth
            },
        })

        if (!resp.ok) {
            const body = await resp.json().catch(() => ({}))
            throw new Error((body as { error?: string }).error ?? `Request failed (${resp.status})`)
        }

        const data = await resp.json() as { deepLink: string; expiresAt: string }
        state.deepLink = data.deepLink
        state.deepLinkExpires = data.expiresAt
    } catch (error) {
        state.error = (error as Error).message
    } finally {
        state.loading = false
        render()
    }
}

async function handleRevoke(): Promise<void> {
    if (!state.walletAddress) return
    if (!confirm('Are you sure you want to disconnect Telegram? Bot access will be immediately revoked.')) return

    state.loading = true
    state.error = null
    render()

    try {
        const resp = await fetch(`${API_BASE}/portal/telegram/revoke`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Wallet-Address': state.walletAddress,
            },
        })

        if (!resp.ok) {
            const body = await resp.json().catch(() => ({}))
            throw new Error((body as { error?: string }).error ?? `Request failed (${resp.status})`)
        }

        state.telegramLinked = false
        state.telegramUserId = null
        state.linkedAt = null
        state.deepLink = null
    } catch (error) {
        state.error = (error as Error).message
    } finally {
        state.loading = false
        render()
    }
}

async function handleRefreshStatus(): Promise<void> {
    await fetchLinkStatus()
    render()
}

async function fetchLinkStatus(): Promise<void> {
    if (!state.walletAddress) return

    try {
        const resp = await fetch(`${API_BASE}/portal/telegram/status`, {
            headers: {
                'X-Wallet-Address': state.walletAddress,
            },
        })

        if (!resp.ok) return

        const data = await resp.json() as { linked: boolean; telegramUserId?: number; linkedAt?: string }
        state.telegramLinked = data.linked
        state.telegramUserId = data.telegramUserId ?? null
        state.linkedAt = data.linkedAt ?? null

        if (data.linked) {
            state.deepLink = null
            state.deepLinkExpires = null
        }
    } catch {
        // Silent fail for status check
    }
}

// ── Helpers ────────────────────────────────────────────────

function truncateWallet(addr: string): string {
    return addr.substring(0, 6) + '...' + addr.substring(addr.length - 4)
}

// ── Init ───────────────────────────────────────────────────

render()
