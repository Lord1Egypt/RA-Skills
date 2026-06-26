#!/usr/bin/env node

/**
 * Skill Orchestrator for OpenClaw
 * Discovers installed skills and recommends the best one for any task
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  skillsDir: path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw-autoclaw', 'skills'),
  threshold: parseInt(process.env.ORCHESTRATOR_THRESHOLD) || 30,
  maxResults: parseInt(process.env.ORCHESTRATOR_MAX_RESULTS) || 3,
  verbosity: 1
};

/**
 * Parse SKILL.md and extract metadata
 */
function parseSkillMarkdown(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);

  let metadata = {
    name: '',
    description: '',
    usage: [],
    triggers: []
  };

  if (frontmatterMatch) {
    const frontmatter = frontmatterMatch[1];
    const lines = frontmatter.split('\n');

    for (const line of lines) {
      const [key, ...valueParts] = line.split(':');
      if (key && valueParts.length) {
        const value = valueParts.join(':').trim().replace(/^"|"$/g, '');
        switch (key.trim()) {
          case 'name':
            metadata.name = value;
            break;
          case 'description':
            metadata.description = value;
            break;
        }
      }
    }

    // Extract triggers from Usage or When to Use sections
    const sections = ['## Usage', '## When to Use', '## Examples'];
    let triggers = [];

    for (const section of sections) {
      const regex = new RegExp(section + '\\n([\\s\\S]*?)(\\n##|$)');
      const match = content.match(regex);
      if (match) {
        const sectionText = match[1];
        // Extract command examples from bold quotes `"command"` or code blocks `command`
        const commandMatches = sectionText.match(/\*\*"([^"]+)"\*\*|`([^`]+)`/g);
        if (commandMatches) {
          const found = commandMatches
            .map(m => m.replace(/\*\*|`/g, '').trim())
            .filter(t => t);
          triggers.push(...found);
        }
      }
    }

    // Deduplicate and store
    if (triggers.length > 0) {
      metadata.triggers = [...new Set(triggers)];
    }
  }

  return metadata;
}

/**
 * Scan skills directory and build skill profiles
 */
function discoverSkills() {
  const skills = [];

  if (!fs.existsSync(CONFIG.skillsDir)) {
    throw new Error(`Skills directory not found: ${CONFIG.skillsDir}`);
  }

  const skillFolders = fs.readdirSync(CONFIG.skillsDir, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);

  for (const skillName of skillFolders) {
    const skillPath = path.join(CONFIG.skillsDir, skillName);
    const skillMD = path.join(skillPath, 'SKILL.md');

    if (fs.existsSync(skillMD)) {
      try {
        const metadata = parseSkillMarkdown(skillMD);
        if (metadata.name && metadata.description) {
          skills.push({
            folder: skillName,
            name: metadata.name,
            description: metadata.description,
            triggers: metadata.triggers,
            path: skillPath
          });
        }
      } catch (err) {
        if (CONFIG.verbosity >= 2) {
          console.error(`Warning: Failed to parse ${skillName}: ${err.message}`);
        }
      }
    }
  }

  return skills;
}

/**
 * Compute similarity score between query and skill (0-100)
 * Uses Jaccard-like word overlap + bonuses
 */
function computeScore(query, skill) {
  const queryLower = query.toLowerCase();
  // Extract meaningful words (3+ chars, ignore common stopwords optionally)
  const queryWords = queryLower.match(/\b[a-z]{3,}\b/g) || [];

  if (queryWords.length === 0) return 0;

  const skillText = (skill.name + ' ' + skill.description).toLowerCase();
  let matches = 0;

  for (const word of queryWords) {
    if (skillText.includes(word)) matches++;
  }

  // Base score: percentage of query words matched
  let score = Math.round((matches / queryWords.length) * 100);

  // Bonus: exact trigger phrase match
  for (const trigger of skill.triggers) {
    const triggerLower = trigger.toLowerCase();
    if (queryLower.includes(triggerLower)) {
      score += 30; // strong boost
      break;
    }
  }

  // Bonus: if all query words matched, add extra boost
  if (matches === queryWords.length) {
    score += 10;
  }

  return Math.min(score, 100); // cap at 100
}

/**
 * Match query to skills and return ranked results
 */
function matchSkills(query, allSkills) {
  const scored = allSkills.map(skill => ({
    ...skill,
    score: computeScore(query, skill)
  }));

  // Filter by threshold
  const filtered = scored.filter(s => s.score >= CONFIG.threshold);

  // Sort by score descending
  filtered.sort((a, b) => b.score - a.score);

  // Return top N
  return filtered.slice(0, CONFIG.maxResults);
}

/**
 * Format recommendation output
 */
function formatOutput(matches, originalQuery) {
  if (matches.length === 0) {
    return `❌ No suitable skill found for: "${originalQuery}"\n\nTry rephrasing your request or check if relevant skills are installed.`;
  }

  let output = `🎯 Best match: ${matches[0].name} (Score: ${matches[0].score}%)\n`;
  output += `   ↳ ${matches[0].description}\n`;
  if (matches[0].triggers.length > 0) {
    output += `   Commands: ${matches[0].triggers.slice(0, 3).join(', ')}\n`;
  }
  output += '\n';

  if (matches.length > 1) {
    output += '🔹 Also consider:\n';
    for (let i = 1; i < matches.length; i++) {
      output += `\n${i}. ${matches[i].name} (Score: ${matches[i].score}%)\n`;
      output += `   ↳ ${matches[i].description}\n`;
      if (matches[i].triggers.length > 0) {
        output += `   Commands: ${matches[i].triggers.slice(0, 2).join(', ')}\n`;
      }
    }
  }

  output += '\n👉 Reply "use ' + matches[0].name.split(' ')[0].toLowerCase() + '" to proceed, or specify another skill name.';
  return output;
}

/**
 * Main orchestrator function
 */
function orchestrate(query) {
  try {
    const allSkills = discoverSkills();

    if (allSkills.length === 0) {
      return '❌ No skills found. Install some skills first in ~/.openclaw-autoclaw/skills/';
    }

    // DEBUG: print some info
    if (process.env.DEBUG) {
      console.error(`DEBUG: Total skills: ${allSkills.length}`);
      console.error('Available skills (first 10):', allSkills.slice(0,10).map(s => s.name).join(', '));
    }

    // Compute scores for all
    const scored = allSkills.map(skill => {
      const score = computeScore(query, skill);
      return { ...skill, score };
    });

    if (process.env.DEBUG) {
      // Show top 10 raw scores
      const sorted = [...scored].sort((a,b) => b.score - a.score);
      console.error('Top 10 raw scores:');
      sorted.slice(0,10).forEach(s => console.error(`  ${s.name}: ${s.score}`));
    }

    const matches = matchSkills(query, allSkills);

    if (matches.length === 0) {
      return `❌ No suitable skill found for: "${query}"\n\nTry rephrasing your request or check if relevant skills are installed.`;
    }

    return formatOutput(matches, query);
  } catch (err) {
    return `❌ Error: ${err.message}`;
  }
}

// OpenClaw skill entry point (text = user's message)
function main(text) {
  // Extract query after common trigger phrases
  const query = text
    .replace(/^(use skill orchestrator to|orchestrate:|orchestrate|what skill should i use for|recommend a skill for|which skill for)\s*/i, '')
    .trim();

  if (!query) {
    return `Skill Orchestrator 🤖

Describe what you want to do and I'll recommend the best skill.

Examples:
• "create a powerpoint from sales data"
• "research competitors in AI"
• "take a screenshot of a website"
• "extract text from PDF"

Just say: "orchestrate: [your task]"`;
  }

  return orchestrate(query);
}

// CLI Interface (for testing)
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log(`
Skill Orchestrator v1.0.0

Usage:
  node index.js "your task description"
  OR
  echo "your task" | node index.js

Examples:
  node index.js "create a powerpoint from data"
  node index.js "research AI trends"
  node index.js "take a screenshot"
`);
    process.exit(0);
  }

  const query = args.join(' ');
  const result = main(query);
  console.log(result);
}

module.exports = { main, orchestrate, discoverSkills, matchSkills };