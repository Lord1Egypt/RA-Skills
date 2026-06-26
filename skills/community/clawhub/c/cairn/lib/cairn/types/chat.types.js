// Chat client contract. Two layers:
//   ChatRuntime — the swappable backend (ollama / llama.cpp). Stateless from
//     the provider's POV; the provider holds the cached `_healthy` flag.
//   Chat        — the public surface that providers (Ingest, doc-extract) DI.
//
// Both share the same shape; the Chat interface adds the cached `healthy`
// getter that ChatProvider maintains across runtime calls.
export {};
