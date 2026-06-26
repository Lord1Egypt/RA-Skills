export const diskTools = [
  { name: "list_disks", description: "List disks", inputSchema: { type: "object", properties: {} } },
  { name: "get_disk_full_info", description: "Get full disk information", inputSchema: { type: "object", properties: {} } },
  { name: "mount_disk", description: "Mount disk", inputSchema: { type: "object", properties: { path: { type: "string" }, mountPoint: { type: "string" }, fsType: { type: "string" }, options: { type: "string" } }, required: ["path", "mountPoint"] } },
  { name: "partition_disk", description: "Partition disk", inputSchema: { type: "object", properties: { path: { type: "string" }, type: { type: "string" } }, required: ["path"] } },
  { name: "unmount_disk", description: "Unmount disk", inputSchema: { type: "object", properties: { mountPoint: { type: "string" } }, required: ["mountPoint"] } },
];

export async function handleDiskTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_disks": return await client.listDisks();
    case "get_disk_full_info": return await client.getDiskFullInfo();
    case "mount_disk": return await client.mountDisk(args);
    case "partition_disk": return await client.partitionDisk(args);
    case "unmount_disk": return await client.unmountDisk(args?.mountPoint);
    default: return null;
  }
}
