# Project Master Plan: Demo REST API

> Write exactly ONE grand objective here. Ensure tickets are extremely granular. Never rewrite files entirely.

## Meta
- created: 2026-03-15
- last_architect_edit: 2026-03-15T14:30:00
- tick_mode: auto          <!-- auto | paused | stopped -->
- max_retries: 3           
- max_tasks_per_tick: 1    
- status_max_entries: 50
- clean_strategy: git-clean
- clean_ignore: .memento_cleanignore
- total_ticks: 5
- total_tasks: 7
- completed_tasks: 3

## Phase 1: Setup & Infrastructure
- [x] T-101: Initialize Express.js server in `src/server.js` with CORS and JSON parsing. [retries: 0]
- [x] T-102: Setup SQLite database connection in `src/db/index.js`. [retries: 0]
- [x] T-103: Create schema migration script for `users` table. [retries: 1]

## Phase 2: Core API Endpoints (depends on Phase 1)
- [~] T-201: Implement `POST /api/users` endpoint for user registration. [retries: 2]
- [ ] T-202: Implement `GET /api/users/:id` endpoint for user retrieval. [retries: 0]
- [!] T-203: Implement user authentication middleware using JWT. [retries: 3]

## Phase 3: Testing & Polish (depends on Phase 2)
- [ ] T-301: Write Jest tests for user registration endpoint. [retries: 0]
