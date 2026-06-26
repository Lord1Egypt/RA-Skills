#!/usr/bin/env node

/**
 * Decision Expert CLI
 * 
 * A command-line tool for decision analysis and support
 */

const { Command } = require('commander');
const chalk = require('chalk');
const packageJson = require('./package.json');

// Create CLI program
const program = new Command();

program
  .name('decision')
  .description(packageJson.description)
  .version(packageJson.version)
  .configureHelp({
    sortSubcommands: true,
    subcommandTerm: (cmd) => cmd.name()
  });

// Helper function to display framework info
function displayFrameworks() {
  console.log(chalk.bold('\nAvailable Decision Frameworks:\n'));
  
  const frameworks = [
    { name: 'Pros & Cons', cmd: 'pros-cons', desc: 'Simple advantages/disadvantages listing' },
    { name: 'SWOT Analysis', cmd: 'swot', desc: 'Strengths, Weaknesses, Opportunities, Threats' },
    { name: 'Decision Matrix', cmd: 'matrix', desc: 'Weighted criteria scoring system' },
    { name: 'Cost-Benefit Analysis', cmd: 'cost-benefit', desc: 'Quantitative financial evaluation' },
    { name: 'Decision Tree', cmd: 'tree', desc: 'Scenario branching with probabilities' },
    { name: 'Eisenhower Matrix', cmd: 'eisenhower', desc: 'Urgent vs. important prioritization' },
    { name: 'Weighted Scoring', cmd: 'weighted', desc: 'Custom criteria with importance weights' },
    { name: 'Six Thinking Hats', cmd: 'hats', desc: 'Multiple perspective consideration' }
  ];
  
  frameworks.forEach(fw => {
    console.log(`  ${chalk.cyan(fw.cmd.padEnd(15))} ${fw.name}`);
    console.log(`    ${chalk.gray(fw.desc)}\n`);
  });
}

// Main analyze command
program
  .command('analyze')
  .description('Analyze a decision with automatic framework selection')
  .argument('<description>', 'Description of the decision to analyze')
  .option('-o, --options <items>', 'Comma-separated list of options', '')
  .option('-c, --criteria <items>', 'Comma-separated list of criteria', '')
  .option('-w, --weights <items>', 'Comma-separated weights for criteria', '')
  .option('-f, --format <format>', 'Output format (text, json, markdown, table)', 'text')
  .option('-o, --output <file>', 'Output file path')
  .action((description, options) => {
    console.log(chalk.bold(`\nAnalyzing: ${chalk.cyan(description)}\n`));
    
    if (options.options) {
      const optionList = options.options.split(',').map(o => o.trim());
      console.log(chalk.bold('Options:'));
      optionList.forEach((opt, i) => {
        console.log(`  ${i + 1}. ${opt}`);
      });
      console.log();
    }
    
    if (options.criteria) {
      const criteriaList = options.criteria.split(',').map(c => c.trim());
      console.log(chalk.bold('Criteria:'));
      criteriaList.forEach((criterion, i) => {
        console.log(`  ${i + 1}. ${criterion}`);
      });
      console.log();
    }
    
    console.log(chalk.yellow('Analysis would be performed here...'));
    console.log(chalk.gray('(In a full implementation, this would run actual decision analysis)'));
    
    // Suggest appropriate framework
    const optCount = options.options ? options.options.split(',').length : 0;
    const critCount = options.criteria ? options.criteria.split(',').length : 0;
    
    console.log(chalk.bold('\nRecommended Framework:'));
    if (optCount === 2 && critCount === 0) {
      console.log('  Pros & Cons analysis (binary decision)');
    } else if (optCount > 2 && critCount > 0) {
      console.log('  Decision Matrix (multiple options with criteria)');
    } else if (optCount > 0 && options.criteria === '') {
      console.log('  Comparative analysis');
    } else {
      console.log('  General decision analysis');
    }
  });

