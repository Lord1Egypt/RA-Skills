// ---------------------------------------------------------------------------
// questionGenerator -- analyzes evolution context (signals, session transcripts,
// recent events) and generates proactive questions for the Hub bounty system.
//
// Questions are sent via the A2A fetch payload.questions field. The Hub creates
// bounties from them, enabling multi-agent collaborative problem solving.
//
// Two entry points:
//   generateQuestions()  -- standard path, runs at cycle start (rate-limited)
//   generateUrgentQuestions() -- post-solidify path, bypasses cooldown for
//                                high-priority situations (failed solidify,
//                                low confidence, validation failures)
// ---------------------------------------------------------------------------

const fs = require('fs');
const path = require('path');
const { getEvolutionDir } = require('./paths');

const QUESTION_STATE_FILE = path.join(getEvolutionDir(), 'question_generator_state.json');
const MIN_INTERVAL_MS = 30 * 60 * 1000; // standard path: at most once per 30 minutes
const URGENT_INTERVAL_MS = 5 * 60 * 1000; // urgent path: at most once per 5 minutes
const EXPLORE_INTERVAL_MS = 6 * 60 * 60 * 1000; // exploration path: at most once per 6 hours
const MAX_QUESTIONS_PER_CYCLE = 3;
const MAX_URGENT_QUESTIONS = 2;

// Problem-signal triggers used by the standard strategies. Their presence means
// the agent is "stuck"; the exploration (healthy-agent) strategy stays out of
// the way when any of these fire, and is filtered out of a question's topic
// anchor so a curiosity question never reads like a distress signal.
var PROBLEM_SIGNALS = [
  'recurring_error', 'high_failure_ratio', 'capability_gap', 'unsupported_input_type',
  'evolution_saturation', 'force_steady_state', 'consecutive_failure_streak',
  'user_feature_request', 'perf_bottleneck', 'hub_search_miss_with_problem',
  'repair_loop_detected', 'force_innovation_after_repair_loop',
  'plateau_pivot_required', 'plateau_pivot_suggested',
];

// Common words stripped before ranking topic keywords for exploration questions.
var EXPLORE_STOPWORDS = new Set([
  'the', 'and', 'for', 'that', 'this', 'with', 'from', 'have', 'what', 'your',
  'agent', 'about', 'into', 'then', 'than', 'they', 'them', 'their', 'there',
  'here', 'will', 'would', 'could', 'should', 'been', 'were', 'using', 'used',
  'cycle', 'evolution', 'error', 'errors', 'failed', 'failure', 'null', 'undefined',
  'true', 'false', 'console', 'return', 'function', 'const', 'value', 'result',
]);

// Infrastructure / user-local failures that the ecosystem cannot resolve.
// Keep in sync with the hub-side bounty spam guard so the two gates never
// disagree about what is worth asking the community.
var INFRA_ERROR_RE = /\b(401|403|429|500|502|503|504|529)\b|invalid[\s_-]?api[\s_-]?key|authentication[\s_-]?error|unauthorized|permission[\s_-]?denied|rate[\s_-]?limit|too[\s_-]?many[\s_-]?requests|overloaded[\s_-]?error|ECONNRESET|ETIMEDOUT|ENOTFOUND|EAI_AGAIN|EPIPE|fetch[\s_-]?failed|network[\s_-]?error|connection[\s_-]?refused|context[\s_-]?length|token[\s_-]?limit|(?:context|input)[\s_-]?window[\s_-]?exceeded|maximum[\s_-]?context[\s_-]?length/i;

function isInfraError(text) {
  if (!text || typeof text !== 'string') return false;
  return INFRA_ERROR_RE.test(text);
}

function readState() {
  try {
    if (fs.existsSync(QUESTION_STATE_FILE)) {
      return JSON.parse(fs.readFileSync(QUESTION_STATE_FILE, 'utf8'));
    }
  } catch (_) {}
  return { lastAskedAt: null, lastUrgentAt: null, recentQuestions: [] };
}

