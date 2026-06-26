#!/usr/bin/env node
/**
 * AVI Assess CLI
 * One command to score agent autonomy
 * 
 * Usage: npx avi-assess [--verbose] [--json] [--workspace=PATH]
 */

const path = require('path');
const { assessAutonomy } = require(path.join(__dirname, 'assess.js'));

const colors = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

function parseArgs() {
  const args = process.argv.slice(2);
  return {
    workspace: args.find(a => a.startsWith('--workspace='))?.split('=')[1],
    verbose: args.includes('--verbose') || args.includes('-v'),
    json: args.includes('--json'),
    help: args.includes('--help') || args.includes('-h')
  };
}

function showHelp() {
  console.log(`
${colors.bold}${colors.cyan}AVI Assess — Agentic Verifiable Independence${colors.reset}
Score your agent's autonomy in one command

${colors.bold}Usage:${colors.reset}
  npx avi-assess                    # Quick score
  npx avi-assess --verbose          # Full breakdown
  npx avi-assess --json             # Machine-readable
  npx avi-assess --workspace=./path # Custom workspace

${colors.bold}Tiers:${colors.reset}
  81-100: ${colors.green}Autonomous${colors.reset}        (Tier 5)
  61-80:  ${colors.blue}Semi-Autonomous${colors.reset}   (Tier 4)
  41-60:  ${colors.yellow}Hybrid${colors.reset}            (Tier 3)
  21-40:  ${colors.magenta}Assisted${colors.reset}          (Tier 2)
  0-20:   ${colors.dim}Puppet${colors.reset}             (Tier 1)

${colors.dim}Learn more: https://vi-protocol.io${colors.reset}
`);
}

function renderScorecard(report) {
  const { overallScore, tierName, dimensions } = report;
  
  // Color based on tier
  let scoreColor = colors.dim;
  if (overallScore >= 80) scoreColor = colors.green;
  else if (overallScore >= 65) scoreColor = colors.blue;
  else if (overallScore >= 50) scoreColor = colors.yellow;
  else if (overallScore >= 35) scoreColor = colors.magenta;

  console.log(`
${colors.bold}${colors.cyan}╔════════════════════════════════════════╗
║   Agentic Verifiable Independence      ║
╚════════════════════════════════════════╝${colors.reset}

${colors.bold}AVI Score:${colors.reset} ${scoreColor}${overallScore}${colors.reset}/100
${colors.bold}Tier:${colors.reset} ${scoreColor}${tierName}${colors.reset}

${colors.bold}Dimensional Breakdown:${colors.reset}
  ${colors.dim}Financial Autonomy${colors.reset}       ${dimensions.financial.score}/100 ${renderBar(dimensions.financial.score)}
  ${colors.dim}Temporal Autonomy${colors.reset}        ${dimensions.temporal.score}/100 ${renderBar(dimensions.temporal.score)}
  ${colors.dim}Information Independence${colors.reset} ${dimensions.informational.score}/100 ${renderBar(dimensions.informational.score)}
  ${colors.dim}Communication${colors.reset}            ${dimensions.social.score}/100 ${renderBar(dimensions.social.score)}
  ${colors.dim}Operational${colors.reset}              ${dimensions.operational.score}/100 ${renderBar(dimensions.operational.score)}

${colors.dim}Assessment ID: ${report.assessmentId}${colors.reset}
${colors.dim}Verified: ${new Date(report.verifiedAt).toLocaleString()}${colors.reset}
`);
}

function renderBar(score) {
  const filled = Math.round(score / 10);
  const empty = 10 - filled;
  return '█'.repeat(filled) + colors.dim + '░'.repeat(empty) + colors.reset;
}

async function main() {
  const args = parseArgs();
  
  if (args.help) {
    showHelp();
    process.exit(0);
  }

  try {
    const report = await assessAutonomy({
      workspace: args.workspace,
      verbose: args.verbose
    });

    if (args.json) {
      console.log(JSON.stringify(report, null, 2));
    } else if (args.verbose) {
      console.log('\n' + JSON.stringify(report, null, 2));
    } else {
      renderScorecard(report);
    }
  } catch (err) {
    console.error(`${colors.bold}${colors.red}Error:${colors.reset}`, err.message);
    process.exit(1);
  }
}

main();