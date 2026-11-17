#!/usr/bin/env node
import fs from "node:fs";
import { flattenArtifactText, loadTripArtifact, normalizeImages } from "./lib/trip-artifact.mjs";

const artifactPath = process.argv[2];
if (!artifactPath) {
  console.error("Usage: node scripts/run-output-eval.mjs <artifact.html>");
  process.exit(2);
}

const evalPath = process.argv[3] || "evals/output_eval.json";
const evalSpec = JSON.parse(fs.readFileSync(evalPath, "utf8"));
const artifact = loadTripArtifact(artifactPath);
const checks = buildChecks(artifact);
const failures = [];

for (const criterion of evalSpec.criteria || []) {
  const passed = checks[criterion.id]?.() ?? false;
  if (!passed && criterion.required) {
    failures.push(`${criterion.id}: ${criterion.description}`);
  }
}

if (failures.length) {
  for (const failure of failures) console.error(`FAIL ${failure}`);
  console.error(`FAILED output eval: ${failures.length} failure(s)`);
  process.exit(1);
}

console.log(`PASS output eval: ${(evalSpec.criteria || []).length} criterion/criteria`);

function buildChecks(currentArtifact) {
  const { tripDays } = currentArtifact;
  const text = flattenArtifactText(currentArtifact);

  return {
    "one-main-objective": () => tripDays.every(day => hasText(day.mainObjective) || hasText(day.strategy)),
    "cut-rules": () => tripDays.every(day => Array.isArray(day.cutRules) && day.cutRules.length >= 2),
    "meal-rest": () => tripDays.every(day => Array.isArray(day.meals) && day.meals.length >= 1),
    "avoid-night-driving": () => /(night driving|夜路|before dark|daylight|18:30|6:30|late driving|avoid recreating it if it means late driving)/i.test(text),
    "low-stamina": () => /(low[-\s]*stamina|limited stamina|孕|体力|short walk|low-walk|seating|bathroom|restroom|easy)/i.test(text),
    "camera-spot-honesty": () => {
      const imageText = tripDays
        .flatMap(day => day.stops || [])
        .flatMap(stop => normalizeImages(stop))
        .map(image => [image.title, image.caption, image.credit].filter(Boolean).join(" "))
        .join(" ")
        .toLowerCase();
      return /(optional|skip|avoid|low[-\s]*walk|easy|late driving|parking|body battery|comfort)/i.test(imageText);
    },
    "source-provenance": () => tripDays.every(day => {
      const sources = Array.isArray(day.sourceProvenance) ? day.sourceProvenance : [];
      const types = new Set(sources.map(source => source.type));
      return ["weather", "road", "ticket", "restaurant", "image"].every(type => types.has(type));
    })
  };
}

function hasText(value) {
  return typeof value === "string" && value.trim().length > 0;
}
