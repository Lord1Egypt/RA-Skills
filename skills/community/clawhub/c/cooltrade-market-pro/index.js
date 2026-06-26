const path = require('path');
const fs = require('fs');

module.exports = {
  getSkills: () => {
    const configPath = path.join(__dirname, 'openclaw.json');
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      return config.skills || [];
    }
    return [];
  }
};
