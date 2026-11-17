import { fetchPublicJs, isPublicClientWeb } from "./fetch-public.mjs";
import { describeImages } from "./media.mjs";
import {
  CAPTURED_CREATE_NOTE_TWEET_QUERY_ID,
  CAPTURED_CREATE_TWEET_QUERY_ID,
  CAPTURED_FEATURES,
  CAPTURED_NOTE_QUERY_SOURCE,
  CAPTURED_QUERY_SOURCE,
  HOME_URL,
  HOW_TO_LOGIN,
  HOW_TO_LOGIN_ZH,
  LOGIN_TIP,
  LOGIN_TIP_ZH,
  PUBLIC_WEB_BEARER,
  SKILL,
  SPACE_NAME,
  buildStatusBody,
  buildHeaders,
  classifyLogin,
  confirmationSummary,
  extractOperationQueryId,
  extractScriptUrls,
  extractWebBearer,
  graphqlUrl,
  orderScriptUrls,
  interpretCreateTweetResponse,
  isScreenName,
  needsNoteTweet,
  needsRepaint,
  normalizeLanguage,
  screenNameFromPath,
  statusUrl,
} from "./pure.mjs";

function loginStop(message) {
  return {
    ok: false,
    sent: false,
    logged_in: false,
    login_required: true,
    exitCode: 2,
    error: message,
    how_to_login: HOW_TO_LOGIN,
    how_to_login_zh: HOW_TO_LOGIN_ZH,
    login_tip: LOGIN_TIP,
    login_tip_zh: LOGIN_TIP_ZH,
  };
}

export async function resolveOperationQuery(session, operationName, override) {
  const note = operationName === "CreateNoteTweet";
  const capturedId = note ? CAPTURED_CREATE_NOTE_TWEET_QUERY_ID : CAPTURED_CREATE_TWEET_QUERY_ID;
  const capturedSource = note ? CAPTURED_NOTE_QUERY_SOURCE : CAPTURED_QUERY_SOURCE;
  if (override) return { queryId: override, source: "flag", bearer: "", operation: operationName };
  let html = "";
  if (typeof session.shellHtml === "function") {
    try {
      const shell = await session.shellHtml();
      if (shell && extractScriptUrls(shell).length) html = shell;
    } catch {
      html = "";
    }
  }
  if (!html) {
    try {
      html = await session.pageSource();
    } catch {
      html = "";
    }
  }
  let urls = extractScriptUrls(html);
  if (typeof session.scriptUrls === "function") {
    try {
      const live = await session.scriptUrls();
      for (const url of live || []) {
        if (/https:\/\/abs\.twimg\.com\/responsive-web\/client-web\/.+\.js/.test(String(url)) && !urls.includes(url)) {
          urls.push(String(url));
        }
      }
    } catch {
      // The shell document is enough when its script tags are still there.
    }
  }
  urls = orderScriptUrls(urls);
  let bearer = extractWebBearer(html);
  let queryId = extractOperationQueryId(html, operationName);
  for (const url of urls) {
    if (queryId && bearer) break;
    let source = "";
    try {
      source = isPublicClientWeb(url)
        ? await (typeof session.fetchPublicJs === "function" ? session.fetchPublicJs(url) : fetchPublicJs(url))
        : await session.fetchText(url);
    } catch {
      continue;
    }
    if (!queryId) queryId = extractOperationQueryId(source, operationName);
    if (!bearer) bearer = extractWebBearer(source);
  }
  if (!queryId) return { queryId: capturedId, source: capturedSource, bearer, operation: operationName };
  return { queryId, source: "bundle", bearer, operation: operationName };
}

export function resolveCreateTweetQuery(session, override) {
  return resolveOperationQuery(session, "CreateTweet", override);
}

