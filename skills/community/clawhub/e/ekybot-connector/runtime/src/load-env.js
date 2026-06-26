const path = require('path');
const dotenv = require('dotenv');

function loadCompanionEnv() {
  const explicitPath =
    process.env.EKYBOT_COMPANION_ENV_FILE || process.env.DOTENV_CONFIG_PATH || null;

  if (explicitPath) {
    dotenv.config({ path: path.resolve(explicitPath) });
    return;
  }

  dotenv.config();
}

module.exports = loadCompanionEnv;
