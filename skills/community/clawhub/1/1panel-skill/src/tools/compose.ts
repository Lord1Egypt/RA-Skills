export const composeTools = [
  { name: "list_composes", description: "List compose projects", inputSchema: { type: "object", properties: {} } },
  { name: "create_compose", description: "Create compose", inputSchema: { type: "object", properties: { name: { type: "string" }, content: { type: "string" } }, required: ["name", "content"] } },
  { name: "remove_compose", description: "Remove compose", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "start_compose", description: "Start compose", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "stop_compose", description: "Stop compose", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "restart_compose", description: "Restart compose", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "update_compose", description: "Update compose", inputSchema: { type: "object", properties: { id: { type: "number" }, content: { type: "string" } }, required: ["id", "content"] } },
  { name: "test_compose", description: "Test compose", inputSchema: { type: "object", properties: { content: { type: "string" } }, required: ["content"] } },
  { name: "get_compose_env", description: "Get compose environment", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "clean_compose_log", description: "Clean compose log", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
];

export async function handleComposeTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_composes": return await client.listComposes();
    case "create_compose": return await client.createCompose(args?.name, args?.content, args?.path);
    case "remove_compose": return await client.removeCompose(args?.id);
    case "start_compose": return await client.startCompose(args?.id);
    case "stop_compose": return await client.stopCompose(args?.id);
    case "restart_compose": return await client.restartCompose(args?.id);
    case "update_compose": return await client.updateCompose(args?.id, args?.content);
    case "test_compose": return await client.testCompose(args?.content);
    case "get_compose_env": return await client.getComposeEnv(args?.id);
    case "clean_compose_log": return await client.cleanComposeLog(args?.id);
    default: return null;
  }
}
