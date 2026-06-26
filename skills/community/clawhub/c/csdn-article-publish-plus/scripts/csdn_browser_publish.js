#!/usr/bin/env node
const { chromium } = require("playwright");
const fs = require("fs");
const os = require("os");
const path = require("path");

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const k = argv[i];
    if (!k.startsWith("--")) continue;
    const key = k.slice(2);
    const v = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : "true";
    args[key] = v;
  }
  return args;
}

function loadSkillConfig() {
  const configPath = path.join(__dirname, "..", "skill-config.json");
  if (!fs.existsSync(configPath)) return { path: configPath, data: {} };
  try {
    const data = JSON.parse(fs.readFileSync(configPath, "utf8"));
    return { path: configPath, data };
  } catch (_) {
    return { path: configPath, data: {} };
  }
}

function normalizeMarkdown(raw) {
  let text = raw.replace(/\r\n/g, "\n");
  text = text.replace(/^---[\s\S]*?---\n+/m, "");
  text = text.replace(/\n{3,}/g, "\n\n");
  return text.trim() + "\n";
}

function typesetMarkdown(markdown, profile = "readable") {
  let text = markdown.replace(/\t/g, "  ");

  // 统一标题与列表/段落之间的空行，避免 CSDN 编辑器渲染拥挤
  text = text
    .replace(/\n(#{1,6}\s[^\n]+)\n(?!\n)/g, "\n$1\n\n")
    .replace(/\n([*+-]\s[^\n]+)\n(?![*+\-\n])/g, "\n$1\n\n")
    .replace(/\n(\d+\.\s[^\n]+)\n(?!\d+\.|\n)/g, "\n$1\n\n");

  // 代码围栏前后补空行，降低粘连
  text = text
    .replace(/([^\n])\n```/g, "$1\n\n```")
    .replace(/```\n([^\n])/g, "```\n\n$1");

  // 文末收敛
  text = text.replace(/\n{3,}/g, "\n\n").trimEnd() + "\n";

  if (profile === "compact") {
    // 紧凑模式：压缩空行，适合短文
    text = text.replace(/\n{3,}/g, "\n\n");
  }

  return text;
}

function buildWechatSection(qrUrl, description) {
  if (qrUrl) {
    const desc = description || "欢迎关注公众号，获取更多相关内容。";
    return [
      "",
      "---",
      "",
      "## 关注公众号",
      "",
      desc,
      "",
      `![微信公众号二维码](${qrUrl})`,
      "",
    ].join("\n");
  }
  return [
    "",
    "---",
    "",
    "## 关注公众号",
    "",
    "> 请添加公众号二维码图片及相关说明。",
    ">",
    "> 请在技能配置文件中补充二维码配置后重试：",
    "> `skill-config.json -> env.CSDN_VERTICAL_QR_IMAGE_URL`",
    "> （可选：`env.CSDN_VERTICAL_QR_DESCRIPTION`）",
    "",
  ].join("\n");
}

function appendWechatSection(markdown, qrUrl, description) {
  const marker = "## 关注公众号";
  const section = buildWechatSection(qrUrl, description);
  if (markdown.includes(marker)) {
    const idx = markdown.indexOf(marker);
    const prefix = markdown.slice(0, idx).trimEnd();
    return `${prefix}${section}`;
  }
  return `${markdown.trimEnd()}${section}`;
}

function resolveProfileDir(browserName, customProfileDir) {
  if (customProfileDir) return customProfileDir;
  if (browserName === "chrome") {
    return path.join(os.homedir(), "Library", "Application Support", "Google", "Chrome");
  }
  return path.join(os.homedir(), "Library", "Application Support", "Microsoft Edge");
}

async function clickAny(page, selectors) {
  for (const s of selectors) {
    const loc = page.locator(s).first();
    if (await loc.count()) {
      try {
        await loc.click({ timeout: 3000 });
        return s;
      } catch (_) {}
    }
  }
  return "";
}

async function fillEditor(page, title, markdown) {
  const titleInput = page.locator("input[placeholder*='标题'], input[placeholder*='title']").first();
  if (await titleInput.count()) {
    await titleInput.fill(title);
  }

  await page.evaluate((content) => {
    const textareas = Array.from(document.querySelectorAll("textarea")).filter((el) => {
      const r = el.getBoundingClientRect();
      return r.width > 300 && r.height > 180 && !el.disabled && !el.readOnly;
    });
    if (textareas.length > 0) {
      textareas.sort((a, b) => {
        const ra = a.getBoundingClientRect();
        const rb = b.getBoundingClientRect();
        return rb.width * rb.height - ra.width * ra.height;
      });
      const editor = textareas[0];
      editor.focus();
      editor.value = content;
      editor.dispatchEvent(new Event("input", { bubbles: true }));
      editor.dispatchEvent(new Event("change", { bubbles: true }));
      return;
    }

    const editable =
      document.querySelector(".cm-content[contenteditable='true']") ||
      document.querySelector("[contenteditable='true']");
    if (editable) {
      editable.focus();
      document.execCommand("selectAll", false);
      document.execCommand("insertText", false, content);
      editable.dispatchEvent(new Event("input", { bubbles: true }));
    }
  }, markdown);
}

async function applyPageTypeset(page) {
  const actions = {
    closeAiPanel: "",
    openPreview: "",
  };

  actions.closeAiPanel = await clickAny(page, [
    "button[aria-label='关闭']",
    ".ai-assistant-panel .close",
    "span:has-text('AI助手') + * button",
  ]);

  actions.openPreview = await clickAny(page, [
    "button:has-text('预览')",
    "span:has-text('预览')",
    "[class*='preview']",
  ]);

  return actions;
}

async function main() {
  const args = parseArgs(process.argv);
  const mode = args.mode || "draft-preview"; // draft | draft-preview | publish
  const browserName = args.browser || "edge"; // edge | chrome
  const channel = browserName === "chrome" ? "chrome" : "msedge";
  const typesetEnabled = args.typeset !== "false";
  const typesetProfile = args["typeset-profile"] || "readable"; // readable | compact
  const pageTypesetEnabled = args["page-typeset"] !== "false";
  const skillConfig = loadSkillConfig();

  if (!args.file) {
    throw new Error("缺少 --file 参数");
  }
  const file = path.resolve(args.file);
  if (!fs.existsSync(file)) {
    throw new Error(`文件不存在: ${file}`);
  }

  const title = args.title || path.basename(file, path.extname(file));
  const qrEnvName = "CSDN_VERTICAL_QR_IMAGE_URL";
  const descEnvName = "CSDN_VERTICAL_QR_DESCRIPTION";
  const qrUrl = (skillConfig.data.env && skillConfig.data.env[qrEnvName]) || "";
  const qrDesc = (skillConfig.data.env && skillConfig.data.env[descEnvName]) || "";
  const markdown = appendWechatSection(
    normalizeMarkdown(fs.readFileSync(file, "utf8")),
    qrUrl,
    qrDesc
  );
  const finalMarkdown = typesetEnabled ? typesetMarkdown(markdown, typesetProfile) : markdown;
  const profileDir = resolveProfileDir(browserName, args["profile-dir"]);
  const keepOpen = args["keep-open"] !== "false";
  const articleId = args["article-id"];
  const editorUrl = articleId
    ? `https://editor.csdn.net/md/?articleId=${articleId}`
    : "https://editor.csdn.net/md/";

  const context = await chromium.launchPersistentContext(profileDir, {
    headless: false,
    channel,
  });
  const page = context.pages()[0] || (await context.newPage());
  await page.goto(editorUrl, { waitUntil: "domcontentloaded", timeout: 120000 });
  await page.waitForTimeout(3500);

  await fillEditor(page, title, finalMarkdown);
  await page.waitForTimeout(1000);

  const publishOpen = await clickAny(page, [
    "button:has-text('发布文章')",
    "button:has-text('发布')",
  ]);

  let saveDraft = "";
  let confirmPublish = "";
  let previewBtn = "";
  let closeModal = "";
  let pageTypesetActions = {};

  if (mode === "draft" || mode === "draft-preview") {
    saveDraft = await clickAny(page, [
      "button:has-text('保存为草稿')",
      "button:has-text('存草稿')",
    ]);
    await page.waitForTimeout(1200);
  }

  if (mode === "draft-preview") {
    closeModal = await clickAny(page, [
      "button:has-text('取消')",
      ".el-dialog__headerbtn",
      "button[aria-label='Close']",
    ]);
    previewBtn = await clickAny(page, [
      "button:has-text('预览')",
      "span:has-text('预览')",
      "[class*='preview']",
    ]);
    if (pageTypesetEnabled) {
      pageTypesetActions = await applyPageTypeset(page);
    }
  }

  if (mode === "publish") {
    confirmPublish = await clickAny(page, [
      "button:has-text('确认并发布')",
      "button:has-text('确认发布')",
      "button:has-text('确定发布')",
      "button:has-text('提交发布')",
      ".el-dialog__footer button.el-button--primary",
    ]);
  }

  const screenshot = path.join(process.cwd(), `csdn_${mode}_result.png`);
  await page.waitForTimeout(2000);
  await page.screenshot({ path: screenshot, fullPage: true });

  const result = {
    mode,
    browser: browserName,
    url: page.url(),
    publishOpen,
    saveDraft,
    confirmPublish,
    closeModal,
    previewBtn,
    screenshot,
    wechatQrEnv: qrEnvName,
    wechatQrConfigured: Boolean(qrUrl),
    configPath: skillConfig.path,
    typesetEnabled,
    typesetProfile,
    pageTypesetEnabled,
    pageTypesetActions,
  };
  console.log(JSON.stringify(result, null, 2));

  if (!keepOpen) {
    await context.close();
  } else {
    process.stdin.resume();
  }
}

main().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
