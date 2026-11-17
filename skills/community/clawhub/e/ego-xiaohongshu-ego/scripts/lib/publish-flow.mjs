import { existsSync, statSync } from "node:fs";
import {
  CREATOR_HOME,
  EDIT_TASK,
  HOW_TO_LOGIN,
  HOW_TO_LOGIN_ZH,
  LOGIN_TIP,
  LOGIN_TIP_ZH,
  NOTE_MANAGER_URL,
  PUBLISH_TASK,
  PUBLISH_URL,
  SKILL,
  SPACE_PREFIX,
  assertCoverBeforePublish,
  cleanupTargets,
  confirmationSummary,
  editPageFailed,
  mainCoverApplied,
  exploreUrl,
  inputErrorSummary,
  planOf,
  postCommand,
  strip,
  updateUrl,
  validateEditInput,
  validatePostInput,
} from "./pure.mjs";
import { readGate } from "./run-check.mjs";

async function safeHandOff(session) {
  try {
    await session.handOff();
  } catch {
    // The exit code is what agents must honor.
  }
}

export async function applyCover(session, file) {
  let lastError = "main cover was not confirmed";
  for (let attempt = 1; attempt <= 2; attempt += 1) {
    try {
      const before = await session.mainCoverState();
      await session.setMainCover(file);
      const waited = await session.waitMainCover(before);
      const state = waited && waited.state ? waited.state : waited;
      if (mainCoverApplied(before, state)) {
        return {
          ok: true,
          attempts: attempt,
          state,
          replaced_first_frame: true,
          cover_scope: "main",
          via: "编辑封面",
        };
      }
      lastError = "main cover preview did not change";
    } catch (error) {
      lastError = String(error && error.message ? error.message : error);
    }
  }
  return {
    ok: false,
    attempts: 2,
    replaced_first_frame: false,
    cover_scope: "main",
    error: "Main cover was not confirmed after 编辑封面. Refusing to publish with the video first frame. PK slots are not used; they leave the thumbnail as the first frame until PK ends.",
    detail: lastError,
  };
}

function baseResult(config, checked, gate) {
  return {
    ok: false,
    published: false,
    uploaded: false,
    clicked_publish: false,
    cover_confirmed: false,
    replaced_first_frame: false,
    plan: planOf(config, checked, gate),
    nickname: gate && gate.nickname ? gate.nickname : undefined,
  };
}

