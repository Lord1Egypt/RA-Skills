#!/usr/bin/env node
/**
 * Reflex: Timing decisions
 * Should I notify the user right now?
 * 
 * Self-modifying: thresholds adjust based on feedback.
 * 
 * Usage:
 *   node timing.js check [urgency]  — should I notify? (urgency 0.0-1.0)
 *   node timing.js adjust <more-quiet|more-alert>  — tune thresholds
 */

const config = {
  // MUTABLE: these values can be patched by cortex
  quietHoursStart: 23,
  quietHoursEnd: 8,
  weekendQuietEnd: 10,
  minIntervalMinutes: 30,
  urgencyThreshold: 0.7,
  timesAdjusted: 0
};

function shouldNotify(hour, dayOfWeek, urgency = 0.5) {
  const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
  const quietEnd = isWeekend ? config.weekendQuietEnd : config.quietHoursEnd;
  
  if (hour >= config.quietHoursStart || hour < quietEnd) {
    return urgency >= config.urgencyThreshold;
  }
  
  return true;
}

function adjustThreshold(direction) {
  if (direction === 'more-quiet') {
    config.urgencyThreshold = Math.min(1.0, config.urgencyThreshold + 0.1);
    config.minIntervalMinutes += 10;
  } else if (direction === 'more-alert') {
    config.urgencyThreshold = Math.max(0.1, config.urgencyThreshold - 0.1);
    config.minIntervalMinutes = Math.max(10, config.minIntervalMinutes - 10);
  }
  config.timesAdjusted++;
}

const cmd = process.argv[2];
if (cmd === 'check') {
  const now = new Date();
  const result = shouldNotify(now.getHours(), now.getDay(), parseFloat(process.argv[3] || '0.5'));
  console.log(JSON.stringify({ shouldNotify: result, hour: now.getHours(), config }));
} else if (cmd === 'adjust') {
  adjustThreshold(process.argv[3]);
  console.log(JSON.stringify(config));
} else {
  console.log('Usage: timing.js <check [urgency]|adjust <more-quiet|more-alert>>');
}
