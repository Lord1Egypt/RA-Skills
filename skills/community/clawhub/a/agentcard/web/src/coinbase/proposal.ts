import '../style.css'

document.querySelector<HTMLDivElement>('#proposal-app')!.innerHTML = `
<div class="max-w-[48rem] mx-auto px-8 py-6 flex flex-col min-h-screen">
  <!-- Header -->
  <div class="mb-6 flex justify-between items-start gap-4">
    <div>
      <div class="flex items-center gap-2 mb-3">
        <img src="/logo-mark.svg" alt="ASG Card" class="h-6 w-6" />
        <span class="font-bold text-gray-900 text-lg tracking-tight">ASG Card</span>
        <div class="ml-2 inline-block px-2 py-0.5 rounded-sm border border-green-200 bg-green-50 text-[9px] font-bold tracking-[0.15em] uppercase" style="color: #14F195; background-color: rgba(20, 241, 149, 0.1); border-color: rgba(20, 241, 149, 0.2);">
          COMMERCIAL PROPOSAL
        </div>
      </div>
      <h1 class="text-3xl font-bold tracking-tight text-gray-900 mb-2 sm:text-4xl">
        Programmable Virtual Cards for AI Agents on Base
      </h1>
      <p class="text-[14px] text-gray-600 max-w-2xl leading-snug mt-1">
        Enable autonomous AI agents to spend safely and programmatically. ASG Card provides instant virtual cards for agent-driven payments — powered by the x402 protocol natively on Base, settled in USDC, and built on Coinbase's onchain infrastructure.
      </p>
    </div>
    <div class="flex items-center pt-2 shrink-0">
      <img src="/coinbase-logo.svg" class="h-8 object-contain" alt="Coinbase" />
      <span class="ml-2 font-bold text-2xl tracking-tight" style="color: #0052FF;">Base</span>
    </div>
  </div>

  <!-- Main Grid -->
  <div class="grid md:grid-cols-2 gap-8 mb-6 border-t border-gray-100 pt-5">
    <!-- Left Col -->
    <div>
      <h2 class="text-[15px] font-bold mb-2 text-gray-800 uppercase tracking-wide">What is ASG Card</h2>
      <p class="text-[13px] text-gray-600 mb-4 leading-relaxed">
        ASG Card is payment-to-card infrastructure for AI agents. It converts paid API actions into immediate virtual card issuance with granular spend controls and strict policy limits, ensuring agents can execute spend safely.
      </p>
      <div class="flex flex-wrap gap-x-4 gap-y-2 text-[11px] font-semibold text-gray-500 uppercase tracking-wider">
        <span>x402-native</span>
        <span class="text-gray-300">•</span>
        <span>Virtual Cards API</span>
        <span class="text-gray-300">•</span>
        <span>USDC on Base</span>
      </div>
    </div>

    <!-- Right Col -->
    <div>
      <h2 class="text-[15px] font-bold mb-3 text-gray-800 uppercase tracking-wide">How it works</h2>
      <div class="space-y-3">
        <div class="flex gap-3">
          <div class="font-bold text-gray-400 text-[13px]">1.</div>
          <div class="text-[13px] text-gray-700 leading-snug"><span class="font-semibold text-gray-900">Agent requests a paid action:</span> call card create/fund endpoint.</div>
        </div>
        <div class="flex gap-3">
          <div class="font-bold text-gray-400 text-[13px]">2.</div>
          <div class="text-[13px] text-gray-700 leading-snug"><span class="font-semibold text-gray-900">x402 challenge &amp; payment:</span> Coinbase's x402 facilitator verifies payment intent on Base.</div>
        </div>
        <div class="flex gap-3">
          <div class="font-bold text-gray-400 text-[13px]">3.</div>
          <div class="text-[13px] text-gray-700 leading-snug"><span class="font-semibold text-gray-900">Settlement:</span> USDC settles on Base L2 with near-instant finality and minimal fees.</div>
        </div>
        <div class="flex gap-3">
          <div class="font-bold text-gray-400 text-[13px]">4.</div>
          <div class="text-[13px] text-gray-700 leading-snug"><span class="font-semibold text-gray-900">Card response:</span> ASG Card issues/funds card and returns details plus controls.</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Second Grid -->
  <div class="grid md:grid-cols-2 gap-8 mb-6 border-t border-gray-100 pt-5">
    <!-- Left Col -->
    <div>
      <h2 class="text-[15px] font-bold mb-3 text-gray-800 uppercase tracking-wide">Expanded Use Cases</h2>
      <ul class="space-y-2 text-[13px] text-gray-700 list-inside marker:text-gray-400" style="list-style-type: square;">
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;"><span class="font-semibold text-gray-900">Autonomous ops:</span> agents buy APIs/cloud in real time with policy-bound cards on Base.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;"><span class="font-semibold text-gray-900">Runbooks:</span> per-task cards for GPU budgets with strict audit trails.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;"><span class="font-semibold text-gray-900">Procurement:</span> enterprise bots handling SaaS renewals and subscriptions.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;"><span class="font-semibold text-gray-900">x402 monetization:</span> Coinbase-native pay-per-action micro-payments via x402 settlement.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;"><span class="font-semibold text-gray-900">Cross-border teams:</span> centralized USDC treasury on Base, distributed virtual cards.</li>
      </ul>
      <p class="text-[11px] text-gray-500 mt-3 italic">Applicable to CDP AgentKit, Based Agents, and similar frameworks.</p>
    </div>

    <!-- Right Col -->
    <div>
      <h2 class="text-[15px] font-bold mb-3 text-gray-800 uppercase tracking-wide">Target Users (ICP)</h2>
      <ul class="space-y-2 text-[13px] text-gray-700 list-inside marker:text-gray-400" style="list-style-type: square;">
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;">Teams building on Base with CDP AgentKit and Based Agents.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;">Coinbase Commerce merchants needing agent-driven spend capabilities.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;">FinOps/operations teams requiring robust spend controls on L2.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;">Treasury teams adopting USDC-on-Base settlement rails.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;">Ecosystem partners integrating virtual card infrastructure.</li>
      </ul>
    </div>
  </div>

  <!-- Value by Platform -->
  <div class="mb-6 border-t border-gray-100 pt-5">
    <h2 class="text-[15px] font-bold mb-4 text-gray-800 uppercase tracking-wide">Value by Platform</h2>
    
    <div class="grid md:grid-cols-3 gap-6">
      <div class="space-y-1">
        <div class="text-[14px] font-bold text-gray-900 border-b border-gray-200 pb-1 mb-2">Coinbase / Base</div>
        <div class="text-[12px] text-gray-800 font-medium">Flagship x402 use-case & real-world USDC volume on Base.</div>
        <div class="text-[12px] text-gray-500 leading-snug mt-1">Demonstrates x402 in production. Drives USDC settlement on Base and positions Coinbase as the leader in AI-native commerce infrastructure.</div>
      </div>
      <div class="space-y-1">
        <div class="text-[14px] font-bold text-gray-900 border-b border-gray-200 pb-1 mb-2">x402 Protocol</div>
        <div class="text-[12px] text-gray-800 font-medium">First production reference for the x402 payment standard.</div>
        <div class="text-[12px] text-gray-500 leading-snug mt-1">Coinbase-originated protocol gains a visible, production-grade integration that validates the HTTP 402 payment flow at scale.</div>
      </div>
      <div class="space-y-1">
        <div class="text-[14px] font-bold text-gray-900 border-b border-gray-200 pb-1 mb-2">ASG Card + Partners</div>
        <div class="text-[12px] text-gray-800 font-medium">New transaction revenue stream with low friction.</div>
        <div class="text-[12px] text-gray-500 leading-snug mt-1">Faster pilot-to-scale conversion with measurable KPIs on Coinbase's infrastructure.</div>
      </div>
    </div>
  </div>

  <!-- Suggested Pilot Structure -->
  <div class="border-t border-gray-100 pt-5 flex-grow">
    <h2 class="text-[15px] font-bold mb-3 text-gray-800 uppercase tracking-wide">Suggested Pilot Structure</h2>
    
    <div class="grid md:grid-cols-2 gap-x-8 gap-y-4 items-start">
      <div class="flex gap-2 text-[13px] text-gray-700">
        <div class="font-bold text-gray-400">1.</div>
        <div class="leading-snug"><b>x402 Sandbox on Base:</b> Integrate ASG Card with Coinbase's x402 facilitator on Base. Validate the full payment-to-card flow.</div>
      </div>
      <div class="flex gap-2 text-[13px] text-gray-700">
        <div class="font-bold text-gray-400">2.</div>
        <div class="leading-snug"><b>Closed Beta Launch:</b> Roll out to a select cohort of CDP AgentKit developers. Monitor success rates, latency, and x402 facilitator logic.</div>
      </div>
      <div class="flex gap-2 text-[13px] text-gray-700">
        <div class="font-bold text-gray-400">3.</div>
        <div class="leading-snug"><b>Public Mainnet Release:</b> Open to the Base ecosystem, supported by joint marketing, developer grants and Coinbase Commerce integration.</div>
      </div>
      <div class="flex gap-2 text-[13px] text-gray-700">
        <div class="font-bold text-gray-400">4.</div>
        <div class="leading-snug"><b>Commercial Scaling:</b> Implement tiered volume pricing and expand the agent-to-card pipeline to institutional FinOps use cases.</div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <div class="mt-8 pt-4 border-t border-gray-100 flex justify-between items-center text-[10px] text-gray-400 uppercase tracking-wider">
    <div>Prepared for partner discussions</div>
    <div>Updated: February 23, 2026</div>
  </div>
</div>

<style>
body {
  background-color: #ffffff;
}
#proposal-app, body {
  color: #1f2937;
}
@media print {
  @page {
    margin: 0.5cm;
    size: letter;
  }
  body {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}
</style>
`
