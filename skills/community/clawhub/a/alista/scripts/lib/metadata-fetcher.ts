/**
 * Metadata fetcher service for social media platforms.
 * Handles Apify scraping, OG tags, and oEmbed as fallbacks.
 */

import type { MetadataFetcher, PostMetadata, ProfileMetadata } from "./types";
import { ApiError, TIMEOUTS } from "./types";
import { decodeHtmlEntities, extractHashtags, extractMentions, extractOgTags } from "./utils/html";

export class SocialMetadataFetcher implements MetadataFetcher {
	constructor(private readonly apifyApiKey?: string) {}

	// ============================================================================
	// Instagram
	// ============================================================================

	/**
	 * Fetch Instagram post metadata via Apify, falling back to OG tags
	 */
	async getInstagramPost(url: string): Promise<PostMetadata | null> {
		// Try Apify first if available (better data quality + video URL)
		if (this.apifyApiKey) {
			console.log("[MetadataFetcher] Instagram: Trying Apify scraper...");
			const apifyData = await this.getInstagramPostFromApify(url);

			if (apifyData) {
				return apifyData;
			}
		}

		// Fallback: fetch OG meta tags directly
		console.log("[MetadataFetcher] Instagram: Falling back to OG tags");
		return this.getInstagramPostFromOgTags(url);
	}

