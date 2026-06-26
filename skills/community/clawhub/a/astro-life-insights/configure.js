#!/usr/bin/env node
// Configure your natal chart (one-time setup)

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import readline from 'readline';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function question(prompt) {
  return new Promise(resolve => rl.question(prompt, resolve));
}

async function configure() {
  console.log('🌟 Astro Life Insights - Natal Chart Setup\n');
  
  const birthDate = await question('Birth date (YYYY-MM-DD): ');
  const birthTime = await question('Birth time (HH:MM in 24-hour format): ');
  const birthCity = await question('Birth city: ');
  const birthCountry = await question('Birth country: ');
  
  // Parse date and time
  const [year, month, day] = birthDate.split('-').map(Number);
  const [hours, minutes] = birthTime.split(':').map(Number);
  
  const natalChart = {
    birthDate: {
      year,
      month,
      day,
      hours,
      minutes
    },
    birthPlace: {
      city: birthCity,
      country: birthCountry
    },
    // Latitude/longitude would normally be geocoded from city
    // For now, we'll just store the city and country
    configured: new Date().toISOString()
  };
  
  // Save to config directory
  const configDir = path.join(process.env.HOME, '.config', 'astro-life-insights');
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }
  
  const configPath = path.join(configDir, 'natal-chart.json');
  fs.writeFileSync(configPath, JSON.stringify(natalChart, null, 2));
  
  console.log(`\n✅ Natal chart saved to ${configPath}`);
  console.log('\nRun `node daily.js` to get your personalized insights!\n');
  
  rl.close();
}

configure().catch(err => {
  console.error('Error:', err.message);
  rl.close();
  process.exit(1);
});
