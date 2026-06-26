/** Image generation model names */
export const ImageModel = {
  /** Nano Banana 2 — default, fast */
  NARWHAL: 'NARWHAL',
  /** Nano Banana Pro */
  NANO_BANANA_PRO: 'NANO_BANANA_PRO',
} as const;

/** All model IDs to user-friendly names */
export const ModelDisplayName: Record<string, string> = {
  NARWHAL: 'Nano Banana 2',
  NANO_BANANA_PRO: 'Nano Banana Pro',
};

/** Image aspect ratios */
export const ImageAspectRatio = {
  LANDSCAPE: 'IMAGE_ASPECT_RATIO_LANDSCAPE',      // 16:9
  PORTRAIT: 'IMAGE_ASPECT_RATIO_PORTRAIT',         // 9:16
} as const;

/** Map user-friendly aspect ratio to API value */
export function resolveImageAspectRatio(input: string): string {
  const k = input.trim().toLowerCase();
  if (k === '16:9' || k === 'landscape') return ImageAspectRatio.LANDSCAPE;
  if (k === '9:16' || k === 'portrait') return ImageAspectRatio.PORTRAIT;
  // Pass through if already an API value
  if (k.startsWith('IMAGE_ASPECT_RATIO_')) return input;
  return ImageAspectRatio.LANDSCAPE;
}

/** Resolve user-friendly model name to API model ID */
export function resolveImageModel(input: string): string {
  const k = input.trim().toLowerCase();
  if (k === 'narwhal' || k === 'nano-banana' || k === 'nano_banana' || k === 'nano-banana-2') return ImageModel.NARWHAL;
  if (k === 'nano_banana_pro' || k === 'nano-banana-pro') return ImageModel.NANO_BANANA_PRO;
  // Fallback: use as-is (may be a new model)
  return input.toUpperCase();
}
