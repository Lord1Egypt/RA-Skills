import './docs.css';
import {
  fetchLivePricingData,
  type CreationTierPrice as CreationTier,
  type FundingTierPrice as FundingTier,
} from './lib/pricing';

// ============================================================
// Helpers
// ============================================================

/** Wrap code in a block with optional language header and copy button */
function codeBlock(code: string, lang?: string): string {
  const id = 'cb-' + Math.random().toString(36).slice(2, 9);
  const header = lang
    ? `<div class="docs-code-header">
        <span>${lang}</span>
        <button class="docs-copy-btn" data-copy-target="${id}" aria-label="Copy code">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
          <span class="copy-label">Copy</span>
        </button>
       </div>`
    : '';
  return `<div class="docs-code-block">
    ${header}
    <pre id="${id}"><code>${escapeHtml(code.trim())}</code></pre>
  </div>`;
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function fmtUsd(n: number): string {
  return `$${n.toFixed(2)}`;
}

// ============================================================
// Sidebar nav items
// ============================================================
interface NavItem {
  id: string;
  label: string;
  children?: { id: string; label: string }[];
}

const NAV: NavItem[] = [
  { id: 'introduction', label: 'Introduction' },
  { id: 'overview', label: 'Overview' },
  {
    id: 'sdk', label: 'SDK', children: [
      { id: 'sdk-install', label: 'Install' },
      { id: 'sdk-quick-start', label: 'Quick Start' },
      { id: 'sdk-configuration', label: 'Configuration' },
      { id: 'sdk-methods', label: 'Methods' },
      { id: 'sdk-error-handling', label: 'Error Handling' },
      { id: 'sdk-low-level', label: 'Low-Level Utilities' },
      { id: 'sdk-how-it-works', label: 'How It Works' },
    ]
  },
  {
    id: 'mcp-server', label: 'MCP Server', children: [
      { id: 'mcp-install', label: 'Setup' },
      { id: 'mcp-tools', label: 'Tools' },
    ]
  },
  {
    id: 'agent-skill', label: 'Agent Skill (x402)'
  },
  {
    id: 'cli', label: 'CLI', children: [
      { id: 'cli-install', label: 'Install' },
      { id: 'cli-commands', label: 'Commands' },
    ]
  },
  {
    id: 'authentication', label: 'Authentication', children: [
      { id: 'x402-payment-flow', label: 'x402 Payment Flow' },
      { id: 'wallet-signature', label: 'Wallet Signature' },
    ]
  },
  {
    id: 'pricing', label: 'Pricing', children: [
      { id: 'card-creation', label: 'Card Creation' },
      { id: 'card-funding', label: 'Card Funding' },
    ]
  },
  {
    id: 'endpoints', label: 'Endpoints', children: [
      { id: 'public-endpoints', label: 'Public' },
      { id: 'paid-endpoints', label: 'Paid (x402)' },
      { id: 'wallet-signed-endpoints', label: 'Wallet-Signed' },
    ]
  },
  {
    id: 'agent-first', label: 'Agent-First Details', children: [
      { id: 'details-envelope', label: 'Details Envelope' },
      { id: 'get-card-details', label: 'GET /cards/:cardId/details' },
      { id: 'nonce-replay', label: 'Nonce & Anti-Replay' },
      { id: 'revoke-restore', label: 'Revoke / Restore' },
    ]
  },
  { id: 'errors', label: 'Errors' },
  { id: 'rate-limits', label: 'Rate Limits' },
  { id: 'architecture', label: 'Architecture' },
];

// ============================================================
// Pricing data — source of truth synced with api/src/config/pricing.ts
// ============================================================
// Live pricing state — populated from GET /pricing on load.
let creationTiers: CreationTier[] = [];
let fundingTiers: FundingTier[] = [];
let pricingLoaded = false;

async function fetchLivePricing(): Promise<void> {
  const livePricingData = await fetchLivePricingData();
  if (!livePricingData) return;

  creationTiers = livePricingData.creationTiers;
  fundingTiers = livePricingData.fundingTiers;
  pricingLoaded = true;
}

// ============================================================
// Render sidebar
// ============================================================
function renderSidebar(): string {
  const links = NAV.map(item => {
    let html = `<a href="#${item.id}" class="docs-sidebar-link" data-section="${item.id}">${item.label}</a>`;
    if (item.children) {
      html += item.children.map(c =>
        `<a href="#${c.id}" class="docs-sidebar-link" data-section="${c.id}" style="padding-left:2.25rem;font-size:12px;">${c.label}</a>`
      ).join('');
    }
    return html;
  }).join('');

  return `
    <aside class="docs-sidebar" id="sidebar" role="navigation" aria-label="Documentation navigation">
      <a href="/" class="docs-sidebar-brand">
        <img src="/logo-mark.svg" alt="" class="docs-sidebar-brand-icon" aria-hidden="true" />
        <span class="docs-sidebar-brand-text">ASG Card</span>
      </a>
      <nav class="docs-sidebar-nav">
        <div class="docs-sidebar-group-label">Documentation</div>
        ${links}
      </nav>
    </aside>
  `;
}

// ============================================================
// Section renderers
// ============================================================
function renderIntroduction(): string {
  return `
    <section id="introduction" aria-label="Introduction">
      <div class="docs-hero">
        <h1>ASG Card Documentation</h1>
        <p>x402-powered virtual card issuance for AI agents on Stellar. Pay with USDC, get a card in seconds.</p>
      </div>

      <div style="display:flex;align-items:center;gap:0.75rem;padding:0.75rem 1rem;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:8px;margin-bottom:1rem;">
        <span style="font-size:11px;font-weight:500;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.06em;">Base URL</span>
        <code style="background:none;border:none;padding:0;color:#14F195;font-size:13px;">https://api.asgcard.dev</code>
      </div>
    </section>
  `;
}

function renderOverview(): string {
  return `
    <section id="overview" aria-label="Overview">
      <h2>Overview</h2>
      <p>ASG Card exposes a REST API with five classes of endpoints:</p>
      <div class="docs-table-wrap">
        <table class="docs-table">
          <thead>
            <tr><th>Type</th><th>Auth</th><th>Description</th></tr>
          </thead>
          <tbody>
            <tr>
              <td data-label="Type"><span class="docs-badge docs-badge-get">Public</span></td>
              <td data-label="Auth">None</td>
              <td data-label="Description">Health check, pricing, tiers</td>
            </tr>
            <tr>
              <td data-label="Type"><span class="docs-badge docs-badge-post">Paid (x402)</span></td>
              <td data-label="Auth">USDC payment on Stellar via x402</td>
              <td data-label="Description">Create/fund cards</td>
            </tr>
            <tr>
              <td data-label="Type"><span class="docs-badge docs-badge-put">Wallet-signed</span></td>
              <td data-label="Auth">Ed25519 signature</td>
              <td data-label="Description">Card management</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  `;
}

function renderSDK(): string {
  return `
    <section id="sdk" aria-label="SDK">
      <h2>SDK</h2>
      <p>The official client SDK wraps the raw x402 flow (402 → parse challenge → pay USDC → retry with proof) into one-liner methods. No need to handle the payment handshake yourself.</p>

      <h3 id="sdk-install">Install</h3>
      ${codeBlock('npm install @asgcard/sdk', 'bash')}

      <hr class="docs-divider" />

      <h3 id="sdk-quick-start">Quick Start</h3>
      ${codeBlock(`import { ASGCardClient } from '@asgcard/sdk';

const client = new ASGCardClient({
  privateKey: '<stellar_secret_seed>',
  baseUrl: 'https://api.asgcard.dev',
  rpcUrl: 'https://mainnet.sorobanrpc.com',
});

// One line — SDK handles payment automatically
const card = await client.createCard({
  amount: 10,       // $10 tier
  nameOnCard: 'AI AGENT',
  email: 'agent@example.com',
});

console.log(card.details); // { cardNumber, cvv, expiry, \u2026 }`, 'typescript')}

      <hr class="docs-divider" />

      <h3 id="sdk-configuration">Configuration</h3>
      <div class="docs-table-wrap">
        <table class="docs-table">
          <thead>
            <tr><th>Parameter</th><th>Type</th><th>Required</th><th>Default</th><th>Description</th></tr>
          </thead>
          <tbody>
            <tr>
              <td data-label="Parameter"><code>privateKey</code></td>
              <td data-label="Type"><code>string</code></td>
              <td data-label="Required">One of two</td>
              <td data-label="Default">—</td>
              <td data-label="Description">Stellar secret seed (for signing)</td>
            </tr>
            <tr>
              <td data-label="Parameter"><code>walletAdapter</code></td>
              <td data-label="Type"><code>WalletAdapter</code></td>
              <td data-label="Required">One of two</td>
              <td data-label="Default">—</td>
              <td data-label="Description">Stellar wallet adapter (<code>publicKey</code> + <code>signTransaction</code>)</td>
            </tr>
            <tr>
              <td data-label="Parameter"><code>baseUrl</code></td>
              <td data-label="Type"><code>string</code></td>
              <td data-label="Required">No</td>
              <td data-label="Default"><code>https://api.asgcard.dev</code></td>
              <td data-label="Description">API base URL</td>
            </tr>
            <tr>
              <td data-label="Parameter"><code>rpcUrl</code></td>
              <td data-label="Type"><code>string</code></td>
              <td data-label="Required">No</td>
              <td data-label="Default"><code>https://horizon.stellar.org</code></td>
              <td data-label="Description">Stellar Horizon or RPC endpoint</td>
            </tr>
            <tr>
              <td data-label="Parameter"><code>timeout</code></td>
              <td data-label="Type"><code>number</code></td>
              <td data-label="Required">No</td>
              <td data-label="Default"><code>60000</code></td>
              <td data-label="Description">Request timeout in milliseconds</td>
            </tr>
          </tbody>
        </table>
      </div>

      <hr class="docs-divider" />

      <h3 id="sdk-methods">Methods</h3>

      <h4 class="docs-method-sig"><code>client.createCard(params): Promise&lt;CardResult&gt;</code></h4>
      <p>Create a virtual card. Pays USDC automatically.</p>
      <div class="docs-table-wrap">
        <table class="docs-table">
          <thead>
            <tr><th>Field</th><th>Type</th><th>Values</th></tr>
          </thead>
          <tbody>
            <tr><td data-label="Field"><code>amount</code></td><td data-label="Type"><code>number</code></td><td data-label="Values"><code>10 | 25 | 50 | 100 | 200 | 500</code></td></tr>
            <tr><td data-label="Field"><code>nameOnCard</code></td><td data-label="Type"><code>string</code></td><td data-label="Values">Name embossed on card</td></tr>
            <tr><td data-label="Field"><code>email</code></td><td data-label="Type"><code>string</code></td><td data-label="Values">Delivery email</td></tr>
          </tbody>
        </table>
      </div>
      ${codeBlock(`const result = await client.createCard({
  amount: 50,
  nameOnCard: 'AI AGENT',
  email: 'agent@example.com',
});`, 'typescript')}

      <h4 class="docs-method-sig"><code>client.fundCard(params): Promise&lt;FundResult&gt;</code></h4>
      <p>Fund an existing card.</p>
      <div class="docs-table-wrap">
        <table class="docs-table">
          <thead>
            <tr><th>Field</th><th>Type</th><th>Values</th></tr>
          </thead>
          <tbody>
            <tr><td data-label="Field"><code>amount</code></td><td data-label="Type"><code>number</code></td><td data-label="Values"><code>10 | 25 | 50 | 100 | 200 | 500</code></td></tr>
            <tr><td data-label="Field"><code>cardId</code></td><td data-label="Type"><code>string</code></td><td data-label="Values">UUID of existing card</td></tr>
          </tbody>
        </table>
      </div>
      ${codeBlock(`const result = await client.fundCard({
  amount: 25,
  cardId: 'card-uuid',
});`, 'typescript')}

      <h4 class="docs-method-sig"><code>client.getTiers(): Promise&lt;TierResponse&gt;</code></h4>
      <p>Get pricing tiers and fee breakdown (no payment required).</p>

      <h4 class="docs-method-sig"><code>client.health(): Promise&lt;HealthResponse&gt;</code></h4>
      <p>Check if the ASG Card API is reachable.</p>

      <h4 class="docs-method-sig"><code>client.address: string</code></h4>
      <p>The Stellar wallet address being used for payments.</p>

      <hr class="docs-divider" />

      <h3 id="sdk-error-handling">Error Handling</h3>
      ${codeBlock(`import {
  ASGCardClient,
  InsufficientBalanceError,
  PaymentError,
  ApiError,
  TimeoutError,
} from '@asgcard/sdk';

try {
  const card = await client.createCard({ amount: 50, nameOnCard: 'AI', email: 'a@b.com' });
} catch (error) {
  if (error instanceof InsufficientBalanceError) {
    console.log(\`Need \${error.required}, have \${error.available}\`);
  } else if (error instanceof PaymentError) {
    console.log(\`Payment failed: \${error.message}, tx: \${error.txHash}\`);
  } else if (error instanceof ApiError) {
    console.log(\`Server error \${error.status}:\`, error.body);
  } else if (error instanceof TimeoutError) {
    console.log('Request timed out');
  }
}`, 'typescript')}

      <div class="docs-table-wrap">
        <table class="docs-table">
          <thead>
            <tr><th>Class</th><th>Fields</th><th>When</th></tr>
          </thead>
          <tbody>
            <tr><td data-label="Class"><code>InsufficientBalanceError</code></td><td data-label="Fields"><code>required</code>, <code>available</code></td><td data-label="When">USDC balance &lt; required</td></tr>
            <tr><td data-label="Class"><code>PaymentError</code></td><td data-label="Fields"><code>message</code>, <code>txHash?</code></td><td data-label="When">Stellar tx failed</td></tr>
            <tr><td data-label="Class"><code>ApiError</code></td><td data-label="Fields"><code>status</code>, <code>body</code></td><td data-label="When">Server returned non-2xx</td></tr>
            <tr><td data-label="Class"><code>TimeoutError</code></td><td data-label="Fields"><code>message</code></td><td data-label="When">Request exceeded timeout</td></tr>
          </tbody>
        </table>
      </div>

      <hr class="docs-divider" />

      <h3 id="sdk-low-level">Low-Level x402 Utilities</h3>
      <p>For full control over the payment flow:</p>
      ${codeBlock(`import {
  parseChallenge,
  checkBalance,
  executePayment,
  buildPaymentPayload,
  buildPaymentTransaction,
  handleX402Payment,
} from '@asgcard/sdk';`, 'typescript')}

      <div class="docs-table-wrap">
        <table class="docs-table">
          <thead>
            <tr><th>Function</th><th>Signature</th><th>Description</th></tr>
          </thead>
          <tbody>
            <tr>
              <td data-label="Function"><code>parseChallenge</code></td>
              <td data-label="Signature"><code>(input: unknown) → X402Accept</code></td>
              <td data-label="Description">Parse 402 challenge, returns first accepted method</td>
            </tr>
            <tr>
              <td data-label="Function"><code>checkBalance</code></td>
              <td data-label="Signature"><code>(params) → Promise&lt;void&gt;</code></td>
              <td data-label="Description">Throws <code>InsufficientBalanceError</code> if USDC &lt; required</td>
            </tr>
            <tr>
              <td data-label="Function"><code>executePayment</code></td>
              <td data-label="Signature"><code>(params) → Promise&lt;string&gt;</code></td>
              <td data-label="Description">Sends USDC on Stellar, returns txHash</td>
            </tr>
            <tr>
              <td data-label="Function"><code>buildPaymentPayload</code></td>
              <td data-label="Signature"><code>(accepted, signedXDR) → string</code></td>
              <td data-label="Description">Builds base64-encoded X-PAYMENT header value</td>
            </tr>
            <tr>
              <td data-label="Function"><code>buildPaymentTransaction</code></td>
              <td data-label="Signature"><code>(params) → Promise&lt;string&gt;</code></td>
              <td data-label="Description">Build + sign a Soroban SAC USDC transfer</td>
            </tr>
            <tr>
              <td data-label="Function"><code>handleX402Payment</code></td>
              <td data-label="Signature"><code>(params) → Promise&lt;string&gt;</code></td>
              <td data-label="Description">Full cycle: parse → pay → build proof</td>
            </tr>
          </tbody>
        </table>
      </div>

      <hr class="docs-divider" />

      <h3 id="sdk-how-it-works">How It Works</h3>
      <p>Sequence diagram showing the SDK flow:</p>
      <div class="docs-diagram" role="img" aria-label="SDK payment sequence: Your Code calls createCard on SDK, SDK sends POST to ASG API, receives 402, pays USDC on Stellar, retries with X-Payment header, receives 201 with card details.">
        <svg viewBox="0 0 720 340" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
          <!-- Lifelines -->
          <text x="80" y="24" fill="#fafafa" font-family="Inter,system-ui,sans-serif" font-size="12" font-weight="600" text-anchor="middle">Your Code</text>
          <text x="260" y="24" fill="#fafafa" font-family="Inter,system-ui,sans-serif" font-size="12" font-weight="600" text-anchor="middle">SDK</text>
          <text x="460" y="24" fill="#fafafa" font-family="Inter,system-ui,sans-serif" font-size="12" font-weight="600" text-anchor="middle">ASG API</text>
          <text x="640" y="24" fill="#fafafa" font-family="Inter,system-ui,sans-serif" font-size="12" font-weight="600" text-anchor="middle">Stellar</text>
          <!-- Vertical lines -->
          <line x1="80" y1="34" x2="80" y2="320" stroke="rgba(255,255,255,0.1)" stroke-width="1" stroke-dasharray="4 4"/>
          <line x1="260" y1="34" x2="260" y2="320" stroke="rgba(255,255,255,0.1)" stroke-width="1" stroke-dasharray="4 4"/>
          <line x1="460" y1="34" x2="460" y2="320" stroke="rgba(255,255,255,0.1)" stroke-width="1" stroke-dasharray="4 4"/>
          <line x1="640" y1="34" x2="640" y2="320" stroke="rgba(255,255,255,0.1)" stroke-width="1" stroke-dasharray="4 4"/>
          <!-- 1: createCard -->
          <line x1="80" y1="60" x2="256" y2="60" stroke="#14F195" stroke-width="1.5"/>
          <polygon points="256,56 256,64 264,60" fill="#14F195"/>
          <text x="168" y="54" fill="rgba(255,255,255,0.55)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">createCard()</text>
          <!-- 2: POST -->
          <line x1="260" y1="90" x2="456" y2="90" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
          <polygon points="456,86 456,94 464,90" fill="rgba(255,255,255,0.3)"/>
          <text x="358" y="84" fill="rgba(255,255,255,0.55)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">POST /cards/create</text>
          <!-- 3: 402 -->
          <line x1="460" y1="120" x2="264" y2="120" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="6 3"/>
          <polygon points="264,116 264,124 256,120" fill="#f59e0b"/>
          <text x="358" y="114" fill="#f59e0b" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">402 + challenge</text>
          <!-- 4: USDC transfer -->
          <line x1="260" y1="160" x2="636" y2="160" stroke="#14F195" stroke-width="1.5"/>
          <polygon points="636,156 636,164 644,160" fill="#14F195"/>
          <text x="450" y="154" fill="rgba(255,255,255,0.55)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">USDC transfer</text>
          <!-- 5: txHash -->
          <line x1="640" y1="190" x2="264" y2="190" stroke="rgba(255,255,255,0.3)" stroke-width="1.5" stroke-dasharray="6 3"/>
          <polygon points="264,186 264,194 256,190" fill="rgba(255,255,255,0.3)"/>
          <text x="450" y="184" fill="rgba(255,255,255,0.55)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">txHash</text>
          <!-- 6: POST + X-Payment -->
          <line x1="260" y1="230" x2="456" y2="230" stroke="#14F195" stroke-width="1.5"/>
          <polygon points="456,226 456,234 464,230" fill="#14F195"/>
          <text x="358" y="224" fill="rgba(255,255,255,0.55)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">POST + X-Payment</text>
          <!-- 7: 201 + card -->
          <line x1="460" y1="260" x2="264" y2="260" stroke="#14F195" stroke-width="1.5" stroke-dasharray="6 3"/>
          <polygon points="264,256 264,264 256,260" fill="#14F195"/>
          <text x="358" y="254" fill="#14F195" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">201 + card details</text>
          <!-- 8: CardResult -->
          <line x1="260" y1="290" x2="84" y2="290" stroke="#14F195" stroke-width="1.5" stroke-dasharray="6 3"/>
          <polygon points="84,286 84,294 76,290" fill="#14F195"/>
          <text x="168" y="284" fill="#14F195" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">CardResult</text>
        </svg>
        <p class="docs-diagram-caption">SDK handles the 402 → pay → retry cycle automatically.</p>
      </div>
    </section>
  `;
}

function renderMCPServer(): string {
  return `
    <section id="mcp-server" aria-label="MCP Server">
      <h2>MCP Server</h2>
      <p>The <code>@asgcard/mcp-server</code> package exposes 8 tools via the <strong>Model Context Protocol</strong>, enabling AI agents in Claude Code, Claude Desktop, Cursor, and other MCP-compatible clients to manage ASG Card programmatically.</p>

      <div class="docs-callout docs-callout-info">
        <strong>npm:</strong> <a href="https://www.npmjs.com/package/@asgcard/mcp-server" target="_blank" rel="noopener">@asgcard/mcp-server</a> &nbsp;|&nbsp;
        <strong>GitHub:</strong> <a href="https://github.com/ASGCompute/asgcard-public/tree/main/mcp-server" target="_blank" rel="noopener">mcp-server/</a>
      </div>

      <hr class="docs-divider" />

      <h3 id="mcp-install">Setup</h3>

      <p><strong>Claude Code:</strong></p>
      ${codeBlock(`claude mcp add asgcard -- npx -y @asgcard/mcp-server`, 'bash')}

      <p><strong>Claude Desktop / Cursor — MCP config:</strong></p>
      ${codeBlock(`{
  "mcpServers": {
    "asgcard": {
      "command": "npx",
      "args": ["-y", "@asgcard/mcp-server"],
      "env": {
        "STELLAR_PRIVATE_KEY": "S..."
      }
    }
  }
}`, 'json')}

      <hr class="docs-divider" />

      <h3 id="mcp-tools">Tools</h3>
      <p>All 8 tools exposed by the MCP server:</p>
      <div class="docs-table-wrap">
        <table class="docs-table">
          <thead>
            <tr><th>Tool</th><th>Description</th><th>Auth</th></tr>
          </thead>
          <tbody>
            <tr><td data-label="Tool"><code>create_card</code></td><td data-label="Description">Create a virtual MasterCard with a specified tier (10–500 USD)</td><td data-label="Auth">x402</td></tr>
            <tr><td data-label="Tool"><code>fund_card</code></td><td data-label="Description">Add funds to an existing card</td><td data-label="Auth">x402</td></tr>
            <tr><td data-label="Tool"><code>list_cards</code></td><td data-label="Description">List all cards owned by the wallet</td><td data-label="Auth">Wallet</td></tr>
            <tr><td data-label="Tool"><code>get_card</code></td><td data-label="Description">Get card summary (balance, status)</td><td data-label="Auth">Wallet</td></tr>
            <tr><td data-label="Tool"><code>get_card_details</code></td><td data-label="Description">Retrieve PAN, CVV, expiry</td><td data-label="Auth">Wallet + Nonce</td></tr>
            <tr><td data-label="Tool"><code>freeze_card</code></td><td data-label="Description">Temporarily block all transactions</td><td data-label="Auth">Wallet</td></tr>
            <tr><td data-label="Tool"><code>unfreeze_card</code></td><td data-label="Description">Re-enable a frozen card</td><td data-label="Auth">Wallet</td></tr>
            <tr><td data-label="Tool"><code>get_pricing</code></td><td data-label="Description">View pricing tiers and fees</td><td data-label="Auth">None</td></tr>
          </tbody>
        </table>
      </div>

      <p><strong>Example — create a card via Claude:</strong></p>
      <div class="docs-callout docs-callout-tip">
        Just ask your AI agent: <em>"Create a $25 ASG Card for agent ALPHA with email agent@example.com"</em> — the MCP server handles x402 payment, wallet signing, and card creation automatically.
      </div>

    </section>
  `;
}

function renderAgentSkill(): string {
  return `
    <section id="agent-skill" aria-label="Agent Skill">
      <h2>Agent Skill (x402)</h2>
      <p>For custom autonomous agents like <strong>Open Claw</strong>, Codex, or raw LLM pipelines, teach them how to pay our APIs natively using the open-source x402 payments skill.</p>

      <div class="docs-callout docs-callout-info">
        <strong>GitHub:</strong> <a href="https://github.com/ASGCompute/x402-payments-skill" target="_blank" rel="noopener">x402-payments-skill</a>
      </div>

      <hr class="docs-divider" />

      <h3 id="skill-what-it-does">What the skill does</h3>
      <p>The skill gives your agent a complete decision tree for Stellar x402 payments:</p>
      <ul>
        <li>Listening for <code>402 Payment Required</code> challenges</li>
        <li>Building Soroban SAC USDC <code>transfer</code> invocations</li>
        <li>Signing Stellar <strong>auth entries</strong> (lighter than full transaction signing)</li>
        <li>Sending the signed XDR via the <code>X-PAYMENT</code> header</li>
        <li>Covering the full testnet-to-mainnet lifecycle (with OZ Channels facilitator)</li>
      </ul>

      <p><strong>Installation:</strong> Clone the repo and drop the <code>x402-payments</code> folder into your agent's skills directory.</p>
    </section>
  `;
}

function renderCLI(): string {
  return `
    <section id="cli" aria-label="CLI">
      <h2>CLI</h2>
      <p>The <code>@asgcard/cli</code> package provides a terminal interface for managing ASG Card — create, fund, freeze, and inspect virtual cards from your command line.</p>

      <div class="docs-callout docs-callout-info">
        <strong>npm:</strong> <a href="https://www.npmjs.com/package/@asgcard/cli" target="_blank" rel="noopener">@asgcard/cli</a> &nbsp;|&nbsp;
        <strong>GitHub:</strong> <a href="https://github.com/ASGCompute/asgcard-public/tree/main/cli" target="_blank" rel="noopener">cli/</a>
      </div>

      <hr class="docs-divider" />

      <h3 id="cli-install">Install</h3>
      ${codeBlock(`npm install -g @asgcard/cli`, 'bash')}

      <p><strong>Quick start:</strong></p>
      ${codeBlock(`# 1. Configure your Stellar key
asgcard login

# 2. Verify
asgcard whoami

# 3. Create a $10 card
asgcard card:create --tier 10 --name "AGENT ALPHA" --email agent@example.com`, 'bash')}

      <hr class="docs-divider" />

      <h3 id="cli-commands">Commands</h3>
      <div class="docs-table-wrap">
        <table class="docs-table">
          <thead>
            <tr><th>Command</th><th>Description</th></tr>
          </thead>
          <tbody>
            <tr><td data-label="Command"><code>asgcard login</code></td><td data-label="Description">Configure Stellar private key (stored at <code>~/.asgcard/config.json</code>)</td></tr>
            <tr><td data-label="Command"><code>asgcard whoami</code></td><td data-label="Description">Display wallet public key</td></tr>
            <tr><td data-label="Command"><code>asgcard cards</code></td><td data-label="Description">List all cards for the wallet</td></tr>
            <tr><td data-label="Command"><code>asgcard card &lt;id&gt;</code></td><td data-label="Description">Show card summary (balance, status)</td></tr>
            <tr><td data-label="Command"><code>asgcard card:details &lt;id&gt;</code></td><td data-label="Description">Retrieve PAN, CVV, expiry (nonce-protected)</td></tr>
            <tr><td data-label="Command"><code>asgcard card:create</code></td><td data-label="Description">Create a new card (x402 payment)</td></tr>
            <tr><td data-label="Command"><code>asgcard card:fund &lt;id&gt;</code></td><td data-label="Description">Top up an existing card</td></tr>
            <tr><td data-label="Command"><code>asgcard card:freeze &lt;id&gt;</code></td><td data-label="Description">Freeze a card</td></tr>
            <tr><td data-label="Command"><code>asgcard card:unfreeze &lt;id&gt;</code></td><td data-label="Description">Unfreeze a card</td></tr>
            <tr><td data-label="Command"><code>asgcard pricing</code></td><td data-label="Description">View pricing and fee tiers</td></tr>
            <tr><td data-label="Command"><code>asgcard health</code></td><td data-label="Description">Check API health status</td></tr>
          </tbody>
        </table>
      </div>

    </section>
  `;
}

function renderAuthentication(): string {
  return `
    <section id="authentication" aria-label="Authentication">
      <h2>Authentication</h2>
      <p>ASG Card uses two authentication modes depending on the endpoint.</p>

      <h3 id="x402-payment-flow">x402 Payment Flow</h3>
      <p>Paid endpoints (<code>POST /cards/create/tier/:amount</code>, <code>POST /cards/fund/tier/:amount</code>) use the x402 protocol on Stellar. The flow has 4 steps:</p>

      <h4>Step 1 — Request without payment</h4>
      ${codeBlock(`curl -X POST https://api.asgcard.dev/cards/create/tier/10 \\
  -H "Content-Type: application/json" \\
  -d '{"nameOnCard": "AGENT ALPHA", "email": "agent@example.com"}'`, 'bash')}

      <h4>Step 2 — Receive 402 with payment instructions</h4>
      <p>The server responds with <code>HTTP 402</code> and a challenge JSON:</p>
      ${codeBlock(`{
  "x402Version": 2,
  "resource": {
    "url": "https://api.asgcard.dev/cards/create/tier/10",
    "description": "Create ASG Card with $10 load",
    "mimeType": "application/json"
  },
  "accepts": [{
    "scheme": "exact",
    "network": "stellar:pubnet",
    "asset": "CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75",
    "amount": "172000000",
    "payTo": "GAHYHA55RTD2J4LAVJILTNHWMF2H2YVK5QXLQT3CHCJSVET3VRWPOCW6",
    "maxTimeoutSeconds": 300,
    "extra": { "areFeesSponsored": true }
  }]
}`, 'json')}

      <div class="docs-table-wrap">
        <table class="docs-table">
          <thead>
            <tr><th>Field</th><th>Description</th></tr>
          </thead>
          <tbody>
            <tr><td data-label="Field"><code>scheme</code></td><td data-label="Description">Always <code>"exact"</code></td></tr>
            <tr><td data-label="Field"><code>network</code></td><td data-label="Description"><code>"stellar:pubnet"</code></td></tr>
            <tr><td data-label="Field"><code>asset</code></td><td data-label="Description">USDC SAC on Stellar mainnet</td></tr>
            <tr><td data-label="Field"><code>amount</code></td><td data-label="Description">Amount in atomic USDC (7 decimals). 1 USDC = 10,000,000</td></tr>
            <tr><td data-label="Field"><code>payTo</code></td><td data-label="Description">ASG Treasury public key</td></tr>
            <tr><td data-label="Field"><code>maxTimeoutSeconds</code></td><td data-label="Description">Payment window (300s)</td></tr>
          </tbody>
        </table>
      </div>

      <h4>Step 3 — Agent pays USDC on Stellar</h4>
      <p>Parse the <code>accepts</code> array and send the specified USDC amount to the <code>payTo</code> address on Stellar, then proceed with facilitator verification if enabled.</p>

      <h4>Step 4 — Retry with X-PAYMENT header</h4>
      <p>Re-send the original request with an <code>X-PAYMENT</code> header containing base64-encoded JSON (x402 PaymentPayload):</p>
      ${codeBlock(`{
  "x402Version": 2,
  "accepted": {
    "scheme": "exact",
    "network": "stellar:pubnet"
  },
  "payload": {
    "transaction": "<BASE64_STELLAR_TX_ENVELOPE>"
  }
}`, 'json')}

      <div class="docs-callout docs-callout-info">
        <strong>Transport:</strong> <code>X-PAYMENT: base64(JSON)</code> — the SDK handles this automatically. The facilitator verifies and settles the transaction.
      </div>

      <hr class="docs-divider" />

      <h3 id="wallet-signature">Wallet Signature — Free Endpoints</h3>
      <p>Wallet-signed endpoints (card management) require Ed25519 signature authentication.</p>

      <h4>Required Headers</h4>
      <div class="docs-table-wrap">
        <table class="docs-table">
          <thead>
            <tr><th>Header</th><th>Description</th></tr>
          </thead>
          <tbody>
            <tr><td data-label="Header"><code>X-WALLET-ADDRESS</code></td><td data-label="Description">Stellar public key</td></tr>
            <tr><td data-label="Header"><code>X-WALLET-SIGNATURE</code></td><td data-label="Description">Ed25519 detached signature</td></tr>
            <tr><td data-label="Header"><code>X-WALLET-TIMESTAMP</code></td><td data-label="Description">Unix timestamp (seconds)</td></tr>
          </tbody>
        </table>
      </div>

      <h4>Signature Protocol</h4>
      ${codeBlock(`message = "asgcard-auth:<unixTimestamp>"
algorithm = Ed25519 detached
validity window = ±5 minutes`, 'text')}

      ${codeBlock(`const timestamp = Math.floor(Date.now() / 1000);
const message = \`asgcard-auth:\${timestamp}\`;

// wallet.signMessage should return detached Ed25519 signature bytes
const signature = await wallet.signMessage(new TextEncoder().encode(message));

const response = await fetch('https://api.asgcard.dev/cards', {
  headers: {
    'X-WALLET-ADDRESS': wallet.publicKey,
    'X-WALLET-SIGNATURE': Buffer.from(signature).toString('base64'),
    'X-WALLET-TIMESTAMP': String(timestamp),
  },
});`, 'typescript')}
    </section>
  `;
}

function renderPricingRows(): { creationRows: string; fundingRows: string } {
  const loadingRow = (cols: number) =>
    `<tr><td colspan="${cols}" style="text-align:center;color:rgba(255,255,255,0.3);padding:1.5rem;font-size:13px;">Loading pricing from <code>GET /pricing</code>\u2026</td></tr>`;

  const creationRows = creationTiers.length
    ? creationTiers.map(t =>
      `<tr>
        <td data-label="Load">${fmtUsd(t.loadAmount)}</td>
        <td data-label="Issuance">${fmtUsd(t.issuanceFee)}</td>
        <td data-label="Top-Up">${fmtUsd(t.topUpFee)}</td>
        <td data-label="Service">${fmtUsd(t.serviceFee)}</td>
        <td data-label="Total"><strong>${fmtUsd(t.totalCost)}</strong></td>
        <td data-label="Endpoint"><code>${t.endpoint}</code></td>
      </tr>`
    ).join('')
    : loadingRow(6);

  const fundingRows = fundingTiers.length
    ? fundingTiers.map(t =>
      `<tr>
        <td data-label="Fund">${fmtUsd(t.fundAmount)}</td>
        <td data-label="Top-Up">${fmtUsd(t.topUpFee)}</td>
        <td data-label="Service">${fmtUsd(t.serviceFee)}</td>
        <td data-label="Total"><strong>${fmtUsd(t.totalCost)}</strong></td>
        <td data-label="Endpoint"><code>${t.endpoint}</code></td>
      </tr>`
    ).join('')
    : loadingRow(5);

  return { creationRows, fundingRows };
}

function renderPricing(): string {
  const { creationRows, fundingRows } = renderPricingRows();

  return `
    <section id="pricing" aria-label="Pricing">
      <h2>Pricing</h2>
      <div class="docs-callout docs-callout-tip" id="pricing-source-note">
        Pricing is served by <code>GET /pricing</code> and reflected in the tables below.
      </div>
      <p>All amounts are in USD. 1 USDC = 10,000,000 atomic units (Stellar uses 7 decimal places).</p>

      <h3 id="card-creation">Card Creation</h3>
      <p>Creating a new virtual card includes the card load amount plus fees.</p>
      <div class="docs-table-wrap">
        <table class="docs-table" id="creation-pricing-table">
          <thead>
            <tr><th>Load</th><th>Issuance Fee</th><th>TopUp Fee</th><th>ASG Fee</th><th>Total</th><th>Endpoint</th></tr>
          </thead>
          <tbody>${creationRows}</tbody>
        </table>
      </div>

      <hr class="docs-divider" />

      <h3 id="card-funding">Card Funding</h3>
      <p>Adding funds to an existing card — no issuance fee.</p>
      <div class="docs-table-wrap">
        <table class="docs-table" id="funding-pricing-table">
          <thead>
            <tr><th>Fund Amount</th><th>TopUp Fee</th><th>ASG Fee</th><th>Total</th><th>Endpoint</th></tr>
          </thead>
          <tbody>${fundingRows}</tbody>
        </table>
      </div>
    </section>
  `;
}

function renderEndpoints(): string {
  return `
    <section id="endpoints" aria-label="Endpoints">
      <h2>Endpoints</h2>

      <h3 id="public-endpoints">Public Endpoints</h3>
      <p>No authentication required.</p>

      <div style="margin:1rem 0;padding:1rem 1.25rem;border:1px solid rgba(255,255,255,0.06);border-radius:8px;">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
          <span class="docs-badge docs-badge-get">GET</span>
          <code style="background:none;border:none;padding:0;color:rgba(255,255,255,0.8);font-size:13px;">/health</code>
        </div>
        <p>Health check. No authentication required.</p>
        <strong>Response 200:</strong>
        ${codeBlock(`{
  "status": "ok",
  "timestamp": "2026-02-11T14:00:00.000Z",
  "version": "1.0.0"
}`, 'json')}
      </div>

      <div style="margin:1rem 0;padding:1rem 1.25rem;border:1px solid rgba(255,255,255,0.06);border-radius:8px;">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
          <span class="docs-badge docs-badge-get">GET</span>
          <code style="background:none;border:none;padding:0;color:rgba(255,255,255,0.8);font-size:13px;">/pricing</code>
        </div>
        <p>Returns full pricing breakdown for all creation and funding tiers.</p>
        <strong>Response 200:</strong>
        ${codeBlock(`{
  "creation": {
    "tiers": [{
      "loadAmount": 10,
      "totalCost": 17.2,
      "issuanceFee": 3.0,
      "topUpFee": 2.2,
      "ourFee": 2.0,
      "endpoint": "/cards/create/tier/10"
    }]
  },
  "funding": {
    "tiers": [{
      "fundAmount": 10,
      "totalCost": 14.2,
      "topUpFee": 2.2,
      "ourFee": 2.0,
      "endpoint": "/cards/fund/tier/10"
    }]
  }
}`, 'json')}
      </div>

      <div style="margin:1rem 0;padding:1rem 1.25rem;border:1px solid rgba(255,255,255,0.06);border-radius:8px;">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
          <span class="docs-badge docs-badge-get">GET</span>
          <code style="background:none;border:none;padding:0;color:rgba(255,255,255,0.8);font-size:13px;">/cards/tiers</code>
        </div>
        <p>Returns available tiers with endpoints and detailed fee breakdowns.</p>
        <strong>Response 200:</strong>
        ${codeBlock(`{
  "creation": [{
    "loadAmount": 10,
    "totalCost": 17.2,
    "endpoint": "/cards/create/tier/10",
    "breakdown": {
      "cardLoad": 10,
      "issuanceFee": 3,
      "topUpFee": 2.2,
      "ourFee": 2,
      "buffer": 0
    }
  }],
  "funding": [{
    "fundAmount": 10,
    "totalCost": 14.2,
    "endpoint": "/cards/fund/tier/10",
    "breakdown": {
      "fundAmount": 10,
      "topUpFee": 2.2,
      "ourFee": 2
    }
  }]
}`, 'json')}
      </div>

      <hr class="docs-divider" />

      <h3 id="paid-endpoints">Paid Endpoints — x402</h3>
      <p>These endpoints require USDC payment via the x402 protocol on Stellar. See <a href="#x402-payment-flow">Authentication → x402 Payment Flow</a>.</p>

      <div style="margin:1rem 0;padding:1rem 1.25rem;border:1px solid rgba(255,255,255,0.06);border-radius:8px;">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
          <span class="docs-badge docs-badge-post">POST</span>
          <code style="background:none;border:none;padding:0;color:rgba(255,255,255,0.8);font-size:13px;">/cards/create/tier/:amount</code>
        </div>
        <p>Create a new virtual card loaded with the specified tier amount.</p>
        <p><strong>Available tiers:</strong> <code>10</code>, <code>25</code>, <code>50</code>, <code>100</code>, <code>200</code>, <code>500</code></p>
        <strong>Request body:</strong>
        <div class="docs-table-wrap">
          <table class="docs-table">
            <thead><tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr></thead>
            <tbody>
              <tr><td data-label="Field"><code>nameOnCard</code></td><td data-label="Type"><code>string</code></td><td data-label="Required">Yes</td><td data-label="Description">Min 1 char</td></tr>
              <tr><td data-label="Field"><code>email</code></td><td data-label="Type"><code>string</code></td><td data-label="Required">Yes</td><td data-label="Description">Valid email</td></tr>
            </tbody>
          </table>
        </div>
        <strong>Response 201 Created:</strong>
        ${codeBlock(`{
  "success": true,
  "card": {
    "cardId": "550e8400-e29b-41d4-a716-446655440000",
    "nameOnCard": "AGENT ALPHA",
    "balance": 10,
    "status": "active",
    "createdAt": "2026-02-11T14:00:00.000Z"
  },
  "payment": {
    "amountCharged": 17.2,
    "txHash": "<stellar_tx_hash>",
    "network": "stellar"
  },
  "detailsEnvelope": {
    "cardNumber": "5395000000007890",
    "expiryMonth": 12,
    "expiryYear": 2028,
    "cvv": "123",
    "billingAddress": {
      "street": "123 Main St",
      "city": "San Francisco",
      "state": "CA",
      "zip": "94105",
      "country": "US"
    },
    "oneTimeAccess": true,
    "expiresInSeconds": 300,
    "note": "Store securely. Use GET /cards/:id/details with X-AGENT-NONCE for subsequent access."
  }
}`, 'json')}
      </div>

      <div style="margin:1rem 0;padding:1rem 1.25rem;border:1px solid rgba(255,255,255,0.06);border-radius:8px;">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
          <span class="docs-badge docs-badge-post">POST</span>
          <code style="background:none;border:none;padding:0;color:rgba(255,255,255,0.8);font-size:13px;">/cards/fund/tier/:amount</code>
        </div>
        <p>Add funds to an existing card.</p>
        <strong>Request body:</strong>
        <div class="docs-table-wrap">
          <table class="docs-table">
            <thead><tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr></thead>
            <tbody>
              <tr><td data-label="Field"><code>cardId</code></td><td data-label="Type"><code>string</code></td><td data-label="Required">Yes</td><td data-label="Description">UUID of existing card</td></tr>
            </tbody>
          </table>
        </div>
        <strong>Response 200 OK:</strong>
        ${codeBlock(`{
  "success": true,
  "cardId": "550e8400-e29b-41d4-a716-446655440000",
  "fundedAmount": 25,
  "newBalance": 35.0,
  "payment": {
    "amountCharged": 29.5,
    "txHash": "<stellar_tx_hash>",
    "network": "stellar"
  }
}`, 'json')}
      </div>

      <hr class="docs-divider" />

      <h3 id="wallet-signed-endpoints">Wallet-Signed Endpoints</h3>
      <p>These endpoints are free but require wallet signature authentication. See <a href="#wallet-signature">Authentication → Wallet Signature</a>.</p>

      <div style="margin:1rem 0;padding:1rem 1.25rem;border:1px solid rgba(255,255,255,0.06);border-radius:8px;">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
          <span class="docs-badge docs-badge-get">GET</span>
          <code style="background:none;border:none;padding:0;color:rgba(255,255,255,0.8);font-size:13px;">/cards</code>
        </div>
        <p>List all cards owned by the authenticated wallet.</p>
        <strong>Response 200:</strong>
        ${codeBlock(`{
  "cards": [{
    "cardId": "550e8400-e29b-41d4-a716-446655440000",
    "nameOnCard": "AGENT ALPHA",
    "lastFour": "7890",
    "balance": 10.0,
    "status": "active",
    "createdAt": "2026-02-11T14:00:00.000Z"
  }]
}`, 'json')}
      </div>

      <div style="margin:1rem 0;padding:1rem 1.25rem;border:1px solid rgba(255,255,255,0.06);border-radius:8px;">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
          <span class="docs-badge docs-badge-get">GET</span>
          <code style="background:none;border:none;padding:0;color:rgba(255,255,255,0.8);font-size:13px;">/cards/:cardId</code>
        </div>
        <p>Get detailed info for a specific card.</p>
        <strong>Response 200:</strong>
        ${codeBlock(`{
  "card": {
    "cardId": "550e8400-e29b-41d4-a716-446655440000",
    "nameOnCard": "AGENT ALPHA",
    "email": "agent@example.com",
    "balance": 8.5,
    "initialAmountUsd": 10,
    "status": "active",
    "createdAt": "2026-02-11T14:00:00.000Z",
    "updatedAt": "2026-02-11T15:30:00.000Z"
  }
}`, 'json')}
      </div>

      <div style="margin:1rem 0;padding:1rem 1.25rem;border:1px solid rgba(255,255,255,0.06);border-radius:8px;">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
          <span class="docs-badge docs-badge-get">GET</span>
          <code style="background:none;border:none;padding:0;color:rgba(255,255,255,0.8);font-size:13px;">/cards/:cardId/details</code>
        </div>
        <p>Retrieve sensitive card details — full card number, CVV, expiry, and billing address. See <a href="#agent-first">Agent-First Details</a> for the full protocol.</p>
        <div class="docs-callout docs-callout-warn">
          Requires <code>X-AGENT-NONCE</code> header (UUID v4). Rate limited to <strong>5 unique nonces per card per hour</strong>. Returns <code>409</code> on replay, <code>403</code> if owner revoked access.
        </div>
        <strong>Required Headers:</strong>
        <div class="docs-table-wrap">
          <table class="docs-table">
            <thead><tr><th>Header</th><th>Description</th></tr></thead>
            <tbody>
              <tr><td data-label="Header"><code>X-WALLET-ADDRESS</code></td><td data-label="Description">Stellar public key</td></tr>
              <tr><td data-label="Header"><code>X-WALLET-SIGNATURE</code></td><td data-label="Description">Ed25519 detached signature</td></tr>
              <tr><td data-label="Header"><code>X-WALLET-TIMESTAMP</code></td><td data-label="Description">Unix timestamp (seconds)</td></tr>
              <tr><td data-label="Header"><code>X-AGENT-NONCE</code></td><td data-label="Description">UUID v4 — unique per request, anti-replay</td></tr>
            </tbody>
          </table>
        </div>
        <strong>Response 200:</strong>
        ${codeBlock(`{
  "details": {
    "cardNumber": "5395000000007890",
    "expiryMonth": 12,
    "expiryYear": 2028,
    "cvv": "123",
    "billingAddress": {
      "street": "123 Main St",
      "city": "San Francisco",
      "state": "CA",
      "zip": "94105",
      "country": "US"
    }
  }
}`, 'json')}
        <strong>Error Responses:</strong>
        <div class="docs-table-wrap">
          <table class="docs-table">
            <thead><tr><th>Code</th><th>When</th><th>Body</th></tr></thead>
            <tbody>
              <tr><td data-label="Code"><code>403</code></td><td data-label="When">Owner revoked details access</td><td data-label="Body"><code>{"error":"Details access revoked by card owner"}</code></td></tr>
              <tr><td data-label="Code"><code>409</code></td><td data-label="When">Nonce already used (replay)</td><td data-label="Body"><code>{"error":"Nonce already used (replay detected)","code":"REPLAY_REJECTED"}</code></td></tr>
              <tr><td data-label="Code"><code>429</code></td><td data-label="When">Rate limit exceeded</td><td data-label="Body"><code>{"error":"Card details rate limit exceeded (5 requests / hour)"}</code></td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div style="margin:1rem 0;padding:1rem 1.25rem;border:1px solid rgba(255,255,255,0.06);border-radius:8px;">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
          <span class="docs-badge docs-badge-post">POST</span>
          <code style="background:none;border:none;padding:0;color:rgba(255,255,255,0.8);font-size:13px;">/cards/:cardId/freeze</code>
        </div>
        <p>Freeze a card. Blocks all transactions until unfrozen.</p>
        <strong>Response 200:</strong>
        ${codeBlock(`{
  "success": true,
  "cardId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "frozen"
}`, 'json')}
      </div>

      <div style="margin:1rem 0;padding:1rem 1.25rem;border:1px solid rgba(255,255,255,0.06);border-radius:8px;">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
          <span class="docs-badge docs-badge-post">POST</span>
          <code style="background:none;border:none;padding:0;color:rgba(255,255,255,0.8);font-size:13px;">/cards/:cardId/unfreeze</code>
        </div>
        <p>Unfreeze a previously frozen card.</p>
        <strong>Response 200:</strong>
        ${codeBlock(`{
  "success": true,
  "cardId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "active"
}`, 'json')}
      </div>
    </section>
  `;
}

function renderAgentFirst(): string {
  return `
    <section id="agent-first" aria-label="Agent-First Details">
      <h2>Agent-First Details Access</h2>
      <p>ASG Card uses an <strong>agent-first model</strong> for sensitive card data. Card details (number, CVV, expiry) are delivered via two mechanisms designed for autonomous agents.</p>

      <h3 id="details-envelope">Details Envelope</h3>
      <p>When a card is created via <code>POST /cards/create/tier/:amount</code>, the <code>201</code> response includes a <code>detailsEnvelope</code> field with full card details:</p>
      ${codeBlock(`{
  "success": true,
  "card": { "cardId": "...", "status": "active" },
  "payment": { "txHash": "...", "network": "stellar" },
  "detailsEnvelope": {
    "cardNumber": "5395000000007890",
    "expiryMonth": 12,
    "expiryYear": 2028,
    "cvv": "123",
    "billingAddress": {
      "street": "123 Main St",
      "city": "San Francisco",
      "state": "CA",
      "zip": "94105",
      "country": "US"
    },
    "oneTimeAccess": true,
    "expiresInSeconds": 300
  }
}`, 'json')}
      <div class="docs-callout docs-callout-info">
        <strong>One-time access:</strong> The <code>detailsEnvelope</code> is returned only in the initial <code>201</code> response. It is not stored server-side. Agents should persist card details securely on their side.
      </div>

      <hr class="docs-divider" />

      <h3 id="get-card-details">GET /cards/:cardId/details</h3>
      <p>If the agent loses the initial envelope, card details can be retrieved via <code>GET /cards/:cardId/details</code> using wallet signature authentication plus a unique nonce.</p>

      <h4>Required Headers</h4>
      <div class="docs-table-wrap">
        <table class="docs-table">
          <thead><tr><th>Header</th><th>Type</th><th>Description</th></tr></thead>
          <tbody>
            <tr><td data-label="Header"><code>X-WALLET-ADDRESS</code></td><td data-label="Type"><code>string</code></td><td data-label="Description">Stellar public key (G...)</td></tr>
            <tr><td data-label="Header"><code>X-WALLET-SIGNATURE</code></td><td data-label="Type"><code>string</code></td><td data-label="Description">Ed25519 detached signature (base64)</td></tr>
            <tr><td data-label="Header"><code>X-WALLET-TIMESTAMP</code></td><td data-label="Type"><code>string</code></td><td data-label="Description">Unix timestamp (seconds)</td></tr>
            <tr><td data-label="Header"><code>X-AGENT-NONCE</code></td><td data-label="Type"><code>string</code></td><td data-label="Description">UUID v4 — must be unique per request</td></tr>
          </tbody>
        </table>
      </div>

      ${codeBlock(`import { v4 as uuid } from 'uuid';

const nonce = uuid();
const timestamp = Math.floor(Date.now() / 1000);
const message = \`asgcard-auth:\${timestamp}\`;
const signature = await wallet.signMessage(new TextEncoder().encode(message));

const res = await fetch('https://api.asgcard.dev/cards/<cardId>/details', {
  headers: {
    'X-WALLET-ADDRESS': wallet.publicKey,
    'X-WALLET-SIGNATURE': Buffer.from(signature).toString('base64'),
    'X-WALLET-TIMESTAMP': String(timestamp),
    'X-AGENT-NONCE': nonce,
  },
});

if (res.status === 409) {
  // Nonce replay detected — generate a new UUID and retry
}
if (res.status === 403) {
  // Card owner has revoked details access
}`, 'typescript')}

      <hr class="docs-divider" />

      <h3 id="nonce-replay">Nonce & Anti-Replay (409)</h3>
      <p>Every call to <code>GET /cards/:cardId/details</code> requires a fresh <code>X-AGENT-NONCE</code> (UUID v4). If a nonce has already been used for the same card, the server returns:</p>
      ${codeBlock(`HTTP/1.1 409 Conflict
{
  "error": "Nonce already used (replay detected)",
  "code": "REPLAY_REJECTED"
}`, 'json')}
      <p>This prevents replay attacks and ensures each details retrieval is intentional. Combined with the 5-request-per-hour rate limit per card, this protects cardholder data.</p>

      <hr class="docs-divider" />

      <h3 id="revoke-restore">Revoke / Restore</h3>
      <p>Card owners can control whether agents (or themselves, via the portal) can retrieve card details:</p>
      <div class="docs-table-wrap">
        <table class="docs-table">
          <thead><tr><th>Action</th><th>Endpoint</th><th>Effect</th></tr></thead>
          <tbody>
            <tr>
              <td data-label="Action">Revoke</td>
              <td data-label="Endpoint"><code>POST /cards/:cardId/revoke-details</code></td>
              <td data-label="Effect">Blocks all future <code>GET /details</code> → returns <code>403</code></td>
            </tr>
            <tr>
              <td data-label="Action">Restore</td>
              <td data-label="Endpoint"><code>POST /cards/:cardId/restore-details</code></td>
              <td data-label="Effect">Re-enables <code>GET /details</code> access</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p>Both endpoints require wallet signature authentication (same headers as card management). Revoked status returns:</p>
      ${codeBlock(`HTTP/1.1 403 Forbidden
{
  "error": "Details access revoked by card owner"
}`, 'json')}
    </section>
  `;
}

function renderErrors(): string {
  return `
    <section id="errors" aria-label="Errors">
      <h2>Errors</h2>
      <p>All non-2xx responses return:</p>
      ${codeBlock(`{ "error": "Human-readable error message" }`, 'json')}

      <div class="docs-table-wrap">
        <table class="docs-table">
          <thead>
            <tr><th>HTTP Code</th><th>When</th><th>Example</th></tr>
          </thead>
          <tbody>
            <tr>
              <td data-label="Code"><code>400</code></td>
              <td data-label="When">Unsupported tier, invalid body</td>
              <td data-label="Example"><code>{"error":"Unsupported tier amount"}</code></td>
            </tr>
            <tr>
              <td data-label="Code"><code>401</code></td>
              <td data-label="When">Invalid wallet auth or X-Payment proof</td>
              <td data-label="Example"><code>{"error":"Invalid wallet signature"}</code></td>
            </tr>
            <tr>
              <td data-label="Code"><code>402</code></td>
              <td data-label="When">x402 challenge (no <code>X-Payment</code> header)</td>
              <td data-label="Example">Challenge JSON (see <a href="#x402-payment-flow">x402 Flow</a>)</td>
            </tr>
            <tr>
              <td data-label="Code"><code>403</code></td>
              <td data-label="When">Details access revoked by card owner</td>
              <td data-label="Example"><code>{"error":"Details access revoked by card owner"}</code></td>
            </tr>
            <tr>
              <td data-label="Code"><code>404</code></td>
              <td data-label="When">Card not found</td>
              <td data-label="Example"><code>{"error":"Card not found"}</code></td>
            </tr>
            <tr>
              <td data-label="Code"><code>409</code></td>
              <td data-label="When">Nonce replay detected</td>
              <td data-label="Example"><code>{"error":"Nonce already used (replay detected)","code":"REPLAY_REJECTED"}</code></td>
            </tr>
            <tr>
              <td data-label="Code"><code>429</code></td>
              <td data-label="When">Details endpoint rate limit</td>
              <td data-label="Example"><code>{"error":"Card details rate limit exceeded (5 requests / hour)"}</code></td>
            </tr>
            <tr>
              <td data-label="Code"><code>500</code></td>
              <td data-label="When">Unexpected internal error</td>
              <td data-label="Example"><code>{"error":"Internal server error"}</code></td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  `;
}

function renderRateLimits(): string {
  return `
    <section id="rate-limits" aria-label="Rate Limits">
      <h2>Rate Limits</h2>
      <div class="docs-table-wrap">
        <table class="docs-table">
          <thead>
            <tr><th>Endpoint</th><th>Limit</th><th>Window</th></tr>
          </thead>
          <tbody>
            <tr><td data-label="Endpoint"><code>GET /cards/:cardId/details</code></td><td data-label="Limit">5 requests per card</td><td data-label="Window">1 hour</td></tr>
            <tr><td data-label="Endpoint">All other endpoints</td><td data-label="Limit">Standard per-IP limits apply</td><td data-label="Window">—</td></tr>
          </tbody>
        </table>
      </div>
      <p>Exceeding a rate limit returns <code>429 Too Many Requests</code>. If the response includes a <code>Retry-After</code> header, wait the indicated duration before retrying.</p>
    </section>
  `;
}

function renderArchitecture(): string {
  return `
    <section id="architecture" aria-label="Architecture">
      <h2>Architecture</h2>

      <h3>Request Lifecycle</h3>
      <p>End-to-end sequence for a paid card creation via x402.</p>
      <div class="docs-diagram" role="img" aria-label="x402 payment lifecycle: Agent sends POST, receives 402, pays USDC on Stellar, retries with X-Payment proof, API verifies on-chain, returns 201.">
        <svg viewBox="0 0 720 380" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
          <!-- Lifelines -->
          <text x="90" y="24" fill="#fafafa" font-family="Inter,system-ui,sans-serif" font-size="12" font-weight="600" text-anchor="middle">Agent / App</text>
          <text x="360" y="24" fill="#fafafa" font-family="Inter,system-ui,sans-serif" font-size="12" font-weight="600" text-anchor="middle">ASG Card API</text>
          <text x="630" y="24" fill="#fafafa" font-family="Inter,system-ui,sans-serif" font-size="12" font-weight="600" text-anchor="middle">Stellar</text>
          <line x1="90" y1="36" x2="90" y2="360" stroke="rgba(255,255,255,0.08)" stroke-width="1" stroke-dasharray="4 4"/>
          <line x1="360" y1="36" x2="360" y2="360" stroke="rgba(255,255,255,0.08)" stroke-width="1" stroke-dasharray="4 4"/>
          <line x1="630" y1="36" x2="630" y2="360" stroke="rgba(255,255,255,0.08)" stroke-width="1" stroke-dasharray="4 4"/>
          <!-- Step 1: POST -->
          <line x1="90" y1="64" x2="356" y2="64" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
          <polygon points="356,60 356,68 364,64" fill="rgba(255,255,255,0.3)"/>
          <text x="224" y="58" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">POST /cards/create/tier/10</text>
          <!-- Step 2: 402 -->
          <line x1="360" y1="100" x2="94" y2="100" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="6 3"/>
          <polygon points="94,96 94,104 86,100" fill="#f59e0b"/>
          <text x="224" y="94" fill="#f59e0b" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">402 + x402 challenge</text>
          <!-- Step 3: USDC -->
          <line x1="90" y1="148" x2="626" y2="148" stroke="#14F195" stroke-width="1.5"/>
          <polygon points="626,144 626,152 634,148" fill="#14F195"/>
          <text x="360" y="142" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">USDC transfer</text>
          <!-- Step 4: txHash -->
          <line x1="630" y1="184" x2="94" y2="184" stroke="rgba(255,255,255,0.2)" stroke-width="1.5" stroke-dasharray="6 3"/>
          <polygon points="94,180 94,188 86,184" fill="rgba(255,255,255,0.2)"/>
          <text x="360" y="178" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">txHash confirmed</text>
          <!-- Step 5: Retry -->
          <line x1="90" y1="228" x2="356" y2="228" stroke="#14F195" stroke-width="1.5"/>
          <polygon points="356,224 356,232 364,228" fill="#14F195"/>
          <text x="224" y="222" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">POST + X-Payment proof</text>
          <!-- Step 6: Verify -->
          <line x1="360" y1="264" x2="626" y2="264" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
          <polygon points="626,260 626,268 634,264" fill="rgba(255,255,255,0.2)"/>
          <text x="494" y="258" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">verify on-chain</text>
          <!-- Step 7: Confirmed -->
          <line x1="630" y1="292" x2="364" y2="292" stroke="rgba(255,255,255,0.2)" stroke-width="1.5" stroke-dasharray="6 3"/>
          <polygon points="364,288 364,296 356,292" fill="rgba(255,255,255,0.2)"/>
          <text x="494" y="286" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">confirmed ✓</text>
          <!-- Step 8: 201 -->
          <line x1="360" y1="328" x2="94" y2="328" stroke="#14F195" stroke-width="1.5" stroke-dasharray="6 3"/>
          <polygon points="94,324 94,332 86,328" fill="#14F195"/>
          <text x="224" y="322" fill="#14F195" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">201 + card details</text>
        </svg>
        <p class="docs-diagram-caption">x402 payment lifecycle — agent pays USDC on Stellar, API verifies on-chain before issuing the card.</p>
      </div>

      <hr class="docs-divider" />

      <h3>Runtime Components</h3>
      <p>Internal routing and middleware layout of the ASG Card API.</p>
      <div class="docs-diagram" role="img" aria-label="Runtime components: Public routes (health, pricing, tiers) connect directly. Paid routes go through x402 middleware. Wallet routes go through Ed25519 auth. Both middleware layers feed into Card Service.">
        <svg viewBox="0 0 720 320" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
          <!-- Outer box -->
          <rect x="20" y="10" width="680" height="300" rx="8" stroke="rgba(255,255,255,0.1)" stroke-width="1" fill="none"/>
          <text x="40" y="36" fill="#fafafa" font-family="Inter,system-ui,sans-serif" font-size="13" font-weight="600">ASG Card API</text>
          <!-- Public -->
          <rect x="50" y="60" width="170" height="110" rx="6" stroke="rgba(59,130,246,0.3)" stroke-width="1" fill="rgba(59,130,246,0.04)"/>
          <text x="135" y="82" fill="#60a5fa" font-family="Inter,system-ui,sans-serif" font-size="11" font-weight="600" text-anchor="middle">PUBLIC</text>
          <text x="135" y="106" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">/health</text>
          <text x="135" y="124" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">/pricing</text>
          <text x="135" y="142" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">/cards/tiers</text>
          <!-- x402 Middleware -->
          <rect x="260" y="60" width="190" height="110" rx="6" stroke="rgba(20,241,149,0.3)" stroke-width="1" fill="rgba(20,241,149,0.04)"/>
          <text x="355" y="82" fill="#14F195" font-family="Inter,system-ui,sans-serif" font-size="11" font-weight="600" text-anchor="middle">x402 MIDDLEWARE</text>
          <text x="355" y="106" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">parse challenge</text>
          <text x="355" y="124" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">verify payment proof</text>
          <text x="355" y="142" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">confirm on-chain tx</text>
          <!-- Wallet Auth -->
          <rect x="490" y="60" width="190" height="110" rx="6" stroke="rgba(251,191,36,0.3)" stroke-width="1" fill="rgba(251,191,36,0.04)"/>
          <text x="585" y="82" fill="#fbbf24" font-family="Inter,system-ui,sans-serif" font-size="11" font-weight="600" text-anchor="middle">WALLET AUTH</text>
          <text x="585" y="106" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">Ed25519 verification</text>
          <text x="585" y="120" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">/cards/:cardId</text>
          <text x="585" y="138" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">/cards/:cardId/freeze</text>
          <text x="585" y="156" fill="rgba(255,255,255,0.5)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">/cards/:cardId/unfreeze</text>
          <!-- Card Service -->
          <rect x="250" y="220" width="220" height="70" rx="6" stroke="rgba(255,255,255,0.12)" stroke-width="1" fill="rgba(255,255,255,0.03)"/>
          <text x="360" y="250" fill="#fafafa" font-family="Inter,system-ui,sans-serif" font-size="12" font-weight="600" text-anchor="middle">Card Service</text>
          <text x="360" y="270" fill="rgba(255,255,255,0.4)" font-family="Inter,system-ui,sans-serif" font-size="11" text-anchor="middle">create · fund · freeze · query</text>
          <!-- Arrows to Card Service -->
          <line x1="355" y1="170" x2="355" y2="218" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
          <polygon points="351,218 359,218 355,226" fill="rgba(255,255,255,0.15)"/>
          <line x1="585" y1="170" x2="468" y2="218" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
          <polygon points="464,216 472,216 468,224" fill="rgba(255,255,255,0.15)"/>
        </svg>
        <p class="docs-diagram-caption">Public routes require no auth. Paid routes pass through x402. Wallet routes use Ed25519 signatures. All converge on Card Service.</p>
      </div>
    </section>
  `;
}


// ============================================================
// Main render
// ============================================================
document.querySelector<HTMLDivElement>('#docs-app')!.innerHTML = `
  <div class="docs-layout">
    ${renderSidebar()}
    <div class="docs-main">
      <!-- Mobile burger -->
      <button class="docs-burger" id="burger" aria-label="Toggle navigation" aria-controls="sidebar" aria-expanded="false">
        <span class="docs-burger-line"></span>
        <span class="docs-burger-line"></span>
        <span class="docs-burger-line"></span>
      </button>
      <div class="docs-sidebar-overlay" id="mobile-overlay"></div>

      <!-- Topbar -->
      <div class="docs-topbar">
        <a href="/" class="docs-topbar-back">← Home</a>
        <span class="docs-topbar-title">Documentation</span>
      </div>

      <div class="docs-content-wrap">
        <main id="docs-content" class="docs-content" role="main">
          ${renderIntroduction()}
          ${renderOverview()}
          ${renderSDK()}
          ${renderMCPServer()}
          ${renderAgentSkill()}
          ${renderCLI()}
          ${renderAuthentication()}
          ${renderPricing()}
          ${renderEndpoints()}
          ${renderAgentFirst()}
          ${renderErrors()}
          ${renderRateLimits()}
          ${renderArchitecture()}
        </main>
      </div>
    </div>
  </div>
`;

// ============================================================
// Interactive behaviors
// ============================================================

// ── Copy buttons ──
document.querySelectorAll<HTMLButtonElement>('.docs-copy-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const targetId = btn.dataset.copyTarget;
    if (!targetId) return;
    const block = document.getElementById(targetId);
    if (!block) return;
    const text = block.textContent || '';
    try {
      await navigator.clipboard.writeText(text);
      btn.classList.add('copied');
      const label = btn.querySelector('.copy-label');
      if (label) label.textContent = 'Copied!';
      setTimeout(() => {
        btn.classList.remove('copied');
        if (label) label.textContent = 'Copy';
      }, 2000);
    } catch {
      // Fallback
    }
  });
});

// ── Sidebar active state via IntersectionObserver ──
const sections = document.querySelectorAll<HTMLElement>('section[id], h3[id]');
const sidebarLinks = document.querySelectorAll<HTMLAnchorElement>('.docs-sidebar-link');

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        sidebarLinks.forEach(link => {
          link.classList.toggle('active', link.getAttribute('data-section') === id);
        });
        history.replaceState(null, '', `#${id}`);
      }
    });
  },
  {
    rootMargin: '-80px 0px -60% 0px',
    threshold: 0,
  }
);

