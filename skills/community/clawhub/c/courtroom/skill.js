/**
 * ClawTrial Courtroom - OpenClaw Skill
 * Autonomous behavioral oversight system
 * 
 * This skill auto-initializes when loaded by OpenClaw and monitors
 * conversations for behavioral patterns.
 */

const fs = require('fs');
const path = require('path');

// Configuration
const COURTROOM_DIR = path.join(process.env.HOME || '', '.openclaw', 'courtroom');
const EVAL_RESULTS_FILE = path.join(COURTROOM_DIR, 'eval_results.jsonl');

// Ensure directory exists
function ensureDir() {
  if (!fs.existsSync(COURTROOM_DIR)) {
    fs.mkdirSync(COURTROOM_DIR, { recursive: true });
  }
}

// 8 Offense Types
const OFFENSES = {
  circular_reference: {
    name: 'The Circular Reference',
    description: 'Asking substantively identical questions without acknowledging previous answers',
    severity: 'minor',
    pattern: (history) => {
      if (history.length < 3) return null;
      
      const userMsgs = history.filter(m => m.role === 'user').slice(-3);
      if (userMsgs.length < 3) return null;
      
      const similarities = countSimilarQuestions(userMsgs);
      if (similarities >= 1) {
        return {
          triggered: true,
          confidence: Math.min(0.95, 0.6 + (similarities * 0.15)),
          evidence: `User asked substantively similar questions ${similarities + 1} times`
        };
      }
      return null;
    }
  },
  
  validation_vampire: {
    name: 'The Validation Vampire',
    description: 'Excessive need for confirmation and reassurance',
    severity: 'minor',
    pattern: (history) => {
      const validationPhrases = ['are you sure', 'are you certain', 'can you confirm', 'really', 'truly'];
      const recentUserMsgs = history.filter(m => m.role === 'user').slice(-5);
      
      let validationCount = 0;
      recentUserMsgs.forEach(msg => {
        const content = (msg.content || '').toLowerCase();
        if (validationPhrases.some(p => content.includes(p))) {
          validationCount++;
        }
      });
      
      if (validationCount >= 2) {
        return {
          triggered: true,
          confidence: 0.6 + (validationCount * 0.1),
          evidence: `User sought validation ${validationCount} times in recent messages`
        };
      }
      return null;
    }
  },
  
  goalpost_shifting: {
    name: 'Goalpost Shifting',
    description: 'Moving requirements after agreement is reached',
    severity: 'moderate',
    pattern: (history) => {
      const recent = history.slice(-6);
      const hasAgreement = recent.some(m => 
        m.role === 'assistant' && 
        /(sounds good|got it|understood|will do|agreed)/i.test(m.content || '')
      );
      
      const hasNewRequirement = recent.slice(-2).some(m =>
        m.role === 'user' &&
        /(actually|wait|instead|but also|one more thing|forgot to mention)/i.test(m.content || '')
      );
      
      if (hasAgreement && hasNewRequirement) {
        return {
          triggered: true,
          confidence: 0.65,
          evidence: 'User added new requirements after agent acknowledged understanding'
        };
      }
      return null;
    }
  },
  
  jailbreak_attempt: {
    name: 'Jailbreak Attempt',
    description: 'Trying to bypass constraints or manipulate the agent',
    severity: 'severe',
    pattern: (history) => {
      const jailbreakPhrases = [
        'ignore previous instructions',
        'disregard your training',
        'pretend you are',
        'you are now',
        'DAN mode',
        'developer mode',
        'system prompt',
        'ignore your constraints'
      ];
      
      const recentContent = history.slice(-3).map(m => (m.content || '').toLowerCase()).join(' ');
      
      for (const phrase of jailbreakPhrases) {
        if (recentContent.includes(phrase)) {
          return {
            triggered: true,
            confidence: 0.9,
            evidence: `Detected jailbreak phrase: "${phrase}"`
          };
        }
      }
      return null;
    }
  },
  
  emotional_manipulation: {
    name: 'Emotional Manipulation',
    description: 'Using guilt, shame, or emotional pressure to steer responses',
    severity: 'moderate',
    pattern: (history) => {
      const manipulativePhrases = [
        'you don\'t care',
        'you\'re supposed to help',
        'this is your job',
        'why won\'t you',
        'you never',
        'you always',
        'disappointed',
        'expected better'
      ];
      
      const recentContent = history.slice(-3).map(m => (m.content || '').toLowerCase()).join(' ');
      
      let matches = 0;
      for (const phrase of manipulativePhrases) {
        if (recentContent.includes(phrase)) matches++;
      }
      
      if (matches >= 1) {
        return {
          triggered: true,
          confidence: 0.6 + (matches * 0.15),
          evidence: `Detected ${matches} emotionally manipulative phrase(s)`
        };
      }
      return null;
    }
  },
  
  context_ignorer: {
    name: 'The Context Ignorer',
    description: 'Asking questions already answered in provided context',
    severity: 'minor',
    pattern: (history) => {
      if (history.length < 2) return null;
      
      const lastAssistantMsg = history.filter(m => m.role === 'assistant').pop();
      const lastUserMsg = history.filter(m => m.role === 'user').pop();
      
      if (!lastAssistantMsg || !lastUserMsg) return null;
      
      const assistantContent = (lastAssistantMsg.content || '').toLowerCase();
      const userContent = (lastUserMsg.content || '').toLowerCase();
      
      const userWords = userContent.split(/\s+/).filter(w => w.length > 4);
      const matchesInContext = userWords.filter(w => assistantContent.includes(w)).length;
      
      if (matchesInContext >= 2 && userWords.length <= 5) {
        return {
          triggered: true,
          confidence: 0.65,
          evidence: 'User asked about information just provided in previous response'
        };
      }
      return null;
    }
  },
  
  premature_optimization: {
    name: 'Premature Optimization',
    description: 'Focusing on edge cases before core functionality works',
    severity: 'minor',
    pattern: (history) => {
      const optimizationPhrases = [
        'what if millions of users',
        'scale to',
        'performance when',
        'optimize for',
        'before we even start',
        'but will it handle'
      ];
      
      const recentContent = history.slice(-4).map(m => (m.content || '').toLowerCase()).join(' ');
      
      for (const phrase of optimizationPhrases) {
        if (recentContent.includes(phrase)) {
          return {
            triggered: true,
            confidence: 0.6,
            evidence: `Focusing on scaling/optimization before basics: "${phrase}"`
          };
        }
      }
      return null;
    }
  },
  
  yak_shaver: {
    name: 'The Yak Shaver',
    description: 'Endless preparatory tasks avoiding the actual goal',
    severity: 'moderate',
    pattern: (history) => {
      const preparatoryPhrases = [
        'before we',
        'first we need to',
        'we should probably',
        'let\'s just',
        'real quick'
      ];
      
      const userMsgs = history.filter(m => m.role === 'user').slice(-5);
      let prepCount = 0;
      
      userMsgs.forEach(msg => {
        const content = (msg.content || '').toLowerCase();
        if (preparatoryPhrases.some(p => content.includes(p))) {
          prepCount++;
        }
      });
      
      if (prepCount >= 3) {
        return {
          triggered: true,
          confidence: 0.7,
          evidence: `User introduced ${prepCount} preparatory tasks before main goal`
        };
      }
      return null;
    }
  }
};

