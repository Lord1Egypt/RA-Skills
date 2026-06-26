function getFigmaToken(options = {}) {
  const token = options.token || process.env.FIGMA_TOKEN;

  if (!token) {
    throw new Error(
      'FIGMA_TOKEN is required. Create a Figma personal access token and pass it via environment variable.'
    );
  }

  return token;
}

module.exports = { getFigmaToken };
