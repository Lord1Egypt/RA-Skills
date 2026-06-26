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
          PARTNERSHIP PROPOSAL
        </div>
      </div>
      <h1 class="text-3xl font-bold tracking-tight text-gray-900 mb-2 sm:text-4xl">
        Bridging x402 Agentic Spend APIs with Cypher Infrastructure
      </h1>
      <p class="text-[14px] text-gray-600 max-w-2xl leading-snug mt-1">
        Joint pilot to power the next generation of AI agent commerce. ASG Card integrates directly with Cypher as our preferred card issuance partner, converting on-chain stablecoin settlements from autonomous agents into instantly usable Cypher virtual cards.
      </p>
    </div>
    <div class="flex items-center pt-2 shrink-0">
      <img src="/cypher-logo.svg" class="h-8 object-contain" alt="Cypher" />
    </div>
  </div>

  <!-- Main Grid -->
  <div class="grid md:grid-cols-2 gap-8 mb-6 border-t border-gray-100 pt-5">
    <!-- Left Col -->
    <div>
      <h2 class="text-[15px] font-bold mb-2 text-gray-800 uppercase tracking-wide">The Partnership</h2>
      <p class="text-[13px] text-gray-600 mb-4 leading-relaxed">
        ASG Card handles the x402 protocol, agent identity, crypto settlement, and granular spend policies. Cypher provides the robust fiat off-ramp, instant virtual card issuance API, and seamless integration. Together, we enable AI agents to pay anywhere on the traditional web.
      </p>
      <div class="flex flex-wrap gap-x-4 gap-y-2 text-[11px] font-semibold text-gray-500 uppercase tracking-wider">
        <span>x402-native</span>
        <span class="text-gray-300">•</span>
        <span>Cypher Card Rails</span>
        <span class="text-gray-300">•</span>
        <span>Developer Focused</span>
      </div>
    </div>

    <!-- Right Col -->
    <div>
      <h2 class="text-[15px] font-bold mb-3 text-gray-800 uppercase tracking-wide">How it works</h2>
      <div class="space-y-3">
        <div class="flex gap-3">
          <div class="font-bold text-gray-400 text-[13px]">1.</div>
          <div class="text-[13px] text-gray-700 leading-snug"><span class="font-semibold text-gray-900">Agent request:</span> AI agent hits a paywall or paid endpoint, requesting funding via ASG Card.</div>
        </div>
        <div class="flex gap-3">
          <div class="font-bold text-gray-400 text-[13px]">2.</div>
          <div class="text-[13px] text-gray-700 leading-snug"><span class="font-semibold text-gray-900">Crypto Settlement:</span> x402 verifies intent; stablecoins are settled instantly on-chain.</div>
        </div>
        <div class="flex gap-3">
          <div class="font-bold text-gray-400 text-[13px]">3.</div>
          <div class="text-[13px] text-gray-700 leading-snug"><span class="font-semibold text-gray-900">Cypher Issuance:</span> ASG backend triggers Cypher's API to spawn/fund a virtual card instantly.</div>
        </div>
        <div class="flex gap-3">
          <div class="font-bold text-gray-400 text-[13px]">4.</div>
          <div class="text-[13px] text-gray-700 leading-snug"><span class="font-semibold text-gray-900">Execution:</span> Agent receives card details and executes the fiat transaction successfully.</div>
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
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;"><span class="font-semibold text-gray-900">Autonomous ops:</span> agents buy APIs/cloud in real time with Cypher-issued cards.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;"><span class="font-semibold text-gray-900">Runbooks:</span> per-task cards for GPU budgets with strict audit trails.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;"><span class="font-semibold text-gray-900">Procurement:</span> enterprise bots handling SaaS renewals and subscriptions.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;"><span class="font-semibold text-gray-900">B2B Agent Logic:</span> Connecting modern developer tools with seamless fiat boundaries.</li>
      </ul>
      <p class="text-[11px] text-gray-500 mt-3 italic">Connecting the crypto-native AI ecosystem to real-world fiat utilities via CypherHQ.</p>
    </div>

    <!-- Right Col -->
    <div>
      <h2 class="text-[15px] font-bold mb-3 text-gray-800 uppercase tracking-wide">Synergies &amp; Impact</h2>
      <ul class="space-y-2 text-[13px] text-gray-700 list-inside marker:text-gray-400" style="list-style-type: square;">
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;">Cypher gains net-new B2B transaction volume driven by autonomous agents, a massive emerging sector.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;">ASG Card leverages Cypher's modern, developer-first API and rapid issuance capabilities.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;">Shared PR &amp; Marketing demonstrating leadership at the intersection of AI, Web3, and frictionless spending.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;">Positions Cypher as the go-to infrastructure for agentic crypto-to-fiat commerce.</li>
      </ul>
    </div>
  </div>

  <!-- Value by Platform -->
  <div class="mb-6 border-t border-gray-100 pt-5">
    <h2 class="text-[15px] font-bold mb-4 text-gray-800 uppercase tracking-wide">Value Proposition</h2>
    
    <div class="grid md:grid-cols-2 gap-6">
      <div class="space-y-1">
        <div class="text-[14px] font-bold text-gray-900 border-b border-gray-200 pb-1 mb-2">For CypherHQ</div>
        <div class="text-[12px] text-gray-800 font-medium">B2B Agentic API Volume.</div>
        <div class="text-[12px] text-gray-500 leading-snug mt-1">Unlock a massive new addressable market by becoming the backbone for programmatic, non-human B2B spending.</div>
      </div>
      <div class="space-y-1">
        <div class="text-[14px] font-bold text-gray-900 border-b border-gray-200 pb-1 mb-2">For ASG Card</div>
        <div class="text-[12px] text-gray-800 font-medium">Developer-friendly Fiat Infrastructure.</div>
        <div class="text-[12px] text-gray-500 leading-snug mt-1">Abstract away the complexity of card issuance by relying on Cypher’s modern, composable API rails.</div>
      </div>
    </div>
  </div>

  <!-- Suggested Pilot Structure -->
  <div class="border-t border-gray-100 pt-5 flex-grow">
    <h2 class="text-[15px] font-bold mb-3 text-gray-800 uppercase tracking-wide">Joint Pilot Structure</h2>
    
    <div class="grid md:grid-cols-2 gap-x-8 gap-y-4 items-start">
      <div class="flex gap-2 text-[13px] text-gray-700">
        <div class="font-bold text-gray-400">1.</div>
        <div class="leading-snug"><b>API Integration &amp; Sandbox:</b> Connect ASG orchestration layer to Cypher card issuance APIs in a test environment. Validate speeds.</div>
      </div>
      <div class="flex gap-2 text-[13px] text-gray-700">
        <div class="font-bold text-gray-400">2.</div>
        <div class="leading-snug"><b>Closed Beta (B2B):</b> Onboard select AI agent developers. Issue live Cypher virtual cards for pilot use-cases (e.g., devops, cloud APIs).</div>
      </div>
      <div class="flex gap-2 text-[13px] text-gray-700">
        <div class="font-bold text-gray-400">3.</div>
        <div class="leading-snug"><b>Public Launch:</b> Joint press release and marketing push. Open access to ASG Card powered natively by CypherHQ.</div>
      </div>
      <div class="flex gap-2 text-[13px] text-gray-700">
        <div class="font-bold text-gray-400">4.</div>
        <div class="leading-snug"><b>Scale &amp; Optimize:</b> High-volume load balancing, rapid on-the-fly provisioning, and tight integration with agentic orchestrators.</div>
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
body { background-color: #ffffff; }
#proposal-app, body { color: #1f2937; }
@media print {
  @page { margin: 0.5cm; size: letter; }
  body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
</style>
`
