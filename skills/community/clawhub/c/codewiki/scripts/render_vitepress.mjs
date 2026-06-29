#!/usr/bin/env node
/**
 * render_vitepress.mjs
 * ===================
 *
 * Generic, parameterized renderer that converts any directory of Markdown
 * files into a static documentation website using **VitePress** with
 * first-class **Mermaid** diagram rendering support.
 *
 * Design goals (read carefully before modifying):
 *   * Sandbox isolation — all Node.js dependencies live inside a private
 *     `node_modules` under `<out>/.vitepress-work`. Nothing is installed
 *     globally, and the user's project-level `node_modules` is untouched.
 *   * Fully parameterized — no hardcoded source/output paths. Everything
 *     is supplied through CLI flags so that any agent or human can drive it.
 *   * Self-healing — the script writes a temporary `package.json`, runs
 *     `npm install` against the Aliyun (npmmirror.com) registry, generates
 *     `.vitepress/config.mjs`, copies the markdown tree, and runs
 *     `vitepress build`. Failures exit with a non-zero status code and a
 *     clear error message.
 *
 * ---------------------------------------------------------------------------
 * Usage
 * ---------------------------------------------------------------------------
 *
 *   node render_vitepress.mjs --src <markdown_dir> --out <output_dir>
 *   node render_vitepress.mjs -s ./wiki -o ./vitepress --force
 *
 * Required arguments:
 *   -s, --src   Source directory containing one or more `*.md` files.
 *               Sub-directories are walked recursively; the relative
 *               structure becomes the sidebar navigation.
 *   -o, --out   Output directory. The static site is written to
 *               `<out>/site`. A private working directory containing
 *               `package.json`, `node_modules`, and `.vitepress/config.mjs`
 *               is created under `<out>/.vitepress-work`.
 *
 * Optional flags:
 *   --force        Overwrite an existing `<out>` directory without prompting.
 *   --clean-node   Re-run `npm install` even if `node_modules` exists.
 *   -h, --help     Show this help message and exit.
 *
 * Exit codes:
 *   0 — build succeeded
 *   1 — invalid arguments / I/O error
 *   2 — npm install failed
 *   3 — VitePress build failed
 */

import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync, copyFileSync, constants } from "node:fs";
import { dirname, join, relative, resolve, sep } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

// ---------------------------------------------------------------------------
// Configuration constants
// ---------------------------------------------------------------------------

/**
 * Aliyun-hosted npm mirror (npmmirror.com). The user explicitly requested
 * Aliyun-style mirrors so that npm downloads are fast from within China.
 * `--registry=` is appended to every npm install invocation.
 */
const NPM_REGISTRY = "https://registry.npmmirror.com";

/**
 * Pinned, known-good dependency versions. Pinning keeps builds reproducible
 * across hosts and protects us from upstream API churn between releases of
 * VitePress or its Mermaid plugin.
 */
const DEPENDENCIES = {
  "vitepress": "^1.5.0",
  "vitepress-plugin-mermaid": "^2.0.17",
  "mermaid": "^11.4.1",
  "vue": "^3.5.13",
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Print a stderr message and exit with the given code. Centralizing failure
 * handling keeps the main flow readable while giving callers a deterministic
 * exit-code taxonomy (see module docstring).
 * @param {string} message
 * @param {number} code
 */
function fail(message, code = 1) {
  process.stderr.write(`[render_vitepress] ERROR: ${message}\n`);
  process.exit(code);
}

/**
 * Print a tagged info line so agent operators can trace script progress.
 * @param {string} message
 */
function info(message) {
  console.log(`[render_vitepress] ${message}`);
}

/**
 * Parse the CLI args. Hand-rolled (instead of `commander`/`yargs`) so the
 * script has zero production dependencies outside its own sandbox — the
 * sandbox is created by the script itself, so it can't depend on anything
 * that lives *inside* the sandbox.
 *
 * @returns {{src: string, out: string, force: boolean, cleanNode: boolean}}
 */
function parseArgs() {
  const argv = process.argv.slice(2);
  const opts = { src: null, out: null, force: false, cleanNode: false };

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    switch (arg) {
      case "-h":
      case "--help":
        printHelp();
        process.exit(0);
        break;
      case "-s":
      case "--src":
        opts.src = argv[++i];
        break;
      case "-o":
      case "--out":
        opts.out = argv[++i];
        break;
      case "--force":
        opts.force = true;
        break;
      case "--clean-node":
        opts.cleanNode = true;
        break;
      default:
        fail(`Unknown argument: ${arg}. Pass -h for usage.`);
    }
  }

  if (!opts.src) {
    printHelp();
    fail("Missing required argument: --src");
  }
  if (!opts.out) {
    printHelp();
    fail("Missing required argument: --out");
  }
  return opts;
}

