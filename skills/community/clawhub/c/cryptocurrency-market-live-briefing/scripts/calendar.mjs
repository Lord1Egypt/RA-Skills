#!/usr/bin/env node

/**
 * Get Market Calendar
 * Usage: node calendar.mjs [date YYYY-MM-DD]
 */

const args = process.argv.slice(2);
const date = args[0] || new Date().toISOString().split('T')[0];

const BASE_URL = 'https://api1.desk3.io/v1/market/calendar';

async function getCalendar(dateStr) {
  try {
    const response = await fetch(`${BASE_URL}?date=${dateStr}`, {
      headers: { 'language': 'en' }
    });
    const data = await response.json();
    
    if (data.code !== 0 || !data.data) {
      console.error('API returned error');
      return null;
    }
    
    console.log(`\n📅 Market Calendar - ${dateStr}\n` + '='.repeat(60));
    
    const events = data.data[0]?.events || [];
    if (events.length > 0) {
      events.forEach((event, i) => {
        const startTime = new Date(event.starttime * 1000).toLocaleString('en-US', {
          month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
        });
        console.log(`\n${i + 1}. ${event.title}`);
        console.log(`   Time: ${startTime}`);
      });
    } else {
      console.log('   No important events');
    }
    
    console.log('\n' + '='.repeat(60));
    return events;
  } catch (error) {
    console.error('Failed to fetch calendar:', error.message);
    return null;
  }
}

getCalendar(date);
