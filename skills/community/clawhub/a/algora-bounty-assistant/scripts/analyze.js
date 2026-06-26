#!/usr/bin/env node

/**
 * Algora Bounty Assistant
 * Analyze GitHub bounties for potential value
 */

const https = require('https');

const PER_PAGE = 20;

function analyzeBounty(issue) {
  // Analyze the issue title and description for potential value
  const title = issue.title.toLowerCase();
  const body = (issue.body || '').toLowerCase();
  
  // Check for high-value indicators
  const valueIndicators = [
    'bug',
    'security',
    'performance',
    'feature',
    'api',
    'integration'
  ];
  
  let valueScore = 0;
  valueIndicators.forEach(indicator => {
    if (title.includes(indicator) || body.includes(indicator)) {
      valueScore++;
    }
  });
  
  // Check for complexity indicators
  const complexityIndicators = [
    'beginner',
    'easy',
    'simple',
    'intermediate',
    'advanced',
    'complex'
  ];
  
  let complexity = 'Unknown';
  complexityIndicators.forEach(indicator => {
    if (title.includes(indicator) || body.includes(indicator)) {
      complexity = indicator.charAt(0).toUpperCase() + indicator.slice(1);
    }
  });
  
  return {
    title: issue.title,
    url: issue.html_url,
    comments: issue.comments,
    valueScore,
    complexity,
    created: issue.created_at
  };
}

function generateAnalysisReport(analyzedBounties) {
  console.log('=========================================');
  console.log('  Algora Bounty Assistant - Analysis');
  console.log('=========================================');
  console.log('');
  console.log(`Analyzed ${analyzedBounties.length} bounties:`);
  console.log('');
  
  // Sort by value score (highest first)
  analyzedBounties.sort((a, b) => b.valueScore - a.valueScore);
  
  analyzedBounties.forEach(bounty => {
    console.log(`👉 ${bounty.title}`);
    console.log(`   URL: \`${bounty.url}\` `);
    console.log(`   💬 Comments: ${bounty.comments} | 💰 Value Score: ${bounty.valueScore} | 📊 Complexity: ${bounty.complexity}`);
    console.log(`   📅 Created: ${new Date(bounty.created).toLocaleDateString()}`);
    console.log('');
  });
}

function analyzeBounties() {
  const query = 'label:bounty state:open';
  const url = `https://api.github.com/search/issues?q=${encodeURIComponent(query)}&per_page=${PER_PAGE}`;
  
  const options = {
    headers: {
      'User-Agent': 'Algora-Bounty-Assistant/1.0.0',
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
        
        const analyzedBounties = issues.map(analyzeBounty);
        generateAnalysisReport(analyzedBounties);
      } catch (error) {
        console.error('Error parsing response:', error);
      }
    });
  }).on('error', (error) => {
    console.error('Error making request:', error);
  });
}

// Run the analysis
analyzeBounties();
