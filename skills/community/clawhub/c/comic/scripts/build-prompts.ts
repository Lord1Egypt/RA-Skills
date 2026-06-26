#!/usr/bin/env bun
import path from "node:path";
import process from "node:process";
import { mkdir, readFile, writeFile } from "node:fs/promises";

type CliArgs = {
  storyboardPath: string | null;
  outputDir: string | null;
  ref: string | null;
  charactersPath: string | null;
  help: boolean;
};

type StoryboardMeta = {
  title: string;
  topic: string;
  art: string;
  tone: string;
  layout: string;
  aspect: string;
  contentScope: string;
  language: string;
  panelsPerPage: number;
  pageCount: number;
  characterReference: string;
};

type CoverEntry = {
  filename: string;
  coreMessage: string;
  visualFocus: string;
  promptNotes: string[];
};

type PageEntry = {
  page: number;
  filename: string;
  coreMessage: string;
  scene: string;
  characters: string[];
  continuityAnchors: string[];
  panelCount: number | null;
  panelPlan: string[];
  pageHook: string;
};

type CharacterProfile = {
  name: string;
  body: string;
};

function printUsage(): void {
  console.log(`Usage:
  npx -y bun scripts/build-prompts.ts --storyboard storyboard.md --output-dir prompts [options]

Options:
  --storyboard <path>   Path to storyboard.md
  --output-dir <path>   Directory for generated prompt files
  --ref <path>          Override character reference image path
  --characters <path>   Override characters/characters.md path
  -h, --help            Show help`);
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    storyboardPath: null,
    outputDir: null,
    ref: null,
    charactersPath: null,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i]!;
    if (current === "--storyboard") args.storyboardPath = argv[++i] ?? null;
    else if (current === "--output-dir") args.outputDir = argv[++i] ?? null;
    else if (current === "--ref") args.ref = argv[++i] ?? null;
    else if (current === "--characters") args.charactersPath = argv[++i] ?? null;
    else if (current === "--help" || current === "-h") args.help = true;
  }

  return args;
}

function extractFrontmatter(content: string): StoryboardMeta {
  const normalized = content.replace(/\r\n/g, "\n");
  const match = normalized.match(/^---\n([\s\S]*?)\n---/);
  const raw = match?.[1] ?? "";
  const map = new Map<string, string>();
  for (const line of raw.split("\n")) {
    const idx = line.indexOf(":");
    if (idx === -1) continue;
    const key = line.slice(0, idx).trim();
    const value = line.slice(idx + 1).trim().replace(/^"(.*)"$/, "$1");
    map.set(key, value);
  }

  const characterReference = normalized.match(/\*\*Character Reference\*\*:\s*(.+)/)?.[1]?.trim() ?? "characters/characters.png";

  return {
    title: map.get("title") ?? "Comic Title",
    topic: map.get("topic") ?? (map.get("title") ?? "Comic topic"),
    art: map.get("art") ?? "ligne-claire",
    tone: map.get("tone") ?? "neutral",
    layout: map.get("layout") ?? "standard",
    aspect: map.get("aspect") ?? "3:4",
    contentScope: map.get("content_scope") ?? "standard",
    language: map.get("language") ?? "en",
    panelsPerPage: Number.parseInt(map.get("panels_per_page") ?? "3", 10) || 3,
    pageCount: Number.parseInt(map.get("page_count") ?? "0", 10) || 0,
    characterReference,
  };
}

function extractField(block: string, label: string): string {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return block.match(new RegExp(`\\*\\*${escaped}\\*\\*:\\s*(.+)`))?.[1]?.trim() ?? "";
}

function extractBullets(block: string, label: string): string[] {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = block.match(new RegExp(`\\*\\*${escaped}\\*\\*:\\s*\\n((?:- .+\\n?)*)`, "m"));
  if (!match?.[1]) return [];
  return match[1]
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.startsWith("- "))
    .map((line) => line.slice(2).trim())
    .filter(Boolean);
}

