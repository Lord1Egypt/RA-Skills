/**
 * Vector Store Adapters — query external vector databases for knowledge verification.
 *
 * Supports: Qdrant, Chroma, Weaviate, Milvus, Redis Vector, OpenViking
 * All adapters use HTTP REST APIs — zero native dependencies.
 *
 * Configure in ~/.openclaw/cove.yaml:
 *
 *   vector_store:
 *     provider: "qdrant"           # qdrant | chroma | weaviate | milvus | redis | openviking
 *     url: "http://localhost:6333"  # Vector DB endpoint
 *     collection: "knowledge"       # Collection/index name
 *     api_key: ""                   # Optional auth key
 *     top_k: 5                      # Number of results per query
 *     score_threshold: 0.7          # Minimum similarity score (0-1)
 */

const http = require('http');
const https = require('https');

// ── HTTP helper ─────────────────────────────────────────────────────────────

function httpRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const isHttps = parsed.protocol === 'https:';
    const lib = isHttps ? https : http;

    const reqOpts = {
      hostname: parsed.hostname,
      port: parsed.port || (isHttps ? 443 : 80),
      path: parsed.pathname + parsed.search,
      method: options.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    const req = lib.request(reqOpts, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data) });
        } catch {
          resolve({ status: res.statusCode, data });
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(options.timeout || 10000, () => { req.destroy(); reject(new Error('Vector store request timed out')); });
    if (options.body) req.write(typeof options.body === 'string' ? options.body : JSON.stringify(options.body));
    req.end();
  });
}

// ── Embedding helper ────────────────────────────────────────────────────────

/**
 * Get embedding vector for a text query via the OpenClaw sidecar proxy.
 * Falls back to text search if embeddings are not available.
 */
async function getEmbedding(text, config = {}) {
  const port = config.proxy_port || 8888;
  const proxyKey = config.proxy_key || '';

  try {
    const res = await httpRequest(`http://127.0.0.1:${port}/v1/embeddings`, {
      method: 'POST',
      headers: proxyKey ? { Authorization: `Bearer ${proxyKey}` } : {},
      body: { input: text, model: 'text-embedding-3-small' },
    });

    if (res.status === 200 && res.data?.data?.[0]?.embedding) {
      return res.data.data[0].embedding;
    }
  } catch { /* embedding not available */ }

  return null;
}

// ── Adapters ────────────────────────────────────────────────────────────────

