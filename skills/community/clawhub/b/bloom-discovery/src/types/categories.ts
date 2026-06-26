/**
 * Canonical Category List
 *
 * Single source of truth for category names used across:
 * - Personality analyzer (detectCategories)
 * - CategoryMapper (fallback)
 * - GitHub recommendations (topic mapping)
 * - Recommendation grouping (findBestCategory)
 * - Browse mode (display categories)
 *
 * Categories represent WHAT the user is interested in (detected from conversation).
 * They are independent of personality type (which represents HOW the user thinks).
 *
 * 14 fine-grained categories match the backend skill-catalog.service.ts exactly.
 * 9 display categories match the frontend skill-category-definitions.ts.
 */

// ─── Fine-grained categories (backend-aligned) ─────────────────────────

export const CANONICAL_CATEGORIES = [
  'Agent Framework',
  'Context Engineering',
  'MCP Ecosystem',
  'Coding Assistant',
  'AI Tools',
  'Productivity',
  'Wellness',
  'Education',
  'Crypto',
  'Lifestyle',
  'Design',
  'Development',
  'Marketing',
  'Finance',
  'Prediction Market',
] as const;

export type CanonicalCategory = (typeof CANONICAL_CATEGORIES)[number];

/**
 * Keyword lists for detecting categories from conversation text.
 * Used by personality-analyzer's detectCategories() and by findBestCategory().
 *
 * Kept in sync with backend CATEGORY_KEYWORDS in skill-catalog.service.ts.
 * Order matters: specific AI subcategories come before broad "AI Tools"
 * so the personality analyzer picks the more precise match first.
 */
export const CATEGORY_KEYWORDS: Record<CanonicalCategory, string[]> = {
  'Agent Framework': [
    'agent framework', 'agent orchestrat', 'multi-agent', 'agent os',
    'agent architect', 'agent system', 'agent workflow', 'agentic',
    'crew ai', 'autogen', 'langchain', 'langgraph', 'swarm',
    'agent skill', 'agent tool', 'subagent', 'orchestrat', 'agent harness',
  ],
  'Context Engineering': [
    'context engineer', 'context window', 'context manag', 'memory manag',
    'knowledge graph', 'rag', 'retrieval augment', 'embedding', 'vector',
    'semantic search', 'long context', 'context protocol',
  ],
  'MCP Ecosystem': [
    'mcp server', 'mcp client', 'mcp tool', 'model context protocol',
    'mcp-server', 'mcp-client', 'mcp-tool', 'mcp plugin',
  ],
  'Coding Assistant': [
    'coding assistant', 'code generat', 'code review', 'code complet',
    'coding agent', 'ai coding', 'copilot', 'code edit', 'refactor',
    'linter', 'debugg', 'test generat', 'code search', 'codebase',
    'claude code', 'cursor', 'continue dev', 'devin', 'openclaw',
    'claude skill', 'vb.net', 'coding standard', 'clean code', 'opencode',
  ],
  'AI Tools': [
    'gpt', 'llm', 'machine learning', 'neural', 'chatbot',
    'openai', 'anthropic', 'prompt engineer', 'inference', 'transformer',
    'gemini', 'image gen', 'text-to', 'ai-powered', 'ai agent',
    'web search', 'tavily', 'ai note', 'ai ppt', 'voice gen', 'tts', 'audio gen',
  ],
  'Productivity': [
    'productivity', 'workflow', 'automation', 'efficiency', 'task management',
    'notion', 'calendar', 'time tracking', 'systematic', 'slide',
    'template', 'saas integrat', 'ppt generat',
  ],
  'Wellness': [
    'wellness', 'health', 'fitness', 'meditation', 'mindfulness',
    'mental health', 'yoga', 'sleep', 'nutrition', 'self-care',
    'therapy', 'therapeutic', 'cbt', 'counseling', 'journaling',
    'self-improv', 'accountability coach',
  ],
  'Education': [
    'education', 'learning', 'course', 'teach', 'tutorial',
    'study', 'mentor', 'curriculum', 'workshop', 'comic', 'explainer',
  ],
  'Crypto': [
    'crypto', 'defi', 'web3', 'blockchain', 'dao', 'nft',
    'onchain', 'smart contract', 'ethereum', 'solana', 'base chain',
    'base network', 'tokenomics', 'dapp',
  ],
  'Lifestyle': [
    'lifestyle', 'fashion', 'travel', 'personal brand', 'food', 'photography',
  ],
  'Design': [
    'ui design', 'ux design', 'figma', 'typography', 'layout', 'prototype',
    'infographic', 'illustration', 'cover image', 'graphic design', 'ui/ux',
    'design system', 'design tool', 'ui audit', 'interface design', 'frontend design',
  ],
  'Development': [
    'developer', 'programming', 'software', 'engineering',
    'typescript', 'python', 'rust', 'cli', 'sdk', 'devtools',
    'dev tool', 'url-to', 'converter', 'terraform',
    'infrastructure as code', 'migration', 'rollout', 'linux',
  ],
  'Marketing': [
    'marketing', 'seo', 'content strategy', 'advertising',
    'conversion', 'funnel', 'campaign', 'copywriting', 'copy editing', 'cro',
    'landing page', 'churn', 'referral', 'email sequence',
    'cold email', 'drip', 'paywall', 'popup', 'a/b test',
    'split test', 'ad creative', 'competitor', 'social content',
    'social media', 'wechat', 'xiaohongshu', 'post to x',
    'product launch', 'go-to-market', 'business growth',
  ],
  'Finance': [
    'finance', 'investing', 'trading', 'portfolio', 'wealth', 'stock market',
    'budget', 'revenue', 'financial', 'dividend', 'screener', 'spending', 'balance',
  ],
  'Prediction Market': [
    'prediction market', 'polymarket', 'metaculus', 'manifold', 'forecast',
    'futarchy', 'information market', 'event contract', 'binary option', 'kalshi',
  ],
};

