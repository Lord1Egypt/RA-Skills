/**
 * Place verification service using Google Places API.
 * Includes circuit breaker for reliability and graceful degradation.
 */

import { isSamePlaceName, normalizePlaceName, tokenOverlapScore } from "./utils/text";
import type { Place, PlaceVerifierInterface } from "./types";
import { ApiError, CONFIDENCE_THRESHOLDS, TIMEOUTS } from "./types";
import { CircuitBreaker, type CircuitState } from "./utils/circuit-breaker";
import { withRetry } from "./utils/retry";

/** Minimum similarity score to accept a Google Places match */
const MIN_MATCH_SCORE = CONFIDENCE_THRESHOLDS.placeMatch;

/** Lower threshold when address matching is used */
const MIN_MATCH_SCORE_WITH_ADDRESS = CONFIDENCE_THRESHOLDS.placeMatchWithAddress;

/** Categories that indicate unsupported place types */
const UNSUPPORTED_TYPES = [
	"library",
	"school",
	"hospital",
	"government",
	"local_government_office",
	"bank",
	"atm",
	"gas_station",
	"parking",
	"transit_station",
	"airport",
	"train_station",
	"bus_station",
	"pharmacy",
	"convenience_store",
	"grocery_store",
	"supermarket",
	// Localities (towns, cities, regions) - not actual establishments
	"locality",
	"sublocality",
	"political",
	"administrative_area_level_1",
	"administrative_area_level_2",
	"administrative_area_level_3",
	"country",
	"postal_code",
	"natural_feature",
	"neighborhood",
];

export class PlaceVerifier implements PlaceVerifierInterface {
	private readonly circuitBreaker: CircuitBreaker;

	constructor(private readonly googlePlacesApiKey: string) {
		this.circuitBreaker = new CircuitBreaker({
			threshold: 5, // 5 failures before opening
			resetTimeMs: 60_000, // 1 minute before trying again
			onStateChange: (state: string) => {
				console.warn(`[PlaceVerifier] Circuit breaker state: ${state}`);
			},
		});
	}

	/**
	 * Verify a place name using Google Places API.
	 * Returns null if no match found or circuit is open.
	 * @param query - The place name to search for
	 * @param locationHint - Optional city/neighborhood to narrow search
	 * @param address - Optional street address to boost matching accuracy
	 */
	async verify(query: string, locationHint?: string, address?: string): Promise<Place | null> {
		// Fast fail if circuit is open
		if (this.circuitBreaker.isOpen()) {
			console.log(`[PlaceVerifier] Circuit open, skipping verification for "${query}"`);
			return null;
		}

		try {
			const result = await this.circuitBreaker.execute(() =>
				withRetry(() => this.callGooglePlaces(query, locationHint, address), {
					maxRetries: 2, // Limit retries for latency
					baseDelayMs: 300,
				}),
			);

			return result;
		} catch (error) {
			console.error(`[PlaceVerifier] Error verifying "${query}":`, error);
			return null;
		}
	}

	/**
	 * Check if the circuit breaker is currently open
	 */
	isCircuitOpen(): boolean {
		return this.circuitBreaker.isOpen();
	}

	/**
	 * Get the current circuit breaker state
	 */
	getState(): CircuitState {
		return this.circuitBreaker.getState();
	}

