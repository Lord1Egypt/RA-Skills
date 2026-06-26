import fs from 'fs';
import path from 'path';
import os from 'os';
import yaml from 'yaml';

const SCRAPBOOK_DIR = path.join(os.homedir(), '.browser-secure', 'scrapbook');
const SITE_PROFILES_FILE = path.join(SCRAPBOOK_DIR, 'site-profiles.yaml');
const CAPTURES_FILE = path.join(SCRAPBOOK_DIR, 'captures.yaml');

fs.mkdirSync(SCRAPBOOK_DIR, { recursive: true });

// ─── Site Profiles ─────────────────────────────────────────────────────────

export interface SitePlaybook {
  discovery: {
    method: 'search' | 'browse' | 'direct';
    search_url?: string;
    search_input_selector?: string;
    search_submit_action?: string;
    browse_url?: string;
  };
  access: {
    login_required: boolean;
    login_url?: string;
    login_form_selector?: string;
  };
  extraction: {
    title_selector?: string;
    body_selector?: string;
    author_selector?: string;
    date_selector?: string;
  };
}

export interface SiteProfile {
  id: string;
  name: string;
  url: string;
  login_required: boolean;
  vault_config?: {
    provider: string;
    vault?: string;
    item?: string;
    username_field?: string;
    password_field?: string;
  };
  search?: {
    available: boolean;
    input_selector?: string;
    submit_action?: string;
  };
  navigation: Array<{ name: string; url: string }>;
  content_selectors: {
    title?: string;
    body?: string;
    author?: string;
    date?: string;
  };
  playbook?: SitePlaybook;
  sample_excerpt?: string;
  init_confirmed_at?: string;
  screenshots?: string[];
}

function loadSiteProfiles(): SiteProfile[] {
  if (!fs.existsSync(SITE_PROFILES_FILE)) return [];
  const data = yaml.parse(fs.readFileSync(SITE_PROFILES_FILE, 'utf-8'));
  return data?.site_profiles || [];
}

function saveSiteProfiles(profiles: SiteProfile[]): void {
  fs.writeFileSync(SITE_PROFILES_FILE, yaml.stringify({ site_profiles: profiles }), { encoding: 'utf-8', mode: 0o600 });
}

export function getSiteProfile(id: string): SiteProfile | undefined {
  return loadSiteProfiles().find(p => p.id === id);
}

export function listSiteProfiles(): SiteProfile[] {
  return loadSiteProfiles();
}

export function saveSiteProfile(profile: SiteProfile): void {
  const profiles = loadSiteProfiles().filter(p => p.id !== profile.id);
  profiles.push(profile);
  saveSiteProfiles(profiles);
}

export function deleteSiteProfile(id: string): void {
  const profiles = loadSiteProfiles().filter(p => p.id !== id);
  saveSiteProfiles(profiles);
}

// ─── Captures ──────────────────────────────────────────────────────────────

export interface Capture {
  id: string;
  site_id: string;
  url: string;
  referrer?: string;
  discovery_method?: string;
  title?: string;
  excerpt?: string;
  full_text?: string;
  html_path?: string;
  word_count?: number;
  captured_at: string;
  credentials_used: boolean;
  screenshot?: string;
  selectors_used?: Record<string, string>;
  approval_chain: {
    site_access?: { approved: boolean; auto: boolean };
    credential_use?: { approved: boolean; auto: boolean };
    extract_content?: { approved: boolean; auto: boolean };
    record_content?: { approved: boolean; auto: boolean };
  };
}

function loadCaptures(): Capture[] {
  if (!fs.existsSync(CAPTURES_FILE)) return [];
  const data = yaml.parse(fs.readFileSync(CAPTURES_FILE, 'utf-8'));
  return data?.captures || [];
}

function saveCaptures(captures: Capture[]): void {
  fs.writeFileSync(CAPTURES_FILE, yaml.stringify({ captures }), { encoding: 'utf-8', mode: 0o600 });
}

export function getCapture(id: string): Capture | undefined {
  return loadCaptures().find(c => c.id === id);
}

export function listCaptures(): Capture[] {
  return loadCaptures();
}

export function listCapturesBySite(siteId: string): Capture[] {
  return loadCaptures().filter(c => c.site_id === siteId);
}

export function saveCapture(capture: Capture): void {
  const captures = loadCaptures().filter(c => c.id !== capture.id);
  captures.push(capture);
  saveCaptures(captures);
}

export function urlAlreadyCaptured(url: string): boolean {
  return loadCaptures().some(c => c.url === url);
}

// ─── Export ────────────────────────────────────────────────────────────────

export function exportToMarkdown(): string {
  const captures = loadCaptures();
  let md = '# browser-secure Scrapbook\n\n';
  for (const c of captures) {
    md += `## ${c.title || 'Untitled'}\n\n`;
    md += `- **Source:** ${c.site_id}\n`;
    md += `- **URL:** ${c.url}\n`;
    md += `- **Captured:** ${c.captured_at}\n`;
    if (c.word_count) md += `- **Word count:** ${c.word_count}\n`;
    md += '\n';
    if (c.excerpt) md += `> ${c.excerpt}\n\n`;
    if (c.full_text) md += `${c.full_text}\n\n`;
    md += '---\n\n';
  }
  return md;
}

export function exportToJson(): string {
  return JSON.stringify({ captures: loadCaptures(), site_profiles: loadSiteProfiles() }, null, 2);
}
