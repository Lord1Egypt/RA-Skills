#!/usr/bin/env node
/**
 * Database Initialization Script
 */

const fs = require('fs');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

const dbPath = path.join(__dirname, '..', 'db', 'finance.db');
const schemaPath = path.join(__dirname, '..', 'db', 'schema.sql');

// Create db directory if it doesn't exist
const dbDir = path.dirname(dbPath);
if (!fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true });
  console.log('✅ Created db directory');
}

// Read schema
const schema = fs.readFileSync(schemaPath, 'utf8');

// Initialize database
const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('❌ Error opening database:', err.message);
    process.exit(1);
  }
  console.log('✅ Connected to SQLite database');
});

// Execute schema
db.exec(schema, (err) => {
  if (err) {
    console.error('❌ Error creating schema:', err.message);
    db.close();
    process.exit(1);
  }
  
  console.log('✅ Database schema created successfully');
  
  // Create storage directories
  const storageDir = path.join(__dirname, '..', 'storage');
  const pdfsDir = path.join(storageDir, 'pdfs');
  const receiptsDir = path.join(storageDir, 'receipts');
  
  [storageDir, pdfsDir, receiptsDir].forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      console.log(`✅ Created ${path.basename(dir)} directory`);
    }
  });
  
  // Create logs directory
  const logsDir = path.join(__dirname, '..', 'logs');
  if (!fs.existsSync(logsDir)) {
    fs.mkdirSync(logsDir, { recursive: true });
    console.log('✅ Created logs directory');
  }
  
  db.close((err) => {
    if (err) {
      console.error('❌ Error closing database:', err.message);
    }
    console.log('\n🎉 Database initialization complete!');
    console.log('\nNext steps:');
    console.log('1. Copy .env.example to .env');
    console.log('2. Fill in your API keys');
    console.log('3. Run: npm run dev');
  });
});
