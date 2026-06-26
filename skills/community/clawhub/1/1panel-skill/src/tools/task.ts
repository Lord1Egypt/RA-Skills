export const taskTools = [
  { name: "get_executing_task_count", description: "Get executing task count", inputSchema: { type: "object", properties: {} } },
  { name: "get_task_logs", description: "Get task logs", inputSchema: { type: "object", properties: {} } },
];

export async function handleTaskTool(client: any, name: string, _args: any) {
  switch (name) {
    case "get_executing_task_count": return await client.getExecutingTaskCount();
    case "get_task_logs": return await client.getTaskLogs();
    default: return null;
  }
}
