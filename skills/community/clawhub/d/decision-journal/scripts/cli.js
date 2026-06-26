#!/usr/bin/env node
/**
 * Decision Journal CLI
 * 
 * Command-line interface for managing decisions
 */

const { Decision } = require('../src/models');
const { Storage } = require('../src/storage');

// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

function colorize(text, color) {
  return `${colors[color]}${text}${colors.reset}`;
}

/**
 * Print usage information
 */
function printUsage() {
  console.log(`
${colorize('Decision Journal CLI', 'bright')}

Usage: decision <command> [options]

Commands:
  ${colorize('add', 'green')} <title>           Add a new decision
    --situation <text>    Context/situation
    --options <list>      Options considered (comma-separated)
    --decision <text>     The decision made
    --reasoning <text>    Reasoning behind decision
    --expected <text>     Expected outcomes
    --tag <tag>          Category tag
    --importance <1-5>   Importance level (default: 3)
    --reversible <yes/no> Whether reversible (default: yes)
    --review <date>      Review date (YYYY-MM-DD)

  ${colorize('list', 'green')}                  List decisions
    --last <n>           Show last N decisions
    --tag <tag>          Filter by tag
    --status <status>    Filter by status (pending/reviewed/completed)
    --since <date>       From date onward

  ${colorize('show', 'green')} <id>            Show a specific decision

  ${colorize('review', 'green')} <id>          Review a decision
    --outcome <text>     Actual outcome
    --lessons <text>     Lessons learned
    --satisfaction <1-5> Satisfaction level

  ${colorize('due', 'green')}                  Show decisions due for review

  ${colorize('analyze', 'green')}              Analyze decision patterns
    --timeframe <period> Analysis period (30d, 90d, 1y, all)
    --tag <tag>          Analyze specific category

  ${colorize('export', 'green')}               Export decisions
    --format <format>    Export format (json, markdown, csv)
    --output <file>      Output file (default: stdout)

  ${colorize('remind', 'green')}               Show pending review reminders

  ${colorize('stats', 'green')}                Show statistics

  ${colorize('help', 'green')}                 Show this help message
`);
}

/**
 * Parse command line arguments
 * @param {string[]} args - Process arguments
 * @returns {Object} Parsed arguments
 */
function parseArgs(args) {
  const result = { command: null, positional: [], options: {} };
  
  if (args.length < 3) {
    return result;
  }
  
  result.command = args[2];
  
  // Handle --help and -h flags
  if (result.command === '--help' || result.command === '-h') {
    result.command = 'help';
    return result;
  }
  
  for (let i = 3; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--help' || arg === '-h') {
      result.options.help = true;
    } else if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
      result.options[key] = value;
    } else {
      result.positional.push(arg);
    }
  }
  
  return result;
}

/**
 * Handle 'add' command
 * @param {Object} args - Parsed arguments
 * @param {Storage} storage - Storage instance
 */
function cmdAdd(args, storage) {
  const title = args.positional[0];
  
  if (!title) {
    console.error(colorize('Error: Title is required', 'red'));
    process.exit(1);
  }
  
  const options = args.options.options 
    ? args.options.options.split(',').map(o => o.trim()) 
    : [];
  
  const decision = new Decision({
    title,
    situation: args.options.situation || '',
    options,
    decision: args.options.decision || '',
    reasoning: args.options.reasoning || '',
    expected: args.options.expected || '',
    tag: args.options.tag || 'uncategorized',
    importance: parseInt(args.options.importance) || 3,
    reversible: args.options.reversible !== 'no',
    reviewDate: args.options.review || null
  });
  
  storage.saveDecision(decision);
  
  console.log(colorize('✅ Decision recorded', 'green'));
  console.log(`   ID: ${decision.id}`);
  console.log(`   Title: ${decision.title}`);
  
  if (decision.reviewDate) {
    console.log(`   Review: ${decision.reviewDate}`);
  }
}

/**
 * Handle 'list' command
 * @param {Object} args - Parsed arguments
 * @param {Storage} storage - Storage instance
 */
function cmdList(args, storage) {
  const filters = {};
  
  if (args.options.tag) filters.tag = args.options.tag;
  if (args.options.status) filters.status = args.options.status;
  if (args.options.since) filters.since = args.options.since;
  if (args.options.last) filters.limit = parseInt(args.options.last);
  
  const decisions = storage.loadDecisionsFiltered(filters);
  
  if (decisions.length === 0) {
    console.log(colorize('No decisions found.', 'dim'));
    return;
  }
  
  console.log(`\n${colorize(`📊 ${decisions.length} decision(s):`, 'bright')}\n`);
  
  decisions.forEach((d, i) => {
    console.log(`${i + 1}. ${d.getSummary()}`);
    console.log();
  });
}

/**
 * Handle 'show' command
 * @param {Object} args - Parsed arguments
 * @param {Storage} storage - Storage instance
 */
