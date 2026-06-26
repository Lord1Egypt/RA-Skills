import { CommunicationHub } from "../src/CommunicationHub.js";

const hub = new CommunicationHub({ dbPath: "./agent-hub.sqlite" });

hub.sessions.registerAgent({ id: "planner", name: "Planner Agent", metadata: { role: "planner" } });
hub.sessions.registerAgent({ id: "executor", name: "Executor Agent", metadata: { role: "executor" } });
hub.sessions.registerAgent({ id: "observer", name: "Observer Agent", metadata: { role: "observer" } });

hub.sessions.connectAgent({ agentId: "planner" });
hub.sessions.connectAgent({ agentId: "executor" });

hub.events.subscribe("observer", "task.created", { priority: "high" });

const direct = hub.sendDirectMessage({
  senderId: "planner",
  recipientId: "executor",
  payload: { taskId: "task-42", action: "analyze" },
  topic: "task.assign",
});

const eventResult = hub.events.publish({
  type: "task.created",
  sourceAgentId: "planner",
  payload: { taskId: "task-42", priority: "high" },
  metadata: { traceId: "trace-1" },
});

console.log("Direct message:", direct);
console.log("Event recipients:", eventResult.recipients);
console.log("Replay:", hub.events.replay({ type: "task.created" }));

hub.close();
