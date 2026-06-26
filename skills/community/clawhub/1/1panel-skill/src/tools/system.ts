export const systemTools = [
  { name: "get_system_info", description: "Get system info", inputSchema: { type: "object", properties: {} } },
  { name: "get_system_monitor", description: "Get system monitor", inputSchema: { type: "object", properties: {} } },
  { name: "get_dashboard_base_info", description: "Get dashboard base info", inputSchema: { type: "object", properties: {} } },
  { name: "get_dashboard_current_info", description: "Get dashboard current info", inputSchema: { type: "object", properties: {} } },
  { name: "get_dashboard_memo", description: "Get dashboard memo", inputSchema: { type: "object", properties: {} } },
  { name: "update_dashboard_memo", description: "Update dashboard memo", inputSchema: { type: "object", properties: { content: { type: "string" } }, required: ["content"] } },
  { name: "get_monitor_data", description: "Get monitor data", inputSchema: { type: "object", properties: { startTime: { type: "string" }, endTime: { type: "string" } } } },
  { name: "get_monitor_setting", description: "Get monitor setting", inputSchema: { type: "object", properties: {} } },
  { name: "update_monitor_setting", description: "Update monitor setting", inputSchema: { type: "object", properties: { setting: { type: "object" } }, required: ["setting"] } },
  { name: "clean_monitor_data", description: "Clean monitor data", inputSchema: { type: "object", properties: {} } },
  { name: "list_processes", description: "List processes", inputSchema: { type: "object", properties: {} } },
  { name: "kill_process", description: "Kill process", inputSchema: { type: "object", properties: { pid: { type: "number" } }, required: ["pid"] } },
  { name: "get_ssh_config", description: "Get SSH config", inputSchema: { type: "object", properties: {} } },
  { name: "update_ssh_config", description: "Update SSH config", inputSchema: { type: "object", properties: { config: { type: "object" } }, required: ["config"] } },
  { name: "exec_command", description: "Execute command", inputSchema: { type: "object", properties: { command: { type: "string" }, cwd: { type: "string" } }, required: ["command"] } },
  { name: "get_settings", description: "Get settings", inputSchema: { type: "object", properties: {} } },
  { name: "update_settings", description: "Update settings", inputSchema: { type: "object", properties: { settings: { type: "object" } }, required: ["settings"] } },
  { name: "list_operation_logs", description: "List operation logs", inputSchema: { type: "object", properties: {} } },
  { name: "list_system_logs", description: "List system logs", inputSchema: { type: "object", properties: {} } },
];

export async function handleSystemTool(client: any, name: string, args: any) {
  switch (name) {
    case "get_system_info": return await client.getSystemInfo();
    case "get_system_monitor": return await client.getSystemMonitor();
    case "get_dashboard_base_info": return await client.getDashboardBaseInfo();
    case "get_dashboard_current_info": return await client.getDashboardCurrentInfo();
    case "get_dashboard_memo": return await client.getDashboardMemo();
    case "update_dashboard_memo": return await client.updateDashboardMemo(args?.content);
    case "get_monitor_data": return await client.getMonitorData(args);
    case "get_monitor_setting": return await client.getMonitorSetting();
    case "update_monitor_setting": return await client.updateMonitorSetting(args?.setting);
    case "clean_monitor_data": return await client.cleanMonitorData();
    case "list_processes": return await client.listProcesses();
    case "kill_process": return await client.killProcess(args?.pid);
    case "get_ssh_config": return await client.getSSHConfig();
    case "update_ssh_config": return await client.updateSSHConfig(args?.config);
    case "exec_command": return await client.execCommand(args?.command, args?.cwd);
    case "get_settings": return await client.getSettings();
    case "update_settings": return await client.updateSettings(args?.settings);
    case "list_operation_logs": return await client.listOperationLogs();
    case "list_system_logs": return await client.listSystemLogs();
    default: return null;
  }
}
