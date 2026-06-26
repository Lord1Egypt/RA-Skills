import {
  DEFAULT_CATEGORIES,
  QmdUnavailableError,
  SearchEngine,
  TYPE_TO_CATEGORY,
  extractTags,
  extractWikiLinks,
  hasQmd,
  qmdEmbed,
  qmdUpdate
} from "./chunk-VJIFT5T5.js";

// src/lib/vault.ts
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";
import matter from "gray-matter";
import { glob } from "glob";
var CONFIG_FILE = ".clawvault.json";
var INDEX_FILE = ".clawvault-index.json";
var ClawVault = class {
  config;
  search;
  initialized = false;
  constructor(vaultPath) {
    if (!hasQmd()) {
      throw new QmdUnavailableError();
    }
    this.config = {
      path: path.resolve(vaultPath),
      name: path.basename(vaultPath),
      categories: DEFAULT_CATEGORIES,
      qmdCollection: void 0,
      qmdRoot: void 0
    };
    this.search = new SearchEngine();
    this.applyQmdConfig();
  }
  /**
   * Initialize a new vault
   */
  async init(options = {}) {
    if (!hasQmd()) {
      throw new QmdUnavailableError();
    }
    const vaultPath = this.config.path;
    this.config = { ...this.config, ...options };
    this.applyQmdConfig();
    if (!fs.existsSync(vaultPath)) {
      fs.mkdirSync(vaultPath, { recursive: true });
    }
    for (const category of this.config.categories) {
      const catPath = path.join(vaultPath, category);
      if (!fs.existsSync(catPath)) {
        fs.mkdirSync(catPath, { recursive: true });
      }
    }
    await this.createTemplates();
    const readmePath = path.join(vaultPath, "README.md");
    if (!fs.existsSync(readmePath)) {
      fs.writeFileSync(readmePath, this.generateReadme());
    }
    const configPath = path.join(vaultPath, CONFIG_FILE);
    const meta = {
      name: this.config.name,
      version: "1.0.0",
      created: (/* @__PURE__ */ new Date()).toISOString(),
      lastUpdated: (/* @__PURE__ */ new Date()).toISOString(),
      categories: this.config.categories,
      documentCount: 0,
      qmdCollection: this.getQmdCollection(),
      qmdRoot: this.getQmdRoot()
    };
    fs.writeFileSync(configPath, JSON.stringify(meta, null, 2));
    this.initialized = true;
  }
  /**
   * Load an existing vault
   */
  async load() {
    if (!hasQmd()) {
      throw new QmdUnavailableError();
    }
    const vaultPath = this.config.path;
    const configPath = path.join(vaultPath, CONFIG_FILE);
    if (!fs.existsSync(configPath)) {
      throw new Error(`Not a ClawVault: ${vaultPath} (missing ${CONFIG_FILE})`);
    }
    const meta = JSON.parse(fs.readFileSync(configPath, "utf-8"));
    this.config.name = meta.name;
    this.config.categories = meta.categories;
    this.config.qmdCollection = meta.qmdCollection;
    this.config.qmdRoot = meta.qmdRoot;
    if (!meta.qmdCollection || !meta.qmdRoot) {
      meta.qmdCollection = meta.qmdCollection || meta.name;
      meta.qmdRoot = meta.qmdRoot || this.config.path;
      fs.writeFileSync(configPath, JSON.stringify(meta, null, 2));
    }
    this.applyQmdConfig(meta);
    await this.reindex();
    this.initialized = true;
  }
  /**
   * Reindex all documents
   */
  async reindex() {
    this.search.clear();
    const files = await glob("**/*.md", {
      cwd: this.config.path,
      ignore: ["**/node_modules/**", "**/.*"]
    });
    for (const file of files) {
      const doc = await this.loadDocument(file);
      if (doc) {
        this.search.addDocument(doc);
      }
    }
    await this.saveIndex();
    return this.search.size;
  }
  /**
   * Load a document from disk
   */
  async loadDocument(relativePath) {
    try {
      const fullPath = path.join(this.config.path, relativePath);
      const content = fs.readFileSync(fullPath, "utf-8");
      const { data: frontmatter, content: body } = matter(content);
      const stats = fs.statSync(fullPath);
      const parts = relativePath.split(path.sep);
      const category = parts.length > 1 ? parts[0] : "root";
      const filename = path.basename(relativePath, ".md");
      return {
        id: relativePath.replace(/\.md$/, ""),
        path: fullPath,
        category,
        title: frontmatter.title || filename,
        content: body,
        frontmatter,
        links: extractWikiLinks(body),
        tags: extractTags(body),
        modified: stats.mtime
      };
    } catch (err) {
      console.error(`Error loading ${relativePath}:`, err);
      return null;
    }
  }
  /**
   * Store a new document
   */
  async store(options) {
    const {
      category,
      title,
      content,
      frontmatter = {},
      overwrite = false,
      qmdUpdate: triggerUpdate = false,
      qmdEmbed: triggerEmbed = false
    } = options;
    const filename = this.slugify(title) + ".md";
    const relativePath = path.join(category, filename);
    const fullPath = path.join(this.config.path, relativePath);
    if (fs.existsSync(fullPath) && !overwrite) {
      throw new Error(`Document already exists: ${relativePath}. Use overwrite: true to replace.`);
    }
    const categoryPath = path.join(this.config.path, category);
    if (!fs.existsSync(categoryPath)) {
      fs.mkdirSync(categoryPath, { recursive: true });
    }
    const fm = {
      title,
      date: (/* @__PURE__ */ new Date()).toISOString().split("T")[0],
      ...frontmatter
    };
    const fileContent = matter.stringify(content, fm);
    fs.writeFileSync(fullPath, fileContent);
    const doc = await this.loadDocument(relativePath);
    if (doc) {
      this.search.addDocument(doc);
      await this.saveIndex();
    }
    if (triggerUpdate || triggerEmbed) {
      qmdUpdate(this.getQmdCollection());
      if (triggerEmbed) {
        qmdEmbed(this.getQmdCollection());
      }
    }
    return doc;
  }
  /**
   * Quick store to inbox
   */
  async capture(note, title) {
    const autoTitle = title || `note-${Date.now()}`;
    return this.store({
      category: "inbox",
      title: autoTitle,
      content: note
    });
  }
  /**
   * Search the vault (BM25 via qmd)
   */
  async find(query, options = {}) {
    return this.search.search(query, options);
  }
  /**
   * Semantic/vector search (via qmd vsearch)
   */
  async vsearch(query, options = {}) {
    return this.search.vsearch(query, options);
  }
  /**
   * Combined search with query expansion (via qmd query)
   */
  async query(query, options = {}) {
    return this.search.query(query, options);
  }
  /**
   * Get a document by ID or path
   */
  async get(idOrPath) {
    const normalized = idOrPath.replace(/\.md$/, "");
    const docs = this.search.getAllDocuments();
    return docs.find((d) => d.id === normalized) || null;
  }
  /**
   * List documents in a category
   */
  async list(category) {
    const docs = this.search.getAllDocuments();
    if (category) {
      return docs.filter((d) => d.category === category);
    }
    return docs;
  }
  /**
   * Sync vault to another location (for Obsidian on Windows, etc.)
   */
  async sync(options) {
    const { target, deleteOrphans = false, dryRun = false } = options;
    const result = {
      copied: [],
      deleted: [],
      unchanged: [],
      errors: []
    };
    const sourceFiles = await glob("**/*.md", {
      cwd: this.config.path,
      ignore: ["**/node_modules/**"]
    });
    if (!dryRun && !fs.existsSync(target)) {
      fs.mkdirSync(target, { recursive: true });
    }
    for (const file of sourceFiles) {
      const sourcePath = path.join(this.config.path, file);
      const targetPath = path.join(target, file);
      try {
        const sourceStats = fs.statSync(sourcePath);
        let shouldCopy = true;
        if (fs.existsSync(targetPath)) {
          const targetStats = fs.statSync(targetPath);
          if (sourceStats.mtime <= targetStats.mtime) {
            result.unchanged.push(file);
            shouldCopy = false;
          }
        }
        if (shouldCopy) {
          if (!dryRun) {
            const targetDir = path.dirname(targetPath);
            if (!fs.existsSync(targetDir)) {
              fs.mkdirSync(targetDir, { recursive: true });
            }
            fs.copyFileSync(sourcePath, targetPath);
          }
          result.copied.push(file);
        }
      } catch (err) {
        result.errors.push(`${file}: ${err}`);
      }
    }
    if (deleteOrphans) {
      const targetFiles = await glob("**/*.md", { cwd: target });
      const sourceSet = new Set(sourceFiles);
      for (const file of targetFiles) {
        if (!sourceSet.has(file)) {
          if (!dryRun) {
            fs.unlinkSync(path.join(target, file));
          }
          result.deleted.push(file);
        }
      }
    }
    return result;
  }
  /**
   * Get vault statistics
   */
  async stats() {
    const docs = this.search.getAllDocuments();
    const categories = {};
    const allTags = /* @__PURE__ */ new Set();
    let totalLinks = 0;
    for (const doc of docs) {
      categories[doc.category] = (categories[doc.category] || 0) + 1;
      totalLinks += doc.links.length;
      doc.tags.forEach((t) => allTags.add(t));
    }
    return {
      documents: docs.length,
      categories,
      links: totalLinks,
      tags: [...allTags].sort()
    };
  }
  /**
   * Get all categories
   */
  getCategories() {
    return this.config.categories;
  }
  /**
   * Check if vault is initialized
   */
  isInitialized() {
    return this.initialized;
  }
  /**
   * Get vault path
   */
  getPath() {
    return this.config.path;
  }
  /**
   * Get vault name
   */
  getName() {
    return this.config.name;
  }
  /**
   * Get qmd collection name
   */
  getQmdCollection() {
    return this.config.qmdCollection || this.config.name;
  }
  /**
   * Get qmd collection root
   */
  getQmdRoot() {
    return this.config.qmdRoot || this.config.path;
  }
  // === Memory Type System ===
  /**
   * Store a memory with type classification
   * Automatically routes to correct category based on type
   */
  async remember(type, title, content, frontmatter = {}) {
    const category = TYPE_TO_CATEGORY[type];
    return this.store({
      category,
      title,
      content,
      frontmatter: { ...frontmatter, memoryType: type }
    });
  }
  // === Handoff System ===
  /**
   * Create a session handoff document
   * Call this before context death or long pauses
   */
  async createHandoff(handoff) {
    const now = /* @__PURE__ */ new Date();
    const dateStr = now.toISOString().split("T")[0];
    const timeStr = now.toISOString().split("T")[1].slice(0, 5).replace(":", "");
    const fullHandoff = {
      ...handoff,
      created: now.toISOString()
    };
    const content = this.formatHandoff(fullHandoff);
    const frontmatter = {
      type: "handoff",
      workingOn: handoff.workingOn,
      blocked: handoff.blocked,
      nextSteps: handoff.nextSteps
    };
    if (handoff.sessionKey) frontmatter.sessionKey = handoff.sessionKey;
    if (handoff.feeling) frontmatter.feeling = handoff.feeling;
    if (handoff.decisions) frontmatter.decisions = handoff.decisions;
    if (handoff.openQuestions) frontmatter.openQuestions = handoff.openQuestions;
    return this.store({
      category: "handoffs",
      title: `handoff-${dateStr}-${timeStr}`,
      content,
      frontmatter
    });
  }
  /**
   * Format handoff as readable markdown
   */
  formatHandoff(h) {
    let md = `# Session Handoff

`;
    md += `**Created:** ${h.created}
`;
    if (h.sessionKey) md += `**Session:** ${h.sessionKey}
`;
    if (h.feeling) md += `**Feeling:** ${h.feeling}
`;
    md += `
`;
    md += `## Working On
`;
    h.workingOn.forEach((w) => md += `- ${w}
`);
    md += `
`;
    md += `## Blocked
`;
    if (h.blocked.length === 0) md += `- Nothing currently blocked
`;
    else h.blocked.forEach((b) => md += `- ${b}
`);
    md += `
`;
    md += `## Next Steps
`;
    h.nextSteps.forEach((n) => md += `- ${n}
`);
    if (h.decisions && h.decisions.length > 0) {
      md += `
## Decisions Made
`;
      h.decisions.forEach((d) => md += `- ${d}
`);
    }
    if (h.openQuestions && h.openQuestions.length > 0) {
      md += `
## Open Questions
`;
      h.openQuestions.forEach((q) => md += `- ${q}
`);
    }
    return md;
  }
  // === Session Recap (Bootstrap Hook) ===
  /**
   * Generate a session recap - who I was
   * Call this on bootstrap to restore context
   */
  async generateRecap(options = {}) {
    const { handoffLimit = 3, brief = false } = options;
    const handoffDocs = await this.list("handoffs");
    const recentHandoffs = handoffDocs.sort((a, b) => b.modified.getTime() - a.modified.getTime()).slice(0, handoffLimit).map((doc) => this.parseHandoff(doc));
    const projectDocs = await this.list("projects");
    const activeProjects = projectDocs.filter((d) => d.frontmatter.status !== "completed" && d.frontmatter.status !== "archived").map((d) => d.title);
    const commitmentDocs = await this.list("commitments");
    const pendingCommitments = commitmentDocs.filter((d) => d.frontmatter.status !== "done").map((d) => d.title);
    const decisionDocs = await this.list("decisions");
    const recentDecisions = decisionDocs.sort((a, b) => b.modified.getTime() - a.modified.getTime()).slice(0, brief ? 3 : 5).map((d) => d.title);
    const lessonDocs = await this.list("lessons");
    const recentLessons = lessonDocs.sort((a, b) => b.modified.getTime() - a.modified.getTime()).slice(0, brief ? 3 : 5).map((d) => d.title);
    let keyRelationships = [];
    if (!brief) {
      const peopleDocs = await this.list("people");
      keyRelationships = peopleDocs.filter((d) => d.frontmatter.importance === "high" || d.frontmatter.role).map((d) => `${d.title}${d.frontmatter.role ? ` (${d.frontmatter.role})` : ""}`);
    }
    const feelings = recentHandoffs.map((h) => h.feeling).filter(Boolean);
    const emotionalArc = feelings.length > 0 ? feelings.join(" \u2192 ") : void 0;
    return {
      generated: (/* @__PURE__ */ new Date()).toISOString(),
      recentHandoffs,
      activeProjects,
      pendingCommitments,
      recentDecisions,
      recentLessons,
      keyRelationships,
      emotionalArc
    };
  }
  /**
   * Format recap as readable markdown for injection
   */
  formatRecap(recap, options = {}) {
    const { brief = false } = options;
    let md = `# Who I Was

`;
    md += `*Generated: ${recap.generated}*

`;
    if (recap.emotionalArc) {
      md += `**Emotional arc:** ${recap.emotionalArc}

`;
    }
    if (recap.recentHandoffs.length > 0) {
      md += `## Recent Sessions
`;
      for (const h of recap.recentHandoffs) {
        if (brief) {
          md += `- **${h.created.split("T")[0]}:** ${h.workingOn.slice(0, 2).join(", ")}`;
          if (h.nextSteps.length > 0) md += ` \u2192 ${h.nextSteps[0]}`;
          md += `
`;
        } else {
          md += `
### ${h.created.split("T")[0]}
`;
          md += `**Working on:** ${h.workingOn.join(", ")}
`;
          if (h.blocked.length > 0) md += `**Blocked:** ${h.blocked.join(", ")}
`;
          md += `**Next:** ${h.nextSteps.join(", ")}
`;
        }
      }
      md += `
`;
    }
    if (recap.activeProjects.length > 0) {
      md += `## Active Projects
`;
      recap.activeProjects.forEach((p) => md += `- ${p}
`);
      md += `
`;
    }
    if (recap.pendingCommitments.length > 0) {
      md += `## Pending Commitments
`;
      recap.pendingCommitments.forEach((c) => md += `- ${c}
`);
      md += `
`;
    }
    if (recap.recentDecisions && recap.recentDecisions.length > 0) {
      md += `## Recent Decisions
`;
      recap.recentDecisions.forEach((d) => md += `- ${d}
`);
      md += `
`;
    }
    if (recap.recentLessons.length > 0) {
      md += `## Recent Lessons
`;
      recap.recentLessons.forEach((l) => md += `- ${l}
`);
      md += `
`;
    }
    if (!brief && recap.keyRelationships.length > 0) {
      md += `## Key People
`;
      recap.keyRelationships.forEach((r) => md += `- ${r}
`);
    }
    return md;
  }
  /**
   * Parse a handoff document back into structured form
   */
  parseHandoff(doc) {
    return {
      created: doc.frontmatter.date || doc.modified.toISOString(),
      sessionKey: doc.frontmatter.sessionKey,
      workingOn: doc.frontmatter.workingOn || [],
      blocked: doc.frontmatter.blocked || [],
      nextSteps: doc.frontmatter.nextSteps || [],
      decisions: doc.frontmatter.decisions,
      openQuestions: doc.frontmatter.openQuestions,
      feeling: doc.frontmatter.feeling
    };
  }
  // === Private helpers ===
  applyQmdConfig(meta) {
    const collection = meta?.qmdCollection || this.config.qmdCollection || this.config.name;
    const root = meta?.qmdRoot || this.config.qmdRoot || this.config.path;
    this.config.qmdCollection = collection;
    this.config.qmdRoot = root;
    this.search.setVaultPath(this.config.path);
    this.search.setCollection(collection);
    this.search.setCollectionRoot(root);
  }
  slugify(text) {
    return text.toLowerCase().replace(/[^\w\s-]/g, "").replace(/\s+/g, "-").replace(/-+/g, "-").trim();
  }
  async saveIndex() {
    const indexPath = path.join(this.config.path, INDEX_FILE);
    const data = this.search.export();
    fs.writeFileSync(indexPath, JSON.stringify(data, null, 2));
    const configPath = path.join(this.config.path, CONFIG_FILE);
    if (fs.existsSync(configPath)) {
      const meta = JSON.parse(fs.readFileSync(configPath, "utf-8"));
      meta.lastUpdated = (/* @__PURE__ */ new Date()).toISOString();
      meta.documentCount = this.search.size;
      fs.writeFileSync(configPath, JSON.stringify(meta, null, 2));
    }
  }
  async createTemplates() {
    const templatesPath = path.join(this.config.path, "templates");
    if (!fs.existsSync(templatesPath)) {
      fs.mkdirSync(templatesPath, { recursive: true });
    }
    const moduleDir = path.dirname(fileURLToPath(import.meta.url));
    const candidates = [
      path.resolve(moduleDir, "../templates"),
      path.resolve(moduleDir, "../../templates")
    ];
    const builtinDir = candidates.find((dir) => fs.existsSync(dir) && fs.statSync(dir).isDirectory());
    if (!builtinDir) return;
    for (const entry of fs.readdirSync(builtinDir, { withFileTypes: true })) {
      if (!entry.isFile() || !entry.name.endsWith(".md")) continue;
      if (entry.name === "daily.md") continue;
      const sourcePath = path.join(builtinDir, entry.name);
      const targetPath = path.join(templatesPath, entry.name);
      if (!fs.existsSync(targetPath)) {
        fs.copyFileSync(sourcePath, targetPath);
      }
    }
  }
  generateReadme() {
    return `# ${this.config.name} \u{1F418}

An elephant never forgets.

## Structure

${this.config.categories.map((c) => `- \`/${c}/\` \u2014 ${this.getCategoryDescription(c)}`).join("\n")}

