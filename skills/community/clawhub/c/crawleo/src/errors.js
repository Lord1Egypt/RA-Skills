export const CRAWLEO_ERROR_CODES = Object.freeze({
  MISSING_API_KEY: 'CRAWLEO_CONFIG_MISSING_API_KEY',
  MISSING_FETCH: 'CRAWLEO_CONFIG_MISSING_FETCH',
  VALIDATION: 'CRAWLEO_VALIDATION_ERROR',
  HTTP_BAD_REQUEST: 'CRAWLEO_HTTP_BAD_REQUEST',
  HTTP_AUTH: 'CRAWLEO_HTTP_AUTH',
  HTTP_PAYMENT_REQUIRED: 'CRAWLEO_HTTP_PAYMENT_REQUIRED',
  HTTP_FORBIDDEN: 'CRAWLEO_HTTP_FORBIDDEN',
  HTTP_RATE_LIMIT: 'CRAWLEO_HTTP_RATE_LIMIT',
  HTTP_UPSTREAM: 'CRAWLEO_HTTP_UPSTREAM',
  RESPONSE_MALFORMED_JSON: 'CRAWLEO_RESPONSE_MALFORMED_JSON',
  TRANSPORT: 'CRAWLEO_TRANSPORT_ERROR'
});

const SECRET_PATTERNS = [
  /x-api-key\s*[:=]\s*[^\s,}]+/gi,
  /authorization\s*[:=]\s*bearer\s+[^\s,}]+/gi,
  /api[_-]?key\s*[:=]\s*[^\s,}]+/gi
];

export function redactSecret(value, explicitSecrets = []) {
  if (value == null) return value;

  let redacted = String(value);
  for (const secret of explicitSecrets) {
    if (secret) {
      redacted = redacted.split(String(secret)).join('[REDACTED]');
    }
  }

  for (const pattern of SECRET_PATTERNS) {
    redacted = redacted.replace(pattern, (match) => {
      const separator = match.includes('=') ? '=' : ':';
      const [name] = match.split(separator);
      return `${name}${separator} [REDACTED]`;
    });
  }

  return redacted;
}

export class CrawleoError extends Error {
  constructor(message, options = {}) {
    super(redactSecret(message, options.secrets));
    this.name = 'CrawleoError';
    this.code = options.code || CRAWLEO_ERROR_CODES.HTTP_UPSTREAM;
    this.endpoint = options.endpoint;
    this.status = options.status;
    this.field = options.field;
    this.details = redactDetails(options.details, options.secrets);

    if (options.cause) {
      this.cause = options.cause;
    }
  }

  toJSON() {
    return {
      name: this.name,
      code: this.code,
      message: this.message,
      endpoint: this.endpoint,
      status: this.status,
      field: this.field,
      details: this.details
    };
  }
}

function redactDetails(details, secrets = []) {
  if (details == null) return details;
  if (typeof details === 'string') return redactSecret(details, secrets);
  if (Array.isArray(details)) return details.map((item) => redactDetails(item, secrets));
  if (typeof details === 'object') {
    return Object.fromEntries(
      Object.entries(details).map(([key, value]) => [key, redactDetails(value, secrets)])
    );
  }
  return details;
}

export function errorCodeForStatus(status) {
  if (status === 400) return CRAWLEO_ERROR_CODES.HTTP_BAD_REQUEST;
  if (status === 401) return CRAWLEO_ERROR_CODES.HTTP_AUTH;
  if (status === 402) return CRAWLEO_ERROR_CODES.HTTP_PAYMENT_REQUIRED;
  if (status === 403) return CRAWLEO_ERROR_CODES.HTTP_FORBIDDEN;
  if (status === 429) return CRAWLEO_ERROR_CODES.HTTP_RATE_LIMIT;
  return CRAWLEO_ERROR_CODES.HTTP_UPSTREAM;
}
