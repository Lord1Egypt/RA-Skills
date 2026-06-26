#!/usr/bin/env node
/**
 * prompt-refiner/scripts/refine.js
 * 
 * Transform raw, messy input into structured AI-optimized prompts.
 * Handles: voice transcriptions, casual messages, mixed languages, vague requests.
 *
 * Usage:
 *   echo "raw input" | node refine.js
 *   node refine.js --input "your request here"
 *   node refine.js --input "your request" --format json
 */

const readline = require('readline');

const args = process.argv.slice(2);
const inputFlagIdx = args.indexOf('--input');
const formatFlagIdx = args.indexOf('--format');

const format = formatFlagIdx !== -1 && args[formatFlagIdx + 1] ? args[formatFlagIdx + 1] : 'text';

function detectLanguage(text) {
  const chineseCount = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const englishCount = (text.match(/[a-zA-Z]/g) || []).length;
  
  if (chineseCount > 0 && englishCount > 0) return 'mixed';
  if (chineseCount > englishCount) return 'chinese';
  return 'english';
}

function detectClarityLevel(text) {
  const length = text.length;
  const hasTargetMarkers = /file|project|service|database|email|document|website|code|api|function|method|class|variable|table|record/i.test(text);
  const hasActionMarkers = /check|create|fix|delete|update|restart|analyze|review|build|deploy|test|validate/i.test(text);
  
  let clarity = 'HIGH — intent is reasonably clear';
  let score = 0;
  
  if (hasActionMarkers) score++;
  if (hasTargetMarkers) score++;
  if (length > 60) score++;
  
  if (score <= 1) clarity = 'LOW — clarification likely needed';
  else if (score === 2) clarity = 'MEDIUM — may need clarification';
  
  return clarity;
}

function detectAction(text) {
  const actionPatterns = [
    [/check|查|看|检查|verify|validate/, '✓ Check / Inspect'],
    [/create|build|make|创建|创造|建|generate|write/, '✏️ Create / Build'],
    [/fix|repair|修复|修|debug|troubleshoot|resolve/, '🔧 Fix / Repair'],
    [/restart|重启|重新|reload|reboot/, '🔄 Restart / Reload'],
    [/send|发送|发|deliver|push|upload/, '📤 Send / Deliver'],
    [/search|find|搜索|查找|找|locate|grep/, '🔍 Search / Find'],
    [/update|modify|更新|修改|change|edit/, '✏️ Update / Modify'],
    [/delete|remove|删除|移除|drop|erase/, '🗑️ Delete / Remove'],
    [/show|list|显示|列出|display|print/, '📋 Show / List'],
    [/summarize|总结|汇总|abstract|condense/, '📄 Summarize'],
    [/analyze|review|分析|审查|audit|inspect/, '🔬 Analyze / Review'],
    [/deploy|release|发布|publish/, '🚀 Deploy / Release'],
    [/test|测试|check quality/, '✅ Test / Verify Quality'],
  ];

  for (const [pattern, label] of actionPatterns) {
    if (pattern.test(text)) return label;
  }
  
  return '❓ Perform task';
}

function generateClarifyingQuestions(text) {
  const questions = [];
  
  if (!/\bwith\b|for\b|about\b|which|which one|哪个|哪个|which service|which file/i.test(text)) {
    questions.push('Which [target/service/file/account] — can you be specific?');
  }
  
  if (!/error|bug|issue|problem|performance|security|review for|check for/i.test(text)) {
    questions.push('What should I look for? (errors, performance, security, etc.)');
  }
  
  if (!/today|now|urgent|asap|when|deadline|by/i.test(text)) {
    questions.push('Do you have a deadline or priority level?');
  }
  
  return questions.slice(0, 2); // Return top 2 questions
}

function refinePrompt(raw) {
  const text = raw.trim();
  if (!text) return 'Error: No input provided.';

  const language = detectLanguage(text);
  const clarity = detectClarityLevel(text);
  const action = detectAction(text);
  const questions = generateClarifyingQuestions(text);
  
  const needsClarification = clarity.startsWith('LOW');

  if (format === 'json') {
    return JSON.stringify({
      input: text,
      analysis: {
        detectedAction: action,
        language: language,
        clarityLevel: clarity,
      },
      needsClarification: needsClarification,
      suggestedQuestions: needsClarification ? questions : [],
      recommendedStructure: {
        persona: '[Role + expertise relevant to the task]',
        task: '[Specific action on specific target]',
        context: '[System/file/service details, environment, account]',
        references: '[Few-shot examples or templates when format matters]',
        requirements: '[Constraints, checks, scope limits, edge cases]',
        output: '[Format, destination, success criteria]',
      },
      nextStep: needsClarification 
        ? 'Ask one clarifying question above before refining.' 
        : 'Ready to refine into structured prompt.',
    }, null, 2);
  }

  // Default: text format (human-friendly)
  let output = `╔════════════════════════════════════════════╗
║        🎯 PROMPT REFINER ANALYSIS        ║
╚════════════════════════════════════════════╝

📝 Raw Input:
  "${text}"

🔍 Analysis:
  Detected Action: ${action}
  Language:       ${language.toUpperCase()}
  Clarity Level:  ${clarity}

${needsClarification ? `\n⚠️  NEEDS CLARIFICATION\n\nAsk ONE question from below before refining:\n${questions.map((q, i) => `  ${i + 1}. ${q}`).join('\n')}\n` : `\n✅ READY TO REFINE\n`}

📋 Structured Prompt Template:

  Persona:
    [Role + expertise relevant to the task]

  Task:
    [Clear action verb + specific what to do]

  Context:
    [System/file/service details, environment, account info]

  References:
    [Few-shot examples or templates when format consistency matters]

  Requirements:
    [Constraints, scope limits, what to check, edge cases]

  Output:
    [Format, destination, level of detail, pass/fail criteria]

  Advanced (when needed):
    - Add "Think step by step:" for complex reasoning (Chain of Thought)
    - Break into chained sub-prompts for multi-phase tasks
    - Add "Meta: What info do you need?" if unsure how to frame it

💡 Next Step:
  ${needsClarification 
    ? 'Ask the clarification question above, then refine.' 
    : 'Refine the input into the template above and confirm with user.'}

`;

  return output;
}

// Read from --input flag or stdin
if (inputFlagIdx !== -1 && args[inputFlagIdx + 1]) {
  const input = args.slice(inputFlagIdx + 1).join(' ');
  console.log(refinePrompt(input));
} else if (process.stdin.isTTY) {
  console.log('Usage:');
  console.log('  echo "your prompt" | node refine.js');
  console.log('  node refine.js --input "your prompt"');
  console.log('  node refine.js --input "your prompt" --format json');
} else {
  let input = '';
  const rl = readline.createInterface({ input: process.stdin });
  rl.on('line', line => { input += line + ' '; });
  rl.on('close', () => console.log(refinePrompt(input)));
}