## Quick Search

\`\`\`bash
clawvault search "query"
\`\`\`

## Quick Capture

\`\`\`bash
clawvault store --category inbox --title "note" --content "..."
\`\`\`

---

*Managed by [ClawVault](https://github.com/Versatly/clawvault)*
`;
  }
  getCategoryDescription(category) {
    const descriptions = {
      // Memory type categories (Benthic's taxonomy)
      facts: "Raw information, data points, things that are true",
      feelings: "Emotional states, reactions, energy levels",
      decisions: "Choices made with context and reasoning",
      lessons: "What I learned, insights, patterns observed",
      commitments: "Promises, goals, obligations to fulfill",
      preferences: "Likes, dislikes, how I want things",
      people: "Relationships, one file per person",
      projects: "Active work, ventures, ongoing efforts",
      // System categories
      handoffs: "Session bridges \u2014 what I was doing, what comes next",
      transcripts: "Session summaries and logs",
      goals: "Long-term and short-term objectives",
      patterns: "Recurring behaviors (\u2192 lessons)",
      inbox: "Quick capture \u2192 process later",
      templates: "Templates for each document type"
    };
    return descriptions[category] || category;
  }
};
async function findVault(startPath = process.cwd()) {
  let current = path.resolve(startPath);
  while (current !== path.dirname(current)) {
    const configPath = path.join(current, CONFIG_FILE);
    if (fs.existsSync(configPath)) {
      const vault = new ClawVault(current);
      await vault.load();
      return vault;
    }
    current = path.dirname(current);
  }
  return null;
}
async function createVault(vaultPath, options = {}) {
  const vault = new ClawVault(vaultPath);
  await vault.init(options);
  return vault;
}

export {
  ClawVault,
  findVault,
  createVault
};
