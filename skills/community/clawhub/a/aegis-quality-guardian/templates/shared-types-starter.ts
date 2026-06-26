// contracts/shared-types.ts
// ⚠️ Single source of truth for shared type definitions.
// Keep in sync with api-spec.yaml.
//
// If using code generation (e.g. .aegis/generate-types.sh), mark as AUTO-GENERATED.
// Otherwise, maintain this file manually — it IS the contract.

// === Base Types ===

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: ApiError;
}

export interface ApiError {
  /** Error code — must match codes in errors.yaml */
  code: string;
  /** Human-readable error message */
  message: string;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: PaginationMeta;
}

export interface PaginationMeta {
  page: number;
  pageSize: number;
  total: number;
}

// === Domain Types ===
// Add your domain-specific types below.
// These should mirror the schemas in api-spec.yaml.

// Example:
// export interface User {
//   id: string;
//   username: string;
//   email: string;
//   createdAt: string; // ISO 8601
// }
