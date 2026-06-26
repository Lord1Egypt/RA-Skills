// CAIRN_OFFLINE gate. When set ('1' or 'true'), cairn refuses any
// non-localhost network egress:
//   - `fetchWeb` throws (blocks `cairn add <url>` and refresh of web sources)
//   - `resolveModel` throws on hf:/http: ids (blocks first-use GGUF downloads)
//
// Localhost ollama is NOT blocked — it's not internet egress. For true
// air-gap, use CAIRN_RUNTIME=embedded with a pre-cached `modelPath`.
export const isOffline = () => process.env.CAIRN_OFFLINE === '1' || process.env.CAIRN_OFFLINE === 'true';