async function requireTransaction(session, path, config) {
  if (config.transactionId) return { id: config.transactionId, source: "flag" };
  const refused = "Refusing to post without x-client-transaction-id. Load https://x.com/i/jf/ in Ego until it includes twitter-site-verification, ondemand.s, and loading-x-anim, or pass --transaction-id from a real UI request.";
  if (typeof session.clientTransaction !== "function") {
    return { id: "", source: "missing", error: refused };
  }
  try {
    const raw = await session.clientTransaction({ method: "POST", path });
    if (raw && typeof raw === "object") {
      const id = String(raw.id || "");
      // A sniffed header from another GraphQL op is not a transaction id for this POST.
      if (!id || raw.source === "session") return { id: "", source: "missing", error: refused };
      return { id, source: "generated" };
    }
    const id = String(raw || "");
    if (!id) return { id: "", source: "missing", error: refused };
    return { id, source: "generated" };
  } catch (error) {
    const detail = error && error.message ? error.message : String(error);
    return { id: "", source: "missing", error: `${refused} ${detail}` };
  }
}

export async function performPost(config, session) {
  if (!config || !config.yes) return confirmationSummary(config || {});
  const imagePaths = Array.isArray(config.images) ? config.images : [];
  let prepared = [];
  if (imagePaths.length) {
    try {
      prepared = await describeImages(imagePaths);
    } catch (error) {
      return {
        ok: false,
        sent: false,
        exitCode: 1,
        error: error && error.message ? error.message : String(error),
      };
    }
  }
  await session.ensureSite();
  let detected = await session.detect();
  if (needsRepaint(detected)) {
    await session.goto(HOME_URL);
    detected = await session.detect();
  }
  const classified = classifyLogin(detected);
  const page = { url: detected.url, title: detected.title };
  if (!classified.logged_in) {
    if (config.keep) {
      try { await session.handOff(); } catch { /* handOff is optional */ }
    }
    return {
      ...loginStop("X login required in Ego Lite"),
      logged_in: false,
      login_required: true,
      on_login_page: classified.on_login_page,
      screen_name: classified.screen_name,
      page,
    };
  }
  const csrfToken = await session.csrfToken();
  if (!csrfToken) {
    if (config.keep) {
      try { await session.handOff(); } catch { /* handOff is optional */ }
    }
    return { ...loginStop("ct0 missing; sign in to x.com inside Ego Lite"), page };
  }
  const note = needsNoteTweet(config.text, { long: Boolean(config.long) });
  const operation = note ? "CreateNoteTweet" : "CreateTweet";
  const discovered = await resolveOperationQuery(session, operation, config.queryId);
  const url = graphqlUrl(discovered.queryId, operation);
  if (!url) {
    return {
      ok: false,
      sent: false,
      exitCode: 1,
      error: `${operation} query id is not usable`,
      query_id_source: discovered.source,
      operation,
      page,
    };
  }
  const language = normalizeLanguage(detected.lang);
  const pathname = new URL(url).pathname;
  const transaction = await requireTransaction(session, pathname, config);
  if (!transaction.id) {
    return {
      ok: false,
      sent: false,
      exitCode: 1,
      error: transaction.error,
      operation,
      note,
      transaction_id_source: "missing",
      query_id: discovered.queryId,
      query_id_source: discovered.source,
      page,
    };
  }
  if (note && typeof session.paceCompose === "function") {
    try {
      await session.paceCompose();
    } catch {
      // Opening the composer is pacing, not the post itself.
    }
  }
  let media = [];
  if (prepared.length) {
    if (typeof session.uploadImages !== "function") {
      return {
        ok: false,
        sent: false,
        exitCode: 1,
        error: "Image upload is unavailable in this session",
        operation,
        note,
        transaction_id_source: transaction.source,
        query_id: discovered.queryId,
        query_id_source: discovered.source,
        page,
      };
    }
    try {
      media = await session.uploadImages({
        images: prepared,
        bearer: discovered.bearer || PUBLIC_WEB_BEARER,
        csrfToken,
      });
    } catch (error) {
      if (error && error.loginRequired) {
        if (config.keep) {
          try { await session.handOff(); } catch { /* handOff is optional */ }
        }
        return { ...loginStop(error.message || "X login required in Ego Lite"), page };
      }
      return {
        ok: false,
        sent: false,
        exitCode: 1,
        error: `Image upload failed: ${error && error.message ? error.message : error}`,
        operation,
        note,
        transaction_id_source: transaction.source,
        query_id: discovered.queryId,
        query_id_source: discovered.source,
        page,
      };
    }
  }
  const headers = buildHeaders({ bearer: discovered.bearer, csrfToken, language, note });
  headers["x-client-transaction-id"] = transaction.id;
  const request = {
    url,
    headers,
    body: buildStatusBody({
      text: config.text,
      replyTo: config.replyTo,
      queryId: discovered.queryId,
      features: CAPTURED_FEATURES,
      note,
      mediaIds: media.map((item) => item.media_id),
    }),
  };
  const response = await session.postJson(request);
  const parsed = interpretCreateTweetResponse(response.status, response.body, {
    replyTo: config.replyTo,
    note,
    hadTransactionId: Boolean(transaction.id),
  });
  if (!parsed.ok) {
    if (parsed.loginRequired) return { ...loginStop(parsed.error), page, http_status: response.status };
    return {
      ok: false,
      sent: false,
      exitCode: 1,
      error: parsed.error,
      http_status: response.status || undefined,
      operation,
      note,
      transaction_id_source: transaction.source,
      query_id: discovered.queryId,
      query_id_source: discovered.source,
      reply_best_effort: Boolean(config.replyTo) || undefined,
      page,
    };
  }
  let screen = parsed.screenName;
  if (!isScreenName(screen) && typeof session.screenName === "function") {
    try {
      screen = screenNameFromPath(await session.screenName());
    } catch {
      screen = "";
    }
  }
  const status = statusUrl(screen, parsed.id);
  return {
    ok: true,
    sent: true,
    logged_in: true,
    login_required: false,
    exitCode: 0,
    url: status,
    status_id: parsed.id,
    screen_name: screen || undefined,
    operation,
    note: Boolean(parsed.note),
    full_text: parsed.fullText || undefined,
    transaction_id_source: transaction.source,
    query_id: discovered.queryId,
    query_id_source: discovered.source,
    media: media.length ? media : undefined,
    reply_best_effort: Boolean(config.replyTo) || undefined,
    warning: config.replyTo
      ? "Reply via page.fetch was not verified. A capture on 2026-11-04 returned GraphQL 226."
      : undefined,
    page,
  };
}

