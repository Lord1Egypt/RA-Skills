export const ollamaTools = [
  { name: "list_ollama_models", description: "List Ollama models (XPack)", inputSchema: { type: "object", properties: {} } },
  { name: "create_ollama_model", description: "Create Ollama model (XPack)", inputSchema: { type: "object", properties: { name: { type: "string" } }, required: ["name"] } },
  { name: "delete_ollama_model", description: "Delete Ollama model (XPack)", inputSchema: { type: "object", properties: { ids: { type: "array", items: { type: "number" } } }, required: ["ids"] } },
  { name: "load_ollama_model", description: "Load Ollama model (XPack)", inputSchema: { type: "object", properties: { name: { type: "string" } }, required: ["name"] } },
  { name: "recreate_ollama_model", description: "Recreate Ollama model (XPack)", inputSchema: { type: "object", properties: { name: { type: "string" } }, required: ["name"] } },
  { name: "sync_ollama_models", description: "Sync Ollama models (XPack)", inputSchema: { type: "object", properties: {} } },
  { name: "close_ollama_model", description: "Close Ollama model connection (XPack)", inputSchema: { type: "object", properties: { name: { type: "string" } }, required: ["name"] } },
];

export async function handleOllamaTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_ollama_models": return await client.listOllamaModels();
    case "create_ollama_model": return await client.createOllamaModel(args?.name);
    case "delete_ollama_model": return await client.deleteOllamaModel(args?.ids);
    case "load_ollama_model": return await client.loadOllamaModel(args?.name);
    case "recreate_ollama_model": return await client.recreateOllamaModel(args?.name);
    case "sync_ollama_models": return await client.syncOllamaModels();
    case "close_ollama_model": return await client.closeOllamaModel(args?.name);
    default: return null;
  }
}
