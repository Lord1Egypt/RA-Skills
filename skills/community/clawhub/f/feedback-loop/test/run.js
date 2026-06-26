#!/usr/bin/env node

/**
 * Feedback Loop Skill - Test Suite
 */

const path = require('path');
const fs = require('fs');
const FeedbackLoop = require('../src/index');

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (error) {
    console.error(`✗ ${name}`);
    console.error(`  Error: ${error.message}`);
    failed++;
  }
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message || 'Assertion failed');
  }
}

function assertEqual(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(message || `Expected ${expected}, got ${actual}`);
  }
}

function assertOk(result, message) {
  if (!result.success) {
    throw new Error(message || 'Expected success to be true');
  }
}

console.log('\n🧪 Feedback Loop Skill - Test Suite\n');
console.log('='.repeat(50));

// Test 1: Initialization
test('Initialize FeedbackLoop', () => {
  const fl = new FeedbackLoop();
  assert(fl, 'FeedbackLoop instance should be created');
  assert(fl.collector, 'Collector should be initialized');
  assert(fl.analyzer, 'Analyzer should be initialized');
  assert(fl.suggester, 'Suggester should be initialized');
  assert(fl.tracker, 'Tracker should be initialized');
});

// Test 2: Provide explicit feedback
test('Provide explicit feedback', () => {
  const fl = new FeedbackLoop();
  const result = fl.provide({
    type: 'explicit',
    rating: 5,
    comment: 'Great response!',
    category: 'accuracy',
    sessionId: 'test_session_1'
  });
  assertOk(result, 'Should successfully provide feedback');
  assert(result.feedback, 'Should return feedback object');
  assertEqual(result.feedback.type, 'explicit', 'Type should be explicit');
});

// Test 3: Provide implicit feedback
test('Provide implicit feedback', () => {
  const fl = new FeedbackLoop();
  const result = fl.provide({
    type: 'implicit',
    signal: 'completion',
    sessionId: 'test_session_2',
    metrics: { responseTime: 2500 }
  });
  assertOk(result, 'Should successfully provide implicit feedback');
  assertEqual(result.feedback.type, 'implicit', 'Type should be implicit');
  assertEqual(result.feedback.inferredSentiment, 'positive', 'Should infer positive sentiment');
});

// Test 4: Get statistics
test('Get statistics', () => {
  const fl = new FeedbackLoop();
  const stats = fl.getStats();
  assert(stats, 'Should return stats object');
  assert(typeof stats.totalFeedback === 'number', 'Should have totalFeedback count');
  assert(typeof stats.explicitFeedback === 'number', 'Should have explicitFeedback count');
  assert(typeof stats.implicitFeedback === 'number', 'Should have implicitFeedback count');
});

// Test 5: Analyze feedback
test('Analyze feedback', () => {
  const fl = new FeedbackLoop();
  const result = fl.analyze({ timeRange: 'all' });
  assertOk(result, 'Should successfully analyze');
  if (result.analysis) {
    assert(result.analysis.clustering, 'Should have clustering data');
    assert(result.analysis.sentiment, 'Should have sentiment data');
    assert(result.analysis.patterns, 'Should have patterns data');
  }
});

// Test 6: Generate suggestions
test('Generate suggestions', () => {
  const fl = new FeedbackLoop();
  const result = fl.suggest({ maxSuggestions: 3 });
  assertOk(result, 'Should successfully generate suggestions');
  assert(Array.isArray(result.suggestions), 'Should return suggestions array');
});

// Test 7: Get feedback with filters
test('Get feedback with filters', () => {
  const fl = new FeedbackLoop();
  const allFeedback = fl.getFeedback();
  const explicitFeedback = fl.getFeedback({ type: 'explicit' });
  
  assert(Array.isArray(allFeedback), 'Should return array');
  assert(Array.isArray(explicitFeedback), 'Should return array');
  
  explicitFeedback.forEach(f => {
    assertEqual(f.type, 'explicit', 'All should be explicit');
  });
});

// Test 8: Get suggestions
test('Get suggestions', () => {
  const fl = new FeedbackLoop();
  const suggestions = fl.getSuggestions();
  assert(Array.isArray(suggestions), 'Should return array');
});

// Test 9: Auto-detect feedback
test('Auto-detect feedback from session data', () => {
  const fl = new FeedbackLoop();
  const result = fl.autoDetect({
    sessionId: 'test_session_3',
    retryCount: 5,
    completionRate: 0.5,
    abandoned: false,
    followUpQuestions: 3
  });
  assertOk(result, 'Should successfully auto-detect');
  assert(typeof result.count === 'number', 'Should return detection count');
});

// Test 10: Get tracking report
test('Get tracking report', () => {
  const fl = new FeedbackLoop();
  const report = fl.getReport();
  assert(report, 'Should return report object');
  assert(report.summary, 'Should have summary');
  assert(report.tracking, 'Should have tracking data');
  assert(Array.isArray(report.suggestions), 'Should have suggestions list');
});

// Test 11: Export data
test('Export data as JSON', () => {
  const fl = new FeedbackLoop();
  const data = fl.exportData('json');
  assert(data, 'Should return data');
  const parsed = JSON.parse(data);
  assert(parsed.tracking !== undefined, 'Should have tracking data');
  assert(parsed.suggestions !== undefined, 'Should have suggestions data');
});

// Test 12: Storage operations
test('Storage operations', () => {
  const Storage = require('../src/storage');
  const storage = new Storage();
  
  const stats = storage.getStats();
  assert(stats, 'Should return stats');
  
  const feedbacks = storage.getAllFeedback();
  assert(Array.isArray(feedbacks), 'Should return array');
});

console.log('\n' + '='.repeat(50));
console.log(`\nResults: ${passed} passed, ${failed} failed\n`);

if (failed > 0) {
  process.exit(1);
}

console.log('✅ All tests passed!\n');
