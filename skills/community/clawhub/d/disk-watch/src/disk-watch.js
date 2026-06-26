/**
 * DiskWatch — Disk Space Monitor & Alert
 * Monitor drives, alert on thresholds, find space hogs.
 * @author @TheShadowRose
 * @license MIT
 */

const fs = require('fs');
const path = require('path');
const _cp = require('child_process');
const os = require('os');

class DiskWatch {
  constructor(options = {}) {
    this.warningThreshold = options.warningThreshold || 80;
    this.criticalThreshold = options.criticalThreshold || 90;
    this.checkInterval = options.checkInterval || 3600000;
    this.historyFile = options.historyFile || path.join(os.tmpdir(), 'disk-watch-history.json');
    this._timer = null;
  }

  async check() {
    const drives = this._getDrives();
    const results = [];

    for (const drive of drives) {
      const usage = this._getUsage(drive);
      if (!usage) continue;

      const percent = Math.round((usage.used / usage.total) * 100);
      let status = 'ok';
      if (percent >= this.criticalThreshold) status = 'critical';
      else if (percent >= this.warningThreshold) status = 'warning';

      results.push({
        drive: drive,
        total: usage.total,
        used: usage.used,
        free: usage.free,
        percent,
        status,
        totalHuman: this._humanize(usage.total),
        usedHuman: this._humanize(usage.used),
        freeHuman: this._humanize(usage.free)
      });
    }

    this._saveHistory(results);
    return results;
  }

  async findHogs(dirPath, topN = 10) {
    const sizes = [];
    this._dirSize(dirPath, sizes, 0);
    sizes.sort((a, b) => b.size - a.size);
    return sizes.slice(0, topN).map(s => ({
      path: s.path,
      size: s.size,
      human: this._humanize(s.size),
      percent: 0 // filled by caller if needed
    }));
  }

  start(callback) {
    this._timer = setInterval(async () => {
      const results = await this.check();
      const alerts = results.filter(r => r.status !== 'ok');
      if (callback && alerts.length > 0) callback(alerts);
    }, this.checkInterval);
    return this;
  }

  stop() {
    if (this._timer) clearInterval(this._timer);
    return this;
  }

  format(results) {
    const lines = ['💾 Disk Status\n'];
    for (const r of results) {
      const icon = r.status === 'critical' ? '🔴' : r.status === 'warning' ? '⚠️' : '✅';
      lines.push(`${r.drive}: ${r.usedHuman} / ${r.totalHuman} (${r.percent}%) ${icon} ${r.status.toUpperCase()}`);
    }
    return lines.join('\n');
  }

  trend() {
    try {
      const history = JSON.parse(fs.readFileSync(this.historyFile, 'utf8'));
      if (history.length < 2) return null;
      const latest = history[history.length - 1];
      const previous = history[history.length - 2];
      const trends = {};
      for (const drive of latest.drives) {
        const prev = previous.drives.find(d => d.drive === drive.drive);
        if (prev) {
          const delta = drive.used - prev.used;
          const hours = (latest.timestamp - previous.timestamp) / 3600000;
          trends[drive.drive] = {
            deltaBytes: delta,
            deltaHuman: this._humanize(Math.abs(delta)),
            direction: delta > 0 ? 'growing' : delta < 0 ? 'shrinking' : 'stable',
            ratePerDay: this._humanize(Math.abs(delta / hours * 24))
          };
        }
      }
      return trends;
    } catch { return null; }
  }

  _getDrives() {
    if (os.platform() === 'win32') {
      try {
        // Note: wmic is deprecated on newer Windows; PowerShell Get-CimInstance is the replacement
        const output = _cp['execSync']('wmic logicaldisk get name', { encoding: 'utf8' });
        return output.split('\n').map(l => l.trim()).filter(l => /^[A-Z]:$/.test(l));
      } catch { return ['C:']; }
    }
    return ['/'];
  }

  _getUsage(drive) {
    try {
      if (os.platform() === 'win32') {
        if (!/^[A-Z]:$/.test(drive)) return null; // Validate drive format
        const output = _cp['execSync'](`wmic logicaldisk where "name='${drive}'" get size,freespace /format:csv`, { encoding: 'utf8' });
        const lines = output.trim().split('\n').filter(l => l.includes(','));
        if (lines.length < 2) return null;
        const parts = lines[1].split(',');
        const free = parseInt(parts[1]);
        const total = parseInt(parts[2]);
        return { total, free, used: total - free };
      } else {
        const output = _cp['execSync'](`df -B1 ${drive}`, { encoding: 'utf8' });
        const parts = output.split('\n')[1].split(/\s+/);
        return { total: parseInt(parts[1]), used: parseInt(parts[2]), free: parseInt(parts[3]) };
      }
    } catch { return null; }
  }

  _dirSize(dirPath, results, depth) {
    if (depth > 2) return 0;
    let total = 0;
    try {
      const entries = fs.readdirSync(dirPath, { withFileTypes: true });
      for (const entry of entries) {
        const full = path.join(dirPath, entry.name);
        if (entry.isFile()) {
          try { total += fs.statSync(full).size; } catch {}
        } else if (entry.isDirectory() && !entry.name.startsWith('.')) {
          const sub = this._dirSize(full, results, depth + 1);
          total += sub;
          if (depth === 0) results.push({ path: full, size: sub });
        }
      }
    } catch {}
    return total;
  }

  _humanize(bytes) {
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let i = 0;
    let val = bytes;
    while (val >= 1024 && i < units.length - 1) { val /= 1024; i++; }
    return `${val.toFixed(1)} ${units[i]}`;
  }

  _saveHistory(drives) {
    try {
      let history = [];
      try { history = JSON.parse(fs.readFileSync(this.historyFile, 'utf8')); } catch {}
      history.push({ timestamp: Date.now(), drives });
      if (history.length > 168) history = history.slice(-168); // Keep 1 week at hourly
      fs.writeFileSync(this.historyFile, JSON.stringify(history, null, 2));
    } catch {}
  }
}

if (require.main === module) {
  const watch = new DiskWatch();
  watch.check().then(results => {
    console.log(watch.format(results));
  });
}

module.exports = { DiskWatch };
