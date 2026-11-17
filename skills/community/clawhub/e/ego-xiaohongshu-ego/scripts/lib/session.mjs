import {
  creatorAct,
  COVER_INPUT_SELECTOR,
  COVER_EDIT_ENTRY_SELECTOR,
  MAIN_COVER_CARD_SELECTOR,
  VIDEO_INPUT_SELECTOR,
} from "./creator-dom.mjs";
import {
  coverReplacedFirstFrame,
  editPageFailed,
  editSettled,
  mainCoverApplied,
  pickNote,
  publishButtonRef,
  publishSucceeded,
  uploadReady,
} from "./pure.mjs";

export function createCreatorSession({ task, page, pageName = "p1", keep = false, timings = {} } = {}) {
  if (!task || !page) throw new Error("createCreatorSession requires task and page");
  let finished = false;
  const uploadAttempts = timings.uploadAttempts ?? 40;
  const coverAttempts = timings.coverAttempts ?? 16;
  const imageTabAttempts = timings.imageTabAttempts ?? 10;
  const doneAttempts = timings.doneAttempts ?? 30;
  const closeAttempts = timings.closeAttempts ?? 20;
  const waitMs = timings.waitMs ?? 500;

  const finishWith = async (names) => {
    if (finished) return;
    finished = true;
    await task.finish({ keep: names });
  };

  async function evalAct(payload) {
    const result = await page.evaluate(creatorAct, payload);
    return result || { ok: false, error: "empty evaluate result" };
  }

  async function pause(ms) {
    if (ms && typeof page.waitForTimeout === "function") await page.waitForTimeout(ms);
  }

  return {
    spaceId: task.spaceId,
    async goto(url) {
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45_000 });
      try {
        if (typeof page.waitForLoadState === "function") {
          await page.waitForLoadState("networkidle", { timeout: 8_000 });
        }
      } catch {
        // The creator site keeps sockets open after the shell is ready.
      }
      if (typeof page.waitForTimeout === "function") await page.waitForTimeout(800);
    },
    async probe() {
      return evalAct({ op: "probe" });
    },
    async detect() {
      let url = "";
      let title = "";
      try { url = await page.url(); } catch { url = ""; }
      try { title = await page.title(); } catch { title = ""; }
      try {
        const probed = await this.probe();
        return {
          url: (probed && probed.url) || url,
          title: (probed && probed.title) || title,
          text: (probed && probed.text) || "",
          nickname: (probed && probed.nickname) || "",
          loginWall: Boolean(probed && probed.loginWall),
          creatorChrome: Boolean(probed && probed.creatorChrome),
          evaluateError: probed && probed.ok === false ? probed.error : "",
        };
      } catch (error) {
        return {
          url,
          title,
          text: "",
          nickname: "",
          loginWall: false,
          creatorChrome: false,
          evaluateError: String(error && error.message ? error.message : error),
        };
      }
    },
    async coverState() {
      const state = await evalAct({ op: "cover-state" });
      const count = state && typeof state.coverCount === "number" ? state.coverCount : null;
      return {
        pkApplied: Boolean(state && state.pkApplied),
        autoFilled: Boolean(state && state.autoFilled),
        coverCount: count,
        counterText: state && state.counterText ? String(state.counterText) : "",
        cropDialog: Boolean(state && state.cropDialog),
        previewSignature: state && state.previewSignature ? String(state.previewSignature) : "",
        previewText: state && state.previewText ? String(state.previewText) : "",
        text: state && state.text ? String(state.text) : "",
      };
    },
    async setInputFiles(selector, file) {
      if (typeof page.setInputFiles !== "function") throw new Error("page.setInputFiles is required");
      await page.setInputFiles(selector, file);
    },
    async setVideo(file) {
      const found = await evalAct({ op: "video-input" });
      if (!found.ok) throw new Error(found.error || "video file input not found");
      await this.setInputFiles(VIDEO_INPUT_SELECTOR, file);
      return found;
    },
    async switchToImageTab() {
      const clicked = await evalAct({ op: "image-tab" });
      if (!clicked.ok) throw new Error(clicked.error || "上传图文 tab not found");
      let found = null;
      for (let i = 0; i < imageTabAttempts; i += 1) {
        found = await evalAct({ op: "image-input" });
        if (found.ok) return { clicked, input: found };
        await pause(waitMs);
      }
      throw new Error(`image upload input did not appear after 上传图文: ${found && found.error ? found.error : "not found"}`);
    },
    async setImageFiles(files) {
      const found = await evalAct({ op: "image-input" });
      if (!found.ok) throw new Error(found.error || "image upload input not found");
      if (found.accept && String(found.accept).toLowerCase().includes(".mp4")) {
        throw new Error("refusing a video accept input for image upload");
      }
      const list = Array.isArray(files) ? files : [files];
      await this.setInputFiles(found.selector, list);
      return { ...found, files: list.length };
    },
    async imageState() {
      const state = await evalAct({ op: "image-state" });
      if (!state || state.ok === false) throw new Error((state && state.error) || "image state was not readable");
      return {
        uploadThumbs: Number(state.uploadThumbs) || 0,
        imgTotal: Number(state.imgTotal) || 0,
        counter: typeof state.counter === "number" ? state.counter : null,
        pending: Boolean(state.pending),
        failed: Boolean(state.failed),
        text: String(state.text || ""),
      };
    },
    async waitImagesReady(expected) {
      const want = Math.max(1, Number(expected) || 1);
      let last = null;
      for (let i = 0; i < uploadAttempts; i += 1) {
        last = await this.imageState();
        if (last.failed) {
          const error = new Error(`image upload failed on the page: ${last.text.slice(0, 200)}`);
          error.state = last;
          throw error;
        }
        const counted = Math.max(last.uploadThumbs, last.counter == null ? 0 : last.counter);
        if (!last.pending && counted >= want) return { ok: true, state: last };
        await pause(waitMs);
      }
      const error = new Error(`image upload did not settle: expected ${want} thumbnails, saw ${last ? last.uploadThumbs : 0} (pending=${last ? last.pending : "?"})`);
      error.state = last;
      throw error;
    },
    async clearAutoCovers() {
      let last = await this.coverState();
      for (let i = 0; i < 3; i += 1) {
        const count = typeof last.coverCount === "number" ? last.coverCount : 0;
        if (count <= 0 && !last.autoFilled) return last;
        const closed = await evalAct({ op: "close-pk-cover" });
        if (!closed.ok) {
          if (count <= 0) return last;
          throw new Error(closed.error || "PK cover close control not found");
        }
        await pause(waitMs);
        last = await this.coverState();
      }
      return last;
    },
    async mainCoverState() {
      const state = await evalAct({ op: "main-cover-state" });
      if (!state.ok && state.error) {
        return { signature: "", label: "", error: state.error, scope: "main" };
      }
      return {
        signature: state && state.signature ? String(state.signature) : "",
        label: state && state.label ? String(state.label) : "",
        scope: "main",
      };
    },
    // 2026-11-05: the main cover is set through the cover editor dialog.
    // Hover the 主封面 card to reveal 编辑封面, click it, upload into the
    // dialog's image input, wait for 完成 to enable, click it. The PK
    // swiper input is never touched.
    async setMainCover(file) {
      await this.openCoverEditor();
      await this.setDialogCover(file);
      await this.confirmCoverEditor();
      return { ok: true, via: "编辑封面", scope: "main" };
    },
    async openCoverEditor() {
      const editorAttempts = timings.editorAttempts ?? 4;
      const polls = timings.editorPolls ?? 8;
      const hoverMs = timings.hoverMs ?? 600;
      for (let attempt = 1; attempt <= editorAttempts; attempt += 1) {
        try {
          if (typeof page.hover === "function") {
            await page.hover(MAIN_COVER_CARD_SELECTOR);
            await pause(hoverMs);
          }
          if (typeof page.click === "function") {
            await page.click(COVER_EDIT_ENTRY_SELECTOR);
          }
        } catch {
          // The entry is hover-revealed; a zero-size box throws until the
          // overlay settles. The dialog poll below decides success.
        }
        for (let i = 0; i < polls; i += 1) {
          await pause(waitMs);
          const state = await evalAct({ op: "cover-editor-state" });
          if (state && state.dialogOpen) return { ok: true, attempts: attempt };
        }
        try {
          if (page.keyboard && typeof page.keyboard.press === "function") {
            await page.keyboard.press("Escape");
          }
        } catch {
          // best effort close of a half-open dialog before the next attempt
        }
        await pause(waitMs);
      }
      throw new Error("封面编辑器（编辑封面）没有打开");
    },
    async setDialogCover(file) {
      const found = await evalAct({ op: "dialog-cover-input" });
      if (!found.ok) throw new Error(found.error || "cover editor image input not found");
      await this.setInputFiles(found.selector, file);
      return found;
    },
    async confirmCoverEditor() {
      let last = null;
      for (let i = 0; i < doneAttempts; i += 1) {
        last = await evalAct({ op: "cover-editor-state" });
        if (last && last.doneFound && last.doneEnabled) break;
        await pause(waitMs);
      }
      if (!last || !last.doneFound || !last.doneEnabled) {
        const error = new Error("封面编辑器的 完成 按钮一直没有就绪（封面图未处理完成）");
        error.state = last;
        throw error;
      }
      const clicked = await evalAct({ op: "click-cover-editor-done" });
      if (!clicked.ok) throw new Error(clicked.error || "完成 click failed");
      for (let i = 0; i < closeAttempts; i += 1) {
        await pause(waitMs);
        const state = await evalAct({ op: "cover-editor-state" });
        if (state && !state.dialogOpen) return { ok: true, state };
      }
      throw new Error("封面编辑器在点 完成 后没有关闭");
    },
    async waitMainCover(before) {
      let last = null;
      for (let i = 0; i < coverAttempts; i += 1) {
        last = await this.mainCoverState();
        if (mainCoverApplied(before, last)) return { ok: true, state: last };
        await pause(waitMs);
      }
      const error = new Error("Main cover preview did not change after 编辑封面");
      error.state = last;
      throw error;
    },
    async setCover(file) {
      let found = await evalAct({ op: "cover-input" });
      if (!found.ok) {
        const revealed = await evalAct({ op: "reveal-cover" });
        if (revealed && revealed.ok) found = await evalAct({ op: "cover-input" });
      }
      if (!found.ok) throw new Error(found.error || "PK cover file input not found");
      await this.setInputFiles(COVER_INPUT_SELECTOR, file);
      return found;
    },
    async waitUpload() {
      let last = "";
      for (let i = 0; i < uploadAttempts; i += 1) {
        const probe = await this.probe();
        last = (probe && probe.text) || "";
        if (uploadReady(last)) return { ok: true, text: last };
        await pause(waitMs);
      }
      throw new Error("video upload did not finish");
    },
    async waitCoverApplied(before) {
      let last = null;
      for (let i = 0; i < coverAttempts; i += 1) {
        last = await this.coverState();
        if (coverReplacedFirstFrame(before, last)) return { ok: true, state: last };
        await pause(waitMs);
      }
      const error = new Error("PK cover was not confirmed (missing toast 「已添加 PK 封面」 or the counter did not advance, for example 0/3 → 1/3)");
      error.state = last;
      throw error;
    },
    async fillTitle(title) {
      const target = await evalAct({ op: "title-target" });
      if (!target.ok) throw new Error(target.error || "title field not found");
      if (typeof page.fill !== "function") throw new Error("page.fill is required for the title input");
      await page.fill(target.selector, title);
      const read = await evalAct({ op: "title-value" });
      if (!read.ok || read.value !== title) {
        throw new Error(`title readback mismatch: ${read && read.value != null ? read.value : read && read.error}`);
      }
      return read;
    },
    async fillBody(body) {
      const target = await evalAct({ op: "body-target" });
      if (!target.ok) throw new Error(target.error || "ProseMirror body not found");
      if (!page.keyboard || typeof page.keyboard.insertText !== "function") {
        throw new Error("page.keyboard.insertText is required for the ProseMirror body");
      }
      // After 编辑封面, a sticky <xhs-publish-btn> can intercept Playwright's
      // hit-target check on the ProseMirror editor. Focus via DOM instead of
      // page.click so insertText still lands in the body.
      if (typeof page.evaluate === "function") {
        const focused = await page.evaluate((selector) => {
          const el = document.querySelector(selector);
          if (!el) return { ok: false, error: "body selector missing" };
          try { el.scrollIntoView({ block: "center", inline: "nearest" }); } catch {}
          if (typeof el.focus === "function") el.focus();
          if (typeof el.click === "function") el.click();
          return { ok: true, active: document.activeElement === el || (el.contains && el.contains(document.activeElement)) };
        }, target.selector);
        if (!focused || !focused.ok) {
          throw new Error((focused && focused.error) || "body focus failed");
        }
      } else if (typeof page.click === "function") {
        await page.click(target.selector);
      } else {
        throw new Error("page.evaluate or page.click is required to focus the ProseMirror body");
      }
      // 2026-11-05: one insertText of the whole body turned every \n into
      // extra blank lines on the publish page. Write line by line and press
      // Enter between lines so ProseMirror splits paragraphs cleanly.
      const lines = String(body || "").split("\n");
      const hasEnter = typeof page.keyboard.press === "function";
      for (let i = 0; i < lines.length; i += 1) {
        if (i > 0) {
          if (hasEnter) await page.keyboard.press("Enter");
          else await page.keyboard.insertText("\n");
        }
        if (lines[i]) await page.keyboard.insertText(lines[i]);
      }
      const read = await evalAct({ op: "body-value" });
      // innerText renders every ProseMirror block as \n\n. Our writer also
      // presses Enter for blank lines in composeBody, so exact newline runs
      // diverge. Compare on content lines only.
      const normalize = (value) => String(value || "").replace(/\n+/g, "\n").trim();
      if (!read.ok || normalize(read.value) !== normalize(body)) {
        throw new Error(`description readback mismatch: ${read && read.value != null ? read.value : read && read.error}`);
      }
      return read;
    },
    async clickPublish(mode = "video") {
      if (mode === "image") return this.clickPublishImage();
      const result = await evalAct({ op: "click-publish" });
      if (result.ok) {
        if (typeof result.x === "number" && page.mouse && typeof page.mouse.click === "function") {
          await page.mouse.click(result.x, result.y);
          return result;
        }
        if (typeof page.click === "function" && result.selector) {
          await page.click(result.selector);
          return result;
        }
        throw new Error("发布 button was found but the page has no click API");
      }
      // 2026-11-05: the video 发布 button can sit in a closed shadow root, so
      // DOM matching finds nothing. Fall back to the a11y snapshot path that
      // image notes already use.
      if (typeof page.snapshot === "function") {
        const snap = await page.snapshot();
        const ref = publishButtonRef(snap);
        if (ref != null && typeof page.click === "function") {
          await page.click(`ref=${ref}`);
          return { ok: true, via: `ref=${ref}` };
        }
        if (typeof page.click === "function") {
          await page.click("loc=role:button[name='发布']");
          return { ok: true, via: "loc=role:button" };
        }
      }
      throw new Error(result.error || "发布 button not found");
    },
    // The image editor footer button lives in a closed shadow root. DOM
    // selectors cannot reach it; the accessibility snapshot names it as a
    // `button` whose exact text child is 发布. Click by snapshot ref.
    async clickPublishImage() {
      if (typeof page.snapshot !== "function") throw new Error("page.snapshot is required for the image-text 发布 button");
      const snap = await page.snapshot();
      const ref = publishButtonRef(snap);
      if (ref != null && typeof page.click === "function") {
        await page.click(`ref=${ref}`);
        return { ok: true, via: `ref=${ref}` };
      }
      if (typeof page.click === "function") {
        await page.click("loc=role:button[name='发布']");
        return { ok: true, via: "loc=role:button" };
      }
      throw new Error("发布 button was found in the snapshot but the page has no click API");
    },
    async waitEditSettled() {
      let last = { url: "", text: "" };
      for (let i = 0; i < uploadAttempts; i += 1) {
        let url = "";
        try { url = await page.url(); } catch { url = ""; }
        const probe = await this.probe();
        last = { url: (probe && probe.url) || url, text: (probe && probe.text) || "" };
        if (editPageFailed(last.text)) {
          const error = new Error("edit page shows 加载失败");
          error.state = last;
          throw error;
        }
        if (editSettled(last)) return { ok: true, url: last.url, text: last.text };
        await pause(waitMs);
      }
      throw new Error("edit publish did not settle");
    },
    async waitSuccess() {
      let lastUrl = "";
      let lastText = "";
      for (let i = 0; i < uploadAttempts; i += 1) {
        let url = "";
        try { url = await page.url(); } catch { url = ""; }
        const probe = await this.probe();
        lastUrl = (probe && probe.url) || url;
        lastText = (probe && probe.text) || "";
        if (publishSucceeded({ url: lastUrl, text: lastText })) return { ok: true, url: lastUrl, text: lastText };
        await pause(waitMs);
      }
      throw new Error("publish success page did not appear");
    },
    async readNote(title) {
      const result = await evalAct({ op: "note-cards" });
      if (!result.ok) throw new Error(result.error || "note cards were not readable");
      return pickNote(result.cards, title);
    },
    async handOff() {
      if (typeof task.handOff === "function") await task.handOff();
    },
    finish() {
      return finishWith(keep ? [pageName] : []);
    },
    cleanup() {
      return finishWith([]);
    },
  };
}
