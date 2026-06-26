export const recycleBinTools = [
  { name: "get_recycle_bin_status", description: "Get recycle bin status", inputSchema: { type: "object", properties: {} } },
  { name: "list_recycle_bin", description: "List recycle bin files", inputSchema: { type: "object", properties: {} } },
  { name: "clear_recycle_bin", description: "Clear recycle bin", inputSchema: { type: "object", properties: {} } },
  { name: "reduce_recycle_bin", description: "Restore file from recycle bin", inputSchema: { type: "object", properties: { name: { type: "string" } }, required: ["name"] } },
];

export async function handleRecycleBinTool(client: any, name: string, args: any) {
  switch (name) {
    case "get_recycle_bin_status": return await client.getRecycleBinStatus();
    case "list_recycle_bin": return await client.listRecycleBin();
    case "clear_recycle_bin": return await client.clearRecycleBin();
    case "reduce_recycle_bin": return await client.reduceRecycleBin(args?.name);
    default: return null;
  }
}