/**
 * Emit the help block to stdout. Mirrors the docstring at the top of the
 * file so it stays authoritative for both humans and agents.
 */
function printHelp() {
  const help = `render_vitepress.mjs — Markdown → static VitePress site with Mermaid.

USAGE
  node render_vitepress.mjs --src <markdown_dir> --out <output_dir> [options]

REQUIRED
  -s, --src <path>   Source directory of Markdown (*.md) files. Walked
                     recursively; relative paths become the sidebar nav.
  -o, --out <path>   Output directory. Static site is written to
                     <out>/site. A private node_modules is created under
                     <out>/.vitepress-work.

OPTIONAL
  --force            Overwrite an existing <out> directory without prompting.
  --clean-node       Re-run 'npm install' even if node_modules already exists.
  -h, --help         Show this help message.

EXAMPLE
  node render_vitepress.mjs \\
      --src /path/to/wiki \\
      --out /path/to/vitepress_output

EXIT CODES
  0  success
  1  invalid arguments / I/O error
  2  npm install failed
  3  VitePress build failed
`;
  console.log(help);
}

/**
 * Recursively copy a directory tree, preserving relative sub-directory
 * structure. Used to mirror the markdown source into the VitePress working
 * directory so that image references and other assets remain intact.
 *
 * @param {string} srcDir  Absolute path to the source directory.
 * @param {string} dstDir  Absolute path to the destination directory.
 */
function copyTree(srcDir, dstDir) {
  if (!existsSync(dstDir)) mkdirSync(dstDir, { recursive: true });
  for (const entry of readdirSync(srcDir)) {
    const srcPath = join(srcDir, entry);
    const dstPath = join(dstDir, entry);
    const stat = statSync(srcPath);
    if (stat.isDirectory()) {
      copyTree(srcPath, dstPath);
    } else if (stat.isFile()) {
      copyFileSync(srcPath, dstPath);
    }
  }
}

/**
 * Recursively collect all `*.md` files under `srcDir`, returned as POSIX-
 * style relative paths so they can be sorted deterministically across
 * operating systems.
 *
 * @param {string} srcDir
 * @returns {string[]}
 */
function listMarkdown(srcDir) {
  /** @type {string[]} */
  const out = [];
  function walk(dir) {
    for (const entry of readdirSync(dir)) {
      const full = join(dir, entry);
      const stat = statSync(full);
      if (stat.isDirectory()) {
        walk(full);
      } else if (stat.isFile() && entry.toLowerCase().endsWith(".md")) {
        out.push(relative(srcDir, full).split(sep).join("/"));
      }
    }
  }
  walk(srcDir);
  out.sort();
  return out;
}

/**
 * Convert a relative markdown path like "foo/bar_baz.md" into a human-
 * readable sidebar label. Underscores and hyphens become spaces, and the
 * file extension is stripped.
 *
 * @param {string} relPath
 * @returns {string}
 */
