#!/usr/bin/env node
import assert from 'node:assert/strict';
import {
  buildDailySummaryRows,
  parseBackupText,
  validateBackupData,
} from './cat-food-core.mjs';

const sample = {
  settings: {
    id: 'singleton',
    wet_to_dry_ratio_default: 1 / 3,
    total_display_mode: 'dry_equivalent',
    weight_daily_policy: 'average',
    theme: 'light',
    data_version: 1,
  },
  pets: [{
    id: 'pet-1',
    name: 'Sample Cat',
    avatar: '',
    water_tracking_enabled: true,
    is_archived: false,
    created_at: 1,
    updated_at: 1,
  }],
  feed_records: [
    {
      id: 'feed-1',
      pet_id: 'pet-1',
      date: '2026-04-24',
      feed_type: 'dry',
      grams: 20,
      ratio_used: 1,
      dry_equivalent_grams: 20,
      note: '',
      created_at: 1,
      updated_at: 1,
    },
    {
      id: 'feed-2',
      pet_id: 'pet-1',
      date: '2026-04-24',
      feed_type: 'wet',
      grams: 30,
      ratio_used: 1 / 3,
      dry_equivalent_grams: 10,
      note: '',
      created_at: 1,
      updated_at: 1,
    },
  ],
  weight_records: [
    {
      id: 'weight-1',
      pet_id: 'pet-1',
      date: '2026-04-24',
      weight_kg: 3.2,
      measured_at: 1,
      note: '',
      created_at: 1,
      updated_at: 1,
    },
    {
      id: 'weight-2',
      pet_id: 'pet-1',
      date: '2026-04-24',
      weight_kg: 3.4,
      measured_at: 2,
      note: '',
      created_at: 1,
      updated_at: 1,
    },
  ],
  water_records: [{
    id: 'water-1',
    pet_id: 'pet-1',
    date: '2026-04-24',
    grams: 15,
    note: '',
    created_at: 1,
    updated_at: 1,
  }],
};

const report = validateBackupData(parseBackupText(JSON.stringify(sample)));
assert.equal(report.valid, true);
assert.deepEqual(report.warnings, []);

const [row] = buildDailySummaryRows(report.backup);
assert.equal(row.dry_total, 20);
assert.equal(row.wet_total, 30);
assert.equal(row.dry_equivalent_total, 30);
assert.equal(row.manual_water_total, 15);
assert.equal(row.wet_water_from_food, 20);
assert.equal(row.total_water, 35);
assert.equal(row.weight_kg, 3.3);

assert.throws(() => validateBackupData({ pets: 'bad' }), /pets must be an array/);

console.log('self-test passed');
