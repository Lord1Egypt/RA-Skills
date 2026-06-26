#!/usr/bin/env tsx
/**
 * Save a place to the local database.
 *
 * Usage: tsx scripts/save-place.ts --name "Place Name" [--city "City"] [--category restaurant|bar|cafe|event] [--notes "Notes"] [--verify]
 * Output: JSON confirmation of saved place
 */

import { savePlace, getDb, type SavePlaceParams } from "./lib/db";
import { PlaceVerifier } from "./lib/place-verifier";

// Parse args
const args = process.argv.slice(2);
let name = "";
let city = "";
let category: "restaurant" | "bar" | "cafe" | "event" = "restaurant";
let notes = "";
let verify = false;
let sourceUrl = "";

for (let i = 0; i < args.length; i++) {
	switch (args[i]) {
		case "--name":
			name = args[++i];
			break;
		case "--city":
			city = args[++i];
			break;
		case "--category":
			category = args[++i] as typeof category;
			break;
		case "--notes":
			notes = args[++i];
			break;
		case "--source-url":
			sourceUrl = args[++i];
			break;
		case "--verify":
			verify = true;
			break;
		default:
			if (!name) name = args[i];
	}
}

if (!name) {
	console.error(
		JSON.stringify({
			error: 'Usage: tsx scripts/save-place.ts --name "Place Name" [--city "City"] [--category restaurant] [--notes "Notes"] [--verify]',
		}),
	);
	process.exit(1);
}

try {
	let placeData: SavePlaceParams = {
		name,
		city: city || undefined,
		contentType: category,
		userNotes: notes || undefined,
		sourceUrl: sourceUrl || undefined,
	};

	// Optionally verify with Google Places
	if (verify) {
		const googlePlacesApiKey = process.env.GOOGLE_PLACES_API_KEY;
		if (!googlePlacesApiKey) {
			throw new Error("GOOGLE_PLACES_API_KEY is required for --verify");
		}

		const verifier = new PlaceVerifier(googlePlacesApiKey);
		const verified = await verifier.verify(name, city || undefined);

		if (verified) {
			placeData = {
				...placeData,
				name: verified.name ?? name,
				address: verified.address ?? undefined,
				city: verified.location?.split(",")[0]?.trim() ?? city,
				region: verified.location?.split(",")[1]?.trim(),
				latitude: verified.latitude ?? undefined,
				longitude: verified.longitude ?? undefined,
				contentType: (verified.category as SavePlaceParams["contentType"]) ?? category,
				confidence: verified.confidence,
				extractionSource: "google_places",
			};
		}
	}

	// Save to database
	const db = getDb();
	const saved = savePlace(placeData);

	console.log(
		JSON.stringify(
			{
				saved: true,
				place: {
					id: saved.id,
					name: saved.name,
					city: saved.city,
					category: saved.content_type,
					address: saved.address,
					verified: verify && !!placeData.confidence,
				},
			},
			null,
			2,
		),
	);
} catch (err) {
	console.error(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }));
	process.exit(1);
}
