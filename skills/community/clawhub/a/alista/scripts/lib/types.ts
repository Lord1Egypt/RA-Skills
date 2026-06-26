/**
 * Types and interfaces for the social media extraction system.
 * Defines the contract between handlers, services, and the orchestrator.
 */

// ============================================================================
// Place Interface (inlined from alista-mvp/src/types.ts)
// ============================================================================

export interface Place {
	name: string | null;
	location: string | null;
	address: string | null; // Street address for verification
	category: string | null;
	latitude: number | null;
	longitude: number | null;
	confidence: number;
	source: string;
	// Database IDs (set after caching)
	placeId?: string | null; // ID in places table
	sourceContentId?: string | null; // ID in source_content table
}

// ============================================================================
// Platform & URL Types
// ============================================================================

export type Platform = "instagram" | "tiktok";

export type UrlType =
	| "post" // Single image/video post
	| "reel" // Short-form video (IG Reels)
	| "video" // TikTok video
	| "profile" // User/business profile page
	| "carousel" // Multi-media post (IG Sidecar)
	| "story"; // Ephemeral content

/**
 * Parsed URL with platform-specific context
 */
export interface ParsedUrl {
	platform: Platform;
	urlType: UrlType;
	identifier: string; // post ID, username, video ID, etc.
	originalUrl: string;
	resolvedUrl?: string; // For short URLs that were resolved
}

// ============================================================================
// Content Source Classification
// ============================================================================

/**
 * Whether content was posted BY a place or ABOUT a place
 */
export interface ContentSource {
	type: "by_place" | "about_place";
	confidence: number;
	signals: ContentSourceSignal[];
}

export type ContentSourceSignal =
	| "profile_url" // URL is a profile page
	| "business_username" // Username looks like a business
	| "location_matches_owner" // Location tag matches owner username
	| "business_caption_style" // Caption has first-person business voice
	| "tagged_business_account" // A business account is tagged in the image
	| "has_place_mentions" // Caption @mentions other places
	| "personal_username_pattern"; // Username looks like a person

// ============================================================================
// Metadata Types
// ============================================================================

/**
 * Metadata for a social media post
 */
export interface PostMetadata {
	caption: string;
	videoUrl: string | null;
	imageUrls?: string[];
	ownerUsername?: string;
	locationName?: string;
	locationCity?: string;
	locationId?: string; // Instagram location ID for verification
	locationSlug?: string; // URL-friendly location name
	mentions: string[];
	hashtags: string[];
	taggedUsers?: string[]; // Users tagged in image (different from @mentions)
	altText?: string; // Image alt text (often contains place names)
	transcript?: string; // Auto-generated video transcript
	postType?: "Image" | "Video" | "Sidecar";
}

/**
 * Metadata for a user/business profile
 */
export interface ProfileMetadata {
	username: string;
	displayName?: string; // Full display name (e.g., "Five Seeds" for @five5eeds)
	bio?: string;
	category?: string;
	followerCount?: number;
	isVerified?: boolean;
	isBusinessAccount?: boolean;
	externalUrl?: string;
}

// ============================================================================
// Extraction Results
// ============================================================================

export type ExtractionContentCategory = "supported" | "recipe" | "product" | "travel" | "other";

/**
 * Error codes for extraction failures
 */
export type ErrorCode =
	| "PRIVATE_ACCOUNT"
	| "STORY_EXPIRED"
	| "NO_PLACES_FOUND"
	| "PERSONAL_PROFILE"
	| "UNSUPPORTED_CONTENT"
	| "PLATFORM_ERROR"
	| "RATE_LIMITED"
	| "VIDEO_TOO_LARGE";

/**
 * Structured error information for failed extractions
 */
export interface ExtractionError {
	code: ErrorCode;
	message: string;
	recoverable: boolean;
	userPrompt?: string; // What to ask user if recoverable
}

/**
 * Services that were invoked during extraction (for debugging/metrics)
 */
export type ServiceUsed =
	| "apify"
	| "og_tags"
	| "oembed"
	| "gemini_image"
	| "gemini_video"
	| "google_places";

