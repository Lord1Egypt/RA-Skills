// Runs on the Windows CI runner: what `run --exec` does with a real program, end to end.
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { programFound, shellCommand } from "../dist/work.js";

const alive = (pid) => {
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
};
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

assert.equal(programFound("node"), true);
assert.equal(programFound("no-such-program-brainchain"), false);

// Report 187: a real program's output reached nobody, while echo's did.
const piped = await shellCommand('node -e "process.stdin.pipe(process.stdout)"').run("a result from a task", {}, 30_000);
assert.equal(piped, "a result from a task");
const native = await shellCommand('findstr "^"').run("line one\r\nline two\r\n", {}, 30_000);
assert.equal(native, "line one\r\nline two\r\n");

// A command past its time is stopped with everything it started.
const pidFile = join(mkdtempSync(join(tmpdir(), "smoke-")), "child.pid");
let leader;
const hang = shellCommand(
  `node -e "const c=require('child_process').spawn(process.execPath,['-e','setInterval(()=>{},1000)'],{stdio:'ignore'});require('fs').writeFileSync(process.env.PIDFILE,String(c.pid));setInterval(()=>{},1000)"`,
  1_000,
);
await assert.rejects(hang.run("", { PIDFILE: pidFile }, 4_000, (pid) => (leader = pid)), /ran past 4 seconds/);
await wait(1_500);
const grandchild = Number(readFileSync(pidFile, "utf8"));
assert.equal(alive(leader), false, "the shell is still running");
assert.equal(alive(grandchild), false, "what the command started is still running");

console.log("windows smoke: output, a native program, and a stop that reaches the whole tree all pass");
