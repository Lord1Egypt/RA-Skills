export const clamTools = [
  { name: "list_clam_configs", description: "List ClamAV configs", inputSchema: { type: "object", properties: {} } },
  { name: "get_clam_base_info", description: "Get ClamAV base info", inputSchema: { type: "object", properties: {} } },
  { name: "create_clam_config", description: "Create ClamAV config", inputSchema: { type: "object", properties: { name: { type: "string" }, path: { type: "string" }, description: { type: "string" } }, required: ["name", "path"] } },
  { name: "update_clam_config", description: "Update ClamAV config", inputSchema: { type: "object", properties: { id: { type: "number" }, name: { type: "string" }, path: { type: "string" }, description: { type: "string" } }, required: ["id"] } },
  { name: "delete_clam_config", description: "Delete ClamAV config", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "get_clam_file", description: "Get ClamAV file config", inputSchema: { type: "object", properties: {} } },
  { name: "update_clam_file", description: "Update ClamAV file config", inputSchema: { type: "object", properties: { content: { type: "string" } }, required: ["content"] } },
  { name: "scan_clam", description: "Scan with ClamAV", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "get_clam_records", description: "Get ClamAV scan records", inputSchema: { type: "object", properties: {} } },
  { name: "clean_clam_records", description: "Clean ClamAV records", inputSchema: { type: "object", properties: {} } },
  { name: "update_clam_status", description: "Update ClamAV status", inputSchema: { type: "object", properties: { status: { type: "string" } }, required: ["status"] } },
];

export async function handleClamTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_clam_configs": return await client.listClamConfigs();
    case "get_clam_base_info": return await client.getClamBaseInfo();
    case "create_clam_config": return await client.createClamConfig(args);
    case "update_clam_config": return await client.updateClamConfig(args);
    case "delete_clam_config": return await client.deleteClamConfig(args?.id);
    case "get_clam_file": return await client.getClamFile();
    case "update_clam_file": return await client.updateClamFile(args?.content);
    case "scan_clam": return await client.scanClam(args?.id);
    case "get_clam_records": return await client.getClamRecords();
    case "clean_clam_records": return await client.cleanClamRecords();
    case "update_clam_status": return await client.updateClamStatus(args?.status);
    default: return null;
  }
}
