// Test run for AI Fact Checker

const { extractFactualStatements, calculateConfidence } = require('./scripts/fact-check');

const testText = `OpenClaw 是 2025 年发布的开源 AI Agent 框架，现在 ClawHub 上已经有超过 10000 个社区技能。作者是 Peter Steinberger。`;

console.log('=== Testing Fact Extraction ===');
console.log('Original text:', testText);
console.log('---');

const statements = extractFactualStatements(testText);
console.log(`Extracted ${statements.length} factual statements:`);
statements.forEach((s, i) => {
    console.log(`${i+1}. ${s}`);
});

// Mock search results for testing
const mockResults = [
    {
        title: 'OpenClaw GitHub',
        snippet: 'OpenClaw - A powerful agent framework for AI assistants, created by Peter Steinberger in 2024.'
    },
    {
        title: 'ClawHub - OpenClaw Skill Registry',
        snippet: 'ClawHub currently hosts over 5705 community skills for OpenClaw.'
    }
];

console.log('\n=== Testing Confidence Calculation ===');
console.log('Statement: "OpenClaw 作者是 Peter Steinberger"');
const result1 = calculateConfidence('OpenClaw 作者是 Peter Steinberger', mockResults);
console.log('Score:', result1.score, 'Verdict:', result1.verdict);

console.log('\nStatement: "ClawHub 上已经有超过 10000 个社区技能"');
const result2 = calculateConfidence('ClawHub 上已经有超过 10000 个社区技能', mockResults);
console.log('Score:', result2.score, 'Verdict:', result2.verdict);

console.log('\nStatement: "OpenClaw 是 2025 年发布"');
const result3 = calculateConfidence('OpenClaw 是 2025 年发布', mockResults);
console.log('Score:', result3.score, 'Verdict:', result3.verdict);
