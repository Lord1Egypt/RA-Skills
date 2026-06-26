#!/usr/bin/env node

/**
 * Feedback Loop CLI
 * 
 * Commands:
 *   provide  - Submit feedback (explicit or implicit)
 *   analyze  - Analyze feedback data
 *   suggest  - Generate improvement suggestions
 *   track    - Track implementation progress
 *   stats    - Show statistics
 *   list     - List feedback, suggestions, or tracking entries
 *   report   - Generate comprehensive report
 *   help     - Show help information
 */

const path = require('path');
const fs = require('fs');

// Import modules
const FeedbackLoop = require('../src/index');

function printHelp() {
  console.log(`
📊 Feedback Loop CLI - Feedback Collection & Analysis Tool

Usage: feedback-loop <command> [options]

Commands:
  provide    Submit feedback (explicit or implicit)
  analyze    Analyze feedback data and generate insights
  suggest    Generate improvement suggestions based on analysis
  track      Track implementation progress of suggestions
  stats      Show feedback statistics
  list       List feedback, suggestions, or tracking entries
  report     Generate comprehensive tracking report
  export     Export data to JSON or CSV
  help       Show this help message

Examples:
  feedback-loop provide --type explicit --rating 5 --comment "Great response!"
  feedback-loop provide --type implicit --signal completion --sessionId abc123
  feedback-loop analyze --range week
  feedback-loop suggest --max 5
  feedback-loop track <suggestion-id> --phase implementation --status in_progress
  feedback-loop stats
  feedback-loop list feedback --limit 10
  feedback-loop list suggestions --status pending
  feedback-loop report
  feedback-loop export --format json

For detailed help on a command:
  feedback-loop help <command>
`);
}

function printCommandHelp(command) {
  const help = {
    provide: `
Provide Feedback
----------------
Submit explicit or implicit feedback.

Options:
  --type <type>        Feedback type: explicit or implicit (required)
  --rating <rating>    Rating for explicit feedback (1-5, thumbs_up, thumbs_down)
  --comment <text>     Optional comment
  --category <cat>     Feedback category (accuracy, speed, helpfulness, etc.)
  --signal <signal>    Signal type for implicit feedback (completion, retry, abandon, etc.)
  --sessionId <id>     Session identifier
  --metrics <json>     JSON metrics for implicit feedback
  --context <json>     JSON context information

Examples:
  feedback-loop provide --type explicit --rating 5 --comment "Excellent!" --category accuracy
  feedback-loop provide --type implicit --signal completion --sessionId sess123
  feedback-loop provide --type implicit --signal retry --metrics '{"retryCount": 3}'
`,

    analyze: `
Analyze Feedback
----------------
Analyze collected feedback and generate insights.

Options:
  --range <range>      Time range: day, week, month, all (default: week)
  --explicit-only      Only analyze explicit feedback
  --output <format>    Output format: json, pretty (default: pretty)

Examples:
  feedback-loop analyze --range month
  feedback-loop analyze --explicit-only --output json
`,

    suggest: `
Generate Suggestions
--------------------
Generate improvement suggestions based on feedback analysis.

Options:
  --max <number>       Maximum suggestions to generate (default: 5)
  --focus <category>   Focus on specific category
  --output <format>    Output format: json, pretty (default: pretty)

Examples:
  feedback-loop suggest --max 10
  feedback-loop suggest --focus quality
`,

    track: `
Track Progress
--------------
Track implementation progress of a suggestion.

Options:
  --phase <phase>      Implementation phase (planning, implementation, testing, deployed)
  --status <status>    Status (in_progress, completed, blocked)
  --notes <text>       Additional notes
  --metrics <json>     Progress metrics

Examples:
  feedback-loop track fb_123 --phase implementation --status in_progress
  feedback-loop track fb_123 --phase deployed --status completed --notes "Successfully implemented"
`,

    stats: `
Show Statistics
---------------
Display feedback statistics summary.

Options:
  --output <format>    Output format: json, pretty (default: pretty)

Examples:
  feedback-loop stats
  feedback-loop stats --output json
`,

    list: `
List Entries
------------
List feedback, suggestions, or tracking entries.

Usage: feedback-loop list <type> [options]

Types:
  feedback    List feedback entries
  suggestions List improvement suggestions
  tracking    List tracking entries

Options:
  --type <type>        Filter by type (for feedback)
  --status <status>    Filter by status (for suggestions/tracking)
  --category <cat>     Filter by category
  --limit <number>     Maximum entries to show (default: 20)
  --output <format>    Output format: json, pretty (default: pretty)

Examples:
  feedback-loop list feedback --limit 10
  feedback-loop list suggestions --status pending
  feedback-loop list tracking --phase implementation
`,

    report: `
Generate Report
---------------
Generate comprehensive tracking report.

Options:
  --output <format>    Output format: json, pretty (default: pretty)

Examples:
  feedback-loop report
  feedback-loop report --output json
`,

    export: `
Export Data
-----------
Export feedback and tracking data.

Options:
  --format <format>    Export format: json, csv (default: json)
  --output <file>      Output file path (default: stdout)

Examples:
  feedback-loop export --format json --output data.json
  feedback-loop export --format csv --output data.csv
`
  };

  console.log(help[command] || 'Command not found. Use "feedback-loop help" for available commands.');
}

function parseArgs(args) {
  const parsed = { command: null, options: { _: [] } };
  const flags = [];
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1];
      if (value && !value.startsWith('--')) {
        parsed.options[key] = value;
        i++;
      } else {
        flags.push(key);
      }
    } else if (!parsed.command) {
      parsed.command = arg;
    } else {
      // Capture additional non-flag arguments
      parsed.options._.push(arg);
    }
  }
  
  flags.forEach(flag => {
    parsed.options[flag] = true;
  });
  
  return parsed;
}

