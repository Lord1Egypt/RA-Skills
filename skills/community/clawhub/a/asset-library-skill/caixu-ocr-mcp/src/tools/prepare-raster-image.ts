import { execFile } from "node:child_process";
import { mkdtemp, readFile, rm, stat } from "node:fs/promises";
import { tmpdir } from "node:os";
import { basename, join } from "node:path";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

export type RasterPreprocessConfig = {
  enabled: boolean;
  thresholdBytes: number;
  maxWidth: number;
};

export type PreparedRasterImage = {
  buffer: Buffer;
  mimeType: "image/png" | "image/jpeg";
  prepared: boolean;
};

function isRasterMimeType(mimeType: string): mimeType is "image/png" | "image/jpeg" {
  return mimeType === "image/png" || mimeType === "image/jpeg";
}

export function shouldPreprocessRasterImage(input: {
  mimeType: string;
  sizeBytes: number;
  config: RasterPreprocessConfig;
}): boolean {
  if (!input.config.enabled) {
    return false;
  }

  if (!isRasterMimeType(input.mimeType)) {
    return false;
  }

  return input.sizeBytes > input.config.thresholdBytes;
}

export async function prepareRasterImageForVision(input: {
  filePath: string;
  mimeType: string;
  config: RasterPreprocessConfig;
}): Promise<PreparedRasterImage> {
  if (!isRasterMimeType(input.mimeType)) {
    return {
      buffer: await readFile(input.filePath),
      mimeType: input.mimeType as "image/png" | "image/jpeg",
      prepared: false
    };
  }

  const fileStat = await stat(input.filePath);
  if (
    !shouldPreprocessRasterImage({
      mimeType: input.mimeType,
      sizeBytes: fileStat.size,
      config: input.config
    })
  ) {
    return {
      buffer: await readFile(input.filePath),
      mimeType: input.mimeType,
      prepared: false
    };
  }

  const workDir = await mkdtemp(join(tmpdir(), "caixu-raster-prep-"));
  const outputPath = join(workDir, `${basename(input.filePath)}.jpg`);

  try {
    await execFileAsync(
      "ffmpeg",
      [
        "-y",
        "-i",
        input.filePath,
        "-vf",
        `scale=${input.config.maxWidth}:-2:force_original_aspect_ratio=decrease`,
        "-q:v",
        "3",
        outputPath
      ],
      {
        timeout: 60_000,
        maxBuffer: 16 * 1024 * 1024
      }
    );

    return {
      buffer: await readFile(outputPath),
      mimeType: "image/jpeg",
      prepared: true
    };
  } catch {
    return {
      buffer: await readFile(input.filePath),
      mimeType: input.mimeType,
      prepared: false
    };
  } finally {
    await rm(workDir, { recursive: true, force: true });
  }
}