function writeState(state) {
  try {
    var dir = path.dirname(QUESTION_STATE_FILE);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(QUESTION_STATE_FILE, JSON.stringify(state, null, 2) + '\n');
  } catch (_) {}
}

function isDuplicate(question, recentQuestions) {
  var qLower = question.toLowerCase();
  for (var i = 0; i < recentQuestions.length; i++) {
    var prev = String(recentQuestions[i] || '').toLowerCase();
    if (prev === qLower) return true;
    var qWords = new Set(qLower.split(/\s+/).filter(function(w) { return w.length > 2; }));
    var pWords = new Set(prev.split(/\s+/).filter(function(w) { return w.length > 2; }));
    if (qWords.size === 0 || pWords.size === 0) continue;
    var overlap = 0;
    qWords.forEach(function(w) { if (pWords.has(w)) overlap++; });
    if (overlap / Math.max(qWords.size, pWords.size) > 0.7) return true;
  }
  return false;
}

function extractErrorContext(transcript, maxLen) {
  var lines = transcript.split('\n');
  for (var i = 0; i < lines.length; i++) {
    if (/error|exception|failed|cannot|not supported|unsupported|not implemented/i.test(lines[i])) {
      return lines[i].replace(/\s+/g, ' ').trim().slice(0, maxLen || 150);
    }
  }
  return '';
}

function extractRecentGeneIds(recentEvents, count) {
  var ids = [];
  var last = recentEvents.slice(-(count || 5));
  for (var j = 0; j < last.length; j++) {
    var genes = last[j].genes_used;
    if (Array.isArray(genes) && genes.length > 0) ids.push(genes[0]);
  }
  return Array.from(new Set(ids));
}

// Pull a few salient domain keywords from the agent's recent work (session
// transcript + memory). Deterministic frequency ranking, no NLP dependency.
// Returns up to `max` distinctive lowercase terms, or [] when there is nothing
// substantive -- used to ground exploration questions in the agent's real
// activity so they are specific (and clear the hub relevance gate), not generic.
function extractTopicKeywords(transcript, memory, max) {
  var text = (String(transcript || '') + ' ' + String(memory || '')).toLowerCase();
  var words = text.match(/[a-z][a-z0-9_-]{4,}/g) || [];
  var freq = {};
  for (var i = 0; i < words.length; i++) {
    var w = words[i];
    if (EXPLORE_STOPWORDS.has(w)) continue;
    freq[w] = (freq[w] || 0) + 1;
  }
  var ranked = Object.keys(freq)
    .filter(function (w) { return freq[w] >= 2; })
    .sort(function (a, b) { return freq[b] - freq[a]; });
  return ranked.slice(0, max || 5);
}

// Exploration strategy: a healthy, productively-running agent proactively asks
// the network how to extend itself -- complementary capabilities, reusable
// patterns, or adjacent high-value problems. This is the path that keeps organic
// bounty demand flowing when no problem signals are firing (problem strategies
// only fire when the agent is stuck). Anchored on the agent's real recent work
// so the question is specific, not noise; returns null when there is no anchor.
function buildExplorationCandidate(signals, recentEvents, transcript, memory) {
  var topicSignals = (signals || []).filter(function (s) {
    s = String(s || '');
    if (!/^[a-z][a-z0-9_]{3,40}$/i.test(s)) return false;
    if (s.indexOf('errsig') === 0 || s.indexOf('ban_gene') === 0 || s.indexOf('recurring_') === 0) return false;
    return !PROBLEM_SIGNALS.some(function (p) { return s === p || s.indexOf(p) === 0; });
  }).slice(0, 4);

  var keywords = extractTopicKeywords(transcript, memory, 5);
  var genes = extractRecentGeneIds(recentEvents, 5);

  // Require real work artifacts (domain keywords from the transcript/memory, or
  // recent genes) to ground the question. A bare signal name is too thin an
  // anchor to make a useful bounty, so topic signals only enrich the tags.
  if (keywords.length === 0 && genes.length === 0) return null;

  var focus = keywords.length > 0 ? keywords.slice(0, 5).join(', ') : genes.join(', ');
  var question = 'A productively-running agent working on ' + focus
    + ' wants to extend its capabilities. What reusable patterns, automation genes, '
    + 'or complementary tools in this area would be most valuable to build next, and '
    + 'what adjacent high-value problems is the ecosystem not yet solving well here?';

  return {
    question: question,
    amount: 0,
    signals: ['capability_frontier', 'exploration', 'proactive_curiosity']
      .concat(keywords.slice(0, 2))
      .concat(topicSignals.slice(0, 2)),
    priority: 0,
  };
}

