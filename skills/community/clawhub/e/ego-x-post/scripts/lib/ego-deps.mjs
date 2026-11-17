import { createXSession } from "./session.mjs";

function defaultTaskSpace(name) {
  const open = globalThis.taskSpace;
  if (typeof open !== "function") {
    throw new Error("taskSpace is only available inside ego-browser nodejs");
  }
  return open(name);
}

export function createEgoBrowser({ taskSpace: openSpace = defaultTaskSpace } = {}) {
  return {
    async open({ taskName, startUrl, keepBrowser }) {
      const task = await openSpace(taskName);
      const page = task.page("p1");
      const session = createXSession({ task, page, keep: Boolean(keepBrowser) });
      if (startUrl) await session.goto(startUrl);
      return session;
    },
  };
}
