import { differenceInDays, isBefore, parseISO } from "date-fns";
import type { PlaceRow } from "./db";

/**
 * Calculate urgency score for items with expiration or event dates.
 * Returns 0-1 where 1 = extremely urgent (expires/happens within 3 days)
 */
export function calculateUrgencyScore(place: PlaceRow, now: Date): number {
	const expiresAt = place.expires_at ? parseISO(place.expires_at) : null;
	const eventDate = place.event_date ? parseISO(place.event_date) : null;

	const urgentDate =
		expiresAt && eventDate
			? isBefore(expiresAt, eventDate)
				? expiresAt
				: eventDate
			: expiresAt || eventDate;

	if (!urgentDate) return 0;
	if (isBefore(urgentDate, now)) return 0;

	const daysUntil = differenceInDays(urgentDate, now);

	if (daysUntil <= 3) return 1.0;
	if (daysUntil <= 7) return 0.7 + (0.3 * (7 - daysUntil)) / 4;
	if (daysUntil <= 14) return 0.4 + (0.3 * (14 - daysUntil)) / 7;
	return Math.max(0, 0.4 * (1 - (daysUntil - 14) / 30));
}

/**
 * Get top-N suggestions from a list of places using scoring algorithm.
 * Scoring: exponential freshness decay + urgency + confidence + diversity bonus
 */
export function getSuggestions(places: PlaceRow[], count = 3): PlaceRow[] {
	if (places.length <= count) return places;

	const now = new Date();
	const HALF_LIFE_DAYS = 60;
	const DECAY_CONSTANT = Math.LN2 / HALF_LIFE_DAYS;

	const scored: Array<{ place: PlaceRow; score: number }> = [];

	for (const place of places) {
		const createdAt = parseISO(place.created_at);
		const daysAgo = differenceInDays(now, createdAt);

		// Exponential decay: 1.0 at day 0, 0.5 at day 60
		const freshness = Math.exp(-DECAY_CONSTANT * daysAgo);

		// Confidence from extraction (default 0.5)
		const confidence = place.confidence ?? 0.5;

		// Urgency score
		const urgency = calculateUrgencyScore(place, now);

		// Random factor
		const randomness = Math.random() * (0.1 + 0.2 * (1 - freshness));

		// Combined score
		const score =
			urgency > 0
				? confidence * 0.3 +
					freshness * 0.25 +
					urgency * 0.4 +
					randomness * 0.05
				: confidence * 0.4 + freshness * 0.45 + randomness * 0.15;

		scored.push({ place, score });
	}

	scored.sort((a, b) => b.score - a.score);

	// Select with content type diversity
	const selected: PlaceRow[] = [];
	const typesUsed = new Set<string>();

	for (const { place } of scored) {
		const contentType = place.content_type || "other";
		if (!typesUsed.has(contentType) || selected.length < count) {
			selected.push(place);
			typesUsed.add(contentType);
		}
		if (selected.length >= count) break;
	}

	return selected;
}
