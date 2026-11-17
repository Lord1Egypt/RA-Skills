import { createCreatorSession } from "./session.mjs";

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
    async open({ taskName, startUrl, keepBrowser }) {
      const task = await openSpace(taskName);
      const page = task.page("p1");
      const session = createCreatorSession({ task, page, keep: Boolean(keepBrowser) });
      if (startUrl) await session.goto(startUrl);
      return session;
    },
  };
}
