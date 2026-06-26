import { resolveImageAspectRatio, resolveImageModel, ImageModel, ModelDisplayName } from './constants.js';
import { AuthError, GenerationError } from './exceptions.js';
import { get_auth_token, type AuthResult } from './utils/get-auth-token.js';
import { type CookieMap } from './utils/cookie-file.js';
import { sleep } from './utils/http.js';
import { logger } from './utils/logger.js';
import {
  CdpConnection,
  get_cdp_port,
  wait_for_chrome_debug_port,
  ensure_chrome_cdp,
} from './utils/load-browser-cookies.js';

export type FlowClientOptions = {
  verbose?: boolean;
};

export type GenerateImagesOptions = {
  prompt: string;
  model?: string;
  aspect?: string;
  count?: number;
  projectId?: string;
};

export type GenerationResult = {
  projectId: string;
};

export class FlowClient {
  public accessToken: string | null = null;
  public cookies: CookieMap = {};
  public verbose: boolean;

  private cdp: CdpConnection | null = null;
  private cdpSessionId: string | null = null;
  private _initialized = false;

  constructor(opts: FlowClientOptions = {}) {
    this.verbose = opts.verbose ?? false;
  }

  /** Initialize: get OAuth token + connect CDP */
  async init(): Promise<void> {
    if (this._initialized) return;

    // Get auth token
    let auth: AuthResult;
    try {
      auth = await get_auth_token(this.verbose);
    } catch (e) {
      throw new AuthError(`Failed to authenticate: ${e instanceof Error ? e.message : String(e)}`);
    }

    this.accessToken = auth.accessToken;
    this.cookies = auth.cookies;

    // Connect to Chrome CDP for UI automation
    await this.ensureCdp();

    this._initialized = true;
    logger.success('Flow client initialized (UI automation mode).');
  }

  private async ensureCdp(): Promise<void> {
    if (this.cdp && this.cdpSessionId) return;

    const port = get_cdp_port();
    await ensure_chrome_cdp(this.verbose);
    const wsUrl = await wait_for_chrome_debug_port(port, 30_000);
    this.cdp = await CdpConnection.connect(wsUrl, 15_000);

    // Find or create a Flow tab
    const targets = await this.cdp.send<{ targetInfos: Array<{ targetId: string; url: string; type: string }> }>('Target.getTargets');
    let flowTab = targets.targetInfos.find(t => t.type === 'page' && t.url.includes('labs.google/fx'));

    let targetId: string;
    if (flowTab) {
      targetId = flowTab.targetId;
      if (this.verbose) logger.debug(`Reusing existing Flow tab: ${flowTab.url}`);
    } else {
      const res = await this.cdp.send<{ targetId: string }>('Target.createTarget', {
        url: 'https://labs.google/fx/zh/tools/flow',
        newWindow: false,
      });
      targetId = res.targetId;
      await sleep(8000); // Wait for page to load
    }

    const { sessionId } = await this.cdp.send<{ sessionId: string }>('Target.attachToTarget', { targetId, flatten: true });
    this.cdpSessionId = sessionId;
    await this.cdp.send('Runtime.enable', {}, { sessionId });
  }

  private async getCurrentUrl(): Promise<string> {
    if (!this.cdp || !this.cdpSessionId) throw new Error('CDP not connected');

    return (await this.cdp.send<{ result: { value?: string } }>('Runtime.evaluate', {
      expression: 'location.href',
      returnByValue: true,
    }, { sessionId: this.cdpSessionId }))?.result?.value || '';
  }

  private async waitForProjectUrl(timeoutMs: number): Promise<string | null> {
    const start = Date.now();

    while (Date.now() - start < timeoutMs) {
      const url = await this.getCurrentUrl();
      const projectId = url.match(/project\/([a-f0-9-]+)/)?.[1];
      if (projectId) return projectId;
      await sleep(500);
    }

    return null;
  }

  private async waitForListingCreateButton(timeoutMs: number): Promise<void> {
    if (!this.cdp || !this.cdpSessionId) throw new Error('CDP not connected');

    const start = Date.now();
    while (Date.now() - start < timeoutMs) {
      const status = (await this.cdp.send<{ result: { value?: string } }>('Runtime.evaluate', {
        expression: `(() => {
          const urlOk = location.href.includes('/tools/flow');
          const ready = document.readyState === 'complete' || document.readyState === 'interactive';
          const hasCreate = Array.from(document.querySelectorAll('a, button')).some((el) => {
            const text = (el.textContent || '').replace(/\\s+/g, ' ').trim();
            return text.includes('新建项目') || text.includes('New project') || text.includes('Create project');
          });
          return urlOk && ready && hasCreate ? 'ready' : 'waiting';
        })()`,
        returnByValue: true,
      }, { sessionId: this.cdpSessionId }))?.result?.value;

      if (status === 'ready') return;
      await sleep(500);
    }

    throw new GenerationError('Flow listing did not become ready for UI project creation.');
  }

