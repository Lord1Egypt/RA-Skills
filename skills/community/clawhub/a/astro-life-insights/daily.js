#!/usr/bin/env node
// Get your daily astrological insights

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { getPlanetaryPositions, calculateAspects, getSignificantAspects } from './calculate.js';
import { generateInsights, formatInsights } from './interpret.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function daily() {
  // Load natal chart
  const configPath = path.join(process.env.HOME, '.config', 'astro-life-insights', 'natal-chart.json');
  
  if (!fs.existsSync(configPath)) {
    console.error('❌ Natal chart not configured!');
    console.error('Run `node configure.js` first to set up your birth chart.\n');
    process.exit(1);
  }
  
  const natalChart = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  
  // Get natal positions (calculate once for birth date)
  const birthDate = new Date(
    natalChart.birthDate.year,
    natalChart.birthDate.month - 1,
    natalChart.birthDate.day,
    natalChart.birthDate.hours,
    natalChart.birthDate.minutes
  );
  
  console.log('Calculating natal chart positions...');
  const natalPositions = getPlanetaryPositions(birthDate);
  
  // Get current transits
  const now = new Date();
  console.log('Calculating current transits...');
  const transitPositions = getPlanetaryPositions(now);
  
  // Calculate aspects
  console.log('Finding aspects...\n');
  const allAspects = calculateAspects(transitPositions, natalPositions);
  const significantAspects = getSignificantAspects(allAspects, 15);
  
  // Generate insights
  const insights = generateInsights(significantAspects);
  
  // Format and display
  const output = formatInsights(insights, now);
  console.log(output);
}

daily().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
