const MAX_BACKUP_FILE_BYTES = 5 * 1024 * 1024;
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

export const FEED_TYPE = Object.freeze({
  DRY: 'dry',
  WET: 'wet',
});

export const WEIGHT_POLICY = Object.freeze({
  LATEST: 'latest',
  AVERAGE: 'average',
});

export const DISPLAY_MODE = Object.freeze({
  DRY_EQUIVALENT: 'dry_equivalent',
  SEPARATE: 'separate',
});

export const defaultSettings = Object.freeze({
  id: 'singleton',
  wet_to_dry_ratio_default: 1 / 3,
  total_display_mode: DISPLAY_MODE.DRY_EQUIVALENT,
  weight_daily_policy: WEIGHT_POLICY.LATEST,
  theme: 'light',
  data_version: 1,
});

export const SUMMARY_HEADERS = Object.freeze([
  'pet_id',
  'pet_name',
  'date',
  'dry_total',
  'wet_total',
  'dry_equivalent_total',
  'manual_water_total',
  'wet_water_from_food',
  'total_water',
  'weight_kg',
  'feed_record_count',
  'weight_record_count',
  'water_record_count',
]);

class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ValidationError';
  }
}

const fail = (message) => {
  throw new ValidationError(message);
};

const isPlainObject = (value) => typeof value === 'object' && value !== null && !Array.isArray(value);

const assertPlainObject = (value, message) => {
  if (!isPlainObject(value)) fail(message);
  return value;
};

const assertString = (value, message) => {
  if (typeof value !== 'string') fail(message);
  return value;
};

const optionalString = (value, fallback = '') => {
  if (value == null) return fallback;
  if (typeof value !== 'string') fail('Optional field must be a string');
  return value;
};

const assertBoolean = (value, message) => {
  if (typeof value !== 'boolean') fail(message);
  return value;
};

const assertFiniteNumber = (value, message) => {
  if (typeof value !== 'number' || !Number.isFinite(value)) fail(message);
  return value;
};

const assertPositiveNumber = (value, message) => {
  const number = assertFiniteNumber(value, message);
  if (number <= 0) fail(message);
  return number;
};

const assertTimestamp = (value, message) => assertFiniteNumber(value, message);

const assertEnum = (value, enumValues, message) => {
  if (!enumValues.includes(value)) fail(message);
  return value;
};

const assertDateString = (value, message) => {
  assertString(value, message);
  if (!DATE_RE.test(value)) fail(message);
  return value;
};

const round = (value, places) => Number(value.toFixed(places));

const sanitizeSettings = (settings) => {
  assertPlainObject(settings, 'settings must be an object');
  const ratio = assertFiniteNumber(settings.wet_to_dry_ratio_default, 'settings.wet_to_dry_ratio_default is invalid');
  if (ratio <= 0 || ratio > 1) fail('settings.wet_to_dry_ratio_default must be in (0, 1]');

  return {
    id: assertString(settings.id, 'settings.id is invalid'),
    wet_to_dry_ratio_default: ratio,
    total_display_mode: assertEnum(
      settings.total_display_mode,
      Object.values(DISPLAY_MODE),
      'settings.total_display_mode is invalid',
    ),
    weight_daily_policy: assertEnum(
      settings.weight_daily_policy,
      Object.values(WEIGHT_POLICY),
      'settings.weight_daily_policy is invalid',
    ),
    theme: optionalString(settings.theme, defaultSettings.theme),
    data_version: assertFiniteNumber(settings.data_version, 'settings.data_version is invalid'),
  };
};

const sanitizePet = (pet, index) => {
  assertPlainObject(pet, `pets[${index}] must be an object`);
  return {
    id: assertString(pet.id, `pets[${index}].id is invalid`),
    name: assertString(pet.name, `pets[${index}].name is invalid`),
    avatar: optionalString(pet.avatar, ''),
    water_tracking_enabled: assertBoolean(pet.water_tracking_enabled, `pets[${index}].water_tracking_enabled is invalid`),
    is_archived: assertBoolean(pet.is_archived, `pets[${index}].is_archived is invalid`),
    created_at: assertTimestamp(pet.created_at, `pets[${index}].created_at is invalid`),
    updated_at: assertTimestamp(pet.updated_at, `pets[${index}].updated_at is invalid`),
  };
};

