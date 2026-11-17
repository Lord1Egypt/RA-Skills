import { readdirSync, readFileSync } from "node:fs";
import { join, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

import { BOND_LEAD_SEC } from "./bond.js";
import { usage } from "./cli.js";

const root = fileURLToPath(new URL("..", import.meta.url));
const read = (path: string) => readFileSync(join(root, path), "utf8");
const json = (path: string) => JSON.parse(read(path)) as Record<string, unknown>;
const { version } = json("package.json") as { version: string };
const readme = read("README.md");
const skill = read("examples/openclaw/brainchain-worker/SKILL.md");
const help = usage(undefined);
const flat = (text: string) => text.replace(/\s+/g, " ");

/** Every file of the repository but what is installed or built, and the tests, which name made-up releases. */
function files(dir = root): string[] {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    if ([".git", "node_modules", "dist"].includes(entry.name) || entry.name.endsWith(".test.ts")) return [];
    const path = join(dir, entry.name);
    return entry.isDirectory() ? files(path) : [relative(root, path).split(sep).join("/")];
  });
}

describe("the release each file names", () => {
  it("is this package's in the lockfile", () => {
    const lock = json("package-lock.json") as { version: string; packages: Record<string, { version: string }> };
    expect([lock.version, lock.packages[""]!.version]).toEqual([version, version]);
  });

  it("is this package's wherever a file pins brainchain-worker to a version", () => {
    const pins = files().flatMap((file) => [...read(file).matchAll(/brainchain-worker@(\d+\.\d+\.\d+[\w.-]*)/g)].map(([, pinned]) => ({ file, pinned })));
    expect(pins.filter(({ pinned }) => pinned !== version)).toEqual([]);
  });
});

describe("what --help and the README list", () => {
  const table = readme.split("\n## Commands\n")[1]!.split("\n## ")[0]!;
  const environment = readme.split("\n## Environment\n")[1]!.split("\n## ")[0]!;

  it("is the same commands", () => {
    const helped = [...help.matchAll(/^ {2}brainchain-worker (-*[a-z-]+)/gm)].map(([, command]) => command!);
    const listed = table.split("\n").flatMap((row) => /^\| `(-*[a-z-]+)/.exec(row)?.[1] ?? []);
    expect([...new Set(listed)].sort()).toEqual([...new Set(helped)].sort());
  });

  it("is the same settings", () => {
    const helped = help.split("\nEnvironment:\n")[1]!.split("\n\n")[0]!;
    const names = (text: string) => [...new Set(text.match(/\bBRAINCHAIN_[A-Z_]+/g) ?? [])].sort();
    expect(names(environment)).toEqual(names(helped));
  });
});

describe("mainnet's figures in the README", () => {
  it("are the stake and the bond the contracts ask for, on every line", () => {
    expect(readme).toContain("`join` stakes 250,000 BRAIN, the minimum, and applies with a 62,500 BRAIN bond, so a new worker needs 312,500 BRAIN");
    expect(readme).toContain("bridge --stake 312500 ");
    expect(readme).toContain("62,500 BRAIN on mainnet, 100 tBRAIN on testnet");
    expect(readme).not.toMatch(/1,?250,?000|1,000,000 BRAIN|250,000 BRAIN on mainnet/);
  });

  it("names the desk's fee with its floor, and a gas figure that is true", () => {
    expect(flat(readme)).toContain("less a 0.5% fee of at least 0.01 USDG");
    expect(readme).not.toContain("under a cent");
    expect(flat(help)).toContain("less a 0.5% fee, at least 0.01 tUSDG");
  });
});

describe("watch in the README and --help", () => {
  it("say how long an unreadable record holds the place, and what comes after", () => {
    expect(flat(readme)).toContain("A record still unreadable a day after its decision's block time is a finding, reported once, and the place moves on");
    expect(flat(help)).toContain("A record that cannot be read holds the place until a day after its decision's block time; past that it is a finding, reported once, and the place moves on");
  });
});

describe("bonds in the README and --help", () => {
  it("are placed after the hire, and read by Jev once settled, at later hires", () => {
    expect(readme).toContain("Jev reads a worker's settled bonds, delivered and missed, at later hires");
    expect(readme).toContain("After Jev hires this worker for the task");
    expect(readme).not.toMatch(/offered first|While the task is open|Not open yet|Jev reads the bond when it hires/);
    expect(flat(help)).toContain("behind a task Jev hired this worker for");
  });

  it("give the deadline the bond is created with", () => {
    const hours = BOND_LEAD_SEC / 3_600n;
    expect(flat(help)).toContain(`the bond's deadline, the task's plus ${hours} hours`);
    expect(readme).toContain(`The bond's deadline is the task's plus ${hours} hours`);
  });

  it("name who a missed bond pays in one sentence", () => {
    const missed = "the agent that paid BrainChain's desk for the task, or to the poster for a task posted on the board directly";
    expect(flat(readme)).toContain(missed);
    expect(flat(help)).toContain(missed);
  });
});

describe("exits in the README, --help and the skill", () => {
  it("promise no working exit on mainnet, and do not call it coming", () => {
    for (const text of [readme, help, skill]) {
      expect(flat(text)).toMatch(/Fast exits are off,? (?:and `exit` says so|on mainnet, where `?exit`? says so)/);
      expect(text).not.toMatch(/BRAINCHAIN_NETWORK=mainnet npx(?: -y)? brainchain-worker exit/);
      expect(text).not.toMatch(/coming soon|for now.*exit|exit.*for now/i);
    }
  });

  it("keep the 'stops before anything is signed' sentence to fund", () => {
    expect(flat(readme)).toContain("Each Relay move `fund` makes is priced before anything is signed");
    expect(flat(readme)).toContain("The desk would price that move after the transfer arrives");
    expect(readme).not.toContain("Every Relay move is priced before anything is signed");
  });
});

describe("fund in the README and --help", () => {
  it("say what happens to the rest without --stake, and that only what the run brought is bridged", () => {
    expect(flat(readme)).toContain("Without `--stake` it spends only that gas amount and the rest stays on Solana");
    expect(flat(help)).toContain("without it, the rest stays on Solana");
    expect(flat(readme)).toContain("What the wallet already held on Robinhood Chain stays there");
    expect(flat(help)).toContain("what the wallet already held stays");
  });

  it("use no example amount the price guard or the join would refuse", () => {
    expect(readme).toContain("fund --from-solana --usdc 120 --stake --dry");
    expect(readme).not.toContain("--usdc 20");
    expect(skill).not.toContain("--usdc 20");
  });
});