function cmdShow(args, storage) {
  const id = args.positional[0];
  
  if (!id) {
    console.error(colorize('Error: Decision ID is required', 'red'));
    process.exit(1);
  }
  
  const decision = storage.getDecision(id);
  
  if (!decision) {
    console.error(colorize(`Error: Decision not found: ${id}`, 'red'));
    process.exit(1);
  }
  
  console.log('\n' + decision.format());
}

/**
 * Handle 'review' command
 * @param {Object} args - Parsed arguments
 * @param {Storage} storage - Storage instance
 */
function cmdReview(args, storage) {
  const id = args.positional[0];
  
  if (!id) {
    console.error(colorize('Error: Decision ID is required', 'red'));
    process.exit(1);
  }
  
  const decision = storage.getDecision(id);
  
  if (!decision) {
    console.error(colorize(`Error: Decision not found: ${id}`, 'red'));
    process.exit(1);
  }
  
  if (args.options.outcome) {
    decision.addReview({
      outcome: args.options.outcome,
      lessons: args.options.lessons || '',
      satisfaction: parseInt(args.options.satisfaction) || null
    });
    
    storage.updateDecision(decision);
    
    // Also save as a separate review record
    const { Review } = require('../src/models');
    const review = new Review({
      decisionId: decision.id,
      outcome: args.options.outcome,
      lessons: args.options.lessons || '',
      satisfaction: parseInt(args.options.satisfaction) || null
    });
    storage.saveReview(review);
    
    console.log(colorize(`✅ Decision ${decision.id} updated with review`, 'green'));
  } else {
    console.log('\n' + decision.format());
    console.log(colorize('\n💡 Use --outcome to record results', 'yellow'));
  }
}

/**
 * Handle 'due' command
 * @param {Object} args - Parsed arguments
 * @param {Storage} storage - Storage instance
 */
function cmdDue(args, storage) {
  const dueDecisions = storage.getDueReviews();
  
  if (dueDecisions.length === 0) {
    console.log(colorize('✅ No decisions are due for review.', 'green'));
    return;
  }
  
  console.log(`\n${colorize(`⏰ ${dueDecisions.length} decision(s) due for review:`, 'bright')}\n`);
  
  dueDecisions.forEach((d, i) => {
    console.log(`${i + 1}. ${d.getSummary()}`);
    console.log(`   Review Date: ${d.reviewDate}`);
    console.log();
  });
}

/**
 * Handle 'analyze' command
 * @param {Object} args - Parsed arguments
 * @param {Storage} storage - Storage instance
 */
function cmdAnalyze(args, storage) {
  const decisions = storage.loadDecisions();
  
  if (decisions.length === 0) {
    console.log(colorize('No decisions to analyze.', 'dim'));
    return;
  }
  
  // Filter by timeframe if specified
  let filteredDecisions = decisions;
  if (args.options.timeframe) {
    const now = new Date();
    let cutoff;
    
    switch (args.options.timeframe) {
      case '30d':
        cutoff = new Date(now - 30 * 24 * 60 * 60 * 1000);
        break;
      case '90d':
        cutoff = new Date(now - 90 * 24 * 60 * 60 * 1000);
        break;
      case '1y':
        cutoff = new Date(now - 365 * 24 * 60 * 60 * 1000);
        break;
      default:
        cutoff = null;
    }
    
    if (cutoff) {
      filteredDecisions = decisions.filter(d => new Date(d.createdAt) >= cutoff);
    }
  }
  
  // Filter by tag if specified
  if (args.options.tag) {
    filteredDecisions = filteredDecisions.filter(d => d.tag === args.options.tag);
  }
  
  // Calculate statistics
  const total = filteredDecisions.length;
  const byTag = {};
  const byStatus = {};
  let totalImportance = 0;
  let reviewedCount = 0;
  let totalSatisfaction = 0;
  
  filteredDecisions.forEach(d => {
    byTag[d.tag] = (byTag[d.tag] || 0) + 1;
    byStatus[d.status] = (byStatus[d.status] || 0) + 1;
    totalImportance += d.importance || 0;
    
    if (d.status === 'reviewed') {
      reviewedCount++;
      if (d.satisfaction) {
        totalSatisfaction += d.satisfaction;
      }
    }
  });
  
  console.log(`\n${colorize('📈 Decision Analysis', 'bright')}\n`);
  console.log(`Total decisions: ${total}`);
  
  if (args.options.timeframe) {
    console.log(`Timeframe: ${args.options.timeframe}`);
  }
  
  console.log(`\n${colorize('By category:', 'cyan')}`);
  Object.entries(byTag)
    .sort((a, b) => b[1] - a[1])
    .forEach(([tag, count]) => {
      console.log(`  • ${tag}: ${count}`);
    });
  
  console.log(`\n${colorize('By status:', 'cyan')}`);
  Object.entries(byStatus).forEach(([status, count]) => {
    const emoji = { pending: '⏳', reviewed: '✅', completed: '✅' }[status] || '○';
    console.log(`  ${emoji} ${status}: ${count}`);
  });
  
  if (total > 0) {
    console.log(`\n${colorize('Quality metrics:', 'cyan')}`);
    console.log(`  Average importance: ${(totalImportance / total).toFixed(1)}/5`);
    
    if (reviewedCount > 0) {
      console.log(`  Reviewed: ${reviewedCount}/${total} (${Math.round(reviewedCount/total*100)}%)`);
      console.log(`  Average satisfaction: ${(totalSatisfaction / reviewedCount).toFixed(1)}/5`);
    }
  }
  
  // Recent trend
  if (filteredDecisions.length >= 5) {
    const recent = filteredDecisions.slice(0, 5);
    const avgImportance = recent.reduce((sum, d) => sum + (d.importance || 0), 0) / recent.length;
    console.log(`\n${colorize('Recent trend (last 5):', 'cyan')}`);
    console.log(`  Average importance: ${avgImportance.toFixed(1)}/5`);
  }
}

