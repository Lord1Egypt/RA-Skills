#!/usr/bin/env tsx
/**
 * Generate nudge suggestions from saved places.
 *
 * Usage: tsx scripts/nudge.ts [--count 3]
 * Output: JSON with suggested places for the weekend
 */

import { getAllPlaces, getDb } from "./lib/db";
import { getSuggestions } from "./lib/nudge-scorer";

const args = process.argv.slice(2);
let count = 3;

for (let i = 0; i < args.length; i++) {
	if (args[i] === "--count" && args[i + 1]) {
		count = Number.parseInt(args[++i], 10);
	}
}

try {
	const db = getDb();
	const places = getAllPlaces({ status: "active" });

	if (places.length === 0) {
		console.log(
			JSON.stringify(
				{
					suggestions: [],
					message: "No saved places yet. Save some places first!",
				},
				null,
				2,
			),
		);
		process.exit(0);
	}

	const suggestions = getSuggestions(places, count);

	console.log(
		JSON.stringify(
			{
				totalSaved: places.length,
				count: suggestions.length,
				suggestions: suggestions.map((p, i) => ({
					rank: i + 1,
					name: p.name,
					city: p.city,
					category: p.content_type,
					address: p.address,
					notes: p.user_notes,
					eventDate: p.event_date,
					savedAt: p.created_at,
				})),
			},
			null,
			2,
		),
	);
} catch (err) {
	console.error(
		JSON.stringify({ error: err instanceof Error ? err.message : String(err) }),
	);
	process.exit(1);
}
