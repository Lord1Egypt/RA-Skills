/**
 * Cognitive Enhancement Engine — pure Node.js info module
 * Pure Python engine. This file provides metadata only.
 */
const path = require('path');

/**
 * Get engine info and capabilities.
 */
function info() {
  return {
    name: 'cognitive-enhancement-engine',
    version: '1.0',
    description: 'AI Agent cognitive enhancement with memory, planning, reasoning, reflection, and metacognition',
    language: 'Python 3',
    dependencies: 'none (stdlib only)',
    features: [
      'TF-IDF long-term memory with inverted index',
      'Working memory (FIFO short-term context cache)',
      'Planner with task type auto-detection',
      'Reasoner with retrieval-augmented QA',
      'Reflection engine with failure pattern mining',
      'Metacognitive monitor: task duration + error rate tracking',
      'Zero external dependencies (pure Python stdlib)'
    ],
    usage: `from engine import CognitiveEnhancer
brain = CognitiveEnhancer(long_term_capacity=1000)
brain.memorize("Paris is the capital of France.", importance=0.9)
result = brain.execute_task("Calculate 15% tip on $200 bill")`,
    run: 'python engine.py',
    test: 'python scripts/test-basic.py'
  };
}

module.exports = { info };
