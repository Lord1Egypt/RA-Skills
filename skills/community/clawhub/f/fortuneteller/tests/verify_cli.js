const { execFileSync } = require("child_process");
const path = require("path");

const root = path.join(__dirname, "..");
const cli = path.join(root, "scripts", "zhouyi_cli.js");

function run(args) {
  return execFileSync("node", [cli, ...args], {
    cwd: root,
    encoding: "utf-8"
  });
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const cast = JSON.parse(run(["cast", "--question", "测试", "--method", "coin", "--seed", "demo", "--json"]));
assert(cast.primary && cast.primary.number >= 1 && cast.primary.number <= 64, "cast should resolve primary hexagram");
assert(cast.changed && cast.changed.number >= 1 && cast.changed.number <= 64, "cast should resolve changed hexagram");
assert(Array.isArray(cast.lines) && cast.lines.length === 6, "cast should return 6 lines");
assert(cast.decision && cast.decision.entries.length >= 1, "cast should return decision entries");

const lookup = JSON.parse(run(["lookup", "--name", "乾", "--json"]));
assert(lookup.number === 1, "lookup by name should return 乾卦");
assert(lookup.extras[0].label === "用九", "乾卦 should retain 用九");

const search = JSON.parse(run(["search", "--query", "十年乃字", "--json"]));
assert(search.some((item) => item.number === 3), "search should find 屯卦");

const catalog = JSON.parse(run(["catalog", "--grade", "S", "--json"]));
assert(catalog.length >= 3, "catalog S grade should include enabled core systems");

console.log("cli verification passed");
