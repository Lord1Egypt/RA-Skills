#!/usr/bin/env node
import { execSync } from 'child_process';
import fs from 'fs';

class DependencyUpdater {
  async checkOutdated() {
    try {
      const result = execSync('npm outdated --json', { encoding: 'utf8' });
      const outdated = JSON.parse(result || '{}');
      
      const security = [];
      const breaking = [];
      const safe = [];
      
      for (const [name, info] of Object.entries(outdated)) {
        const current = info.current;
        const latest = info.latest;
        
        // Simple heuristic
        const currentMajor = parseInt(current.split('.')[0]);
        const latestMajor = parseInt(latest.split('.')[0]);
        
        if (latestMajor > currentMajor) {
          breaking.push({ name, current, latest, type: 'major' });
        } else {
          safe.push({ name, current, latest, type: 'minor/patch' });
        }
      }
      
      return { security, breaking, safe };
    } catch (error) {
      return { security: [], breaking: [], safe: [] };
    }
  }

  generateReport(data) {
    let report = '\n📦 Dependency Update Report\n';
    report += '━'.repeat(50) + '\n\n';
    
    if (data.security.length > 0) {
      report += `🔴 Security updates (${data.security.length}):\n`;
      data.security.forEach(dep => {
        report += `  - ${dep.name}: ${dep.current} → ${dep.latest}\n`;
      });
      report += '\n';
    }
    
    if (data.breaking.length > 0) {
      report += `🟡 Breaking changes (${data.breaking.length}):\n`;
      data.breaking.forEach(dep => {
        report += `  - ${dep.name}: ${dep.current} → ${dep.latest} (Major)\n`;
      });
      report += '\n';
    }
    
    if (data.safe.length > 0) {
      report += `🟢 Safe updates (${data.safe.length}):\n`;
      data.safe.slice(0, 5).forEach(dep => {
        report += `  - ${dep.name}: ${dep.current} → ${dep.latest}\n`;
      });
      if (data.safe.length > 5) {
        report += `  ... and ${data.safe.length - 5} more\n`;
      }
    }
    
    return report;
  }
}

export default DependencyUpdater;

if (import.meta.url === `file://${process.argv[1]}`) {
  const updater = new DependencyUpdater();
  const data = await updater.checkOutdated();
  console.log(updater.generateReport(data));
}
