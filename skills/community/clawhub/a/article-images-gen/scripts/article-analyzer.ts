import { writeFile, mkdir } from "node:fs/promises";
import path from "node:path";

type IllustrationPosition = {
  index: number;
  section: string;
  purpose: string;
  visualContent: string;
  filename: string;
};

export type OutlineData = {
  style: string;
  density: string;
  image_count: number;
  positions: IllustrationPosition[];
};

/** Convert text to a safe ASCII slug for filenames. Chinese chars use Unicode codepoint hex. */
function toSlug(text: string): string {
  return text
    .split("")
    .map((char) => {
      const code = char.charCodeAt(0);
      if (code >= 0x4e00 && code <= 0x9fff) {
        return code.toString(16);
      }
      return char.toLowerCase();
    })
    .join("")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 40) || "concept";
}

function buildIllustrationPositions(content: string): IllustrationPosition[] {
  const sections = content.split(/^##+\s+/m).filter((s) => s.trim());
  const positions: IllustrationPosition[] = [];

  for (let i = 0; i < sections.length && positions.length < 8; i++) {
    const section = sections[i]!;
    const sectionHeading = section.split("\n")[0]?.replace(/^#+\s*/, "").trim() || "";

    if (!sectionHeading) continue;

    const index = positions.length + 1;
    const filenameSlug = toSlug(sectionHeading);

    positions.push({
      index,
      section: sectionHeading,
      purpose: `Visualize key concept of ${sectionHeading}`,
      visualContent: `Illustrate the main idea of ${sectionHeading} in hand-drawn minimalist style`,
      filename: `${String(index).padStart(2, "0")}-hand-drawn-${filenameSlug}.png`,
    });
  }

  return positions;
}

function recommendDensity(content: string): string {
  const sections = content.split(/^##+\s+/m).filter((s) => s.trim());
  if (sections.length <= 3) return "minimal";
  if (sections.length <= 6) return "balanced";
  if (sections.length <= 10) return "per-section";
  return "rich";
}

function formatOutlineMarkdown(outline: OutlineData, articlePath: string): string {
  const header = `---
style: ${outline.style}
density: ${outline.density}
image_count: ${outline.image_count}
---

# Article Illustration Outline

Article: ${articlePath}
Style: Hand-drawn Minimalist
Density: ${outline.density}
Total Images: ${outline.image_count}

---

`;

  const body = outline.positions
    .map(
      (pos) => `## Illustration ${pos.index}

**Position**: ${pos.section}
**Purpose**: ${pos.purpose}
**Visual Content**: ${pos.visualContent}
**Filename**: ${pos.filename}

---
`
    )
    .join("\n");

  return header + body;
}

export async function generateOutline(
  articlePath: string,
  content: string,
  density: string,
  outputDir: string
): Promise<OutlineData> {
  let positions = buildIllustrationPositions(content);

  if (density === "minimal") {
    positions = positions.slice(0, 2);
  } else if (density === "balanced") {
    positions = positions.slice(0, 4);
  }
  // per-section and rich keep all positions

  const outline: OutlineData = {
    style: "hand-drawn",
    density,
    image_count: positions.length,
    positions,
  };

  await mkdir(outputDir, { recursive: true });
  await writeFile(path.join(outputDir, "outline.md"), formatOutlineMarkdown(outline, articlePath));

  return outline;
}

export async function generatePromptFiles(
  outline: OutlineData,
  articleContent: string,
  outputDir: string
): Promise<string[]> {
  const promptsDir = path.join(outputDir, "prompts");
  await mkdir(promptsDir, { recursive: true });

  const promptFiles: string[] = [];

  for (const position of outline.positions) {
    const promptContent = buildHandDrawnPrompt(articleContent, position.visualContent, position.section);
    const filePath = path.join(promptsDir, position.filename.replace(".png", ".md"));

    await writeFile(filePath, `---
illustration_id: ${position.index}
style: hand-drawn
---

${promptContent}`);
    promptFiles.push(filePath);
  }

  return promptFiles;
}

function buildHandDrawnPrompt(articleContent: string, illustrationDesc: string, sectionTitle: string): string {
  const { primaryColor, accentColor, elements } = extractKeyTerms(articleContent);

  return `请生成一张手绘风格插图，用于文章章节「${sectionTitle}」的配图：

## 主题描述
${illustrationDesc}

## 核心元素
${elements.map((e) => `- ${e}`).join("\n") || "- 抽象概念可视化"}

## 色彩要求
- 主色调：${primaryColor}
- 辅助色：${accentColor}
- 色调统一，风格一致

## 风格要求
- 手绘风格，有手工绘制的质感
- 简约，不复杂
- 整洁，画面干净
- 适当留白，不要填满
- 构图平衡，视觉焦点清晰
- 色调统一，不要过于跳跃
- 不要包含任何文字

## 技术规格
- 横版构图 (16:9)
- 适合文章配图使用
- 便于排版的简洁设计`;
}

function extractKeyTerms(content: string): {
  primaryColor: string;
  accentColor: string;
  elements: string[];
} {
  const elements: string[] = [];
  const lowerContent = content.toLowerCase();

  const quoteMatches = content.match(/[""](.*?)[""]/g) || [];
  for (const quote of quoteMatches.slice(0, 5)) {
    const text = quote.replace(/[""']/g, "").trim();
    if (text.length > 1 && text.length < 30) {
      elements.push(text);
    }
  }

  let primaryColor = "蓝色/青色系";
  let accentColor = "橙色/黄色系";

  if (lowerContent.includes("科技") || lowerContent.includes("tech") || lowerContent.includes("ai") || lowerContent.includes("代码")) {
    primaryColor = "蓝色/紫色系";
    accentColor = "青色/绿色系";
  } else if (lowerContent.includes("温暖") || lowerContent.includes("warm") || lowerContent.includes("story")) {
    primaryColor = "橙色/黄色系";
    accentColor = "红色/粉色调";
  } else if (lowerContent.includes("自然") || lowerContent.includes("nature") || lowerContent.includes("green")) {
    primaryColor = "绿色/青色系";
    accentColor = "黄色/橙色调";
  } else if (lowerContent.includes("商业") || lowerContent.includes("business") || lowerContent.includes("金融")) {
    primaryColor = "深蓝/灰色系";
    accentColor = "金色/橙色调";
  }

  return { primaryColor, accentColor, elements };
}

export { recommendDensity };
