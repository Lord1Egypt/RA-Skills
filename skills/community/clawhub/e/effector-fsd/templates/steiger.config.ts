import { defineConfig } from 'steiger';
import fsd from '@feature-sliced/steiger-plugin';

export default defineConfig([
  ...fsd.configs.recommended,
  {
    // Example: ignore generated files and colocated mocks.
    ignores: ['**/__generated__/**', '**/__mocks__/**'],
  },
  {
    // Example: many teams disable public-api for Shared while keeping it for slices.
    // Remove this exception if your team wants strict Shared public APIs too.
    files: ['./src/shared/**'],
    rules: {
      'fsd/public-api': 'off',
    },
  },
]);
