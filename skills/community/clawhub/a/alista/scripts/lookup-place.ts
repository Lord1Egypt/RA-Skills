#!/usr/bin/env tsx
/**
 * Look up a place by name using Google Places API.
 *
 * Usage: tsx scripts/lookup-place.ts --name "Place Name" [--city "City"]
 * Output: JSON with verified place data
 */

import { PlaceVerifier } from "./lib/place-verifier";

// Parse args
const args = process.argv.slice(2);
let name = "";
let city = "";

for (let i = 0; i < args.length; i++) {
	if (args[i] === "--name" && args[i + 1]) {
		name = args[++i];
	} else if (args[i] === "--city" && args[i + 1]) {
		city = args[++i];
	} else if (!name) {
		// Allow positional first arg as name
		name = args[i];
	}
}

if (!name) {
	console.error(
		JSON.stringify({
			error: 'Usage: tsx scripts/lookup-place.ts --name "Place Name" [--city "City"]',
		}),
	);
	process.exit(1);
}

try {
	const googlePlacesApiKey = process.env.GOOGLE_PLACES_API_KEY;
	if (!googlePlacesApiKey) {
		throw new Error("GOOGLE_PLACES_API_KEY is required");
	}

	const verifier = new PlaceVerifier(googlePlacesApiKey);
	const result = await verifier.verify(name, city || undefined);

	if (result) {
		console.log(JSON.stringify(result, null, 2));
	} else {
		console.log(JSON.stringify({ found: false, query: name, city: city || null }));
	}
} catch (err) {
	console.error(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }));
	process.exit(1);
}
