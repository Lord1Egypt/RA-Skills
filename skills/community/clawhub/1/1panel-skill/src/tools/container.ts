export const containerTools = [
  { name: "list_containers", description: "List Docker containers", inputSchema: { type: "object", properties: {} } },
  { name: "list_containers_simple", description: "List containers (simple)", inputSchema: { type: "object", properties: {} } },
  { name: "get_container", description: "Get container info", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
  { name: "inspect_container", description: "Inspect container", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
  { name: "start_container", description: "Start container", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
  { name: "stop_container", description: "Stop container", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
  { name: "restart_container", description: "Restart container", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
  { name: "pause_container", description: "Pause container", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
  { name: "unpause_container", description: "Unpause container", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
  { name: "kill_container", description: "Kill container", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
  { name: "remove_container", description: "Remove container", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
  { name: "create_container", description: "Create container", inputSchema: { type: "object", properties: { config: { type: "object" } }, required: ["config"] } },
  { name: "update_container", description: "Update container", inputSchema: { type: "object", properties: { id: { type: "string" }, config: { type: "object" } }, required: ["id", "config"] } },
  { name: "rename_container", description: "Rename container", inputSchema: { type: "object", properties: { id: { type: "string" }, name: { type: "string" } }, required: ["id", "name"] } },
  { name: "upgrade_container", description: "Upgrade container", inputSchema: { type: "object", properties: { id: { type: "string" }, image: { type: "string" } }, required: ["id", "image"] } },
  { name: "get_container_logs", description: "Get container logs", inputSchema: { type: "object", properties: { id: { type: "string" }, tail: { type: "number" } }, required: ["id"] } },
  { name: "get_container_stats", description: "Get container stats", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
  { name: "get_container_status", description: "Get containers status", inputSchema: { type: "object", properties: {} } },
  { name: "prune_containers", description: "Prune containers", inputSchema: { type: "object", properties: {} } },
  { name: "clean_container_log", description: "Clean container log", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
  { name: "get_container_users", description: "Get container users", inputSchema: { type: "object", properties: { name: { type: "string" } }, required: ["name"] } },
  { name: "list_containers_by_image", description: "List containers by image", inputSchema: { type: "object", properties: { image: { type: "string" } }, required: ["image"] } },
  { name: "commit_container", description: "Commit container", inputSchema: { type: "object", properties: { id: { type: "string" }, repo: { type: "string" }, tag: { type: "string" } }, required: ["id", "repo", "tag"] } },
];

export async function handleContainerTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_containers": return await client.listContainers();
    case "list_containers_simple": return await client.listContainersSimple();
    case "get_container": return await client.getContainer(args?.id);
    case "inspect_container": return await client.inspectContainer(args?.id);
    case "start_container": return await client.startContainer(args?.id);
    case "stop_container": return await client.stopContainer(args?.id);
    case "restart_container": return await client.restartContainer(args?.id);
    case "pause_container": return await client.pauseContainer(args?.id);
    case "unpause_container": return await client.unpauseContainer(args?.id);
    case "kill_container": return await client.killContainer(args?.id);
    case "remove_container": return await client.removeContainer(args?.id);
    case "create_container": return await client.createContainer(args?.config);
    case "update_container": return await client.updateContainer(args?.id, args?.config);
    case "rename_container": return await client.renameContainer(args?.id, args?.name);
    case "upgrade_container": return await client.upgradeContainer(args?.id, args?.image);
    case "get_container_logs": return await client.getContainerLogs(args?.id, args?.tail);
    case "get_container_stats": return await client.getContainerStats(args?.id);
    case "get_container_status": return await client.getContainerStatus();
    case "prune_containers": return await client.pruneContainers();
    case "clean_container_log": return await client.cleanContainerLog(args?.id);
    case "get_container_users": return await client.getContainerUsers(args?.name);
    case "list_containers_by_image": return await client.listContainersByImage(args?.image);
    case "commit_container": return await client.commitContainer(args?.id, args?.repo, args?.tag);
    default: return null;
  }
}
