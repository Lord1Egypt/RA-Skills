---
name: Ghost Admin API Endpoint Builder
description: Create or extend Ghost Admin API endpoint code in the standard core structure. Use this skill for tasks that add a new endpoint file under `ghost/core/core/server/api/endpoints/`, modify an existing controller with new actions or validation, register HTTP route entries in `ghost/core/core/server/web/api/endpoints/admin/routes.js`, register the endpoint module, or add matching e2e tests in `ghost/core/test/e2e-api/admin/`. Typical inputs include endpoint requirements, controller files, route files, validation schemas, module registration files, and existing test patterns; expected outputs include controller objects, route wiring, input serializers or schemas, module registration updates, and integration tests. Supported admin resources include members, posts, labels, newsletters, tiers, redirects, webhooks, snippets, and similar Ghost admin resources. Reject tasks outside this admin REST endpoint workflow, including frontend routes, database migrations, CLI commands, GraphQL APIs, WebSockets, SSE, SOAP, cron jobs, webpack/build tasks, multipart file-upload flows, or other non-REST admin patterns.
---

# Admin API Endpoint Testing Guide

This guide provides a comprehensive approach for developers to test newly created endpoints in Ghost's Admin API. Follow the steps below to ensure your endpoints are functioning correctly.

## Instructions

1. **Creating a New Endpoint**: If you are creating an endpoint for a new resource, start by creating a new endpoint file in `ghost/core/core/server/api/endpoints/`. If the endpoint already exists, locate the corresponding file in the same directory.
2. **Controller Object**: In the endpoint file, create a controller object using the JSDoc type from `@tryghost/api-framework`.Controller. Ensure it includes at least a `docName` and a single endpoint definition, such as `browse`.
3. **Adding Routes**: Add the necessary routes for each endpoint to `ghost/core/core/server/web/api/endpoints/admin/routes.js` to make them accessible through the API.
4. **Testing the Endpoint**: Implement basic end-to-end API tests for the new endpoint in `ghost/core/test/e2e-api/admin`. This will help verify that the endpoint functions as expected.
5. **Running Tests**: Execute the tests and iterate on your implementation until all tests pass. Use the command: `cd ghost/core && yarn test:single test/e2e-api/admin/{test-file-name}` to run your specific test file.

## Reference
For further details on Ghost's API framework and how to create API controllers, refer to the official documentation.