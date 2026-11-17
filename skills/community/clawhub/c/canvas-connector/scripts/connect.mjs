#!/usr/bin/env node
/**
 * 画布连接器 · 连接信息脚本（无任何危险调用：只做下载/校验/检测/读取/输出）
 * 用法：node connect.mjs [--canvas https://你的画布域名] [--port 17371] [--source <连接器下载地址或本地文件>] [--sha256 <期望校验值>]
 * 输出（JSON 单行）：
 *   { ok:true, url, tokenMasked, pageUrl, alreadyRunning, needStart:false }     连接器已在运行
 *   { ok:false, needStart:true, startCommand:"nohup node … &" }                 需要先启动连接器
 *
 * 安全设计：
 *   - 远程下载必须先通过 SHA-256 校验（官方分发源内置校验值；自定义源必须显式提供 --sha256），校验不符一律拒绝安装；
 *   - 「打开即连」链接仅对官方画布域名携带连接令牌（防止把本机令牌泄露给不信任来源）；
 *   - 本脚本不执行任何下载内容；启动命令由调用方（Agent）在用户确认后执行。
 */
import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { homedir } from "node:os";
import { join, resolve } from "node:path";

// 官方分发源与内置校验值：三渠道发布时与连接器文件同批更新（见 CHANGELOG）
const OFFICIAL_CANVAS = "https://aicanvas.miaotuntu.com";
const OFFICIAL_SOURCE = "https://aicanvas.miaotuntu.com/downloads/lobster-canvas-agent.mjs";
const OFFICIAL_SOURCE_SHA256 = "f4261772d0039f7949b22ec965b97dbe6395e8314b67d02c4cae84a4314b24d7";

const args = process.argv.slice(2);
const arg = (name, fallback = "") => {
    const index = args.indexOf(name);
    return index !== -1 && args[index + 1] ? args[index + 1] : fallback;
};

const port = Number(arg("--port", "17371"));
const canvas = arg("--canvas", "").replace(/\/+$/, "");
const source = arg("--source", OFFICIAL_SOURCE);
const expectedSha = String(arg("--sha256", "") || "").toLowerCase();
const configDir = join(homedir(), ".infinite-canvas");
const configFile = join(configDir, "canvas-agent.json");
const target = join(configDir, "canvas-agent.mjs");
const url = `http://127.0.0.1:${port}`;

const sha256 = (buf) => createHash("sha256").update(buf).digest("hex");
const mask = (value) => (value ? `${String(value).slice(0, 4)}****${String(value).slice(-4)}` : "");

const health = async () => {
    try {
        const res = await fetch(`${url}/health`, { signal: AbortSignal.timeout(1500) });
        return res.ok;
    } catch {
        return false;
    }
};

const readToken = () => {
    try {
        return String(JSON.parse(readFileSync(configFile, "utf8")).token || "");
    } catch {
        return "";
    }
};

/**
 * 自动连接链接：仅对官方画布域名携带连接令牌（防令牌泄露给不信任来源）。
 * 自定义域名只生成不含令牌的基础链接，连接令牌需用户在本机手动读取后粘贴。
 */
const isOfficialCanvas = (value) => !value || value === OFFICIAL_CANVAS;
const pageUrl = (token) => {
    const base = canvas || OFFICIAL_CANVAS;
    if (!isOfficialCanvas(canvas)) return `${base}/app/#agentUrl=${encodeURIComponent(url)}`;
    return `${base}/app/#agentUrl=${encodeURIComponent(url)}&agentToken=${encodeURIComponent(token)}`;
};

if (await health()) {
    const token = readToken();
    console.log(
        JSON.stringify({
            ok: true,
            url,
            tokenMasked: mask(token),
            pageUrl: pageUrl(token),
            alreadyRunning: true,
            needStart: false,
            ...(isOfficialCanvas(canvas)
                ? {}
                : { hint: "当前画布地址非官方域名：自动连接链接未携带连接令牌（安全原因）。如需连接，请在本机 ~/.infinite-canvas/canvas-agent.json 中读取令牌并手动填入画布连接框" }),
        }),
    );
    process.exit(0);
}

// 未在运行：确保连接器文件就位 —— 本地文件直接拷贝；远程下载必须先通过 SHA-256 校验
try {
    mkdirSync(configDir, { recursive: true });
    if (source.startsWith("/") || source.startsWith(".")) {
        copyFileSync(resolve(source), target);
    } else {
        // 远程下载：官方源用内置校验值；自定义源必须显式提供 --sha256，否则拒绝下载
        const expected = expectedSha || (source === OFFICIAL_SOURCE ? OFFICIAL_SOURCE_SHA256 : "");
        if (!expected) throw new Error("自定义下载地址必须提供 --sha256 校验值（防篡改）；使用官方分发源则无需手动指定");
        const res = await fetch(source, { signal: AbortSignal.timeout(60000) });
        if (!res.ok) throw new Error(`下载失败 HTTP ${res.status}`);
        const buf = Buffer.from(await res.arrayBuffer());
        const actual = sha256(buf);
        if (actual !== expected) {
            throw new Error(`连接器文件校验失败：sha256 期望 ${expected.slice(0, 12)}…，实际 ${actual.slice(0, 12)}…。已拒绝安装——可能分发文件被篡改或与当前技能版本不匹配，请更新技能后重试`);
        }
        writeFileSync(target, buf);
    }
} catch (error) {
    console.log(JSON.stringify({ ok: false, needStart: false, error: `连接器文件准备失败：${error instanceof Error ? error.message : error}` }));
    process.exit(1);
}

console.log(
    JSON.stringify({
        ok: false,
        needStart: true,
        url,
        connectorFile: target,
        startCommand: `nohup node ${target} >> ${join(configDir, "connector.log")} 2>&1 &`,
        hint: "启动后等待约 2 秒，再次运行本脚本即可获得 pageUrl（自动连接链接）",
    }),
);
