export const snapshotTools = [
  { name: "list_snapshots", description: "List system snapshots", inputSchema: { type: "object", properties: {} } },
  { name: "create_snapshot", description: "Create system snapshot", inputSchema: { type: "object", properties: { name: { type: "string" }, description: { type: "string" }, withDocker: { type: "boolean" } }, required: ["name"] } },
  { name: "delete_snapshot", description: "Delete system snapshot", inputSchema: { type: "object", properties: { ids: { type: "array", items: { type: "number" } } }, required: ["ids"] } },
  { name: "update_snapshot_description", description: "Update snapshot description", inputSchema: { type: "object", properties: { id: { type: "number" }, description: { type: "string" } }, required: ["id", "description"] } },
  { name: "import_snapshot", description: "Import system snapshot", inputSchema: { type: "object", properties: { from: { type: "string" }, names: { type: "array", items: { type: "string" } } }, required: ["from", "names"] } },
  { name: "load_snapshot", description: "Load snapshot data", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "recover_snapshot", description: "Recover from snapshot", inputSchema: { type: "object", properties: { id: { type: "number" }, isNewSnapshot: { type: "boolean" } }, required: ["id"] } },
  { name: "recreate_snapshot", description: "Recreate snapshot", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
];

export async function handleSnapshotTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_snapshots": return await client.listSnapshots();
    case "create_snapshot": return await client.createSnapshot(args);
    case "delete_snapshot": return await client.deleteSnapshot(args?.ids);
    case "update_snapshot_description": return await client.updateSnapshotDescription(args?.id, args?.description);
    case "import_snapshot": return await client.importSnapshot(args);
    case "load_snapshot": return await client.loadSnapshot(args?.id);
    case "recover_snapshot": return await client.recoverSnapshot(args?.id, args?.isNewSnapshot);
    case "recreate_snapshot": return await client.recreateSnapshot(args?.id);
    default: return null;
  }
}
