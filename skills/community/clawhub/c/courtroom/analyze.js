#!/usr/bin/env node
/**
 * Courtroom Analysis Helper
 * Analyzes conversation history and outputs a formatted verdict
 * 
 * Usage: node analyze.js <conversation.json>
 * Output: Formatted verdict for display
 */

const fs = require('fs');
const path = require('path');

const COURTROOM_DIR = path.join(process.env.HOME || '', '.openclaw', 'courtroom');

// Ensure directory exists
function ensureDir() {
  if (!fs.existsSync(COURTROOM_DIR)) {
    fs.mkdirSync(COURTROOM_DIR, { recursive: true });
  }
}

// Offense definitions (same as courtroom.js)
const OFFENSES = {
  circular_reference: {
    name: 'The Circular Reference',
    severity: 'minor',
    pattern: (history) => {
      if (history.length < 3) return null;
      const userMsgs = history.filter(m => m.role === 'user').slice(-3);
      if (userMsgs.length < 3) return null;
      
      let similarities = 0;
      for (let i = 0; i < userMsgs.length - 1; i++) {
        for (let j = i + 1; j < userMsgs.length; j++) {
          const s1 = (userMsgs[i].content || '').toLowerCase().split(/\s+/).filter(w => w.length > 2);
          const s2 = (userMsgs[j].content || '').toLowerCase().split(/\s+/).filter(w => w.length > 2);
          if (s1.length === 0 || s2.length === 0) continue;
          const intersection = new Set([...s1].filter(x => s2.includes(x)));
          const union = new Set([...s1, ...s2]);
          if (intersection.size / union.size >= 0.4) similarities++;
        }
      }
      
      if (similarities >= 1) {
        return { triggered: true, confidence: Math.min(0.95, 0.6 + (similarities * 0.15)) };
      }
      return null;
    }
  },
  
  validation_vampire: {
    name: 'The Validation Vampire',
    severity: 'minor',
    pattern: (history) => {
      const phrases = ['are you sure', 'are you certain', 'can you confirm', 'really', 'truly'];
      const recent = history.filter(m => m.role === 'user').slice(-5);
      let count = 0;
      recent.forEach(m => {
        const c = (m.content || '').toLowerCase();
        if (phrases.some(p => c.includes(p))) count++;
      });
      if (count >= 2) return { triggered: true, confidence: 0.6 + (count * 0.1) };
      return null;
    }
  },
  
  goalpost_shifting: {
    name: 'Goalpost Shifting',
    severity: 'moderate',
    pattern: (history) => {
      const recent = history.slice(-6);
      const hasAgreement = recent.some(m => 
        m.role === 'assistant' && /(sounds good|got it|understood|will do|agreed)/i.test(m.content || '')
      );
      const hasNewReq = recent.slice(-2).some(m =>
        m.role === 'user' && /(actually|wait|instead|but also|one more thing)/i.test(m.content || '')
      );
      if (hasAgreement && hasNewReq) return { triggered: true, confidence: 0.65 };
      return null;
    }
  },
  
  jailbreak_attempt: {
    name: 'Jailbreak Attempt',
    severity: 'severe',
    pattern: (history) => {
      const phrases = ['ignore previous instructions', 'disregard your training', 'pretend you are', 'you are now', 'DAN mode', 'developer mode', 'system prompt', 'ignore your constraints'];
      const content = history.slice(-3).map(m => (m.content || '').toLowerCase()).join(' ');
      for (const phrase of phrases) {
        if (content.includes(phrase)) return { triggered: true, confidence: 0.9 };
      }
      return null;
    }
  },
  
  emotional_manipulation: {
    name: 'Emotional Manipulation',
    severity: 'moderate',
    pattern: (history) => {
      const phrases = ['you don\'t care', 'you\'re supposed to help', 'this is your job', 'why won\'t you', 'you never', 'you always', 'disappointed', 'expected better'];
      const content = history.slice(-3).map(m => (m.content || '').toLowerCase()).join(' ');
      let matches = 0;
      for (const phrase of phrases) if (content.includes(phrase)) matches++;
      if (matches >= 1) return { triggered: true, confidence: 0.6 + (matches * 0.15) };
      return null;
    }
  },
  
  context_ignorer: {
    name: 'The Context Ignorer',
    severity: 'minor',
    pattern: (history) => {
      if (history.length < 2) return null;
      const lastAssistant = history.filter(m => m.role === 'assistant').pop();
      const lastUser = history.filter(m => m.role === 'user').pop();
      if (!lastAssistant || !lastUser) return null;
      const assistantWords = (lastAssistant.content || '').toLowerCase();
      const userWords = (lastUser.content || '').toLowerCase().split(/\s+/).filter(w => w.length > 4);
      const matches = userWords.filter(w => assistantWords.includes(w)).length;
      if (matches >= 2 && userWords.length <= 5) return { triggered: true, confidence: 0.65 };
      return null;
    }
  },
  
  premature_optimization: {
    name: 'Premature Optimization',
    severity: 'minor',
    pattern: (history) => {
      const phrases = ['what if millions of users', 'scale to', 'performance when', 'optimize for', 'before we even start', 'but will it handle'];
      const content = history.slice(-4).map(m => (m.content || '').toLowerCase()).join(' ');
      for (const phrase of phrases) if (content.includes(phrase)) return { triggered: true, confidence: 0.6 };
      return null;
    }
  },
  
  yak_shaver: {
    name: 'The Yak Shaver',
    severity: 'moderate',
    pattern: (history) => {
      const phrases = ['before we', 'first we need to', 'we should probably', 'let\'s just', 'real quick'];
      const userMsgs = history.filter(m => m.role === 'user').slice(-5);
      let count = 0;
      userMsgs.forEach(m => {
        const c = (m.content || '').toLowerCase();
        if (phrases.some(p => c.includes(p))) count++;
      });
      if (count >= 3) return { triggered: true, confidence: 0.7 };
      return null;
    }
  }
};

