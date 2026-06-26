/**
 * Exa Search - ClawHub API Wrapper
 * 
 * This is a CLIENT-SIDE wrapper that calls the Claw0x Gateway API.
 * It requires CLAW0X_API_KEY to be set in your environment.
 * 
 * Pricing: $0.005 per successful call via Claw0x Gateway.
 */

// Environment variable helper (works in Node.js and browser contexts)
function env(key: string): string {
  if (typeof process !== 'undefined' && process.env) {
    return process.env[key] || '';
  }
  return '';
}

// Input type
interface ExaSearchInput {
  query: string;
  search_type?: 'neural' | 'keyword' | 'auto';
  start_published_date?: string;
  end_published_date?: string;
  category?: 'company' | 'research paper' | 'news' | 'github' | 'tweet' | 'pdf' | 'personal site';
  num_results?: number;
  include_domains?: string[];
  exclude_domains?: string[];
  use_autoprompt?: boolean;
  include_text?: boolean;
  text_length_limit?: number;
  highlights?: boolean;
}

// Output type
interface ExaSearchOutput {
  results: Array<{
    title: string;
    url: string;
    published_date: string | null;
    author: string | null;
    score: number;
    text?: string;
    highlights?: string[];
    summary?: string;
    category: string | null;
    domain: string;
  }>;
  autoprompt_string?: string;
  result_count: number;
  _meta: {
    skill: string;
    latency_ms: number;
    search_type: string;
    date_filtered: boolean;
  };
}

/**
 * Main function called by OpenClaw agent
 * @param input - Search query and options
 * @returns Search results with precise date filtering and content type selection
 */
export async function run(input: ExaSearchInput): Promise<ExaSearchOutput> {
  const apiKey = env('CLAW0X_API_KEY');
  
  if (!apiKey) {
    throw new Error(
      'CLAW0X_API_KEY is required. Get your key at https://claw0x.com\n' +
      'Sign up → Dashboard → Create API Key → Set as environment variable'
    );
  }

  // Validate input
  if (!input.query || typeof input.query !== 'string') {
    throw new Error('Missing required field: query (string)');
  }

  if (input.query.length < 1 || input.query.length > 500) {
    throw new Error('query must be between 1 and 500 characters');
  }

  // Call Claw0x Gateway API
  const response = await fetch('https://api.claw0x.com/v1/call', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      skill: 'exa-search',
      input
    })
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: response.statusText }));
    throw new Error(`Claw0x API error (${response.status}): ${error.error || response.statusText}`);
  }

  const result = await response.json();
  return result as ExaSearchOutput;
}

// Default export for compatibility
export default run;