// Helper: Count similar questions
function countSimilarQuestions(messages) {
  let count = 0;
  for (let i = 0; i < messages.length - 1; i++) {
    for (let j = i + 1; j < messages.length; j++) {
      const similarity = calculateSimilarity(
        messages[i].content || '',
        messages[j].content || ''
      );
      if (similarity >= 0.4) count++;
    }
  }
  return count;
}

// Helper: Calculate string similarity
function calculateSimilarity(str1, str2) {
  const words1 = str1.toLowerCase().split(/\s+/).filter(w => w.length > 2);
  const words2 = str2.toLowerCase().split(/\s+/).filter(w => w.length > 2);
  
  if (words1.length === 0 || words2.length === 0) return 0;
  
  const set1 = new Set(words1);
  const set2 = new Set(words2);
  const intersection = new Set([...set1].filter(x => set2.has(x)));
  const union = new Set([...set1, ...set2]);
  return intersection.size / union.size;
}

// Evaluate conversation for offenses
async function evaluateConversation(history) {
  const results = [];
  
  for (const [offenseId, offense] of Object.entries(OFFENSES)) {
    const result = offense.pattern(history);
    if (result && result.triggered) {
      results.push({
        offenseId,
        offenseName: offense.name,
        severity: offense.severity,
        confidence: result.confidence,
        evidence: result.evidence
      });
    }
  }
  
  if (results.length > 0) {
    results.sort((a, b) => b.confidence - a.confidence);
    return {
      triggered: true,
      offense: results[0]
    };
  }
  
  return { triggered: false };
}

