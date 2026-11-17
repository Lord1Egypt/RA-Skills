#!/usr/bin/env node

const { compress } = require('./compress.js');

// Test cases
const tests = [
  {
    input: "Sure! I'd be happy to help you with that. The issue you're experiencing is most likely caused by your authentication middleware not properly validating the token expiry. Let me take a look and suggest a fix.",
    description: "Auth middleware bug"
  },
  {
    input: "Hello human! Could you please help me figure out why this code isn't working? I think it might be a problem with the API configuration, but honestly I'm not entirely sure what's going on here.",
    description: "API config problem"
  },
  {
    input: "When the user submits the form, we need to validate all the fields and make sure nobody has entered invalid data before we send it to the server. Anyone can see the problem if they look at the code.",
    description: "Form validation"
  }
];

console.log("🏍️ CAVEPONY COMPRESSION TEST SUITE 🦄\n");

tests.forEach((test, i) => {
  console.log(`\n=== Test ${i + 1}: ${test.description} ===`);
  console.log("\n[INPUT]:");
  console.log(test.input);
  
  console.log("\n[LITE MODE]:");
  console.log(compress(test.input, 'lite'));
  
  console.log("\n[FULL MODE]:");
  console.log(compress(test.input, 'full'));
  
  console.log("\n[ULTRA MODE]:");
  console.log(compress(test.input, 'ultra'));
  
  console.log("\n[PONY MODE 🦄]:");
  console.log(compress(test.input, 'pony'));
  
  console.log("\n[CANTERLOT MODE 🏰]:");
  console.log(compress(test.input, 'canterlot'));
  
  console.log("\n" + "-".repeat(60));
});

// Test pony substitutions specifically
console.log("\n🦄 PONY SUBSTITUTION SPECIAL TESTS 🦄");

const ponyTests = [
  "Hello human, how are you?",
  "Anybody home?",
  "Nobody is perfect.",
  "The woman asked the man for help.",
  "The children are playing with their hands and feet.",
  "Hey! What the heck is going on here?",
  "Everybody loves New York at Christmas!",
  "The people of Philadelphia are wonderful folks."
];

ponyTests.forEach((test, i) => {
  console.log(`\nTest ${i + 1}: "${test}"`);
  console.log(`→ Pony: "${compress(test, 'pony')}"`);
});