function parseJSON(value) {
  try {
    return JSON.parse(value);
  } catch (e) {
    console.error(`Invalid JSON: ${value}`);
    process.exit(1);
  }
}

function output(data, format) {
  if (format === 'json') {
    console.log(JSON.stringify(data, null, 2));
  } else {
    // Pretty format
    if (typeof data === 'object') {
      console.log(JSON.stringify(data, null, 2));
    } else {
      console.log(data);
    }
  }
}

function run(args) {
  const parsed = parseArgs(args.slice(2));
  const { command, options } = parsed;
  const feedbackLoop = new FeedbackLoop();

  if (!command || command === 'help') {
    if (options._ && options._[0]) {
      printCommandHelp(options._[0]);
    } else {
      printHelp();
    }
    return;
  }

  switch (command) {
    case 'provide':
      handleProvide(feedbackLoop, options);
      break;
    
    case 'analyze':
      handleAnalyze(feedbackLoop, options);
      break;
    
    case 'suggest':
      handleSuggest(feedbackLoop, options);
      break;
    
    case 'track':
      handleTrack(feedbackLoop, options, args);
      break;
    
    case 'stats':
      handleStats(feedbackLoop, options);
      break;
    
    case 'list':
      handleList(feedbackLoop, options);
      break;
    
    case 'report':
      handleReport(feedbackLoop, options);
      break;
    
    case 'export':
      handleExport(feedbackLoop, options);
      break;
    
    default:
      console.error(`Unknown command: ${command}`);
      console.log('Use "feedback-loop help" for available commands.');
      process.exit(1);
  }
}

function handleProvide(fl, options) {
  if (!options.type) {
    console.error('Error: --type is required (explicit or implicit)');
    process.exit(1);
  }

  let result;
  if (options.type === 'explicit') {
    if (!options.rating) {
      console.error('Error: --rating is required for explicit feedback');
      process.exit(1);
    }
    result = fl.provide({
      type: 'explicit',
      rating: options.rating,
      comment: options.comment,
      category: options.category,
      sessionId: options.sessionId,
      source: 'cli'
    });
  } else if (options.type === 'implicit') {
    if (!options.signal) {
      console.error('Error: --signal is required for implicit feedback');
      process.exit(1);
    }
    result = fl.provide({
      type: 'implicit',
      signal: options.signal,
      sessionId: options.sessionId,
      metrics: options.metrics ? parseJSON(options.metrics) : {},
      context: options.context ? parseJSON(options.context) : {}
    });
  } else {
    console.error('Error: --type must be "explicit" or "implicit"');
    process.exit(1);
  }

  output(result, options.output || 'pretty');
}

function handleAnalyze(fl, options) {
  const result = fl.analyze({
    timeRange: options.range || 'week',
    includeImplicit: !options['explicit-only']
  });
  output(result, options.output || 'pretty');
}

function handleSuggest(fl, options) {
  const result = fl.suggest({
    maxSuggestions: parseInt(options.max) || 5,
    focusArea: options.focus
  });
  output(result, options.output || 'pretty');
}

function handleTrack(fl, options, args) {
  const suggestionId = args.find((arg, i) => i > 2 && !arg.startsWith('--'));
  
  if (!suggestionId) {
    console.error('Error: suggestion ID is required');
    console.log('Usage: feedback-loop track <suggestion-id> [options]');
    process.exit(1);
  }

  const result = fl.track(suggestionId, {
    phase: options.phase,
    status: options.status,
    notes: options.notes,
    metrics: options.metrics ? parseJSON(options.metrics) : {}
  });
  output(result, options.output || 'pretty');
}

function handleStats(fl, options) {
  const result = fl.getStats();
  output(result, options.output || 'pretty');
}

function handleList(fl, options) {
  const listType = options._ ? options._[0] : null;
  
  if (!listType) {
    console.error('Error: list type is required (feedback, suggestions, tracking)');
    console.log('Usage: feedback-loop list <type> [options]');
    process.exit(1);
  }

  let result;
  const filters = {
    limit: parseInt(options.limit) || 20
  };

  switch (listType) {
    case 'feedback':
      if (options.type) filters.type = options.type;
      if (options.category) filters.category = options.category;
      result = fl.getFeedback(filters);
      break;
    
    case 'suggestions':
      if (options.status) filters.status = options.status;
      if (options.category) filters.category = options.category;
      if (options.priority) filters.priority = options.priority;
      result = fl.getSuggestions(filters);
      break;
    
    case 'tracking':
      if (options.suggestionId) filters.suggestionId = options.suggestionId;
      if (options.phase) filters.phase = options.phase;
      if (options.category) filters.category = options.category;
      result = fl.tracker.getAllTracking(filters);
      break;
    
    default:
      console.error(`Unknown list type: ${listType}`);
      process.exit(1);
  }

  output(result, options.output || 'pretty');
}

function handleReport(fl, options) {
  const result = fl.getReport();
  output(result, options.output || 'pretty');
}

function handleExport(fl, options) {
  const format = options.format || 'json';
  const data = fl.exportData(format);
  
  if (options.output) {
    fs.writeFileSync(options.output, data);
    console.log(`Data exported to ${options.output}`);
  } else {
    console.log(data);
  }
}

module.exports = { run, parseArgs };

// Run if called directly
if (require.main === module) {
  run(process.argv);
}
