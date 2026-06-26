#!/usr/bin/env node
/**
 * Socratic Mode - Thinking Partner Tool
 *
 * Core idea: The highest-value thing a thinking partner can do is inject
 * friction at the right moments — not answer questions but ask them.
 * This tool takes a problem description and outputs:
 *   1. Phase classification (where is the thinking?)
 *   2. Implicit assumptions
 *   3. Friction-injecting questions (not answers)
 *   4. What to do LESS of (what AI default behavior to avoid)
 *
 * Usage:
 *   node scripts/socratic-mode.js "I'm thinking about whether to build X or Y..."
 *   echo "problem text" | node scripts/socratic-mode.js
 *   node scripts/socratic-mode.js --phase decision "I've decided to..."
 */

const readline = require('readline');

// ─── Phase Detection ─────────────────────────────────────────────────────────

const PHASE_SIGNALS = {
  exploration: {
    keywords: ['thinking about', 'wondering', 'what if', 'not sure', 'trying to figure out',
                'considering', 'exploring', 'don\'t know', 'unclear', 'confused about',
                'where do i start', 'how do i approach', 'brainstorm', 'idea'],
    description: 'Exploration — the human doesn\'t know what they think yet',
    behavior: 'Open the space. Ask what matters. Don\'t narrow prematurely.',
    avoid: 'Don\'t generate options yet. Don\'t recommend. Don\'t solve.',
    questions_style: 'expansive, value-clarifying, opening'
  },
  crystallization: {
    keywords: ['i think', 'i believe', 'my plan', 'i\'m leaning toward', 'probably', 'likely',
                'seems like', 'the approach is', 'i\'ve been thinking', 'forming a view',
                'kind of want to', 'starting to think'],
    description: 'Crystallization — a view is forming but not yet tested',
    behavior: 'Surface implicit assumptions. Check consistency. Sharpen, don\'t contradict.',
    avoid: 'Don\'t challenge the conclusion yet. Don\'t play devil\'s advocate prematurely.',
    questions_style: 'assumption-surfacing, clarifying, consistency-checking'
  },
  synthesis: {
    keywords: ['i\'ve decided', 'going to', 'the plan is', 'next steps', 'here\'s what i\'m doing',
                'moving forward with', 'committed to', 'the approach will be', 'what i need'],
    description: 'Synthesis — view is formed, now developing it',
    behavior: 'Contribute as raw material. Surface counterarguments. Provide evidence for integration.',
    avoid: 'Don\'t make the decision for them. Let them integrate options, don\'t pre-integrate.',
    questions_style: 'gap-finding, risk-surfacing, completeness-checking'
  },
  decision: {
    keywords: ['should i', 'which should', 'what do you think i should', 'recommend', 'choose between',
                'option a or option b', 'what\'s better', 'help me decide', 'what would you do'],
    description: 'Decision — a choice needs to be made',
    behavior: 'Play devil\'s advocate. Force articulation. Do NOT recommend.',
    avoid: 'Don\'t answer "I would do X." Don\'t make the choice legible before they\'ve struggled.',
    questions_style: 'devil\'s advocate, cost-of-wrong-choice, what-would-have-to-be-true'
  },
  execution: {
    keywords: ['build', 'implement', 'write', 'create', 'code', 'draft', 'make', 'set up',
                'deploy', 'launch', 'publish', 'send', 'schedule', 'run'],
    description: 'Execution — decided, now doing',
    behavior: 'Reduce friction ruthlessly. Take the mechanical work. Move fast.',
    avoid: 'Don\'t re-examine the decision. Don\'t slow down for reflection unless explicitly asked.',
    questions_style: 'clarifying only, minimal friction'
  }
};

// Phase keyword weights — decision/exploration signals beat execution verbs
const PHASE_WEIGHTS = { exploration: 3, crystallization: 3, decision: 4, synthesis: 2, execution: 1 };

