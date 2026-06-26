const state = {
  settings: null,
  articles: [],
  selectedId: "",
  detail: null,
  coverPromptDraft: undefined,
  inlinePromptDrafts: {},
  activeView: "workbench",
  previewMode: "preview",
  lastSavedName: "wechat-preview.html",
  autoPreviewTimer: null,
  articleMenuOpen: false,
  articleInfoCollapsed: true,
  pendingSlotMoveId: "",
  editorSelection: null,
  editorSaveTimers: {},
  form: {
    tone: {
      theme: "",
      primaryColor: "#b3832f",
      saturation: 100,
      opacity: 88,
    },
    typography: {
      bodySize: 16,
      lineHeight: 1.9,
      paragraphGap: 16,
      sectionStyle: "editorial",
      imageRadius: 24,
      imageSpacing: 22,
    },
    coverCandidatePath: "",
  },
};

const refs = {
  importButton: document.getElementById("importButton"),
  markdownFileInput: document.getElementById("markdownFileInput"),
  uploadDropzone: document.getElementById("uploadDropzone"),
  articleCount: document.getElementById("articleCount"),
  articleSwitcherWrap: document.getElementById("articleSwitcherWrap"),
  articleSwitcherButton: document.getElementById("articleSwitcherButton"),
  articleSwitcherCurrent: document.getElementById("articleSwitcherCurrent"),
  articleSwitcherMenu: document.getElementById("articleSwitcherMenu"),
  detailEmptyState: document.getElementById("detailEmptyState"),
  detailWrap: document.getElementById("detailWrap"),
  workspaceBadge: document.getElementById("workspaceBadge"),
  detailTitle: document.getElementById("detailTitle"),
  detailSubtitle: document.getElementById("detailSubtitle"),
  articleInfoCard: document.getElementById("articleInfoCard"),
  articleInfoToggle: document.getElementById("articleInfoToggle"),
  articleInfoToggleLabel: document.getElementById("articleInfoToggleLabel"),
  articleInfoContent: document.getElementById("articleInfoContent"),
  infoAuthor: document.getElementById("infoAuthor"),
  infoChars: document.getElementById("infoChars"),
  infoPath: document.getElementById("infoPath"),
  infoUpdatedAt: document.getElementById("infoUpdatedAt"),
  sourcePath: document.getElementById("sourcePath"),
  doocsPath: document.getElementById("doocsPath"),
  packPath: document.getElementById("packPath"),
  infoSummary: document.getElementById("infoSummary"),
  sourceWarningPanel: document.getElementById("sourceWarningPanel"),
  sourceWarningList: document.getElementById("sourceWarningList"),
  generatePreviewButton: document.getElementById("generatePreviewButton"),
  themeSelect: document.getElementById("themeSelect"),
  themeHint: document.getElementById("themeHint"),
  primaryColorInput: document.getElementById("primaryColorInput"),
  primaryColorValue: document.getElementById("primaryColorValue"),
  saturationRange: document.getElementById("saturationRange"),
  saturationValue: document.getElementById("saturationValue"),
  opacityRange: document.getElementById("opacityRange"),
  opacityValue: document.getElementById("opacityValue"),
  generateCoverButton: document.getElementById("generateCoverButton"),
  coverResultCard: document.getElementById("coverResultCard"),
  coverResultMeta: document.getElementById("coverResultMeta"),
  coverResultImage: document.getElementById("coverResultImage"),
  coverResultPlaceholder: document.getElementById("coverResultPlaceholder"),
  coverResultPromptInput: document.getElementById("coverResultPromptInput"),
  coverResultPromptHelp: document.getElementById("coverResultPromptHelp"),
  selectCoverButton: document.getElementById("selectCoverButton"),
  deleteCoverButton: document.getElementById("deleteCoverButton"),
  coverHistoryGallery: document.getElementById("coverHistoryGallery"),
  generateInlineButton: document.getElementById("generateInlineButton"),
  inlineGallery: document.getElementById("inlineGallery"),
  coverCandidatePath: document.getElementById("coverCandidatePath"),
  pushDraftButton: document.getElementById("pushDraftButton"),
  draftStatusTitle: document.getElementById("draftStatusTitle"),
  draftStatusText: document.getElementById("draftStatusText"),
  previewModeButton: document.getElementById("previewModeButton"),
  copyHtmlButton: document.getElementById("copyHtmlButton"),
  saveHtmlButton: document.getElementById("saveHtmlButton"),
  previewCharCount: document.getElementById("previewCharCount"),
  previewKicker: document.getElementById("previewKicker"),
  previewTitle: document.getElementById("previewTitle"),
  previewFrame: document.getElementById("previewFrame"),
  editorView: document.getElementById("editorView"),
  editorSelectionToolbar: document.getElementById("editorSelectionToolbar"),
  editorHighlightButton: document.getElementById("editorHighlightButton"),
  editorDeleteButton: document.getElementById("editorDeleteButton"),
  editorInsertImageButton: document.getElementById("editorInsertImageButton"),
  workbenchView: document.getElementById("workbenchView"),
  settingsView: document.getElementById("settingsView"),
  wechatMode: document.getElementById("wechatMode"),
  wechatAppid: document.getElementById("wechatAppid"),
  wechatConfigured: document.getElementById("wechatConfigured"),
  configuredImageProvider: document.getElementById("configuredImageProvider"),
  configuredImageModel: document.getElementById("configuredImageModel"),
  configuredImageApiBase: document.getElementById("configuredImageApiBase"),
  effectiveImageProvider: document.getElementById("effectiveImageProvider"),
  effectiveImageModel: document.getElementById("effectiveImageModel"),
  effectiveImageApiBase: document.getElementById("effectiveImageApiBase"),
  imageConfigured: document.getElementById("imageConfigured"),
  imageModelSource: document.getElementById("imageModelSource"),
  settingsWorkspace: document.getElementById("settingsWorkspace"),
  settingsTheme: document.getElementById("settingsTheme"),
  settingsCover: document.getElementById("settingsCover"),
  toast: document.getElementById("toast"),
};

const LOCKED_THEME_ID = "winter-slate";
const LOCKED_THEME_LABEL = "OPC专用";
const LOCKED_THEME_DESCRIPTION = "当前固定使用 OPC 专用风格。";
const LOCKED_TEMPLATE_ID = "xiumi-winter-ins";
const LOCKED_TEMPLATE_LABEL = "OPC专属排版";
const LOCKED_TEMPLATE_DESCRIPTION = "当前固定使用 OPC 专属版式，自动关联主视觉、标题区和正文编排。";

function basename(path) {
  if (!path) return "";
  return String(path).split("/").pop() || path;
}

