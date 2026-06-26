#!/usr/bin/env node
/**
 * Initialize appointment-scheduler configuration
 */

const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(process.env.HOME, '.openclaw', 'workspace', 'config');
const CONFIG_FILE = path.join(CONFIG_DIR, 'appointment-scheduler.json');

const defaultConfig = {
  business_name: "MUFI 포토부스",
  business_hours: {
    monday: { open: "10:00", close: "20:00" },
    tuesday: { open: "10:00", close: "20:00" },
    wednesday: { open: "10:00", close: "20:00" },
    thursday: { open: "10:00", close: "20:00" },
    friday: { open: "10:00", close: "22:00" },
    saturday: { open: "10:00", close: "22:00" },
    sunday: { open: "12:00", close: "18:00" }
  },
  services: {
    "포토촬영": { duration: 30, buffer: 10 },
    "컷": { duration: 60, buffer: 10 },
    "펌": { duration: 120, buffer: 15 },
    "염색": { duration: 90, buffer: 15 }
  },
  reminders: {
    day_before: { enabled: true, time: "09:00" },
    hour_before: { enabled: true, hours: 2 }
  },
  noshow_policy: {
    grace_period_min: 15,
    flag_threshold: 3,
    require_deposit_when_flagged: true
  },
  calendar: {
    google: {
      enabled: true,
      calendar_id: "primary"
    },
    naver: {
      enabled: false
    }
  }
};

// Create config directory if it doesn't exist
if (!fs.existsSync(CONFIG_DIR)) {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
}

// Check if config already exists
if (fs.existsSync(CONFIG_FILE)) {
  console.log('⚠️  Config file already exists:', CONFIG_FILE);
  console.log('Delete it first if you want to reinitialize.');
  process.exit(0);
}

// Write default config
fs.writeFileSync(CONFIG_FILE, JSON.stringify(defaultConfig, null, 2));
console.log('✅ Config initialized:', CONFIG_FILE);
console.log('📝 Edit the config file to customize for your business.');
