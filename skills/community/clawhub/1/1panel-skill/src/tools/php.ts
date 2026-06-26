export const phpTools = [
  { name: "list_php_runtimes", description: "List PHP runtimes", inputSchema: { type: "object", properties: {} } },
  { name: "get_php_conf", description: "Get PHP config", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "update_php_conf", description: "Update PHP config", inputSchema: { type: "object", properties: { id: { type: "number" }, content: { type: "string" } }, required: ["id", "content"] } },
  { name: "list_php_extensions", description: "List PHP extensions", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "install_php_extension", description: "Install PHP extension", inputSchema: { type: "object", properties: { id: { type: "number" }, extension: { type: "string" } }, required: ["id", "extension"] } },
  { name: "uninstall_php_extension", description: "Uninstall PHP extension", inputSchema: { type: "object", properties: { id: { type: "number" }, extension: { type: "string" } }, required: ["id", "extension"] } },
  { name: "get_php_conf_file", description: "Get PHP config file", inputSchema: { type: "object", properties: { id: { type: "number" }, type: { type: "string" } }, required: ["id", "type"] } },
  { name: "update_php_conf_file", description: "Update PHP config file", inputSchema: { type: "object", properties: { id: { type: "number" }, type: { type: "string" }, content: { type: "string" } }, required: ["id", "type", "content"] } },
  { name: "update_php_version", description: "Update PHP version", inputSchema: { type: "object", properties: { id: { type: "number" }, version: { type: "string" } }, required: ["id", "version"] } },
];

export async function handlePHPTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_php_runtimes": return await client.listPHPRuntimes();
    case "get_php_conf": return await client.getPHPConf(args?.id);
    case "update_php_conf": return await client.updatePHPConf(args?.id, args?.content);
    case "list_php_extensions": return await client.listPHPExtensions(args?.id);
    case "install_php_extension": return await client.installPHPExtension(args?.id, args?.extension);
    case "uninstall_php_extension": return await client.uninstallPHPExtension(args?.id, args?.extension);
    case "get_php_conf_file": return await client.getPHPConfFile(args?.id, args?.type);
    case "update_php_conf_file": return await client.updatePHPConfFile(args?.id, args?.type, args?.content);
    case "update_php_version": return await client.updatePHPVersion(args?.id, args?.version);
    default: return null;
  }
}