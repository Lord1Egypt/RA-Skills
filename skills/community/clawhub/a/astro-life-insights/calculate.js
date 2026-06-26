// Calculate planetary positions and aspects
import * as astronomy from 'astronomy-engine';

// Planet list
const PLANETS = [
  { name: 'sun', body: astronomy.Body.Sun, emoji: '☀️' },
  { name: 'moon', body: astronomy.Body.Moon, emoji: '🌙' },
  { name: 'mercury', body: astronomy.Body.Mercury, emoji: '☿️' },
  { name: 'venus', body: astronomy.Body.Venus, emoji: '♀️' },
  { name: 'mars', body: astronomy.Body.Mars, emoji: '♂️' },
  { name: 'jupiter', body: astronomy.Body.Jupiter, emoji: '♃' },
  { name: 'saturn', body: astronomy.Body.Saturn, emoji: '♄' },
  { name: 'uranus', body: astronomy.Body.Uranus, emoji: '♅' },
  { name: 'neptune', body: astronomy.Body.Neptune, emoji: '♆' },
  { name: 'pluto', body: astronomy.Body.Pluto, emoji: '♇' }
];

// Aspect definitions
const ASPECTS = [
  { name: 'conjunction', angle: 0, orb: 8 },
  { name: 'sextile', angle: 60, orb: 4 },
  { name: 'square', angle: 90, orb: 6 },
  { name: 'trine', angle: 120, orb: 6 },
  { name: 'opposition', angle: 180, orb: 6 }
];

/**
 * Get planetary positions for a given date
 */
export function getPlanetaryPositions(date = new Date()) {
  const positions = {};
  
  PLANETS.forEach(({ name, body, emoji }) => {
    try {
      const equator = astronomy.GeoVector(body, date, false);
      const ecliptic = astronomy.Ecliptic(equator);
      
      positions[name] = {
        longitude: ecliptic.elon,
        latitude: ecliptic.elat,
        emoji,
        sign: getZodiacSign(ecliptic.elon)
      };
    } catch (err) {
      console.error(`Error calculating ${name}:`, err.message);
    }
  });
  
  return positions;
}

/**
 * Calculate aspects between current transits and natal positions
 */
export function calculateAspects(transitPositions, natalPositions) {
  const aspects = [];
  
  Object.keys(transitPositions).forEach(transitPlanet => {
    Object.keys(natalPositions).forEach(natalPlanet => {
      const transitLon = transitPositions[transitPlanet].longitude;
      const natalLon = natalPositions[natalPlanet].longitude;
      
      const aspect = findAspect(transitLon, natalLon);
      
      if (aspect) {
        aspects.push({
          transitPlanet,
          natalPlanet,
          aspect: aspect.name,
          orb: aspect.actualOrb,
          exactness: 1 - (Math.abs(aspect.actualOrb) / aspect.allowedOrb) // 0-1, 1 = exact
        });
      }
    });
  });
  
  // Sort by exactness (most exact first)
  aspects.sort((a, b) => b.exactness - a.exactness);
  
  return aspects;
}

/**
 * Find if two longitudes form an aspect
 */
function findAspect(lon1, lon2) {
  // Calculate the angular distance
  let diff = Math.abs(lon1 - lon2);
  
  // Normalize to 0-180
  if (diff > 180) diff = 360 - diff;
  
  // Check each aspect
  for (const aspect of ASPECTS) {
    const deviation = Math.abs(diff - aspect.angle);
    
    if (deviation <= aspect.orb) {
      return {
        name: aspect.name,
        actualOrb: deviation,
        allowedOrb: aspect.orb
      };
    }
  }
  
  return null;
}

/**
 * Get zodiac sign from longitude
 */
function getZodiacSign(longitude) {
  let lon = longitude % 360;
  if (lon < 0) lon += 360;
  
  const signs = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
  ];
  
  const signIndex = Math.floor(lon / 30);
  const degree = (lon % 30).toFixed(1);
  
  return `${degree}° ${signs[signIndex]}`;
}

/**
 * Filter aspects by importance (slow planets = more important)
 */
export function getSignificantAspects(aspects, limit = 10) {
  // Weight aspects by planet speed (slower = more important)
  const planetWeights = {
    pluto: 10,
    neptune: 9,
    uranus: 8,
    saturn: 7,
    jupiter: 6,
    mars: 4,
    venus: 3,
    mercury: 2,
    sun: 5,
    moon: 3
  };
  
  return aspects
    .map(aspect => ({
      ...aspect,
      importance: (planetWeights[aspect.transitPlanet] || 1) * aspect.exactness
    }))
    .sort((a, b) => b.importance - a.importance)
    .slice(0, limit);
}
