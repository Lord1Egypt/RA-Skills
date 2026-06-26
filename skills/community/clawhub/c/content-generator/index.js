"use strict";

const {
  generateContentPack,
  normalizeProduct,
  renderMarkdown,
  validateProduct
} = require("./scripts/generate_content_pack");

class ContentGenerator {
  generate(product, options = {}) {
    const input = {
      ...product,
      platforms: [options.platform || product.platform || "xiaohongshu"]
    };
    const pack = generateContentPack(input);
    return pack.platforms[input.platforms[0]];
  }

  generateAll(product) {
    return generateContentPack(product).platforms;
  }

  generatePack(product) {
    return generateContentPack(product);
  }
}

module.exports = {
  ContentGenerator,
  generateContentPack,
  normalizeProduct,
  renderMarkdown,
  validateProduct
};
