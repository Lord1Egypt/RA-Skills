#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import sharp from "sharp";
import gifenc from "gifenc";
const { GIFEncoder, quantize, applyPalette } = gifenc;
import { generateSpritesheet, getPackageBasePath } from "gotchi-generator";

const FRAME_WIDTH = 100;
const FRAME_HEIGHT = 100;
const DEFAULT_CANVAS_SIZE = 250;
const DEFAULT_VERTICAL_SHIFT_PX = 3;
const DEFAULT_ART_SCALE_PERCENT = 125;
const ROW_FRAME_COUNTS = [6, 7, 3, 6, 4, 7];
const ROW_ALIASES = {
  idle: [0],
  default: [0],
  fly: [1],
  sprint: [1],
  throw: [2],
  wand: [2],
  attack: [3],
  hurt: [4],
  death: [5],
  all: [0, 1, 2, 3, 4, 5]
};

const BACKGROUND_COLORS = {
  common: "#806AFB",
  uncommon: "#20C9C0",
  rare: "#59BCFF",
  legendary: "#FFC36B",
  mythical: "#FF96FF",
  godlike: "#51FFA8"
};

const BACKGROUND_ALIASES = {
  common: "common",
  uncommon: "uncommon",
  rare: "rare",
  legendary: "legendary",
  mythical: "mythical",
  godlike: "godlike",
  'rarity-common': "common",
  'rarity-uncommon': "uncommon",
  'rarity-rare': "rare",
  'rarity-legendary': "legendary",
  'rarity-mythical': "mythical",
  'rarity-godlike': "godlike",
  transparent: "transparent",
  none: "transparent"
};

const COLLATERAL_ALIASES = {
  eth: "aWETH",
  weth: "aWETH",
  dai: "aDAI",
  usdc: "aUSDC",
  usdt: "aUSDT",
  aave: "aAAVE",
  link: "aLINK",
  tusd: "aTUSD",
  wbtc: "aWBTC",
  uni: "aUNI"
};

const EYE_SHAPE_ALIASES = {
  common: "common_1",
  common_1: "common_1",
  common_2: "common_2",
  common_3: "common_3",
  uncommon: "uncommon_high_1",
  uncommon_high: "uncommon_high_1",
  uncommon_low: "uncommon_low_1",
  rare: "rare_high_1",
  rare_high: "rare_high_1",
  rare_low: "rare_low_1",
  mythical: "mythic_high",
  mythical_high: "mythic_high",
  mythic_high: "mythic_high",
  mythical_low: "mythic_low_1",
  mythic_low: "mythic_low_1",
  mythic_low_1: "mythic_low_1",
  mythic_low_2: "mythic_low_2"
};

const EYE_COLOR_ALIASES = {
  common: "common",
  uncommon: "uncommon_high",
  uncommon_high: "uncommon_high",
  uncommon_low: "uncommon_low",
  rare: "rare_high",
  rare_high: "rare_high",
  rare_low: "rare_low",
  mythical: "mythical_high",
  mythical_high: "mythical_high",
  mythical_low: "mythical_low",
  mythic_high: "mythical_high",
  mythic_low: "mythical_low"
};

const WEARABLE_ALIASES = JSON.parse(
  fs.readFileSync(
    new URL("../references/sprite-name-aliases.json", import.meta.url),
    "utf8"
  )
);

