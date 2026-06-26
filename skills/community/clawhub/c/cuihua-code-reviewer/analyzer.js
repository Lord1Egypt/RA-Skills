#!/usr/bin/env node

/**
 * code-reviewer - AI Code Review Engine
 * Core analysis logic for detecting security, performance, and quality issues
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class CodeReviewer {
  constructor(options = {}) {
    this.options = {
      severity: options.severity || 'medium',
      languages: options.languages || ['javascript', 'python', 'go', 'rust'],
      output: options.output || 'markdown',
      ...options
    };
    
    this.issues = [];
    this.stats = {
      filesAnalyzed: 0,
      linesAnalyzed: 0,
      issuesFound: 0,
      critical: 0,
      high: 0,
      medium: 0,
      low: 0
    };
  }

  /**
   * Analyze a single file
   */
  async analyzeFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    const ext = path.extname(filePath);
    
    this.stats.filesAnalyzed++;
    this.stats.linesAnalyzed += lines.length;

    // Detect language
    const language = this.detectLanguage(ext);
    if (!this.options.languages.includes(language)) {
      return;
    }

    // Run checks
    this.checkSecurity(filePath, content, lines);
    this.checkPerformance(filePath, content, lines);
    this.checkQuality(filePath, content, lines);
    this.checkBestPractices(filePath, content, lines);
  }

  /**
   * Security checks
   */
  checkSecurity(filePath, content, lines) {
    // Check for hardcoded secrets
    const secretPatterns = [
      { regex: /(['"])(sk-[a-zA-Z0-9]{32,})\1/, name: 'OpenAI API Key' },
      { regex: /(['"])([A-Za-z0-9]{40})\1.*github/i, name: 'GitHub Token' },
      { regex: /password\s*=\s*['"][^'"]+['"]/i, name: 'Hardcoded Password' },
      { regex: /api[_-]?key\s*=\s*['"][^'"]+['"]/i, name: 'Hardcoded API Key' }
    ];

    lines.forEach((line, index) => {
      secretPatterns.forEach(pattern => {
        if (pattern.regex.test(line)) {
          this.addIssue({
            file: filePath,
            line: index + 1,
            severity: 'critical',
            category: 'security',
            title: `Hardcoded ${pattern.name}`,
            description: 'Sensitive credentials found in code',
            code: line.trim(),
            fix: 'Move to environment variables or secure vault',
            impact: 'Credentials could be exposed in version control or logs'
          });
        }
      });
    });

    // Check for command injection
    const cmdInjectionPatterns = [
      /exec\s*\(\s*`.*\$\{.*\}.*`\s*\)/,
      /exec\s*\(\s*['"].*\+.*['"]\s*\)/,
      /spawn\s*\(\s*['"].*\+.*['"]/,
      /child_process\.exec.*\$\{/
    ];

    lines.forEach((line, index) => {
      cmdInjectionPatterns.forEach(pattern => {
        if (pattern.test(line)) {
          this.addIssue({
            file: filePath,
            line: index + 1,
            severity: 'critical',
            category: 'security',
            title: 'Potential Command Injection',
            description: 'Unsanitized input in shell command',
            code: line.trim(),
            fix: 'Use execFile() or properly escape arguments',
            impact: 'Attacker could execute arbitrary system commands'
          });
        }
      });
    });

    // Check for SQL injection (JavaScript/Python)
    if (content.includes('SELECT') || content.includes('INSERT')) {
      const sqlInjectionPatterns = [
        /`SELECT.*\$\{.*\}`/,
        /['"]SELECT.*\+.*['"]/,
        /f['"]SELECT.*\{.*\}['"]/  // Python f-strings
      ];

      lines.forEach((line, index) => {
        sqlInjectionPatterns.forEach(pattern => {
          if (pattern.test(line)) {
            this.addIssue({
              file: filePath,
              line: index + 1,
              severity: 'critical',
              category: 'security',
              title: 'SQL Injection Vulnerability',
              description: 'Unsanitized input in SQL query',
              code: line.trim(),
              fix: 'Use parameterized queries or ORM',
              impact: 'Database could be read, modified, or deleted'
            });
          }
        });
      });
    }

    // Check for eval() usage
    if (/\beval\s*\(/.test(content)) {
      lines.forEach((line, index) => {
        if (/\beval\s*\(/.test(line)) {
          this.addIssue({
            file: filePath,
            line: index + 1,
            severity: 'high',
            category: 'security',
            title: 'Dangerous eval() Usage',
            description: 'eval() executes arbitrary code',
            code: line.trim(),
            fix: 'Use safer alternatives like JSON.parse() or Function constructor',
            impact: 'Code injection vulnerability'
          });
        }
      });
    }
  }

  /**
   * Performance checks
   */
  checkPerformance(filePath, content, lines) {
    // Check for nested loops (potential O(n²))
    let loopDepth = 0;
    lines.forEach((line, index) => {
      if (/\b(for|while)\s*\(/.test(line)) {
        loopDepth++;
        if (loopDepth >= 2) {
          this.addIssue({
            file: filePath,
            line: index + 1,
            severity: 'medium',
            category: 'performance',
            title: 'Nested Loop Detected',
            description: 'Potential O(n²) or worse complexity',
            code: line.trim(),
            fix: 'Consider using Map/Set for O(n) lookups',
            impact: 'Performance degrades with input size'
          });
        }
      }
      if (/^\s*\}/.test(line)) {
        loopDepth = Math.max(0, loopDepth - 1);
      }
    });

    // Check for synchronous file operations
    const syncOps = ['readFileSync', 'writeFileSync', 'existsSync', 'statSync'];
    lines.forEach((line, index) => {
      syncOps.forEach(op => {
        if (line.includes(op) && !line.includes('//') && !line.includes('/*')) {
          this.addIssue({
            file: filePath,
            line: index + 1,
            severity: 'medium',
            category: 'performance',
            title: 'Synchronous File Operation',
            description: `${op} blocks the event loop`,
            code: line.trim(),
            fix: `Use async version: ${op.replace('Sync', '')}`,
            impact: 'Blocks other operations, poor scalability'
          });
        }
      });
    });

    // Check for regex in loops
    lines.forEach((line, index) => {
      if (/new\s+RegExp\(/.test(line) || /\/.*\/[gimuy]*(?!;)/.test(line)) {
        // Check if we're inside a loop (basic heuristic)
        const contextStart = Math.max(0, index - 10);
        const context = lines.slice(contextStart, index).join('\n');
        if (/\b(for|while|forEach|map)\b/.test(context)) {
          this.addIssue({
            file: filePath,
            line: index + 1,
            severity: 'low',
            category: 'performance',
            title: 'Regex Compiled in Loop',
            description: 'Regular expression compiled repeatedly',
            code: line.trim(),
            fix: 'Move regex compilation outside the loop',
            impact: 'Unnecessary CPU overhead'
          });
        }
      }
    });
  }

  /**
   * Code quality checks
   */
  checkQuality(filePath, content, lines) {
    // Check for long functions
    let functionStart = -1;
    let functionName = '';
    lines.forEach((line, index) => {
      const funcMatch = line.match(/function\s+(\w+)|const\s+(\w+)\s*=.*=>|(\w+)\s*\(/);
      if (funcMatch) {
        if (functionStart !== -1) {
          const length = index - functionStart;
          if (length > 50) {
            this.addIssue({
              file: filePath,
              line: functionStart + 1,
              severity: 'low',
              category: 'quality',
              title: 'Long Function',
              description: `Function ${functionName} is ${length} lines`,
              code: `function ${functionName}() { ... }`,
              fix: 'Break into smaller, focused functions',
              impact: 'Harder to understand and maintain'
            });
          }
        }
        functionStart = index;
        functionName = funcMatch[1] || funcMatch[2] || funcMatch[3] || 'anonymous';
      }
    });

    // Check for magic numbers
    lines.forEach((line, index) => {
      const magicNumbers = line.match(/\b(\d{3,})\b/g);
      if (magicNumbers && !line.includes('//') && !line.includes('const')) {
        magicNumbers.forEach(num => {
          if (parseInt(num) > 100) {
            this.addIssue({
              file: filePath,
              line: index + 1,
              severity: 'low',
              category: 'quality',
              title: 'Magic Number',
              description: `Unexplained constant: ${num}`,
              code: line.trim(),
              fix: 'Define as named constant',
              impact: 'Unclear intent, hard to maintain'
            });
          }
        });
      }
    });

    // Check for console.log in production code
    if (filePath.includes('src/') && !filePath.includes('test')) {
      lines.forEach((line, index) => {
        if (/console\.(log|debug|info)/.test(line) && !line.includes('//')) {
          this.addIssue({
            file: filePath,
            line: index + 1,
            severity: 'low',
            category: 'quality',
            title: 'Debug Statement in Production',
            description: 'console.log() found in production code',
            code: line.trim(),
            fix: 'Use proper logging library or remove',
            impact: 'Performance overhead, potential info leak'
          });
        }
      });
    }
  }

  /**
   * Best practices checks
   */
  checkBestPractices(filePath, content, lines) {
    // Check for error handling
    if (content.includes('async') || content.includes('Promise')) {
      let hasErrorHandling = content.includes('catch') || content.includes('try');
      if (!hasErrorHandling) {
        this.addIssue({
          file: filePath,
          line: 1,
          severity: 'medium',
          category: 'best-practices',
          title: 'Missing Error Handling',
          description: 'Async code without try/catch or .catch()',
          code: '(entire file)',
          fix: 'Add error handling for async operations',
          impact: 'Unhandled promise rejections, crashes'
        });
      }
    }

    // Check for TODO/FIXME comments
    lines.forEach((line, index) => {
      if (/\/\/\s*(TODO|FIXME|HACK|XXX)/.test(line)) {
        this.addIssue({
          file: filePath,
          line: index + 1,
          severity: 'low',
          category: 'best-practices',
          title: 'Technical Debt Marker',
          description: 'TODO/FIXME comment found',
          code: line.trim(),
          fix: 'Address the issue or create a ticket',
          impact: 'Incomplete implementation'
        });
      }
    });
  }

  /**
   * Add an issue to the list
   */
  addIssue(issue) {
    this.issues.push(issue);
    this.stats.issuesFound++;
    this.stats[issue.severity]++;
  }

  /**
   * Detect programming language from file extension
   */
  detectLanguage(ext) {
    const langMap = {
      '.js': 'javascript',
      '.mjs': 'javascript',
      '.cjs': 'javascript',
      '.ts': 'typescript',
      '.py': 'python',
      '.go': 'go',
      '.rs': 'rust',
      '.sh': 'shell'
    };
    return langMap[ext] || 'unknown';
  }

  /**
   * Generate report
   */
  generateReport(format = 'markdown') {
    if (format === 'markdown') {
      return this.generateMarkdownReport();
    } else if (format === 'json') {
      return JSON.stringify({
        stats: this.stats,
        issues: this.issues
      }, null, 2);
    } else {
      return this.generateTerminalReport();
    }
  }

  /**
   * Generate Markdown report
   */
  generateMarkdownReport() {
    const now = new Date().toLocaleString();
    let md = `# Code Review Report\n\n`;
    md += `**Generated**: ${now}\n`;
    md += `**Files Analyzed**: ${this.stats.filesAnalyzed}\n`;
    md += `**Lines Analyzed**: ${this.stats.linesAnalyzed}\n`;
    md += `**Total Issues**: ${this.stats.issuesFound}\n\n`;

    md += `## Issue Breakdown\n\n`;
    md += `- 🔴 Critical: ${this.stats.critical}\n`;
    md += `- 🟠 High: ${this.stats.high}\n`;
    md += `- 🟡 Medium: ${this.stats.medium}\n`;
    md += `- 🟢 Low: ${this.stats.low}\n\n`;

    // Group by severity
    const bySeverity = {
      critical: [],
      high: [],
      medium: [],
      low: []
    };

    this.issues.forEach(issue => {
      bySeverity[issue.severity].push(issue);
    });

    // Critical issues
    if (bySeverity.critical.length > 0) {
      md += `## 🔴 Critical Issues\n\n`;
      bySeverity.critical.forEach((issue, i) => {
        md += this.formatIssueMarkdown(issue, i + 1);
      });
    }

    // High issues
    if (bySeverity.high.length > 0) {
      md += `## 🟠 High Priority Issues\n\n`;
      bySeverity.high.forEach((issue, i) => {
        md += this.formatIssueMarkdown(issue, i + 1);
      });
    }

    // Medium issues
    if (bySeverity.medium.length > 0) {
      md += `## 🟡 Medium Priority Issues\n\n`;
      bySeverity.medium.forEach((issue, i) => {
        md += this.formatIssueMarkdown(issue, i + 1);
      });
    }

    // Low issues
    if (bySeverity.low.length > 0) {
      md += `## 🟢 Low Priority Issues\n\n`;
      bySeverity.low.forEach((issue, i) => {
        md += this.formatIssueMarkdown(issue, i + 1);
      });
    }

    md += `\n---\n\n`;
    md += `**Generated by code-reviewer** | 🌸 Made with ❤️ by 翠花\n`;

    return md;
  }

  /**
   * Format single issue for Markdown
   */
  formatIssueMarkdown(issue, number) {
    let md = `### ${number}. ${issue.title}\n\n`;
    md += `**File**: \`${issue.file}:${issue.line}\`  \n`;
    md += `**Category**: ${issue.category}  \n`;
    md += `**Severity**: ${issue.severity.toUpperCase()}\n\n`;
    md += `**Issue**:  \n${issue.description}\n\n`;
    md += `**Code**:\n\`\`\`\n${issue.code}\n\`\`\`\n\n`;
    md += `**Fix**:  \n${issue.fix}\n\n`;
    md += `**Impact**:  \n${issue.impact}\n\n`;
    md += `---\n\n`;
    return md;
  }

  /**
   * Generate terminal-friendly report
   */
  generateTerminalReport() {
    let report = `\n🔍 Code Review Summary\n`;
    report += `━`.repeat(50) + `\n\n`;
    report += `📁 Files analyzed: ${this.stats.filesAnalyzed}\n`;
    report += `📝 Lines analyzed: ${this.stats.linesAnalyzed}\n`;
    report += `⚠️  Issues found: ${this.stats.issuesFound}\n\n`;
    report += `Severity Breakdown:\n`;
    report += `  🔴 Critical: ${this.stats.critical}\n`;
    report += `  🟠 High:     ${this.stats.high}\n`;
    report += `  🟡 Medium:   ${this.stats.medium}\n`;
    report += `  🟢 Low:      ${this.stats.low}\n\n`;

    if (this.stats.issuesFound > 0) {
      report += `Top Issues:\n`;
      const topIssues = this.issues
        .sort((a, b) => {
          const severityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
          return severityOrder[a.severity] - severityOrder[b.severity];
        })
        .slice(0, 5);

      topIssues.forEach((issue, i) => {
        const emoji = { critical: '🔴', high: '🟠', medium: '🟡', low: '🟢' }[issue.severity];
        report += `  ${i + 1}. [${emoji} ${issue.severity.toUpperCase()}] ${issue.title} (${issue.file}:${issue.line})\n`;
      });
    }

    report += `\n💡 Run with --detailed for full report\n`;
    return report;
  }
}

export default CodeReviewer;

// CLI usage
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const targetPath = args[0] || '.';
  
  const reviewer = new CodeReviewer();
  
  // Analyze files
  const analyzeDirectory = (dir) => {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      
      if (stat.isDirectory() && !file.startsWith('.') && file !== 'node_modules') {
        analyzeDirectory(filePath);
      } else if (stat.isFile()) {
        const ext = path.extname(file);
        if (['.js', '.ts', '.py', '.go', '.rs'].includes(ext)) {
          reviewer.analyzeFile(filePath);
        }
      }
    });
  };
  
  if (fs.statSync(targetPath).isDirectory()) {
    analyzeDirectory(targetPath);
  } else {
    reviewer.analyzeFile(targetPath);
  }
  
  // Output report
  if (args.includes('--detailed')) {
    const report = reviewer.generateReport('markdown');
    fs.writeFileSync('code-review-report.md', report);
    console.log('📄 Detailed report saved to code-review-report.md');
  }
  
  console.log(reviewer.generateReport('terminal'));
}
