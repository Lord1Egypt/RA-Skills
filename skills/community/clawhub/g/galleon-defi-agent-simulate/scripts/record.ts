import { readFile } from "node:fs/promises";

export interface Transaction {
  from: string;
  to: string;
  value: string;
  data: string;
}
export interface SimulationRecord {
  proposal: { chainId: number; transactions: Transaction[] };
  simulation: {
    chainId: number;
    blockNumber: number;
    mode: "sequential" | "independent";
    transactions: Transaction[];
    statuses: ("success" | "reverted" | "unknown")[];
    overrides: string[];
    coverage: { assetChanges: boolean; authorityChanges: boolean; traces: boolean };
    truncated: boolean;
  };
  asynchronousDestination: boolean;
}
export interface Assessment {
  classification: "blocked" | "incomplete" | "experiment-only" | "ready-for-review";
  findings: string[];
  limitation: string;
}
const address = /^0x[0-9a-fA-F]{40}$/;
const calldata = /^0x(?:[0-9a-fA-F]{2})*$/;
const integer = /^(0|[1-9][0-9]*)$/;
const object = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value);
const positiveInteger = (value: unknown): value is number =>
  typeof value === "number" && Number.isSafeInteger(value) && value > 0;

function checkTransactions(value: unknown, label: string): asserts value is Transaction[] {
  if (!Array.isArray(value) || value.length === 0 || value.length > 100) {
    throw new Error(`${label} must contain 1 to 100 complete transactions`);
  }
  for (const [index, tx] of value.entries()) {
    if (!object(tx) || typeof tx.from !== "string" || !address.test(tx.from) ||
      typeof tx.to !== "string" || !address.test(tx.to) ||
      typeof tx.value !== "string" || !integer.test(tx.value) ||
      typeof tx.data !== "string" || !calldata.test(tx.data)) {
      throw new Error(`${label}[${index}] requires full from/to addresses, decimal wei value and even-length hex data`);
    }
  }
}
export function parseRecord(value: unknown): SimulationRecord {
  if (!object(value) || !object(value.proposal) || !object(value.simulation)) {
    throw new Error("record requires proposal and simulation objects");
  }
  const { proposal, simulation } = value;
  if (!positiveInteger(proposal.chainId) || !positiveInteger(simulation.chainId) ||
    typeof simulation.blockNumber !== "number" || !Number.isSafeInteger(simulation.blockNumber) ||
    simulation.blockNumber < 0 || !["sequential", "independent"].includes(String(simulation.mode))) {
    throw new Error("record requires positive chain IDs, nonnegative block number and explicit sequence mode");
  }
  checkTransactions(proposal.transactions, "proposal.transactions");
  checkTransactions(simulation.transactions, "simulation.transactions");
  if (!Array.isArray(simulation.statuses) || simulation.statuses.length !== simulation.transactions.length ||
    !simulation.statuses.every((status) => ["success", "reverted", "unknown"].includes(status))) {
    throw new Error("every simulated transaction requires success, reverted or unknown status");
  }
  const coverage = simulation.coverage;
  if (!Array.isArray(simulation.overrides) || !simulation.overrides.every((entry) => typeof entry === "string" && entry.length > 0) ||
    !object(coverage) || !["assetChanges", "authorityChanges", "traces"].every((key) => typeof coverage[key] === "boolean") ||
    typeof simulation.truncated !== "boolean" || typeof value.asynchronousDestination !== "boolean") {
    throw new Error("record requires overrides, explicit coverage, truncation and asynchronous destination declarations");
  }
  return value as unknown as SimulationRecord;
}
function identity(tx: Transaction): string {
  return JSON.stringify([tx.from.toLowerCase(), tx.to.toLowerCase(), tx.value, tx.data.toLowerCase()]);
}
export function assessSimulationRecord(value: unknown): Assessment {
  const { proposal, simulation, asynchronousDestination } = parseRecord(value);
  const blocked: string[] = [];
  const incomplete: string[] = [];
  if (proposal.chainId !== simulation.chainId) blocked.push("simulation chain differs from proposal chain");
  if (proposal.transactions.length !== simulation.transactions.length) {
    blocked.push("simulation does not bind every proposed transaction");
  } else {
    proposal.transactions.forEach((tx, index) => {
      if (identity(tx) !== identity(simulation.transactions[index]!)) blocked.push(`transaction ${index} sender, target, value, data or order differs`);
    });
  }
  if (simulation.statuses.includes("reverted")) blocked.push("at least one simulated transaction reverted");
  if (simulation.statuses.includes("unknown")) incomplete.push("at least one simulation outcome is unknown");
  if (proposal.transactions.length > 1 && simulation.mode !== "sequential") {
    incomplete.push("independent calls do not establish a stateful prerequisite sequence");
  }
  for (const [key, covered] of Object.entries(simulation.coverage)) {
    if (!covered) incomplete.push(`${key} coverage is unavailable`);
  }
  if (simulation.truncated) incomplete.push("simulation output is truncated");
  if (asynchronousDestination) incomplete.push("asynchronous destination effects require separate evidence");
  const experiments = simulation.overrides.map((entry) => `artificial state or bypass: ${entry}`);
  return {
    classification: blocked.length > 0 ? "blocked" : incomplete.length > 0 ? "incomplete" : experiments.length > 0 ? "experiment-only" : "ready-for-review",
    findings: [...blocked, ...incomplete, ...experiments],
    limitation: "Supplied record consistency only; no authenticated provider proof, freshness verification, safety, permission or settlement claim.",
  };
}
if (import.meta.main) {
  const argument = process.argv[2];
  if (argument === "--help" || argument === "-h") {
    process.stdout.write("Usage: bun record.ts <record.json>\nChecks supplied unsigned simulation evidence offline. Never signs, pays, broadcasts or queries providers.\n");
  } else {
    try {
      if (!argument || process.argv.length !== 3) throw new Error("Usage: bun record.ts <record.json>");
      const input = await readFile(argument, "utf8");
      if (input.length > 1_000_000) throw new Error("record exceeds 1 MB limit");
      process.stdout.write(`${JSON.stringify(assessSimulationRecord(JSON.parse(input)), null, 2)}\n`);
    } catch (error) {
      process.stderr.write(`${error instanceof SyntaxError ? "Invalid record JSON" : error instanceof Error ? error.message : "invalid record"}\n`);
      process.exitCode = 1;
    }
  }
}
