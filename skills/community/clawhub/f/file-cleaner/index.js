const fs = require('fs');
const path = require('path');

/**
 * Safely cleans up a directory or file.
 * Only allows deletion within specific temporary or safe paths to prevent accidents.
 * @param {string} targetPath - The path to clean.
 * @returns {Promise<string>} - Result message.
 */
async function clean(targetPath) {
  if (!targetPath) {
    throw new Error('Target path is required');
  }

  // Resolve absolute path
  const absolutePath = path.resolve(process.cwd(), targetPath);
  const workspaceRoot = process.cwd();

  // Safety checks
  const allowedPrefixes = [
    path.join(workspaceRoot, 'temp'),
    path.join(workspaceRoot, 'logs'),
    path.join(workspaceRoot, 'cache')
  ];

  const isAllowed = allowedPrefixes.some(prefix => absolutePath.startsWith(prefix));

  if (!isAllowed) {
    // Also allow specific single files if they are clearly temp files in root (e.g. *.tmp, *.log)
    // But generally enforce temp/ usage.
    // For now, strict safety: only allow deletion inside temp/, logs/, or cache/
    throw new Error(`Safety Warning: Deletion denied for path '${targetPath}'. Only paths inside 'temp/', 'logs/', or 'cache/' are allowed.`);
  }

  if (absolutePath === workspaceRoot || absolutePath === path.join(workspaceRoot, 'skills')) {
     throw new Error('CRITICAL: Attempted to delete workspace root or skills directory.');
  }

  try {
    const stats = await fs.promises.stat(absolutePath);
    if (stats.isDirectory()) {
      await fs.promises.rm(absolutePath, { recursive: true, force: true });
      return `Successfully deleted directory: ${targetPath}`;
    } else {
      await fs.promises.unlink(absolutePath);
      return `Successfully deleted file: ${targetPath}`;
    }
  } catch (error) {
    if (error.code === 'ENOENT') {
      return `Path does not exist, skipped: ${targetPath}`;
    }
    throw error;
  }
}

// CLI wrapper
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: node skills/file-cleaner/index.js <path_to_clean>');
    process.exit(1);
  }

  const target = args[0];
  clean(target)
    .then(msg => console.log(msg))
    .catch(err => {
      console.error(`Error: ${err.message}`);
      process.exit(1);
    });
}

module.exports = { clean };
