const { runSkill } = require("../_easybuy_browser_runtime");

async function run(inputText) {
  return runSkill("message_monitor", inputText || "");
}

if (require.main === module) {
  const input = process.argv.slice(2).join(" ");
  run(input)
    .then((out) => process.stdout.write(String(out)))
    .catch((err) => {
      process.stderr.write(err && err.message ? err.message : String(err));
      process.exit(1);
    });
}

module.exports = { run };
