export const volumeTools = [
  { name: "list_volumes", description: "List volumes", inputSchema: { type: "object", properties: {} } },
  { name: "create_volume", description: "Create volume", inputSchema: { type: "object", properties: { name: { type: "string" } }, required: ["name"] } },
  { name: "remove_volume", description: "Remove volume", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
];

export async function handleVolumeTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_volumes": return await client.listVolumes();
    case "create_volume": return await client.createVolume(args?.name);
    case "remove_volume": return await client.removeVolume(args?.id);
    default: return null;
  }
}
