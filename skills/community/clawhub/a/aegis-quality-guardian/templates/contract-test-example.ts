// Contract Test Example — Backend Provider Test
//
// Validates that your API implementation conforms to the OpenAPI contract.
// Uses the actual contract file as the source of truth.
//
// Adapt to your test framework (Jest, Vitest, Mocha, etc.)

import { describe, it, expect } from 'vitest'; // or jest
import request from 'supertest';
import { app } from '../src/app'; // your Express/Koa/Fastify app

// Option A: Use a contract validation library
// import SwaggerParser from '@apidevtools/swagger-parser';
// import { OpenAPIValidator } from 'express-openapi-validator';

// Option B: Simple structural validation
import { readFileSync } from 'fs';
import { load } from 'js-yaml';

const apiSpec = load(readFileSync('./contracts/api-spec.yaml', 'utf8')) as any;

describe('Contract Tests — API Provider', () => {
  describe('GET /api/health', () => {
    it('should conform to contract', async () => {
      const response = await request(app).get('/api/health');

      expect(response.status).toBe(200);

      // Validate against contract schema
      const schema = apiSpec.paths['/api/health'].get.responses['200']
        .content['application/json'].schema;

      // Check required fields
      for (const field of schema.required || []) {
        expect(response.body).toHaveProperty(field);
      }

      // Check field types
      if (schema.properties) {
        for (const [key, prop] of Object.entries(schema.properties) as any) {
          if (response.body[key] !== undefined) {
            if (prop.type === 'string') expect(typeof response.body[key]).toBe('string');
            if (prop.type === 'number' || prop.type === 'integer') expect(typeof response.body[key]).toBe('number');
            if (prop.type === 'boolean') expect(typeof response.body[key]).toBe('boolean');
          }
        }
      }
    });
  });

  // Add more endpoint tests following the same pattern:
  //
  // describe('GET /api/users', () => {
  //   it('should return paginated response conforming to contract', async () => {
  //     const response = await request(app).get('/api/users?page=1&pageSize=10');
  //     expect(response.status).toBe(200);
  //     expect(response.body).toHaveProperty('success', true);
  //     expect(response.body).toHaveProperty('data');
  //     expect(response.body).toHaveProperty('pagination');
  //     expect(Array.isArray(response.body.data)).toBe(true);
  //   });
  // });
});

// === Frontend Consumer Test Example ===
//
// describe('Contract Tests — Frontend Consumer', () => {
//   it('UserList handles contract-compliant response', () => {
//     // Build test data from contract types (not arbitrary mock data)
//     const contractResponse: ApiResponse<User[]> = {
//       success: true,
//       data: [{
//         id: '1',
//         username: 'test',
//         email: 'test@example.com',
//         createdAt: '2026-01-01T00:00:00Z'
//       }]
//     };
//
//     render(<UserList data={contractResponse} />);
//     expect(screen.getByText('test')).toBeInTheDocument();
//   });
// });
