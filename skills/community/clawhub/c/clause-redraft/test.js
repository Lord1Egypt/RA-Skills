#!/usr/bin/env node
/**
 * Clause Redrafter - Test Suite
 */

const { redraftClause, formatResults } = require('./scripts/clause-redrafter.js');

const TEST_CASES = [
  {
    name: 'Empty input',
    input: '',
    expectError: true
  },
  {
    name: 'Payment upon completion',
    input: 'Payment due upon completion of services.',
    expectIssues: true,
    expectSuggestions: true
  },
  {
    name: 'Termination at any time',
    input: 'Either party may terminate at any time.',
    expectIssues: true,
    expectSuggestions: true
  },
  {
    name: 'Work for hire',
    input: 'All work shall be work-made-for-hire.',
    expectIssues: true,
    expectSuggestions: true
  },
  {
    name: 'Indefinite confidentiality',
    input: 'All information shall be kept confidential indefinitely.',
    expectIssues: true,
    expectSuggestions: true
  },
  {
    name: 'Generic clause',
    input: 'The parties agree to work together on the project.',
    expectIssues: true  // Should detect lack of specificity
  }
];

function runTests() {
  console.log('=== Clause Redrafter Test Suite ===\n');
  
  let passed = 0;
  let failed = 0;

  for (const testCase of TEST_CASES) {
    process.stdout.write('Test: ' + testCase.name + ' ... ');
    
    try {
      const result = redraftClause(testCase.input);
      let testPassed = true;
      let failReason = '';

      if (testCase.expectError) {
        if (!result.error) {
          testPassed = false;
          failReason = 'Expected error but got none';
        }
      } else {
        if (result.error) {
          testPassed = false;
          failReason = 'Unexpected error: ' + result.error;
        } else {
          if (testCase.expectIssues && result.issues.length === 0) {
            testPassed = false;
            failReason = 'Expected issues but none found';
          }
          if (testCase.expectSuggestions && result.suggestions.length === 0) {
            testPassed = false;
            failReason = 'Expected suggestions but none found';
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
