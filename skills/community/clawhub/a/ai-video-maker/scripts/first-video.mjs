import { validateCreatePayload } from "./contract.mjs";

export const firstVideoScenarios = [
  {
    id: "product",
    title: "Turn a product image into a short showcase",
    input: "Product image and what to highlight",
  },
  {
    id: "social",
    title: "Create a short social media clip",
    input: "Topic or a one-sentence idea",
  },
  { id: "custom", title: "Use my own idea", input: "Prompt and any image or references" },
];

export function validateFirstVideoFlow(flowId) {
  if (
    !/^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(flowId || "")
  ) {
    throw new Error("Use the firstVideo.flowId returned by connect.mjs.");
  }
  return flowId;
}

export function firstVideoPayload(scenario, payload) {
  if (!firstVideoScenarios.some((item) => item.id === scenario))
    throw new Error("Choose product, social, or custom.");
  if (!payload || typeof payload !== "object" || Array.isArray(payload))
    throw new Error("Provide a JSON payload with your video idea.");
  if (Object.hasOwn(payload, "image"))
    throw new Error("MiniMax uses imageUrl, not image. Supply the product image as imageUrl.");
  if (scenario === "product" && !payload.imageUrl) {
    throw new Error("A product image is required. Ask for an image before quoting.");
  }
  const value = {
    duration: 5,
    resolution: "720p",
    tier: "turbo",
    aspectRatio: scenario === "social" ? "9:16" : "16:9",
    ...payload,
  };
  const validation = validateCreatePayload("minimax", value);
  if (!validation.ok) throw new Error(validation.errorMessage);
  return value;
}
