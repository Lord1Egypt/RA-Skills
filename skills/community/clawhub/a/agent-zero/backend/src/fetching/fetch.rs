//! HTML fetching: direct HTTP client with Safari/AppleScript and Chrome CDP fallbacks
//! for bot-protected hosts.

use chromiumoxide::browser::{Browser, BrowserConfig};
use chromiumoxide::cdp::browser_protocol::page::AddScriptToEvaluateOnNewDocumentParams;
use futures::StreamExt;
use reqwest::header::{
    HeaderMap, HeaderValue, ACCEPT, ACCEPT_ENCODING, ACCEPT_LANGUAGE, REFERER, USER_AGENT,
};
use reqwest::Client;
use std::time::Duration;
use url::Url;

/// Stealth JS injected via CDP before any page script runs.
/// Hides automation signals that Incapsula/Imperva use for bot detection.
const STEALTH_JS: &str = r#"
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
if (!window.chrome) { window.chrome = {}; }
if (!window.chrome.runtime) { window.chrome.runtime = {}; }
Object.defineProperty(navigator, 'plugins', {
    get: () => {
        const arr = [
            { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format' },
            { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: '' },
            { name: 'Native Client', filename: 'internal-nacl-plugin', description: '' },
        ];
        arr.refresh = () => {};
        return arr;
    },
});
Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) =>
    parameters.name === 'notifications'
        ? Promise.resolve({ state: Notification.permission })
        : originalQuery(parameters);
try {
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37445) return 'Intel Inc.';
        if (parameter === 37446) return 'Intel Iris OpenGL Engine';
        return getParameter.call(this, parameter);
    };
} catch (e) {}
Object.defineProperty(navigator, 'connection', {
    get: () => ({ effectiveType: '4g', rtt: 50, downlink: 10, saveData: false }),
});
"#;

/// Fetch HTML using the reqwest HTTP client.
async fn fetch_html_direct(client: &Client, url: &Url) -> Result<String, reqwest::Error> {
    let mut headers = HeaderMap::new();
    headers.insert(
        USER_AGENT,
        HeaderValue::from_static("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"),
    );
    headers.insert(
        ACCEPT,
        HeaderValue::from_static(
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        ),
    );
    headers.insert(ACCEPT_LANGUAGE, HeaderValue::from_static("en-US,en;q=0.9"));
    headers.insert(
        ACCEPT_ENCODING,
        HeaderValue::from_static("gzip, deflate, br"),
    );
    if let Ok(rv) = HeaderValue::from_str(url.as_str()) {
        headers.insert(REFERER, rv);
    }

    let resp = client.get(url.as_str()).headers(headers).send().await?;
    resp.error_for_status_ref()?;
    resp.text().await
}

/// Fetch HTML by opening the URL in Safari via AppleScript.
///
/// Safari passes bot-protection checks (Incapsula, PerimeterX) that block
/// plain HTTP clients because it runs the full JS challenge in a real browser
/// context.  The page is opened in a new tab, allowed to settle for ~20 s,
/// and the rendered DOM source is returned.
async fn fetch_html_safari(url: &Url) -> Result<String, String> {
    let script = format!(
        r#"
tell application "Safari"
    activate
    make new document with properties {{URL:"{url}"}}
    delay 20
    set pageSource to source of document 1
    close document 1
    return pageSource
end tell
"#,
        url = url.as_str()
    );
    let output = tokio::process::Command::new("osascript")
        .arg("-e")
        .arg(&script)
        .output()
        .await
        .map_err(|e| format!("osascript failed: {e}"))?;

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        return Err(format!("osascript error: {stderr}"));
    }
    let html = String::from_utf8_lossy(&output.stdout).to_string();
    if html.len() < 2000 {
        return Err(format!("Safari returned only {} bytes (likely blocked)", html.len()));
    }
    Ok(html)
}

