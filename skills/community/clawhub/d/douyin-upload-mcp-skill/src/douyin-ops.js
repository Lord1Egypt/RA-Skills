/**
 * douyin-ops.js — 抖音操作高层 API
 *
 * 职责：
 *   基于 operator.js 的底层原子操作，编排抖音创作者平台的业务流程。
 *   全部通过 CDP 实现，不往页面注入任何对象。
 */
import { createOperator } from './operator.js';
import { sleep } from './util.js';
import config from './config.js';
import { existsSync } from 'node:fs';
import { join, resolve as pathResolve, normalize as pathNormalize } from 'node:path';
import { spawnSync } from 'node:child_process';

// ── 抖音创作者平台页面元素选择器 ──
const SELECTORS = {
  /** 左上角「高清发布」按钮 — 点击后进入上传页 */
  hdPublishBtn: [
    'button[class*="douyin-creator-master-button"]',
    '#douyin-creator-master-side-upload-wrap button',
    'button.header-button-KP2xn1',
  ],
  /** 标题输入框（标准 input） */
  titleInput: [
    'input[placeholder*="作品标题"]',
    'input.semi-input-default[placeholder*="标题"]',
    'input[placeholder*="标题"]',
  ],
  /** 作品简介（slate 富文本编辑器，contenteditable div） */
  descriptionInput: [
    'div[data-placeholder*="作品简介"][contenteditable="true"]',
    'div[data-placeholder*="添加作品简介"][contenteditable="true"]',
    'div.editor-kit-container[contenteditable="true"]',
    'div[contenteditable="true"][data-slate-editor="true"]',
  ],
  /** 用户头像（登录状态指示） */
  userAvatar: [
    '[class*="avatar"]',
    'img[class*="avatar"]',
  ],
  /** 上传区域容器（包裹上传按钮和拖拽区） */
  uploadContainer: [
    'div[class*="drag-upload"]',
  ],
  /** 上传区域内的 file input（隐藏的，通过 CDP 直接设置文件） */
  uploadFileInput: [
    'div[class*="drag-upload"] input[type="file"]',
    'input[type="file"]',
  ],
  /** 「上传视频」按钮 — 发布视频 tab 下的入口 */
  uploadVideoBtn: [
    'div[class*="drag-upload"] button:has-text("上传视频")',
    'button[class*="container-drag-btn"]:has-text("上传视频")',
  ],
  /** 「上传图文」按钮 — 发布图文 tab 下的入口 */
  uploadImageTextBtn: [
    'div[class*="drag-upload"] button:has-text("上传图文")',
    'button[class*="container-drag-btn"]:has-text("上传图文")',
  ],
  /** 「我要发文」按钮 — 发布文章 tab 下的入口 */
  publishArticleBtn: [
    'div[class*="drag-upload"] button:has-text("我要发文")',
    'button[class*="container-drag-btn"]:has-text("我要发文")',
  ],
  /** 侧边栏导航 */
  sideNav: [
    'aside.sider-EdbKED',
    '[class*="sider"]',
    'aside',
  ],
  /** 发布类型 tab — 通用（匹配任意 tab 项） */
  publishTab: [
    'div[class*="tab-item"]',
  ],
  /** 发布类型 tab：发布视频 */
  tabVideo: [
    'div[class*="tab-item"]:has-text("发布视频")',
  ],
  /** 发布类型 tab：发布图文 */
  tabImageText: [
    'div[class*="tab-item"]:has-text("发布图文")',
  ],
  /** 发布类型 tab：发布文章 */
  tabArticle: [
    'div[class*="tab-item"]:has-text("发布文章")',
  ],
};