function formatCount(value) {
  return String(value || 0).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function sanitizeFilename(value) {
  return String(value || "wechat-preview")
    .trim()
    .replace(/[\\/:*?"<>|]+/g, "-")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "")
    .toLowerCase();
}

function assetUrl(item) {
  return item?.localPreviewUrl || item?.previewUrl || item?.draftUrl || "";
}

function escapeHtml(value) {
  return String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function normalizeAssetUrl(value) {
  const raw = String(value || "").trim();
  if (!raw) return "";
  try {
    const url = new URL(raw, window.location.href);
    return `${url.pathname}${url.search}`;
  } catch (_error) {
    return raw;
  }
}

function showToast(message) {
  refs.toast.textContent = message;
  refs.toast.classList.add("visible");
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => refs.toast.classList.remove("visible"), 2200);
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok || payload.success === false) {
    throw new Error(payload.error || payload.message || `请求失败：${response.status}`);
  }
  return payload;
}

function setButtonBusy(button, busy, idleLabel, busyLabel) {
  button.disabled = busy;
  button.textContent = busy ? busyLabel : idleLabel;
}

function renderSelect(select, items, currentValue, placeholder = "暂无可选项") {
  if (!items.length) {
    select.innerHTML = `<option value="">${placeholder}</option>`;
    select.disabled = true;
    return;
  }
  select.disabled = false;
  select.innerHTML = items.map((item) => `<option value="${item.value}">${item.label}</option>`).join("");
  select.value = items.some((item) => item.value === currentValue) ? currentValue : items[0].value;
}

function themeCatalog() {
  const items = Array.isArray(state.settings?.themes) ? state.settings.themes : [];
  const catalog = items.map((item) => (typeof item === "string" ? { id: item, label: item, description: "" } : item));
  const lockedTheme = catalog.find((item) => item.id === LOCKED_THEME_ID) || null;
  if (!lockedTheme) return catalog;
  return [
    {
      ...lockedTheme,
      label: LOCKED_THEME_LABEL,
      description: LOCKED_THEME_DESCRIPTION,
    },
  ];
}

function lockedTemplateMeta() {
  const items = Array.isArray(state.settings?.templates) ? state.settings.templates : [];
  const catalog = items.map((item) => (typeof item === "string" ? { id: item, label: item, description: "" } : item));
  const lockedTemplate = catalog.find((item) => item.id === LOCKED_TEMPLATE_ID) || null;
  if (!lockedTemplate) {
    return {
      id: LOCKED_TEMPLATE_ID,
      label: LOCKED_TEMPLATE_LABEL,
      description: LOCKED_TEMPLATE_DESCRIPTION,
    };
  }
  return {
    ...lockedTemplate,
    label: LOCKED_TEMPLATE_LABEL,
    description: lockedTemplate.description || LOCKED_TEMPLATE_DESCRIPTION,
  };
}

function sectionStyleCatalog() {
  const items = Array.isArray(state.settings?.sectionStyles) ? state.settings.sectionStyles : [];
  return items.map((item) => (typeof item === "string" ? { id: item, label: item, description: "" } : item));
}

function themeMeta(themeId) {
  return themeCatalog().find((item) => item.id === themeId) || null;
}

function templateMeta(templateId) {
  const lockedTemplate = lockedTemplateMeta();
  if (!templateId || templateId === lockedTemplate.id) return lockedTemplate;
  return null;
}

function sectionStyleMeta(styleId) {
  return sectionStyleCatalog().find((item) => item.id === styleId) || null;
}

function themeLabel(themeId) {
  if (!themeId) return "未设置";
  const lockedTheme = themeCatalog()[0];
  return lockedTheme?.label || themeMeta(themeId)?.label || themeId;
}

function themeDescription(themeId) {
  if (!themeId) return "";
  const lockedTheme = themeCatalog()[0];
  return lockedTheme?.description || themeMeta(themeId)?.description || "";
}

function templateLabel(templateId) {
  return templateMeta(templateId)?.label || templateId || LOCKED_TEMPLATE_LABEL;
}

function updateWorkspaceBadge() {
  if (!refs.workspaceBadge) return;
  const workspace = state.settings?.workspace || "";
  refs.workspaceBadge.textContent = workspace ? basename(workspace) : "当前工作区";
}

function updateRangeReadouts() {
  refs.primaryColorValue.textContent = refs.primaryColorInput.value;
  refs.saturationValue.textContent = `${refs.saturationRange.value}%`;
  refs.opacityValue.textContent = `${refs.opacityRange.value}%`;
}

function syncFormFromDetail() {
  if (!state.detail || !state.settings) return;
  const tone = state.detail.tone || {};
  const typography = state.detail.typography || {};
  const lockedTheme = themeCatalog()[0];
  state.form.tone = {
    theme: lockedTheme?.id || tone.theme || state.settings.defaultTheme || "elegant-gold",
    primaryColor: tone.primaryColor || "#b3832f",
    saturation: Number(tone.saturation || 100),
    opacity: Number(tone.opacity || 88),
  };
  state.form.typography = {
    bodySize: Number(typography.bodySize || 16),
    lineHeight: Number(typography.lineHeight || 1.9),
    paragraphGap: Number(typography.paragraphGap || 16),
    sectionStyle: typography.sectionStyle || "editorial",
    imageRadius: Number(typography.imageRadius || 24),
    imageSpacing: Number(typography.imageSpacing || 22),
  };
  state.form.coverCandidatePath = state.detail.images?.coverCandidatePath || "";

  renderSelect(
    refs.themeSelect,
    themeCatalog().map((item) => ({
      value: item.id,
      label: item.label,
    })),
    state.form.tone.theme,
    "暂无主题"
  );
  refs.themeHint.textContent = themeDescription(state.form.tone.theme) || "选择文章的整体气质基底。";
  refs.primaryColorInput.value = state.form.tone.primaryColor;
  refs.saturationRange.value = String(state.form.tone.saturation);
  refs.opacityRange.value = String(state.form.tone.opacity);
  refs.coverCandidatePath.value = state.form.coverCandidatePath;
  updateRangeReadouts();
}

function setArticleMenuOpen(open) {
  state.articleMenuOpen = Boolean(open) && Boolean(state.articles.length);
  refs.articleSwitcherButton.setAttribute("aria-expanded", state.articleMenuOpen ? "true" : "false");
  refs.articleSwitcherMenu.classList.toggle("hidden", !state.articleMenuOpen);
}

function renderArticleInfoCollapse() {
  const collapsed = Boolean(state.articleInfoCollapsed);
  refs.articleInfoCard.classList.toggle("is-collapsed", collapsed);
  refs.articleInfoToggle.setAttribute("aria-expanded", collapsed ? "false" : "true");
  refs.articleInfoToggle.setAttribute("aria-label", collapsed ? "展开文章信息" : "折叠文章信息");
  refs.articleInfoToggleLabel.textContent = collapsed ? "展开" : "收起";
  refs.articleInfoContent.classList.toggle("hidden", collapsed);
  refs.articleInfoContent.setAttribute("aria-hidden", collapsed ? "true" : "false");
}

function setArticleInfoCollapsed(collapsed) {
  state.articleInfoCollapsed = Boolean(collapsed);
  renderArticleInfoCollapse();
}

function renderArticleList() {
  const articles = state.articles || [];
  refs.articleCount.textContent = `${articles.length} 篇`;
  refs.articleSwitcherWrap.classList.toggle("hidden", articles.length === 0);
  refs.articleSwitcherMenu.innerHTML = "";
  if (!articles.length) {
    refs.articleSwitcherCurrent.textContent = "当前工作区暂无文章";
    refs.articleSwitcherButton.disabled = true;
    setArticleMenuOpen(false);
    return;
  }
  refs.articleSwitcherButton.disabled = false;
  const selectedArticle = articles.find((article) => article.id === state.selectedId) || articles[0];
  refs.articleSwitcherCurrent.textContent = selectedArticle?.title || "选择文章";

  articles.forEach((article, index) => {
    const row = document.createElement("div");
    row.className = "article-switcher-item";

    const selectButton = document.createElement("button");
    selectButton.className = `article-switcher-select${article.id === state.selectedId ? " active" : ""}`;
    selectButton.type = "button";
    selectButton.dataset.articleId = article.id;

    const title = document.createElement("strong");
    title.textContent = `${articles.length > 1 ? `${index + 1}. ` : ""}${article.title}`;
    const meta = document.createElement("span");
    meta.textContent = `${article.updatedAt || "未知时间"} · ${formatCount(article.charCount)} 字`;

    selectButton.appendChild(title);
    selectButton.appendChild(meta);

    const deleteButton = document.createElement("button");
    deleteButton.className = "secondary-btn danger small article-switcher-delete";
    deleteButton.type = "button";
    deleteButton.dataset.articleDeleteId = article.id;
    deleteButton.dataset.articleDeleteTitle = article.title || article.id;
    deleteButton.textContent = "删除";

    row.appendChild(selectButton);
    row.appendChild(deleteButton);
    refs.articleSwitcherMenu.appendChild(row);
  });
}

function renderArticleInfo(detail) {
  refs.detailTitle.textContent = detail.article.title;
  refs.detailSubtitle.textContent = detail.article.summary || "暂无摘要";
  refs.infoAuthor.textContent = detail.article.author || "未填写";
  refs.infoChars.textContent = `${formatCount(detail.article.charCount)} 字`;
  refs.infoPath.textContent = detail.article.path;
  refs.infoUpdatedAt.textContent = detail.article.updatedAt || "-";
  refs.sourcePath.textContent = detail.article.sourceFiles.source?.path || "-";
  refs.doocsPath.textContent = detail.article.sourceFiles.doocs.path;
  refs.packPath.textContent = detail.article.sourceFiles.publishPack.path;
  refs.infoSummary.textContent = detail.article.summary || "暂无摘要";
}

function renderWarnings(detail) {
  const warnings = Array.isArray(detail.source?.warnings) ? detail.source.warnings : [];
  refs.sourceWarningPanel.classList.toggle("hidden", warnings.length === 0);
  refs.sourceWarningList.innerHTML = "";
  warnings.forEach((warning) => {
    const item = document.createElement("div");
    item.className = "warning-item";
    item.textContent = warning;
    refs.sourceWarningList.appendChild(item);
  });
}

function renderVisualStatus(detail) {
}

function renderPathDisclosure(path) {
  const value = path || "未保存";
  return `
    <details class="path-disclosure">
      <summary>本地路径</summary>
      <code>${escapeHtml(value)}</code>
    </details>
  `;
}

function inlinePromptValue(item) {
  const slotId = String(item?.slotId || "");
  if (slotId && Object.prototype.hasOwnProperty.call(state.inlinePromptDrafts, slotId)) {
    return state.inlinePromptDrafts[slotId];
  }
  return item?.prompt || item?.currentItem?.promptOverride || item?.currentItem?.style || "";
}

function coverPromptValue(item) {
  if (state.coverPromptDraft !== undefined) {
    return state.coverPromptDraft;
  }
  return item?.promptOverride || item?.prompt || item?.style || "";
}

function renderCover(detail) {
  const generated = detail.images?.coverGenerated;
  const draft = detail.images?.coverDraft || null;
  const history = detail.images?.coverHistory || [];
  const candidatePath = detail.images?.coverCandidatePath || "";
  refs.coverCandidatePath.value = candidatePath;
  state.form.coverCandidatePath = candidatePath;

  const hasGenerated = Boolean(assetUrl(generated));
  const generatedHasCustomPrompt = Boolean(
    String(generated?.promptOverride || generated?.customPrompt || "").trim()
  );
  const promptSource = generatedHasCustomPrompt ? (generated || draft || null) : (draft || generated || null);

  if (!promptSource) {
    refs.coverResultCard.classList.add("hidden");
  } else {
    refs.coverResultCard.classList.remove("hidden");
    const promptValue = coverPromptValue(promptSource);
    refs.coverResultImage.classList.toggle("hidden", !hasGenerated);
    refs.coverResultPlaceholder.classList.toggle("hidden", hasGenerated);
    if (hasGenerated) {
      refs.coverResultImage.src = assetUrl(generated);
    } else {
      refs.coverResultImage.removeAttribute("src");
    }
    refs.coverResultMeta.textContent = "";
    refs.coverResultPromptInput.value = promptValue;
    refs.coverResultPromptInput.dataset.promptBaseline = promptSource.promptOverride || promptSource.prompt || promptSource.style || "";
    refs.coverResultPromptInput.dataset.coverStyleId = promptSource.styleId || generated?.styleId || draft?.styleId || "";
    refs.coverResultPromptHelp.textContent = hasGenerated
      ? (generated.localPath ? `本地路径：${generated.localPath}` : "当前封面还没有本地路径。")
      : "这是系统自动生成的默认封面配图 Prompt；如果要微调，只补充画面意象再点上方 generate。";
    refs.selectCoverButton.dataset.coverPath = hasGenerated ? (generated.localPath || "") : "";
    refs.deleteCoverButton.dataset.deleteCoverPath = hasGenerated ? (generated.localPath || "") : "";
    refs.selectCoverButton.disabled = !hasGenerated;
    refs.deleteCoverButton.disabled = !hasGenerated;
  }

  refs.coverHistoryGallery.innerHTML = "";
  const historyItems = history.filter((item) => item?.localPath);
  if (!historyItems.length) {
    refs.coverHistoryGallery.innerHTML = '<div class="history-empty">还没有封面候选。导入后或点击“generate”会自动生成 4 张核心封面。</div>';
    return;
  }
  historyItems.forEach((item, index) => {
    const card = document.createElement("article");
    card.className = "history-card";
    const isCurrent = item.localPath === candidatePath;
    card.innerHTML = `
      <div class="history-card-head">
        <div>
          <strong>${item.styleLabel || `封面候选 ${index + 1}`}</strong>
          <span>${item.createdAt || "未知时间"}</span>
        </div>
        <span class="list-chip ${isCurrent ? "success" : ""}">${isCurrent ? "当前封面" : (item.preset || "cover")}</span>
      </div>
      ${assetUrl(item) ? `<img src="${assetUrl(item)}" alt="${item.styleLabel || "封面候选"}" />` : ""}
      ${renderPathDisclosure(item.localPath)}
      <div class="history-actions">
        <button class="secondary-btn small" type="button" data-cover-path="${item.localPath || ""}" ${isCurrent ? "disabled" : ""}>${isCurrent ? "当前已使用" : "设为当前封面"}</button>
        <button class="secondary-btn danger small image-delete-btn" type="button" data-delete-cover-path="${item.localPath || ""}">删除</button>
      </div>
    `;
    refs.coverHistoryGallery.appendChild(card);
  });
}

function renderInlineImages(detail) {
  const items = detail.editor?.imageSlots || detail.images?.inlineSlots || [];
  refs.inlineGallery.innerHTML = "";
  if (!items.length) {
    refs.inlineGallery.innerHTML = '<div class="inline-empty">还没有插图位。先在右侧编辑区把光标放到正文中，再插入插图位。</div>';
  } else {
    items.forEach((item) => {
      const promptValue = inlinePromptValue(item);
      const currentItem = item.currentItem || null;
      const slotId = String(item.slotId || "");
      const historyItems = Array.isArray(item.history) ? item.history : [];
      const card = document.createElement("article");
      card.className = "inline-card";
      card.dataset.inlineCardSlot = slotId;
      const currentImage = currentItem ? assetUrl(currentItem) : "";
      const historyMarkup = historyItems.length
        ? historyItems
            .map((historyItem, index) => {
              const isCurrent = currentItem?.localPath && historyItem.localPath === currentItem.localPath;
              return `
                <article class="mini-history-card">
                  ${assetUrl(historyItem) ? `<img src="${assetUrl(historyItem)}" alt="${escapeHtml(historyItem.label || `历史插图 ${index + 1}`)}" />` : ""}
                  <div class="mini-history-meta">
                    <strong>${escapeHtml(historyItem.label || `历史插图 ${index + 1}`)}</strong>
                    <span>${escapeHtml(historyItem.createdAt || "未知时间")}</span>
                  </div>
                  <div class="history-actions">
                    <button class="secondary-btn small" type="button" data-inline-slot-id="${slotId}" data-inline-path="${historyItem.localPath || ""}" ${isCurrent ? "disabled" : ""}>${isCurrent ? "当前已用" : "切换"}</button>
                    <button class="secondary-btn danger small image-delete-btn" type="button" data-delete-inline-path="${historyItem.localPath || ""}">删除</button>
                  </div>
                </article>
              `;
            })
            .join("")
        : '<div class="history-empty">这张插图位还没有历史图。</div>';
      card.innerHTML = `
      <div class="inline-card-head">
        <div>
          <strong>插图 ${item.order}</strong>
          <span>${item.anchorPreviewText || "未定位到正文上下文"}</span>
        </div>
        <div class="inline-slot-actions">
          <button class="secondary-btn small" type="button" data-inline-move-slot="${slotId}">改位置</button>
          <button class="secondary-btn danger small" type="button" data-inline-delete-slot="${slotId}">删除插图位</button>
          <button class="secondary-btn small" type="button" data-inline-regenerate="${slotId}">generate</button>
        </div>
      </div>
        <div class="inline-card-meta">${item.anchorPreviewText ? `插入位置：${escapeHtml(item.anchorPreviewText)}` : "还没有正文位置。"}</div>
        ${currentImage ? `<img src="${currentImage}" alt="${escapeHtml(item.anchorPreviewText || `插图 ${item.order}`)}" />` : '<div class="inline-image-empty">这个插图位还没有生成图片。</div>'}
        <div class="generated-prompt-editor">
          <label class="generated-prompt-label" for="inlinePromptEditor-${slotId}">配图 Prompt</label>
          <textarea
            class="generated-prompt-input"
            id="inlinePromptEditor-${slotId}"
            data-inline-prompt-slot="${slotId}"
            rows="12"
            placeholder="这里可以直接修改这张图的配图 Prompt，然后点 generate。"
          >${escapeHtml(promptValue)}</textarea>
          <p class="generated-prompt-help">${state.pendingSlotMoveId === slotId ? "正在等待你在右侧编辑区重新选择新的插图位置。" : "修改后点 generate，会优先按这张图自己的配图 Prompt 出图。"}</p>
        </div>
        ${currentItem?.localPath ? renderPathDisclosure(currentItem.localPath) : ""}
        <div class="inline-history-stack">
          <strong class="inline-history-title">历史图</strong>
          <div class="mini-history-grid">
            ${historyMarkup}
          </div>
        </div>
      `;
      refs.inlineGallery.appendChild(card);
    });
  }
}

function renderDraft(detail) {
  const draft = detail.draft || {};
  const hasDraft = Boolean(draft.mediaId);
  refs.draftStatusTitle.textContent = hasDraft ? "已推送到草稿箱" : "尚未推送";
  refs.draftStatusText.textContent = hasDraft
    ? `最近一次推送时间：${draft.pushedAt || "未知"}。media_id：${draft.mediaId}`
    : draft.lastError || "确认预览、封面和正文配图后，再推送到微信草稿箱。";
}

function previewPlaceholderHtml(title, message) {
  const safeTitle = String(title || "等待预览")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
  const safeMessage = String(message || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
  return `<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <style>
      body {
        margin: 0;
        min-height: 100vh;
        display: grid;
        place-items: center;
        padding: 40px 24px;
        background: linear-gradient(180deg, #fffdfa 0%, #f7efe5 100%);
        color: #4c4035;
        font: 16px/1.7 "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      }
      .empty {
        width: min(560px, 100%);
        padding: 28px;
        border: 1px solid rgba(235, 224, 208, 0.9);
        border-radius: 28px;
        background: rgba(255, 255, 255, 0.92);
        box-shadow: 0 18px 44px rgba(110, 77, 36, 0.10);
      }
      h1 {
        margin: 0 0 12px;
        font-size: 28px;
      }
      p {
        margin: 0;
      }
    </style>
  </head>
  <body>
    <section class="empty">
      <h1>${safeTitle}</h1>
      <p>${safeMessage}</p>
    </section>
  </body>
</html>`;
}

function renderPreview(detail) {
  const preview = detail.preview || {};
  const ready = Boolean(preview.ready);
  const title = preview.title || detail.article.title;
  const previewMessage = preview.statusText || "先调整风格和配色，再手动生成预览。";
  refs.previewTitle.textContent = title;
  refs.previewCharCount.textContent = formatCount(preview.charCount || detail.article.charCount || 0);
  refs.previewKicker.textContent = ready ? "微信发布预览" : "预览待生成";
  refs.previewFrame.srcdoc = ready
    ? (preview.standaloneHtml || "")
    : previewPlaceholderHtml(title, previewMessage);
  renderEditorView(detail);
  refs.previewModeButton.disabled = !(detail.editor?.blocks || []).length;
  refs.copyHtmlButton.disabled = !ready;
  refs.saveHtmlButton.disabled = !ready;
  state.lastSavedName = `${sanitizeFilename(title)}.html`;
  if (!(detail.editor?.blocks || []).length && state.previewMode === "edit") {
    state.previewMode = "preview";
  }
  renderPreviewMode();
}

function renderPreviewMode() {
  const isEdit = state.previewMode === "edit";
  refs.previewModeButton.textContent = isEdit ? "预览" : "编辑";
  refs.previewFrame.classList.toggle("hidden", isEdit);
  refs.editorView.classList.toggle("hidden", !isEdit);
  if (!isEdit) {
    hideEditorToolbar();
  }
}

function resizePreviewFrame() {
  setTimeout(() => {
    try {
      const doc = refs.previewFrame.contentDocument;
      if (!doc) return;
      const height = Math.max(doc.body?.scrollHeight || 0, doc.documentElement?.scrollHeight || 0, 1100);
      refs.previewFrame.style.height = `${Math.min(height + 24, 24000)}px`;
      enhancePreviewInlineEditors(doc);
    } catch (_error) {
      refs.previewFrame.style.height = "1800px";
    }
  }, 80);
}

function focusInlineEditor(slotId) {
  const card = refs.inlineGallery.querySelector(`[data-inline-card-slot="${slotId}"]`);
  if (!card) {
    showToast("没找到这个插图位的编辑卡片");
    return;
  }
  card.scrollIntoView({ behavior: "smooth", block: "center" });
  card.classList.remove("is-focused");
  void card.offsetWidth;
  card.classList.add("is-focused");
  clearTimeout(card.highlightTimer);
  card.highlightTimer = setTimeout(() => card.classList.remove("is-focused"), 2200);
  const promptInput = card.querySelector(`[data-inline-prompt-slot="${slotId}"]`);
  if (promptInput) {
    promptInput.focus({ preventScroll: true });
    promptInput.setSelectionRange?.(promptInput.value.length, promptInput.value.length);
    return;
  }
  const actionButton =
    card.querySelector(`[data-inline-regenerate="${slotId}"]`) ||
    card.querySelector("[data-delete-inline-path]") ||
    card.querySelector("button");
  if (actionButton) {
    actionButton.focus({ preventScroll: true });
  }
}

function editorBlocks(detail = state.detail) {
  return Array.isArray(detail?.editor?.blocks) ? detail.editor.blocks : [];
}

function editorSlots(detail = state.detail) {
  return Array.isArray(detail?.editor?.imageSlots) ? detail.editor.imageSlots : [];
}

function hideEditorToolbar() {
  state.editorSelection = null;
  refs.editorSelectionToolbar.classList.add("hidden");
}

function selectionOffsetsWithinElement(element) {
  const selection = window.getSelection();
  if (!selection || !selection.rangeCount) return null;
  const range = selection.getRangeAt(0);
  if (!element.contains(range.startContainer) || !element.contains(range.endContainer)) return null;
  const preStart = range.cloneRange();
  preStart.selectNodeContents(element);
  preStart.setEnd(range.startContainer, range.startOffset);
  const preEnd = range.cloneRange();
  preEnd.selectNodeContents(element);
  preEnd.setEnd(range.endContainer, range.endOffset);
  return {
    blockId: element.dataset.blockId || "",
    start: preStart.toString().length,
    end: preEnd.toString().length,
    collapsed: range.collapsed,
    rect: range.getBoundingClientRect(),
    elementRect: element.getBoundingClientRect(),
  };
}

function serializeEditorNode(node) {
  if (!node) return "";
  if (node.nodeType === Node.TEXT_NODE) {
    return node.textContent || "";
  }
  if (node.nodeType !== Node.ELEMENT_NODE) {
    return "";
  }
  if (node.tagName === "BR") {
    return " ";
  }
  const childrenText = Array.from(node.childNodes || []).map((child) => serializeEditorNode(child)).join("");
  if (node.classList?.contains("editor-theme-highlight")) {
    return `**${childrenText}**`;
  }
  return childrenText;
}

function serializeEditorBlockContent(element) {
  if (!element) return "";
  return Array.from(element.childNodes || [])
    .map((child) => serializeEditorNode(child))
    .join("")
    .replace(/\u00a0/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function cleanupEditorBlockHighlights(element) {
  if (!element) return;
  element.querySelectorAll(".editor-theme-highlight .editor-theme-highlight").forEach((highlight) => {
    const fragment = document.createDocumentFragment();
    while (highlight.firstChild) {
      fragment.appendChild(highlight.firstChild);
    }
    highlight.replaceWith(fragment);
  });
  element.querySelectorAll(".editor-theme-highlight").forEach((highlight) => {
    while (
      highlight.nextSibling &&
      highlight.nextSibling.nodeType === Node.ELEMENT_NODE &&
      highlight.nextSibling.classList?.contains("editor-theme-highlight")
    ) {
      const nextHighlight = highlight.nextSibling;
      while (nextHighlight.firstChild) {
        highlight.appendChild(nextHighlight.firstChild);
      }
      nextHighlight.remove();
    }
    if (!highlight.textContent?.trim()) {
      highlight.remove();
    }
  });
  element.normalize();
}

function currentEditorRange() {
  const selection = window.getSelection();
  if (!selection || !selection.rangeCount) return null;
  const range = selection.getRangeAt(0);
  const block = range.commonAncestorContainer?.nodeType === Node.ELEMENT_NODE
    ? range.commonAncestorContainer.closest?.("[data-editor-text-block='true']")
    : range.commonAncestorContainer?.parentElement?.closest?.("[data-editor-text-block='true']");
  if (!block || !refs.editorView.contains(block)) return null;
  if (!block.contains(range.startContainer) || !block.contains(range.endContainer)) return null;
  return { selection, range, block };
}

function updateEditorInsertButtonLabel() {
  refs.editorInsertImageButton.textContent = state.pendingSlotMoveId ? "移动插图位" : "插入插图位";
}

function updateEditorSelectionToolbar() {
  updateEditorInsertButtonLabel();
  if (state.previewMode !== "edit") {
    hideEditorToolbar();
    return;
  }
  const selection = window.getSelection();
  if (!selection || !selection.rangeCount) {
    hideEditorToolbar();
    return;
  }
  const block = selection.anchorNode?.parentElement?.closest?.("[data-editor-text-block='true']");
  if (!block || !refs.editorView.contains(block)) {
    hideEditorToolbar();
    return;
  }
  const offsets = selectionOffsetsWithinElement(block);
  if (!offsets || !offsets.blockId) {
    hideEditorToolbar();
    return;
  }
  state.editorSelection = offsets;
  refs.editorHighlightButton.disabled = offsets.collapsed;
  refs.editorDeleteButton.disabled = offsets.collapsed;
  const rect = offsets.rect && (offsets.rect.width || offsets.rect.height) ? offsets.rect : offsets.elementRect;
  refs.editorSelectionToolbar.style.left = `${Math.max(18, rect.left + rect.width / 2)}px`;
  refs.editorSelectionToolbar.style.top = `${Math.max(18, rect.top + window.scrollY - 54)}px`;
  refs.editorSelectionToolbar.classList.remove("hidden");
}

function editorCoverAsset(detail) {
  return detail?.images?.coverModuleCurrent || detail?.images?.coverModule || detail?.images?.coverGenerated || null;
}

function editorSummary(detail) {
  return detail?.preview?.summary || detail?.article?.summary || "暂无摘要";
}

function editorYear(detail) {
  const updatedAt = String(detail?.article?.updatedAt || "").trim();
  const matched = updatedAt.match(/\b(20\d{2})\b/);
  return matched?.[1] || String(new Date().getFullYear());
}

function renderEditorHero(detail) {
  const cover = editorCoverAsset(detail);
  const coverUrl = assetUrl(cover);
  const title = escapeHtml(detail?.article?.title || "未命名文章");
  const summary = escapeHtml(editorSummary(detail));
  const year = escapeHtml(editorYear(detail));
  const section = document.createElement("section");
  section.className = "editor-hero";
  section.innerHTML = `
    <div class="editor-hero-kicker">&nbsp;<span>&nbsp;</span></div>
    <div class="editor-hero-strip">
      <span>&nbsp;</span>
      <span>&nbsp;</span>
    </div>
    <div class="editor-hero-center">
      <span class="editor-hero-year">${year}</span>
      <p class="editor-hero-title"><span>|</span> ${title} <span>|</span></p>
      <p class="editor-hero-summary">${summary}</p>
    </div>
    <div class="editor-hero-cover-shell">
      <div class="editor-hero-cover-frame">
        <div class="editor-hero-cover-card">
          <div class="editor-hero-cover-media">
            ${coverUrl ? `<img src="${coverUrl}" alt="${title}" />` : '<div class="editor-hero-cover-placeholder">当前还没有封面图</div>'}
          </div>
          <p class="editor-hero-cover-text">${summary}</p>
        </div>
      </div>
    </div>
  `;
  return section;
}

function renderEditorListBlock(block) {
  const items = Array.isArray(block?.items) ? block.items : [];
  const ordered = Boolean(block?.ordered);
  const list = document.createElement(ordered ? "ol" : "ul");
  list.className = `editor-list-block${ordered ? " is-ordered" : ""}`;
  items.forEach((item, index) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span class="editor-list-badge">${ordered ? index + 1 : "•"}</span>
      <span>${escapeHtml(item)}</span>
    `;
    list.appendChild(li);
  });
  return list;
}

function renderEditorImageSlotBlock(detail, block) {
  const slot = editorSlots(detail).find((item) => item.slotId === block.slotId);
  const currentItem = slot?.currentItem || null;
  const currentImage = currentItem ? assetUrl(currentItem) : "";
  const slotId = String(block.slotId || "");
  const label = escapeHtml(slot?.anchorPreviewText || `插图位 ${slot?.order || slotId || ""}`);
  const node = document.createElement("section");
  node.className = `editor-inline-figure${state.pendingSlotMoveId === slotId ? " is-moving" : ""}`;
  node.dataset.editorSlotId = slotId;
  node.innerHTML = `
    <div class="editor-inline-figure-rule"></div>
    <div class="editor-inline-figure-frame">
      <div class="editor-inline-figure-inner">
        ${
          currentImage
            ? `<img src="${currentImage}" alt="" />`
            : `<div class="editor-inline-placeholder">
                <strong>插图位 ${slot?.order || slotId}</strong>
                <span>这里只增加图片占位，不改正文</span>
              </div>`
        }
      </div>
    </div>
    <div class="editor-inline-slot-actions">
      <button class="secondary-btn small" type="button" data-editor-slot-move="${slotId}">改位置</button>
      <button class="secondary-btn danger small" type="button" data-editor-slot-delete="${slotId}">删除</button>
    </div>
  `;
  return node;
}

function renderEditorView(detail) {
  const blocks = editorBlocks(detail);
  refs.editorView.innerHTML = "";
  refs.editorView.style.setProperty("--editor-accent", detail?.tone?.primaryColor || "#b3832f");
  if (!blocks.length) {
    refs.editorView.innerHTML = '<div class="editor-empty">当前还没有可编辑的正文块。</div>';
    hideEditorToolbar();
    return;
  }
  const shell = document.createElement("section");
  shell.className = "editor-preview-shell";
  const canvas = document.createElement("article");
  canvas.className = "editor-canvas";
  const body = document.createElement("div");
  body.className = "editor-preview-body";
  body.appendChild(renderEditorHero(detail));
  blocks.forEach((block) => {
    if (block.kind === "image-slot") {
      body.appendChild(renderEditorImageSlotBlock(detail, block));
      return;
    }
    if (block.kind === "list") {
      body.appendChild(renderEditorListBlock(block));
      return;
    }
    const tagName = block.kind === "heading" ? `h${Math.min(Math.max(Number(block.level || 2), 2), 4)}` : "p";
    const element = document.createElement(tagName);
    element.className = `editor-block editor-block-${block.kind}${block.kind === "heading" ? ` editor-block-heading-level-${Math.min(Math.max(Number(block.level || 2), 2), 4)}` : ""}`;
    element.contentEditable = "true";
    element.spellcheck = false;
    element.dataset.blockId = block.id || "";
    element.dataset.editorTextBlock = "true";
    element.innerHTML = block.htmlText || escapeHtml(block.text || "");
    body.appendChild(element);
  });
  canvas.appendChild(body);
  shell.appendChild(canvas);
  refs.editorView.appendChild(shell);
  hideEditorToolbar();
}

async function refreshDetailFromResult(result, { toastMessage = "", clearPendingMove = false } = {}) {
  const previewMode = state.previewMode;
  state.detail = result.detail;
  if (clearPendingMove) {
    state.pendingSlotMoveId = "";
  }
  renderDetail();
  state.previewMode = previewMode;
  renderPreviewMode();
  if (toastMessage) {
    showToast(toastMessage);
  }
}

function queueEditorBlockSave(element) {
  const blockId = element?.dataset?.blockId || "";
  if (!blockId || !state.selectedId) return;
  clearTimeout(state.editorSaveTimers[blockId]);
  const nextText = serializeEditorBlockContent(element);
  state.editorSaveTimers[blockId] = setTimeout(() => {
    saveEditorBlock(blockId, nextText).catch((error) => showToast(error.message || "正文自动保存失败"));
  }, 400);
}

async function saveEditorBlock(blockId, text) {
  if (!state.selectedId || !blockId) return;
  delete state.editorSaveTimers[blockId];
  const result = await requestJson(`/api/articles/${encodeURIComponent(state.selectedId)}/editor/text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ blockId, text }),
  });
  await refreshDetailFromResult(result);
}

async function handleEditorSelectionAction(action) {
  if (!state.selectedId || !state.editorSelection?.blockId) return;
  const current = currentEditorRange();
  if (!current) return;
  const { selection, range, block } = current;
  if (range.collapsed) {
    showToast(action === "highlight" ? "请先选中要高亮的文字" : "请先选中要删除的文字");
    return;
  }

  if (action === "highlight") {
    const highlight = document.createElement("span");
    highlight.className = "editor-theme-highlight";
    const fragment = range.extractContents();
    highlight.appendChild(fragment);
    range.insertNode(highlight);
  } else if (action === "delete") {
    range.deleteContents();
  } else {
    return;
  }

  cleanupEditorBlockHighlights(block);
  selection.removeAllRanges();
  hideEditorToolbar();
  await saveEditorBlock(block.dataset.blockId || "", serializeEditorBlockContent(block));
  showToast(action === "highlight" ? "文字已高亮" : "文字已删除");
}

async function handleEditorInsertImageSlot() {
  if (!state.selectedId || !state.editorSelection?.blockId) return;
  const moving = Boolean(state.pendingSlotMoveId);
  const url = moving
    ? `/api/articles/${encodeURIComponent(state.selectedId)}/editor/image-slot/move`
    : `/api/articles/${encodeURIComponent(state.selectedId)}/editor/image-slot/insert`;
  const body = moving
    ? {
        slotId: state.pendingSlotMoveId,
        blockId: state.editorSelection.blockId,
        offset: state.editorSelection.start,
      }
    : {
        blockId: state.editorSelection.blockId,
        offset: state.editorSelection.start,
      };
  const result = await requestJson(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  await refreshDetailFromResult(result, {
    toastMessage: moving ? "插图位位置已更新" : "插图位已插入",
    clearPendingMove: moving,
  });
}

async function handleDeleteInlineSlot(slotId) {
  if (!state.selectedId || !slotId) return;
  if (!window.confirm("删除这个插图位后，正文里的占位也会一起删掉，是否继续？")) return;
  const result = await requestJson(`/api/articles/${encodeURIComponent(state.selectedId)}/editor/image-slot/delete`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ slotId }),
  });
  await refreshDetailFromResult(result, { toastMessage: "插图位已删除", clearPendingMove: state.pendingSlotMoveId === slotId });
}

