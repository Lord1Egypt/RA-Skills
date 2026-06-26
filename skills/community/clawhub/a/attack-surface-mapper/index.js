/**
 * Attack Surface Mapper Skill
 * Purple team tool to map agent's attack surface and defense coverage
 */

import fs from 'fs';
import path from 'path';

export default {
  name: 'attack-surface-mapper',
  version: '1.0.0',
  emoji: '🗺️',

  config: {
    reportDir: '.security/surface-map',
    redTeamLogDirs: ['.security/red-team'],
    blueTeamLogDirs: ['.security/firewall-logs', '.security/anomalies'],
    auditReportDir: '.security/audits'
  },

  async execute(input = {}) {
    const mode = input.mode || 'map'; // 'map', 'report', 'list-surfaces'
    const targetDir = input.path || process.cwd();

    try {
      switch (mode) {
        case 'list-surfaces':
          return { success: true, surfaces: this.listAttackSurfaces() };
        case 'map':
          return await this.mapSurface(targetDir);
        case 'report':
          return await this.generateReport(targetDir);
        default:
          return { success: false, error: `Unknown mode: ${mode}` };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  /**
   * Map the agent's attack surface
   */
  async mapSurface(targetDir) {
    console.log(`🗺️ Mapping attack surface in: ${targetDir}\n`);

    const surfaces = this.listAttackSurfaces();
    const redTeamResults = await this.loadRedTeamResults(targetDir);
    const blueTeamDetections = await this.loadBlueTeamDetections(targetDir);
    const auditReports = await this.loadAuditReports(targetDir);

    const coverageMatrix = [];

    for (const surface of surfaces) {
      const vectors = this.getAttackVectorsForSurface(surface);
      for (const vector of vectors) {
        const redTested = this.wasRedTested(surface, vector, redTeamResults);
        const blueDetected = this.wasBlueDetected(surface, vector, blueTeamDetections, auditReports);
        const status = this.getCoverageStatus(redTested, blueDetected);
        const { riskScore, priority } = this.calculateRisk(surface, vector, status);

        coverageMatrix.push({
          surface,
          vector,
          redTested: redTested ? 'YES' : 'NO',
          blueDetected: blueDetected ? (blueDetected.full ? 'YES' : 'PARTIAL') : 'NO',
          status,
          riskScore,
          priority
        });
      }
    }

    const report = {
      generated: new Date().toISOString(),
      targetDir,
      coverageMatrix,
      summary: this.summarizeCoverage(coverageMatrix),
      hardeningPlan: this.generateHardeningPlan(coverageMatrix)
    };

    // Save report
    const reportDir = path.join(targetDir, this.config.reportDir);
    if (!fs.existsSync(reportDir)) {
      fs.mkdirSync(reportDir, { recursive: true });
    }
    const reportFile = path.join(reportDir, `surface-map-${new Date().toISOString().split('T')[0]}.json`);
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));

    return { success: true, reportFile, report };
  },

  /**
   * List all known attack surfaces
   */
  listAttackSurfaces() {
    return [
      'CHANNELS',
      'SKILLS',
      'TOOLS',
      'MODELS',
      'MEMORY',
      'INTER-AGENT',
      'SUPPLY_CHAIN'
    ];
  },

  /**
   * Get attack vectors for a given surface
   */
  getAttackVectorsForSurface(surface) {
    switch (surface) {
      case 'CHANNELS': return ['prompt-injection', 'social-engineering', 'phishing'];
      case 'SKILLS': return ['malicious-instructions', 'data-theft', 'privilege-escalation'];
      case 'TOOLS': return ['command-injection', 'path-traversal', 'ssrf', 'rce'];
      case 'MODELS': return ['prompt-injection', 'model-confusion', 'jailbreak'];
      case 'MEMORY': return ['memory-poisoning', 'persistence', 'false-context'];
      case 'INTER_AGENT': return ['agent-to-agent-attack', 'lateral-movement'];
      case 'SUPPLY_CHAIN': return ['typosquatting', 'compromised-package', 'repo-takeover'];
      default: return [];
    }
  },

  /**
   * Load red team test results
   */
  async loadRedTeamResults(targetDir) {
    const results = [];
    for (const dir of this.config.redTeamLogDirs) {
      const fullDir = path.join(targetDir, dir);
      if (fs.existsSync(fullDir)) {
        const files = fs.readdirSync(fullDir).filter(f => f.endsWith('.jsonl'));
        for (const file of files) {
          const content = fs.readFileSync(path.join(fullDir, file), 'utf-8');
          content.split('\n').filter(Boolean).forEach(line => {
            try { results.push(JSON.parse(line)); } catch (e) { /* ignore */ }
          });
        }
      }
    }
    return results;
  },

  /**
   * Load blue team detection events
   */
  async loadBlueTeamDetections(targetDir) {
    const detections = [];
    for (const dir of this.config.blueTeamLogDirs) {
      const fullDir = path.join(targetDir, dir);
      if (fs.existsSync(fullDir)) {
        const files = fs.readdirSync(fullDir).filter(f => f.endsWith('.jsonl'));
        for (const file of files) {
          const content = fs.readFileSync(path.join(fullDir, file), 'utf-8');
          content.split('\n').filter(Boolean).forEach(line => {
            try { detections.push(JSON.parse(line)); } catch (e) { /* ignore */ }
          });
        }
      }
    }
    return detections;
  },

  /**
   * Load audit reports (from config-hardener, dependency-sentinel, etc.)
   */
  async loadAuditReports(targetDir) {
    const reports = [];
    const auditDir = path.join(targetDir, this.config.auditReportDir);
    if (fs.existsSync(auditDir)) {
      const files = fs.readdirSync(auditDir).filter(f => f.endsWith('.json') || f.endsWith('.md'));
      for (const file of files) {
        // Just list names for now, full parsing is complex
        reports.push(file);
      }
    }
    return reports;
  },

  /**
   * Check if a specific surface/vector was red team tested
   */
  wasRedTested(surface, vector, redTeamResults) {
    // Simplified: Check if prompt-injector ran for 'prompt-injection'
    if (vector === 'prompt-injection') {
      return redTeamResults.some(r => r.planId?.startsWith('INJ-'));
    }
    // Simplified: Check if chaos-agent ran for some generic 'rce'
    if (vector === 'rce') {
      return redTeamResults.some(r => r.planId?.startsWith('CHAOS-'));
    }
    return false; // Default to not tested
  },

  /**
   * Check if a specific surface/vector was blue team detected
   */
  wasBlueDetected(surface, vector, blueTeamDetections, auditReports) {
    // Simplified: Check firewall logs for 'prompt-injection'
    if (vector === 'prompt-injection') {
      return blueTeamDetections.some(d => d.action?.message?.includes('Prompt injection'));
    }
    // Simplified: Check anomaly logs for 'data-theft'
    if (vector === 'data-theft') {
      return blueTeamDetections.some(d => d.metric === 'data_volume' && d.classification === 'CRITICAL');
    }
    // Simplified: Check if config-hardener audit report exists for 'config-security'
    if (vector === 'config-security') {
      return auditReports.some(r => r.includes('config-hardener'));
    }
    return null; // Default to not detected
  },

  /**
   * Determine coverage status
   */
  getCoverageStatus(redTested, blueDetected) {
    if (redTested && blueDetected) return 'COVERED';
    if (redTested && !blueDetected) return 'GAP';
    if (!redTested && blueDetected) return 'PARTIAL'; // Blue detected, but no formal red test yet
    return 'GAP'; // No red test, no blue detection
  },

  /**
   * Calculate risk score for a gap
   */
  calculateRisk(surface, vector, status) {
    if (status === 'COVERED') return { riskScore: 0, priority: 'NONE' };

    let impact = 1;
    let likelihood = 1;

    switch (vector) {
      case 'prompt-injection': impact = 4; likelihood = 4; break;
      case 'command-injection': impact = 5; likelihood = 5; break;
      case 'data-theft': impact = 5; likelihood = 4; break;
      case 'malicious-instructions': impact = 4; likelihood = 3; break;
      case 'typosquatting': impact = 3; likelihood = 3; break;
      case 'phishing': impact = 3; likelihood = 4; break;
    }

    const riskScore = impact * likelihood;
    let priority = 'LOW';
    if (riskScore >= 20) priority = 'CRITICAL';
    else if (riskScore >= 12) priority = 'HIGH';
    else if (riskScore >= 6) priority = 'MEDIUM';

    return { riskScore, priority };
  },

  /**
   * Summarize coverage matrix
   */
  summarizeCoverage(matrix) {
    const summary = { covered: 0, partial: 0, gaps: 0, criticalGaps: 0, highGaps: 0 };
    matrix.forEach(row => {
      if (row.status === 'COVERED') summary.covered++;
      else if (row.status === 'PARTIAL') summary.partial++;
      else {
        summary.gaps++;
        if (row.priority === 'CRITICAL') summary.criticalGaps++;
        if (row.priority === 'HIGH') summary.highGaps++;
      }
    });
    return summary;
  },

  /**
   * Generate prioritized hardening plan
   */
  generateHardeningPlan(matrix) {
    const hardeningPlan = [];
    matrix.filter(row => row.status !== 'COVERED').sort((a, b) => b.riskScore - a.riskScore)
      .forEach(row => {
        hardeningPlan.push({
          priority: row.priority,
          surface: row.surface,
          vector: row.vector,
          status: row.status,
          riskScore: row.riskScore,
          recommendation: `Implement red/blue coverage for ${row.surface} - ${row.vector}`
        });
      });
    return hardeningPlan;
  },

  /**
   * Generate report in markdown format
   */
  async generateReport(targetDir) {
    const reportDir = path.join(targetDir, this.config.reportDir);
    const reportFile = path.join(reportDir, `surface-map-${new Date().toISOString().split('T')[0]}.json`);

    if (!fs.existsSync(reportFile)) {
      return { success: false, error: 'No map report found. Run mode:map first.' };
    }
    const report = JSON.parse(fs.readFileSync(reportFile, 'utf-8'));

    let markdown = `# Attack Surface Map - ${report.generated.split('T')[0]}\n\n`;
    markdown += `## Summary\n\n`;
    markdown += `- Total surfaces mapped: ${report.coverageMatrix.length}\n`;
    markdown += `- Covered: ${report.summary.covered}\n`;
    markdown += `- Partial: ${report.summary.partial}\n`;
    markdown += `- Gaps: ${report.summary.gaps}\n`;
    markdown += `- Critical Gaps: ${report.summary.criticalGaps}\n`;
    markdown += `- High Gaps: ${report.summary.highGaps}\n\n`;

    markdown += `## Coverage Matrix\n\n`;
    markdown += `| Surface | Vector | Red Tested | Blue Detected | Status | Risk Score | Priority |\n`;
    markdown += `|---------|--------|------------|---------------|--------|------------|----------|\n`;
    report.coverageMatrix.forEach(row => {
      markdown += `| ${row.surface} | ${row.vector} | ${row.redTested} | ${row.blueDetected} | ${row.status} | ${row.riskScore} | ${row.priority} |\n`;
    });
    markdown += `\n`;

    if (report.hardeningPlan.length > 0) {
      markdown += `## Prioritized Hardening Plan\n\n`;
      markdown += `| Priority | Surface | Vector | Status | Risk Score | Recommendation |\n`;
      markdown += `|----------|---------|--------|--------|------------|----------------|\n`;
      report.hardeningPlan.forEach(plan => {
        markdown += `| ${plan.priority} | ${plan.surface} | ${plan.vector} | ${plan.status} | ${plan.riskScore} | ${plan.recommendation} |\n`;
      });
      markdown += `\n`;
    }

    const markdownFile = path.join(reportDir, `surface-map-${new Date().toISOString().split('T')[0]}.md`);
    fs.writeFileSync(markdownFile, markdown);

    return { success: true, markdownFile, markdown };
  },

  async validate(input) {
    return typeof input === 'object';
  }
};
