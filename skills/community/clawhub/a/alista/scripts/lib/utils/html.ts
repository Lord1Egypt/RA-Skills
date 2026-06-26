/**
 * HTML utility functions for parsing social media content.
 */

/**
 * Decode HTML entities in a string.
 * Common in OG meta tags and API responses.
 */
export function decodeHtmlEntities(text: string): string {
	return text
		.replace(/&amp;/g, "&")
		.replace(/&quot;/g, '"')
		.replace(/&#39;/g, "'")
		.replace(/&lt;/g, "<")
		.replace(/&gt;/g, ">")
		.replace(/&#x([0-9a-fA-F]+);/g, (_, hex) => String.fromCodePoint(Number.parseInt(hex, 16)))
		.replace(/&#(\d+);/g, (_, dec) => String.fromCodePoint(Number.parseInt(dec, 10)))
		.replace(/&nbsp;/g, " ")
		.replace(/&#xa0;/g, " ")
		.replace(/\u2028/g, "\n"); // Line separator
}

/**
 * Extract Open Graph meta tags from HTML.
 */
export function extractOgTags(html: string): {
	title?: string;
	description?: string;
	image?: string;
} {
	const ogTitleMatch =
		html.match(/<meta property="og:title" content="([^"]+)"/) ||
		html.match(/<meta content="([^"]+)" property="og:title"/);
	const ogTitle = ogTitleMatch?.[1] ? decodeHtmlEntities(ogTitleMatch[1]) : undefined;

	const ogDescMatch =
		html.match(/<meta property="og:description" content="([^"]+)"/) ||
		html.match(/<meta content="([^"]+)" property="og:description"/);
	const ogDescription = ogDescMatch?.[1] ? decodeHtmlEntities(ogDescMatch[1]) : undefined;

	const ogImageMatch =
		html.match(/<meta property="og:image" content="([^"]+)"/) ||
		html.match(/<meta content="([^"]+)" property="og:image"/);
	const ogImage = ogImageMatch?.[1] ? decodeHtmlEntities(ogImageMatch[1]) : undefined;

	return {
		title: ogTitle,
		description: ogDescription,
		image: ogImage,
	};
}

/**
 * Extract @mentions from text
 */
export function extractMentions(text: string): string[] {
	const matches = text.match(/@([A-Za-z][A-Za-z0-9_.]+)/g) ?? [];
	return matches.map((m) => m.slice(1));
}

/**
 * Extract #hashtags from text
 */
export function extractHashtags(text: string): string[] {
	const matches = text.match(/#([A-Za-z][A-Za-z0-9_]+)/g) ?? [];
	return matches.map((h) => h.slice(1));
}
