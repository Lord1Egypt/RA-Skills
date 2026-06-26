#!/usr/bin/env node
/**
 * Search Module
 * Fuzzy, regex, and case-insensitive search for Obsidian vault
 */

const fs = require('fs');
const path = require('path');

/**
 * Calculate Levenshtein distance between two strings
 * @param {string} a 
 * @param {string} b 
 * @returns {number}
 */
function levenshteinDistance(a, b) {
  const matrix = [];
  const lenA = a.length;
  const lenB = b.length;

  // Initialize first row and column
  for (let i = 0; i <= lenB; i++) {
    matrix[i] = [i];
  }
  for (let j = 0; j <= lenA; j++) {
    matrix[0][j] = j;
  }

  // Fill the matrix
  for (let i = 1; i <= lenB; i++) {
    for (let j = 1; j <= lenA; j++) {
      const cost = b[i - 1] === a[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,      // deletion
        matrix[i][j - 1] + 1,      // insertion
        matrix[i - 1][j - 1] + cost // substitution
      );
    }
  }

  return matrix[lenB][lenA];
}

/**
 * Calculate fuzzy match score (0-1, higher is better match)
 * @param {string} query 
 * @param {string} target 
 * @returns {number}
 */
function fuzzyScore(query, target) {
  if (!query || !target) return 0;
  
  const queryLower = query.toLowerCase();
  const targetLower = target.toLowerCase();
  
  // Exact match is best
  if (queryLower === targetLower) return 1;
  
  // Contains is very good
  if (targetLower.includes(queryLower)) return 0.9;
  
  // Calculate Levenshtein distance normalized by max length
  const distance = levenshteinDistance(queryLower, targetLower.slice(0, queryLower.length + 5));
  const maxLen = Math.max(queryLower.length, targetLower.length);
  
  if (maxLen === 0) return 0;
  
  const score = 1 - (distance / maxLen);
  return Math.max(0, score * 0.8); // Fuzzy matches cap at 0.8
}

/**
 * Find fuzzy matches in content
 * @param {string} content 
 * @param {string} query 
 * @param {number} threshold 
 * @returns {Array<{line: number, text: string, score: number}>}
 */
function findFuzzyMatches(content, query, threshold = 0.6) {
  const lines = content.split('\n');
  const matches = [];
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const words = line.split(/\s+/);
    
    // Check if any word is a fuzzy match
    for (const word of words) {
      const cleanWord = word.replace(/[^\w]/g, '');
      if (cleanWord.length > 0) {
        const score = fuzzyScore(query, cleanWord);
        if (score >= threshold) {
          matches.push({
            line: i + 1,
            text: line.trim(),
            score: score,
            matchedWord: cleanWord
          });
          break; // Only report first match per line
        }
      }
    }
    
    // Also check if the entire line contains query (substring match)
    if (line.toLowerCase().includes(query.toLowerCase())) {
      // Don't duplicate if already found via fuzzy
      if (!matches.find(m => m.line === i + 1)) {
        matches.push({
          line: i + 1,
          text: line.trim(),
          score: 0.85,
          matchedWord: query
        });
      }
    }
  }
  
  return matches.sort((a, b) => b.score - a.score);
}

/**
 * Recursively find all .md files in directory
 * @param {string} dir - Directory to search
 * @param {Array} files - Accumulator for files
 * @returns {Array<string>} Array of file paths
 */
function findMarkdownFiles(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== '.obsidian') {
      findMarkdownFiles(fullPath, files);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      files.push(fullPath);
    }
  }
  return files;
}

/**
 * Search notes with case-insensitive matching (default behavior)
 * @param {string} vaultPath 
 * @param {string} query 
 * @param {Object} options
 * @returns {{success: boolean, results: Array, error?: string}}
 */
