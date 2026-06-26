export const nodeTools = [
  { name: "get_node_modules", description: "Get Node modules (XPack)", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "operate_node_module", description: "Operate Node module (XPack)", inputSchema: { type: "object", properties: { id: { type: "number" }, params: { type: "object" } }, required: ["id", "params"] } },
  { name: "get_node_package_scripts", description: "Get Node package scripts (XPack)", inputSchema: { type: "object", properties: { id: { type: "number" }, params: { type: "object" } }, required: ["id", "params"] } },
];

export async function handleNodeTool(client: any, name: string, args: any) {
  switch (name) {
    case "get_node_modules": return await client.getNodeModules(args?.id);
    case "operate_node_module": return await client.operateNodeModule(args?.id, args?.params);
    case "get_node_package_scripts": return await client.getNodePackageScripts(args?.id, args?.params);
    default: return null;
  }
}