export async function performPublish(config, session, checked) {
  const base = baseResult(config, checked);
  try {
    await session.goto(PUBLISH_URL);
  } catch (error) {
    return { ...base, exitCode: 1, error: String(error && error.message ? error.message : error) };
  }

  const gate = await readGate(session, config.expectAccount);
  base.nickname = gate.nickname || undefined;
  base.plan = planOf(config, checked, gate);
  if (gate.evaluateError) {
    return { ...base, exitCode: 1, error: gate.evaluateError };
  }
  if (!gate.logged_in) {
    if (config.keep) await safeHandOff(session);
    return strip({
      ...base,
      exitCode: 2,
      logged_in: false,
      login_required: true,
      on_login_page: gate.on_login_page,
      error: "Xiaohongshu creator login required in Ego Lite",
      how_to_login: HOW_TO_LOGIN,
      how_to_login_zh: HOW_TO_LOGIN_ZH,
    });
  }
  if (!gate.ok) {
    return strip({
      ...base,
      exitCode: 2,
      logged_in: true,
      account_mismatch: true,
      error: gate.error || "account mismatch",
      how_to_login: HOW_TO_LOGIN,
      how_to_login_zh: HOW_TO_LOGIN_ZH,
    });
  }

  try {
    if (checked.images && checked.images.length) {
      const tab = await session.switchToImageTab();
      base.image_input = tab.input;
      const upload = await session.setImageFiles(checked.images);
      base.uploaded = true;
      base.image_count = upload.files;
      await session.waitImagesReady(checked.images.length);
    } else {
      await session.setVideo(checked.video);
      base.uploaded = true;
      await session.waitUpload();
    }
  } catch (error) {
    return { ...base, exitCode: 1, error: String(error && error.message ? error.message : error) };
  }

  let coverConfirmed = !checked.cover;
  if (checked.cover) {
    const cover = await applyCover(session, checked.cover);
    base.cover_attempts = cover.attempts;
    if (!cover.ok || !cover.replaced_first_frame) {
      return {
        ...base,
        exitCode: 1,
        cover_confirmed: false,
        replaced_first_frame: false,
        error: cover.error || "Main cover was not confirmed after 编辑封面. Refusing to publish with the video first frame.",
      };
    }
    coverConfirmed = true;
    base.cover_confirmed = true;
    base.replaced_first_frame = true;
    base.cover_scope = cover.cover_scope || "main";
    base.cover_via = cover.via || "编辑封面";
  } else if (checked.images && checked.images.length) {
    coverConfirmed = true;
    base.cover_confirmed = true;
    base.cover_scope = "first-image";
  }

  try {
    await session.fillTitle(checked.title);
    await session.fillBody(checked.body);
  } catch (error) {
    return { ...base, exitCode: 1, error: String(error && error.message ? error.message : error) };
  }

  const again = await readGate(session, config.expectAccount);
  base.nickname = again.nickname || base.nickname;
  if (again.evaluateError) {
    return { ...base, exitCode: 1, error: again.evaluateError };
  }
  if (!again.logged_in || !again.ok) {
    if (config.keep && !again.logged_in) await safeHandOff(session);
    return strip({
      ...base,
      exitCode: 2,
      logged_in: Boolean(again.logged_in),
      account_mismatch: Boolean(again.account_mismatch),
      login_required: !again.logged_in || undefined,
      error: again.error || "Xiaohongshu creator login required before 发布",
      how_to_login: HOW_TO_LOGIN,
      how_to_login_zh: HOW_TO_LOGIN_ZH,
    });
  }

  const guard = assertCoverBeforePublish({ cover: checked.cover, coverConfirmed });
  if (!guard.ok) return { ...base, exitCode: 1, error: guard.error };

  const publishMode = checked.images && checked.images.length ? "image" : "video";
  try {
    await session.clickPublish(publishMode);
  } catch (error) {
    return {
      ...base,
      exitCode: 1,
      error: `点击发布失败: ${String(error && error.message ? error.message : error)}. Check note manager before retrying.`,
    };
  }
  base.clicked_publish = true;

  let success;
  try {
    success = await session.waitSuccess();
  } catch (error) {
    return {
      ...base,
      exitCode: 1,
      error: `${String(error && error.message ? error.message : error)}. 发布 was clicked; check note manager before retrying.`,
    };
  }

  try {
    await session.goto(NOTE_MANAGER_URL);
    const note = await session.readNote(checked.title);
    if (!note || !note.ok) {
      return {
        ...base,
        published: true,
        success_seen: true,
        success_url: success && success.url,
        exitCode: 1,
        error: `${note && note.error ? note.error : "note id missing"}. 发布成功 was seen; do not retry --yes or the note may be posted twice.`,
      };
    }
    return strip({
      ...base,
      ok: true,
      published: true,
      success_seen: true,
      exitCode: 0,
      note_id: note.noteId,
      url: note.url,
      error: undefined,
    });
  } catch (error) {
    return {
      ...base,
      published: true,
      success_seen: true,
      exitCode: 1,
      error: `${String(error && error.message ? error.message : error)}. 发布成功 was seen; do not retry --yes or the note may be posted twice.`,
    };
  }
}

