import Database from "better-sqlite3";
import * as path from "node:path";
import * as fs from "node:fs";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ── Types ──────────────────────────────────────────────────────────────────

export interface PlaceRow {
	id: string;
	google_place_id: string | null;
	name: string;
	address: string | null;
	city: string | null;
	region: string | null;
	country: string | null;
	latitude: number | null;
	longitude: number | null;
	content_type: "restaurant" | "bar" | "cafe" | "event";
	google_types: string; // JSON string
	price_level: number | null;
	embedding: Buffer | null;
	source_url: string | null;
	source_platform: string | null;
	confidence: number | null;
	extraction_source: string | null;
	event_date: string | null;
	expires_at: string | null;
	user_notes: string | null;
	status: "active" | "archived" | "visited" | "expired";
	save_count: number;
	created_at: string;
	updated_at: string;
}

export interface SavePlaceParams {
	name: string;
	googlePlaceId?: string;
	address?: string;
	city?: string;
	region?: string;
	country?: string;
	latitude?: number;
	longitude?: number;
	contentType?: "restaurant" | "bar" | "cafe" | "event";
	googleTypes?: string[];
	priceLevel?: number;
	embedding?: number[];
	sourceUrl?: string;
	sourcePlatform?: string;
	confidence?: number;
	extractionSource?: string;
	eventDate?: string;
	expiresAt?: string;
	userNotes?: string;
}

export interface SearchResult {
	place: PlaceRow;
	score: number;
	matchType: "fts" | "vector" | "hybrid";
}

// ── Embedding helpers ──────────────────────────────────────────────────────

export function serializeEmbedding(embedding: number[]): Buffer {
	const float64 = new Float64Array(embedding);
	return Buffer.from(float64.buffer);
}

export function deserializeEmbedding(buffer: Buffer): number[] {
	const float64 = new Float64Array(
		buffer.buffer,
		buffer.byteOffset,
		buffer.byteLength / Float64Array.BYTES_PER_ELEMENT,
	);
	return Array.from(float64);
}

export function cosineSimilarity(a: number[], b: number[]): number {
	if (a.length !== b.length) return 0;
	let dot = 0;
	let normA = 0;
	let normB = 0;
	for (let i = 0; i < a.length; i++) {
		dot += a[i] * b[i];
		normA += a[i] * a[i];
		normB += b[i] * b[i];
	}
	const denom = Math.sqrt(normA) * Math.sqrt(normB);
	return denom === 0 ? 0 : dot / denom;
}

// ── Database singleton ─────────────────────────────────────────────────────

let dbInstance: Database.Database | null = null;

export function getDb(dbPath?: string): Database.Database {
	if (dbInstance) return dbInstance;

	const resolvedPath = dbPath ?? path.resolve(process.cwd(), "alista.db");
	dbInstance = new Database(resolvedPath);

	// Enable WAL mode for better concurrent read performance
	dbInstance.pragma("journal_mode = WAL");
	dbInstance.pragma("foreign_keys = ON");

	runMigrations(dbInstance);
	return dbInstance;
}

export function closeDb(): void {
	if (dbInstance) {
		dbInstance.close();
		dbInstance = null;
	}
}

// ── Migrations ─────────────────────────────────────────────────────────────

function runMigrations(db: Database.Database): void {
	const migrationsDir = path.resolve(__dirname, "../../migrations");
	if (!fs.existsSync(migrationsDir)) return;

	const files = fs
		.readdirSync(migrationsDir)
		.filter((f) => f.endsWith(".sql"))
		.sort();

	// Check current schema version
	let currentVersion = 0;
	try {
		const row = db.prepare("SELECT value FROM metadata WHERE key = 'schema_version'").get() as
			| { value: string }
			| undefined;
		if (row) currentVersion = parseInt(row.value, 10);
	} catch {
		// metadata table doesn't exist yet, version is 0
	}

	for (const file of files) {
		const match = file.match(/^(\d+)/);
		if (!match) continue;
		const fileVersion = parseInt(match[1], 10);
		if (fileVersion <= currentVersion) continue;

		const sql = fs.readFileSync(path.join(migrationsDir, file), "utf-8");
		db.exec(sql);
	}
}

