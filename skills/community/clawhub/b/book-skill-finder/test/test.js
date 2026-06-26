/**
 * Find-Book Skill Tests
 */

const FindBookSkill = require('../index.js');

const skill = new FindBookSkill();

console.log('=== Find-Book Skill Tests ===\n');

// Test 1: Search by title
console.log('Test 1: Search by title "Atomic Habits"');
const result1 = skill.search('Atomic Habits');
console.log(JSON.stringify(result1, null, 2));
console.log('\n---\n');

// Test 2: Search by author
console.log('Test 2: Search by author "James Clear"');
const result2 = skill.getByAuthor('James Clear');
console.log(JSON.stringify(result2, null, 2));
console.log('\n---\n');

// Test 3: Search by concept
console.log('Test 3: Search by concept "productivity"');
const result3 = skill.searchByConcept('productivity');
console.log(JSON.stringify(result3, null, 2));
console.log('\n---\n');

// Test 4: Top rated books
console.log('Test 4: Top 5 rated books');
const result4 = skill.getTopRated(5);
console.log(JSON.stringify(result4, null, 2));
console.log('\n---\n');

// Test 5: Stats
console.log('Test 5: Skill stats');
const result5 = skill.getStats();
console.log(JSON.stringify(result5, null, 2));
console.log('\n---\n');

// Test 6: Fuzzy search
console.log('Test 6: Fuzzy search "atomic"');
const result6 = skill.search('atomic');
console.log(JSON.stringify(result6, null, 2));
console.log('\n---\n');

console.log('✅ All tests completed');
