const PATH_ALLOWLIST = [
    '/Applications/',
    '/System/Applications/',
];
const NAME_PATTERN_BLOCKLIST = [
    /Helper(?:$|\s\()/,
    /Agent(?:$|\s\()/,
    /Service(?:$|\s\()/,
    /Uninstaller(?:$|\s\()/,
    /Updater(?:$|\s\()/,
    /^\./,
];
const ALWAYS_KEEP_BUNDLE_IDS = new Set([
    'com.apple.Safari',
    'com.google.Chrome',
    'com.microsoft.edgemac',
    'org.mozilla.firefox',
    'company.thebrowser.Browser',
    'com.tinyspeck.slackmacgap',
    'us.zoom.xos',
    'com.microsoft.teams2',
    'com.microsoft.teams',
    'com.apple.MobileSMS',
    'com.apple.mail',
    'com.microsoft.Word',
    'com.microsoft.Excel',
    'com.microsoft.Powerpoint',
    'com.microsoft.Outlook',
    'com.apple.iWork.Pages',
    'com.apple.iWork.Numbers',
    'com.apple.iWork.Keynote',
    'notion.id',
    'com.apple.Notes',
    'md.obsidian',
    'com.linear',
    'com.figma.Desktop',
    'com.microsoft.VSCode',
    'com.apple.Terminal',
    'com.googlecode.iterm2',
    'com.github.GitHubDesktop',
    'com.apple.finder',
    'com.apple.iCal',
    'com.apple.systempreferences',
]);
const APP_NAME_ALLOWED = /^[\p{L}\p{M}\p{N}_ .&'()+-]+$/u;
const APP_NAME_MAX_LEN = 40;
const APP_NAME_MAX_COUNT = 50;
function isUserFacingPath(path, homeDir) {
    if (PATH_ALLOWLIST.some(root => path.startsWith(root)))
        return true;
    if (homeDir) {
        const userApps = homeDir.endsWith('/') ? `${homeDir}Applications/` : `${homeDir}/Applications/`;
        if (path.startsWith(userApps))
            return true;
    }
    return false;
}
function sanitizeCore(raw, applyCharFilter) {
    const seen = new Set();
    return raw
        .map(name => name.trim())
        .filter(trimmed => {
        if (!trimmed || trimmed.length > APP_NAME_MAX_LEN)
            return false;
        if (applyCharFilter && !APP_NAME_ALLOWED.test(trimmed))
            return false;
        if (seen.has(trimmed))
            return false;
        seen.add(trimmed);
        return true;
    })
        .sort((a, b) => a.localeCompare(b));
}
function sanitizeAppNames(raw) {
    const filtered = sanitizeCore(raw, true);
    if (filtered.length <= APP_NAME_MAX_COUNT)
        return filtered;
    return [
        ...filtered.slice(0, APP_NAME_MAX_COUNT),
        `... and ${filtered.length - APP_NAME_MAX_COUNT} more`,
    ];
}
export function filterAppsForDescription(installed, homeDir) {
    const alwaysKept = [];
    const rest = [];
    for (const app of installed) {
        if (ALWAYS_KEEP_BUNDLE_IDS.has(app.bundleId)) {
            alwaysKept.push(app.displayName);
            continue;
        }
        if (isUserFacingPath(app.path, homeDir) && !NAME_PATTERN_BLOCKLIST.some(re => re.test(app.displayName))) {
            rest.push(app.displayName);
        }
    }
    const sanitizedAlways = sanitizeCore(alwaysKept, false);
    const alwaysSet = new Set(sanitizedAlways);
    return [
        ...sanitizedAlways,
        ...sanitizeAppNames(rest).filter(name => !alwaysSet.has(name)),
    ];
}
//# sourceMappingURL=appNames.js.map