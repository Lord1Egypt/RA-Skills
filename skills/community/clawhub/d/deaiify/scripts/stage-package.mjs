import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const repoDir = path.resolve(new URL("..", import.meta.url).pathname);
const outDir = process.argv[2]
  ? path.resolve(process.cwd(), process.argv[2])
  : path.join(repoDir, ".release", "package");

const filesToCopy = [
  "dist/constants.js",
  "dist/index.js",
  "dist/utils.js",
  "openclaw.json",
  "openclaw.plugin.json",
  "README.md",
];

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true });
}

async function copyFile(relPath) {
  const src = path.join(repoDir, relPath);
  const dest = path.join(outDir, relPath);
  await ensureDir(path.dirname(dest));
  await fs.copyFile(src, dest);
}

async function main() {
  await fs.rm(outDir, { recursive: true, force: true });
  await ensureDir(outDir);

  const packageJson = JSON.parse(
    await fs.readFile(path.join(repoDir, "package.json"), "utf8")
  );

  const publishPackageJson = {
    name: packageJson.name,
    version: packageJson.version,
    description: packageJson.description,
    main: packageJson.main,
    type: packageJson.type,
    peerDependencies: packageJson.peerDependencies,
    openclaw: packageJson.openclaw,
  };

  await Promise.all(filesToCopy.map(copyFile));
  await fs.writeFile(
    path.join(outDir, "package.json"),
    `${JSON.stringify(publishPackageJson, null, 2)}\n`,
    "utf8"
  );

  console.log(
    JSON.stringify(
      {
        outDir,
        files: [...filesToCopy, "package.json"],
      },
      null,
      2
    )
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
