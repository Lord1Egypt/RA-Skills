// Interpret aspects and generate insights
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load interpretation databases
const interpretations = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'data', 'interpretations.json'), 'utf8')
);

const lifeAreas = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'data', 'life-areas.json'), 'utf8')
);

/**
 * Generate insights from aspects
 */
export function generateInsights(aspects) {
  const insights = {
    relationships: [],
    work: [],
    growth: [],
    luck: []
  };
  
  aspects.forEach(aspect => {
    const { transitPlanet, natalPlanet, aspect: aspectType, exactness } = aspect;
    
    // Get interpretation for this transit planet
    const planetInterpretations = interpretations.transits[transitPlanet];
    
    if (!planetInterpretations) return;
    
    // Check which life areas this transit affects
    Object.keys(lifeAreas).forEach(area => {
      const areaInfo = lifeAreas[area];
      
      // Does this planet influence this life area?
      if (areaInfo.planets.includes(transitPlanet) || areaInfo.planets.includes(natalPlanet)) {
        const interpretation = planetInterpretations[area]?.[aspectType];
        const advice = planetInterpretations.advice?.[aspectType];
        
        if (interpretation) {
          insights[area].push({
            transitPlanet,
            natalPlanet,
            aspect: aspectType,
            exactness,
            interpretation,
            advice,
            emoji: getLifeAreaEmoji(area)
          });
        }
      }
    });
  });
  
  return insights;
}

/**
 * Format insights for display
 */
export function formatInsights(insights, date = new Date()) {
  const lines = [];
  
  lines.push(`✨ Your Astrological Weather - ${date.toLocaleDateString('en-US', { 
    month: 'long', 
    day: 'numeric', 
    year: 'numeric' 
  })}\n`);
  
  // Relationships
  if (insights.relationships.length > 0) {
    lines.push('💕 RELATIONSHIPS');
    insights.relationships.slice(0, 2).forEach(insight => {
      lines.push(formatInsight(insight));
    });
    lines.push('');
  }
  
  // Work
  if (insights.work.length > 0) {
    lines.push('💼 WORK');
    insights.work.slice(0, 2).forEach(insight => {
      lines.push(formatInsight(insight));
    });
    lines.push('');
  }
  
  // Personal Growth
  if (insights.growth.length > 0) {
    lines.push('🌱 PERSONAL GROWTH');
    insights.growth.slice(0, 2).forEach(insight => {
      lines.push(formatInsight(insight));
    });
    lines.push('');
  }
  
  // Luck
  if (insights.luck.length > 0) {
    lines.push('🍀 LUCK');
    insights.luck.slice(0, 2).forEach(insight => {
      lines.push(formatInsight(insight));
    });
    lines.push('');
  }
  
  // Overall summary
  const totalInsights = Object.values(insights).flat().length;
  if (totalInsights > 0) {
    lines.push(`✨ ${totalInsights} active transits supporting your journey today!`);
  } else {
    lines.push('✨ A quiet day cosmically - perfect for rest and integration.');
  }
  
  return lines.join('\n');
}

/**
 * Format a single insight
 */
function formatInsight(insight) {
  const { transitPlanet, aspect, interpretation, advice, exactness } = insight;
  
  const exactnessTag = exactness > 0.8 ? ' (exact!)' : '';
  const aspectName = aspect.charAt(0).toUpperCase() + aspect.slice(1);
  
  let output = `${capitalize(transitPlanet)} ${aspect}${exactnessTag}\n`;
  output += `→ ${interpretation}\n`;
  
  if (advice) {
    output += `→ Action: ${advice}`;
  }
  
  return output;
}

/**
 * Get emoji for life area
 */
function getLifeAreaEmoji(area) {
  const emojis = {
    relationships: '💕',
    work: '💼',
    growth: '🌱',
    luck: '🍀'
  };
  return emojis[area] || '✨';
}

/**
 * Capitalize first letter
 */
function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}