function searchNotes(vaultPath, query, options = {}) {
  try {
    const folder = options.folder || '';
    const searchPath = path.join(vaultPath, folder);
    const caseSensitive = options.caseSensitive || false;
    
    if (!fs.existsSync(searchPath)) {
      return { success: false, results: [], error: `Search path not found: ${folder}` };
    }

    // Pure Node.js file search - no shell execution
    const files = findMarkdownFiles(searchPath);
    const searchLower = caseSensitive ? query : query.toLowerCase();
    
    const results = [];
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf8');
      const contentToSearch = caseSensitive ? content : content.toLowerCase();
      
      if (contentToSearch.includes(searchLower)) {
        results.push({
          fullPath: file,
          relativePath: path.relative(vaultPath, file),
        });
      }
    }

    return { success: true, results };
  } catch (err) {
    return { success: false, error: err.message, results: [] };
  }
}

/**
 * Search notes with fuzzy matching
 * @param {string} vaultPath 
 * @param {string} query 
 * @param {Object} options
 * @returns {{success: boolean, results: Array, error?: string}}
 */
function searchNotesFuzzy(vaultPath, query, options = {}) {
  try {
    const folder = options.folder || '';
    const searchPath = path.join(vaultPath, folder);
    const threshold = options.threshold || 0.6;
    
    if (!fs.existsSync(searchPath)) {
      return { success: false, results: [], error: `Search path not found: ${folder}` };
    }

    // Collect all markdown files
    const files = [];
    const walkDir = (dir) => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== '.obsidian') {
          walkDir(fullPath);
        } else if (entry.isFile() && entry.name.endsWith('.md')) {
          files.push(fullPath);
        }
      }
    };
    
    walkDir(searchPath);
    
    const results = [];
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf8');
      const matches = findFuzzyMatches(content, query, threshold);
      
      if (matches.length > 0) {
        // Score based on best match in file
        const bestScore = Math.max(...matches.map(m => m.score));
        const fileName = path.basename(file, '.md');
        const fileNameScore = fuzzyScore(query, fileName);
        const combinedScore = Math.max(bestScore, fileNameScore * 0.9);
        
        results.push({
          fullPath: file,
          relativePath: path.relative(vaultPath, file),
          bestScore: combinedScore,
          matches: matches.slice(0, 3), // Top 3 matches
        });
      }
    }
    
    // Sort by score descending
    results.sort((a, b) => b.bestScore - a.bestScore);
    
    return { success: true, results };
  } catch (err) {
    return { success: false, error: err.message, results: [] };
  }
}

/**
 * Search notes with regex pattern
 * @param {string} vaultPath 
 * @param {string} pattern 
 * @param {Object} options
 * @returns {{success: boolean, results: Array, error?: string}}
 */
function searchNotesRegex(vaultPath, pattern, options = {}) {
  try {
    const folder = options.folder || '';
    const searchPath = path.join(vaultPath, folder);
    const caseSensitive = options.caseSensitive || false;
    
    if (!fs.existsSync(searchPath)) {
      return { success: false, results: [], error: `Search path not found: ${folder}` };
    }

    let regex;
    try {
      const flags = caseSensitive ? 'g' : 'gi';
      regex = new RegExp(pattern, flags);
    } catch (e) {
      return { success: false, error: `Invalid regex pattern: ${e.message}`, results: [] };
    }

    // Collect all markdown files
    const files = [];
    const walkDir = (dir) => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== '.obsidian') {
          walkDir(fullPath);
        } else if (entry.isFile() && entry.name.endsWith('.md')) {
          files.push(fullPath);
        }
      }
    };
    
    walkDir(searchPath);
    
    const results = [];
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf8');
      const lines = content.split('\n');
      const matches = [];
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        regex.lastIndex = 0; // Reset regex
        const match = regex.exec(line);
        
        if (match) {
          matches.push({
            line: i + 1,
            text: line.trim(),
            match: match[0],
            index: match.index,
          });
        }
      }
      
      if (matches.length > 0) {
        results.push({
          fullPath: file,
          relativePath: path.relative(vaultPath, file),
          matchCount: matches.length,
          matches: matches, // All matches
        });
      }
    }
    
    // Sort by number of matches descending
    results.sort((a, b) => b.matchCount - a.matchCount);
    
    return { success: true, results, pattern };
  } catch (err) {
    return { success: false, error: err.message, results: [] };
  }
}

module.exports = {
  levenshteinDistance,
  fuzzyScore,
  findFuzzyMatches,
  searchNotes,
  searchNotesFuzzy,
  searchNotesRegex,
};