function parseStoryboard(content: string): { meta: StoryboardMeta; cover: CoverEntry | null; pages: PageEntry[] } {
  const normalized = content.replace(/\r\n/g, "\n");
  const meta = extractFrontmatter(normalized);

  const lines = normalized.split("\n");
  let cover: CoverEntry | null = null;
  const pages: PageEntry[] = [];

  for (let i = 0; i < lines.length; i++) {
    if (lines[i] === "## Cover") {
      const body: string[] = [];
      for (let j = i + 1; j < lines.length; j++) {
        if (lines[j]!.startsWith("## Page ")) break;
        body.push(lines[j]!);
        i = j;
      }
      const text = body.join("\n");
      cover = {
        filename: extractField(text, "Filename"),
        coreMessage: extractField(text, "Core Message"),
        visualFocus: extractField(text, "Visual Focus"),
        promptNotes: extractBullets(text, "Prompt Notes"),
      };
      continue;
    }

    const pageHeader = lines[i]!.match(/^## Page (\d+)$/);
    if (!pageHeader) continue;

    const body: string[] = [];
    for (let j = i + 1; j < lines.length; j++) {
      if (lines[j] === "## Cover" || lines[j]!.startsWith("## Page ")) break;
      body.push(lines[j]!);
      i = j;
    }
    const text = body.join("\n");
    pages.push({
      page: Number.parseInt(pageHeader[1] ?? "0", 10),
      filename: extractField(text, "Filename"),
      coreMessage: extractField(text, "Core Message"),
      scene: extractField(text, "Scene"),
      characters: extractBullets(text, "Characters"),
      continuityAnchors: extractBullets(text, "Continuity Anchors"),
      panelCount: Number.parseInt(extractField(text, "Panel Count") || "", 10) || null,
      panelPlan: extractBullets(text, "Panel Plan"),
      pageHook: extractField(text, "Page Hook"),
    });
  }

  return { meta, cover, pages };
}

function promptFileNameFromImage(filename: string): string {
  return filename.replace(/\.(png|jpg|jpeg|webp)$/i, ".md");
}

function inferCharactersPath(storyboardPath: string, overridePath: string | null): string {
  if (overridePath) return path.resolve(overridePath);
  return path.resolve(path.dirname(storyboardPath), "characters", "characters.md");
}

function parseCharacterProfiles(content: string): CharacterProfile[] {
  const normalized = content.replace(/\r\n/g, "\n");
  const pattern = /^## Character \d+:\s*(.+)$/gm;
  const matches = [...normalized.matchAll(pattern)];
  const profiles: CharacterProfile[] = [];

  for (let i = 0; i < matches.length; i++) {
    const match = matches[i]!;
    const name = match[1]?.trim();
    const start = match.index ?? 0;
    const end = i + 1 < matches.length ? (matches[i + 1]!.index ?? normalized.length) : normalized.length;
    const body = normalized.slice(start, end).trim();
    if (!name || !body) continue;
    profiles.push({ name, body });
  }

  return profiles;
}

function normalizeName(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9\u4e00-\u9fff]+/g, " ").trim();
}

function selectCharacterProfiles(pageCharacters: string[], profiles: CharacterProfile[]): CharacterProfile[] {
  if (!profiles.length) return [];
  if (!pageCharacters.length) return profiles.slice(0, 3);

  const selected = profiles.filter((profile) => {
    const profileName = normalizeName(profile.name);
    return pageCharacters.some((character) => {
      const pageName = normalizeName(character);
      return pageName.includes(profileName) || profileName.includes(pageName);
    });
  });

  return selected.length ? selected : profiles.slice(0, 3);
}

function buildCharacterBible(pageCharacters: string[], charactersMarkdown: string): string {
  const profiles = parseCharacterProfiles(charactersMarkdown);
  const selected = selectCharacterProfiles(pageCharacters, profiles);
  if (!selected.length) {
    return charactersMarkdown.trim() || "<character bible missing>";
  }
  return selected.map((profile) => profile.body).join("\n\n---\n\n");
}

function buildCoverPrompt(meta: StoryboardMeta, cover: CoverEntry, ref: string): string {
  const promptNotes = cover.promptNotes.length
    ? cover.promptNotes.map((note) => `- ${note}`).join("\n")
    : "- <note 1>\n- <note 2>";

  return `Create a comic cover about: ${meta.topic}.

Comic role: cover.
Art style: ${meta.art}.
Tone: ${meta.tone}.
Layout: ${meta.layout}.
Aspect ratio: ${meta.aspect}.
Content scope: ${meta.contentScope}.
Total comic length: ${meta.pageCount || "<page count>"} content pages plus one cover.
Language: ${meta.language}.

Character reference:
- reference image: ${ref}
- consistency rule: keep faces, costume colors, accessories, and silhouette stable across pages
- priority rule: treat the reference sheet as the canonical source of truth for character design; do not redesign the cast from scratch

Core message: ${cover.coreMessage || "<one-line hook>"}.
Visual focus: ${cover.visualFocus || "<main cover concept>"}.
Prompt notes:
${promptNotes}

Avoid: inconsistent character appearance, unreadable text, cluttered composition, watermark.
`;
}