/// Fetch HTML by launching Chrome via CDP with stealth JS injection.
///
/// Uses chromiumoxide to control a real Chrome instance (headed, non-headless)
/// which bypasses Incapsula/Imperva bot detection. Cookies are persisted in a
/// profile directory so subsequent fetches reuse the session.
///
/// This is the fallback when both the direct HTTP fetch and Safari fail.
async fn fetch_html_chrome(url: &Url) -> Result<String, String> {
    let home = std::env::var("HOME").unwrap_or_else(|_| ".".to_string());
    let profile_dir = std::path::PathBuf::from(home).join(".agent-zero-chrome-profile");
    let _ = std::fs::create_dir_all(&profile_dir);
    let profile_dir = std::fs::canonicalize(&profile_dir).unwrap_or(profile_dir);

    let mut builder = BrowserConfig::builder()
        .disable_default_args()
        .no_sandbox()
        .window_size(1920, 1080)
        .user_data_dir(profile_dir)
        .arg("--disable-blink-features=AutomationControlled")
        .arg("--disable-features=IsolateOrigins,site-per-process")
        .arg("--disable-infobars")
        .arg("--disable-dev-shm-usage")
        .arg("--no-first-run")
        .arg("--disable-gpu")
        .arg("--lang=en-US,en")
        .arg("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
        .with_head();

    // On macOS, Chrome may not be in PATH — try the standard app location.
    let macos_chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
    if std::path::Path::new(macos_chrome).exists() {
        builder = builder.chrome_executable(macos_chrome);
    }

    let config = builder
        .build()
        .map_err(|e| format!("Chrome config error: {e}"))?;

    let (mut browser, mut handler) = Browser::launch(config)
        .await
        .map_err(|e| format!("Failed to launch Chrome: {e}"))?;

    let _handle = tokio::spawn(async move {
        while let Some(h) = handler.next().await {
            if h.is_err() {
                break;
            }
        }
    });

    let page = browser
        .new_page("about:blank")
        .await
        .map_err(|e| format!("Chrome new page error: {e}"))?;

    page.execute(
        AddScriptToEvaluateOnNewDocumentParams::builder()
            .source(STEALTH_JS)
            .build()
            .unwrap(),
    )
    .await
    .map_err(|e| format!("Chrome stealth injection error: {e}"))?;

    page.goto(url.as_str())
        .await
        .map_err(|e| format!("Chrome navigation error: {e}"))?;

    // Poll until real listing content appears or timeout.
    let timeout = Duration::from_secs(30);
    let start = std::time::Instant::now();
    let html = loop {
        let html: String = page
            .evaluate("document.documentElement.outerHTML")
            .await
            .map_err(|e| format!("Chrome eval error: {e}"))?
            .into_value()
            .map_err(|e| format!("Chrome HTML deserialize error: {e}"))?;

        let has_content = html.len() > 50_000
            || html.contains("listingId")
            || html.contains("propertyDetails");

        if has_content || start.elapsed() >= timeout {
            break html;
        }

        tokio::time::sleep(Duration::from_secs(2)).await;
    };

    let _ = browser.close().await;

    if html.len() < 5000 {
        return Err(format!(
            "Chrome returned only {} bytes (likely blocked)",
            html.len()
        ));
    }
    Ok(html)
}

/// Returns `true` when the HTML looks like a bot-protection challenge page
/// rather than real listing content.
fn is_challenge_page(html: &str) -> bool {
    html.len() < 2000
        && (html.contains("Incapsula")
            || html.contains("_Incapsula_Resource")
            || html.contains("px-blocked")
            || html.contains("PerimeterX"))
}

/// Returns `true` for hosts known to use aggressive bot protection that
/// blocks plain HTTP clients (even with TLS impersonation).
fn is_bot_protected_host(url: &Url) -> bool {
    match url.host_str().unwrap_or("") {
        h if h.contains("zillow.com") => true,
        h if h.contains("realtor.ca") => true,
        _ => false,
    }
}

/// Fetch HTML for a listing URL.
///
/// Strategy:
/// 1. Try the reqwest HTTP client directly.
/// 2. For bot-protected hosts (realtor.ca, zillow.com), fall back to Safari
///    via AppleScript (lower overhead when Safari is already running).
/// 3. If Safari fails or `SKIP_SAFARI=1` is set, fall back to Chrome via CDP.
pub(crate) async fn fetch_html(client: &Client, url: &Url) -> Result<String, String> {
    // Fast path: direct HTTP fetch.
    match fetch_html_direct(client, url).await {
        Ok(html) if !is_challenge_page(&html) => return Ok(html),
        Ok(html) if !is_bot_protected_host(url) => return Ok(html),
        Ok(_challenge) => {
            tracing::info!(
                "fetch_html: direct fetch returned challenge page for {}, trying Safari",
                url
            );
        }
        Err(e) if is_bot_protected_host(url) => {
            tracing::info!(
                "fetch_html: direct fetch failed for {} ({}), trying Safari",
                url,
                e
            );
        }
        Err(e) => return Err(format!("Failed to fetch {url}: {e}")),
    }

    // SKIP_SAFARI=1 bypasses Safari entirely (useful for testing Chrome directly).
    let skip_safari = std::env::var("SKIP_SAFARI").map(|v| v == "1").unwrap_or(false);

    if !skip_safari {
        // Try Safari first (lower overhead if already open).
        match fetch_html_safari(url).await {
            Ok(html) => return Ok(html),
            Err(e) => {
                tracing::info!(
                    "fetch_html: Safari failed for {} ({}), trying Chrome",
                    url,
                    e
                );
            }
        }
    } else {
        tracing::info!("fetch_html: SKIP_SAFARI=1, skipping Safari for {}", url);
    }

    // Chrome via CDP (works even when Safari is not running).
    fetch_html_chrome(url).await
}
