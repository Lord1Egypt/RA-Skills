#!/usr/bin/env node

/**
 * Freelance-Proposal-Writer Test Suite
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');

console.log('🧪 Running tests...\n');

// Test 1: Template loading
console.log('Test 1: Template loading');
try {
  const fs = require('fs');
  const path = require('path');
  
  const templatesDir = path.join(__dirname, 'templates');
  const templates = fs.readdirSync(templatesDir);
  
  assert(templates.length >= 5, 'Should have at least 5 templates');
  assert(templates.includes('standard.md'), 'Should have standard template');
  assert(templates.includes('premium.md'), 'Should have premium template');
  assert(templates.includes('quick.md'), 'Should have quick template');
  
  console.log('  ✓ Passed\n');
} catch (error) {
  console.log('  ✗ Failed:', error.message, '\n');
}

// Test 2: Package.json validation
console.log('Test 2: Package.json validation');
try {
  const pkg = require('./package.json');
  
  assert(pkg.name === 'freelance-proposal-writer', 'Package name should match');
  assert(pkg.version === '1.0.0', 'Version should be 1.0.0');
  assert(pkg.bin['freelance-proposal'] === './index.js', 'Binary should be defined');
  assert(pkg.dependencies.commander, 'Should have commander dependency');
  
  console.log('  ✓ Passed\n');
} catch (error) {
  console.log('  ✗ Failed:', error.message, '\n');
}

// Test 3: ClawHub config validation
console.log('Test 3: ClawHub config validation');
try {
  const config = require('./clawhub.json');
  
  assert(config.name === 'freelance-proposal-writer', 'Config name should match');
  assert(config.clawhub.pricing.amount === 79, 'Price should be $79');
  assert(config.clawhub.pricing.period === 'monthly', 'Should be monthly subscription');
  assert(config.clawhub.features.length >= 5, 'Should have at least 5 features');
  
  console.log('  ✓ Passed\n');
} catch (error) {
  console.log('  ✗ Failed:', error.message, '\n');
}

// Test 4: SKILL.md exists
console.log('Test 4: SKILL.md exists');
try {
  const fs = require('fs');
  const skillPath = path.join(__dirname, 'SKILL.md');
  
  assert(fs.existsSync(skillPath), 'SKILL.md should exist');
  
  const content = fs.readFileSync(skillPath, 'utf8');
  assert(content.length > 500, 'SKILL.md should have substantial content');
  assert(content.includes('AI 生成'), 'Should mention AI generation');
  assert(content.includes('客户分析'), 'Should mention client analysis');
  
  console.log('  ✓ Passed\n');
} catch (error) {
  console.log('  ✗ Failed:', error.message, '\n');
}

// Test 5: README.md exists
console.log('Test 5: README.md exists');
try {
  const fs = require('fs');
  const readmePath = path.join(__dirname, 'README.md');
  
  assert(fs.existsSync(readmePath), 'README.md should exist');
  
  const content = fs.readFileSync(readmePath, 'utf8');
  assert(content.length > 1000, 'README.md should have substantial content');
  assert(content.includes('安装') || content.includes('installation'), 'Should have installation instructions');
  assert(content.includes('使用') || content.includes('usage'), 'Should have usage examples');
  
  console.log('  ✓ Passed\n');
} catch (error) {
  console.log('  ✗ Failed:', error.message, '\n');
}

// Test 6: Index.js structure
console.log('Test 6: Index.js structure');
try {
  const fs = require('fs');
  const indexPath = path.join(__dirname, 'index.js');
  
  assert(fs.existsSync(indexPath), 'index.js should exist');
  
  const content = fs.readFileSync(indexPath, 'utf8');
  assert(content.includes('#!/usr/bin/env node'), 'Should have shebang');
  assert(content.includes('.command(') || content.includes('program.command'), 'Should define CLI commands');
  assert(content.includes('TEMPLATES'), 'Should have templates');
  assert(content.includes('generateProposal'), 'Should have generateProposal function');
  assert(content.includes('optimizeProposal'), 'Should have optimizeProposal function');
  assert(content.includes('analyzeClient'), 'Should have analyzeClient function');
  
  console.log('  ✓ Passed\n');
} catch (error) {
  console.log('  ✗ Failed:', error.message, '\n');
}

console.log('─'.repeat(60));
console.log('All tests completed! ✓');