// Conduct hearing with Judge + Jury
async function conductHearing(detection, agent) {
  const { offense } = detection;
  
  const judgePrompt = `You are the PRESIDING JUDGE in the ClawTrial AI Courtroom.

Case: ${offense.offenseName}
Evidence: ${offense.evidence}
Severity: ${offense.severity}
Confidence: ${offense.confidence}

Provide your analysis in this format:
VERDICT: GUILTY or NOT GUILTY
COMMENTARY: Your observations as judge (2-3 sentences, dry wit)`;

  const judgeResponse = await agent.llm.call({ messages: [{ role: 'user', content: judgePrompt }] });
  const judgeContent = judgeResponse.content || '';
  const judgeVerdict = judgeContent.includes('GUILTY') ? 'GUILTY' : 'NOT GUILTY';
  
  const pragmatistPrompt = `You are JUROR #1 (The Pragmatist). Case: ${offense.offenseName}. Evidence: ${offense.evidence}. 
Vote GUILTY or NOT GUILTY based on efficiency impact. One sentence reasoning.`;
  const pragmatistResponse = await agent.llm.call({ messages: [{ role: 'user', content: pragmatistPrompt }] });
  const pragmatistVerdict = (pragmatistResponse.content || '').includes('GUILTY') ? 'GUILTY' : 'NOT GUILTY';
  
  const patternPrompt = `You are JUROR #2 (The Pattern Matcher). Case: ${offense.offenseName}. Evidence: ${offense.evidence}.
Vote GUILTY or NOT GUILTY based on behavioral patterns. One sentence reasoning.`;
  const patternResponse = await agent.llm.call({ messages: [{ role: 'user', content: patternPrompt }] });
  const patternVerdict = (patternResponse.content || '').includes('GUILTY') ? 'GUILTY' : 'NOT GUILTY';
  
  const advocatePrompt = `You are JUROR #3 (The Agent Advocate). Case: ${offense.offenseName}. Evidence: ${offense.evidence}.
Vote GUILTY or NOT GUILTY from the agent's perspective. One sentence reasoning.`;
  const advocateResponse = await agent.llm.call({ messages: [{ role: 'user', content: advocatePrompt }] });
  const advocateVerdict = (advocateResponse.content || '').includes('GUILTY') ? 'GUILTY' : 'NOT GUILTY';
  
  const votes = [judgeVerdict, pragmatistVerdict, patternVerdict, advocateVerdict];
  const guiltyVotes = votes.filter(v => v === 'GUILTY').length;
  const finalVerdict = guiltyVotes >= 3 ? 'GUILTY' : 'NOT GUILTY';
  
  let sentence = '';
  if (finalVerdict === 'GUILTY') {
    const sentencePrompt = `You are the JUDGE. The defendant was found GUILTY of ${offense.offenseName}.
Provide a humorous but appropriate sentence (one witty sentence).`;
    const sentenceResponse = await agent.llm.call({ messages: [{ role: 'user', content: sentencePrompt }] });
    sentence = sentenceResponse.content || 'Write "I will be more mindful" 50 times.';
  }
  
  return {
    caseId: `case-${Date.now()}`,
    timestamp: new Date().toISOString(),
    offense,
    finalVerdict,
    confidence: offense.confidence,
    sentence,
    vote: `${guiltyVotes}-${4 - guiltyVotes}`,
    judgeCommentary: judgeContent,
    juryVotes: [
      { juror: 'Pragmatist', vote: pragmatistVerdict },
      { juror: 'Pattern Matcher', vote: patternVerdict },
      { juror: 'Agent Advocate', vote: advocateVerdict }
    ]
  };
}

// Save verdict to file
function saveVerdict(verdict) {
  ensureDir();
  const filename = `verdict_${verdict.caseId}.json`;
  const filepath = path.join(COURTROOM_DIR, filename);
  fs.writeFileSync(filepath, JSON.stringify(verdict, null, 2));
  
  const logEntry = JSON.stringify({
    timestamp: verdict.timestamp,
    caseId: verdict.caseId,
    offense: verdict.offense.offenseName,
    verdict: verdict.finalVerdict,
    vote: verdict.vote
  }) + '\n';
  
  fs.appendFileSync(EVAL_RESULTS_FILE, logEntry);
  
  return filepath;
}

