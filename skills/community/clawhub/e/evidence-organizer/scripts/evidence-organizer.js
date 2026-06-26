#!/usr/bin/env node
/**
 * Evidence Organizer
 * 
 * Organizes and structures evidence for legal proceedings.
 * This is an organizational assistance tool and does not constitute legal advice.
 */

const EVIDENCE_CATEGORIES = {
  'documentary': {
    name: 'Documentary Evidence',
    description: 'Written documents and records',
    examples: ['Contracts', 'Emails', 'Letters', 'Invoices', 'Financial records', 'Reports'],
    authentication: 'May require witness testimony or business records certification'
  },
  'testimonial': {
    name: 'Testimonial Evidence',
    description: 'Witness testimony',
    examples: ['Witness statements', 'Deposition transcripts', 'Affidavits', 'Expert reports'],
    authentication: 'Witness must be competent and testify under oath'
  },
  'physical': {
    name: 'Physical Evidence',
    description: 'Tangible objects',
    examples: ['Photographs', 'Videos', 'Audio recordings', 'Physical objects', 'Digital files'],
    authentication: 'Chain of custody documentation required'
  },
  'demonstrative': {
    name: 'Demonstrative Evidence',
    description: 'Visual aids to help explain evidence',
    examples: ['Charts', 'Graphs', 'Timelines', 'Maps', 'Diagrams', 'Summaries'],
    authentication: 'Must accurately represent underlying evidence'
  }
};

const RELEVANCE_LEVELS = {
  'critical': { label: 'Critical', description: 'Essential to proving/disproving key elements', priority: 1 },
  'important': { label: 'Important', description: 'Supports main claims or defenses', priority: 2 },
  'supporting': { label: 'Supporting', description: 'Provides context or corroboration', priority: 3 },
  'background': { label: 'Background', description: 'General context information', priority: 4 }
};

/**
 * Organize evidence for legal proceedings
 * @param {Object} evidenceData - Evidence information
 * @returns {Object} Organized evidence structure
 */
function organizeEvidence(evidenceData) {
  if (!evidenceData || typeof evidenceData !== 'object') {
    return {
      error: 'Invalid input: evidence data is required',
      organization: null
    };
  }

  const {
    items = [],
    caseType = '',
    claims = [],
    organization = 'by-category'
  } = evidenceData;

  if (!items || items.length === 0) {
    return {
      error: 'At least one evidence item is required',
      organization: null
    };
  }

  // Process and categorize each item
  const processedItems = items.map((item, index) => processEvidenceItem(item, index + 1));

  // Organize based on requested method
  let organized;
  switch (organization) {
    case 'by-category':
      organized = organizeByCategory(processedItems);
      break;
    case 'by-claim':
      organized = organizeByClaim(processedItems, claims);
      break;
    case 'by-chronology':
      organized = organizeByChronology(processedItems);
      break;
    case 'by-witness':
      organized = organizeByWitness(processedItems);
      break;
    default:
      organized = organizeByCategory(processedItems);
  }

  // Generate summary and analysis
  const summary = generateSummary(processedItems, organized);
  const gaps = identifyGaps(processedItems, claims);
  const checklist = generateChecklist(processedItems);

  return {
    organization: organized,
    summary,
    gaps,
    checklist,
    nextSteps: [
      'Review evidence organization with attorney',
      'Verify chain of custody for physical evidence',
      'Prepare exhibit labels and markings',
      'Create copies for court and opposing party',
      'Prepare witness testimony about evidence',
      'Check authentication requirements',
      'Review privilege and admissibility issues'
    ],
    disclaimer: 'This tool provides organizational assistance only. It does not constitute legal advice, nor does it guarantee evidence admissibility. Always consult a qualified attorney regarding evidence rules and admissibility requirements.'
  };
}

function processEvidenceItem(item, number) {
  const category = item.category || 'documentary';
  const relevance = item.relevance || 'supporting';
  
  return {
    number,
    description: item.description || '[DESCRIPTION NEEDED]',
    category,
    categoryName: EVIDENCE_CATEGORIES[category]?.name || 'Other',
    date: item.date || '[DATE UNKNOWN]',
    source: item.source || '[SOURCE UNKNOWN]',
    relevance,
    relevanceLabel: RELEVANCE_LEVELS[relevance]?.label || 'Supporting',
    priority: RELEVANCE_LEVELS[relevance]?.priority || 3,
    claims: item.claims || [],
    witness: item.witness || '',
    location: item.location || '',
    status: item.status || 'available',
    notes: item.notes || ''
  };
}

