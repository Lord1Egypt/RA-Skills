#!/usr/bin/env node
/**
 * Evidence Organizer - Test Suite
 */

const { organizeEvidence, formatEvidence } = require('./scripts/evidence-organizer.js');

const TEST_CASES = [
  {
    name: 'Empty input',
    input: null,
    expectError: true
  },
  {
    name: 'Missing items',
    input: { items: [] },
    expectError: true
  },
  {
    name: 'Basic organization by category',
    input: {
      items: [
        { description: 'Contract', category: 'documentary', relevance: 'critical' },
        { description: 'Photo', category: 'physical', relevance: 'important' }
      ],
      organization: 'by-category'
    },
    expectSuccess: true,
    expectItems: 2
  },
  {
    name: 'Organization by chronology',
    input: {
      items: [
        { description: 'Event 1', date: '2024-01-01' },
        { description: 'Event 2', date: '2024-02-01' },
        { description: 'Event 3', date: '2024-01-15' }
      ],
      organization: 'by-chronology'
    },
    expectSuccess: true,
    expectItems: 3
  },
  {
    name: 'Organization by claim',
    input: {
      items: [
        { description: 'Contract', claims: ['breach'] },
        { description: 'Receipt', claims: ['damages'] },
        { description: 'General doc', claims: [] }
      ],
      claims: ['breach', 'damages'],
      organization: 'by-claim'
    },
    expectSuccess: true,
    expectItems: 3
  }
];

function runTests() {
  console.log('=== Evidence Organizer Test Suite ===\n');
  
  let passed = 0;
  let failed = 0;

  for (const testCase of TEST_CASES) {
    process.stdout.write('Test: ' + testCase.name + ' ... ');
    
    try {
      const result = organizeEvidence(testCase.input);
      let testPassed = true;
      let failReason = '';

      if (testCase.expectError) {
        if (!result.error) {
          testPassed = false;
          failReason = 'Expected error but got none';
        }
      } else if (testCase.expectSuccess) {
        if (result.error) {
          testPassed = false;
          failReason = 'Unexpected error: ' + result.error;
        } else {
          if (testCase.expectItems && result.summary.totalItems !== testCase.expectItems) {
            testPassed = false;
            failReason = 'Expected ' + testCase.expectItems + ' items, got ' + result.summary.totalItems;
          }
        }
      }

      if (testPassed) {
        console.log('✓ PASS');
        passed++;
      } else {
        console.log('✗ FAIL: ' + failReason);
        failed++;
      }
    } catch (err) {
      console.log('✗ ERROR: ' + err.message);
      failed++;
    }
  }

  console.log('\n=== Test Summary ===');
  console.log('Passed: ' + passed + '/' + TEST_CASES.length);
  console.log('Failed: ' + failed + '/' + TEST_CASES.length);
  
  if (failed === 0) {
    console.log('\n✓ All tests passed!');
    process.exit(0);
  } else {
    console.log('\n✗ Some tests failed');
    process.exit(1);
  }
}

// Run tests if called directly
if (require.main === module) {
  runTests();
}

module.exports = { runTests, TEST_CASES };