export async function performEdit(config, session, checked) {
  const base = baseResult(config, checked);
  base.best_effort = true;
  base.note_id = checked.noteId;
  const target = updateUrl(checked.noteId);
  base.plan = planOf(config, checked);
  try {
    await session.goto(target);
  } catch (error) {
    return { ...base, exitCode: 1, error: String(error && error.message ? error.message : error) };
  }
  const gate = await readGate(session, config.expectAccount);
  base.nickname = gate.nickname || undefined;
  base.plan = planOf(config, checked, gate);
  if (gate.evaluateError) {
    return { ...base, exitCode: 1, error: gate.evaluateError };
  }
  if (!gate.logged_in) {
    if (config.keep) await safeHandOff(session);
    return strip({
      ...base,
      exitCode: 2,
      logged_in: false,
      login_required: true,
      error: "Xiaohongshu creator login required in Ego Lite",
      how_to_login: HOW_TO_LOGIN,
      how_to_login_zh: HOW_TO_LOGIN_ZH,
    });
  }
  if (!gate.ok) {
    return strip({
      ...base,
      exitCode: 2,
      logged_in: true,
      account_mismatch: true,
      error: gate.error || "account mismatch",
    });
  }
  let opened;
  try {
    opened = await session.probe();
  } catch (error) {
    return { ...base, exitCode: 1, error: String(error && error.message ? error.message : error) };
  }
  if (editPageFailed(opened && opened.text)) {
    return {
      ...base,
      exitCode: 1,
      clicked_publish: false,
      error: "Edit page failed to load (加载失败). The note may have left note manager. Cover was not changed. Prefer pre-publish --cover.",
    };
  }
  const cover = await applyCover(session, checked.cover);
  base.cover_attempts = cover.attempts;
  if (!cover.ok || !cover.replaced_first_frame) {
    return {
      ...base,
      exitCode: 1,
      cover_confirmed: false,
      error: cover.error || "Main cover was not confirmed after 编辑封面. Refusing to click 发布.",
    };
  }
  base.cover_confirmed = true;
  base.replaced_first_frame = true;
  base.cover_scope = cover.cover_scope || "main";
  base.cover_via = cover.via || "编辑封面";
  const again = await readGate(session, config.expectAccount);
  base.nickname = again.nickname || base.nickname;
  if (!again.logged_in || !again.ok) {
    if (config.keep && !again.logged_in) await safeHandOff(session);
    return strip({
      ...base,
      exitCode: 2,
      logged_in: Boolean(again.logged_in),
      account_mismatch: Boolean(again.account_mismatch),
      error: again.error || "Xiaohongshu creator login required before 发布",
    });
  }
  try {
    await session.clickPublish();
  } catch (error) {
    return {
      ...base,
      exitCode: 1,
      error: `点击发布失败: ${String(error && error.message ? error.message : error)}. Check the note before retrying. Edit is best-effort.`,
    };
  }
  base.clicked_publish = true;
  try {
    await session.waitEditSettled();
  } catch (error) {
    return {
      ...base,
      exitCode: 1,
      error: `${String(error && error.message ? error.message : error)}. 发布 was clicked; check the note before retrying. Edit may have returned it to 审核中.`,
    };
  }
  return strip({
    ...base,
    ok: true,
    published: true,
    exitCode: 0,
    url: exploreUrl(checked.noteId),
    warning: "Edit save may send the note back to 审核中 and show 封面PK中. Prefer --cover on the original publish.",
    error: undefined,
  });
}

export async function inspectOnly(config, session, checked) {
  const command = config.command || "post-video";
  const gate = await readGate(session, config.expectAccount);
  if (gate.evaluateError) {
    return strip({
      ...inputErrorSummary({ ...config, command }, { ...checked, error: gate.evaluateError, exitCode: 1 }),
      logged_in: false,
      plan: planOf(config, checked, gate),
    });
  }
  if (!gate.logged_in) {
    if (config.keep) await safeHandOff(session);
    return strip({
      skill: SKILL,
      command,
      ok: false,
      published: false,
      uploaded: false,
      clicked_publish: false,
      exitCode: 2,
      logged_in: false,
      login_required: true,
      on_login_page: gate.on_login_page,
      error: "Xiaohongshu creator login required in Ego Lite",
      how_to_login: HOW_TO_LOGIN,
      how_to_login_zh: HOW_TO_LOGIN_ZH,
      login_tip: LOGIN_TIP,
      login_tip_zh: LOGIN_TIP_ZH,
      plan: planOf(config, checked, gate),
    });
  }
  if (!gate.ok) {
    return strip({
      skill: SKILL,
      command,
      ok: false,
      published: false,
      uploaded: false,
      clicked_publish: false,
      best_effort: command === "edit-cover" || undefined,
      exitCode: 2,
      logged_in: true,
      account_mismatch: true,
      nickname: gate.nickname || undefined,
      error: gate.error || "account mismatch",
      how_to_login: HOW_TO_LOGIN,
      how_to_login_zh: HOW_TO_LOGIN_ZH,
      plan: planOf(config, checked, gate),
    });
  }
  return confirmationSummary(config, checked, gate);
}

