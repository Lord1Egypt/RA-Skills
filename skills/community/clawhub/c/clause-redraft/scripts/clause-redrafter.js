#!/usr/bin/env node
/**
 * Clause Redrafter
 * 
 * Provides alternative wording for contract clauses.
 * This is a drafting assistance tool and does not constitute legal advice.
 */

const REDRAFT_PATTERNS = [
  // Payment terms
  {
    pattern: /payment due (?:upon|on) completion/i,
    issue: 'Vague payment trigger - "completion" is subjective',
    balanced: 'Payment shall be due within 30 days of invoice date or within 10 days of acceptance of deliverables, whichever is earlier.',
    protective: 'Payment shall be due within 15 days of invoice. Late payments subject to 1.5% monthly service charge.',
    simple: 'Payment is due 30 days after you receive the invoice.'
  },
  {
    pattern: /net\s*6[0-9]|payment within\s*6[0-9]|payment within\s*9[0-9]/i,
    issue: 'Extended payment terms (60+ days) may impact cash flow',
    balanced: 'Payment terms are net 30 days from invoice date.',
    protective: 'Payment terms are net 15 days from invoice date.',
    simple: 'Please pay within 30 days of receiving the invoice.'
  },
  
  // Termination
  {
    pattern: /may (?:terminate|end).*at any time/i,
    issue: 'No notice period creates uncertainty',
    balanced: 'Either party may terminate with 30 days written notice.',
    protective: 'Either party may terminate with 60 days written notice. Client remains obligated to pay for the notice period.',
    simple: 'Either side can end this agreement by giving 30 days notice.'
  },
  {
    pattern: /automatically renew|auto-renew/i,
    issue: 'Automatic renewal without notice requirement',
    balanced: 'This agreement automatically renews for successive one-year terms unless either party provides 60 days written notice of non-renewal.',
    protective: 'This agreement automatically renews for successive one-year terms unless either party provides 30 days written notice of non-renewal.',
    simple: 'This agreement renews automatically each year unless someone cancels it 60 days before the end.'
  },
  
  // IP
  {
    pattern: /work[-\s]made[-\s]for[-\s]hire|work for hire/i,
    issue: 'Work-for-hire may capture unintended IP',
    balanced: 'Deliverables shall be work-made-for-hire for Client. Vendor retains rights to pre-existing materials and general methodologies.',
    protective: 'Vendor grants Client a license to use deliverables. Vendor retains ownership of all intellectual property.',
    simple: 'The work product belongs to the client, but I keep rights to my general methods and tools.'
  },
  {
    pattern: /assigns all rights|all (?:inventions|intellectual property)/i,
    issue: 'Broad IP assignment may be overreaching',
    balanced: 'Vendor assigns rights in deliverables specifically created for Client. Vendor retains rights to pre-existing materials.',
    protective: 'Vendor retains all ownership rights and grants Client a perpetual license for internal use.',
    simple: 'I give you rights to use what I create for you, but I keep ownership.'
  },
  
  // Confidentiality
  {
    pattern: /indefinitely|perpetual confidentiality/i,
    issue: 'Indefinite confidentiality obligation may be unenforceable',
    balanced: 'Confidential information shall be held for 3 years from disclosure, or indefinitely for trade secrets.',
    protective: 'Confidential information shall be held for 2 years from disclosure.',
    simple: 'Keep secrets for 3 years (or forever if they are trade secrets).'
  },
  {
    pattern: /all information.*confidential/i,
    issue: 'Overly broad confidentiality definition',
    balanced: '"Confidential Information" means information marked as confidential or reasonably understood to be confidential.',
    protective: '"Confidential Information" is limited to information explicitly marked as confidential.',
    simple: 'Only information marked "confidential" needs to be kept secret.'
  },
  
  // Liability
  {
    pattern: /unlimited liability|no limit.*liability/i,
    issue: 'Unlimited liability creates excessive exposure',
    balanced: 'Each party\'s liability is limited to fees paid under this agreement in the 12 months preceding the claim.',
    protective: 'Vendor\'s liability is limited to fees paid for the specific services giving rise to the claim.',
    simple: 'Our liability is limited to what you paid us in the past year.'
  },
  
  // Indemnification
  {
    pattern: /indemnify.*any and all|hold harmless.*any/i,
    issue: 'Broad indemnification obligation',
    balanced: 'Each party shall indemnify the other for claims arising from its breach of this agreement or negligence.',
    protective: 'Vendor shall indemnify Client only for IP infringement claims related to deliverables.',
    simple: 'We each cover damages caused by our own mistakes.'
  },
  
  // Assignment
  {
    pattern: /may not be assigned|assignment.*consent/i,
    issue: 'Assignment restrictions may limit business flexibility',
    balanced: 'Either party may assign to an affiliate or in connection with a merger or sale of assets.',
    protective: 'Either party may assign without restriction upon 30 days notice.',
    simple: 'You can transfer this agreement if you sell your business.'
  }
];

/**
 * Analyze a clause and provide redraft suggestions
 * @param {string} clauseText - The clause to analyze
 * @param {string} userRole - 'client' or 'vendor' (optional)
 * @returns {Object} Redraft suggestions
 */