	/**
	 * Call Google Places API (New) Text Search
	 */
	private async callGooglePlaces(
		query: string,
		locationHint?: string,
		address?: string,
	): Promise<Place | null> {
		// Include location in the text query for better results
		const textQuery = locationHint ? `${query} in ${locationHint}` : query;

		const resp = await fetch("https://places.googleapis.com/v1/places:searchText", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-Goog-Api-Key": this.googlePlacesApiKey,
				"X-Goog-FieldMask":
					"places.displayName,places.formattedAddress,places.location,places.types,places.primaryType,places.primaryTypeDisplayName,places.addressComponents",
			},
			body: JSON.stringify({
				textQuery,
				pageSize: 10, // Get more results to find best match
			}),
			signal: AbortSignal.timeout(TIMEOUTS.googlePlaces ?? 10000),
		});

		if (!resp.ok) {
			const errorText = await resp.text();
			console.error(`[PlaceVerifier] Google Places API error: ${resp.status}`, errorText);
			throw new ApiError(
				`Google Places API error: ${resp.status}`,
				resp.status,
				resp.status >= 500,
			);
		}

		const data = (await resp.json()) as GooglePlacesResponse;

		if (!data.places || data.places.length === 0) {
			console.log(`[PlaceVerifier] No results for "${query}"`);
			return null;
		}

		// Score each result by name similarity and find the best match
		return this.findBestMatch(query, data.places, address);
	}

	/**
	 * Find the best matching place from Google Places results
	 */
	private findBestMatch(
		query: string,
		results: GooglePlaceResult[],
		extractedAddress?: string,
	): Place | null {
		const normalizedQuery = normalizePlaceName(query);
		let bestMatch: GooglePlaceResult | null = null;
		let bestScore = 0;
		let hasAddressMatch = false;

		for (const result of results) {
			const displayName = result.displayName?.text;
			if (!displayName) continue;

			const normalizedResult = normalizePlaceName(displayName);
			const types = result.types ?? [];

			// Skip unsupported types (libraries, schools, etc.)
			if (this.isUnsupportedType(types)) {
				console.log(
					`[PlaceVerifier] Skipping unsupported type "${displayName}" (${types.join(", ")})`,
				);
				continue;
			}

			// Calculate similarity score
			let score = this.calculateSimilarityScore(
				normalizedQuery,
				normalizedResult,
				query,
				displayName,
			);

			// Bonus for food/drink types
			if (this.isFoodDrinkType(types)) {
				score += 0.1;
			}

			// Address matching bonus: +0.2 if addresses match
			let addressMatched = false;
			if (extractedAddress && result.formattedAddress) {
				const addressSimilarity = this.compareAddresses(extractedAddress, result.formattedAddress);
				if (addressSimilarity > 0.6) {
					score += 0.2;
					addressMatched = true;
					console.log(
						`[PlaceVerifier] Address match bonus for "${displayName}" (similarity: ${addressSimilarity.toFixed(2)})`,
					);
				}
			}

			if (score > bestScore) {
				bestScore = score;
				bestMatch = result;
				hasAddressMatch = addressMatched;
			}
		}

		// Use lower threshold if we have address matching
		const threshold = hasAddressMatch ? MIN_MATCH_SCORE_WITH_ADDRESS : MIN_MATCH_SCORE;

		// Only return if we have a good enough match
		if (!bestMatch || bestScore < threshold) {
			console.log(
				`[PlaceVerifier] No good match for "${query}" (best score: ${bestScore.toFixed(2)}, threshold: ${threshold}, match: "${bestMatch?.displayName?.text ?? "none"}")`,
			);
			return null;
		}

		console.log(
			`[PlaceVerifier] Matched "${query}" to "${bestMatch.displayName?.text}" (score: ${bestScore.toFixed(2)}, address match: ${hasAddressMatch})`,
		);

		return this.mapToPlace(bestMatch, bestScore);
	}

	/**
	 * Compare two addresses for similarity
	 * Normalizes street abbreviations and extracts key components
	 */
	private compareAddresses(extracted: string, googleAddress: string): number {
		const normalize = (addr: string): string => {
			return addr
				.toLowerCase()
				.replace(/[.,#]/g, "")
				.replace(/\bst\b/g, "street")
				.replace(/\bave\b/g, "avenue")
				.replace(/\bblvd\b/g, "boulevard")
				.replace(/\bdr\b/g, "drive")
				.replace(/\brd\b/g, "road")
				.replace(/\bln\b/g, "lane")
				.replace(/\bct\b/g, "court")
				.replace(/\bpl\b/g, "place")
				.replace(/\bpkwy\b/g, "parkway")
				.replace(/\bhwy\b/g, "highway")
				.replace(/\bste\b/g, "suite")
				.replace(/\bapt\b/g, "apartment")
				.replace(/\s+/g, " ")
				.trim();
		};

		const norm1 = normalize(extracted);
		const norm2 = normalize(googleAddress);

		// Improved pattern: capture street number + full street name (up to 4 words)
		const streetPattern = /^(\d+)\s+(\w+(?:\s+\w+){0,3})/;
		const match1 = norm1.match(streetPattern);
		const match2 = norm2.match(streetPattern);

		if (match1 && match2) {
			const [, num1, street1] = match1;
			const [, num2, street2] = match2;

			// Same street number
			if (num1 === num2) {
				// Check if street names share a common prefix (handles abbreviations)
				if (street1.startsWith(street2) || street2.startsWith(street1)) {
					return 0.9;
				}
				// Same number, first word matches = good confidence
				const words1 = street1.split(" ");
				const words2 = street2.split(" ");
				if (words1[0] === words2[0]) {
					return 0.7;
				}
				// Same number but different street = low confidence
				return 0.5;
			}
		}

		// Fallback: substring containment
		if (norm1.includes(norm2) || norm2.includes(norm1)) {
			const minLen = Math.min(norm1.length, norm2.length);
			const maxLen = Math.max(norm1.length, norm2.length);
			return 0.6 + 0.3 * (minLen / maxLen);
		}

		return 0;
	}

	/**
	 * Calculate similarity score between query and result
	 */
	private calculateSimilarityScore(
		normalizedQuery: string,
		normalizedResult: string,
		originalQuery: string,
		originalResult: string,
	): number {
		// Exact match after normalization
		if (normalizedResult === normalizedQuery) {
			return 1.0;
		}

		// One contains the other
		if (normalizedResult.includes(normalizedQuery) || normalizedQuery.includes(normalizedResult)) {
			const minLen = Math.min(normalizedResult.length, normalizedQuery.length);
			const maxLen = Math.max(normalizedResult.length, normalizedQuery.length);
			return 0.7 + 0.3 * (minLen / maxLen);
		}

		// Token overlap: all query tokens found in result → strong signal
		// Handles "Cafe 140B" matching "Café 140B at Ellerbeck B&B"
		const tokenScore = tokenOverlapScore(originalQuery, originalResult);
		if (tokenScore >= 1.0) {
			// All query tokens present in result
			const queryTokenCount = normalizedQuery.split(/\s+/).length;
			const resultTokenCount = normalizedResult.split(/\s+/).length;
			return 0.65 + 0.25 * (queryTokenCount / resultTokenCount);
		}
		if (tokenScore >= 0.8) {
			return 0.55 + 0.15 * tokenScore;
		}

		// Fuzzy match using similarity
		if (isSamePlaceName(originalQuery, originalResult, 0.5)) {
			return 0.5;
		}

		return 0;
	}

	/**
	 * Check if types indicate an unsupported place type
	 */
	private isUnsupportedType(types: string[]): boolean {
		return types.some((type) =>
			UNSUPPORTED_TYPES.some((unsupported) => type.includes(unsupported)),
		);
	}

	/**
	 * Check if types indicate a food/drink establishment
	 */
	private isFoodDrinkType(types: string[]): boolean {
		const foodDrinkTypes = [
			"restaurant",
			"bar",
			"cafe",
			"coffee",
			"food",
			"meal",
			"bakery",
			"pizza",
			"burger",
			"sushi",
			"brewery",
			"winery",
			"pub",
			"bistro",
			"diner",
		];
		return types.some((t) => foodDrinkTypes.some((keyword) => t.includes(keyword)));
	}

	/**
	 * Map Google Places result to Place object
	 */
	private mapToPlace(result: GooglePlaceResult, confidence: number): Place {
		const types = result.types ?? [];

		// Determine category from Google Places types
		// Default to "restaurant" as fallback (valid content type)
		let category = "restaurant";
		if (types.some((t) => t.includes("restaurant") || t.includes("meal"))) {
			category = "restaurant";
		} else if (types.some((t) => t.includes("bar") || t.includes("pub") || t.includes("brewery"))) {
			category = "bar";
		} else if (
			types.some((t) => t.includes("cafe") || t.includes("coffee") || t.includes("bakery"))
		) {
			category = "cafe";
		}

		// Extract city from address components or formatted address
		let locationStr: string | null = null;
		if (result.addressComponents) {
			const locality = result.addressComponents.find((c) => c.types?.includes("locality"));
			const region = result.addressComponents.find((c) =>
				c.types?.includes("administrative_area_level_1"),
			);
			const country = result.addressComponents.find((c) => c.types?.includes("country"));

			locationStr =
				[locality?.longText, region?.shortText, country?.shortText].filter(Boolean).join(", ") ||
				null;
		}

		// Fallback: extract from formatted address
		if (!locationStr && result.formattedAddress) {
			// Take everything after the first comma as location hint
			const parts = result.formattedAddress.split(",").map((p) => p.trim());
			if (parts.length >= 2) {
				locationStr = parts.slice(1).join(", ");
			}
		}

		return {
			name: result.displayName?.text ?? null,
			location: locationStr,
			address: result.formattedAddress ?? null,
			category,
			latitude: result.location?.latitude ?? null,
			longitude: result.location?.longitude ?? null,
			confidence,
			source: "google_places",
		};
	}
}

// ============================================================================
// Google Places API Types
// ============================================================================

interface GooglePlacesResponse {
	places?: GooglePlaceResult[];
}

interface GooglePlaceResult {
	displayName?: { text?: string; languageCode?: string };
	formattedAddress?: string;
	location?: { latitude?: number; longitude?: number };
	types?: string[];
	primaryType?: string;
	primaryTypeDisplayName?: { text?: string };
	addressComponents?: Array<{
		longText?: string;
		shortText?: string;
		types?: string[];
	}>;
}
