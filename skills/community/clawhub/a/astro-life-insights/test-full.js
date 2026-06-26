// Test the full system with sample data
import { getPlanetaryPositions, calculateAspects, getSignificantAspects } from './calculate.js';
import { generateInsights, formatInsights } from './interpret.js';

console.log('Testing astro-life-insights system...\n');

// Sample natal chart (August 16, 1987, noon)
const birthDate = new Date(1987, 7, 16, 12, 0);
console.log(`Sample birth date: ${birthDate.toLocaleDateString()}\n`);

// Calculate natal positions
console.log('Calculating natal positions...');
const natalPositions = getPlanetaryPositions(birthDate);
console.log(`✅ ${Object.keys(natalPositions).length} natal planets calculated\n`);

// Get current transits
const now = new Date();
console.log('Calculating current transits...');
const transitPositions = getPlanetaryPositions(now);
console.log(`✅ ${Object.keys(transitPositions).length} transit planets calculated\n`);

// Find aspects
console.log('Finding aspects...');
const allAspects = calculateAspects(transitPositions, natalPositions);
console.log(`✅ Found ${allAspects.length} total aspects\n`);

const significantAspects = getSignificantAspects(allAspects, 15);
console.log(`✅ ${significantAspects.length} significant aspects identified\n`);

// Generate insights
console.log('Generating insights...');
const insights = generateInsights(significantAspects);
const insightCount = Object.values(insights).flat().length;
console.log(`✅ Generated ${insightCount} life-area insights\n`);

// Format output
console.log('='
.repeat(60));
console.log(formatInsights(insights, now));
console.log('='.repeat(60));

console.log('\n✅ Full system test complete!\n');