function redraftClause(clauseText, userRole = 'balanced') {
  if (!clauseText || typeof clauseText !== 'string') {
    return {
      error: 'Invalid input: clause text is required',
      original: '',
      issues: [],
      suggestions: []
    };
  }

  const text = clauseText.toLowerCase();
  const issues = [];
  const matchedPatterns = [];

  // Check for known problematic patterns
  for (const pattern of REDRAFT_PATTERNS) {
    if (pattern.pattern.test(text)) {
      matchedPatterns.push(pattern);
      issues.push(pattern.issue);
    }
  }

  // If no specific pattern matched, do general analysis
  if (issues.length === 0) {
    if (text.length < 20) {
      issues.push('Clause is very short - may lack specificity');
    }
    if (!text.includes('shall') && !text.includes('must') && !text.includes('will')) {
      issues.push('Clause lacks clear obligation language');
    }
    if (text.includes('etc') || text.includes('and so on')) {
      issues.push('Vague language ("etc.", "and so on") should be replaced with specific list');
    }
  }

  // Generate suggestions based on role preference
  const suggestions = [];
  
  if (matchedPatterns.length > 0) {
    // Use matched pattern templates
    for (const pattern of matchedPatterns) {
      suggestions.push({
        type: 'balanced',
        text: pattern.balanced,
        note: 'Fair to both parties'
      });
      suggestions.push({
        type: 'protective',
        text: pattern.protective,
        note: userRole === 'vendor' ? 'More favorable to service provider' : 'More favorable to client'
      });
      suggestions.push({
        type: 'simple',
        text: pattern.simple,
        note: 'Plain language version'
      });
    }
  } else {
    // Generic suggestions
    suggestions.push({
      type: 'improved',
      text: makeMoreSpecific(clauseText),
      note: 'Added specificity'
    });
    suggestions.push({
      type: 'simplified',
      text: simplifyLanguage(clauseText),
      note: 'Plain language version'
    });
  }

  return {
    original: clauseText,
    issues: issues.length > 0 ? issues : ['No obvious issues detected'],
    suggestions: suggestions,
    disclaimer: 'These suggestions are for drafting assistance only and do not constitute legal advice. Consult qualified counsel before finalizing contract language.'
  };
}

/**
 * Make clause more specific
 * @param {string} text - Original text
 * @returns {string} More specific version
 */
function makeMoreSpecific(text) {
  // Add specificity improvements
  let improved = text;
  
  // Replace vague time references
  improved = improved.replace(/\b(promptly|timely|reasonable time)\b/gi, 'within 10 business days');
  improved = improved.replace(/\b(as soon as possible|ASAP)\b/gi, 'within 5 business days');
  
  // Replace vague quantity references
  improved = improved.replace(/\b(some|several|a few)\b/gi, 'a reasonable number of');
  
  return improved;
}

/**
 * Simplify legal language
 * @param {string} text - Original text
 * @returns {string} Simplified version
 */
function simplifyLanguage(text) {
  const replacements = {
    'pursuant to': 'under',
    'hereinafter': 'below',
    'herein': 'in this agreement',
    'thereto': 'to it',
    'whereas': 'because',
    'witnesseth': 'agrees',
    'shall': 'must',
    'provided that': 'if',
    'notwithstanding': 'despite',
    'prior to': 'before',
    'subsequent to': 'after',
    'in the event that': 'if',
    'for the duration of': 'during',
    'in accordance with': 'under',
    'by means of': 'by',
    'in order to': 'to',
    'with respect to': 'about',
    'in connection with': 'related to'
  };
  
  let simplified = text;
  for (const [legal, plain] of Object.entries(replacements)) {
    const regex = new RegExp('\\b' + legal + '\\b', 'gi');
    simplified = simplified.replace(regex, plain);
  }
  
  return simplified;
}

/**
 * Format redraft results for display
 * @param {Object} results - Redraft results
 * @returns {string} Formatted output
 */
function formatResults(results) {
  if (results.error) {
    return 'Error: ' + results.error;
  }

  let output = '=== CLAUSE REDRAFT RESULTS ===\n\n';
  
  output += 'ORIGINAL:\n';
  output += results.original + '\n\n';
  
  output += 'ISSUES IDENTIFIED:\n';
  results.issues.forEach((issue, index) => {
    output += (index + 1) + '. ' + issue + '\n';
  });
  output += '\n';
  
  output += 'SUGGESTED ALTERNATIVES:\n\n';
  results.suggestions.forEach((suggestion, index) => {
    output += '--- ' + suggestion.type.toUpperCase() + ' ---\n';
    output += suggestion.text + '\n';
    output += '(' + suggestion.note + ')\n\n';
  });
  
  output += '=== DISCLAIMER ===\n';
  output += results.disclaimer + '\n';

  return output;
}

// Export for use as module
module.exports = { redraftClause, formatResults, REDRAFT_PATTERNS };

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    console.log('Usage: node clause-redrafter.js "clause text"');
    console.log('   or: node clause-redrafter.js --test');
    process.exit(0);
  }

  if (args[0] === '--test') {
    const test = require('./test.js');
    test.runTests();
    process.exit(0);
  }

  const clauseText = args.join(' ');
  const results = redraftClause(clauseText);
  console.log(formatResults(results));
}