function titleFromRel(relPath) {
  const base = relPath.split("/").pop().replace(/\.md$/i, "");
  return base
    .replace(/[_-]+/g, " ")
    .trim()
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

/**
 * Build a VitePress sidebar structure from a list of relative markdown
 * paths. Files at the root level appear directly; files inside sub-
 * directories are grouped under a collapsible section. The hierarchy
 * mirrors the source directory tree, which is the most predictable mapping
 * for an external agent.
 *
 * @param {string[]} relPaths
 * @returns {Array}
 */
function buildSidebar(relPaths) {
  /** @type {Array} */
  const sidebar = [];
  /** @type {Map<string, Array>} */
  const groups = new Map();

  for (const rel of relPaths) {
    const parts = rel.split("/");
    if (parts.length === 1) {
      sidebar.push({
        text: titleFromRel(rel),
        link: `/${rel}`,
      });
    } else {
      const section = parts[0];
      if (!groups.has(section)) groups.set(section, []);
      groups.get(section).push({
        text: titleFromRel(parts.slice(1).join("/")),
        link: `/${rel}`,
      });
    }
  }

  // Append grouped (sub-directory) items in stable, alphabetical order.
  for (const section of [...groups.keys()].sort()) {
    sidebar.push({
      text: section
        .replace(/[_-]+/g, " ")
        .replace(/\b\w/g, (c) => c.toUpperCase()),
      collapsed: false,
      items: groups.get(section),
    });
  }
  return sidebar;
}

/**
 * Write `package.json` into the working directory. The file declares only
 * the dependencies the script needs; `vitepress` is added as a dev
 * dependency (typical convention) but `npm install --omit=dev` is NOT
 * used so all four packages are always present.
 *
 * @param {string} workDir
 */
function writePackageJson(workDir) {
  const pkg = {
    name: "render-vitepress-sandbox",
    version: "1.0.0",
    private: true,
    type: "module",
    description: "Auto-generated sandbox for rendering markdown with VitePress + Mermaid.",
    scripts: {
      "docs:build": "vitepress build",
      "docs:dev": "vitepress dev",
    },
    dependencies: {
      "vitepress": DEPENDENCIES.vitepress,
      "vitepress-plugin-mermaid": DEPENDENCIES["vitepress-plugin-mermaid"],
      "mermaid": DEPENDENCIES.mermaid,
    },
    devDependencies: {
      "vue": DEPENDENCIES.vue,
    },
  };
  const path = join(workDir, "package.json");
  writeFileSync(path, JSON.stringify(pkg, null, 2), "utf8");
  info(`Wrote ${path}`);
}

/**
 * Generate `.vitepress/config.mjs`. The configuration enables:
 *   * The official `vitepress-plugin-mermaid` so that ```mermaid fenced
 *     blocks render as SVG via a headless mermaid instance.
 *   * Site title, clean URLs, and an auto-generated sidebar derived from
 *     the discovered markdown paths.
 *
 * The sidebar is serialized as JSON so the resulting config file is valid
 * JavaScript regardless of path quoting nuances.
 *
 * @param {string} workDir
 * @param {Array} sidebar
 */
function writeVitePressConfig(workDir, sidebar) {
  const cfg = `// AUTO-GENERATED by render_vitepress.mjs — do not edit by hand.
import { defineConfig } from "vitepress";
import { withMermaid } from "vitepress-plugin-mermaid";

export default withMermaid(
  defineConfig({
    title: "Documentation",
    description: "Auto-rendered Markdown documentation",
    lang: "zh-CN",
    // IMPORTANT: do NOT set base:"./". VitePress is a Vue SPA whose
    // client-side router uses pushState and cannot reliably resolve routes
    // when the base is relative — the page briefly renders then redirects
    // to 404 because the router can't compute the next URL. Keep the
    // default base "/" and serve the built site via an HTTP server (the
    // wrapper's --serve flag handles this automatically). Opening the
    // built .html directly via file:// is unsupported for VitePress.
    // The wiki source contains cross-references to source files (config.md,
    // services.md, etc.) that are NOT part of the documentation set. Treat
    // them as ordinary un-linked text instead of build-breaking dead links.
    ignoreDeadLinks: true,
    // Restrict VitePress's source-discovery to the content/ subdirectory so
    // that the bundled node_modules (which contains hundreds of unrelated
    // README.md / CHANGELOG.md files) is never scanned.
    srcDir: "content",
    // KEEP .html suffixes on links. cleanUrls:true strips them, which only
    // works on HTTP servers with URL rewriting; the bundled python http.server
    // doesn't do rewriting, so links would 404 on refresh.
    cleanUrls: false,
    lastUpdated: true,
    markdown: {
      lineNumbers: true,
      theme: { light: "github-light", dark: "github-dark" },
    },
    mermaid: {
      // Mermaid is initialised client-side; theme follows VitePress dark mode.
      theme: "default",
    },
    themeConfig: {
      sidebar: ${JSON.stringify(sidebar, null, 2)},
      outline: { level: 2, label: "本页目录" },
      docFooter: { prev: "上一页", next: "下一页" },
      search: { provider: "local" },
      socialLinks: [],
    },
  })
);
`;
  const dir = join(workDir, ".vitepress");
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  const path = join(dir, "config.mjs");
  writeFileSync(path, cfg, "utf8");
  info(`Wrote ${path}`);
}

/**
 * Generate a top-level `index.md` landing page if (and only if) the source
 * tree does not already provide one. The page lists every discovered
 * markdown file so a human reader can navigate from a single entry point.
 *
 * @param {string} workDir
 * @param {string[]} relPaths
 */
function writeIndexIfNeeded(workDir, relPaths) {
  const indexPath = join(workDir, "index.md");
  if (existsSync(indexPath)) return;

  const lines = [
    "---",
    "title: 首页",
    "outline: [2, 3]",
    "---",
    "",
    "# 文档索引",
    "",
  ];
  for (const rel of relPaths) {
    // Always reference the markdown file by name; VitePress rewrites
    // .md links to .html at build time so they resolve cleanly under
    // both file:// and static HTTP hosts.
    lines.push(`- [${titleFromRel(rel)}](${rel})`);
  }
  writeFileSync(indexPath, lines.join("\n") + "\n", "utf8");
  info(`Wrote ${indexPath}`);
}

// ---------------------------------------------------------------------------
// npm install & build
// ---------------------------------------------------------------------------

/**
 * Run `npm install` inside the working directory. The Aliyun mirror is
 * pinned via `--registry=` so package downloads are fast from within China.
 * `--no-audit --no-fund` keep the install quiet and dependency-free of
 * telemetry.
 *
 * @param {string} workDir
 * @param {boolean} cleanNode  If true, remove node_modules before install.
 */
function npmInstall(workDir, cleanNode) {
  const nodeModules = join(workDir, "node_modules");
  if (existsSync(nodeModules)) {
    if (cleanNode) {
      info(`Removing existing node_modules at ${nodeModules}`);
      rmSync(nodeModules, { recursive: true, force: true });
    } else {
      info(`Reusing existing node_modules at ${nodeModules}`);
      return;
    }
  }
  const args = [
    "install",
    "--registry", NPM_REGISTRY,
    "--no-audit",
    "--no-fund",
    "--loglevel", "error",
  ];
  info(`Running: npm ${args.join(" ")} (cwd=${workDir})`);
  try {
    execFileSync("npm", args, { cwd: workDir, stdio: "inherit" });
  } catch (err) {
    fail(`npm install failed: ${err.message}`, 2);
  }
}

/**
 * Invoke `npx vitepress build` from inside the working directory, writing
 * the static site into `siteDir`. `execFileSync` ensures any non-zero exit
 * code propagates to the parent process.
 *
 * @param {string} workDir
 * @param {string} siteDir
 */
function vitepressBuild(workDir, siteDir) {
  if (existsSync(siteDir)) {
    info(`Removing previous build output: ${siteDir}`);
    rmSync(siteDir, { recursive: true, force: true });
  }
  const args = [
    "vitepress", "build",
    "--outDir", siteDir,
    "--clean",
  ];
  info(`Running: npx ${args.join(" ")} (cwd=${workDir})`);
  try {
    execFileSync("npx", args, { cwd: workDir, stdio: "inherit" });
  } catch (err) {
    fail(`VitePress build failed: ${err.message}`, 3);
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
  const opts = parseArgs();
  const src = resolve(opts.src);
  const out = resolve(opts.out);

  // ----- Step 1: validate inputs -----------------------------------------
  if (!existsSync(src)) fail(`Source directory does not exist: ${src}`);
  if (!statSync(src).isDirectory()) fail(`Source path is not a directory: ${src}`);

  // ----- Step 2: prepare output dirs ------------------------------------
  if (existsSync(out) && readdirSync(out).length > 0) {
    if (!opts.force) {
      fail(
        `Output directory is not empty: ${out}. Re-run with --force to overwrite.`,
      );
    }
    info(`Removing existing output directory: ${out}`);
    rmSync(out, { recursive: true, force: true });
  }
  mkdirSync(out, { recursive: true });

  const work = join(out, ".vitepress-work");
  const siteDir = join(out, "site");
  mkdirSync(work, { recursive: true });

  // ----- Step 3: write package.json & install --------------------------
  writePackageJson(work);
  npmInstall(work, opts.cleanNode);

  // ----- Step 4: copy source tree & generate config --------------------
  // The markdown source lives under <work>/content/ so that VitePress
  // (configured with srcDir:"content") never scans the bundled node_modules
  // in <work>/node_modules/. Without this separation, every README.md /
  // CHANGELOG.md shipped by a dependency would be parsed as a wiki page
  // and the build would drown in dead-link warnings.
  const contentDir = join(work, "content");
  if (existsSync(contentDir)) {
    info(`Removing existing content directory: ${contentDir}`);
    rmSync(contentDir, { recursive: true, force: true });
  }
  mkdirSync(contentDir, { recursive: true });
  info(`Copying source tree ${src} → ${contentDir}`);
  copyTree(src, contentDir);

  const relPaths = listMarkdown(contentDir);
  if (relPaths.length === 0) {
    fail(`No Markdown (*.md) files found under ${src}. Nothing to render.`);
  }
  const sidebar = buildSidebar(relPaths);
  writeVitePressConfig(work, sidebar);
  writeIndexIfNeeded(contentDir, relPaths);

  // ----- Step 5: build the static site ----------------------------------
  vitepressBuild(work, siteDir);

  // ----- Step 6: summarize ---------------------------------------------
  const indexHtml = join(siteDir, "index.html");
  if (!existsSync(indexHtml)) {
    fail(`Build reported success but ${indexHtml} was not produced.`, 3);
  }
  console.log("");
  info("Build succeeded.");
  console.log(`  Static site : ${siteDir}`);
  console.log(`  Entry point : ${indexHtml}`);
  console.log(`  Open with   : open ${indexHtml}`);
  console.log(`  Serve with  : npx vitepress dev ${work}`);
}

main();