/**
 * Unified extraction result across all platforms
 */
export interface ExtractionResult {
	places: Place[];
	contentCategory: ExtractionContentCategory;
	contentSource?: ContentSource;
	metadata?: {
		platform: Platform;
		urlType: UrlType;
		ownerUsername?: string;
		postType?: "Image" | "Video" | "Sidecar";
		isListicle?: boolean;
		totalPlacesInContent?: number;
	};
	error?: ExtractionError;
	// Observability
	durationMs?: number;
	servicesUsed?: ServiceUsed[];
}

// ============================================================================
// Handler Interfaces
// ============================================================================

/**
 * Base interface for platform-specific handlers.
 * Each platform implements this interface independently.
 */
export interface PlatformHandler {
	/**
	 * Platform identifier
	 */
	readonly platform: Platform;

	/**
	 * Check if this handler can process the given URL
	 */
	canHandle(url: string): boolean;

	/**
	 * Parse URL into structured components
	 */
	parseUrl(url: string): ParsedUrl | null;

	/**
	 * Extract places from the URL
	 */
	extract(parsedUrl: ParsedUrl): Promise<ExtractionResult>;
}

// ============================================================================
// Service Interfaces
// ============================================================================

/**
 * Interface for fetching metadata from social platforms
 */
export interface MetadataFetcher {
	getInstagramPost(url: string): Promise<PostMetadata | null>;
	getInstagramProfile(username: string): Promise<ProfileMetadata | null>;
	getTiktokVideo(url: string): Promise<PostMetadata | null>;
	getTiktokProfile(username: string): Promise<ProfileMetadata | null>;
}

/**
 * Interface for verifying places via external APIs (Google Places)
 */
export interface PlaceVerifierInterface {
	verify(query: string, locationHint?: string, address?: string): Promise<Place | null>;
	isCircuitOpen(): boolean;
	getState(): "closed" | "open" | "half-open";
}

// ============================================================================
// User Input Types
// ============================================================================

export type UserInputStatus =
	| "verified" // User input matched in Google Places
	| "unverified" // No Google Places match found
	| "needs_confirmation" // Partial match, needs user confirmation
	| "needs_clarification" // Input too vague
	| "needs_location" // Chain restaurant needs location
	| "duplicate"; // User already has this saved

/**
 * Result from user input extraction
 */
export interface UserInputResult {
	status: UserInputStatus;
	places: Place[];
	message: string;
	suggestedPlace?: Place; // For confirmation flow
	originalInput?: string; // For confirmation flow
}

/**
 * Context for user input extraction
 */
export interface UserInputContext {
	locationHint?: string; // User's city or from pending URL
	pendingUrl?: string; // Original URL that failed extraction
	pendingPlatform?: Platform; // Platform of the failed URL
}

// ============================================================================
// Error Classes
// ============================================================================

/**
 * Custom error class that preserves HTTP status for retry logic
 */
export class ApiError extends Error {
	constructor(
		message: string,
		public readonly status: number,
		public readonly retryable: boolean,
	) {
		super(message);
		this.name = "ApiError";
	}
}

// ============================================================================
// Constants
// ============================================================================

/**
 * Platform-specific timeouts based on expected latency
 */
export const TIMEOUTS = {
	apify: {
		instagram: 90_000, // 90s - Instagram scraper is slow
		tiktok: 120_000, // 120s - TikTok video download takes longer
	},
	googlePlaces: 10_000, // 10s
	ogTags: 15_000, // 15s for direct page fetch
	oembed: 10_000, // 10s for oEmbed
} as const;

/**
 * Confidence thresholds for various decisions
 */
export const CONFIDENCE_THRESHOLDS = {
	placeMatch: 0.55, // Minimum score to accept a Google Places match
	placeMatchWithAddress: 0.4, // Lower threshold when address matches
	byPlaceClassification: 0.7, // Threshold for BY_PLACE classification
	includePlace: 0.5, // Minimum confidence to include a place in results
	userConfirmation: {
		high: 0.6, // Above this, save directly
		low: 0.35, // Below this, save as unverified; between = ask for confirmation
	},
} as const;
