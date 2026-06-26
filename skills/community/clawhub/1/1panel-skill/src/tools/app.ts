export const appTools = [
  { name: "list_installed_apps", description: "List installed apps", inputSchema: { type: "object", properties: {} } },
  { name: "list_app_store", description: "List app store", inputSchema: { type: "object", properties: {} } },
  { name: "install_app", description: "Install app", inputSchema: { type: "object", properties: { app: { type: "object" } }, required: ["app"] } },
  { name: "uninstall_app", description: "Uninstall app", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "update_app", description: "Update app", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
];

export async function handleAppTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_installed_apps": return await client.listInstalledApps();
    case "list_app_store": return await client.listAppStore();
    case "install_app": return await client.installApp(args?.app);
    case "uninstall_app": return await client.uninstallApp(args?.id);
    case "update_app": return await client.updateApp(args?.id);
    default: return null;
  }
}
