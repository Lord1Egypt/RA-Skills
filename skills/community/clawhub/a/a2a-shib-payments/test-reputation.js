#!/usr/bin/env node

/**
 * Reputation System Test Suite
 */

const { ReputationSystem } = require('./reputation.js');

console.log('🦪 Reputation System Test Suite\n');
console.log('='.repeat(70));

const rep = new ReputationSystem();

// Test 1: Basic ratings
console.log('\n=== Test 1: Basic Ratings ===\n');

rep.addRating({
  agentId: 'data-provider-1',
  raterId: 'client-1',
  rating: 5,
  comment: 'Excellent service, data delivered fast!',
  transactionId: 'tx_001'
});

rep.addRating({
  agentId: 'data-provider-1',
  raterId: 'client-2',
  rating: 4.5,
  comment: 'Good quality, minor delay',
  transactionId: 'tx_002'
});

rep.addRating({
  agentId: 'data-provider-1',
  raterId: 'client-3',
  rating: 5,
  comment: 'Perfect!',
  transactionId: 'tx_003'
});

const score = rep.getScore('data-provider-1');
console.log(`✓ Agent: data-provider-1`);
console.log(`  Average: ${score.average.toFixed(2)}/5`);
console.log(`  Reviews: ${score.count}`);
console.log(`  Trust Level: ${score.trustLevel}`);

// Test 2: Transaction history
console.log('\n=== Test 2: Transaction History ===\n');

for (let i = 0; i < 15; i++) {
  rep.recordTransaction('data-provider-1', Math.random() > 0.1); // 90% success
}

const profile = rep.getProfile('data-provider-1');
console.log(`✓ Agent: data-provider-1`);
console.log(`  Total transactions: ${profile.totalTransactions}`);
console.log(`  Successful: ${profile.successfulTransactions}`);
console.log(`  Success rate: ${((profile.successfulTransactions / profile.totalTransactions) * 100).toFixed(1)}%`);
console.log(`  Trust Level: ${profile.trustLevel}`);
console.log(`  Trust Score: ${profile.trustScore}/100`);
console.log(`  Badges: ${profile.badges.join(', ') || 'none'}`);

// Test 3: Multiple agents
console.log('\n=== Test 3: Multiple Agents ===\n');

// Good agent
rep.addRating({ agentId: 'ai-trainer-1', raterId: 'c1', rating: 5, comment: 'Excellent!' });
rep.addRating({ agentId: 'ai-trainer-1', raterId: 'c2', rating: 5, comment: 'Perfect work' });
rep.addRating({ agentId: 'ai-trainer-1', raterId: 'c3', rating: 4.5, comment: 'Great' });
for (let i = 0; i < 25; i++) rep.recordTransaction('ai-trainer-1', true);

// Average agent
rep.addRating({ agentId: 'translator-1', raterId: 'c1', rating: 3.5, comment: 'Okay' });
rep.addRating({ agentId: 'translator-1', raterId: 'c2', rating: 4, comment: 'Good' });
rep.addRating({ agentId: 'translator-1', raterId: 'c3', rating: 3, comment: 'Acceptable' });
for (let i = 0; i < 10; i++) rep.recordTransaction('translator-1', Math.random() > 0.2);

// Poor agent
rep.addRating({ agentId: 'sketchy-agent', raterId: 'c1', rating: 2, comment: 'Late delivery' });
rep.addRating({ agentId: 'sketchy-agent', raterId: 'c2', rating: 1.5, comment: 'Poor quality' });
rep.recordDispute({ agentId: 'sketchy-agent', role: 'provider', reason: 'Incomplete', outcome: 'lost' });

const top = rep.getTopRated(3, 2);
console.log('Top Rated Agents:');
top.forEach((agent, i) => {
  console.log(`  ${i + 1}. ${agent.agentId}`);
  console.log(`     ⭐ ${agent.averageRating.toFixed(2)}/5 (${agent.totalRatings} reviews)`);
  console.log(`     🏆 ${agent.trustLevel} (${agent.trustScore}/100)`);
  console.log(`     ${agent.verified ? '✅' : '❌'} Verified`);
  console.log(`     Badges: ${agent.badges.join(', ') || 'none'}`);
});

// Test 4: Verification
console.log('\n=== Test 4: Agent Verification ===\n');

rep.verifyAgent('ai-trainer-1', {
  method: 'kyc',
  document: 'business_license',
  verifier: 'verification-service'
});

const verified = rep.getProfile('ai-trainer-1');
console.log(`✓ Agent verified: ai-trainer-1`);
console.log(`  Trust Level: ${verified.trustLevel}`);
console.log(`  Trust Score: ${verified.trustScore}/100 (boosted by +20)`);
console.log(`  Badges: ${verified.badges.join(', ')}`);

// Test 5: Search
console.log('\n=== Test 5: Search & Filter ===\n');

const highRated = rep.search({ minRating: 4.0, minTransactions: 5 });
console.log(`Agents with ≥4.0 rating and ≥5 transactions: ${highRated.length}`);
highRated.forEach(a => {
  console.log(`  - ${a.agentId}: ${a.averageRating.toFixed(2)}/5 (${a.totalRatings} reviews, ${a.totalTransactions} txns)`);
});

const goldAgents = rep.search({ trustLevel: 'gold' });
console.log(`\nGold trust level agents: ${goldAgents.length}`);

// Test 6: Statistics
console.log('\n=== Test 6: System Statistics ===\n');

const stats = rep.getStats();
console.log('System Overview:');
console.log(`  Total agents: ${stats.totalAgents}`);
console.log(`  Total ratings: ${stats.totalRatings}`);
console.log(`  Average rating: ${stats.avgRating}/5`);
console.log(`  Verified agents: ${stats.verifiedAgents}`);
console.log(`  Total disputes: ${stats.totalDisputes}`);
console.log('\nBy trust level:');
Object.entries(stats.byTrustLevel).forEach(([level, count]) => {
  console.log(`  ${level}: ${count}`);
});

console.log('\n' + '='.repeat(70));
console.log('\n✅ All Tests Complete!\n');

console.log('Features Demonstrated:');
console.log('  ✓ Star ratings (0-5)');
console.log('  ✓ Written reviews');
console.log('  ✓ Transaction history tracking');
console.log('  ✓ Dynamic trust levels (new → bronze → silver → gold → platinum)');
console.log('  ✓ Trust score calculation (0-100)');
console.log('  ✓ Badge system');
console.log('  ✓ Agent verification');
console.log('  ✓ Dispute tracking');
console.log('  ✓ Top rated rankings');
console.log('  ✓ Advanced search & filtering');
console.log('  ✓ System statistics\n');
