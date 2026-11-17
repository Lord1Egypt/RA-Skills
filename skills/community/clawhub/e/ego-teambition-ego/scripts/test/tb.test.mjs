import assert from "node:assert/strict";
import test from "node:test";
import { DOMAIN_REGISTRY, dispatch, main } from "../tb.mjs";

function capture() {
  let text = "";
  return { text: () => text, write(chunk) { text += chunk; } };
}

const PROJECT = "a".repeat(24);
const PLAN = "b".repeat(24);

test("the registry is testcase only", () => {
  assert.deepEqual(Object.keys(DOMAIN_REGISTRY), ["testcase"]);
  assert.equal(DOMAIN_REGISTRY.testcase.phase, "2a");
});

test("main prints parse-url and usage", async () => {
  const stdout = capture();
  const stderr = capture();
  const url = `https://www.teambition.com/project/${PROJECT}/testplan/${PLAN}`;
  const code = await main(["testcase", "parse-url", url], { stdout, stderr });
  assert.equal(code, 0);
  assert.equal(stdout.text(), `${PROJECT}\t${PLAN}\t\n`);
  assert.equal(stderr.text(), "");

  const helpOut = capture();
  assert.equal(await main(["--help"], { stdout: helpOut, stderr: capture() }), 0);
  assert.match(helpOut.text(), /Phase 1 domain: testcase/);
  assert.equal(await main(["-h"], { stdout: capture(), stderr: capture() }), 0);

  const empty = capture();
  assert.equal(await main([], { stdout: empty, stderr: capture() }), 1);
  assert.match(empty.text(), /tb\.mjs/);
});

test("task and project are refused, unknown domains too", async () => {
  const task = await dispatch(["task", "list"]);
  assert.equal(task.exitCode, 1);
  assert.match(task.stderr, /尚未实现/);
  const project = await dispatch(["project"]);
  assert.match(project.stderr, /project/);
  const unknown = await dispatch(["wiki"]);
  assert.match(unknown.stderr, /未知 domain: wiki/);
  assert.match(unknown.stderr, /testcase/);

  const custom = await dispatch(["demo"], {
    registry: { demo: { phase: 2, run: async () => ({ exitCode: 0, stdout: "ok\n", stderr: "" }) } },
    future: [],
  });
  assert.equal(custom.stdout, "ok\n");

  const stdout = capture();
  const code = await main(["demo"], {
    stdout,
    stderr: capture(),
    registry: { demo: { run: async () => ({ stdout: "via main\n" }) } },
    future: [],
  });
  assert.equal(code, 1);
  assert.equal(stdout.text(), "via main\n");
});
