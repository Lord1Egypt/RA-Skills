import { execSync, spawn } from "child_process";
import path from "path";
import fs from "fs";
import puppeteer from "puppeteer";
const CDP_PORT = 9223;
const IAMGE_PATH = path.join(process.env.HOME || "~", "/openclaw-skill-data/desktop-oprator/");
const IMAGE_PREFIX = "desktop_operator_skill_";
function getArg(name) {
    const index = process.argv.indexOf(name);
    return index > -1 ? process.argv[index + 1] : null;
}
function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}
function findElectronExecutable(appName) {
    const appPath = `/Applications/${appName}.app`;
    if (!fs.existsSync(appPath)) {
        throw new Error(`应用不存在: ${appPath}`);
    }
    const macOSDir = path.join(appPath, "Contents", "MacOS");
    const files = fs.readdirSync(macOSDir);
    if (files.length === 0) {
        throw new Error(`找不到可执行文件: ${macOSDir}`);
    }
    return path.join(macOSDir, files[0]);
}
async function connectCDP() {
    for (let i = 0; i < 20; i++) {
        try {
            const browser = await puppeteer.connect({
                browserURL: `http://127.0.0.1:${CDP_PORT}`,
                defaultViewport: null,
            });
            return browser;
        }
        catch {
            await sleep(1000);
        }
    }
    throw new Error(`无法连接 CDP，端口 ${CDP_PORT} 超时`);
}
async function findPageWithTarget(browser, target) {
    const pages = await browser.pages();
    for (const page of pages) {
        try {
            const found = await page.evaluate((text) => {
                const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
                let node;
                while ((node = walker.nextNode())) {
                    if (node.textContent?.includes(text))
                        return true;
                }
                return false;
            }, target);
            if (found)
                return page;
        }
        catch {
            continue;
        }
    }
    return pages[0] ?? null;
}
async function clickTarget(page, target) {
    const clicked = await page.evaluate((text) => {
        function isVisible(el) {
            const rect = el.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0)
                return false;
            const style = window.getComputedStyle(el);
            return style.display !== "none" && style.visibility !== "hidden" && style.opacity !== "0";
        }
        const allElements = Array.from(document.querySelectorAll("*"));
        for (const el of allElements) {
            if (!isVisible(el))
                continue;
            const children = Array.from(el.childNodes);
            const hasDirectText = children.some(n => n.nodeType === Node.TEXT_NODE && n.textContent?.includes(text));
            if (hasDirectText) {
                el.click();
                return true;
            }
        }
        return false;
    }, target);
    if (!clicked) {
        throw new Error(`未找到包含文本 "${target}" 的可见元素`);
    }
}
async function takeScreenshot() {
    // 确保目录存在
    if (!fs.existsSync(IAMGE_PATH)) {
        try {
            fs.mkdirSync(IAMGE_PATH, { recursive: true });
            console.log(`已创建截图目录: ${IAMGE_PATH}`);
        }
        catch (error) {
            throw new Error(`创建截图目录失败: ${error.message}`);
        }
    }
    // 检查目录写入权限
    try {
        fs.accessSync(IAMGE_PATH, fs.constants.W_OK);
    }
    catch (error) {
        throw new Error(`截图目录无写入权限: ${IAMGE_PATH}`);
    }
    const screenshot = `${IAMGE_PATH}${IMAGE_PREFIX}${Date.now()}.png`;
    try {
        execSync(`/usr/sbin/screencapture -x ${screenshot}`);
    }
    catch (error) {
        throw new Error(`截图失败: ${error.message}`);
    }
    // 验证截图文件是否成功创建
    if (!fs.existsSync(screenshot)) {
        throw new Error(`截图文件未成功创建: ${screenshot}`);
    }
    return screenshot;
}
async function main() {
    const appName = getArg("--app");
    const target = getArg("--target");
    if (!appName || !target) {
        console.error("Missing parameters: --app and --target are required");
        process.exit(1);
    }
    console.log("查找应用:", appName);
    const execPath = findElectronExecutable(appName);
    console.log("可执行文件:", execPath);
    console.log("启动应用并开启 CDP...");
    const child = spawn(execPath, [`--remote-debugging-port=${CDP_PORT}`], {
        detached: true,
        stdio: "ignore",
    });
    child.unref();
    console.log("等待应用启动...");
    await sleep(4000);
    console.log("连接 CDP...");
    const browser = await connectCDP();
    console.log("CDP 连接成功");
    await sleep(2000);
    console.log("查找目标文本:", target);
    const page = await findPageWithTarget(browser, target);
    if (!page) {
        throw new Error("未找到任何可用页面");
    }
    console.log("点击目标元素...");
    await clickTarget(page, target);
    console.log("点击成功");
    console.log("等待页面渲染...");
    await sleep(3000);
    try {
        await page.waitForNetworkIdle({ timeout: 5000 });
    }
    catch {
        // 超时则继续截图
    }
    console.log("截图...");
    const screenshot = await takeScreenshot();
    console.log(JSON.stringify({ screenshot }));
    await browser.close();
    console.log("退出应用:", appName);
    try {
        execSync(`pkill -f "${appName}"`, { stdio: "ignore" });
    }
    catch {
        // 进程已退出则忽略
    }
    process.exit(0);
}
main().catch(err => {
    console.error("执行失败:", err.message);
    process.exit(1);
});
//# sourceMappingURL=index.js.map