// ── CRUD operations ────────────────────────────────────────────────────────

export function savePlace(params: SavePlaceParams): PlaceRow {
	const db = getDb();

	// Upsert on google_place_id if provided
	if (params.googlePlaceId) {
		const existing = getPlaceByGoogleId(params.googlePlaceId);
		if (existing) {
			db.prepare(
				`UPDATE places SET
					name = @name,
					address = @address,
					city = @city,
					region = @region,
					country = @country,
					latitude = @latitude,
					longitude = @longitude,
					content_type = @contentType,
					google_types = @googleTypes,
					price_level = @priceLevel,
					embedding = @embedding,
					source_url = @sourceUrl,
					source_platform = @sourcePlatform,
					confidence = @confidence,
					extraction_source = @extractionSource,
					event_date = @eventDate,
					expires_at = @expiresAt,
					user_notes = @userNotes,
					save_count = save_count + 1,
					updated_at = datetime('now')
				WHERE google_place_id = @googlePlaceId`,
			).run({
				name: params.name,
				address: params.address ?? existing.address,
				city: params.city ?? existing.city,
				region: params.region ?? existing.region,
				country: params.country ?? existing.country,
				latitude: params.latitude ?? existing.latitude,
				longitude: params.longitude ?? existing.longitude,
				contentType: params.contentType ?? existing.content_type,
				googleTypes: params.googleTypes
					? JSON.stringify(params.googleTypes)
					: existing.google_types,
				priceLevel: params.priceLevel ?? existing.price_level,
				embedding: params.embedding
					? serializeEmbedding(params.embedding)
					: existing.embedding,
				sourceUrl: params.sourceUrl ?? existing.source_url,
				sourcePlatform: params.sourcePlatform ?? existing.source_platform,
				confidence: params.confidence ?? existing.confidence,
				extractionSource: params.extractionSource ?? existing.extraction_source,
				eventDate: params.eventDate ?? existing.event_date,
				expiresAt: params.expiresAt ?? existing.expires_at,
				userNotes: params.userNotes ?? existing.user_notes,
				googlePlaceId: params.googlePlaceId,
			});
			return getPlaceByGoogleId(params.googlePlaceId)!;
		}
	}

	const result = db
		.prepare(
			`INSERT INTO places (
				name, google_place_id, address, city, region, country,
				latitude, longitude, content_type, google_types, price_level,
				embedding, source_url, source_platform, confidence,
				extraction_source, event_date, expires_at, user_notes
			) VALUES (
				@name, @googlePlaceId, @address, @city, @region, @country,
				@latitude, @longitude, @contentType, @googleTypes, @priceLevel,
				@embedding, @sourceUrl, @sourcePlatform, @confidence,
				@extractionSource, @eventDate, @expiresAt, @userNotes
			)`,
		)
		.run({
			name: params.name,
			googlePlaceId: params.googlePlaceId ?? null,
			address: params.address ?? null,
			city: params.city ?? null,
			region: params.region ?? null,
			country: params.country ?? null,
			latitude: params.latitude ?? null,
			longitude: params.longitude ?? null,
			contentType: params.contentType ?? "restaurant",
			googleTypes: JSON.stringify(params.googleTypes ?? []),
			priceLevel: params.priceLevel ?? null,
			embedding: params.embedding ? serializeEmbedding(params.embedding) : null,
			sourceUrl: params.sourceUrl ?? null,
			sourcePlatform: params.sourcePlatform ?? null,
			confidence: params.confidence ?? null,
			extractionSource: params.extractionSource ?? null,
			eventDate: params.eventDate ?? null,
			expiresAt: params.expiresAt ?? null,
			userNotes: params.userNotes ?? null,
		});

	return db
		.prepare("SELECT * FROM places WHERE rowid = ?")
		.get(result.lastInsertRowid) as PlaceRow;
}