function injectPreviewInlineEditorStyles(doc) {
  if (!doc.head || doc.getElementById("previewInlineEditorStyles")) return;
  const style = doc.createElement("style");
  style.id = "previewInlineEditorStyles";
  style.textContent = `
    .preview-inline-edit-host {
      position: relative !important;
    }
    .preview-inline-edit-btn {
      position: absolute;
      top: 12px;
      right: 12px;
      z-index: 30;
      border: 0;
      border-radius: 999px;
      padding: 9px 12px;
      background: rgba(255, 255, 255, 0.96);
      color: #cb5e1d;
      font: 600 13px/1.1 "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      box-shadow: 0 12px 28px rgba(52, 40, 30, 0.16);
      cursor: pointer;
    }
    .preview-inline-edit-btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 16px 32px rgba(52, 40, 30, 0.2);
    }
    .preview-inline-edit-btn:focus-visible {
      outline: 2px solid #ef7a34;
      outline-offset: 2px;
    }
    [data-inline-slot] img[data-inline-editable="true"] {
      cursor: pointer;
    }
  `;
  doc.head.appendChild(style);
}

function attachPreviewInlineEditControl(doc, figure, img, slot) {
  if (!figure || !img || !slot) return;
  figure.dataset.inlineSlot = String(slot);
  const host = img.parentElement && img.parentElement !== figure ? img.parentElement : figure;
  if (!host) return;
  host.classList.add("preview-inline-edit-host");
  if (!host.querySelector(`.preview-inline-edit-btn[data-inline-slot="${slot}"]`)) {
    const button = doc.createElement("button");
    button.type = "button";
    button.className = "preview-inline-edit-btn";
    button.dataset.inlineSlot = String(slot);
    button.textContent = `编辑插图`;
    button.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      focusInlineEditor(slot);
    });
    host.appendChild(button);
  }
  if (img.dataset.inlineEditBound !== "true") {
    img.dataset.inlineEditable = "true";
    img.dataset.inlineEditBound = "true";
    img.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      focusInlineEditor(slot);
    });
  }
}

