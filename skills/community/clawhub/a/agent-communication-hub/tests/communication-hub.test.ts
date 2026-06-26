import { afterEach, describe, expect, test } from "vitest";
import { CommunicationHub } from "../src/CommunicationHub.js";

function createHub(): CommunicationHub {
  const hub = new CommunicationHub();
  hub.sessions.registerAgent({ id: "agent-alpha", name: "Alpha" });
  hub.sessions.registerAgent({ id: "agent-beta", name: "Beta" });
  hub.sessions.registerAgent({ id: "agent-gamma", name: "Gamma" });
  return hub;
}

let activeHub: CommunicationHub | undefined;

afterEach(() => {
  activeHub?.close();
  activeHub = undefined;
});

describe("CommunicationHub", () => {
  test("queues direct messages for offline agents and drains them on reconnect", () => {
    activeHub = createHub();
    activeHub.sessions.connectAgent({ agentId: "agent-alpha" });

    const message = activeHub.sendDirectMessage({
      senderId: "agent-alpha",
      recipientId: "agent-beta",
      payload: { text: "ping" },
    });

    expect(message.status).toBe("pending");
    expect(activeHub.getPendingMessages("agent-beta")).toHaveLength(1);

    activeHub.sessions.connectAgent({ agentId: "agent-beta" });
    const delivered = activeHub.drainOfflineQueue("agent-beta");

    expect(delivered).toHaveLength(1);
    expect(delivered[0]?.status).toBe("delivered");
  });

  test("acknowledges delivered messages", () => {
    activeHub = createHub();
    activeHub.sessions.connectAgent({ agentId: "agent-alpha" });
    activeHub.sessions.connectAgent({ agentId: "agent-beta" });

    const message = activeHub.sendPrivateMessage({
      senderId: "agent-alpha",
      recipientId: "agent-beta",
      payload: { text: "secret" },
      topic: "private.sync",
    });

    expect(message.status).toBe("delivered");

    const acknowledged = activeHub.acknowledgeMessage(message.id);
    expect(acknowledged.status).toBe("acknowledged");
    expect(acknowledged.acknowledgedAt).not.toBeNull();
  });

  test("broadcasts to all other registered agents", () => {
    activeHub = createHub();
    activeHub.sessions.connectAgent({ agentId: "agent-alpha" });
    activeHub.sessions.connectAgent({ agentId: "agent-beta" });

    const messages = activeHub.broadcastMessage({
      senderId: "agent-alpha",
      payload: { announcement: true },
      topic: "system.broadcast",
    });

    expect(messages).toHaveLength(2);
    expect(messages.map((message) => message.recipientId).sort()).toEqual(["agent-beta", "agent-gamma"]);
  });

  test("tracks subscriptions and replays matching events", () => {
    activeHub = createHub();
    activeHub.events.subscribe("agent-beta", "task.updated", { priority: "high" });
    activeHub.events.subscribe("agent-gamma", "task.updated", { priority: "low" });

    const published = activeHub.events.publish({
      type: "task.updated",
      sourceAgentId: "agent-alpha",
      payload: { id: "task-1", priority: "high" },
      metadata: { origin: "planner" },
    });

    expect(published.recipients).toEqual(["agent-beta"]);

    const replayed = activeHub.events.replay({ type: "task.updated", limit: 10 });
    expect(replayed).toHaveLength(1);
    expect(replayed[0]?.payload).toMatchObject({ id: "task-1" });
  });

  test("stores session history", () => {
    activeHub = createHub();
    activeHub.sessions.connectAgent({ agentId: "agent-beta", metadata: { region: "cn" } });
    activeHub.sessions.disconnectAgent("agent-beta");

    const history = activeHub.sessions.getSessionHistory("agent-beta");
    expect(history).toHaveLength(1);
    expect(history[0]?.status).toBe("disconnected");
    expect(history[0]?.metadata).toMatchObject({ region: "cn" });
  });
});