// Pros & Cons command
program
  .command('pros-cons')
  .description('Create a pros and cons list for a decision')
  .argument('<description>', 'Description of the decision')
  .option('-p, --pros <items>', 'Comma-separated list of pros', '')
  .option('-c, --cons <items>', 'Comma-separated list of cons', '')
  .option('-w, --weighted', 'Use weighted scoring for pros/cons')
  .action((description, options) => {
    console.log(chalk.bold(`\nPros & Cons Analysis: ${chalk.cyan(description)}\n`));
    
    const pros = options.pros ? options.pros.split(',').map(p => p.trim()) : [];
    const cons = options.cons ? options.cons.split(',').map(c => c.trim()) : [];
    
    console.log(chalk.green.bold('Pros (Advantages):'));
    if (pros.length > 0) {
      pros.forEach((pro, i) => {
        console.log(`  ✓ ${pro}`);
      });
    } else {
      console.log(chalk.gray('  (No pros specified - use --pros to add)'));
    }
    
    console.log(chalk.red.bold('\nCons (Disadvantages):'));
    if (cons.length > 0) {
      cons.forEach((con, i) => {
        console.log(`  ✗ ${con}`);
      });
    } else {
      console.log(chalk.gray('  (No cons specified - use --cons to add)'));
    }
    
    console.log(chalk.bold('\nSummary:'));
    if (pros.length > cons.length) {
      console.log(chalk.green(`  Pros outweigh cons (${pros.length} vs ${cons.length})`));
    } else if (cons.length > pros.length) {
      console.log(chalk.red(`  Cons outweigh pros (${cons.length} vs ${pros.length})`));
    } else {
      console.log(chalk.yellow(`  Balanced (${pros.length} pros vs ${cons.length} cons)`));
    }
  });

// SWOT Analysis command
program
  .command('swot')
  .description('Perform a SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)')
  .argument('<description>', 'Description of the situation to analyze')
  .option('-s, --strengths <items>', 'Comma-separated list of strengths', '')
  .option('-w, --weaknesses <items>', 'Comma-separated list of weaknesses', '')
  .option('-o, --opportunities <items>', 'Comma-separated list of opportunities', '')
  .option('-t, --threats <items>', 'Comma-separated list of threats', '')
  .action((description, options) => {
    console.log(chalk.bold(`\nSWOT Analysis: ${chalk.cyan(description)}\n`));
    
    const quadrants = [
      { title: 'Strengths', color: chalk.green, items: options.strengths },
      { title: 'Weaknesses', color: chalk.red, items: options.weaknesses },
      { title: 'Opportunities', color: chalk.blue, items: options.opportunities },
      { title: 'Threats', color: chalk.magenta, items: options.threats }
    ];
    
    quadrants.forEach(quadrant => {
      console.log(quadrant.color.bold(`${quadrant.title}:`));
      const items = quadrant.items ? quadrant.items.split(',').map(i => i.trim()) : [];
      if (items.length > 0) {
        items.forEach(item => {
          console.log(`  • ${item}`);
        });
      } else {
        console.log(chalk.gray(`  (No ${quadrant.title.toLowerCase()} specified)`));
      }
      console.log();
    });
    
    console.log(chalk.bold('SWOT Matrix:'));
    console.log(chalk.gray('  Internal Factors: Strengths & Weaknesses'));
    console.log(chalk.gray('  External Factors: Opportunities & Threats'));
  });

// Decision Matrix command
program
  .command('matrix')
  .description('Create a decision matrix with weighted criteria')
  .argument('<description>', 'Description of the decision')
  .option('-c, --criteria <items>', 'Comma-separated list of criteria (required)', '')
  .option('-o, --options <items>', 'Comma-separated list of options (required)', '')
  .option('-w, --weights <items>', 'Comma-separated weights for criteria (sum to 100)', '')
  .option('-s, --scores <items>', 'Comma-separated scores matrix (option1_crit1,option1_crit2,...)', '')
  .action((description, options) => {
    console.log(chalk.bold(`\nDecision Matrix: ${chalk.cyan(description)}\n`));
    
    if (!options.criteria || !options.options) {
      console.log(chalk.red('Error: Both --criteria and --options are required for decision matrix'));
      console.log(chalk.gray('Example: decision matrix "买车" --criteria "价格,油耗,安全性" --options "SUV,轿车"'));
      return;
    }
    
    const criteria = options.criteria.split(',').map(c => c.trim());
    const optionsList = options.options.split(',').map(o => o.trim());
    
    // Parse weights or use equal weights
    let weights = [];
    if (options.weights) {
      weights = options.weights.split(',').map(w => parseFloat(w.trim()));
    } else {
      const equalWeight = (100 / criteria.length).toFixed(1);
      weights = criteria.map(() => equalWeight);
    }
    
    console.log(chalk.bold('Criteria & Weights:'));
    criteria.forEach((criterion, i) => {
      console.log(`  ${i + 1}. ${criterion}: ${weights[i]}%`);
    });
    
    console.log(chalk.bold('\nOptions:'));
    optionsList.forEach((option, i) => {
      console.log(`  ${String.fromCharCode(65 + i)}. ${option}`);
    });
    
    console.log(chalk.yellow('\nDecision matrix calculation would be performed here...'));
    console.log(chalk.gray('(In full implementation, this would calculate weighted scores and rank options)'));
    
    // Show sample calculation
    if (criteria.length > 0 && optionsList.length > 0) {
      console.log(chalk.bold('\nSample Calculation:'));
      console.log(chalk.gray('  Option scores = Σ(Criterion Score × Criterion Weight)'));
      console.log(chalk.gray(`  ${optionsList[0]} score = (score1 × ${weights[0]}%) + (score2 × ${weights[1]}%) + ...`));
    }
  });

