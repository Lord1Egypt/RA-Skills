const fs = require("fs");

function readJsonInput({ argv = process.argv, stdin = process.stdin } = {}) {
  const inputFileFlag = argv.indexOf("--input-file");
  if (inputFileFlag !== -1) {
    const inputFile = argv[inputFileFlag + 1];
    if (!inputFile) {
      throw new Error("Usage: --input-file <path>");
    }
    return JSON.parse(fs.readFileSync(inputFile, "utf8"));
  }

  return (async () => {
    let input = "";
    for await (const chunk of stdin) input += chunk;
    return JSON.parse(input);
  })();
}

function writeJsonOutput(value, { argv = process.argv, stdout = process.stdout } = {}) {
  const outputFileFlag = argv.indexOf("--output-file");
  if (outputFileFlag !== -1) {
    const outputFile = argv[outputFileFlag + 1];
    if (!outputFile) {
      throw new Error("Usage: --output-file <path>");
    }
    fs.mkdirSync(require("path").dirname(outputFile), { recursive: true });
    fs.writeFileSync(outputFile, JSON.stringify(value));
    return;
  }

  stdout.write(JSON.stringify(value));
}

module.exports = {
  readJsonInput,
  writeJsonOutput,
};