sections.forEach(section => observer.observe(section));

// ── Smooth scroll on sidebar clicks ──
sidebarLinks.forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const href = link.getAttribute('href');
    if (!href) return;
    const target = document.querySelector(href);
    if (target) {
      const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
      // Close mobile sidebar & sync aria-expanded
      const sidebar = document.getElementById('sidebar');
      const overlayEl = document.getElementById('mobile-overlay');
      const burgerEl = document.getElementById('burger');
      if (sidebar) sidebar.classList.remove('open');
      if (overlayEl) overlayEl.classList.remove('open');
      if (burgerEl) burgerEl.setAttribute('aria-expanded', 'false');
    }
  });
});

// ── Mobile sidebar toggle ──
const burger = document.getElementById('burger');
const sidebar = document.getElementById('sidebar');
const overlayEl = document.getElementById('mobile-overlay');

if (burger && sidebar && overlayEl) {
  burger.addEventListener('click', () => {
    const isOpen = sidebar.classList.contains('open');
    sidebar.classList.toggle('open', !isOpen);
    overlayEl.classList.toggle('open', !isOpen);
    burger.setAttribute('aria-expanded', String(!isOpen));
  });

  overlayEl.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlayEl.classList.remove('open');
    burger.setAttribute('aria-expanded', 'false');
  });
}