function normalizeTopicList(topics) {
  const raw = Array.isArray(topics)
    ? topics
    : String(topics || '').split(/(?=#)|[,，、\s]+/);
  const cleaned = raw
    .map((item) => String(item || '').trim().replace(/^#+/, '').trim())
    .filter(Boolean);
  return [...new Set(cleaned)];
}

function normalizePublishTitle(title, maxLength = 60) {
  const clean = String(title || '')
    .replace(/#[^\s#，。,;；!！?？)）(（]+/g, '')
    .replace(/\s+/g, ' ')
    .replace(/[，,、；;：:|｜\\/-]+$/g, '')
    .trim();
  const limit = Number.isFinite(Number(maxLength)) && Number(maxLength) > 0
    ? Number(maxLength)
    : 60;
  return Array.from(clean).slice(0, limit).join('');
}

function closeBrowserNativePrompts() {
  const script = join(process.env.HOME || '.', '.openclaw', 'skills', 'douyin-upload-mcp-skill', 'scripts', 'close-browser-prompts.py');
  const result = spawnSync('python3', [script], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: 3000,
  });
  return {
    ok: result.status === 0,
    status: result.status,
    output: `${result.stdout || ''}${result.stderr || ''}`.trim(),
  };
}

async function safeDismissBeforeUnload(dialog) {
  if (dialog.type() !== 'beforeunload') return false;
  await dialog.dismiss().catch(() => {});
  return true;
}

async function safeAcceptBeforeUnload(dialog) {
  if (dialog.type() !== 'beforeunload') return false;
  await dialog.accept().catch(() => {});
  return true;
}

/**
 * 创建抖音操作实例
 * @param {import('puppeteer-core').Page} page
 */
export function createOps(page) {
  const op = createOperator(page);

  return {
    /** 暴露底层 operator */
    operator: op,

    /** 暴露选择器定义 */
    selectors: SELECTORS,

    /**
     * 探测页面各元素是否就位
     */
    async probe() {
      const [hdPublishBtn, titleInput, descriptionInput, userAvatar, sideNav, uploadContainer] = await Promise.all([
        op.locate(SELECTORS.hdPublishBtn),
        op.locate(SELECTORS.titleInput),
        op.locate(SELECTORS.descriptionInput),
        op.locate(SELECTORS.userAvatar),
        op.locate(SELECTORS.sideNav),
        op.locate(SELECTORS.uploadContainer),
      ]);

      const url = op.url();
      const isCreatorPage = url.includes('creator.douyin.com');

      return {
        hdPublishBtn: hdPublishBtn.found,
        titleInput: titleInput.found,
        descriptionInput: descriptionInput.found,
        userAvatar: userAvatar.found,
        sideNav: sideNav.found,
        uploadContainer: uploadContainer.found,
        currentUrl: url,
        isCreatorPage,
      };
    },

    /**
     * 切换到上传页
     *
     * 点击左上角「高清发布」按钮，页面切换到视频/图文上传界面。
     * 点击后等待页面导航完成（URL 变为 content/upload）。
     *
     * @param {object} [opts]
     * @param {number} [opts.timeout=15000] - 等待页面切换完成的超时
     * @returns {Promise<{ok: boolean, url?: string, elapsed?: number, error?: string}>}
     */
    async goUploadPage(opts = {}) {
      const { timeout = 30_000, force = false } = opts;
      const start = Date.now();

      // 如果已经在上传页，直接返回
      const currentUrl = op.url();
      if (currentUrl.includes('content/upload')) {
        console.log('[ops] 已在上传页');
        return { ok: true, url: currentUrl, elapsed: 0, alreadyThere: true };
      }

      if (currentUrl.includes('/content/post/video')) {
        const editorState = await this._getPublishEditState().catch(() => null);
        if (!force) {
          return {
            ok: false,
            error: 'editor_has_unpublished_changes',
            message: '当前仍在发布编辑页，为避免触发浏览器“离开页面”弹窗，已停止跳转上传页。',
            state: editorState,
            url: currentUrl,
            elapsed: Date.now() - start,
          };
        }
        const onDialog = async (dialog) => {
          if (await safeAcceptBeforeUnload(dialog)) {
            console.warn('[ops] 检测到离开页面确认弹窗，已确认离开旧草稿。');
          }
        };
        op.page.on('dialog', onDialog);
        try {
          await op.page.goto('https://creator.douyin.com/creator-micro/content/upload', {
            waitUntil: 'domcontentloaded',
            timeout,
          });
        } catch {
          // Continue with whatever the SPA rendered.
        }
        const arrived = await op.waitFor(() => window.location.href.includes('content/upload'), { timeout, interval: 500 });
        op.page.off('dialog', onDialog);
        if (arrived.ok) {
          return { ok: true, url: op.url(), elapsed: Date.now() - start, fromEditor: true };
        }
        return {
          ok: false,
          error: 'editor_navigation_blocked',
          message: '尝试离开编辑页时被页面拦截，已保留当前编辑页。',
          url: op.url(),
          elapsed: Date.now() - start,
        };
      }

      const waitForUploadPage = async (waitTimeout) => op.waitFor(() => {
        const text = document.body?.innerText || '';
        const hasUploadArea = Boolean(document.querySelector('input[type="file"]'))
          && /发布视频|上传视频|拖拽到此处上传/.test(text);
        return window.location.href.includes('content/upload') || hasUploadArea;
      }, { timeout: waitTimeout, interval: 500 });

      // 优先点击「高清发布」，保留站内 SPA 正常路径；失败或超时后直接进入上传 URL。
      const clickResult = await op.click(SELECTORS.hdPublishBtn, { jitter: 4, delayBeforeClick: 80 });
      let waitResult = clickResult.ok ? await waitForUploadPage(Math.min(timeout, 12_000)) : { ok: false };
      if (!waitResult.ok) {
        console.warn(`[ops] 高清发布入口未进入上传页，改用直达上传页: ${clickResult.ok ? 'timeout' : clickResult.error}`);
        try {
          await op.page.goto('https://creator.douyin.com/creator-micro/content/upload', {
            waitUntil: 'domcontentloaded',
            timeout,
          });
        } catch {
          // Continue with whatever the SPA rendered.
        }
        waitResult = await waitForUploadPage(timeout);
      }

      if (!waitResult.ok) {
        return {
          ok: false,
          error: clickResult.ok ? 'upload_page_timeout' : 'hd_publish_btn_not_found',
          elapsed: Date.now() - start,
          currentUrl: op.url(),
          click: clickResult,
        };
      }

      await sleep(800); // 等 UI 稳定

      console.log('[ops] 已切换到上传页');
      return { ok: true, url: op.url(), elapsed: Date.now() - start, click: clickResult.ok ? clickResult : undefined };
    },

    async resumeUnpublishedDraft() {
      const target = await op.query(() => {
        const text = document.body?.innerText || '';
        if (!/你还有上次未发布的视频，是否继续编辑/.test(text)) return { found: false };
        const visible = (el) => {
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const el = [...document.querySelectorAll('button, div, span, a')]
          .filter(visible)
          .filter((node) => (node.textContent || '').replace(/\s+/g, '').trim() === '继续编辑')
          .sort((a, b) => {
            const ar = a.getBoundingClientRect();
            const br = b.getBoundingClientRect();
            return (ar.width * ar.height) - (br.width * br.height);
          })[0];
        if (!el) return { found: false, hasDraftPrompt: true };
        const rect = el.getBoundingClientRect();
        return {
          found: true,
          x: rect.x + rect.width / 2,
          y: rect.y + rect.height / 2,
          text: (el.textContent || '').trim(),
        };
      });
      if (!target.found) return { ok: false, ...target };
      closeBrowserNativePrompts();
      await sleep(200);
      await op.page.mouse.click(target.x, target.y);
      const changed = await op.waitFor(() => {
        const text = document.body?.innerText || '';
        return location.href.includes('/content/post/video') || /基础信息|作品描述|发布设置|作品标题/.test(text);
      }, { timeout: 15_000, interval: 500 });
      return { ok: changed.ok, target, url: op.url(), result: changed.result };
    },

    async abandonUnpublishedDraft() {
      const target = await op.query(() => {
        const text = document.body?.innerText || '';
        if (!/你还有上次未发布的视频，是否继续编辑/.test(text)) return { found: false };
        const visible = (el) => {
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const el = [...document.querySelectorAll('button, div, span, a')]
          .filter(visible)
          .filter((node) => (node.textContent || '').replace(/\s+/g, '').trim() === '放弃')
          .sort((a, b) => {
            const ar = a.getBoundingClientRect();
            const br = b.getBoundingClientRect();
            return (ar.width * ar.height) - (br.width * br.height);
          })[0];
        if (!el) return { found: false, hasDraftPrompt: true };
        const rect = el.getBoundingClientRect();
        return {
          found: true,
          x: rect.x + rect.width / 2,
          y: rect.y + rect.height / 2,
          text: (el.textContent || '').trim(),
        };
      });
      if (!target.found) return { ok: false, ...target };
      closeBrowserNativePrompts();
      await sleep(200);
      await op.page.mouse.click(target.x, target.y);
      const gone = await op.waitFor(() => {
        const text = document.body?.innerText || '';
        return !/你还有上次未发布的视频，是否继续编辑/.test(text);
      }, { timeout: 5000, interval: 300 });
      return { ok: gone.ok, target, url: op.url(), promptGone: gone.ok };
    },

    /**
     * 切换发布类型（视频 / 图文 / 文章）
     *
     * 点击上传页顶部的 tab 切换发布类型。
     * 若当前 tab 已经是目标类型则跳过。
     *
     * @param {'video'|'imagetext'|'article'} type - 目标发布类型
     * @returns {Promise<{ok: boolean, type?: string, error?: string}>}
     */
    async switchPublishType(type) {
      const tabMap = {
        //  这里先暂时不支持全景视频，估计也没啥人发吧
        video:     { selectors: SELECTORS.tabVideo,     label: '发布视频' },
        imagetext: { selectors: SELECTORS.tabImageText, label: '发布图文' },
        article:   { selectors: SELECTORS.tabArticle,   label: '发布文章' },
      };

      const target = tabMap[type];
      if (!target) {
        return { ok: false, error: `unknown_type: ${type}，可选: video / imagetext / article` };
      }

      // 等待 tab 元素渲染出来（首次进入上传页时 tab 可能还未加载）
      const tabReady = await op.waitFor((label) => {
        const tabs = [...document.querySelectorAll('div[class*="tab-item"]')];
        return tabs.some(t => t.textContent?.includes(label));
      }, { timeout: 10_000, interval: 500, args: [target.label] });

      if (!tabReady.ok) {
        return { ok: false, error: `tab_not_found: ${target.label}（等待 10s 未出现）` };
      }

      // 检查当前激活的 tab 是否已经是目标类型
      const isActive = await op.query((label) => {
        const tabs = [...document.querySelectorAll('div[class*="tab-item"]')];
        const target = tabs.find(t => t.textContent?.includes(label));
        if (!target) return false;
        return target.className.includes('active');
      }, target.label);

      if (isActive) {
        console.log(`[ops] 当前已在「${target.label}」tab`);
        return { ok: true, type, alreadyActive: true };
      }

      // 点击目标 tab
      const clickResult = await op.click(target.selectors);
      if (!clickResult.ok) {
        return { ok: false, error: `tab_not_found: ${target.label}` };
      }

      await sleep(250); // 等 UI 切换稳定

      console.log(`[ops] 已切换到「${target.label}」`);
      return { ok: true, type };
    },

    /**
     * 发布视频
     *
     * 前置条件：需在上传页 + 「发布视频」tab。
     * 会自动切换到发布视频 tab，然后通过 file input 上传视频文件。
     *
     * @param {string} filePath - 视频文件绝对路径
     * @param {object} [opts] - 发布选项（标题、描述等，待后续扩展）
     * @returns {Promise<{ok: boolean, error?: string}>}
     */
    async publishVideo(filePath, opts = {}) {
      // 1. 确保在上传页
      const goResult = await this.goUploadPage({ force: Boolean(opts.freshUpload) });
      if (!goResult.ok) return goResult;

      let resumedDraft = false;
      if (opts.freshUpload) {
        for (let i = 0; i < 3; i += 1) {
          const abandonResult = await this.abandonUnpublishedDraft();
          if (!abandonResult.ok) {
            if (abandonResult.found || abandonResult.promptGone === false) {
              return { ok: false, error: 'draft_prompt_not_closed', detail: abandonResult, file: filePath };
            }
            break;
          }
          console.log('[ops] 已放弃上次未发布草稿，准备重新上传');
          await sleep(800);
        }
      } else {
        const draftResult = await this.resumeUnpublishedDraft();
        resumedDraft = draftResult.ok;
      }

      let elapsed = 0;
      if (!resumedDraft) {
        // 2. 切换到发布视频 tab
        const switchResult = await this.switchPublishType('video');
        if (!switchResult.ok) return switchResult;

        await sleep(500);

        // 3. 点击「上传视频」按钮，同时拦截文件选择对话框
        const uploadResult = await this._clickAndChooseFile(SELECTORS.uploadVideoBtn, [filePath]);
        if (!uploadResult.ok) return uploadResult;

        // 4. 等待视频上传完成（uploading-container 消失）
        console.log('[ops] 视频文件已塞入，等待上传完成...');
        const uploadTimeout = opts.timeout || 1_800_000; // 大视频上传和转码可能很慢，默认等 30 分钟。
        const uploadStart = Date.now();

        await sleep(250); // 短暂等待 UI 开始上传

        while (Date.now() - uploadStart < uploadTimeout) {
          const state = await this._getPublishEditState();
          if (state.blocked) {
            return { ok: false, error: state.blocked, detail: state.textSample, file: filePath };
          }
          if (state.uploadDone) break;
          await sleep(1000);
        }

        // 判断是否超时
        elapsed = Date.now() - uploadStart;
        const finalUploadState = await this._getPublishEditState();
        if (!finalUploadState.uploadDone) {
          return { ok: false, error: 'upload_timeout', detail: finalUploadState.textSample || `视频上传超时 (${uploadTimeout}ms)`, file: filePath };
        }
        console.log(`[ops] 视频上传完成 (${elapsed}ms): ${filePath}`);
      } else {
        console.log('[ops] 已继续编辑未发布草稿，跳过重新上传');
      }

      // 5. 设置封面：上游提供封面图时优先使用；否则回退 AI 推荐封面。
      const customCoverPath = opts.coverImagePath || opts.coverPath;
      const coverResult = customCoverPath
        ? await this.setCustomCover(customCoverPath)
        : await this.selectRecommendedCover();
      if (customCoverPath && !coverResult.ok) {
        return { ok: false, error: coverResult.error || 'custom_cover_failed', detail: coverResult, file: filePath };
      }

      // 6. 填写标题
      const { title, description } = opts;
      const topics = normalizeTopicList(opts.topics || opts.tags);
      if (title) {
        const titleResult = await this.fillTitle(title);
        if (!titleResult.ok) {
          return { ok: false, error: titleResult.error || 'title_fill_failed', detail: titleResult, file: filePath };
        }
      }

      // 7. 填写作品简介
      if (description) {
        const descResult = await this.fillDescription(description);
        if (!descResult.ok) {
          return { ok: false, error: descResult.error || 'description_fill_failed', detail: descResult, file: filePath };
        }
      }
      if (topics.length) {
        const topicsResult = await this.fillTopics(topics);
        if (!topicsResult.ok) {
          return { ok: false, error: topicsResult.error || 'topics_fill_failed', detail: topicsResult, file: filePath };
        }
      }

      // 8. 点击发布按钮；普通点击无效时兜底触发 React onClick。
      const assistantReady = await this._waitForPublishAssistantReady({ timeout: opts.assistantTimeout || 180_000 });
      if (!assistantReady.ok) {
        console.warn(`[ops] 发文助手未完全完成，继续尝试发布: ${assistantReady.error || assistantReady.state?.status}`);
      }
      const coverDialog = await this.confirmPendingCoverDialog();
      if (!coverDialog.ok) {
        return { ok: false, error: coverDialog.error || 'cover_apply_confirm_failed', detail: coverDialog, file: filePath };
      }
      await sleep(250);
      const publishResult = await this._clickPublishButton();
      if (publishResult.ok) {
        console.log(`[ops] 已触发发布按钮 (${publishResult.method})，检测发布结果...`);
      } else {
        return { ok: false, error: publishResult.error || 'publish_btn_not_found', detail: publishResult.detail, file: filePath };
      }

      // 9. 检测 toast、发布接口和管理页跳转，避免把“点击成功”误判成“发布成功”。
      const submitResult = await this._waitForPublishSubmit({ title, timeout: opts.publishTimeout || 60_000 });
      if (submitResult.ok) {
        console.log('[ops] ✅ 视频发布已提交');
        return { ok: true, type: 'video', file: filePath, elapsed, coverSelected: coverResult.ok, cover: coverResult, publish: submitResult };
      }
      console.error(`[ops] ❌ 视频发布未确认: ${submitResult.error}`);
      return { ok: false, error: submitResult.error, detail: submitResult.detail, file: filePath, publish: submitResult };
    },

    async selectRecommendedCover() {
      console.log('[ops] 等待 AI 封面生成完毕...');
      const coverReady = await op.waitFor(() => {
        const title = document.querySelector('span[class*="recommendTitle"]');
        if (!title) return false;
        return title.textContent && !title.textContent.includes('生成中');
      }, { timeout: 60_000, interval: 1000 });

      if (!coverReady.ok) {
        console.warn('[ops] AI 封面生成超时（60s），跳过封面选择');
      }

      await sleep(250);
      const coverResult = await op.click(['div[class*="recommendCoverContainer"] > div:first-child']);
      if (!coverResult.ok) {
        console.warn('[ops] 未找到推荐封面，跳过');
        return { ok: false, mode: 'auto_recommended', error: 'recommended_cover_not_found' };
      }

      console.log('[ops] 已点击推荐封面，等待确认弹窗...');
      await sleep(250);
      const confirmResult = await op.click(['div.semi-modal-footer button.semi-button-primary']);
      if (confirmResult.ok) {
        console.log('[ops] 已确认推荐封面');
        return { ok: true, mode: 'auto_recommended' };
      }
      console.warn('[ops] 未找到封面确认按钮，跳过');
      return { ok: true, mode: 'auto_recommended', warning: 'confirm_button_not_found' };
    },

    async setCustomCover(imagePath) {
      const file = pathResolve(pathNormalize(imagePath));
      if (!existsSync(file)) {
        return { ok: false, mode: 'custom_image', error: 'cover_file_not_found', file };
      }

      console.log(`[ops] 上传自定义封面: ${file}`);
      const inputHandle = await op.page.evaluateHandle(() => {
        const inputs = [...document.querySelectorAll('input[type="file"]')];
        return inputs.find((el) => /image\/png|image\/jpeg|image\/jpg|image\//i.test(el.accept || '')) || null;
      });
      const input = inputHandle.asElement();
      if (!input) {
        return { ok: false, mode: 'custom_image', error: 'cover_input_not_found', file };
      }

      await input.uploadFile(file);
      const modalReady = await op.waitFor(() => {
        const text = document.body?.innerText || '';
        return /设置封面/.test(text) && /保存/.test(text) && Boolean(document.querySelector('.ReactCrop__image, img[alt*="裁剪"]'));
      }, { timeout: 30_000, interval: 500 });
      if (!modalReady.ok) {
        return { ok: false, mode: 'custom_image', error: 'cover_crop_modal_timeout', file };
      }

      const saveTarget = await op.query(() => {
        const visible = (el) => {
          if (!el) return false;
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const buttons = [...document.querySelectorAll('button, div, span')]
          .filter(visible)
          .filter((el) => (el.innerText || el.textContent || '').replace(/\s+/g, '').trim() === '保存')
          .sort((a, b) => {
            const ar = a.getBoundingClientRect();
            const br = b.getBoundingClientRect();
            const ap = /primary/.test(a.className?.toString?.() || '') ? 0 : 1;
            const bp = /primary/.test(b.className?.toString?.() || '') ? 0 : 1;
            if (ap !== bp) return ap - bp;
            return (ar.width * ar.height) - (br.width * br.height);
          });
        const btn = buttons[0];
        if (!btn) return { found: false };
        const rect = btn.getBoundingClientRect();
        return {
          found: true,
          x: rect.x + rect.width / 2,
          y: rect.y + rect.height / 2,
          text: (btn.textContent || '').trim(),
        };
      });
      if (!saveTarget.found) {
        return { ok: false, mode: 'custom_image', error: 'cover_save_button_not_found', file };
      }

      closeBrowserNativePrompts();
      await sleep(200);
      await op.page.mouse.click(saveTarget.x, saveTarget.y);
      await sleep(500);
      const applyConfirm = await this.confirmPendingCoverDialog();
      if (!applyConfirm.ok) {
        return { ok: false, mode: 'custom_image', error: applyConfirm.error || 'cover_apply_confirm_failed_after_save', file, applyConfirm };
      }
      const saved = await op.waitFor(() => {
        const text = document.body?.innerText || '';
        const visible = (el) => {
          if (!el) return false;
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const modalVisible = [...document.querySelectorAll('.semi-modal, .semi-modal-wrap')]
          .some((el) => visible(el) && /设置封面/.test(el.innerText || ''));
        if (modalVisible) return false;
        const pageHtml = document.body?.innerHTML || '';
        if (/creator-media-private|tos-cn-i-jm8ajry58r|background-image:\s*url\(/i.test(pageHtml)) return true;
        const covers = [...document.querySelectorAll('[class*="coverControl"], [class*="cover-"]')];
        return covers.some((el) => {
          const html = el.innerHTML || '';
          const bg = [...el.querySelectorAll('*')]
            .some((child) => /url\(/i.test(getComputedStyle(child).backgroundImage || ''));
          return /background-image:\s*url\(/i.test(html) || bg;
        });
      }, { timeout: 30_000, interval: 500 });
      if (!saved.ok) {
        return { ok: false, mode: 'custom_image', error: 'cover_save_timeout', file };
      }

      const state = await op.query(() => {
        const covers = [...document.querySelectorAll('[class*="coverControl"], [class*="cover-"]')].map((el) => {
          const hasComputedBackground = [...el.querySelectorAll('*')]
            .some((child) => /url\(/i.test(getComputedStyle(child).backgroundImage || ''));
          return {
            text: (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim(),
            hasBackground: /background-image:\s*url\(/i.test(el.innerHTML || '') || hasComputedBackground,
          };
        });
        const html = document.body?.innerHTML || '';
        return {
          coverSlots: covers,
          hasCover: covers.some((item) => item.hasBackground) || /creator-media-private|tos-cn-i-jm8ajry58r/i.test(html),
        };
      });
      console.log('[ops] 已保存自定义封面');
      return { ok: Boolean(state.hasCover), mode: 'custom_image', file, state };
    },

    async confirmPendingCoverDialog() {
      const target = await op.query(() => {
        const text = document.body?.innerText || '';
        if (!/是否确认应用此封面/.test(text)) return { found: false };
        const visible = (el) => {
          if (!el) return false;
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const buttons = [...document.querySelectorAll('button, [role="button"], div, span')]
          .filter(visible)
          .filter((el) => /^确定$/.test((el.innerText || el.textContent || '').replace(/\s+/g, '').trim()))
          .filter((el) => {
            const parentText = (el.closest('.semi-modal, .semi-modal-wrap, [role="dialog"]')?.innerText || document.body?.innerText || '');
            return /是否确认应用此封面/.test(parentText);
          })
          .sort((a, b) => {
            const ar = a.getBoundingClientRect();
            const br = b.getBoundingClientRect();
            const ap = /primary/.test(String(a.className || '')) ? 0 : 1;
            const bp = /primary/.test(String(b.className || '')) ? 0 : 1;
            if (ap !== bp) return ap - bp;
            return (ar.width * ar.height) - (br.width * br.height);
          });
        const btn = buttons[0];
        if (!btn) return { found: true, ok: false, error: 'cover_apply_confirm_button_not_found' };
        const rect = btn.getBoundingClientRect();
        return { found: true, ok: true, x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
      });
      if (!target.found) return { ok: true, found: false };
      if (!target.ok) return target;
      closeBrowserNativePrompts();
      await sleep(200);
      await op.page.mouse.click(target.x, target.y);
      const closed = await op.waitFor(() => !/是否确认应用此封面/.test(document.body?.innerText || ''), { timeout: 10_000, interval: 300 });
      return { ok: Boolean(closed.ok), found: true, closed };
    },

    async publishCurrentDraft(opts = {}) {
      const title = opts.title || '';
      let lastDetail = null;
      for (let attempt = 1; attempt <= (opts.attempts || 4); attempt += 1) {
        const pageState = await op.query(() => {
          const text = document.body?.innerText || '';
          return {
            url: location.href,
            hasDraftPrompt: /你还有上次未发布的视频，是否继续编辑/.test(text),
            inEditor: location.href.includes('/content/post/video') || /基础信息|作品描述|发布设置|作品标题/.test(text),
            textSample: text.replace(/\s+/g, ' ').slice(0, 500),
          };
        });
        if (!pageState.inEditor || pageState.hasDraftPrompt) {
          if (!pageState.url.includes('/content/upload')) {
            const goResult = await this.goUploadPage();
            if (!goResult.ok) return goResult;
          }
          const draftResult = await this.resumeUnpublishedDraft();
          lastDetail = { attempt, pageState, draftResult };
          if (!draftResult.ok) {
            await sleep(1200);
            continue;
          }
          await sleep(1500);
        }

        const assistantReady = await this._waitForPublishAssistantReady({ timeout: opts.assistantTimeout || 180_000 });
        if (!assistantReady.ok) {
          console.warn(`[ops] 发文助手未完全完成，继续尝试发布: ${assistantReady.error || assistantReady.state?.status}`);
        }
        const coverDialog = await this.confirmPendingCoverDialog();
        if (!coverDialog.ok) {
          lastDetail = { attempt, coverDialog, assistantReady };
          await sleep(1000);
          continue;
        }
        const publishResult = await this._clickPublishButton();
        if (!publishResult.ok) {
          lastDetail = { attempt, publishResult, assistantReady };
          await sleep(1500);
          continue;
        }
        const submitResult = await this._waitForPublishSubmit({ title, timeout: opts.publishTimeout || 60_000 });
        if (submitResult.ok) {
          return { ok: true, type: 'video', publish: submitResult };
        }
        return { ok: false, error: submitResult.error, detail: submitResult.detail, publish: submitResult };
      }
      return { ok: false, error: 'publish_btn_not_found', detail: lastDetail };
    },

    async _getPublishAssistantState() {
      return op.query(() => {
        const text = document.body?.innerText || '';
        const compact = text.replace(/\s+/g, '');
        const uploadProgressMatch = compact.match(/(\d{1,3})%文件(?:解析|上传|处理中)|文件(?:解析|上传|处理中)[^0-9]{0,8}(\d{1,3})%/);
        const uploadPercent = uploadProgressMatch ? Number(uploadProgressMatch[1] || uploadProgressMatch[2]) : null;
        const uploadBusy = /上传过程中请不要删除\/移动文件|文件解析中|取消上传/.test(text)
          || /(?:文件|视频)(?:解析|上传|处理)中/.test(text)
          || (uploadPercent !== null && uploadPercent < 100);
        const percentMatch = compact.match(/(?:检测中|封面诊断中|作品检测中|诊断中)[^0-9]{0,10}(\d{1,3})%|发文助手[^0-9]{0,30}(\d{1,3})%/);
        const percent = percentMatch ? Number(percentMatch[1] || percentMatch[2]) : null;
        const finished = /作品未见异常|检测完成|快速检测[^\\n]{0,20}作品未见异常|结果由机器检测提供/.test(text);
        const failed = /作品检测失败|检测人数过多|抱歉，当前检测人数过多/.test(text);
        const running = uploadBusy || /检测中|封面诊断中|作品检测中|诊断中/.test(text) || (percent !== null && percent < 100);
        const visible = (el) => {
          if (!el) return false;
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const textOf = (el) => ((el.innerText || el.textContent || '').replace(/\s+/g, '').trim());
        const publishButtonVisible = [...document.querySelectorAll('button, [role="button"], a')]
          .filter(visible)
          .some((el) => textOf(el) === '发布' && !textOf(el).includes('高清发布'));
        return {
          ready: Boolean(!uploadBusy && !running && (finished || failed || /发布设置|点击发布后/.test(text))),
          running,
          uploadBusy,
          uploadPercent,
          finished,
          failed,
          percent,
          publishButtonVisible,
          status: failed ? 'failed' : (finished ? 'finished' : (running ? 'running' : 'unknown')),
          textSample: text.replace(/\s+/g, ' ').slice(0, 800),
        };
      });
    },

    async getPublishAssistantState() {
      return this._getPublishAssistantState();
    },

    async _waitForPublishAssistantReady(opts = {}) {
      const timeout = opts.timeout || 180_000;
      const softTimeout = opts.softTimeout || 45_000;
      const start = Date.now();
      let lastState = null;
      while (Date.now() - start < timeout) {
        lastState = await this._getPublishAssistantState();
        if (lastState.ready) {
          return { ok: true, state: lastState, elapsed: Date.now() - start };
        }
        if (
          Date.now() - start >= softTimeout
          && !lastState.uploadBusy
          && lastState.publishButtonVisible
          && /发布设置|发布暂存离开|预览视频/.test(lastState.textSample || '')
        ) {
          return { ok: true, soft: true, reason: 'publish_button_visible_after_soft_timeout', state: lastState, elapsed: Date.now() - start };
        }
        await sleep(lastState.percent !== null ? 3000 : 1000);
      }
      return { ok: false, error: 'assistant_timeout', state: lastState, elapsed: Date.now() - start };
    },

    /**
     * 填写标题（标准 input 元素）
     * @param {string} title
     * @returns {Promise<{ok: boolean, error?: string}>}
     */
    async fillTitle(title) {
      const requestedTitle = String(title || '').trim();
      const result = await op.query((selectors, value) => {
        const visible = (el) => {
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
        let input = null;
        for (const selector of selectors) {
          input = [...document.querySelectorAll(selector)].find(visible);
          if (input) break;
        }
        if (!input) return { ok: false, error: 'title_input_not_found' };
        const htmlLimit = Number(input.maxLength || input.getAttribute('maxlength') || 0);
        const limit = htmlLimit > 0 ? htmlLimit : 60;
        const expected = Array.from(String(value || '').replace(/\s+/g, ' ').trim()).slice(0, limit).join('');
        input.focus();
        setter?.call(input, '');
        input.dispatchEvent(new Event('input', { bubbles: true }));
        setter?.call(input, expected);
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        return { ok: true, value: input.value, expected, maxLength: limit };
      }, SELECTORS.titleInput, requestedTitle);

      const expectedTitle = result.expected || normalizePublishTitle(requestedTitle);
      if (!result.ok || result.value !== expectedTitle) {
        const loc = await op.locate(SELECTORS.titleInput);
        if (!loc.found) {
          return { ok: false, error: result.error || 'title_input_not_found' };
        }
        await op.click(SELECTORS.titleInput);
        await sleep(200);
        await op.page.keyboard.down('Control');
        await op.page.keyboard.press('a');
        await op.page.keyboard.up('Control');
        await op.type(expectedTitle);
      }

      const verified = await op.query((expected) => {
        const input = [...document.querySelectorAll('input[placeholder*="作品标题"], input[placeholder*="标题"]')]
          .find((el) => el.getBoundingClientRect().width > 0 && el.getBoundingClientRect().height > 0);
        return input?.value === expected;
      }, expectedTitle);
      if (!verified) return { ok: false, error: 'title_fill_not_reflected', expected: expectedTitle, requested: requestedTitle };
      console.log(`[ops] 已填写标题: ${expectedTitle}`);
      return { ok: true, title: expectedTitle, requestedTitle };
    },

    /**
     * 填写作品简介（slate 富文本编辑器，contenteditable div）
     * @param {string} description
     * @returns {Promise<{ok: boolean, error?: string}>}
     */
    async fillDescription(description) {
      const loc = await op.locate(SELECTORS.descriptionInput);
      if (!loc.found) {
        return { ok: false, error: 'description_input_not_found' };
      }

      // 点击聚焦 contenteditable 区域
      await op.click(SELECTORS.descriptionInput);
      await sleep(200);

      await op.page.keyboard.down('Control');
      await op.page.keyboard.press('a');
      await op.page.keyboard.up('Control');
      await op.page.keyboard.press('Backspace');
      await op.type(description);

      const verified = await op.query((expected) => {
        const editor = [...document.querySelectorAll('div[data-placeholder*="作品简介"][contenteditable="true"], div[data-placeholder*="添加作品简介"][contenteditable="true"], div.editor-kit-container[contenteditable="true"], div[contenteditable="true"][data-slate-editor="true"]')]
          .find((el) => el.getBoundingClientRect().width > 0 && el.getBoundingClientRect().height > 0);
        return (editor?.innerText || '').includes(expected);
      }, description);
      if (!verified) return { ok: false, error: 'description_fill_not_reflected' };
      console.log(`[ops] 已填写作品简介: ${description.slice(0, 30)}${description.length > 30 ? '...' : ''}`);
      return { ok: true };
    },

    /**
     * 通过「#添加话题」控件生成真实话题节点，支持 1 个或多个话题。
     */
    async fillTopics(topics) {
      const list = normalizeTopicList(topics);
      if (!list.length) return { ok: true, topics: [] };

      for (const topic of list) {
        const clicked = await op.query((topicName) => {
          const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
          const visible = (el) => {
            if (!el) return false;
            const rect = el.getBoundingClientRect();
            const style = getComputedStyle(el);
            return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
          };
          const editor = [...document.querySelectorAll('div[data-placeholder*="作品简介"][contenteditable="true"], div[data-placeholder*="添加作品简介"][contenteditable="true"], div.editor-kit-container[contenteditable="true"], div[contenteditable="true"][data-slate-editor="true"]')]
            .find(visible);
          if (!editor) return { ok: false, error: 'description_input_not_found' };
          const hasTopicNode = [...editor.querySelectorAll('[data-mention="#"], [data-fake-text]')]
            .some((el) => (el.textContent || '').includes(`#${topicName}`));
          if (hasTopicNode) {
            return { ok: true, alreadyPresent: true };
          }
          const button = [...document.querySelectorAll('.toolbar-button-spPS4r, button, div, span')]
            .find((el) => visible(el) && compact(el.innerText || el.textContent) === '#添加话题');
          if (!button) return { ok: false, error: 'topic_button_not_found' };
          button.scrollIntoView({ block: 'center', inline: 'nearest' });
          button.click();
          return { ok: true, alreadyPresent: false };
        }, topic);
        if (!clicked?.ok) return { ok: false, error: clicked?.error || 'topic_button_click_failed', topic, clicked };
        if (!clicked.alreadyPresent) {
          await sleep(250);
          await op.page.keyboard.type(topic, { delay: 20 });
          await sleep(250);
          await op.page.keyboard.press('Enter');
          await sleep(650);
        }
      }

      const verification = await op.query((expectedTopics) => {
        const visible = (el) => {
          if (!el) return false;
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const editor = [...document.querySelectorAll('div[data-placeholder*="作品简介"][contenteditable="true"], div[data-placeholder*="添加作品简介"][contenteditable="true"], div.editor-kit-container[contenteditable="true"], div[contenteditable="true"][data-slate-editor="true"]')]
          .find(visible);
        const text = editor?.innerText || '';
        const mentionNodes = editor
          ? [...editor.querySelectorAll('[data-mention="#"], [data-fake-text]')]
              .map((el) => el.textContent || '')
              .join(' ')
          : '';
        const combined = `${text} ${mentionNodes}`;
        const missing = expectedTopics.filter((topic) => !combined.includes(`#${topic}`));
        return {
          ok: missing.length === 0,
          missing,
          text,
          mentionNodes,
        };
      }, list);
      if (!verification?.ok) return { ok: false, error: 'topics_fill_not_reflected', topics: list, verification };
      console.log(`[ops] 已填写话题: ${list.map((item) => `#${item}`).join(' ')}`);
      return { ok: true, topics: list, verification };
    },

    /**
     * 发布图文
     *
     * 前置条件：需在上传页 + 「发布图文」tab。
     * 会自动切换到发布图文 tab，然后通过 file input 上传图片。
     *
     * @param {string|string[]} filePaths - 图片文件路径（单张或多张）
     * @param {object} [opts] - 发布选项（标题、描述等，待后续扩展）
     * @returns {Promise<{ok: boolean, error?: string}>}
     */
    async publishImageText(filePaths, opts = {}) {
      const paths = Array.isArray(filePaths) ? filePaths : [filePaths];

      // 1. 确保在上传页
      const goResult = await this.goUploadPage();
      if (!goResult.ok) return goResult;

      // 2. 切换到发布图文 tab
      const switchResult = await this.switchPublishType('imagetext');
      if (!switchResult.ok) return switchResult;

      await sleep(500);

      // 3. 点击「上传图文」按钮，同时拦截文件选择对话框
      const uploadResult = await this._clickAndChooseFile(SELECTORS.uploadImageTextBtn, paths);
      if (!uploadResult.ok) return uploadResult;

      console.log(`[ops] 图文已上传 ${paths.length} 张图片`);

      // 4. 填写标题
      const { title, description } = opts;
      if (title) {
        const titleResult = await this.fillTitle(title);
        if (!titleResult.ok) {
          return { ok: false, error: titleResult.error || 'title_fill_failed', detail: titleResult };
        }
      }

      // 5. 填写作品简介
      if (description) {
        const descResult = await this.fillDescription(description);
        if (!descResult.ok) {
          return { ok: false, error: descResult.error || 'description_fill_failed', detail: descResult };
        }
      }
      const topics = normalizeTopicList(opts.topics || opts.tags);
      if (topics.length) {
        const topicsResult = await this.fillTopics(topics);
        if (!topicsResult.ok) {
          return { ok: false, error: topicsResult.error || 'topics_fill_failed', detail: topicsResult };
        }
      }

      // 6. 点击「选择音乐」（先滚动到视图中心）
      await sleep(500);
      await op.query(() => {
        const btn = [...document.querySelectorAll('span')].find(s => s.textContent?.includes('选择音乐'));
        if (btn) btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
      });
      await sleep(500);
      const musicResult = await op.click([
        'div[class*="container-right"] span[class*="action"]:has-text("选择音乐")',
        'span[class*="action"]:has-text("选择音乐")',
      ]);
      if (musicResult.ok) {
        console.log('[ops] 已点击「选择音乐」');
      } else {
        console.warn('[ops] 未找到「选择音乐」按钮，跳过');
      }
      await sleep(500);

      // 5. 等待音乐收藏面板加载，hover 第一个 card，点击「使用」
      const musicPanelReady = await op.waitFor(() => {
        return !!document.querySelector('div[class*="music-collection-container"]');
      }, { timeout: 5000, interval: 500 });

      if (musicPanelReady.ok) {
        console.log('[ops] 音乐收藏面板已加载');
        await sleep(500);// 等待一小会

        // hover 第一个 card（触发「使用」按钮显示）
        const firstCard = await op.locate(['div[class*="music-collection-container"] div[class*="card-container"]:first-child']);
        if (firstCard.found) {
          await op.page.mouse.move(firstCard.x, firstCard.y);
          await sleep(500);

          // 点击「使用」按钮
          const useResult = await op.click([
            'div[class*="card-container"] button[class*="apply-btn"]',
            'div[class*="card-container-right"] button.semi-button-primary',
          ]);
          if (useResult.ok) {
            console.log('[ops] 已点击音乐「使用」按钮');
          } else {
            console.warn('[ops] 未找到音乐「使用」按钮');
          }
          await sleep(500);
        } else {
          console.warn('[ops] 未找到音乐卡片');
        }
      } else {
        console.warn('[ops] 音乐收藏面板未加载，跳过');
      }

      // 8. 点击发布按钮（先滚动到视图中心）
      await sleep(500);
      await op.query(() => {
        const container = document.querySelector('div[class*="card-container-creator-layout"]');
        const btn = container && [...container.querySelectorAll('button')].find(b => b.textContent?.trim() === '发布');
        if (btn) btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
      });
      await sleep(500);
      const publishLoc = await op.query(() => {
        const container = document.querySelector('div[class*="card-container-creator-layout"]');
        if (!container) return { found: false };
        const btn = [...container.querySelectorAll('button')].find(b => b.textContent?.trim() === '发布');
        if (!btn) return { found: false };
        const rect = btn.getBoundingClientRect();
        return { found: true, x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
      });
      let publishResult = { ok: false };
      if (publishLoc.found) {
        await op.page.mouse.click(publishLoc.x, publishLoc.y);
        publishResult = { ok: true };
      }
      if (publishResult.ok) {
        console.log('[ops] 已点击发布按钮，检测发布结果...');
      } else {
        return { ok: false, error: 'publish_btn_not_found', type: 'imagetext' };
      }

      // 9. 检测 toast 判断发布结果
      const toastResult = await this._waitForToast();
      if (toastResult.found) {
        if (toastResult.success) {
          console.log('[ops] ✅ 图文发布成功');
          return { ok: true, type: 'imagetext', count: paths.length, files: paths };
        } else {
          console.error(`[ops] ❌ 图文发布失败: ${toastResult.text}`);
          return { ok: false, error: 'publish_failed', detail: toastResult.text, type: 'imagetext' };
        }
      }

      return { ok: true, type: 'imagetext', count: paths.length, files: paths };
    },

    /**
     * 内部方法：等待 toast 提示出现，判断发布结果
     *
     * 点击发布按钮后，5 秒内每秒检测 semi-toast-content-text：
     *   - 文本包含"发布成功" → success
     *   - 其他文本 → 失败，返回 toast 内容
     *   - 超时无 toast → 未检测到
     *
     * @returns {Promise<{found: boolean, success?: boolean, text?: string}>}
     * @private
     */
    async _waitForToast() {
      for (let i = 0; i < 5; i++) {
        await sleep(1000);
        const toastText = await op.query(() => {
          const el = document.querySelector('span[class*="semi-toast-content-text"]');
          return el ? el.textContent?.trim() : null;
        });
        if (toastText) {
          console.log(`[ops] 检测到 toast: "${toastText}"`);
          return {
            found: true,
            success: toastText.includes('发布成功'),
            text: toastText,
          };
        }
      }
      console.log('[ops] 5 秒内未检测到 toast');
      return { found: false };
    },

    /**
     * 发布文章
     *
     * 前置条件：需在上传页 + 「发布文章」tab。
     * 会自动切换到发布文章 tab，然后点击「我要发文」进入编辑器。
     *
     * @param {object} [opts] - 发布选项（待后续扩展）
     * @returns {Promise<{ok: boolean, error?: string}>}
     */
    async publishArticle(opts = {}) {
      // 1. 确保在上传页
      const goResult = await this.goUploadPage();
      if (!goResult.ok) return goResult;

      // 2. 切换到发布文章 tab
      const switchResult = await this.switchPublishType('article');
      if (!switchResult.ok) return switchResult;

      await sleep(500);

      // 3. 点击「我要发文」按钮进入文章编辑器
      const clickResult = await op.click([
        'button[class*="container-drag-btn"]:has-text("我要发文")',
        ...SELECTORS.publishArticleBtn,
      ]);
      if (!clickResult.ok) {
        return { ok: false, error: 'publish_article_btn_not_found' };
      }

      // 等待页面跳转到文章编辑器
      const navDone = await Promise.race([
        op.page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 15_000 })
          .then(() => true)
          .catch(() => false),
        sleep(15_000).then(() => false),
      ]);

      if (!navDone) {
        console.warn('[ops] 文章编辑器页面未跳转，可能需要手动操作');
      }

      await sleep(1000); // 等待编辑器加载

      console.log('[ops] 已进入文章编辑器');
      return { ok: true, type: 'article' };
    },

    /**
     * 内部方法：点击按钮并通过 CDP 拦截文件选择对话框传入文件
     *
     * 参考 Gemini skill 的 uploadImage 实现：
     *   1. 路径规范化 + 文件存在性检查
     *   2. Promise.all 同时监听 fileChooser 和点击按钮
     *   3. fileChooser.accept() 直接传入文件，不弹出系统对话框
     *
     * @param {string[]} btnSelectors - 触发文件选择的按钮选择器
     * @param {string[]} filePaths - 要上传的文件绝对路径数组
     * @returns {Promise<{ok: boolean, error?: string}>}
     * @private
     */
    async _clickAndChooseFile(btnSelectors, filePaths) {
      try {
        // 1. 路径规范化 + 文件存在性检查
        const paths = filePaths.map(p => pathResolve(pathNormalize(p)));
        for (const p of paths) {
          if (!existsSync(p)) {
            return { ok: false, error: 'file_not_found', detail: `文件不存在: ${p}` };
          }
        }

        let chooserError = null;
        try {
          // 2. 同时监听 fileChooser 和点击按钮（必须并行，否则会错过事件）
          const [fileChooser] = await Promise.all([
            op.page.waitForFileChooser({ timeout: 5_000 }),
            op.click(btnSelectors),
          ]);

          // 3. 弹窗被拦截，直接塞入文件
          await fileChooser.accept(paths);
          console.log(`[ops] 文件已通过 file chooser 塞入 (${paths.length} 个)，等待处理...`);
        } catch (err) {
          chooserError = err;
          const direct = await this._uploadFilesByInput(paths);
          if (!direct.ok) {
            return {
              ok: false,
              error: 'file_chooser_failed',
              detail: `${chooserError.message}; direct input fallback: ${direct.error || direct.detail}`,
            };
          }
          console.log(`[ops] 文件已通过隐藏 input 直接塞入 (${paths.length} 个)，等待处理...`);
        }

        await sleep(1000);

        return { ok: true, count: paths.length };
      } catch (err) {
        return { ok: false, error: 'file_chooser_failed', detail: err.message };
      }
    },

    async _uploadFilesByInput(paths) {
      const inputs = await op.page.$$('input[type="file"]');
      for (const input of inputs) {
        try {
          await input.uploadFile(...paths);
          return { ok: true, count: paths.length };
        } catch {
          // Try the next file input; Douyin can render several hidden inputs.
        }
      }
      return { ok: false, error: 'file_input_not_found_or_rejected' };
    },

    async _getPublishEditState() {
      return op.query(() => {
        const text = document.body?.innerText || '';
        const compact = text.replace(/\s+/g, '');
        const visible = (el) => {
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const titleInput = !![...document.querySelectorAll('input[placeholder*="作品标题"], input[placeholder*="标题"]')].find(visible);
        const descriptionInput = !![...document.querySelectorAll('div[data-placeholder*="作品简介"][contenteditable="true"], div[data-placeholder*="添加作品简介"][contenteditable="true"], div.editor-kit-container[contenteditable="true"], div[contenteditable="true"][data-slate-editor="true"]')].find(visible);
        const uploading = !!document.querySelector('[class*="uploading-container"]');
        const uploadProgressMatch = compact.match(/(\d{1,3})%文件(?:解析|上传|处理中)|文件(?:解析|上传|处理中)[^0-9]{0,8}(\d{1,3})%/);
        const uploadPercent = uploadProgressMatch ? Number(uploadProgressMatch[1] || uploadProgressMatch[2]) : null;
        const uploadBusy = /上传过程中请不要删除\/移动文件|文件解析中|取消上传/.test(text)
          || /(?:文件|视频)(?:解析|上传|处理)中/.test(text)
          || (uploadPercent !== null && uploadPercent < 100);
        const uploadComplete = !uploadBusy && !uploading && /发布设置|作品标题|作品简介|发布暂存/.test(text);
        let blocked = null;
        if (/扫码登录|验证码登录|密码登录|登录\/注册/.test(text)) blocked = 'login_required';
        if (/安全验证|拖动滑块|机器人|真人验证|请完成验证|拼图/.test(text)) blocked = 'captcha_required';
        if (/手机验证|扫码验证|已登录账号的设备|已登录设备|用手机.*验证|手机.*确认|抖音 App.*扫码验证|抖音APP.*扫码验证|为确保.*本人操作|确保为本人操作|使用.*设备扫码/.test(text)) blocked = 'device_verification_required';
        if (/上传失败|格式不支持|文件损坏|视频处理失败|上传出错/.test(text)) blocked = 'upload_failed';
        return {
          url: location.href,
          titleInput,
          descriptionInput,
          uploading: uploading || uploadBusy,
          uploadDone: uploadComplete,
          uploadPercent,
          blocked,
          textSample: text.replace(/\s+/g, ' ').slice(0, 500),
        };
      });
    },

    async _getPublishEditorGuardState() {
      return op.query(() => {
        const text = document.body?.innerText || '';
        const url = location.href;
        const visible = (el) => {
          if (!el) return false;
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const titleInput = [...document.querySelectorAll('input[placeholder*="作品标题"], input[placeholder*="标题"]')].some(visible);
        const descriptionInput = [...document.querySelectorAll('div[data-placeholder*="作品简介"][contenteditable="true"], div[data-placeholder*="添加作品简介"][contenteditable="true"], div.editor-kit-container[contenteditable="true"], div[contenteditable="true"][data-slate-editor="true"]')].some(visible);
        const editorText = /基础信息|作品描述|作品简介|作品标题|发布设置|点击发布后|发布暂存离开|预览视频/.test(text);
        const loginGate = /扫码登录|验证码登录|密码登录|登录\/注册/.test(text);
        const uploadHome = url.includes('/content/upload') && /发布视频|上传视频|发布图文|发布文章|我要发文|一键导入/.test(text) && !titleInput;
        const inVideoEditor = !loginGate && !uploadHome && (
          url.includes('/content/post/video')
          || ((titleInput || descriptionInput) && editorText)
        );
        return {
          inVideoEditor: Boolean(inVideoEditor),
          url,
          titleInput,
          descriptionInput,
          editorText,
          uploadHome,
          loginGate,
          textSample: text.replace(/\s+/g, ' ').slice(0, 700),
        };
      });
    },

    async _clickPublishButton() {
      const editorGuard = await this._getPublishEditorGuardState();
      if (!editorGuard.inVideoEditor) {
        return { ok: false, error: 'publish_editor_not_ready', detail: editorGuard };
      }
      await op.query(() => {
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'instant' });
        const scrollables = [...document.querySelectorAll('*')]
          .filter((el) => {
            const style = getComputedStyle(el);
            return /(auto|scroll)/.test(style.overflowY || '') && el.scrollHeight > el.clientHeight + 20;
          })
          .sort((a, b) => (b.scrollHeight - b.clientHeight) - (a.scrollHeight - a.clientHeight))
          .slice(0, 8);
        const containers = [
          document.querySelector('.micro-wrapper-OGvOEm'),
          document.querySelector('[class*="micro-wrapper"]'),
          document.scrollingElement,
          ...scrollables,
        ].filter(Boolean);
        for (const el of containers) {
          try { el.scrollTop = el.scrollHeight; } catch {}
        }
      });
      await sleep(500);
      const appear = await op.waitFor(() => {
        const pageText = document.body?.innerText || '';
        const titleInput = [...document.querySelectorAll('input[placeholder*="作品标题"], input[placeholder*="标题"]')]
          .some((el) => {
            const rect = el.getBoundingClientRect();
            const style = getComputedStyle(el);
            return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
          });
        if (location.href.includes('/content/upload') && !titleInput) return false;
        if (!location.href.includes('/content/post/video') && !/作品标题|发布设置|发布暂存离开|预览视频/.test(pageText)) return false;
        const visible = (el) => {
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const inNavigation = (el) => Boolean(el.closest('aside, header, nav, [class*="sider"], [class*="header"], [class*="nav"], [class*="menu"], [class*="tab"]'));
        const textOf = (el) => ((el.innerText || el.textContent || '').replace(/\s+/g, '').trim());
        const btn = [...document.querySelectorAll('button, [role="button"], a')]
          .filter(visible)
          .filter((b) => textOf(b) === '发布')
          .filter((b) => !String(b.className).includes('tab-item') && !textOf(b).includes('高清发布'))
          .filter((b) => !inNavigation(b))
          .sort((a, b) => {
            const ar = a.getBoundingClientRect();
            const br = b.getBoundingClientRect();
            const score = (el, rect) => {
              let value = 0;
              if (el.tagName === 'BUTTON') value -= 1000;
              if (String(el.className).includes('fixed')) value -= 500;
              if (String(el.className).includes('primary')) value -= 200;
              value -= rect.y;
              value += Math.abs((rect.width * rect.height) - 4000) / 100;
              return value;
            };
            return score(a, ar) - score(b, br);
          })[0];
        if (!btn) return false;
        btn.scrollIntoView({ behavior: 'instant', block: 'nearest', inline: 'nearest' });
        return true;
      }, { timeout: 45_000, interval: 1000 });
      if (!appear.ok) return { ok: false, error: 'publish_btn_not_found' };
      await sleep(250);

      const loc = await op.query(() => {
        const visible = (el) => {
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const inNavigation = (el) => Boolean(el.closest('aside, header, nav, [class*="sider"], [class*="header"], [class*="nav"], [class*="menu"], [class*="tab"]'));
        const textOf = (el) => ((el.innerText || el.textContent || '').replace(/\s+/g, '').trim());
        const btn = [...document.querySelectorAll('button, [role="button"], a')]
          .filter(visible)
          .filter((b) => textOf(b) === '发布')
          .filter((b) => !String(b.className).includes('tab-item') && !textOf(b).includes('高清发布'))
          .filter((b) => !inNavigation(b))
          .sort((a, b) => {
            const ar = a.getBoundingClientRect();
            const br = b.getBoundingClientRect();
            const score = (el, rect) => {
              let value = 0;
              if (el.tagName === 'BUTTON') value -= 1000;
              if (String(el.className).includes('fixed')) value -= 500;
              if (String(el.className).includes('primary')) value -= 200;
              value -= rect.y;
              value += Math.abs((rect.width * rect.height) - 4000) / 100;
              return value;
            };
            return score(a, ar) - score(b, br);
          })[0];
        if (!btn) return { found: false };
        const rect = btn.getBoundingClientRect();
        const clickable = btn.closest('button, [role="button"], a') || btn;
        const clickRect = clickable.getBoundingClientRect();
        const x = clickRect.x + clickRect.width / 2;
        const y = clickRect.y + clickRect.height / 2;
        const inViewport = x >= 0 && y >= 0 && x <= window.innerWidth && y <= window.innerHeight;
        const topStack = inViewport ? document.elementsFromPoint(x, y) : [];
        const unobstructed = topStack.some((el) => el === clickable || clickable.contains(el) || el.contains(clickable));
        return {
          found: true,
          x,
          y,
          inViewport,
          unobstructed,
          rect: { x: clickRect.x, y: clickRect.y, width: clickRect.width, height: clickRect.height },
          disabled: Boolean(clickable.disabled || clickable.getAttribute('aria-disabled') === 'true' || String(clickable.className).includes('disabled')),
          text: btn.textContent,
        };
      });

      if (!loc.found) return { ok: false, error: 'publish_btn_not_found' };
      if (loc.disabled) return { ok: false, error: 'publish_btn_disabled', detail: loc.text };

      if (!loc.inViewport || !loc.unobstructed) {
        closeBrowserNativePrompts();
        await sleep(300);
        const refreshed = await op.query(() => {
          const visible = (el) => {
            const rect = el.getBoundingClientRect();
            const style = getComputedStyle(el);
            return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
          };
          const inNavigation = (el) => Boolean(el.closest('aside, header, nav, [class*="sider"], [class*="header"], [class*="nav"], [class*="menu"], [class*="tab"]'));
          const textOf = (el) => ((el.innerText || el.textContent || '').replace(/\s+/g, '').trim());
          const btn = [...document.querySelectorAll('button, [role="button"], a')]
            .filter(visible)
            .filter((b) => textOf(b) === '发布')
            .filter((b) => !String(b.className).includes('tab-item') && !textOf(b).includes('高清发布'))
            .filter((b) => !inNavigation(b))
            .sort((a, b) => {
              const ar = a.getBoundingClientRect();
              const br = b.getBoundingClientRect();
              return ar.y - br.y;
            })[0];
          if (!btn) return { found: false };
          const clickable = btn.closest('button, [role="button"], a') || btn;
          const rect = clickable.getBoundingClientRect();
          const x = rect.x + rect.width / 2;
          const y = rect.y + rect.height / 2;
          const topStack = x >= 0 && y >= 0 && x <= window.innerWidth && y <= window.innerHeight
            ? document.elementsFromPoint(x, y)
            : [];
          return {
            found: true,
            x,
            y,
            inViewport: x >= 0 && y >= 0 && x <= window.innerWidth && y <= window.innerHeight,
            unobstructed: topStack.some((el) => el === clickable || clickable.contains(el) || el.contains(clickable)),
            rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
          };
        });
        if (!refreshed.found || !refreshed.inViewport || !refreshed.unobstructed) {
          return { ok: false, error: 'publish_btn_obstructed', detail: refreshed.found ? refreshed : loc };
        }
        loc.x = refreshed.x;
        loc.y = refreshed.y;
        loc.inViewport = refreshed.inViewport;
        loc.unobstructed = refreshed.unobstructed;
      }

      closeBrowserNativePrompts();
      await sleep(200);
      await op.page.mouse.move(loc.x, loc.y);
      await sleep(100);
      await op.page.mouse.click(loc.x, loc.y);
      await sleep(1200);
      let currentUrl = op.page.url();
      if (currentUrl.includes('/content/upload')) {
        const resume = await this.resumeUnpublishedDraft().catch((err) => ({ ok: false, error: err.message }));
        if (!resume.ok) {
          return { ok: false, error: 'publish_click_returned_to_upload', detail: { url: currentUrl, method: 'mouse_click', resume } };
        }
        await sleep(1200);
      }
      let moved = await op.query(() => {
        const text = document.body?.innerText || '';
        return location.href.includes('/content/manage') || /发布成功|审核中|提交成功/.test(text);
      });
      if (moved) return { ok: true, method: 'mouse_click' };
      let verification = await this._getPublishVerificationState();
      if (verification.found) {
        return { ok: true, method: 'mouse_click', verification };
      }
      const firstToast = await this._readToast();
      if (firstToast.found) {
        return firstToast.success
          ? { ok: true, method: 'mouse_click', toast: firstToast.text }
          : { ok: false, error: 'publish_failed', detail: firstToast.text };
      }

      // 普通鼠标点击没有触发页面变化时，再使用 React/DOM fallback。
      const react = await op.query(() => {
        const visible = (el) => {
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const pageText = document.body?.innerText || '';
        const titleInput = [...document.querySelectorAll('input[placeholder*="作品标题"], input[placeholder*="标题"]')].some(visible);
        if (location.href.includes('/content/upload') && !titleInput) return { ok: false, error: 'publish_editor_not_ready' };
        if (!location.href.includes('/content/post/video') && !/作品标题|发布设置|发布暂存离开|预览视频/.test(pageText)) return { ok: false, error: 'publish_editor_not_ready' };
        const inNavigation = (el) => Boolean(el.closest('aside, header, nav, [class*="sider"], [class*="header"], [class*="nav"], [class*="menu"], [class*="tab"]'));
        const textOf = (el) => ((el.innerText || el.textContent || '').replace(/\s+/g, '').trim());
        const btn = [...document.querySelectorAll('button, [role="button"], a')]
          .filter(visible)
          .filter((b) => textOf(b) === '发布')
          .filter((b) => !String(b.className).includes('tab-item') && !textOf(b).includes('高清发布'))
          .filter((b) => !inNavigation(b))
          .sort((a, b) => {
            const ar = a.getBoundingClientRect();
            const br = b.getBoundingClientRect();
            const score = (el, rect) => {
              let value = 0;
              if (el.tagName === 'BUTTON') value -= 1000;
              if (String(el.className).includes('fixed')) value -= 500;
              if (String(el.className).includes('primary')) value -= 200;
              value -= rect.y;
              value += Math.abs((rect.width * rect.height) - 4000) / 100;
              return value;
            };
            return score(a, ar) - score(b, br);
          })[0];
        if (!btn) return { ok: false, error: 'publish_btn_not_found' };
        const clickable = btn.closest('button, [role="button"], a') || btn;
        const disabled = clickable.disabled || clickable.getAttribute('aria-disabled') === 'true' || /disabled/i.test(String(clickable.className || ''));
        if (disabled) return { ok: false, error: 'publish_btn_disabled' };
        const key = Object.keys(clickable).find((k) => k.startsWith('__reactProps'));
        const props = key ? clickable[key] : null;
        if (typeof props?.onClick !== 'function') {
          clickable.click?.();
          return { ok: true, method: 'dom_click' };
        }
        const event = {
          type: 'click',
          target: clickable,
          currentTarget: clickable,
          nativeEvent: new MouseEvent('click', { bubbles: true, cancelable: true }),
          defaultPrevented: false,
          propagationStopped: false,
          preventDefault() { this.defaultPrevented = true; },
          stopPropagation() { this.propagationStopped = true; },
          persist() {},
          isDefaultPrevented() { return Boolean(this.defaultPrevented); },
          isPropagationStopped() { return Boolean(this.propagationStopped); },
        };
        props.onClick(event);
        return { ok: true, method: 'react_onclick' };
      });
      if (react.ok) {
        await sleep(800);
        currentUrl = op.page.url();
        if (currentUrl.includes('/content/upload')) {
          return { ok: false, error: 'publish_click_returned_to_upload', detail: { url: currentUrl, method: react.method } };
        }
        moved = await op.query(() => {
          const text = document.body?.innerText || '';
          return location.href.includes('/content/manage') || /发布成功|审核中|提交成功/.test(text);
        });
        if (moved) return { ok: true, method: react.method || 'react_onclick' };
        verification = await this._getPublishVerificationState();
        if (verification.found) {
          return { ok: true, method: react.method || 'react_onclick', verification };
        }
        return { ok: true, method: react.method || 'react_onclick' };
      }
      return react;
    },

    async _readToast() {
      const toastText = await op.query(() => {
        const el = document.querySelector('span[class*="semi-toast-content-text"], div[class*="semi-toast-content"]');
        return el ? el.textContent?.trim() : null;
      });
      if (!toastText) return { found: false };
      return {
        found: true,
        success: /发布成功|提交成功|已发布|审核中/.test(toastText),
        text: toastText,
      };
    },

    async _waitForPublishSubmit(opts = {}) {
      const timeout = opts.timeout || 60_000;
      const title = opts.title || '';
      const page = op.page;
      const observed = [];
      const handler = async (res) => {
        const url = res.url();
        if (!/create_v2|publish|aweme\/v1\/open/.test(url)) return;
        const item = { status: res.status(), url };
        try {
          const headers = res.headers();
          if (headers['content-type']?.includes('application/json')) {
            const text = await res.text();
            item.body = text.slice(0, 1000);
            item.okBody = /"status_code"\s*:\s*0|"StatusCode"\s*:\s*0|"code"\s*:\s*0/.test(text);
            item.errorBody = /error|失败|captcha|verify|login|session_expired|无权限|风控|频繁/i.test(text);
          }
        } catch {
          // Body may already be consumed by the page.
        }
        observed.push(item);
      };
      page.on('response', handler);
      try {
        const start = Date.now();
        while (Date.now() - start < timeout) {
          const toast = await this._readToast();
          if (toast.found && !toast.success) {
            return { ok: false, error: 'publish_failed', detail: toast.text, observed };
          }
          if (toast.success) return { ok: true, method: 'toast', toast: toast.text, observed };
          if (page.url().includes('/content/manage')) {
            return { ok: true, method: 'manage_navigation', url: page.url(), observed };
          }
          const createResponse = observed.find((item) => /create_v2/.test(item.url) && item.status >= 200 && item.status < 300);
          if (createResponse?.okBody) {
            return { ok: true, method: 'create_v2_response', response: createResponse, observed };
          }
          const badResponse = observed.find((item) => item.errorBody);
          if (badResponse) {
            return { ok: false, error: 'publish_api_error', detail: badResponse.body, observed };
          }
          const verifyPrompt = await this._getPublishVerificationState();
          if (verifyPrompt.found) {
            return {
              ok: false,
              error: 'publish_verification_required',
              detail: verifyPrompt,
              observed,
            };
          }
          await sleep(1000);
        }
        return { ok: false, error: 'publish_submit_unconfirmed', detail: { title }, observed };
      } finally {
        page.off('response', handler);
      }
    },

    async _getPublishVerificationState() {
      return op.query(() => {
        const text = document.body?.innerText || '';
        const visible = (el) => {
          if (!el) return false;
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const sendSmsInstruction = /发送短信验证/.test(text) && /编辑短信|发送至|可能产生费用|去使用短信验证/.test(text);
        const publishSms = /接收短信验证码|发送短信验证|为确保是本人操作抖音账号|使用原设备扫码|当前手机号[^，。]*短信验证码|收到的短信验证码|编辑短信|发送至|去使用短信验证/.test(text)
          && /creator-micro\/content\/post\/video/.test(location.href);
        const input = [...document.querySelectorAll('.second-verify-panel input, [class*="second-verify-panel"] input, input[placeholder*="验证码"], input#button-input')]
          .find((el) => visible(el) && /验证码|code/i.test(`${el.placeholder || ''} ${el.className || ''}`));
        const qr = [...document.querySelectorAll('img.uc-ui-verify_qr-verify_main_qr-img, img')]
          .find((el) => visible(el) && Boolean(el.closest('.uc-ui-verify_qr-verify_main_qr, .second-verify-panel, article.uc-ui-verify_qr-verify')));
        return {
          found: Boolean(publishSms || input || qr),
          type: sendSmsInstruction ? 'publish_send_sms_instruction' : (input ? 'publish_sms' : (qr ? 'publish_qr' : (publishSms ? 'publish_sms_choice' : null))),
          url: location.href,
          textSample: text.replace(/\s+/g, ' ').slice(0, 500),
        };
      });
    },

    async getPublishVerificationState() {
      return this._getPublishVerificationState();
    },

    async requestPublishSmsCode(opts = {}) {
      const { allowResend = false } = opts;
      let state = await this._getPublishVerificationState();
      let switchResult = null;
      if (state.type === 'publish_send_sms_instruction') {
        switchResult = await this._switchPublishSendSmsToReceiveSmsCode();
        await sleep(1200);
        state = await this._getPublishVerificationState();
      }
      if (!state.found || !['publish_sms', 'publish_sms_choice'].includes(state.type)) {
        return { ok: false, found: state.found, error: 'publish_sms_prompt_not_found', state, switchResult };
      }
      const result = await this._clickSmsCodeSender({ allowResend, context: 'publish' });
      const nextState = await this._getPublishVerificationState();
      return {
        ok: Boolean(result.ok && (result.changed || nextState.type === 'publish_sms')),
        found: true,
        phase: 'publish_sms_code_input',
        sendCodeResult: result,
        verificationState: nextState,
        switchResult,
        message: result.ok && (result.changed || nextState.type === 'publish_sms')
          ? '发布短信验证码已发送。'
          : '未确认发布短信验证码已发送。',
      };
    },

    async _switchPublishSendSmsToReceiveSmsCode() {
      const target = await op.query(() => {
        const visible = (el) => {
          if (!el) return false;
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const bodyText = document.body?.innerText || '';
        if (!/creator-micro\/content\/post\/video/.test(location.href) || !/编辑短信|发送至|可能产生费用/.test(bodyText)) {
          return { found: false, reason: 'not_send_sms_instruction' };
        }
        const el = [...document.querySelectorAll('button, div, span, a')]
          .filter(visible)
          .find((item) => (item.textContent || '').replace(/\s+/g, '').trim() === '去使用短信验证');
        if (!el) return { found: false, reason: 'switch_link_not_found' };
        const rect = el.getBoundingClientRect();
        return {
          found: true,
          x: rect.x + rect.width / 2,
          y: rect.y + rect.height / 2,
          text: (el.textContent || '').replace(/\s+/g, ' ').trim(),
        };
      });
      if (!target.found) return { ok: false, ...target };
      closeBrowserNativePrompts();
      await sleep(200);
      await op.page.mouse.click(target.x, target.y);
      await sleep(2000);
      const state = await this._getPublishVerificationState();
      return {
        ok: Boolean(state.type && state.type !== 'publish_send_sms_instruction'),
        target,
        state,
      };
    },

    async requestLoginSmsCode(opts = {}) {
      const { allowResend = true } = opts;
      const login = await this.checkLogin();
      if (login.loggedIn) {
        return { ok: false, loggedIn: true, phase: 'logged_in', message: '当前已登录，不需要短信验证码。' };
      }
      if (!['sms_verification', 'sms_code_input'].includes(login.phase)) {
        return { ok: false, loggedIn: false, phase: login.phase, message: login.message || '当前不是短信验证阶段。' };
      }
      const result = await this._clickSmsCodeSender({ allowResend });
      return {
        ok: Boolean(result.ok && (result.changed || login.phase === 'sms_code_input')),
        loggedIn: false,
        phase: 'sms_code_input',
        sendCodeResult: result,
        message: result.ok ? '登录短信验证码已发送。' : '未确认登录短信验证码已发送。',
      };
    },

    async getCurrentPageSummary() {
      return op.query(() => {
        const text = document.body?.innerText || '';
        return {
          url: location.href,
          title: document.title,
          textSample: text.replace(/\s+/g, ' ').slice(0, 1200),
        };
      });
    },

    async submitVisibleSmsCode(smsCode) {
      const publishResult = await this._submitPublishSmsCode(smsCode);
      if (publishResult.found) return publishResult;
      return this.checkLogin({ smsCode });
    },

    async _submitPublishSmsCode(smsCode, attempt = 0) {
      const locate = await op.query((code) => {
        const visible = (el) => {
          if (!el) return false;
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const text = document.body?.innerText || '';
        if (!/creator-micro\/content\/post\/video/.test(location.href) || !/接收短信验证码|发送短信验证|为确保是本人操作抖音账号|使用原设备扫码|当前手机号[^，。]*短信验证码|收到的短信验证码|编辑短信|发送至|去使用短信验证/.test(text)) {
          return { found: false };
        }
        const panels = [...document.querySelectorAll('.second-verify-panel, [class*="second-verify-panel"], body')]
          .filter(visible)
          .filter((el) => /接收短信验证码|发送短信验证|为确保是本人操作|短信验证码|编辑短信|发送至|去使用短信验证/.test(el.innerText || ''))
          .sort((a, b) => {
            const ar = a.getBoundingClientRect();
            const br = b.getBoundingClientRect();
            return (ar.width * ar.height) - (br.width * br.height);
          });
        const panel = panels[0] || document.body;
        const input = [...panel.querySelectorAll('input')]
          .filter(visible)
          .find((el) => /验证码|code/i.test(`${el.placeholder || ''} ${el.className || ''}`));
        if (!input) {
          const sender = [...panel.querySelectorAll('button, div, span, a')]
            .filter(visible)
            .filter((el) => /^(接收短信验证码|获取验证码|发送验证码|去使用短信验证)$/.test((el.textContent || '').replace(/\s+/g, '').trim()))
            .sort((a, b) => {
              const ar = a.getBoundingClientRect();
              const br = b.getBoundingClientRect();
              return (ar.width * ar.height) - (br.width * br.height);
            })[0];
          if (sender) {
            const rect = sender.getBoundingClientRect();
            return {
              found: true,
              ok: false,
              phase: 'publish_sms_code_input',
              error: 'publish_sms_input_not_found',
              needsSenderClick: true,
              x: rect.x + rect.width / 2,
              y: rect.y + rect.height / 2,
              text: (sender.textContent || '').replace(/\s+/g, '').trim(),
            };
          }
          return { found: true, ok: false, error: 'publish_sms_input_not_found' };
        }
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
        input.focus();
        setter?.call(input, '');
        input.dispatchEvent(new Event('input', { bubbles: true }));
        setter?.call(input, code);
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        const verifyBtn = [...panel.querySelectorAll('button, div, span, a')]
          .filter(visible)
          .filter((el) => (el.textContent || '').replace(/\s+/g, '').trim() === '验证')
          .sort((a, b) => {
            const ac = a.className?.toString?.() || '';
            const bc = b.className?.toString?.() || '';
            const as = /disabled/.test(ac) ? 1 : 0;
            const bs = /disabled/.test(bc) ? 1 : 0;
            if (as !== bs) return as - bs;
            const ar = a.getBoundingClientRect();
            const br = b.getBoundingClientRect();
            return (br.width * br.height) - (ar.width * ar.height);
          })[0];
        if (!verifyBtn) return { found: true, ok: false, error: 'publish_sms_verify_button_not_found', value: input.value };
        const className = verifyBtn.className?.toString?.() || '';
        const rect = verifyBtn.getBoundingClientRect();
        return {
          found: true,
          ok: input.value === code && !/disabled/i.test(className),
          value: input.value,
          x: rect.x + rect.width / 2,
          y: rect.y + rect.height / 2,
          buttonClassName: className,
        };
      }, smsCode);

      if (!locate.found) return { found: false };
      if (!locate.ok) {
        if (locate.needsSenderClick && attempt < 2) {
          closeBrowserNativePrompts();
          await sleep(200);
          await op.page.mouse.click(locate.x, locate.y);
          await sleep(2500);
          return this._submitPublishSmsCode(smsCode, attempt + 1);
        }
        return { found: true, ok: false, phase: 'publish_sms_code_input', error: locate.error || 'publish_sms_code_not_ready', detail: locate };
      }

      closeBrowserNativePrompts();
      await sleep(200);
      await op.page.mouse.click(locate.x, locate.y);
      await sleep(6000);
      const state = await op.query(() => {
        const text = document.body?.innerText || '';
        return {
          url: location.href,
          published: location.href.includes('/content/manage') || /发布成功|审核中|已发布|提交成功/.test(text),
          stillVerifying: /接收短信验证码|为确保是本人操作抖音账号|使用原设备扫码/.test(text),
          textSample: text.replace(/\s+/g, ' ').slice(0, 800),
        };
      });
      return {
        found: true,
        ok: Boolean(state.published && !state.stillVerifying),
        phase: state.published ? 'publish_submitted' : 'publish_sms_code_submitted',
        loggedIn: true,
        message: state.published ? '发布验证码已提交，作品已进入发布/管理流程。' : '发布验证码已提交，但页面尚未确认发布完成。',
        state,
      };
    },

    /**
     * 检查登录状态
     *
     * 判断逻辑（多级检测，适配多次调用的登录流程）：
     *   0. 如果传入了 smsCode，检测验证码输入框并填入提交
     *   1. 检测是否在二维码登录页
     *      → 有 aria-label="二维码" → 截图保存二维码，返回 phase='qrcode'
     *   2. 检测是否在身份验证界面（扫码后可能出现）
     *      → 有「接收短信验证码」元素 → 自动点击，返回 phase='sms_verification'
     *   3. 检测是否在验证码输入界面（已点击接收短信后出现）
     *      → 有验证码输入框 → 返回 phase='sms_code_input'，提示传入验证码
     *   4. 都没有 → 已登录，返回 phase='logged_in'
     *
     * MCP 客户端可多次调用此接口推进登录流程：
     *   第1次 → qrcode（用户去扫码）
     *   第2次 → sms_verification（自动点了接收验证码）
     *   第3次 → sms_code_input（提示需要传入验证码）
     *   第4次（带 smsCode）→ 填入验证码并提交
     *   第5次 → logged_in
     *
     * @param {object} [opts]
     * @param {string} [opts.smsCode] - 短信验证码（6位数字）
     * @returns {Promise<{ok: boolean, loggedIn: boolean, phase?: string, qrcodePath?: string}>}
     */
    async checkLogin(opts = {}) {
      const { smsCode } = opts;

      const SMS_CODE_INPUT = 'div[class*="second_verify"] input#button-input[placeholder*="验证码"], article[class*="uc_verification_component_layout"] #button-input[placeholder*="验证码"]';

      // ── 第1优先级：检测二维码登录页 ──
      const qrcodeInfo = await op.query(() => {
        const visible = (el) => {
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const secondVerify = [...document.querySelectorAll('[class*="second_verify"], [class*="uc_verification_component"]')]
          .some((el) => visible(el) && /身份验证|为保障账号安全|接收短信验证码|发送短信验证|请输入验证码/.test(el.textContent || ''));
        if (secondVerify) return null;

        const candidates = [
          ...document.querySelectorAll('img[aria-label="二维码"], img.uc-ui-verify_qr-verify_main_qr-img'),
        ].filter((el) => {
          if (!visible(el)) return false;
          const rect = el.getBoundingClientRect();
          if (rect.width < 160 || rect.height < 160) return false;
          const src = el.currentSrc || el.src || '';
          return Boolean(src || el.complete);
        }).sort((a, b) => {
          const ar = a.getBoundingClientRect();
          const br = b.getBoundingClientRect();
          return (br.width * br.height) - (ar.width * ar.height);
        });
        const img = candidates[0];
        if (!img) return null;
        img.scrollIntoView({ block: 'center', inline: 'center' });
        const rect = img.getBoundingClientRect();
        const padding = Math.max(24, Math.round(Math.min(rect.width, rect.height) * 0.12));
        const x = Math.max(0, rect.x - padding);
        const y = Math.max(0, rect.y - padding);
        const right = Math.min(window.innerWidth, rect.x + rect.width + padding);
        const bottom = Math.min(window.innerHeight, rect.y + rect.height + padding);
        const width = right - x;
        const height = bottom - y;
        if (width < 180 || height < 180) return null;
        return {
          x,
          y,
          width,
          height,
          image: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
          padding,
        };
      });

      if (qrcodeInfo) {
        console.log('[ops] 检测到未登录（发现二维码），截取中...');
        try {
          await sleep(300);
          const qrcodeHandle = await op.page.evaluateHandle(() => {
            const visible = (el) => {
              const rect = el.getBoundingClientRect();
              const style = getComputedStyle(el);
              return rect.width >= 160 && rect.height >= 160 && style.display !== 'none' && style.visibility !== 'hidden';
            };
            const candidates = [...document.querySelectorAll('img[aria-label="二维码"], img.uc-ui-verify_qr-verify_main_qr-img')]
              .filter(visible)
              .sort((a, b) => {
                const ar = a.getBoundingClientRect();
                const br = b.getBoundingClientRect();
                return (br.width * br.height) - (ar.width * ar.height);
              });
            const img = candidates[0] || null;
            img?.scrollIntoView({ block: 'center', inline: 'center' });
            return img;
          });
          const qrcodeElement = qrcodeHandle.asElement();
          if (!qrcodeElement) {
            return {
              ok: true,
              loggedIn: false,
              phase: 'qrcode',
              message: '检测到二维码登录页，但二维码不在可截取区域内；请保持浏览器窗口可见后重试。',
            };
          }
          const { mkdirSync, existsSync: exists } = await import('node:fs');
          const { join, dirname } = await import('node:path');

          const tempDir = join(dirname(config.outputDir), 'temp');
          if (!exists(tempDir)) mkdirSync(tempDir, { recursive: true });

          const qrcodePath = join(tempDir, `qrcode_${Date.now()}.png`);
          await qrcodeElement.screenshot({
            path: qrcodePath,
          });
          await qrcodeHandle.dispose();

          console.log(`[ops] 二维码已保存: ${qrcodePath}`);
          return { ok: true, loggedIn: false, phase: 'qrcode', qrcodePath };
        } catch (err) {
          console.warn(`[ops] 截图二维码失败: ${err.message}`);
        }

        return { ok: true, loggedIn: false, phase: 'qrcode' };
      }

      // ── 第2优先级：检测验证码输入框（只认二次验证浮层，避免底层登录卡片误判） ──
      const codeInput = await op.query((sel) => {
        const visible = (el) => {
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const input = [...document.querySelectorAll(sel)]
          .find((el) => visible(el) && Boolean(el.closest('[class*="second_verify"], article[class*="uc_verification_component_layout"]')));
        if (!input) return { found: false };
        return { found: true };
      }, SMS_CODE_INPUT);

      if (codeInput.found) {
        // 没传验证码 → 提示用户
        if (!smsCode) {
          const smsPanelState = await op.query(() => {
            const text = document.body?.innerText || '';
            return {
              sent: /短信已发送|已发送至|重新发送|重新获取|\d+\s*s|\d+\s*秒/.test(text),
            };
          });
          if (smsPanelState.sent) {
            return {
              ok: true,
              loggedIn: false,
              phase: 'sms_code_input',
              smsCodeSent: true,
              message: '短信验证码已发送，请查看手机短信，收到后携带 smsCode 参数再次调用本接口',
            };
          }

          console.log('[ops] 检测到验证码输入框，尝试点击「获取验证码」...');
          const sendCodeResult = await this._clickSmsCodeSender({ allowResend: false });
          const sent = sendCodeResult.ok && sendCodeResult.changed;
          console.log(`[ops] 获取验证码点击结果: ${JSON.stringify(sendCodeResult)}`);
          return {
            ok: true,
            loggedIn: false,
            phase: 'sms_code_input',
            smsCodeSent: sent,
            sendCodeResult,
            message: sent
              ? '已点击获取验证码，请查看手机短信，收到后携带 smsCode 参数再次调用本接口'
              : '已进入验证码输入界面，但未确认短信已发送。请在浏览器中点击「获取验证码」，收到短信后携带 smsCode 参数再次调用本接口',
          };
        }

        // 传了验证码 → 填入并提交
        console.log(`[ops] 收到验证码: ${smsCode}，填入中...`);

        await op.click([SMS_CODE_INPUT]);
        await sleep(300);

        const fillResult = await op.page.evaluate((sel, code) => {
          const inputs = [...document.querySelectorAll(sel)];
          const visible = (el) => {
            const rect = el.getBoundingClientRect();
            const style = getComputedStyle(el);
            return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
          };
          const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
          const input = inputs
            .filter(visible)
            .filter((el) => Boolean(el.closest('[class*="second_verify"], article[class*="uc_verification_component_layout"]')))
            .find((el) => /验证码|code/i.test(`${el.placeholder || ''} ${el.name || ''} ${el.id || ''} ${el.className || ''}`));
          if (!input) return { ok: false, reason: 'input_not_found' };
          input.focus();
          setter?.call(input, '');
          input.dispatchEvent(new Event('input', { bubbles: true }));
          setter?.call(input, code);
          input.dispatchEvent(new Event('input', { bubbles: true }));
          input.dispatchEvent(new Event('change', { bubbles: true }));
          return { ok: true, value: input.value, className: input.className?.toString?.() || '' };
        }, SMS_CODE_INPUT, smsCode);

        if (!fillResult.ok || fillResult.value !== smsCode) {
          await op.page.keyboard.down('Control');
          await op.page.keyboard.press('a');
          await op.page.keyboard.up('Control');
          await op.page.keyboard.press('Backspace');
          await op.type(smsCode, { mode: 'typeChar', minDelay: 60, maxDelay: 110 });
        }

        const inputState = await op.query((sel) => {
          const input = [...document.querySelectorAll(sel)].find((el) => {
            const rect = el.getBoundingClientRect();
            const style = getComputedStyle(el);
            return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden'
              && Boolean(el.closest('[class*="second_verify"], article[class*="uc_verification_component_layout"]'));
          });
          const verifyBtn = [...document.querySelectorAll('div, button, span, a')]
            .find((el) => {
              const text = (el.textContent || '').replace(/\s+/g, '').trim();
              return text === '验证' && Boolean(el.closest('[class*="second_verify"], article[class*="uc_verification_component_layout"]'));
            });
          const className = verifyBtn?.className?.toString?.() || '';
          return {
            value: input ? input.value : '',
            verifyEnabled: Boolean(verifyBtn) && !/disabled/i.test(className),
            verifyClassName: className,
          };
        }, SMS_CODE_INPUT);
        console.log(`[ops] 验证码填入结果: value="${inputState.value}", verifyEnabled=${inputState.verifyEnabled}`);

        await sleep(300);

        if (inputState.value !== smsCode || !inputState.verifyEnabled) {
          return {
            ok: true,
            loggedIn: false,
            phase: 'sms_code_input',
            message: '验证码未成功写入二次验证输入框，或验证按钮仍未启用。请发送最新验证码后重试。',
          };
        }

        // 点击「验证」按钮：直接在二次验证弹层内按可见文本定位，避免点到底层登录表单。
        const verifyTarget = await op.page.evaluate(() => {
          const visible = (el) => {
            const rect = el.getBoundingClientRect();
            const style = getComputedStyle(el);
            return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
          };
          const candidates = [...document.querySelectorAll('button, div, span, a')]
            .filter((el) => {
              if (!visible(el)) return false;
              const text = (el.textContent || '').replace(/\s+/g, '').trim();
              if (text !== '验证') return false;
              if (!el.closest('[class*="second_verify"], article[class*="uc_verification_component_layout"]')) return false;
              const className = el.className?.toString?.() || '';
              const disabled = el.disabled || el.getAttribute('aria-disabled') === 'true' || /disabled/i.test(className);
              return !disabled;
            })
            .sort((a, b) => {
              const ac = a.className?.toString?.() || '';
              const bc = b.className?.toString?.() || '';
              const as = /primary|btn/.test(ac) ? 0 : 1;
              const bs = /primary|btn/.test(bc) ? 0 : 1;
              if (as !== bs) return as - bs;
              const ar = a.getBoundingClientRect();
              const br = b.getBoundingClientRect();
              return (ar.width * ar.height) - (br.width * br.height);
            });
          const el = candidates[0];
          if (!el) return { found: false };
          const rect = el.getBoundingClientRect();
          return {
            found: true,
            x: rect.x + rect.width / 2,
            y: rect.y + rect.height / 2,
            width: rect.width,
            height: rect.height,
            text: (el.textContent || '').replace(/\s+/g, ' ').trim(),
            className: el.className?.toString?.() || '',
          };
        });

        let verifyBtnResult = { ok: false, error: 'verify_button_not_found', target: verifyTarget };
        if (verifyTarget.found) {
          closeBrowserNativePrompts();
          await sleep(200);
          await op.page.mouse.move(verifyTarget.x, verifyTarget.y);
          await sleep(120);
          await op.page.mouse.click(verifyTarget.x, verifyTarget.y);
          verifyBtnResult = { ok: true, target: verifyTarget };
        }

        if (!verifyBtnResult.ok) {
          return {
            ok: true,
            loggedIn: false,
            phase: 'sms_code_submitted',
            message: '验证码已输入但未找到验证按钮，请手动点击验证按钮后再次调用本接口',
          };
        }

        console.log('[ops] 已点击验证按钮，等待页面跳转...');

        const navTimeout = 15_000;
        const verifyDone = await Promise.race([
          op.page.waitForNavigation({ waitUntil: 'networkidle2', timeout: navTimeout })
            .then(() => 'navigated')
            .catch(() => null),
          op.waitFor((sel) => {
            return !document.querySelector(sel);
          }, { timeout: navTimeout, interval: 500, args: [SMS_CODE_INPUT] })
            .then(r => r.ok ? 'element_gone' : null),
        ]);

        if (!verifyDone) {
          return {
            ok: true,
            loggedIn: false,
            phase: 'sms_code_submitted',
            message: '验证码已输入，但页面尚未跳转。可能验证码有误或需要等待，请稍后再次调用本接口检测状态',
          };
        }

        console.log(`[ops] 验证页面已变化 (${verifyDone})，等待稳定...`);
        await sleep(1000);
        let postVerifyState;
        try {
          postVerifyState = await op.query(() => {
            const text = document.body?.innerText || '';
            const visible = (el) => {
              const rect = el.getBoundingClientRect();
              const style = getComputedStyle(el);
              return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
            };
            const hasLoginGate = /扫码登录|验证码登录|密码登录|登录\/注册/.test(text)
              || [...document.querySelectorAll('img[aria-label="二维码"]')].some(visible);
            const hasSmsInput = [...document.querySelectorAll('input[placeholder*="验证码"], #button-input')]
              .some((el) => visible(el) && Boolean(el.closest('[class*="second_verify"], article[class*="uc_verification_component_layout"]')));
            const hasCreatorHome = location.href.includes('creator.douyin.com')
              && !hasLoginGate
              && (/发布|内容管理|创作者中心/.test(text) || Boolean(document.querySelector('[class*="avatar"], img[class*="avatar"]')));
            return {
              hasLoginGate,
              hasSmsInput,
              hasCreatorHome,
              url: location.href,
            };
          });
        } catch (err) {
          if (!/Execution context was destroyed|Cannot find context|navigation/i.test(err.message || '')) throw err;
          await sleep(2000);
          postVerifyState = await op.query(() => {
            const text = document.body?.innerText || '';
            const hasLoginGate = /扫码登录|验证码登录|密码登录|登录\/注册/.test(text);
            return {
              hasLoginGate,
              hasSmsInput: /请输入验证码|短信验证码/.test(text),
              hasCreatorHome: location.href.includes('creator.douyin.com') && !hasLoginGate
                && (/发布|内容管理|创作者中心/.test(text) || Boolean(document.querySelector('[class*="avatar"], img[class*="avatar"]'))),
              url: location.href,
              recoveredFromNavigation: true,
            };
          });
        }
        if (postVerifyState.hasCreatorHome) {
          return { ok: true, loggedIn: true, phase: 'logged_in' };
        }
        if (postVerifyState.hasSmsInput) {
          return {
            ok: true,
            loggedIn: false,
            phase: 'sms_code_input',
            message: '验证码已提交，但页面仍停留在短信输入界面，请确认是否需要重新提交最新验证码。',
          };
        }
        return {
          ok: true,
          loggedIn: false,
          phase: 'page_loading',
          message: postVerifyState.hasLoginGate
            ? '验证码已提交，页面仍在加载，请稍后再检查登录状态。'
            : '验证码已提交，正在确认是否进入创作者后台，请稍后再检查登录状态。',
        };
      }

      // ── 第3优先级：检测身份验证界面（扫码后的验证码/设备验证支线） ──
      const smsVerification = await op.query(() => {
        const text = document.body?.innerText || '';
        const visible = (el) => {
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const baseLoginQr = [...document.querySelectorAll('img[aria-label="二维码"]')]
          .some((el) => visible(el));
        const hasSecurityPanel = /身份验证|为保障账号安全|手机验证|接收短信验证码|发送短信验证|手机刷脸验证|验证登录密码/.test(text);
        if (!hasSecurityPanel || (baseLoginQr && !/身份验证|为保障账号安全|手机验证/.test(text))) {
          return { found: false };
        }

        const candidates = [...document.querySelectorAll('div, button')]
          .filter((el) => visible(el) && /^(接收短信验证码|发送短信验证|短信验证|验证码登录|获取验证码|发送验证码)$/.test((el.textContent || '').replace(/\s+/g, '').trim()))
          .sort((a, b) => {
            const ar = a.getBoundingClientRect();
            const br = b.getBoundingClientRect();
            return (ar.width * ar.height) - (br.width * br.height);
          });
        const target = candidates.find((el) => {
          const className = el.className?.toString?.() || '';
          const panel = el.closest('[class*="second_verify"], [class*="verification"]');
          return Boolean(panel) && className.includes('list_item');
        }) || candidates.find((el) => {
          const panel = el.closest('[class*="second_verify"], [class*="verification"]');
          return Boolean(panel);
        }) || candidates[0];
        if (!target) return { found: false };
        const rect = target.getBoundingClientRect();
        return {
          found: true,
          x: rect.x + rect.width / 2,
          y: rect.y + rect.height / 2,
          width: rect.width,
          height: rect.height,
          text: (target.textContent || '').replace(/\s+/g, ' ').trim(),
          className: target.className?.toString?.() || '',
        };
      });

      if (smsVerification.found) {
        console.log('[ops] 检测到身份验证界面，自动点击「接收短信验证码」...');

        let clickResult = { ok: false, error: 'sms_option_not_found' };
        if (smsVerification.x && smsVerification.y) {
          closeBrowserNativePrompts();
          await sleep(200);
          await op.page.mouse.move(smsVerification.x, smsVerification.y);
          await sleep(80);
          await op.page.mouse.click(smsVerification.x, smsVerification.y);
          clickResult = { ok: true, target: smsVerification };
        }

        if (clickResult.ok) {
          console.log('[ops] 已点击短信验证选项，等待验证码输入界面...');
          let changed = await op.waitFor((sel) => {
            const text = document.body?.innerText || '';
            const input = [...document.querySelectorAll(sel)].find((el) => Boolean(el.closest('[class*="second_verify"], article[class*="uc_verification_component_layout"]')));
            const hasInput = input && input.getBoundingClientRect().width > 0 && input.getBoundingClientRect().height > 0;
            const stillOnChoice = /身份验证|手机验证/.test(text) && /接收短信验证码|发送短信验证|短信验证|验证码登录|获取验证码|手机刷脸验证|验证登录密码/.test(text);
            return hasInput ? 'code_input' : (!stillOnChoice ? 'choice_gone' : false);
          }, { timeout: 5000, interval: 300, args: [SMS_CODE_INPUT] });

          if (!changed.ok) {
            const fallback = await op.page.evaluate(() => {
              const visible = (el) => {
                const rect = el.getBoundingClientRect();
                const style = getComputedStyle(el);
                return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
              };
              const target = [...document.querySelectorAll('div, button')]
                .filter((el) => visible(el) && /^(接收短信验证码|发送短信验证|短信验证|验证码登录|获取验证码|发送验证码)$/.test((el.textContent || '').replace(/\s+/g, '').trim()))
                .sort((a, b) => {
                  const ac = a.className?.toString?.() || '';
                  const bc = b.className?.toString?.() || '';
                  const as = ac.includes('list_item') ? 0 : 1;
                  const bs = bc.includes('list_item') ? 0 : 1;
                  if (as !== bs) return as - bs;
                  const ar = a.getBoundingClientRect();
                  const br = b.getBoundingClientRect();
                  return (br.width * br.height) - (ar.width * ar.height);
                })[0];
              if (!target) return { ok: false, reason: 'target_not_found' };
              const rect = target.getBoundingClientRect();
              const init = { bubbles: true, cancelable: true, clientX: rect.x + rect.width / 2, clientY: rect.y + rect.height / 2 };
              target.scrollIntoView({ block: 'center', inline: 'center' });
              target.focus?.();
              target.dispatchEvent(new PointerEvent('pointerdown', { ...init, pointerId: 1, pointerType: 'mouse' }));
              target.dispatchEvent(new MouseEvent('mousedown', init));
              target.dispatchEvent(new PointerEvent('pointerup', { ...init, pointerId: 1, pointerType: 'mouse' }));
              target.dispatchEvent(new MouseEvent('mouseup', init));
              target.dispatchEvent(new MouseEvent('click', init));
              target.click?.();
              return {
                ok: true,
                text: (target.textContent || '').replace(/\s+/g, ' ').trim(),
                className: target.className?.toString?.() || '',
              };
            });
            if (fallback.ok) {
              changed = await op.waitFor((sel) => {
                const text = document.body?.innerText || '';
                const input = [...document.querySelectorAll(sel)].find((el) => Boolean(el.closest('[class*="second_verify"], article[class*="uc_verification_component_layout"]')));
                const hasInput = input && input.getBoundingClientRect().width > 0 && input.getBoundingClientRect().height > 0;
                const stillOnChoice = /身份验证|手机验证/.test(text) && /接收短信验证码|发送短信验证|短信验证|验证码登录|获取验证码|手机刷脸验证|验证登录密码/.test(text);
                return hasInput ? 'code_input' : (!stillOnChoice ? 'choice_gone' : false);
              }, { timeout: 5000, interval: 300, args: [SMS_CODE_INPUT] });
            }
          }

          if (!changed.ok) {
            console.warn('[ops] 点击短信验证选项后页面未变化');
            return {
              ok: true,
              loggedIn: false,
              phase: 'sms_verification',
              clicked: false,
              clickTarget: smsVerification,
              message: '检测到身份验证界面，但自动点击短信验证后页面未变化。请在浏览器中手动点击「接收短信验证码」或「发送短信验证」。',
            };
          }

          return {
            ok: true,
            loggedIn: false,
            phase: changed.result === 'code_input' ? 'sms_code_input' : 'sms_verification',
            clicked: true,
            clickTarget: smsVerification,
            message: changed.result === 'code_input'
              ? '已进入验证码输入界面，请查看手机短信，获取验证码后携带 smsCode 参数再次调用本接口'
              : '短信验证选项已点击，页面已变化；请再次调用本接口检查下一步状态',
          };
        } else {
          console.warn('[ops] 找到验证界面但点击失败，可能需要手动操作');
        }

        return {
          ok: true,
          loggedIn: false,
          phase: 'sms_verification',
          clicked: clickResult.ok,
          clickTarget: smsVerification,
          message: clickResult.ok
            ? '已点击「接收短信验证码」，请查看手机短信，获取验证码后携带 smsCode 参数再次调用本接口'
            : '检测到身份验证界面但自动点击失败，请手动点击「接收短信验证码」后再次调用本接口',
        };
      }

      const loginGate = await op.query(() => {
        const text = document.body?.innerText || '';
        const hasLoginText = /扫码登录|验证码登录|密码登录|登录\/注册/.test(text);
        const hasLoginInput = Boolean(document.querySelector('input[placeholder*="手机号"], #button-input[placeholder*="验证码"]'));
        return { found: hasLoginText || hasLoginInput };
      });
      if (loginGate.found) {
        return {
          ok: true,
          loggedIn: false,
          phase: 'qrcode',
          message: '当前仍在抖音登录页，但没有截取到可用二维码。',
        };
      }

      const creatorState = await op.query(() => {
        const text = document.body?.innerText || '';
        const visible = (el) => {
          if (!el) return false;
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const hasCreatorHome = location.href.includes('creator.douyin.com')
          && /高清发布|内容管理|作品管理|数据中心|创作中心|发布视频|创作者中心/.test(text)
          && !/扫码登录|验证码登录|密码登录|登录\/注册/.test(text);
        const hasAvatar = [...document.querySelectorAll('[class*="avatar"], img[class*="avatar"]')].some(visible);
        return {
          hasCreatorHome: Boolean(hasCreatorHome || (hasAvatar && /发布|内容管理|创作者/.test(text))),
          url: location.href,
          title: document.title,
          textLength: text.trim().length,
          textSample: text.replace(/\s+/g, ' ').slice(0, 300),
        };
      });
      if (creatorState.hasCreatorHome) {
        return { ok: true, loggedIn: true, phase: 'logged_in' };
      }

      return {
        ok: true,
        loggedIn: false,
        phase: 'page_loading',
        message: '页面仍在加载，尚未确认登录状态。',
        detail: creatorState,
      };
    },

    async _clickSmsCodeSender(opts = {}) {
      const { allowResend = false, context = 'login' } = opts;
      const before = await op.query(() => document.body?.innerText || '');
      const target = await op.query((allowResendInner, contextInner) => {
        const visible = (el) => {
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
        };
        const scoreText = (text) => {
          if (/^重新/.test(text)) return allowResendInner ? 0 : 99;
          if (/^(获取验证码|发送验证码)$/.test(text)) return 1;
          if (text === '接收短信验证码') return 2;
          if (contextInner !== 'publish' && text === '发送短信验证') return 4;
          if (contextInner !== 'publish' && text === '短信验证') return 5;
          return 50;
        };
        const candidates = [...document.querySelectorAll('button, div, span, a')]
          .filter((el) => {
            const text = (el.textContent || '').replace(/\s+/g, '').trim();
            const allowed = contextInner === 'publish'
              ? (allowResendInner
                ? /^(获取验证码|重新获取|重新发送|发送验证码|接收短信验证码)$/
                : /^(获取验证码|发送验证码|接收短信验证码)$/)
              : (allowResendInner
                ? /^(获取验证码|重新获取|重新发送|发送验证码|接收短信验证码|发送短信验证|短信验证)$/
                : /^(获取验证码|发送验证码|接收短信验证码|发送短信验证|短信验证)$/);
            if (!allowed.test(text)) return false;
            if (!visible(el)) return false;
            if (contextInner === 'publish') {
              const panelText = (el.closest('[class*="second-verify"], [class*="verification"], [class*="verify"], [class*="modal"], article')?.innerText || document.body?.innerText || '');
              if (/编辑短信|发送至|可能产生费用/.test(panelText)) return false;
            }
            return Boolean(el.closest('[class*="second_verify"], [class*="verification"], [class*="verify"], [class*="modal"], article, body'));
          })
          .sort((a, b) => {
            const at = (a.textContent || '').replace(/\s+/g, '').trim();
            const bt = (b.textContent || '').replace(/\s+/g, '').trim();
            const as = scoreText(at);
            const bs = scoreText(bt);
            if (as !== bs) return as - bs;
            const ar = a.getBoundingClientRect();
            const br = b.getBoundingClientRect();
            return (ar.width * ar.height) - (br.width * br.height);
          });
        const el = candidates[0];
        if (!el) return { found: false };
        const rect = el.getBoundingClientRect();
        return {
          found: true,
          x: rect.x + rect.width / 2,
          y: rect.y + rect.height / 2,
          text: (el.textContent || '').replace(/\s+/g, ' ').trim(),
        };
      }, allowResend, context);
      if (!target.found) return { ok: false, reason: 'send_code_button_not_found' };
      closeBrowserNativePrompts();
      await sleep(200);
      await op.page.mouse.click(target.x, target.y);
      await sleep(1200);
      const after = await op.query(() => document.body?.innerText || '');
      return {
        ok: true,
        target,
        changed: before !== after || /重新获取|后重新获取|验证码已发送|已发送|\d+\s*s|\d+\s*秒/.test(after),
      };
    },

    /**
     * 导航到指定的抖音页面
     * @param {string} url
     * @param {object} [opts]
     */
    async navigateTo(url, opts = {}) {
      const { timeout = 30_000 } = opts;

      // 安全检查：只允许抖音域名
      try {
        const parsed = new URL(url);
        if (!parsed.hostname.endsWith('douyin.com')) {
          return { ok: false, error: 'invalid_domain', detail: `仅允许 douyin.com 域名，收到: ${parsed.hostname}` };
        }
      } catch {
        return { ok: false, error: 'invalid_url', detail: url };
      }

      const start = Date.now();
      try {
        await op.page.goto(url, { waitUntil: 'networkidle2', timeout });
        return { ok: true, url: op.url(), elapsed: Date.now() - start };
      } catch (err) {
        return { ok: false, error: 'navigation_failed', detail: err.message, elapsed: Date.now() - start };
      }
    },

    /**
     * 刷新页面
     */
    async reloadPage(opts = {}) {
      const { timeout = 30_000 } = opts;
      const start = Date.now();
      try {
        await op.page.reload({ waitUntil: 'networkidle2', timeout });
        return { ok: true, elapsed: Date.now() - start };
      } catch (err) {
        return { ok: false, error: 'reload_failed', detail: err.message, elapsed: Date.now() - start };
      }
    },

    /**
     * 发送文本消息并等待页面响应
     * 通用方法：向某个输入框填入文本并提交
     * @param {string} text
     * @param {object} [opts]
     */
    async fillAndSubmit(text, opts = {}) {
      const { inputSelectors = SELECTORS.descriptionInput, submitSelectors = SELECTORS.hdPublishBtn } = opts;

      const fillResult = await op.fill(inputSelectors, text);
      if (!fillResult.ok) {
        return { ok: false, error: 'fill_failed', detail: fillResult };
      }

      await sleep(300);

      const clickResult = await op.click(submitSelectors);
      if (!clickResult.ok) {
        return { ok: false, error: 'submit_click_failed', detail: clickResult };
      }

      return { ok: true };
    },

    /**
     * 截图（调试用）
     */
    async screenshot(opts = {}) {
      const { path, fullPage = true } = opts;
      return op.screenshot({ path, fullPage, type: 'png' });
    },

    async verifyPublished(opts = {}) {
      const { title = '', waitMs = 8000 } = opts;
      try {
        await op.page.goto('https://creator.douyin.com/creator-micro/content/manage?enter_from=publish_verify', {
          waitUntil: 'domcontentloaded',
          timeout: 30_000,
        });
      } catch {
        // SPA navigation can keep loading after the timeout; inspect whatever rendered.
      }
      await sleep(waitMs);
      return op.query((expectedTitle) => {
        const text = document.body?.innerText || '';
        const loginGate = /扫码登录|验证码登录|密码登录|登录\/注册/.test(text);
        const statusHits = [...new Set((text.match(/审核中|已发布|发布成功|不通过|草稿|自动发布测试/g) || []))];
        return {
          ok: true,
          url: location.href,
          loggedIn: !loginGate,
          loginGate,
          found: expectedTitle ? text.includes(expectedTitle) : false,
          statusHits,
          textSample: text.replace(/\s+/g, ' ').slice(0, 1500),
        };
      }, title);
    },
  };
}
