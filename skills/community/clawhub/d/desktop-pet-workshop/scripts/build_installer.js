#!/usr/bin/env node
/**
 * Desktop Pet Installer Builder
 *
 * Copies the Electron app template, embeds generated pet assets,
 * installs dependencies, and builds platform-specific installers.
 *
 * Usage:
 *   node build_installer.js <assets-dir> <output-dir> [--os windows|mac|auto]
 *
 * Arguments:
 *   assets-dir   Directory containing pet action images (01_idle_breathing.png, etc.)
 *   output-dir   Directory where the final installer will be placed
 *   --os         Target OS: windows (.exe), mac (.dmg), or auto (detect current OS)
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const TEMPLATE_DIR = path.join(__dirname, '..', 'assets', 'desktop-pet-template');
const EXPECTED_FILES = [
  '01_idle_breathing.png',
  '02_happy_jumping.png',
  '03_cute_cuddling.png',
  '04_sleepy_dozing.png',
  '05_waving_greeting.png'
];

function parseArgs() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error('Usage: node build_installer.js <assets-dir> <output-dir> [--os windows|mac|auto]');
    process.exit(1);
  }
  const assetsDir = path.resolve(args[0]);
  const outputDir = path.resolve(args[1]);
  let targetOS = 'auto';
  const osIndex = args.indexOf('--os');
  if (osIndex !== -1 && args[osIndex + 1]) {
    targetOS = args[osIndex + 1];
  }
  return { assetsDir, outputDir, targetOS };
}

function detectOS() {
  const platform = process.platform;
  if (platform === 'win32') return 'windows';
  if (platform === 'darwin') return 'mac';
  return 'windows'; // default fallback
}

function validateAssets(assetsDir) {
  for (const file of EXPECTED_FILES) {
    const filePath = path.join(assetsDir, file);
    if (!fs.existsSync(filePath)) {
      console.error(`Missing required asset: ${file} in ${assetsDir}`);
      console.error(`Expected files: ${EXPECTED_FILES.join(', ')}`);
      process.exit(1);
    }
  }
  console.log('Asset validation passed.');
}

function copyTemplate(buildDir) {
  console.log('Copying Electron app template...');
  copyDirRecursive(TEMPLATE_DIR, buildDir);
  // Remove the config.json template - it will be regenerated
  console.log('Template copied.');
}

function copyDirRecursive(src, dest) {
  if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function embedAssets(assetsDir, buildDir) {
  console.log('Embedding pet assets...');
  const petAssetsDir = path.join(buildDir, 'pet-assets');
  if (!fs.existsSync(petAssetsDir)) fs.mkdirSync(petAssetsDir, { recursive: true });

  for (const file of EXPECTED_FILES) {
    fs.copyFileSync(path.join(assetsDir, file), path.join(petAssetsDir, file));
  }
  console.log('Pet assets embedded.');
}

function generateConfig(buildDir, actionList) {
  // config.json already exists in template, but can be overridden here
  if (actionList) {
    const configPath = path.join(buildDir, 'src', 'config.json');
    fs.writeFileSync(configPath, JSON.stringify(actionList, null, 2));
    console.log('Custom config.json generated.');
  }
}

function installDependencies(buildDir) {
  console.log('Installing dependencies (this may take a few minutes)...');
  try {
    execSync('npm install', { cwd: buildDir, stdio: 'inherit', timeout: 300000 });
    console.log('Dependencies installed.');
  } catch (err) {
    console.error('Failed to install dependencies:', err.message);
    process.exit(1);
  }
}

function buildInstaller(buildDir, targetOS, outputDir) {
  console.log(`Building installer for ${targetOS}...`);
  const buildCommand = targetOS === 'windows'
    ? 'npm run build:win'
    : targetOS === 'mac'
    ? 'npm run build:mac'
    : 'npm run build';

  try {
    execSync(buildCommand, { cwd: buildDir, stdio: 'inherit', timeout: 600000 });
    console.log('Build completed.');
  } catch (err) {
    console.error('Build failed:', err.message);
    process.exit(1);
  }

  // Copy installer to output directory
  const distDir = path.join(buildDir, 'dist');
  if (!fs.existsSync(distDir)) {
    console.error('Build output directory not found:', distDir);
    process.exit(1);
  }

  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  const installers = fs.readdirSync(distDir).filter(f =>
    f.endsWith('.exe') || f.endsWith('.dmg') || f.endsWith('.AppImage')
  );

  for (const installer of installers) {
    const srcPath = path.join(distDir, installer);
    const destPath = path.join(outputDir, installer);
    fs.copyFileSync(srcPath, destPath);
    console.log(`Installer copied to: ${destPath}`);
  }

  if (installers.length === 0) {
    console.warn('No installer files found in dist directory. Check build output.');
  }
}

function main() {
  const { assetsDir, outputDir, targetOS } = parseArgs();
  const os = targetOS === 'auto' ? detectOS() : targetOS;

  console.log('=== Desktop Pet Installer Builder ===');
  console.log(`Assets dir: ${assetsDir}`);
  console.log(`Output dir: ${outputDir}`);
  console.log(`Target OS: ${os}`);
  console.log('');

  // Step 1: Validate assets
  validateAssets(assetsDir);

  // Step 2: Prepare build directory
  const buildDir = path.join(outputDir, 'build-temp');
  if (fs.existsSync(buildDir)) fs.rmSync(buildDir, { recursive: true });
  fs.mkdirSync(buildDir, { recursive: true });
  copyTemplate(buildDir);

  // Step 3: Embed assets
  embedAssets(assetsDir, buildDir);

  // Step 4: Install dependencies
  installDependencies(buildDir);

  // Step 5: Build installer
  buildInstaller(buildDir, os, outputDir);

  // Step 6: Cleanup
  console.log('Cleaning up build directory...');
  fs.rmSync(buildDir, { recursive: true });

  console.log('');
  console.log('=== Build Complete ===');
  console.log(`Installer(s) saved to: ${outputDir}`);
  const finalInstallers = fs.readdirSync(outputDir).filter(f =>
    f.endsWith('.exe') || f.endsWith('.dmg')
  );
  for (const f of finalInstallers) {
    console.log(`  - ${f}`);
  }
}

main();
