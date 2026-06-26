export const runtimeTools = [
  { name: "list_environments", description: "List environments", inputSchema: { type: "object", properties: { type: { type: "string" } }, required: ["type"] } },
  { name: "install_environment", description: "Install environment", inputSchema: { type: "object", properties: { type: { type: "string" }, config: { type: "object" } }, required: ["type", "config"] } },
  { name: "uninstall_environment", description: "Uninstall environment", inputSchema: { type: "object", properties: { type: { type: "string" }, id: { type: "number" } }, required: ["type", "id"] } },
];

export async function handleRuntimeTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_environments": return await client.listEnvironments(args?.type);
    case "install_environment": return await client.installEnvironment(args?.type, args?.config);
    case "uninstall_environment": return await client.uninstallEnvironment(args?.type, args?.id);
    default: return null;
  }
}