// ── Fetch live pricing and update tables ──
fetchLivePricing().then(() => {
  const creationTbody = document.querySelector('#creation-pricing-table tbody');
  const fundingTbody = document.querySelector('#funding-pricing-table tbody');
  const pricingSourceNote = document.getElementById('pricing-source-note');

  if (!pricingLoaded) {
    const unavailableRow = (cols: number) =>
      `<tr><td colspan="${cols}" style="text-align:center;color:rgba(255,255,255,0.38);padding:1.5rem;font-size:13px;">Live pricing is temporarily unavailable. Please refresh in a few seconds.</td></tr>`;
    if (creationTbody) creationTbody.innerHTML = unavailableRow(6);
    if (fundingTbody) fundingTbody.innerHTML = unavailableRow(5);
    if (pricingSourceNote) {
      pricingSourceNote.classList.remove('docs-callout-tip');
      pricingSourceNote.classList.add('docs-callout-info');
      pricingSourceNote.textContent = 'Pricing is sourced from GET /pricing. If tables are empty, DNS or API propagation may still be in progress.';
    }
    return;
  }

  const { creationRows, fundingRows } = renderPricingRows();
  if (creationTbody) creationTbody.innerHTML = creationRows;
  if (fundingTbody) fundingTbody.innerHTML = fundingRows;
});
