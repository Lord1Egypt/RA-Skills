/**
 * URL normalization utilities for caching and deduplication.
 * Matches the normalize_url() SQL function behavior.
 */

/**
 * Normalize a social media URL for caching/deduplication.
 * Removes tracking params, normalizes domains, and extracts canonical identifiers.
 */
export function normalizeUrl(url: string): string {
	let normalized = url;

	// Remove protocol
	normalized = normalized.replace(/^https?:\/\//, "");

	// Normalize Instagram short URLs
	normalized = normalized.replace(/^instagr\.am\//, "instagram.com/");

	// Remove www. prefix
	normalized = normalized.replace(/^www\./, "");

	// Remove trailing slashes and query params
	normalized = normalized.replace(/\?.*$/, "");
	normalized = normalized.replace(/\/+$/, "");

	// Extract canonical identifiers for Instagram
	if (normalized.includes("instagram.com")) {
		// Reels
		const reelMatch = normalized.match(/instagram\.com\/reel\/([A-Za-z0-9_-]+)/);
		if (reelMatch) {
			return `instagram.com/reel/${reelMatch[1]}`;
		}

		// Posts
		const postMatch = normalized.match(/instagram\.com\/p\/([A-Za-z0-9_-]+)/);
		if (postMatch) {
			return `instagram.com/p/${postMatch[1]}`;
		}

		// Profiles (catch-all for usernames)
		const profileMatch = normalized.match(/instagram\.com\/([A-Za-z0-9_.]+)\/?$/);
		if (profileMatch) {
			return `instagram.com/${profileMatch[1].toLowerCase()}`;
		}
	}

	// Extract canonical identifiers for TikTok
	if (normalized.includes("tiktok.com")) {
		// Video URLs
		const videoMatch = normalized.match(/tiktok\.com\/@([^/]+)\/video\/(\d+)/);
		if (videoMatch) {
			return `tiktok.com/@${videoMatch[1].toLowerCase()}/video/${videoMatch[2]}`;
		}

		// Short URLs (vm.tiktok.com)
		const shortMatch = normalized.match(/vm\.tiktok\.com\/([A-Za-z0-9]+)/);
		if (shortMatch) {
			return `vm.tiktok.com/${shortMatch[1]}`;
		}
	}

	return normalized;
}

/**
 * Check if a URL is from a supported platform
 */
export function isSupportedUrl(url: string): boolean {
	const normalized = url.toLowerCase();
	return normalized.includes("instagram.com") || normalized.includes("tiktok.com");
}