const sanitizeFeedRecord = (record, index) => {
  assertPlainObject(record, `feed_records[${index}] must be an object`);
  const feedType = assertEnum(record.feed_type, Object.values(FEED_TYPE), `feed_records[${index}].feed_type is invalid`);
  const grams = assertPositiveNumber(record.grams, `feed_records[${index}].grams is invalid`);
  const ratio = assertFiniteNumber(record.ratio_used, `feed_records[${index}].ratio_used is invalid`);
  if (ratio <= 0 || ratio > 1) fail(`feed_records[${index}].ratio_used must be in (0, 1]`);
  const fallbackDryEquivalent = feedType === FEED_TYPE.WET ? grams * ratio : grams;

  return {
    id: assertString(record.id, `feed_records[${index}].id is invalid`),
    pet_id: assertString(record.pet_id, `feed_records[${index}].pet_id is invalid`),
    date: assertDateString(record.date, `feed_records[${index}].date is invalid`),
    feed_type: feedType,
    grams,
    ratio_used: ratio,
    dry_equivalent_grams: record.dry_equivalent_grams == null
      ? round(fallbackDryEquivalent, 3)
      : assertFiniteNumber(record.dry_equivalent_grams, `feed_records[${index}].dry_equivalent_grams is invalid`),
    note: optionalString(record.note),
    created_at: assertTimestamp(record.created_at, `feed_records[${index}].created_at is invalid`),
    updated_at: assertTimestamp(record.updated_at, `feed_records[${index}].updated_at is invalid`),
  };
};

const sanitizeWeightRecord = (record, index) => {
  assertPlainObject(record, `weight_records[${index}] must be an object`);
  return {
    id: assertString(record.id, `weight_records[${index}].id is invalid`),
    pet_id: assertString(record.pet_id, `weight_records[${index}].pet_id is invalid`),
    date: assertDateString(record.date, `weight_records[${index}].date is invalid`),
    weight_kg: assertPositiveNumber(record.weight_kg, `weight_records[${index}].weight_kg is invalid`),
    measured_at: assertTimestamp(record.measured_at, `weight_records[${index}].measured_at is invalid`),
    note: optionalString(record.note),
    created_at: assertTimestamp(record.created_at, `weight_records[${index}].created_at is invalid`),
    updated_at: assertTimestamp(record.updated_at, `weight_records[${index}].updated_at is invalid`),
  };
};

const sanitizeWaterRecord = (record, index) => {
  assertPlainObject(record, `water_records[${index}] must be an object`);
  return {
    id: assertString(record.id, `water_records[${index}].id is invalid`),
    pet_id: assertString(record.pet_id, `water_records[${index}].pet_id is invalid`),
    date: assertDateString(record.date, `water_records[${index}].date is invalid`),
    grams: assertPositiveNumber(record.grams, `water_records[${index}].grams is invalid`),
    note: optionalString(record.note),
    created_at: assertTimestamp(record.created_at, `water_records[${index}].created_at is invalid`),
    updated_at: assertTimestamp(record.updated_at, `water_records[${index}].updated_at is invalid`),
  };
};

const sanitizeCollection = (value, name, sanitizer) => {
  if (value == null) return [];
  if (!Array.isArray(value)) fail(`${name} must be an array`);
  return value.map(sanitizer);
};

export function parseBackupText(text) {
  if (typeof text !== 'string') fail('Backup input must be text');
  if (text.length === 0) fail('Backup input is empty');
  if (Buffer.byteLength(text, 'utf8') > MAX_BACKUP_FILE_BYTES) fail('Backup input exceeds 5 MB');

  try {
    return JSON.parse(text);
  } catch {
    fail('Backup input is not valid JSON');
  }
}

export function sanitizeBackupData(data) {
  assertPlainObject(data, 'Backup must be a JSON object');
  return {
    settings: data.settings == null ? { ...defaultSettings } : sanitizeSettings(data.settings),
    pets: sanitizeCollection(data.pets, 'pets', sanitizePet),
    feed_records: sanitizeCollection(data.feed_records, 'feed_records', sanitizeFeedRecord),
    weight_records: sanitizeCollection(data.weight_records, 'weight_records', sanitizeWeightRecord),
    water_records: sanitizeCollection(data.water_records, 'water_records', sanitizeWaterRecord),
  };
}

export function validateBackupData(data) {
  const backup = sanitizeBackupData(data);
  const petIds = new Set(backup.pets.map((pet) => pet.id));
  const warnings = [];

  for (const [name, records] of [
    ['feed_records', backup.feed_records],
    ['weight_records', backup.weight_records],
    ['water_records', backup.water_records],
  ]) {
    const missing = new Set(records.filter((record) => !petIds.has(record.pet_id)).map((record) => record.pet_id));
    for (const petId of missing) {
      warnings.push(`${name} references missing pet_id: ${petId}`);
    }
  }

  for (const record of backup.feed_records) {
    if (record.dry_equivalent_grams < 0) {
      warnings.push(`feed_records record ${record.id} has negative dry_equivalent_grams`);
    }
    if (record.feed_type === FEED_TYPE.DRY && Math.abs(record.dry_equivalent_grams - record.grams) > 0.01) {
      warnings.push(`dry feed record ${record.id} has dry_equivalent_grams different from grams`);
    }
    if (record.feed_type === FEED_TYPE.WET && record.dry_equivalent_grams > record.grams) {
      warnings.push(`wet feed record ${record.id} has dry_equivalent_grams greater than grams; water estimate will be negative`);
    }
  }

  return {
    valid: true,
    counts: {
      pets: backup.pets.length,
      feed_records: backup.feed_records.length,
      weight_records: backup.weight_records.length,
      water_records: backup.water_records.length,
    },
    settings: backup.settings,
    warnings,
    backup,
  };
}

