export const openrestyTools = [
  { name: "get_openresty_conf", description: "Get OpenResty configuration (XPack)", inputSchema: { type: "object", properties: {} } },
  { name: "build_openresty", description: "Build OpenResty (XPack)", inputSchema: { type: "object", properties: { params: { type: "object" } }, required: ["params"] } },
  { name: "update_openresty_by_file", description: "Update OpenResty config by file (XPack)", inputSchema: { type: "object", properties: { content: { type: "string" } }, required: ["content"] } },
  { name: "get_openresty_modules", description: "Get OpenResty modules (XPack)", inputSchema: { type: "object", properties: {} } },
  { name: "update_openresty_module", description: "Update OpenResty module (XPack)", inputSchema: { type: "object", properties: { params: { type: "object" } }, required: ["params"] } },
  { name: "get_openresty_partial_conf", description: "Get OpenResty partial config (XPack)", inputSchema: { type: "object", properties: {} } },
  { name: "get_openresty_status", description: "Get OpenResty status (XPack)", inputSchema: { type: "object", properties: {} } },
  { name: "update_openresty_conf", description: "Update OpenResty configuration (XPack)", inputSchema: { type: "object", properties: { params: { type: "object" } }, required: ["params"] } },
];

export async function handleOpenRestyTool(client: any, name: string, args: any) {
  switch (name) {
    case "get_openresty_conf": return await client.getOpenRestyConf();
    case "build_openresty": return await client.buildOpenResty(args?.params);
    case "update_openresty_by_file": return await client.updateOpenRestyByFile(args?.content);
    case "get_openresty_modules": return await client.getOpenRestyModules();
    case "update_openresty_module": return await client.updateOpenRestyModule(args?.params);
    case "get_openresty_partial_conf": return await client.getOpenRestyPartialConf();
    case "get_openresty_status": return await client.getOpenRestyStatus();
    case "update_openresty_conf": return await client.updateOpenRestyConf(args?.params);
    default: return null;
  }
}