/**
 * Handle 'export' command
 * @param {Object} args - Parsed arguments
 * @param {Storage} storage - Storage instance
 */
function cmdExport(args, storage) {
  const format = args.options.format || 'markdown';
  
  try {
    const output = storage.exportData(format);
    
    if (args.options.output) {
      const fs = require('fs');
      fs.writeFileSync(args.options.output, output);
      console.log(colorize(`✅ Exported to ${args.options.output}`, 'green'));
    } else {
      console.log(output);
    }
  } catch (e) {
    console.error(colorize(`Error: ${e.message}`, 'red'));
    process.exit(1);
  }
}

/**
 * Handle 'remind' command
 * @param {Object} args - Parsed arguments
 * @param {Storage} storage - Storage instance
 */
function cmdRemind(args, storage) {
  const dueDecisions = storage.getDueReviews();
  
  if (dueDecisions.length === 0) {
    console.log(colorize('✅ No pending review reminders.', 'green'));
    return;
  }
  
  console.log(`\n${colorize(`🔔 ${dueDecisions.length} review reminder(s):`, 'bright')}\n`);
  
  dueDecisions.forEach((d, i) => {
    const daysOverdue = Math.floor(
      (new Date() - new Date(d.reviewDate)) / (1000 * 60 * 60 * 24)
    );
    const overdueText = daysOverdue > 0 
      ? colorize(`(${daysOverdue} days overdue)`, 'red') 
      : colorize('(due today)', 'yellow');
    
    console.log(`${i + 1}. ${d.title} ${overdueText}`);
    console.log(`   ID: ${d.id} | Review: ${d.reviewDate}`);
    console.log(`   Command: decision review ${d.id} --outcome "..."`);
    console.log();
  });
}

/**
 * Handle 'stats' command
 * @param {Object} args - Parsed arguments
 * @param {Storage} storage - Storage instance
 */
function cmdStats(args, storage) {
  const stats = storage.getStats();
  
  console.log(`\n${colorize('📊 Decision Statistics', 'bright')}\n`);
  console.log(`Total decisions: ${stats.totalDecisions}`);
  console.log(`Total reviews: ${stats.totalReviews}`);
  console.log(`Reviewed decisions: ${stats.reviewedDecisions}`);
  console.log(`Pending reviews: ${stats.pendingReviews}`);
  console.log(`Average importance: ${stats.averageImportance.toFixed(1)}/5`);
  
  if (stats.averageSatisfaction > 0) {
    console.log(`Average satisfaction: ${stats.averageSatisfaction.toFixed(1)}/5`);
  }
  
  if (Object.keys(stats.byTag).length > 0) {
    console.log(`\n${colorize('By tag:', 'cyan')}`);
    Object.entries(stats.byTag)
      .sort((a, b) => b[1] - a[1])
      .forEach(([tag, count]) => {
        console.log(`  • ${tag}: ${count}`);
      });
  }
  
  if (Object.keys(stats.byStatus).length > 0) {
    console.log(`\n${colorize('By status:', 'cyan')}`);
    Object.entries(stats.byStatus).forEach(([status, count]) => {
      console.log(`  • ${status}: ${count}`);
    });
  }
}

/**
 * Main entry point
 */
function main() {
  const args = parseArgs(process.argv);
  
  if (!args.command || args.command === 'help') {
    printUsage();
    process.exit(0);
  }
  
  const storage = new Storage();
  
  switch (args.command) {
    case 'add':
      cmdAdd(args, storage);
      break;
    case 'list':
      cmdList(args, storage);
      break;
    case 'show':
      cmdShow(args, storage);
      break;
    case 'review':
      cmdReview(args, storage);
      break;
    case 'due':
      cmdDue(args, storage);
      break;
    case 'analyze':
      cmdAnalyze(args, storage);
      break;
    case 'export':
      cmdExport(args, storage);
      break;
    case 'remind':
      cmdRemind(args, storage);
      break;
    case 'stats':
      cmdStats(args, storage);
      break;
    default:
      console.error(colorize(`Error: Unknown command: ${args.command}`, 'red'));
      printUsage();
      process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { parseArgs, main };
