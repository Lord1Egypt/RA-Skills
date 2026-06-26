/**
 * core/text-processing.ts — Shared text processing utilities.
 *
 * Used by the matching engine (Phase 4), resume intelligence (Phase 5),
 * and gap analysis (Phase 5). All functions are pure and stateless.
 *
 * Design notes:
 * - No external NLP dependencies — stopword logic is ported directly
 *   from the Python careerclaw implementation.
 * - STOPWORDS is the single source of truth. No parallel lists.
 * - Phrases are sliding-window bigrams and trigrams over the token stream.
 * - SECTION_WEIGHTS drives keyword importance in resume intelligence (Phase 5).
 */

// ---------------------------------------------------------------------------
// Stopwords
// ---------------------------------------------------------------------------

/**
 * Combined stopword set: common English function words + recruitment
 * boilerplate terms that carry zero signal value for job matching.
 *
 * Recruitment boilerplate sourced from PR-E signal hygiene analysis
 * (February 2026): terms that appeared consistently in gap keyword lists
 * despite having no technical meaning.
 */
export const STOPWORDS: ReadonlySet<string> = new Set([
  // Common English function words
  "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
  "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
  "been", "being", "am", "have", "has", "had", "do", "does", "did", "will",
  "would", "could", "should", "may", "might", "shall", "can", "need",
  "dare", "ought", "used", "it", "its", "this", "that", "these", "those",
  "i", "you", "he", "she", "we", "they", "me", "him", "her", "us",
  // Contractions
  "i'm", "i've", "i'll", "i'd", "you're", "we're", "they're", "it's",
  "don't", "doesn't", "can't", "won't", "isn't", "aren't", "wasn't", "weren't",
  "them", "my", "your", "his", "our", "their", "what", "which", "who",
  "whom", "when", "where", "why", "how", "all", "each", "every", "both",
  "few", "more", "most", "other", "some", "such", "no", "not", "only",
  "same", "so", "than", "too", "very", "just", "about", "above", "after",
  "also", "between", "during", "into", "through", "up", "out", "if",
  "while", "then", "than", "there", "here", "any", "now", "new", "well",
  "back", "even", "still", "way", "take", "get", "make", "know", "time",
  "year", "day", "part", "over", "many", "much", "own", "go", "see",
  "come", "think", "look", "want", "give", "use", "find", "tell", "ask",
  "work", "seem", "feel", "try", "leave", "call", "keep", "let", "begin",
  "show", "hear", "play", "run", "move", "live", "believe", "hold",
  "bring", "happen", "write", "provide", "sit", "stand", "lose", "pay",
  "meet", "include", "continue", "set", "learn", "change", "lead",
  "understand", "watch", "follow", "stop", "create", "speak", "read",
  "spend", "grow", "open", "walk", "win", "offer", "remember", "love",
  "consider", "appear", "buy", "wait", "serve", "die", "send", "expect",
  "build", "stay", "fall", "cut", "reach", "kill", "remain", "suggest",
  "raise", "pass", "sell", "require", "report", "decide", "pull", "based",
  "able", "across", "against", "along", "already", "although", "among",
  "around", "away", "because", "before", "below", "beside", "beyond",
  "down", "early", "enough", "ever", "first", "further", "however", "last",
  "late", "later", "least", "less", "like", "long", "near", "never",
  "next", "often", "once", "our", "per", "quite", "rather", "since",
  "soon", "still", "though", "together", "under", "until", "upon",
  "usually", "whether", "within", "without", "yet", "second", "third",

  // Recruitment process terms (PR-E signal hygiene)
  "apply", "applying", "applicant", "applicants", "application",
  "applications", "submit", "submission", "submissions",
  "candidate", "candidates", "qualified", "successful", "shortlisted",
  "interview", "interviewing", "hire", "hiring", "onboard", "onboarding",
  "recruit", "recruiting", "recruitment",

  // Generic descriptor terms (PR-E signal hygiene)
  "competitive", "opportunity", "opportunities", "benefit", "benefits",
  "package", "responsible", "responsibilities", "responsibility",
  "seeking", "looking", "plus", "bonus", "nice-to-have", "preferred",
  "required", "requirement", "requirements", "experience", "years",
  "role", "roles", "position", "positions", "team", "teams", "company",
  "companies", "business", "businesses", "product", "products",
  "mission", "vision", "values", "culture", "environment", "office",
  "full-time", "part-time", "contract", "permanent", "temporary",
  "salary", "compensation", "equity", "stock", "options", "remote",
  "hybrid", "onsite", "location", "worldwide", "anywhere", "global",
  "join", "help", "love", "great", "good", "best", "strong", "deep",
  "high", "low", "fast", "smart", "care", "important", "key", "top",
  "amazing", "excellent", "outstanding", "exceptional", "passionate",
  "driven", "motivated", "collaborative", "dynamic", "innovative",
  "exciting", "unique", "diverse", "inclusive", "equal", "opportunity",
]);

