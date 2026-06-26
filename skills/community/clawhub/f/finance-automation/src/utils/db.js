/**
 * Database Utility
 * Promisified SQLite3 wrapper
 */

const path = require('path');
const sqlite3 = require('sqlite3').verbose();
const logger = require('./logger');

const dbPath = path.join(__dirname, '..', '..', 'db', 'finance.db');

let db;

function getDb() {
  if (!db) {
    db = new sqlite3.Database(dbPath, (err) => {
      if (err) {
        logger.error('Failed to connect to database', { error: err.message });
        throw err;
      }
      logger.info('Connected to SQLite database');
    });
    db.run('PRAGMA journal_mode = WAL');
    db.run('PRAGMA foreign_keys = ON');
  }
  return db;
}

function run(sql, params = []) {
  return new Promise((resolve, reject) => {
    getDb().run(sql, params, function (err) {
      if (err) reject(err);
      else resolve({ lastID: this.lastID, changes: this.changes });
    });
  });
}

function get(sql, params = []) {
  return new Promise((resolve, reject) => {
    getDb().get(sql, params, (err, row) => {
      if (err) reject(err);
      else resolve(row);
    });
  });
}

function all(sql, params = []) {
  return new Promise((resolve, reject) => {
    getDb().all(sql, params, (err, rows) => {
      if (err) reject(err);
      else resolve(rows);
    });
  });
}

async function transaction(fn) {
  await run('BEGIN TRANSACTION');
  try {
    const result = await fn({ run, get, all });
    await run('COMMIT');
    return result;
  } catch (err) {
    await run('ROLLBACK');
    throw err;
  }
}

module.exports = { getDb, run, get, all, transaction };