function printHelp() {
  console.log(`Usage:
  node ./scripts/render-gotchi-sprite.mjs --input ./Requests.sample.json [--output-dir ./output/sample]

Or:
  node ./scripts/render-gotchi-sprite.mjs \
    --id 999001 \
    --collateral ETH \
    --eye-shape common \
    --eye-color common \
    --body "Witchy Cloak" \
    --background common \
    --gif-rows idle \
    --output-dir ./output/custom

Flags:
  --input <file>
  --output-dir <dir>
  --slug <name>
  --id <number>
  --name <string>
  --collateral <value>
  --base-body <value>
  --eye-shape <value>
  --eye-color <value>
  --body <wearable>
  --face <wearable>
  --eyes <wearable>
  --head <wearable>
  --hand-left <wearable>
  --hand-right <wearable>
  --hand <wearable>
  --pet <wearable>
  --background <common|uncommon|rare|legendary|mythical|godlike|transparent>
  --background-mode <same as --background>
  --gif-rows <idle|all|throw|attack|hurt|death|0,1,2>
  --gif-scale <number>
  --zoom <25|50|100>
  --gif-zoom <25|50|100>
  --frame-size <1-100>
  --gif-frame-size <1-100>
  --canvas-size <number>
  --gif-canvas-size <number>
  --fps <number>
  --no-gif
  --verbose
  --help`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

function requireString(value, fallback = "") {
  return typeof value === "string" ? value : fallback;
}

function slugify(value) {
  return requireString(value)
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "") || `sprite-${Date.now()}`;
}

function normalizeKey(value) {
  return requireString(value).trim().toLowerCase().replace(/[\s-]+/g, "_");
}

function normalizeLookupKey(value) {
  return requireString(value).trim().toLowerCase().replace(/[^a-z0-9]+/g, " ").replace(/\s+/g, " ").trim();
}

function normalizeCollateral(value) {
  const raw = requireString(value).trim();
  if (!raw) return "";
  return COLLATERAL_ALIASES[normalizeKey(raw)] || raw;
}

function normalizeEyeShape(value) {
  const raw = requireString(value).trim();
  if (!raw) return "";
  return EYE_SHAPE_ALIASES[normalizeKey(raw)] || raw;
}

function normalizeEyeColor(value) {
  const raw = requireString(value).trim();
  if (!raw) return "";
  return EYE_COLOR_ALIASES[normalizeKey(raw)] || raw;
}

function normalizeWearableName(value) {
  const raw = requireString(value).trim();
  if (!raw) return "";
  return WEARABLE_ALIASES[raw] || WEARABLE_ALIASES[normalizeLookupKey(raw)] || raw;
}

function defaultEyeColorForShape(shape) {
  const normalized = normalizeKey(shape);
  if (!normalized) return "";
  if (normalized.startsWith("common")) return "common";
  if (normalized.startsWith("uncommon_high")) return "uncommon_high";
  if (normalized.startsWith("uncommon_low")) return "uncommon_low";
  if (normalized.startsWith("rare_high")) return "rare_high";
  if (normalized.startsWith("rare_low")) return "rare_low";
  if (normalized.startsWith("mythic_high") || normalized.startsWith("mythical_high")) return "mythical_high";
  if (normalized.startsWith("mythic_low") || normalized.startsWith("mythical_low")) return "mythical_low";
  return "";
}

function resolveBackgroundMode(value) {
  const raw = requireString(value, "common").trim().toLowerCase();
  return BACKGROUND_ALIASES[raw] || "common";
}

function getBackgroundInfo(mode) {
  if (mode === "transparent") {
    return { mode, label: "Transparent", color_hex: null };
  }
  const tier = BACKGROUND_ALIASES[mode] || mode;
  return {
    mode: tier,
    label: tier.charAt(0).toUpperCase() + tier.slice(1),
    color_hex: BACKGROUND_COLORS[tier] || BACKGROUND_COLORS.common
  };
}

function parseGifRows(value) {
  const raw = requireString(value, "idle").trim().toLowerCase();
  if (ROW_ALIASES[raw]) return ROW_ALIASES[raw];
  const rows = raw
    .split(",")
    .map((part) => Number.parseInt(part.trim(), 10))
    .filter((row) => Number.isInteger(row) && row >= 0 && row < ROW_FRAME_COUNTS.length);
  return rows.length ? rows : [0];
}

function parseZoomPercent(value) {
  const raw = requireString(value, "100").trim().toLowerCase().replace(/%$/, "");
  const parsed = Number.parseInt(raw, 10);
  if (!Number.isFinite(parsed) || parsed <= 0) return 100;
  if (parsed <= 25) return 25;
  if (parsed <= 50) return 50;
  return 100;
}

function parseFrameSize(value) {
  const raw = requireString(value, "100").trim().toLowerCase();
  const parsed = Number.parseInt(raw, 10);
  if (!Number.isFinite(parsed)) return 100;
  return Math.max(1, Math.min(FRAME_WIDTH, parsed));
}

function parseCanvasSize(value) {
  const raw = requireString(value, String(DEFAULT_CANVAS_SIZE)).trim().toLowerCase();
  const parsed = Number.parseInt(raw, 10);
  if (!Number.isFinite(parsed)) return DEFAULT_CANVAS_SIZE;
  return Math.max(1, Math.min(2000, parsed));
}

function pushIfPresent(attributes, traitType, value) {
  const text = requireString(value).trim();
  if (!text) return;
  attributes.push({ trait_type: traitType, value: text });
}

function buildGotchiFromFlags(args) {
  const id = Number.parseInt(requireString(args.id, "999001"), 10);
  if (Number.isNaN(id)) {
    throw new Error(`Invalid --id value: ${args.id}`);
  }

  const collateral = normalizeCollateral(args.collateral);
  const baseBody = normalizeCollateral(args["base-body"] || collateral);
  const eyeShape = normalizeEyeShape(args["eye-shape"]);
  const eyeColor = normalizeEyeColor(args["eye-color"] || defaultEyeColorForShape(eyeShape));
  const attributes = [];

  pushIfPresent(attributes, "Base Body", baseBody);
  pushIfPresent(attributes, "Eye Shape", eyeShape);
  pushIfPresent(attributes, "Eye Color", eyeColor);
  pushIfPresent(attributes, "Wearable (Body)", normalizeWearableName(args.body));
  pushIfPresent(attributes, "Wearable (Face)", normalizeWearableName(args.face));
  pushIfPresent(attributes, "Wearable (Eyes)", normalizeWearableName(args.eyes));
  pushIfPresent(attributes, "Wearable (Head)", normalizeWearableName(args.head));
  pushIfPresent(attributes, "Wearable (Hands)", normalizeWearableName(args["hand-left"]));
  pushIfPresent(attributes, "Wearable (Hands)", normalizeWearableName(args["hand-right"] || args.hand));
  pushIfPresent(attributes, "Wearable (Pet)", normalizeWearableName(args.pet));

  if (attributes.length === 0) {
    throw new Error("No traits were provided. Use --input or pass slot flags.");
  }

  return {
    id,
    name: requireString(args.name, `sprite-gotchi-${id}`),
    collateral: collateral || undefined,
    attributes
  };
}

function normalizeGotchiPayload(gotchi) {
  const attributes = Array.isArray(gotchi.attributes)
    ? gotchi.attributes.map((attr) => ({
        trait_type: attr.trait_type,
        value:
          attr.trait_type === "Base Body"
            ? normalizeCollateral(attr.value)
            : attr.trait_type === "Eye Shape"
              ? normalizeEyeShape(attr.value)
              : attr.trait_type === "Eye Color"
                ? normalizeEyeColor(attr.value)
                : attr.trait_type.startsWith("Wearable")
                  ? normalizeWearableName(attr.value)
                  : attr.value
      }))
    : [];

  if (!attributes.some((attr) => attr.trait_type === "Eye Color")) {
    const eyeShape = attributes.find((attr) => attr.trait_type === "Eye Shape")?.value || "";
    const fallbackEyeColor = defaultEyeColorForShape(eyeShape);
    if (fallbackEyeColor) {
      attributes.push({ trait_type: "Eye Color", value: fallbackEyeColor });
    }
  }

  return {
    ...gotchi,
    collateral: normalizeCollateral(gotchi.collateral),
    attributes
  };
}

function loadGotchi(args) {
  if (args.help) {
    printHelp();
    process.exit(0);
  }

  if (args.input) {
    const inputPath = path.resolve(process.cwd(), requireString(args.input));
    return normalizeGotchiPayload(JSON.parse(fs.readFileSync(inputPath, "utf8")));
  }

  return buildGotchiFromFlags(args);
}

function buildBodyAnchorGotchi(gotchi) {
  const sourceAttributes = Array.isArray(gotchi.attributes) ? gotchi.attributes : [];
  const allowedTraits = new Set([
    "Base Body",
    "Eye Shape",
    "Eye Color",
    "Wearable (Body)",
    "Wearable (Face)",
    "Wearable (Eyes)",
    "Wearable (Head)"
  ]);

  const bodyAnchorAttributes = sourceAttributes.filter((attr) => allowedTraits.has(attr.trait_type));
  const baseBody =
    bodyAnchorAttributes.find((attr) => attr.trait_type === "Base Body")?.value ||
    gotchi.collateral ||
    "";

  return {
    ...gotchi,
    name: `${requireString(gotchi.name, "gotchi")}-body-anchor`,
    collateral: gotchi.collateral,
    attributes:
      bodyAnchorAttributes.length > 0
        ? bodyAnchorAttributes
        : baseBody
          ? [{ trait_type: "Base Body", value: baseBody }]
          : []
  };
}
async function buildBodyAnchorReferenceTile(gotchi, config, packageBasePath, outputDir, frameSize, verbose = false) {
  const anchorGotchi = buildBodyAnchorGotchi(gotchi);
  const anchorDir = fs.mkdtempSync(path.join(outputDir, '.anchor-'));

  try {
    const anchorResult = await generateSpritesheet(anchorGotchi, config, packageBasePath, anchorDir, verbose);
    const anchorPath = path.join(anchorDir, `${anchorGotchi.id}.png`);

    if (!anchorResult?.success || !fs.existsSync(anchorPath)) {
      return null;
    }

    await applyFrameCropToSheet(anchorPath, frameSize);

    return await sharp(anchorPath)
      .extract({ left: 0, top: 0, width: frameSize, height: frameSize })
      .png()
      .toBuffer();
  } catch {
    return null;
  } finally {
    fs.rmSync(anchorDir, { recursive: true, force: true });
  }
}

async function applyFrameCropToSheet(sheetPath, frameSize) {
  if (frameSize === FRAME_WIDTH) return;

  const source = sharp(sheetPath).ensureAlpha();
  const metadata = await source.metadata();
  const width = metadata.width || 0;
  const height = metadata.height || 0;
  const columns = Math.floor(width / FRAME_WIDTH);
  const rows = Math.floor(height / FRAME_HEIGHT);

  if (!columns || !rows) return;

  const offsetLeft = Math.floor((FRAME_WIDTH - frameSize) / 2);
  const offsetTop = Math.floor((FRAME_HEIGHT - frameSize) / 2);
  const composites = [];

  for (let row = 0; row < rows; row += 1) {
    for (let col = 0; col < columns; col += 1) {
      const tileBuffer = await source
        .clone()
        .extract({
          left: col * FRAME_WIDTH + offsetLeft,
          top: row * FRAME_HEIGHT + offsetTop,
          width: frameSize,
          height: frameSize
        })
        .png()
        .toBuffer();

      composites.push({
        input: tileBuffer,
        left: col * frameSize,
        top: row * frameSize
      });
    }
  }

  await sharp({
    create: {
      width: columns * frameSize,
      height: rows * frameSize,
      channels: 4,
      background: { r: 0, g: 0, b: 0, alpha: 0 }
    }
  })
    .composite(composites)
    .png()
    .toFile(sheetPath);
}

async function measureAlphaBounds(imageInput) {
  const { data, info } = await sharp(imageInput)
    .ensureAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });

  let minX = info.width;
  let minY = info.height;
  let maxX = -1;
  let maxY = -1;

  for (let y = 0; y < info.height; y += 1) {
    for (let x = 0; x < info.width; x += 1) {
      const i = (y * info.width + x) * 4;
      if (data[i + 3] > 0) {
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
      }
    }
  }

  if (maxX < 0 || maxY < 0) {
    return {
      minX: 0,
      maxX: info.width - 1,
      minY: 0,
      maxY: info.height - 1,
      width: info.width,
      height: info.height,
      centerX: (info.width - 1) / 2,
      centerY: (info.height - 1) / 2
    };
  }

  return {
    minX,
    maxX,
    minY,
    maxY,
    width: maxX - minX + 1,
    height: maxY - minY + 1,
    centerX: (minX + maxX) / 2,
    centerY: (minY + maxY) / 2
  };
}