export function calcDailySummary({ feedRecords = [], weightRecords = [], waterRecords = [], weightPolicy = WEIGHT_POLICY.LATEST }) {
  const dryTotal = feedRecords.filter((r) => r.feed_type === FEED_TYPE.DRY).reduce((sum, r) => sum + r.grams, 0);
  const wetTotal = feedRecords.filter((r) => r.feed_type === FEED_TYPE.WET).reduce((sum, r) => sum + r.grams, 0);
  const dryEquivalentTotal = feedRecords.reduce((sum, r) => sum + r.dry_equivalent_grams, 0);
  const manualWaterTotal = waterRecords.reduce((sum, r) => sum + r.grams, 0);
  const wetWaterFromFood = feedRecords
    .filter((r) => r.feed_type === FEED_TYPE.WET)
    .reduce((sum, r) => sum + (r.grams - r.dry_equivalent_grams), 0);

  let weight = null;
  if (weightRecords.length > 0) {
    if (weightPolicy === WEIGHT_POLICY.AVERAGE) {
      weight = round(weightRecords.reduce((sum, r) => sum + r.weight_kg, 0) / weightRecords.length, 3);
    } else {
      weight = [...weightRecords].sort((a, b) => a.measured_at - b.measured_at).at(-1).weight_kg;
    }
  }

  return {
    dry_total: round(dryTotal, 2),
    wet_total: round(wetTotal, 2),
    dry_equivalent_total: round(dryEquivalentTotal, 2),
    manual_water_total: round(manualWaterTotal, 2),
    wet_water_from_food: round(wetWaterFromFood, 2),
    total_water: round(manualWaterTotal + wetWaterFromFood, 2),
    weight_kg: weight,
  };
}

export function buildDailySummaryRows(backup, filters = {}) {
  const petById = new Map(backup.pets.map((pet) => [pet.id, pet]));
  const petIds = new Set([
    ...backup.pets.map((pet) => pet.id),
    ...backup.feed_records.map((record) => record.pet_id),
    ...backup.weight_records.map((record) => record.pet_id),
    ...backup.water_records.map((record) => record.pet_id),
  ]);

  const rows = [];
  for (const petId of [...petIds].sort()) {
    const pet = petById.get(petId) ?? { id: petId, name: '' };
    if (filters.petId && petId !== filters.petId) continue;
    if (filters.petName && pet.name !== filters.petName) continue;

    const dates = new Set([
      ...backup.feed_records.filter((r) => r.pet_id === petId).map((r) => r.date),
      ...backup.weight_records.filter((r) => r.pet_id === petId).map((r) => r.date),
      ...backup.water_records.filter((r) => r.pet_id === petId).map((r) => r.date),
    ]);

    for (const date of [...dates].sort()) {
      if (filters.from && date < filters.from) continue;
      if (filters.to && date > filters.to) continue;

      const feedRecords = backup.feed_records.filter((r) => r.pet_id === petId && r.date === date);
      const weightRecords = backup.weight_records.filter((r) => r.pet_id === petId && r.date === date);
      const waterRecords = backup.water_records.filter((r) => r.pet_id === petId && r.date === date);
      const summary = calcDailySummary({
        feedRecords,
        weightRecords,
        waterRecords,
        weightPolicy: backup.settings.weight_daily_policy,
      });

      rows.push({
        pet_id: petId,
        pet_name: pet.name,
        date,
        ...summary,
        weight_kg: summary.weight_kg ?? '',
        feed_record_count: feedRecords.length,
        weight_record_count: weightRecords.length,
        water_record_count: waterRecords.length,
      });
    }
  }

  return rows;
}

export function toCSV(rows) {
  const headers = rows.length === 0 ? SUMMARY_HEADERS : Object.keys(rows[0]);
  const lines = rows.map((row) => headers.map((header) => JSON.stringify(row[header] ?? '')).join(','));
  return [headers.join(','), ...lines].join('\n');
}

export function parseCliArgs(argv) {
  const options = { input: null, format: 'json', pretty: false };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--help' || arg === '-h') {
      options.help = true;
    } else if (arg === '--pretty') {
      options.pretty = true;
    } else if (arg === '--format') {
      options.format = argv[++index];
    } else if (arg === '--pet-id') {
      options.petId = argv[++index];
    } else if (arg === '--pet-name') {
      options.petName = argv[++index];
    } else if (arg === '--from') {
      options.from = argv[++index];
    } else if (arg === '--to') {
      options.to = argv[++index];
    } else if (!options.input) {
      options.input = arg;
    } else {
      fail(`Unknown argument: ${arg}`);
    }
  }
  return options;
}

export function assertDateFilter(value, label) {
  if (value != null && !DATE_RE.test(value)) fail(`${label} must use YYYY-MM-DD`);
}

export { ValidationError };
