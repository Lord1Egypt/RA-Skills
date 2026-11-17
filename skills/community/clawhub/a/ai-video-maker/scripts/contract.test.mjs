import assert from "node:assert/strict";
import { ALLOWED_MODELS, validateCreatePayload } from "./contract.mjs";

const validPayloads = {
  t2v: { prompt: "A sunrise", aspectRatio: "16:9", duration: "5" },
  i2v: { image: "https://example.com/frame.jpg", duration: "8" },
  minimax: { content: "A sunrise" },
  t2v_v3: { prompt: "A sunrise", aspectRatio: "9:16", duration: "10" },
  i2v_v3: {
    image: "data:image/png;base64,AAAA",
    prompt: null,
    duration: "15",
  },
  seedance20: {
    prompt: "A sunrise",
    duration: 5,
    resolution: 720,
    ratio: "16:9",
  },
  wan30: {
    prompt: "A sunrise",
    duration: "5",
    resolution: "480P",
    ratio: "1:1",
  },
  happyhorse: {
    prompt: "A horse running",
    image: ["https://example.com/horse.jpg"],
    duration: 5,
    resolution: "1080P",
  },
};

assert.deepEqual(Object.keys(validPayloads), ALLOWED_MODELS);

for (const [model, payload] of Object.entries(validPayloads)) {
  assert.equal(validateCreatePayload(model, payload).ok, true, `${model} should be valid`);
}

const invalidPayloads = [
  ["t2v", { prompt: "", aspectRatio: "16:9", duration: "5" }],
  ["i2v", { image: "file:///tmp/frame.jpg", duration: "5" }],
  [
    "minimax",
    {
      content: "test",
      imageUrl: "https://example.com/a.jpg",
      referenceVideoUrl: "https://example.com/a.mp4",
    },
  ],
  ["t2v_v3", { prompt: "test", aspectRatio: "4:3", duration: "10" }],
  ["i2v_v3", { image: "https://example.com/a.jpg", duration: "8" }],
  [
    "seedance20",
    { audio: "https://example.com/a.mp3", duration: 5, resolution: 720, ratio: "16:9" },
  ],
  ["wan30", { prompt: "test", duration: 5, resolution: "720p", ratio: "16:9" }],
  ["happyhorse", { prompt: "test", image: [], duration: 5, resolution: "720P" }],
];

for (const [model, payload] of invalidPayloads) {
  assert.equal(validateCreatePayload(model, payload).ok, false, `${model} should be rejected`);
}

console.log(`Validated ${ALLOWED_MODELS.length} supported model contracts.`);
