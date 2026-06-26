/**
 * tile-compare.cjs
 *
 * Splits reference and screenshot PNGs into horizontal 300px tiles,
 * runs pixelmatch on each, and returns per-tile mismatch data.
 *
 * Tiles with diffPercent > 0 are candidates for targeted OpenCV analysis.
 * topMismatchTiles gives the agent a ranked list of which vertical zones
 * to focus fixes on.
 */

'use strict';

const fs = require('fs');

function loadModule(name) {
  try {
    return require(name);
  } catch {
    throw new Error(`Missing dependency: ${name}\nInstall with: npm install ${name}`);
  }
}

/**
 * Extract a horizontal slice from a PNG buffer.
 * @param {Buffer} data   - raw RGBA buffer from pngjs
 * @param {number} srcW   - full image width (stride)
 * @param {number} y      - top of slice
 * @param {number} width  - slice width (≤ srcW)
 * @param {number} height - slice height
 * @returns {Buffer}
 */
function extractSlice(data, srcW, y, width, height) {
  const buf = Buffer.alloc(width * height * 4);
  for (let row = 0; row < height; row++) {
    const src = ((y + row) * srcW) * 4;
    const dst = row * width * 4;
    data.copy(buf, dst, src, src + width * 4);
  }
  return buf;
}

/**
 * Compare two PNGs tile by tile.
 *
 * @param {string} refPath        - path to reference PNG
 * @param {string} scrPath        - path to screenshot PNG
 * @param {object} [options]
 * @param {number} [options.tileHeight=300] - tile height in px
 * @param {number} [options.threshold=0.1]  - pixelmatch threshold
 * @returns {{
 *   ok: boolean,
 *   width: number,
 *   height: number,
 *   tileHeight: number,
 *   tileCount: number,
 *   tiles: Array<{tileIndex,y,height,diffPixels,diffPercent}>,
 *   topMismatchTiles: Array<{tileIndex,y,height,diffPercent}>,
 * }}
 */
function compareTiles(refPath, scrPath, options = {}) {
  const tileHeight = options.tileHeight || 300;
  const threshold = options.threshold != null ? options.threshold : 0.1;

  const { PNG } = loadModule('pngjs');
  const pm = loadModule('pixelmatch');
  const pixelmatch = pm.default || pm;

  const ref = PNG.sync.read(fs.readFileSync(refPath));
  const scr = PNG.sync.read(fs.readFileSync(scrPath));

  const width = Math.min(ref.width, scr.width);
  const height = Math.min(ref.height, scr.height);

  const tiles = [];

  for (let y = 0; y < height; y += tileHeight) {
    const h = Math.min(tileHeight, height - y);

    const refSlice = extractSlice(ref.data, ref.width, y, width, h);
    const scrSlice = extractSlice(scr.data, scr.width, y, width, h);
    const diffSlice = Buffer.alloc(width * h * 4);

    const diffPixels = pixelmatch(refSlice, scrSlice, diffSlice, width, h, { threshold });
    const diffPercent = +(diffPixels / (width * h) * 100).toFixed(2);

    tiles.push({
      tileIndex: tiles.length,
      y,
      height: h,
      diffPixels,
      diffPercent,
    });
  }

  const topMismatchTiles = [...tiles]
    .filter((t) => t.diffPercent > 0)
    .sort((a, b) => b.diffPercent - a.diffPercent)
    .slice(0, 5);

  return {
    ok: true,
    width,
    height,
    tileHeight,
    tileCount: tiles.length,
    tiles,
    topMismatchTiles,
  };
}

module.exports = { compareTiles };