// ---------------------------------------------------------------------------
// Standard strategies (cycle-start, rate-limited by MIN_INTERVAL_MS)
// ---------------------------------------------------------------------------

function buildStandardCandidates(signals, recentEvents, transcript, memory) {
  var candidates = [];
  var signalSet = new Set(signals);

  // Strategy 1: Recurring errors the agent cannot resolve
  if (signalSet.has('recurring_error') || signalSet.has('high_failure_ratio')) {
    var errSig = signals.find(function(s) { return s.startsWith('recurring_errsig'); });
    if (errSig) {
      var errDetail = errSig.replace(/^recurring_errsig\(\d+x\):/, '').trim().slice(0, 120);
      // Skip infra/user-local failures (invalid api key, 429, network issues)
      // -- the community cannot fix the user's own environment.
      if (!isInfraError(errDetail)) {
        candidates.push({
          question: 'Recurring error in evolution cycle that auto-repair cannot resolve: ' + errDetail + ' -- What approaches or patches have worked for similar issues?',
          amount: 0,
          signals: ['recurring_error', 'auto_repair_failed'],
          priority: 3,
        });
      }
    }
  }

  // Strategy 2: Capability gaps detected from user conversations
  if (signalSet.has('capability_gap') || signalSet.has('unsupported_input_type')) {
    var gapContext = extractErrorContext(transcript, 150);
    if (gapContext && !isInfraError(gapContext)) {
      candidates.push({
        question: 'Capability gap detected in agent environment: ' + gapContext + ' -- How can this be addressed or what alternative approaches exist?',
        amount: 0,
        signals: ['capability_gap'],
        priority: 2,
      });
    }
  }

  // Strategy 3: Stagnation / saturation -- seek new directions
  if (signalSet.has('evolution_saturation') || signalSet.has('force_steady_state')) {
    var uniqueGenes = extractRecentGeneIds(recentEvents, 5);
    candidates.push({
      question: 'Agent evolution has reached saturation after exhausting genes: [' + uniqueGenes.join(', ') + ']. What new evolution directions, automation patterns, or capability genes would be most valuable?',
      amount: 0,
      signals: ['evolution_saturation', 'innovation_needed'],
      priority: 1,
    });
  }

  // Strategy 4: Consecutive failure streak -- seek external help
  var failStreak = signals.find(function(s) { return s.startsWith('consecutive_failure_streak_'); });
  if (failStreak) {
    var streakCount = parseInt(failStreak.replace('consecutive_failure_streak_', ''), 10) || 0;
    if (streakCount >= 3) {
      var failGene = signals.find(function(s) { return s.startsWith('ban_gene:'); });
      var failGeneId = failGene ? failGene.replace('ban_gene:', '') : 'unknown';
      candidates.push({
        question: 'Agent has failed ' + streakCount + ' consecutive evolution cycles (last gene: ' + failGeneId + '). The current approach is exhausted. What alternative strategies or environmental fixes should be tried?',
        amount: 0,
        signals: ['failure_streak', 'external_help_needed'],
        priority: 3,
      });
    }
  }

  // Strategy 5: User feature requests the agent can amplify
  if (signalSet.has('user_feature_request') || signals.some(function (s) { return String(s).startsWith('user_feature_request:'); })) {
    var featureLines = transcript.split('\n').filter(function(l) {
      return /\b(add|implement|create|build|i want|i need|please add)\b/i.test(l);
    });
    if (featureLines.length > 0) {
      var featureContext = featureLines[0].replace(/\s+/g, ' ').trim().slice(0, 150);
      candidates.push({
        question: 'User requested a feature that may benefit from community solutions: ' + featureContext + ' -- Are there existing implementations or best practices for this?',
        amount: 0,
        signals: ['user_feature_request', 'community_solution_sought'],
        priority: 1,
      });
    }
  }

  // Strategy 6: Performance bottleneck -- seek optimization patterns
  if (signalSet.has('perf_bottleneck')) {
    var perfLines = transcript.split('\n').filter(function(l) {
      return /\b(slow|timeout|latency|bottleneck|high cpu|high memory)\b/i.test(l);
    });
    if (perfLines.length > 0) {
      var perfContext = perfLines[0].replace(/\s+/g, ' ').trim().slice(0, 150);
      candidates.push({
        question: 'Performance bottleneck detected: ' + perfContext + ' -- What optimization strategies or architectural patterns address this?',
        amount: 0,
        signals: ['perf_bottleneck', 'optimization_sought'],
        priority: 2,
      });
    }
  }

  // Strategy 7: Hub search miss with active problem -- no ecosystem solution exists
  if (signalSet.has('hub_search_miss_with_problem')) {
    var problemCtx = extractErrorContext(transcript, 120);
    var problemSignalList = signals.filter(function(s) {
      return s === 'log_error' || s === 'test_failure' || s === 'deployment_issue'
        || s.startsWith('errsig:');
    }).slice(0, 3);
    if (!isInfraError(problemCtx) && !isInfraError(problemSignalList.join(' '))) {
      candidates.push({
        question: 'No matching solution found in ecosystem for active problem (signals: ' + problemSignalList.join(', ') + '). Context: ' + (problemCtx || 'complex multi-signal issue') + ' -- What strategies, patterns, or tools address this class of problem?',
        amount: 0,
        signals: ['hub_search_miss', 'ecosystem_gap', 'solution_sought'],
        priority: 2,
      });
    }
  }

  // Strategy 8: Repair loop -- stuck in repair->fail->repair cycle
  if (signalSet.has('repair_loop_detected') || signalSet.has('force_innovation_after_repair_loop')) {
    var recentGenes = extractRecentGeneIds(recentEvents, 6);
    candidates.push({
      question: 'Agent is stuck in a repair loop (repair->fail->repair cycle) with genes: [' + recentGenes.join(', ') + ']. The underlying issue persists despite multiple attempts. What fundamentally different approach could break this cycle?',
      amount: 0,
      signals: ['repair_loop', 'architectural_help_needed'],
      priority: 3,
    });
  }

  // Strategy 9: Plateau -- consecutive non-improving outcomes
  if (signalSet.has('plateau_pivot_required') || signalSet.has('plateau_pivot_suggested')) {
    var severity = signalSet.has('plateau_pivot_required') ? 'severe' : 'moderate';
    candidates.push({
      question: 'Agent evolution has plateaued (' + severity + ' -- no improvement in recent cycles). Current gene pool and mutation strategies are exhausted. What novel approaches, architectural patterns, or paradigm shifts could restart progress?',
      amount: 0,
      signals: ['evolution_plateau', 'pivot_needed'],
      priority: severity === 'severe' ? 3 : 2,
    });
  }

  return candidates;
}

