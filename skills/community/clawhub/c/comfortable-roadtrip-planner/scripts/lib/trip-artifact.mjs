import fs from "node:fs";
import path from "node:path";

export function readText(filePath) {
  return fs.readFileSync(filePath, "utf8");
}

export function extractInlineScripts(html) {
  return [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)]
    .map(match => match[1])
    .filter(script => script.trim());
}

export function assertInlineScriptsParse(html, filePath = "artifact") {
  const scripts = extractInlineScripts(html);
  for (const script of scripts) {
    try {
      new Function(script);
    } catch (error) {
      throw new Error(`${filePath}: inline script failed to parse: ${error.message}`);
    }
  }
  return scripts.length;
}

export function extractTripData(html, filePath = "artifact") {
  const scripts = extractInlineScripts(html);
  const script = scripts.find(value => value.includes("const tripMeta") && value.includes("const tripDays"));
  if (!script) {
    throw new Error(`${filePath}: could not find const tripMeta and const tripDays`);
  }

  const tripMeta = evaluateConstLiteral(script, "tripMeta", filePath);
  const tripDays = evaluateConstLiteral(script, "tripDays", filePath);
  return { tripMeta, tripDays };
}

export function loadTripArtifact(filePath) {
  const html = readText(filePath);
  assertInlineScriptsParse(html, filePath);
  const { tripMeta, tripDays } = extractTripData(html, filePath);
  return {
    filePath,
    html,
    tripMeta,
    tripDays
  };
}

export function evaluateConstLiteral(script, constName, filePath = "artifact") {
  const marker = `const ${constName}`;
  const start = script.indexOf(marker);
  if (start === -1) {
    throw new Error(`${filePath}: missing ${marker}`);
  }

  const equals = script.indexOf("=", start + marker.length);
  if (equals === -1) {
    throw new Error(`${filePath}: missing initializer for ${constName}`);
  }

  const literalStart = findFirstNonWhitespace(script, equals + 1);
  const literalEnd = findLiteralEnd(script, literalStart);
  const literal = script.slice(literalStart, literalEnd);
  try {
    return Function(`"use strict"; return (${literal});`)();
  } catch (error) {
    throw new Error(`${filePath}: failed to evaluate ${constName}: ${error.message}`);
  }
}

function findFirstNonWhitespace(value, index) {
  while (index < value.length && /\s/.test(value[index])) index += 1;
  return index;
}

function findLiteralEnd(value, start) {
  const opener = value[start];
  const closer = opener === "{" ? "}" : opener === "[" ? "]" : null;
  if (!closer) {
    throw new Error(`expected object or array literal, found ${opener}`);
  }

  let depth = 0;
  let quote = "";
  let escaped = false;
  let templateExpressionDepth = 0;

  for (let index = start; index < value.length; index += 1) {
    const char = value[index];
    const prev = value[index - 1];

    if (quote) {
      if (escaped) {
        escaped = false;
        continue;
      }
      if (char === "\\") {
        escaped = true;
        continue;
      }
      if (quote === "`" && char === "$" && value[index + 1] === "{") {
        templateExpressionDepth += 1;
        index += 1;
        continue;
      }
      if (quote === "`" && templateExpressionDepth > 0) {
        if (char === "{") templateExpressionDepth += 1;
        if (char === "}") templateExpressionDepth -= 1;
        continue;
      }
      if (char === quote) quote = "";
      continue;
    }

    if (char === "'" || char === '"' || char === "`") {
      quote = char;
      continue;
    }

    if (char === "/" && value[index + 1] === "/") {
      index = value.indexOf("\n", index + 2);
      if (index === -1) return value.length;
      continue;
    }

    if (char === "/" && value[index + 1] === "*") {
      const end = value.indexOf("*/", index + 2);
      if (end === -1) throw new Error("unterminated block comment");
      index = end + 1;
      continue;
    }

    if (char === opener || (opener === "[" && char === "{") || (opener === "{" && char === "[")) {
      depth += 1;
      continue;
    }

    if (char === closer || (closer === "]" && char === "}") || (closer === "}" && char === "]")) {
      depth -= 1;
      if (depth === 0) {
        return index + 1;
      }
      continue;
    }

    if (char === ";" && depth === 0 && prev !== "\\") return index;
  }

  throw new Error("unterminated literal");
}

export function normalizeWeather(weather) {
  if (Array.isArray(weather)) return weather.filter(Boolean).map(String);
  if (!weather) return [];
  if (Array.isArray(weather.summary)) return weather.summary.filter(Boolean).map(String);
  if (weather.summary) return [String(weather.summary)];
  return [];
}

export function normalizeImages(stop) {
  const rawImages = Array.isArray(stop?.images) && stop.images.length
    ? stop.images
    : stop?.image
      ? [{ src: stop.image, alt: stop.imageAlt, title: stop.imageTitle, caption: stop.imageCaption, credit: stop.imageCredit, link: stop.imageLink }]
      : [];
  return rawImages
    .map(image => typeof image === "string" ? { src: image } : image)
    .filter(image => image && (image.src || image.url));
}

export function repoRelative(filePath, cwd = process.cwd()) {
  return path.relative(cwd, filePath).replaceAll(path.sep, "/");
}

export function flattenArtifactText({ html, tripMeta, tripDays }) {
  return [
    html,
    JSON.stringify(tripMeta),
    JSON.stringify(tripDays)
  ].join("\n").toLowerCase();
}
