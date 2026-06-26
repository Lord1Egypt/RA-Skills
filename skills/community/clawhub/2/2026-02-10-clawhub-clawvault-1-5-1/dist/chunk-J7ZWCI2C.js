// src/lib/entity-index.ts
import * as fs from "fs";
import * as path from "path";
import matter from "gray-matter";
function buildEntityIndex(vaultPath) {
  const entries = /* @__PURE__ */ new Map();
  const byPath = /* @__PURE__ */ new Map();
  const entityFolders = ["people", "projects", "agents", "lessons", "decisions", "commitments"];
  for (const folder of entityFolders) {
    const folderPath = path.join(vaultPath, folder);
    if (!fs.existsSync(folderPath)) continue;
    const files = fs.readdirSync(folderPath).filter((f) => f.endsWith(".md"));
    for (const file of files) {
      const filePath = path.join(folderPath, file);
      const content = fs.readFileSync(filePath, "utf-8");
      const { data: frontmatter } = matter(content);
      const relativePath = `${folder}/${file.replace(".md", "")}`;
      const baseName = file.replace(".md", "");
      const aliases = [baseName];
      if (frontmatter.title && frontmatter.title.toLowerCase() !== baseName.toLowerCase()) {
        aliases.push(frontmatter.title);
      }
      if (Array.isArray(frontmatter.aliases)) {
        aliases.push(...frontmatter.aliases);
      }
      for (const alias of aliases) {
        const key = alias.toLowerCase();
        if (!entries.has(key)) {
          entries.set(key, relativePath);
        }
      }
      byPath.set(relativePath, { path: relativePath, aliases });
    }
  }
  return { entries, byPath };
}
function getSortedAliases(index) {
  const result = [];
  for (const [alias, path2] of index.entries) {
    result.push({ alias, path: path2 });
  }
  result.sort((a, b) => b.alias.length - a.alias.length);
  return result;
}

export {
  buildEntityIndex,
  getSortedAliases
};