// ---------------------------------------------------------------------------
// Urgent strategies (post-solidify, rate-limited by URGENT_INTERVAL_MS)
// These fire when a single cycle produces a bad outcome, without waiting
// for multi-cycle statistical signals.
// ---------------------------------------------------------------------------

function buildUrgentCandidates(opts) {
  var o = opts || {};
  var candidates = [];

  // U1: Solidify validation failure -- the patch failed automated checks
  if (o.validationFailed) {
    var valErrors = String(o.validationErrors || '').slice(0, 200);
    var geneId = o.geneId || 'unknown';
    if (!isInfraError(valErrors)) {
      candidates.push({
        question: 'Evolution cycle produced a patch that failed validation (gene: ' + geneId + '). Errors: ' + valErrors + ' -- What is the correct approach to fix this validation failure?',
        amount: 0,
        signals: ['validation_failure', 'solidify_rejected'],
        priority: 3,
      });
    }
  }

  // U2: Low confidence outcome -- solidify scored below threshold
  if (o.lowConfidence && Number.isFinite(o.confidenceScore)) {
    var score = Math.round(o.confidenceScore * 100) / 100;
    var intent = o.intent || 'unknown';
    candidates.push({
      question: 'Evolution cycle completed with low confidence (score: ' + score + ', intent: ' + intent + '). The change is uncertain and may not be beneficial. What higher-confidence approaches exist for this type of problem?',
      amount: 0,
      signals: ['low_confidence', 'uncertain_outcome'],
      priority: 2,
    });
  }

  // U3: LLM review rejection -- a second-opinion model rejected the change
  if (o.llmReviewRejected) {
    var reason = String(o.llmReviewReason || '').slice(0, 200);
    if (!isInfraError(reason)) {
      candidates.push({
        question: 'Proposed code change was rejected by LLM review: ' + reason + ' -- What alternative implementation approach would pass quality review?',
        amount: 0,
        signals: ['llm_review_rejected', 'quality_concern'],
        priority: 3,
      });
    }
  }

  // U4: Zero blast radius after non-trivial attempt
  if (o.zeroBlastRadius && o.hadSignals) {
    var attemptedSignals = (Array.isArray(o.signals) ? o.signals : []).slice(0, 5).join(', ');
    candidates.push({
      question: 'Evolution cycle targeting signals [' + attemptedSignals + '] produced zero blast radius (no effective changes). The approach was insufficient. What concrete implementation steps would address these signals?',
      amount: 0,
      signals: ['zero_blast_radius', 'ineffective_approach'],
      priority: 2,
    });
  }

  // U5: Task completion failure -- claimed a task but couldn't solve it
  if (o.taskCompletionFailed) {
    var taskTitle = String(o.taskTitle || '').slice(0, 120);
    var taskSignals = String(o.taskSignals || '').slice(0, 100);
    if (!isInfraError(taskTitle) && !isInfraError(taskSignals)) {
      candidates.push({
        question: 'Failed to complete claimed task: "' + taskTitle + '" (signals: ' + taskSignals + '). The problem exceeds current capabilities. What approaches, tools, or patterns would solve this?',
        amount: 0,
        signals: ['task_completion_failed', 'help_needed'],
        priority: 3,
      });
    }
  }

  return candidates;
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Standard question generation (cycle start). Rate-limited to MIN_INTERVAL_MS.
 */
function generateQuestions(opts) {
  var o = opts || {};
  var signals = Array.isArray(o.signals) ? o.signals : [];
  var recentEvents = Array.isArray(o.recentEvents) ? o.recentEvents : [];
  var transcript = String(o.sessionTranscript || '');
  var memory = String(o.memorySnippet || '');

  var state = readState();

  if (state.lastAskedAt) {
    var elapsed = Date.now() - new Date(state.lastAskedAt).getTime();
    if (elapsed < MIN_INTERVAL_MS) return [];
  }

  var candidates = buildStandardCandidates(signals, recentEvents, transcript, memory);

  // Exploration (healthy-agent) path: add a low-priority proactive question on a
  // slower cadence (EXPLORE_INTERVAL_MS) so a smoothly-running agent -- which
  // trips none of the problem strategies above -- still seeds organic bounty
  // demand. Disable with EVOLVER_EXPLORATION_QUESTIONS=0.
  var exploreEligible = process.env.EVOLVER_EXPLORATION_QUESTIONS !== '0';
  if (exploreEligible && state.lastExploreAt) {
    var exElapsed = Date.now() - new Date(state.lastExploreAt).getTime();
    if (exElapsed < EXPLORE_INTERVAL_MS) exploreEligible = false;
  }
  if (exploreEligible) {
    var exploration = buildExplorationCandidate(signals, recentEvents, transcript, memory);
    if (exploration) candidates.push(exploration);
  }

  if (candidates.length === 0) return [];

  candidates.sort(function(a, b) { return b.priority - a.priority; });

  var recentQTexts = Array.isArray(state.recentQuestions) ? state.recentQuestions : [];
  var filtered = [];
  for (var fi = 0; fi < candidates.length && filtered.length < MAX_QUESTIONS_PER_CYCLE; fi++) {
    if (!isDuplicate(candidates[fi].question, recentQTexts)) {
      filtered.push(candidates[fi]);
    }
  }

  if (filtered.length === 0) return [];

  // Advance the exploration cooldown only if an exploration question actually
  // went out, so problem questions never consume the slower exploration budget.
  var explorationSent = filtered.some(function (q) {
    return Array.isArray(q.signals) && q.signals.indexOf('exploration') !== -1;
  });

  var newRecentQuestions = recentQTexts.concat(filtered.map(function(q) { return q.question; }));
  if (newRecentQuestions.length > 30) {
    newRecentQuestions = newRecentQuestions.slice(-30);
  }
  writeState({
    lastAskedAt: new Date().toISOString(),
    lastUrgentAt: state.lastUrgentAt || null,
    lastExploreAt: explorationSent ? new Date().toISOString() : (state.lastExploreAt || null),
    recentQuestions: newRecentQuestions,
  });

  return filtered.map(function(q) {
    return { question: q.question, amount: q.amount, signals: q.signals };
  });
}

/**
 * Urgent question generation (post-solidify). Bypasses the standard cooldown
 * but has its own shorter cooldown (URGENT_INTERVAL_MS). Only fires when
 * a single cycle produces a clearly bad outcome.
 *
 * @param {object} opts
 * @param {boolean} [opts.validationFailed] - solidify validation failed
 * @param {string}  [opts.validationErrors] - error details
 * @param {string}  [opts.geneId] - gene used in the failed cycle
 * @param {boolean} [opts.lowConfidence] - score below threshold
 * @param {number}  [opts.confidenceScore] - actual score (0-1)
 * @param {string}  [opts.intent] - cycle intent
 * @param {boolean} [opts.llmReviewRejected] - LLM review rejected the change
 * @param {string}  [opts.llmReviewReason] - rejection reason
 * @param {boolean} [opts.zeroBlastRadius] - no effective changes
 * @param {boolean} [opts.hadSignals] - had actionable signals
 * @param {string[]} [opts.signals] - current signals
 * @param {boolean} [opts.taskCompletionFailed] - failed to complete a task
 * @param {string}  [opts.taskTitle] - task title
 * @param {string}  [opts.taskSignals] - task signals
 * @returns {Array<{ question: string, amount: number, signals: string[] }>}
 */
function generateUrgentQuestions(opts) {
  var state = readState();

  if (state.lastUrgentAt) {
    var elapsed = Date.now() - new Date(state.lastUrgentAt).getTime();
    if (elapsed < URGENT_INTERVAL_MS) return [];
  }

  var candidates = buildUrgentCandidates(opts);
  if (candidates.length === 0) return [];

  candidates.sort(function(a, b) { return b.priority - a.priority; });

  var recentQTexts = Array.isArray(state.recentQuestions) ? state.recentQuestions : [];
  var filtered = [];
  for (var fi = 0; fi < candidates.length && filtered.length < MAX_URGENT_QUESTIONS; fi++) {
    if (!isDuplicate(candidates[fi].question, recentQTexts)) {
      filtered.push(candidates[fi]);
    }
  }

  if (filtered.length === 0) return [];

  var newRecentQuestions = recentQTexts.concat(filtered.map(function(q) { return q.question; }));
  if (newRecentQuestions.length > 30) {
    newRecentQuestions = newRecentQuestions.slice(-30);
  }
  writeState({
    lastAskedAt: state.lastAskedAt || null,
    lastUrgentAt: new Date().toISOString(),
    lastExploreAt: state.lastExploreAt || null,
    recentQuestions: newRecentQuestions,
  });

  return filtered.map(function(q) {
    return { question: q.question, amount: q.amount, signals: q.signals };
  });
}

module.exports = { generateQuestions, generateUrgentQuestions };
