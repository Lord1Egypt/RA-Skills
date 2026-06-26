#!/usr/bin/env node

import { existsSync } from 'fs';
import { mkdir, readFile, rm, stat, writeFile } from 'fs/promises';
import { dirname } from 'path';

function pathExists(path) {
  return existsSync(path);
}

async function ensureDir(path) {
  await mkdir(path, { recursive: true });
}

async function makeDir(path, options = {}) {
  await mkdir(path, options);
}

async function readJsonFile(path, fallbackValue) {
  if (!pathExists(path)) {
    return fallbackValue;
  }
  return JSON.parse(await readFile(path, 'utf-8'));
}

async function writeJsonFile(path, value) {
  await ensureDir(dirname(path));
  await writeFile(path, JSON.stringify(value, null, 2));
}

async function readTextFile(path) {
  return readFile(path, 'utf-8');
}

async function writeTextFile(path, value) {
  await ensureDir(dirname(path));
  await writeFile(path, value);
}

async function removePath(path, options = {}) {
  await rm(path, options);
}

async function statPath(path) {
  return stat(path);
}

export {
  ensureDir,
  makeDir,
  pathExists,
  readJsonFile,
  readTextFile,
  removePath,
  statPath,
  writeJsonFile,
  writeTextFile
};