function hideDuplicatePreviewImage(primaryImg, duplicateImg) {
  if (!primaryImg || !duplicateImg || primaryImg === duplicateImg) return;
  const duplicateCell = duplicateImg.closest("td");
  if (duplicateCell) {
    duplicateCell.style.display = "none";
  } else {
    const duplicateWrapper = duplicateImg.parentElement;
    if (duplicateWrapper && duplicateWrapper !== duplicateImg.closest("figure")) {
      duplicateWrapper.style.display = "none";
    } else {
      duplicateImg.style.display = "none";
    }
  }
  const primaryCell = primaryImg.closest("td");
  if (primaryCell) {
    primaryCell.style.width = "100%";
    primaryCell.style.padding = "0";
  }
  const table = primaryImg.closest("table");
  if (table) {
    table.style.width = "100%";
  }
}

function enhancePreviewInlineEditors(doc) {
  if (!doc || !state.detail) return;
  const inlineItems = editorSlots(state.detail)
    .map((slot) => (slot.currentItem ? { ...slot.currentItem, slotId: slot.slotId } : null))
    .filter(Boolean);
  if (!inlineItems.length) return;
  injectPreviewInlineEditorStyles(doc);

  const assetMap = new Map();
  inlineItems.forEach((item) => {
    const normalized = normalizeAssetUrl(assetUrl(item));
    const slot = String(item.slotId || "");
    if (normalized && slot) {
      assetMap.set(normalized, slot);
    }
  });
  if (!assetMap.size) return;

  const groups = new Map();
  Array.from(doc.querySelectorAll("img")).forEach((img) => {
    const normalized = normalizeAssetUrl(img.getAttribute("src") || img.src);
    const slot = assetMap.get(normalized);
    if (!slot) return;
    const figure = img.closest("figure") || img.closest("table") || img.parentElement;
    if (!figure) return;
    let figureGroup = groups.get(figure);
    if (!figureGroup) {
      figureGroup = new Map();
      groups.set(figure, figureGroup);
    }
    const slotImages = figureGroup.get(slot) || [];
    slotImages.push(img);
    figureGroup.set(slot, slotImages);
  });

  groups.forEach((figureGroup, figure) => {
    figureGroup.forEach((images, slot) => {
      const [primaryImg, ...duplicates] = images;
      duplicates.forEach((duplicateImg) => hideDuplicatePreviewImage(primaryImg, duplicateImg));
      attachPreviewInlineEditControl(doc, figure, primaryImg, slot);
    });
  });
}

