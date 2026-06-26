import { mkdirSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

export type SearchEmbedder = {
  modelId: string;
  dimensions: number;
  embedTexts(texts: string[]): number[][];
};

export type LocalSearchEmbedderOptions = {
  modelId?: string;
  cacheDir?: string;
  dimensions?: number;
  timeoutMs?: number;
};

const defaultModelId = "Xenova/paraphrase-multilingual-MiniLM-L12-v2";
const defaultDimensions = 384;
const defaultTimeoutMs = 120_000;
const packageRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");

const workerSource = `
import { env, pipeline } from "@huggingface/transformers";
import { readFileSync } from "node:fs";

const payload = JSON.parse(readFileSync(0, "utf8"));
env.useFSCache = true;
env.allowLocalModels = true;
env.cacheDir = payload.cacheDir;

const extractor = await pipeline("feature-extraction", payload.modelId);
const embeddings = [];
for (const text of payload.texts) {
  const output = await extractor(text, { pooling: "mean", normalize: true });
  const vector = Array.from(output.data ?? output);
  embeddings.push(vector);
}

process.stdout.write(JSON.stringify({ embeddings }));
`;

function defaultCacheDir(): string {
  return resolve(
    process.env.CAIXU_EMBEDDING_CACHE_DIR ??
      join(homedir(), ".cache", "caixu", "embeddings")
  );
}

function normalizeVector(vector: unknown, dimensions: number): number[] {
  if (!Array.isArray(vector)) {
    throw new Error("Embedding worker returned a non-array vector.");
  }
  if (vector.length !== dimensions) {
    throw new Error(
      `Embedding worker returned ${vector.length} dimensions, expected ${dimensions}.`
    );
  }
  const values = vector.map((value) => Number(value));
  if (values.some((value) => !Number.isFinite(value))) {
    throw new Error("Embedding worker returned non-finite values.");
  }
  return values;
}

export function createLocalSearchEmbedder(
  options: LocalSearchEmbedderOptions = {}
): SearchEmbedder {
  const modelId = options.modelId ?? process.env.CAIXU_EMBEDDING_MODEL ?? defaultModelId;
  const dimensions = options.dimensions ?? defaultDimensions;
  const cacheDir = resolve(options.cacheDir ?? defaultCacheDir());
  const timeoutMs =
    options.timeoutMs ??
    (Number.parseInt(process.env.CAIXU_EMBEDDING_TIMEOUT_MS ?? "", 10) ||
      defaultTimeoutMs);

  mkdirSync(dirname(cacheDir), { recursive: true });
  mkdirSync(cacheDir, { recursive: true });

  return {
    modelId,
    dimensions,
    embedTexts(texts: string[]) {
      if (texts.length === 0) {
        return [];
      }

      const result = spawnSync(
        process.execPath,
        ["--input-type=module", "-e", workerSource],
        {
          cwd: packageRoot,
          input: JSON.stringify({ modelId, texts, cacheDir }),
          encoding: "utf8",
          timeout: timeoutMs,
          maxBuffer: 64 * 1024 * 1024
        }
      );

      if (result.error) {
        throw result.error;
      }
      if (result.status !== 0) {
        throw new Error(
          `Embedding worker failed with status ${result.status}: ${result.stderr || "unknown error"}`
        );
      }

      const stdout = result.stdout?.trim();
      if (!stdout) {
        throw new Error("Embedding worker returned empty stdout.");
      }

      const parsed = JSON.parse(stdout) as { embeddings?: unknown[] };
      if (!Array.isArray(parsed.embeddings)) {
        throw new Error("Embedding worker returned no embeddings array.");
      }

      return parsed.embeddings.map((vector) => normalizeVector(vector, dimensions));
    }
  };
}
