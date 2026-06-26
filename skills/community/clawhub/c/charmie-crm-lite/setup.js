const readline = require('readline');
const fs = require('fs');
const sqlite3 = require('sqlite3');
const path = require('path');
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

async function ask(question) {
  return new Promise(resolve => rl.question(question, resolve));
}

async function run() {
  console.log("\n==========================================");
  console.log("   Charmie CRM Lite 3.0.3 Setup          ");
  console.log("==========================================\n");

  console.log("This skill uses SQLite – no database server required.");
  console.log("The database will be created automatically when you start the skill.");
  console.log("\nNo configuration is needed. You can start the skill immediately with: npm start\n");
  console.log("For email and messaging features, please upgrade to Professional.\n");

  rl.close();
}

run();
