#!/usr/bin/env node

/**
 * cuihua-logger - AI-Powered Logging Assistant
 * Generate production-ready structured logs
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class Logger {
  constructor(options = {}) {
    this.options = {
      logLevel: options.logLevel || 'info',
      includePerformance: options.includePerformance !== false,
      ...options
    };
    
    this.functions = [];
    this.stats = {
      filesScanned: 0,
      functionsAnalyzed: 0,
      withLogging: 0,
      needsLogging: 0
    };
  }

  /**
   * Analyze file for logging
   */
  analyzeFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const ext = path.extname(filePath);
    
    if (!['.js', '.ts', '.jsx', '.tsx'].includes(ext)) {
      return;
    }
    
    this.stats.filesScanned++;
    this.findFunctions(content, filePath);
  }

  /**
   * Find functions needing logging
   */
  findFunctions(content, filePath) {
    // Find async functions
    const asyncPattern = /async\s+function\s+(\w+)\s*\([^)]*\)\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}/g;
    let match;
    
    while ((match = asyncPattern.exec(content)) !== null) {
      const name = match[1];
      const body = match[2];
      const hasLogging = this.checkLogging(body);
      
      this.addFunction({
        name,
        file: filePath,
        body,
        hasLogging,
        line: this.getLineNumber(content, match.index)
      });
    }
  }

  /**
   * Check if function has logging
   */
  checkLogging(body) {
    return /logger\.|console\./.test(body);
  }

  /**
   * Add function to analysis
   */
  addFunction(fn) {
    this.functions.push(fn);
    this.stats.functionsAnalyzed++;
    
    if (fn.hasLogging) {
      this.stats.withLogging++;
    } else {
      this.stats.needsLogging++;
    }
  }

  /**
   * Generate logging code
   */
  generateLogging(fn) {
    const { name, body } = fn;
    
    return `async function ${name}(...args) {
  logger.info('${name} started', { args });
  const startTime = Date.now();
  
  try {
${body.trim().split('\n').map(line => '    ' + line).join('\n')}
    
    const duration = Date.now() - startTime;
    logger.info('${name} completed', { args, duration });
    
  } catch (error) {
    const duration = Date.now() - startTime;
    logger.error('${name} failed', { 
      args, 
      duration,
      error: error.message,
      stack: error.stack 
    });
    throw error;
  }
}`;
  }

  /**
   * Get line number
   */
  getLineNumber(content, offset) {
    return content.substring(0, offset).split('\n').length;
  }

  /**
   * Generate report
   */
  generateReport() {
    const coverage = this.stats.functionsAnalyzed > 0
      ? Math.round((this.stats.withLogging / this.stats.functionsAnalyzed) * 100)
      : 0;
    
    let report = `\n📝 Logging Coverage Report\n`;
    report += `━`.repeat(50) + `\n\n`;
    report += `📁 Files scanned: ${this.stats.filesScanned}\n`;
    report += `🔍 Functions analyzed: ${this.stats.functionsAnalyzed}\n`;
    report += `📊 Coverage: ${coverage}%\n`;
    report += `  ✅ With logging: ${this.stats.withLogging}\n`;
    report += `  ❌ Needs logging: ${this.stats.needsLogging}\n\n`;

    if (this.stats.needsLogging > 0) {
      report += `❌ Functions without logging:\n`;
      this.functions
        .filter(fn => !fn.hasLogging)
        .slice(0, 10)
        .forEach((fn, i) => {
          report += `  ${i + 1}. ${fn.file}:${fn.line} - ${fn.name}()\n`;
        });
      
      if (this.stats.needsLogging > 10) {
        report += `  ... and ${this.stats.needsLogging - 10} more\n`;
      }
    }

    return report;
  }

  /**
   * Scan directory
   */
  scanDirectory(dir) {
    const files = fs.readdirSync(dir);
    
    files.forEach(file => {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      
      if (stat.isDirectory()) {
        if (!file.startsWith('.') && file !== 'node_modules') {
          this.scanDirectory(filePath);
        }
      } else if (stat.isFile()) {
        this.analyzeFile(filePath);
      }
    });
  }
}

export default Logger;

// CLI
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const command = args[0] || 'check';
  const targetPath = args[1] || './src';
  
  const logger = new Logger();
  
  console.log('📝 cuihua-logger starting...\n');
  
  if (command === 'check') {
    if (fs.existsSync(targetPath)) {
      const stat = fs.statSync(targetPath);
      if (stat.isDirectory()) {
        logger.scanDirectory(targetPath);
      } else {
        logger.analyzeFile(targetPath);
      }
    }
    
    console.log(logger.generateReport());
  }
}
