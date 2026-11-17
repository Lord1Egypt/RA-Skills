import { describe, expect, test } from "bun:test";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { assessSimulationRecord, type SimulationRecord } from "./record.ts";

function record(): SimulationRecord {
  const tx = { from: `0x${"1".repeat(40)}`, to: `0x${"2".repeat(40)}`, value: "0", data: "0x12345678" };
  return {
    proposal: { chainId: 8453, transactions: [{ ...tx }, { ...tx, data: "0xaabbccdd" }] },
    simulation: {
      chainId: 8453, blockNumber: 123, mode: "sequential",
      transactions: [{ ...tx }, { ...tx, data: "0xaabbccdd" }], statuses: ["success", "success"], overrides: [],
      coverage: { assetChanges: true, authorityChanges: true, traces: true }, truncated: false,
    },
    asynchronousDestination: false,
  };
}
describe("simulation evidence boundaries", () => {
  test("complete byte-bound sequential evidence is ready for review only", () => {
    expect(assessSimulationRecord(record()).classification).toBe("ready-for-review");
    expect(assessSimulationRecord(record()).limitation).toContain("no authenticated provider proof");
  });
  test.each(["from", "to", "value", "data"] as const)("changed %s blocks reuse of a prior result", (field) => {
    const input = record();
    input.simulation.transactions[0]![field] = field === "value" ? "1" : field === "data" ? "0x" : `0x${"3".repeat(40)}`;
    expect(assessSimulationRecord(input).classification).toBe("blocked");
  });
  test("changed chain or reordered calls blocks reuse", () => {
    const input = record(); input.simulation.chainId = 1;
    expect(assessSimulationRecord(input).classification).toBe("blocked");
    const reordered = record(); reordered.simulation.transactions.reverse();
    expect(assessSimulationRecord(reordered).classification).toBe("blocked");
  });
  test("missing prerequisite transaction blocks partial coverage", () => {
    const input = record(); input.simulation.transactions.pop(); input.simulation.statuses.pop();
    expect(assessSimulationRecord(input).classification).toBe("blocked");
  });
  test("independent success labels cannot establish dependent execution", () => {
    const input = record(); input.simulation.mode = "independent";
    expect(assessSimulationRecord(input).classification).toBe("incomplete");
  });
  test("successful HTTP envelope with a reverted call is blocked", () => {
    const input = record(); input.simulation.statuses[1] = "reverted";
    expect(assessSimulationRecord(input).classification).toBe("blocked");
  });
  test("artificial funding is only an experiment", () => {
    const input = record(); input.simulation.overrides = ["token balance injected"];
    expect(assessSimulationRecord(input).classification).toBe("experiment-only");
  });
  test("unknown effects and truncated results remain incomplete", () => {
    const input = record(); input.simulation.coverage.authorityChanges = false; input.simulation.truncated = true;
    const result = assessSimulationRecord(input);
    expect(result.classification).toBe("incomplete"); expect(result.findings).toHaveLength(2);
  });
  test("source success cannot prove asynchronous destination execution", () => {
    const input = record(); input.asynchronousDestination = true;
    expect(assessSimulationRecord(input).classification).toBe("incomplete");
  });
  test("unknown per-call outcome remains incomplete", () => {
    const input = record(); input.simulation.statuses[1] = "unknown";
    expect(assessSimulationRecord(input).classification).toBe("incomplete");
  });
  test.each([{}, { proposal: {}, simulation: {} }, { ...record(), asynchronousDestination: undefined }])("invalid record fails explicitly", (input) => {
    expect(() => assessSimulationRecord(input)).toThrow();
  });
  test("unscaled hex value and abbreviated address are rejected", () => {
    const input = record(); input.proposal.transactions[0]!.value = "0x01";
    expect(() => assessSimulationRecord(input)).toThrow("decimal wei");
    input.proposal.transactions[0]!.value = "0"; input.proposal.transactions[0]!.to = "0x123";
    expect(() => assessSimulationRecord(input)).toThrow("full from/to");
  });
});


test("malformed JSON diagnostic never echoes private input", async () => {
  const directory = await mkdtemp(join(tmpdir(), "defi-record-"));
  const file = join(directory, "record.json");
  const privateMarker = "private-example-value-must-not-leak";
  try {
    await writeFile(file, `{ "secret": "${privateMarker}", invalid-json }`);
    const processResult = Bun.spawnSync([process.execPath, new URL("./record.ts", import.meta.url).pathname, file]);
    expect(processResult.exitCode).toBe(1);
    const output = `${processResult.stdout.toString()}${processResult.stderr.toString()}`;
    expect(output).toContain("Invalid record JSON");
    expect(output).not.toContain(privateMarker);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});
