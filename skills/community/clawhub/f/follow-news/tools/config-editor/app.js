(() => {
  const PAGE_SIZE = 20;
  const PODCAST_PLATFORMS = ["auto", "rss", "youtube", "xiaoyuzhou"];
  const PODCAST_TRANSCRIPT_BACKENDS = ["auto", "yt-dlp", "opencli"];

  const TEXT = {
    zh: {
      title: "Follow-News JSON 编辑器",
      subtitle: "无外部依赖，编辑默认 sources.json 与 topics.json",
      saveHint: "保存中...",
      loaded: "已加载",
      loadFailed: "加载失败",
      refresh: "正在刷新...",
      saveSuccess: "保存成功",
      saveFailed: "保存失败",
      parseError: "JSON 格式错误，请先修复后再切换/保存",
      noSourceData: "sources.json 缺少 sources 数组",
      noTopicData: "topics.json 缺少 topics 数组",
      invalidData: "请求返回格式不正确",
      searchHint: "未搜索到匹配项",
      tableMode: "切换到表格模式",
      jsonMode: "切换到 JSON 模式",
      confirmDelete: "确定删除该项？",
      titleSources: "订阅源配置",
      titleTopics: "话题配置",
      footer: "本工具仅改本地默认配置文件。修改前建议先做 git 备份。",
      actions: {
        reload: "重新加载",
        save: "保存",
        addSource: "新增来源",
        addTopic: "新增话题",
        tableMode: "切换到表格模式",
        jsonMode: "切换到 JSON 模式",
        delete: "删除",
        prev: "上一页",
        next: "下一页",
      },
      sources: {
        title: "订阅源配置",
        searchPlaceholder: "搜索 id / 名称 / 来源字段...",
        thId: "ID",
        thType: "类型",
        thName: "名称",
        thSourceField: "来源字段",
        thEnabled: "启用",
        thPriority: "优先",
        thTopics: "topics",
        thPlatform: "platform",
        thTranscriptEnabled: "transcript.enabled",
        thTranscriptBackend: "transcript.backend",
        thTranscriptLanguages: "transcript.languages",
        typeAll: "全部类型",
      },
      topics: {
        title: "话题配置",
        hint: "说明：topics.json 结构较小，建议直接在表格里修改",
        searchPlaceholder: "搜索 id / 标签...",
        thEmoji: "emoji",
        thLabel: "标签",
        thMaxItems: "最大条数",
        thStyle: "样式",
        thStyleDetailed: "detailed",
        thStyleCompact: "compact",
        thQueries: "queries（逗号）",
      },
      langLabel: "English",
      lang: "zh",
    },
    en: {
      title: "Follow-News JSON Editor",
      subtitle: "Local editor with no external dependencies for sources.json and topics.json",
      saveHint: "Saving...",
      loaded: "Loaded",
      loadFailed: "Load failed",
      refresh: "Refreshing...",
      saveSuccess: "Saved",
      saveFailed: "Save failed",
      parseError: "Invalid JSON, please fix it before switching/saving",
      noSourceData: "sources.json is missing 'sources' array",
      noTopicData: "topics.json is missing 'topics' array",
      invalidData: "Unexpected response format",
      searchHint: "No matching items",
      tableMode: "Switch to table mode",
      jsonMode: "Switch to JSON mode",
      confirmDelete: "Delete this item?",
      titleSources: "Sources",
      titleTopics: "Topics",
      footer: "This tool only edits local default config files. Make a git backup before changes.",
      actions: {
        reload: "Reload",
        save: "Save",
        addSource: "Add source",
        addTopic: "Add topic",
        tableMode: "Switch to table mode",
        jsonMode: "Switch to JSON mode",
        delete: "Delete",
        prev: "Prev",
        next: "Next",
      },
      sources: {
        title: "Sources",
        searchPlaceholder: "Search by id / name / source field",
        thId: "ID",
        thType: "Type",
        thName: "Name",
        thSourceField: "Source field",
        thEnabled: "Enabled",
        thPriority: "Priority",
        thTopics: "topics",
        thPlatform: "platform",
        thTranscriptEnabled: "transcript.enabled",
        thTranscriptBackend: "transcript.backend",
        thTranscriptLanguages: "transcript.languages",
        typeAll: "All types",
      },
      topics: {
        title: "Topics",
        hint: "topics.json is small; table mode is recommended",
        searchPlaceholder: "Search by id / label",
        thEmoji: "emoji",
        thLabel: "Label",
        thMaxItems: "Max items",
        thStyle: "Style",
        thStyleDetailed: "detailed",
        thStyleCompact: "compact",
        thQueries: "queries (comma-separated)",
      },
      langLabel: "中文",
      lang: "en",
    },
  };

  const state = {
    lang: "zh",
    sources: {
      key: "sources",
      raw: {},
      rows: [],
      filtered: [],
      typeFilter: "",
      page: 1,
      mode: "table",
    },
    topics: {
      key: "topics",
      raw: {},
      rows: [],
      filtered: [],
      mode: "table",
    },
  };

  const el = {
    langBtn: $("langBtn"),
    saveAllStatus: $("saveAllStatus"),
    loadAllBtn: $("loadAllBtn"),
    sourceSearch: $("sourceSearch"),
    sourceTypeFilter: $("sourceTypeFilter"),
    addSourceBtn: $("addSourceBtn"),
    toggleSourceModeBtn: $("toggleSourceModeBtn"),
    saveSourcesBtn: $("saveSourcesBtn"),
    sourceModeTable: $("sourceModeTable"),
    sourceModeJson: $("sourceModeJson"),
    sourceTableBody: $("sourceTableBody"),
    sourcePrevBtn: $("sourcePrevBtn"),
    sourceNextBtn: $("sourceNextBtn"),
    sourcePageLabel: $("sourcePageLabel"),
    sourceTableSummary: $("sourceTableSummary"),
    sourceJsonText: $("sourceJsonText"),
    sourceStatus: $("sourceStatus"),
    topicSearch: $("topicSearch"),
    addTopicBtn: $("addTopicBtn"),
    toggleTopicModeBtn: $("toggleTopicModeBtn"),
    saveTopicsBtn: $("saveTopicsBtn"),
    topicModeTable: $("topicModeTable"),
    topicModeJson: $("topicModeJson"),
    topicTableBody: $("topicTableBody"),
    topicJsonText: $("topicJsonText"),
    topicStatus: $("topicStatus"),
  };

  function $(id) {
    return document.getElementById(id);
  }

  function t(path) {
    const langPack = TEXT[state.lang];
    const parts = path.split(".");
    let cursor = langPack;
    for (const part of parts) {
      cursor = cursor && cursor[part];
    }
    return cursor || path;
  }

  function setStatus(target, msg, ok = true) {
    target.textContent = msg;
    target.classList.toggle("ok", ok);
    target.classList.toggle("err", !ok);
  }

  function setGlobalStatus(msg, ok = true) {
    setStatus(el.saveAllStatus, msg, ok);
  }

  function escapeValue(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll('"', "&quot;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  function parseCommaList(raw) {
    return String(raw || "")
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);
  }

  function joinCommaList(value) {
    if (!Array.isArray(value)) return "";
    return value.join(", ");
  }

  function toBool(value) {
    return String(value).toLowerCase() === "true" || value === 1 || value === true;
  }

  function normalizeSource(raw = {}) {
    const sourceType = String(raw.type || "rss").toLowerCase() || "rss";
    const source = {
      ...raw,
      id: raw.id || "",
      type: sourceType,
      name: raw.name || "",
      url: raw.url || "",
      handle: raw.handle || "",
      repo: raw.repo || "",
      subreddit: raw.subreddit || "",
      enabled: toBool(raw.enabled),
      priority: toBool(raw.priority),
      topics: Array.isArray(raw.topics) ? raw.topics.map((item) => String(item)) : [],
    };
    if (source.type === "podcast") {
      source.platform = typeof raw.platform === "string" && raw.platform.trim() ? raw.platform.trim() : "auto";
      source.transcript = normalizePodcastTranscript(raw.transcript);
    }
    return source;
  }

  function normalizePodcastTranscript(raw = {}) {
    if (!raw || typeof raw !== "object") {
      return {
        enabled: false,
        backend: "auto",
        languages: [],
      };
    }

    return {
      ...raw,
      enabled: toBool(raw.enabled),
      backend: typeof raw.backend === "string" && raw.backend.trim() ? raw.backend.trim() : "auto",
      languages: Array.isArray(raw.languages) ? raw.languages.map((item) => String(item)) : [],
    };
  }

  function ensurePodcastDefaults(row) {
    if (!row || String(row.type || "").toLowerCase() !== "podcast") return;
    if (typeof row.platform !== "string" || !row.platform.trim()) row.platform = "auto";
    row.transcript = normalizePodcastTranscript(row.transcript);
  }

  function getSourcePrimaryFieldKey(type = "rss") {
    const normalizedType = String(type || "rss").toLowerCase();
    const fieldByType = {
      rss: "url",
      web: "url",
      x: "handle",
      twitter: "handle",
      github: "repo",
      reddit: "subreddit",
    };
    return fieldByType[normalizedType] || "url";
  }

  function getSourcePrimaryFieldLabel(type = "rss") {
    const field = getSourcePrimaryFieldKey(type);
    if (field === "handle") return state.lang === "zh" ? "handle" : "Handle";
    if (field === "repo") return state.lang === "zh" ? "repo" : "Repo";
    if (field === "subreddit") return state.lang === "zh" ? "subreddit" : "Subreddit";
    return "URL";
  }

  function normalizeTopic(raw = {}) {
    const searchRaw = raw.search || {};
    const displayRaw = raw.display || {};
    return {
      ...raw,
      id: raw.id || "",
      emoji: raw.emoji || "",
      label: raw.label || "",
      description: raw.description || "",
      search: {
        ...searchRaw,
        queries: Array.isArray(searchRaw.queries) ? searchRaw.queries.map(String) : [],
      },
      display: {
        ...displayRaw,
        max_items: Number.isFinite(Number(displayRaw.max_items)) ? Number(displayRaw.max_items) : 8,
        style: displayRaw.style || "detailed",
      },
    };
  }

  function updateI18n() {
    const pack = TEXT[state.lang];
    document.querySelectorAll("[data-i18n]").forEach((node) => {
      const key = node.getAttribute("data-i18n");
      if (key) node.textContent = t(key);
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
      const key = node.getAttribute("data-i18n-placeholder");
      if (key) node.setAttribute("placeholder", t(key));
    });
    el.langBtn.textContent = t("langLabel");
    document.documentElement.lang = pack.lang;
    const typeAllOption = el.sourceTypeFilter.querySelector("option[value='']");
    if (typeAllOption) {
      typeAllOption.textContent = t("sources.typeAll");
    }
  }

  function syncSourceTypeFilterOptions() {
    const current = state.sources.typeFilter || "";
    const types = Array.from(
      new Set(
        state.sources.rows
          .map((row) => String(row.type || "").trim())
          .filter(Boolean),
      ),
    ).sort((a, b) => a.localeCompare(b));

    const prev = el.sourceTypeFilter.value;
    el.sourceTypeFilter.innerHTML = "";
    const allOpt = document.createElement("option");
    allOpt.value = "";
    allOpt.textContent = t("sources.typeAll");
    el.sourceTypeFilter.appendChild(allOpt);

    for (const type of types) {
      const option = document.createElement("option");
      option.value = type;
      option.textContent = type;
      el.sourceTypeFilter.appendChild(option);
    }

    if (current && types.includes(current)) {
      el.sourceTypeFilter.value = current;
    } else if (types.includes(prev)) {
      el.sourceTypeFilter.value = prev;
      state.sources.typeFilter = prev;
    } else {
      el.sourceTypeFilter.value = "";
      state.sources.typeFilter = "";
    }
  }

  function ensureSourceFiltered() {
    const query = (el.sourceSearch.value || "").trim().toLowerCase();
    state.sources.filtered = state.sources.rows
      .map((row, index) => ({ row, index }))
      .filter(({ row }) => {
        if (state.sources.typeFilter && (row.type || "").toLowerCase() !== state.sources.typeFilter.toLowerCase()) {
          return false;
        }
        if (!query) return true;
        const sourceFieldKey = getSourcePrimaryFieldKey(row.type);
        const sourceFieldValue = row[sourceFieldKey] || "";
        const haystack = `${row.id} ${row.type} ${row.name} ${sourceFieldValue} ${row.topics?.join(",")}`.toLowerCase();
        return haystack.includes(query);
      });
  }

  function renderSourcesSummary() {
    const total = state.sources.filtered.length;
    const pageTotal = Math.max(1, Math.ceil(total / PAGE_SIZE));
    if (state.sources.page > pageTotal) state.sources.page = pageTotal;
    if (state.sources.page < 1) state.sources.page = 1;

    const start = total === 0 ? 0 : (state.sources.page - 1) * PAGE_SIZE + 1;
    const end = Math.min(state.sources.page * PAGE_SIZE, total);
    el.sourcePageLabel.textContent = `${start}-${end}/${total}`;
    el.sourcePrevBtn.disabled = state.sources.page <= 1 || total === 0;
    el.sourceNextBtn.disabled = state.sources.page >= pageTotal || total === 0;
    el.sourceTableSummary.textContent =
      total === 0 ? t("searchHint") : `${start}-${end} / ${total}`;
  }

  function renderSourcesTable() {
    state.sources.filtered = state.sources.filtered || [];
    el.sourceTableBody.innerHTML = "";
    const total = state.sources.filtered.length;
    if (state.sources.page > Math.max(1, Math.ceil(total / PAGE_SIZE))) {
      state.sources.page = 1;
    }
    const pageTotal = Math.max(1, Math.ceil(total / PAGE_SIZE));
    state.sources.page = Math.min(Math.max(state.sources.page, 1), pageTotal);

    const start = (state.sources.page - 1) * PAGE_SIZE;
    const end = start + PAGE_SIZE;
    const visible = state.sources.filtered.slice(start, end);

    if (visible.length === 0) {
      const tr = document.createElement("tr");
      const td = document.createElement("td");
      td.colSpan = 12;
      td.textContent = t("searchHint");
      tr.appendChild(td);
      el.sourceTableBody.appendChild(tr);
      renderSourcesSummary();
      return;
    }

    for (const item of visible) {
      const { row, index } = item;
      const isPodcast = String(row.type || "").toLowerCase() === "podcast";
      const isCurrentPodcast = () => String(row.type || "").toLowerCase() === "podcast";
      if (isPodcast) {
        ensurePodcastDefaults(row);
      }
      const tr = document.createElement("tr");

      const idInput = document.createElement("input");
      idInput.value = row.id || "";
      idInput.addEventListener("input", (e) => {
        row.id = e.target.value;
      });
      const tdId = document.createElement("td");
      tdId.appendChild(idInput);

      const typeInput = document.createElement("input");
      typeInput.value = row.type || "rss";
      typeInput.placeholder = "rss";
      typeInput.addEventListener("input", (e) => {
        row.type = e.target.value;
      });
      typeInput.addEventListener("change", () => {
        if (isCurrentPodcast()) {
          ensurePodcastDefaults(row);
        }
        syncSourceTypeFilterOptions();
        ensureSourceFiltered();
        renderSourcesMode();
      });
      const tdType = document.createElement("td");
      tdType.appendChild(typeInput);

      const nameInput = document.createElement("input");
      nameInput.value = row.name || "";
      nameInput.addEventListener("input", (e) => {
        row.name = e.target.value;
      });
      const tdName = document.createElement("td");
      tdName.appendChild(nameInput);

      const sourceFieldKey = getSourcePrimaryFieldKey(row.type);
      const sourceFieldInput = document.createElement("input");
      sourceFieldInput.value = row[sourceFieldKey] || "";
      sourceFieldInput.placeholder = getSourcePrimaryFieldLabel(row.type);
      sourceFieldInput.addEventListener("input", (e) => {
        row[sourceFieldKey] = e.target.value;
      });
      const tdUrl = document.createElement("td");
      tdUrl.appendChild(sourceFieldInput);

      const enabledInput = document.createElement("input");
      enabledInput.type = "checkbox";
      enabledInput.checked = !!row.enabled;
      enabledInput.addEventListener("change", (e) => {
        row.enabled = !!e.target.checked;
      });
      const tdEnabled = document.createElement("td");
      tdEnabled.appendChild(enabledInput);

      const priorityInput = document.createElement("input");
      priorityInput.type = "checkbox";
      priorityInput.checked = !!row.priority;
      priorityInput.addEventListener("change", (e) => {
        row.priority = !!e.target.checked;
      });
      const tdPriority = document.createElement("td");
      tdPriority.appendChild(priorityInput);

      const topicsInput = document.createElement("input");
      topicsInput.value = joinCommaList(row.topics);
      topicsInput.addEventListener("input", (e) => {
        row.topics = parseCommaList(e.target.value);
      });
      const tdTopics = document.createElement("td");
      tdTopics.appendChild(topicsInput);

      const tdPlatform = document.createElement("td");
      const platformInput = document.createElement("select");
      for (const value of PODCAST_PLATFORMS) {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        platformInput.appendChild(option);
      }
      platformInput.value = isPodcast ? row.platform || "auto" : "auto";
      platformInput.disabled = !isCurrentPodcast();
      platformInput.addEventListener("change", (e) => {
        if (!isCurrentPodcast()) return;
        row.platform = e.target.value;
      });
      tdPlatform.appendChild(platformInput);

      const tdTranscriptEnabled = document.createElement("td");
      const transcriptEnabledInput = document.createElement("input");
      transcriptEnabledInput.type = "checkbox";
      transcriptEnabledInput.checked = !!row.transcript?.enabled;
      transcriptEnabledInput.disabled = !isCurrentPodcast();
      transcriptEnabledInput.addEventListener("change", (e) => {
        if (!isCurrentPodcast()) return;
        row.transcript.enabled = !!e.target.checked;
      });
      tdTranscriptEnabled.appendChild(transcriptEnabledInput);

      const tdTranscriptBackend = document.createElement("td");
      const transcriptBackendInput = document.createElement("select");
      for (const value of PODCAST_TRANSCRIPT_BACKENDS) {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        transcriptBackendInput.appendChild(option);
      }
      transcriptBackendInput.value = isPodcast ? row.transcript?.backend || "auto" : "auto";
      transcriptBackendInput.disabled = !isCurrentPodcast();
      transcriptBackendInput.addEventListener("change", (e) => {
        if (!isCurrentPodcast()) return;
        row.transcript.backend = e.target.value;
      });
      tdTranscriptBackend.appendChild(transcriptBackendInput);

      const tdTranscriptLanguages = document.createElement("td");
      const transcriptLanguagesInput = document.createElement("input");
      transcriptLanguagesInput.value = isPodcast ? joinCommaList(row.transcript?.languages) : "";
      transcriptLanguagesInput.addEventListener("input", (e) => {
        if (!isCurrentPodcast()) return;
        row.transcript.languages = parseCommaList(e.target.value);
      });
      transcriptLanguagesInput.disabled = !isCurrentPodcast();
      tdTranscriptLanguages.appendChild(transcriptLanguagesInput);

      const delBtn = document.createElement("button");
      delBtn.type = "button";
      delBtn.className = "secondary icon-btn";
      delBtn.textContent = "×";
      delBtn.setAttribute("title", t("actions.delete"));
      delBtn.addEventListener("click", () => {
        if (!window.confirm(t("confirmDelete"))) return;
        state.sources.rows.splice(index, 1);
        ensureSourceFiltered();
        if (state.sources.rows.length === 0) {
          state.sources.page = 1;
        }
        renderSourcesMode();
      });
      const tdDelete = document.createElement("td");
      tdDelete.className = "action-col-cell";
      tdDelete.appendChild(delBtn);

      tr.appendChild(tdId);
      tr.appendChild(tdType);
      tr.appendChild(tdName);
      tr.appendChild(tdUrl);
      tr.appendChild(tdEnabled);
      tr.appendChild(tdPriority);
      tr.appendChild(tdTopics);
      tr.appendChild(tdPlatform);
      tr.appendChild(tdTranscriptEnabled);
      tr.appendChild(tdTranscriptBackend);
      tr.appendChild(tdTranscriptLanguages);
      tr.appendChild(tdDelete);
      el.sourceTableBody.appendChild(tr);
    }

    renderSourcesSummary();
  }

  function renderTopicsTable() {
    const query = (el.topicSearch.value || "").trim().toLowerCase();
    const filtered = state.topics.rows
      .map((row, index) => ({ row, index }))
      .filter(({ row }) => {
        if (!query) return true;
        const haystack = `${row.id} ${row.label} ${row.description}`.toLowerCase();
        return haystack.includes(query);
      });
    state.topics.filtered = filtered;

    el.topicTableBody.innerHTML = "";
    if (filtered.length === 0) {
      const tr = document.createElement("tr");
      const td = document.createElement("td");
      td.colSpan = 7;
      td.textContent = t("searchHint");
      tr.appendChild(td);
      el.topicTableBody.appendChild(tr);
      return;
    }

    for (const item of filtered) {
      const { row, index } = item;
      const tr = document.createElement("tr");

      const idInput = document.createElement("input");
      idInput.value = row.id || "";
      idInput.addEventListener("input", (e) => {
        row.id = e.target.value;
      });
      const tdId = document.createElement("td");
      tdId.appendChild(idInput);

      const emojiInput = document.createElement("input");
      emojiInput.value = row.emoji || "";
      emojiInput.addEventListener("input", (e) => {
        row.emoji = e.target.value;
      });
      const tdEmoji = document.createElement("td");
      tdEmoji.appendChild(emojiInput);

      const labelInput = document.createElement("input");
      labelInput.value = row.label || "";
      labelInput.addEventListener("input", (e) => {
        row.label = e.target.value;
      });
      const tdLabel = document.createElement("td");
      tdLabel.appendChild(labelInput);

      const maxItemsInput = document.createElement("input");
      maxItemsInput.type = "number";
      maxItemsInput.min = "1";
      maxItemsInput.value = Number.isFinite(row.display?.max_items) ? String(row.display.max_items) : "8";
      maxItemsInput.addEventListener("input", (e) => {
        row.display.max_items = Math.max(1, Number(e.target.value || 0));
      });
      const tdMax = document.createElement("td");
      tdMax.appendChild(maxItemsInput);

      const styleSelect = document.createElement("select");
      const compact = document.createElement("option");
      compact.value = "compact";
      compact.textContent = t("topics.thStyleCompact");
      const detailed = document.createElement("option");
      detailed.value = "detailed";
      detailed.textContent = t("topics.thStyleDetailed");
      styleSelect.appendChild(compact);
      styleSelect.appendChild(detailed);
      styleSelect.value = row.display?.style || "detailed";
      styleSelect.addEventListener("change", (e) => {
        row.display.style = e.target.value;
      });
      const tdStyle = document.createElement("td");
      tdStyle.appendChild(styleSelect);

      const queryInput = document.createElement("input");
      queryInput.value = joinCommaList(row.search?.queries);
      queryInput.addEventListener("input", (e) => {
        row.search.queries = parseCommaList(e.target.value);
      });
      const tdQuery = document.createElement("td");
      tdQuery.appendChild(queryInput);

      const delBtn = document.createElement("button");
      delBtn.type = "button";
      delBtn.className = "secondary icon-btn";
      delBtn.textContent = "×";
      delBtn.setAttribute("title", t("actions.delete"));
      delBtn.addEventListener("click", () => {
        if (!window.confirm(t("confirmDelete"))) return;
        state.topics.rows.splice(index, 1);
        renderTopicsMode();
      });
      const tdDelete = document.createElement("td");
      tdDelete.className = "action-col-cell";
      tdDelete.appendChild(delBtn);

      tr.appendChild(tdId);
      tr.appendChild(tdEmoji);
      tr.appendChild(tdLabel);
      tr.appendChild(tdMax);
      tr.appendChild(tdStyle);
      tr.appendChild(tdQuery);
      tr.appendChild(tdDelete);
      el.topicTableBody.appendChild(tr);
    }
  }

  function buildSourcesPayload() {
    const copy = {
      ...state.sources.raw,
      sources: state.sources.rows.map((row) => ({
        ...row,
        topics: Array.isArray(row.topics) ? row.topics.slice() : [],
        enabled: !!row.enabled,
        priority: !!row.priority,
      })),
    };
    delete copy.pretty;
    return copy;
  }

  function buildTopicsPayload() {
    const copy = {
      ...state.topics.raw,
      topics: state.topics.rows.map((row) => ({
        ...row,
        display: {
          ...(row.display || {}),
          max_items: Number(row.display?.max_items) || 8,
          style: row.display?.style || "detailed",
        },
        search: {
          ...(row.search || {}),
          queries: Array.isArray(row.search?.queries) ? row.search.queries.slice() : [],
        },
      })),
    };
    return copy;
  }

  function syncSourceJsonFromState() {
    el.sourceJsonText.value = JSON.stringify(buildSourcesPayload(), null, 2);
  }

  function syncTopicJsonFromState() {
    el.topicJsonText.value = JSON.stringify(buildTopicsPayload(), null, 2);
  }

  function syncSourceFromJson() {
    try {
      const payload = JSON.parse(el.sourceJsonText.value);
      if (!payload || !Array.isArray(payload.sources)) {
        setStatus(el.sourceStatus, t("noSourceData"), false);
        return false;
      }
      state.sources.raw = payload;
      state.sources.rows = payload.sources.map(normalizeSource);
      syncSourceTypeFilterOptions();
      ensureSourceFiltered();
      renderSourcesTable();
      setStatus(el.sourceStatus, t("loaded"), true);
      return true;
    } catch (error) {
      setStatus(el.sourceStatus, `${t("parseError")}: ${error.message}`, false);
      return false;
    }
  }

  function syncTopicFromJson() {
    try {
      const payload = JSON.parse(el.topicJsonText.value);
      if (!payload || !Array.isArray(payload.topics)) {
        setStatus(el.topicStatus, t("noTopicData"), false);
        return false;
      }
      state.topics.raw = payload;
      state.topics.rows = payload.topics.map(normalizeTopic);
      renderTopicsTable();
      setStatus(el.topicStatus, t("loaded"), true);
      return true;
    } catch (error) {
      setStatus(el.topicStatus, `${t("parseError")}: ${error.message}`, false);
      return false;
    }
  }

  function updateSourceModeUI() {
    const isTable = state.sources.mode === "table";
    el.sourceModeTable.hidden = !isTable;
    el.sourceModeJson.hidden = isTable;
    el.toggleSourceModeBtn.textContent = isTable ? t("actions.jsonMode") : t("actions.tableMode");
    if (isTable) {
      ensureSourceFiltered();
      renderSourcesTable();
    }
  }

  function updateTopicModeUI() {
    const isTable = state.topics.mode === "table";
    el.topicModeTable.hidden = !isTable;
    el.topicModeJson.hidden = isTable;
    el.toggleTopicModeBtn.textContent = isTable ? t("actions.jsonMode") : t("actions.tableMode");
    if (isTable) {
      renderTopicsTable();
    }
  }

  function renderSourcesMode() {
    renderSourcesTable();
    if (state.sources.mode === "table") {
      renderSourcesSummary();
    }
  }

  function renderTopicsMode() {
    if (state.topics.mode === "table") {
      renderTopicsTable();
    }
  }

  function setSourcePage(page) {
    const total = state.sources.filtered.length;
    const maxPage = Math.max(1, Math.ceil(total / PAGE_SIZE));
    state.sources.page = Math.min(Math.max(page, 1), maxPage);
    renderSourcesTable();
  }

  function updateCommonHeaders() {
    const labels = document.querySelectorAll("[data-i18n-key]");
  }

  async function requestJSON(url, options = {}) {
    const res = await fetch(url, options);
    const json = await res.json();
    if (!res.ok || json.ok === false) {
      const err = json?.error || `${res.status} ${res.statusText}`;
      throw new Error(err);
    }
    return json;
  }

  async function loadSourcesFromServer() {
    const response = await requestJSON(`/api/file?key=${state.sources.key}`);
    if (!response.ok || !response.content || !Array.isArray(response.content.sources)) {
      throw new Error(t("invalidData"));
    }
    state.sources.raw = response.content;
    state.sources.rows = response.content.sources.map(normalizeSource);
    state.sources.page = 1;
    syncSourceTypeFilterOptions();
    ensureSourceFiltered();
    if (state.sources.mode === "json") syncSourceJsonFromState();
    else renderSourcesMode();
  }

  async function loadTopicsFromServer() {
    const response = await requestJSON(`/api/file?key=${state.topics.key}`);
    if (!response.ok || !response.content || !Array.isArray(response.content.topics)) {
      throw new Error(t("invalidData"));
    }
    state.topics.raw = response.content;
    state.topics.rows = response.content.topics.map(normalizeTopic);
    if (state.topics.mode === "json") syncTopicJsonFromState();
    else renderTopicsMode();
  }

  async function loadAll() {
    setGlobalStatus(t("refresh"), true);
    try {
      await Promise.all([loadSourcesFromServer(), loadTopicsFromServer()]);
      setGlobalStatus(t("loaded"), true);
    } catch (error) {
      setGlobalStatus(`${t("loadFailed")}: ${error.message}`, false);
    }
  }

  async function saveSources() {
    try {
      setStatus(el.sourceStatus, t("saveHint"), true);
      let payload = buildSourcesPayload();
      if (state.sources.mode === "json") {
        const parsed = JSON.parse(el.sourceJsonText.value);
        if (!parsed || !Array.isArray(parsed.sources)) {
          throw new Error(t("noSourceData"));
        }
        payload = parsed;
        state.sources.raw = parsed;
        state.sources.rows = parsed.sources.map(normalizeSource);
      }
      if (!Array.isArray(payload.sources)) throw new Error(t("noSourceData"));
      await requestJSON("/api/file", {
        method: "POST",
        headers: { "Content-Type": "application/json;charset=utf-8" },
        body: JSON.stringify({ key: "sources", content: payload }),
      });
      setStatus(el.sourceStatus, t("saveSuccess"), true);
      await loadSourcesFromServer();
    } catch (error) {
      setStatus(el.sourceStatus, `${t("saveFailed")}: ${error.message}`, false);
    }
  }

  async function saveTopics() {
    try {
      setStatus(el.topicStatus, t("saveHint"), true);
      let payload = buildTopicsPayload();
      if (state.topics.mode === "json") {
        const parsed = JSON.parse(el.topicJsonText.value);
        if (!parsed || !Array.isArray(parsed.topics)) {
          throw new Error(t("noTopicData"));
        }
        payload = parsed;
        state.topics.raw = parsed;
        state.topics.rows = parsed.topics.map(normalizeTopic);
      }
      if (!Array.isArray(payload.topics)) throw new Error(t("noTopicData"));
      await requestJSON("/api/file", {
        method: "POST",
        headers: { "Content-Type": "application/json;charset=utf-8" },
        body: JSON.stringify({ key: "topics", content: payload }),
      });
      setStatus(el.topicStatus, t("saveSuccess"), true);
      await loadTopicsFromServer();
    } catch (error) {
      setStatus(el.topicStatus, `${t("saveFailed")}: ${error.message}`, false);
    }
  }

  function initEvents() {
    el.langBtn.addEventListener("click", () => {
      state.lang = state.lang === "zh" ? "en" : "zh";
      updateI18n();
      updateSourceModeUI();
      updateTopicModeUI();
    });

    el.loadAllBtn.addEventListener("click", loadAll);
    el.addSourceBtn.addEventListener("click", () => {
      state.sources.rows.push(
        normalizeSource({
          id: `custom-${Date.now()}`,
          type: "rss",
          enabled: true,
          priority: false,
          topics: [],
        }),
      );
      state.sources.page = 1;
      syncSourceTypeFilterOptions();
      ensureSourceFiltered();
      renderSourcesMode();
    });
    el.addTopicBtn.addEventListener("click", () => {
      state.topics.rows.push(
        normalizeTopic({
          id: `topic-${Date.now()}`,
          emoji: "🧩",
          label: "",
          display: { max_items: 8, style: "detailed" },
          search: { queries: [] },
        }),
      );
      renderTopicsMode();
    });

    el.sourceSearch.addEventListener("input", () => {
      state.sources.page = 1;
      ensureSourceFiltered();
      renderSourcesMode();
    });
    el.sourceTypeFilter.addEventListener("change", () => {
      state.sources.typeFilter = el.sourceTypeFilter.value;
      state.sources.page = 1;
      ensureSourceFiltered();
      renderSourcesMode();
    });
    el.topicSearch.addEventListener("input", () => {
      renderTopicsMode();
    });

    el.sourcePrevBtn.addEventListener("click", () => {
      setSourcePage(state.sources.page - 1);
    });
    el.sourceNextBtn.addEventListener("click", () => {
      setSourcePage(state.sources.page + 1);
    });

    el.toggleSourceModeBtn.addEventListener("click", () => {
      if (state.sources.mode === "table") {
        syncSourceJsonFromState();
        state.sources.mode = "json";
        updateSourceModeUI();
      } else {
        if (!syncSourceFromJson()) return;
        state.sources.mode = "table";
        updateSourceModeUI();
      }
    });

    el.toggleTopicModeBtn.addEventListener("click", () => {
      if (state.topics.mode === "table") {
        syncTopicJsonFromState();
        state.topics.mode = "json";
        updateTopicModeUI();
      } else {
        if (!syncTopicFromJson()) return;
        state.topics.mode = "table";
        updateTopicModeUI();
      }
    });

    el.saveSourcesBtn.addEventListener("click", saveSources);
    el.saveTopicsBtn.addEventListener("click", saveTopics);
  }

  async function bootstrap() {
    updateI18n();
    initEvents();
    await loadAll();
    updateSourceModeUI();
    updateTopicModeUI();
  }

  bootstrap();
})();
