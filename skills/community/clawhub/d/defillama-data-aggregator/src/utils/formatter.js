/**
 * Data formatting utilities
 */

const chalk = require('chalk');
const Table = require('cli-table3');

class DataFormatter {
  /**
   * Format data as JSON
   */
  static json(data) {
    return JSON.stringify(data, null, 2);
  }

  /**
   * Format data as pretty JSON with colors
   */
  static pretty(data) {
    const formatValue = (value) => {
      if (typeof value === 'number') {
        return chalk.green(value.toLocaleString());
      } else if (typeof value === 'string') {
        return chalk.yellow(value);
      } else if (typeof value === 'boolean') {
        return value ? chalk.green('✓') : chalk.red('✗');
      } else if (value === null || value === undefined) {
        return chalk.gray('N/A');
      } else if (Array.isArray(value)) {
        return `[${value.map(formatValue).join(', ')}]`;
      } else if (typeof value === 'object') {
        const entries = Object.entries(value)
          .map(([k, v]) => `  ${chalk.cyan(k)}: ${formatValue(v)}`)
          .join('\n');
        return `{\n${entries}\n}`;
      }
      return value;
    };

    return JSON.stringify(data, null, 2)
      .replace(/"([^"]+)":/g, (match, key) => `"${chalk.cyan(key)}":`)
      .replace(/: ("[^"]+")/g, (match, value) => `: ${formatValue(value.slice(1, -1))}`)
      .replace(/: (\d+)/g, (match, value) => `: ${formatValue(parseInt(value))}`);
  }

  /**
   * Format data as table
   */
  static table(data, options = {}) {
    if (!data || (Array.isArray(data) && data.length === 0)) {
      return chalk.yellow('No data available');
    }

    const items = Array.isArray(data) ? data : [data];
    const keys = options.columns || Object.keys(items[0]);

    const table = new Table({
      head: keys.map(k => chalk.cyan(k)),
      style: {
        head: [],
        border: ['grey']
      }
    });

    items.forEach(item => {
      const row = keys.map(key => this.formatCell(item[key]));
      table.push(row);
    });

    return table.toString();
  }

  /**
   * Format table cell
   */
  static formatCell(value) {
    if (value === null || value === undefined) {
      return chalk.gray('N/A');
    }

    if (typeof value === 'number') {
      // Format large numbers
      if (value >= 1e9) {
        return `$${(value / 1e9).toFixed(2)}B`;
      } else if (value >= 1e6) {
        return `$${(value / 1e6).toFixed(2)}M`;
      } else if (value >= 1e3) {
        return `$${(value / 1e3).toFixed(2)}K`;
      } else if (value < 1 && value > 0) {
        return `$${value.toFixed(4)}`;
      } else {
        return value.toLocaleString();
      }
    }

    if (typeof value === 'string') {
      // Truncate long strings
      return value.length > 30 ? `${value.substring(0, 27)}...` : value;
    }

    if (typeof value === 'boolean') {
      return value ? chalk.green('Yes') : chalk.red('No');
    }

    return String(value);
  }

  /**
   * Format data as CSV
   */
  static csv(data) {
    if (!data || (Array.isArray(data) && data.length === 0)) {
      return '';
    }

    const items = Array.isArray(data) ? data : [data];
    const keys = Object.keys(items[0]);

    const escapeCsv = (value) => {
      if (value === null || value === undefined) return '';
      const str = String(value);
      if (str.includes(',') || str.includes('"') || str.includes('\n')) {
        return `"${str.replace(/"/g, '""')}"`;
      }
      return str;
    };

    const header = keys.join(',');
    const rows = items.map(item =>
      keys.map(key => escapeCsv(item[key])).join(',')
    );

    return [header, ...rows].join('\n');
  }

  /**
   * Format percentage
   */
  static percentage(value, decimals = 2) {
    if (value === null || value === undefined) {
      return chalk.gray('N/A');
    }

    const formatted = `${value > 0 ? '+' : ''}${value.toFixed(decimals)}%`;
    return value > 0 ? chalk.green(formatted) : value < 0 ? chalk.red(formatted) : chalk.yellow(formatted);
  }

  /**
   * Format currency
   */
  static currency(value, decimals = 2) {
    if (value === null || value === undefined) {
      return chalk.gray('N/A');
    }

    const formatted = `$${value.toFixed(decimals)}`;
    return value > 0 ? chalk.green(formatted) : chalk.red(formatted);
  }

  /**
   * Format date
   */
  static date(timestamp) {
    if (!timestamp) {
      return chalk.gray('N/A');
    }

    const date = new Date(timestamp);
    return chalk.yellow(date.toLocaleString());
  }

  /**
   * Format change indicator
   */
  static change(value) {
    const icon = value > 0 ? '↑' : value < 0 ? '↓' : '→';
    const color = value > 0 ? 'green' : value < 0 ? 'red' : 'yellow';
    return chalk[color](`${icon} ${Math.abs(value).toFixed(2)}%`);
  }
}

module.exports = DataFormatter;
