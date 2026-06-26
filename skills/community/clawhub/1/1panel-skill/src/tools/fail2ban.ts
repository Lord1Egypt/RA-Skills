export const fail2banTools = [
  { name: "get_fail2ban_base_info", description: "Get Fail2ban base info", inputSchema: { type: "object", properties: {} } },
  { name: "get_fail2ban_conf", description: "Get Fail2ban configuration", inputSchema: { type: "object", properties: {} } },
  { name: "operate_fail2ban", description: "Operate Fail2ban (start/stop/restart)", inputSchema: { type: "object", properties: { operation: { type: "string", enum: ["start", "stop", "restart"] } }, required: ["operation"] } },
  { name: "operate_fail2ban_ssh", description: "Operate Fail2ban SSH (start/stop/restart)", inputSchema: { type: "object", properties: { operation: { type: "string", enum: ["start", "stop", "restart"] } }, required: ["operation"] } },
  { name: "search_fail2ban_banned_ips", description: "Search banned IPs in Fail2ban", inputSchema: { type: "object", properties: { page: { type: "number" }, pageSize: { type: "number" } } } },
  { name: "update_fail2ban_conf", description: "Update Fail2ban configuration", inputSchema: { type: "object", properties: { key: { type: "string" }, value: { type: "string" } }, required: ["key", "value"] } },
  { name: "update_fail2ban_conf_by_file", description: "Update Fail2ban configuration by file content", inputSchema: { type: "object", properties: { content: { type: "string" } }, required: ["content"] } },
];

export async function handleFail2banTool(client: any, name: string, args: any) {
  switch (name) {
    case "get_fail2ban_base_info": return await client.getFail2BanBaseInfo();
    case "get_fail2ban_conf": return await client.getFail2BanConf();
    case "operate_fail2ban": return await client.operateFail2Ban(args);
    case "operate_fail2ban_ssh": return await client.operateFail2BanSSH(args);
    case "search_fail2ban_banned_ips": return await client.searchFail2BanBannedIPs(args);
    case "update_fail2ban_conf": return await client.updateFail2BanConf(args);
    case "update_fail2ban_conf_by_file": return await client.updateFail2BanConfByFile(args?.content);
    default: return null;
  }
}
