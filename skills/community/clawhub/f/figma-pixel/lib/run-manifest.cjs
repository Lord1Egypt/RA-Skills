const fs = require('fs');
const path = require('path');

function slugify(input) {
  return String(input || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/-{2,}/g, '-');
}

function createRunManifest(projectSlugInput = 'project', runIdInput = '', rootDirInput = path.resolve(process.cwd(), 'figma-pixel-runs')) {
  const projectSlug = slugify(projectSlugInput || 'project');
  const runId = runIdInput || new Date().toISOString().replace(/[:.]/g, '-');
  const rootDir = path.resolve(rootDirInput);

  const projectDir = path.join(rootDir, projectSlug);
  const runDir = path.join(projectDir, runId);
  const subdirs = ['figma', 'capture', 'backstop', 'pixelmatch', 'final'];
  const sharedDirs = {
    root: path.join(projectDir, 'shared'),
    figma: path.join(projectDir, 'shared', 'figma'),
  };

  fs.mkdirSync(runDir, { recursive: true });
  for (const dir of subdirs) fs.mkdirSync(path.join(runDir, dir), { recursive: true });
  for (const dir of Object.values(sharedDirs)) fs.mkdirSync(dir, { recursive: true });

  const manifest = {
    projectSlug,
    runId,
    rootDir,
    projectDir,
    runDir,
    subdirs: Object.fromEntries(subdirs.map((dir) => [dir, path.join(runDir, dir)])),
    sharedDirs,
  };

  const manifestPath = path.join(runDir, 'run-manifest.json');
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
  return { ok: true, manifestPath, ...manifest };
}

module.exports = { createRunManifest };