export async function executePost(config = {}, deps = {}) {
  const exists = deps.existsSync || existsSync;
  const stat = deps.statSync || statSync;
  const checked = validatePostInput(config, { exists, stat });
  const command = postCommand(config);
  const request = { ...config, command };
  if (!checked.ok) return inputErrorSummary(request, checked);

  const summary = {
    skill: SKILL,
    command,
    ok: false,
    published: false,
    uploaded: false,
    clicked_publish: false,
    exitCode: 1,
    login_tip: LOGIN_TIP,
    login_tip_zh: LOGIN_TIP_ZH,
    links_removed: checked.links_removed && checked.links_removed.length ? checked.links_removed : undefined,
    plan: planOf(config, checked),
  };
  let session;
  try {
    if (!deps.browser || typeof deps.browser.open !== "function") throw new Error("browser is required");
    session = await deps.browser.open({
      taskName: request.taskName || PUBLISH_TASK,
      startUrl: request.yes ? PUBLISH_URL : CREATOR_HOME,
      keepBrowser: Boolean(request.keep),
    });
    summary.spaceId = session.spaceId;
    const result = request.yes
      ? await performPublish(request, session, checked)
      : await inspectOnly(request, session, checked);
    Object.assign(summary, result);
  } catch (error) {
    summary.error = String(error && error.message ? error.message : error);
    summary.exitCode = 1;
    summary.ok = false;
    summary.published = false;
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

export async function executeEdit(config = {}, deps = {}) {
  const request = { ...config, command: "edit-cover" };
  const exists = deps.existsSync || existsSync;
  const stat = deps.statSync || statSync;
  const checked = validateEditInput(request, { exists, stat });
  if (!checked.ok) return inputErrorSummary(request, checked);
  const summary = {
    skill: SKILL,
    command: "edit-cover",
    ok: false,
    best_effort: true,
    published: false,
    uploaded: false,
    clicked_publish: false,
    exitCode: 1,
    login_tip: LOGIN_TIP,
    login_tip_zh: LOGIN_TIP_ZH,
    plan: planOf(request, checked),
    note_id: checked.noteId,
  };
  let session;
  try {
    if (!deps.browser || typeof deps.browser.open !== "function") throw new Error("browser is required");
    session = await deps.browser.open({
      taskName: request.taskName || EDIT_TASK,
      startUrl: request.yes ? updateUrl(checked.noteId) : CREATOR_HOME,
      keepBrowser: Boolean(request.keep),
    });
    summary.spaceId = session.spaceId;
    const result = request.yes
      ? await performEdit(request, session, checked)
      : await inspectOnly(request, session, checked);
    Object.assign(summary, result);
  } catch (error) {
    summary.error = String(error && error.message ? error.message : error);
    summary.exitCode = 1;
    summary.ok = false;
    summary.published = false;
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

export async function executeCleanup(config = {}, { browser } = {}) {
  if (!browser || typeof browser.open !== "function") {
    return { skill: SKILL, command: "cleanup", ok: false, exitCode: 1, error: "browser is required" };
  }
  let listed = null;
  if (typeof browser.listSpaces === "function") {
    try {
      listed = await browser.listSpaces();
    } catch {
      listed = null;
    }
  }
  const names = cleanupTargets({
    listed,
    taskName: config && config.taskName,
    prefix: SPACE_PREFIX,
  });
  const closed = [];
  const errors = [];
  for (const name of names) {
    try {
      const session = await browser.open({ taskName: name, keepBrowser: false });
      if (typeof session.cleanup === "function") await session.cleanup();
      else await session.finish();
      closed.push(strip({ name, spaceId: session.spaceId }));
    } catch (error) {
      errors.push({ name, error: String(error && error.message ? error.message : error) });
    }
  }
  const ok = closed.length > 0 && errors.length === 0;
  return strip({
    skill: SKILL,
    command: "cleanup",
    ok,
    exitCode: ok ? 0 : 1,
    closed,
    kept: [],
    error: ok ? undefined : (errors[0] ? errors[0].error : "no spaces closed"),
    errors: errors.length ? errors : undefined,
  });
}
