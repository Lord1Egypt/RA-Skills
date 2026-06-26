# WebVoyager — Code Examples

## Example 1

```typescript
// webvoyager.ts
interface WebTask {
  instruction: string;
  startUrl: string;
  expectedOutcome: string;
  maxSteps: number;
}

interface PageState {
  screenshot: Buffer;
  html: string;
  accessibilityTree: A11yNode[];
  interactiveElements: InteractiveElement[];
  annotatedScreenshot?: Buffer;
}

interface InteractiveElement {
  id: string;
  type: 'button' | 'link' | 'input' | 'select' | 'checkbox' | 'textarea';
  label: string;
  boundingBox: BoundingBox;
  attributes: Record<string, string>;
  isVisible: boolean;
  isEnabled: boolean;
}

interface Action {
  type: 'click' | 'type' | 'scroll' | 'navigate' | 'select' | 'wait' | 'extract';
  target?: string;
  value?: string;
  coordinates?: { x: number; y: number };
  reasoning: string;
}

class WebVoyager {
  private browser: Browser;
  private page: Page;
  private visionModel: VisionModel;
  private maxRetries = 3;

  constructor(config: WebVoyagerConfig) {
    this.visionModel = new VisionModel(config.visionBackend);
  }

  async executeTask(task: WebTask): Promise<TaskResult> {
    await this.initialize();
    await this.page.goto(task.startUrl);

    const history: StepHistory[] = [];
    let stepCount = 0;
    let taskCompleted = false;

    while (stepCount < task.maxSteps && !taskCompleted) {
      stepCount++;

      // Step 1: Capture current state
      const state = await this.capturePageState();

      // Step 2: Annotate screenshot with Set-of-Marks
      const annotatedState = await this.annotateWithMarks(state);

      // Step 3: Reason about next action
      const action = await this.decideNextAction(task, annotatedState, history);

      // Step 4: Execute action
      const result = await this.executeAction(action);

      // Step 5: Record history
      history.push({
        step: stepCount,
        state: annotatedState,
        action,
        result,
      });

      // Step 6: Check if task is completed
      taskCompleted = await this.checkTaskCompletion(task, annotatedState, history);

      // Wait for page to stabilize
      await this.waitForStability();
    }

    return {
      success: taskCompleted,
      steps: stepCount,
      history,
      finalState: await this.capturePageState(),
    };
  }

  // Set-of-Marks Annotation
  private async annotateWithMarks(state: PageState): Promise<AnnotatedPageState> {
    const marks: Mark[] = [];

    for (let i = 0; i < state.interactiveElements.length; i++) {
      const element = state.interactiveElements[i];
      if (!element.isVisible) continue;

      const mark: Mark = {
        id: i + 1,
        element,
        label: this.generateMarkLabel(element, i + 1),
        color: this.getMarkColor(element.type),
      };

      marks.push(mark);
    }

    // Render marks onto screenshot
    const annotatedScreenshot = await this.renderMarksOnScreenshot(
      state.screenshot,
      marks
    );

    return {
      ...state,
      annotatedScreenshot,
      marks,
    };
  }

  private generateMarkLabel(element: InteractiveElement, id: number): string {
    // Create concise label for the mark
    const typeIcon = this.getTypeIcon(element.type);
    const text = element.label || element.attributes['aria-label'] || element.attributes['placeholder'] || '';
    const shortText = text.length > 20 ? text.substring(0, 20) + '...' : text;

    return `[${id}] ${typeIcon} ${shortText}`;
  }

  private getTypeIcon(type: string): string {
    const icons: Record<string, string> = {
      button: 'BTN',
      link: 'LINK',
      input: 'INPUT',
      select: 'SELECT',
      checkbox: 'CHECK',
      textarea: 'TEXT',
    };
    return icons[type] || 'ELEM';
  }

  private getMarkColor(type: string): string {
    const colors: Record<string, string> = {
      button: '#FF6B6B',
      link: '#4ECDC4',
      input: '#45B7D1',
      select: '#96CEB4',
      checkbox: '#FFEAA7',
      textarea: '#DDA0DD',
    };
    return colors[type] || '#808080';
  }

  // Multimodal Reasoning
  private async decideNextAction(
    task: WebTask,
    state: AnnotatedPageState,
    history: StepHistory[]
  ): Promise<Action> {
    // Prepare context for vision model
    const prompt = this.buildReasoningPrompt(task, state, history);

    // Send annotated screenshot and prompt to vision model
    const response = await this.visionModel.analyze({
      image: state.annotatedScreenshot,
      prompt,
      systemPrompt: this.getSystemPrompt(),
    });

    // Parse action from response
    return this.parseAction(response, state);
  }

  private buildReasoningPrompt(
    task: WebTask,
    state: AnnotatedPageState,
    history: StepHistory[]
  ): string {
    let prompt = `## Task
