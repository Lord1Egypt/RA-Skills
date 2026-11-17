import { createMpSession } from "./session.mjs";

function defaultTaskSpace(name) {
  const open = globalThis.taskSpace;
  if (typeof open !== "function") {
    throw new Error("taskSpace is only available inside ego-browser nodejs");
  }
  return open(name);
}

function defaultListSpaces() {
  const list = globalThis.listTaskSpaces || globalThis.taskSpaces;
  if (typeof list !== "function") return null;
  return list();
}

export function createEgoBrowser({
  taskSpace: openSpace = defaultTaskSpace,
  listSpaces = defaultListSpaces,
} = {}) {
  return {
    listSpaces,
    async finishSpace(entry) {
      const task = await openSpace(entry.id || entry.name);
      await task.finish({ keep: [] });
      return true;
    },
    async open({ taskName, startUrl }) {
      const task = await openSpace(taskName);
      const page = task.page("p1");
      const session = createMpSession({ task, page });
      if (startUrl) await session.goto(startUrl);
      return session;
    },
  };
}
