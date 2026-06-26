export const ftpTools = [
  { name: "list_ftp_users", description: "List FTP users", inputSchema: { type: "object", properties: {} } },
  { name: "get_ftp_base_info", description: "Get FTP base info", inputSchema: { type: "object", properties: {} } },
  { name: "create_ftp_user", description: "Create FTP user", inputSchema: { type: "object", properties: { userName: { type: "string" }, password: { type: "string" }, path: { type: "string" }, description: { type: "string" } }, required: ["userName", "password", "path"] } },
  { name: "update_ftp_user", description: "Update FTP user", inputSchema: { type: "object", properties: { id: { type: "number" }, password: { type: "string" }, path: { type: "string" }, description: { type: "string" } }, required: ["id"] } },
  { name: "delete_ftp_user", description: "Delete FTP user", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "operate_ftp", description: "Operate FTP (start/stop/restart)", inputSchema: { type: "object", properties: { operation: { type: "string", enum: ["start", "stop", "restart"] } }, required: ["operation"] } },
  { name: "sync_ftp_users", description: "Sync FTP users", inputSchema: { type: "object", properties: {} } },
  { name: "get_ftp_logs", description: "Get FTP logs", inputSchema: { type: "object", properties: {} } },
];

export async function handleFTPTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_ftp_users": return await client.listFTPUsers();
    case "get_ftp_base_info": return await client.getFTPBaseInfo();
    case "create_ftp_user": return await client.createFTPUser(args);
    case "update_ftp_user": return await client.updateFTPUser(args);
    case "delete_ftp_user": return await client.deleteFTPUser(args?.id);
    case "operate_ftp": return await client.operateFTP(args?.operation);
    case "sync_ftp_users": return await client.syncFTPUsers();
    case "get_ftp_logs": return await client.getFTPLogs();
    default: return null;
  }
}
