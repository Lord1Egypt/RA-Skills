# Web Workers

Move expensive browser computation to workers with clear messaging and transferable data.

## Skill

- ID: `fec-web-workers`
- Category: `implementation-capability`
- Version: `2.9.0`
- Source: `skills/fec-web-workers/SKILL.md`

## Description

Use when moving expensive browser work off the main thread with Web Workers, SharedWorker, worker pools, Comlink, transferable objects, Vite/Webpack worker integration, or UI responsiveness fixes. Do not use for lightweight synchronous work or DOM manipulation; Chinese triggers include Web Worker, background thread, main thread blocking.

## Usage

Install or import this package with any skill runtime that understands the standard `SKILL.md` layout. The canonical source remains the Frontend Craft repository.

## Packaged Files

- [references/advanced-workers.md](references/advanced-workers.md)
- [references/basic-worker.md](references/basic-worker.md)

## Optional Related Packages

- `@bovinphang/fec-canvas-threejs`
- `@bovinphang/fec-list-virtualization`
- `@bovinphang/fec-validation-fix`

## License

MIT
