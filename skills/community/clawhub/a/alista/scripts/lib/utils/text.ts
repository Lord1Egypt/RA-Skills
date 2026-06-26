/**
 * Text utilities for name normalization and comparison
 */

/**
 * Transliterate accented/diacritic characters to ASCII equivalents.
 * e.g., "Café" → "Cafe", "über" → "uber"
 */
function transliterate(str: string): string {
	return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

/**
 * Normalize a place name for comparison
 * - Lowercase
 * - Transliterate accented characters (é→e, ü→u, etc.)
 * - Remove common suffixes (restaurant, bar, cafe, etc.)
 * - Remove special characters
 * - Collapse whitespace
 */
export function normalizePlaceName(name: string): string {
	return transliterate(name)
		.toLowerCase()
		.trim()
		.replace(
			/\s+(restaurant|bar|cafe|café|coffee|shop|kitchen|eatery|bistro|grill|pub|lounge|bakery|brewery|winery|pizzeria|taqueria|diner|tavern)$/i,
			"",
		)
		.replace(/[^\w\s]/g, "") // Remove remaining special chars
		.replace(/\s+/g, " ") // Collapse whitespace
		.trim();
}

/**
 * Calculate similarity between two strings using Levenshtein distance
 * Returns a score between 0 (completely different) and 1 (identical)
 */
export function stringSimilarity(str1: string, str2: string): number {
	const s1 = str1.toLowerCase();
	const s2 = str2.toLowerCase();

	if (s1 === s2) return 1;
	if (s1.length === 0 || s2.length === 0) return 0;

	// Quick check: if one contains the other, high similarity
	if (s1.includes(s2) || s2.includes(s1)) {
		const minLen = Math.min(s1.length, s2.length);
		const maxLen = Math.max(s1.length, s2.length);
		return minLen / maxLen;
	}

	// Levenshtein distance
	const matrix: number[][] = [];

	for (let i = 0; i <= s1.length; i++) {
		matrix[i] = [i];
	}
	for (let j = 0; j <= s2.length; j++) {
		matrix[0][j] = j;
	}

	for (let i = 1; i <= s1.length; i++) {
		for (let j = 1; j <= s2.length; j++) {
			const cost = s1[i - 1] === s2[j - 1] ? 0 : 1;
			matrix[i][j] = Math.min(
				matrix[i - 1][j] + 1, // deletion
				matrix[i][j - 1] + 1, // insertion
				matrix[i - 1][j - 1] + cost, // substitution
			);
		}
	}

	const distance = matrix[s1.length][s2.length];
	const maxLen = Math.max(s1.length, s2.length);
	return 1 - distance / maxLen;
}

/**
 * Calculate token overlap score between two strings.
 * Returns a score between 0 and 1 based on how many tokens from the
 * shorter string appear in the longer string.
 * Handles cases like "Cafe 140B" matching "Cafe 140B at Ellerbeck B&B".
 */
export function tokenOverlapScore(str1: string, str2: string): number {
	const tokens1 = normalizePlaceName(str1).split(/\s+/).filter(Boolean);
	const tokens2 = normalizePlaceName(str2).split(/\s+/).filter(Boolean);

	if (tokens1.length === 0 || tokens2.length === 0) return 0;

	// Use the shorter token list as the query
	const [queryTokens, targetTokens] =
		tokens1.length <= tokens2.length ? [tokens1, tokens2] : [tokens2, tokens1];

	let matchCount = 0;
	for (const qt of queryTokens) {
		if (targetTokens.some((tt) => tt === qt || tt.includes(qt) || qt.includes(tt))) {
			matchCount++;
		}
	}

	// Score = proportion of query tokens found in target
	return matchCount / queryTokens.length;
}

/**
 * Check if two place names are similar enough to be considered the same
 * Uses normalized comparison with a threshold
 */
export function isSamePlaceName(name1: string, name2: string, threshold = 0.7): boolean {
	const norm1 = normalizePlaceName(name1);
	const norm2 = normalizePlaceName(name2);

	// Exact match after normalization
	if (norm1 === norm2) return true;

	// Check token overlap (catches "Cafe 140B" ≈ "Cafe 140B at Ellerbeck B&B")
	if (tokenOverlapScore(name1, name2) >= threshold) return true;

	// Check similarity score
	return stringSimilarity(norm1, norm2) >= threshold;
}

/**
 * Deduplicate an array of items by a key function
 * Keeps the first occurrence of each unique key
 */
export function deduplicateBy<T>(items: T[], keyFn: (item: T) => string): T[] {
	const seen = new Set<string>();
	const result: T[] = [];

	for (const item of items) {
		const key = normalizePlaceName(keyFn(item));
		if (!seen.has(key)) {
			seen.add(key);
			result.push(item);
		}
	}

	return result;
}
