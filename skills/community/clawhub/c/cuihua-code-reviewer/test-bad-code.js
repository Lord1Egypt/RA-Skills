// Test file with intentional issues for code-reviewer to detect

// ISSUE 1: Hardcoded API key (CRITICAL)
const API_KEY = "sk-1234567890abcdef1234567890abcdef";

// ISSUE 2: SQL Injection (CRITICAL)
function getUserById(userId) {
  const query = `SELECT * FROM users WHERE id = ${userId}`;
  return db.query(query);
}

// ISSUE 3: Command Injection (CRITICAL)
function runCommand(userInput) {
  exec(`ls -la ${userInput}`);
}

// ISSUE 4: eval() usage (HIGH)
function executeCode(code) {
  return eval(code);
}

// ISSUE 5: Nested loops (MEDIUM - Performance)
function findDuplicates(arr1, arr2) {
  for (let i = 0; i < arr1.length; i++) {
    for (let j = 0; j < arr2.length; j++) {
      if (arr1[i] === arr2[j]) {
        console.log('Duplicate found:', arr1[i]);
      }
    }
  }
}

// ISSUE 6: Sync file operation (MEDIUM)
function loadConfig() {
  const data = fs.readFileSync('./config.json', 'utf8');
  return JSON.parse(data);
}

// ISSUE 7: Magic number (LOW)
function calculateDiscount(price) {
  if (price > 1000) {
    return price * 0.9; // 10% discount
  }
  return price;
}

// ISSUE 8: console.log in production (LOW)
function processData(data) {
  console.log('Processing:', data);
  return data.map(item => item * 2);
}

// ISSUE 9: TODO comment (LOW - Technical Debt)
function uploadFile(file) {
  // TODO: Add file validation
  // FIXME: Handle large files
  return file.save();
}

// ISSUE 10: Missing error handling (MEDIUM)
async function fetchData(url) {
  const response = await fetch(url);
  return response.json();
  // No try/catch!
}

module.exports = {
  getUserById,
  runCommand,
  executeCode,
  findDuplicates,
  loadConfig,
  calculateDiscount,
  processData,
  uploadFile,
  fetchData
};
