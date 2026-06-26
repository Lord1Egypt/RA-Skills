"use strict";

const fs = require("fs");
const path = require("path");
const {
  appRoot,
  assertRegisteredOwnership,
  assertSafeUserName,
  assertSafeToken,
  parseArgs,
  readJsonIfExists,
} = require("./common");

function writeText(filePath, content) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, content, "utf8");
}

function writeJson(filePath, data) {
  writeText(filePath, `${JSON.stringify(data, null, 2)}\n`);
}

function rootPackageJson() {
  return {
    name: "web-app-workspace",
    private: true,
    workspaces: ["client", "server"],
    scripts: {
      dev: 'npm run dev -w server',
      build: "npm run build -w client && npm run build -w server",
      start: "npm run start -w server",
    },
  };
}

function clientPackageJson() {
  return {
    name: "client",
    private: true,
    version: "0.1.0",
    type: "module",
    scripts: {
      dev: "vite",
      build: "node ../node_modules/typescript/bin/tsc -b && node ../node_modules/vite/bin/vite.js build",
      preview: "vite preview",
    },
    dependencies: {
      react: "^19.1.0",
      "react-dom": "^19.1.0",
    },
    devDependencies: {
      "@types/react": "^19.1.2",
      "@types/react-dom": "^19.1.2",
      "@vitejs/plugin-react": "^4.4.1",
      typescript: "^5.8.3",
      vite: "^6.3.5",
    },
  };
}

function serverPackageJson() {
  return {
    name: "server",
    private: true,
    version: "0.1.0",
    type: "commonjs",
    scripts: {
      dev: "tsx watch src/index.ts",
      build: "node ../node_modules/typescript/bin/tsc -p tsconfig.json",
      start: "node dist/index.js",
    },
    dependencies: {
      "better-sqlite3": "^11.10.0",
      express: "^4.21.2",
    },
    devDependencies: {
      "@types/better-sqlite3": "^7.6.13",
      "@types/express": "^5.0.1",
      "@types/node": "^22.15.17",
      tsx: "^4.19.4",
      typescript: "^5.8.3",
    },
  };
}

function rootTsConfig() {
  return {
    files: [],
    references: [{ path: "./client" }, { path: "./server" }],
  };
}

function clientTsConfig() {
  return {
    compilerOptions: {
      target: "ES2020",
      useDefineForClassFields: true,
      lib: ["ES2020", "DOM", "DOM.Iterable"],
      module: "ESNext",
      skipLibCheck: true,
      moduleResolution: "Bundler",
      allowImportingTsExtensions: false,
      resolveJsonModule: true,
      isolatedModules: true,
      noEmit: true,
      jsx: "react-jsx",
      strict: true,
    },
    include: ["src"],
  };
}

function serverTsConfig() {
  return {
    compilerOptions: {
      target: "ES2020",
      module: "CommonJS",
      moduleResolution: "Node",
      outDir: "dist",
      rootDir: "src",
      esModuleInterop: true,
      strict: true,
      skipLibCheck: true,
      types: ["node"],
    },
    include: ["src"],
  };
}

function viteConfig(basePath) {
  return `import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "${basePath}/",
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "${basePath}/api": {
        target: "http://127.0.0.1:3001",
        changeOrigin: true,
      },
    },
  },
});
`;
}

