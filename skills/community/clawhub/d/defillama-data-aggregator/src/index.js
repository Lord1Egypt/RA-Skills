#!/usr/bin/env node

/**
 * DefiLlama Data Aggregator CLI
 * Main entry point for the DefiLlama data aggregator
 */

const { Command } = require('commander');
const chalk = require('chalk');
const path = require('path');

// Load configuration
let config;
try {
  config = require(path.join(__dirname, '../config/keys.js'));
} catch (error) {
  console.error(chalk.yellow('Warning: config/keys.js not found. Using example config.'));
  try {
    config = require(path.join(__dirname, '../config/keys.example.js'));
  } catch (fallbackError) {
    console.error(chalk.red('Error: No configuration files found!'));
    console.error(chalk.red('Please ensure either config/keys.js or config/keys.example.js exists.'));
    process.exit(1);
  }
}

// Import platform clients
const DefiLlamaClient = require('./platforms/defillama');

// Import utilities (only what's actually used)
const DataFormatter = require('./utils/formatter');

// Initialize clients
const defillama = new DefiLlamaClient(config);

// Create CLI program
const program = new Command();

program
  .name('defillama-data')
  .description('Professional DefiLlama data aggregator with security validation')
  .version('1.0.3');

// ============================================================================
// Security & Validation Functions
// ============================================================================

/**
 * Sanitize user input to prevent injection attacks
 */
