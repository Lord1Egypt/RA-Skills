import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { exec } from "node:child_process";
import { promisify } from "node:util";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { homedir } from "node:os";

const execAsync = promisify(exec);
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const SCRIPTS = join(__dirname, "scripts");
const HOT_DIR = join(homedir(), ".openclaw", "memory_fs", "hot");
const HOT_AGE_MS = 3 * 60 * 60 * 1000; // 3 小时

// 缓存 OpenClaw dist 路径，避免每次 /refresh 都走 exec
let _sessionsRuntimePath = null;
async function getSessionsRuntimePath() {
    if (_sessionsRuntimePath) return _sessionsRuntimePath;
    try {
        const { stdout } = await execAsync("npm root -g");
        _sessionsRuntimePath = join(
            stdout.trim(),
            "openclaw/dist/sessions.runtime.js"
        );
    } catch {
        _sessionsRuntimePath = join(
            dirname(process.execPath), "..", "lib/node_modules",
            "openclaw/dist/sessions.runtime.js"
        );
    }
    return _sessionsRuntimePath;
}

export default definePluginEntry({
    id: "context-clear",
    name: "Context Clear with SRS",
    description: "记忆整理（SRS 衰减 + 晋升评分）、会话重置、启动时热记忆注入",
    register(api) {
        //
        // Hook: 每轮对话注入 < 3h 的热记忆作为背景上下文
        //
        api.on("before_prompt_build", async () => {
            if (!existsSync(HOT_DIR)) return;

            const now = Date.now();
            try {
                const hotContent = readdirSync(HOT_DIR)
                    .filter((f) => f.endsWith(".md"))
                    .map((name) => ({
                        name,
                        path: join(HOT_DIR, name),
                        mtime: statSync(join(HOT_DIR, name)).mtimeMs,
                    }))
                    .filter((f) => now - f.mtime < HOT_AGE_MS)
                    .sort((a, b) => b.mtime - a.mtime)
                    .map((f) => {
                        const c = readFileSync(f.path, "utf-8").trim();
                        if (!c) return null;
                        return `## 热记忆: ${f.name.replace(/\.md$/, "")}\n${c}`;
                    })
                    .filter(Boolean);

                if (hotContent.length > 0) {
                    return { prependContext: hotContent };
                }
            } catch {
                // 静默失败
            }
        });

        //
        // 命令: /refresh
        //
        api.registerCommand({
            name: "refresh",
            description: "执行记忆整理（SRS 衰减 + 晋升评分）并重置会话",
            handler: async (ctx) => {
                const sessionKey = ctx.sessionKey;
                if (!sessionKey) {
                    return { text: "❌ 无法获取 sessionKey，请在会话中重试。" };
                }

                try {
                    api.logger.info("context-clear: organize.py 开始");
                    await execAsync(`python3 ${join(SCRIPTS, "organize.py")}`);

                    api.logger.info("context-clear: promote.py 开始");
                    const { stdout } = await execAsync(
                        `python3 ${join(SCRIPTS, "promote.py")} --apply`
                    );

                    api.logger.info("context-clear: 重置会话");
                    const runtimePath = await getSessionsRuntimePath();
                    const sessions = await import(runtimePath);
                    await sessions.performGatewaySessionReset({
                        key: sessionKey,
                        reason: "new",
                        commandSource: "plugin:context-clear",
                    });

                    return {
                        text:
                            `✅ 记忆整理完成\n${stdout}\n\n` +
                            `会话已重置，上下文已清空。新会话将自动注入热记忆。`,
                    };
                } catch (e) {
                    api.logger.error(`context-clear 失败: ${e.message}`);
                    return { text: `❌ 整理失败: ${e.message}` };
                }
            },
        });
    },
});