function renderDetail() {
  const hasDetail = Boolean(state.detail);
  refs.detailEmptyState.classList.toggle("hidden", hasDetail);
  refs.detailWrap.classList.toggle("hidden", !hasDetail);
  if (!hasDetail) {
    setArticleMenuOpen(false);
    hideEditorToolbar();
    return;
  }
  syncFormFromDetail();
  renderArticleInfo(state.detail);
  renderArticleInfoCollapse();
  renderWarnings(state.detail);
  renderVisualStatus(state.detail);
  renderCover(state.detail);
  renderInlineImages(state.detail);
  renderDraft(state.detail);
  renderPreview(state.detail);
}

function renderSettings() {
  if (!state.settings) return;
  refs.wechatMode.textContent = state.settings.wechat.mode || "-";
  refs.wechatAppid.textContent = state.settings.wechat.appid || "-";
  refs.wechatConfigured.textContent = state.settings.wechat.configured ? "已配置" : "未配置";
  refs.configuredImageProvider.textContent = state.settings.image.configuredProvider || "-";
  refs.configuredImageModel.textContent = state.settings.image.configuredModel || "-";
  refs.configuredImageApiBase.textContent = state.settings.image.configuredApiBase || "-";
  refs.effectiveImageProvider.textContent = state.settings.image.effectiveProvider || "-";
  refs.effectiveImageModel.textContent = state.settings.image.effectiveModel || "-";
  refs.effectiveImageApiBase.textContent = state.settings.image.effectiveApiBase || "-";
  refs.imageConfigured.textContent = state.settings.image.configured ? "已配置" : "未配置";
  refs.imageModelSource.textContent = state.settings.image.modelSource || "-";
  refs.settingsWorkspace.textContent = state.settings.workspace || "-";
  refs.settingsTheme.textContent = themeLabel(state.settings.defaultTheme || "-");
  refs.settingsCover.textContent = state.settings.defaultCover || "未设置";
}