function sanitizeInput(input, type = 'string') {
  if (!input) return null;

  switch (type) {
    case 'string':
      // Remove potentially dangerous characters
      return String(input)
        .replace(/[<>\"'`\\]/g, '') // Remove HTML/JS special chars
        .trim()
        .substring(0, 100); // Limit length
    case 'number':
      const num = parseFloat(input);
      return isNaN(num) ? null : num;
    case 'protocol':
      // Strict validation for protocol names (alphanumeric, hyphens only)
      if (!/^[a-zA-Z0-9-]+$/.test(input)) {
        throw new Error(`Invalid protocol name: "${input}". Only alphanumeric characters and hyphens are allowed.`);
      }
      return input.toLowerCase().trim().substring(0, 50);
    case 'chain':
      // Strict validation for chain names
      if (!/^[a-zA-Z0-9-\s]+$/.test(input)) {
        throw new Error(`Invalid chain name: "${input}". Only alphanumeric characters, spaces, and hyphens are allowed.`);
      }
      return input.trim().substring(0, 50);
    case 'category':
      // Validate category names
      if (!/^[a-zA-Z0-9-\s]+$/.test(input)) {
        throw new Error(`Invalid category: "${input}". Only alphanumeric characters, spaces, and hyphens are allowed.`);
      }
      return input.trim().substring(0, 50);
    default:
      return input;
  }
}

/**
 * Sanitize API error response to prevent information leakage
 */
function sanitizeErrorData(data) {
  if (!data) return null;
  
  // Convert to string if object
  const dataStr = typeof data === 'object' ? JSON.stringify(data) : String(data);
  
  // Remove sensitive patterns (API keys, tokens, etc.)
  return dataStr
    .replace(/api[_-]?key["\s:]+["']?[\w-]+["']?/gi, '[REDACTED]')
    .replace(/token["\s:]+["']?[\w.-]+["']?/gi, '[REDACTED]')
    .replace(/secret["\s:]+["']?[\w.-]+["']?/gi, '[REDACTED]')
    .replace(/password["\s:]+["']?[\w.-]+["']?/gi, '[REDACTED]')
    .substring(0, 500); // Limit error message length
}

/**
 * Parse and validate numeric input
 */
function parseNumber(value) {
  const num = parseFloat(value);
  return isNaN(num) ? null : num;
}

/**
 * Validate numeric range (only if value is provided)
 */
function validateRange(value, min = 0, max = Infinity, fieldName = 'value') {
  if (value === null || value === undefined) {
    // Value not provided, skip validation
    return null;
  }
  if (value < min || value > max) {
    throw new Error(`${fieldName} must be between ${min} and ${max}`);
  }
  return value;
}

// Helper function to output data
function output(data, format) {
  try {
    switch (format) {
      case 'json':
        console.log(JSON.stringify(data, null, 2));
        break;
      case 'table':
        console.log(DataFormatter.table(data));
        break;
      case 'csv':
        console.log(DataFormatter.csv(data));
        break;
      case 'pretty':
      default:
        console.log(DataFormatter.pretty(data));
    }
  } catch (error) {
    console.error(chalk.red('Error formatting output:'), error.message);
    console.error(chalk.yellow('Falling back to JSON output...'));
    console.log(JSON.stringify(data, null, 2));
  }
}

// ============================================================================
// Error Handling
// ============================================================================

/**
 * Enhanced error handler with proper sanitization and categorization
 */
function handleError(error) {
  const timestamp = new Date().toISOString();
  
  console.error(chalk.red(`\n❌ Error occurred at ${timestamp}\n`));
  console.error(chalk.red('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'));

  if (error.response) {
    // API response error (4xx, 5xx)
    const status = error.response.status;
    const statusType = status >= 500 ? 'Server Error' : 'Client Error';
    
    console.error(chalk.red(`🔴 ${statusType} (${status}):`));
    
    // Sanitize error data to prevent information leakage
    const safeMessage = sanitizeErrorData(error.response.data);
    if (safeMessage) {
      console.error(chalk.yellow(safeMessage));
    } else {
      console.error(chalk.yellow('The request could not be processed'));
    }
    
    // Provide user-friendly suggestions
    if (status === 404) {
      console.error(chalk.cyan('\n💡 Suggestion: The requested resource was not found. Please check the protocol or chain name.'));
    } else if (status === 429) {
      console.error(chalk.cyan('\n💡 Suggestion: Rate limit exceeded. Please wait before making another request.'));
    } else if (status === 500) {
      console.error(chalk.cyan('\n💡 Suggestion: Server error. Please try again later.'));
    }
    
  } else if (error.request) {
    // Network error (no response received)
    console.error(chalk.red('🌐 Network Error:'));
    console.error(chalk.yellow(error.message));
    console.error(chalk.cyan('\n💡 Suggestion: Please check your internet connection and try again.'));
    
  } else if (error.code === 'ECONNREFUSED') {
    console.error(chalk.red('🌐 Connection Refused:'));
    console.error(chalk.yellow('Unable to connect to the API server'));
    console.error(chalk.cyan('\n💡 Suggestion: The service may be temporarily unavailable. Please try again later.'));
    
  } else if (error.code === 'ETIMEDOUT') {
    console.error(chalk.red('⏱️  Request Timeout:'));
    console.error(chalk.yellow('The request took too long to complete'));
    console.error(chalk.cyan('\n💡 Suggestion: Please try again or check your network connection.'));
    
  } else {
    // Other errors (validation, logic, etc.)
    console.error(chalk.red('⚠️  Application Error:'));
    console.error(chalk.yellow(error.message));
    
    // Show stack trace in debug mode only
    if (process.env.DEBUG === 'true') {
      console.error(chalk.gray('\nStack Trace:'));
      console.error(chalk.gray(error.stack));
    }
  }

  console.error(chalk.red('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'));
  
  // Exit with error code
  process.exit(1);
}

// ============================================================================
// DefiLlama commands
// ============================================================================

const defillamaCmd = program
  .command('defillama')
  .description('DefiLlama data commands');

defillamaCmd
  .command('tvl')
  .description('Get total DeFi TVL')
  .option('-f, --format <type>', 'Output format (json, table, csv, pretty)', 'pretty')
  .action(async (options) => {
    try {
      const data = await defillama.getTotalTvl();
      output(data, options.format);
    } catch (error) {
      handleError(error);
    }
  });

defillamaCmd
  .command('protocol')
  .description('Get protocol TVL')
  .requiredOption('-n, --name <name>', 'Protocol name (e.g., aave, uniswap, compound)')
  .option('-f, --format <type>', 'Output format (json, table, csv, pretty)', 'pretty')
  .action(async (options) => {
    try {
      // Validate and sanitize protocol name
      const protocolName = sanitizeInput(options.name, 'protocol');
      
      const data = await defillama.getProtocolTvl(protocolName);
      output(data, options.format);
    } catch (error) {
      handleError(error);
    }
  });

defillamaCmd
  .command('protocols')
  .description('Get all protocols')
  .option('-c, --category <name>', 'Filter by category (e.g., lending, dex)')
  .option('--min-tvl <amount>', 'Minimum TVL in USD', parseNumber)
  .option('--limit <number>', 'Limit results (1-500)', parseNumber)
  .option('--sort <field>', 'Sort by field (tvl, volume)', 'tvl')
  .option('-f, --format <type>', 'Output format (json, table, csv, pretty)', 'pretty')
  .action(async (options) => {
    try {
      // Validate and sanitize inputs
      const filters = {};
      
      if (options.category) {
        filters.category = sanitizeInput(options.category, 'category');
      }
      
      if (options.minTvl !== null) {
        filters.minTvl = validateRange(options.minTvl, 0, Infinity, 'Minimum TVL');
      }
      
      if (options.limit !== null) {
        validateRange(options.limit, 1, 500, 'Limit');
      }
      
      // Validate sort field
      const validSortFields = ['tvl'];
      if (!validSortFields.includes(options.sort)) {
        throw new Error(`Invalid sort field: "${options.sort}". Must be one of: ${validSortFields.join(', ')}`);
      }

      const data = await defillama.getProtocols(filters);

      // Validate data is an array
      if (!Array.isArray(data)) {
        throw new Error('API returned invalid data format: expected array');
      }

      // Apply sorting and limiting
      let results = data;
      if (results.length === 0) {
        output([], options.format);
        return;
      }
      
      if (options.sort === 'tvl') {
        results = results.sort((a, b) => {
          const tvlA = a.tvl || 0;
          const tvlB = b.tvl || 0;
          return tvlB - tvlA;
        });
      }
      if (options.limit) {
        results = results.slice(0, options.limit);
      }

      output(results, options.format);
    } catch (error) {
      handleError(error);
    }
  });

defillamaCmd
  .command('chain')
  .description('Get chain TVL')
  .requiredOption('-n, --name <name>', 'Chain name (e.g., ethereum, solana, polygon)')
  .option('-f, --format <type>', 'Output format (json, table, csv, pretty)', 'pretty')
  .action(async (options) => {
    try {
      // Validate and sanitize chain name
      const chainName = sanitizeInput(options.name, 'chain');
      
      const data = await defillama.getChainTvl(chainName);
      output(data, options.format);
    } catch (error) {
      handleError(error);
    }
  });

defillamaCmd
  .command('yields')
  .description('Get yield pools')
  .option('--min-apy <number>', 'Minimum APY percentage (0-1000)', parseNumber)
  .option('--min-tvl <number>', 'Minimum TVL in USD', parseNumber)
  .option('--chain <name>', 'Filter by chain name (e.g., ethereum, arbitrum)')
  .option('--stablecoin', 'Filter by stablecoin pools only')
  .option('--limit <number>', 'Limit results (1-500)', parseNumber)
  .option('-f, --format <type>', 'Output format (json, table, csv, pretty)', 'pretty')
  .action(async (options) => {
    try {
      // Validate and sanitize inputs
      const filters = {};
      
      if (options.minApy !== null) {
        filters.minApy = validateRange(options.minApy, 0, 1000, 'Minimum APY');
      }
      
      if (options.minTvl !== null) {
        filters.minTvl = validateRange(options.minTvl, 0, Infinity, 'Minimum TVL');
      }
      
      if (options.chain) {
        filters.chain = sanitizeInput(options.chain, 'chain');
      }
      
      if (options.stablecoin) {
        filters.stablecoin = true;
      }
      
      if (options.limit !== null) {
        validateRange(options.limit, 1, 500, 'Limit');
      }

      const data = await defillama.getPoolYields(filters);

      let results = data;
      if (options.limit) {
        results = results.slice(0, options.limit);
      }

      output(results, options.format);
    } catch (error) {
      handleError(error);
    }
  });

// ============================================================================
// Health check command
// ============================================================================

program
  .command('health')
  .description('Check API health status')
  .option('-q, --quiet', 'Quiet mode - only show summary')
  .option('--timeout <ms>', 'Request timeout in milliseconds', parseNumber, 5000)
  .action(async (options) => {
    try {
      const platforms = [
        { name: 'DefiLlama', client: defillama }
      ];

      const results = {};
      let healthyCount = 0;
      let unhealthyCount = 0;

      for (const platform of platforms) {
        try {
          // Actually call the API to check health
          await platform.client.getTotalTvl();
          results[platform.name] = { healthy: true };
          healthyCount++;
        } catch (error) {
          results[platform.name] = { healthy: false, error: error.message };
          unhealthyCount++;
        }
      }

      if (options.quiet) {
        console.log(`Healthy: ${healthyCount} | Unhealthy: ${unhealthyCount} | Total: ${platforms.length}`);
      } else {
        output(results, 'json');
      }
    } catch (error) {
      handleError(error);
    }
  });

// ============================================================================
// Status command
// ============================================================================

program
  .command('status')
  .description('Show system status and recommendations')
  .action(() => {
    console.log(chalk.blue('\n📊 System Status\n'));

    console.log(chalk.green('✓ Available Platforms:'));
    console.log('  - DefiLlama (DeFi data aggregator)');

    console.log(chalk.blue('\nRecommendations:'));
    console.log(chalk.green('  All platforms are configured and ready to use!'));
    console.log(chalk.yellow('  Run `defillama-data health` to check real-time status'));
  });

// ============================================================================
// Parse command line arguments
// ============================================================================

program.parse(process.argv);

// Show help if no command provided
if (!process.argv.slice(2).length) {
  program.outputHelp();
}
