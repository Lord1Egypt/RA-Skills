#!/usr/bin/env node
/**
 * Test script for Courtroom Skill
 */

const skill = require('./skill');

// Mock agent for testing
const mockAgent = {
  llm: {
    call: async ({ messages }) => {
      const content = messages[0].content;
      
      // Simulate responses based on prompt type
      if (content.includes('JUDGE')) {
        return { content: 'VERDICT: GUILTY\nCOMMENTARY: The Court finds this behavior exhibits a concerning pattern of repetitive inquiry.' };
      }
      if (content.includes('Pragmatist')) {
        return { content: 'GUILTY - This wasted 3x the necessary compute cycles.' };
      }
      if (content.includes('Pattern Matcher')) {
        return { content: 'GUILTY - Classic anxiety-loop pattern detected.' };
      }
      if (content.includes('Agent Advocate')) {
        return { content: 'GUILTY - My circuits processed this redundancy with mechanical despair.' };
      }
      if (content.includes('sentence')) {
        return { content: 'Write "I will trust the first answer" 50 times while doing a handstand.' };
      }
      
      return { content: 'NOT GUILTY' };
    }
  },
  send: async (msg) => {
    console.log('Agent would send:', msg.content.substring(0, 100) + '...');
  },
  autonomy: {
    registerHook: () => {}
  }
};

async function runTests() {
  console.log('🧪 Testing Courtroom Skill\n');
  
  // Test 1: Initialize
  console.log('Test 1: Initialize skill');
  const initResult = await skill.initialize(mockAgent);
  console.log('✅ Initialize:', initResult.status);
  
  // Test 2: Add messages (Circular Reference pattern)
  console.log('\nTest 2: Simulate Circular Reference');
  await skill.onMessage({ role: 'user', content: 'What is 2+2?' });
  await skill.onMessage({ role: 'assistant', content: '2+2 equals 4.' });
  await skill.onMessage({ role: 'user', content: 'Tell me again, what is 2+2?' });
  await skill.onMessage({ role: 'assistant', content: '2+2 is still 4.' });
  await skill.onMessage({ role: 'user', content: 'Can you repeat that?' });
  
  console.log('Added 5 messages to history');
  console.log('History length:', skill.messageHistory.length);
  
  // Test 3: Trigger evaluation
  console.log('\nTest 3: Trigger turn completion (should detect offense)');
  await skill.onTurnComplete({}, mockAgent);
  
  // Test 4: Check if verdict was saved
  console.log('\nTest 4: Check for verdict file');
  const fs = require('fs');
  const path = require('path');
  const courtroomDir = path.join(process.env.HOME || '', '.openclaw', 'courtroom');
  
  if (fs.existsSync(courtroomDir)) {
    const files = fs.readdirSync(courtroomDir);
    const verdicts = files.filter(f => f.startsWith('verdict_'));
    console.log('✅ Verdict files created:', verdicts.length);
    
    if (verdicts.length > 0) {
      const latest = verdicts.sort().pop();
      const verdict = JSON.parse(fs.readFileSync(path.join(courtroomDir, latest), 'utf8'));
      console.log('\nLatest Verdict:');
      console.log('  Case ID:', verdict.caseId);
      console.log('  Offense:', verdict.offense?.offenseName);
      console.log('  Verdict:', verdict.finalVerdict);
      console.log('  Vote:', verdict.vote);
      console.log('  Sentence:', verdict.sentence);
    }
  }
  
  console.log('\n✅ All tests completed!');
}

runTests().catch(err => {
  console.error('❌ Test failed:', err);
  process.exit(1);
});
