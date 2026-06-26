#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

const LOG_FILE = path.join(__dirname, '..', 'service.log');

function showLogs() {
  console.log(chalk.blue.bold('📋 Ekybot Connector Service Logs\n'));

  if (!fs.existsSync(LOG_FILE)) {
    console.log(chalk.yellow('⚠️  No log file found'));
    console.log(chalk.gray('The service may not have been started yet, or logging is disabled.'));
    console.log(chalk.gray(`Expected log file: ${LOG_FILE}`));
    return;
  }

  try {
    const logContent = fs.readFileSync(LOG_FILE, 'utf8');
    const lines = logContent.trim().split('\n');

    // Show last 50 lines by default
    const maxLines = process.argv.includes('--all') ? lines.length : 50;
    const displayLines = lines.slice(-maxLines);

    console.log(
      chalk.gray(`Showing last ${displayLines.length} lines (use --all for full log):\n`)
    );

    displayLines.forEach((line) => {
      // Color-code log levels
      if (line.includes('[ERROR]') || line.includes('❌')) {
        console.log(chalk.red(line));
      } else if (line.includes('[WARN]') || line.includes('⚠️')) {
        console.log(chalk.yellow(line));
      } else if (line.includes('[INFO]') || line.includes('✓')) {
        console.log(chalk.green(line));
      } else if (line.includes('[DEBUG]') || line.includes('🔍')) {
        console.log(chalk.blue(line));
      } else {
        console.log(line);
      }
    });

    // Show file info
    const stats = fs.statSync(LOG_FILE);
    console.log(chalk.gray(`\nLog file: ${LOG_FILE}`));
    console.log(chalk.gray(`Size: ${(stats.size / 1024).toFixed(2)} KB`));
    console.log(chalk.gray(`Last modified: ${stats.mtime.toISOString()}`));
  } catch (error) {
    console.error(chalk.red(`❌ Failed to read log file: ${error.message}`));
  }
}

// Follow logs in real-time (like tail -f)
function followLogs() {
  console.log(chalk.blue.bold('📋 Following Ekybot Connector Logs (Ctrl+C to stop)\n'));

  if (!fs.existsSync(LOG_FILE)) {
    console.log(chalk.yellow('⚠️  Log file not found, waiting for creation...'));
  }

  let lastSize = fs.existsSync(LOG_FILE) ? fs.statSync(LOG_FILE).size : 0;

  setInterval(() => {
    if (!fs.existsSync(LOG_FILE)) {
      return;
    }

    const currentSize = fs.statSync(LOG_FILE).size;

    if (currentSize > lastSize) {
      const stream = fs.createReadStream(LOG_FILE, {
        start: lastSize,
        end: currentSize - 1,
      });

      let buffer = '';
      stream.on('data', (chunk) => {
        buffer += chunk.toString();
      });

      stream.on('end', () => {
        const newLines = buffer
          .trim()
          .split('\n')
          .filter((line) => line.length > 0);
        newLines.forEach((line) => {
          const timestamp = new Date().toISOString();

          if (line.includes('[ERROR]') || line.includes('❌')) {
            console.log(chalk.red(`[${timestamp}] ${line}`));
          } else if (line.includes('[WARN]') || line.includes('⚠️')) {
            console.log(chalk.yellow(`[${timestamp}] ${line}`));
          } else if (line.includes('[INFO]') || line.includes('✓')) {
            console.log(chalk.green(`[${timestamp}] ${line}`));
          } else if (line.includes('[DEBUG]') || line.includes('🔍')) {
            console.log(chalk.blue(`[${timestamp}] ${line}`));
          } else {
            console.log(`[${timestamp}] ${line}`);
          }
        });
      });

      lastSize = currentSize;
    }
  }, 1000);
}

// Clear logs
function clearLogs() {
  if (fs.existsSync(LOG_FILE)) {
    fs.writeFileSync(LOG_FILE, '');
    console.log(chalk.green('✓ Log file cleared'));
  } else {
    console.log(chalk.yellow('⚠️  No log file to clear'));
  }
}

// Main function
function main() {
  const args = process.argv.slice(2);

  if (args.includes('--follow') || args.includes('-f')) {
    followLogs();
  } else if (args.includes('--clear')) {
    clearLogs();
  } else {
    showLogs();
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { showLogs, followLogs, clearLogs };
