const DEFAULTS = {
  indexName: "dual-brain-memory-guardian-memory",
  cloud: "aws",
  region: "us-east-1",
  model: "multilingual-e5-large",
  textField: "content",
  namespacePrefix: "dualbrain",
  defaultTenant: "default"
};

function required(value, fieldName) {
  if (value === undefined || value === null || String(value).trim() === "") {
    throw new Error(`${fieldName} is required.`);
  }

  return String(value).trim();
}

export function normalizeTenantId(input) {
  const raw = String(input ?? DEFAULTS.defaultTenant).trim().toLowerCase();
  const safe = raw.replace(/[^a-z0-9_-]/g, "-").replace(/-+/g, "-");
  return safe || DEFAULTS.defaultTenant;
}

export function namespaceForTenant(prefix, tenantId) {
  const safePrefix = String(prefix || DEFAULTS.namespacePrefix)
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9_-]/g, "-")
    .replace(/-+/g, "-");

  return `${safePrefix}-${normalizeTenantId(tenantId)}`;
}

export function loadConfig(overrides = {}) {
  const env = process.env;

  const config = {
    apiKey: required(overrides.apiKey ?? env.PINECONE_API_KEY, "PINECONE_API_KEY"),
    indexName: String(overrides.indexName ?? env.PINECONE_INDEX_NAME ?? DEFAULTS.indexName).trim(),
    cloud: String(overrides.cloud ?? env.PINECONE_CLOUD ?? DEFAULTS.cloud).trim(),
    region: String(overrides.region ?? env.PINECONE_REGION ?? DEFAULTS.region).trim(),
    model: String(overrides.model ?? env.PINECONE_MODEL ?? DEFAULTS.model).trim(),
    textField: String(overrides.textField ?? env.PINECONE_FIELD_MAP_TEXT ?? DEFAULTS.textField).trim(),
    namespacePrefix: String(
      overrides.namespacePrefix ?? env.PINECONE_NAMESPACE_PREFIX ?? DEFAULTS.namespacePrefix
    ).trim(),
    defaultTenant: normalizeTenantId(overrides.defaultTenant ?? env.MEMORY_TENANT ?? DEFAULTS.defaultTenant),
    importIntegrationId: String(
      overrides.importIntegrationId ?? env.PINECONE_IMPORT_INTEGRATION_ID ?? ""
    ).trim()
  };

  return config;
}
