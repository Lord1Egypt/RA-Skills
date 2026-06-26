import { splitLocalDateTime } from "./utils.mjs";
import { normalizeTransitScene } from "./onehai-policy.mjs";

function normalizeString(value) {
  return value === undefined || value === null ? "" : String(value).trim();
}

function normalizeDateTime(value) {
  const normalized = normalizeString(value).replace("T", " ");
  splitLocalDateTime(normalized);
  return normalized;
}

export function normalizeQuery(input) {
  const pickupCity = normalizeString(input.pickupCity);
  const dropoffCity = normalizeString(input.dropoffCity) || pickupCity;
  const pickupDateTime = normalizeDateTime(input.pickupDateTime);
  const dropoffDateTime = normalizeDateTime(input.dropoffDateTime);

  if (!pickupCity) {
    throw new Error("pickupCity is required");
  }

  if (!pickupDateTime || !dropoffDateTime) {
    throw new Error("pickupDateTime and dropoffDateTime are required");
  }

  return {
    pickup: {
      city: pickupCity,
      location: normalizeString(input.pickupLocation) || null,
      scene: normalizeTransitScene(input.pickupScene, input.pickupLocation)
    },
    dropoff: {
      city: dropoffCity,
      location: normalizeString(input.dropoffLocation) || null,
      scene: normalizeTransitScene(input.dropoffScene, input.dropoffLocation)
    },
    pickupAt: pickupDateTime,
    dropoffAt: dropoffDateTime,
    vehicleClass: normalizeString(input.vehicleClass) || null,
    sameCity: pickupCity === dropoffCity
  };
}

export function queryCacheKey(query) {
  return JSON.stringify(query);
}
