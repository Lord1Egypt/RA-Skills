import path from "node:path";
import fs from "node:fs/promises";
import { dontDealHome, ensureDirectory, pathExists, writeJsonFile } from "./utils.js";

function profilePath(env = process.env) {
  return path.join(dontDealHome(env), "profile.json");
}

function eventsPath(env = process.env) {
  return path.join(dontDealHome(env), "events.json");
}

async function readJsonFileOrDefault(targetPath, fallback) {
  if (!(await pathExists(targetPath))) {
    return fallback;
  }

  const text = await fs.readFile(targetPath, "utf8");
  if (!text.trim()) {
    return fallback;
  }

  return JSON.parse(text);
}

export async function loadProfile(env = process.env) {
  return readJsonFileOrDefault(profilePath(env), {
    version: 1,
    updated_at: null,
    person: {
      age_range: null,
      sex: null
    },
    baseline_risks: {
      hypertension: null,
      diabetes: null,
      smoking: null,
      high_cholesterol: null,
      family_history_early_heart_disease: null
    },
    medications: [],
    emergency_contacts: [],
    notes: []
  });
}

export async function saveProfile(profile, env = process.env) {
  const nextProfile = {
    ...profile,
    version: 1,
    updated_at: new Date().toISOString()
  };

  await writeJsonFile(profilePath(env), nextProfile);
  return nextProfile;
}

export async function loadEvents(env = process.env) {
  return readJsonFileOrDefault(eventsPath(env), []);
}

export async function appendEvent(event, env = process.env) {
  const home = dontDealHome(env);
  await ensureDirectory(home);

  const events = await loadEvents(env);
  const nextEvent = {
    ...event,
    id: event.id ?? crypto.randomUUID(),
    recorded_at: event.recorded_at ?? new Date().toISOString()
  };

  events.push(nextEvent);
  await writeJsonFile(eventsPath(env), events);
  return nextEvent;
}
