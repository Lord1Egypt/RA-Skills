/**
 * Code Review Expert - Multi-Agent Code Review System
 * 
 * Uses Manager-Worker pattern with specialized agents:
 * - Syntax Checker
 * - Logic Reviewer
 * - Security Scanner
 * - Performance Analyzer
 */

const { ManagerAgent, WorkerAgent } = require('./workers/base-workers');

class CodeReviewExpert {
  constructor(options = {}) {
    this.languages = options.languages || ['javascript', 'typescript'];
    this.strictMode = options.strictMode || false;
    this.autoFix = options.autoFix || false;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
    
    // Initialize specialized workers
    this.workers = [
      new SyntaxWorker('syntax-checker', this.llm),
      new LogicWorker('logic-reviewer', this.llm),
      new SecurityWorker('security-scanner', this.llm),
      new PerformanceWorker('performance-analyzer', this.llm)
    ];
    
    // Create manager
    this.manager = new ManagerAgent(this.workers, {
      maxRetries: 2,
      timeout: 30000,
      verbose: this.verbose,
      llm: this.llm
    });
  }

  async review(code, options = {}) {
    const task = this.buildReviewTask(code, options);
    
    if (this.verbose) {
      console.log('🔍 Starting code review...');
      console.log(`   Languages: ${this.languages.join(', ')}`);
      console.log(`   Strict mode: ${this.strictMode}`);
      console.log();
    }
    
    // Execute multi-agent review
    const reportText = await this.manager.coordinate(task);
    
    // Parse and structure the report
    const report = this.parseReport(reportText, code);
    
    if (this.verbose) {
      console.log('\n✅ Review complete');
      console.log(`   Score: ${report.score}/10`);
      console.log(`   Issues: ${report.issues.length}`);
    }
    
    return report;
  }

  buildReviewTask(code, options) {
    const focus = options.focus || ['syntax', 'logic', 'security', 'performance'];
    
    return `
Review the following code comprehensively:

${code}

Focus areas: ${focus.join(', ')}
Language: ${this.languages.join(', ')}
Strict mode: ${this.strictMode}

Provide a detailed review report with:
1. Overview (file name, issue count, severity breakdown)
2. Issues by severity (Critical, High, Medium, Low)
3. For each issue:
   - Description
   - Line number (if applicable)
   - Why it's a problem
   - Suggested fix with code example
4. Overall score (0-10)
5. Summary and recommendations
`;
  }

  parseReport(reportText, code) {
    // Simplified parsing - in production, use more robust parsing
    const lines = reportText.split('\n');
    const issues = [];
    let score = 10;
    
    // Extract score
    const scoreMatch = reportText.match(/score[:\s]+(\d+)[\/\s]+10/i);
    if (scoreMatch) {
      score = parseInt(scoreMatch[1]);
    }
    
    // Extract issues (simplified)
    const issuePatterns = [
      /(\🔴|Critical|High|Medium|Low)[:\s]+(.+)/gi,
      /(\d+)\.\s+\*\*(.+)\*\*/gi,
      /Issue[:\s]+(.+)/gi
    ];
    
    for (const pattern of issuePatterns) {
      let match;
      while ((match = pattern.exec(reportText)) !== null) {
        issues.push({
          severity: this.extractSeverity(match[0]),
          description: match[2] || match[1],
          line: this.extractLine(match[0]),
          suggestion: 'See report for details'
        });
      }
    }
    
    return {
      score,
      issues,
      summary: this.extractSummary(reportText),
      suggestions: this.extractSuggestions(reportText),
      fullReport: reportText
    };
  }

  extractSeverity(text) {
    const lower = text.toLowerCase();
    if (lower.includes('critical') || lower.includes('🔴')) return 'critical';
    if (lower.includes('high') || lower.includes('🟠')) return 'high';
    if (lower.includes('medium') || lower.includes('🟡')) return 'medium';
    if (lower.includes('low') || lower.includes('🟢')) return 'low';
    return 'medium';
  }

  extractLine(text) {
    const lineMatch = text.match(/line\s*[:#]?(\d+)/i);
    return lineMatch ? parseInt(lineMatch[1]) : null;
  }

  extractSummary(text) {
    const summaryMatch = text.match(/(?:summary|overview)[:\s]+([\s\S]+?)(?:\n\n|$)/i);
    return summaryMatch ? summaryMatch[1].trim() : 'Review complete';
  }

  extractSuggestions(text) {
    const suggestions = [];
    const suggestionMatches = text.matchAll(/(?:suggestion|recommendation|fix)[:\s]+(.+?)(?:\n\n|$)/gi);
    for (const match of suggestionMatches) {
      suggestions.push(match[1].trim());
    }
    return suggestions;
  }

  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Review complete. No issues found.';
    }
  };
}

// ============================================
// Specialized Workers
// ============================================

class SyntaxWorker extends WorkerAgent {
  constructor(id, llm) {
    super(id, ['javascript', 'typescript', 'eslint'], { codeReview: true });
    this.llm = llm;
  }

  async execute(subtask) {
    const prompt = `
**Syntax and Code Style Review**

Review the code for:
1. ESLint compliance
2. Code formatting
3. Naming conventions
4. Comment quality
5. JSDoc documentation

Code:
${subtask.code || subtask.description}

Provide specific issues with line numbers and fixes.`;

    return await this.llm.generate(prompt);
  }
}

class LogicWorker extends WorkerAgent {
  constructor(id, llm) {
    super(id, ['javascript', 'code-review', 'debugging'], { codeReview: true });
    this.llm = llm;
  }

  async execute(subtask) {
    const prompt = `
**Logic and Bug Detection Review**

Review the code for:
1. Null/undefined handling
2. Error handling
3. Edge cases
4. Logic errors
5. Code duplication
6. Maintainability

Code:
${subtask.code || subtask.description}

Identify potential bugs and logic issues.`;

    return await this.llm.generate(prompt);
  }
}

class SecurityWorker extends WorkerAgent {
  constructor(id, llm) {
    super(id, ['security', 'javascript', 'owasp'], { codeReview: true });
    this.llm = llm;
  }

  async execute(subtask) {
    const prompt = `
**Security Vulnerability Scan**

Review the code for:
1. SQL injection
2. XSS (Cross-Site Scripting)
3. CSRF (Cross-Site Request Forgery)
4. Sensitive data exposure
5. Authentication/Authorization issues
6. Input validation

Code:
${subtask.code || subtask.description}

Highlight security vulnerabilities with severity ratings.`;

    return await this.llm.generate(prompt);
  }
}

class PerformanceWorker extends WorkerAgent {
  constructor(id, llm) {
    super(id, ['performance', 'javascript', 'optimization'], { codeReview: true });
    this.llm = llm;
  }

  async execute(subtask) {
    const prompt = `
**Performance Analysis**

Review the code for:
1. Time complexity issues
2. Space complexity issues
3. Unnecessary computations
4. Database query optimization
5. Caching opportunities
6. Memory leaks

Code:
${subtask.code || subtask.description}

Suggest performance optimizations.`;

    return await this.llm.generate(prompt);
  }
}

module.exports = { CodeReviewExpert };
