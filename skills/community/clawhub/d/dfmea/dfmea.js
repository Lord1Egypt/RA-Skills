#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// DFMEA Analysis Class
class DFMEA {
  constructor() {
    this.rpnThresholds = {
      high: 120,
      medium: 80,
      low: 40
    };
  }

  // Calculate Risk Priority Number (RPN)
  calculateRPN(severity, occurrence, detection) {
    return severity * occurrence * detection;
  }

  // Categorize risk level based on RPN
  categorizeRisk(rpn) {
    if (rpn >= this.rpnThresholds.high) return 'High';
    if (rpn >= this.rpnThresholds.medium) return 'Medium';
    if (rpn >= this.rpnThresholds.low) return 'Low';
    return 'Minimal';
  }

  // Generate DFMEA template
  generateTemplate(projectName, teamMembers = []) {
    const template = {
      projectInfo: {
        projectName: projectName,
        teamMembers: teamMembers,
        date: new Date().toISOString().split('T')[0],
        revision: '1.0'
      },
      dfmeaItems: [],
      summary: {
        totalItems: 0,
        highRiskItems: 0,
        mediumRiskItems: 0,
        lowRiskItems: 0,
        minimalRiskItems: 0
      }
    };
    return template;
  }

  // Add a DFMEA item
  addItem(dfmea, itemData) {
    const { 
      functionDesc, 
      failureMode, 
      effects, 
      severity, 
      causes, 
      occurrence, 
      currentControls, 
      detection,
      recommendedActions = []
    } = itemData;

    const rpn = this.calculateRPN(severity, occurrence, detection);
    const riskLevel = this.categorizeRisk(rpn);

    const newItem = {
      id: dfmea.dfmeaItems.length + 1,
      function: functionDesc,
      failureMode,
      effects,
      severity,
      causes,
      occurrence,
      currentControls,
      detection,
      rpn,
      riskLevel,
      recommendedActions,
      status: 'Open'
    };

    dfmea.dfmeaItems.push(newItem);
    this.updateSummary(dfmea);
    return newItem;
  }

  // Update summary statistics
  updateSummary(dfmea) {
    const items = dfmea.dfmeaItems;
    dfmea.summary.totalItems = items.length;
    dfmea.summary.highRiskItems = items.filter(item => item.riskLevel === 'High').length;
    dfmea.summary.mediumRiskItems = items.filter(item => item.riskLevel === 'Medium').length;
    dfmea.summary.lowRiskItems = items.filter(item => item.riskLevel === 'Low').length;
    dfmea.summary.minimalRiskItems = items.filter(item => item.riskLevel === 'Minimal').length;
  }

  // Generate risk report
  generateRiskReport(dfmea) {
    const summary = dfmea.summary;
    const highRiskItems = dfmea.dfmeaItems
      .filter(item => item.riskLevel === 'High')
      .sort((a, b) => b.rpn - a.rpn);

    let report = `# DFMEA Risk Report\n\n`;
    report += `## Project Summary\n`;
    report += `- Project: ${dfmea.projectInfo.projectName}\n`;
    report += `- Team: ${dfmea.projectInfo.teamMembers.join(', ') || 'Not specified'}\n`;
    report += `- Date: ${dfmea.projectInfo.date}\n\n`;

    report += `## Risk Summary\n`;
    report += `| Risk Level | Count |\n`;
    report += `|------------|-------|\n`;
    report += `| High       | ${summary.highRiskItems} |\n`;
    report += `| Medium     | ${summary.mediumRiskItems} |\n`;
    report += `| Low        | ${summary.lowRiskItems} |\n`;
    report += `| Minimal    | ${summary.minimalRiskItems} |\n\n`;

    if (highRiskItems.length > 0) {
      report += `## High Risk Items (RPN ≥ ${this.rpnThresholds.high})\n\n`;
      highRiskItems.forEach(item => {
        report += `### Item ${item.id}: ${item.function}\n`;
        report += `- **Failure Mode**: ${item.failureMode}\n`;
        report += `- **Effects**: ${item.effects}\n`;
        report += `- **Severity**: ${item.severity}/10\n`;
        report += `- **Causes**: ${item.causes}\n`;
        report += `- **Occurrence**: ${item.occurrence}/10\n`;
        report += `- **Current Controls**: ${item.currentControls}\n`;
        report += `- **Detection**: ${item.detection}/10\n`;
        report += `- **RPN**: ${item.rpn}\n`;
        report += `- **Recommended Actions**: ${Array.isArray(item.recommendedActions) ? item.recommendedActions.join('; ') : item.recommendedActions || 'None specified'}\n\n`;
      });
    }

    return report;
  }

  // Export to JSON
  exportToJson(dfmea, filename) {
    fs.writeFileSync(filename, JSON.stringify(dfmea, null, 2));
  }

  // Import from JSON
  importFromJson(filename) {
    if (!fs.existsSync(filename)) {
      throw new Error(`File ${filename} not found`);
    }
    return JSON.parse(fs.readFileSync(filename, 'utf8'));
  }
}

// Command line interface
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  const dfmea = new DFMEA();

  switch (command) {
    case 'create':
      const projectName = args[1] || 'New DFMEA Project';
      const teamMembers = args.slice(2);
      const template = dfmea.generateTemplate(projectName, teamMembers);
      const outputFile = `${projectName.replace(/\s+/g, '_')}_dfmea.json`;
      dfmea.exportToJson(template, outputFile);
      console.log(`DFMEA template created: ${outputFile}`);
      break;

    case 'add-item':
      if (args.length < 2) {
        console.error('Usage: dfmea add-item <dfmea-file> [options]');
        process.exit(1);
      }
      const dfmeaFile = args[1];
      // This would need more sophisticated argument parsing for a full CLI
      console.log('Adding DFMEA item (interactive mode would be implemented here)');
      break;

    case 'report':
      if (args.length < 2) {
        console.error('Usage: dfmea report <dfmea-file>');
        process.exit(1);
      }
      const reportFile = args[1];
      try {
        const dfmeaData = dfmea.importFromJson(reportFile);
        const report = dfmea.generateRiskReport(dfmeaData);
        console.log(report);
      } catch (error) {
        console.error('Error generating report:', error.message);
        process.exit(1);
      }
      break;

    case 'help':
    default:
      console.log(`
DFMEA - Design Failure Mode and Effects Analysis Tool

Usage:
  dfmea create <project-name> [team-member1 team-member2 ...]
  dfmea add-item <dfmea-file> [interactive mode]
  dfmea report <dfmea-file>
  dfmea help

Examples:
  dfmea create "Brake System Design" "John Doe" "Jane Smith"
  dfmea report brake_system_design_dfmea.json
      `);
  }
}

if (require.main === module) {
  main();
}

module.exports = DFMEA;