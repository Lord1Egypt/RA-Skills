#!/usr/bin/env node
/**
 * Example: Full-featured CLI with Commander.js
 * Demonstrates: commands, options, validation, output formatting
 */

import { Command } from "commander";
// import chalk from "chalk";
// import ora from "ora";

const program = new Command();

program
  .name("devtool")
  .description("Developer productivity CLI")
  .version("1.0.0");

// ─── Init command ─────────────────────────────────────────────────────────────

program
  .command("init")
  .description("Initialize a new project")
  .argument("<name>", "Project name (lowercase, no spaces)")
  .option("-t, --template <template>", "Project template", "default")
  .option("--no-git", "Skip git initialization")
  .option("-d, --dir <directory>", "Output directory", ".")
  .action(async (name: string, options) => {
    // Validate name
    if (!/^[a-z0-9-]+$/.test(name)) {
      console.error(`Error: Project name must be lowercase alphanumeric with hyphens.`);
      console.error(`  Got: "${name}"`);
      console.error(`  Try: "${name.toLowerCase().replace(/[^a-z0-9]+/g, "-")}"`);
      process.exit(2);
    }

    console.log(`Creating project: ${name}`);
    console.log(`  Template: ${options.template}`);
    console.log(`  Directory: ${options.dir}`);
    console.log(`  Git: ${options.git ? "yes" : "no"}`);

    // const spinner = ora("Scaffolding project...").start();
    // await scaffold(name, options);
    // spinner.succeed("Project created!");

    console.log("");
    console.log("Next steps:");
    console.log(`  cd ${name}`);
    console.log(`  npm install`);
    console.log(`  npm run dev`);
  });

// ─── Build command ────────────────────────────────────────────────────────────

program
  .command("build")
  .description("Build the project")
  .option("-w, --watch", "Watch for changes")
  .option("-o, --outdir <dir>", "Output directory", "dist")
  .option("--minify", "Minify output", false)
  .option("--sourcemap", "Generate source maps", true)
  .action(async (options) => {
    console.log("Building project...");
    console.log(`  Output: ${options.outdir}`);
    console.log(`  Watch: ${options.watch ? "yes" : "no"}`);
    console.log(`  Minify: ${options.minify ? "yes" : "no"}`);
    console.log(`  Sourcemaps: ${options.sourcemap ? "yes" : "no"}`);
    // ... build implementation
    console.log("Build complete!");
  });

// ─── List command with formatted output ───────────────────────────────────────

interface ProjectInfo {
  name: string;
  version: string;
  status: string;
}

program
  .command("list")
  .description("List projects")
  .option("--json", "Output as JSON")
  .option("-q, --quiet", "Only output names")
  .action(async (options) => {
    const projects: ProjectInfo[] = [
      { name: "web-app", version: "2.1.0", status: "active" },
      { name: "api-server", version: "1.5.3", status: "active" },
      { name: "legacy-tool", version: "0.9.0", status: "archived" },
    ];

    if (options.json) {
      console.log(JSON.stringify(projects, null, 2));
      return;
    }

    if (options.quiet) {
      projects.forEach((p) => console.log(p.name));
      return;
    }

    // Table output
    console.log("NAME          VERSION  STATUS");
    console.log("────          ───────  ──────");
    for (const p of projects) {
      console.log(
        `${p.name.padEnd(14)}${p.version.padEnd(9)}${p.status}`
      );
    }
    console.log(`\n${projects.length} projects total`);
  });

// ─── Config command (get/set) ─────────────────────────────────────────────────

const configCmd = program.command("config").description("Manage configuration");

configCmd
  .command("get")
  .description("Get a config value")
  .argument("<key>", "Config key")
  .action((key: string) => {
    const config: Record<string, string> = {
      "editor": "code",
      "theme": "dark",
      "lang": "en",
    };
    const value = config[key];
    if (value === undefined) {
      console.error(`Unknown config key: ${key}`);
      console.error(`Available keys: ${Object.keys(config).join(", ")}`);
      process.exit(1);
    }
    console.log(value);
  });

configCmd
  .command("set")
  .description("Set a config value")
  .argument("<key>", "Config key")
  .argument("<value>", "Config value")
  .action((key: string, value: string) => {
    console.log(`Set ${key} = ${value}`);
  });

// ─── Parse ────────────────────────────────────────────────────────────────────

program.parse();