function organizeByCategory(items) {
  const categories = {};
  
  Object.keys(EVIDENCE_CATEGORIES).forEach(key => {
    categories[key] = {
      name: EVIDENCE_CATEGORIES[key].name,
      description: EVIDENCE_CATEGORIES[key].description,
      authentication: EVIDENCE_CATEGORIES[key].authentication,
      items: []
    };
  });
  
  items.forEach(item => {
    if (categories[item.category]) {
      categories[item.category].items.push(item);
    } else {
      categories['documentary'].items.push(item);
    }
  });
  
  // Remove empty categories
  Object.keys(categories).forEach(key => {
    if (categories[key].items.length === 0) {
      delete categories[key];
    }
  });
  
  return { method: 'by-category', categories };
}

function organizeByClaim(items, claims) {
  const byClaim = {};
  
  // Initialize with provided claims
  claims.forEach(claim => {
    byClaim[claim] = {
      name: claim,
      items: []
    };
  });
  
  // Add general category
  byClaim['general'] = { name: 'General/Background', items: [] };
  
  items.forEach(item => {
    let assigned = false;
    if (item.claims && item.claims.length > 0) {
      item.claims.forEach(claim => {
        if (byClaim[claim]) {
          byClaim[claim].items.push(item);
          assigned = true;
        }
      });
    }
    if (!assigned) {
      byClaim['general'].items.push(item);
    }
  });
  
  // Remove empty categories
  Object.keys(byClaim).forEach(key => {
    if (byClaim[key].items.length === 0) {
      delete byClaim[key];
    }
  });
  
  return { method: 'by-claim', claims: byClaim };
}

function organizeByChronology(items) {
  const sorted = [...items].sort((a, b) => {
    if (a.date === '[DATE UNKNOWN]') return 1;
    if (b.date === '[DATE UNKNOWN]') return -1;
    return new Date(a.date) - new Date(b.date);
  });
  
  return { method: 'by-chronology', items: sorted };
}

function organizeByWitness(items) {
  const byWitness = {};
  
  items.forEach(item => {
    const witness = item.witness || 'No Witness Specified';
    if (!byWitness[witness]) {
      byWitness[witness] = {
        witness,
        items: []
      };
    }
    byWitness[witness].items.push(item);
  });
  
  return { method: 'by-witness', witnesses: byWitness };
}

function generateSummary(items, organized) {
  const totalItems = items.length;
  const criticalItems = items.filter(i => i.relevance === 'critical').length;
  const importantItems = items.filter(i => i.relevance === 'important').length;
  const missingItems = items.filter(i => i.status === 'missing').length;
  
  const byCategory = {};
  Object.keys(EVIDENCE_CATEGORIES).forEach(key => {
    const count = items.filter(i => i.category === key).length;
    if (count > 0) {
      byCategory[EVIDENCE_CATEGORIES[key].name] = count;
    }
  });
  
  return {
    totalItems,
    criticalItems,
    importantItems,
    supportingItems: totalItems - criticalItems - importantItems,
    missingItems,
    byCategory,
    organizationMethod: organized.method
  };
}

function identifyGaps(items, claims) {
  const gaps = [];
  
  // Check for missing dates
  const itemsWithoutDates = items.filter(i => i.date === '[DATE UNKNOWN]');
  if (itemsWithoutDates.length > 0) {
    gaps.push({
      type: 'missing-dates',
      description: itemsWithoutDates.length + ' item(s) missing dates',
      items: itemsWithoutDates.map(i => i.number)
    });
  }
  
  // Check for missing sources
  const itemsWithoutSources = items.filter(i => i.source === '[SOURCE UNKNOWN]');
  if (itemsWithoutSources.length > 0) {
    gaps.push({
      type: 'missing-sources',
      description: itemsWithoutSources.length + ' item(s) missing source information',
      items: itemsWithoutSources.map(i => i.number)
    });
  }
  
  // Check for missing descriptions
  const itemsWithoutDescriptions = items.filter(i => i.description === '[DESCRIPTION NEEDED]');
  if (itemsWithoutDescriptions.length > 0) {
    gaps.push({
      type: 'missing-descriptions',
      description: itemsWithoutDescriptions.length + ' item(s) need descriptions',
      items: itemsWithoutDescriptions.map(i => i.number)
    });
  }
  
  // Check for items not assigned to any claim
  if (claims.length > 0) {
    const unassignedItems = items.filter(i => !i.claims || i.claims.length === 0);
    if (unassignedItems.length > 0) {
      gaps.push({
        type: 'unassigned-items',
        description: unassignedItems.length + ' item(s) not assigned to any claim',
        items: unassignedItems.map(i => i.number)
      });
    }
  }
  
  // Check for missing items
  const missingItems = items.filter(i => i.status === 'missing');
  if (missingItems.length > 0) {
    gaps.push({
      type: 'missing-items',
      description: missingItems.length + ' item(s) marked as missing',
      items: missingItems.map(i => ({ number: i.number, description: i.description }))
    });
  }
  
  return gaps;
}