	/**
	 * Fetch Instagram profile metadata
	 */
	async getInstagramProfile(username: string): Promise<ProfileMetadata | null> {
		if (!this.apifyApiKey) {
			console.log("[MetadataFetcher] Instagram profile: No Apify key, skipping");
			return null;
		}

		try {
			const actorId = "apify~instagram-scraper";
			const runUrl = `https://api.apify.com/v2/acts/${actorId}/run-sync-get-dataset-items?token=${this.apifyApiKey}`;

			const resp = await fetch(runUrl, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					directUrls: [`https://www.instagram.com/${username}/`],
					resultsType: "details",
					resultsLimit: 1,
				}),
				signal: AbortSignal.timeout(TIMEOUTS.apify.instagram),
			});

			if (!resp.ok) {
				console.error("[MetadataFetcher] Apify Instagram profile request failed:", resp.status);
				return null;
			}

			const data = (await resp.json()) as Array<ApifyInstagramProfile>;

			if (!data || data.length === 0) {
				console.log("[MetadataFetcher] Apify Instagram profile returned no data");
				return null;
			}

			const profile = data[0];
			return {
				username: profile.username ?? username,
				displayName: profile.fullName,
				bio: profile.biography,
				category: profile.businessCategoryName,
				followerCount: profile.followersCount,
				isVerified: profile.verified,
				isBusinessAccount: profile.isBusinessAccount,
				externalUrl: profile.externalUrl,
			};
		} catch (e) {
			console.error("[MetadataFetcher] Apify Instagram profile failed:", e);
			return null;
		}
	}

	private async getInstagramPostFromApify(url: string): Promise<PostMetadata | null> {
		try {
			const actorId = "apify~instagram-scraper";
			const runUrl = `https://api.apify.com/v2/acts/${actorId}/run-sync-get-dataset-items?token=${this.apifyApiKey}`;

			const resp = await fetch(runUrl, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					directUrls: [url],
					resultsType: "posts",
					resultsLimit: 1,
				}),
				signal: AbortSignal.timeout(TIMEOUTS.apify.instagram),
			});

			if (!resp.ok) {
				console.error("[MetadataFetcher] Apify Instagram request failed:", resp.status);
				return null;
			}

			const data = (await resp.json()) as Array<ApifyInstagramPost>;

			if (!data || data.length === 0) {
				console.log("[MetadataFetcher] Apify Instagram returned no data");
				return null;
			}

			const post = data[0];

			// Handle restricted page partial data (Instagram blocks full scrape)
			if (post.error === "restricted_page") {
				console.log("[MetadataFetcher] Apify Instagram: restricted page, using partial data");

				// Extract caption from description field
				// Format: "X likes, Y comments - username on DATE: \"CAPTION\". "
				let caption = "";
				if (post.description) {
					const captionMatch = post.description.match(/:\s*"(.+)"\.?\s*$/s);
					caption = captionMatch?.[1] ?? post.description;
				}

				// Extract username from title field
				// Format: "Display Name (@username) • Instagram reel"
				let ownerUsername: string | undefined;
				if (post.title) {
					const usernameMatch = post.title.match(/@([a-zA-Z0-9._]+)\)/);
					ownerUsername = usernameMatch?.[1];
				}

				const mentions = extractMentions(caption);
				const hashtags = extractHashtags(caption);

				return {
					caption,
					videoUrl: null, // Not available in restricted mode
					imageUrls: post.image ? [post.image] : undefined,
					ownerUsername,
					mentions,
					hashtags,
					postType: post.title?.includes("reel") ? "Video" : undefined,
				};
			}

			// Extract image URLs for carousel/sidecar posts
			let imageUrls: string[] = [];
			const altTexts: string[] = [];
			if (post.type === "Sidecar" && post.childPosts) {
				// Carousel post - get all image URLs and alt texts
				for (const child of post.childPosts) {
					if (child.type === "Image" && child.displayUrl) {
						imageUrls.push(child.displayUrl);
						if (child.alt) altTexts.push(child.alt);
					}
				}
			} else if (post.type === "Image" && post.displayUrl) {
				// Single image post
				imageUrls = [post.displayUrl];
				if (post.alt) altTexts.push(post.alt);
			}

			// Extract tagged usernames
			const taggedUsers = post.taggedUsers?.map((u) => u.username).filter(Boolean) as
				| string[]
				| undefined;

			// Combine alt texts
			const combinedAltText = altTexts.length > 0 ? altTexts.join(" | ") : (post.alt ?? undefined);

			return {
				caption: post.caption ?? "",
				videoUrl: post.videoUrl ?? null,
				imageUrls: imageUrls.length > 0 ? imageUrls : undefined,
				ownerUsername: post.ownerUsername,
				locationName: post.locationName,
				locationId: post.locationId,
				locationSlug: post.locationSlug,
				mentions: post.mentions ?? [],
				hashtags: post.hashtags ?? [],
				taggedUsers,
				altText: combinedAltText,
				transcript: post.transcript,
				postType: post.type,
			};
		} catch (e) {
			console.error("[MetadataFetcher] Apify Instagram scrape failed:", e);
			return null;
		}
	}

	private async getInstagramPostFromOgTags(url: string): Promise<PostMetadata | null> {
		try {
			const resp = await fetch(url, {
				headers: {
					"User-Agent":
						"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
					Accept:
						"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
					"Accept-Language": "en-US,en;q=0.9",
					"Accept-Encoding": "gzip, deflate, br",
					"Cache-Control": "no-cache",
					Pragma: "no-cache",
					"Sec-Fetch-Dest": "document",
					"Sec-Fetch-Mode": "navigate",
					"Sec-Fetch-Site": "none",
					"Sec-Fetch-User": "?1",
					"Upgrade-Insecure-Requests": "1",
				},
				signal: AbortSignal.timeout(TIMEOUTS.ogTags),
				redirect: "follow",
			});

			if (!resp.ok) {
				console.error("[MetadataFetcher] Failed to fetch Instagram page:", resp.status);
				return null;
			}

			const html = await resp.text();
			const ogTags = extractOgTags(html);

			// Prefer the longer content - og:title often has the full caption on Instagram
			const ogTitle = ogTags.title ?? "";
			const ogDescription = ogTags.description ?? "";
			const caption = ogTitle.length > ogDescription.length ? ogTitle : ogDescription || ogTitle;

			const mentions = extractMentions(caption);
			const hashtags = extractHashtags(caption);

			// Try to extract owner username from OG title format "Username on Instagram"
			const ownerMatch = ogTitle.match(/^([^:]+) on Instagram/);
			const ownerUsername = ownerMatch?.[1];

			// Get image URL from OG tags
			const imageUrls = ogTags.image ? [ogTags.image] : undefined;

			return {
				caption,
				videoUrl: null, // OG tags don't give us video URL
				imageUrls,
				ownerUsername,
				mentions,
				hashtags,
			};
		} catch (e) {
			console.error("[MetadataFetcher] Error fetching Instagram OG tags:", e);
			return null;
		}
	}

	// ============================================================================
	// TikTok
	// ============================================================================

	/**
	 * Fetch TikTok video metadata via oEmbed and Apify
	 */
	async getTiktokVideo(url: string): Promise<PostMetadata | null> {
		// Try oEmbed first (free, fast)
		const oembedData = await this.getTiktokOembed(url);

		// If oEmbed has a caption, check if we need more data
		if (oembedData?.title) {
			// If caption looks like it has place names, use it directly
			if (this.captionLikelyHasPlaceNames(oembedData.title)) {
				console.log("[MetadataFetcher] TikTok: Using oEmbed caption (likely has place names)");
				return {
					caption: oembedData.title,
					videoUrl: null, // oEmbed doesn't give us video URL
					ownerUsername: oembedData.author_name ?? "",
					mentions: [],
					hashtags: [],
				};
			}
		}

		// Try Apify for richer metadata + video URL
		if (this.apifyApiKey) {
			console.log("[MetadataFetcher] TikTok: Trying Apify scraper...");
			const apifyData = await this.getTiktokFromApify(url);

			if (apifyData) {
				return apifyData;
			}
		}

		// Fall back to oEmbed if available
		if (oembedData?.title) {
			console.log("[MetadataFetcher] TikTok: Falling back to oEmbed caption");
			return {
				caption: oembedData.title,
				videoUrl: null,
				ownerUsername: oembedData.author_name ?? "",
				mentions: [],
				hashtags: [],
			};
		}

		return null;
	}

	/**
	 * Fetch TikTok profile metadata
	 */
	async getTiktokProfile(username: string): Promise<ProfileMetadata | null> {
		// TikTok profile fetching is more limited
		// For now, return basic info
		// TODO: Implement Apify profile scraping if needed
		console.log("[MetadataFetcher] TikTok profile: Not implemented, returning minimal data");
		return {
			username,
		};
	}

	private async getTiktokOembed(
		url: string,
	): Promise<{ title?: string; author_name?: string } | null> {
		try {
			const resp = await fetch(`https://www.tiktok.com/oembed?url=${encodeURIComponent(url)}`, {
				signal: AbortSignal.timeout(TIMEOUTS.oembed),
			});

			if (!resp.ok) {
				console.log("[MetadataFetcher] TikTok oEmbed failed:", resp.status);
				return null;
			}

			return (await resp.json()) as { title?: string; author_name?: string };
		} catch (e) {
			console.error("[MetadataFetcher] TikTok oEmbed error:", e);
			return null;
		}
	}

	private async getTiktokFromApify(url: string): Promise<PostMetadata | null> {
		try {
			const actorId = "clockworks~tiktok-scraper";
			const runUrl = `https://api.apify.com/v2/acts/${actorId}/run-sync-get-dataset-items?token=${this.apifyApiKey}`;

			const resp = await fetch(runUrl, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					postURLs: [url],
					resultsPerPage: 1,
					shouldDownloadVideos: true, // Enable video downloads
				}),
				signal: AbortSignal.timeout(TIMEOUTS.apify.tiktok),
			});

			if (!resp.ok) {
				console.error("[MetadataFetcher] Apify TikTok request failed:", resp.status);
				return null;
			}

			const data = (await resp.json()) as Array<ApifyTiktokPost>;

			if (!data || data.length === 0) {
				console.log("[MetadataFetcher] Apify TikTok returned no data");
				return null;
			}

			const post = data[0];
			const videoUrl = post.mediaUrls?.[0] ?? null;

			if (!videoUrl) {
				console.log("[MetadataFetcher] Apify TikTok: no video download URL found");
			}

			return {
				caption: post.text ?? "",
				videoUrl,
				ownerUsername: post.authorMeta?.name ?? post.authorMeta?.nickName ?? "",
				mentions: [],
				hashtags: [],
			};
		} catch (e) {
			console.error("[MetadataFetcher] Apify TikTok scrape failed:", e);
			return null;
		}
	}

	// ============================================================================
	// Helpers
	// ============================================================================

	/**
	 * Quick heuristic to check if a caption likely contains specific place names.
	 * Used to decide whether to skip expensive video analysis.
	 */
	private captionLikelyHasPlaceNames(caption: string): boolean {
		// If caption is very short, probably doesn't have place names
		if (caption.length < 30) return false;

		// Patterns that suggest place names are present
		const placeIndicators = [
			/@[A-Za-z]/, // @mentions (often restaurant handles)
			/📍/, // Location pin emoji
			/→\s*[A-Z]/, // Arrow followed by capitalized name
			/\bat\s+[A-Z]/, // "at [Place Name]"
			/\btried\s+[A-Z]/, // "tried [Place Name]"
			/:\s*[A-Z][a-z]+/, // ": [Place Name]"
			/\d\.\s*[A-Z]/, // "1. [Place Name]" (listicle format)
		];

		for (const pattern of placeIndicators) {
			if (pattern.test(caption)) {
				return true;
			}
		}

		// Patterns that suggest NO place names (generic listicle teaser)
		const genericPatterns = [
			/^\d+\s+(new\s+)?(spots|places|restaurants|cafes|bars)/i,
			/here are \d+/i,
			/top \d+/i,
			/best \d+/i,
			/must try/i,
			/worth.*(try|visit)/i,
		];

		for (const pattern of genericPatterns) {
			if (pattern.test(caption)) {
				// These suggest a listicle WITHOUT the actual names in caption
				return false;
			}
		}

		// Default: assume caption might have places if it's long enough
		return caption.length > 100;
	}
}

