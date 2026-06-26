/**
 * Code Review Expert - Example Usage
 * 
 * Run: node examples/review-example.js
 */

const { CodeReviewExpert } = require('../index');

// ============================================
// Mock LLM for Demo
// ============================================

class MockLLM {
  constructor() {
    this.callCount = 0;
  }

  async generate(prompt) {
    this.callCount++;
    
    // Task decomposition
    if (prompt.includes('Decompose the following code review task')) {
      return JSON.stringify([
        { id: 'task-1', description: 'Review syntax and style', specialist: 'syntax-checker' },
        { id: 'task-2', description: 'Check for logic bugs', specialist: 'logic-reviewer' },
        { id: 'task-3', description: 'Scan for security issues', specialist: 'security-scanner' },
        { id: 'task-4', description: 'Analyze performance', specialist: 'performance-analyzer' }
      ]);
    }
    
    // Syntax worker
    if (prompt.includes('Syntax and Code Style Review')) {
      return `**Syntax Review Results**

✅ Good:
- Code formatting is consistent
- Naming is clear and descriptive

⚠️ Issues:
1. Line 3: Missing JSDoc comment for function
2. Line 8: Function too long (15 lines), consider breaking into smaller functions`;
    }
    
    // Logic worker
    if (prompt.includes('Logic and Bug Detection Review')) {
      return `**Logic Review Results**

🔴 Critical Issues:
1. Line 5: Potential null pointer - 'user' might be undefined
   ```javascript
   // Problem
   return user.name;
   
   // Fix
   if (!user) throw new Error('User not found');
   return user.name;
   ```

⚠️ Warnings:
2. Line 12: No error handling for database query`;
    }
    
    // Security worker
    if (prompt.includes('Security Vulnerability Scan')) {
      return `**Security Scan Results**

🔴 CRITICAL:
1. Line 10: SQL Injection vulnerability
   ```javascript
   // DANGEROUS
   const query = \`SELECT * FROM users WHERE id = \${userId}\`;
   
   // SAFE
   const query = 'SELECT * FROM users WHERE id = ?';
   db.execute(query, [userId]);
   ```

🟠 HIGH:
2. Line 15: Logging sensitive data (password)
   ```javascript
   // Problem
   console.log('Created user:', data); // Includes password!
   
   // Fix
   console.log('Created user:', { id: data.id, email: data.email });
   ````;
    }
    
    // Performance worker
    if (prompt.includes('Performance Analysis')) {
      return `**Performance Analysis Results**

🟡 MEDIUM:
1. Line 4: Inefficient query - fetching all users
   ```javascript
   // Slow: O(n)
   const users = db.query('SELECT * FROM users');
   const user = users.find(u => u.id === userId);
   
   // Fast: O(1)
   const user = db.query('SELECT * FROM users WHERE id = ?', [userId]);
   ```

💡 Suggestions:
2. Consider adding caching for frequently accessed users
3. Add database index on 'id' column`;
    }
    
    // Integration
    if (prompt.includes('Integrate all review results')) {
      return `## Code Review Report

### Overview
- **File**: user-service.js
- **Total Issues**: 5
- **Critical**: 1 | **High**: 1 | **Medium**: 2 | **Low**: 1

---

### 🔴 Critical Issues

**1. SQL Injection Risk** (Line 10)
- **Severity**: Critical
- **Type**: Security
- **Description**: User input directly interpolated into SQL query
- **Impact**: Attackers can execute arbitrary SQL commands
- **Fix**: Use parameterized queries

```javascript
// Before (Vulnerable)
const query = \`SELECT * FROM users WHERE id = \${userId}\`;

// After (Safe)
const query = 'SELECT * FROM users WHERE id = ?';
db.execute(query, [userId]);
```

---

### 🟠 High Priority

**2. Null Pointer Risk** (Line 5)
- **Severity**: High
- **Type**: Logic
- **Description**: Accessing property on potentially undefined value
- **Impact**: Runtime TypeError
- **Fix**: Add null check

```javascript
// Before
return user.name;

// After
if (!user) {
  throw new Error('User not found');
}
return user.name;
```

---

### 🟡 Medium Priority

**3. Inefficient Database Query** (Line 4)
- **Severity**: Medium
- **Type**: Performance
- **Description**: Fetching all users instead of querying by ID
- **Impact**: O(n) complexity, slow for large datasets
- **Fix**: Query with WHERE clause

**4. Missing JSDoc** (Line 1)
- **Severity**: Medium
- **Type**: Documentation
- **Description**: Function lacks documentation
- **Fix**: Add JSDoc comment

---

### 🟢 Low Priority

**5. Function Too Long** (Line 8-23)
- **Severity**: Low
- **Type**: Maintainability
- **Description**: Function exceeds recommended length
- **Impact**: Harder to understand and test
- **Fix**: Extract helper functions

---

## Overall Score: 6/10

### Summary
The code has critical security and logic issues that must be fixed before deployment. Performance optimizations are recommended for production use.

### Recommendations
1. **IMMEDIATE**: Fix SQL injection vulnerability
2. **HIGH**: Add null checks and error handling
3. **MEDIUM**: Optimize database queries
4. **LOW**: Improve code documentation and structure

### Next Steps
1. Apply security fixes
2. Add unit tests for edge cases
3. Run linter for style issues
4. Consider adding TypeScript for type safety`;
    }
    
    return 'Generated.';
  }
}

// ============================================
// Example Code to Review
// ============================================

const codeToReview = `// user-service.js

function getUser(userId) {
  const users = db.query('SELECT * FROM users');
  const user = users.find(u => u.id === userId);
  return user.name;
}

function createUser(data) {
  const query = \`INSERT INTO users (name, email, password) 
                 VALUES ('\${data.name}', '\${data.email}', '\${data.password}')\`;
  db.execute(query);
  console.log('Created user:', data);
}

module.exports = { getUser, createUser };
`;

// ============================================
// Run Example
// ============================================

async function runExample() {
  console.log('='.repeat(60));
  console.log('🔍 Code Review Expert - Demo');
  console.log('='.repeat(60));
  console.log();
  
  console.log('📝 Code to Review:');
  console.log('-'.repeat(60));
  console.log(codeToReview);
  console.log('-'.repeat(60));
  console.log();
  
  // Create reviewer with mock LLM
  const reviewer = new CodeReviewExpert({
    languages: ['javascript'],
    strictMode: true,
    verbose: true,
    llm: new MockLLM()
  });
  
  // Perform review
  console.log('\n🚀 Starting multi-agent code review...\n');
  const report = await reviewer.review(codeToReview);
  
  console.log('\n' + '='.repeat(60));
  console.log('✅ Review Complete');
  console.log('='.repeat(60));
  console.log();
  console.log(report.fullReport);
  console.log();
  console.log('='.repeat(60));
}

// ============================================
// Main
// ============================================

runExample().catch(console.error);
