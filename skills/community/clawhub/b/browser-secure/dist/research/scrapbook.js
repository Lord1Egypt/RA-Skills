import fs from 'fs';
import path from 'path';
import os from 'os';
import yaml from 'yaml';
const SCRAPBOOK_DIR = path.join(os.homedir(), '.browser-secure', 'scrapbook');
const SITE_PROFILES_FILE = path.join(SCRAPBOOK_DIR, 'site-profiles.yaml');
const CAPTURES_FILE = path.join(SCRAPBOOK_DIR, 'captures.yaml');
fs.mkdirSync(SCRAPBOOK_DIR, { recursive: true });
function loadSiteProfiles() {
    if (!fs.existsSync(SITE_PROFILES_FILE))
        return [];
    const data = yaml.parse(fs.readFileSync(SITE_PROFILES_FILE, 'utf-8'));
    return data?.site_profiles || [];
}
function saveSiteProfiles(profiles) {
    fs.writeFileSync(SITE_PROFILES_FILE, yaml.stringify({ site_profiles: profiles }), { encoding: 'utf-8', mode: 0o600 });
}
export function getSiteProfile(id) {
    return loadSiteProfiles().find(p => p.id === id);
}
export function listSiteProfiles() {
    return loadSiteProfiles();
}
export function saveSiteProfile(profile) {
    const profiles = loadSiteProfiles().filter(p => p.id !== profile.id);
    profiles.push(profile);
    saveSiteProfiles(profiles);
}
export function deleteSiteProfile(id) {
    const profiles = loadSiteProfiles().filter(p => p.id !== id);
    saveSiteProfiles(profiles);
}
function loadCaptures() {
    if (!fs.existsSync(CAPTURES_FILE))
        return [];
    const data = yaml.parse(fs.readFileSync(CAPTURES_FILE, 'utf-8'));
    return data?.captures || [];
}
function saveCaptures(captures) {
    fs.writeFileSync(CAPTURES_FILE, yaml.stringify({ captures }), { encoding: 'utf-8', mode: 0o600 });
}
export function getCapture(id) {
    return loadCaptures().find(c => c.id === id);
}
export function listCaptures() {
    return loadCaptures();
}
export function listCapturesBySite(siteId) {
    return loadCaptures().filter(c => c.site_id === siteId);
}
export function saveCapture(capture) {
    const captures = loadCaptures().filter(c => c.id !== capture.id);
    captures.push(capture);
    saveCaptures(captures);
}
export function urlAlreadyCaptured(url) {
    return loadCaptures().some(c => c.url === url);
}
// ─── Export ────────────────────────────────────────────────────────────────
export function exportToMarkdown() {
    const captures = loadCaptures();
    let md = '# browser-secure Scrapbook\n\n';
    for (const c of captures) {
        md += `## ${c.title || 'Untitled'}\n\n`;
        md += `- **Source:** ${c.site_id}\n`;
        md += `- **URL:** ${c.url}\n`;
        md += `- **Captured:** ${c.captured_at}\n`;
        if (c.word_count)
            md += `- **Word count:** ${c.word_count}\n`;
        md += '\n';
        if (c.excerpt)
            md += `> ${c.excerpt}\n\n`;
        if (c.full_text)
            md += `${c.full_text}\n\n`;
        md += '---\n\n';
    }
    return md;
}
export function exportToJson() {
    return JSON.stringify({ captures: loadCaptures(), site_profiles: loadSiteProfiles() }, null, 2);
}
