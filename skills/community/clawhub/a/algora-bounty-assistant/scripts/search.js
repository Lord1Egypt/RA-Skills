#!/usr/bin/env node

/**
 * GitHub Bounty Hunter
 * Search for low-competition open bounties on GitHub
 */

const https = require('https');

const MAX_COMMENTS = process.argv[2] ? parseInt(process.argv[2], 10) : 5;
const PER_PAGE = 20;

const query = `label:bounty state:open comments:<=${MAX_COMMENTS}`;
const url = `https://api.github.com/search/issues?q=${encodeURIComponent(query)}&per_page=${PER_PAGE}`;

function estimateDifficulty(title) {
  const lower = title.toLowerCase();
  if (lower.includes('beginner') || lower.includes('tier 1') || lower.includes('faq') || lower.includes('page') || lower.includes('add')) {
    return 'Beginner';
  }
  if (lower.includes('intermediate') || lower.includes('tier 2') || lower.includes('feature') || lower.includes('system')) {
    return 'Intermediate';
  }
  if (lower.includes('advanced') || lower.includes('tier 3') || lower.includes('security') || lower.includes('architecture')) {
    return 'Advanced';
  }
  return 'Unknown';
}

function generateReport(issues) {
  console.log('=========================================');
  console.log('  GitHub Bounty Hunter - Search Results');
  console.log('=========================================');
  console.log('');
  console.log(`Found ${issues.length} low-competition bounties:`);
  console.log('');
  
  issues.forEach(issue => {
    console.log(`👉 ${issue.title}`);
    console.log(`   URL: \`${issue.html_url}\` `);
    console.log(`   💬 Comments: ${issue.comments} | 💪 Difficulty: ${estimateDifficulty(issue.title)}`);
    console.log('');
  });
}

function searchBounties() {
  const options = {
    headers: {
      'User-Agent': 'GitHub-Bounty-Hunter/1.0.0',
      'Accept': 'application/vnd.github.v3+json'
    }
  };

  https.get(url, options, (res) => {
    let data = '';
    
    res.on('data', (chunk) => {
      data += chunk;
    });
    
    res.on('end', () => {
      try {
        const response = JSON.parse(data);
        const issues = response.items || [];
        
        // Sort by comment count (least first)
        issues.sort((a, b) => a.comments - b.comments);
        
        generateReport(issues);
      } catch (error) {
        console.error('Error parsing response:', error);
      }
    });
  }).on('error', (error) => {
    console.error('Error making request:', error);
  });
}

// Run the search
searchBounties();