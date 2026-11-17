import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";

/** One field of `ps` for a process, or undefined when it is gone or ps cannot tell. */
export function ps(pid: number, field: "etime" | "pgid"): string | undefined {
  const result = spawnSync("ps", ["-o", `${field}=`, "-p", String(pid)], { encoding: "utf8" });
  return result.status === 0 ? result.stdout.trim() : undefined;
}

/** The fields of a process's /proc stat after its name, which can hold spaces and parentheses, so the first is field 3. */
function statFields(pid: number): string[] {
  const stat = readFileSync(`/proc/${pid}/stat`, "utf8");
  return stat.slice(stat.lastIndexOf(")") + 2).split(" ");
}

/**
 * When a Linux process started, from /proc, which slim container images have
 * without ps. The kernel counts it in ticks since boot, 100 a second on every
 * architecture Node.js runs on.
 */
function procStart(pid: number): number | undefined {
  try {
    const ticks = Number(statFields(pid)[19]);
    const boot = Number(/^btime (\d+)$/m.exec(readFileSync("/proc/stat", "utf8"))?.[1]);
    return Number.isSafeInteger(ticks) && boot > 0 ? boot * 1000 + ticks * 10 : undefined;
  } catch {
    return undefined;
  }
}

/** When a process started, in ms since the epoch, or undefined when it is gone or neither /proc nor ps can tell. */
export function startTime(pid: number): number | undefined {
  const started = procStart(pid);
  if (started !== undefined) return started;
  const elapsed = /^(?:(?:(\d+)-)?(\d+):)?(\d+):(\d+)$/.exec(ps(pid, "etime") ?? "");
  if (!elapsed) return undefined;
  const [days, hours, minutes, seconds] = elapsed.slice(1).map((part) => Number(part ?? 0)) as [number, number, number, number];
  return Date.now() - (((days * 24 + hours) * 60 + minutes) * 60 + seconds) * 1000;
}

/** A process's group, from ps or, where there is none, field 5 of its /proc stat; undefined when neither can tell. */
export function processGroup(pid: number): string | undefined {
  const group = ps(pid, "pgid");
  if (group !== undefined) return group;
  try {
    return statFields(pid)[2];
  } catch {
    return undefined;
  }
}