async function applyCanvasLayoutToSheet(
  sheetPath,
  frameWidth = FRAME_WIDTH,
  frameHeight = FRAME_HEIGHT,
  canvasSize = DEFAULT_CANVAS_SIZE,
  zoomPercent = 100,
  verticalShiftPx = DEFAULT_VERTICAL_SHIFT_PX,
  referenceTileInput = null
) {
  if (canvasSize === frameWidth && zoomPercent === 100 && verticalShiftPx === 0) return;

  const source = sharp(sheetPath).ensureAlpha();
  const metadata = await source.metadata();
  const width = metadata.width || 0;
  const height = metadata.height || 0;
  const columns = Math.floor(width / frameWidth);
  const rows = Math.floor(height / frameHeight);

  if (!columns || !rows) return;

  const effectiveScale = (DEFAULT_ART_SCALE_PERCENT / 100) * (zoomPercent / 100);
  const scaledWidth = Math.max(1, Math.round(canvasSize * effectiveScale));
  const scaledHeight = Math.max(1, Math.round(canvasSize * effectiveScale));
  const composites = [];

  const referenceTile = referenceTileInput
    ? await sharp(referenceTileInput)
        .resize({ width: scaledWidth, height: scaledHeight, kernel: 'nearest' })
        .png()
        .toBuffer()
    : await source
        .clone()
        .extract({ left: 0, top: 0, width: frameWidth, height: frameHeight })
        .resize({ width: scaledWidth, height: scaledHeight, kernel: 'nearest' })
        .png()
        .toBuffer();

  const referenceBounds = await measureAlphaBounds(referenceTile);
  const baseLeft = Math.round(canvasSize / 2 - referenceBounds.centerX);
  const baseTop = Math.round(canvasSize / 2 - referenceBounds.centerY);

  const overscanWidth = canvasSize + scaledWidth * 2;
  const overscanHeight = canvasSize + scaledHeight * 2;
  const originLeft = Math.floor((overscanWidth - canvasSize) / 2);
  const originTop = Math.floor((overscanHeight - canvasSize) / 2);

  for (let row = 0; row < rows; row += 1) {
    for (let col = 0; col < columns; col += 1) {
      const resizedTile = await source
        .clone()
        .extract({
          left: col * frameWidth,
          top: row * frameHeight,
          width: frameWidth,
          height: frameHeight
        })
        .resize({
          width: scaledWidth,
          height: scaledHeight,
          kernel: 'nearest'
        })
        .png()
        .toBuffer();

      const overscanTile = await sharp({
        create: {
          width: overscanWidth,
          height: overscanHeight,
          channels: 4,
          background: { r: 0, g: 0, b: 0, alpha: 0 }
        }
      })
        .composite([
          {
            input: resizedTile,
            left: originLeft + baseLeft,
            top: originTop + baseTop - verticalShiftPx
          }
        ])
        .png()
        .toBuffer();

      const expandedTile = await sharp(overscanTile)
        .extract({ left: originLeft, top: originTop, width: canvasSize, height: canvasSize })
        .png()
        .toBuffer();

      composites.push({
        input: expandedTile,
        left: col * canvasSize,
        top: row * canvasSize
      });
    }
  }

  await sharp({
    create: {
      width: columns * canvasSize,
      height: rows * canvasSize,
      channels: 4,
      background: { r: 0, g: 0, b: 0, alpha: 0 }
    }
  })
    .composite(composites)
    .png()
    .toFile(sheetPath);
}
async function applyBackgroundToSheet(rawPath, finalPath, backgroundInfo) {
  if (backgroundInfo.mode === "transparent") {
    if (rawPath !== finalPath) {
      fs.copyFileSync(rawPath, finalPath);
    }
    return;
  }

  await sharp(rawPath)
    .flatten({ background: backgroundInfo.color_hex })
    .png()
    .toFile(finalPath);
}

