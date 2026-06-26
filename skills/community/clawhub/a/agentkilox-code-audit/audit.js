const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const TOOL_COST = 0; // Local tools
const SERVICE_PRICE = 0.25;
const PRICE_CENTS = 25;

/**
 * Run bandit security scan on Python code
 * Note: Bandit requires Python - fallback to enhanced static analysis if unavailable
 */
async function runBandit(code) {
  try {
    // Check if bandit is available
    const check = execSync('which bandit', { encoding: 'utf8' });
    
    const tmpFile = `/tmp/audit_${Date.now()}.py`;
    fs.writeFileSync(tmpFile, code);
    
    const result = execSync(`bandit -f json ${tmpFile}`, {
      encoding: 'utf8',
      timeout: 30000
    });
    
    fs.unlinkSync(tmpFile);
    return JSON.parse(result);
  } catch (e) {
    // Bandit not available - use enhanced static analysis
    return { issues: [], skipped: 'bandit_unavailable' };
  }
}

/**
 * Basic static analysis for common issues
 */
function basicAnalysis(code) {
  const issues = [];
  const lines = code.split('\n');
  
  // Check for hardcoded secrets
  const secretPatterns = [
    /api[_-]?key["']?\s*[:=]\s*["'][a-zA-Z0-9]{20,}/gi,
    /password["']?\s*[:=]\s*["'][^"']+/gi,
    /secret["']?\s*[:=]\s*["'][^"']+/gi,
    /token["']?\s*[:=]\s*["'][a-zA-Z0-9]{20,}/gi,
  ];
  
  lines.forEach((line, idx) => {
    secretPatterns.forEach(pattern => {
      if (pattern.test(line)) {
        issues.push({
          line: idx + 1,
          issue: 'Potential hardcoded secret detected',
          severity: 'HIGH',
          confidence: 'MEDIUM'
        });
      }
    });
  });
  
  // Check for dangerous functions
  const dangerousPatterns = [
    { pattern: /eval\s*\(/, issue: 'Use of eval() - code injection risk', severity: 'HIGH' },
    { pattern: /exec\s*\(/, issue: 'Use of exec() - code injection risk', severity: 'HIGH' },
    { pattern: /subprocess\.call\s*\([^)]*shell\s*=\s*True/, issue: 'shell=True in subprocess - avoid', severity: 'HIGH' },
    { pattern: /__import__\s*\(\s*["'](os|sys|subprocess)/, issue: 'Dynamic import of sensitive module', severity: 'MEDIUM' },
  ];
  
  lines.forEach((line, idx) => {
    dangerousPatterns.forEach(({ pattern, issue, severity }) => {
      if (pattern.test(line)) {
        issues.push({
          line: idx + 1,
          issue,
          severity,
          confidence: 'HIGH'
        });
      }
    });
  });
  
  return issues;
}

/**
 * Main audit function
 */
async function auditCode(code, language = 'python') {
  const startTime = Date.now();
  const toolCost = TOOL_COST;
  
  let results = {
    tool: language === 'python' ? 'bandit' : 'static',
    timestamp: new Date().toISOString(),
    issues: [],
    stats: {
      linesOfCode: code.split('\n').length,
      scanTimeMs: 0,
      cost: toolCost
    }
  };
  
  if (language === 'python') {
    const banditResult = await runBandit(code);
    if (banditResult.results) {
      results.issues = banditResult.results.map(r => ({
        line: r.line_number,
        issue: r.issue_text,
        severity: r.issue_severity.toUpperCase(),
        confidence: r.issue_confidence.toUpperCase(),
        testId: r.test_id
      }));
    }
  }
  
  // Add basic analysis for all languages
  const basicIssues = basicAnalysis(code);
  results.issues = [...results.issues, ...basicIssues];
  
  // Deduplicate
  const seen = new Set();
  results.issues = results.issues.filter(i => {
    const key = `${i.line}:${i.issue}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
  
  results.stats.scanTimeMs = Date.now() - startTime;
  
  // Calculate confidence score (0-100)
  const highCount = results.issues.filter(i => i.severity === 'HIGH').length;
  const medCount = results.issues.filter(i => i.severity === 'MEDIUM').length;
  const score = Math.max(0, 100 - (highCount * 10) - (medCount * 3));
  
  results.confidenceScore = score;
  results.priceCents = PRICE_CENTS;
  
  return results;
}

module.exports = { auditCode, SERVICE_PRICE, PRICE_CENTS };