function generateChecklist(items) {
  return [
    'All evidence items catalogued and numbered',
    'Each item has description and date (if known)',
    'Source identified for each item',
    'Relevance level assessed',
    'Chain of custody documented (physical evidence)',
    'Authentication requirements identified',
    'Copies prepared for court and opposing party',
    'Exhibit labels/markings prepared',
    'Witness testimony prepared',
    'Privilege review completed',
    'Admissibility issues identified',
    'Backup copies stored securely'
  ];
}

/**
 * Format evidence organization for display
 * @param {Object} result - Organization result
 * @returns {string} Formatted output
 */
function formatEvidence(result) {
  if (result.error) {
    return 'Error: ' + result.error;
  }

  let output = '=== EVIDENCE ORGANIZATION ===\n\n';
  
  // Summary
  const s = result.summary;
  output += '--- SUMMARY ---\n';
  output += 'Total Items: ' + s.totalItems + '\n';
  output += 'Critical: ' + s.criticalItems + ' | Important: ' + s.importantItems + ' | Supporting: ' + s.supportingItems + '\n';
  output += 'Missing: ' + s.missingItems + '\n';
  output += 'Organization Method: ' + s.organizationMethod + '\n\n';
  
  output += 'By Category:\n';
  Object.keys(s.byCategory).forEach(cat => {
    output += '  - ' + cat + ': ' + s.byCategory[cat] + '\n';
  });
  output += '\n';
  
  // Organized items
  const org = result.organization;
  output += '--- ORGANIZED EVIDENCE ---\n\n';
  
  if (org.method === 'by-category') {
    Object.keys(org.categories).forEach(key => {
      const cat = org.categories[key];
      output += '[' + cat.name + ']\n';
      output += 'Authentication: ' + cat.authentication + '\n';
      cat.items.forEach(item => {
        output += '  #' + item.number + ' [' + item.relevanceLabel + '] ' + item.description + '\n';
        output += '      Date: ' + item.date + ' | Source: ' + item.source + '\n';
        if (item.notes) output += '      Notes: ' + item.notes + '\n';
      });
      output += '\n';
    });
  } else if (org.method === 'by-chronology') {
    org.items.forEach(item => {
      output += '#' + item.number + ' [' + item.date + '] ' + item.description + '\n';
      output += '    Category: ' + item.categoryName + ' | Relevance: ' + item.relevanceLabel + '\n';
      output += '    Source: ' + item.source + '\n\n';
    });
  }
  
  // Gaps
  if (result.gaps.length > 0) {
    output += '--- IDENTIFIED GAPS ---\n';
    result.gaps.forEach(gap => {
      output += '• ' + gap.description + '\n';
    });
    output += '\n';
  }
  
  // Checklist
  output += '--- PREPARATION CHECKLIST ---\n';
  result.checklist.forEach(item => {
    output += '[ ] ' + item + '\n';
  });
  output += '\n';
  
  // Next steps
  output += '--- NEXT STEPS ---\n';
  result.nextSteps.forEach((step, index) => {
    output += (index + 1) + '. ' + step + '\n';
  });
  output += '\n';
  
  // Disclaimer
  output += '=== DISCLAIMER ===\n';
  output += result.disclaimer + '\n';
  
  return output;
}

// Export for use as module
module.exports = { organizeEvidence, formatEvidence, EVIDENCE_CATEGORIES, RELEVANCE_LEVELS };

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    console.log('Usage: node evidence-organizer.js --example');
    console.log('   or: node evidence-organizer.js --test');
    process.exit(0);
  }

  if (args[0] === '--test') {
    const test = require('../test.js');
    test.runTests();
    process.exit(0);
  }

  if (args[0] === '--example') {
    const exampleData = {
      items: [
        { description: 'Service Agreement', category: 'documentary', date: '2024-01-15', source: 'Plaintiff files', relevance: 'critical', claims: ['breach-of-contract'] },
        { description: 'Invoice #1234', category: 'documentary', date: '2024-02-01', source: 'Accounting', relevance: 'critical', claims: ['breach-of-contract'] },
        { description: 'Email correspondence', category: 'documentary', date: '2024-02-10', source: 'Email archive', relevance: 'important', claims: ['breach-of-contract'] },
        { description: 'Photographs of work completed', category: 'physical', date: '2024-01-30', source: 'Plaintiff', relevance: 'supporting', witness: 'John Doe' }
      ],
      claims: ['breach-of-contract'],
      organization: 'by-category'
    };
    
    const result = organizeEvidence(exampleData);
    console.log(formatEvidence(result));
    process.exit(0);
  }

  console.log('Use --example to see a sample evidence organization');
  console.log('Use --test to run tests');
}