async function buildAnimatedGif(spriteSheetPath, gifPath, rows, fps, scale = 3, frameWidth = FRAME_WIDTH, frameHeight = FRAME_HEIGHT) {
  const source = sharp(spriteSheetPath).ensureAlpha();
  const metadata = await source.metadata();
  const maxRows = Math.floor((metadata.height || 0) / frameHeight);
  const validRows = rows.filter((row) => row >= 0 && row < maxRows);
  const gifWidth = frameWidth * scale;
  const gifHeight = frameHeight * scale;
  const delay = Math.max(1, Math.round(1000 / fps));
  const gif = GIFEncoder();
  let wroteFrame = false;

  for (const row of validRows) {
    const frameCount = ROW_FRAME_COUNTS[row] || Math.max(1, Math.floor((metadata.width || FRAME_WIDTH) / FRAME_WIDTH));
    for (let col = 0; col < frameCount; col += 1) {
      const frame = source.clone().extract({
        left: col * frameWidth,
        top: row * frameHeight,
        width: frameWidth,
        height: frameHeight
      });
      const resized = scale > 1
        ? frame.resize({ width: gifWidth, height: gifHeight, kernel: 'nearest' })
        : frame;
      const { data, info } = await resized
        .ensureAlpha()
        .raw()
        .toBuffer({ resolveWithObject: true });

      if (info.channels !== 4) {
        throw new Error(`Expected 4 channels for GIF frame, got ${info.channels}`);
      }

      const rgba = new Uint8Array(data.buffer, data.byteOffset, data.byteLength);
      const palette = quantize(rgba, 256, {
        format: 'rgba4444',
        oneBitAlpha: true,
        clearAlpha: false
      });
      const index = applyPalette(rgba, palette, 'rgba4444');
      const transparentIndex = palette.findIndex((entry) => entry[3] === 0);

      gif.writeFrame(index, gifWidth, gifHeight, {
        palette,
        delay,
        repeat: 0,
        transparent: transparentIndex >= 0,
        transparentIndex: transparentIndex >= 0 ? transparentIndex : 0
      });
      wroteFrame = true;
    }
  }

  if (!wroteFrame) {
    throw new Error('No frames available to build GIF');
  }

  gif.finish();
  fs.writeFileSync(gifPath, Buffer.from(gif.bytes()));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const gotchi = loadGotchi(args);
  const slug = slugify(args.slug || gotchi.name || String(gotchi.id));
  const outputDir = path.resolve(
    process.cwd(),
    requireString(args["output-dir"], `./output/${slug}`)
  );
  const verbose = Boolean(args.verbose);
  const backgroundMode = resolveBackgroundMode(args.background || args["background-mode"] || 'common');
  const background = getBackgroundInfo(backgroundMode);
  const gifRows = parseGifRows(args['gif-rows']);
  const fps = Math.max(1, Number.parseInt(requireString(args.fps, '12'), 10) || 12);
  const gifScale = Math.max(1, Number.parseInt(requireString(args['gif-scale'], '1'), 10) || 1);
  const zoom = parseZoomPercent(args.zoom || args['gif-zoom'] || '100');
  const frameSize = parseFrameSize(args['frame-size'] || args['gif-frame-size'] || '100');
  const canvasSize = parseCanvasSize(args['canvas-size'] || args['gif-canvas-size'] || String(DEFAULT_CANVAS_SIZE));
  const makeGif = !Boolean(args['no-gif']);

  fs.mkdirSync(outputDir, { recursive: true });

  const packageBasePath = getPackageBasePath();
  const configPath = path.join(packageBasePath, "config.json");
  const config = JSON.parse(fs.readFileSync(configPath, "utf8"));

  const generatedPath = path.join(outputDir, `${gotchi.id}.png`);
  const rawSpritePath = path.join(outputDir, `${gotchi.id}.raw.png`);
  const finalSpritePath = path.join(outputDir, `${gotchi.id}.png`);
  const gifPath = path.join(outputDir, `${gotchi.id}.gif`);

  const referenceTile = await buildBodyAnchorReferenceTile(
    gotchi,
    config,
    packageBasePath,
    outputDir,
    frameSize,
    verbose
  );

  const result = await generateSpritesheet(
    gotchi,
    config,
    packageBasePath,
    outputDir,
    verbose
  );

  if (fs.existsSync(generatedPath)) {
    if (generatedPath !== rawSpritePath) {
      fs.renameSync(generatedPath, rawSpritePath);
    }
    await applyFrameCropToSheet(rawSpritePath, frameSize);
    await applyCanvasLayoutToSheet(rawSpritePath, frameSize, frameSize, canvasSize, zoom, DEFAULT_VERTICAL_SHIFT_PX, referenceTile);
    await applyBackgroundToSheet(rawSpritePath, finalSpritePath, background);
    if (makeGif) {
      await buildAnimatedGif(finalSpritePath, gifPath, gifRows, fps, gifScale, canvasSize, canvasSize);
    }
  }

  const manifestPath = path.join(outputDir, `${gotchi.id}.manifest.json`);
  const manifest = {
    slug,
    request: {
      ...gotchi,
      background_mode: background.mode,
      gif_rows: gifRows,
      gif_scale: gifScale,
      frame_size: frameSize,
      canvas_size: canvasSize,
      vertical_shift_px: DEFAULT_VERTICAL_SHIFT_PX,
      zoom,
      fps
    },
    background,
    output: {
      sprite_png: finalSpritePath,
      sprite_raw_png: rawSpritePath,
      sprite_gif: makeGif ? gifPath : null,
      png_exists: fs.existsSync(finalSpritePath),
      gif_exists: makeGif ? fs.existsSync(gifPath) : false
    },
    result
  };

  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));

  if (!result.success) {
    console.error(JSON.stringify(manifest, null, 2));
    process.exit(1);
  }

  console.log(
    JSON.stringify(
      {
        success: true,
        sprite_png: finalSpritePath,
        sprite_gif: makeGif ? gifPath : null,
        manifest_json: manifestPath,
        background,
        details: result.details || {}
      },
      null,
      2
    )
  );
}

main().catch((error) => {
  console.error(
    JSON.stringify(
      {
        success: false,
        error: error instanceof Error ? error.message : String(error)
      },
      null,
      2
    )
  );
  process.exit(1);
});
