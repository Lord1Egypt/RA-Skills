export const networkTools = [
  { name: "list_networks", description: "List networks", inputSchema: { type: "object", properties: {} } },
  { name: "create_network", description: "Create network", inputSchema: { type: "object", properties: { name: { type: "string" }, driver: { type: "string" } }, required: ["name"] } },
  { name: "remove_network", description: "Remove network", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
];

export async function handleNetworkTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_networks": return await client.listNetworks();
    case "create_network": return await client.createNetwork(args?.name, args?.driver);
    case "remove_network": return await client.removeNetwork(args?.id);
    default: return null;
  }
}