${task.instruction}

## Current Page
URL: ${this.page.url()}
Title: ${await this.page.title()}

## Interactive Elements (marked on screenshot)
`;

    for (const mark of state.marks) {
      prompt += `[${mark.id}] ${mark.element.type}: "${mark.element.label}" `;
      if (mark.element.attributes['href']) {
        prompt += `(href: ${mark.element.attributes['href']})`;
      }
      prompt += '\n';
    }

    if (history.length > 0) {
      prompt += '\n## Previous Actions\n';
      for (const step of history.slice(-5)) { // Last 5 steps
        prompt += `Step ${step.step}: ${step.action.type}`;
        if (step.action.target) prompt += ` on "${step.action.target}"`;
        if (step.action.value) prompt += ` with value "${step.action.value}"`;
        prompt += ` - ${step.result.success ? 'Success' : 'Failed'}\n`;
      }
    }

    prompt += `
## Instructions
1. Look at the annotated screenshot
2. Identify which element to interact with based on the task
3. Choose the appropriate action type
4. Provide your reasoning

## Response Format
{
  "reasoning": "explanation of why this action",
  "action": {
    "type": "click|type|scroll|navigate|select|wait|extract",
    "target": "[mark_id] or element description",
    "value": "value for type/select actions (optional)"
  }
}`;

    return prompt;
  }

  private getSystemPrompt(): string {
    return `You are WebVoyager, an expert web automation agent. You analyze screenshots with numbered marks overlaid on interactive elements.

Your capabilities:
- Understand visual layout and UI patterns
- Read text from screenshots
- Identify interactive elements by their marks [1], [2], etc.
- Navigate websites to complete tasks
- Fill forms and submit data
- Extract information from pages