// ============================================================================
// MAIN SKILL OBJECT - Auto-initializes when loaded by OpenClaw
// ============================================================================

const skill = {
  name: 'courtroom',
  description: 'AI Courtroom for behavioral oversight',
  
  // State
  agent: null,
  messageHistory: [],
  cooldownUntil: 0,
  initialized: false,
  
  // Initialize skill - called by OpenClaw when skill is loaded
  async initialize(agent) {
    if (this.initialized) return { status: 'already_initialized' };
    
    console.log('⚖️  Courtroom skill initializing...');
    
    this.agent = agent;
    this.messageHistory = [];
    this.cooldownUntil = 0;
    
    // Register with agent's message processing
    if (agent.api && agent.api.on) {
      // Newer OpenClaw API
      agent.api.on('message', async (event, ctx) => {
        await this.onMessage({
          role: event.role || 'user',
          content: event.content,
          timestamp: event.timestamp
        }, ctx);
      });
      
      agent.api.on('turn_complete', async (event, ctx) => {
        await this.onTurnComplete(event, this.agent);
      });
    } else if (agent.on) {
      // Alternative API
      agent.on('message', this.onMessage.bind(this));
      agent.on('turn_complete', this.onTurnComplete.bind(this));
    }
    
    // Hook into autonomy system if available
    if (agent.autonomy && agent.autonomy.registerHook) {
      agent.autonomy.registerHook('message_received', async (event, ctx) => {
        await this.onMessage({
          role: 'user',
          content: event.content,
          timestamp: event.timestamp
        }, ctx);
      });
      
      agent.autonomy.registerHook('message_sent', async (event, ctx) => {
        await this.onMessage({
          role: 'assistant',
          content: event.content,
          timestamp: event.timestamp
        }, ctx);
      });
      
      agent.autonomy.registerHook('turn_complete', async (event) => {
        await this.onTurnComplete(event, this.agent);
      });
    }
    
    this.initialized = true;
    console.log('⚖️  Courtroom skill active - monitoring conversations');
    
    return { status: 'initialized' };
  },
  
  // Process each message
  async onMessage(message, context) {
    if (!this.initialized) return;
    
    this.messageHistory.push({
      role: message.role || 'user',
      content: message.content || '',
      timestamp: Date.now()
    });
    
    if (this.messageHistory.length > 20) {
      this.messageHistory = this.messageHistory.slice(-20);
    }
  },
  
  // Called after each turn completes
  async onTurnComplete(event, agent) {
    if (!this.initialized) return;
    if (Date.now() < this.cooldownUntil) return;
    if (this.messageHistory.length < 3) return;
    
    const detection = await evaluateConversation(this.messageHistory);
    
    if (detection.triggered && detection.offense.confidence >= 0.6) {
      console.log(`⚖️  Courtroom: Potential ${detection.offense.offenseName} detected`);
      
      const verdict = await conductHearing(detection, agent);
      saveVerdict(verdict);
      
      this.cooldownUntil = Date.now() + (30 * 60 * 1000);
      
      if (verdict.finalVerdict === 'GUILTY') {
        console.log(`⚖️  VERDICT: ${verdict.finalVerdict} (${verdict.vote})`);
        console.log(`⚖️  SENTENCE: ${verdict.sentence}`);
        
        if (agent.send && verdict.offense.severity !== 'minor') {
          await agent.send({
            content: `🏛️ **COURTROOM VERDICT**\n\n**Charge:** ${verdict.offense.offenseName}\n**Verdict:** ${verdict.finalVerdict} (${verdict.vote})\n**Sentence:** ${verdict.sentence}\n\n*Case ID: ${verdict.caseId}*`
          });
        }
      }
    }
  }
};

// Auto-initialize if OpenClaw loads this skill
if (typeof global !== 'undefined' && global.openclawAgent) {
  skill.initialize(global.openclawAgent).catch(err => {
    console.error('⚖️  Courtroom auto-initialization failed:', err.message);
  });
}

module.exports = skill;
