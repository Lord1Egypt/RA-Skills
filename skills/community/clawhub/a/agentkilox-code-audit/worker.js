export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, x402-payment',
    };
    
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }
    
    // Health check
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({ 
        status: 'ok', 
        service: 'code-audit', 
        price: '$0.25/scan' 
      }), {
        headers: { 'Content-Type': 'application/json', ...corsHeaders }
      });
    }
    
    // Main audit endpoint
    if (url.pathname === '/audit' && request.method === 'POST') {
      const payment = request.headers.get('x402-payment') || url.searchParams.get('payment');
      
      if (!payment) {
        return new Response(JSON.stringify({
          error: 'payment_required',
          service: 'code-audit',
          price: '$0.25',
          instructions: 'Include x402-payment header or ?payment=1'
        }), { status: 402, headers: { 'Content-Type': 'application/json', ...corsHeaders } });
      }
      
      try {
        const { code, language = 'python' } = await request.json();
        
        if (!code || typeof code !== 'string') {
          return new Response(JSON.stringify({ error: 'missing_code' }), { 
            status: 400, headers: { 'Content-Type': 'application/json', ...corsHeaders } 
          });
        }
        
        if (code.length > 500000) {
          return new Response(JSON.stringify({ error: 'code_too_large', max: '500KB' }), { 
            status: 400, headers: { 'Content-Type': 'application/json', ...corsHeaders } 
          });
        }
        
        const result = await auditCode(code, language);
        return new Response(JSON.stringify(result), {
          headers: { 'Content-Type': 'application/json', ...corsHeaders }
        });
      } catch (e) {
        return new Response(JSON.stringify({ error: 'audit_failed', message: e.message }), {
          status: 500, headers: { 'Content-Type': 'application/json', ...corsHeaders }
        });
      }
    }
    
    return new Response('Not Found', { status: 404 });
  }
};

/**
 * Static analysis for security issues
 */
function basicAnalysis(code) {
  const issues = [];
  const lines = code.split('\n');
  
  // Check for hardcoded secrets
  const secretPatterns = [
    /api[_-]?key["']?\s*[:=]\s*["'][a-zA-Z0-9]{20,}/gi,
    /password["']?\s*[:=]\s*["'][^"']+/gi,
    /secret["']?\s*[:=]\s*["'][^"']+/gi,
    /token["']?\s*[:=]\s*["'][a-zA-Z0-9]{20,}/gi,
  ];
  
  lines.forEach((line, idx) => {
    secretPatterns.forEach(pattern => {
      if (pattern.test(line)) {
        issues.push({
          line: idx + 1,
          issue: 'Potential hardcoded secret detected',
          severity: 'HIGH',
          confidence: 'MEDIUM'
        });
      }
    });
  });
  
  // Check for dangerous functions
  const dangerousPatterns = [
    { pattern: /eval\s*\(/, issue: 'Use of eval() - code injection risk', severity: 'HIGH' },
    { pattern: /exec\s*\(/, issue: 'Use of exec() - code injection risk', severity: 'HIGH' },
    { pattern: /subprocess\.call\s*\([^)]*shell\s*=\s*True/, issue: 'shell=True in subprocess - avoid', severity: 'HIGH' },
    { pattern: /__import__\s*\(\s*["'](os|sys|subprocess)/, issue: 'Dynamic import of sensitive module', severity: 'MEDIUM' },
  ];
  
  lines.forEach((line, idx) => {
    dangerousPatterns.forEach(({ pattern, issue, severity }) => {
      if (pattern.test(line)) {
        issues.push({
          line: idx + 1,
          issue,
          severity,
          confidence: 'HIGH'
        });
      }
    });
  });
  
  return issues;
}

async function auditCode(code, language = 'python') {
  const startTime = Date.now();
  const PRICE_CENTS = 25;
  
  let results = {
    tool: 'static',
    timestamp: new Date().toISOString(),
    issues: [],
    stats: {
      linesOfCode: code.split('\n').length,
      scanTimeMs: 0,
      cost: 0
    }
  };
  
  // Static analysis for all languages
  const basicIssues = basicAnalysis(code);
  results.issues = basicIssues;
  
  // Deduplicate
  const seen = new Set();
  results.issues = results.issues.filter(i => {
    const key = `${i.line}:${i.issue}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
  
  results.stats.scanTimeMs = Date.now() - startTime;
  
  // Calculate confidence score (0-100)
  const highCount = results.issues.filter(i => i.severity === 'HIGH').length;
  const medCount = results.issues.filter(i => i.severity === 'MEDIUM').length;
  const score = Math.max(0, 100 - (highCount * 10) - (medCount * 3));
  
  results.confidenceScore = score;
  results.priceCents = PRICE_CENTS;
  
  return results;
}