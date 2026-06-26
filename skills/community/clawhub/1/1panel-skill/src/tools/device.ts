export const deviceTools = [
  { name: "get_device_base_info", description: "Get device base info", inputSchema: { type: "object", properties: {} } },
  { name: "check_device_dns", description: "Check device DNS", inputSchema: { type: "object", properties: {} } },
  { name: "update_device", description: "Update device configuration", inputSchema: { type: "object", properties: { conf: { type: "object" } }, required: ["conf"] } },
  { name: "update_device_by_file", description: "Update device configuration by file", inputSchema: { type: "object", properties: { content: { type: "string" } }, required: ["content"] } },
  { name: "update_device_hosts", description: "Update device hosts", inputSchema: { type: "object", properties: { hosts: { type: "string" } }, required: ["hosts"] } },
  { name: "update_device_password", description: "Update device password", inputSchema: { type: "object", properties: { oldPass: { type: "string" }, newPass: { type: "string" } }, required: ["oldPass", "newPass"] } },
  { name: "update_device_swap", description: "Update device swap", inputSchema: { type: "object", properties: { swap: { type: "object" } }, required: ["swap"] } },
];

export async function handleDeviceTool(client: any, name: string, args: any) {
  switch (name) {
    case "get_device_base_info": return await client.getDeviceBaseInfo();
    case "check_device_dns": return await client.checkDeviceDNS();
    case "update_device": return await client.updateDevice(args?.conf);
    case "update_device_by_file": return await client.updateDeviceByFile(args?.content);
    case "update_device_hosts": return await client.updateDeviceHosts(args?.hosts);
    case "update_device_password": return await client.updateDevicePassword(args?.oldPass, args?.newPass);
    case "update_device_swap": return await client.updateDeviceSwap(args?.swap);
    default: return null;
  }
}
