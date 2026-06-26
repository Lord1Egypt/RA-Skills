export const backupTools = [
  { name: "list_backups", description: "List backups", inputSchema: { type: "object", properties: {} } },
  { name: "create_backup", description: "Create backup", inputSchema: { type: "object", properties: { backup: { type: "object" } }, required: ["backup"] } },
  { name: "restore_backup", description: "Restore backup", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "delete_backup", description: "Delete backup", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "list_backup_accounts", description: "List backup accounts", inputSchema: { type: "object", properties: {} } },
  { name: "get_backup_account_options", description: "Get backup account options", inputSchema: { type: "object", properties: {} } },
  { name: "get_backup_account_client_info", description: "Get backup account client info", inputSchema: { type: "object", properties: { clientType: { type: "string" } }, required: ["clientType"] } },
  { name: "create_backup_account", description: "Create backup account", inputSchema: { type: "object", properties: { type: { type: "string" }, name: { type: "string" }, vars: { type: "object" }, isDefault: { type: "boolean" } }, required: ["type", "name", "vars"] } },
  { name: "update_backup_account", description: "Update backup account", inputSchema: { type: "object", properties: { type: { type: "string" }, name: { type: "string" }, vars: { type: "object" }, isDefault: { type: "boolean" } }, required: ["type", "name", "vars"] } },
  { name: "delete_backup_account", description: "Delete backup account", inputSchema: { type: "object", properties: { type: { type: "string" }, name: { type: "string" } }, required: ["type"] } },
  { name: "check_backup_account", description: "Check backup account", inputSchema: { type: "object", properties: { type: { type: "string" }, vars: { type: "object" } }, required: ["type", "vars"] } },
  { name: "list_backup_account_files", description: "List files in backup account", inputSchema: { type: "object", properties: { backupAccountID: { type: "number" }, path: { type: "string" } }, required: ["backupAccountID"] } },
];

export async function handleBackupTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_backups": return await client.listBackups();
    case "create_backup": return await client.createBackup(args?.backup);
    case "restore_backup": return await client.restoreBackup(args?.id);
    case "delete_backup": return await client.deleteBackup(args?.id);
    case "list_backup_accounts": return await client.listBackupAccounts();
    case "get_backup_account_options": return await client.getBackupAccountOptions();
    case "get_backup_account_client_info": return await client.getBackupAccountClientInfo(args?.clientType);
    case "create_backup_account": return await client.createBackupAccount(args);
    case "update_backup_account": return await client.updateBackupAccount(args);
    case "delete_backup_account": return await client.deleteBackupAccount(args);
    case "check_backup_account": return await client.checkBackupAccount(args);
    case "list_backup_account_files": return await client.listBackupAccountFiles(args?.backupAccountID, args?.path);
    default: return null;
  }
}