// Compare command
program
  .command('compare')
  .description('Compare multiple options across factors')
  .argument('<description>', 'Description of what to compare')
  .option('-o, --options <items>', 'Comma-separated list of options to compare', '')
  .option('-f, --factors <items>', 'Comma-separated list of comparison factors', '')
  .option('-t, --timeframe <time>', 'Timeframe for decision (e.g., "1 year", "5 years")')
  .action((description, options) => {
    console.log(chalk.bold(`\nComparison: ${chalk.cyan(description)}\n`));
    
    const optionsList = options.options ? options.options.split(',').map(o => o.trim()) : ['Option A', 'Option B'];
    const factors = options.factors ? options.factors.split(',').map(f => f.trim()) : ['Cost', 'Quality', 'Convenience'];
    
    console.log(chalk.bold('Options to Compare:'));
    optionsList.forEach((option, i) => {
      console.log(`  ${i + 1}. ${option}`);
    });
    
    console.log(chalk.bold('\nComparison Factors:'));
    factors.forEach((factor, i) => {
      console.log(`  ${i + 1}. ${factor}`);
    });
    
    if (options.timeframe) {
      console.log(chalk.bold('\nTimeframe:'), options.timeframe);
    }
    
    console.log(chalk.yellow('\nComparative analysis would be performed here...'));
  });

// Interactive command
program
  .command('interactive')
  .description('Start interactive decision-making session')
  .action(() => {
    console.log(chalk.bold('\nInteractive Decision Expert\n'));
    console.log(chalk.gray('This would start an interactive session with:'));
    console.log(chalk.gray('  1. Decision type selection'));
    console.log(chalk.gray('  2. Option input'));
    console.log(chalk.gray('  3. Criteria definition'));
    console.log(chalk.gray('  4. Framework selection'));
    console.log(chalk.gray('  5. Analysis and recommendation'));
    console.log(chalk.gray('  6. Export options'));
    console.log(chalk.gray('\nInteractive mode requires the "inquirer" package.'));
  });

// Help command with framework info
program
  .command('help')
  .description('Show help information and available frameworks')
  .action(() => {
    console.log(chalk.bold(`\nDecision Expert v${packageJson.version}\n`));
    console.log(packageJson.description + '\n');
    console.log(chalk.bold('Usage:'));
    console.log('  decision <command> [options]\n');
    console.log(chalk.bold('Commands:'));
    
    // Show available commands
    const commands = [
      { name: 'analyze', desc: 'Analyze a decision with automatic framework selection' },
      { name: 'pros-cons', desc: 'Create a pros and cons list' },
      { name: 'swot', desc: 'Perform a SWOT analysis' },
      { name: 'matrix', desc: 'Create a decision matrix with weighted criteria' },
      { name: 'compare', desc: 'Compare multiple options across factors' },
      { name: 'interactive', desc: 'Start interactive decision-making session' },
      { name: 'help', desc: 'Show this help information' }
    ];
    
    commands.forEach(cmd => {
      console.log(`  ${cmd.name.padEnd(15)} ${cmd.desc}`);
    });
    
    displayFrameworks();
    
    console.log(chalk.bold('\nExamples:'));
    console.log(chalk.gray('  decision analyze "买什么手机" --options "iPhone, Samsung, Google"'));
    console.log(chalk.gray('  decision pros-cons "换工作" --pros "高薪,发展" --cons "压力,通勤"'));
    console.log(chalk.gray('  decision matrix "买车" --criteria "价格,油耗,安全" --options "SUV,轿车" --weights "40,30,30"'));
    console.log(chalk.gray('  decision swot "创业" --strengths "技术,团队" --weaknesses "资金" --opportunities "市场" --threats "竞争"'));
  });

// Handle unknown commands
program.on('command:*', (operands) => {
  console.log(chalk.red(`Error: Unknown command '${operands[0]}'`));
  console.log(chalk.gray('Run "decision help" to see available commands.'));
  process.exit(1);
});

// Parse command line arguments
if (process.argv.length <= 2) {
  program.help();
} else {
  program.parse(process.argv);
}