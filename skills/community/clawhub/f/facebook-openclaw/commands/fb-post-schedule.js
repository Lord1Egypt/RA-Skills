#!/usr/bin/env node
/**
 * OpenClaw Command: fb-post-schedule
 * Schedule a post for later publication on Facebook Page.
 * 
 * Usage:
 *   openclaw fb-post-schedule "<message>" "<time>"
 * 
 * Time formats:
 *   Natural language: "tomorrow 9am", "in 2 hours", "next monday"
 *   ISO format: "2024-12-31T23:59:59Z"
 */

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');
const https = require('https');

const program = new Command();

// Parse time string to Unix timestamp
function parseTime(timeStr) {
  const now = new Date();
  const lower = timeStr.toLowerCase();
  
  // Try ISO format first
  const isoMatch = timeStr.match(/^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})(Z)?$/);
  if (isoMatch) {
    const date = new Date(timeStr.replace(' ', 'T'));
    if (!isNaN(date.getTime())) {
      return Math.floor(date.getTime() / 1000);
    }
  }
  
  // Natural language parsing
  let hoursToAdd = 0;
  let minutesToAdd = 0;
  let daysToAdd = 0;
  let targetHour = null;
  let targetMinute = 0;
  
  // "in X hours"
  const inHoursMatch = lower.match(/in\s+(\d+)\s+hours?/);
  if (inHoursMatch) {
    hoursToAdd = parseInt(inHoursMatch[1], 10);
    return Math.floor((now.getTime() + hoursToAdd * 60 * 60 * 1000) / 1000);
  }
  
  // "in X minutes"
  const inMinutesMatch = lower.match(/in\s+(\d+)\s+minutes?/);
  if (inMinutesMatch) {
    minutesToAdd = parseInt(inMinutesMatch[1], 10);
    return Math.floor((now.getTime() + minutesToAdd * 60 * 1000) / 1000);
  }
  
  // "tomorrow"
  if (lower.includes('tomorrow')) {
    daysToAdd = 1;
  }
  
  // "next week"
  if (lower.includes('next week')) {
    daysToAdd = 7;
  }
  
  // "next month"
  if (lower.includes('next month')) {
    daysToAdd = 30;
  }
  
  // "next monday" etc
  const dayNames = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
  for (let i = 0; i < dayNames.length; i++) {
    if (lower.includes(dayNames[i])) {
      const currentDay = now.getDay();
      let daysUntil = i - currentDay;
      if (daysUntil <= 0) {
        daysUntil += 7;
      }
      // If "next monday" and today is monday, add 7 days
      if (lower.startsWith('next ') && daysUntil === 7 && currentDay === i) {
        daysUntil = 7;
      }
      daysToAdd = daysUntil;
      break;
    }
  }
  
  // Time like "9am", "10:30pm", "2pm"
  const timeMatch = lower.match(/(\d{1,2})(?::(\d{2}))?\s*(am|pm)?/);
  if (timeMatch) {
    targetHour = parseInt(timeMatch[1], 10);
    targetMinute = timeMatch[2] ? parseInt(timeMatch[2], 10) : 0;
    const period = timeMatch[3] || 'am';
    
    if (period === 'pm' && targetHour < 12) {
      targetHour += 12;
    } else if (period === 'am' && targetHour === 12) {
      targetHour = 0;
    }
  }
  
  // Calculate target date
  const targetDate = new Date(now);
  targetDate.setDate(now.getDate() + daysToAdd);
  
  if (targetHour !== null) {
    targetDate.setHours(targetHour, targetMinute, 0, 0);
    
    // If time has passed today, add a day
    if (targetDate <= now && daysToAdd === 0) {
      targetDate.setDate(targetDate.getDate() + 1);
    }
  } else {
    // Default to 9am
    targetDate.setHours(9, 0, 0, 0);
    if (targetDate <= now) {
      targetDate.setDate(targetDate.getDate() + 1);
    }
  }
  
  return Math.floor(targetDate.getTime() / 1000);
}

program
  .name('fb-post-schedule')
  .description('Schedule a post for later')
  .argument('<message>', 'The message to schedule')
  .argument('<time>', 'When to post (e.g., "tomorrow 9am", "in 2 hours", "2024-12-31T23:59:59Z")')
  .action((message, timeStr) => {
    const workspace = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace');
    const configPath = path.join(workspace, 'facebook-posting.json');
    
    if (!fs.existsSync(configPath)) {
      console.error('❌ Configuration file not found: facebook-posting.json');
      console.error('Run "openclaw fb-post-setup" first.');
      process.exit(1);
    }
    
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const { access_token, page_id } = config;
    
    const scheduledTime = parseTime(timeStr);
    const scheduledDate = new Date(scheduledTime * 1000);
    const now = new Date();
    const timeUntil = Math.floor((scheduledTime * 1000 - now.getTime()) / (1000 * 60 * 60)); // hours
    
    console.log('⏰ Scheduling post...\n');
    console.log(`Page: ${config.page_name || page_id}`);
    console.log(`Message: "${message}"`);
    console.log(`Scheduled for: ${scheduledDate.toLocaleString()}`);
    if (timeUntil > 0) {
      console.log(`In: ${timeUntil} hour(s)`);
    }
    console.log('');
    
    const bodyData = {
      message: message,
      scheduled_publish_time: scheduledTime,
      access_token: access_token
    };
    
    const queryString = Object.keys(bodyData)
      .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(bodyData[key])}`)
      .join('&');
    
    const options = {
      hostname: 'graph.facebook.com',
      path: `/${page_id}/feed?${queryString}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.id) {
            console.log('✅ Post scheduled successfully!');
            console.log(`Post ID: ${result.id}`);
            console.log('');
            console.log('To view scheduled posts:');
            console.log('  openclaw fb-post-schedule-list');
            console.log('');
            console.log('To cancel this post:');
            console.log(`  openclaw fb-post-schedule-delete ${result.id}`);
          } else {
            console.error('❌ Error scheduling post:');
            if (result.error) {
              console.error(result.error.message);
            } else {
              console.error(result);
            }
            process.exit(1);
          }
        } catch (err) {
          console.error('❌ Error parsing response:', err.message);
          process.exit(1);
        }
      });
    });
    
    req.on('error', (err) => {
      console.error('❌ Request error:', err.message);
      process.exit(1);
    });
    
    req.end();
  });

program.parse();
