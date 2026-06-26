export const gpuTools = [
  { name: "get_gpu_info", description: "Get GPU/XPU info (XPack)", inputSchema: { type: "object", properties: {} } },
  { name: "get_gpu_monitor_data", description: "Get GPU monitor data (XPack)", inputSchema: { type: "object", properties: { params: { type: "object" } }, required: ["params"] } },
];

export async function handleGPUTool(client: any, name: string, args: any) {
  switch (name) {
    case "get_gpu_info": return await client.getGPUInfo();
    case "get_gpu_monitor_data": return await client.getGPUMonitorData(args?.params);
    default: return null;
  }
}