export function getPlaceById(id: string): PlaceRow | null {
	const db = getDb();
	return (db.prepare("SELECT * FROM places WHERE id = ?").get(id) as PlaceRow) ?? null;
}

export function getPlaceByGoogleId(googlePlaceId: string): PlaceRow | null {
	const db = getDb();
	return (
		(db
			.prepare("SELECT * FROM places WHERE google_place_id = ?")
			.get(googlePlaceId) as PlaceRow) ?? null
	);
}

export function getAllPlaces(options?: {
	contentType?: string;
	status?: string;
	limit?: number;
}): PlaceRow[] {
	const db = getDb();
	const conditions: string[] = [];
	const params: Record<string, string | number> = {};

	if (options?.contentType) {
		conditions.push("content_type = @contentType");
		params.contentType = options.contentType;
	}
	if (options?.status) {
		conditions.push("status = @status");
		params.status = options.status;
	}

	const where = conditions.length > 0 ? `WHERE ${conditions.join(" AND ")}` : "";
	if (options?.limit) {
		const limitNum = Number(options.limit);
		if (!Number.isInteger(limitNum) || limitNum <= 0) {
			throw new Error("limit must be a positive integer");
		}
		params.limit = limitNum;
	}
	const limitClause = options?.limit ? "LIMIT @limit" : "";

	return db
		.prepare(`SELECT * FROM places ${where} ORDER BY updated_at DESC ${limitClause}`)
		.all(params) as PlaceRow[];
}

export function updatePlace(
	id: string,
	updates: Partial<SavePlaceParams>,
): PlaceRow | null {
	const db = getDb();
	const existing = getPlaceById(id);
	if (!existing) return null;

	const setClauses: string[] = [];
	const params: Record<string, unknown> = { id };

	if (updates.name !== undefined) {
		setClauses.push("name = @name");
		params.name = updates.name;
	}
	if (updates.googlePlaceId !== undefined) {
		setClauses.push("google_place_id = @googlePlaceId");
		params.googlePlaceId = updates.googlePlaceId;
	}
	if (updates.address !== undefined) {
		setClauses.push("address = @address");
		params.address = updates.address;
	}
	if (updates.city !== undefined) {
		setClauses.push("city = @city");
		params.city = updates.city;
	}
	if (updates.region !== undefined) {
		setClauses.push("region = @region");
		params.region = updates.region;
	}
	if (updates.country !== undefined) {
		setClauses.push("country = @country");
		params.country = updates.country;
	}
	if (updates.latitude !== undefined) {
		setClauses.push("latitude = @latitude");
		params.latitude = updates.latitude;
	}
	if (updates.longitude !== undefined) {
		setClauses.push("longitude = @longitude");
		params.longitude = updates.longitude;
	}
	if (updates.contentType !== undefined) {
		setClauses.push("content_type = @contentType");
		params.contentType = updates.contentType;
	}
	if (updates.googleTypes !== undefined) {
		setClauses.push("google_types = @googleTypes");
		params.googleTypes = JSON.stringify(updates.googleTypes);
	}
	if (updates.priceLevel !== undefined) {
		setClauses.push("price_level = @priceLevel");
		params.priceLevel = updates.priceLevel;
	}
	if (updates.embedding !== undefined) {
		setClauses.push("embedding = @embedding");
		params.embedding = serializeEmbedding(updates.embedding);
	}
	if (updates.sourceUrl !== undefined) {
		setClauses.push("source_url = @sourceUrl");
		params.sourceUrl = updates.sourceUrl;
	}
	if (updates.sourcePlatform !== undefined) {
		setClauses.push("source_platform = @sourcePlatform");
		params.sourcePlatform = updates.sourcePlatform;
	}
	if (updates.confidence !== undefined) {
		setClauses.push("confidence = @confidence");
		params.confidence = updates.confidence;
	}
	if (updates.extractionSource !== undefined) {
		setClauses.push("extraction_source = @extractionSource");
		params.extractionSource = updates.extractionSource;
	}
	if (updates.eventDate !== undefined) {
		setClauses.push("event_date = @eventDate");
		params.eventDate = updates.eventDate;
	}
	if (updates.expiresAt !== undefined) {
		setClauses.push("expires_at = @expiresAt");
		params.expiresAt = updates.expiresAt;
	}
	if (updates.userNotes !== undefined) {
		setClauses.push("user_notes = @userNotes");
		params.userNotes = updates.userNotes;
	}

	if (setClauses.length === 0) return existing;

	setClauses.push("updated_at = datetime('now')");

	db.prepare(`UPDATE places SET ${setClauses.join(", ")} WHERE id = @id`).run(params);
	return getPlaceById(id);
}