// ---------------------------------------------------------------------------
// Section weights
// ---------------------------------------------------------------------------

/**
 * Relative importance weights for resume sections in keyword extraction.
 * Used by resume intelligence (Phase 5) to weight keyword scores.
 * Skills = 1.0 is the maximum weight.
 */
export const SECTION_WEIGHTS: Readonly<Record<string, number>> = {
  skills: 1.0,
  summary: 0.8,
  experience: 0.6,
  education: 0.4,
  other: 0.3,
};

// ---------------------------------------------------------------------------
// Tokenization
// ---------------------------------------------------------------------------

/**
 * Tokenize a text string into a filtered array of lowercase tokens.
 *
 * Steps:
 *   1. Lowercase
 *   2. Split on non-alphanumeric boundaries (preserves hyphenated terms)
 *   3. Strip leading/trailing punctuation from each token
 *   4. Drop tokens shorter than MIN_TOKEN_LENGTH
 *   5. Drop stopwords
 */
const MIN_TOKEN_LENGTH = 2;

export function tokenize(text: string): string[] {
  return text
    .toLowerCase()
    .split(/[\s,;:!?()[\]{}<>"]+/)
    .map((t) => t.replace(/^[^a-z0-9-]+|[^a-z0-9-]+$/g, ""))
    .filter((t) => t.length >= MIN_TOKEN_LENGTH && !STOPWORDS.has(t));
}

/**
 * Tokenize and return only unique tokens (set semantics, insertion order).
 * Useful for keyword overlap scoring where duplicates add no information.
 */
export function tokenizeUnique(text: string): string[] {
  return [...new Set(tokenize(text))];
}

// ---------------------------------------------------------------------------
// Phrase extraction
// ---------------------------------------------------------------------------

/**
 * Extract bigrams and trigrams from a token stream.
 *
 * Tokens are joined with a space: ["senior", "engineer"] → "senior engineer".
 * Phrases from short token streams (< 2 tokens) are returned as empty array.
 */
export function extractPhrases(tokens: string[]): string[] {
  const phrases: string[] = [];

  for (let i = 0; i < tokens.length - 1; i++) {
    // Bigram
    phrases.push(`${tokens[i]} ${tokens[i + 1]}`);

    // Trigram
    if (i < tokens.length - 2) {
      phrases.push(`${tokens[i]} ${tokens[i + 1]} ${tokens[i + 2]}`);
    }
  }

  return phrases;
}

/**
 * Tokenize text and extract bigram + trigram phrases in one pass.
 * Returns unique phrases (insertion order).
 */
export function extractPhrasesFromText(text: string): string[] {
  return [...new Set(extractPhrases(tokenize(text)))];
}

// ---------------------------------------------------------------------------
// Keyword overlap
// ---------------------------------------------------------------------------

/**
 * Compute the Jaccard-like overlap between two token sets.
 * Returns a value in [0, 1]: |intersection| / |union|.
 */
export function tokenOverlap(a: string[], b: string[]): number {
  if (a.length === 0 && b.length === 0) return 0;
  const setA = new Set(a);
  const setB = new Set(b);
  const intersection = a.filter((t) => setB.has(t)).length;
  const union = new Set([...setA, ...setB]).size;
  return union === 0 ? 0 : intersection / union;
}

/**
 * Return tokens in `query` that are present in `corpus`.
 * Used to produce "matched_keywords" in ScoredJob.
 */
export function matchedTokens(query: string[], corpus: string[]): string[] {
  const corpusSet = new Set(corpus);
  return [...new Set(query.filter((t) => corpusSet.has(t)))];
}

/**
 * Return tokens in `query` that are absent from `corpus`.
 * Used to produce "gap_keywords" in ScoredJob.
 */
export function gapTokens(query: string[], corpus: string[]): string[] {
  const corpusSet = new Set(corpus);
  return [...new Set(query.filter((t) => !corpusSet.has(t)))];
}
