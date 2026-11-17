// One Official Account article draft. Login and account checks happen before
// any editor write. --yes is the only path that clicks 保存.
import {
  decideAccount,
  decideSave,
  howToLogin,
  loginTip,
  normalizeText,
  planOf,
  validateReadback,
  figureSlotHtml,
  articleShell,
} from "./pure.mjs";
import { createReceiptStore } from "./prepare.mjs";

function base(command, extra = {}) {
  return { ok: false, command, saved: false, ...extra };
}

function accountFailure(command, decision) {
  const copy = decision.loginRequired ? howToLogin() : {};
  return base(command, {
    exitCode: decision.exitCode,
    login_required: Boolean(decision.loginRequired),
    account: decision.account || "",
    accounts: decision.accounts || [],
    reason: decision.reason,
    error: decision.reason,
    ...copy,
  });
}

async function compose(session, article) {
  await session.openEditor();
  await session.fillTitle(article.title);
  await session.fillOptional("set-digest", article.digest);
  await session.fillOptional("set-source", article.sourceUrl);
  const html = [];
  const images = [];
  for (const segment of article.segments) {
    if (segment.kind === "html") html.push(segment.html);
    if (segment.kind === "image") {
      html.push(figureSlotHtml(images.length, segment.captionHtml));
      images.push(segment);
    }
  }
  if (html.length) await session.pasteHtml(articleShell(html.join("")), images.map((_, index) => `WXIMG${index}`).join(" "));
  for (let index = 0; index < images.length; index += 1) {
    await session.replaceSlot(index, images[index].path);
  }
  const fixed = typeof session.applyReferenceFixes === "function" ? await session.applyReferenceFixes() : { ok: true };
  if (fixed && fixed.doubleRail) {
    const error = new Error("quote still has a grey rail beside the coral line");
    error.code = "quote";
    throw error;
  }
  await session.fillTitle(article.title);
  if (typeof session.stripRepeatedTitle === "function") await session.stripRepeatedTitle(article.title);
  const coverResult = await session.ensureCover();
  if (!coverResult.ok && !coverResult.retryAfterSave) {
    const error = new Error(coverResult.error || "cover was not set");
    error.code = "cover";
    throw error;
  }
  const readback = await session.readEditor();
  if (String(readback && readback.text || "").includes("WXIMG")) {
    throw new Error("image slot was not replaced");
  }
  if (typeof session.stripRepeatedTitle === "function") await session.stripRepeatedTitle(article.title);
  return { ...readback, coverPending: !coverResult.ok };
}

function draftRef(match) {
  if (!match) return { draftId: "", draftTime: "" };
  return { draftId: match.id || "", draftTime: match.time || "" };
}

export async function executeCheck(config, deps) {
  return run(config, deps, "check");
}

export async function executeSave(config, deps) {
  return run(config, deps, "save");
}

export async function executeCleanup(config, deps) {
  const browser = deps.browser;
  let spaces = [];
  try {
    const listed = await browser.listSpaces();
    spaces = Array.isArray(listed) ? listed : [];
  } catch (error) {
    return base("cleanup", { exitCode: 1, error: String(error.message || error) });
  }
  const matched = spaces.filter((space) => space && (
    space.name === "wechat-article-ego" || String(space.name || "").startsWith("wechat-article-ego-")
  ));
  const closed = [];
  for (const space of matched) {
    await browser.finishSpace(space);
    closed.push(space.id || space.name);
  }
  return { ok: true, exitCode: 0, command: "cleanup", saved: false, closed };
}