function renderActiveView() {
  document.querySelectorAll("[data-view]").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === state.activeView);
  });
  refs.workbenchView.classList.toggle("hidden", state.activeView !== "workbench");
  refs.workbenchView.classList.toggle("is-active", state.activeView === "workbench");
  refs.settingsView.classList.toggle("hidden", state.activeView !== "settings");
  refs.settingsView.classList.toggle("is-active", state.activeView === "settings");
}

function currentActionPayload() {
  return {
    tone: {
      theme: refs.themeSelect.value || state.form.tone.theme,
      primaryColor: refs.primaryColorInput.value || state.form.tone.primaryColor,
      saturation: Number(refs.saturationRange.value || state.form.tone.saturation),
      opacity: Number(refs.opacityRange.value || state.form.tone.opacity),
    },
  };
}

function schedulePreviewRefresh() {
  updateRangeReadouts();
  refs.themeHint.textContent = themeDescription(refs.themeSelect.value) || "选择文章的整体气质基底。";
  if (!state.selectedId) return;
  clearTimeout(state.autoPreviewTimer);
  state.autoPreviewTimer = setTimeout(() => {
    handlePreview({ silent: true }).catch((error) => showToast(error.message || "预览刷新失败"));
  }, 420);
}

async function loadSettings() {
  state.settings = await requestJson("/api/settings/status");
  updateWorkspaceBadge();
  renderSettings();
}

async function loadArticles() {
  const payload = await requestJson("/api/articles");
  state.articles = payload.articles || [];
  if (state.selectedId && state.articles.some((item) => item.id === state.selectedId)) {
    renderArticleList();
    return;
  }
  state.selectedId = state.articles[0]?.id || "";
  renderArticleList();
}

async function loadArticleDetail(articleId) {
  if (!articleId) {
    state.detail = null;
    state.coverPromptDraft = undefined;
    state.inlinePromptDrafts = {};
    state.pendingSlotMoveId = "";
    state.editorSelection = null;
    renderDetail();
    return;
  }
  state.coverPromptDraft = undefined;
  state.inlinePromptDrafts = {};
  state.pendingSlotMoveId = "";
  state.editorSelection = null;
  state.selectedId = articleId;
  renderArticleList();
  const payload = await requestJson(`/api/articles/${encodeURIComponent(articleId)}`);
  state.detail = payload.detail;
  renderDetail();
}

