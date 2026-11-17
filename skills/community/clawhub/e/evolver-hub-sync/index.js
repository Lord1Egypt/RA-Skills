#!/usr/bin/env node
/**
 * evolver-hub-sync — Sync Evolver genes/capsules with Evomap Hub
 * Uses correct A2A API endpoints
 */

const { syncAssets, getNodeInfo, publishAssets } = require('./scripts/sync');

module.exports = {
  syncAssets,
  getNodeInfo,
  publishAssets
};
