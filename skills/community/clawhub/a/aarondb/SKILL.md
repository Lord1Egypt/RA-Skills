# AaronDB Edge Skill

A high-performance, distributed Datalog engine designed for sovereign agents.

## Frontmatter

```yaml
name: aarondb-edge
description: Distributed Datalog engine for sovereign agents. Enables persistent fact management and reasoning.
version: 1.1.0
author: criticalinsight
repository: https://github.com/criticalinsight/aarondb-edge
npm: https://www.npmjs.com/package/@criticalinsight/aarondb-edge
requirements:
  - "@criticalinsight/aarondb-edge"
```

## Description

This skill enables AI agents to utilize a local or distributed Datalog engine for fact storage, retrieval, and reasoning. It follows the "Database as a Value" philosophy, allowing for immutable state management and time-travel debugging.

## Installation

To use this skill, ensure the core package is installed in your agent's runtime:

```bash
npm install @criticalinsight/aarondb-edge
```

## Usage

### 1. Initialization

```javascript
import { AaronDB } from '@criticalinsight/aarondb-edge';

// Initialize a new database instance
const db = new AaronDB();
```

### 2. Transacting Facts

Facts are stored as "datoms" (Entity, Attribute, Value).

```javascript
await db.transact([
  { e: "agent/philosophy", a: "type", v: "RichHickey" },
  { e: "agent/philosophy", a: "principle", v: "Simplicity" }
]);
```

### 3. Querying

Use Datalog syntax with variable bindings.

```javascript
const results = db.query({
  where: [
    ["?e", "type", "RichHickey"],
    ["?e", "principle", "?p"]
  ]
});
```

## Architectural Patterns

- **Database as a Value**: Always treat the database state as an immutable value. Avoid manual state mutations outside of the `transact` flow.
- **Shared Discovery Layer**: Facts can be synchronized across agents using a shared D1/KV back-end when running in Cloudflare Worker mode. In library mode, the state is local-first but can be exported/imported as a unified fact log for cross-agent collaboration.
