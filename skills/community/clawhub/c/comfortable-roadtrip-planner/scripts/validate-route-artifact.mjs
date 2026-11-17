#!/usr/bin/env node
import { loadTripArtifact, normalizeImages, normalizeWeather, repoRelative } from "./lib/trip-artifact.mjs";

const filePath = process.argv[2];
if (!filePath) {
  console.error("Usage: node scripts/validate-route-artifact.mjs <artifact.html>");
  process.exit(2);
}

const strict = process.argv.includes("--strict") || filePath.includes("/examples/") || filePath.startsWith("examples/");
const result = {
  errors: [],
  warnings: []
};

function fail(message) {
  result.errors.push(message);
}

function warn(message) {
  result.warnings.push(message);
}

function recommended(message) {
  if (strict) fail(message);
  else warn(message);
}

function hasText(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function isNumber(value) {
  return Number.isFinite(Number(value));
}

function asArray(value) {
  return Array.isArray(value) ? value : [];
}

function linkLooksValid(link) {
  return Array.isArray(link) && link.length === 2 && hasText(link[0]) && /^https?:\/\//.test(String(link[1]));
}

function validateArtifact() {
  let artifact;
  try {
    artifact = loadTripArtifact(filePath);
  } catch (error) {
    fail(error.message);
    return;
  }

  const { html, tripMeta, tripDays } = artifact;
  validateHtmlCapabilities(html);
  validatePrivacy(html);
  validateTripMeta(tripMeta);
  validateDays(tripDays);
}

function validateHtmlCapabilities(html) {
  const requiredSnippets = [
    ["Apple Maps provider", "maps.apple.com"],
    ["Google Maps provider", "google.com/maps"],
    ["Amap provider", "uri.amap.com"],
    ["Baidu provider", "api.map.baidu.com"],
    ["route chooser trigger", "data-map-route"],
    ["stop chooser trigger", "data-map-stop"],
    ["priority badge renderer", "renderPriorityBadge"],
    ["swipe gallery class", "stop-gallery"],
    ["calendar generation", "BEGIN:VEVENT"]
  ];
  for (const [label, snippet] of requiredSnippets) {
    if (!html.includes(snippet)) fail(`Missing ${label}: ${snippet}`);
  }
}

function validatePrivacy(html) {
  const privacyPatterns = [
    [/confirmation\s*(number|#|code)/i, "hotel or booking confirmation"],
    [/\broom\s*(number|#)?\s*\d{2,5}\b/i, "room number"],
    [/\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i, "email address"],
    [/\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b/i, "phone number"],
    [/\b(?:visa|mastercard|amex|card number|cvv)\b/i, "payment detail"]
  ];
  for (const [pattern, label] of privacyPatterns) {
    if (pattern.test(html)) fail(`Privacy risk detected: ${label}`);
  }
}

function validateTripMeta(tripMeta) {
  if (!tripMeta || typeof tripMeta !== "object") {
    fail("tripMeta must be an object");
    return;
  }
  for (const key of ["title", "intro", "timezone"]) {
    if (!hasText(tripMeta[key])) fail(`tripMeta.${key} is required`);
  }
}

function validateDays(tripDays) {
  if (!Array.isArray(tripDays) || tripDays.length === 0) {
    fail("tripDays must be a non-empty array");
    return;
  }

  const dayIds = new Set();
  tripDays.forEach((day, dayIndex) => validateDay(day, dayIndex, dayIds));
}

function validateDay(day, dayIndex, dayIds) {
  const label = day?.id || `day ${dayIndex + 1}`;
  if (!day || typeof day !== "object") {
    fail(`${label}: day must be an object`);
    return;
  }

  for (const key of ["id", "title", "date", "strategy"]) {
    if (!hasText(day[key])) fail(`${label}: ${key} is required`);
  }
  if (day.id && dayIds.has(day.id)) fail(`${label}: duplicate day id`);
  if (day.id) dayIds.add(day.id);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(String(day.date || ""))) fail(`${label}: date must be YYYY-MM-DD`);

  const weatherItems = normalizeWeather(day.weather);
  if (!weatherItems.length) fail(`${label}: weather summary is required`);
  if (day.weather && !Array.isArray(day.weather)) {
    for (const key of ["checkedAt", "source", "appliesToDate"]) {
      if (!hasText(day.weather[key])) fail(`${label}: weather.${key} is required for object weather`);
    }
  } else {
    recommended(`${label}: use object weather with checkedAt/source/appliesToDate`);
  }

  if (!day.drive || typeof day.drive !== "object") {
    fail(`${label}: drive object is required`);
  } else {
    for (const key of ["summary", "difficulty", "note"]) {
      if (!hasText(day.drive[key])) fail(`${label}: drive.${key} is required`);
    }
    if (!asArray(day.drive.fatigueSources).length) recommended(`${label}: drive.fatigueSources[] is recommended`);
  }

  const stops = asArray(day.stops);
  if (stops.length < 2) fail(`${label}: at least two ordered stops are required`);
  stops.forEach((stop, stopIndex) => validateStop(stop, label, stopIndex));
  validateRouteOrder(stops, label);

  if (!asArray(day.meals).length) recommended(`${label}: meals[] should include meal/rest strategy`);
  if (!asArray(day.cutRules).length) recommended(`${label}: cutRules[] should explain what to remove first`);
  if (!asArray(day.tickets).length) recommended(`${label}: tickets[] should record ticket/venue actions`);
  if (!day.parking) recommended(`${label}: parking note is recommended`);
  if (!asArray(day.medicalBackup).length) recommended(`${label}: medicalBackup[] is recommended when useful`);
  validateSourceProvenance(day, label);
}

function validateStop(stop, dayLabel, stopIndex) {
  const label = `${dayLabel} stop ${stopIndex + 1}${stop?.name ? ` (${stop.name})` : ""}`;
  if (!stop || typeof stop !== "object") {
    fail(`${label}: stop must be an object`);
    return;
  }

  for (const key of ["name", "address", "priority", "why", "tip"]) {
    if (!hasText(stop[key])) fail(`${label}: ${key} is required`);
  }
  if (!isNumber(stop.lat) || !isNumber(stop.lng)) fail(`${label}: numeric lat/lng are required`);
  if (!/^[ABC]\b/i.test(String(stop.priority || ""))) fail(`${label}: priority must start with A, B, or C`);
  if (!hasText(stop.history)) recommended(`${label}: history/context sentence is recommended`);

  const images = normalizeImages(stop);
  if (!images.length && !hasText(stop.imageQuery)) {
    recommended(`${label}: images[] or imageQuery is required`);
  }
  images.forEach((image, imageIndex) => {
    const imageLabel = `${label} image ${imageIndex + 1}`;
    const src = image.src || image.url;
    if (!/^https?:\/\//.test(String(src || ""))) fail(`${imageLabel}: src must be an http(s) URL`);
    for (const key of ["alt", "title", "caption", "credit", "link"]) {
      if (!hasText(image[key])) recommended(`${imageLabel}: ${key} is recommended`);
    }
  });

  for (const link of asArray(stop.links)) {
    if (!linkLooksValid(link)) fail(`${label}: links must be [label, https? URL] pairs`);
  }
}

function validateRouteOrder(stops, dayLabel) {
  const names = stops.map(stop => stop?.name).filter(Boolean);
  if (new Set(names).size !== names.length) warn(`${dayLabel}: duplicate stop names can make route order unclear`);
  const first = stops[0];
  const last = stops[stops.length - 1];
  if (first && last && first.name === last.name) fail(`${dayLabel}: first and last stop should not be identical`);
}

function validateSourceProvenance(day, dayLabel) {
  const sources = asArray(day.sourceProvenance);
  if (!sources.length) {
    recommended(`${dayLabel}: sourceProvenance[] is required for reusable artifacts`);
    return;
  }

  const seenTypes = new Set();
  sources.forEach((source, sourceIndex) => {
    const label = `${dayLabel} source ${sourceIndex + 1}`;
    for (const key of ["type", "label", "url", "checkedAt"]) {
      if (!hasText(source[key])) fail(`${label}: ${key} is required`);
    }
    if (source.type) seenTypes.add(source.type);
    if (source.url && !/^https?:\/\//.test(String(source.url))) fail(`${label}: url must be http(s)`);
  });
  for (const type of ["weather", "road", "ticket", "restaurant", "image"]) {
    if (!seenTypes.has(type)) recommended(`${dayLabel}: sourceProvenance should include ${type}`);
  }
}

validateArtifact();

const relative = repoRelative(filePath);
for (const warning of result.warnings) console.warn(`WARN ${warning}`);
for (const error of result.errors) console.error(`ERROR ${error}`);

if (result.errors.length) {
  console.error(`FAILED ${relative}: ${result.errors.length} error(s), ${result.warnings.length} warning(s)`);
  process.exit(1);
}

console.log(`PASS ${relative}: ${result.warnings.length} warning(s)`);
