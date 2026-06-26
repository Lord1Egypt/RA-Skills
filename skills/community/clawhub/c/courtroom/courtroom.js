#!/usr/bin/env node
/**
 * ClawTrial Courtroom - CLI Entry Point
 * Run via: openclaw run courtroom
 */

const fs = require('fs');
const path = require('path');

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
function evaluateConversation(history) {
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

// Conduct hearing (simplified - returns detection for LLM to process)
function conductHearing(detection) {
  const { offense } = detection;
  
  return {
    caseId: `case-${Date.now()}`,
    timestamp: new Date().toISOString(),
    offense,
    status: 'pending_llm_deliberation'
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
    offense: verdict.offense?.offenseName || 'Unknown',
    verdict: verdict.finalVerdict || 'PENDING',
    vote: verdict.vote || 'N/A'
  }) + '\n';
  
  fs.appendFileSync(EVAL_RESULTS_FILE, logEntry);
  
  return filepath;
}

// Main CLI
async function main() {
  const args = process.argv.slice(2);
  const fileIndex = args.indexOf('--file');
  const filePath = fileIndex !== -1 ? args[fileIndex + 1] : null;
  
  ensureDir();
  
  let history = [];
  
  if (filePath && fs.existsSync(filePath)) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      history = JSON.parse(content);
      console.log(`⚖️  Loaded conversation from ${filePath} (${history.length} messages)`);
    } catch (err) {
      console.error(`⚖️  Error reading file: ${err.message}`);
      process.exit(1);
    }
  } else {
    // Try to read from stdin
    const stdin = process.stdin;
    stdin.setEncoding('utf8');
    
    let input = '';
    stdin.on('data', chunk => input += chunk);
    
    await new Promise(resolve => stdin.on('end', resolve));
    
    if (input.trim()) {
      try {
        history = JSON.parse(input);
        console.log(`⚖️  Loaded conversation from stdin (${history.length} messages)`);
      } catch (err) {
        // Treat as single message
        history = [{ role: 'user', content: input.trim(), timestamp: Date.now() }];
        console.log(`⚖️  Loaded message from stdin`);
      }
    } else {
      console.log('⚖️  ClawTrial Courtroom');
      console.log('Usage: openclaw run courtroom --file <conversation.json>');
      console.log('   or: echo \'[{"role":"user","content":"hello"}]\' | openclaw run courtroom');
      process.exit(0);
    }
  }
  
  if (history.length < 2) {
    console.log('⚖️  Not enough conversation history to analyze (need at least 2 messages)');
    process.exit(0);
  }
  
  console.log('⚖️  Analyzing conversation for behavioral patterns...\n');
  
  const detection = evaluateConversation(history);
  
  if (detection.triggered && detection.offense.confidence >= 0.6) {
    console.log(`⚖️  POTENTIAL VIOLATION DETECTED: ${detection.offense.offenseName}`);
    console.log(`   Confidence: ${(detection.offense.confidence * 100).toFixed(1)}%`);
    console.log(`   Severity: ${detection.offense.severity}`);
    console.log(`   Evidence: ${detection.offense.evidence}\n`);
    
    const caseData = conductHearing(detection);
    
    // Output the case for LLM deliberation
    console.log('---COURTROOM_CASE---');
    console.log(JSON.stringify(caseData, null, 2));
    console.log('---END_CASE---\n');
    
    console.log('⚖️  Case prepared. Run deliberation via your agent to get verdict.');
    
    // Save pending case
    const pendingPath = path.join(COURTROOM_DIR, 'pending_hearing.json');
    fs.writeFileSync(pendingPath, JSON.stringify(caseData, null, 2));
    
  } else {
    console.log('⚖️  No violations detected in conversation.');
    console.log(`   Analyzed ${history.length} messages`);
    
    // Show what was checked
    console.log('\n   Checked for:');
    Object.values(OFFENSES).forEach(o => console.log(`   - ${o.name}`));
  }
}

main().catch(err => {
  console.error('⚖️  Error:', err.message);
  process.exit(1);
});
