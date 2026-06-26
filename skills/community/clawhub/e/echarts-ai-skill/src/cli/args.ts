import { access, mkdir, readFile, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";

export function getArg(flag: string): string | undefined {
  const index = process.argv.indexOf(flag);
  if (index === -1) {
    return undefined;
  }
  return process.argv[index + 1];
}

function resolveHomePath(inputPath: string): string {
  if (inputPath === "~") {
    return os.homedir();
  }
  if (inputPath.startsWith("~/") || inputPath.startsWith("~\\")) {
    return path.join(os.homedir(), inputPath.slice(2));
  }
  return inputPath;
}

function resolveNamedDirectory(rawPath: string): string {
  const normalized = rawPath.trim().toLowerCase();
  if (normalized === "desktop") {
    return path.join(os.homedir(), "Desktop");
  }
  if (normalized === "home" || normalized === "~") {
    return os.homedir();
  }
  return rawPath;
}

function resolvePath(rawPath: string): string {
  const expanded = resolveHomePath(resolveNamedDirectory(rawPath));
  return path.isAbsolute(expanded) ? expanded : path.resolve(expanded);
}

async function pathExists(targetPath: string): Promise<boolean> {
  try {
    await access(targetPath);
    return true;
  } catch {
    return false;
  }
}

async function defaultOutputDirectory(): Promise<string> {
  const currentDirectory = process.cwd();
  if (await pathExists(currentDirectory)) {
    return currentDirectory;
  }
  return path.resolve(".");
}

export async function readJsonInput<T>(): Promise<T> {
  const inputPath = getArg("--input");
  if (!inputPath) {
    throw new Error("Missing --input <file>.");
  }
  const content = await readFile(resolvePath(inputPath), "utf8");
  return JSON.parse(content) as T;
}

export async function resolveOutputPath(defaultFileName?: string): Promise<string | undefined> {
  const outputPath = getArg("--out");
  if (outputPath) {
    return resolvePath(outputPath);
  }

  const outputDir = getArg("--out-dir");
  if (outputDir && defaultFileName) {
    return path.join(resolvePath(outputDir), defaultFileName);
  }

  if (!defaultFileName) {
    return undefined;
  }

  return path.join(await defaultOutputDirectory(), defaultFileName);
}

export async function writeTextOutput(content: string, defaultFileName?: string): Promise<string | undefined> {
  const outputPath = await resolveOutputPath(defaultFileName);
  if (!outputPath) {
    process.stdout.write(content);
    return undefined;
  }
  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, content, "utf8");
  return outputPath;
}

export function getNumberArg(flag: string, fallback: number): number {
  const raw = getArg(flag);
  if (!raw) {
    return fallback;
  }
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : fallback;
}