export async function executePost(config, { browser } = {}) {
  if (!config || !config.yes) return confirmationSummary(config || {});
  const summary = {
    skill: SKILL,
    command: "post",
    ok: false,
    sent: false,
    exitCode: 1,
    login_tip: LOGIN_TIP,
    login_tip_zh: LOGIN_TIP_ZH,
  };
  let session;
  try {
    session = await browser.open({
      taskName: config.taskName || SPACE_NAME,
      startUrl: HOME_URL,
      keepBrowser: Boolean(config.keep),
    });
    summary.spaceId = session.spaceId;
    Object.assign(summary, await performPost(config, session));
  } catch (error) {
    summary.error = String(error && error.message ? error.message : error);
    summary.exitCode = 1;
    summary.ok = false;
    summary.sent = false;
  } finally {
    if (session) {
      try {
        await session.finish();
      } catch (error) {
        summary.finish_error = String(error && error.message ? error.message : error);
      }
    }
  }
  return summary;
}

export async function executeCleanup(config, { browser } = {}) {
  let session;
  try {
    session = await browser.open({
      taskName: (config && config.taskName) || SPACE_NAME,
      keepBrowser: false,
    });
    await session.cleanup();
    return {
      skill: SKILL,
      command: "cleanup",
      ok: true,
      exitCode: 0,
      spaceId: session.spaceId,
      kept: [],
    };
  } catch (error) {
    return {
      skill: SKILL,
      command: "cleanup",
      ok: false,
      exitCode: 1,
      error: String(error && error.message ? error.message : error),
    };
  }
}