function indexHtml(title) {
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>${title}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="./src/main.tsx"></script>
  </body>
</html>
`;
}

function clientMain() {
  return `import React from "react";
import ReactDOM from "react-dom/client";
import { App } from "./App";
import "./styles.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
`;
}

function clientApp(basePath) {
  return `import { FormEvent, useEffect, useState } from "react";

type Todo = {
  id: number;
  title: string;
  done: number;
  createdAt: string;
};

const apiBase = "${basePath}/api";

export function App() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [draft, setDraft] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadTodos() {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(\`\${apiBase}/todos\`);
      if (!response.ok) throw new Error("Failed to load todos");
      const data = await response.json();
      setTodos(data.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadTodos();
  }, []);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    if (!draft.trim()) return;
    const response = await fetch(\`\${apiBase}/todos\`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: draft.trim() }),
    });
    if (!response.ok) {
      setError("Could not create item");
      return;
    }
    setDraft("");
    await loadTodos();
  }

  async function toggle(todo: Todo) {
    await fetch(\`\${apiBase}/todos/\${todo.id}\`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ done: todo.done ? 0 : 1 }),
    });
    await loadTodos();
  }

  async function remove(todo: Todo) {
    await fetch(\`\${apiBase}/todos/\${todo.id}\`, { method: "DELETE" });
    await loadTodos();
  }

  const remaining = todos.filter((todo) => !todo.done).length;

  return (
    <div className="page-shell">
      <main className="layout">
        <section className="hero">
          <p className="eyebrow">LITEAPP WORKSPACE</p>
          <h1>Focused planning with a crafted editorial interface.</h1>
          <p className="lede">
            A compact React, Express, and SQLite workspace with deliberate typography,
            structured composition, and a live persistence layer.
          </p>
          <div className="hero-stats">
            <div>
              <span>Open items</span>
              <strong>{remaining}</strong>
            </div>
            <div>
              <span>Total records</span>
              <strong>{todos.length}</strong>
            </div>
          </div>
        </section>

        <section className="composer">
          <div className="panel-heading">
            <p>New entry</p>
            <h2>Add a task worth tracking</h2>
          </div>
          <form onSubmit={onSubmit} className="compose-form">
            <input
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              placeholder="Define the next concrete task"
            />
            <button type="submit">Create</button>
          </form>
          {error ? <p className="message error">{error}</p> : null}
        </section>

        <section className="board">
          <div className="panel-heading">
            <p>Current board</p>
            <h2>Tracked work</h2>
          </div>
          {loading ? <p className="message">Loading data…</p> : null}
          {!loading && todos.length === 0 ? (
            <p className="message">No items yet. Start with one clear objective.</p>
          ) : null}
          <div className="todo-list">
            {todos.map((todo) => (
              <article className={todo.done ? "todo done" : "todo"} key={todo.id}>
                <div>
                  <p className="todo-title">{todo.title}</p>
                  <p className="todo-meta">{new Date(todo.createdAt).toLocaleString()}</p>
                </div>
                <div className="todo-actions">
                  <button type="button" onClick={() => toggle(todo)}>
                    {todo.done ? "Reopen" : "Complete"}
                  </button>
                  <button type="button" className="ghost" onClick={() => remove(todo)}>
                    Remove
                  </button>
                </div>
              </article>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
`;
}

function clientStyles() {
  return `:root {
  --bg: #f4efe6;
  --paper: rgba(255, 251, 245, 0.82);
  --ink: #1d1a17;
  --muted: #6f675f;
  --line: rgba(29, 26, 23, 0.12);
  --accent: #ba4a2f;
  --accent-dark: #923621;
  --shadow: 0 18px 50px rgba(45, 31, 22, 0.08);
  --radius: 28px;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  color: var(--ink);
  background:
    radial-gradient(circle at top left, rgba(186, 74, 47, 0.12), transparent 30%),
    linear-gradient(180deg, #f7f1e8, #efe4d5 55%, #eadcca);
  min-height: 100vh;
}

button,
input {
  font: inherit;
}

.page-shell {
  min-height: 100vh;
  padding: 32px;
}

.layout {
  display: grid;
  grid-template-columns: 1.2fr 0.9fr;
  gap: 24px;
  max-width: 1240px;
  margin: 0 auto;
}

.hero,
.composer,
.board {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  backdrop-filter: blur(14px);
}

.hero {
  padding: 40px;
  min-height: 320px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background:
    linear-gradient(135deg, rgba(255,255,255,0.6), rgba(255,255,255,0.18)),
    linear-gradient(160deg, rgba(186,74,47,0.15), transparent 45%);
}

.hero h1,
.panel-heading h2 {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  font-weight: 600;
  line-height: 0.95;
  text-wrap: pretty;
}

.hero h1 {
  max-width: 10ch;
  font-size: clamp(3.2rem, 7vw, 6.2rem);
}

.eyebrow,
.panel-heading p,
.todo-meta,
.hero-stats span {
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--muted);
  font-size: 0.78rem;
}

.lede {
  max-width: 42rem;
  font-size: 1.03rem;
  line-height: 1.75;
  color: #453f39;
}

.hero-stats {
  display: flex;
  gap: 16px;
}

.hero-stats div {
  min-width: 160px;
  padding-top: 16px;
  border-top: 1px solid var(--line);
}

.hero-stats strong {
  display: block;
  margin-top: 8px;
  font-size: 2rem;
  font-weight: 700;
}

.composer,
.board {
  padding: 28px;
}

.composer {
  align-self: start;
}

.board {
  grid-column: 1 / -1;
}

.compose-form {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  margin-top: 24px;
}

.compose-form input {
  min-height: 54px;
  border: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.78);
  border-radius: 18px;
  padding: 0 18px;
}

button {
  border: none;
  background: var(--accent);
  color: white;
  padding: 0 18px;
  min-height: 54px;
  border-radius: 18px;
  cursor: pointer;
  transition: background-color 160ms ease, transform 160ms ease;
}

button:hover {
  background: var(--accent-dark);
  transform: translateY(-1px);
}

button.ghost {
  background: transparent;
  color: var(--ink);
  border: 1px solid var(--line);
}

.message {
  color: var(--muted);
  margin: 18px 0 0;
}

.message.error {
  color: #9b2d21;
}

.todo-list {
  display: grid;
  gap: 14px;
  margin-top: 24px;
}

.todo {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 16px;
  padding: 18px 20px;
  border-radius: 22px;
  border: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.7);
}

.todo.done .todo-title {
  text-decoration: line-through;
  color: var(--muted);
}

.todo-title {
  margin: 0;
  font-size: 1.08rem;
  font-weight: 600;
}

.todo-meta {
  margin: 10px 0 0;
}

.todo-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

@media (max-width: 900px) {
  .page-shell {
    padding: 18px;
  }

  .layout {
    grid-template-columns: 1fr;
  }

  .board {
    grid-column: auto;
  }

  .compose-form,
  .todo {
    grid-template-columns: 1fr;
  }

  .todo-actions {
    justify-content: stretch;
    flex-direction: column;
  }
}
`;
}

function serverDbSource() {
  return `import Database from "better-sqlite3";
import fs from "fs";
import path from "path";

const dataDir = path.resolve(__dirname, "../data");
fs.mkdirSync(dataDir, { recursive: true });

const db = new Database(path.join(dataDir, "app.db"));

db.exec(\`
  CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
  )
\`);

export { db };
`;
}

function serverIndexSource() {
  return `import express from "express";
import path from "path";
import { db } from "./db";

const app = express();
const port = Number(process.env.PORT || "3000");
const token = process.env.APP_TOKEN || "APP00000";
const basePath = process.env.BASE_PATH || \`/\${token}\`;
const apiBase = \`\${basePath}/api\`;
const clientDist = path.resolve(__dirname, "../../client/dist");

app.use(express.json());

app.get(\`\${apiBase}/health\`, (_req, res) => {
  res.json({ ok: true, token, basePath });
});

app.get(\`\${apiBase}/todos\`, (_req, res) => {
  const items = db.prepare("SELECT id, title, done, created_at as createdAt FROM todos ORDER BY id DESC").all();
  res.json({ items });
});

app.post(\`\${apiBase}/todos\`, (req, res) => {
  const title = String(req.body?.title || "").trim();
  if (!title) {
    res.status(400).json({ error: "title is required" });
    return;
  }
  const result = db.prepare("INSERT INTO todos (title) VALUES (?)").run(title);
  res.status(201).json({ id: result.lastInsertRowid });
});

app.patch(\`\${apiBase}/todos/:id\`, (req, res) => {
  const id = Number(req.params.id);
  const done = req.body?.done ? 1 : 0;
  db.prepare("UPDATE todos SET done = ? WHERE id = ?").run(done, id);
  res.json({ ok: true });
});

app.delete(\`\${apiBase}/todos/:id\`, (req, res) => {
  const id = Number(req.params.id);
  db.prepare("DELETE FROM todos WHERE id = ?").run(id);
  res.status(204).end();
});

app.use(basePath, express.static(clientDist));

app.get(\`\${basePath}/*\`, (_req, res) => {
  res.sendFile(path.join(clientDist, "index.html"));
});

app.listen(port, "0.0.0.0", () => {
  // eslint-disable-next-line no-console
  console.log(\`App listening on port \${port} at \${basePath}/\`);
});
`;
}

function readmeText(meta) {
  return `# ${meta.title}

Generated by the develop-and-deploy-web-app skill scaffold script.

Type: ${meta.appKind} (${meta.appLabel})

## Stack

- React + TypeScript + Vite
- Express + TypeScript
- SQLite via better-sqlite3

## Expected environment variables

- \`PORT\`
- \`APP_TOKEN\`
- \`BASE_PATH\`
`;
}

function scaffoldProject(meta) {
  const appDir = appRoot(meta.userName, meta.token);
  const basePath = `/${meta.token}`;

  writeJson(path.join(appDir, "package.json"), rootPackageJson());
  writeJson(path.join(appDir, "tsconfig.json"), rootTsConfig());
  writeText(path.join(appDir, "README.md"), readmeText(meta));

  writeJson(path.join(appDir, "client", "package.json"), clientPackageJson());
  writeJson(path.join(appDir, "client", "tsconfig.json"), clientTsConfig());
  writeText(path.join(appDir, "client", "vite.config.ts"), viteConfig(basePath));
  writeText(path.join(appDir, "client", "index.html"), indexHtml(meta.title));
  writeText(path.join(appDir, "client", "src", "main.tsx"), clientMain());
  writeText(path.join(appDir, "client", "src", "App.tsx"), clientApp(basePath));
  writeText(path.join(appDir, "client", "src", "styles.css"), clientStyles());

  writeJson(path.join(appDir, "server", "package.json"), serverPackageJson());
  writeJson(path.join(appDir, "server", "tsconfig.json"), serverTsConfig());
  writeText(path.join(appDir, "server", "src", "db.ts"), serverDbSource());
  writeText(path.join(appDir, "server", "src", "index.ts"), serverIndexSource());
}

function main() {
  const args = parseArgs(process.argv);
  const userName = args.userName;
  const token = args.token;

  assertSafeUserName(userName);
  assertSafeToken(token);
  assertRegisteredOwnership(userName, token);

  const meta = readJsonIfExists(path.join(appRoot(userName, token), "APP-META.json"), null);
  if (!meta) {
    throw new Error("Run init-app.js before scaffold-app.js");
  }

  scaffoldProject(meta);
  process.stdout.write(
    `${JSON.stringify(
      {
        userName,
        token,
        path: meta.path,
        scaffolded: true,
      },
      null,
      2
    )}\n`
  );
}

main();