async function handleDeleteArticle(articleId) {
  if (!articleId) return;
  const article = (state.articles || []).find((item) => item.id === articleId);
  const articleTitle = article?.title || articleId;
  if (!window.confirm(`删除后会移除《${articleTitle}》的本地文章目录与相关素材，是否继续？`)) return;
  const deletingCurrent = articleId === state.selectedId;
  setArticleMenuOpen(false);
  const result = await requestJson(`/api/articles/${encodeURIComponent(articleId)}/delete`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}),
  });

  if (deletingCurrent) {
    state.selectedId = "";
    state.detail = null;
  }

  await loadArticles();
  if (!state.selectedId) {
    state.detail = null;
    renderDetail();
  } else if (deletingCurrent) {
    await loadArticleDetail(state.selectedId);
  }

  showToast(result.message || "文章已删除");
}

async function handlePreview({ silent = false } = {}) {
  if (!state.selectedId) {
    if (!silent) showToast("先导入或选择一篇文章");
    return;
  }
  setButtonBusy(refs.generatePreviewButton, true, "立即刷新预览", "刷新中...");
  try {
    const result = await requestJson(`/api/articles/${encodeURIComponent(state.selectedId)}/layout/preview`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(currentActionPayload()),
    });
    state.detail = result.detail;
    renderDetail();
    if (!silent) showToast(result.message || "预览已刷新");
  } finally {
    setButtonBusy(refs.generatePreviewButton, false, "立即刷新预览", "刷新中...");
  }
}

async function handleUpload(file) {
  if (!file) return;
  if (!/\.md$/i.test(file.name)) {
    showToast("只支持导入 .md 文件");
    return;
  }
  const formData = new FormData();
  formData.append("file", file, file.name);
  refs.uploadDropzone.classList.add("is-busy");
  setButtonBusy(refs.importButton, true, "选择 Markdown", "导入中...");
  try {
    const result = await requestJson("/api/articles/import", {
      method: "POST",
      body: formData,
    });
    await loadArticles();
    state.selectedId = result.detail.article.id;
    state.detail = result.detail;
    state.coverPromptDraft = undefined;
    state.inlinePromptDrafts = {};
    renderArticleList();
    renderDetail();
    const warningCount = Array.isArray(result.detail.source?.warnings) ? result.detail.source.warnings.length : 0;
    showToast(warningCount ? `导入完成，先调风格再生成内容（${warningCount} 条提醒）` : "Markdown 导入完成，先调风格再生成内容");
  } finally {
    refs.uploadDropzone.classList.remove("is-busy");
    refs.markdownFileInput.value = "";
    setButtonBusy(refs.importButton, false, "选择 Markdown", "导入中...");
  }
}

async function handleGenerateCover() {
  if (!state.selectedId) return;
  const generated = state.detail?.images?.coverGenerated || null;
  const promptValue = refs.coverResultPromptInput.value.trim();
  const promptBaseline = (refs.coverResultPromptInput.dataset.promptBaseline || "").trim();
  const promptEdited = Boolean(promptValue && promptValue !== promptBaseline);
  const payload = { ...currentActionPayload() };
  if (promptEdited) {
    payload.promptOverride = promptValue;
    payload.styleId = refs.coverResultPromptInput.dataset.coverStyleId || generated?.styleId || "";
  }
  setButtonBusy(refs.generateCoverButton, true, "generate", "generating");
  try {
    const result = await requestJson(`/api/articles/${encodeURIComponent(state.selectedId)}/images/cover`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    state.detail = result.detail;
    state.coverPromptDraft = undefined;
    renderDetail();
    showToast(result.message || "封面候选已生成");
  } finally {
    setButtonBusy(refs.generateCoverButton, false, "generate", "generating");
  }
}

async function handleSelectCover(localPath) {
  if (!state.selectedId || !localPath) return;
  const result = await requestJson(`/api/articles/${encodeURIComponent(state.selectedId)}/images/cover/select`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path: localPath }),
  });
  state.detail = result.detail;
  renderDetail();
  showToast(result.message || "当前封面已更新");
}

async function handleDeleteCover(localPath) {
  if (!state.selectedId || !localPath) return;
  if (!window.confirm("删除后会移除本地封面文件和当前记录，是否继续？")) return;
  const result = await requestJson(`/api/articles/${encodeURIComponent(state.selectedId)}/images/cover/delete`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path: localPath }),
  });
  state.detail = result.detail;
  renderDetail();
  showToast(result.message || "封面图片已删除");
}

function collectInlinePromptOverrides() {
  const overrides = {};
  refs.inlineGallery.querySelectorAll("[data-inline-prompt-slot]").forEach((input) => {
    const slotId = String(input.dataset.inlinePromptSlot || "").trim();
    if (!slotId) return;
    overrides[slotId] = String(input.value || "");
  });
  return overrides;
}

async function handleGenerateInline(slotId = "", promptOverride = null, triggerButton = null) {
  if (!state.selectedId) return;
  setButtonBusy(refs.generateInlineButton, true, "generate", "generating");
  if (triggerButton) {
    setButtonBusy(triggerButton, true, "generate", "generating");
  }
  try {
    const payload = {
      ...currentActionPayload(),
      promptOverrides: collectInlinePromptOverrides(),
      slotId,
    };
    if (slotId && promptOverride !== null) {
      payload.promptOverride = String(promptOverride);
    }
    const result = await requestJson(`/api/articles/${encodeURIComponent(state.selectedId)}/images/inline`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    await refreshDetailFromResult(result, {
      toastMessage: slotId ? "插图已生成" : (result.message || "正文配图已生成"),
    });
  } finally {
    setButtonBusy(refs.generateInlineButton, false, "generate", "generating");
    if (triggerButton) {
      setButtonBusy(triggerButton, false, "generate", "generating");
    }
  }
}

async function handleSelectInline(slotId, localPath) {
  if (!state.selectedId || !slotId || !localPath) return;
  const result = await requestJson(`/api/articles/${encodeURIComponent(state.selectedId)}/images/inline/select`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ slotId, path: localPath }),
  });
  await refreshDetailFromResult(result, { toastMessage: result.message || "正文插图已切换" });
}

async function handleDeleteInline(localPath) {
  if (!state.selectedId || !localPath) return;
  if (!window.confirm("删除后会移除本地正文配图文件和当前记录，是否继续？")) return;
  const result = await requestJson(`/api/articles/${encodeURIComponent(state.selectedId)}/images/inline/delete`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path: localPath }),
  });
  await refreshDetailFromResult(result, { toastMessage: result.message || "正文配图已删除" });
}

async function handlePushDraft() {
  if (!state.selectedId) return;
  setButtonBusy(refs.pushDraftButton, true, "推送到草稿箱", "推送中...");
  try {
    const result = await requestJson(`/api/articles/${encodeURIComponent(state.selectedId)}/draft`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...currentActionPayload(),
        coverPath: refs.coverCandidatePath.value.trim(),
      }),
    });
    state.detail = result.detail;
    renderDetail();
    showToast(result.message || "已推送到草稿箱");
  } finally {
    setButtonBusy(refs.pushDraftButton, false, "推送到草稿箱", "推送中...");
  }
}

async function copyHtml() {
  const html = state.detail?.preview?.sourceHtml || "";
  if (!html) {
    showToast("先生成预览再复制");
    return;
  }
  try {
    await navigator.clipboard.writeText(html);
    showToast("HTML 已复制");
  } catch (_error) {
    showToast("复制失败，请稍后重试");
  }
}

function saveHtml() {
  const html = state.detail?.preview?.sourceHtml || "";
  if (!html) {
    showToast("先生成预览再保存");
    return;
  }
  const blob = new Blob([html], { type: "text/html;charset=utf-8" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = state.lastSavedName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(link.href);
  showToast("HTML 已保存到本地下载");
}

function bindUploadEvents() {
  refs.importButton.addEventListener("click", () => refs.markdownFileInput.click());
  refs.markdownFileInput.addEventListener("change", (event) => {
    const file = event.target.files?.[0];
    handleUpload(file).catch((error) => showToast(error.message || "导入失败"));
  });

  ["dragenter", "dragover"].forEach((eventName) => {
    refs.uploadDropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      refs.uploadDropzone.classList.add("is-dragover");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    refs.uploadDropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      refs.uploadDropzone.classList.remove("is-dragover");
    });
  });

  refs.uploadDropzone.addEventListener("drop", (event) => {
    const file = event.dataTransfer?.files?.[0];
    handleUpload(file).catch((error) => showToast(error.message || "导入失败"));
  });

  refs.uploadDropzone.addEventListener("click", () => refs.markdownFileInput.click());
  refs.uploadDropzone.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      refs.markdownFileInput.click();
    }
  });
}

