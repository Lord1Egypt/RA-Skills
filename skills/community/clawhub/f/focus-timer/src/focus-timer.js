/**
 * FocusTimer — Pomodoro Timer via Agent
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');
const path = require('path');

class FocusTimer {
  constructor(options = {}) {
    this.focusDuration = (options.focusDuration || 25) * 60000;
    this.shortBreak = (options.shortBreak || 5) * 60000;
    this.longBreak = (options.longBreak || 15) * 60000;
    this.dailyGoal = options.dailyGoal || 8;
    this.dataFile = options.dataFile || './focus-data.json';
    this.sessions = this._load();
    this.current = null;
  }

  start(task) {
    this.current = {
      task: task || 'untagged',
      startTime: Date.now(),
      duration: this.focusDuration,
      status: 'active'
    };
    return {
      message: `🍅 Focus started: ${task}. ${this.focusDuration / 60000} minutes.`,
      endsAt: new Date(Date.now() + this.focusDuration).toLocaleTimeString()
    };
  }

  check() {
    if (!this.current) return { status: 'idle', message: 'No active focus block.' };
    const elapsed = Date.now() - this.current.startTime;
    const remaining = Math.max(0, this.current.duration - elapsed);
    if (remaining === 0) { const r = this.complete(); return r.status === undefined ? { status: 'idle', message: 'Session already completed.' } : r; }
    return {
      status: 'active',
      task: this.current.task,
      elapsed: Math.round(elapsed / 60000),
      remaining: Math.round(remaining / 60000),
      message: `🍅 ${this.current.task} — ${Math.round(remaining / 60000)} min remaining`
    };
  }

  complete() {
    if (!this.current) return { message: 'Nothing to complete.' };
    const session = {
      task: this.current.task,
      date: new Date().toISOString().split('T')[0],
      startTime: this.current.startTime,
      duration: Date.now() - this.current.startTime
    };
    this.sessions.push(session);
    this._save();
    const todayCount = this.todayBlocks();
    this.current = null;
    const breakType = todayCount % 4 === 0 ? 'long' : 'short';
    const breakMin = breakType === 'long' ? this.longBreak / 60000 : this.shortBreak / 60000;
    return {
      status: 'complete',
      message: `⏰ Done! ${Math.round(session.duration / 60000)} min on ${session.task}. Blocks today: ${todayCount}/${this.dailyGoal}. Take a ${breakMin}-min break.`
    };
  }

  todayBlocks() {
    const today = new Date().toISOString().split('T')[0];
    return this.sessions.filter(s => s.date === today).length;
  }

  dailyReport() {
    const today = new Date().toISOString().split('T')[0];
    const todaySessions = this.sessions.filter(s => s.date === today);
    const totalMs = todaySessions.reduce((sum, s) => sum + s.duration, 0);
    const byTask = {};
    for (const s of todaySessions) {
      byTask[s.task] = (byTask[s.task] || 0) + 1;
    }
    return {
      date: today,
      blocks: todaySessions.length,
      goal: this.dailyGoal,
      totalMinutes: Math.round(totalMs / 60000),
      byTask,
      message: `🍅 ${today}: ${todaySessions.length}/${this.dailyGoal} blocks (${Math.round(totalMs / 60000)} min)`
    };
  }

  _load() {
    try { return JSON.parse(fs.readFileSync(this.dataFile, 'utf8')); } catch { return []; }
  }
  _save() {
    try { fs.writeFileSync(this.dataFile, JSON.stringify(this.sessions, null, 2)); } catch {}
  }
}

module.exports = { FocusTimer };
