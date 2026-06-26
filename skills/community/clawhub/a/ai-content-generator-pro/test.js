#!/usr/bin/env node

import aiContentGeneratorPro from './index.js';

async function runTests() {
  console.log('🧪 Testing AI Content Generator Pro Skill\n');
  
  const tests = [
    {
      name: 'Help Command',
      args: ['help'],
      expected: '🤖 AI Content Generator Pro'
    },
    {
      name: 'Generate Blog (simulated)',
      args: ['generate', 'blog', 'Test Topic'],
      expected: '✅ Content generated successfully'
    },
    {
      name: 'Configuration Show',
      args: ['config', 'show'],
      expected: 'Current configuration'
    },
    {
      name: 'Content Schedule',
      args: ['schedule', 'weekly'],
      expected: '📅 Content calendar created'
    },
    {
      name: 'Invalid Command',
      args: ['invalid'],
      expected: '🤖 AI Content Generator Pro'
    }
  ];
  
  let passed = 0;
  let failed = 0;
  
  for (const test of tests) {
    process.stdout.write(`Testing: ${test.name}... `);
    
    try {
      const result = await aiContentGeneratorPro(test.args, {});
      
      if (result.includes(test.expected)) {
        console.log('✅ PASS');
        passed++;
      } else {
        console.log('❌ FAIL');
        console.log(`  Expected: ${test.expected}`);
        console.log(`  Got: ${result.substring(0, 100)}...`);
        failed++;
      }
    } catch (error) {
      console.log('❌ ERROR');
      console.log(`  ${error.message}`);
      failed++;
    }
  }
  
  console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);
  
  if (failed === 0) {
    console.log('\n🎉 All tests passed! The skill is working correctly.');
    console.log('\nNext steps:');
    console.log('1. Run: bash scripts/setup.sh (for full setup)');
    console.log('2. Add API keys to config/config.json');
    console.log('3. Test with real AI generation');
  } else {
    console.log('\n⚠️  Some tests failed. Check the implementation.');
    process.exit(1);
  }
}

// Create test directory structure
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Ensure config directory exists
const configDir = path.join(__dirname, 'config');
if (!fs.existsSync(configDir)) {
  fs.mkdirSync(configDir, { recursive: true });
}

// Create minimal config for testing
const configPath = path.join(configDir, 'config.json');
if (!fs.existsSync(configPath)) {
  fs.writeFileSync(configPath, JSON.stringify({
    openai: { apiKey: 'test', model: 'gpt-4' },
    defaultModel: 'openai',
    tone: 'professional'
  }, null, 2));
}

// Ensure content directory exists
const contentDir = path.join(process.cwd(), 'content');
if (!fs.existsSync(contentDir)) {
  fs.mkdirSync(contentDir, { recursive: true });
}

// Run tests
runTests().catch(console.error);