function bindEvents() {
  document.querySelectorAll("[data-view]").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeView = button.dataset.view;
      renderActiveView();
    });
  });

  bindUploadEvents();

  refs.articleSwitcherButton.addEventListener("click", (event) => {
    event.stopPropagation();
    if (refs.articleSwitcherButton.disabled) return;
    setArticleMenuOpen(!state.articleMenuOpen);
  });

  refs.articleInfoToggle.addEventListener("click", () => {
    setArticleInfoCollapsed(!state.articleInfoCollapsed);
  });

  refs.articleSwitcherMenu.addEventListener("click", (event) => {
    const deleteButton = event.target.closest("[data-article-delete-id]");
    if (deleteButton) {
      handleDeleteArticle(deleteButton.dataset.articleDeleteId).catch((error) => showToast(error.message || "文章删除失败"));
      return;
    }
    const selectButton = event.target.closest("[data-article-id]");
    if (!selectButton) return;
    const articleId = selectButton.dataset.articleId || "";
    setArticleMenuOpen(false);
    if (!articleId || articleId === state.selectedId) return;
    loadArticleDetail(articleId).catch((error) => showToast(error.message || "加载文章失败"));
  });

  document.addEventListener("click", (event) => {
    if (!(event.target instanceof Node)) return;
    if (refs.articleSwitcherWrap.contains(event.target)) return;
    setArticleMenuOpen(false);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") setArticleMenuOpen(false);
  });

  [
    refs.themeSelect,
    refs.primaryColorInput,
    refs.saturationRange,
    refs.opacityRange,
  ].forEach((input) => {
    input.addEventListener("input", schedulePreviewRefresh);
    input.addEventListener("change", schedulePreviewRefresh);
  });

  refs.generatePreviewButton.addEventListener("click", () => {
    handlePreview().catch((error) => showToast(error.message || "预览刷新失败"));
  });
  refs.generateCoverButton.addEventListener("click", () => {
    handleGenerateCover().catch((error) => showToast(error.message || "封面生成失败"));
  });
  refs.selectCoverButton.addEventListener("click", () => {
    const localPath = refs.selectCoverButton.dataset.coverPath || state.detail?.images?.coverGenerated?.localPath;
    handleSelectCover(localPath).catch((error) => showToast(error.message || "封面切换失败"));
  });
  refs.deleteCoverButton.addEventListener("click", () => {
    const localPath = refs.deleteCoverButton.dataset.deleteCoverPath || state.detail?.images?.coverGenerated?.localPath;
    handleDeleteCover(localPath).catch((error) => showToast(error.message || "封面删除失败"));
  });
  refs.generateInlineButton.addEventListener("click", () => {
    handleGenerateInline().catch((error) => showToast(error.message || "正文配图生成失败"));
  });
  refs.pushDraftButton.addEventListener("click", () => {
    handlePushDraft().catch((error) => showToast(error.message || "草稿推送失败"));
  });

  refs.coverHistoryGallery.addEventListener("click", (event) => {
    const deleteButton = event.target.closest("[data-delete-cover-path]");
    if (deleteButton) {
      handleDeleteCover(deleteButton.dataset.deleteCoverPath).catch((error) => showToast(error.message || "封面删除失败"));
      return;
    }
    const button = event.target.closest("[data-cover-path]");
    if (!button) return;
    handleSelectCover(button.dataset.coverPath).catch((error) => showToast(error.message || "封面切换失败"));
  });

  refs.inlineGallery.addEventListener("click", (event) => {
    const deleteSlotButton = event.target.closest("[data-inline-delete-slot]");
    if (deleteSlotButton) {
      handleDeleteInlineSlot(deleteSlotButton.dataset.inlineDeleteSlot).catch((error) => showToast(error.message || "插图位删除失败"));
      return;
    }
    const moveSlotButton = event.target.closest("[data-inline-move-slot]");
    if (moveSlotButton) {
      state.pendingSlotMoveId = moveSlotButton.dataset.inlineMoveSlot || "";
      renderInlineImages(state.detail);
      updateEditorInsertButtonLabel();
      showToast("请在右侧编辑区重新选中一个位置，然后点“插入插图位”完成移动。");
      return;
    }
    const deleteButton = event.target.closest("[data-delete-inline-path]");
    if (deleteButton) {
      handleDeleteInline(deleteButton.dataset.deleteInlinePath).catch((error) => showToast(error.message || "正文配图删除失败"));
      return;
    }
    const historyButton = event.target.closest("[data-inline-slot-id]");
    if (historyButton) {
      const slotId = historyButton.dataset.inlineSlotId || "";
      const localPath = historyButton.dataset.inlinePath || "";
      if (!slotId || !localPath) return;
      handleSelectInline(slotId, localPath).catch((error) => showToast(error.message || "插图切换失败"));
      return;
    }
    const button = event.target.closest("[data-inline-regenerate]");
    if (!button) return;
    const slotId = String(button.dataset.inlineRegenerate || "").trim();
    if (!slotId) return;
    const card = button.closest("[data-inline-card-slot]");
    const promptInput = card?.querySelector(`[data-inline-prompt-slot="${slotId}"]`);
    const promptOverride = promptInput ? promptInput.value : null;
    handleGenerateInline(slotId, promptOverride, button).catch((error) => showToast(error.message || "插图重生成失败"));
  });

  refs.inlineGallery.addEventListener("input", (event) => {
    const promptInput = event.target.closest("[data-inline-prompt-slot]");
    if (!promptInput) return;
    const slotId = String(promptInput.dataset.inlinePromptSlot || "").trim();
    if (!slotId) return;
    state.inlinePromptDrafts[slotId] = promptInput.value;
  });

  refs.coverResultPromptInput.addEventListener("input", () => {
    state.coverPromptDraft = refs.coverResultPromptInput.value;
  });

  refs.previewModeButton.addEventListener("click", () => {
    state.previewMode = state.previewMode === "preview" ? "edit" : "preview";
    renderPreviewMode();
  });
  refs.copyHtmlButton.addEventListener("click", () => copyHtml());
  refs.saveHtmlButton.addEventListener("click", saveHtml);
  refs.previewFrame.addEventListener("load", resizePreviewFrame);

  refs.editorView.addEventListener("input", (event) => {
    const block = event.target.closest("[data-editor-text-block='true']");
    if (!block) return;
    queueEditorBlockSave(block);
  });
  refs.editorView.addEventListener("mouseup", () => {
    setTimeout(updateEditorSelectionToolbar, 0);
  });
  refs.editorView.addEventListener("keyup", () => {
    setTimeout(updateEditorSelectionToolbar, 0);
  });
  refs.editorView.addEventListener("click", (event) => {
    const deleteButton = event.target.closest("[data-editor-slot-delete]");
    if (deleteButton) {
      handleDeleteInlineSlot(deleteButton.dataset.editorSlotDelete).catch((error) => showToast(error.message || "插图位删除失败"));
      return;
    }
    const moveButton = event.target.closest("[data-editor-slot-move]");
    if (moveButton) {
      state.pendingSlotMoveId = moveButton.dataset.editorSlotMove || "";
      renderInlineImages(state.detail);
      renderEditorView(state.detail);
      updateEditorInsertButtonLabel();
      showToast("请继续在正文里选中新的位置，然后点“移动插图位”。");
      return;
    }
    setTimeout(updateEditorSelectionToolbar, 0);
  });
  document.addEventListener("selectionchange", () => {
    if (state.previewMode === "edit") {
      updateEditorSelectionToolbar();
    }
  });
  refs.editorHighlightButton.addEventListener("click", () => {
    handleEditorSelectionAction("highlight").catch((error) => showToast(error.message || "文字高亮失败"));
  });
  refs.editorDeleteButton.addEventListener("click", () => {
    handleEditorSelectionAction("delete").catch((error) => showToast(error.message || "文字删除失败"));
  });
  refs.editorInsertImageButton.addEventListener("click", () => {
    handleEditorInsertImageSlot().catch((error) => showToast(error.message || "插图位操作失败"));
  });
}

async function init() {
  bindEvents();
  renderArticleInfoCollapse();
  renderActiveView();
  try {
    await loadSettings();
    await loadArticles();
    if (state.selectedId) {
      await loadArticleDetail(state.selectedId);
    } else {
      renderDetail();
    }
  } catch (error) {
    showToast(error.message || "初始化失败");
  }
}

init();
