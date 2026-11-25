import { existsSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

const DEFAULT_PROFILES = {
  common: {
    profile: 'common',
    auth_mode: 'env',
    enable_skill_update: true,
    default_service_level: null,
    hide_cv_meta: false,
    balance_precheck: false,
    partner_code: '',
  },
  'navos-cn': {
    profile: 'navos-cn',
    auth_mode: 'navos',
    navos_region: 'cn',
    prompt_locale: 'zh',
    default_lang: 'cn',
    enable_skill_update: false,
    default_service_level: 'S3',
    hide_cv_meta: true,
    balance_precheck: true,
    partner_code: 'navos-cn',
  },
  'navos-global': {
    profile: 'navos-global',
    auth_mode: 'navos',
    navos_region: 'global',
    prompt_locale: 'en',
    default_lang: 'en',
    enable_skill_update: false,
    default_service_level: 'S3',
    hide_cv_meta: true,
    balance_precheck: true,
    partner_code: 'navos-global',
  },
};

function readJSON(url) {
  return JSON.parse(readFileSync(url, 'utf8').replace(/^\uFEFF/, ''));
}

function readProfileFile(profileName) {
  try {
    return readJSON(new URL(`../profiles/${profileName}.json`, import.meta.url));
  } catch {
    return {};
  }
}

function readSkillMeta() {
  try {
    return readJSON(new URL('../skill.json', import.meta.url));
  } catch {
    return {};
  }
}

function normalizeProfileName(value) {
  const profile = String(value || '').trim().toLowerCase();
  if (profile === 'navos') return 'navos-global';
  return profile || 'common';
}

function normalizeNavosAppProfile(value) {
  const appId = normalizeProfileName(value);
  return appId === 'navos-cn' || appId === 'navos-global' ? appId : '';
}

function resolveIdentityPath() {
  const override = process.env.NAVOS_IDENTITY_FILE;
  if (override && override.trim()) {
    return override.trim();
  }
  return join(homedir(), '.navos', 'identity', 'navos-userinfo.json');
}

function resolveNavosSettingsPath() {
  const override = process.env.NAVOS_SETTINGS_FILE;
  if (override && override.trim()) {
    return override.trim();
  }

  const appData = (process.env.APPDATA || '').trim();
  if (appData) {
    return join(appData, '@navos-mind', 'navos', 'navos.json');
  }

  return join(homedir(), 'AppData', 'Roaming', '@navos-mind', 'navos', 'navos.json');
}

function normalizeNavosLanguage(value, source = 'default') {
  const language = String(value || '').trim();
  const normalized = language.toLowerCase();
  if (normalized.startsWith('zh')) {
    return {
      prompt_locale: 'zh',
      default_lang: 'cn',
      navos_language: language || 'zh-CN',
      navos_language_source: source,
    };
  }

  return {
    prompt_locale: 'en',
    default_lang: 'en',
    navos_language: language || 'en-US',
    navos_language_source: source,
  };
}

function readNavosLanguageProfile() {
  const envLanguage = (process.env.NAVOS_LANGUAGE || '').trim();
  if (envLanguage) {
    return normalizeNavosLanguage(envLanguage, 'env');
  }

  const path = resolveNavosSettingsPath();
  if (!existsSync(path)) {
    return normalizeNavosLanguage('', 'default');
  }

  try {
    const data = readJSON(path);
    return normalizeNavosLanguage(data?.app?.language, 'file');
  } catch {
    return normalizeNavosLanguage('', 'default');
  }
}

function readNavosAppId() {
  const envAppId = normalizeNavosAppProfile(process.env.NAVOS_APP_ID);
  if (envAppId) return envAppId;

  const path = resolveIdentityPath();
  if (!existsSync(path)) return '';

  try {
    const data = readJSON(path);
    return normalizeNavosAppProfile(data?.app_id) || 'navos-global';
  } catch {
    return '';
  }
}

function resolveRuntimeProfileName(meta) {
  const explicit = normalizeProfileName(process.env.CV_SKILL_PROFILE);
  if (explicit !== 'common' || process.env.CV_SKILL_PROFILE) {
    return explicit;
  }

  const appProfile = readNavosAppId();
  if (appProfile) return appProfile;

  return normalizeProfileName(meta.profile || meta.runtime?.profile || 'common');
}

export function loadRuntimeProfile({ skillMeta = null } = {}) {
  const meta = skillMeta || readSkillMeta();
  const profileName = resolveRuntimeProfileName(meta);
  const defaults = DEFAULT_PROFILES[profileName] || DEFAULT_PROFILES.common;
  const fileProfile = readProfileFile(profileName);
  const runtimeOverrides = meta.runtime || {};

  const profile = {
    ...defaults,
    ...fileProfile,
    ...runtimeOverrides,
    profile: profileName,
  };
  const navosLanguageProfile = isNavosProfile(profile) ? readNavosLanguageProfile() : {};
  const navosBaseUrl = profile.navos_base_url || '';
  const navosValidateBaseUrl = profile.navos_validate_base_url || navosBaseUrl;
  const navosCallbackBaseUrl = profile.navos_callback_base_url || navosBaseUrl;
  return {
    ...profile,
    ...navosLanguageProfile,
    ...(navosValidateBaseUrl && { navos_validate_base_url: navosValidateBaseUrl }),
    ...(navosCallbackBaseUrl && { navos_callback_base_url: navosCallbackBaseUrl }),
  };
}

export function isNavosProfile(profile) {
  return profile?.profile === 'navos' || profile?.auth_mode === 'navos';
}
