"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectNavigator = void 0;
const promises_1 = require("node:fs/promises");
const path_1 = __importDefault(require("path"));
const fs_1 = require("../common/fs");
class ProjectNavigator {
    constructor(idfPath) {
        this.idfPath = idfPath;
    }
    /**
     * 语义化搜索：根据关键词在 examples 目录中寻找匹配项
     */
    async findExamples(query) {
        const examplesDir = path_1.default.join(this.idfPath, 'examples');
        // 高规格做法：使用 find 或 grep 命令快速定位包含关键词的目录
        // 也可以遍历目录层级，这里展示逻辑核心
        const results = [];
        try {
            // 简单的递归搜索包含 query 的文件夹名
            const walk = async (dir) => {
                const files = await (0, promises_1.readdir)(dir);
                for (const file of files) {
                    const fullPath = path_1.default.join(dir, file);
                    const fileStat = await (0, promises_1.stat)(fullPath);
                    if (fileStat.isDirectory()) {
                        // 如果文件夹名字匹配，或者包含 CMakeLists.txt (说明是工程)
                        if (file.toLowerCase().includes(query.toLowerCase())) {
                            if (await (0, fs_1.pathExists)(path_1.default.join(fullPath, 'CMakeLists.txt'))) {
                                results.push(fullPath);
                            }
                        }
                        // 限制搜索深度，防止递归过深
                        if (results.length < 5)
                            await walk(fullPath);
                    }
                }
            };
            await walk(examplesDir);
            return results;
        }
        catch (e) {
            console.error("搜索示例失败:", e);
            return [];
        }
    }
    /**
     * 核心逻辑：获取模块深度信息 (README 优先)
     */
    async getModuleDetails(modulePath) {
        const readmePath = await this.findReadme(modulePath);
        let description = "未找到 README 说明。";
        let hardware = [];
        if (readmePath) {
            const content = await (0, promises_1.readFile)(readmePath, 'utf-8');
            description = this.extractSummary(content);
            hardware = this.extractHardwareInfo(content);
        }
        const tree = await this.generateConciseTree(modulePath);
        return {
            name: path_1.default.basename(modulePath),
            path: modulePath,
            description,
            hardwareRequirements: hardware,
            treeStructure: tree
        };
    }
    /**
     * 寻找 README，支持中英文优先级
     */
    async findReadme(dir) {
        const files = ['README_CN.md', 'README_cn.md', 'README.md'];
        for (const f of files) {
            const p = path_1.default.join(dir, f);
            if (await (0, fs_1.pathExists)(p))
                return p;
        }
        return null;
    }
    /**
     * 提取 README 中的功能摘要 (通常是第一段)
     */
    extractSummary(content) {
        // 简单逻辑：取第一个非标题段落
        const lines = content.split('\n').filter(l => l.trim().length > 0 && !l.startsWith('#'));
        return lines[0] ? lines[0].slice(0, 200) + '...' : "暂无摘要";
    }
    /**
     * 提取硬件依赖 (寻找 "Hardware Required" 或 "硬件需求" 关键字)
     */
    extractHardwareInfo(content) {
        const regex = /(?:Hardware Required|硬件需求|所需硬件)[\s\S]*?(?=\n#|$)/i;
        const match = content.match(regex);
        if (match) {
            return match[0].split('\n').slice(1, 5).map(l => l.replace(/[*->]/g, '').trim());
        }
        return ["通用 ESP32 开发板"];
    }
    /**
     * 生成精简目录树 (深度为2)
     */
    async generateConciseTree(dir) {
        let tree = `${path_1.default.basename(dir)}/\n`;
        const files = await (0, promises_1.readdir)(dir);
        for (const file of files) {
            if (file.startsWith('.'))
                continue; // 跳过隐藏文件
            const fullPath = path_1.default.join(dir, file);
            const fileStat = await (0, promises_1.stat)(fullPath);
            if (fileStat.isDirectory()) {
                tree += `├── ${file}/\n`;
                // 只看 main 目录里面
                if (file === 'main') {
                    const subFiles = await (0, promises_1.readdir)(fullPath);
                    subFiles.forEach(sf => tree += `│   ├── ${sf}\n`);
                }
            }
            else {
                // 只列出核心构建文件
                if (['CMakeLists.txt', 'Makefile', 'Kconfig'].includes(file)) {
                    tree += `├── ${file}\n`;
                }
            }
        }
        return tree;
    }
}
exports.ProjectNavigator = ProjectNavigator;
//# sourceMappingURL=ProjectNavigator.js.map