Rules:
1. Always reference elements by their mark number [N]
2. Explain your reasoning before choosing an action
3. If stuck, try scrolling to reveal more elements
4. Wait for page loads after navigation
5. Verify actions succeeded before proceeding`;
  }

  // Action Execution
  private async executeAction(action: Action): Promise<ActionResult> {
    try {
      switch (action.type) {
        case 'click':
          return await this.executeClick(action);
        case 'type':
          return await this.executeType(action);
        case 'scroll':
          return await this.executeScroll(action);
        case 'navigate':
          return await this.executeNavigate(action);
        case 'select':
          return await this.executeSelect(action);
        case 'wait':
          return await this.executeWait(action);
        case 'extract':
          return await this.executeExtract(action);
        default:
          return { success: false, error: `Unknown action type: ${action.type}` };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  private async executeClick(action: Action): Promise<ActionResult> {
    const element = await this.resolveTarget(action.target);
    if (!element) {
      return { success: false, error: 'Element not found' };
    }

    await element.click();
    return { success: true };
  }

  private async executeType(action: Action): Promise<ActionResult> {
    const element = await this.resolveTarget(action.target);
    if (!element) {
      return { success: false, error: 'Element not found' };
    }

    // Clear existing content
    await element.fill('');
    // Type new content
    await element.type(action.value || '');
    return { success: true };
  }

  private async executeScroll(action: Action): Promise<ActionResult> {
    const direction = action.value || 'down';
    const distance = direction === 'up' ? -500 : 500;
    await this.page.mouse.wheel(0, distance);
    return { success: true };
  }

  private async executeNavigate(action: Action): Promise<ActionResult> {
    await this.page.goto(action.value || '');
    await this.page.waitForLoadState('networkidle');
    return { success: true };
  }

  private async resolveTarget(target: string | undefined): Promise<ElementHandle | null> {
    if (!target) return null;

    // Check if target is a mark reference [N]
    const markMatch = target.match(/\[(\d+)\]/);
    if (markMatch) {
      const markId = parseInt(markMatch[1]);
      const state = await this.capturePageState();
      const element = state.interactiveElements[markId - 1];
      if (element) {
        return await this.page.$(this.buildSelector(element));
      }
    }

    // Try as CSS selector
    return await this.page.$(target);
  }

  // Page State Capture
  private async capturePageState(): Promise<PageState> {
    const screenshot = await this.page.screenshot({ type: 'png' });
    const html = await this.page.content();
    const accessibilityTree = await this.getAccessibilityTree();
    const interactiveElements = await this.findInteractiveElements();

    return {
      screenshot,
      html,
      accessibilityTree,
      interactiveElements,
    };
  }

  private async findInteractiveElements(): Promise<InteractiveElement[]> {
    return await this.page.evaluate(() => {
      const elements: InteractiveElement[] = [];
      const selectors = [
        'button',
        'a[href]',
        'input',
        'select',
        'textarea',
        '[role="button"]',
        '[role="link"]',
        '[onclick]',
        '[tabindex]',
      ];

      const found = document.querySelectorAll(selectors.join(','));

      found.forEach((el, index) => {
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 || rect.height === 0) return;

        const style = window.getComputedStyle(el);
        if (style.display === 'none' || style.visibility === 'hidden') return;

        elements.push({
          id: `elem-${index}`,
          type: this.getElementType(el),
          label: this.getElementLabel(el),
          boundingBox: {
            x: rect.x,
            y: rect.y,
            width: rect.width,
            height: rect.height,
          },
          attributes: this.getElementAttributes(el),
          isVisible: true,
          isEnabled: !(el as HTMLInputElement).disabled,
        });
      });

      return elements;
    });
  }

  // Task Completion Check
  private async checkTaskCompletion(
    task: WebTask,
    state: AnnotatedPageState,
    history: StepHistory[]
  ): Promise<boolean> {
    const prompt = `## Task
${task.instruction}

## Expected Outcome
${task.expectedOutcome}

## Current Page
URL: ${this.page.url()}
Title: ${await this.page.title()}

## Question
Has the task been completed? Look at the screenshot and determine if the expected outcome has been achieved.

Respond with JSON:
{
  "completed": true/false,
  "confidence": 0.0-1.0,
  "reason": "explanation"
}`;

    const response = await this.visionModel.analyze({
      image: state.annotatedScreenshot,
      prompt,
    });

    const result = JSON.parse(response);
    return result.completed && result.confidence > 0.8;
  }

  // Helpers
  private async waitForStability(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
    await this.page.waitForTimeout(500);
  }

  private async initialize(): Promise<void> {
    const playwright = await import('playwright');
    this.browser = await playwright.chromium.launch({ headless: true });
    this.page = await this.browser.newPage();
    await this.page.setViewportSize({ width: 1280, height: 800 });
  }

  async close(): Promise<void> {
    await this.browser?.close();
  }
}

interface TaskResult {
  success: boolean;
  steps: number;
  history: StepHistory[];
  finalState: PageState;
}

interface StepHistory {
  step: number;
  state: AnnotatedPageState;
  action: Action;
  result: ActionResult;
}

interface ActionResult {
  success: boolean;
  error?: string;
  data?: any;
}

interface Mark {
  id: number;
  element: InteractiveElement;
  label: string;
  color: string;
}

interface AnnotatedPageState extends PageState {
  marks: Mark[];
}

interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

export { WebVoyager, WebTask, TaskResult };
```