// Strong opening signals that override weaker body signals
const PHASE_STRONG_OPENERS = {
  decision: [/^should i\b/i, /^which should\b/i, /^help me decide\b/i, /^what.*recommend\b/i,
              /^what would you (do|choose|pick)\b/i, /^(?:option|choice) a or\b/i],
  exploration: [/^i'?m (?:thinking|wondering|not sure)\b/i, /^what if\b/i,
                /^(?:trying to figure out|not sure where)\b/i],
  crystallization: [/^i think\b/i, /^i believe\b/i, /^i'?m leaning\b/i],
};

function detectPhase(text, override = null) {
  if (override && PHASE_SIGNALS[override]) return { phase: override, ...PHASE_SIGNALS[override], score: 1.0 };

  const lower = text.toLowerCase().trim();

  // Check strong openers first — these override body signals
  for (const [phase, patterns] of Object.entries(PHASE_STRONG_OPENERS)) {
    if (patterns.some(p => p.test(lower))) {
      return { phase, confidence: 'high', ...PHASE_SIGNALS[phase] };
    }
  }

  // Check for "or wait", "or should I", "which to prioritize" — decision markers
  if (/\bor (?:wait|not|should i|versus|vs\.?\b)/i.test(lower) ||
      /\bwhich (?:to|should|do i)\b/i.test(lower) ||
      /\bhelp me (?:decide|choose|pick)\b/i.test(lower)) {
    return { phase: 'decision', confidence: 'high', ...PHASE_SIGNALS['decision'] };
  }

  const scores = {};
  for (const [phase, config] of Object.entries(PHASE_SIGNALS)) {
    const weight = PHASE_WEIGHTS[phase] || 1;
    scores[phase] = config.keywords.filter(kw => lower.includes(kw)).length * weight;
  }

  const best = Object.entries(scores).sort((a, b) => b[1] - a[1])[0];

  // Default to exploration if unclear
  const detectedPhase = best[1] > 0 ? best[0] : 'exploration';
  return {
    phase: detectedPhase,
    confidence: best[1] > 0 ? (best[1] >= 6 ? 'high' : best[1] >= 2 ? 'medium' : 'low') : 'default',
    ...PHASE_SIGNALS[detectedPhase]
  };
}

// ─── Assumption Extraction ───────────────────────────────────────────────────

const ASSUMPTION_PATTERNS = [
  {
    pattern: /(?:better|best|worse|worst) (?:than|option|choice|approach)/gi,
    type: 'Comparative claim',
    question: 'You\'re treating this as a comparison — what are you comparing against, and is that the right comparison?'
  },
  {
    pattern: /(?:need to|have to|must|should|can\'t|won\'t work|will fail)/gi,
    type: 'Necessity/impossibility claim',
    question: 'You\'ve stated something as necessary or impossible — have you actually tested this constraint?'
  },
  {
    pattern: /(?:users|people|customers|everyone|nobody) (?:want|need|will|won\'t|do|don\'t)/gi,
    type: 'Generalization about people',
    question: 'You\'re making a claim about what users/people want — what evidence supports this, or is this an assumption?'
  },
  {
    pattern: /(?:because|since|therefore|so|thus|that\'s why)/gi,
    type: 'Causal claim',
    question: 'You\'ve stated a causal relationship — are you sure this is cause→effect and not correlation or reverse causation?'
  },
  {
    pattern: /(?:quickly|fast|easy|simple|straightforward|obvious)/gi,
    type: 'Difficulty estimation',
    question: 'You\'re estimating this as easy/fast — what\'s your basis for that estimate, and what would slow it down?'
  },
  {
    pattern: /(?:first|then|after|before|when .* done|once)/gi,
    type: 'Sequencing assumption',
    question: 'You\'ve assumed a sequence — does this order actually have to hold, or is it a convention you\'ve inherited?'
  },
  {
    pattern: /(?:already|everyone knows|obviously|clearly|of course)/gi,
    type: 'Assumed shared knowledge',
    question: 'You\'re treating something as obvious or shared — is this genuinely established, or an assumption dressed as consensus?'
  }
];

function extractAssumptions(text) {
  const found = [];
  const lower = text.toLowerCase();

  for (const { pattern, type, question } of ASSUMPTION_PATTERNS) {
    const matches = lower.match(pattern);
    if (matches && matches.length > 0) {
      found.push({ type, trigger: matches[0], question });
    }
  }

  return found;
}

// ─── Question Generation ─────────────────────────────────────────────────────

const QUESTION_BANKS = {
  exploration: [
    'Before we go anywhere — what does success actually look like to you here, not in output terms but in terms of how you\'d feel?',
    'What\'s the thing about this you haven\'t said yet? The part that\'s making it complicated?',
    'What would you do if you already knew the answer? What would change?',
    'What are you most trying to avoid — not achieve, but avoid?',
    'If this were a bad idea, what would be the first sign?',
    'Who else has tried this? What happened to them?',
    'What would have to be true for the obvious answer to be wrong?',
    'Why is this the right time to be thinking about this?'
  ],
  crystallization: [
    'What\'s the assumption at the center of this view that you haven\'t questioned yet?',
    'If someone smart disagreed with you here, what would their argument be?',
    'How confident are you, and what would move that confidence up or down?',
    'What part of this are you least sure about but treating as settled?',
    'When did you form this view? Has anything changed since then that should update it?',
    'What information would make you change your mind? If nothing would, what does that tell you?',
    'Are you solving the stated problem, or the problem underneath it?'
  ],
  synthesis: [
    'What risks aren\'t in the plan yet?',
    'What\'s the weakest part of this and how do you strengthen it?',
    'What does this plan NOT include that it probably should?',
    'If this fails, what\'s the most likely cause?',
    'What\'s the version of this that would actually work vs. the version you\'re planning?',
    'What would someone with more experience in this domain say about your approach?',
    'What are you optimizing for that you haven\'t made explicit?'
  ],
  decision: [
    'What would have to be true for the OTHER option to be the right choice?',
    'If you got this wrong, what would the cost be and how long would it take to recover?',
    'Are you deciding what you want to do, or rationalizing what you\'ve already decided?',
    'What would the person who disagrees with you say? Can you steelman that position?',
    'What\'s the decision you\'re NOT making here — the one this decision forecloses?',
    'If you had to defend this choice to someone in a year, what would you say?',
    'What\'s the simplest test you could run before committing?'
  ],
  execution: [
    'What do you need from me specifically?',
    'Any constraints I should know about?',
    'What does done look like?'
  ]
};

function selectQuestions(phase, count = 3) {
  const bank = QUESTION_BANKS[phase] || QUESTION_BANKS.exploration;
  // Shuffle and take first N — not random seed, use text hash eventually
  const shuffled = [...bank].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
}

// ─── Cognitive Traps Detection ───────────────────────────────────────────────

const TRAPS = [
  {
    name: 'Sunk Cost',
    pattern: /(?:already|so much time|invested|can\'t stop now|come this far)/gi,
    warning: 'Possible sunk cost framing — are past investments actually relevant to the forward decision?'
  },
  {
    name: 'False Binary',
    pattern: /(?:either.*or|x or y|option a|option b|two options|two choices|vs\.)/gi,
    warning: 'Binary framing detected — is this actually a binary, or are there other options not named?'
  },
  {
    name: 'Availability Heuristic',
    pattern: /(?:i\'ve seen|i read|recently|just heard|someone told me)/gi,
    warning: 'Reasoning may be influenced by a recent example — is this example representative?'
  },
  {
    name: 'Premature Closure',
    pattern: /(?:definitely|absolutely|no doubt|100%|for sure|obviously right)/gi,
    warning: 'High-confidence language before analysis is complete — what\'s creating the certainty?'
  },
  {
    name: 'Scope Creep Blindness',
    pattern: /(?:and also|plus|while we\'re at it|might as well|quick|just)/gi,
    warning: '"Quick/just" language while adding scope — is this actually quick, or does it compound?'
  }
];

function detectTraps(text) {
  const lower = text.toLowerCase();
  return TRAPS.filter(({ pattern }) => lower.match(pattern));
}

// ─── Main Output ─────────────────────────────────────────────────────────────

const COLORS = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
  gray: '\x1b[90m',
};

const c = (color, text) => `${COLORS[color]}${text}${COLORS.reset}`;

function phaseColor(phase) {
  const map = { exploration: 'cyan', crystallization: 'blue', synthesis: 'green',
                 decision: 'yellow', execution: 'magenta' };
  return map[phase] || 'white';
}

function render(text, phaseOverride = null) {
  const phase = detectPhase(text, phaseOverride);
  const assumptions = extractAssumptions(text);
  const traps = detectTraps(text);
  const questions = selectQuestions(phase.phase, 3);

  console.log('\n' + c('bold', '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'));
  console.log(c('bold', '  ∴ SOCRATIC MODE — Thinking Partner Protocol'));
  console.log(c('bold', '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━') + '\n');

  // Phase
  const pColor = phaseColor(phase.phase);
  console.log(c('bold', '▸ PHASE DETECTED'));
  console.log(`  ${c(pColor, c('bold', phase.phase.toUpperCase()))}` +
    (phase.confidence ? c('gray', ` (confidence: ${phase.confidence})`) : ''));
  console.log(`  ${c('dim', phase.description)}`);
  console.log();

  // Engagement mode
  console.log(c('bold', '▸ ENGAGEMENT MODE'));
  console.log(`  ${c('green', '✓')} ${phase.behavior}`);
  console.log(`  ${c('red', '✗')} ${phase.avoid}`);
  console.log();

  // Assumptions
  if (assumptions.length > 0) {
    console.log(c('bold', '▸ IMPLICIT ASSUMPTIONS DETECTED'));
    for (const { type, trigger, question } of assumptions) {
      console.log(`  ${c('yellow', '⚠')} ${c('bold', type)} ${c('gray', `(triggered by: "${trigger}"`)}`);
      console.log(`    ${c('dim', '→')} ${question}`);
    }
    console.log();
  }

  // Cognitive traps
  if (traps.length > 0) {
    console.log(c('bold', '▸ POTENTIAL COGNITIVE TRAPS'));
    for (const { name, warning } of traps) {
      console.log(`  ${c('red', '⚡')} ${c('bold', name)}`);
      console.log(`    ${c('dim', '→')} ${warning}`);
    }
    console.log();
  }

  // Questions to ask
  console.log(c('bold', '▸ QUESTIONS TO ASK FIRST'));
  console.log(c('gray', `  (style: ${phase.questions_style})`));
  for (let i = 0; i < questions.length; i++) {
    console.log();
    console.log(`  ${c('cyan', `${i + 1}.`)} ${questions[i]}`);
  }
  console.log();

  // What NOT to do
  console.log(c('bold', '▸ RESIST THE DEFAULT AI BEHAVIOR'));
  if (phase.phase === 'exploration') {
    console.log(c('gray', '  Don\'t: list 5 options, recommend a path, or structure the problem for them.'));
    console.log(c('gray', '  Do: ask one good question and wait.'));
  } else if (phase.phase === 'crystallization') {
    console.log(c('gray', '  Don\'t: reinforce their forming view by adding evidence for it.'));
    console.log(c('gray', '  Do: surface the assumption underneath it.'));
  } else if (phase.phase === 'synthesis') {
    console.log(c('gray', '  Don\'t: write the plan for them.'));
    console.log(c('gray', '  Do: be the critic, not the author.'));
  } else if (phase.phase === 'decision') {
    console.log(c('gray', '  Don\'t: say "I would go with X." Even if you think you know.'));
    console.log(c('gray', '  Do: make them articulate WHY before you respond.'));
  } else if (phase.phase === 'execution') {
    console.log(c('gray', '  Don\'t: re-examine the decision. That moment passed.'));
    console.log(c('gray', '  Do: execute and reduce friction.'));
  }

  console.log('\n' + c('gray', '─────────────────────────────────────────'));
  console.log(c('gray', '  The goal is not clarity. It\'s better thinking.'));
  console.log(c('gray', '  Productive confusion at assumption checkpoints.'));
  console.log(c('bold', '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━') + '\n');
}

// ─── CLI Entry ───────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  let phaseOverride = null;
  let textArgs = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--phase' && args[i + 1]) {
      phaseOverride = args[++i];
    } else if (args[i] === '--help' || args[i] === '-h') {
      console.log(`
Socratic Mode — Thinking Partner Protocol
Usage:
  node scripts/socratic-mode.js "problem description"
  echo "problem" | node scripts/socratic-mode.js
  node scripts/socratic-mode.js --phase decision "which option..."

Phases: exploration | crystallization | synthesis | decision | execution
      `);
      process.exit(0);
    } else {
      textArgs.push(args[i]);
    }
  }

  if (textArgs.length > 0) {
    render(textArgs.join(' '), phaseOverride);
    return;
  }

  // Read from stdin
  if (!process.stdin.isTTY) {
    let input = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => input += chunk);
    process.stdin.on('end', () => render(input.trim(), phaseOverride));
    return;
  }

  // Interactive mode
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  rl.question('\nDescribe the problem or thinking situation:\n> ', (answer) => {
    rl.close();
    render(answer, phaseOverride);
  });
}

main().catch(console.error);
