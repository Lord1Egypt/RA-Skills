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
        Programmable Virtual Cards for AI Agents on Arbitrum
      </h1>
      <p class="text-[14px] text-gray-600 max-w-2xl leading-snug mt-1">
        Enable autonomous AI agents to spend safely and programmatically. ASG Card provides instant virtual cards for agent-driven payments — funded via the x402 protocol, settled in USDC on Arbitrum, and secured by x402.
      </p>
    </div>
    <div class="flex items-center pt-2 shrink-0">
      <img src="/arbitrum-logo.svg" class="h-8 object-contain" alt="Arbitrum" />
      <span class="ml-2 font-bold text-2xl tracking-tight" style="color: #213147;">arbitrum</span>
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
        <span>USDC on Arbitrum</span>
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
          <div class="text-[13px] text-gray-700 leading-snug"><span class="font-semibold text-gray-900">x402 challenge & payment:</span> x402 facilitator verifies payment intent and execution.</div>
        </div>
        <div class="flex gap-3">
          <div class="font-bold text-gray-400 text-[13px]">3.</div>
          <div class="text-[13px] text-gray-700 leading-snug"><span class="font-semibold text-gray-900">Settlement:</span> USDC settles on Arbitrum and payment is confirmed.</div>
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
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;"><span class="font-semibold text-gray-900">Autonomous ops:</span> agents buy APIs/cloud in real time with policy-bound cards.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;"><span class="font-semibold text-gray-900">Runbooks:</span> per-task cards for GPU budgets with strict audit trails.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;"><span class="font-semibold text-gray-900">Procurement:</span> enterprise bots handling SaaS renewals and subscriptions.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;"><span class="font-semibold text-gray-900">API monetization:</span> pay-per-action micro-payments via x402 settlement.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;"><span class="font-semibold text-gray-900">Cross-border teams:</span> centralized USDC treasury, distributed virtual cards.</li>
      </ul>
      <p class="text-[11px] text-gray-500 mt-3 italic">Applicable to OpenClaw and similar agent frameworks.</p>
    </div>

    <!-- Right Col -->
    <div>
      <h2 class="text-[15px] font-bold mb-3 text-gray-800 uppercase tracking-wide">Target Users (ICP)</h2>
      <ul class="space-y-2 text-[13px] text-gray-700 list-inside marker:text-gray-400" style="list-style-type: square;">
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;">Teams shipping agentic products (OpenClaw and similar stacks).</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;">API platforms launching paid agent endpoints.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;">FinOps/operations teams requiring robust spend controls.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;">Treasury teams adopting USDC settlement rails.</li>
        <li class="pl-1" style="text-indent: -1rem; margin-left: 1rem;">Ecosystem partners integrating virtual card infrastructure.</li>
      </ul>
    </div>
  </div>

  <!-- Value by Platform -->
  <div class="mb-6 border-t border-gray-100 pt-5">
    <h2 class="text-[15px] font-bold mb-4 text-gray-800 uppercase tracking-wide">Value by Platform</h2>
    
    <div class="grid md:grid-cols-3 gap-6">
      <div class="space-y-1">
        <div class="text-[14px] font-bold text-gray-900 border-b border-gray-200 pb-1 mb-2">Arbitrum</div>
        <div class="text-[12px] text-gray-800 font-medium">USDC settlement growth & brand leadership in agentic commerce.</div>
        <div class="text-[12px] text-gray-500 leading-snug mt-1">Drives real-world USDC volume and highlights Arbitrum’s high-throughput L2 infrastructure for scalable AI native use-cases.</div>
      </div>
      <div class="space-y-1">
        <div class="text-[14px] font-bold text-gray-900 border-b border-gray-200 pb-1 mb-2">x402 Facilitator</div>
        <div class="text-[12px] text-gray-800 font-medium">Facilitator adoption in production-grade flows.</div>
        <div class="text-[12px] text-gray-500 leading-snug mt-1">Visible reference integration for x402 monetization orchestration.</div>
      </div>
      <div class="space-y-1">
        <div class="text-[14px] font-bold text-gray-900 border-b border-gray-200 pb-1 mb-2">ASG Card + Partners</div>
        <div class="text-[12px] text-gray-800 font-medium">New transaction revenue stream with low friction.</div>
        <div class="text-[12px] text-gray-500 leading-snug mt-1">Faster pilot-to-scale conversion with measurable KPIs.</div>
      </div>
    </div>
  </div>

  <!-- Suggested Pilot Structure -->
  <div class="border-t border-gray-100 pt-5 flex-grow">
    <h2 class="text-[15px] font-bold mb-3 text-gray-800 uppercase tracking-wide">Suggested Pilot Structure</h2>
    
    <div class="grid md:grid-cols-2 gap-x-8 gap-y-4 items-start">
      <div class="flex gap-2 text-[13px] text-gray-700">
        <div class="font-bold text-gray-400">1.</div>
        <div class="leading-snug"><b>Co-Development & Sandbox:</b> Integrate ASG Card with the x402 Arbitrum infrastructure. Validate the x402 USDC flow.</div>
      </div>
      <div class="flex gap-2 text-[13px] text-gray-700">
        <div class="font-bold text-gray-400">2.</div>
        <div class="leading-snug"><b>Closed Beta Launch:</b> Roll out to a select cohort of agent developers. Monitor success rates, latency, and facilitator logic.</div>
      </div>
      <div class="flex gap-2 text-[13px] text-gray-700">
        <div class="font-bold text-gray-400">3.</div>
        <div class="leading-snug"><b>Public Mainnet Release:</b> Open the full solution to the OpenClaw ecosystem, supported by joint marketing and developer grants.</div>
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
    <div>Updated: February 21, 2026</div>
  </div>
</div>

<style>
/* Specific tweaks to override global dark theme where necessary for the proposal */
body {
  background-color: #ffffff;
}
#proposal-app, body {
  color: #1f2937; /* gray-800 */
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