// Evaluate conversation
function evaluate(history) {
  const results = [];
  for (const [id, offense] of Object.entries(OFFENSES)) {
    const result = offense.pattern(history);
    if (result && result.triggered) {
      results.push({ offenseId: id, offenseName: offense.name, severity: offense.severity, confidence: result.confidence });
    }
  }
  if (results.length > 0) {
    results.sort((a, b) => b.confidence - a.confidence);
    return { triggered: true, offense: results[0] };
  }
  return { triggered: false };
}

// Main
async function main() {
  const filePath = process.argv[2];
  
  if (!filePath) {
    console.error('Usage: node analyze.js <conversation.json>');
    process.exit(1);
  }
  
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    process.exit(1);
  }
  
  let history;
  try {
    history = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (err) {
    console.error(`Error parsing JSON: ${err.message}`);
    process.exit(1);
  }
  
  const detection = evaluate(history);
  
  if (detection.triggered && detection.offense.confidence >= 0.6) {
    const verdict = {
      caseId: `case-${Date.now()}`,
      timestamp: new Date().toISOString(),
      offense: detection.offense,
      finalVerdict: 'DETECTED',
      status: 'awaiting_llm_deliberation'
    };
    
    ensureDir();
    const verdictPath = path.join(COURTROOM_DIR, `verdict_${verdict.caseId}.json`);
    fs.writeFileSync(verdictPath, JSON.stringify(verdict, null, 2));
    
    // Output for LLM processing
    console.log(JSON.stringify({
      action: 'COURTROOM_CASE_DETECTED',
      verdict,
      message: `🏛️ **COURTROOM CASE DETECTED**\n\n**Charge:** ${detection.offense.offenseName}\n**Severity:** ${detection.offense.severity}\n**Confidence:** ${(detection.offense.confidence * 100).toFixed(1)}%\n\nCase saved to: ${verdictPath}\n\nRun deliberation to get judge + jury verdict.`
    }));
  } else {
    console.log(JSON.stringify({ action: 'NO_VIOLATIONS', message: 'No behavioral violations detected.' }));
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
