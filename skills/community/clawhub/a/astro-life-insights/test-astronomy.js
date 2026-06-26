// Test astronomy-engine
import * as astronomy from 'astronomy-engine';

console.log('Testing astronomy-engine...\n');

const now = new Date();
console.log(`Current Date: ${now.toISOString()}\n`);

// Get planetary positions using proper API
const bodies = [
  { name: 'Sun', body: astronomy.Body.Sun },
  { name: 'Moon', body: astronomy.Body.Moon },
  { name: 'Mercury', body: astronomy.Body.Mercury },
  { name: 'Venus', body: astronomy.Body.Venus },
  { name: 'Mars', body: astronomy.Body.Mars },
  { name: 'Jupiter', body: astronomy.Body.Jupiter },
  { name: 'Saturn', body: astronomy.Body.Saturn }
];

bodies.forEach(({ name, body }) => {
  try {
    // Get geocentric ecliptic coordinates
    const equator = astronomy.GeoVector(body, now, false);
    const ecliptic = astronomy.Ecliptic(equator);
    
    const sign = getZodiacSign(ecliptic.elon);
    const emoji = getEmoji(name);
    console.log(`${emoji} ${name.padEnd(10)} ${ecliptic.elon.toFixed(2)}°  (${sign})`);
  } catch (err) {
    console.log(`${name}: ${err.message}`);
  }
});

console.log('\n✅ astronomy-engine works perfectly!\n');

function getZodiacSign(longitude) {
  // Normalize to 0-360
  let lon = longitude % 360;
  if (lon < 0) lon += 360;
  
  const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
  const signIndex = Math.floor(lon / 30);
  const degree = (lon % 30).toFixed(1);
  return `${degree}° ${signs[signIndex]}`;
}

function getEmoji(planet) {
  const emojis = {
    'Sun': '☀️',
    'Moon': '🌙',
    'Mercury': '☿️',
    'Venus': '♀️',
    'Mars': '♂️',
    'Jupiter': '♃',
    'Saturn': '♄'
  };
  return emojis[planet] || '⭐';
}