function buildPagePrompt(
  meta: StoryboardMeta,
  page: PageEntry,
  ref: string,
  charactersMarkdown: string,
  previousPage: PageEntry | null,
  nextPage: PageEntry | null,
): string {
  const characters = page.characters.length
    ? page.characters.map((character) => `- ${character}`).join("\n")
    : "- <character 1>\n- <character 2>";
  const continuityAnchors = page.continuityAnchors.length
    ? page.continuityAnchors.map((anchor) => `- ${anchor}`).join("\n")
    : [
        "- Keep the same character faces, outfits, color palette, and signature props as previous pages.",
        "- Preserve the same scene progression unless this page explicitly changes location or time.",
      ].join("\n");
  const panels = page.panelPlan.length
    ? page.panelPlan.map((panel) => `- ${panel}`).join("\n")
    : "- Panel 1: Title + one-sentence setup\n- Panel 2: Main explanation with one example\n- Panel 3: Mini summary + next-step hint";
  const characterBible = buildCharacterBible(page.characters, charactersMarkdown);
  const previousRecap = previousPage
    ? `Page ${previousPage.page}: ${previousPage.coreMessage || "<previous page core message>"} | Scene: ${previousPage.scene || "<previous scene>"} | Hook: ${previousPage.pageHook || "<no hook>"}`
    : "Cover or opening setup immediately before this page.";
  const nextHook = nextPage
    ? `Page ${nextPage.page}: ${nextPage.coreMessage || "<next page core message>"} | Scene: ${nextPage.scene || "<next scene>"}`
    : page.pageHook || "<story resolution or ending beat>";

  return `Create a comic page about: ${meta.topic}.

Comic role: page.
Art style: ${meta.art}.
Tone: ${meta.tone}.
Layout: ${meta.layout}.
Aspect ratio: ${meta.aspect}.
Content scope: ${meta.contentScope}.
Language: ${meta.language}.

Character reference:
- reference image: ${ref}
- consistency rule: keep faces, costume colors, accessories, and silhouette stable across pages
- priority rule: treat the reference sheet as the canonical source of truth for faces, outfits, props, and palette; do not redesign characters on later pages

Character bible (reuse these visual facts exactly):
${characterBible}

Core message: ${page.coreMessage || "<what this page must convey>"}.

Characters:
${characters}

Continuity anchors:
${continuityAnchors}

Scene:
- location: ${page.scene || "<location and situation>"}
- key action: ${page.coreMessage || "<action or event>"}
- emotional beat: ${page.pageHook || "<emotional beat>"}

Story continuity:
- previous page recap: ${previousRecap}
- current page transition: continue the same cast, visual identity, and scene logic unless this page explicitly changes them
- next page hook: ${nextHook}

Panel structure:
Panel count target: ${page.panelCount ?? meta.panelsPerPage}.
${panels}

Page hook: ${page.pageHook || "<transition to next page>"}.
Text treatment: narration-only.
If text is used, keep it sparse, readable, and native to the target language.

Avoid: inconsistent character appearance, overcrowded tiny panels, unreadable text, broken anatomy, random extra limbs, watermark.
`;
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printUsage();
    return;
  }
  if (!args.storyboardPath) {
    console.error("Error: --storyboard is required");
    process.exit(1);
  }
  if (!args.outputDir) {
    console.error("Error: --output-dir is required");
    process.exit(1);
  }

  const content = await readFile(path.resolve(args.storyboardPath), "utf8");
  const { meta, cover, pages } = parseStoryboard(content);
  const outputDir = path.resolve(args.outputDir);
  const ref = args.ref ?? meta.characterReference ?? "characters/characters.png";
  const charactersPath = inferCharactersPath(args.storyboardPath, args.charactersPath);
  let charactersMarkdown = "";
  try {
    charactersMarkdown = await readFile(charactersPath, "utf8");
  } catch {
    charactersMarkdown = "";
  }
  await mkdir(outputDir, { recursive: true });

  let count = 0;
  if (cover?.filename) {
    await writeFile(path.join(outputDir, promptFileNameFromImage(cover.filename)), buildCoverPrompt(meta, cover, ref), "utf8");
    count++;
  }
  for (const page of pages) {
    if (!page.filename) continue;
    const previousPage = pages.find((candidate) => candidate.page === page.page - 1) ?? null;
    const nextPage = pages.find((candidate) => candidate.page === page.page + 1) ?? null;
    await writeFile(
      path.join(outputDir, promptFileNameFromImage(page.filename)),
      buildPagePrompt(meta, page, ref, charactersMarkdown, previousPage, nextPage),
      "utf8",
    );
    count++;
  }

  console.log(`Prompts written: ${outputDir} (${count} files)`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