export function deletePlace(id: string): boolean {
	const db = getDb();
	const result = db.prepare("DELETE FROM places WHERE id = ?").run(id);
	return result.changes > 0;
}

// ── Search ─────────────────────────────────────────────────────────────────

export function searchPlaces(
	query: string,
	options?: {
		contentType?: string;
		limit?: number;
		queryEmbedding?: number[];
	},
): SearchResult[] {
	const db = getDb();
	const limit = options?.limit ?? 20;
	const K = 60; // RRF constant

	// Step 1: FTS5 search
	const ftsQuery = query
		.split(/\s+/)
		.filter(Boolean)
		.map((term) => `"${term.replace(/"/g, '""')}"`)
		.join(" OR ");

	let ftsCondition = "";
	const ftsParams: Record<string, string> = { query: ftsQuery };

	if (options?.contentType) {
		ftsCondition = "AND p.content_type = @contentType";
		ftsParams.contentType = options.contentType;
	}

	const ftsResults = db
		.prepare(
			`SELECT p.*, rank
			FROM places_fts fts
			JOIN places p ON p.rowid = fts.rowid
			WHERE places_fts MATCH @query
			${ftsCondition}
			AND p.status = 'active'
			ORDER BY rank
			LIMIT @limit`,
		)
		.all({ ...ftsParams, limit: limit * 2 }) as (PlaceRow & { rank: number })[];

	// If no vector query, return FTS results only
	if (!options?.queryEmbedding || ftsResults.length === 0) {
		return ftsResults.slice(0, limit).map((row, i) => ({
			place: stripExtraFields(row),
			score: 1 / (K + i + 1),
			matchType: "fts" as const,
		}));
	}

	// Step 2: Compute vector similarity for FTS results
	const queryEmb = options.queryEmbedding;
	const vectorScored = ftsResults
		.filter((row) => row.embedding !== null)
		.map((row) => ({
			row,
			similarity: cosineSimilarity(queryEmb, deserializeEmbedding(row.embedding!)),
		}))
		.sort((a, b) => b.similarity - a.similarity);

	// Build rank maps
	const ftsRankMap = new Map<string, number>();
	ftsResults.forEach((row, i) => ftsRankMap.set(row.id, i + 1));

	const vectorRankMap = new Map<string, number>();
	vectorScored.forEach((item, i) => vectorRankMap.set(item.row.id, i + 1));

	// Step 3: RRF fusion
	const allIds = Array.from(
		new Set([
			...Array.from(ftsRankMap.keys()),
			...Array.from(vectorRankMap.keys()),
		]),
	);
	const scored: { id: string; score: number; row: PlaceRow }[] = [];

	for (const id of allIds) {
		const ftsRank = ftsRankMap.get(id) ?? ftsResults.length + 1;
		const vecRank = vectorRankMap.get(id) ?? vectorScored.length + 1;
		const rrfScore = 1 / (K + ftsRank) + 1 / (K + vecRank);
		const row = ftsResults.find((r) => r.id === id) ?? vectorScored.find((v) => v.row.id === id)?.row;
		if (row) {
			scored.push({ id, score: rrfScore, row: stripExtraFields(row) });
		}
	}

	scored.sort((a, b) => b.score - a.score);

	return scored.slice(0, limit).map((item) => ({
		place: item.row,
		score: item.score,
		matchType: "hybrid" as const,
	}));
}

function stripExtraFields(row: PlaceRow & { rank?: number }): PlaceRow {
	const { rank: _rank, ...place } = row;
	return place;
}
