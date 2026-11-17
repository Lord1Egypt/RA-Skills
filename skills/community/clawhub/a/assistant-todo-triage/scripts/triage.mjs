import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

function validDate(value) {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value))
    return false;
  const date = new Date(value + "T00:00:00Z");
  return (
    Number.isFinite(date.getTime()) && date.toISOString().slice(0, 10) === value
  );
}

export function triage(tasks, today) {
  if (!validDate(today)) throw Error("TODAY_INVALID");
  if (!Array.isArray(tasks) || tasks.length > 10000)
    throw Error("TASK_ARRAY_INVALID");
  const ids = new Set();
  const clean = tasks.map((task) => {
    if (
      !task ||
      typeof task.id !== "string" ||
      !/^[a-zA-Z0-9_-]{1,100}$/.test(task.id) ||
      typeof task.title !== "string" ||
      !task.title.trim() ||
      task.title.length > 200 ||
      Array.from(task.title).some(
        (c) => c.charCodeAt(0) < 32 || c.charCodeAt(0) === 127,
      ) ||
      !(task.dueDate === null || validDate(task.dueDate)) ||
      !Number.isInteger(task.priority) ||
      task.priority < 1 ||
      task.priority > 4 ||
      !["open", "completed"].includes(task.status)
    )
      throw Error("TASK_INVALID");
    if (ids.has(task.id)) throw Error("DUPLICATE_ID");
    ids.add(task.id);
    const { id, title, dueDate, priority, status } = task;
    return { id, title, dueDate, priority, status };
  });
  const compare = (a, b) => (a < b ? -1 : a > b ? 1 : 0);
  const open = clean
    .filter((task) => task.status === "open")
    .sort(
      (a, b) =>
        compare(a.dueDate ?? "9999-99-99", b.dueDate ?? "9999-99-99") ||
        a.priority - b.priority ||
        compare(a.id, b.id),
    );
  return {
    today,
    total: clean.length,
    completed: clean.length - open.length,
    overdue: open.filter(
      (task) => task.dueDate !== null && task.dueDate < today,
    ),
    dueToday: open.filter((task) => task.dueDate === today),
    upcoming: open.filter(
      (task) => task.dueDate !== null && task.dueDate > today,
    ),
    undated: open.filter((task) => task.dueDate === null),
  };
}

if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(process.argv[1]).href
) {
  try {
    if (process.argv.length !== 4)
      throw Error("USAGE: triage.mjs INPUT.json YYYY-MM-DD");
    const bytes = readFileSync(process.argv[2]);
    if (bytes.length > 5000000) throw Error("INPUT_TOO_LARGE");
    console.log(
      JSON.stringify(
        triage(JSON.parse(bytes.toString("utf8")), process.argv[3]),
        null,
        2,
      ),
    );
  } catch (error) {
    console.error(
      error instanceof SyntaxError ? "INVALID_JSON" : error.message,
    );
    process.exitCode = 1;
  }
}
