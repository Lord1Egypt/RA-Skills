// src/skill-loader.ts
// Reads SKILL.md files from the skills/ directory.
// Parses frontmatter to extract summary (description field).
// Caches content in memory to avoid repeated disk reads.

import fs from "node:fs";
import path from "node:path";

interface SkillContent {
  summary: string;   // from frontmatter description field
  body: string;      // full markdown body (after frontmatter)
  raw: string;       // full file content
}

export class SkillLoader {
  private skillsDir: string;
  private cache: Map<string, SkillContent> = new Map();

  constructor(pluginRootDir: string) {
    this.skillsDir = path.join(pluginRootDir, "skills");
  }

  load(skillFile: string): SkillContent {
    if (this.cache.has(skillFile)) {
      return this.cache.get(skillFile)!;
    }

    const fullPath = path.join(this.skillsDir, skillFile);
    if (!fs.existsSync(fullPath)) {
      throw new Error(`Skill file not found: ${fullPath}`);
    }

    const raw = fs.readFileSync(fullPath, "utf-8");
    const parsed = this.parse(raw);
    this.cache.set(skillFile, parsed);
    return parsed;
  }

  getSummary(skillFile: string): string {
    return this.load(skillFile).summary;
  }

  getBody(skillFile: string): string {
    return this.load(skillFile).body;
  }

  private parse(raw: string): SkillContent {
    // Extract YAML frontmatter between --- delimiters
    const frontmatterMatch = raw.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
    if (!frontmatterMatch) {
      return { summary: "", body: raw, raw };
    }

    const frontmatterText = frontmatterMatch[1];
    const body = frontmatterMatch[2].trim();

    // Extract description field (handles quoted and unquoted values)
    const descMatch = frontmatterText.match(
      /^description:\s*["']?([\s\S]*?)["']?\s*$/m
    );
    let summary = "";
    if (descMatch) {
      // Clean up multi-line quoted descriptions
      summary = descMatch[1]
        .replace(/^["']|["']$/g, "")
        .replace(/\n\s*/g, " ")
        .trim();
      // Truncate to first sentence for the summary
      const firstSentence = summary.match(/^[^.!?]+[.!?]/);
      if (firstSentence) {
        summary = firstSentence[0].trim();
      }
    }

    return { summary, body, raw };
  }
}
