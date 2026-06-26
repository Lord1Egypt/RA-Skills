#!/usr/bin/env node
// Output today's astrological insights as JSON for dashboard use

import fs from 'fs';
import path from 'path';
import { getPlanetaryPositions, calculateAspects, getSignificantAspects } from './calculate.js';
import { generateInsights } from './interpret.js';

async function dailyJson() {
  const configPath = path.join(process.env.HOME, '.config', 'astro-life-insights', 'natal-chart.json');

  if (!fs.existsSync(configPath)) {
    console.log(JSON.stringify({ error: 'Natal chart not configured' }));
    process.exit(1);
  }

  const natalChart = JSON.parse(fs.readFileSync(configPath, 'utf8'));

  const birthDate = new Date(
    natalChart.birthDate.year,
    natalChart.birthDate.month - 1,
    natalChart.birthDate.day,
    natalChart.birthDate.hours,
    natalChart.birthDate.minutes
  );

  const natalPositions  = getPlanetaryPositions(birthDate);
  const transitPositions = getPlanetaryPositions(new Date());
  const allAspects       = calculateAspects(transitPositions, natalPositions);
  const significant      = getSignificantAspects(allAspects, 15);
  const insights         = generateInsights(significant);

  // Format each category into clean objects
  const format = (items) => items.slice(0, 2).map(item => ({
    transit:  `${capitalize(item.transitPlanet || '')} ${item.aspect || ''}`.trim(),
    planet:   item.transitPlanet || '',
    natal:    item.natalPlanet   || '',
    insight:  item.interpretation || '',
    action:   item.advice         || '',
    exact:    (item.exactness || 0) > 0.9,
    emoji:    item.emoji          || '✨',
  }));

  console.log(JSON.stringify({
    date:          new Date().toISOString().split('T')[0],
    totalTransits: significant.length,
    relationships: format(insights.relationships || []),
    work:          format(insights.work          || []),
    growth:        format(insights.growth        || []),
    luck:          format(insights.luck          || []),
  }));
}

function capitalize(str) {
  return str ? str.charAt(0).toUpperCase() + str.slice(1) : '';
}

dailyJson().catch(err => {
  console.log(JSON.stringify({ error: err.message }));
  process.exit(1);
});