  private async clickCreateProjectButton(): Promise<boolean> {
    if (!this.cdp || !this.cdpSessionId) throw new Error('CDP not connected');

    const result = (await this.cdp.send<{ result: { value?: string } }>('Runtime.evaluate', {
      expression: `(() => {
        const normalize = (value) => (value || '').replace(/\\s+/g, ' ').trim();
        const isVisible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);

        const candidates = Array.from(document.querySelectorAll('a, button'));
        for (const el of candidates) {
          const text = normalize(el.textContent);
          if (!isVisible(el)) continue;
          if (text.includes('新建项目') || text.includes('New project') || text.includes('Create project')) {
            el.click();
            return 'clicked';
          }
        }

        return 'not-found';
      })()`,
      returnByValue: true,
    }, { sessionId: this.cdpSessionId }))?.result?.value;

    return result === 'clicked';
  }

  /**
   * Navigate to a project page in the browser and wait for it to load.
   */
  private async navigateToProject(projectId: string): Promise<void> {
    if (!this.cdp || !this.cdpSessionId) throw new Error('CDP not connected');

    const url = `https://labs.google/fx/zh/tools/flow/project/${projectId}`;
    if (this.verbose) logger.debug(`Navigating to project: ${projectId}`);

    const currentUrl = await this.getCurrentUrl();
    if (currentUrl.includes(`/project/${projectId}`)) {
      if (this.verbose) logger.debug('Already on project page');
      return;
    }

    await this.cdp.send('Page.navigate', { url }, { sessionId: this.cdpSessionId });

    const resolvedProjectId = await this.waitForProjectUrl(20_000);
    if (resolvedProjectId !== projectId) {
      const finalUrl = await this.getCurrentUrl();
      throw new GenerationError(`Failed to navigate to project page. URL: ${finalUrl}`);
    }
  }

  /**
   * Navigate to Flow listing and create a project through the UI.
   */
  private async createProjectViaUI(): Promise<string> {
    if (!this.cdp || !this.cdpSessionId) throw new Error('CDP not connected');

    for (let attempt = 1; attempt <= 2; attempt++) {
      await this.cdp.send('Page.navigate', {
        url: 'https://labs.google/fx/zh/tools/flow',
      }, { sessionId: this.cdpSessionId });

      await this.waitForListingCreateButton(20_000);

      const clicked = await this.clickCreateProjectButton();
      if (!clicked) {
        throw new GenerationError('Could not find the UI "新建项目" button on the Flow listing page.');
      }

      const projectId = await this.waitForProjectUrl(20_000);
      if (projectId) {
        if (this.verbose) logger.debug(`Created project via UI: ${projectId}`);
        return projectId;
      }

      if (this.verbose) logger.debug(`UI project creation attempt ${attempt} did not reach a project page, retrying...`);
    }

    const finalUrl = await this.getCurrentUrl();
    throw new GenerationError(`Failed to create project via UI. URL: ${finalUrl}`);
  }

  /**
   * Configure the UI: select direction (横向/纵向), count (x1-x4), and model.
   */
  private async configureUI(model: string, aspect: string, count: number): Promise<void> {
    if (!this.cdp || !this.cdpSessionId) throw new Error('CDP not connected');

    const modelDisplay = ModelDisplayName[model] || model;
    const isPortrait = aspect.includes('PORTRAIT');

    if (this.verbose) logger.debug(`Configuring UI: model=${modelDisplay}, aspect=${isPortrait ? '纵向' : '横向'}, count=x${count}`);

    // 1. Direction: click 横向 or 纵向 button
    const dirLabel = isPortrait ? '纵向' : '横向';
    await this.cdp.send('Runtime.evaluate', {
      expression: `(() => {
        for (const btn of document.querySelectorAll('button')) {
          const t = btn.textContent?.trim();
          if (t === '${dirLabel}') { btn.click(); return 'clicked'; }
        }
        return 'not-found';
      })()`,
      returnByValue: true,
    }, { sessionId: this.cdpSessionId });
    await sleep(500);

    // 2. Count: click x1/x2/x3/x4 button
    const countLabel = `x${count}`;
    await this.cdp.send('Runtime.evaluate', {
      expression: `(() => {
        for (const btn of document.querySelectorAll('button')) {
          const t = btn.textContent?.trim();
          if (t === '${countLabel}') { btn.click(); return 'clicked'; }
        }
        return 'not-found';
      })()`,
      returnByValue: true,
    }, { sessionId: this.cdpSessionId });
    await sleep(500);

    // 3. Model: click current model button to open dropdown, then select target
    // a. Find and click the model selector button (contains "Nano Banana")
    const openResult = (await this.cdp.send<{ result: { value?: string } }>('Runtime.evaluate', {
      expression: `(() => {
        for (const btn of document.querySelectorAll('button')) {
          const t = btn.textContent?.trim();
          if (t && t.includes('Nano Banana')) { btn.click(); return 'opened'; }
        }
        return 'not-found';
      })()`,
      returnByValue: true,
    }, { sessionId: this.cdpSessionId }))?.result?.value;

    if (openResult === 'opened') {
      await sleep(500);

      // b. Click the target model in the dropdown
      const targetModelName = modelDisplay; // e.g. "Nano Banana 2" or "Nano Banana Pro"
      await this.cdp.send('Runtime.evaluate', {
        expression: `(() => {
          // Look in dropdown/menu items for the target model name
          const candidates = document.querySelectorAll('[role="option"], [role="menuitem"], [role="listbox"] *, li, button');
          for (const el of candidates) {
            const t = el.textContent?.trim();
            if (t && t.includes('${targetModelName}')) { el.click(); return 'selected'; }
          }
          return 'not-found';
        })()`,
        returnByValue: true,
      }, { sessionId: this.cdpSessionId });
      await sleep(500);
    }

    if (this.verbose) logger.debug('UI configured');
  }