// ─── Display categories (frontend-aligned) ──────────────────────────────

/**
 * Maps user-facing display categories → backend fine-grained categories.
 * Matches both:
 *   - Backend:  skills-public.controller.ts DISPLAY_CATEGORY_MAP
 *   - Frontend: skill-category-definitions.ts SKILL_CATEGORY_DEFINITIONS
 */
export const DISPLAY_CATEGORY_MAP: Record<string, (CanonicalCategory | 'General')[]> = {
  'Agent & MCP': ['Agent Framework', 'Context Engineering', 'MCP Ecosystem'],
  'AI & Dev Tools': ['AI Tools', 'Development', 'Coding Assistant'],
  'Productivity': ['Productivity'],
  'Design': ['Design'],
  'Marketing': ['Marketing'],
  'Crypto & Web3': ['Crypto'],
  'Finance': ['Finance'],
  'Prediction Market': ['Prediction Market'],
  'Wellness': ['Wellness'],
  'Education': ['Education', 'Lifestyle'],
  'Other': ['General'],
};

export const DISPLAY_CATEGORIES = Object.keys(DISPLAY_CATEGORY_MAP);

/**
 * Map a fine-grained canonical category to its display category.
 * Returns the input string if no mapping exists (graceful fallback).
 */
export function toDisplayCategory(canonical: string): string {
  for (const [display, fineGrained] of Object.entries(DISPLAY_CATEGORY_MAP)) {
    if ((fineGrained as string[]).includes(canonical)) return display;
  }
  return canonical;
}

// ─── GitHub topics ──────────────────────────────────────────────────────

/**
 * GitHub search topics for each canonical category.
 * Used by GitHubRecommendations to build search queries.
 */
export const CATEGORY_GITHUB_TOPICS: Record<CanonicalCategory, string[]> = {
  'Agent Framework': ['ai-agent', 'agent-framework', 'multi-agent', 'agentic', 'langchain', 'langgraph'],
  'Context Engineering': ['rag', 'embeddings', 'vector-database', 'knowledge-graph', 'context-engineering'],
  'MCP Ecosystem': ['mcp', 'model-context-protocol', 'mcp-server', 'mcp-client'],
  'Coding Assistant': ['coding-assistant', 'code-generation', 'copilot', 'ai-coding', 'developer-tools'],
  'AI Tools': ['ai', 'artificial-intelligence', 'machine-learning', 'llm', 'chatgpt', 'gpt'],
  'Productivity': ['productivity', 'automation', 'workflow', 'tools', 'utilities'],
  'Wellness': ['health', 'fitness', 'wellness', 'meditation', 'mindfulness', 'mental-health'],
  'Education': ['education', 'learning', 'tutorial', 'course', 'teaching'],
  'Crypto': ['blockchain', 'web3', 'crypto', 'ethereum', 'solana', 'defi', 'smart-contracts'],
  'Lifestyle': ['lifestyle', 'travel', 'food', 'photography', 'personal'],
  'Design': ['design', 'ui', 'ux', 'figma', 'design-tools', 'creative'],
  'Development': ['developer-tools', 'devtools', 'cli', 'sdk', 'library', 'framework'],
  'Marketing': ['marketing', 'seo', 'analytics', 'growth', 'content'],
  'Finance': ['finance', 'fintech', 'trading', 'investing', 'budgeting'],
  'Prediction Market': ['prediction-market', 'forecasting', 'polymarket', 'metaculus', 'manifold', 'kalshi'],
};

/**
 * Default fallback categories when conversation analysis detects nothing.
 * These are the broadest, most universally populated categories across all sources.
 */
export const DEFAULT_FALLBACK_CATEGORIES: CanonicalCategory[] = [
  'AI Tools',
  'Development',
  'Productivity',
];

/**
 * Blocked keywords for filtering out potentially malicious or harmful repos/skills.
 * Applied to both GitHub and Claude Code recommendation pipelines.
 */
export const BLOCKED_KEYWORDS = [
  'hack', 'crack', 'exploit', 'phishing', 'drainer', 'stealer',
  'keylogger', 'malware', 'trojan', 'botnet', 'ransomware',
  'brute-force', 'password-crack', 'rat-tool', 'spyware',
  'wallet-drainer', 'token-grabber', 'cookie-stealer',
];

/**
 * Check if text contains any blocked keywords (case-insensitive).
 * Uses word-boundary matching where practical to avoid false positives.
 */
export function containsBlockedKeyword(text: string): boolean {
  const lower = text.toLowerCase();
  return BLOCKED_KEYWORDS.some(keyword => {
    // Use word boundary regex for single-word keywords, plain includes for hyphenated
    if (keyword.includes('-')) {
      return lower.includes(keyword);
    }
    const regex = new RegExp(`\\b${keyword}\\b`, 'i');
    return regex.test(lower);
  });
}