async function run(config, deps, command) {
  const store = deps.receipts || createReceiptStore(deps.fs);
  const now = deps.now || (() => new Date().toISOString());
  let session = null;
  try {
    session = await deps.browser.open({
      taskName: "wechat-article-ego",
      startUrl: "https://mp.weixin.qq.com/",
    });
    const probe = await session.probe();
    const account = decideAccount(probe, config.expectAccount || "");
    if (!account.ok) {
      const failure = accountFailure(command, account);
      if (command === "save" && config.article && config.article.hash) {
        failure.plan = planOf(config.article, "");
      }
      return failure;
    }
    const tip = loginTip(account.account);
    if (command === "check") {
      return {
        ok: true,
        exitCode: 0,
        command,
        saved: false,
        account: account.account,
        accounts: account.accounts,
        ...tip,
      };
    }
    const article = config.article;
    if (!article || !article.hash) {
      return base(command, { exitCode: 1, error: "article was not prepared", account: account.account });
    }
    const receipt = store.read(config.receiptDir, article.hash);
    let decision = decideSave({
      yes: Boolean(config.yes),
      receipt,
      draftsListed: false,
      hash: article.hash,
      title: article.title,
    });
    if (decision.action === "reconcile-first") {
      const drafts = await session.listDrafts();
      decision = decideSave({
        yes: true,
        receipt,
        drafts,
        draftsListed: true,
        hash: article.hash,
        title: article.title,
      });
    }
    const plan = planOf(article, account.account);
    if (!decision.save) {
      const ref = draftRef(decision.match || (decision.receipt && {
        id: decision.receipt.draftId,
        time: decision.receipt.draftTime,
      }));
      return {
        ok: decision.exitCode === 0 || decision.action === "dry-run",
        exitCode: decision.exitCode,
        command,
        action: decision.action,
        saved: false,
        duplicate: decision.action === "already-saved" || decision.action === "reconciled",
        account: account.account,
        accounts: account.accounts,
        plan,
        draftId: ref.draftId,
        draftTime: ref.draftTime,
        confirmation_required: decision.action === "dry-run",
        ...tip,
        ...(decision.action === "ambiguous-draft" ? { error: "ambiguous-draft", matches: decision.matches } : {}),
      };
    }
    const pending = {
      version: 1,
      hash: article.hash,
      title: article.title,
      account: account.account,
      status: "pending",
      startedAt: now(),
      imageCount: article.imageCount,
    };
    try {
      store.write(config.receiptDir, pending);
    } catch (error) {
      return base(command, {
        exitCode: 1,
        error: `cannot write receipt: ${error.message}`,
        account: account.account,
        plan,
      });
    }
    let readback;
    try {
      readback = await compose(session, article);
    } catch (error) {
      store.write(config.receiptDir, { ...pending, status: "aborted", error: String(error.message || error) });
      return base(command, {
        exitCode: 1,
        error: String(error.message || error),
        account: account.account,
        plan,
        saved: false,
      });
    }
    const check = validateReadback(article, readback);
    if (!check.ok) {
      store.write(config.receiptDir, { ...pending, status: "aborted", readback: check });
      return base(command, {
        exitCode: 1,
        error: `readback did not match the source (title=${readback && readback.title ? readback.title : ""}; missing=${(check.missing || []).slice(0, 2).join(" | ")})`,
        account: account.account,
        plan,
        readback: check,
        differences: check.missingHrefs,
      });
    }
    let saveClicked = false;
    try {
      await session.clickSave();
      saveClicked = true;
    } catch (error) {
      store.write(config.receiptDir, { ...pending, status: "aborted", error: String(error.message || error) });
      return base(command, { exitCode: 1, error: String(error.message || error), account: account.account, plan });
    }
    const confirmed = await session.saveConfirmed();
    let drafts = [];
    try {
      drafts = await session.listDrafts();
    } catch {
      drafts = [];
    }
    const want = normalizeText(article.title);
    const matches = drafts.filter((row) => row && normalizeText(row.title) === want);
    if (matches.length !== 1) {
      const uncertain = {
        ...pending,
        status: "uncertain",
        saveClicked,
        confirmed,
        finishedAt: now(),
      };
      store.write(config.receiptDir, uncertain);
      return base(command, {
        exitCode: 4,
        error: matches.length > 1 ? "ambiguous-draft" : "save outcome uncertain",
        account: account.account,
        plan,
        action: "uncertain",
        confirmed,
        matches,
      });
    }
    const match = matches[0] || {};
    const thumb = typeof session.coverThumb === "function"
      ? await session.coverThumb(want)
      : { filled: true, skipped: true };
    let coverThumb = thumb;
    if (!coverThumb.filled && typeof session.openDraftEditor === "function") {
      try {
        await session.openDraftEditor(want);
        const cover = await session.ensureCover();
        if (!cover.ok) {
          return base(command, {
            exitCode: 1,
            error: cover.error || "cover is empty after save",
            account: account.account,
            plan,
            saved: true,
            confirmed,
            cover: { filled: false, src: "" },
            draftId: match.id || "",
            draftTime: match.time || "",
          });
        }
        await session.clickSave();
        drafts = await session.listDrafts();
        coverThumb = await session.coverThumb(want);
      } catch (error) {
        return base(command, {
          exitCode: 1,
          error: String(error.message || error),
          account: account.account,
          plan,
          saved: true,
          confirmed,
          cover: { filled: false },
          draftId: match.id || "",
          draftTime: match.time || "",
        });
      }
    }
    if (!coverThumb.filled) {
      store.write(config.receiptDir, {
        ...pending,
        status: "uncertain",
        saveClicked,
        confirmed,
        finishedAt: now(),
        error: "cover is empty after save",
      });
      return base(command, {
        exitCode: 1,
        error: "cover is empty after save",
        account: account.account,
        plan,
        saved: true,
        confirmed,
        cover: { filled: false, src: coverThumb.src || "" },
        draftId: match.id || "",
        draftTime: match.time || "",
      });
    }
    const saved = {
      ...pending,
      status: "saved",
      savedAt: now(),
      draftId: match.id || "",
      draftTime: match.time || "",
      confirmed,
    };
    store.write(config.receiptDir, saved);
    let reopened = null;
    const shots = [];
    try {
      if (match.title) await session.openDraft(match.title);
      reopened = await session.readEditor();
      if (config.screenshotDir) {
        shots.push(...await session.captureViews(config.screenshotDir, "draft"));
        const preview = await session.openPreview();
        if (preview.ok) shots.push(...await session.captureViews(config.screenshotDir, "preview"));
      }
    } catch (error) {
      reopened = { warning: String(error.message || error) };
    }
    const again = reopened && reopened.title ? validateReadback(article, reopened) : null;
    return {
      ok: true,
      exitCode: 0,
      command,
      action: "saved",
      saved: true,
      account: account.account,
      title: article.title,
      hash: article.hash,
      draftId: saved.draftId,
      draftTime: saved.draftTime,
      imageCount: article.imageCount,
      cover: { filled: true, src: coverThumb.src || "" },
      fidelity: article.fidelity,
      differences: check.missingHrefs,
      readback: again || check,
      warning: reopened && reopened.warning ? reopened.warning : "",
      screenshots: shots,
      preview: shots.some((file) => String(file).includes("preview")),
      ...tip,
    };
  } catch (error) {
    return base(command, { exitCode: 1, error: String(error.message || error) });
  } finally {
    if (session) {
      try {
        await session.finish();
      } catch {
        // The result above is the source of truth; closing must not replace it.
      }
    }
  }
}