  /**
   * Input prompt into the Slate editor via CDP.
   */
  private async inputPrompt(prompt: string): Promise<void> {
    if (!this.cdp || !this.cdpSessionId) throw new Error('CDP not connected');

    // Focus the Slate editor
    await this.cdp.send('Runtime.evaluate', {
      expression: `document.querySelector('[data-slate-editor]')?.focus()`,
      returnByValue: true,
    }, { sessionId: this.cdpSessionId });
    await sleep(300);

    // Select all existing text
    await this.cdp.send('Input.dispatchKeyEvent', {
      type: 'keyDown', key: 'a', code: 'KeyA', modifiers: 2,
      windowsVirtualKeyCode: 65, nativeVirtualKeyCode: 65,
    }, { sessionId: this.cdpSessionId });
    await this.cdp.send('Input.dispatchKeyEvent', {
      type: 'keyUp', key: 'a', code: 'KeyA', modifiers: 2,
      windowsVirtualKeyCode: 65, nativeVirtualKeyCode: 65,
    }, { sessionId: this.cdpSessionId });
    await sleep(200);

    // Insert the prompt text
    await this.cdp.send('Input.insertText', { text: prompt }, { sessionId: this.cdpSessionId });
    await sleep(500);

    // Verify
    const editorText = (await this.cdp.send<{ result: { value?: string } }>('Runtime.evaluate', {
      expression: `document.querySelector('[data-slate-editor]')?.textContent || ''`,
      returnByValue: true,
    }, { sessionId: this.cdpSessionId }))?.result?.value || '';

    if (!editorText.includes(prompt.slice(0, 20))) {
      throw new GenerationError('Failed to input prompt into editor');
    }

    if (this.verbose) logger.debug(`Prompt entered: "${prompt.slice(0, 50)}..."`);
  }

  /**
   * Click the Create/Generate button.
   * Returns immediately after confirming the button was clicked.
   * Completion detection is handled by the LLM via browser screenshots.
   */
  private async clickCreate(): Promise<void> {
    if (!this.cdp || !this.cdpSessionId) throw new Error('CDP not connected');

    const clickResult = (await this.cdp.send<{ result: { value?: string } }>('Runtime.evaluate', {
      expression: `(() => {
        for (const btn of document.querySelectorAll('button')) {
          const t = btn.textContent?.trim();
          if (t?.includes('arrow_forward') && t?.includes('创建')) { btn.click(); return 'clicked'; }
        }
        // Fallback
        for (const btn of document.querySelectorAll('button')) {
          const t = btn.textContent?.trim();
          if (t?.includes('Create') || t?.includes('Generate')) { btn.click(); return 'clicked-fallback'; }
        }
        return 'not-found';
      })()`,
      returnByValue: true,
    }, { sessionId: this.cdpSessionId }))?.result?.value;

    if (clickResult === 'not-found') {
      throw new GenerationError('Create button not found on page');
    }

    if (this.verbose) logger.debug('Create button clicked');
  }

  /**
   * Generate images via UI automation.
   * Creates or reuses a Flow project through the UI, configures options, inputs the prompt, and clicks Create.
   */
  async generateImages(opts: GenerateImagesOptions): Promise<GenerationResult> {
    await this.ensureInit();

    const model = resolveImageModel(opts.model ?? ImageModel.NARWHAL);
    const aspect = resolveImageAspectRatio(opts.aspect ?? '16:9');
    const count = opts.count ?? 2;

    // Create project via UI (ensures proper page state)
    const projectId = opts.projectId ?? await this.createProjectViaUI();

    // Navigate to project if needed
    await this.navigateToProject(projectId);

    // Configure direction, count, and model in the UI
    await this.configureUI(model, aspect, count);

    // Input prompt
    await this.inputPrompt(opts.prompt);

    // Click create button (completion is detected by LLM via screenshots)
    logger.info(`Generating image: "${opts.prompt.slice(0, 60)}..."`);
    await this.clickCreate();

    logger.success('Generation complete.');

    return { projectId };
  }

  private async ensureInit(): Promise<void> {
    if (!this._initialized) await this.init();
    if (!this.accessToken) throw new AuthError('Not authenticated');
  }

  /** Clean up CDP connection */
  async close(): Promise<void> {
    this._initialized = false;
    this.accessToken = null;

    if (this.cdp) {
      this.cdp.close();
      this.cdp = null;
    }
    this.cdpSessionId = null;
  }
}
