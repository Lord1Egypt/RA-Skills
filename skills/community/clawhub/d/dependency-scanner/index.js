/**
 * Dependency Scanner Skill
 * Scans project dependencies for known security vulnerabilities
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * Run npm audit and parse results
 * @param {string} targetDir - Directory to scan
 * @param {object} options - Scan options
 * @returns {object} Scan results
 */
function scanDependencies(targetDir = process.cwd(), options = {}) {
  const results = {
    timestamp: new Date().toISOString(),
    target: targetDir,
    summary: {
      total: 0,
      critical: 0,
      high: 0,
      moderate: 0,
      low: 0,
      info: 0
    },
    vulnerabilities: [],
    recommendations: []
  };

  // Check if package.json exists
  const packageJsonPath = path.join(targetDir, 'package.json');
  if (!fs.existsSync(packageJsonPath)) {
    results.error = 'No package.json found in target directory';
    results.recommendations.push('Run this scanner in a Node.js project directory');
    return results;
  }

  try {
    // Run npm audit --json
    const auditOutput = execSync('npm audit --json', {
      cwd: targetDir,
      encoding: 'utf8',
      timeout: 60000,
      stdio: ['pipe', 'pipe', 'pipe']
    });

    const audit = JSON.parse(auditOutput);

    // Parse audit results
    if (audit.auditReportVersion) {
      const metadata = audit.metadata || {};
      results.summary.total = metadata.vulnerabilities?.total || 0;
      results.summary.critical = metadata.vulnerabilities?.critical || 0;
      results.summary.high = metadata.vulnerabilities?.high || 0;
      results.summary.moderate = metadata.vulnerabilities?.moderate || 0;
      results.summary.low = metadata.vulnerabilities?.low || 0;
      results.summary.info = metadata.vulnerabilities?.info || 0;
    }

    // Extract vulnerability details
    if (audit.vulnerabilities) {
      for (const [name, vuln] of Object.entries(audit.vulnerabilities)) {
        if (vuln.severity && vuln.via) {
          results.vulnerabilities.push({
            package: name,
            severity: vuln.severity,
            version: vuln.effects?.[0] || 'unknown',
            via: Array.isArray(vuln.via) ? vuln.via.map(v => typeof v === 'string' ? v : v.title || v) : [vuln.via],
            fixAvailable: vuln.fixAvailable || false,
            path: vuln.name || name
          });
        }
      }
    }

    // Generate recommendations
    if (results.summary.critical > 0) {
      results.recommendations.push('CRITICAL: Update vulnerable packages immediately');
      results.recommendations.push('Run: npm audit fix --force (review changes first)');
    }
    if (results.summary.high > 0) {
      results.recommendations.push('HIGH: Address high-severity vulnerabilities soon');
      results.recommendations.push('Run: npm audit fix');
    }
    if (results.summary.moderate > 0) {
      results.recommendations.push('MODERATE: Consider updating affected packages');
    }
    if (results.summary.total === 0) {
      results.recommendations.push('No vulnerabilities found - dependencies are secure');
    }

  } catch (error) {
    // npm audit returns non-zero exit code when vulnerabilities found
    if (error.stdout) {
      try {
        const audit = JSON.parse(error.stdout);
        const metadata = audit.metadata || {};
        results.summary.total = metadata.vulnerabilities?.total || 0;
        results.summary.critical = metadata.vulnerabilities?.critical || 0;
        results.summary.high = metadata.vulnerabilities?.high || 0;
        results.summary.moderate = metadata.vulnerabilities?.moderate || 0;
        results.summary.low = metadata.vulnerabilities?.low || 0;

        // Still parse vulnerabilities from error output
        if (audit.vulnerabilities) {
          for (const [name, vuln] of Object.entries(audit.vulnerabilities)) {
            if (vuln.severity) {
              results.vulnerabilities.push({
                package: name,
                severity: vuln.severity,
                version: vuln.effects?.[0] || 'unknown',
                via: Array.isArray(vuln.via) ? vuln.via.map(v => typeof v === 'string' ? v : v.title || v) : [],
                fixAvailable: vuln.fixAvailable || false
              });
            }
          }
        }

        if (results.summary.total > 0) {
          results.recommendations.push('Vulnerabilities detected - review and fix');
        } else {
          results.recommendations.push('No vulnerabilities found - dependencies are secure');
        }
      } catch (parseError) {
        results.error = 'Failed to parse npm audit output';
      }
    } else {
      results.error = error.message;
    }
  }

  return results;
}

/**
 * Format scan results for display
 * @param {object} results - Scan results
 * @returns {string} Formatted output
 */
function formatResults(results) {
  const lines = [];

  lines.push('=== Dependency Security Scan ===');
  lines.push(`Target: ${results.target}`);
  lines.push(`Time: ${results.timestamp}`);
  lines.push('');

  if (results.error && results.summary.total === 0) {
    lines.push(`ERROR: ${results.error}`);
    return lines.join('\n');
  }

  lines.push('Summary:');
  lines.push(`  Total vulnerabilities: ${results.summary.total}`);
  if (results.summary.critical > 0) lines.push(`  Critical: ${results.summary.critical}`);
  if (results.summary.high > 0) lines.push(`  High: ${results.summary.high}`);
  if (results.summary.moderate > 0) lines.push(`  Moderate: ${results.summary.moderate}`);
  if (results.summary.low > 0) lines.push(`  Low: ${results.summary.low}`);
  lines.push('');

  if (results.vulnerabilities.length > 0) {
    lines.push('Vulnerabilities:');
    for (const vuln of results.vulnerabilities) {
      lines.push(`  [${vuln.severity.toUpperCase()}] ${vuln.package}@${vuln.version}`);
      if (vuln.via.length > 0) {
        lines.push(`    Via: ${vuln.via.slice(0, 2).join(', ')}${vuln.via.length > 2 ? '...' : ''}`);
      }
      lines.push(`    Fix available: ${vuln.fixAvailable ? 'Yes' : 'No'}`);
    }
    lines.push('');
  }

  if (results.recommendations.length > 0) {
    lines.push('Recommendations:');
    for (const rec of results.recommendations) {
      lines.push(`  - ${rec}`);
    }
  }

  return lines.join('\n');
}

/**
 * Main entry point
 */
function main() {
  const targetDir = process.argv[2] || process.cwd();
  const results = scanDependencies(targetDir);
  console.log(formatResults(results));

  // Exit with error code if critical vulnerabilities found
  if (results.summary.critical > 0) {
    process.exit(1);
  }
}

module.exports = {
  scanDependencies,
  formatResults,
  main
};

// Run main if executed directly
if (require.main === module) {
  main();
}