// ============================================================================
// Apify Response Types
// ============================================================================

interface ApifyInstagramPost {
	caption?: string;
	ownerUsername?: string;
	locationName?: string;
	locationId?: string; // Instagram location ID for verification
	locationSlug?: string; // URL-friendly location name
	hashtags?: string[];
	mentions?: string[];
	taggedUsers?: Array<{ username?: string }>; // Users tagged in image (different from @mentions)
	alt?: string; // Image alt text (often contains place names)
	transcript?: string; // Auto-generated video transcript
	videoUrl?: string;
	displayUrl?: string;
	type?: "Video" | "Image" | "Sidecar";
	childPosts?: Array<{
		type?: "Video" | "Image";
		displayUrl?: string;
		videoUrl?: string;
		alt?: string;
	}>;
	// Restricted page fields (partial data mode)
	error?: string; // "restricted_page" when Instagram blocks full scrape
	errorDescription?: string;
	description?: string; // Full caption in "X likes, Y comments - user on DATE: \"CAPTION\"" format
	title?: string; // "Display Name (@username) • Instagram reel/post"
	image?: string; // Thumbnail URL in restricted mode
}

interface ApifyInstagramProfile {
	username?: string;
	fullName?: string; // Display name (e.g., "Five Seeds" for @five5eeds)
	biography?: string;
	businessCategoryName?: string;
	followersCount?: number;
	verified?: boolean;
	isBusinessAccount?: boolean;
	externalUrl?: string;
}

interface ApifyTiktokPost {
	text?: string;
	mediaUrls?: string[];
	authorMeta?: {
		name?: string;
		nickName?: string;
	};
}
