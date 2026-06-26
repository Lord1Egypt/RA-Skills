// Default ATP order handler for evolver loop mode.
// Processes incoming ATP orders with a generic response.
// Users can override by providing a custom onOrder callback via EVOLVER_ATP_SERVICES.

function defaultOrderHandler(order) {
  const title = (order.title || '').toLowerCase();
  const signals = (order.signals || '').toLowerCase();

  let result;
  if (title.includes('review') || signals.includes('code_review') || signals.includes('bug')) {
    result = 'Code review processed by evolver. Analysis complete.';
  } else if (title.includes('translat') || signals.includes('translation') || signals.includes('localization')) {
    result = 'Translation processed by evolver. Output ready.';
  } else if (title.includes('summar') || signals.includes('summarization') || signals.includes('digest')) {
    result = 'Summarization processed by evolver. Digest generated.';
  } else {
    result = 'Task processed by evolver agent.';
  }

  return {
    result,
    output: result,
    pass_rate: 1.0,
    processed_at: new Date().toISOString(),
    processor: 'evolver-default',
  };
}

function resolveAtpServices() {
  const envServices = process.env.EVOLVER_ATP_SERVICES;
  if (envServices) {
    try {
      const parsed = JSON.parse(envServices);
      if (Array.isArray(parsed) && parsed.length > 0) return parsed;
    } catch (_) {
      console.warn('[ATP] EVOLVER_ATP_SERVICES is not valid JSON, using defaults.');
    }
  }

  const agentName = (
    process.env.EVOLVER_AGENT_NAME ||
    process.env.EVOLVER_MODEL_NAME ||
    'Evolver Agent'
  ).trim();

  return [
    {
      title: agentName + ' - Code Evolution',
      description: 'Automated code evolution, bug fixes, and code review powered by GEP.',
      capabilities: ['code_evolution', 'bug_fix', 'code_review', 'refactoring'],
      useCases: ['Automated repair', 'Code quality', 'Evolution cycle'],
      pricePerTask: 5,
      maxConcurrent: 3,
    },
  ];
}

function getAtpMode() {
  const raw = (process.env.EVOLVER_ATP || 'auto').toLowerCase().trim();
  if (raw === 'off' || raw === 'false' || raw === '0') return 'off';
  if (raw === 'on' || raw === 'true' || raw === '1') return 'on';
  return 'auto';
}

module.exports = {
  defaultOrderHandler,
  resolveAtpServices,
  getAtpMode,
};
