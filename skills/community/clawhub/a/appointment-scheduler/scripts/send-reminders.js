#!/usr/bin/env node
/**
 * Send appointment reminders
 * Usage:
 *   node send-reminders.js --type day-before
 *   node send-reminders.js --type hour-before
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const type = args.includes('--type') ? args[args.indexOf('--type') + 1] : 'day-before';

const DATA_DIR = path.join(process.env.HOME, '.openclaw', 'workspace', 'data', 'appointments', 'bookings');
const REMINDER_LOG = path.join(process.env.HOME, '.openclaw', 'workspace', 'data', 'appointments', 'reminders', 'sent.json');

// Load config
const CONFIG_FILE = path.join(process.env.HOME, '.openclaw', 'workspace', 'config', 'appointment-scheduler.json');
if (!fs.existsSync(CONFIG_FILE)) {
  console.error('❌ Config not found. Run init-config.js first.');
  process.exit(1);
}
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));

// Load reminder log
if (!fs.existsSync(path.dirname(REMINDER_LOG))) {
  fs.mkdirSync(path.dirname(REMINDER_LOG), { recursive: true });
}
let reminderLog = {};
if (fs.existsSync(REMINDER_LOG)) {
  reminderLog = JSON.parse(fs.readFileSync(REMINDER_LOG, 'utf8'));
}

function formatDate(date) {
  return date.toISOString().split('T')[0];
}

function getTargetDate() {
  const now = new Date();
  if (type === 'day-before') {
    const tomorrow = new Date(now);
    tomorrow.setDate(now.getDate() + 1);
    return formatDate(tomorrow);
  } else if (type === 'hour-before') {
    return formatDate(now);
  }
  return null;
}

function shouldSendReminder(booking, type) {
  const now = new Date();
  const bookingDate = new Date(`${booking.date}T${booking.time}:00`);
  
  if (type === 'day-before') {
    const hoursDiff = (bookingDate - now) / (1000 * 60 * 60);
    return hoursDiff > 12 && hoursDiff < 36 && !booking.reminded.day_before;
  } else if (type === 'hour-before') {
    const hoursDiff = (bookingDate - now) / (1000 * 60 * 60);
    return hoursDiff > 1.5 && hoursDiff < 2.5 && !booking.reminded.hour_before;
  }
  return false;
}

function formatMessage(booking, type) {
  const businessName = config.business_name || '저희';
  
  if (type === 'day-before') {
    return `안녕하세요 ${booking.customer.name}님, ${businessName}입니다.\n\n내일(${booking.date}) ${booking.time}에 ${booking.service} 예약이 있습니다.\n\n변경이 필요하시면 미리 연락 부탁드립니다. 감사합니다! 🙏`;
  } else if (type === 'hour-before') {
    return `${booking.customer.name}님, 2시간 후(${booking.time})에 ${booking.service} 예약이 있습니다.\n\n곧 뵙겠습니다! 😊`;
  }
  return '';
}

// Main logic
const targetDate = getTargetDate();
if (!targetDate) {
  console.error('❌ Invalid type. Use day-before or hour-before');
  process.exit(1);
}

const filePath = path.join(DATA_DIR, `${targetDate}.json`);
if (!fs.existsSync(filePath)) {
  console.log(`ℹ️  No bookings found for ${targetDate}`);
  process.exit(0);
}

const bookings = JSON.parse(fs.readFileSync(filePath, 'utf8'));
let sent = 0;

bookings.forEach(booking => {
  if (shouldSendReminder(booking, type)) {
    const message = formatMessage(booking, type);
    const contact = booking.customer.phone || booking.customer.email;
    
    if (!contact) {
      console.log(`⚠️  No contact info for ${booking.customer.name} (booking ${booking.id})`);
      return;
    }
    
    // Output reminder message for agent to send via message tool
    console.log('\n📤 SEND_REMINDER');
    console.log(JSON.stringify({
      booking_id: booking.id,
      customer: booking.customer.name,
      contact: contact,
      message: message,
      type: type
    }, null, 2));
    
    // Mark as reminded
    booking.reminded[type === 'day-before' ? 'day_before' : 'hour_before'] = true;
    
    // Log
    if (!reminderLog[booking.id]) {
      reminderLog[booking.id] = {};
    }
    reminderLog[booking.id][type] = {
      sent_at: new Date().toISOString(),
      contact: contact
    };
    
    sent++;
  }
});

// Save updated bookings
fs.writeFileSync(filePath, JSON.stringify(bookings, null, 2));

// Save reminder log
fs.writeFileSync(REMINDER_LOG, JSON.stringify(reminderLog, null, 2));

console.log(`\n✅ Sent ${sent} reminders (type: ${type})`);
