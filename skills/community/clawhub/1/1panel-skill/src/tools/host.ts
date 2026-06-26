export const hostTools = [
  { name: "list_hosts", description: "List hosts", inputSchema: { type: "object", properties: {} } },
  { name: "get_host", description: "Get host", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "create_host", description: "Create host", inputSchema: { type: "object", properties: { name: { type: "string" }, addr: { type: "string" }, port: { type: "number" }, user: { type: "string" }, authMode: { type: "string" }, password: { type: "string" }, privateKey: { type: "string" }, groupID: { type: "number" }, description: { type: "string" } }, required: ["name", "addr"] } },
  { name: "update_host", description: "Update host", inputSchema: { type: "object", properties: { id: { type: "number" }, name: { type: "string" }, addr: { type: "string" }, port: { type: "number" }, user: { type: "string" }, groupID: { type: "number" }, description: { type: "string" } }, required: ["id"] } },
  { name: "delete_host", description: "Delete host", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "test_host_connection", description: "Test host connection", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "test_host_connection_by_info", description: "Test host connection by info", inputSchema: { type: "object", properties: { name: { type: "string" }, addr: { type: "string" }, port: { type: "number" }, user: { type: "string" }, authMode: { type: "string" }, password: { type: "string" }, privateKey: { type: "string" } }, required: ["name", "addr"] } },
  { name: "get_host_tree", description: "Get host tree", inputSchema: { type: "object", properties: {} } },
  { name: "update_host_group", description: "Update host group", inputSchema: { type: "object", properties: { id: { type: "number" }, groupID: { type: "number" } }, required: ["id", "groupID"] } },
  { name: "list_host_groups", description: "List host groups", inputSchema: { type: "object", properties: {} } },
  { name: "create_host_group", description: "Create host group", inputSchema: { type: "object", properties: { name: { type: "string" }, isDefault: { type: "boolean" } }, required: ["name"] } },
  { name: "update_host_group_by_id", description: "Update host group", inputSchema: { type: "object", properties: { id: { type: "number" }, name: { type: "string" }, isDefault: { type: "boolean" } }, required: ["id"] } },
  { name: "delete_host_group", description: "Delete host group", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "generate_host_ssh_key", description: "Generate host SSH key", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "get_host_ssh_key", description: "Get host SSH key", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "delete_host_ssh_key", description: "Delete host SSH key", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "sync_host_ssh_key", description: "Sync host SSH key", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "update_host_ssh_key", description: "Update host SSH key", inputSchema: { type: "object", properties: { id: { type: "number" }, authMode: { type: "string" }, password: { type: "string" }, privateKey: { type: "string" } }, required: ["id", "authMode"] } },
  { name: "get_host_ssh_conf", description: "Get host SSH config", inputSchema: { type: "object", properties: {} } },
  { name: "get_host_ssh_logs", description: "Get host SSH logs", inputSchema: { type: "object", properties: {} } },
];

export async function handleHostTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_hosts": return await client.listHosts();
    case "get_host": return await client.getHost(args?.id);
    case "create_host": return await client.createHost(args);
    case "update_host": return await client.updateHost(args);
    case "delete_host": return await client.deleteHost(args?.id);
    case "test_host_connection": return await client.testHostConnection(args?.id);
    case "test_host_connection_by_info": return await client.testHostConnectionByInfo(args);
    case "get_host_tree": return await client.getHostTree();
    case "update_host_group": return await client.updateHostGroup(args?.id, args?.groupID);
    case "list_host_groups": return await client.listHostGroups();
    case "create_host_group": return await client.createHostGroup(args);
    case "update_host_group_by_id": return await client.updateHostGroupByID(args);
    case "delete_host_group": return await client.deleteHostGroup(args?.id);
    case "generate_host_ssh_key": return await client.generateHostSSHKey(args?.id);
    case "get_host_ssh_key": return await client.getHostSSHKey(args?.id);
    case "delete_host_ssh_key": return await client.deleteHostSSHKey(args?.id);
    case "sync_host_ssh_key": return await client.syncHostSSHKey(args?.id);
    case "update_host_ssh_key": return await client.updateHostSSHKey(args?.id, args?.authMode, args?.password, args?.privateKey);
    case "get_host_ssh_conf": return await client.getHostSSHConf();
    case "get_host_ssh_logs": return await client.getHostSSHLogs();
    default: return null;
  }
}
