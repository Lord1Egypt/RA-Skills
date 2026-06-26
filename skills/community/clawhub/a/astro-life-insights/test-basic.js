// Quick test to see if swisseph works
import swisseph from 'swisseph';

console.log('Testing Swiss Ephemeris...\n');

// Set ephemeris path (will use built-in Moshier if no files)
swisseph.swe_set_ephe_path(null);

// Get today's date
const now = new Date();
const julianDay = swisseph.swe_julday(
  now.getFullYear(),
  now.getMonth() + 1,
  now.getDate(),
  now.getHours() + now.getMinutes() / 60,
  swisseph.SE_GREG_CAL
);

console.log(`Today's Julian Day: ${julianDay}\n`);

// Calculate Sun position
const sun = swisseph.swe_calc_ut(julianDay, swisseph.SE_SUN, swisseph.SEFLG_SPEED);
if (sun.flag >= 0) {
  console.log('☀️  Sun Position:');
  console.log(`   Longitude: ${sun.longitude.toFixed(2)}°`);
  console.log(`   Zodiac: ${getZodiacSign(sun.longitude)}\n`);
}

// Calculate Moon position
const moon = swisseph.swe_calc_ut(julianDay, swisseph.SE_MOON, swisseph.SEFLG_SPEED);
if (moon.flag >= 0) {
  console.log('🌙 Moon Position:');
  console.log(`   Longitude: ${moon.longitude.toFixed(2)}°`);
  console.log(`   Zodiac: ${getZodiacSign(moon.longitude)}\n`);
}

// Calculate Venus position
const venus = swisseph.swe_calc_ut(julianDay, swisseph.SE_VENUS, swisseph.SEFLG_SPEED);
if (venus.flag >= 0) {
  console.log('💕 Venus Position:');
  console.log(`   Longitude: ${venus.longitude.toFixed(2)}°`);
  console.log(`   Zodiac: ${getZodiacSign(venus.longitude)}\n`);
}

// Close Swiss Ephemeris
swisseph.swe_close();

console.log('✅ Swiss Ephemeris working!\n');

function getZodiacSign(longitude) {
  const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
  const signIndex = Math.floor(longitude / 30);
  const degree = (longitude % 30).toFixed(2);
  return `${degree}° ${signs[signIndex]}`;
}