const adapters = {

  /**
   * Qdrant — https://qdrant.tech/documentation/
   * REST API: POST /collections/{name}/points/search
   */
  async qdrant(query, config) {
    const { url, collection, api_key, top_k = 5, score_threshold = 0.7 } = config;
    const embedding = await getEmbedding(query, config);
    if (!embedding) return [];

    const headers = {};
    if (api_key) headers['api-key'] = api_key;

    const res = await httpRequest(`${url}/collections/${collection}/points/search`, {
      method: 'POST',
      headers,
      body: {
        vector: embedding,
        limit: top_k,
        score_threshold,
        with_payload: true,
      },
    });

    if (res.status !== 200 || !res.data?.result) return [];
    return res.data.result.map(r => ({
      text: r.payload?.text || r.payload?.content || r.payload?.chunk || JSON.stringify(r.payload),
      score: r.score,
      source: `qdrant/${collection}`,
    }));
  },

  /**
   * Chroma — https://docs.trychroma.com/
   * REST API: POST /api/v1/collections/{id}/query
   */
  async chroma(query, config) {
    const { url, collection, api_key, top_k = 5 } = config;
    const headers = {};
    if (api_key) headers['Authorization'] = `Bearer ${api_key}`;

    // First get collection ID by name
    const colRes = await httpRequest(`${url}/api/v1/collections/${collection}`, { headers });
    if (colRes.status !== 200) return [];
    const colId = colRes.data?.id || collection;

    // Chroma supports query by text (it embeds internally)
    const res = await httpRequest(`${url}/api/v1/collections/${colId}/query`, {
      method: 'POST',
      headers,
      body: {
        query_texts: [query],
        n_results: top_k,
        include: ['documents', 'distances'],
      },
    });

    if (res.status !== 200 || !res.data?.documents?.[0]) return [];
    return (res.data.documents[0] || []).map((doc, i) => ({
      text: doc,
      score: res.data.distances?.[0]?.[i] != null ? 1 - res.data.distances[0][i] : null,
      source: `chroma/${collection}`,
    }));
  },

  /**
   * Weaviate — https://weaviate.io/developers/weaviate
   * REST API: POST /v1/graphql
   */
  async weaviate(query, config) {
    const { url, collection, api_key, top_k = 5, score_threshold = 0.7 } = config;
    const headers = {};
    if (api_key) headers['Authorization'] = `Bearer ${api_key}`;

    const className = collection.charAt(0).toUpperCase() + collection.slice(1);
    const graphql = {
      query: `{
        Get {
          ${className}(
            nearText: { concepts: ["${query.replace(/"/g, '\\"')}"] }
            limit: ${top_k}
          ) {
            text
            content
            chunk
            _additional { certainty distance }
          }
        }
      }`,
    };

    const res = await httpRequest(`${url}/v1/graphql`, {
      method: 'POST',
      headers,
      body: graphql,
    });

    if (res.status !== 200) return [];
    const results = res.data?.data?.Get?.[className] || [];
    return results
      .filter(r => (r._additional?.certainty || 0) >= score_threshold)
      .map(r => ({
        text: r.text || r.content || r.chunk || JSON.stringify(r),
        score: r._additional?.certainty || null,
        source: `weaviate/${collection}`,
      }));
  },

  /**
   * Milvus — https://milvus.io/docs/
   * REST API: POST /v2/vectordb/entities/search
   */
  async milvus(query, config) {
    const { url, collection, api_key, top_k = 5 } = config;
    const embedding = await getEmbedding(query, config);
    if (!embedding) return [];

    const headers = {};
    if (api_key) headers['Authorization'] = `Bearer ${api_key}`;

    const res = await httpRequest(`${url}/v2/vectordb/entities/search`, {
      method: 'POST',
      headers,
      body: {
        collectionName: collection,
        data: [embedding],
        limit: top_k,
        outputFields: ['text', 'content', 'chunk'],
      },
    });

    if (res.status !== 200 || !res.data?.data) return [];
    return (res.data.data || []).map(r => ({
      text: r.text || r.content || r.chunk || JSON.stringify(r),
      score: r.distance || r.score || null,
      source: `milvus/${collection}`,
    }));
  },

  /**
   * Redis Vector (RediSearch) — https://redis.io/docs/interact/search-and-query/
   * REST API: POST via Redis REST / RedisInsight API
   * Assumes redis-stack with REST API or a proxy like redis-rest.
   */
  async redis(query, config) {
    const { url, collection, api_key, top_k = 5 } = config;
    const embedding = await getEmbedding(query, config);
    if (!embedding) return [];

    const headers = {};
    if (api_key) headers['Authorization'] = `Bearer ${api_key}`;

    // Redis vector search via FT.SEARCH with KNN
    const indexName = collection || 'idx:knowledge';
    const res = await httpRequest(`${url}/search`, {
      method: 'POST',
      headers,
      body: {
        index: indexName,
        query: `*=>[KNN ${top_k} @embedding $BLOB AS score]`,
        params: { BLOB: embedding },
        return: ['text', 'content', 'chunk', 'score'],
        sortby: 'score',
        limit: { from: 0, size: top_k },
      },
    });

    if (res.status !== 200) return [];
    const results = res.data?.results || res.data?.documents || [];
    return results.map(r => {
      const fields = r.extra_attributes || r.fields || r;
      return {
        text: fields.text || fields.content || fields.chunk || JSON.stringify(fields),
        score: fields.score || null,
        source: `redis/${collection}`,
      };
    });
  },

  /**
   * OpenViking — OpenViking vector search
   * REST API: POST /api/v1/search
   */
  async openviking(query, config) {
    const { url, collection, api_key, top_k = 5 } = config;
    const embedding = await getEmbedding(query, config);

    const headers = {};
    if (api_key) headers['Authorization'] = `Bearer ${api_key}`;

    const body = {
      collection,
      top_k,
    };

    // Support both text and vector search
    if (embedding) {
      body.vector = embedding;
    } else {
      body.query = query;
    }

    const res = await httpRequest(`${url}/api/v1/search`, {
      method: 'POST',
      headers,
      body,
    });

    if (res.status !== 200) return [];
    const results = res.data?.results || res.data?.matches || [];
    return results.map(r => ({
      text: r.text || r.content || r.metadata?.text || JSON.stringify(r),
      score: r.score || r.similarity || null,
      source: `openviking/${collection}`,
    }));
  },
};

// ── Public API ──────────────────────────────────────────────────────────────

/**
 * Query the configured vector store for relevant knowledge.
 *
 * @param {string[]} queries - Claim texts to search for.
 * @param {object} config - Plugin config with vector_store section.
 * @returns {Promise<string|null>} Formatted results or null if not configured.
 */
async function queryVectorStore(queries, config) {
  const vsConfig = config.vector_store;
  if (!vsConfig || !vsConfig.provider || !vsConfig.url) return null;

  const adapter = adapters[vsConfig.provider];
  if (!adapter) {
    console.log(`[cove] Unknown vector store provider: ${vsConfig.provider}`);
    return null;
  }

  // Pass proxy settings alongside vector store config so adapters can call getEmbedding
  const adapterConfig = { ...vsConfig, proxy_port: config.proxy_port, proxy_key: config.proxy_key };

  const allResults = [];
  // Limit to 5 queries to control latency
  const limitedQueries = queries.slice(0, 5);

  for (const query of limitedQueries) {
    try {
      const results = await adapter(query, adapterConfig);
      if (results.length > 0) {
        const formatted = results.map(r =>
          `[${r.source}] (score: ${r.score != null ? r.score.toFixed(3) : 'N/A'})\n${r.text}`
        ).join('\n\n');
        allResults.push(`Query: "${query}"\n${formatted}`);
      }
    } catch (err) {
      console.log(`[cove] Vector store query failed for "${query.slice(0, 50)}...": ${err.message}`);
    }
  }

  return allResults.length > 0 ? allResults.join('\n\n---\n\n') : null;
}

/**
 * List supported vector store providers.
 */
function listProviders() {
  return Object.keys(adapters);
}

module.exports = { queryVectorStore, listProviders };
