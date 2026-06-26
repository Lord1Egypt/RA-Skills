export const DEFAULT_DROP_API_BASE_URL = "https://api.element.market/drop/api/v1";
export const DEFAULT_ELEMENT_GRAPHQL_URL = "https://api.element.market/graphql";
export const DEFAULT_NETWORK_TIMEOUT_MS = 30_000;
export const DEFAULT_OSS_UPLOAD_TIMEOUT_MS = 60_000;

const DEFAULT_GRAPHQL_TOKEN_A_BYTES = [
  122, 81, 98, 89, 106, 55, 82, 104, 67, 49, 86, 72, 73, 66, 100, 87, 85, 54, 51, 107, 105, 53,
  65, 74, 75, 88, 108, 111, 97, 109, 68, 84
];

const DEFAULT_GRAPHQL_TOKEN_B_BYTES = [
  85, 113, 67, 77, 112, 102, 71, 110, 51, 86, 121, 81, 69, 100, 115, 106, 76, 107, 122, 74, 118,
  57, 116, 78, 108, 103, 98, 75, 70, 68, 55, 79
];

function decodeAsciiBytes(bytes: number[]): string {
  return String.fromCharCode(...bytes);
}

export function resolveElementGraphqlTokenA(): string {
  return decodeAsciiBytes(DEFAULT_GRAPHQL_TOKEN_A_BYTES);
}

export function resolveElementGraphqlTokenB(): string {
  return decodeAsciiBytes(DEFAULT_GRAPHQL_TOKEN_B_BYTES);
}
