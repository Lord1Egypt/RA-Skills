export const cronjobTools = [
  { name: "list_cronjobs", description: "List cronjobs", inputSchema: { type: "object", properties: {} } },
  { name: "create_cronjob", description: "Create cronjob", inputSchema: { type: "object", properties: { job: { type: "object" } }, required: ["job"] } },
  { name: "delete_cronjob", description: "Delete cronjob", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
];

export async function handleCronjobTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_cronjobs": return await client.listCronjobs();
    case "create_cronjob": return await client.createCronjob(args?.job);
    case "delete_cronjob": return await client.deleteCronjob(args?.id);
    default: return null;
  }
}
