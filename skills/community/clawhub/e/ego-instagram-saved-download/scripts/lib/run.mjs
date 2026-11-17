import {
  SAVED_URL,
  acceptPost,
  assertCdn,
  attachLoginCopy,
  domPosts,
  EXT,
  filesForPost,
  interpretSession,
  loginRequiredSummary,
  matchesQuery,
  outputName,
  parseSavedResponse,
  savedPath,
  sniffImage,
  sniffVideo,
} from "./pure.mjs";

async function publish(summary, fs, path) {
  if (!summary.outDir) return;
  await fs.mkdir(summary.outDir, { recursive: true });
  const manifest = path.join(summary.outDir, "manifest.json");
  summary.manifest = manifest;
  await fs.writeFile(manifest, JSON.stringify(summary, null, 2));
}

async function firstGood(session, urls, accept, maxBytes) {
  let last = "no candidate";
  for (const url of urls) {
    let got;
    try {
      assertCdn(url);
      got = await session.fetchBytes(url, { maxBytes });
    } catch (error) {
      last = String(error.message || error);
      continue;
    }
    if (accept(got, maxBytes)) return { ...got, url };
    if (got?.error) last = got.error;
    else if (got?.buf && maxBytes && got.buf.length > maxBytes) last = `larger than ${maxBytes} bytes`;
    else last = `HTTP ${got?.status || "error"}`;
  }
  throw new Error(last);
}

function acceptImage(got) {
  return Boolean(got?.ok && sniffImage(got.buf));
}

function acceptVideo(got, maxBytes) {
  if (!got?.ok || !got.buf || got.buf.length < 100 || got.buf.length > maxBytes) return false;
  return String(got.type || "").startsWith("video/") || sniffVideo(got.buf);
}

async function loadSaved(session, config) {
  const posts = [];
  const seen = new Set();
  let maxId;
  let pages = 0;
  for (let pageNo = 0; pageNo < config.maxPages && posts.length < config.limit; pageNo++) {
    pages += 1;
    const parsed = parseSavedResponse(await session.fetchJson(savedPath(maxId)));
    if (parsed.loginRequired) {
      const error = new Error(parsed.error || "login_required");
      error.loginRequired = true;
      throw error;
    }
    if (parsed.error) throw new Error(parsed.error);
    for (const post of parsed.posts) {
      const key = post.id || post.code || post.images?.[0]?.urls?.[0] || post.videos?.[0]?.urls?.[0];
      if (!key || seen.has(key)) continue;
      seen.add(key);
      if (!matchesQuery(post, config.query) || !acceptPost(post, config.media)) continue;
      posts.push(post);
      if (posts.length >= config.limit) break;
    }
    if (!parsed.nextMaxId) break;
    maxId = parsed.nextMaxId;
  }
  return { posts, pages };
}

export async function execute(config, deps) {
  const fs = deps.fs;
  const path = deps.path;
  const summary = attachLoginCopy({
    skill: "instagram-saved-download",
    command: "saved",
    ok: false,
    login_required: false,
    logged_in: false,
    query: config.query || null,
    limit: config.limit,
    outDir: config.outDir,
    media: config.media,
    method: null,
    spaceId: null,
    posts: [],
    downloads: [],
    failures: [],
    error: null,
    exitCode: 1,
  });
  let session = null;
  let dirReady = false;
  const ensureDir = async () => {
    if (dirReady || !config.outDir) return;
    await fs.mkdir(config.outDir, { recursive: true });
    dirReady = true;
  };
  try {
    session = await deps.browser.open({
      taskName: config.taskName,
      startUrl: SAVED_URL,
      keepBrowser: config.keepBrowser,
    });
    summary.spaceId = session.spaceId;
    const who = interpretSession(await session.detect());
    summary.logged_in = who.loggedIn;
    summary.signals = {
      password: who.password,
      inbox: who.inbox,
      saved: who.saved,
      ds_user: who.dsUser,
      login_url: who.loginUrl,
    };
    summary.page = { url: who.url, title: who.title };
    if (!who.loggedIn) {
      loginRequiredSummary(summary);
      return summary;
    }

    let posts = [];
    try {
      const loaded = await loadSaved(session, config);
      posts = loaded.posts;
      summary.pages = loaded.pages;
      summary.method = "feed/saved/posts";
    } catch (error) {
      if (error.loginRequired) {
        loginRequiredSummary(summary);
        summary.error = "Instagram asked for a login while reading Saved. Sign in once in Ego Lite. No password was entered.";
        return summary;
      }
      summary.failures.push({ stage: "feed/saved/posts", error: String(error.message || error) });
      if (!config.query && config.media !== "video") {
        posts = domPosts(await session.domImages(config.limit)).slice(0, config.limit);
        if (posts.length) summary.method = "dom";
      }
    }

    summary.posts = posts.map((post) => ({
      id: post.id,
      code: post.code,
      permalink: post.permalink,
      username: post.username,
      caption: post.caption,
      images: (post.images || []).length,
      videos: (post.videos || []).length,
    }));
    await ensureDir();
    for (let index = 0; index < posts.length; index++) {
      const post = posts[index];
      const files = filesForPost(post, config.media);
      for (let slide = 0; slide < files.length; slide++) {
        const file = files[slide];
        try {
          const maxBytes = file.kind === "video" ? config.maxVideoBytes : 20_000_000;
          const got = await firstGood(
            session,
            file.urls,
            file.kind === "video" ? acceptVideo : acceptImage,
            maxBytes,
          );
          const type = file.kind === "video" ? got.type || "video/mp4" : sniffImage(got.buf);
          const ext = file.kind === "video" ? "mp4" : EXT[type] || "jpg";
          const dest = path.join(config.outDir, outputName(index, slide, post.code, ext));
          await fs.writeFile(dest, got.buf);
          summary.downloads.push({
            n: String(index + 1).padStart(2, "0"),
            path: dest,
            url: got.url,
            bytes: got.buf.length,
            contentType: type,
            kind: file.kind,
            code: post.code,
          });
        } catch (error) {
          summary.failures.push({ code: post.code, kind: file.kind, error: String(error.message || error) });
        }
      }
    }

    summary.count = summary.downloads.length;
    summary.posts_saved = posts.length;
    summary.ok = summary.downloads.length > 0;
    summary.exitCode = summary.ok ? 0 : 1;
    if (!summary.ok) summary.error = summary.error || "No Saved media was saved.";
    return summary;
  } catch (error) {
    summary.ok = false;
    summary.error = String(error.message || error);
    summary.exitCode = 1;
    return summary;
  } finally {
    try {
      await publish(summary, fs, path);
    } catch {
      // stdout JSON remains the result when the directory cannot be written
    }
    if (session) {
      try {
        await session.finish();
      } catch (error) {
        summary.failures.push({ stage: "finish", error: String(error.message || error) });
      }
    }
  }
}
