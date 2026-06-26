#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

class A11yChecker {
  constructor() {
    this.issues = [];
  }

  checkFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const ext = path.extname(filePath);
    
    if (!['.jsx', '.tsx', '.html'].includes(ext)) return;
    
    this.checkImages(content, filePath);
    this.checkButtons(content, filePath);
    this.checkForms(content, filePath);
    this.checkHeadings(content, filePath);
  }

  checkImages(content, file) {
    const imgPattern = /<img[^>]+>/g;
    const matches = content.match(imgPattern) || [];
    
    matches.forEach((img, i) => {
      if (!img.includes('alt=')) {
        this.addIssue({
          file,
          type: 'critical',
          rule: 'missing-alt-text',
          message: 'Image missing alt attribute',
          element: img,
          fix: 'Add alt="" or alt="Description"'
        });
      }
    });
  }

  checkButtons(content, file) {
    const btnPattern = /<button[^>]*>.*?<\/button>/g;
    const matches = content.match(btnPattern) || [];
    
    matches.forEach(btn => {
      const hasText = !/<button[^>]*><[^>]+><\/button>/.test(btn);
      const hasAriaLabel = btn.includes('aria-label');
      
      if (!hasText && !hasAriaLabel) {
        this.addIssue({
          file,
          type: 'critical',
          rule: 'button-no-text',
          message: 'Button has no accessible name',
          element: btn,
          fix: 'Add text content or aria-label'
        });
      }
    });
  }

  checkForms(content, file) {
    const inputPattern = /<input[^>]+>/g;
    const matches = content.match(inputPattern) || [];
    
    matches.forEach(input => {
      const hasLabel = content.includes(`for="${input.match(/id="([^"]+)"/)?.[1]}"`);
      const hasAriaLabel = input.includes('aria-label');
      
      if (!hasLabel && !hasAriaLabel && input.includes('type=')) {
        this.addIssue({
          file,
          type: 'critical',
          rule: 'input-no-label',
          message: 'Form input missing label',
          element: input,
          fix: 'Add <label> or aria-label'
        });
      }
    });
  }

  checkHeadings(content, file) {
    const headings = [];
    for (let i = 1; i <= 6; i++) {
      const pattern = new RegExp(`<h${i}[^>]*>.*?<\/h${i}>`, 'g');
      const matches = content.match(pattern) || [];
      matches.forEach(h => headings.push({ level: i, text: h }));
    }
    
    // Check if h1 exists
    if (!headings.some(h => h.level === 1)) {
      this.addIssue({
        file,
        type: 'warning',
        rule: 'missing-h1',
        message: 'Page missing h1 heading',
        fix: 'Add main h1 heading'
      });
    }
  }

  addIssue(issue) {
    this.issues.push(issue);
  }

  generateReport() {
    const critical = this.issues.filter(i => i.type === 'critical');
    const warnings = this.issues.filter(i => i.type === 'warning');
    
    let report = '\n♿ Accessibility Report\n';
    report += '━'.repeat(50) + '\n\n';
    report += `Total issues: ${this.issues.length}\n\n`;
    
    if (critical.length > 0) {
      report += `🔴 CRITICAL (${critical.length}):\n`;
      critical.slice(0, 5).forEach(issue => {
        report += `  - ${issue.message} (${issue.file})\n`;
        report += `    Fix: ${issue.fix}\n`;
      });
      report += '\n';
    }
    
    if (warnings.length > 0) {
      report += `🟡 WARNINGS (${warnings.length}):\n`;
      warnings.slice(0, 3).forEach(issue => {
        report += `  - ${issue.message}\n`;
      });
    }
    
    return report;
  }

  scanDirectory(dir) {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      
      if (stat.isDirectory() && !file.startsWith('.') && file !== 'node_modules') {
        this.scanDirectory(filePath);
      } else if (stat.isFile()) {
        this.checkFile(filePath);
      }
    });
  }
}

export default A11yChecker;

if (import.meta.url === `file://${process.argv[1]}`) {
  const checker = new A11yChecker();
  const target = process.argv[2] || './src';
  
  if (fs.existsSync(target)) {
    const stat = fs.statSync(target);
    if (stat.isDirectory()) {
      checker.scanDirectory(target);
    } else {
      checker.checkFile(target);
    }
  }
  
  console.log(checker.generateReport());
}
