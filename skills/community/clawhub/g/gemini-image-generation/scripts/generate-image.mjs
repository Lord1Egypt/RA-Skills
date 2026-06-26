import {
  createGeminiImageClientFromEnv,
  createImageGenerationRequest,
  formatImageSummary,
  parseArgs,
  readImageConfigArgs,
  requireSingleArg,
  saveImageResponse,
} from "./gemini-image-runtime.mjs";

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const prompt = requireSingleArg(args.prompt, "prompt");
  const output = requireSingleArg(args.output, "output");
  const imageConfig = readImageConfigArgs(args);
  const { ai, model } = createGeminiImageClientFromEnv();
  const response = await ai.models.generateContent(
    createImageGenerationRequest({
      model,
      prompt,
      imageConfig,
    }),
  );
  const { outputLines, savedImages } = await saveImageResponse(response, output);

  for (const line of outputLines) {
    console.log(line);
  }

  console.log(formatImageSummary(savedImages, imageConfig));
}

main().catch((error) => {
  console.error(`ERROR: ${error.message}`);
  process.exitCode = 1;
});
